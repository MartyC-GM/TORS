/**
 * @NApiVersion 2.1
 * @NScriptType UserEventScript
 *
 * Purchase Order: when a line's Expected Receipt Date is set or changed, kick off
 * the map/reduce that copies the date onto backordered sales order lines for that item.
 */
define(['N/task', 'N/query', 'N/log'], (task, query, log) => {
    const MR_SCRIPT_ID = 'customscript_tors_mr_po_eta_to_so';
    const ITEMS_PARAM = 'custscript_tors_eta_items';

    const dateKey = (d) => (d ? new Date(d).toDateString() : '');

    const changedItems = (context) => {
        const { newRecord, oldRecord, type } = context;

        // Inline edit only carries the changed fields, so just take every item on the PO.
        if (type === context.UserEventType.XEDIT) {
            return query.runSuiteQL({
                query: `SELECT DISTINCT item FROM transactionline
                        WHERE transaction = ? AND mainline = 'F' AND item IS NOT NULL`,
                params: [newRecord.id]
            }).asMappedResults().map((r) => r.item);
        }

        const oldDates = {};
        if (oldRecord) {
            const oldCount = oldRecord.getLineCount({ sublistId: 'item' });
            for (let i = 0; i < oldCount; i++) {
                const lineId = oldRecord.getSublistValue({ sublistId: 'item', fieldId: 'line', line: i });
                oldDates[lineId] = dateKey(oldRecord.getSublistValue({ sublistId: 'item', fieldId: 'expectedreceiptdate', line: i }));
            }
        }

        const items = new Set();
        const count = newRecord.getLineCount({ sublistId: 'item' });
        for (let i = 0; i < count; i++) {
            const lineId = newRecord.getSublistValue({ sublistId: 'item', fieldId: 'line', line: i });
            const newDate = dateKey(newRecord.getSublistValue({ sublistId: 'item', fieldId: 'expectedreceiptdate', line: i }));
            if (newDate && newDate !== oldDates[lineId]) {
                items.add(newRecord.getSublistValue({ sublistId: 'item', fieldId: 'item', line: i }));
            }
        }
        return [...items];
    };

    const afterSubmit = (context) => {
        const { UserEventType } = context;
        if (![UserEventType.CREATE, UserEventType.EDIT, UserEventType.XEDIT].includes(context.type)) return;

        const items = changedItems(context);
        if (!items.length) return;

        try {
            // No deploymentId: NetSuite picks whichever deployment is free.
            const taskId = task.create({
                taskType: task.TaskType.MAP_REDUCE,
                scriptId: MR_SCRIPT_ID,
                params: { [ITEMS_PARAM]: JSON.stringify(items) }
            }).submit();
            log.audit('PO ETA sync queued', `PO ${context.newRecord.id}, items ${items.join(',')}, task ${taskId}`);
        } catch (e) {
            // All deployments busy. The nightly full run will pick these up.
            log.error('PO ETA sync not queued', `PO ${context.newRecord.id}: ${e.message}`);
        }
    };

    return { afterSubmit };
});
