/**
 * TORS Late Order Notice
 *
 * Finds open sales orders that are running late, emails the customer from the
 * account's salesperson through a HubSpot sequence, and creates a HubSpot call
 * task for the salesperson when the order is over $1,000 or the customer is new.
 *
 * Late = an unshipped item line whose expected ship date (or the order's ship
 * date) has passed, or an order still not shipped 5+ days after it was entered.
 * House accounts (Sales Rep TORS, TORS Online or blank) are skipped.
 *
 * Setup and testing steps: netsuite/scripts/README-late-order-notice.md
 *
 * @NApiVersion 2.1
 * @NScriptType MapReduceScript
 */
define(['N/query', 'N/https', 'N/record', 'N/runtime', 'N/email', 'N/format', 'N/log'],
    (query, https, record, runtime, email, format, log) => {

        const HUBSPOT = 'https://api.hubapi.com';
        const SECRET = '{custsecret_tors_hubspot_token}';
        const HOUSE_REPS = [102570, 132]; // TORS, TORS Online
        const BIG_ORDER = 1000;
        const NEW_CUSTOMER_DAYS = 90;
        const LATE_AFTER_DAYS = 5;

        const param = (id) => runtime.getCurrentScript().getParameter({ name: id });
        const settings = () => ({
            dryRun: param('custscript_tors_lon_dryrun') !== false,
            sequenceId: param('custscript_tors_lon_sequence_id'),
            maxPerRun: Number(param('custscript_tors_lon_max')) || 25,
            resendDays: Number(param('custscript_tors_lon_resend_days')) || 7,
            summaryTo: param('custscript_tors_lon_summary_to')
        });

        // ---------- HubSpot ----------

        const hubspot = (method, path, body) => {
            const headers = {
                Authorization: https.createSecureString({ input: 'Bearer ' + SECRET }),
                'Content-Type': 'application/json'
            };
            const options = { url: HUBSPOT + path, headers };
            if (body) options.body = JSON.stringify(body);
            const res = method === 'GET' ? https.get(options)
                : method === 'PATCH' ? https.request({ method: https.Method.PATCH, ...options })
                    : https.post(options);
            const ok = res.code >= 200 && res.code < 300;
            let data = null;
            try { data = res.body ? JSON.parse(res.body) : null; } catch (e) { data = res.body; }
            if (!ok) log.audit('HubSpot ' + method + ' ' + path, res.code + ' ' + res.body);
            return { ok, code: res.code, data };
        };

        const findOwner = (repEmail) => {
            const res = hubspot('GET', '/crm/v3/owners?limit=1&email=' + encodeURIComponent(repEmail));
            const owner = res.ok && res.data.results && res.data.results[0];
            return owner ? { ownerId: owner.id, userId: owner.userId } : null;
        };

        const upsertContact = (o, ownerId) => {
            const props = {
                tors_late_order_number: o.tranid,
                tors_late_order_po: o.po || 'not given',
                tors_late_order_items: o.itemsText,
                tors_late_order_new_date: o.newDate
            };
            const found = hubspot('POST', '/crm/v3/objects/contacts/search', {
                filterGroups: [{ filters: [{ propertyName: 'email', operator: 'EQ', value: o.email }] }],
                properties: ['hubspot_owner_id', 'firstname'],
                limit: 1
            });
            const existing = found.ok && found.data.results && found.data.results[0];
            if (existing) {
                if (!existing.properties.hubspot_owner_id) props.hubspot_owner_id = ownerId;
                hubspot('PATCH', '/crm/v3/objects/contacts/' + existing.id, { properties: props });
                return existing.id;
            }
            props.email = o.email;
            props.company = o.company;
            props.hubspot_owner_id = ownerId;
            const created = hubspot('POST', '/crm/v3/objects/contacts', { properties: props });
            return created.ok ? created.data.id : null;
        };

        const enroll = (contactId, owner, repEmail, sequenceId) =>
            hubspot('POST', '/automation/v4/sequences/enrollments?userId=' + owner.userId, {
                contactId: String(contactId),
                sequenceId: String(sequenceId),
                senderEmail: repEmail
            });

        const createTask = (contactId, ownerId, subject, bodyText, priority) =>
            hubspot('POST', '/crm/v3/objects/tasks', {
                properties: {
                    hs_timestamp: new Date().toISOString(),
                    hs_task_subject: subject,
                    hs_task_body: bodyText,
                    hs_task_status: 'NOT_STARTED',
                    hs_task_priority: priority,
                    hs_task_type: 'CALL',
                    hubspot_owner_id: String(ownerId)
                },
                associations: [{
                    to: { id: String(contactId) },
                    types: [{ associationCategory: 'HUBSPOT_DEFINED', associationTypeId: 204 }]
                }]
            });

        // ---------- NetSuite ----------

        const lateOrdersSql = (resendDays) => `
            SELECT so.id, so.tranid, so.otherrefnum AS po, so.email AS so_email,
                   ABS(so.foreigntotal) AS amount, TO_CHAR(so.trandate,'YYYY-MM-DD') AS order_date,
                   c.id AS cust_id, c.companyname AS company, c.email AS cust_email,
                   TO_CHAR(c.firstsaledate,'YYYY-MM-DD') AS first_sale,
                   CASE WHEN c.firstsaledate IS NULL OR c.firstsaledate >= CURRENT_DATE - ${NEW_CUSTOMER_DAYS}
                        THEN 'T' ELSE 'F' END AS new_customer,
                   e.id AS rep_id, e.email AS rep_email, e.firstname AS rep_first
            FROM transaction so
            JOIN customer c ON c.id = so.entity
            JOIN employee e ON e.id = c.salesrep
            WHERE so.type = 'SalesOrd'
              AND so.status IN ('B','D','E')
              AND c.salesrep NOT IN (${HOUSE_REPS.join(',')})
              AND (so.custbody_tors_late_notice_dt IS NULL
                   OR so.custbody_tors_late_notice_dt <= CURRENT_DATE - ${resendDays})
              AND EXISTS (
                SELECT 1 FROM transactionline tl
                WHERE tl.transaction = so.id AND tl.mainline = 'F'
                  AND tl.itemtype IN ('InvtPart','NonInvtPart','Assembly','Kit')
                  AND ABS(tl.quantity) > NVL(tl.quantityshiprecv,0)
                  AND (NVL(tl.expectedshipdate, so.shipdate) < CURRENT_DATE
                       OR so.trandate <= CURRENT_DATE - ${LATE_AFTER_DAYS}))
            ORDER BY CASE WHEN ABS(so.foreigntotal) > ${BIG_ORDER} THEN 0 ELSE 1 END, so.trandate`;

        const lateLines = (soId) => query.runSuiteQL({
            query: `SELECT BUILTIN.DF(tl.item) AS item,
                           ABS(tl.quantity) - NVL(tl.quantityshiprecv,0) AS open_qty,
                           TO_CHAR(NVL(tl.expectedshipdate, so.shipdate),'MM/DD/YYYY') AS exp_date,
                           NVL(tl.expectedshipdate, so.shipdate) AS exp_raw
                    FROM transactionline tl JOIN transaction so ON so.id = tl.transaction
                    WHERE tl.transaction = ? AND tl.mainline = 'F'
                      AND tl.itemtype IN ('InvtPart','NonInvtPart','Assembly','Kit')
                      AND ABS(tl.quantity) > NVL(tl.quantityshiprecv,0)`,
            params: [soId]
        }).asMappedResults();

        const today = () => format.format({ value: new Date(), type: format.Type.DATE });

        // ---------- Map/Reduce stages ----------

        const getInputData = () => {
            const s = settings();
            const paged = query.runSuiteQLPaged({ query: lateOrdersSql(s.resendDays), pageSize: 1000 });
            const out = [];
            paged.pageRanges.forEach((range) => {
                paged.fetch({ index: range.index }).data.asMappedResults().forEach((r) => out.push(r));
            });
            log.audit('Late orders found', out.length + ' (sending up to ' + s.maxPerRun + ', dry run: ' + s.dryRun + ')');
            return out.slice(0, s.maxPerRun);
        };

        const map = (context) => {
            const s = settings();
            const o = JSON.parse(context.value);
            o.email = o.so_email || o.cust_email;
            const result = { so: o.tranid, company: o.company, rep: o.rep_first, amount: o.amount,
                emailed: false, task: false, note: '' };

            if (!o.email) { result.note = 'No customer email'; context.write({ key: 'skipped', value: JSON.stringify(result) }); return; }
            if (!o.rep_email) { result.note = 'Sales rep has no email'; context.write({ key: 'skipped', value: JSON.stringify(result) }); return; }

            const lines = lateLines(o.id);
            o.itemsText = lines.map((l) => l.item + ' (qty ' + l.open_qty + ')').join('; ').slice(0, 900);
            const latest = lines.reduce((m, l) => (l.exp_raw && (!m || l.exp_raw > m.exp_raw) ? l : m), null);
            o.newDate = latest && latest.exp_date ? latest.exp_date : 'to be confirmed';

            const needsCall = Number(o.amount) > BIG_ORDER || o.new_customer === 'T';
            const why = Number(o.amount) > BIG_ORDER ? 'Late order over $1,000' : 'Late order, new customer';

            if (s.dryRun) {
                result.note = 'DRY RUN: would email ' + o.email + ' as ' + o.rep_email
                    + (needsCall ? '; would create CALL task (' + why + ')' : '');
                log.audit('Dry run SO ' + o.tranid, result.note + ' | items: ' + o.itemsText + ' | new date: ' + o.newDate);
                context.write({ key: 'dryrun', value: JSON.stringify(result) });
                return;
            }

            const owner = findOwner(o.rep_email);
            if (!owner) { result.note = 'No HubSpot user for ' + o.rep_email; context.write({ key: 'skipped', value: JSON.stringify(result) }); return; }

            const contactId = upsertContact(o, owner.ownerId);
            if (!contactId) { result.note = 'Could not create HubSpot contact'; context.write({ key: 'skipped', value: JSON.stringify(result) }); return; }

            const enrolled = enroll(contactId, owner, o.rep_email, s.sequenceId);
            result.emailed = enrolled.ok;
            if (!enrolled.ok) {
                // Usually means the contact is already in a sequence. Hand it to the rep instead.
                createTask(contactId, owner.ownerId, 'Email ' + o.company + ': SO ' + o.tranid + ' is running late',
                    'The automatic late-order email could not go out (HubSpot said: ' + enrolled.code + '). '
                    + 'Please send it yourself. Items: ' + o.itemsText + '. Best date now: ' + o.newDate + '.', 'MEDIUM');
                result.note = 'Email failed (' + enrolled.code + '), task created for rep';
            }

            if (needsCall) {
                const task = createTask(contactId, owner.ownerId, 'CALL ' + o.company + ': SO ' + o.tranid + ' is late',
                    why + '. Order $' + Math.round(o.amount) + ', PO ' + (o.po || 'not given') + '. '
                    + 'Late items: ' + o.itemsText + '. Best date now: ' + o.newDate + '. '
                    + 'Ask if the date works or if they need it sooner (expedite, partial ship, or an alternate).', 'HIGH');
                result.task = task.ok;
            }

            if (result.emailed || result.task) {
                record.submitFields({ type: record.Type.SALES_ORDER, id: o.id,
                    values: { custbody_tors_late_notice_dt: new Date() },
                    options: { ignoreMandatoryFields: true } });
            }
            context.write({ key: result.emailed ? 'sent' : 'skipped', value: JSON.stringify(result) });
        };

        const reduce = (context) => {
            context.write({ key: context.key, value: JSON.stringify(context.values.map((v) => JSON.parse(v))) });
        };

        const summarize = (summary) => {
            const s = settings();
            const groups = {};
            summary.output.iterator().each((key, value) => { groups[key] = JSON.parse(value); return true; });
            summary.mapSummary.errors.iterator().each((key, err) => { log.error('Map error ' + key, err); return true; });

            const lines = [];
            Object.keys(groups).forEach((k) => {
                lines.push(k.toUpperCase() + ': ' + groups[k].length);
                groups[k].forEach((r) => lines.push('  SO ' + r.so + ', ' + r.company + ', $' + Math.round(r.amount)
                    + ', ' + r.rep + (r.task ? ', CALL task' : '') + (r.note ? ', ' + r.note : '')));
            });
            const text = 'Late order notices for ' + today() + (s.dryRun ? ' (DRY RUN, nothing sent)' : '') + '\n\n'
                + (lines.length ? lines.join('\n') : 'No late orders needed a notice today.');
            log.audit('Summary', text);
            if (s.summaryTo) {
                email.send({ author: Number(s.summaryTo), recipients: [Number(s.summaryTo)],
                    subject: 'Late order notices ' + today() + (s.dryRun ? ' (dry run)' : ''), body: text });
            }
        };

        return { getInputData, map, reduce, summarize };
    });
