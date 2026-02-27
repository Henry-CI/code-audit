# Pass 1 Security Audit — Agent APP58
**App:** forkliftiqapp (Android/Java)
**Date:** 2026-02-27
**Agent:** APP58

---

## Step 1 — Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

Checklist specifies "Branch: main". Actual branch is "master". Discrepancy recorded. Branch is "master" — audit proceeds.

---

## Step 2 — Reading Evidence

### File 1: ServiceRecordFragment.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.ui.fragment.ServiceRecordFragment`

**Superclass:** `FleetFragment` (extends Fragment)

**Fields and constants:**
- `private ServiceRecordListAdapter listAdapter` — instance field
- `private ArrayList<ServiceRecordItem> listData` — instance field, initialised to empty ArrayList
- `final static String TYPE_SET_HOURS = "setHrs"` — package-private constant, line 35
- `final static String TYPE_SET_INTERVAL = "setDur"` — package-private constant, line 36
- `private PieChart mChart` — instance field, line 37
- `private static final int STATUS_NORMAL = 0` — line 39
- `private static final int STATUS_DUE = 1` — line 40
- `private static final int STATUS_OVERDUE = 2` — line 41
- `private static final int STATUS_NOT_SET = 3` — line 42
- `private static final int SERVICE_DUE_HOURS = 25` — line 43
- `boolean fromProfile = true` — package-private (no access modifier), instance field, line 45
- `private ServiceRecordResultArray serviceRecordResultArray` — instance field, line 46

**Public/package-private methods with line numbers:**
- `static int getStatus(ServiceRecordItem recordItem)` — line 48 (package-private)
- `static int getColorForStatus(int status)` — line 76 (package-private)
- `static String getTextForStatus(Context context, int status)` — line 95 (package-private)
- `public View onCreateView(@NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState)` — line 137
- `public void initViews()` — line 142
- `public void onMiddleButton(View view)` — line 199

**Private methods (for completeness):**
- `private static String getLabelForStatus(int status)` — line 115
- `private void showServiceDetail(int position)` — line 170
- `private void loadData()` — line 176
- `private void onData(ServiceRecordResultArray result)` — line 205
- `private void initServiceChart()` — line 225
- `private ArrayList<Integer> getColorForPieEntry(ArrayList<PieEntry> pieEntries)` — line 231
- `private ArrayList<PieEntry> getServicePieData()` — line 247
- `private void setData()` — line 304

**Fragment type:** Fragment (UI fragment, not declared in manifest directly — attached by host Activity)

**Third-party imports observed:**
- `com.github.mikephil.charting` (MPAndroidChart) — PieChart, PieData, PieDataSet, PieEntry, PercentFormatter

---

### File 2: ServiceRecordListAdapter.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.ui.fragment.ServiceRecordListAdapter`

**Superclass:** `ArrayAdapter<ServiceRecordItem>`

**Fields:**
- `private Context context` — line 18
- `private ArrayList<ServiceRecordItem> mData` — line 19

**Constructor:**
- `ServiceRecordListAdapter(Context context, ArrayList<ServiceRecordItem> data)` — line 21 (package-private)

**Public/overridden methods with line numbers:**
- `public View getView(int position, View convertView, @NonNull ViewGroup parent)` — line 29
- `public int getCount()` — line 62
- `public ServiceRecordItem getItem(int i)` — line 67

**Inner class:**
- `static class ListHolder` — line 71 (package-private), fields: `TextView name`, `View status_bar`, `TextView status_text`

---

### File 3: ServiceStatsListAdapter.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.ui.fragment.ServiceStatsListAdapter`

**Superclass:** `ArrayAdapter<DriverStatsItem>`

**Fields:**
- `private Context context` — line 20
- `private ArrayList<DriverStatsItem> mData` — line 21

**Constructor:**
- `ServiceStatsListAdapter(Context context, ArrayList<DriverStatsItem> data)` — line 23 (package-private)

**Public/overridden methods with line numbers:**
- `public View getView(int position, View convertView, @NonNull ViewGroup parent)` — line 30
- `public int getCount()` — line 67
- `public DriverStatsItem getItem(int i)` — line 72

