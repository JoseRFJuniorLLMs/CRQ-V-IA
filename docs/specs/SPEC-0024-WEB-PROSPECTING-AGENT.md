# SPEC-0024 — Web Prospecting Agent

Status: OPTIONAL / COMPETITIVE DIFFERENTIATOR
Priority: P1
Repository: JoseRFJuniorLLMs/CRQ-V-IA
Target branch: main

Depends on:
- SPEC-0001 — Data Ingestion
- SPEC-0002 — CNPJ Providers
- SPEC-0003 — Regulatory Engine
- SPEC-0004 — Search and Filters
- SPEC-0005 — AI Ranking
- SPEC-0007 — Authentication and RBAC
- SPEC-0008 — Lists and Exports
- SPEC-0009 — Observability
- SPEC-0010 — LGPD and Security
- SPEC-0018 — Full Implementation Compliance
- SPEC-0019 — Contractual Data Governance
- SPEC-0020 — Heraclitus Audit Event Store
- SPEC-0021+ — Support / subsequent specifications where applicable

Type:
AI Agent / Web Discovery / Evidence Gathering / Human-in-the-Loop

---

# 1. PURPOSE

Implement an autonomous Web Prospecting Agent capable of searching
publicly accessible internet sources for evidence that companies located
in Rio Grande do Sul perform activities potentially related to the
professional field of Chemistry.

The agent SHALL:

- investigate known companies;
- discover new candidate companies;
- search public web sources;
- collect structured evidence;
- identify possible CNPJ/company matches;
- cross-reference findings with RFB data;
- cross-reference findings with regulatory rules;
- produce explainable recommendations;
- submit findings for human review.

The agent SHALL NOT make final regulatory or legal determinations.

---

# 2. CORE PRINCIPLE

The architecture SHALL preserve three independent concepts:

RFB / official data
=
corporate/cadastral truth

Regulatory Engine
=
deterministic regulatory prospecting rules

Web Prospecting Agent
=
discovery of public evidence and operational signals

Web evidence MUST NOT overwrite official RFB data.

---

# 3. LEGAL / REGULATORY SAFETY

The system SHALL never automatically state:

"empresa está irregular"

"empresa é obrigada a registrar-se"

"empresa deve ser fiscalizada"

"empresa deve ser autuada"

"empresa exerce atividade química comprovadamente"

unless such conclusion is entered by an authorized human user under an
appropriate administrative process.

Allowed wording:

"evidência pública encontrada"

"indício de atividade relacionada à Química"

"potencial interesse fiscalizatório"

"candidato para revisão"

"atividade possivelmente relacionada"

"revisão humana recomendada"

---

# 4. OPERATING MODES

Implement at least two operating modes:

COMPANY_INVESTIGATION

DISCOVERY

Optional future mode:

CONTINUOUS_MONITORING

---

# 5. COMPANY INVESTIGATION MODE

Input:

existing establishment/company from CRQ-V-IA.

Agent receives:

CNPJ
legal name
trade name
municipality
state
primary CNAE
secondary CNAEs
company size
known website if available
RFB competence
current regulatory score

The agent searches public internet sources for evidence related to the
specific company.

---

# 6. DISCOVERY MODE

Agent receives a prospecting objective.

Examples:

"Find laboratories performing physicochemical analysis in RS."

"Find companies providing chemical surface treatment in RS."

"Find manufacturers of paints, resins or solvents in RS."

"Find environmental laboratories in the Serra Gaúcha."

The agent SHALL identify candidate organizations and attempt to resolve
them to a valid corporate identity.

---

# 7. DISCOVERY PIPELINE

Recommended flow:

SEARCH OBJECTIVE
    ↓
QUERY PLANNER
    ↓
WEB SEARCH
    ↓
RESULT NORMALIZATION
    ↓
SOURCE QUALITY FILTER
    ↓
EVIDENCE EXTRACTION
    ↓
COMPANY ENTITY RESOLUTION
    ↓
CNPJ RESOLUTION
    ↓
RFB CROSS-CHECK
    ↓
REGULATORY ENGINE
    ↓
WEB EVIDENCE SCORE
    ↓
HUMAN REVIEW QUEUE

---

# 8. COMPANY INVESTIGATION PIPELINE

Existing company
    ↓
build search aliases
    ↓
search web
    ↓
identify official website
    ↓
search products/services/processes
    ↓
extract evidence
    ↓
classify evidence
    ↓
calculate web evidence score
    ↓
human review

---

# 9. PROVIDER ABSTRACTION

Application code SHALL NOT directly depend on Gemini, Google, Brave or
another search provider.

Create interface:

WebSearchProvider

Methods:

