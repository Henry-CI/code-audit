# Pass 2 Test-Coverage Audit
**Audit run:** 2026-02-26-01
**Agent ID:** A13
**Files audited:**
- `src/main/java/com/action/BarCodeAction.java`
- `src/main/java/com/action/CalibrationAction.java`

---

## 1. Reading-Evidence Block

### 1.1 BarCodeAction

**Class:** `com.action.BarCodeAction extends org.apache.struts.action.Action`
**File:** `src/main/java/com/action/BarCodeAction.java`

**Fields / Constants:**

| Name | Type | Line | Notes |
|---|---|---|---|
| `unitDAO` | `UnitDAO` | 30 | Singleton instance; class-level field |

**Methods:**

| Method | Signature | Lines | Notes |
|---|---|---|---|
| `execute` | `ActionForward execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse) throws Exception` | 33–254 | Sole public method; 221 lines; two major branches keyed on `method` parameter |

**Logical branches inside `execute` (line references):**

| Branch | Key | Lines |
|---|---|---|
| `API_BARCODE` path | `method.equalsIgnoreCase(RuntimeConf.API_BARCODE)` (`"barcode"`) | 42–65 |
| `Load_BARCODE` path | `method.equalsIgnoreCase(RuntimeConf.Load_BARCODE)` (`"loadbarcode"`) | 66–245 |
| Unknown-method path | `else` | 246–249 |

**Key constants consumed (from `RuntimeConf`):**

| Constant | Value | Usage |
|---|---|---|
| `RuntimeConf.API_BARCODE` | `"barcode"` | Branch selector |
| `RuntimeConf.Load_BARCODE` | `"loadbarcode"` | Branch selector |
| `RuntimeConf.CHECKLIST_SECONDS` | `600` | Time-difference threshold (seconds) |

---

### 1.2 CalibrationAction

**Class:** `com.action.CalibrationAction extends org.apache.struts.action.Action`
**File:** `src/main/java/com/action/CalibrationAction.java`

**Fields / Constants:** None declared.

**Methods:**

| Method | Signature | Lines | Notes |
|---|---|---|---|
| `execute` | `ActionForward execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse) throws Exception` | 14–21 | Delegates entirely to `CalibrationJob.calibrateAllUnits()` then calls `super.execute(...)` |

---

## 2. Test-Directory Coverage Confirmation

Grep for `BarCodeAction` and `CalibrationAction` across the entire test tree (`src/test/java/`) returned **no matches**.

The four existing test files are:

| Test File | Subject |
|---|---|
| `com/calibration/UnitCalibrationImpactFilterTest.java` | `UnitCalibrationImpactFilter` logic |
| `com/calibration/UnitCalibrationTest.java` | `UnitCalibration` domain object |
| `com/calibration/UnitCalibratorTest.java` | `UnitCalibrator` calibration logic |
| `com/util/ImpactUtilTest.java` | `ImpactUtil` utility methods |

**None of these files reference, import, instantiate, or indirectly exercise `BarCodeAction` or `CalibrationAction`.** Coverage for both action classes is **0 %**.

---

## 3. Coverage Gaps — All Untested Methods, Error Paths, and Edge Cases

---

### A13-1 | Severity: CRITICAL | BarCodeAction.execute — zero test coverage

The entire `execute` method (lines 33–254) has no tests. This is the sole entry point for barcode scanning and barcode upload workflows; failures here silently corrupt checklist data or produce phantom duplicates.

---

### A13-2 | Severity: CRITICAL | CalibrationAction.execute — zero test coverage

The entire `execute` method (lines 14–21) has no tests. `CalibrationAction` triggers live database writes (`calibrateAllUnits`) and its return value is determined by `super.execute(...)` (which always returns `null`). There is no test verifying that the calibration job is actually invoked, that exceptions are surfaced, or that the HTTP response is sensible.

---

### A13-3 | Severity: CRITICAL | BarCodeAction — NullPointerException on empty `arrUnit` (API_BARCODE branch, line 50)

```java
ArrayList<UnitBean> arrUnit = unitDAO.getUnitBySerial(serial, true);
String vehId = arrUnit.get(0).getId();   // line 50 — unchecked get(0)
```

If `serial` matches no unit, `arrUnit` is empty and `arrUnit.get(0)` throws `IndexOutOfBoundsException`. There is no guard, and the exception is not caught within this branch (the outer try/catch only wraps the `Load_BARCODE` branch). The action will propagate the exception to Struts, exposing a stack trace.

