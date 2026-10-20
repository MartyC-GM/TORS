# PO Confirmation Checker

Watches purchasing@theoringstore.com for vendor order confirmations, checks each
one against our purchase order in NetSuite, and does the busywork when it all lines up.

## What it does

For every new email in purchasing@:

1. Figures out if it's a vendor confirming one of our POs. Invoices, packing
   slips, tracking, and sales pitches get skipped.
2. Reads the confirmation (email body and PDF) and pulls the PO from NetSuite.
3. Checks every line:
   - **Parts**: every PO line is on the confirmation, nothing extra. Matches on
     our part number, or the vendor's part number from the item's vendor list.
   - **Quantities**: exact. Split shipments get added up.
   - **Pricing**: per piece, after converting per-100 (C) and per-1000 (M)
     pricing. OK if it's just 4th-decimal rounding or the whole line is off by 50 cents or less.
   - **Ship method**: FX1D, FXGD, UPS/GROUND/COLL and so on get matched to the PO's ship method.
   - **Dates**: vendor ship date plus transit days (by ship method, skipping
     weekends and carrier holidays) = Expected Receipt Date.
   - **Extras**: surcharges, tariffs, and vendor notes get reported.
4. Acts on it:

| Result | NetSuite | Purchasing gets |
|---|---|---|
| All good, nothing changed | Fixes due dates, checks **Ship Dates Confirmed**, sets Expected Ship Date | nothing |
| All good, but something changed (date moved a day or two, surcharge, vendor note) | Same as above | "PO X confirmed, a few changes" |
| Dates pushed out more than 2 business days | Fixes due dates, box stays **unchecked** | "PO X confirmed but running late" |
| Price, qty, part, ship method, or missing date doesn't match | **Nothing touched** | "Hey, PO X didn't match" with exactly what's off |

It never changes price, quantity, items, vendor, or ship method, and never emails vendors.

## Files

- `config.json` holds the knobs: tolerances, transit days per ship method, ship method
  nicknames vendors use, per-vendor overrides, and the NetSuite field ids.
- `po_check.py` is the referee. Same input, same answer every time. Doesn't
  touch NetSuite or email, just decides.
- `RUNBOOK.md` is the step-by-step the scheduled job follows (and a person can too).
- `tests/` has tests built from real confirmations from 10/19 to 10/20/2026
  (Seal Tech 35247 and 35248, Freudenberg 35246, Eagle 35219).

Run the tests: `python3 -m unittest discover -s purchasing/po-confirmations/tests`

## Tuning it

- **Vendor uses a ship code we haven't seen**: add it to that ship method's `aliases`.
- **Transit time is off for a vendor**: add `transit_days` under that vendor's
  id in `vendor_overrides`, like `"1502": {"transit_days": {"UPS® Ground": 5}}`.
- **Vendor's date is when it arrives, not when it ships**: set `"date_means": "arrival"` for that vendor.
- **Surcharges should hold up the confirmation**: set `extra_charges_block` to `true`.
- **Late threshold**: `late_tolerance_business_days` (default 2).

## Where the record lives

Every email it handles gets a line in Marty's OneDrive:
`PO Confirmation Checker/processed-log-<YEAR>.json` (message, PO, verdict, time).
That's how it knows not to handle the same email twice, and it doubles as an
audit trail for ISO 9001.