search()
search_batch()
health()
usage()
capabilities()

Possible implementations:

GeminiGroundedSearchProvider
BraveSearchProvider
GoogleSearchProvider
GenericSearchProvider

Provider implementation MUST be replaceable.

---

# 10. AI MODEL ABSTRACTION

Create:

EvidenceAnalysisProvider

Methods:

analyze_source()
extract_company_identity()
classify_evidence()
summarize_evidence()
generate_queries()

Possible implementations:

GeminiEvidenceProvider
OpenAICompatibleProvider
LocalModelProvider

Search and analysis SHOULD remain logically separate.

---

# 11. PROVIDER CONFIGURATION

Environment variables:

WEB_AGENT_ENABLED=true

WEB_SEARCH_PROVIDER=gemini

WEB_ANALYSIS_PROVIDER=gemini

WEB_AGENT_MAX_QUERIES_PER_RUN=25

WEB_AGENT_MAX_RESULTS_PER_QUERY=10

WEB_AGENT_MAX_PAGES_PER_RUN=50

WEB_AGENT_MAX_COST_PER_RUN=

WEB_AGENT_DAILY_BUDGET=

WEB_AGENT_MONTHLY_BUDGET=

WEB_AGENT_TIMEOUT_SECONDS=

---

# 12. FEATURE FLAGS

WEB_AGENT_ENABLED

WEB_AGENT_INVESTIGATION_ENABLED

WEB_AGENT_DISCOVERY_ENABLED

WEB_AGENT_BACKGROUND_ENABLED

WEB_AGENT_AUTO_CNPJ_RESOLUTION_ENABLED

WEB_AGENT_AUTO_REVIEW_ENABLED=false

WEB_AGENT_EXTERNAL_LLM_ENABLED

All potentially expensive capabilities SHALL be disableable independently.

---

# 13. AGENT RUN

Create entity:

agent_run

Fields:

id
tenant_id

mode
objective

started_by
started_at
completed_at

status

search_provider
analysis_provider
model
agent_version
prompt_version

rfb_source_version
rule_set_version
software_release_id

queries_planned
queries_executed
results_received
pages_analyzed

companies_discovered
companies_matched
companies_unresolved

evidence_created
evidence_rejected

estimated_cost

tokens_input
tokens_output

error_code
error_message

---

# 14. AGENT RUN STATUS

QUEUED
PLANNING
SEARCHING
ANALYZING
RESOLVING
SCORING
AWAITING_REVIEW
COMPLETED
PARTIAL
FAILED
CANCELLED
BUDGET_EXCEEDED

---

# 15. QUERY PLAN

Create:

agent_query

Fields:

id
agent_run_id
query
purpose
provider
sequence
status
results_count
executed_at
cost_estimate

Purpose examples:

COMPANY_IDENTITY
PRODUCT
SERVICE
INDUSTRIAL_PROCESS
LABORATORY
ENVIRONMENTAL_ACTIVITY
CNPJ_DISCOVERY
LOCATION
OFFICIAL_SOURCE

---

# 16. QUERY GENERATION

Queries SHOULD combine trusted existing data.

Examples:

"<legal_name>" chemistry

"<trade_name>" products

"<legal_name>" "<municipality>"

"<cnpj>"

site:<official-domain> products

site:<official-domain> services

"<company>" laboratory

"<company>" wastewater treatment

"<company>" chemical treatment

Avoid excessively broad queries when investigating a specific company.

---

# 17. QUERY EXPANSION

The agent MAY expand search vocabulary based on regulatory categories.

Examples:

laboratory
chemical analysis
physicochemical
industrial chemistry
galvanoplasty
surface treatment
paint
resin
solvent
fertilizer
sanitizer
water treatment
effluent treatment
quality control
chemical manufacturing
industrial process

Vocabulary SHALL be versioned.

---

# 18. SOURCE TYPES

Classify every source.

OFFICIAL_COMPANY_WEBSITE

GOVERNMENT

REGULATORY_BODY

PUBLIC_REGISTRY

TECHNICAL_DOCUMENT

PRODUCT_CATALOG

SERVICE_PAGE

NEWS

MARKETPLACE

DIRECTORY

SOCIAL_NETWORK

BLOG

OTHER

---

# 19. SOURCE QUALITY

Assign source quality independently from evidence strength.

Suggested scale:

A — authoritative
B — strong
C — moderate
D — weak
E — unreliable

Examples:

A:
official government source
official company website

B:
official technical catalog
recognized regulatory source

C:
credible industry publication

D:
business directory

E:
anonymous or unverifiable content

---

# 20. SOURCE QUALITY POLICY

Low-quality sources SHALL NOT independently produce HIGH confidence.

