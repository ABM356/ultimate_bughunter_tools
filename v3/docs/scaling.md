# Scaling Considerations

How HopeUp scales with load, where the bottlenecks are, and how we mitigate
them.

## Scaling targets

| Dimension           | v1.0 target     | Stretch target |
|---------------------|-----------------|----------------|
| Concurrent users    | 10,000          | 100,000        |
| Active scans / hr   | 1,000           | 10,000         |
| API requests / sec  | 2,000           | 20,000         |
| WebSocket sessions  | 5,000           | 50,000         |
| Stored findings     | 100M            | 1B             |
| p99 API latency     | < 300 ms        | < 200 ms       |

## Horizontal scaling

Stateless tiers (frontend, backend, worker) all sit behind a Kubernetes HPA.

| Component   | Replicas | HPA trigger              |
|-------------|----------|--------------------------|
| Frontend    | 3-15     | CPU 70%, mem 80%         |
| Backend     | 3-20     | CPU 70%, mem 80%         |
| Worker      | 3-30     | CPU 75% + Redis depth    |
| Beat        | 1 only   | singleton (must be 1)    |

PodDisruptionBudgets keep at least 2 replicas of each tier available during
voluntary disruption.

## Vertical scaling

- Postgres: start `db.r6g.large` (2 vCPU / 16 GB), step to `db.r6g.4xlarge`
  (16 / 128 GB) per environment.
- Redis: `cache.r6g.large` (2 vCPU / 13 GB) is enough for session + Celery
  broker for ~10k concurrent users. Move to `cache.r6g.2xlarge` once memory
  passes 60%.
- OpenSearch: 3x `r6g.large.search` data nodes baseline; scale data tier
  before master tier.

## Database bottlenecks

The relational database is the single most common scaling bottleneck.
Specific risks:

1. **Connection storm.** Workers + backend pods can exhaust Postgres'
   default 100 max_connections. Mitigation: PgBouncer in front of RDS (in
   transaction mode) so each pod can have many sessions but only a few real
   backend connections.
2. **Long-running queries.** Heavy scans block transactions. Mitigation:
   `statement_timeout = 30s` for the application user, `lock_timeout = 5s`
   for migrations.
3. **Hot-row contention** on `audit_log` and `scan_progress`. Mitigation:
   partition `audit_log` by month; write `scan_progress` to Redis Stream
   instead, persist summary to Postgres only on completion.
4. **Schema migration downtime.** Mitigation: backwards-compatible
   migrations only; the migration job runs in-place with the old code
   still serving traffic.

## Cache strategy

- **Redis** session store: 30-min TTL on user sessions; LRU eviction.
- **Redis** rate-limit counters: sliding-window with per-tenant key
  prefix.
- **OpenSearch** result cache: enabled per index (`index.queries.cache.enabled`).
- **CDN** in front of frontend: static assets cached at edge with a short
  TTL on the HTML wrapper and long TTLs on hashed asset filenames.

## Worker / queue scaling

Celery queues are partitioned so that long jobs (large scans) don't block
short jobs (notifications):

- `default` - misc fast tasks
- `scans`   - scan jobs (heavy, can exhaust workers)
- `reports` - report generation (CPU-bound)
- `notifications` - email / Slack (small, frequent)

Each queue has its own worker pool. The `worker-hpa` scales on Redis queue
depth — when `scans` backs up beyond 20 pending jobs per pod, more workers
spin up.

## OpenSearch / log scaling

- Indices roll daily (`scan-{tenant}-YYYY.MM.DD`) and the rollover policy
  shrinks to 1 shard / 0 replicas after 7 days for cold data.
- Hot tier (last 7 days): 3 nodes, 2 replicas, fast SSD.
- Warm tier: data routes to cheaper nodes once frozen.
- Aggressive logs (debug-level) are dropped at the Fluent Bit forwarder.

## CDN & static assets

- Next.js standalone build serves with built-in static asset hashing.
- Production: put CloudFront in front of the ingress for static asset
  acceleration; the ingress handles dynamic /api/* and /ws/*.

## Limits to watch

| Limit                      | Watch on                  | Threshold          |
|----------------------------|---------------------------|--------------------|
| AWS NAT GW per AZ          | NAT data                  | 5 Gbps sustained   |
| ALB target groups          | API listener              | 1000 targets       |
| RDS connections            | `pg_stat_activity`        | 80% of max         |
| Elasticsearch JVM heap     | OpenSearch metric         | 75% sustained      |
| Celery queue depth         | Prometheus exporter       | > 1000 backlog     |
| EKS pod density            | nodes / pods per node     | 90% of node IP cap |

## Cost optimization

- Workload node group runs on Spot (with on-demand fallback). System node
  group stays on-demand for stability.
- Karpenter (recommended over Cluster Autoscaler) bin-packs aggressively.
- S3 lifecycle: scan outputs expire after 90 days; reports go to
  Glacier after 1 year.
- Reserved instances or Savings Plans for steady-state capacity (system
  group + RDS + OpenSearch).

## Open questions

- **Per-customer dedicated regions.** Some enterprise prospects ask for a
  dedicated cell. Open how to deploy: lift the Helm chart into a per-cell
  EKS, or run a multi-tenant fleet with stronger isolation guarantees.
- **Real-time streaming reports.** Live findings with subscriptions imply
  a fan-out problem at high session counts. Consider GraphQL subscriptions
  with a dedicated subscription server.
- **Search-heavy workloads.** Once OpenSearch storage passes 1 TB / tenant,
  evaluate dedicated indexes per tenant or tiered storage tiers.
