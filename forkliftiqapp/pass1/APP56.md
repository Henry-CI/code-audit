# Pass 1 Security Audit — APP56
**Agent ID:** APP56
**Date:** 2026-02-27
**Repo:** forkliftiqapp
**Stack:** Android/Java

---

## Step 1 — Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

**Discrepancy:** The checklist header states `Branch: main`. The actual branch is `master`. Branch confirmed as `master`; audit proceeds.

---

## Step 2 — Assigned Files

1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/JobsFragment.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/LoginFragment.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/ProfileFragment.java`

Supporting files read to trace credential flow:
- `user/CurrentUser.java`
- `user/UserDb.java`
- `user/User.java`
- `user/UserRealmObject.java`
- `model/ModelPrefs.java`
- `WebService/WebData.java`
- `util/CommonFunc.java`

---

## Step 3 — Reading Evidence

### File 1: JobsFragment.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.ui.fragment.JobsFragment`

**Extends / Implements:**
`FleetFragment`, `AbsRecyclerAdapter.OnItemClickListener`, `View.OnClickListener`

**Fields:**
- `JobsActivity activity` (package-private, line 44)
- `public TextView timerText` (line 45)
- `public TextView textViewSecondText` (line 45)
- `private ImageView finishBtn` (line 46)
- `public JobsPresenter presenter` (line 47)
- `private CompanyDateFormatter companyDateFormatter` (line 48)
- `private ServerDateFormatter serverDateFormatter` (line 49)

**Public methods (signature : line):**
- `public View onCreateView(LayoutInflater, ViewGroup, Bundle) : 53`
- `public void onActivityCreated(Bundle) : 59`
- `public void logout() : 78`
- `public void initViews() : 113`
- `public void onSessionSaved() : 150`
- `public void onItemClick(View, int) : 155`
- `public void onClick(View) : 159`
- `public void onSessionEnded() : 172`

---

### File 2: LoginFragment.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.ui.fragment.LoginFragment`

**Extends / Implements:**
`FleetFragment`, `View.OnClickListener`

**Fields:**
- `private EditText nameText` (line 29)
- `private EditText passwordText` (line 29)

**Public methods (signature : line):**
- `public View onCreateView(LayoutInflater, ViewGroup, Bundle) : 33`
- `public void initViews() : 38`
- `public void onStop() : 79`
- `public void onDestroy() : 84`
- `public void onClick(View) : 89`

**Private methods:**
- `private void login() : 67`

---

### File 3: ProfileFragment.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.ui.fragment.ProfileFragment`

**Extends / Implements:**
`FleetFragment`, `View.OnClickListener`

**Fields:**
- `ProfileActivity activity` (package-private, line 28)
- `private EditText lastEText` (line 29)
- `private EditText firstEText` (line 29)
- `private LinearLayout editButton` (line 30)
- `private LinearLayout saveButton` (line 31)

**Public methods (signature : line):**
- `public View onCreateView(LayoutInflater, ViewGroup, Bundle) : 34`
- `public void onActivityCreated(Bundle) : 40`
- `public void initViews() : 59`
- `public void onLeftButton(View) : 79`
- `public void onRightButton(View) : 84`
- `public void onResume() : 89`
- `public void onStop() : 94`
- `public void onDestroy() : 99`
- `public void onClick(View) : 155`

**Private methods:**
- `private void setUserData() : 46`
- `private void saveModifiedResult() : 103`
- `private void updateUser(int, UpdateUserParameter) : 122`
- `private void onEnableEdit(boolean) : 147`

---

## Step 4 — Credential and Authentication Flow Analysis

### LoginFragment credential collection (LoginFragment.java lines 67–76)

```java
private void login() {
    if (passwordText.getText().length() < 4 ) {
        showToast("Please enter required number of digits. Min: 4 and Max: 8");
        return;
    }
    WebData.instance().logout();
    CurrentUser.setTemporaryLoginInformation(nameText.getText().toString(),
            passwordText.getText().toString());
    getBaseActivity().showFragmentWithStack(..., new SignupLoadingFragment());
}
```

