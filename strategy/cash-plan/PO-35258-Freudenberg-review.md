# PO 35258, VN30 Freudenberg: Original Run vs. Current

Reviewed 2026-10-23. Read only. Nothing in NetSuite was changed.

## What NetSuite records show

- Created 10/22/2026 by the automated PO run (REST web services, under Marty's login).
- Original memo: "Automated PO run 10/22/2026 - HOLD for approval by Marty or Darion - do not send"
- **Original total: $4,594.21** (system note on create)
- **Current total: $8,327.29** (up $3,733, +81%). Memo is now blank, vendor ref C26907 added, status Pending Receipt (approved).
- Employee on the PO is Darion. The PO run rules say to write POs under the Purchasing Department employee (ID 1553211) so they hold for approval. Under Darion, it saves as approved.
- The line-by-line edits aren't in the system notes this connection can see, and the PO run only reports to chat, so the original line list isn't saved anywhere. The table below rebuilds it from the run's rules using today's stock numbers.

## Line by line

| Item | Freudenberg preferred? | Net position | Run would order (est.) | Run $ (est.) | On PO now | PO $ now | Read |
|---|---|---|---|---|---|---|---|
| 21334TC | Y | 0 | 16 | $50 | 20 | $57 | About the same |
| 35X54X10SC | Y | -80 | 80 | $105 | 80 | $105 | Same |
| 6226-52 | **N** | -11 | 0 | $0 | 100 | $37 | **Added by hand** (not preferred vendor) |
| A75108 | **N** | -429 | 0 | $0 | 2,500 | $290 | **Added by hand** |
| B70022-N888 | Y | -8 | 237 | $50 | 1,000 | $220 | Raised |
| B70212-N888 | Y | -7 | 118 | $50 | 1,150 | $403 | **Raised to ~$400** |
| B70242-N888 | Y | -37 | 37 | $73 | 190 | $405 | **Raised to ~$400** |
| BV75229 | **N** | -10 | 0 | $0 | 100 | $38 | **Added by hand** |
| FFKM-009-SZ498 | Y | 0 | 49 | $374 | 14 | $77 | Lowered |
| FFKM-120-SZ484 | Y | -16 | 16 | $144 | 27 | $243 | Raised |
| FFKM-125-SZ495 | Y | -20 | 20 | $218 | 30 | $327 | Raised |
| FFKM-152-SZ485 | Y | -3 | 3 | $74 | 16 | $414 | **Raised to ~$400** |
| FFKM-214-SZ498 | Y | -35 | 41 | $1,056 | 50 | $1,291 | Slightly raised |
| FFKM-224-SZ498 | Y | 10 | 14 | $652 | 15 | $719 | About the same |
| FFKM-391-SZ485 | Y | -5 | 5 | $1,899 | 5 | $2,011 | Same qty, higher price |
| FS70329 | Y | -2 | 16 | $51 | 126 | $403 | **Raised to ~$400** |
| FS70910 | Y | -98 | 135 | $50 | 1,100 | $409 | **Raised to ~$400** |
| HNBR90214-BLK | Y | -100 | 209 | $50 | 100 | $29 | About the same need |
| UC70126 | Y | -1 | 76 | $50 | 502 | $401 | **Raised to ~$400** |
| V75125-MS | Y | 17 | 149 | $81 | 800 | $433 | **Raised to ~$400** |
| V90017 | **N** | -139 | 0 | $0 | 250 | $17 | **Added by hand** |
| **Total** | | | | **~$5,028** | | **$8,327** | |

Rebuild is about $430 over the recorded $4,594 because stock and backorders moved a day, so treat line quantities as close, not exact.

## The pattern

1. **Eight lines were raised to about $400 each.** Looks like a $400 per-line minimum (possibly Freudenberg's) applied after the run. The run's table has no line minimum for Freudenberg, so it used the $50 default. If $400 is Freudenberg's real minimum, it belongs in `vendor-parameters.md`. If not, these lines are overbuying.
2. **Four lines were added for items where Freudenberg isn't the preferred vendor** (A75108, 6226-52, BV75229, V90017). They're all backordered, so it may have been on purpose to fill customer orders.
3. Vendor ref C26907 and the split receipt dates (11/06, 12/10, 12/28) suggest Freudenberg already acknowledged the order. Cutting it back now likely means a call to Freudenberg.

Rolling back to the run's quantities would cut roughly $3,300 to $3,700 from this PO.
