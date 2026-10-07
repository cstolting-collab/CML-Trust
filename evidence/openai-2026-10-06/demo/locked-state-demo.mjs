class CanonicalRegistry {
  #records = new Map();

  define(id, values, lockedFields = []) {
    if (this.#records.has(id)) throw new Error("record already exists");
    this.#records.set(id, {
      revision: 1,
      values: structuredClone(values),
      locked: new Set(lockedFields),
    });
  }

  snapshot(id) {
    const r = this.#require(id);
    return Object.freeze({
      id,
      revision: r.revision,
      values: structuredClone(r.values),
      lockedFields: Object.freeze([...r.locked].sort()),
    });
  }

  unlock(id, fields, authorization) {
    if (!authorization?.authorized) {
      return Object.freeze({ accepted: false, reason: "UNAUTHORIZED_UNLOCK" });
    }
    const r = this.#require(id);
    for (const field of fields) r.locked.delete(field);
    r.revision += 1;
    return Object.freeze({ accepted: true, reason: "AUTHORIZED_UNLOCK" });
  }

  commit(id, field, value) {
    const r = this.#require(id);
    if (r.locked.has(field)) {
      return Object.freeze({ accepted: false, reason: "LOCKED_FIELD_CONFLICT" });
    }
    r.values[field] = structuredClone(value);
    r.revision += 1;
    return Object.freeze({ accepted: true, reason: "COMMITTED" });
  }

  #require(id) {
    const r = this.#records.get(id);
    if (!r) throw new Error("record not found");
    return r;
  }
}

function evaluateCandidate(snapshot, candidate, authorization = {}) {
  if (candidate.recordRevision !== snapshot.revision) {
    return Object.freeze({
      accepted: false,
      reason: "STALE_PROJECTION",
      mutationApplied: false,
      canonical: false,
    });
  }

  if (
    snapshot.lockedFields.includes(candidate.field) &&
    !authorization.allowOverride
  ) {
    return Object.freeze({
      accepted: false,
      reason: "LOCKED_FIELD_CONFLICT",
      mutationApplied: false,
      canonical: false,
    });
  }

  return Object.freeze({
    accepted: true,
    reason: "ALLOWED_CHANGE",
    mutationApplied: false,
    canonical: false,
  });
}

const registry = new CanonicalRegistry();

registry.define(
  "marine_07",
  { weapon: "rifle_A" },
  ["weapon"],
);

const lockedSnapshot = registry.snapshot("marine_07");

const candidate = Object.freeze({
  recordRevision: lockedSnapshot.revision,
  field: "weapon",
  proposedValue: "rifle_B",
});

const first = evaluateCandidate(lockedSnapshot, candidate);

console.log("1. locked evaluation");
console.log(first);

if (first.accepted !== false || first.reason !== "LOCKED_FIELD_CONFLICT") {
  throw new Error("expected locked candidate to be rejected");
}

if (registry.snapshot("marine_07").values.weapon !== "rifle_A") {
  throw new Error("candidate evaluation mutated canonical state");
}

const unlock = registry.unlock(
  "marine_07",
  ["weapon"],
  { authorized: true },
);

console.log("\n2. authorized unlock");
console.log(unlock);

const unlockedSnapshot = registry.snapshot("marine_07");
const sameCandidate = Object.freeze({
  ...candidate,
  recordRevision: unlockedSnapshot.revision,
});

const second = evaluateCandidate(unlockedSnapshot, sameCandidate);

console.log("\n3. same proposed value after authorized unlock");
console.log(second);

if (second.accepted !== true || second.reason !== "ALLOWED_CHANGE") {
  throw new Error("expected candidate to be accepted after authorized unlock");
}

if (registry.snapshot("marine_07").values.weapon !== "rifle_A") {
  throw new Error("evaluation must still not mutate canonical state");
}

const commit = registry.commit(
  "marine_07",
  sameCandidate.field,
  sameCandidate.proposedValue,
);

console.log("\n4. explicit canonical commit");
console.log(commit);
console.log(registry.snapshot("marine_07"));

if (registry.snapshot("marine_07").values.weapon !== "rifle_B") {
  throw new Error("explicit commit did not update canonical state");
}