`setTemporaryLoginInformation` in `CurrentUser.java` (lines 120–123):
```java
public static void setTemporaryLoginInformation(String email, String password) {
    loginEmail = email;
    loginPassword = CommonFunc.MD5_Hash(password);
}
```

Both `loginEmail` and `loginPassword` are `private static String` fields on `CurrentUser` (lines 22–23). They persist for the lifetime of the class in memory.

### Transmission (CurrentUser.java lines 80–84)

```java
LoginParameter loginParameter = new LoginParameter();
loginParameter.email = CommonFunc.MD5_Hash(loginEmail);
loginParameter.password = loginPassword;
```

The email is MD5-hashed before transmission. The password is already the MD5 hash of the raw input (hashed in `setTemporaryLoginInformation`). Both are transmitted as MD5 digests, not raw plaintext — however MD5 is a broken cryptographic primitive (see Section 5 findings).

### Post-login password persistence (CurrentUser.java lines 88–91)

```java
setUser(result.arrayList.get(0));
get().setPassword(loginPassword);
```

`setPassword()` calls `UserDb.save(this)`. `UserDb.save()` writes to Realm (`UserRealmObject`). `UserRealmObject` stores the `password` field as a plain string (line 15 of UserRealmObject.java). The Realm database is not encrypted.

### Offline fallback authentication (CurrentUser.java lines 103–106)

```java
User localUser = UserDb.get(loginEmail, loginPassword);
```

`UserDb.get(email, password)` queries Realm with both fields (UserDb.java lines 55–63). This confirms password hashes are persisted to the Realm database and used for offline authentication.

### Token storage (WebData.java lines 91–93)

```java
void setGetTokenResult(GetTokenResult result) {
    getTokenResult = result;
    ModelPrefs.saveObject(TOKEN_ITEM_KEY, result);
}
```

The bearer token is serialised via Gson and saved to plain `SharedPreferences` via `ModelPrefs.saveObject()`. `ModelPrefs` uses `Context.MODE_PRIVATE` SharedPreferences without encryption (ModelPrefs.java lines 16–18).

### Logout handling — WebData / CurrentUser (WebData.java line 108–110; CurrentUser.java lines 125–128)

```java
// WebData.logout():
public void logout() {
    CurrentUser.logout();
}

// CurrentUser.logout():
public static void logout() {
    ModelPrefs.deleteDataForKey(CURRENT_USER_ID_KEY);
    user = null;
}
```

`logout()` removes `current_user_id` from SharedPreferences and nulls the in-memory `user` reference. It does **not** clear `loginEmail` or `loginPassword` static fields, does not delete the token from SharedPreferences (`token_result` key), and does not clear the Realm database of stored user records (including password hashes).

### Hardcoded service credentials (WebData.java lines 56–82)

```java
String clientId = "987654321";
String clientSecret = "8752361E593A573E86CA558FFD39E";
String userName = "gas";
String password = "ciiadmin";
```

Four service-layer credentials are hardcoded in `getTokenFormData()`.

---

## Step 5 — Checklist Section Findings

### Section 1 — Signing and Keystores

Not directly assessable from the three assigned fragment files. No signing-related code observed in the assigned files.

No issues found — Section 1 (within scope of assigned files).

---

### Section 2 — Network Security

**FINDING SEC-2-A — Hardcoded service credentials in source (Critical)**

File: `WebService/WebData.java`, method `getTokenFormData()`, lines 62–77.

Four credentials are hardcoded as string literals in the compiled application binary:
- `client_id`: `"987654321"`
- `client_secret`: `"8752361E593A573E86CA558FFD39E"`
- `username`: `"gas"`
- `password`: `"ciiadmin"`

These values are embedded in every build variant (debug and release) and are readable from the APK by decompiling with tools such as jadx or apktool. The `client_secret` and `password` values in particular constitute compromised service credentials.

This is a critical-severity finding. The credentials should be removed from source, loaded from a secure secret store at runtime, or injected as build-time variables from a secrets manager rather than committed to version control.

---

### Section 3 — Data Storage

**FINDING SEC-3-A — Password hash persisted in unencrypted Realm database (High)**

Credential flow traced through `LoginFragment` -> `CurrentUser.setTemporaryLoginInformation()` -> `CurrentUser.login()` -> `User.setPassword()` -> `UserDb.save()` -> `UserRealmObject`.

