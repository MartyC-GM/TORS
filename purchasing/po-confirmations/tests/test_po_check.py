import copy
import json
import sys
import unittest
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import po_check  # noqa: E402

CONFIG = json.loads((HERE.parent / "config.json").read_text())
TODAY = date(2026, 10, 20)


def load(name):
    return json.loads((HERE / "fixtures" / name).read_text())


def run(data):
    return po_check.check(data["po"], data["confirmation"], CONFIG, TODAY)


class RealConfirmations(unittest.TestCase):
    """Built from actual confirmations that hit purchasing@ on 10/19 and 10/20/2026."""

    def test_sealtech_35247_clean(self):
        r = run(load("po35247_sealtech_clean.json"))
        self.assertEqual(r["verdict"], "confirmed")
        self.assertTrue(r["check_ship_dates_confirmed"])
        self.assertEqual(r["netsuite_update"]["body"], {"custbody23": True, "custbody20": "2026-10-20"})
        self.assertEqual(r["netsuite_update"]["line_updates"], [])
        self.assertIsNone(r["email"])

    def test_sealtech_35248_price_change_blocks(self):
        r = run(load("po35248_sealtech_price_change.json"))
        self.assertEqual(r["verdict"], "mismatch")
        self.assertIsNone(r["netsuite_update"])
        self.assertEqual(len(r["problems"]), 2)
        self.assertIn("B70041", r["problems"][1])
        self.assertIn("$0.0308", r["problems"][1])
        self.assertIn("didn't match", r["email"]["body"])

    def test_freudenberg_35246_surcharge_and_date(self):
        r = run(load("po35246_freudenberg_surcharge.json"))
        self.assertEqual(r["verdict"], "changes")
        self.assertTrue(r["check_ship_dates_confirmed"])
        self.assertEqual(r["netsuite_update"]["line_updates"][0]["new_expected_receipt_date"], "2026-10-23")
        self.assertTrue(any("Customs Surcharge $1.85" in c for c in r["changes"]))

    def test_eagle_35219_matches_on_vendor_part_number(self):
        r = run(load("po35219_eagle_vendor_parts.json"))
        self.assertEqual(r["verdict"], "confirmed")
        self.assertEqual(r["netsuite_update"]["line_updates"], [])


class Rules(unittest.TestCase):
    def setUp(self):
        self.data = copy.deepcopy(load("po35247_sealtech_clean.json"))
        self.po = self.data["po"]
        self.conf = self.data["confirmation"]

    def test_short_quantity(self):
        self.conf["lines"][1]["qty"] = 1500
        r = run(self.data)
        self.assertEqual(r["verdict"], "mismatch")
        self.assertIn("qty ordered 2000, vendor confirmed 1500", r["problems"][0])

    def test_missing_line(self):
        del self.conf["lines"][2]
        r = run(self.data)
        self.assertEqual(r["verdict"], "mismatch")
        self.assertIn("E70247: on the PO but missing", r["problems"][0])

    def test_extra_line(self):
        self.conf["lines"].append({"our_part": "B70010", "qty": 100, "unit_price": 1, "price_per": 100, "date": "10/20/26"})
        r = run(self.data)
        self.assertEqual(r["verdict"], "mismatch")
        self.assertIn("B70010: on the confirmation but not on the PO", r["problems"][0])

    def test_wrong_ship_method(self):
        self.conf["ship_via"] = "UPS GROUND"
        r = run(self.data)
        self.assertEqual(r["verdict"], "mismatch")
        self.assertIn("Ship method", r["problems"][0])

    def test_unknown_ship_method(self):
        self.conf["ship_via"] = "ZZTOP"
        r = run(self.data)
        self.assertEqual(r["verdict"], "mismatch")
        self.assertIn("Couldn't tell", r["problems"][0])

    def test_wrong_po_number(self):
        self.conf["po_number"] = "35248"
        self.assertEqual(run(self.data)["verdict"], "mismatch")

    def test_late_updates_dates_but_leaves_box_unchecked(self):
        for l in self.conf["lines"]:
            l["date"] = "11/10/26"
        r = run(self.data)
        self.assertEqual(r["verdict"], "late")
        self.assertFalse(r["check_ship_dates_confirmed"])
        self.assertNotIn("custbody23", r["netsuite_update"]["body"])
        self.assertEqual(len(r["netsuite_update"]["line_updates"]), 6)
        self.assertEqual(r["netsuite_update"]["line_updates"][0]["new_expected_receipt_date"], "2026-11-11")

    def test_small_slip_is_a_change_not_late(self):
        self.conf["lines"][0]["date"] = "10/21/26"
        r = run(self.data)
        self.assertEqual(r["verdict"], "changes")
        self.assertTrue(r["check_ship_dates_confirmed"])

    def test_missing_date(self):
        self.conf["lines"][0]["date"] = "TBD"
        self.assertEqual(run(self.data)["verdict"], "mismatch")

    def test_split_shipment_sums_qty_and_uses_latest_date(self):
        first = self.conf["lines"][4]
        second = dict(first, qty=383, date="10/21/26")
        first["qty"] = 4000
        self.conf["lines"].append(second)
        r = run(self.data)
        self.assertEqual(r["verdict"], "changes")
        upd = r["netsuite_update"]["line_updates"]
        self.assertEqual(upd[0]["line"], 5)
        self.assertEqual(upd[0]["new_expected_receipt_date"], "2026-10-22")

    def test_closed_line_not_required(self):
        self.po["lines"][2]["closed"] = True
        del self.conf["lines"][2]
        self.assertEqual(run(self.data)["verdict"], "confirmed")

    def test_partially_received_line_compares_remaining_qty(self):
        self.po["lines"][1]["qty_remaining"] = 500
        self.conf["lines"][1]["qty"] = 500
        self.assertEqual(run(self.data)["verdict"], "confirmed")

    def test_higher_price_blocks(self):
        self.conf["lines"][4]["unit_price"] = 19.21
        r = run(self.data)
        self.assertEqual(r["verdict"], "mismatch")
        self.assertIn("higher", r["problems"][0])

    def test_arrival_date_vendor(self):
        cfg = copy.deepcopy(CONFIG)
        cfg["vendor_overrides"]["21"]["date_means"] = "arrival"
        for l in self.conf["lines"]:
            l["date"] = "10/21/26"
        r = po_check.check(self.po, self.conf, cfg, TODAY)
        self.assertEqual(r["verdict"], "confirmed")

    def test_charges_can_block(self):
        cfg = copy.deepcopy(CONFIG)
        cfg["extra_charges_block"] = True
        self.conf["charges"] = [{"description": "Tariff", "amount": 12}]
        self.assertEqual(po_check.check(self.po, self.conf, cfg, TODAY)["verdict"], "mismatch")


