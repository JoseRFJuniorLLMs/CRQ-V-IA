Sim. **Para o CRQ-V-IA, eu usaria o HeraclitusDB para o log de auditoria e eventos**, mas **não para todo e qualquer log da aplicação**. Jogar `HTTP 200`, stack trace e mensagem de debug dentro de um event store imutável seria um jeito muito sofisticado de armazenar lixo para sempre.

A separação ideal seria esta:

| Tipo de log                              | Destino                      |
| ---------------------------------------- | ---------------------------- |
| Debug, access log HTTP, métricas, traces | OpenTelemetry / logs normais |
| Erros de aplicação                       | observabilidade convencional |
| Login/logout                             | **HeraclitusDB**             |
| Alterações de usuário/permissão          | **HeraclitusDB**             |
| Empresa adicionada/removida de lista     | **HeraclitusDB**             |
| Mudança de prioridade/status             | **HeraclitusDB**             |
| Importação da RFB                        | **HeraclitusDB**             |
| Publicação de nova competência           | **HeraclitusDB**             |
| Alteração/publicação de ruleset          | **HeraclitusDB**             |
| Score/snapshot usado em fiscalização     | **HeraclitusDB**             |
| Exportação CSV/XLSX                      | **HeraclitusDB**             |
| Mudança de configuração                  | **HeraclitusDB**             |
| Incidente de segurança                   | **HeraclitusDB**             |
| Release/deploy/rollback                  | **HeraclitusDB**             |
| Contract exit / exclusão                 | **HeraclitusDB**             |

O desenho que eu adotaria é:

```text
                    CRQ-V-IA
                        |
          +-------------+-------------+
          |                           |
          v                           v
    PostgreSQL                 Audit/Event Bus
  estado operacional                 |
                                      v
                                HeraclitusDB
                              log imutável
```

O PostgreSQL responde à pergunta:

> **“Qual é o estado atual?”**

O HeraclitusDB responde:

> **“Como chegamos até este estado?”**

Essa diferença é particularmente boa para o CRQ-V-IA.

Um evento poderia ter estrutura semelhante a:

```json
{
  "event_id": "019...",
  "tenant_id": "crq-v",
  "event_type": "PROSPECT_ADDED_TO_LIST",

  "actor_id": "user-42",
  "actor_role": "INSPECTOR",

  "entity_type": "establishment",
  "entity_id": "cnpj:12345678000199",

  "request_id": "req-...",
  "correlation_id": "corr-...",

  "software_release": "1.0.4",
  "commit_sha": "a32f7cd",

  "rfb_source_version": "2027-03",
  "rule_set_version": "CFQ-339-v4",

  "occurred_at": "2027-03-18T14:32:10Z",

  "payload": {
    "list_id": "list-123",
    "score": 82,
    "tier": "HIGH"
  }
}
```

E é exatamente aí que características do HeraclitusDB como **append-only, LSN/HLC, hash/Merkle e replay temporal** começam a ter utilidade real, em vez de serem apenas coisas bonitas escritas numa arquitetura.

### O maior ganho seria auditoria histórica

Imagine:

```text
09:00  empresa detectada na nova competência RFB
09:02  score = 74
09:05  fiscal adiciona à lista
09:10  prioridade muda para HIGH
10:30  coordenador atribui ao fiscal B
14:20  lista é exportada
16:00  regra regulatória é atualizada
```

No PostgreSQL você terá principalmente o estado atual.

No HeraclitusDB você pode reconstruir:

```text
state_at(09:02)
state_at(09:10)
state_at(14:20)
```

E responder:

> Qual regra estava ativa quando essa empresa foi selecionada?

> Qual versão da Receita foi utilizada?

> Quem colocou a empresa na lista?

> Qual score existia naquele momento?

> O registro foi alterado depois?

Isso encaixa perfeitamente com a `SPEC-0019`.

### Eu também usaria uma interface abstrata

Não colocaria código da aplicação chamando Heraclitus diretamente em cinquenta lugares.

Algo assim:

```python
class AuditSink:
    async def append(self, event: AuditEvent) -> None:
        ...
```

Implementações:

```text
PostgresAuditSink
HeraclitusAuditSink
CompositeAuditSink
```

Então a aplicação simplesmente faz:

```python
await audit.append(event)
```

E a configuração decide:

```env
AUDIT_POSTGRES=true
AUDIT_HERACLITUS=true
HERACLITUS_REQUIRED=false
```

Esse último é importante:

```text
HERACLITUS_REQUIRED=false
```

No começo, **se o HeraclitusDB cair, o CRQ-V-IA continua operando**.

Depois que ele provar estabilidade, você pode inverter:

```text
HeraclitusDB = source of truth do audit log
PostgreSQL   = projeção/index operacional
```

### E dá para criar uma prova fantástica do HeraclitusDB

