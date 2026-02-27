# Pass 1 Security Audit — forkliftiqapp
**Agent ID:** APP32
**Date:** 2026-02-27
**Stack:** Android/Java

---

## Step 1 — Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

**Discrepancy noted:** The checklist specifies `Branch: main`, but the actual branch is `master`. Audit proceeds on `master` as instructed.

---

## Step 2 — Checklist

Full checklist read from `/c/Projects/cig-audit/audit-skills/PASS1-CHECKLIST-forkliftiqapp.md`. Sections covered:
1. Signing and Keystores
2. Network Security
3. Data Storage
4. Input and Intent Handling
5. Authentication and Session
6. Third-Party Libraries
7. Google Play and Android Platform

---

## Step 3 — Assigned Files

1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/results/ServiceRecordResultArray.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/results/ServiceSummaryResultArray.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/results/SessionEndResult.java`

---

## Step 4 — Reading Evidence

### File 1: ServiceRecordResultArray.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.ServiceRecordResultArray`

**Superclass:** `WebServiceResultPacket` (implements `Serializable`)

**Fields:**
- `public ArrayList<ServiceRecordItem> arrayList` (line 14) — public, non-final

**Public methods:**
- `ServiceRecordResultArray()` — default constructor, line 16
- `ServiceRecordResultArray(JSONArray jsonArray) throws JSONException` — parameterized constructor, line 19

**Activities / Services / BroadcastReceivers / ContentProviders declared:** None

**Summary of logic:**
- Default constructor takes no arguments (lines 16–17).
- Parameterized constructor (lines 19–30): initializes `arrayList`, iterates a `JSONArray` if non-null, constructs a `ServiceRecordItem` from each `JSONObject`, and adds it to the list.

---

### File 2: ServiceSummaryResultArray.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.ServiceSummaryResultArray`

**Superclass:** `WebServiceResultPacket` (implements `Serializable`)

**Fields:**
- `public ArrayList<ServiceSummaryItem> arrayList` (line 14) — public, non-final

**Public methods:**
- `ServiceSummaryResultArray()` — default constructor, line 16
- `ServiceSummaryResultArray(JSONArray jsonArray) throws JSONException` — parameterized constructor, line 19

**Activities / Services / BroadcastReceivers / ContentProviders declared:** None

**Summary of logic:**
- Structurally identical to `ServiceRecordResultArray` with the item type changed to `ServiceSummaryItem`.

---

### File 3: SessionEndResult.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.SessionEndResult`

**Superclass:** `WebServicePacket` (implements `Serializable`)

**Fields:**
- `public String message_id` (line 11) — public, non-final
- `public String error` (line 12) — public, non-final

**Public methods:**
- `SessionEndResult()` — default constructor, line 14
- `SessionEndResult(JSONObject jsonObject) throws JSONException` — parameterized constructor, line 17

**Activities / Services / BroadcastReceivers / ContentProviders declared:** None

**Summary of logic:**
- Default constructor takes no arguments (lines 14–15).
- Parameterized constructor (lines 17–34): calls `super(jsonObject)`, then conditionally parses `message_id` and `error` string fields from the JSON object using null checks (`isNull`).

---

## Step 5 — Security Review by Checklist Section

### Section 1 — Signing and Keystores

No signing configuration, keystore files, Gradle build scripts, or properties files are present in the assigned files. These are pure data-model/result classes.

No issues found — Section 1.

---

### Section 2 — Network Security

The assigned files are server-response deserialization classes. They consume already-received JSON; they do not initiate network connections, configure HTTP clients, or specify URLs.

No hardcoded API endpoints, IP addresses, or TLS configuration present.

No issues found — Section 2.

---

### Section 3 — Data Storage

**Finding — LOW: Public non-final fields expose deserialized data without access control**

All three classes expose their deserialized data through public, non-final fields with no accessor methods:

- `ServiceRecordResultArray.arrayList` (line 14) — `public ArrayList<ServiceRecordItem>`
- `ServiceSummaryResultArray.arrayList` (line 14) — `public ArrayList<ServiceSummaryItem>`
- `SessionEndResult.message_id` (line 11) — `public String`
- `SessionEndResult.error` (line 12) — `public String`

