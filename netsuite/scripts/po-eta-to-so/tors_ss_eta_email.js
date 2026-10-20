/**
 * @NApiVersion 2.1
 * @NScriptType ScheduledScript
 *
 * Sends "1. Order Update Email Template" to the customer on any sales order whose
 * custbody_tors_eta_email_due time has passed, then clears the field.
 * The due time is set by tors_mr_po_eta_to_so when it changes ship dates.
 * Runs every 15 minutes.
 */
define(['N/query', 'N/record', 'N/render', 'N/email', 'N/runtime', 'N/log'],
    (query, record, render, email, runtime, log) => {
        const EMAIL_DUE_FIELD = 'custbody_tors_eta_email_due';
        const TEMPLATE_ID = 20;        // 1. Order Update Email Template
        const DEFAULT_AUTHOR = 3196556; // Sales Team, used when the order has no sales rep
        const MIN_USAGE = 100;

        const clearDue = (soId) => record.submitFields({
            type: record.Type.SALES_ORDER,
            id: soId,
            values: { [EMAIL_DUE_FIELD]: '' },
            options: { ignoreMandatoryFields: true }
        });

        const execute = () => {
            const script = runtime.getCurrentScript();

            const pending = query.runSuiteQL({
                query: `SELECT t.id, t.tranid, t.entity, t.employee,
                               NVL(t.email, c.email) email, t.${EMAIL_DUE_FIELD} due
                          FROM transaction t
                          JOIN customer c ON c.id = t.entity
                         WHERE t.type = 'SalesOrd' AND t.${EMAIL_DUE_FIELD} IS NOT NULL`
            }).asMappedResults().filter((so) => Number(so.due) <= Date.now());

            for (const so of pending) {
                if (script.getRemainingUsage() < MIN_USAGE) {
                    log.audit('Out of usage', 'The rest go out on the next run.');
                    return;
                }
                try {
                    if (!so.email) {
                        log.error(`SO ${so.tranid} not emailed`, 'No email on the order or customer.');
                        clearDue(so.id);
                        continue;
                    }

                    const merged = render.mergeEmail({
                        templateId: TEMPLATE_ID,
                        entity: { type: 'customer', id: Number(so.entity) },
                        transactionId: Number(so.id)
                    });

                    email.send({
                        author: Number(so.employee) || DEFAULT_AUTHOR,
                        recipients: [so.email],
                        subject: merged.subject,
                        body: merged.body,
                        relatedRecords: { transactionId: Number(so.id), entityId: Number(so.entity) }
                    });

                    clearDue(so.id);
                    log.audit(`SO ${so.tranid} emailed`, so.email);
                } catch (e) {
                    // Leave the due time in place so the next run tries again.
                    log.error(`SO ${so.tranid} email failed`, e.message);
                }
            }
        };

        return { execute };
    });