Um verificador periódico poderia comparar:

```text
CRQ-V Audit Integrity
─────────────────────────────
PostgreSQL events      824.551
Heraclitus events      824.551

Missing events               0
Duplicate events             0
Hash mismatches              0

HLC ordering             VALID
Merkle verification      VALID
Replay                    VALID
Recovery test             PASS
```

Isso transforma o CRQ-V-IA em **workload real de validação do HeraclitusDB**, o que é muito mais valioso do que benchmark sintético.

### O que eu não colocaria no HeraclitusDB

Não mandaria:

```text
GET /favicon.ico 200
healthcheck OK
CSS loaded
query took 42ms
debug variable x=3
```

Esses continuam em logs convencionais.

Eu definiria três categorias:

```text
OBSERVABILITY
    logs descartáveis

AUDIT
    eventos relevantes e duráveis

EVIDENCE
    eventos que precisam permitir reconstrução histórica
```

O HeraclitusDB ficaria com **AUDIT + EVIDENCE**.

Então sim: **o log de auditoria do CRQ-V-IA é provavelmente um dos melhores lugares para usar e testar o HeraclitusDB**. Não como “banco de logs genérico”, mas como **event store imutável e verificável da história operacional do sistema**.


# SPEC-0020 — HeraclitusDB Audit & Evidence Event Store

Status: REQUIRED FOR EXPERIMENTAL INTEGRATION
Priority: P1
Repository: JoseRFJuniorLLMs/CRQ-V-IA
Integration: HeraclitusDB

Depends on:
- SPEC-0009 — Observability
- SPEC-0010 — LGPD and Security
- SPEC-0014 — Test and Acceptance
- SPEC-0018 — Full Implementation Compliance
- SPEC-0019 — Contractual Data Governance and Hardening

Purpose:
Use HeraclitusDB as an immutable, temporally ordered and verifiable
event store for audit and evidentiary events generated by CRQ-V-IA.

---

# 1. OBJECTIVE

Integrate HeraclitusDB into CRQ-V-IA as a specialized append-only
event store for:

AUDIT
and
EVIDENCE

The integration SHALL NOT initially replace PostgreSQL as the
operational database.

Initial architecture:

CRQ-V-IA
    |
    +---- PostgreSQL
    |       operational state
    |
    +---- Audit Pipeline
             |
             +---- PostgreSQL Audit
             |
             +---- HeraclitusDB

HeraclitusDB SHALL initially operate in shadow/dual-write mode.

---

# 2. DESIGN PRINCIPLE

PostgreSQL answers:

"What is the current state?"

HeraclitusDB answers:

"What happened, when, in which order, under which rules and data,
and how did the system arrive at the current state?"

The two responsibilities MUST remain separated.

---

# 3. NON-GOAL

HeraclitusDB SHALL NOT initially store generic application telemetry.

Do NOT use HeraclitusDB for routine events such as:

- HTTP 200 access logs;
- static asset requests;
- health checks;
- frontend debug logs;
- ordinary stack traces;
- CSS/JS resource logs;
- performance traces;
- low-value debug messages.

These remain under the conventional observability stack.

---

# 4. EVENT CLASSES

All emitted events MUST be classified into one of:

OBSERVABILITY
AUDIT
EVIDENCE

## OBSERVABILITY

Ephemeral operational information.

Examples:

HTTP request duration
CPU
memory
health checks
traces
debug information

Destination:

OpenTelemetry
application logs
metrics platform

NOT HeraclitusDB by default.

## AUDIT

Durable record of relevant user/system actions.

Destination:

PostgreSQL Audit + HeraclitusDB.

## EVIDENCE

Events necessary to reconstruct or demonstrate a historical
administrative/fiscal decision context.

Destination:

HeraclitusDB mandatory when integration is enabled.

---

# 5. AUDIT EVENTS

HeraclitusDB SHOULD receive at least:

AUTH_LOGIN_SUCCESS
AUTH_LOGIN_FAILURE
AUTH_LOGOUT

USER_CREATED
USER_DISABLED
USER_ROLE_CHANGED

COMPANY_VIEWED

LIST_CREATED
LIST_UPDATED
LIST_DELETED

PROSPECT_ADDED_TO_LIST
PROSPECT_REMOVED_FROM_LIST
PROSPECT_STATUS_CHANGED
PROSPECT_PRIORITY_CHANGED
PROSPECT_ASSIGNED

SAVED_SEARCH_CREATED
SAVED_SEARCH_UPDATED
SAVED_SEARCH_DELETED

EXPORT_REQUESTED
EXPORT_GENERATED
EXPORT_DOWNLOADED
EXPORT_EXPIRED

RFB_IMPORT_STARTED
RFB_IMPORT_VALIDATED
RFB_IMPORT_PUBLISHED
RFB_IMPORT_FAILED
RFB_IMPORT_ROLLED_BACK

