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

The click-by-click version is in the TORS install checklist page. This is the short form.
Statuses: User Event scripts use Testing / Released. Map/Reduce and Scheduled scripts use
Not Scheduled / Scheduled.

Day one sets everything up in safe mode: only the script owner's PO saves trigger it, and no
customer emails go out.

1. **Custom field** (Customization > Lists, Records, & Fields > Transaction Body Fields > New)
   - Label "ETA Email Due", ID `_tors_eta_email_due`, Type Free-Form Text, Store Value checked.
   - Applies To: Sale. Display: Display Type = Hidden.
2. **Upload** `tors-po-eta-scripts.zip` into the File Cabinet's SuiteScripts folder with
   Advanced Add and the unzip box checked.
3. **Map/Reduce script** `tors_mr_po_eta_to_so.js`, ID `_tors_mr_po_eta_to_so`
   - Parameters: `_tors_eta_items` (Long Text, "Item IDs") and `_tors_eta_notify`
     (Check Box, "Email Customers").
   - Deployment A "PO ETA Sync 1": Not Scheduled. Deployment B "PO ETA Sync 2": Not Scheduled.
     Deployment C "PO ETA Sync Nightly": Not Scheduled for now, Daily at 2:00 am.
     Email Customers unchecked on all three.
4. **User Event script** `tors_ue_po_eta_to_so.js`, ID `_tors_ue_po_eta_to_so`
   - Deployment: Applies To Purchase Order, Status Testing, Execute As Role Administrator.
5. **Scheduled script** `tors_ss_eta_email.js`, ID `_tors_ss_eta_email`
   - Deployment: Not Scheduled for now, Daily, repeat every 15 minutes.
   - Uses template 20 ("1. Order Update Email Template"). Sends from the order's sales rep,
     or Sales Team if there isn't one, to the order's email (or the customer's).

## Go live

1. **Dates for everybody:** User Event deployment to Released, Nightly deployment to Scheduled.
   Let the nightly run go once. It catches up the roughly 150 orders already waiting, with
   no emails, because emails are still off.
2. **Emails:** check Email Customers on all three Map/Reduce deployments, and set the email
   script's deployment to Scheduled.

Updates usually land on the sales orders within a minute or two of saving the PO. The
customer email goes out 60 to 75 minutes after the last change. Results show in each
script's Execution Log.

## Undo it

Fastest off switch (stops it in under a minute, nothing gets deleted):

| What to stop | Deployment | Change |
| --- | --- | --- |
| Ship date updates from PO saves | User Event | Status = Testing, or check Inactive |
| Nightly ship date sweep | PO ETA Sync Nightly | Status = Not Scheduled |
| Customer emails | Email script | Status = Not Scheduled |
| Emails only, keep dates updating | All three Map/Reduce | Uncheck Email Customers |

Turn it back on by flipping the same settings back.

What stays after you turn it off:
- **Ship dates already changed stay changed.** System Notes on the sales order should show
  the old date, so a bad batch can be fixed by hand or with a CSV import.
- **Emails already sent can't be unsent.** Each one is on the order's Communication tab.
- Orders waiting on an email keep a time in the hidden ETA Email Due field. With the email
  script off, nothing happens with it.

To remove it for good: delete the three script records (deployments go with them), delete
the three files from SuiteScripts, then delete the ETA Email Due field.

## Test it

Pick a backordered SO line, find an open PO for that item, change the PO line's Expected
Receipt Date, save, wait a minute, and check the SO line's Expected Ship Date. For the email,
try it first on an order for a test customer with your own email address, then make sure the
Order Status Update button shows up with the customer's link.