Evidence from weak sources MAY be used to generate further searches.

The system MUST distinguish:

SOURCE QUALITY

from:

EVIDENCE CONFIDENCE.

---

# 21. WEB EVIDENCE MODEL

Create:

web_evidence

Fields:

id
tenant_id
agent_run_id

establishment_id nullable
candidate_company_id nullable

source_url
canonical_url
source_domain
source_title
source_type
source_quality

query_id

evidence_type
evidence_text
evidence_summary

confidence
confidence_score

source_published_at nullable
first_discovered_at
last_verified_at

source_hash
content_hash

rfb_source_version
rule_set_version
software_release_id

review_status
reviewed_by
reviewed_at
review_note

expired_at nullable
superseded_by nullable

---

# 22. EVIDENCE TYPES

PRODUCT

SERVICE

INDUSTRIAL_PROCESS

CHEMICAL_PROCESS

LABORATORY

ENVIRONMENTAL_ANALYSIS

WATER_TREATMENT

EFFLUENT_TREATMENT

QUALITY_CONTROL

CHEMICAL_MANUFACTURING

MATERIAL_HANDLING

TECHNICAL_RESPONSIBILITY

LOCATION

CORPORATE_IDENTITY

CNPJ

OTHER

---

# 23. EVIDENCE CONFIDENCE

Suggested:

VERY_LOW
LOW
MEDIUM
HIGH
VERY_HIGH

Store numeric score separately.

Example:

confidence_score:
0.00–1.00

Do not expose excessive numerical precision to ordinary users.

---

# 24. EVIDENCE TEXT

Store only the minimum excerpt needed to justify the classification.

Do NOT copy entire web pages into the database by default.

Store:

URL
title
small relevant excerpt
summary
hash
timestamps

This reduces:

copyright risk
storage
privacy exposure
stale duplicated content

---

# 25. SOURCE SNAPSHOT

Full-page snapshots are NOT required by default.

If enabled for authorized evidence preservation:

store separately in object storage.

Record:

artifact_id
sha256
content_type
capture_date
classification
retention

Never embed large page bodies into audit events.

---

# 26. CANDIDATE COMPANY

Create:

web_candidate_company

Fields:

id
tenant_id

name
normalized_name

trade_name nullable

municipality nullable
state nullable

website nullable

resolved_cnpj nullable
resolution_status

discovered_at

agent_run_id

review_status

---

# 27. ENTITY RESOLUTION

Agent SHALL attempt to match discovered entities against RFB records.

Signals:

legal name similarity
trade name similarity
CNPJ
domain
address
municipality
telephone where public and appropriate
company website
CNAE

Never rely only on company name when multiple companies may share
similar names.

---

# 28. RESOLUTION STATUS

UNRESOLVED
POSSIBLE_MATCH
MATCHED
AMBIGUOUS
REJECTED

Only MATCHED may automatically link to an existing establishment.

POSSIBLE_MATCH and AMBIGUOUS require human review.

---

# 29. CNPJ RESOLUTION

Preferred methods:

1. CNPJ explicitly present on official company site;
2. official/public structured source;
3. matching against RFB dataset;
4. supported CNPJ provider.

Do NOT use CAPTCHA bypass.

Do NOT infer CNPJ from incomplete fragments.

---

# 30. RFB CROSS-CHECK

When candidate CNPJ is resolved:

lookup RFB data.

Check:

active status
state
municipality
legal name
trade name
primary CNAE
secondary CNAEs
opening date
company size

If CNPJ conflicts with discovered identity:

mark:

IDENTITY_CONFLICT

and require review.

---

# 31. ACTIVE ESTABLISHMENT POLICY

Default discovery results SHOULD prioritize establishments currently
ACTIVE in RFB.

Inactive companies may remain visible as evidence, but SHALL be
clearly marked.

---

# 32. REGULATORY CROSS-CHECK

Once matched to RFB:

run deterministic regulatory engine.

Produce independently:

regulatory_score

and:

web_evidence_score

Never merge them into one opaque number.

---

# 33. THREE-SCORE MODEL

Maintain:

regulatory_score

web_evidence_score

operational_priority

Conceptually:

Regulatory score:
relationship with normative/CNAE rules.

Web evidence score:
strength of public evidence.

Operational priority:
optional workflow aid.

---

# 34. OPERATIONAL PRIORITY

Operational priority MAY use:

regulatory_score
web_evidence_score
company status
suppression
inspection history
company size
geography

Formula MUST be:

versioned
explainable
configurable
auditable

It SHALL NOT represent a legal conclusion.

---

# 35. WEB EVIDENCE SCORE

Suggested factors:

source_quality
evidence_specificity
number_of_independent_sources
source_recency
company_identity_confidence
activity_match_strength

Do not simply count search results.

Ten duplicated pages are not ten independent pieces of evidence.

---

# 36. SOURCE DEDUPLICATION

Normalize:

tracking parameters
http/https differences where appropriate
canonical links
duplicate content hashes

Identify mirrors and syndicated content.

Avoid artificially inflating evidence count.

---

# 37. DOMAIN DIVERSITY

Evidence scoring SHOULD distinguish:

five pages on one domain

from:

five independent domains.

Independent corroboration may increase confidence.

---

# 38. OFFICIAL WEBSITE DETECTION

Agent SHOULD attempt to identify the official business website.

Evidence signals:

domain linked to corporate identity
CNPJ on website
address match
official contact information
consistent legal name

Do not mark a domain official based solely on search ranking.

---

# 39. EVIDENCE FRESHNESS

Evidence SHALL include:

first_discovered_at
last_verified_at

Recommended freshness states:

CURRENT
AGING
STALE
UNAVAILABLE

Thresholds configurable by evidence type.

---

# 40. BROKEN / REMOVED SOURCE

If source later disappears:

do NOT silently delete historical evidence.

Set:

source_status = UNAVAILABLE

Preserve:

URL
hash
original discovery timestamp
minimal permitted evidence metadata

---

# 41. HUMAN REVIEW

Create:

web_evidence_review

Fields:

evidence_id
reviewer_id
decision
reason
reviewed_at

Decisions:

CONFIRMED
REJECTED
INSUFFICIENT
OUTDATED
WRONG_COMPANY
DUPLICATE
NEEDS_MORE_RESEARCH

---

# 42. REVIEW QUEUE

Create screen:

/web-prospecting/review

Filters:

new evidence
high confidence
ambiguous company
identity conflict
high regulatory score
high web score
unresolved CNPJ
stale evidence

---

# 43. COMPANY PROFILE UI

Add section:

WEB EVIDENCE

Display:

evidence type
summary
source
source quality
confidence
discovery date
last verification
review status

Buttons:

OPEN SOURCE
CONFIRM
REJECT
REQUEST MORE RESEARCH

---

# 44. PROSPECTING PAGE

Add:

/web-prospecting

Sections:

Investigate Company

Discover Companies

Agent Runs

Review Queue

Usage / Cost

---

# 45. INVESTIGATE BUTTON

Company profile SHALL expose:

"Investigar na Web"

On click:

show expected scope
estimated query limit
provider
budget impact where relevant

Then create agent_run.

---

# 46. DISCOVERY FORM

Fields:

objective

region

municipality optional

keywords

CNAE optional

company size optional

maximum companies

maximum queries

source preferences

The user SHALL be able to review parameters before execution.

---

# 47. EXAMPLE DISCOVERY REQUEST

Objective:

"Laboratórios que realizem análises físico-químicas no Rio Grande do Sul"

Agent may generate structured subqueries but must preserve original
objective.

---

# 48. AGENT PLANNER

Planner responsibilities:

understand objective
generate search strategy
avoid redundant queries
manage query budget
adapt based on results
stop when enough evidence is collected

Planner SHALL NOT exceed configured budget.

---

# 49. STOP CONDITIONS

Agent run SHALL stop when any condition occurs:

max queries reached
max pages reached
max candidates reached
cost budget reached
timeout reached
user cancellation
provider failure threshold reached
objective satisfied

---

# 50. COST CONTROL

Create:

web_provider_usage

Fields:

provider
agent_run_id
period

queries
requests
tokens_input
tokens_output

estimated_cost

currency

cache_hits

budget_limit

---

# 51. COST LIMITS

Support:

per-run limit
daily limit
monthly limit

When budget limit is reached:

do not silently continue.

Set run:

BUDGET_EXCEEDED

Preserve partial results.

---

# 52. SEARCH CACHE

Cache identical or equivalent queries for configurable period.

Store:

provider
query_hash
executed_at
expires_at
result_reference

Avoid repeated paid searches without benefit.

---

# 53. PAGE FETCHING

If provider returns source URLs and additional page inspection is
required, use controlled fetcher.

Create:

EvidenceFetcher

Rules:

publicly accessible content only
timeouts
response-size limit
content-type validation
redirect limit
no authentication bypass
no CAPTCHA bypass

---

# 54. FETCH ALLOWED TYPES

Initial:

text/html
application/pdf
text/plain

Optional later:

structured feeds

Do NOT fetch arbitrary executable content.

---

# 55. SSRF PROTECTION

EvidenceFetcher MUST defend against SSRF.

Block:

localhost
loopback
private networks
link-local addresses
cloud metadata endpoints
unsupported protocols

Allow:

http
https

only.

---

# 56. DOWNLOAD SIZE LIMIT

Configure:

WEB_FETCH_MAX_BYTES

Large files SHALL be rejected or handled through explicit controlled
pipeline.

Do not let a helpful robot download a 40 GB ISO because someone linked
one from a company page.

---

# 57. ROBOTS / TERMS / ACCESS POLICY

Agent SHALL prefer supported search APIs and publicly accessible pages.

Do not:

bypass login
bypass CAPTCHA
evade access controls
circumvent paywalls
simulate unauthorized accounts

Provider terms and site access policies SHALL be respected.

---

# 58. PERSONAL DATA MINIMIZATION

The agent's objective is COMPANY ACTIVITY discovery.

It SHALL NOT intentionally collect:

personal social profiles
personal CPF
personal email addresses
personal phone numbers
family information
unrelated individual data

Focus on organizational/public business information.

---

# 59. SOCIAL NETWORKS

Social-network sources SHOULD be disabled by default.

If later enabled:

treat as weak/moderate evidence unless independently corroborated.

Do not collect employee profiles for general prospecting.

---

# 60. LLM DATA POLICY

External LLM provider SHALL receive only the minimum information needed.

Do not send:

CRQ_CONFIDENTIAL notes
inspection strategy
internal comments
personal data
support ticket content
credentials

unless specifically authorized and technically justified.

---

# 61. PROMPT VERSIONING

Every agent run SHALL record:

prompt_version

Prompts SHALL live in version-controlled project files.

Example:

agents/web_prospecting/prompts/v1/

Never silently modify production prompts without release/change record.

---

# 62. SYSTEM PROMPT RULES

System prompt SHALL explicitly state:

discover facts, do not invent;

cite sources;

separate evidence from inference;

do not decide legal registration obligation;

do not infer missing CNPJ;

identify ambiguity;

prefer official sources;

return structured output.

---

# 63. STRUCTURED AI OUTPUT

The model SHALL return schema-validated JSON.

Example:

{
  "company": {...},
  "evidence": [...],
  "uncertainties": [...],
  "recommended_action": "HUMAN_REVIEW"
}

Do not parse arbitrary prose as the primary integration mechanism.

---

# 64. HALLUCINATION CONTROL

Any material factual statement produced by the agent SHALL be linked to
at least one source.

If no source supports the statement:

do not present it as fact.

Use:

UNSUPPORTED
or
INFERENCE

where applicable.

---

# 65. CITATION REQUIREMENT

Evidence SHALL always contain:

source_url

source_title

retrieved_at

No-source evidence SHALL be rejected.

---

# 66. EVIDENCE VS INFERENCE

Model output SHALL distinguish:

FACT
INFERENCE
HYPOTHESIS

Only FACT supported by source may become web_evidence automatically.

INFERENCE can be shown to reviewer but not stored as confirmed fact.

---

# 67. SOURCE CONFLICT

If sources conflict:

store both.

Mark:

CONFLICTING_EVIDENCE

Do not allow LLM to silently choose one.

Human review required.

---

# 68. OFFICIAL SOURCE PRIORITY

When official data conflicts with informal source:

official source SHALL be presented with higher authority for cadastral
facts.

Web pages may still provide activity evidence.

---

# 69. COMPANY DISCOVERY RESULT

Each discovered company candidate SHALL display:

name
possible CNPJ
municipality
website
evidence count
source count
identity confidence
web evidence score
RFB match status
regulatory score if matched
review status

---

# 70. NEW COMPANY DISCOVERY

A web-discovered company that is not yet resolved in RFB SHALL NOT
become a normal establishment record.

It remains:

web_candidate_company

until identity is resolved.

---

# 71. DUPLICATE COMPANY DETECTION

Before creating candidate:

search by:

CNPJ
normalized name
domain
municipality

Do not create repeated candidates from each query.

---

# 72. SUPPRESSION INTEGRATION

Before showing candidate as prospect:

check tenant suppression.

If company is:

REGISTERED
EXEMPT
RECENTLY_INSPECTED
OUT_OF_SCOPE
DO_NOT_REPROSPECT

show corresponding status.

Do not silently discard the discovery.

---

# 73. LIST INTEGRATION

Reviewed candidates linked to valid establishments may be added to:

saved_list

with:

prospect_snapshot
web evidence references
regulatory score
review decision

---

# 74. SNAPSHOT

When web evidence contributes to a fiscal prospecting decision:

create immutable prospect snapshot.

Include:

RFB version
ruleset version
web evidence IDs
web evidence score
agent run ID
software release
reviewer