CRQ_IMPORT_STARTED
CRQ_IMPORT_DRY_RUN
CRQ_IMPORT_CONFIRMED
CRQ_IMPORT_COMPLETED
CRQ_IMPORT_FAILED

RULESET_CREATED
RULESET_REVIEWED
RULESET_APPROVED
RULESET_ACTIVATED
RULESET_RETIRED

REGULATORY_SCORE_CALCULATED
PROSPECT_SNAPSHOT_CREATED

CNPJ_VERIFICATION_REQUESTED
CNPJ_VERIFICATION_COMPLETED
CNPJ_VERIFICATION_FAILED

SUPPRESSION_CREATED
SUPPRESSION_REMOVED

INCIDENT_CREATED
INCIDENT_UPDATED
INCIDENT_RESOLVED

RELEASE_DEPLOYED
RELEASE_ROLLED_BACK

CHANGE_REQUEST_APPROVED

BACKUP_CREATED
RESTORE_TEST_COMPLETED

CONTRACT_EXIT_STARTED
CONTRACT_EXPORT_GENERATED
CONTRACT_EXPORT_CONFIRMED
CONTRACT_DATA_DELETION_APPROVED
CONTRACT_DATA_DELETION_COMPLETED

---

# 6. EVENT ENVELOPE

Every event SHALL use a common immutable envelope.

Example:

{
  "event_id": "019...",
  "event_type": "PROSPECT_ADDED_TO_LIST",
  "event_class": "EVIDENCE",

  "tenant_id": "crq-v",

  "actor": {
    "id": "user-42",
    "role": "INSPECTOR",
    "type": "HUMAN"
  },

  "entity": {
    "type": "establishment",
    "id": "cnpj:12345678000199"
  },

  "request_id": "...",
  "correlation_id": "...",

  "software": {
    "version": "1.0.4",
    "commit_sha": "abcdef1",
    "database_revision": "0042"
  },

  "data_context": {
    "rfb_source_version": "2027-03",
    "rule_set_version": "CFQ-339-v4"
  },

  "payload": {},

  "occurred_at": "2027-03-18T14:32:10.123Z",

  "schema_version": 1
}

---

# 7. EVENT ID

event_id MUST be globally unique.

Preferred options:

UUIDv7
or equivalent time-sortable identifier.

event_id MUST NOT depend exclusively on database auto-increment IDs.

---

# 8. TIME

Application timestamps SHALL use UTC internally.

HeraclitusDB MAY add its own HLC timestamp.

Store separately:

occurred_at
received_at
hlc_timestamp
lsn

occurred_at:
time reported by producer.

received_at:
time event entered HeraclitusDB.

hlc_timestamp:
ordering generated by HeraclitusDB.

lsn:
HeraclitusDB logical sequence number.

Never overwrite occurred_at with received_at.

---

# 9. ORDERING

HeraclitusDB SHALL provide canonical ingestion order using:

LSN
and/or
HLC.

Event consumers MUST NOT assume client timestamps are perfectly ordered.

For events with the same correlation_id, the system SHOULD preserve
logical causal ordering when possible.

---

# 10. PAYLOAD POLICY

Payload MUST contain only information required to understand or
reconstruct the event.

DO NOT place in payload:

passwords
access tokens
refresh tokens
session secrets
API credentials
private keys
authorization headers
raw sensitive HTTP bodies

CRQ_CONFIDENTIAL information SHALL be minimized.

---

# 11. EVENT SCHEMA VERSIONING

Every event SHALL contain:

schema_version

Schemas SHALL be backward compatible when possible.

Breaking schema changes REQUIRE a new version.

Example:

PROSPECT_ADDED_TO_LIST:v1
PROSPECT_ADDED_TO_LIST:v2

Old events MUST remain readable.

---

# 12. AUDIT SINK ABSTRACTION

Application code SHALL NOT depend directly on the HeraclitusDB client.

Create abstraction:

AuditSink

Interface concept:

append(event)
append_batch(events)
health()
flush()

Implementations:

PostgresAuditSink
HeraclitusAuditSink
CompositeAuditSink

Application code SHALL call only AuditSink.

---

# 13. COMPOSITE SINK

CompositeAuditSink SHALL support writing to multiple destinations.

Initial:

CompositeAuditSink(
    PostgresAuditSink,
    HeraclitusAuditSink
)

Heraclitus integration MUST therefore remain replaceable.

---

# 14. FEATURE FLAGS

Configuration:

AUDIT_POSTGRES_ENABLED=true

AUDIT_HERACLITUS_ENABLED=false

AUDIT_HERACLITUS_REQUIRED=false

HERACLITUS_ENDPOINT=
HERACLITUS_DATABASE=
HERACLITUS_TENANT=

Initial production recommendation:

AUDIT_POSTGRES_ENABLED=true
AUDIT_HERACLITUS_ENABLED=true
AUDIT_HERACLITUS_REQUIRED=false

---

# 15. INITIAL FAILURE SEMANTICS

During experimental/shadow mode:

HeraclitusDB failure SHALL NOT interrupt core CRQ-V-IA functionality.

If HeraclitusDB is unavailable:

1. operational transaction completes;
2. PostgreSQL audit remains authoritative fallback;
3. event enters retry queue/outbox;
4. alert is generated;
5. reconciliation runs after recovery.

This is mandatory during Phase 1.

---

# 16. OUTBOX PATTERN

Implement transactional outbox.

PostgreSQL transaction:

business state update
+
audit event insert
+
outbox record

commit atomically.

Background worker publishes the outbox event to HeraclitusDB.

This prevents:

business transaction committed
but event permanently lost.

---

# 17. OUTBOX TABLE

Create:

audit_outbox

Fields:

id
event_id
tenant_id
event_type
payload_json
created_at

publish_attempts
last_attempt_at
next_attempt_at

published_at
heraclitus_lsn
heraclitus_hlc

status
last_error

status:

PENDING
PUBLISHING
PUBLISHED
FAILED
DEAD_LETTER

---

# 18. DELIVERY SEMANTICS

The integration SHALL assume:

AT-LEAST-ONCE DELIVERY

Therefore Heraclitus writes MUST be idempotent.

event_id SHALL be the idempotency key.

Publishing the same event twice MUST NOT generate two logical audit events.

---

# 19. DUPLICATE HANDLING

HeraclitusDB MUST detect duplicate event_id.

Expected result:

first append:
ACCEPTED

subsequent identical append:
ALREADY_EXISTS / IDEMPOTENT_SUCCESS

same event_id with different payload:
INTEGRITY_ERROR

The last case MUST generate a security alert.

---

# 20. RETRY

Retry strategy:

exponential backoff
+
bounded jitter.

Example:

1 s
2 s
4 s
8 s
...
maximum configurable.

After retry exhaustion:

DEAD_LETTER

Dead-letter records MUST remain visible to administrators.

---

# 21. BACKPRESSURE

HeraclitusDB latency SHALL NOT propagate uncontrolled latency to the
main request path.

Normal application requests SHOULD NOT synchronously wait for
HeraclitusDB during shadow mode.

Use:

transactional outbox
+
background publisher.

---

# 22. HERACLITUS STREAM PARTITIONING

Suggested logical stream:

tenant_id

Optional secondary key:

event_class
or
entity_type.

Avoid excessive stream fragmentation.

Recommended initial stream:

crq-v:audit

---

# 23. APPEND-ONLY

Events stored in HeraclitusDB SHALL NOT support ordinary:

UPDATE
DELETE

Corrections SHALL be represented by new events.

Example:

incorrect event
→ EVENT_CORRECTION

Do not rewrite history.

---

# 24. CORRECTION EVENTS

Create event type:

AUDIT_CORRECTION

Fields:

corrected_event_id
reason
corrected_by
corrected_at
replacement_data

Original event remains present.

---

# 25. MERKLE INTEGRITY

HeraclitusDB SHOULD produce Merkle-based integrity verification over
audit segments.

Maintain:

segment_id
first_lsn
last_lsn
event_count
merkle_root
created_at

---

# 26. PERIODIC VERIFICATION

Run periodic integrity task.

Example:

daily:

verify latest completed segments.

weekly:

verify full audit range or rolling historical window.

Store result:

audit_integrity_check

Fields:

id
started_at
completed_at
first_lsn
last_lsn
events_checked
segments_checked
merkle_status
chain_status
errors
software_version

---

# 27. INTEGRITY API

Create restricted endpoint:

GET /api/v1/admin/audit/integrity

Return:

{
  "status": "VALID",
  "last_verified_lsn": 845223,
  "events_checked": 845223,
  "segments_checked": 128,
  "missing_events": 0,
  "hash_mismatches": 0,
  "last_check": "..."
}

Only authorized roles may access detailed information.

---

# 28. RECONCILIATION

Implement reconciliation between PostgreSQL and HeraclitusDB.

Command:

python -m app.audit.reconcile

Compare:

event_id
event_type
tenant
timestamp
payload_hash

Output:

postgres_total
heraclitus_total
missing_in_heraclitus
missing_in_postgres
duplicates
hash_mismatches

---

# 29. RECONCILIATION SAFETY

Reconciliation MUST NOT silently repair mismatches.

First:

detect
report
classify

Then:

optionally republish missing events after explicit rule allows it.

Conflicting payload hashes require manual/security review.

---

# 30. EVENT REPLAY

HeraclitusDB SHALL support replay by:

LSN range
HLC range
time range
tenant
entity
correlation_id
event_type

