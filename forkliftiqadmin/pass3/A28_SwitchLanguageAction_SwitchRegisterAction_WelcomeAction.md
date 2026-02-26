# Pass 3 – Documentation Audit
**Agent:** A28
**Audit run:** 2026-02-26-01
**Files audited:**
- `src/main/java/com/action/SwitchLanguageAction.java`
- `src/main/java/com/action/SwitchRegisterAction.java`
- `src/main/java/com/action/WelcomeAction.java`

---

## 1. Reading Evidence

### 1.1 SwitchLanguageAction.java

**Class:** `SwitchLanguageAction` (line 18)
Extends: `org.apache.struts.action.Action`

**Fields:**

| Name | Type | Line |
|------|------|------|
| `log` | `static Logger` | 20 |

**Methods:**

| Method | Visibility | Return Type | Line |
|--------|-----------|-------------|------|
| `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` | `public` | `ActionForward` | 22 |
| `getCookie(HttpServletRequest, String)` | `public static` | `Cookie` | 71 |
| `getLocale(String)` | `public static` | `Locale` | 83 |

---

### 1.2 SwitchRegisterAction.java

**Class:** `SwitchRegisterAction` (line 17)
Extends: `org.apache.struts.action.Action`

**Fields:**

| Name | Type | Line |
|------|------|------|
| `log` | `static Logger` | 18 |

**Methods:**

| Method | Visibility | Return Type | Line |
|--------|-----------|-------------|------|
| `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` | `public` | `ActionForward` | 20 |

---

### 1.3 WelcomeAction.java

**Class:** `WelcomeAction` (line 33)
Extends: `org.apache.struts.action.Action`

**Fields:**

| Name | Type | Line |
|------|------|------|
| `log` | `static Logger` | 35 |

**Methods:**

| Method | Visibility | Return Type | Line |
|--------|-----------|-------------|------|
| `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` | `public` | `ActionForward` | 37 |

---

## 2. Javadoc Analysis

### 2.1 SwitchLanguageAction.java

**Class-level Javadoc:** ABSENT

**Method-level Javadoc:**

- `execute` (line 22): ABSENT
- `getCookie` (line 71): ABSENT
- `getLocale` (line 83): ABSENT

---

### 2.2 SwitchRegisterAction.java

**Class-level Javadoc:** ABSENT

**Method-level Javadoc:**

- `execute` (line 20): ABSENT

---

### 2.3 WelcomeAction.java

**Class-level Javadoc:** ABSENT

**Method-level Javadoc:**

- `execute` (line 37): ABSENT

---

## 3. Findings

### A28-1 [LOW] Missing class-level Javadoc — SwitchLanguageAction

**File:** `src/main/java/com/action/SwitchLanguageAction.java`, line 18
**Detail:** The class `SwitchLanguageAction` has no class-level Javadoc comment. There is no `/** ... */` block above the class declaration describing its purpose, responsibilities, or usage.

---

### A28-2 [MEDIUM] Undocumented non-trivial public method — SwitchLanguageAction.execute