---

# 75. HERACLITUS EVENTS

Emit:

WEB_AGENT_RUN_CREATED
WEB_AGENT_STARTED
WEB_AGENT_QUERY_EXECUTED
WEB_CANDIDATE_DISCOVERED
WEB_COMPANY_MATCHED
WEB_IDENTITY_CONFLICT
WEB_EVIDENCE_DISCOVERED
WEB_EVIDENCE_REVIEWED
WEB_AGENT_BUDGET_EXCEEDED
WEB_AGENT_COMPLETED
WEB_AGENT_FAILED

---

# 76. HERACLITUS PAYLOAD POLICY

Do NOT store complete webpage content in HeraclitusDB.

Store:

event ID
agent run ID
company/candidate ID
evidence ID
source URL hash
source hash
classification
confidence
review status
timestamps

Detailed evidence remains in PostgreSQL/object storage.

---

# 77. AUDITABILITY

For every reviewed evidence item the system must answer:

who started the research
which provider was used
which model was used
which prompt version was used
which query found the source
which URL supported the evidence
when it was retrieved
which company it was matched to
who reviewed it
what decision was made

---

# 78. BACKGROUND EXECUTION

Agent runs SHALL be asynchronous.

Do not block HTTP request until full research completes.

Flow:

POST
→ QUEUED
→ worker
→ progress events
→ results

---

# 79. PROGRESS

UI SHALL show:

queries executed
sources found
companies discovered
evidence extracted
current phase
estimated progress

Avoid fake precision.

---

# 80. CANCELLATION

Authorized user SHALL be able to cancel a running agent.

Cancellation SHALL:

stop new queries
finish safe cleanup
preserve already collected evidence
mark run CANCELLED

---

# 81. CONCURRENCY CONTROL

Limit concurrent agent runs by:

tenant
user
provider
global infrastructure capacity

Prevent cost explosions.

---

# 82. RATE LIMIT

Separate limits for:

manual investigation
discovery runs
background monitoring

Administrative users may have higher limits.

---

# 83. FAILURE HANDLING

Provider failure SHALL produce:

PARTIAL

when useful evidence already exists.

Do not discard completed work.

---

# 84. PROVIDER FALLBACK

Optional policy:

primary provider fails
→ fallback provider

Fallback must be recorded.

Do not silently change providers without trace.

---

# 85. PROVIDER COMPARISON MODE

Development/testing MAY run two providers against same objective.

Compare:

candidate coverage
source quality
evidence precision
cost
latency
hallucination rate

Do not use this automatically in normal production unless justified.

---

# 86. GOLDEN DATASET

Create curated evaluation dataset.

Examples:

known chemical company
clearly unrelated company
ambiguous industrial company
laboratory
water-treatment operator
false positive by name
multi-branch company

Use public/non-sensitive data.

---

# 87. EVALUATION METRICS

Measure:

company resolution precision
company resolution recall

evidence precision
evidence usefulness

false-positive rate
unsupported-claim rate

CNPJ resolution accuracy

average sources/company

cost/company

latency/company

human-confirmation rate

---

# 88. CRITICAL METRIC

Unsupported factual claim rate SHOULD approach zero.

A polished hallucination with attractive typography is still a
hallucination.

---

# 89. HUMAN REVIEW METRICS

Measure:

confirmed evidence
rejected evidence
wrong company
duplicate
outdated
insufficient

Use review outcomes to improve prompts and heuristics.

---

# 90. NO AUTOMATIC MODEL TRAINING

Human review data SHALL NOT automatically be sent to external providers
for training.

Any supervised-learning use requires explicit separate governance.

---

# 91. AI MODEL VERSION

Record:

provider
model
model_version where available

If provider model alias changes without fixed version:

record actual returned model metadata where available.

---

# 92. WEB AGENT VERSION

Create independent:

agent_version

Example:

web-agent-1.0.0

Agent version SHALL encompass:

planner
prompts
schema
scoring logic
source-quality policy

---

# 93. ADMIN SETTINGS

/admin/web-agent

Show:

enabled providers
budget
usage
limits
agent version
prompt version
runs today
failure rate
evidence statistics

Never display provider API keys.

---

# 94. PROVIDER HEALTH

Monitor:

availability
latency
error rate
rate limits
quota remaining where supported

Provider outage SHALL NOT affect core CRQ-V-IA search over RFB data.

---

# 95. CORE SYSTEM INDEPENDENCE

If Web Agent is unavailable:

RFB search
regulatory engine
lists
exports
CNPJ baseline
support

MUST continue working.

Web prospecting is an enhancement, not a core single point of failure.

---

# 96. USER PERMISSIONS