Example:

replay all events for one company:

entity_id = cnpj:...

---

# 31. HISTORICAL RECONSTRUCTION

Support reconstruction of selected operational state from events.

Initial supported projections:

saved list membership
prospect workflow status
priority
assignment
suppression state
ruleset lifecycle

The replay engine is evidentiary/debug-oriented.

It SHALL NOT initially replace PostgreSQL production reads.

---

# 32. TIME-TRAVEL AUDIT

Provide administrative query concept:

GET /api/v1/admin/audit/entity/{id}/timeline

and optionally:

GET /api/v1/admin/audit/entity/{id}/state-at?timestamp=...

This is read-only.

---

# 33. EVENT PROJECTIONS

HeraclitusDB events MAY generate projections for:

timeline
statistics
audit reports
security analysis

Projection failures MUST NOT mutate the source event stream.

---

# 34. CRQ-V EXAMPLE

Given:

09:00 RFB_IMPORT_PUBLISHED

09:02 REGULATORY_SCORE_CALCULATED

09:05 PROSPECT_ADDED_TO_LIST

09:10 PROSPECT_PRIORITY_CHANGED

10:30 PROSPECT_ASSIGNED

14:20 EXPORT_GENERATED

16:00 RULESET_ACTIVATED

HeraclitusDB must allow reconstruction of:

which data version existed;
which score existed;
which rule set existed;
who performed each action;
the exact order of events.

---

# 35. SOURCE CONTEXT

Events related to prospecting SHALL include where applicable:

rfb_source_version
rfb_source_hash
rule_set_version
software_release
prospect_snapshot_id

This allows later legal/administrative explanation.

---

# 36. EXPORT EVENTS

EXPORT_GENERATED SHOULD store:

export_id
saved_list_id
query_snapshot_hash
record_count
format
file_hash
expires_at

Do NOT store the full export file inside the audit event.

---

# 37. RELEASE EVENTS

RELEASE_DEPLOYED SHALL store:

release_id
version
commit_sha
container_digest
database_revision
ruleset_version
deployed_by
environment

---

# 38. RULESET EVENTS

RULESET_ACTIVATED SHALL store:

rule_set_version
previous_rule_set
approved_by
approval_reference
rule_count
source_document_hash

---

# 39. RFB INGEST EVENTS

RFB_IMPORT_PUBLISHED SHALL store:

source_version
competence
source_files
aggregate_hash
record_count
quality_status
previous_version

---

# 40. SECURITY EVENTS

HeraclitusDB SHOULD receive:

AUTH_BRUTE_FORCE_DETECTED
PRIVILEGE_CHANGE
ADMIN_LOGIN
AUDIT_INTEGRITY_FAILURE
SECRET_ROTATION
SECURITY_INCIDENT
VULNERABILITY_EXCEPTION_APPROVED

Do NOT write secret values.

---

# 41. LGPD INCIDENT EVENTS

Events involving security incidents SHALL reference:

incident_id

Do not duplicate unnecessary personal data into the immutable log.

Detailed incident data may remain in the controlled incident store.

---

# 42. TENANT ISOLATION

Every Heraclitus audit event MUST contain tenant_id.

Queries MUST enforce tenant isolation.

Cross-tenant access is forbidden except for explicitly authorized
system-level security operations.

---

# 43. DATA RETENTION

Audit retention SHALL follow contractual and legal requirements.

HeraclitusDB immutability does NOT mean infinite retention for every
data category.

Design retention by event class.

For events containing personal data:

minimize payload before append.

Deletion/legal-retention requirements SHALL be addressed through
event design rather than careless permanent copying.

---

# 44. PAYLOAD REDACTION

Before append:

AuditRedactor SHALL process the event.

Remove:

password
token
secret
authorization headers
private certificate material

Mask or omit personal data where unnecessary.

---

# 45. CANONICAL SERIALIZATION

For hashing and comparison, serialize events deterministically.

Recommended:

canonical JSON

Requirements:

stable key ordering
stable UTF-8 representation
no insignificant whitespace differences
normalized timestamps

---

# 46. PAYLOAD HASH

Each event SHOULD contain:

payload_hash

Calculated over canonical payload.

This enables cross-store verification without exposing full payload.

---

# 47. HASH MODEL

Suggested values:

payload_hash
event_hash

event_hash SHOULD incorporate immutable envelope + payload_hash.

HeraclitusDB internal Merkle structures remain independent.

---

# 48. PERFORMANCE TARGET

Audit publishing MUST NOT materially affect ordinary API latency.

Shadow-mode target:

request-path added latency:
< 5 ms P95

because synchronous Heraclitus commit is not required.

Outbox processing:

configurable batch size.

Suggested starting value:

100–1000 events/batch.

Benchmark instead of assuming optimal size.

---

# 49. THROUGHPUT BENCHMARK

