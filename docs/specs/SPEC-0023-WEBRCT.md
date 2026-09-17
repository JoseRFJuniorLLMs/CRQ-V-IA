# SPEC-0021 — Support Center, Text Tickets and WebRTC Calls

Status: REQUIRED / OPTIONAL WEBRTC
Priority:
- Ticketing: P0
- WebRTC: P1

Repository: JoseRFJuniorLLMs/CRQ-V-IA

Depends on:
- SPEC-0007 — Authentication and RBAC
- SPEC-0009 — Observability
- SPEC-0010 — LGPD and Security
- SPEC-0015 — Support and Operations
- SPEC-0018 — Full Implementation
- SPEC-0019 — Governance
- SPEC-0020 — Heraclitus Audit Event Store

---

# 1. OBJECTIVE

Implement an integrated support center for CRQ-V users.

The system SHALL provide:

1. text-based support tickets;
2. ticket history;
3. ticket attachments;
4. communication between CRQ-V users and support staff;
5. SLA tracking;
6. optional real-time WebRTC call;
7. audit trail;
8. notification and escalation;
9. operational metrics.

WebRTC SHALL complement text support.

WebRTC SHALL NOT be the only available support channel.

---

# 2. ARCHITECTURE

Support Center:

CRQ-V User
    |
    +--> Text Ticket
    |       |
    |       +--> Support Agent
    |
    +--> WebRTC Call
            |
            +--> Signaling Service
            +--> STUN
            +--> TURN fallback

Operational persistence:

PostgreSQL

Audit history:

HeraclitusDB

Attachments:

S3-compatible object storage

Notifications:

Email / in-app

---

# 3. SUPPORT ROUTES

Frontend:

/support

/support/new

/support/tickets

/support/tickets/{id}

/support/calls/{id}

/admin/support

/admin/support/tickets

/admin/support/calls

---

# 4. TICKET MODEL

Create:

support_ticket

Fields:

id
tenant_id

number

requester_user_id
assigned_agent_id

category
severity
priority

subject
description

status

created_at
acknowledged_at
work_started_at
resolved_at
closed_at

last_activity_at

related_entity_type
related_entity_id

incident_id

sla_policy_id

resolution
resolution_code

created_from

---

# 5. TICKET NUMBER

Human-readable number example:

CRQV-2027-000001

Internal ID remains opaque UUID/UUIDv7.

Do not expose database sequential IDs as security identifiers.

---

# 6. TICKET STATUS

Supported lifecycle:

OPEN
ACKNOWLEDGED
IN_PROGRESS
WAITING_USER
WAITING_EXTERNAL
RESOLVED
CLOSED
CANCELLED

Transitions SHALL be validated.

Example:

OPEN
→ ACKNOWLEDGED
→ IN_PROGRESS
→ RESOLVED
→ CLOSED

---

# 7. SEVERITY

Use:

P1 — critical

Platform unavailable or essential function unavailable.

P2 — high

Essential function significantly degraded.

P3 — normal

Non-blocking malfunction or operational problem.

P4 — question / guidance

Usage question or minor request.

Do not automatically infer severity solely from user text.

User may suggest severity.

Support agent may adjust it with audit trail.

---

# 8. TICKET CATEGORIES

Initial categories:

ACCESS
LOGIN
SEARCH
CNPJ
DATA
EXPORT
LIST
REGULATORY_RULE
PERFORMANCE
AVAILABILITY
SECURITY
LGPD
TRAINING
BILLING
OTHER

Categories MUST be configurable.

---

# 9. TEXT CONVERSATION

Create:

support_message

Fields:

id
ticket_id
author_user_id
author_type

message
created_at
edited_at

visibility

author_type:

USER
SUPPORT
SYSTEM

visibility:

PUBLIC
INTERNAL

CRQ-V users MUST NOT see INTERNAL support notes.

---

# 10. MESSAGE EDITING

User messages SHOULD NOT be destructively overwritten.

If editing is allowed:

store original version
store new version
record editor
record edit timestamp.

For audit-sensitive tickets, append correction instead of destructive edit.

---

# 11. ATTACHMENTS

Create:

support_attachment

Fields:

id
ticket_id
message_id
filename
content_type
size
sha256
storage_uri
classification
uploaded_by
uploaded_at
expires_at

