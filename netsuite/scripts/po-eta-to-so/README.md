# PO Expected Receipt Date to SO Expected Ship Date

When someone puts an Expected Receipt Date on a PO line, every backordered sales order
line for that same item gets its Expected Ship Date set to match. If more than one open PO
has the item coming, the SO gets the earliest date.

Only lines that are actually backordered get touched. Lines with stock committed, closed
lines, and closed/billed orders are left alone. If there's no open PO for the item, the SO
line keeps whatever date it already has.

## Files

- `tors_mr_po_eta_to_so.js` does the work (Map/Reduce).
- `tors_ue_po_eta_to_so.js` watches POs and fires the Map/Reduce right after a save (User Event).

## Setup in NetSuite

1. Upload both files to the File Cabinet under `SuiteScripts/TORS/`.
2. **Map/Reduce script**
   - Customization > Scripting > Scripts > New, pick `tors_mr_po_eta_to_so.js`.
   - ID: `_tors_mr_po_eta_to_so`
   - Parameters tab: add `_tors_eta_items`, type Long Text, label "Item IDs".
   - Deployments (all Status = Released, Log Level = Audit):
     - `_tors_mr_po_eta_to_so_1` and `_tors_mr_po_eta_to_so_2`, Not Scheduled. These are
       what the PO save fires. Two of them means two POs saved back to back both run.
     - `_tors_mr_po_eta_to_so_nightly`, Daily at 2:00 AM, parameter blank. Safety net that
       catches anything missed (both deployments busy, inline edits, etc.).
3. **User Event script**
   - New script, pick `tors_ue_po_eta_to_so.js`, ID `_tors_ue_po_eta_to_so`.
   - Deploy to Purchase Order, Status = Released, Event Type blank (runs on create, edit,
     and inline edit), Execute As Role = Administrator.

Updates usually land on the sales orders within a minute or two of saving the PO.
Results show up in the Map/Reduce script's Execution Log.

## Test it

Pick a backordered SO line, find an open PO for that item, change the PO line's Expected
Receipt Date, save, wait a minute, and check the SO line's Expected Ship Date.