After a successful login, `get().setPassword(loginPassword)` is called at `CurrentUser.java` line 90, where `loginPassword` is an MD5 hash of the user's raw password. `UserDb.save()` then persists this hash to a Realm `UserRealmObject` record (UserRealmObject.java, `password` field, line 15). The Realm database is not configured with encryption. Any process with access to the app's data directory (rooted device, ADB backup if `allowBackup` is true) can extract the MD5 password hash.

Additionally, `UserRealmObject` stores `licenseNumber`, `securityNumber`, `address`, `phoneNumber`, and `email` — all operator PII — in the same unencrypted Realm database.

**FINDING SEC-3-B — Bearer token stored in plain SharedPreferences (High)**

`WebData.setGetTokenResult()` serialises the `GetTokenResult` object to JSON via Gson and writes it to plain `SharedPreferences` via `ModelPrefs.saveObject("token_result", result)`. `ModelPrefs` wraps `getSharedPreferences("prefs", Context.MODE_PRIVATE)` without any encryption layer. The token is readable from the SharedPreferences XML file on rooted devices or via ADB backup.

The fix is `EncryptedSharedPreferences` from the Jetpack Security library.

**FINDING SEC-3-C — Credentials remain in static fields after logout (Medium)**

`CurrentUser` holds `private static String loginEmail` and `private static String loginPassword` (lines 22–23). `CurrentUser.logout()` (lines 125–128) sets `user = null` and removes `current_user_id` from SharedPreferences but does **not** clear `loginEmail` or `loginPassword`. These fields retain their values (the MD5 of the raw email and of the raw password) in process memory until the application process is killed. In a multi-operator shift-change scenario this allows a subsequent operator's login flow to momentarily observe the previous operator's credentials if the logout is not followed immediately by a process restart.

**FINDING SEC-3-D — Token not cleared from SharedPreferences on logout (High)**

`CurrentUser.logout()` removes only `current_user_id` from SharedPreferences. The bearer token stored under `"token_result"` is not removed. After logout, the token persists in the SharedPreferences XML file on disk. If the device is subsequently accessed by another person (lost device, stolen device, shared device shift change), the token can be read and replayed against the backend API until it naturally expires.

---

### Section 4 — Input and Intent Handling

**FINDING SEC-4-A — No input validation on username field in LoginFragment (Low)**

`LoginFragment.login()` (line 68) validates only that `passwordText.getText().length() >= 4`. The username/email field `nameText` is not validated for format, length, or content before being passed to `CurrentUser.setTemporaryLoginInformation()` and ultimately transmitted as an MD5-hashed value to the server. While the server should also validate, absent any client-side check, a zero-length or malformed email string will be MD5-hashed and submitted, which could produce confusing server-side errors or log noise.

No WebView usage observed in assigned files. No deep-link handlers observed in assigned files.

No other issues found — Section 4.

---

### Section 5 — Authentication and Session

**FINDING SEC-5-A — MD5 used for credential hashing (High)**

`CommonFunc.MD5_Hash()` (CommonFunc.java lines 68–83) is the sole hashing function applied to operator credentials.

- The email is MD5-hashed in `CurrentUser.login()` (line 82) before transmission.
- The password is MD5-hashed in `CurrentUser.setTemporaryLoginInformation()` (line 122) before transmission and before storage.

MD5 is a cryptographically broken hash function since at least 2004. It is not a suitable password hashing algorithm: it is computationally fast (enabling brute force), has no salt, and pre-computed rainbow tables for common 4–8 digit PINs (the enforced password length) are publicly available. An attacker who obtains the Realm database or intercepts a network request can recover the original PIN trivially.

Password hashing for stored values should use bcrypt, scrypt, or Argon2. For transmission, the server should accept the raw password over TLS rather than receiving a pre-hashed value, as the MD5 hash effectively becomes the credential.

**FINDING SEC-5-B — Logout does not invalidate stored user records in Realm (Medium)**

`WebData.logout()` -> `CurrentUser.logout()` removes the `current_user_id` preference and nulls the in-memory user reference. It does not delete `UserRealmObject` records from the Realm database. All previously authenticated users' PII, password hashes, license numbers, and security numbers remain on device indefinitely. In a shift-change scenario where multiple operators use the same device, each operator's data accumulates in the Realm database across sessions.