Create benchmark scenarios:

1 event/sec
10 events/sec
100 events/sec
1000 events/sec

Measure:

append throughput
P50
P95
P99
CPU
memory
disk
batch efficiency

The objective is validation, not arbitrary throughput competition.

---

# 50. SOAK TEST

Run prolonged test.

Minimum recommended:

24 hours.

Preferred for Heraclitus validation:

72 hours+

Generate realistic event distribution rather than identical synthetic
records only.

---

# 51. CRASH TEST

Test:

kill -9 HeraclitusDB during append.

Expected:

CRQ-V-IA continues working.

Outbox remains intact.

After restart:

publishing resumes.

No event loss.

No duplicate logical events.

---

# 52. POWER-LOSS / ABRUPT TERMINATION TEST

Simulate abrupt Heraclitus termination during segment/WAL writes.

Verify:

startup recovery
segment integrity
LSN continuity
Merkle integrity
idempotent replay

---

# 53. NETWORK PARTITION TEST

Block CRQ-V-IA → Heraclitus network connectivity.

Expected:

outbox grows;
core application remains available;
alerts trigger;
reconnection drains backlog;
ordering remains explainable.

---

# 54. SLOW HERACLITUS TEST

Inject high append latency.

Ensure publisher backpressure does not exhaust:

DB pool
memory
worker threads
disk.

---

# 55. DUPLICATE TEST

Republish same event repeatedly.

Expected:

one logical event.

---

# 56. CONFLICT TEST

Publish:

same event_id
different payload.

Expected:

integrity rejection.

Generate:

AUDIT_INTEGRITY_FAILURE.

---

# 57. REPLAY TEST

Create sequence of list events.

Then rebuild projection from zero.

Final replay state MUST match PostgreSQL operational state.

---

# 58. HISTORICAL STATE TEST

Create:

ADD
PRIORITY_CHANGE
ASSIGN
REMOVE

Verify state at each event boundary.

---

# 59. MERKLE CORRUPTION TEST

In controlled test environment:

corrupt one stored event/segment.

Integrity verification MUST detect mismatch.

Never perform intentional corruption in production.

---

# 60. BACKUP / RESTORE

HeraclitusDB audit data SHALL participate in backup strategy once the
integration becomes production-relevant.

Test:

backup
destroy instance
restore
verify Merkle
verify LSN
verify event counts
run reconciliation.

---

# 61. DISASTER RECOVERY EVIDENCE

Generate report:

docs/acceptance/HERACLITUS-RECOVERY-REPORT.md

Fields:

backup id
event count
first LSN
last LSN
restore duration
Merkle result
reconciliation result
missing events
duplicates
status

---

# 62. OBSERVABILITY OF HERACLITUS

Monitor:

availability
append latency
batch latency
outbox depth
outbox age
publish failures
retry count
dead letters
last successful append
last Heraclitus LSN
reconciliation lag
integrity verification status
disk usage

---

# 63. ALERTS

Alert when:

outbox age > threshold
dead-letter count > 0
Heraclitus unavailable
integrity verification fails
reconciliation mismatch occurs
disk usage critical
append error rate elevated

---

# 64. HEALTH ENDPOINT

CRQ-V-IA health response SHOULD distinguish:

core application health

from:

Heraclitus audit health.

Example:

{
  "core": "UP",
  "postgres": "UP",
  "heraclitus": "DEGRADED"
}

During shadow mode:

Heraclitus DEGRADED must not cause core readiness failure.

---

# 65. SECURITY

Connection to HeraclitusDB SHALL use:

TLS where supported
authentication
least privilege
network restrictions

The CRQ-V-IA application user SHALL have only required append/read
permissions.

Administrative operations use separate credentials.

---

# 66. SECRET MANAGEMENT

Heraclitus credentials SHALL NOT be stored in Git.

Use:

secret manager
or protected environment configuration.

---

# 67. ACCESS CONTROL

Suggested Heraclitus permissions:

crqvia_writer:
append

crqvia_auditor:
read
verify

crqvia_admin:
administrative operations

Application runtime SHOULD NOT run as admin.

---

# 68. EVENT QUERY SECURITY

Audit query endpoints MUST be RBAC protected.

Suggested permission:

AUDIT_VIEW

More sensitive integrity operations:

AUDIT_ADMIN

---

# 69. UI

Add administration page:

/admin/audit

Sections:

Audit Events
Integrity
Reconciliation
Heraclitus Status
Outbox
Dead Letters

---

# 70. TIMELINE UI

Entity profile MAY show:

Audit Timeline

Example:

10:04 Added to list
10:08 Priority changed
10:20 Assigned
11:15 CNPJ verified
14:30 Exported

Only authorized users may see internal events.

---

# 71. HERACLITUS FEATURE FLAG UI

Do NOT allow arbitrary enable/disable by ordinary administrators.

