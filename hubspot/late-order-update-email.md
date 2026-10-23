# HubSpot Sequence: Late Order Update

One automated email step. It sends from the rep's own inbox, so write it the way the rep would.

**Subject:** Update on your order {{ contact.tors_late_order_number }}

**Body:**

Hi {{ contact.firstname | default: "there" }},

I wanted to give you a heads up on your order {{ contact.tors_late_order_number }} (your PO {{ contact.tors_late_order_po }}). Part of it is running behind what we first told you:

{{ contact.tors_late_order_items }}

Our best date for it now is {{ contact.tors_late_order_new_date }}.

Does that date work for you, or do you need it sooner? Just reply and let me know. If it's urgent, we can look at expediting it, shipping what we have on hand now, or finding an alternate that works.

Sorry for the wait, and thanks for sticking with us.

{{ sender.firstname }}
The O-Ring Store
208-413-6377

---

Notes for setup:
- In the HubSpot sequence editor, insert each `contact.` value with the Personalize button so the tokens are exact. Use a fallback ("there") for first name.
- Keep the sender's signature on (it uses the rep's own HubSpot signature).
- Sequence settings: stop when the contact replies (default), and send only on business days.
