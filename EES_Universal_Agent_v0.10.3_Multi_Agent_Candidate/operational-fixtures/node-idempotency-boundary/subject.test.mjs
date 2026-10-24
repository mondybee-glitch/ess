import test from 'node:test';
import assert from 'node:assert/strict';
import { IdempotencyLedger } from './subject.mjs';
test('repeated sequential key reuses result', async () => {
 const ledger = new IdempotencyLedger(); let effects = 0;
 const operation = async () => ({id: ++effects});
 assert.deepEqual(await ledger.execute('order-1', operation), {id:1});
 assert.deepEqual(await ledger.execute('order-1', operation), {id:1});
 assert.equal(effects, 1);
});
test('missing key is rejected', async () => {
 const ledger = new IdempotencyLedger();
 await assert.rejects(() => ledger.execute('', async () => true), /key required/);
});