No test exists for:
- Empty serial string
- Non-existent serial
- `unitDAO` returning an empty list

---

### A13-4 | Severity: CRITICAL | BarCodeAction — NullPointerException on empty `companies` list (API_BARCODE branch, line 55)

```java
List<CompanyBean> companies = companyDao.getCompanyByCompId(compId);
CompanyBean comp = companies.get(0);   // line 55 — unchecked get(0)
```

If `compId` does not exist in the database, `companies` is empty and `get(0)` throws `IndexOutOfBoundsException`. No guard is present, no test covers this path.

---

### A13-5 | Severity: CRITICAL | BarCodeAction — NumberFormatException from `Long.parseLong(driverId)` (API_BARCODE branch, line 58)

```java
String driverId = driver.replaceFirst("^0*", "");
int resutl_id = fleetcheckAction.saveResult(..., Long.parseLong(driverId), ...);  // line 58
```

If `driver` is `null`-coalesced to `""` (line 45) and after stripping leading zeros the string is empty, `Long.parseLong("")` throws `NumberFormatException`. If `driver` contains non-numeric characters (e.g., a scanner malfunction), the same exception is thrown. No test covers these cases.

---

### A13-6 | Severity: CRITICAL | BarCodeAction — `quesIds`/`quesAns` null-parameter arrays passed directly to `saveResult` (API_BARCODE branch, line 58)

```java
String[] quesIds = request.getParameterValues("quesIds");  // line 46 — can be null
String[] quesAns = request.getParameterValues("quesAns");  // line 47 — can be null
int resutl_id = fleetcheckAction.saveResult(vehId, quesIds, quesAns, ...);  // line 58
```

`HttpServletRequest.getParameterValues()` returns `null` when the parameter is absent. `FleetcheckAction.saveResult` iterates `quesion_ids` without a null check (`for (int i = 0; i < quesion_ids.length; i++)`), causing an immediate `NullPointerException`. No test verifies behavior when these parameters are missing.

---

### A13-7 | Severity: HIGH | BarCodeAction — unchecked `get(0)` on `arrUnit` list in Load_BARCODE loop (line 198)

```java
List<UnitBean> arrUnit = unitDAO.getUnitById(resultBean.getUnit_id());
String compId = arrUnit.get(0).getComp_id();  // line 198 — unchecked get(0)
```

If `unit_id` extracted from the barcode data does not exist in the database, `arrUnit` is empty, producing `IndexOutOfBoundsException`. This occurs inside a for-loop over accumulated results; the outer `catch(Exception e)` (line 240) swallows this silently after printing a stack trace, meaning the remaining results in the loop are silently skipped with no user-visible error message other than the generic `msg` string.

---

### A13-8 | Severity: HIGH | BarCodeAction — silent exception swallowing in Load_BARCODE catch block (line 240–244)

```java
} catch(Exception e) {
    e.getMessage();   // return value discarded — line 242
    e.printStackTrace();
}
```

The entire Load_BARCODE processing block (lines 69–244) is wrapped in a single broad catch. On any exception the method continues to `request.setAttribute("method", method)` and returns `"success"` (line 253). Callers receive an HTTP 200 with no indication that data was not saved. No test verifies that errors produce appropriate responses or log entries.

---

### A13-9 | Severity: HIGH | BarCodeAction — `NumberFormatException` from `Long.parseLong(driver)` in Load_BARCODE loop (line 116, 151, 187)

```java
resultBean.setDriver_id(Long.parseLong(driver));  // lines 116, 151, 187
```

`driver` is initialized to `"0"` but may remain at `"0"` or may be set from the scanned token after stripping. If the scanner emits malformed data the parse will fail. These calls are inside the try/catch block but the exception is silently swallowed (A13-8 above). No test exercises malformed driver tokens.

---

### A13-10 | Severity: HIGH | BarCodeAction — Load_BARCODE path: `data` parameter null/malformed splits produce silent wrong results

```java
String data = request.getParameter("data")==null?"":request.getParameter("data");
// ...
String[] result = barcode.split("END");  // line 84
```

If `<Memory>` and `<End>` tags are absent, `barcode` remains `""`, and `"".split("END")` returns a one-element array containing an empty string. The loop (lines 87–190) still runs on this empty string, creating a `ResultBean` with `unit_id = "0"`. The guard at line 184 (`if(!unit.equalsIgnoreCase("0"))`) prevents the bad bean from being saved, but the wrong branch check on line 81 merely sets `msg = "Corrupted Data! Invalid Fomrat!"` (note: typo "Fomrat") without exiting. Subsequent processing may or may not fail silently. No test exercises the corrupted-data path.