**Inner class:**
- `static class ListHolder` — line 76 (package-private), fields: `TextView name`, `View status_bar`, `TextView status_text`

**Notable logic in getView (lines 54–61):**
- Parses `recordItem.value` (a String from the server response) using `Integer.valueOf(s)` inside a bare `catch (Exception ignored)` block. On parse failure `v` remains 0 and the displayed text silently becomes "0 Services".

---

## Step 3 — Checklist Section Findings

### Section 1 — Signing and Keystores

No signing configuration, keystore references, gradle files, or pipeline files are present in the three assigned files. These topics are not addressable from this file set.

No issues found from these files — Section 1.

---

### Section 2 — Network Security

**Finding — WebApi call passes userId without visible input sanitisation (Informational)**

`ServiceRecordFragment.java`, line 183:
```java
WebApi.async().getServiceRecord(WebData.instance().getUserId(), new WebListener<ServiceRecordResultArray>() { ... });
```
The user ID is retrieved from `WebData.instance().getUserId()` and passed directly to the web API call. The assigned files do not expose the implementation of `WebApi` or `WebData`, so the transport security (HTTPS enforcement, certificate validation) cannot be assessed here. The data flow originates from server-sourced data and no URL construction or HTTP client configuration is visible in these files.

No TrustAllCertificates patterns, hostnameVerifier overrides, or hardcoded URLs are present in the three assigned files.

No issues found within scope — Section 2.

---

### Section 3 — Data Storage

No SharedPreferences access, file I/O, SQLite access, external storage access, or credential caching is present in any of the three files. Data flows from the web API response into in-memory `ArrayList` structures used exclusively for UI display.

No issues found — Section 3.

---

### Section 4 — Input and Intent Handling

**Finding — Uncontrolled array index access from list item click (Low)**

`ServiceRecordFragment.java`, lines 158–166 and 170–174:
```java
service_record_list.setOnItemClickListener(new AdapterView.OnItemClickListener() {
    @Override
    public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
        showServiceDetail(position);
    }
});
```
```java
private void showServiceDetail(int position) {
    ServiceEditFragment serviceEditFragment = ServiceEditFragment.createInstance(listData, position);
    ...
}
```
The `position` value from `onItemClick` is passed directly to `ServiceEditFragment.createInstance(listData, position)`. No bounds check is performed before passing `position` alongside the `listData` reference. If `listData` is mutated concurrently (e.g. by an in-flight `loadData()` callback updating the list while the user taps), the position could be stale and index out-of-bounds behaviour in `ServiceEditFragment` could result. The security impact is low (no privilege escalation), but the pattern is fragile. This is a data integrity concern rather than a direct security vulnerability in isolation.

No implicit intents carrying sensitive data, WebView usage, or deep link handlers are present in any of the three files.

No issues found beyond the above — Section 4.

---

### Section 5 — Authentication and Session

No authentication logic, token handling, credential storage, or session lifecycle management is present in any of the three files. The call to `WebData.instance().getUserId()` at line 183 of `ServiceRecordFragment.java` consumes an already-resolved user ID; the mechanism by which that ID is obtained and stored is outside this file set.

No issues found within scope — Section 5.

---

### Section 6 — Third-Party Libraries

**Finding — Deprecated Android support library in use (Medium)**

All three files import from `android.support.annotation` (the legacy Android Support Library):
- `ServiceRecordFragment.java` lines 5–6: `import android.support.annotation.NonNull;` and `import android.support.annotation.Nullable;`
- `ServiceRecordListAdapter.java` line 6: `import android.support.annotation.NonNull;`
- `ServiceStatsListAdapter.java` line 6: `import android.support.annotation.NonNull;`

The Android Support Library was superseded by AndroidX in 2018 and is no longer receiving security patches. Use of the support library indicates the project has not been migrated to AndroidX. While the annotation classes themselves carry no runtime security risk, this is a strong signal that the broader dependency tree may include outdated, unpatched support library components (`com.android.support:appcompat-v7`, `com.android.support:recyclerview-v7`, etc.) that should be assessed at the `build.gradle` level.

