# Pass 1 Security Audit — APP50
**App:** forkliftiqapp
**Stack:** Android/Java
**Date:** 2026-02-27
**Agent:** APP50
**Branch verified:** master (checklist states "main" — discrepancy recorded; actual branch is master, audit proceeds)

---

## Assigned File

`app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/adapter/SelectForkAdapter.java`

---

## Step 4 — Reading Evidence

### Fully Qualified Class Name

`au.com.collectiveintelligence.fleetiq360.ui.adapter.SelectForkAdapter`

### Inheritance

`SelectForkAdapter` extends `AbsRecyclerAdapter<String>`
(`au.com.collectiveintelligence.fleetiq360.ui.adapter.AbsRecyclerAdapter`)

### Fields

| Name | Type | Visibility | Line |
|---|---|---|---|
| `presenter` | `EquipmentSelectForkPresenter` | private | 11 |

### Public Methods

| Signature | Line |
|---|---|
| `void setPresenter(EquipmentSelectForkPresenter presenter)` | 13 |
| `SelectForkAdapter(Context context, int resId)` (constructor) | 17 |
| `void bindDatas(MyViewHolder holder, String data, final int position)` (override) | 22 |

### Android Components Declared

None — this is an adapter class, not an Activity, Fragment, Service, BroadcastReceiver, or ContentProvider.

### Supporting Types Read (for full evidence)

Two additional files were read to support findings:

**`AbsRecyclerAdapter<T>`** (`...ui/adapter/AbsRecyclerAdapter.java`)
Parent RecyclerView adapter. Public methods: `setDatas(List<T>)` (L31), `getDatas()` (L36), `getItemCount()` (L41), `onCreateViewHolder(...)` (L47), `onBindViewHolder(...)` (L54), `bindDatas(...)` abstract (L58), `setOnItemClickListener(...)` (L100). Inner class `MyViewHolder` with `getView(int)` (L72). Interface `OnItemClickListener` (L96–98).

**`EquipmentSelectForkPresenter`** (`...presenter/EquipmentSelectForkPresenter.java`)
Referenced by the assigned file. Public fields and methods: `public EquipmentListFragment ui` (L22), constructor `EquipmentSelectForkPresenter(EquipmentListFragment)` (L25), `void getEquipmentList()` (L30), `void showImage(String url, ImageView imageView)` (L57). Interface `ShowResultCallBack` (L75).
At line 71 of this presenter, `showImage()` calls `UserPhotoFragment.SSLCertificateHandler.nuke()` unconditionally before every image load.

**`UserPhotoFragment.SSLCertificateHandler`** (`...ui/fragment/UserPhotoFragment.java`)
`public static void nuke()` (L41): installs a permissive `X509TrustManager` (both `checkClientTrusted` and `checkServerTrusted` are empty — no validation performed), sets it as the JVM-wide `HttpsURLConnection` default SSL socket factory, and installs a `HostnameVerifier` that always returns `true`. Annotated `@SuppressLint("TrustAllX509TrustManager")` and `@SuppressLint("BadHostnameVerifier")` — the developer was aware of the lint warnings and suppressed them.

---

## Step 5 — Checklist Review

### Section 1 — Signing and Keystores

No findings from this file. `SelectForkAdapter.java` contains no references to keystores, signing configuration, passwords, or build credentials.

No issues found — Section 1.

---

### Section 2 — Network Security

**CRITICAL — Full SSL/TLS certificate validation disabled globally at runtime**

Severity: Critical
Location (direct trigger): `EquipmentSelectForkPresenter.showImage()` — line 71
Location (implementation): `UserPhotoFragment.SSLCertificateHandler.nuke()` — lines 41–69

The call chain is:
1. `SelectForkAdapter.bindDatas()` (line 26–28, assigned file) calls `presenter.showImage(url, iv)` for every list item that has a URL.
2. `EquipmentSelectForkPresenter.showImage()` (line 71) calls `UserPhotoFragment.SSLCertificateHandler.nuke()` unconditionally before displaying each image.
3. `nuke()` installs a `TrustManager` whose `checkServerTrusted()` and `checkClientTrusted()` methods have empty bodies — they perform no certificate chain validation whatsoever. It then installs a `HostnameVerifier` that always returns `true` regardless of the hostname presented.
4. Both overrides are set as the **JVM-wide process defaults** via `HttpsURLConnection.setDefaultSSLSocketFactory()` and `HttpsURLConnection.setDefaultHostnameVerifier()`. This means every HTTPS connection made by the application process after the first list item is rendered — including connections to the forkliftiqws backend carrying operator credentials and telemetry — is made without any certificate or hostname verification.