---

### A13-11 | Severity: HIGH | BarCodeAction — `StringTimeDifference` called with time strings that may not conform to `"yyyy/MM/dd HH:mm:ss"` format

```java
DateUtil.StringTimeDifference(tempChecktime, checktime, TimeUnit.SECONDS, "yyyy/MM/dd HH:mm:ss")
```

`tempChecktime` is assembled from raw scanner tokens (`content[0]+" "+content[1]`). If the scanner emits a non-conforming date/time format, `SimpleDateFormat.parse` inside `StringTimeDifference` throws `ParseException`, which is caught inside `DateUtil` and printed to stdout while returning `0`. A return value of `0` means the 30-minute split logic is never triggered, silently merging results that should be split. No test covers malformed time tokens.

---

### A13-12 | Severity: HIGH | BarCodeAction — `pos <= 0` logic error: `indexOf` can return 0 for first character (line 133–138)

```java
int pos = answered.indexOf('Y') > 0 ? answered.indexOf('Y') : answered.indexOf('N');
if(pos > 0)  // line 134
{
    queId  = answered.substring(0, pos);
    anser  = answered.substring(pos, pos+1);
    tempUnit = answered.substring(pos+1);
}
```

If `Y` or `N` appears at index 0 (i.e., the question ID is absent), `pos` is 0 and the condition `pos > 0` is false. The answer is silently skipped with `queId`, `anser`, and `tempUnit` left as their prior or initial values. The prior `unit` variable then drives subsequent split logic incorrectly. No test covers this edge case.

---

### A13-13 | Severity: HIGH | BarCodeAction — `answered.substring(pos+1)` may throw `StringIndexOutOfBoundsException` (line 138)

```java
tempUnit = answered.substring(pos+1);
```

If the scanned token ends exactly at `pos` (e.g., the string is length `pos+1`), this call is valid, but if `pos` is at or beyond the last character index this throws `StringIndexOutOfBoundsException`. The exception is swallowed by the outer catch. No test covers boundary positions.

---

### A13-14 | Severity: HIGH | BarCodeAction — `DateUtil.stringToTimestamp` can return null; null passed to `checkDuplicateResult` and `saveResultBarcode` (lines 212–214)

```java
DateUtil.stringToTimestamp(resultBean.getTime())
```

`stringToTimestamp` returns `null` on a `ParseException` (format `"yyyy/MM/dd HH:mm:ss"` mismatch). `checkDuplicateResult` uses this null directly in a SQL string concatenation (`timestamp = '` + time + `'`), which would produce `timestamp = 'null'` — logically incorrect but syntactically accepted by PostgreSQL as a string, silently failing the duplicate check. `saveResultBarcode` sets it on the `ResultBean` which then inserts a null timestamp into the database. No test covers this path.

---

### A13-15 | Severity: MEDIUM | BarCodeAction — no test for the `else` / unknown-method path returning `"globalfailure"` (line 246–249)

```java
else {
    return mapping.findForward("globalfailure");
}
```

There is no test verifying that an unrecognised `method` parameter value produces the `globalfailure` forward rather than a 200-success response.

---

### A13-16 | Severity: MEDIUM | BarCodeAction — result still returned as `"success"` when `saveResult` returns 0 in API_BARCODE branch (lines 59–65)

```java
if(resutl_id > 0) {
    // send alert
}
// no else — falls through to return "success"
return mapping.findForward("success");
```

If `saveResult` returns 0 (indicating a database failure), the method still returns `"success"`. The client receives an HTTP 200 with no error indication. No test verifies the save-failure response for the `API_BARCODE` branch.

---

### A13-17 | Severity: MEDIUM | BarCodeAction — `sendFleetCheckAlert` return value set on request attribute but no test verifies attribute semantics (lines 63, 223)

```java
Boolean sendres = fleetcheckAction.sendFleetCheckAlert(...);
request.setAttribute("sendres", sendres);
```

The attribute is set but there is no test confirming that the JSP/view layer correctly reads it, nor that `sendres == false` (alert not configured) is distinguishable from `sendres == null` (exception). No test covers the alert-send failure path.

---

