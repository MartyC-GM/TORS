"""Compare a vendor's order confirmation against our NetSuite purchase order.

Usage:
    python3 po_check.py input.json [--config config.json] [--today YYYY-MM-DD]

input.json holds two objects, "po" (pulled from NetSuite) and "confirmation"
(read off the vendor's email/PDF). See README.md for the exact shape.

Prints a decision as JSON: the verdict, what to write back to NetSuite, and the
email to send purchasing (if any). This script never touches NetSuite or email
itself. It only decides, so the rules stay the same every run.
"""

import argparse
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent


# ---------- dates ----------

def parse_date(value):
    """Accept 2026-10-21, 10/21/2026, 10/21/26, 21-Oct-2026. Return date or None."""
    if not value:
        return None
    s = str(value).strip()
    m = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", s)
    if m:
        return date(int(m[1]), int(m[2]), int(m[3]))
    m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{2}|\d{4})", s)
    if m:
        year = int(m[3])
        if year < 100:
            year += 2000
        return date(year, int(m[1]), int(m[2]))
    m = re.fullmatch(r"(\d{1,2})-([A-Za-z]{3})-(\d{4})", s)
    if m:
        months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
        mon = m[2].lower()
        if mon in months:
            return date(int(m[3]), months.index(mon) + 1, int(m[1]))
    return None


def _nth_weekday(year, month, weekday, n):
    d = date(year, month, 1)
    d += timedelta(days=(weekday - d.weekday()) % 7)
    return d + timedelta(weeks=n - 1)


def _last_weekday(year, month, weekday):
    d = date(year + (month == 12), month % 12 + 1, 1) - timedelta(days=1)
    return d - timedelta(days=(d.weekday() - weekday) % 7)


def carrier_holidays(year):
    """Days UPS and FedEx don't move ground or air packages."""
    return {
        date(year, 1, 1),
        _last_weekday(year, 5, 0),       # Memorial Day
        date(year, 7, 4),
        _nth_weekday(year, 9, 0, 1),     # Labor Day
        _nth_weekday(year, 11, 3, 4),    # Thanksgiving
        date(year, 12, 25),
    }


def add_business_days(start, days):
    d = start
    added = 0
    while added < days:
        d += timedelta(days=1)
        if d.weekday() < 5 and d not in carrier_holidays(d.year):
            added += 1
    return d


def business_days_between(a, b):
    """Business days from a to b (negative if b is before a)."""
    if a == b:
        return 0
    sign = 1 if b > a else -1
    lo, hi = (a, b) if b > a else (b, a)
    count = 0
    d = lo
    while d < hi:
        d += timedelta(days=1)
        if d.weekday() < 5 and d not in carrier_holidays(d.year):
            count += 1
    return sign * count


def fmt(d):
    return d.strftime("%m/%d/%Y") if d else "none"


# ---------- matching helpers ----------

def norm(text):
    return re.sub(r"[^A-Z0-9]", "", str(text or "").upper())


def resolve_ship_method(text, config):
    """Turn whatever the vendor printed (FX1D, UPS/GROUND/COLL) into a NetSuite ship method name."""
    if not text:
        return None
    t = norm(text)
    best = None
    for name, info in config["ship_methods"].items():
        for alias in [name] + info.get("aliases", []):
            a = norm(alias)
            if a and (t == a or a in t):
                # longest alias wins so "UPS NEXT DAY AIR SAVER" beats "UPS NEXT DAY AIR"
                if best is None or len(a) > best[1]:
                    best = (name, len(a))
    return best[0] if best else None


def transit_days(ship_method, vendor_id, config):
    override = config.get("vendor_overrides", {}).get(str(vendor_id), {})
    by_vendor = override.get("transit_days", {})
    if ship_method in by_vendor:
        return by_vendor[ship_method]
    info = config["ship_methods"].get(ship_method)
    return info["transit_days"] if info else None


def money(x):
    return f"${x:,.2f}"


def per_piece(x):
    return f"${x:,.4f}"


# ---------- NetSuite rows -> PO ----------

CLOSED_PO_STATUSES = {"C", "F", "G", "H"}  # rejected, pending bill, fully billed, closed


def po_from_suiteql(rows):
    """Build the "po" object from the SuiteQL rows in RUNBOOK.md (one row per PO line)."""
    if not rows:
        raise ValueError("no PO rows")
    head = rows[0]
    lines = []
    for r in rows:
        qty = float(r["qty"])
        received = float(r.get("qty_received") or 0)
        lines.append({
            "line": r["line"],
            "line_id": r.get("line_id"),
            "item": r["item"],
            "vendor_code": r.get("vendor_code"),
            "qty": qty,
            "qty_remaining": qty - received,
            "rate": float(r["rate"]),
            "expected_receipt_date": r.get("expectedreceiptdate"),
            "closed": r.get("isclosed") == "T",
        })
    return {
        "id": head["id"],
        "tranid": head["tranid"],
        "vendor_id": head["vendor_id"],
        "vendor_name": head["vendor_name"],
        "ship_method": head.get("ship_method"),
        "ship_dates_confirmed": head.get("custbody23") == "T",
        "status_closed": head.get("status") in CLOSED_PO_STATUSES,
        "url": head.get("url"),
        "lines": lines,
    }


