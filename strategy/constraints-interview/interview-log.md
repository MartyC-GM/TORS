# Constraints Interview Log

This is the saved state for the Constraints Interview. The `first-principles` skill reads it at the start of every session and updates it at every pause. Commit and push after each update.

## Where we left off

- **Status:** In progress
- **Next module:** Module 0 wrap-up (questions 0.2 to 0.7), then Module 1, Demand
- **Next question:** 0.2 "Where did $10M, $20M, $50M come from?"
- **Follow-ups owed:** Build the Jan 1 cash plan (Track 1). Bookkeeper items: payroll tax liabilities, AP vs. AP schedule mismatch, GM Financial and Ally account types. Why gross margin % slid from 66% to 60%. Software spend line by line. Monthly payroll trend (run the income statement by month). Where did the cash go? (inventory buys, expenses outside NetSuite, owner draws, debt payments). Bookkeeping fixes for the GM Financial and Ally loan accounts.
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
| 3 | **Profitable but cash-poor.** $354K net income YTD while about $165K behind on bills. Cash is going to balance sheet items (inventory, debt, draws, buyout) that the P&L doesn't show. Need a monthly cash flow view, not just a P&L. | Capital / Administration | Income statement 0.1c | Known (gap), cause pending |
| 3b | **Capital leaving the business.** $293K lent to Groundwork, $106K of debt paid off early, all in a year the cash ran tight. A policy constraint: no rule on what TORS cash can be used for. | Policy / Capital | Balance sheets 0.1d | Known |
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
- **0.1c Payroll in NetSuite?** Marty sent the FY 2026 Custom Income Statement (CustomIncomeStatement216.xlsx). **Correction: payroll IS in NetSuite.** The SuiteQL connection can't see payroll postings (most likely a role permission), so my earlier "nothing posted" read was wrong. Use the income statement report for payroll from here on. (Known)
  - **FY 2026 year to date (about 9.7 months):**

    | Line | YTD | % of income |
    |---|---|---|
    | Total income | $3.97M | 100% |
    | Cost of sales (incl. inbound freight $141K, tariffs $58K) | $1.46M | 37% |
    | **Gross profit** | **$2.51M** | **63%** |
    | Payroll all in (wages $992K, taxes $59K, health $125K, comp $7K) | $1.19M | 30% |
    | Outbound shipping + fuel surcharge | $319K | 8% (shipping income was $336K) |
    | Software | $174K | 4.4% |
    | Rent | $84K | 2.1% |
    | Marketing | $84K | 2.1% |
    | PayPal fees | $55K | 1.4% |
    | Late fees, penalties, interest | $33K | 0.8% |
    | **Net income** | **$354K** | **8.9%** |

  - Payroll runs about $102K a month in wages, about $122K a month all in.
  - Fixed costs run about $222K a month. At 63% gross margin, breakeven is about $352K a month in sales. We're doing about $409K. That's a cushion of only about 14%.
  - **Read:** the business is profitable on paper ($354K YTD, about $36K a month). But we're about $165K behind on bills. So the cash went somewhere the income statement doesn't show: inventory build, loan payments, owner draws, the shareholder buyout (account 27001, Amanda), equipment, or vehicles. That's the balance sheet, and it's the next thing to check.
  - $33K in late fees and penalties is money lost to the cash crunch itself. Software at $174K YTD is high for a 17-person company and worth a line-by-line review.

- **0.1d Where did the cash go?** Marty sent balance sheets for Dec 31, 2025 (BalanceSheet94) and FY 2026 to date (BalanceSheet135). Cash flow traced, ties to within about $200. (Known)

  | Where the money came from | |
  |---|---|
  | Net income YTD | +$354K |
  | Vendors carried more (AP net of the A/P adjusting account) | +$92K |
  | More customer deposits | +$26K |
  | **Total in** | **about $476K** |

  | Where it went | |
  |---|---|
  | Paid off debt: PayPal Capital $74K, P1FCU loan $21K, truck loan $11K | $106K |
  | Payroll taxes parked on the balance sheet (negative liability accounts) | $85K |
  | **New loan to Groundwork** (25800 "GW Loan from TORS") | $60K |
  | Inventory build | $62K |
  | Vehicles and equipment | $37K |
  | AR and undeposited funds up | $44K |
  | Accrued purchases and accrued interest paid down | $35K |
  | Shareholder buyout (27000) | $19K |
  | **Total out** | **about $448K** |
  | Bank balance change | +$28K |

  - **Groundwork:** TORS now has about **$293K** out to Groundwork ($233K in 13500 GW Loan from before 2026, plus $60K this year). That's more than the whole current shortfall. (Known)
  - **Payroll taxes:** employer Social Security, Medicare, and federal withholding are sitting as negative liabilities (about -$85K) instead of hitting the P&L. The income statement shows only $22K of employer tax on $992K of wages; it should be more like $75K to $80K. So **real net income is probably closer to $270K**, not $354K. Bookkeeper item. (Known pattern, exact number pending)
  - **AP mismatch:** NetSuite AP is $103K, but the AP schedule shows $346K of open bills. The A/P Adjusting Account went from -$247K to -$7K. Something in AP isn't reconciled. Bookkeeper item. (Known)
  - No owner draws recorded in 2026. Notes receivable from Daro ($25K) and Darion ($29K) unchanged.
  - **Read:** the business didn't lose money. Cash went to paying off debt early ($106K), Groundwork ($60K), inventory, and equipment, while vendors quietly financed the gap. Paying off PayPal Capital and the P1FCU loan was a good long-term move but drained the cushion. With the Groundwork money back, we'd be close to even.

## Data requests

- Custom Income Statement by month for 2026 (to see whether payroll climbed through the summer).
- Balance sheet at Dec 31, 2025 vs. today (to see where the cash went).
- Note: the SuiteQL connection can't see payroll postings. Use NetSuite reports for anything payroll.
- Lost-sale tracking: do we capture "couldn't fill" or "lost on price"? If not, consider starting.
- Sales by channel (web store vs. phone/email vs. marketplace) if NetSuite can split it.

## Decisions made

_(Anything we decide along the way, with the date.)_

- **2026-10-23: No more TORS money goes to Groundwork.** Marty expects the $293K already out to be a straight loss. Handle the Groundwork loan as its own project (CPA on write-off and tax treatment).
- **2026-10-23: Two tracks from here.** Track 1 is a 10-week cash plan to get even by Jan 1 (about $165K gap). Track 2 is to keep going with the interview (Module 1, Demand) to find the growth constraint.

## Session history

| Date | Modules covered | Notes |
|---|---|---|
| 2026-10-23 | Setup | Built skill, pulled baseline from NetSuite and HubSpot |
| 2026-10-23 | Module 0 (0.1) | AP schedule, income statement, balance sheets. Found the cash went to debt payoff, Groundwork, inventory, equipment. Decided: no more money to Groundwork, two-track plan. |
