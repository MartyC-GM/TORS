# PO Expected Receipt Date to SO Expected Ship Date

When someone puts an Expected Receipt Date on a PO line, every backordered sales order
line for that same item gets its Expected Ship Date set to match. If more than one open PO
has the item coming, the SO gets the earliest date.

About an hour after a sales order's ship dates change, the customer gets
"1. Order Update Email Template" with their Order Status Update link. If the dates change
again inside that hour, the clock restarts, so they get one email covering everything
instead of a pile of them.

Only lines that are actually backordered get touched. Lines with stock committed, closed
lines, and closed/billed orders are left alone. If there's no open PO for the item, the SO
line keeps whatever date it already has.

## Files

- `tors_mr_po_eta_to_so.js` does the work (Map/Reduce).
- `tors_ue_po_eta_to_so.js` watches POs and fires the Map/Reduce right after a save (User Event).
- `tors_ss_eta_email.js` sends the customer email once the hour is up (Scheduled).

## Setup in NetSuite

1. **Custom field** (Customization > Lists, Records, & Fields > Transaction Body Fields > New)
   - Label "ETA Email Due", ID `_tors_eta_email_due`, Type Free-Form Text.
   - Applies To: Sale. Display tab: Display Type = Hidden. Store Value checked.
   - It holds the time the customer email is due. Blank means nothing is waiting.
2. Upload all three files to the File Cabinet under `SuiteScripts/TORS/`.
3. **Map/Reduce script**
   - Customization > Scripting > Scripts > New, pick `tors_mr_po_eta_to_so.js`.
   - ID: `_tors_mr_po_eta_to_so`
   - Parameters tab: add `_tors_eta_items`, type Long Text, label "Item IDs", and
     `_tors_eta_notify`, type Check Box, label "Email Customers".
   - Deployments (all Status = Released, Log Level = Audit, Email Customers checked):
     - `_tors_mr_po_eta_to_so_1` and `_tors_mr_po_eta_to_so_2`, Not Scheduled. These are
       what the PO save fires. Two of them means two POs saved back to back both run.
     - `_tors_mr_po_eta_to_so_nightly`, Daily at 2:00 AM, parameter blank. Safety net that
       catches anything missed (both deployments busy, inline edits, etc.).
4. **User Event script**
   - New script, pick `tors_ue_po_eta_to_so.js`, ID `_tors_ue_po_eta_to_so`.
   - Deploy to Purchase Order, Status = Released, Event Type blank (runs on create, edit,
     and inline edit), Execute As Role = Administrator.
5. **Scheduled script** (the customer email)
   - New script, pick `tors_ss_eta_email.js`, ID `_tors_ss_eta_email`.
   - Parameters: `_tors_eta_email_template` (Integer, label "Email Template ID") and
     `_tors_eta_email_author` (List/Record > Employee, label "Default Sender").
   - Deploy: Status = Released, Daily, Repeat every 15 minutes, Template ID = `20`,
     Default Sender = whoever should send when an order has no sales rep.
   - Email comes from the sales rep on the order. It goes to the email on the sales
     order, or the customer's email if the order doesn't have one, and lands on the
     order's Communication tab.

**Heads up on the first run:** right now about 150 open orders would get new ship dates,
which means about 150 customer emails an hour later. If you don't want that blast, uncheck
Email Customers on the nightly deployment for its first run, then check it again the next
morning.

Updates usually land on the sales orders within a minute or two of saving the PO. The
customer email goes out 60 to 75 minutes after the last change (the script checks every
15 minutes). Results show up in each script's Execution Log.

## Turn it on slowly

1. Set every deployment to **Status = Testing** at first. In Testing, the PO script only
   fires when the script owner saves a PO, so nobody else's work kicks it off.
2. Leave **Email Customers unchecked** on all three Map/Reduce deployments, and leave the
   email script's deployment at Testing with no schedule.
3. Save a PO or two yourself and check the sales orders. When the dates look right, set
   the Map/Reduce and PO deployments to Released.
4. When you're ready for emails, check Email Customers and release the email script.

## Undo it

Fastest off switch (stops everything in under a minute, nothing gets deleted):

| What to stop | Where | Change |
| --- | --- | --- |
| Ship date updates from PO saves | The PO script's deployment (`_tors_ue_po_eta_to_so`) | Status = Not Scheduled, or check Inactive |
| Nightly ship date sweep | The `_tors_mr_po_eta_to_so_nightly` deployment | Status = Not Scheduled |
| Customer emails | The `_tors_ss_eta_email` deployment | Status = Not Scheduled |
| Customer emails only (keep dates updating) | All Map/Reduce deployments | Uncheck Email Customers |

Turn it back on by setting the same deployments back to Released.

What stays after you turn it off:
- **Ship dates already changed stay changed.** Every change shows in the sales order's
  System Information > System Notes, which should show the old and new date, so a bad batch can be fixed
  by hand or with a CSV import.
- **Emails already sent can't be unsent.** Each one is logged on the order's Communication tab.
- Orders waiting on an email keep a time in the hidden ETA Email Due field. With the email
  script off, nothing happens with it.

To remove it for good: set the deployments to Not Scheduled, delete the three script records
(deployments go with them), delete the three files from the File Cabinet, then delete the
ETA Email Due field.

## Test it

Pick a backordered SO line, find an open PO for that item, change the PO line's Expected
Receipt Date, save, wait a minute, and check the SO line's Expected Ship Date. For the email,
try it first on an order for a test customer with your own email address, then make sure the
Order Status Update button shows up with the customer's link.
