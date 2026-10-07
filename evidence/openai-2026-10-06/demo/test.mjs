import assert from "node:assert/strict";

class Registry {
  constructor() {
    this.revision = 1;
    this.value = "A";
    this.locked = true;
  }
  snapshot() {
    return Object.freeze({
      revision: this.revision,
      value: this.value,
      locked: this.locked,
    });
  }
  unlock(authorized) {
    if (!authorized) return { accepted: false, reason: "UNAUTHORIZED_UNLOCK" };
    this.locked = false;
    this.revision += 1;
    return { accepted: true, reason: "AUTHORIZED_UNLOCK" };
  }
}

function evaluate(snapshot, candidate) {
  if (candidate.revision !== snapshot.revision) {
    return { accepted: false, reason: "STALE_PROJECTION", mutationApplied: false };
  }
  if (snapshot.locked) {
    return { accepted: false, reason: "LOCKED_FIELD_CONFLICT", mutationApplied: false };
  }
  return { accepted: true, reason: "ALLOWED_CHANGE", mutationApplied: false };
}

const registry = new Registry();

const s1 = registry.snapshot();
const candidate1 = { revision: s1.revision, proposedValue: "B" };
const r1 = evaluate(s1, candidate1);

assert.equal(r1.accepted, false);
assert.equal(r1.reason, "LOCKED_FIELD_CONFLICT");
assert.equal(r1.mutationApplied, false);
assert.equal(registry.value, "A");

const unauthorized = registry.unlock(false);
assert.equal(unauthorized.accepted, false);
assert.equal(registry.locked, true);

const authorized = registry.unlock(true);
assert.equal(authorized.accepted, true);
assert.equal(registry.locked, false);

const stale = evaluate(registry.snapshot(), candidate1);
assert.equal(stale.accepted, false);
assert.equal(stale.reason, "STALE_PROJECTION");

const s2 = registry.snapshot();
const candidate2 = { revision: s2.revision, proposedValue: "B" };
const r2 = evaluate(s2, candidate2);

assert.equal(r2.accepted, true);
assert.equal(r2.reason, "ALLOWED_CHANGE");
assert.equal(r2.mutationApplied, false);
assert.equal(registry.value, "A");

console.log("CML public verification evidence: PASS");