Allowed initial types:

PDF
PNG
JPEG
TXT
CSV
XLSX

Set configurable size limits.

---

# 12. ATTACHMENT SECURITY

Uploads SHALL be:

size validated;
MIME validated;
extension validated;
malware scanned where available;
stored outside application filesystem;
served through authorized signed URLs.

Never execute uploaded content.

---

# 13. SUPPORT NOTIFICATIONS

Notify requester on:

ticket created
agent assigned
new public reply
status changed
ticket resolved
ticket closed

Channels:

in-app
email

Do not expose confidential ticket content in email subject lines.

---

# 14. SLA

Track:

time_to_acknowledge
time_to_first_response
time_to_restore
time_to_resolve

Targets come from SPEC-0015 unless contractual SLA supersedes them.

SLA calculation SHALL pause only for explicitly defined conditions.

Example:

WAITING_USER may pause resolution SLA when configured.

---

# 15. SUPPORT DASHBOARD

Support staff SHALL see:

open tickets
P1/P2 tickets
unassigned tickets
tickets near SLA
tickets over SLA
average response time
average resolution time
tickets by category
tickets by status
tickets by requester
recent activity

---

# 16. SEARCH

Allow ticket search by:

ticket number
subject
requester
category
status
severity
date
assigned agent

Do not expose cross-tenant support data.

---

# 17. LINK TO APPLICATION CONTEXT

Ticket may optionally reference:

company
CNPJ
saved list
export
import job
incident
ruleset
release

Example:

related_entity_type = EXPORT
related_entity_id = ...

This allows support to understand the user's context without copying
large amounts of data into the ticket.

---

# 18. CREATE TICKET FROM ERROR

Application error screens MAY expose:

"Open support ticket"

Automatically attach safe metadata:

request_id
correlation_id
application_version
page
timestamp

Do NOT automatically attach:

tokens
cookies
passwords
confidential payloads.

---

# 19. WEBRTC OBJECTIVE

Allow an authenticated CRQ-V user and authorized support agent to
establish a real-time audio/video support session directly in the web
application.

Initial recommended scope:

1-to-1 support calls.

Do NOT implement multiparty conferencing in Phase 1.

---

# 20. CALL TYPES

Support:

AUDIO
VIDEO

Default:

AUDIO

Video is optional and user controlled.

---

# 21. CALL MODEL

Create:

support_call

Fields:

id
tenant_id
ticket_id

requested_by
support_agent_id

call_type

status

requested_at
accepted_at
started_at
ended_at

ended_by
end_reason

duration_seconds

signaling_room_id

turn_used
connection_type

quality_summary_json

---

# 22. CALL STATUS

REQUESTED
RINGING
ACCEPTED
CONNECTING
CONNECTED
ENDED
FAILED
DECLINED
CANCELLED
TIMEOUT

---

# 23. CALL FLOW

User:

Open ticket
→ Request call

Support:

Receive call request
→ Accept

System:

Create ephemeral signaling room
→ negotiate WebRTC
→ ICE candidate discovery
→ STUN
→ TURN fallback if required
→ establish encrypted media session

At end:

close room
→ revoke temporary credentials
→ store metadata
→ emit audit event.

---

# 24. SIGNALING

WebRTC media SHALL NOT pass through the application API.

API handles:

authorization
room creation
call lifecycle
temporary credentials

Signaling MAY use:

WebSocket

Recommended:

/ws/support/calls/{call_id}

Messages:

offer
answer
ice-candidate
hangup
state

---

# 25. STUN

Use STUN for public endpoint discovery.

STUN servers SHALL be configurable.

Do not hard-code provider-specific infrastructure into business logic.

---

# 26. TURN

TURN is REQUIRED as fallback for environments where direct peer-to-peer
connection fails.

Without TURN, WebRTC support is not operationally reliable behind
government/corporate NATs and firewalls.

TURN credentials SHALL be:

temporary
short-lived
scoped to the call.

Never expose permanent TURN credentials in frontend source.

---

# 27. SELF-HOSTED TURN

Preferred initial option:

coturn

Reasons:

low cost;
portable;
well understood;
no forced commercial provider dependency.

Configuration SHALL remain replaceable.

---

