# Baseline Data Snapshot: October 2026

Pulled 2026-10-23 from NetSuite and HubSpot. Read only. Numbers are rounded.

## Sales (NetSuite, invoice totals)

Invoice totals include freight and tax, so treat them as close to, not exactly, net sales.

| Year | Invoiced | Change |
|---|---|---|
| 2023 | $3.57M | |
| 2024 | $3.78M | +6% |
| 2025 | $4.49M | +19% |
| 2026 Jan to Sep | $3.70M | +9% vs. Jan to Sep 2025 ($3.39M) |
| 2026 full-year pace | about $4.8M | |

- About 2,200 invoices a month (roughly 100 a shipping day). Average invoice about $175.
- Best months in 2026: June ($455K) and August ($456K).
- Credit memos are tiny (a few thousand a month). Returns aren't a problem.

**Goal gap:** $10M in 2026 would take about $5.2M more than the current pace. $20M in 2027 is about 4x the 2026 pace. $50M in 2028 is about 10x.

## Customers (NetSuite, trailing 12 months from 2025-10-01)

| Annual spend | Customers | Sales | Share of sales |
|---|---|---|---|
| $50K and up | 5 | $394K | 8% |
| $10K to $50K | 61 | $1.21M | 24% |
| $1K to $10K | 703 | $1.86M | 36% |
| Under $1K | 14,739 | $1.65M | 32% |
| **Total** | **15,508** | **$5.11M** | |

- Very low concentration. Biggest customer is under 2% of sales.
- Top accounts: Cabka North America ($89K), McMaster-Carr ($85K, 331 invoices), Acorn Engineering ($76K), Depot Street II ($74K), Semco Tank ($70K), Dwyer Instruments ($47K), JMJ Parts ($47K), 5H Energy ($47K), Avionic Industries ($42K), PolyJohn ($39K), Hilcorp North Slope ($37K).
- 66 customers over $10K a year make up about a third of sales. That's the account base to grow.

## Margin and expense (NetSuite, Q3 2026 Jul to Sep)

| | Amount | % of sales |
|---|---|---|
| Sales (income accounts) | $1.23M | 100% |
| Cost of goods | $491K | 40% |
| **Gross margin** | **$740K** | **60%** |
| Operating expense in NetSuite | $325K | 26% |

**Open question:** $325K a quarter looks light for 17 people plus a 13,000 sq ft building. Payroll or other costs may be booked outside NetSuite. Ask before drawing profit conclusions.

## Inventory (NetSuite, on hand today)

- On-hand value: **$1.43M** across **12,544 SKUs** with stock.
- **No sales in 12 months: 3,257 SKUs worth about $251K** (18% of inventory value).
- Annual cost of goods (Q3 x 4): about $1.96M. **Turns: about 1.4 a year** (about 265 days of supply).
- Annual gross margin (Q3 x 4): about $2.96M. **GMROI: about 2.1** (each $1 of stock earns about $2.10 of margin a year).
- Read: high margin, slow turns. That's the "we have the odd size nobody else does" pattern. It works, but it soaks up capital. Industrial / MRO distributors often run 3 to 6 turns.
- Capital math: at 1.4 turns, each extra $1M in sales needs about $285K more inventory. At 3 turns it needs about $135K.

## Receivables (NetSuite, today)

- Open AR: **$170K** on 237 invoices (about 12 days of sales).
- More than 30 days past due: about $7K.
- Read: customers pay fast (lots of card and prepay). Cash isn't stuck in AR. If capital is tight, it's stuck in inventory.

## Pipeline (HubSpot, deals created since 2025-10-01)

| | Deals | Amount |
|---|---|---|
| Open | 184 | $269K |
| Won | 110 | $133K |
| Lost | 108 | $136K |

- About 50% win rate by count. Average deal about $1,200.
- HubSpot deals cover a small slice of total sales, so most business doesn't run through the pipeline.
- Open deals by owner (IDs): 166272224 has 82 deals / $170K; 166438107 has 73 / $42K; 166438104 has 21 / $55K.
- Contacts: about 22,700 loaded in July 2026, about 1,350 added since. HubSpot is new.

## First read on constraint hypotheses (before the interview)

These are guesses from the data. The interview is how we test them.

1. **Inventory productivity, not just capital.** $1.43M at 1.4 turns with $251K dead. Freeing and re-aiming existing stock may unlock more than new capital would.
2. **Demand from mid-size accounts.** 15,500 customers but only 66 over $10K. Growth to $10M+ probably needs more $10K to $100K accounts, which points at sales and marketing capacity.
3. **Profit visibility.** We can't size a capital plan without a full P&L. Possible admin constraint.
4. **People leverage.** Unknown until Module 5.

## Queries used

Re-run these to refresh. Narrow the date range if accounting-line queries time out.

```sql
-- Monthly invoice totals
SELECT TO_CHAR(t.trandate,'YYYY-MM') AS mon, t.type, COUNT(*) AS cnt, SUM(t.foreigntotal) AS total
FROM transaction t
WHERE t.type IN ('CustInvc','CashSale','CustCred') AND t.trandate >= TO_DATE('2023-01-01','YYYY-MM-DD')
GROUP BY TO_CHAR(t.trandate,'YYYY-MM'), t.type ORDER BY mon, t.type

-- Customer spend tiers (trailing 12 months)
SELECT COUNT(*) customers, SUM(tot) total, ... FROM (
  SELECT t.entity, SUM(t.foreigntotal) tot FROM transaction t
  WHERE t.type='CustInvc' AND t.trandate >= TO_DATE('2025-10-01','YYYY-MM-DD') GROUP BY t.entity)

-- Quarter P&L by account type (one quarter at a time; a full year timed out)
SELECT a.accttype, SUM(tal.amount) amt FROM transactionaccountingline tal
JOIN transaction t ON t.id=tal.transaction JOIN account a ON a.id=tal.account
WHERE tal.posting='T' AND t.trandate >= TO_DATE('2026-07-01','YYYY-MM-DD') AND t.trandate < TO_DATE('2026-10-01','YYYY-MM-DD')
AND a.accttype IN ('Income','COGS','Expense','OthIncome','OthExpense') GROUP BY a.accttype

-- Inventory value and dead stock
SELECT COUNT(*) skus, SUM(CASE WHEN s.sold IS NULL THEN 1 ELSE 0 END) no_sales_12m,
       SUM(CASE WHEN s.sold IS NULL THEN i.totalvalue ELSE 0 END) dead_value, SUM(i.totalvalue) total_value
FROM item i LEFT JOIN (SELECT tl.item, SUM(-tl.quantity) sold FROM transactionline tl
  JOIN transaction t ON t.id=tl.transaction
  WHERE t.type='CustInvc' AND t.trandate >= TO_DATE('2025-10-01','YYYY-MM-DD') GROUP BY tl.item) s ON s.item=i.id
WHERE i.itemtype='InvtPart' AND i.totalquantityonhand > 0

-- Open AR
SELECT SUM(t.foreignamountunpaid) open_ar, COUNT(*) open_invoices FROM transaction t
WHERE t.type='CustInvc' AND t.foreignamountunpaid > 0
```

HubSpot (query_crm_data):

```sql
SELECT hs_is_closed_won, hs_is_closed, COUNT(*), SUM(amount_in_home_currency) FROM DEAL
WHERE createdate >= '2025-10-01' GROUP BY hs_is_closed_won, hs_is_closed
```
