import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const input = JSON.parse(fs.readFileSync(path.join(here, "input.json"), "utf8"));
const expected = JSON.parse(fs.readFileSync(path.join(here, "expected.json"), "utf8"));

class CanonicalRegistry {
  #records = new Map();

  define(record) {
    if (this.#records.has(record.id)) throw new Error("record already exists");
    this.#records.set(record.id, {
      revision: record.revision,
      values: structuredClone(record.values),
      locked: new Set(record.lockedFields),
    });
  }

  snapshot(id) {
    const record = this.#require(id);
    return {
      revision: record.revision,
      values: structuredClone(record.values),
      lockedFields: [...record.locked].sort(),
    };
  }

  unlock(id, fields, authorization) {
    if (!authorization?.authorized) {
      return { accepted: false, reason: "UNAUTHORIZED_UNLOCK" };
    }
    const record = this.#require(id);
    for (const field of fields) record.locked.delete(field);
    record.revision += 1;
    return { accepted: true, reason: "AUTHORIZED_UNLOCK" };
  }

  commit(id, field, value) {
    const record = this.#require(id);
    if (record.locked.has(field)) {
      return { accepted: false, reason: "LOCKED_FIELD_CONFLICT" };
    }
    record.values[field] = structuredClone(value);
    record.revision += 1;
    return { accepted: true, reason: "COMMITTED" };
  }

  #require(id) {
    const record = this.#records.get(id);
    if (!record) throw new Error("record not found");
    return record;
  }
}

function evaluateCandidate(snapshot, candidate) {
  if (candidate.recordRevision !== snapshot.revision) {
    return { accepted: false, reason: "STALE_PROJECTION", mutationApplied: false };
  }
  if (snapshot.lockedFields.includes(candidate.field)) {
    return { accepted: false, reason: "LOCKED_FIELD_CONFLICT", mutationApplied: false };
  }
  return { accepted: true, reason: "ALLOWED_CHANGE", mutationApplied: false };
}

const registry = new CanonicalRegistry();
registry.define(input.record);

const beforeReject = registry.snapshot(input.record.id);
const reject = evaluateCandidate(beforeReject, input.rejectCandidate);
assert.deepEqual(reject, expected.reject);

const afterReject = registry.snapshot(input.record.id);
assert.deepEqual(afterReject, expected.canonicalAfterReject);
assert.deepEqual(afterReject, beforeReject, "reject mutated canonical state");

const unlock = registry.unlock(
  input.record.id,
  [input.acceptCandidate.field],
  { authorized: true },
);
assert.deepEqual(unlock, expected.unlock);

const unlocked = registry.snapshot(input.record.id);
const acceptCandidate = {
  ...input.acceptCandidate,
  recordRevision: unlocked.revision,
};
const accept = evaluateCandidate(unlocked, acceptCandidate);
assert.deepEqual(accept, expected.accept);

const beforeCommit = registry.snapshot(input.record.id);
assert.deepEqual(
  beforeCommit.values,
  expected.canonicalAfterReject.values,
  "accept evaluation mutated canonical state before explicit commit",
);

const commit = registry.commit(
  input.record.id,
  acceptCandidate.field,
  acceptCandidate.proposedValue,
);
assert.deepEqual(commit, expected.commit);

const canonicalFinal = registry.snapshot(input.record.id);
assert.deepEqual(canonicalFinal, expected.canonicalFinal);

console.log(JSON.stringify({
  reject,
  canonicalAfterReject: afterReject,
  unlock,
  accept,
  commit,
  canonicalFinal,
}, null, 2));
console.log("REPLAY FIXTURE: PASS");
