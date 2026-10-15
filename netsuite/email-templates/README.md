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