Integration configuration is deployment-level infrastructure.

---

# 72. MIGRATION PHASE 0

No Heraclitus dependency.

Implement:

AuditSink
PostgresAuditSink
CompositeAuditSink
outbox
event schema

This prepares clean integration.

---

# 73. MIGRATION PHASE 1 — SHADOW

Enable:

PostgresAuditSink
+
HeraclitusAuditSink

Configuration:

HERACLITUS_REQUIRED=false

Duration recommended:

at least 30 days of meaningful use before promotion.

---

# 74. PHASE 1 SUCCESS CRITERIA

Target:

0 permanent event loss
0 unexplained hash mismatch
0 unresolved duplicate conflict
successful crash recovery
successful backup restore
successful reconciliation
acceptable resource usage

---

# 75. MIGRATION PHASE 2 — VERIFIED AUDIT STORE

HeraclitusDB becomes preferred source for historical audit queries.

PostgreSQL audit remains fallback/projection.

HERACLITUS_REQUIRED remains configurable.

---

# 76. MIGRATION PHASE 3 — AUDIT SOURCE OF TRUTH

Only after explicit technical approval.

Possible architecture:

HeraclitusDB:
canonical event history

PostgreSQL:
operational state + audit projection/index

Promotion requires:

long-term stability;
recovery proof;
replay proof;
performance proof;
integrity proof;
documented operational support.

---

# 77. PROMOTION GATE

HeraclitusDB SHALL NOT become mandatory merely because integration
"works on developer machine".

Required evidence:

soak test
crash recovery
network partition recovery
backup restore
reconciliation
Merkle verification
replay correctness
load benchmark
security review

---

# 78. FALLBACK

Even after promotion, define emergency operational fallback.

Document:

docs/operations/HERACLITUS-FAILURE-RUNBOOK.md

Include:

detection
impact
temporary mode
outbox handling
recovery
reconciliation
incident closure

---

# 79. HERACLITUS DATA MODEL

Prefer a generic event envelope rather than one table/type per event.

Core searchable attributes:

event_id
tenant_id
event_type
event_class
actor_id
entity_type
entity_id
correlation_id
occurred_at
software_version
source_version
rule_set_version

Payload carries event-specific information.

---

# 80. INDEXING

Benchmark indexes/views for:

tenant + time
entity + time
event_type + time
actor + time
correlation_id
source_version
rule_set_version

Do not index every payload field automatically.

---

# 81. MATERIALIZED VIEWS

Possible Heraclitus projections:

audit_by_entity
audit_by_actor
audit_by_event_type
audit_by_correlation
security_events
release_history
ruleset_history

These are disposable/rebuildable projections.

Source event stream remains authoritative.

---

# 82. SEARCH

Full-text search over audit payload is optional.

Do not expose unrestricted search over confidential events.

---

# 83. EXPORTING AUDIT

Authorized export:

CSV
JSONL

Audit export SHALL include:

range
event count
first/last LSN
Merkle root where available
generated_at
generated_by
file hash

---

# 84. CONTRACT EXIT

If Heraclitus contains CRQ-V audit history required for contractual
handover, contract-exit package SHOULD include an open-format audit
export.

Do not make future access dependent on proprietary Heraclitus binary
files only.

---

# 85. OPEN FORMAT

Audit handover format:

JSONL UTF-8

Recommended each line:

one complete audit envelope.

Include:

schema definitions
checksums
metadata.

---

# 86. CRQ-V CONTRACTUAL SAFETY

HeraclitusDB SHALL initially be considered an implementation detail of
the contracted solution.

It MUST NOT create a new obligation for CRQ-V to:

install servers;
administer HeraclitusDB;
purchase separate licenses;
operate database infrastructure.

The contracted platform remains accessed as a service.

---

# 87. COST CONTROL

Track:

storage growth/day
storage growth/month
events/day
average event size
backup size
compute usage

The architecture must remain proportional to the low contractual value.

---

# 88. DATA VOLUME POLICY

Large artifacts SHALL NOT be embedded directly in events.

Examples:

CSV exports
PDFs
raw RFB files
screenshots
backup files

Store only:

artifact_id
hash
URI/reference
metadata

---

# 89. ATTACHMENTS

Evidence attachments SHOULD live in object storage.

Audit event records:

artifact hash
artifact reference
classification
retention date

---

# 90. PRIVACY

An immutable store creates special privacy risks.

Therefore:

data minimization happens BEFORE append.

Never rely on later deletion to fix excessive audit logging.

This principle is mandatory.

---

# 91. TEST DATA

Heraclitus development/testing SHALL use synthetic or public company
data where possible.

Do not clone CRQ_CONFIDENTIAL production audit streams into developer
environments.

---

# 92. SCHEMA VALIDATION

Producer MUST validate event schema before publishing to outbox.

