# Constraints Interview Log

This is the saved state for the Constraints Interview. The `first-principles` skill reads it at the start of every session and updates it at every pause. Commit and push after each update.

## Where we left off

- **Status:** In progress
- **Next module:** Module 0, The Goals Themselves
- **Next question:** 0.1 "When you say $10 million this year, what does hitting it give you?"
- **Follow-ups owed:** Monthly payroll all-in (wages + taxes + benefits) by month for 2026; reconnect QuickBooks. Why gross margin % slid from 66% to 60%. Where did the cash go? (inventory buys, expenses outside NetSuite, owner draws, debt payments). Bookkeeping fixes for the GM Financial and Ally loan accounts.
- **Baseline in use:** `baseline-2026-10.md`

## Progress

| Module | Status | Date |
|---|---|---|
| 0. The Goals Themselves | In progress | 2026-10-23 |
| 1. Demand | Not started | |
| 2. Sales Process and Capacity | Not started | |
| 3. Inventory and Supply | Not started | |
| 4. Capital and Cash | Not started | |
| 5. Operations and People | Not started | |
| 6. Administration, Succession, Policy | Not started | |
| 7. Marketing | Not started | |
| 8. Synthesis | Not started | |

## Constraint hypotheses (ranked)

| # | Hypothesis | Type | Evidence | Confidence |
|---|---|---|---|---|
| 0 | **Cash crunch right now:** about $165K short on bills and cards, $149K of AP past due. Has to be handled no matter what the long-term constraint turns out to be. | Capital / Cash | AP schedule 10/22 | Known |
| 1 | Capital is tied up in slow inventory ($1.43M at about 1.4 turns, $251K with no sales in 12 months). Getting more out of stock may beat raising new money. | Capital / Policy | Baseline | Known (data), cause unknown |
| 1b | **Built for $10M, selling at $4.8M.** Payroll and costs were sized ahead of sales. New customers flat at about 850 a month for two years. Constraint is demand, not capacity. | Market | NetSuite + Marty 0.1b | Known (sales side), payroll number pending |
| 2 | Not enough mid-size accounts. 15,500 customers, only 66 over $10K a year. | Market / Sales | Baseline | Known (data), cause unknown |
| 3 | No full profit picture in NetSuite (opex looks light). Hard to plan capital without it. | Administration | Baseline | Guess |
| 4 | Marty believes capital is the constraint. | Capital | Marty, master prompt | Believed |

## Answers captured

_(Add by module. Short, Marty's words where possible. Tag each: Known / Believed / Guess.)_

### Module 0: The Goals Themselves (2026-10-23)

- **0.1 What $10M gets us:** "Increase the inventory, pay all the bills, make sure we're starting even by the first of the year, and actually give us a little purse to really make a push next year." (Believed)
  - Read: $10M isn't the goal itself. It's how we pay for the real goals: (a) more inventory, (b) bills paid and starting the year even, (c) a pot of money for next year's push. "Starting even" hints we're behind on something right now. Following up.
- **0.1a What are we behind on?** Marty answered with the AP schedule (TORS_AP_Schedule_10222026.xlsx). (Known)
  - Operating cash: about $63K.
  - Vendor bills (AP) due through Nov 20: about $346K. About $149K of that was already past due as of Oct 22.
  - Credit cards: about $55K (MC $22.7K, Amex $32.5K), no payment posted in September.
  - Vehicle loans: about $91K (GM Financial $38.8K, Ally truck $52.4K). Line of credit shows $0.
  - Coming in: open AR about $170K to $180K, and customers pay fast.
  - Biggest vendor balances: Freudenberg $76K, FedEx $54K, GE MAO Rubber $39K, Universal Polymer $28K, Seal and Rubber Tech $24K, ShipJunction $16.5K (all past due), Olypsys® $15K.
  - $27K of bills are on 2% 10 / Net 30 terms. Paying late means losing those discounts.
  - **Rough gap to "starting even":** cash + AR (about $235K) against AP + cards (about $400K) leaves us **about $165K short**, before any cushion or a fund for next year's push.
  - Bookkeeping flags from the sheet: GM Financial is set up as a Bank account and the Ally loan as a Fixed Asset in NetSuite. Both are wrong and should go to the bookkeeper.
  - Read: the business makes about $245K a month in gross margin but is about $165K behind on bills, and inventory is $1.43M with $251K not moving. Either the cash went into stock, or expenses are bigger than NetSuite shows (see the opex question), or both. Next step is finding out where the cash went.
- **0.1b When did it get tight?** "Started out pretty decent. Beginning of summer it felt real comfortable, and now it's been a downhill slide since." Thinks it's payroll ("quite a bit of payroll," some turnover) and "not enough incoming new business." "I feel that we're stacked to do about 10 million, we're just not doing it." (Believed)
  - **Checked in NetSuite:**
    - Sales did NOT slide after summer. Jun to Sep 2026 averaged about $416K a month, vs about $401K Jan to May. Year to date is up about 9%. (Known)
    - New customers are flat, not down: 780 to 900 first-time buyers every month for two years. (Known) So "not enough new business" is true in the sense of no growth, not a drop.
    - Gross margin % is drifting down: about 66% in Q1, about 60% in Q3. At $410K a month that's about $25K a month less margin. Could be pricing, product mix, freight, or how COGS gets booked. (Known number, cause unknown)
    - Vendor bills went up: about $208K a month in Jan and Feb, about $280K a month Jun to Oct (Aug was $349K). (Known)
    - **Payroll is not in NetSuite.** Expense accounts only show health insurance ($45K a quarter) and L&I. Wages are kept somewhere else (QuickBooks payroll, most likely). QuickBooks needs to be reconnected before we can pull it. (Known)
    - NetSuite shows about $145K a month in operating profit **before payroll**. Real profit depends on the payroll number.
    - Other costs worth a look: software $60K a quarter (about $240K a year), shipping $78K a quarter, late fees and interest $5.3K a quarter. (Known)
  - **Read:** the slide is on the spending side, not the sales side. Sales and new customers held steady while bills climbed and margin slipped. "Stacked to do $10M" while selling at a $4.8M pace means the cost base was built ahead of revenue. That points the main constraint at **demand / sales conversion** (Market), with cost discipline as the urgent fix.

## Data requests

- Full P&L for the last 12 months, including payroll. **Confirmed payroll is not in NetSuite.** Reconnect QuickBooks (claude.ai connector settings) or export a payroll summary by month.
- Lost-sale tracking: do we capture "couldn't fill" or "lost on price"? If not, consider starting.
- Sales by channel (web store vs. phone/email vs. marketplace) if NetSuite can split it.

## Decisions made

_(Anything we decide along the way, with the date.)_

## Session history

| Date | Modules covered | Notes |
|---|---|---|
| 2026-10-23 | Setup | Built skill, pulled baseline from NetSuite and HubSpot |
