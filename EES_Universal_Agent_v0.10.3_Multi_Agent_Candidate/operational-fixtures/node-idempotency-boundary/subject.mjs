// Minimal model of an idempotent request handler. In production, the key and effect
// must be committed atomically in durable storage.
export class IdempotencyLedger {
  #results = new Map();
  async execute(key, operation) {
    if (typeof key !== 'string' || key.trim() === '') throw new TypeError('idempotency key required');
    if (this.#results.has(key)) return this.#results.get(key);
    const result = await operation();
    this.#results.set(key, result);
    return result;
  }
}
