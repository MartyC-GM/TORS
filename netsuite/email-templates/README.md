# NetSuite Email Templates

## order-status-update.ftl

Send from the Customer record when a customer asks "where's my order?"

- **Name:** 2. B. Order Status Update
- **Record Type:** Entity (so it shows up when emailing from a Customer record)
- **Subject:** `Order Status Update for ${customer.companyName}`
- **Body:** paste `order-status-update.ftl` into the template's HTML source.

Uses `customer.custentity_tors_order_link`. If a customer has no link yet, the
email falls back to "we're pulling your status and will reply shortly" instead
of showing an empty button.

## so-confirmation.ftl

Replaces "2. A. SO Email Template" (Record Type: Transaction). The old version read the
link from `customer.custentity_tors_order_link`, but the `customer` object comes back
empty when you email from a sales order, so the button silently dropped out (SO #306632).

This version tries `customer.custentity_tors_order_link` first, then
`transaction.entity.custentity_tors_order_link`. If neither comes through, the section
still shows with "reply and we'll send your link" instead of disappearing.
No new fields needed. Paste into the HTML source of "2. A. SO Email Template".