**FINDING SEC-5-C — Offline authentication bypasses server-side session controls (Medium)**

`CurrentUser.login()` (lines 103–106) contains an offline fallback:
```java
User localUser = UserDb.get(loginEmail, loginPassword);
if (localUser != null) {
    setUser(localUser);
    handler.HandleSuccess();
}
```
When the network is unavailable or returns an HTTP 502, authentication succeeds if a matching `(email, password)` pair is found in the local unencrypted Realm database. A revoked, suspended, or terminated operator account can continue to authenticate locally indefinitely as long as the Realm database retains their record, bypassing any server-side access controls.

**FINDING SEC-5-D — Token expiry not handled in assigned fragments (Informational)**

No token refresh or re-authentication logic is visible in the three assigned fragment files. Token expiry handling is deferred to other components not assigned in this pass and should be confirmed by the agent covering the WebApi/network layer.

---

### Section 6 — Third-Party Libraries

The assigned fragments import the following third-party dependencies relevant to security scope:

- `io.realm.Realm` / `io.realm.RealmObject` / `io.realm.annotations.PrimaryKey` — Realm database (used in UserDb, UserRealmObject). No encryption configured. Version not determinable from fragment files; should be checked in build.gradle.
- `com.yy.libcommon.*` — internal/vendored library (`ThemedSingleListDialog`, `AMTextView`, `NetworkDetect`, `GsonHelper`, `Font`). Origin and update status not determinable from fragments.

No issues found in the assigned files beyond what is noted under Sections 3 and 5 — Section 6.

---

### Section 7 — Google Play and Android Platform

**FINDING SEC-7-A — Deprecated `onActivityCreated()` usage (Low)**

`JobsFragment.onActivityCreated()` (line 59) and `ProfileFragment.onActivityCreated()` (line 40) override the deprecated `Fragment.onActivityCreated(Bundle)` lifecycle callback. This method was deprecated in API level 28 (Android 9.0 / Pie). The recommended replacement is `onViewCreated()` combined with `getParentFragmentManager()` observers or `Activity.onCreate()` with `ViewModelProvider`.

**FINDING SEC-7-B — Support library annotations used instead of AndroidX (Low)**

All three fragments import `android.support.annotation.NonNull` and `android.support.annotation.Nullable` (the legacy support library namespace) rather than `androidx.annotation.*`. The Android Support Library reached end-of-life in 2018; Jetpack/AndroidX is the current supported replacement. This affects the ability to adopt `EncryptedSharedPreferences` (requires AndroidX Security) and other Jetpack components.

No `AsyncTask` usage observed. No `startActivityForResult` usage observed. No runtime permission requests observed in the assigned files.

---

## Summary of Findings

| ID | Section | Severity | Title |
|----|---------|----------|-------|
| SEC-2-A | Network Security | Critical | Hardcoded service credentials (`client_secret`, `password`, `client_id`, `username`) in `WebData.getTokenFormData()` |
| SEC-3-A | Data Storage | High | Operator password hash persisted in unencrypted Realm database |
| SEC-3-B | Data Storage | High | Bearer token stored in plain (unencrypted) SharedPreferences |
| SEC-3-C | Data Storage | Medium | Static `loginEmail` / `loginPassword` fields not cleared on logout |
| SEC-3-D | Data Storage | High | Bearer token not removed from SharedPreferences on logout |
| SEC-4-A | Input Handling | Low | No format validation on username field before submission |
| SEC-5-A | Authentication | High | MD5 used for credential hashing — broken algorithm, no salt |
| SEC-5-B | Authentication | Medium | Logout does not delete user records from Realm database |
| SEC-5-C | Authentication | Medium | Offline auth fallback bypasses server-side account revocation |
| SEC-5-D | Authentication | Informational | Token expiry handling not visible in assigned files |
| SEC-7-A | Android Platform | Low | Deprecated `onActivityCreated()` used in two fragments |
| SEC-7-B | Android Platform | Low | Legacy support library annotations used instead of AndroidX |