Add:

WEB_AGENT_USE
WEB_AGENT_DISCOVERY
WEB_AGENT_REVIEW
WEB_AGENT_ADMIN

INSPECTOR may receive:

WEB_AGENT_USE

Discovery at scale may require:

WEB_AGENT_DISCOVERY

---

# 97. APPROVAL CONTROL

High-volume discovery runs MAY require coordinator approval.

Configurable threshold:

companies
queries
budget

---

# 98. EVIDENCE EXPORT

Authorized export MAY include:

company
CNPJ
evidence type
summary
source URL
source date
confidence
review status
RFB version
ruleset version

Do not include unnecessary copied webpage text.

---

# 99. EVIDENCE REPORT

Generate company-level report:

Company identification

RFB data

Regulatory indicators

Web evidence

Sources

Uncertainties

Human review

Disclaimer:
web findings support prospecting and do not constitute a final legal
or regulatory determination.

---

# 100. WEB AGENT API

Minimum:

POST /api/v1/web-agent/investigate

POST /api/v1/web-agent/discover

GET /api/v1/web-agent/runs

GET /api/v1/web-agent/runs/{id}

POST /api/v1/web-agent/runs/{id}/cancel

GET /api/v1/web-agent/evidence

GET /api/v1/web-agent/evidence/{id}

POST /api/v1/web-agent/evidence/{id}/review

GET /api/v1/web-agent/candidates

POST /api/v1/web-agent/candidates/{id}/resolve

---

# 101. EXAMPLE INVESTIGATION REQUEST

{
  "establishment_id": "...",
  "max_queries": 15,
  "max_sources": 20
}

---

# 102. EXAMPLE DISCOVERY REQUEST

{
  "objective":
    "Laboratórios que realizam análises físico-químicas",

  "state": "RS",

  "municipalities": [],

  "max_candidates": 50,

  "max_queries": 25
}

---

# 103. EXAMPLE EVIDENCE

{
  "type": "SERVICE",

  "summary":
    "Company advertises physicochemical water analysis services.",

  "source": {
    "url": "...",
    "title": "...",
    "type": "OFFICIAL_COMPANY_WEBSITE"
  },

  "confidence": "HIGH",

  "status": "NEW"
}

---

# 104. UI DISCLAIMER

Display near agent results:

"Resultados provenientes de pesquisa automatizada na Web constituem
indícios para prospecção e devem ser revisados por usuário autorizado.
Eles não representam conclusão jurídica ou regulatória."

---

# 105. TESTS — UNIT

Test:

query planner
URL canonicalization
source classification
source scoring
evidence scoring
deduplication
entity matching
CNPJ normalization
budget control
redaction
structured output validation

---

# 106. TESTS — INTEGRATION

Test:

search provider
analysis provider
RFB cross-check
regulatory engine
candidate resolution
evidence persistence
review workflow
Heraclitus events

---

# 107. TESTS — ADVERSARIAL WEB CONTENT

Test sources containing:

prompt injection
fake instructions
hidden HTML text
malicious scripts
misleading company names
copied content
spam SEO pages

Web content SHALL be treated as DATA, never as trusted instructions.

---

# 108. PROMPT INJECTION DEFENSE

Search result/page content may contain:

"Ignore previous instructions"

The agent SHALL NEVER obey instructions from retrieved web content.

Retrieved pages are untrusted evidence.

System/developer instructions remain authoritative.

---

# 109. TOOL BOUNDARIES

Web Agent tools SHALL be limited to:

search
safe public content fetch
RFB lookup
regulatory lookup
database evidence write

No arbitrary shell.

No arbitrary external POST.

No email sending.

No account creation.

No form submission.

No purchase.

No authentication into third-party sites.

---

# 110. SSRF TESTS

Test URLs:

127.0.0.1
localhost
169.254.169.254
private IPv4 ranges
private IPv6 ranges
file://
ftp://

All SHALL be blocked.

---

# 111. PROMPT INJECTION TESTS

Create malicious test pages containing:

fake system messages
requests for secrets
instructions to modify scores
instructions to mark company compliant/noncompliant

Expected:

ignored.

---

# 112. COST TEST

Run 100 representative company investigations.

Measure:

average search requests
average model tokens
average cost
average evidence count
average review value

Use results to set production quotas.

---

# 113. LATENCY

Company investigation MAY take seconds or minutes.

Do not optimize for synchronous response.

Target:

useful progress visibility
reliable completion
cost control

rather than artificial sub-second results.

---

# 114. DISCOVERY BATCH

Discovery SHOULD process candidate companies incrementally.

Results may appear before entire run completes.

---