**File:** `src/main/java/com/action/SwitchLanguageAction.java`, line 22
**Detail:** The `execute` method is a non-trivial public method with no Javadoc. It performs the following logic: reads a `language` request parameter, resolves a `Locale` from it, stores the locale in the session under `Globals.LOCALE_KEY` (using the request's own locale if `language` equals `"0"`, or the resolved locale otherwise), manages a `ckLanguage` cookie (clearing it when `language` is `"0"`, updating or creating it otherwise), stores the language parameter as a request attribute, and forwards to `"success"`. None of this behaviour is documented. No `@param`, `@return`, or `@throws` tags are present.

---

### A28-3 [MEDIUM] Undocumented non-trivial public static method — SwitchLanguageAction.getCookie

**File:** `src/main/java/com/action/SwitchLanguageAction.java`, line 71
**Detail:** The `getCookie` static utility method is public and non-trivial: it iterates over all cookies in the request and returns the first one whose name matches the given `name` parameter, returning `null` if no match is found or if the cookie array is `null`. No Javadoc is present. Missing `@param` tags for `request` and `name`, and a `@return` tag describing the nullable return value.

---

### A28-4 [MEDIUM] Undocumented non-trivial public static method — SwitchLanguageAction.getLocale

**File:** `src/main/java/com/action/SwitchLanguageAction.java`, line 83
**Detail:** The `getLocale` static method is public and non-trivial. It maps an integer-as-string language code to a `Locale`:
- `"1"` → `Locale.ENGLISH`
- `"2"` → `Locale.SIMPLIFIED_CHINESE`
- `"3"` → `new Locale("tr", "TR", "")` (Turkish)
- `"4"` → `new Locale("ms", "MY", "")` (Malay)
- Any other value (including `"0"`) → returns `null`

The return of `null` for unrecognised or `"0"` input is a notable and potentially dangerous behaviour — callers must guard against it, but there is no documentation of this contract. No Javadoc, no `@param`, no `@return` tag documenting the nullable semantics.

---

### A28-5 [LOW] Missing class-level Javadoc — SwitchRegisterAction

**File:** `src/main/java/com/action/SwitchRegisterAction.java`, line 17
**Detail:** The class `SwitchRegisterAction` has no class-level Javadoc comment.

---

### A28-6 [MEDIUM] Undocumented non-trivial public method — SwitchRegisterAction.execute

**File:** `src/main/java/com/action/SwitchRegisterAction.java`, line 20
**Detail:** The `execute` method is non-trivial and has no Javadoc. It: obtains the existing session via `getSession(false)` (will throw a `NullPointerException` if no session exists — an implicit precondition that is undocumented); populates the session with all timezones (`"arrTimezone"`) from `TimezoneDAO`, all languages (`"arrLanguage"`) from `LanguageDAO`, and the string `"register"` for the attribute `"accountAction"`; then forwards to `"success"`. The implicit session-must-exist precondition and the session attributes set are not documented anywhere. No `@param`, `@return`, or `@throws` tags.

---

### A28-7 [LOW] Missing class-level Javadoc — WelcomeAction

**File:** `src/main/java/com/action/WelcomeAction.java`, line 33
**Detail:** The class `WelcomeAction` has no class-level Javadoc comment.

---

### A28-8 [MEDIUM] Undocumented non-trivial public method — WelcomeAction.execute

**File:** `src/main/java/com/action/WelcomeAction.java`, line 37
**Detail:** The `execute` method is non-trivial and has no Javadoc. It: reads the `ckLanguage` cookie via `SwitchLanguageAction.getCookie`; if found, resolves the corresponding `Locale` via `SwitchLanguageAction.getLocale` and sets it in the session; loads all advertisements from `AdvertismentDAO` into the session attribute `"sessAds"`; then forwards to `"success"`. There is a latent risk: if `getLocale` returns `null` (e.g. for an unrecognised cookie value), `null` is stored as the session locale — this silent null-locale assignment is undocumented. No `@param`, `@return`, or `@throws` tags.

---

## 4. Summary Table

| ID | Severity | File | Line | Description |
|----|----------|------|------|-------------|
| A28-1 | LOW | SwitchLanguageAction.java | 18 | No class-level Javadoc |
| A28-2 | MEDIUM | SwitchLanguageAction.java | 22 | `execute` undocumented — non-trivial public method |
| A28-3 | MEDIUM | SwitchLanguageAction.java | 71 | `getCookie` undocumented — non-trivial public static method; nullable return undocumented |
| A28-4 | MEDIUM | SwitchLanguageAction.java | 83 | `getLocale` undocumented — non-trivial public static method; null return for unrecognised input undocumented |
| A28-5 | LOW | SwitchRegisterAction.java | 17 | No class-level Javadoc |
| A28-6 | MEDIUM | SwitchRegisterAction.java | 20 | `execute` undocumented — non-trivial public method; implicit session-exists precondition undocumented |
| A28-7 | LOW | WelcomeAction.java | 33 | No class-level Javadoc |
| A28-8 | MEDIUM | WelcomeAction.java | 37 | `execute` undocumented — non-trivial public method; silent null-locale risk from `getLocale` undocumented |

**Totals:** 3 LOW, 5 MEDIUM, 0 HIGH
**Total findings:** 8
