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
| 1. Demand | In progress | 2026-10-23 |
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

- **13-week cash forecast built** (`strategy/cash-plan/TORS_13-Week_Cash_Forecast.xlsx`, 10/23). Marty has a PayPal line, repaid at about 10% of sales. Results through Jan 22:

  | Plan | Lowest cash | Cash Jan 22 |
  |---|---|---|
  | A: business as usual | -$118K | -$118K |
  | B: tighten up (buy 25% less, cut software, sell dead stock, vendor plans) | -$61K | +$16K |
  | C: tighten up + $150K PayPal loan | +$22K | +$79K (still owe PayPal about $93K) |
  | D: PayPal loan only | -$41K | -$41K |

  - **Why "we make money" doesn't cover it:** Nov to Jan sales run about $350K to $385K a month, and at that level the business is about break-even (fixed costs about $228K a month, gross margin about 64%). The profit gets made in the busy months. The $148K of past-due bills has to be paid out of the slow months.
  - **A loan alone doesn't work** (Plan D). The repayment, about $5K to $6K a week, eats what little the slow months make. The loan only works paired with buying less.
  - **First move:** starting Monday, buy only for open orders and proven fast movers. It's free, it's in our control, and it's the piece every working plan depends on.

- **Sales-only worst case** (Marty, 10/23): no loan, no vendor calls, every bill paid no more than 15 days late, cash only from sales. Added as a tab in the cash forecast.
  - $35K of bills are already more than 15 days late and have to be paid now. Existing AP comes due (+15 days) heavily in the first 6 weeks: about $102K, $75K, $61K, $43K, $26K, $40K.
  - **Open purchase orders not yet received: about $291K** (Freudenberg $114K, GE MAO $82K, Tuico $25K, Best Ring $10K). These become bills Dec to Jan. (Known)
  - At plan sales: cash goes negative the week of Nov 2, bottoms around -$31K mid-November, recovers early December, then open POs pull it to about -$57K by Jan 22. Negative 10 of 13 weeks.
  - **What it takes:** about $10K a week (about $43K a month) more sales than plan keeps cash above zero the whole way, meaning Nov to Jan sold at the Jun to Oct pace (about $416K a month). A $40K cushion from sales alone would take about $25K a week extra, which isn't realistic.
  - If sales come in 10% under plan: about -$168K by Jan 22.
  - **Buying limits:** stocked items that would run short in 13 weeks at the 12-month pace total only about $65K to replenish ($41K for items under 4 weeks of supply, $24K for 4 to 13 weeks). Open POs ($291K) more than cover it. $903K of stock sits in 6,439 SKUs with over a year of supply. So: no new stock buys until February, buy-to-order only against a customer order.
  - If half the open POs slide past January, Jan 22 cash goes from about -$57K to about +$52K. Biggest single lever, and it's a buying decision, not a bill call.
  - Note: average cost on the 1,051 items with zero on hand looks unreliable (it implies $2.7M a year of cost against $1.5M actual COGS). Worth a cleanup.

- **Weekly sales target to be whole by Feb 1** (Marty, 10/23): 50% GP, sales only, no new purchases, open POs arrive as ordered, all bills paid within due date + 15 days.
  - Cash out Oct 26 to Jan 31 (14 weeks): about $1.27M (payroll, expenses, existing AP $346K, open POs as they come due, cards, loans, buyout).
  - **$97K a week (about $422K a month) keeps cash at or above zero every week.** The tight spot is the week of Nov 9. That's about $17K a week over plan.
  - $101K a week also pays off the $55K of credit cards by Feb 1. $118K a week holds a $40K cushion the whole way.
  - At 50% GP, $97K a week uses about $680K of inventory at cost over 14 weeks. On hand $1.43M + open POs $291K covers it, but only about $560K of that is in items that turn within a year, so about $120K has to come out of slow stock.
  - After February, once we restock: break-even is about $108K a week at 50% GP, or about $86K a week at our actual 63%.

