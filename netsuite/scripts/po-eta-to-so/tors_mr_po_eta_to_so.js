/**
 * @NApiVersion 2.1
 * @NScriptType MapReduceScript
 *
 * Sets Expected Ship Date on backordered sales order lines to the earliest
 * Expected Receipt Date of any open PO line for the same item.
 *
 * Parameter custscript_tors_eta_items: JSON array of item internal IDs.
 * Left blank (the nightly scheduled deployment), it checks every backordered line.
 */
define(['N/query', 'N/record', 'N/runtime', 'N/log'], (query, record, runtime, log) => {
    const ITEMS_PARAM = 'custscript_tors_eta_items';

    const getInputData = () => {
        const raw = runtime.getCurrentScript().getParameter({ name: ITEMS_PARAM });
        const items = raw ? JSON.parse(raw).map(Number).filter((n) => n > 0) : [];
        const itemFilter = items.length ? `AND tl.item IN (${items.join(',')})` : '';

        // Open PO statuses: B Pending Receipt, D Partially Received, E Pending Billing/Partially Received.
        // Open SO statuses: A Pending Approval, B Pending Fulfillment, D Partially Fulfilled, E Pending Billing/Partially Fulfilled.
        return {
            type: 'suiteql',
            query: `
                SELECT so_id, line_id, po_date FROM (
                    SELECT tl.transaction so_id, tl.id line_id,
                           TO_CHAR(tl.expectedshipdate, 'YYYY-MM-DD') so_date,
                           (SELECT TO_CHAR(MIN(pl.expectedreceiptdate), 'YYYY-MM-DD')
                              FROM transactionline pl
                              JOIN transaction p ON p.id = pl.transaction
                             WHERE p.type = 'PurchOrd' AND p.status IN ('B','D','E')
                               AND pl.item = tl.item AND pl.mainline = 'F' AND pl.isclosed = 'F'
                               AND pl.quantity > NVL(pl.quantityshiprecv, 0)
                               AND pl.expectedreceiptdate IS NOT NULL) po_date
                      FROM transactionline tl
                      JOIN transaction t ON t.id = tl.transaction
                     WHERE t.type = 'SalesOrd' AND t.status IN ('A','B','D','E')
                       AND tl.mainline = 'F' AND tl.isclosed = 'F'
                       AND tl.quantitybackordered > 0
                       ${itemFilter}
                )
                WHERE po_date IS NOT NULL AND (so_date IS NULL OR so_date <> po_date)`
        };
    };

    const map = (context) => {
        const [soId, lineId, poDate] = JSON.parse(context.value).values;
        context.write({ key: String(soId), value: { lineId: String(lineId), poDate } });
    };

    const reduce = (context) => {
        const so = record.load({ type: record.Type.SALES_ORDER, id: context.key });
        let changed = 0;

        context.values.map(JSON.parse).forEach(({ lineId, poDate }) => {
            const line = so.findSublistLineWithValue({ sublistId: 'item', fieldId: 'line', value: lineId });
            if (line < 0) return;
            const [y, m, d] = poDate.split('-').map(Number);
            so.setSublistValue({ sublistId: 'item', fieldId: 'expectedshipdate', line, value: new Date(y, m - 1, d) });
            changed++;
        });

        if (changed) {
            so.save({ ignoreMandatoryFields: true });
            log.audit('SO ship dates updated', `SO ${context.key}: ${changed} line(s)`);
        }
    };

    const summarize = (summary) => {
        summary.reduceSummary.errors.iterator().each((soId, err) => {
            log.error(`SO ${soId} not updated`, JSON.parse(err).message);
            return true;
        });
        if (summary.inputSummary.error) log.error('Input error', summary.inputSummary.error);
    };

    return { getInputData, map, reduce, summarize };
});