**Finding — Integer.valueOf with swallowed exception (Informational / Robustness)**

`ServiceStatsListAdapter.java`, lines 56–59:
```java
try {
    v = Integer.valueOf(s);
} catch (Exception ignored) {
}
```
Server-supplied string `recordItem.value` is parsed without any validation. On malformed or unexpected server input, the exception is silently swallowed and the UI displays "0 Services". While the security impact is low (display only), this pattern of suppressing exceptions broadly (`catch (Exception)`) rather than handling `NumberFormatException` specifically can mask unexpected failures. No injection risk exists here because the value is only used to construct a display string, not in a SQL, shell, or URL context.

**Finding — MPAndroidChart library present (Informational)**

`ServiceRecordFragment.java` imports `com.github.mikephil.charting` (MPAndroidChart). Version cannot be determined from these files alone; the `build.gradle` should be checked to confirm the version is current and has no known CVEs.

No issues found beyond the above within scope — Section 6.

---

### Section 7 — Google Play and Android Platform

**Finding — Deprecated API: `getResources().getColor(int)` without theme (Low)**

`ServiceRecordFragment.java`, lines 235–241:
```java
colorList.add(getResources().getColor(R.color.service_status_normal));
colorList.add(getResources().getColor(R.color.service_status_due));
colorList.add(getResources().getColor(R.color.service_status_overdue));
colorList.add(getResources().getColor(R.color.service_status_not_set));
```
And at line 322:
```java
data.setValueTextColor(getResources().getColor(R.color.text_black));
```
`Resources.getColor(int)` was deprecated in API 23 (Android 6.0). The two-argument form `getColor(int id, Resources.Theme theme)` should be used instead. Similarly in `ServiceRecordListAdapter.java`, line 55:
```java
holder.status_bar.setBackgroundColor(getContext().getResources().getColor(color));
```
This is a deprecated API call. These calls function correctly on current Android versions but generate lint warnings and should be remediated.

**Finding — Deprecated API: `Integer.valueOf()` instead of `Integer.parseInt()` (Informational)**

`ServiceStatsListAdapter.java`, line 57:
```java
v = Integer.valueOf(s);
```
`Integer.valueOf(String)` returns a boxed `Integer` which is then auto-unboxed to primitive `int`. `Integer.parseInt(String)` is the correct and more efficient method for this use case. This is a minor code quality concern, not a security issue.

**Finding — No AsyncTask usage observed (Positive)**

None of the three files uses the deprecated `AsyncTask` API. Network calls are dispatched through `WebApi.async()` which likely uses a non-deprecated concurrency mechanism.

No issues found beyond the above within scope — Section 7.

---

## Summary of Findings

| # | Severity | File | Description |
|---|----------|------|-------------|
| 1 | Medium | All three files | `android.support.*` imports — Support Library not migrated to AndroidX; entire support dependency tree is unpatched |
| 2 | Low | ServiceRecordFragment.java (L235–241, L322) | `getResources().getColor(int)` — deprecated since API 23; should use two-argument form with theme |
| 3 | Low | ServiceRecordListAdapter.java (L55) | `getResources().getColor(int)` — same deprecated API |
| 4 | Low | ServiceRecordFragment.java (L158–174) | No bounds check on list click position before passing to ServiceEditFragment; potential for index mismatch under concurrent list mutation |
| 5 | Informational | ServiceStatsListAdapter.java (L56–59) | `catch (Exception ignored)` swallows parse failures on server-supplied value; silent failure produces misleading "0 Services" display |
| 6 | Informational | ServiceStatsListAdapter.java (L57) | `Integer.valueOf(String)` with auto-unbox; use `Integer.parseInt(String)` instead |
| 7 | Informational | ServiceRecordFragment.java (L13–17) | MPAndroidChart version not determinable from this file; verify in build.gradle |

**Sections with no issues from assigned files:** Section 1 (Signing/Keystores), Section 2 (Network Security — within file scope), Section 3 (Data Storage), Section 5 (Authentication/Session).

---

*End of report — Agent APP58*
