# Late Order Notice (NetSuite to HubSpot)

Every weekday morning this finds open sales orders that are running late and:

1. **Emails the customer from their salesperson.** HubSpot sends it from the rep's own connected inbox through a one-step sequence, so it reads as a personal note from the rep. It tells them what's late and the new date, and asks: *does this date work, or do you need it sooner?*
2. **Notifies the rep when the customer replies.** HubSpot sequences stop on a reply and alert the sender. The reply also lands in the rep's own inbox.
3. **Tells the rep to call** when the late order is over $1,000 or the customer is new (first purchase in the last 90 days). This creates a high-priority HubSpot **Call** task for the rep, due today.
4. **Marks the order** with the date the notice went out, so the customer isn't emailed again for 7 days.

**Late** means an unshipped item line whose expected ship date (or the order's ship date) has passed, or an order still not shipped 5+ days after it was entered. House accounts (Sales Rep = TORS, TORS Online or blank) are skipped and stay with customer service.

On 10/23/2026 that rule matched 270 open orders: 64 over $1,000, and 94 on house accounts. To keep the first runs from flooding customers, the script **starts in dry-run mode** and **sends no more than 25 a day** (biggest orders first) until you raise the cap.

## Setup

### HubSpot (once)

1. **Contact properties** (Settings > Properties > Contact, group "TORS Orders"). All are single-line text:
   - `tors_late_order_number` (Late order number)
   - `tors_late_order_po` (Late order PO)
   - `tors_late_order_items` (Late order items)
   - `tors_late_order_new_date` (Late order new date)
2. **Sequence** named "Late Order Update" with one **automated email** step (send right away). Use the copy in `hubspot/late-order-update-email.md`. Sequence settings: stop on reply (default), send on business days. Note the sequence ID from its URL.
3. **Each rep** (Marty, Janevea, Daro, Darion, Anson) needs a Sales Hub seat and their inbox connected in HubSpot (Settings > General > Email). Your account has Sales Pro seats. Check that each rep has one assigned.
4. **Private app** (Settings > Integrations > Private Apps) named "NetSuite Late Orders" with scopes:
   - `crm.objects.contacts.read`, `crm.objects.contacts.write`
   - `crm.objects.owners.read`
   - `automation.sequences.read`, `automation.sequences.enrollments.write`
   - `crm.objects.tasks.write` (some portals list task access under contacts write)

   Copy the access token.

### NetSuite (once)

1. **API Secret:** Setup > Company > API Secrets > New. ID `custsecret_tors_hubspot_token`, paste the HubSpot token, restrict to domain `api.hubapi.com` and to this script.
2. **Custom field:** Customization > Lists, Records & Fields > Transaction Body Fields > New.
   - Label "Late Notice Sent", ID `custbody_tors_late_notice_dt`, type Date, applies to Sale (Sales Order)
   - Display on a subtab, not mandatory
3. **Upload the script:** put `tors_mr_late_order_notice.js` in File Cabinet > SuiteScripts > TORS.
4. **Script record:** Customization > Scripting > Scripts > New, and pick the file. Add these parameters:

   | ID | Type | Default |
   |---|---|---|
   | `custscript_tors_lon_dryrun` | Check Box | Checked |
   | `custscript_tors_lon_sequence_id` | Free-Form Text | the HubSpot sequence ID |
   | `custscript_tors_lon_max` | Integer | 25 |
   | `custscript_tors_lon_resend_days` | Integer | 7 |
   | `custscript_tors_lon_summary_to` | List/Record (Employee) | Marty |

5. **Deployment:** status Testing first, then Scheduled, every weekday at 6:30 AM Pacific, Execute As Administrator.

## Testing (do this before it goes live)

1. Leave **dry run checked** and run the deployment once (Save and Execute). Nothing is sent. The execution log and Marty's summary email list every order it *would* email and every call task it *would* create. Check that the reps, emails and dates look right.
2. Pick one friendly customer, or set a test order's customer email to your own. Uncheck dry run, set max to 1, and run it. Confirm:
   - the email arrives from the rep's address, with the right items and date
   - replying notifies the rep in HubSpot
   - a $1,000+ test order creates a Call task for the rep
   - the order's "Late Notice Sent" field shows today
3. Raise max to 25 and schedule it. Raise the cap as the backlog clears.

## Notes

- If a contact is already enrolled in another sequence, HubSpot won't enroll them again. The script then creates a task for the rep to send the update by hand, so nothing falls through.
- New contacts are created in HubSpot when the customer's email isn't there yet, owned by the rep.
- The rep comes from the customer's Sales Rep in NetSuite. Getting customers off TORS (the morning assignment task) means more late orders get a personal note.