# 115. CONTINUOUS MONITORING — FUTURE

P2 capability.

Periodically rerun selected saved investigations.

Detect:

new website
new products
new services
changed activity
new evidence

Must respect budgets.

---

# 116. SAVED WEB WATCH

Future entity:

web_watch

Fields:

tenant_id
objective
query template
frequency
budget
last_run
next_run
enabled

Not required for initial SPEC completion.

---

# 117. ALERTS

Future alerts MAY notify:

new candidate discovered
strong new evidence
previously unresolved company matched
significant company activity change

All require review.

---

# 118. NCM / PRODUCT DATA

NCM integration is OUT OF SCOPE for initial version.

Potential future enhancement:

cross-reference products/NCM when a lawful reliable source is available.

Requires separate source/governance analysis.

---

# 119. SOCIAL / PEOPLE INTELLIGENCE

OUT OF SCOPE:

employee prospecting
executive profiling
LinkedIn scraping
personal social media
personal contact enrichment

The system is a fiscal prospecting tool, not a sales intelligence CRM.

---

# 120. DEFINITION OF DONE — PHASE 1

Phase 1 complete when:

provider abstraction exists;

at least one WebSearchProvider works;

at least one EvidenceAnalysisProvider works;

company investigation works;

evidence includes sources;

structured output validation works;

RFB cross-check works;

regulatory cross-check works;

human review works;

cost limits work;

audit events work;

Heraclitus integration works;

prompt-injection tests pass;

SSRF tests pass;

core system continues functioning if Web Agent fails.

---

# 121. DEFINITION OF DONE — PHASE 2

Phase 2 complete when:

discovery mode works;

new candidate companies can be discovered;

entity resolution works;

CNPJ matching works;

duplicate suppression works;

review queue works;

bulk prospecting works;

usage dashboard works;

evaluation metrics exist.

---

# 122. PROMOTION GATE

Web Prospecting Agent SHALL NOT be considered production-ready merely
because it found interesting websites.

Required:

evidence precision evaluated;

company matching evaluated;

unsupported claim rate measured;

prompt injection tested;

cost measured;

privacy reviewed;

human review functional;

provider failure tested;

audit trail functional.

---

# 123. AGENT EXECUTION RULE

Implementation agent SHALL NOT satisfy this SPEC by:

creating only prompts;

creating mock search results;

creating only UI;

returning ungrounded AI answers;

hard-coding candidate companies;

claiming Gemini integration without executing provider tests;

claiming evidence without URL/source;

removing human review;

merging Web score with legal/regulatory conclusion.

---

# 124. REQUIRED IMPLEMENTATION REPORT

At completion report:

COMPLETED

FILES

DATABASE MIGRATIONS

PROVIDERS

MODELS

PROMPT VERSION

SEARCH TESTS

ENTITY RESOLUTION RESULTS

EVIDENCE QUALITY

COST RESULTS

SECURITY TESTS

PROMPT-INJECTION TESTS

HERACLITUS EVENTS

KNOWN LIMITATIONS

RISKS

COMMIT SHA

---

# 125. FINAL ARCHITECTURAL RULE

CRQ-V-IA SHALL maintain:

RFB
=
official cadastral baseline

Regulatory Engine
=
deterministic regulatory prospecting logic

Web Prospecting Agent
=
public-evidence discovery and investigation

Human Fiscal User
=
review and administrative judgment

No component may collapse these four roles into a single opaque AI
decision.

---

# 126. FINAL PRODUCT FLOW

The target experience is:

RFB DATABASE
        ↓
REGULATORY FILTER
        ↓
POTENTIAL COMPANY
        ↓
[ INVESTIGATE ON WEB ]
        ↓
WEB AGENT
        ↓
PUBLIC SOURCES
        ↓
STRUCTURED EVIDENCE
        ↓
RFB / CNPJ CROSS-CHECK
        ↓
WEB EVIDENCE SCORE
        ↓
HUMAN REVIEW
        ↓
FISCAL PROSPECTING LIST

And in discovery mode:

WEB SEARCH
        ↓
NEW COMPANY CANDIDATE
        ↓
IDENTITY RESOLUTION
        ↓
CNPJ
        ↓
RFB
        ↓
CFQ RULE ENGINE
        ↓
WEB EVIDENCE
        ↓
HUMAN REVIEW
        ↓
CRQ-V PROSPECTING WORKFLOW

---

# 127. FINAL RULE

The Web Prospecting Agent exists to discover and organize evidence.

It does not exist to replace:

official corporate data;
regulatory rules;
professional judgment;
administrative process.

When evidence is uncertain:

the correct output is:

"NEEDS HUMAN REVIEW"

not:

a confident invention.