These fields can be freely read or mutated by any code holding a reference to the object. For `SessionEndResult`, the field `error` may carry server-side error strings that could include diagnostic information useful to an attacker if logged or displayed; `message_id` may carry a session-scoped identifier. While none of these classes directly persist data to storage, the public field design means a future caller could inadvertently write these values to unencrypted SharedPreferences, a log, or a file without the class offering any resistance.

This is a design hygiene observation rather than an immediately exploitable vulnerability in these files alone. The actual risk depends on how callers handle these objects (out of scope for this assignment).

**Finding — INFORMATIONAL: Serializable implementation without explicit serialVersionUID**

All three classes implement `java.io.Serializable` but declare no `serialVersionUID`. Without an explicit `serialVersionUID`, the JVM generates one at compile time from the class structure. If the class is ever modified and a previously serialized object is deserialized, a `InvalidClassException` will be thrown rather than handled gracefully. For a production app that may persist or transmit serialized objects, this creates a fragility risk. No credential or data-integrity security risk is present in isolation.

No issues found related to external storage, encrypted preferences, `allowBackup`, `MODE_WORLD_READABLE`, or static credential caching in these files.

---

### Section 4 — Input and Intent Handling

The assigned files contain no Activity, Service, BroadcastReceiver, ContentProvider, WebView, or Intent handling code.

**Finding — INFORMATIONAL: No input validation on JSON array bounds or item count**

`ServiceRecordResultArray` (lines 23–29) and `ServiceSummaryResultArray` (lines 23–29) iterate over the full length of a server-supplied `JSONArray` without any bounds check on the number of elements. A server returning an abnormally large array would cause unbounded `ArrayList` growth, consuming heap memory. This is a denial-of-service robustness concern rather than a code-injection risk, and is low severity given the app communicates with a trusted backend. However, it is worth noting in the context of input validation.

`SessionEndResult` (lines 24–32) uses `isNull()` guards before extracting fields, which is correct defensive practice for optional JSON fields.

No exported components, deep links, or implicit intents present.

No issues found — Section 4 (no security issues; informational note recorded above).

---

### Section 5 — Authentication and Session

`SessionEndResult` carries a `message_id` and `error` field deserialized from the session-end response. This class represents the server acknowledgment when a session ends.

No token storage, credential caching, or logout logic is present in these files. Whether the `message_id` is used as a session token elsewhere, and whether it is cleared on logout, cannot be determined from these files alone.

No issues found — Section 5 (scope limited to assigned files).

---

### Section 6 — Third-Party Libraries

The assigned files import only:
- `org.json.JSONException`
- `org.json.JSONObject`
- `org.json.JSONArray`
- `java.io.Serializable`
- `java.util.ArrayList`
- `java.math.BigDecimal` (imported but unused in both array result classes)

All imports are from the Android platform SDK or the Java standard library. No third-party dependencies are introduced in these files.

**Finding — INFORMATIONAL: Unused import `java.math.BigDecimal`**

`ServiceRecordResultArray.java` (line 8) and `ServiceSummaryResultArray.java` (line 8) both import `java.math.BigDecimal` but neither class uses it. This is dead code / import pollution. It carries no security impact but indicates the files may have been generated from a template without cleanup.

No CVE-relevant third-party libraries present in these files.

No issues found — Section 6.

---

### Section 7 — Google Play and Android Platform

The assigned files contain no `build.gradle` configuration, no `targetSdkVersion` or `minSdkVersion` declarations, no permission declarations, and no deprecated API calls such as `AsyncTask` or `startActivityForResult`.

No issues found — Section 7.

---

## Summary of Findings

| ID | Severity | Section | File | Description |
|----|----------|---------|------|-------------|
| APP32-01 | Low | 3 — Data Storage | All three files | Public non-final fields expose deserialized data (including session-related strings) without access control; any caller can freely mutate or pass values to insecure storage. |
| APP32-02 | Informational | 3 — Data Storage | All three files | No explicit `serialVersionUID` declared on `Serializable` classes; version mismatch during deserialization will produce an unhandled runtime exception. |
| APP32-03 | Informational | 4 — Input Handling | ServiceRecordResultArray.java, ServiceSummaryResultArray.java | No upper-bound limit on server-supplied JSON array length; abnormally large responses cause unbounded heap growth. |
| APP32-04 | Informational | 6 — Third-Party Libraries | ServiceRecordResultArray.java, ServiceSummaryResultArray.java | Unused import `java.math.BigDecimal` — template artifact, no security impact. |

**No Critical or High severity findings in the assigned files.**