# 28. TURN COST CONTROL

Track:

calls
TURN sessions
relay bytes
duration
bandwidth estimate

TURN relay can become the principal infrastructure cost of WebRTC.

Expose monthly usage to administrators.

---

# 29. MEDIA SECURITY

Use standard WebRTC encryption:

DTLS-SRTP.

Application SHALL NOT disable browser WebRTC media encryption.

Media SHALL NOT be transmitted unencrypted.

---

# 30. RECORDING

Phase 1:

CALL RECORDING IS DISABLED.

No automatic audio/video recording.

Reasons:

privacy
LGPD
storage
consent
contractual scope
security

If recording is ever required:

create a separate specification.

---

# 31. SCREEN SHARING

Optional Phase 2 feature.

If implemented:

user must explicitly start sharing;
user selects screen/window/tab through browser APIs;
support agent cannot remotely force screen sharing.

No remote desktop control in this SPEC.

---

# 32. REMOTE CONTROL

OUT OF SCOPE.

WebRTC support DOES NOT provide:

remote keyboard control;
remote mouse control;
automatic desktop access;
file-system access.

Any future remote-assistance function requires separate security review.

---

# 33. CAMERA AND MICROPHONE PERMISSIONS

Browser permission SHALL be requested only when user initiates a call.

Never request microphone/camera permission during normal page load.

If user chooses AUDIO:

do not request camera.

---

# 34. PRE-CALL CHECK

Before connecting, test:

microphone availability
camera availability when requested
network connectivity
WebRTC support
STUN reachability
TURN availability

Display simple result:

READY
WARNING
FAILED

---

# 35. CALL DEVICE SELECTION

Allow selection where browser supports it:

microphone
speaker/output
camera

Remember preference only where safe.

Do not store device labels unnecessarily.

---

# 36. CALL UI

Controls:

mute microphone
unmute
camera on/off
hang up
device settings
connection state
duration

Optional:

screen sharing

Display ticket number during call.

---

# 37. CONNECTION QUALITY

Collect minimal WebRTC statistics:

packet loss
round-trip time
jitter
bitrate
connection type

Do not store raw media.

Quality information should be aggregated.

---

# 38. QUALITY LEVEL

Compute simple classification:

GOOD
FAIR
POOR

Used only for troubleshooting.

It is not a contractual SLA unless explicitly adopted later.

---

# 39. NETWORK FALLBACK

If WebRTC fails:

ticket text conversation remains available.

UI SHALL display:

"Não foi possível estabelecer a ligação. Continue o atendimento pelo
chamado."

Never leave support unavailable because WebRTC failed.

---

# 40. BROWSER SUPPORT

WebRTC support SHALL target current supported versions of:

Chrome
Edge
Firefox
Safari

Feature detection is mandatory.

Do not depend exclusively on user-agent strings.

---

# 41. MOBILE / TABLET

Calls MAY work on mobile browsers.

Initial acceptance requirement:

desktop
tablet

Mobile support is best-effort unless explicitly adopted as requirement.

---

# 42. AUTHORIZATION

Only:

ticket requester;
authorized CRQ-V participants;
assigned support agents;
authorized support supervisors

may join the call.

Knowing call_id MUST NOT grant access.

---

# 43. EPHEMERAL ROOM

Signaling rooms SHALL be temporary.

Room lifecycle:

created for call
active during negotiation/session
destroyed after call

Do not reuse signaling room IDs across calls.

---

# 44. TEMPORARY CALL TOKEN

Create short-lived call token.

Claims:

call_id
user_id
tenant_id
role
expires_at

Token MUST NOT be equivalent to normal application session token.

---

# 45. CALL AUDIT

Generate audit events:

SUPPORT_CALL_REQUESTED
SUPPORT_CALL_ACCEPTED
SUPPORT_CALL_STARTED
SUPPORT_CALL_ENDED
SUPPORT_CALL_FAILED
SUPPORT_CALL_DECLINED

Store metadata only.

Do NOT store:

raw SDP indefinitely;
ICE credentials;
media content;
audio;
video.

---

# 46. HERACLITUS INTEGRATION

The following support events SHOULD be written to HeraclitusDB:

SUPPORT_TICKET_CREATED
SUPPORT_TICKET_ASSIGNED
SUPPORT_TICKET_STATUS_CHANGED
SUPPORT_TICKET_RESOLVED
SUPPORT_TICKET_CLOSED

SUPPORT_CALL_REQUESTED
SUPPORT_CALL_STARTED
SUPPORT_CALL_ENDED
SUPPORT_CALL_FAILED

Store:

ticket_id
call_id
actor
timestamp
status
duration
result

Do not send message text to HeraclitusDB by default.

PostgreSQL remains the controlled content store.

---

# 47. WHY MESSAGE TEXT IS NOT IMMUTABLE AUDIT PAYLOAD

Support tickets may contain:

screenshots
technical descriptions
personal data
internal information

Therefore:

HeraclitusDB stores lifecycle evidence.

PostgreSQL/object storage stores ticket content according to retention
policy.

This avoids permanent duplication of unnecessary sensitive content.

---

# 48. TICKET AUDIT

Every sensitive operation SHALL generate audit event:

ticket creation
assignment
severity change
internal/public message
attachment download
status transition
call creation
ticket export

Message body does not need to be duplicated into audit log.

Use:

message_id
message_hash

where evidence is needed.

---

# 49. MESSAGE HASH

Optionally compute:

SHA-256(canonical_message)

Audit event may record:

message_id
message_hash

This proves later that ticket content was not silently changed without
copying full content to the immutable store.

---

# 50. ATTACHMENT AUDIT

Record:

attachment_id
sha256
uploaded_by
downloaded_by
timestamp

Do not duplicate attachment bytes in HeraclitusDB.

---

# 51. SUPPORT AGENT ROLE

Add:

SUPPORT_AGENT

Optional:

SUPPORT_SUPERVISOR

Permissions:

SUPPORT_AGENT:
view assigned tickets
reply
request/accept call
resolve

SUPPORT_SUPERVISOR:
view all tenant tickets
reassign
change severity
manage SLA
review reports

---

# 52. INTERNAL NOTES

Support staff may add INTERNAL notes.

They SHALL NOT be visible to ordinary requester.

Audit:

SUPPORT_INTERNAL_NOTE_CREATED

Do not copy note content into general audit event.

---

# 53. SECURITY INCIDENT ESCALATION

Ticket may be escalated to security incident.

Action:

"Convert to incident"

Creates:

incident

linked by:

incident_id

Original support history remains.

---

# 54. P1 ESCALATION

P1 ticket SHOULD:

generate alert;
notify support;
notify operational responsible;
create incident when appropriate.

WebRTC MAY be offered automatically.

Do not automatically call the user without acceptance.

---

# 55. CALL INVITATION

Calls are user-initiated or explicitly accepted.

No unsolicited media connection.

Example:

"Suporte solicita uma ligação de áudio."

Buttons:

ACEITAR
RECUSAR

---

# 56. NOTIFICATIONS

Call notifications:

in-app
optional email

Future:

browser push notification.

Do not depend on push notifications for basic support operation.

---

# 57. WAITING QUEUE

Optional support queue:

request call
→ waiting

Agent accepts first appropriate request.

Initial implementation may remain ticket-based 1-to-1 without queue.

---

# 58. BUSINESS HOURS

Support configuration:

timezone
business_days
start_time
end_time
holidays

Display estimated availability.

Do not falsely promise immediate WebRTC support outside staffed periods.

---

# 59. OUTSIDE BUSINESS HOURS

Text ticket creation remains available 24/7.

WebRTC button may display:

"Atendimento por ligação disponível em horário de suporte."

---

# 60. PRIVACY NOTICE

Before first WebRTC call show concise notice:

- microphone/camera only activated with permission;
- media is encrypted in transit;
- calls are not recorded;
- connection metadata may be retained for support and security.

Acceptance stored with:

user_id
notice_version
accepted_at

---

# 61. LGPD

Apply data minimization.

Store only support information necessary for:

service execution
security
audit
contract management

Retention SHALL be configurable.

Ticket content is not automatically permanent.

---

# 62. RETENTION

Suggested configurable classes:

ticket metadata
ticket messages
attachments
call metadata
incident records
audit lifecycle events

Retention policy SHALL not be hard-coded.

---

# 63. TICKET EXPORT

Authorized user MAY export one ticket as:

PDF
or
HTML

Containing:

ticket number
timeline
public messages
attachments list
resolution

Internal notes only for authorized administrative exports.

---

# 64. SUPPORT API

Minimum endpoints:

POST /api/v1/support/tickets

GET /api/v1/support/tickets

GET /api/v1/support/tickets/{id}

POST /api/v1/support/tickets/{id}/messages

POST /api/v1/support/tickets/{id}/attachments

PATCH /api/v1/support/tickets/{id}

POST /api/v1/support/tickets/{id}/resolve

POST /api/v1/support/tickets/{id}/close

POST /api/v1/support/tickets/{id}/calls

GET /api/v1/support/calls/{id}

POST /api/v1/support/calls/{id}/accept

POST /api/v1/support/calls/{id}/decline

POST /api/v1/support/calls/{id}/end

---

# 65. SIGNALING API

WebSocket:

/api/v1/support/calls/{id}/signal

or dedicated signaling service.

Messages:

CALL_READY
OFFER
ANSWER
ICE_CANDIDATE
PEER_JOINED
PEER_LEFT
HANGUP
ERROR

Validate all messages.

---

# 66. SIGNALING SECURITY

Never trust client-provided:

user_id
tenant_id
role

Resolve authorization server-side from authenticated connection.

---

# 67. SIGNALING RATE LIMIT

Rate-limit:

connection attempts
offers
ICE messages
reconnect attempts

Protect against signaling abuse.

---

# 68. WEBRTC CANDIDATE PRIVACY

Avoid unnecessary long-term storage of ICE candidate details.

Network addresses and connection metadata may expose infrastructure
information.

Store only summarized connection type when possible.

---

# 69. TURN LOG PRIVACY

TURN server logs SHALL NOT contain more user information than required.

Define retention.

Protect access.

---

# 70. CALL FAILURE REASONS

Normalized reasons:

USER_DECLINED
AGENT_DECLINED
TIMEOUT
NO_MEDIA_PERMISSION
NO_DEVICE
SIGNALING_FAILURE
ICE_FAILURE
TURN_FAILURE
NETWORK_LOST
BROWSER_UNSUPPORTED
SERVER_ERROR
USER_HANGUP
AGENT_HANGUP

---

# 71. SUPPORT METRICS

Track:

tickets_created
tickets_resolved
tickets_closed

tickets_by_category
tickets_by_priority

first_response_time
resolution_time

calls_requested
calls_connected
calls_failed

average_call_duration
TURN_usage_rate

call_quality_good
call_quality_fair
call_quality_poor

---

# 72. MONTHLY SUPPORT REPORT

Include in contractual monthly report:

tickets
severity distribution
response SLA
resolution SLA
P1/P2 incidents
call count
failed calls
average duration
WebRTC availability
support improvements

Do not expose unnecessary user message contents.

---

# 73. OBSERVABILITY

Monitor:

support API latency
WebSocket connections
active calls
signaling errors
STUN failures
TURN failures
TURN bandwidth
call setup time
call failure rate

---

# 74. HEALTH

Expose internal checks:

support_database
signaling
turn_reachability

WebRTC failure SHALL NOT make the entire CRQ-V application unready.

---

# 75. COST CONTROL

The CRQ-V contract has low economic value.

WebRTC infrastructure SHALL remain lightweight.

Recommended:

existing API
WebSocket signaling
coturn
no media server for 1-to-1 calls

Do NOT introduce:

SFU
MCU
recording cluster
Kafka

for initial 1-to-1 support.

---

# 76. WHY P2P FIRST

WebRTC 1-to-1 normally sends media peer-to-peer.

Advantages:

lower server cost
lower bandwidth cost
simpler architecture

TURN is relay fallback.

This matches the project's low-cost constraint.

---

# 77. FUTURE SFU

An SFU such as:

LiveKit
Janus
mediasoup
Jitsi

MAY be evaluated later if requirements expand to:

multiparty calls
recording
supervision
advanced screen sharing

Not required for Phase 1.

---

# 78. TESTS — TICKETS

Automated tests SHALL cover:

create ticket
reply
internal note authorization
assignment
severity change
status transitions
resolve
close
attachment permissions
tenant isolation
SLA calculation
ticket search