# ---------- the check ----------

def check(po, conf, config, today=None):
    today = today or date.today()
    problems = []   # anything here means "didn't match", nothing gets written
    changes = []    # worth telling purchasing, but OK to confirm
    late = []       # dates pushed out, update dates but leave the box unchecked

    vendor_id = str(po.get("vendor_id"))
    override = config.get("vendor_overrides", {}).get(vendor_id, {})
    date_means = override.get("date_means", "ship")
    tol = config["price_tolerance"]

    # Right PO, right vendor?
    if norm(conf.get("po_number")) != norm(po.get("tranid")):
        problems.append(f"Confirmation is for PO {conf.get('po_number')}, not PO {po.get('tranid')}.")
    if po.get("status_closed"):
        problems.append(f"PO {po.get('tranid')} is closed or fully received in NetSuite.")
    if conf.get("date_only"):
        problems.append(
            f"Vendor only sent a date ({conf.get('date_only')}), no prices or quantities to check. "
            "Someone needs to look at this one by hand."
        )

    # Ship method
    po_ship = po.get("ship_method")
    conf_ship = resolve_ship_method(conf.get("ship_via"), config)
    if conf.get("ship_via") and not conf_ship:
        problems.append(f"Couldn't tell what ship method \"{conf.get('ship_via')}\" is. PO says {po_ship or 'nothing'}.")
    elif conf_ship and po_ship and conf_ship != po_ship:
        problems.append(f"Ship method: PO says {po_ship}, vendor says {conf.get('ship_via')} ({conf_ship}).")
    elif not conf.get("ship_via"):
        changes.append(f"Vendor didn't list a ship method. PO says {po_ship or 'nothing'}.")
    ship_method = po_ship or conf_ship

    # Match confirmation lines to PO lines: our part number first, then the vendor's part number.
    open_lines = [l for l in po["lines"] if not l.get("closed") and float(l.get("qty_remaining", l["qty"])) > 0]
    matched = {id(l): [] for l in open_lines}
    extras = []
    for cl in conf.get("lines", []):
        target = None
        for key_conf, key_po in (("our_part", "item"), ("vendor_part", "vendor_code")):
            want = norm(cl.get(key_conf))
            if not want:
                continue
            candidates = [l for l in open_lines if norm(l.get(key_po)) == want]
            if candidates:
                # same item on the PO twice: fill the first one that isn't matched yet
                target = next((l for l in candidates if not matched[id(l)]), candidates[0])
                break
        if target is None:
            extras.append(cl)
        else:
            matched[id(target)].append(cl)

    for cl in extras:
        label = cl.get("our_part") or cl.get("vendor_part") or cl.get("description") or "unknown part"
        problems.append(f"{label}: on the confirmation but not on the PO (qty {cl.get('qty')}).")

    line_updates = []
    ship_dates = []
    for l in open_lines:
        cls = matched[id(l)]
        tag = f"Line {l['line']} {l['item']}"
        if not cls:
            problems.append(f"{tag}: on the PO but missing from the confirmation.")
            continue

        # Quantity (a split shipment shows up as the same part on more than one line)
        want_qty = float(l.get("qty_remaining", l["qty"]))
        got_qty = sum(float(c.get("qty") or 0) for c in cls)
        if abs(got_qty - want_qty) > 1e-9:
            problems.append(f"{tag}: qty ordered {want_qty:g}, vendor confirmed {got_qty:g}.")
        if len(cls) > 1:
            changes.append(f"{tag}: vendor split this into {len(cls)} shipments.")

        # Price, per piece, after converting per-100 / per-1000 pricing
        po_rate = float(l["rate"])
        for c in cls:
            if c.get("unit_price") is None:
                problems.append(f"{tag}: no price on the confirmation.")
                continue
            per = float(c.get("price_per") or 1)
            conf_rate = float(c["unit_price"]) / per
            diff = conf_rate - po_rate
            line_diff = diff * float(c.get("qty") or want_qty)
            if abs(diff) > tol["per_unit"] + 1e-9 and abs(line_diff) > tol["per_line_dollars"] + 1e-9:
                way = "higher" if diff > 0 else "lower"
                problems.append(
                    f"{tag}: price on PO {per_piece(po_rate)}/pc, vendor has {per_piece(conf_rate)}/pc "
                    f"({way}, {money(abs(line_diff))} on the line)."
                )

        # Dates
        dates = [parse_date(c.get("date")) for c in cls]
        if any(d is None for d in dates):
            problems.append(f"{tag}: no ship date on the confirmation.")
            continue
        vendor_date = max(dates)
        if date_means == "arrival":
            new_receipt = vendor_date
            ship_dates.append(vendor_date)
        else:
            days = transit_days(ship_method, vendor_id, config)
            if days is None:
                problems.append(f"{tag}: don't know transit time for {ship_method or 'no ship method'}.")
                continue
            new_receipt = add_business_days(vendor_date, days)
            ship_dates.append(vendor_date)
        if vendor_date < today and date_means != "arrival":
            changes.append(f"{tag}: vendor ship date {fmt(vendor_date)} is already in the past.")

        old_receipt = parse_date(l.get("expected_receipt_date"))
        if old_receipt != new_receipt:
            line_updates.append({
                "line": l["line"],
                "line_id": l.get("line_id"),
                "item": l["item"],
                "old_expected_receipt_date": fmt(old_receipt),
                "new_expected_receipt_date": new_receipt.isoformat(),
            })
            if old_receipt and business_days_between(old_receipt, new_receipt) > config["late_tolerance_business_days"]:
                late.append(f"{tag}: now due {fmt(new_receipt)}, we had {fmt(old_receipt)} "
                            f"({business_days_between(old_receipt, new_receipt)} business days late).")
            else:
                changes.append(f"{tag}: due date {fmt(old_receipt)} -> {fmt(new_receipt)}." if old_receipt
                               else f"{tag}: due date set to {fmt(new_receipt)}.")

    # Surcharges, tariffs, freight the PO doesn't have
    for ch in conf.get("charges", []) or []:
        msg = f"Extra charge on confirmation: {ch.get('description', 'charge')} {money(float(ch.get('amount') or 0))}."
        (problems if config.get("extra_charges_block") else changes).append(msg)

    for note in conf.get("notes", []) or []:
        changes.append(f"Vendor note: {note}")

    if po.get("ship_dates_confirmed"):
        changes.append("This PO was already marked Ship Dates Confirmed. Treated this as a revised confirmation.")

    # Verdict
    if problems:
        verdict = "mismatch"
    elif late:
        verdict = "late"
    elif changes:
        verdict = "changes"
    else:
        verdict = "confirmed"

    netsuite = None
    if verdict in ("confirmed", "changes", "late"):
        f = config["netsuite_fields"]
        body = {}
        if verdict != "late":
            body[f["ship_dates_confirmed"]] = True
        if ship_dates:
            body[f["expected_ship_date"]] = max(ship_dates).isoformat()
        netsuite = {"po_id": po.get("id"), "body": body, "line_updates": line_updates}

    return {
        "po": po.get("tranid"),
        "vendor": po.get("vendor_name"),
        "verdict": verdict,
        "check_ship_dates_confirmed": verdict in ("confirmed", "changes"),
        "netsuite_update": netsuite,
        "problems": problems,
        "late": late,
        "changes": changes,
        "email": build_email(po, conf, verdict, problems, late, changes),
    }