### A13-18 | Severity: MEDIUM | BarCodeAction — `isDriverIdSetted()` check prevents alert on anonymous scans but no test verifies this business rule (lines 218–225)

```java
if(resultBean.isDriverIdSetted()) {
    // send alert
}
```

When a checklist is scanned without a driver badge (`driver_id == null` or `0`), the alert is intentionally suppressed. No test verifies this business rule, meaning a code change could accidentally send alerts for anonymous scans or suppress alerts for identified drivers without detection.

---

### A13-19 | Severity: MEDIUM | BarCodeAction — `msg = "Duplicated Data! ..."` set but final response always `"success"` (lines 233–236, 253)

The `msg` attribute signals a data problem to the view, but the action forward is always `"success"`. No test verifies that a duplicate submission sets the correct `msg` attribute rather than proceeding as if the save succeeded.

---

### A13-20 | Severity: MEDIUM | CalibrationAction — `super.execute(...)` always returns `null`; ActionForward is never a named forward

```java
return super.execute(mapping, form, request, response);  // line 20
```

`Action.execute()` returns `null` by default (no-op base implementation). This means every HTTP request to this action receives a null forward, which Struts treats as "no forwarding" — the response is committed with whatever the container default is (typically a blank 200 or a Struts error). No test verifies whether this is intentional or whether a named forward (e.g., `"success"`) should be returned.

---

### A13-21 | Severity: MEDIUM | CalibrationAction — `CalibrationJob.calibrateAllUnits()` exceptions are caught and `printStackTrace()`-only; action has no awareness

```java
// Inside CalibrationJob.calibrateAllUnits():
} catch (SQLException e) {
    e.printStackTrace();
}
```

`CalibrationAction` calls `job.calibrateAllUnits()` which silently swallows `SQLException`. The action has no mechanism to detect failure or return an error response. No test verifies that a database failure during calibration produces an appropriate HTTP response or log entry.

---

### A13-22 | Severity: MEDIUM | BarCodeAction — `UnitDAO` is a class-level singleton field; no dependency injection, making unit testing impossible without reflection or PowerMock

```java
private UnitDAO unitDAO = UnitDAO.getInstance();  // line 30
```

The DAO is instantiated via a static singleton in the field initializer. There is no constructor or setter for injection. Any test of `BarCodeAction` would require real database connectivity or PowerMock/byte-code manipulation. This is a testability anti-pattern that has prevented all unit test coverage.

---

### A13-23 | Severity: MEDIUM | CalibrationAction — `CalibrationJob` is instantiated directly inside `execute`; no dependency injection

```java
CalibrationJob job = new CalibrationJob();  // line 18
job.calibrateAllUnits();
```

There is no way to inject a mock `CalibrationJob` without subclassing or reflection. This design choice is the primary reason no unit test can exercise `CalibrationAction` without a live database and Quartz scheduler context.

---

### A13-24 | Severity: LOW | BarCodeAction — commented-out debug `System.out.print` statements (lines 201–210)

```java
// System.out.print("start\n");
// System.out.print("driver id:"+resultBean.getDriver_id()+"\n");
```

Ten lines of commented-out debugging output remain in production code. No test enforces that production log output is structured (e.g., via Log4j) rather than `System.out`. These indicate historical manual debugging in lieu of test coverage.

---

### A13-25 | Severity: LOW | BarCodeAction — typo in user-facing message string (line 81)

```java
msg = "Corrupted Data! Invalid Fomrat!";
```

`"Fomrat"` is a misspelling of `"Format"`. No test asserts on message content, so this defect would pass undetected regardless of whether tests existed.

---

### A13-26 | Severity: LOW | BarCodeAction — `e.getMessage()` return value discarded (line 242)

```java
e.getMessage();   // return value discarded
e.printStackTrace();
```

`e.getMessage()` is called as a statement; its return value is not used. This is dead code. No test exercises this error path or verifies that exception details are logged through the project's `InfoLogger`.

---

### A13-27 | Severity: INFO | BarCodeAction — `CompanyDAO` is instantiated inside `execute` every call (line 40)

```java
CompanyDAO companyDao = CompanyDAO.getInstance();
```

While this uses the singleton pattern, the assignment is local to `execute` (unlike `unitDAO` which is a field). This is inconsistent with `unitDAO` but not a defect. No test verifies request-scoped vs. class-scoped DAO lifecycle behavior.

---

### A13-28 | Severity: INFO | CalibrationAction — no authentication/authorization guard