**Impact:** Any network-level attacker capable of intercepting the device's traffic (e.g., on the same Wi-Fi network as a forklift terminal, or via a rogue access point) can present a self-signed or forged certificate and conduct a full man-in-the-middle attack. All data transmitted — operator credentials, session tokens, forklift assignment data, and telemetry — is exposed in plaintext to the attacker. This is a permanent process-wide side effect triggered by routine UI rendering.

**Supporting observation — suppressed lint warnings:** The `@SuppressLint("TrustAllX509TrustManager")` and `@SuppressLint("BadHostnameVerifier")` annotations confirm the developer was explicitly warned by Android tooling that these patterns are dangerous and chose to suppress those warnings rather than fix the underlying issue.

**Supporting observation — scope of exposure via the assigned file:** The assigned adapter renders a list of forklifts. Each item rendered calls `bindDatas()`, which calls `presenter.showImage()`, which calls `nuke()`. The disabling of SSL validation therefore occurs as a direct and predictable consequence of displaying the equipment selection screen — a core user journey in the app.

No issues found — Section 2 (other items): no hardcoded API URLs, no `TrustAllCertificates` pattern introduced within the assigned file itself; the critical finding originates in the presenter called by the assigned file.

---

### Section 3 — Data Storage

No findings from this file. No SharedPreferences, file I/O, SQLite operations, or external storage access in `SelectForkAdapter.java`.

No issues found — Section 3.

---

### Section 4 — Input and Intent Handling

No findings from this file. No exported components, no WebView, no intent construction, no deep link handling in `SelectForkAdapter.java`.

No issues found — Section 4.

---

### Section 5 — Authentication and Session

No direct authentication or session token handling in `SelectForkAdapter.java`. The critical SSL finding in Section 2 has direct authentication consequences (credentials transmitted over unprotected connections), but no additional session-specific issues are present in the assigned file itself.

No issues found — Section 5 (in isolation from Section 2 cross-impact).

---

### Section 6 — Third-Party Libraries

**Medium — Abandoned third-party library: Universal Image Loader**

The presenter called by the assigned file uses `com.nostra13.universalimageloader` (Universal Image Loader by Sergey Tarasevich). This library has had no releases since 2016 and is officially abandoned. The project's own GitHub repository explicitly states it is no longer maintained and recommends migrating to Glide or Picasso. Using an unmaintained image loading library in a production application means any vulnerabilities discovered in that library will not receive patches.

The assigned file indirectly depends on this library via `EquipmentSelectForkPresenter.showImage()`, which calls `ImageLoader.getInstance().displayImage()`.

No issues found — Section 6 (other items: no additional library findings within the scope of the assigned file).

---

### Section 7 — Google Play and Android Platform

**Low — Deprecated support library imports in base adapter**

`AbsRecyclerAdapter.java` (parent of `SelectForkAdapter`) imports from `android.support.v7.widget.RecyclerView` (lines 6–7) rather than `androidx.recyclerview.widget.RecyclerView`. The AndroidX migration was the recommended path from Android 9 onwards. If the project has migrated other files to AndroidX, mixing support library and AndroidX imports can cause build and runtime conflicts. This is a code quality / maintenance flag rather than a security finding, but is noted per checklist completeness.

No further issues found — Section 7.

---

## Summary of Findings

| # | Severity | Section | Finding |
|---|---|---|---|
| 1 | Critical | 2 — Network Security | `SSLCertificateHandler.nuke()` called unconditionally by `EquipmentSelectForkPresenter.showImage()`, which is invoked by `SelectForkAdapter.bindDatas()` on every list item render. Installs a process-wide trust-all `TrustManager` and always-true `HostnameVerifier`, disabling all TLS certificate and hostname validation for the entire application. Directly triggered by the equipment selection screen. |
| 2 | Medium | 6 — Third-Party Libraries | Universal Image Loader (`com.nostra13.universalimageloader`) is abandoned since 2016 with no further security patches. |
| 3 | Low | 7 — Google Play / Platform | `AbsRecyclerAdapter` uses legacy `android.support.v7` imports rather than AndroidX equivalents. |

---

## Branch Discrepancy

The checklist header states `Branch: main`. The actual current branch is `master`. Audit was performed on `master` as instructed.