def build_email(po, conf, verdict, problems, late, changes):
    """Plain note to purchasing. No email when everything matched and nothing changed."""
    if verdict == "confirmed":
        return None
    po_no = po.get("tranid")
    vendor = po.get("vendor_name", "the vendor")
    link = po.get("url") or ""
    src = conf.get("email_subject") or "no subject line"
    if verdict == "mismatch":
        subject = f"PO {po_no} didn't match the vendor confirmation"
        lead = (f"Hey, PO {po_no} ({vendor}) didn't match the vendor's confirmation ({src}). "
                "Nothing was changed in NetSuite and Ship Dates Confirmed is still unchecked. "
                "Here's what's off:")
        items = problems + late
    elif verdict == "late":
        subject = f"PO {po_no} confirmed but running late"
        lead = (f"PO {po_no} ({vendor}) matches on parts, quantities, and price, but the vendor pushed dates out. "
                "I updated the due dates in NetSuite and left Ship Dates Confirmed unchecked so someone can decide "
                "if we need to expedite or let the customer know:")
        items = late
    else:
        subject = f"PO {po_no} confirmed, a few changes"
        lead = (f"PO {po_no} ({vendor}) checked out on parts, quantities, price, and ship method. "
                "I updated NetSuite and checked Ship Dates Confirmed. Heads up on these changes:")
        items = []
    other = [c for c in changes if c not in items]
    lines = [lead, ""] + [f"- {p}" for p in items]
    if other:
        lines += ["", "Other changes:" if items else ""] + [f"- {c}" for c in other]
    if link:
        lines += ["", f"PO in NetSuite: {link}"]
    lines += ["", "Sent by the PO confirmation checker."]
    text = "\n".join(l for l in lines if l is not None)
    return {"subject": subject, "body": re.sub(r"\n{3,}", "\n\n", text)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("input")
    ap.add_argument("--config", default=str(HERE / "config.json"))
    ap.add_argument("--today")
    args = ap.parse_args(argv)
    config = json.loads(Path(args.config).read_text())
    data = json.loads(Path(args.input).read_text())
    today = parse_date(args.today) if args.today else None
    po = data["po"] if "po" in data else po_from_suiteql(data["po_rows"])
    json.dump(check(po, data["confirmation"], config, today), sys.stdout, indent=2, ensure_ascii=False)
    print()


if __name__ == "__main__":
    main()
