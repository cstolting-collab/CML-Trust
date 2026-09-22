# Real-workload performance evidence

This is a standing evidence rule for optimization work.

A performance or efficiency claim is not promoted from implementation evidence
to verified performance evidence until a supported workload has been executed.

Required conditions:

1. The workload corresponds to a real supported path, shipped example, or
   documented user operation.
2. Baseline and treatment produce equivalent expected results before timing.
3. Exact revision, runtime, dependency/provider versions, workload size, and
   operation count are recorded.
4. Baseline and treatment are measured in the same environment where practical.
5. Startup and steady-state work are separated unless startup is itself the
   performance claim.
6. Measurements use repeated observations and alternate baseline/treatment
   order where practical.
7. Results report a distribution, not a single best number: at minimum median
   and a spread measure such as p95 or min/max, plus absolute and relative
   deltas.
8. Faster execution does not override changed semantics, permissions, error
   mapping, retry safety, cancellation, integrity, size limits, or other
   compatibility boundaries.
9. A harness that has not run against the required live provider is
   `benchmark_ready`, not verified evidence.
10. Upstream submission decisions preserve the unresolved performance question
    when material benefit is part of maintainer acceptance.

Status vocabulary:

```text
benchmark_ready
measured
verified_performance_evidence
performance_hold
```

CI may verify that benchmark code formats, type-checks, and executes in supported
test environments. CI alone does not establish the external performance result.