---

# 79. TESTS — WEBRTC

Automated/integration tests SHALL cover:

create call
accept call
decline call
timeout
authorization
expired call token
WebSocket connection
signaling exchange
call end

Browser E2E SHALL exercise real WebRTC where CI environment allows.

---

# 80. TURN TEST

Test scenario:

block direct peer-to-peer path.

Expected:

TURN relay establishes media connection.

If TURN has never been tested under forced relay conditions,
WebRTC support is NOT considered production-ready.

---

# 81. FIREWALL TEST

Validate from:

normal broadband
mobile network
restricted corporate network where available

Document failures.

---

# 82. MEDIA PERMISSION TEST

Test:

microphone denied
camera denied
permission revoked
device disconnected during call

Application SHALL recover gracefully.

---

# 83. CONNECTION DROP TEST

Disconnect network during call.

Expected:

UI indicates reconnecting;
attempt ICE restart/reconnect;
eventually recover or end cleanly.

Text ticket remains available.

---

# 84. SECURITY TESTS

Test:

unauthorized call join
cross-tenant call access
reused call token
expired token
WebSocket spoofing
message flooding
attachment abuse
ticket ID enumeration
internal-note leakage

---

# 85. ACCESSIBILITY

Call UI SHALL support:

keyboard operation
accessible buttons
visible focus
screen reader labels
status announcements

Do not rely solely on visual icons for:

mute
camera
hangup.

---

# 86. FALLBACK CONTACT

The platform SHOULD display alternative support channel where configured:

support email

WebRTC is enhancement, not single point of failure.

---

# 87. PHASE 1

Implement:

text tickets
messages
attachments
assignment
status
severity
SLA
email/in-app notifications
support dashboard
audit events

This phase is P0.

---

# 88. PHASE 2

Implement WebRTC:

audio
optional video
WebSocket signaling
STUN
TURN
temporary credentials
pre-call check
call metadata
audit integration

This phase is P1.

---

# 89. PHASE 3

Optional:

screen sharing
advanced call quality
call queue
supervisor dashboard

No recording.

---

# 90. PHASE 4

Only if future requirement exists:

multiparty support
SFU
recording
transcription

Requires separate privacy/security specification.

---

# 91. ACCEPTANCE — TEXT SUPPORT

PASS when:

user can create a ticket;
support agent receives it;
conversation works;
attachment works;
status works;
assignment works;
SLA timestamps work;
notifications work;
audit exists;
tenant isolation passes.

---

# 92. ACCEPTANCE — WEBRTC

PASS when:

authenticated user requests call;
authorized support agent accepts;
audio connection establishes;
video can optionally establish;
TURN fallback works;
call can end cleanly;
call metadata is recorded;
no media is recorded;
text support continues if call fails;
audit event is generated.

---

# 93. DEFINITION OF DONE

SPEC is complete when:

ticketing is fully functional;

WebRTC audio is functional;

video is functional if enabled;

TURN fallback has been tested;

authorization tests pass;

cross-tenant tests pass;

ticket attachments are protected;

WebRTC tokens expire;

call metadata is audited;

raw media is not stored;

Heraclitus receives lifecycle events;

support reports work;

CI contains relevant tests;

documentation exists;

operational runbook exists.

---

# 94. RUNBOOK

Create:

docs/operations/SUPPORT-WEBRTC-RUNBOOK.md

Include:

ticket outage
signaling outage
TURN outage
high packet loss
call failures
credential rotation
emergency disable WebRTC
fallback to text support

---

# 95. EMERGENCY FEATURE FLAG

Configuration:

SUPPORT_TICKETS_ENABLED=true
SUPPORT_WEBRTC_ENABLED=true
SUPPORT_WEBRTC_VIDEO_ENABLED=true

Emergency:

SUPPORT_WEBRTC_ENABLED=false

Text ticket support SHALL remain operational.

---

# 96. FINAL RULE

Text support is contractual service infrastructure.

WebRTC is a value-added real-time support capability.

Failure of WebRTC MUST NOT prevent:

ticket creation
ticket replies
incident handling
contractual support communication.

The system SHALL always degrade gracefully from:

WEBRTC
→ TEXT SUPPORT

rather than from:

WEBRTC
→ NO SUPPORT.