Invalid event:

reject
log local error
generate operational alert

Do not publish malformed immutable events.

---

# 93. EVENT REGISTRY

Create:

docs/audit/EVENT-CATALOG.md

For each event document:

name
class
description
trigger
actor
entity
payload schema
retention
classification
introduced_version
deprecated_version

---

# 94. EVENT DEPRECATION

Do not delete old event definitions.

Mark:

DEPRECATED

Consumers MUST remain capable of reading historical schema versions.

---

# 95. TEST DIRECTORY

Recommended:

apps/api/tests/audit/
    test_sink.py
    test_outbox.py
    test_idempotency.py
    test_reconciliation.py
    test_redaction.py
    test_schema.py

integration/heraclitus/
    test_append.py
    test_duplicate.py
    test_replay.py
    test_recovery.py
    test_partition.py
    test_merkle.py

---

# 96. BENCHMARK DIRECTORY

Create:

benchmarks/heraclitus/

Include:

audit-generator
realistic-distribution
append-benchmark
replay-benchmark
reconciliation-benchmark
soak-test

---

# 97. REALISTIC EVENT DISTRIBUTION

Benchmark traffic SHOULD approximate expected application use.

Example distribution:

SEARCH-related audit       25%
LIST workflow              30%
AUTH                       10%
EXPORT                      5%
CNPJ verification          10%
DATA INGEST                 5%
RULE/ADMIN                  5%
OTHER                      10%

Do not optimize solely for uniform synthetic traffic.

---

# 98. ACCEPTANCE REPORT

Create:

docs/acceptance/HERACLITUS-AUDIT-ACCEPTANCE.md

Include:

Heraclitus version
CRQ-V-IA version
commit
test environment
event count
append results
recovery results
integrity results
reconciliation results
replay results
resource usage
known limitations

---

# 99. REQUIRED METRICS FOR ACCEPTANCE

At minimum:

events_generated
events_published
events_reconciled
events_missing

duplicate_attempts
duplicate_logical_events

hash_mismatches

first_lsn
last_lsn

P50 append
P95 append
P99 append

replay_duration
restore_duration

outbox_max_depth

---

# 100. SUCCESS CRITERIA

Initial shadow integration is successful when:

CRQ-V-IA continues operating if HeraclitusDB is down;

no committed audit event is permanently lost;

duplicate publishing does not create duplicate logical events;

reconciliation detects zero unexplained differences;

Merkle/integrity verification succeeds;

historical event order is recoverable;

replay produces expected state;

crash recovery succeeds;

backup/restore succeeds;

no secrets appear in stored events;

performance impact on the main application is negligible.

---

# 101. DEFINITION OF DONE

SPEC-0020 is complete for Phase 1 when:

AuditSink exists;

PostgresAuditSink exists;

HeraclitusAuditSink exists;

CompositeAuditSink exists;

transactional outbox exists;

schema validation exists;

redaction exists;

idempotency exists;

retry/dead-letter exists;

Heraclitus shadow mode works;

health monitoring exists;

reconciliation exists;

integrity verification exists;

replay tests exist;

crash test passes;

network outage test passes;

duplicate test passes;

Merkle verification passes;

backup/restore test passes;

acceptance report is generated.

---

# 102. FINAL ARCHITECTURAL RULE

HeraclitusDB is not the CRQ-V-IA operational database.

In the initial architecture:

PostgreSQL
=
operational source of truth

HeraclitusDB
=
immutable audit/evidence event store

OpenTelemetry/log platform
=
observability

These responsibilities MUST NOT be casually merged.

Only after objective operational evidence may HeraclitusDB become the
canonical source of audit history.

---

# 103. AGENT EXECUTION RULE

The implementation agent SHALL NOT satisfy this SPEC by:

creating interfaces only;
creating mock clients only;
creating documentation only;
writing TODOs;
adding Heraclitus configuration without running it;
declaring integrity without corrupt/recovery tests.

The agent MUST produce executable integration and test evidence.

---

# 104. AGENT REPORT

At the end report:

COMPLETED

FILES

EVENTS IMPLEMENTED

TESTS EXECUTED

BENCHMARKS

RECOVERY RESULTS

RECONCILIATION

MERKLE VERIFICATION

KNOWN LIMITATIONS

RISKS

NEXT PHASE

COMMIT SHA

If recovery, replay, idempotency or reconciliation remain untested:

SPEC-0020 REMAINS OPEN.

Transação PostgreSQL
   ├─ altera estado
   ├─ registra audit_event
   └─ registra audit_outbox
          ↓
        COMMIT

Worker
   ↓
HeraclitusDB
   ↓
ACK + LSN/HLC

empresa adicionada à fiscalização
        ↓
PostgreSQL COMMIT
        ↓
processo morre
        ↓
Heraclitus nunca recebe o evento

