## Metadata Naming Conventions and Units

* All `_TIME` fields are Unix timestamps, and are eventually removed from the metric sending part (e.g. there is no need to aggregate a bunch of absolute unix timestamps...).

* All `_DURATION` and `_LATENCY` fields are in Seconds

* Counters are flattened automatically to `COUNTERS.<counter-group>.<counter-name>`

* `JOB_STATUS` is treated in a special way since it's an enum. It is falttened out to `JOB_STATUS.<status>` with a value of 1. This allows easy aggregation of job counts per status.