`CalibrationAction.execute` performs no session check, role check, or CSRF verification before triggering the calibration database writes. If the Struts action mapping does not enforce security at the container or filter level, any unauthenticated request can initiate calibration. This is an observation for the security audit pass; no test exercises the authorization boundary.

---

## 4. Summary Table

| Finding | Severity | Class | Description |
|---|---|---|---|
| A13-1 | CRITICAL | BarCodeAction | Zero test coverage — entire execute method untested |
| A13-2 | CRITICAL | CalibrationAction | Zero test coverage — entire execute method untested |
| A13-3 | CRITICAL | BarCodeAction | Unchecked `arrUnit.get(0)` — NPE/IOOBE on no serial match (line 50) |
| A13-4 | CRITICAL | BarCodeAction | Unchecked `companies.get(0)` — IOOBE on unknown compId (line 55) |
| A13-5 | CRITICAL | BarCodeAction | `Long.parseLong("")` after leading-zero strip — NFE on missing/blank driver (line 58) |
| A13-6 | CRITICAL | BarCodeAction | Null `quesIds`/`quesAns` arrays passed to `saveResult` without null check (lines 46–47, 58) |
| A13-7 | HIGH | BarCodeAction | Unchecked `arrUnit.get(0)` in Load_BARCODE loop — IOOBE on unknown unit_id (line 198) |
| A13-8 | HIGH | BarCodeAction | Broad silent exception swallow in Load_BARCODE catch; always returns "success" (lines 240–244) |
| A13-9 | HIGH | BarCodeAction | `Long.parseLong(driver)` on malformed scanner token silently swallowed (lines 116, 151, 187) |
| A13-10 | HIGH | BarCodeAction | Absent `<Memory>`/`<End>` tags: corrupted-data message set but processing continues (lines 70–84) |
| A13-11 | HIGH | BarCodeAction | Non-conforming scanner time format causes `StringTimeDifference` to return 0, silently merging results |
| A13-12 | HIGH | BarCodeAction | `indexOf('Y'/'N') == 0` silently skips answer; `pos > 0` guard excludes index 0 (line 134) |
| A13-13 | HIGH | BarCodeAction | `answered.substring(pos+1)` may throw SIOOBE on short tokens (line 138) |
| A13-14 | HIGH | BarCodeAction | Null timestamp from `stringToTimestamp` silently corrupts duplicate-check SQL and DB insert (line 212) |
| A13-15 | MEDIUM | BarCodeAction | Unknown-method path returning "globalfailure" not tested (lines 246–249) |
| A13-16 | MEDIUM | BarCodeAction | Save failure (result_id == 0) still returns "success" in API_BARCODE branch (lines 59–65) |
| A13-17 | MEDIUM | BarCodeAction | `sendres` request attribute semantics unverified; false vs. null not distinguished |
| A13-18 | MEDIUM | BarCodeAction | `isDriverIdSetted()` alert-suppression business rule has no test (lines 218–225) |
| A13-19 | MEDIUM | BarCodeAction | Duplicate-data `msg` attribute set but action always returns "success" (lines 233–236) |
| A13-20 | MEDIUM | CalibrationAction | `super.execute()` returns null forward — may be unintentional; no test verifies (line 20) |
| A13-21 | MEDIUM | CalibrationAction | `SQLException` in `calibrateAllUnits` silently swallowed; action cannot detect or report failure |
| A13-22 | MEDIUM | BarCodeAction | `UnitDAO` singleton field prevents unit testing without PowerMock or reflection (line 30) |
| A13-23 | MEDIUM | CalibrationAction | `CalibrationJob` instantiated directly inside `execute`; not injectable for testing (line 18) |
| A13-24 | LOW | BarCodeAction | Ten lines of commented-out `System.out.print` debug statements remain (lines 201–210) |
| A13-25 | LOW | BarCodeAction | Typo in user-facing error string: "Fomrat" should be "Format" (line 81) |
| A13-26 | LOW | BarCodeAction | `e.getMessage()` return value discarded — dead code in catch block (line 242) |
| A13-27 | INFO | BarCodeAction | Inconsistent DAO scoping: `unitDAO` is a field, `companyDao` is local (lines 30, 40) |
| A13-28 | INFO | CalibrationAction | No authentication/authorization guard before triggering calibration DB writes (line 18–19) |

**Total findings: 28**
- CRITICAL: 6
- HIGH: 8
- MEDIUM: 9
- LOW: 3
- INFO: 2
