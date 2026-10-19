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

This version reads `transaction.custbody_tors_order_link` first, then falls back to the
customer field. Needs a Transaction Body Field:

- ID: `_tors_order_link` (becomes `custbody_tors_order_link`), type Hyperlink
- Applies To: Sale
- Sourcing & Filtering: Source List = Customer, Source From = Order Status Link
- Store Value: checked