- **Working answer on the constraint (10/23, before Modules 1 to 8):** the constraint is **demand**, meaning not enough of the right customers ordering, especially mid-size accounts. Doubling test: doubling inventory wouldn't double sales ($903K already sits in items with over a year of supply). Doubling staff wouldn't either (we're built for more than we sell). Doubling demand would, since the shelves and crew can handle it. Evidence: new customers flat at about 850 a month for two years, 15,500 customers but only 66 over $10K a year, $175 average invoice, quote win rate is fine, sales come in on their own (web and inbound) with no outbound engine. Made worse by a **policy constraint**: no rules on cash (Groundwork, early debt payoff) and buying ahead of demand (1.4 turns, $291K open POs, PO run lines raised to $400). The capital squeeze is a symptom, not the root. Modules 1 and 2 test this.

- **Over-a-year-supply report** (10/23, `strategy/cash-plan/TORS_Over_1_Year_Supply.xlsx`): 6,475 items that sold in the last 12 months but have more on hand than a year of sales, about $909K at cost. $427K of it is 10+ years of supply. 1,798 of these items (about $303K on hand) were bought again in the last 12 months, and on 1,659 of them the last PO was for more than a full year of sales. Biggest by last-PO vendor: Freudenberg $195K, Tuico $131K, GE MAO $107K, no PO on file $105K, Seal and Rubber Tech $90K. Read: the buying process orders big lots (minimums, price breaks, line minimums) well past what sells. Policy constraint, confirmed with data.

### Module 1: Demand (2026-10-23)

- **1.7 Who should we have 10x more of?** "OEMs. Original equipment manufacturers." (Believed)
  - **Checked in NetSuite:** only 66 customers are tagged OEM, $161K in the last 12 months (about 3% of sales). But **14,254 of 15,500 customers (about $3.43M, 67% of sales) have no category at all.** Many top accounts look like OEMs (Cabka, Acorn Engineering, Dwyer, PolyJohn, Air Squared, Radium, Penske Racing Shocks, Rugged Suppressors) but aren't tagged. (Known)
  - Read: we can't see how many OEMs we have, so we can't aim at them or measure growth. Tagging customers by type is a cheap admin fix that serves the sales constraint.
- **1.3 Best OEM and why us?** "Spray Poly Parts, and we believe it's because they order online and in bulk, and the pricing is good." (Believed)
  - **Checked in NetSuite:** two customer records. SprayPolyParts (CU115961, no category) $3.1K, and Spray Polyurethane Parts (CU119736, tagged Distribution) $8.0K. About **$11K combined** in the last 12 months. (Known)
  - Read: our best OEM in Marty's mind is an $11K-a-year account that NetSuite calls a distributor, and it's split across two records. So the OEM base is thin, and the reasons we win (online, bulk, price) aren't unique to us. Next: define the target OEM by size and what they make.
- **Top 25 customers, last 12 months** (Marty asked, 10/23; branches rolled up to parent): $1.03M combined, about 20% of sales. Biggest is Cabka at $89K (1.7%). **15 of the 25 build products** (Cabka, Acorn, Semco Tank, Dwyer, Avionic, PolyJohn, Engineered Composites, JST, Q-Pumps, Meditrina, Air Squared, Rugged Suppressors, Checkpoint Pumps, Excel Plastics, Pacific Fusion), about $590K. Only Dwyer and Checkpoint are tagged OEM. Distributors: McMaster $82K, Fastenal (37 branches) $44K, Motion (51 branches) $43K, JMJ, HMFT, Maqui. Estimated gross margin ranges from about 20% (Engineered Composites) to 90% (Dwyer); NetSuite's estimated cost, so treat as rough. (Known)
  - Read: OEMs are already our biggest customers, they're just untagged and each is small. Getting to $10M through OEMs means about 100 OEM accounts at $50K+, versus about 5 today.
- **1.3b How did we land Cabka?** "They ordered on the website first, and then they came back to Jim, our former sales manager, who almost fucked it up entirely. We turned it over to Sophie, our sales coordinator. She salvaged it, and she's just honest with them and takes care of them, giving them the prices they need and delivering their request." (Believed)
  - Read: the pattern is **website gets the first order, a person turns it into an account.** The website is the front door and Sophie is the account builder. The risk is that it depends on who catches the lead: Jim nearly lost it, Sophie saved it. Question: is there a system that hands every promising first web order to a Sophie, or did Cabka get lucky? If Sophie is the growth engine, her capacity may be the real bottleneck inside the demand constraint.
- **First-time orders over $1,000, 2026 so far** (Marty's test, 10/23): 8,109 new customers this year. **48** had a first order of $1,000+. Only **12 came back** (25%); those 12 have bought $87K. The other **36 bought once and never again** ($90K of first orders). 149 new customers had a first order of $500+. Some of the one-time buyers are big names: ISCO Industries ($19.6K), Navy NSWC Indian Head ($8.8K), Toshiba, LG Energy Solution, DuPont, TRUMPF, Teledyne Dalsa, Spectral Systems. (Known)
  - Read: about one $1K+ first-timer a week walks in the door, and 3 out of 4 never come back. That's a catch-and-keep problem, not a find-them problem. A rule like "every first order over $1,000 gets a call from Sophie within a week" costs almost nothing.
- **1.3c Does Sophie have room?** "She can do some, but not every one of them. I also have, in the sales department, Anson, Darion, Daro, myself, and Janevea. It's not a lack of people." (Believed)
  - Read: six people touch sales (Sophie, Anson, Darion, Daro, Marty, Janevea), and still about one $1K+ first-timer a week never gets a call. So it isn't headcount. It's **no trigger, no owner, no follow-up**. A process and policy constraint inside the demand constraint. Fix idea: an automatic alert on every first order over $1,000, assigned in rotation to a named person, with a 7-day call and a 30-day follow-up, tracked on the scorecard. Next: where does the sales team's time actually go today?
- **1.3d Where does sales time go?** "They are [busy]. Everybody has another role: purchasing, marketing, accounting, general manager, but I think all those need to be understood. We are all sales first, customers first." (Believed)
  - Read: "sales first" is the culture, but not how the day is built. Everyone's main job is something else, so sales happens when a customer calls, not by plan. When everybody owns sales, nobody owns growing accounts. TOC step 3 (subordinate) says the other jobs should bend around the constraint: protected selling time, named accounts per person, a scorecard per person. The Elevate step may be one person whose main job is growing accounts the way Sophie grew Cabka.

- **1.8 Where does the extra $30K a week come from?** "With a little attention and care, especially in expediting, we're going to get more frequent orders and first-time [buyers] coming back." (Believed)
  - **Checked in NetSuite, Q3 2026 orders over $250 (891 that shipped):** 65% shipped in 0 to 1 days, 8% in 2 to 5 days, **14% in 6 to 14 days, and 13% (115 orders) took 15+ days**. Average 5.8 days. (Known)
  - Read: about 1 in 4 bigger orders waits more than 5 days (backorders, special orders, buyouts). That's where expediting and keeping the customer posted matter most, and where a first-timer decides whether to come back. Next: who tells the customer when an order runs late, and how fast?
- **1.8b Who tells the customer?** "We have typically been sending an order update, but we don't ask the customer if it's okay. We don't ask them if it's expediting. We don't even make sure they got the email. Customer service sends it out, but they don't notify the salesperson responsible either." (Known, Marty's account)
  - Read: the delay message goes one way, nobody confirms it landed, nobody asks "does this date work or do you need it sooner?", and the account owner never hears about it. So the person who owns the relationship finds out when the customer is already upset, or never. Fix ideas: (1) add "your customers' late orders" to each owner's morning Slack list; (2) change the order status email to ask "Does this date work, or do you need it sooner?" with a reply that goes to the owner; (3) owner calls on any late order over $1,000 or any first-time buyer.

## Data requests

- Custom Income Statement by month for 2026 (to see whether payroll climbed through the summer).
- Balance sheet at Dec 31, 2025 vs. today (to see where the cash went).
- Note: the SuiteQL connection can't see payroll postings. Use NetSuite reports for anything payroll.
- Lost-sale tracking: do we capture "couldn't fill" or "lost on price"? If not, consider starting.
- Sales by channel (web store vs. phone/email vs. marketplace) if NetSuite can split it.

## Decisions made

_(Anything we decide along the way, with the date.)_

- **2026-10-23: 90-day targets (to about Jan 21, 2027).** Marty: weekly sales up 25%, "to at least be $133,000 a week," and first-time buyers coming back at least 25% of the time within 90 days.
  - Check: 2026 has averaged about $95K a week. Up 25% is about $119K. $133K is about 40% up, and January usually runs around $83K to $89K a week, so $133K in January would be about 50% over last January. **Marty's answer: $125K a week minimum, and it'd be nice to beat that by 25% (about $156K).** Not stated as a percentage. "We're investing a lot of high-paid professionals, and if we don't get this, it's going to be embarrassing as fuck and detrimental." Dashboard updated: $125K goal line, $97K cash floor line, and a first-timer repeat-rate tile (at 10% on 10/23, 269 of 2,598).
  - Baseline for repeat: of 2,416 first-time buyers in Q2 2026, 299 (12%) ordered again within 90 days. First-timers at $1,000+: 3 of 14 (21%). So 25% means about doubling the overall repeat rate.

- **2026-10-23: Selling time set.** Marty, Daro and Darion each do 2 hours inbound + 2 hours proactive sales every day (4 hours each). Janevea does 1 hour, as one team with Marty. That's about 13 hours a day of protected selling time, plus Anson and Sophie. SOP updated.

- **2026-10-23: Order assignment and selling time.** Marty set protected selling time (Marty 2 hrs, Janevea 1 hr with Marty, Daro 2 inbound + 2 proactive) and routing for every sales order over $250: OEM, pumps, distributors to Marty and Janevea; oil, gas and energy to Darion; military and aerospace to Anson; retail, individuals and no company name to house; everyone else, including fluid power and untagged customers, to Daro. SOP: `strategy/sops/SOP-Sales-Order-Assignment.md`. Daily Slack DM to each owner chosen; scheduled weekdays 7:17 AM Pacific starting 10/26 (needs NetSuite and Slack connectors added to the scheduled task). Marty's calls: no new accounts to Sophie; TORS house customers with $250+ orders move to one of the four (best guess or round robin); named reps stay. Started live 10/23 with today's orders: Vapourtec, Purcraft and ICT Billet moved from TORS to Marty in NetSuite, and DMs went to Marty, Janevea and Darion. The 1,411-customer backlog (`strategy/sops/house-account-reassignment.csv`) is parked for later. Customers who already have a named rep (2,302, including 1,580 with no purchase in 12 months) are left alone. Only TORS house accounts get reassigned.

- **2026-10-23: Customer category = type of buyer.** Manufacturers are called OEM. Marty approved, and 39 customers were changed to OEM in NetSuite: the 13 top-25 manufacturers (Avionic, JST and Meditrina keep their old industry in Comments) plus 26 active Manufacturing-tagged customers who bought in the last 12 months. 58 Manufacturing-tagged customers with no recent sales, and inactive Pack4, were left alone. Next: add an Industry field and tag customers as they order.

- **2026-10-23: No more TORS money goes to Groundwork.** Marty expects the $293K already out to be a straight loss. Handle the Groundwork loan as its own project (CPA on write-off and tax treatment).
- **2026-10-23: Two tracks from here.** Track 1 is a 10-week cash plan to get even by Jan 1 (about $165K gap). Track 2 is to keep going with the interview (Module 1, Demand) to find the growth constraint.

## Session history

| Date | Modules covered | Notes |
|---|---|---|
| 2026-10-23 | Setup | Built skill, pulled baseline from NetSuite and HubSpot |
| 2026-10-23 | Module 0 (0.1) | AP schedule, income statement, balance sheets. Found the cash went to debt payoff, Groundwork, inventory, equipment. Decided: no more money to Groundwork, two-track plan. |
