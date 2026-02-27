# Pass 1 Security Audit — Agent APP30
**App:** forkliftiqapp (Android/Java)
**Date:** 2026-02-27
**Agent:** APP30

---

## Step 1 — Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

**Discrepancy recorded:** Checklist specifies `Branch: main`; actual branch is `master`. Proceeding on `master` as instructed.

---

## Step 2 — Checklist Reference

Checklist read in full: `/c/Projects/cig-audit/audit-skills/PASS1-CHECKLIST-forkliftiqapp.md`
Sections reviewed: Signing and Keystores, Network Security, Data Storage, Input and Intent Handling, Authentication and Session, Third-Party Libraries, Google Play and Android Platform.

---

## Step 3 — Files Assigned

1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/results/PreStartQuestionResultArray.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/results/ReportResultArray.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/results/SaveImpactResult.java`

---

## Step 4 — Reading Evidence

### File 1: PreStartQuestionResultArray.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.PreStartQuestionResultArray`

**Superclass:** `WebServiceResultPacket`
**Interfaces implemented:** `Serializable`

**Fields:**
- Line 14: `public ArrayList<PreStartQuestionItem> arrayList`

**Public methods:**
- Line 16: `public PreStartQuestionResultArray()` — default constructor
- Line 19: `public PreStartQuestionResultArray(JSONArray jsonArray) throws JSONException` — parameterised constructor; iterates `jsonArray`, constructing `PreStartQuestionItem` from each `JSONObject` and appending to `arrayList`

**Android components declared:** None (plain data model class)

---

### File 2: ReportResultArray.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.ReportResultArray`

**Superclass:** `WebServiceResultPacket`
**Interfaces implemented:** `Serializable`

**Fields:**
- Line 14: `public ArrayList<ReportItem> arrayList`

**Public methods:**
- Line 16: `public ReportResultArray()` — default constructor
- Line 19: `public ReportResultArray(JSONArray jsonArray) throws JSONException` — parameterised constructor; iterates `jsonArray`, constructing `ReportItem` from each `JSONObject` and appending to `arrayList`

**Android components declared:** None (plain data model class)

---

### File 3: SaveImpactResult.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.SaveImpactResult`

**Superclass:** `WebServiceResultPacket`
**Interfaces implemented:** `Serializable`

**Fields (all public):**
- Line 14: `public int id`
- Line 15: `public String signature`
- Line 16: `public String image`
- Line 17: `public String injury_type`
- Line 18: `public String witness`
- Line 19: `public String location`
- Line 20: `public boolean injury`
- Line 21: `public boolean near_miss`
- Line 22: `public String description`
- Line 23: `public String report_time`
- Line 24: `public String event_time`
- Line 25: `public String job_number`

**Public methods:**
- Line 27: `public SaveImpactResult()` — default constructor
- Line 30: `public SaveImpactResult(JSONObject jsonObject) throws JSONException` — parameterised constructor; calls `super(jsonObject)` then deserialises each nullable field from the `JSONObject`

**Android components declared:** None (plain data model class)

---

## Step 5 — Findings by Checklist Section

### Section 1 — Signing and Keystores

No issues found — Section 1. These files contain no signing configuration, keystore references, passwords, or credential values.

---

### Section 2 — Network Security

No issues found — Section 2. No HTTP client calls, URL construction, TrustManager implementations, hostname verifier overrides, or hardcoded endpoint strings are present in any of the three files.

---

### Section 3 — Data Storage

**Finding — Medium — Public fields on Serializable result objects exposing sensitive incident data**

All three classes expose their fields with `public` access modifier and implement `java.io.Serializable`. The concern is most acute in `SaveImpactResult.java`.

`SaveImpactResult` holds fields that constitute workplace incident records: `injury_type` (line 17), `witness` (line 18), `location` (line 19), `injury` (line 20), `near_miss` (line 21), and `description` (line 22). These represent safety-critical, personally identifiable, and potentially legally significant data. Because the class implements `Serializable` with all fields public and no `serialVersionUID` declared, instances can be written to disk or passed via Android's `Intent` extras and `Bundle` mechanisms in serialised form without any access control.

The absence of `private` access control combined with `Serializable` means:
- Any component that obtains a reference to a `SaveImpactResult` object has unrestricted read and write access to all incident fields, including overwriting injury and witness data.
- If passed via `Intent` extras, the serialised payload is readable by any component that receives the intent. If an exported component (identified by other agents) receives such an intent, incident data is exposed to third-party apps.
- No `serialVersionUID` is declared; this can cause `InvalidClassException` on version upgrades and is a minor robustness issue.

The same public-field pattern applies to `PreStartQuestionResultArray` (`arrayList`, line 14) and `ReportResultArray` (`arrayList`, line 14), which hold pre-start inspection question data and report data respectively. These are lower sensitivity than incident records but the same structural risk applies.

**Recommendation (for Pass 2 / remediation):** Declare fields `private`, provide getters, and consider `EncryptedSharedPreferences` or equivalent for any persistence of `SaveImpactResult` data. Declare `serialVersionUID` on all three classes.

---

### Section 4 — Input and Intent Handling

No issues found — Section 4. None of the three files are Activity, Fragment, Service, BroadcastReceiver, or ContentProvider subclasses. No WebView usage, no intent construction, no deep link handling is present.

The `JSONArray` / `JSONObject` inputs parsed in the constructors are consumed directly via the Android `org.json` library without additional validation beyond null-checks (`!jsonObject.isNull(...)`). This is standard for internal web service result deserialization and does not constitute an injection surface in these files in isolation; however, the absence of type or bounds validation on fields such as `description` (free text, unbounded) and `witness` is noted — if these values were ever rendered in a WebView or used to construct dynamic queries, they would need sanitization upstream.

---

### Section 5 — Authentication and Session

No issues found — Section 5. No authentication tokens, session identifiers, credentials, or login logic are present in these files.

---

### Section 6 — Third-Party Libraries

No issues found — Section 6. The only imports are from the Java standard library (`java.io.Serializable`, `java.util.ArrayList`, `java.math.BigDecimal`) and the Android platform (`org.json.*`), plus internal package imports. No third-party dependencies are introduced by these files.

Note: `java.math.BigDecimal` is imported in all three files but is not used by any field or method in any of the three classes. This is dead import code; it carries no security implication but indicates minor code hygiene issues.

---

### Section 7 — Google Play and Android Platform

No issues found — Section 7. No deprecated API usage, no permission declarations, no SDK version references, and no AsyncTask usage are present in these files.

---

## Summary Table

| # | File | Severity | Finding |
|---|------|----------|---------|
| 1 | `SaveImpactResult.java` | Medium | All incident-data fields are `public` with no access control; class is `Serializable` enabling uncontrolled serialisation of sensitive safety/PII data |
| 2 | `PreStartQuestionResultArray.java` | Low | `arrayList` field is `public`; class is `Serializable` without `serialVersionUID` |
| 3 | `ReportResultArray.java` | Low | `arrayList` field is `public`; class is `Serializable` without `serialVersionUID` |
| 4 | All three files | Info | Unused import of `java.math.BigDecimal` in all three files |

---

## Audit Metadata

- **Agent:** APP30
- **Pass:** 1
- **Checklist:** `/c/Projects/cig-audit/audit-skills/PASS1-CHECKLIST-forkliftiqapp.md`
- **Branch audited:** `master` (checklist listed `main` — discrepancy recorded)
- **Files reviewed:** 3 of 3
- **Lines reviewed:** 32 + 32 + 99 = 163 total