class DateOnlyAndRows(unittest.TestCase):
    def test_date_only_confirmation_needs_a_person(self):
        data = load("po35247_sealtech_clean.json")
        data["confirmation"]["date_only"] = "Delivery: Nov 15th"
        r = run(data)
        self.assertEqual(r["verdict"], "mismatch")
        self.assertIn("only sent a date", r["problems"][0])

    def test_po_from_suiteql_rows(self):
        rows = [
            {"id": 14699851, "tranid": "35248", "vendor_id": 21, "vendor_name": "VN01 Seal and Rubber Technologies",
             "ship_method": "FedEx Ground®", "custbody23": "F", "status": "B", "line": 1, "line_id": 1,
             "item": "V75014", "vendor_code": "V500-75/2-014", "qty": 20000, "qty_received": 5000,
             "isclosed": "F", "rate": 0.0194, "expectedreceiptdate": "10/26/2026"},
        ]
        po = po_check.po_from_suiteql(rows)
        self.assertFalse(po["ship_dates_confirmed"])
        self.assertFalse(po["status_closed"])
        self.assertEqual(po["lines"][0]["qty_remaining"], 15000)
        rows[0]["status"] = "H"
        self.assertTrue(po_check.po_from_suiteql(rows)["status_closed"])


class Helpers(unittest.TestCase):
    def test_parse_dates(self):
        for s in ("2026-12-01", "12/1/2026", "12/01/26", "1-Dec-2026"):
            self.assertEqual(po_check.parse_date(s), date(2026, 12, 1), s)
        self.assertIsNone(po_check.parse_date("TBD"))

    def test_business_days_skip_weekend_and_thanksgiving(self):
        self.assertEqual(po_check.add_business_days(date(2026, 10, 23), 1), date(2026, 10, 26))
        self.assertEqual(po_check.add_business_days(date(2026, 11, 25), 1), date(2026, 11, 27))

    def test_ship_method_aliases(self):
        r = lambda t: po_check.resolve_ship_method(t, CONFIG)
        self.assertEqual(r("FX1D"), "FedEx Priority Overnight®")
        self.assertEqual(r("FXGD"), "FedEx Ground®")
        self.assertEqual(r("UPS/GROUND/COLL"), "UPS® Ground")
        self.assertEqual(r("UPS 2 DAY AIR"), "UPS 2nd Day Air®")
        self.assertEqual(r("UPS Next Day Air Saver"), "UPS Next Day Air Saver®")
        self.assertIsNone(r("ZZTOP"))


if __name__ == "__main__":
    unittest.main()
