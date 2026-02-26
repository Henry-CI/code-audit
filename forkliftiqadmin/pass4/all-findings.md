# P4 Agent A01 — AdminAddAlertAction, AdminAlertAction

## Reading Evidence

### AdminAddAlertAction
- Class: `AdminAddAlertAction` extends `org.apache.struts.action.Action` (line 17)
- Methods:
  - `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` (line 20) — `@Override`, returns `ActionForward`, throws `Exception`
- Constants/Types: None declared in this class

### AdminAlertAction
- Class: `AdminAlertAction` extends `org.apache.struts.action.Action` (line 15)
- Methods:
  - `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` (line 18) — `@Override`, returns `ActionForward`, throws `Exception`
- Constants/Types: None declared in this class

---

## Findings

A01-1 | HIGH | AdminAddAlertAction.java:22 | Null-dereference risk on session. `request.getSession(false)` can return `null` when no session exists. The result is used immediately on line 22 (`session.getAttribute(...)`) without a null check, causing a `NullPointerException` at runtime for any unauthenticated request that reaches this action. `AdminAlertAction` avoids this issue entirely because it does not call `getSession` at all, making the pattern inconsistent between the two files.

A01-2 | HIGH | AdminAddAlertAction.java:24 | Unsafe unboxing cast from session attribute. `(Integer) session.getAttribute("sessUserId")` on line 24 will throw a `ClassCastException` if the attribute is not an `Integer`, and will throw a `NullPointerException` during auto-unboxing if the attribute is present but null. The null guard `== null ? 0 :` only protects the outer `getAttribute` call returning null; it does not protect against the cast itself. A non-`Integer` value stored in that session key will bypass the null check and still cause a `ClassCastException`.

A01-3 | MEDIUM | AdminAddAlertAction.java:31 | Duplicate logic — `addUserSubscription` called identically in both the `"alert"` branch (line 28) and the `"report"` branch (line 31) before fetching different lists. The subscription call does not vary between branches. This indicates either a missing abstraction (the common call should be extracted before the if/else) or a logic error where the `"report"` branch should not be calling `addUserSubscription` at all.

A01-4 | MEDIUM | AdminAddAlertAction.java:39 | Inconsistent forward on error. When `src` does not match `"alert"` or `"report"`, errors are saved but the action still forwards to `"adminalerts"` (line 39). `AdminAlertAction` correctly forwards to `"globalfailure"` on its error path (line 34). The inconsistency means the add-alert action silently renders the alerts page as if nothing went wrong, making the saved error message the only signal of failure — and only if that forward page displays global errors.

A01-5 | MEDIUM | AdminAddAlertAction.java:22-24 | Session attributes read twice per attribute. `session.getAttribute("sessCompId")` is called twice on line 22 (once for the null check, once for the cast), and `session.getAttribute("sessUserId")` is called twice on line 24. Each call is a separate map lookup. The pattern is inconsistent with a cleaner single-assignment approach and introduces a narrow TOCTOU window if session state could change between calls, though more importantly it is a readability and maintenance issue.

A01-6 | MEDIUM | AdminAddAlertAction.java:22 | `sessCompId` is read from the session and assigned (line 22) but never used anywhere in the method body. This is dead code / unused variable that adds noise and may indicate an incomplete implementation (e.g., the subscription or list query was originally intended to be filtered by company).

A01-7 | LOW | AdminAlertAction.java:18-20 | Inconsistent method signature formatting relative to `AdminAddAlertAction`. In `AdminAddAlertAction` the entire parameter list is on a single line (line 20). In `AdminAlertAction` the parameters are split across three lines with inconsistent indentation — line 18 starts the declaration, line 19 uses 7-space indent for `ActionForm`, and line 20 uses a mix of tabs and spaces for alignment. This cross-file and intra-file formatting inconsistency indicates no enforced formatter is in use.

A01-8 | LOW | AdminAlertAction.java:22 | Missing spaces around the ternary operator. `request.getParameter("action")==null?"":request.getParameter("action")` has no whitespace around `==`, `?`, or `:`. `AdminAddAlertAction` (lines 22–24) formats equivalent ternaries with spaces. This is an inconsistency within the codebase's own style.

A01-9 | LOW | AdminAlertAction.java:17-35 | Mixed indentation: tabs and spaces used interchangeably within the method body. Lines 24–29 use 4-space soft-indentation while lines 31–34 switch to tab characters. `AdminAddAlertAction` uses spaces throughout. The inconsistency will cause misalignment across editors and indicates no common formatter configuration is enforced.

A01-10 | LOW | AdminAddAlertAction.java:22-24 | String parameter name `src` (from the HTTP request, line 23) versus the session-derived user/company identifiers is not validated or sanitized beyond a null-to-empty-string coercion. The same pattern appears in `AdminAlertAction` line 22 with `action`. While not directly exploitable in this logic, the pattern of trusting raw request parameters in `equalsIgnoreCase` branching without any input sanitisation is worth flagging for consistency with a defensive coding standard.

A01-11 | INFO | AdminAlertAction.java:4 | `HttpServletResponse` is imported (line 4) and declared as a parameter (line 19) but the response object is never used in the method body. This is a required part of the Struts `Action.execute` contract so it is not a removable import, but it is worth noting as expected dead parameter usage inherent to the framework.

A01-12 | INFO | AdminAddAlertAction.java:28,31 | `CompanyDAO.addUserSubscription` and the list-fetching methods (`getAlertList`, `getReportList`) are all `static` methods called directly on the DAO class. Combined with `AdminAlertAction` calling `CompanyDAO.getAlertList()`/`getReportList()` the same way, both action classes are tightly coupled to the concrete `CompanyDAO` static implementation with no interface or abstraction layer. This is a leaky abstraction / layering violation: the action (controller) layer directly invokes static DAO methods, making unit testing and DAO substitution impossible without class-level mocking.
# P4 Agent A02 — AdminDealerAction, AdminDriverAddAction

## Reading Evidence

### AdminDealerAction
- Class: `AdminDealerAction extends Action` (line 16)
- Methods:
  - `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` (line 18) — overrides `Action.execute`
  - `prepareDealerRequest(HttpServletRequest, HttpSession)` (line 32) — `public static`
- Constants/Types: none defined in this file
- Imports used: `AdminDealerActionForm`, `CompanyBean`, `RoleBean`, `CompanyDAO`, `StringUtils`, Struts `Action`/`ActionForward`/`ActionForm`/`ActionMapping`, `HttpServletRequest`, `HttpServletResponse`, `HttpSession`, `SQLException`, `ArrayList`

### AdminDriverAddAction
- Class: `AdminDriverAddAction extends Action` (line 19)
- Methods:
  - `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` (line 21) — overrides `Action.execute`
- Constants/Types: none defined in this file
- Imports used: `AdminDriverAddForm`, `DriverBean`, `UserBean`, `UserSignUpRequest`, `UserSignUpResponse`, `CompanyDAO`, `DriverDAO`, `RestClientService`, `RuntimeConf`, Struts action types, `HttpServletRequest`, `HttpServletResponse`, `HttpSession`

---

## Findings

A02-1 | HIGH | AdminDealerAction.java:33 | Null-dereference risk on session attribute. `session.getAttribute("isSuperAdmin")` returns `Object` and is compared with `.equals(false)` without a null guard. If the attribute is absent the call throws `NullPointerException`, bypassing the super-admin check entirely and allowing the method to execute for unauthenticated or anonymous sessions.

A02-2 | HIGH | AdminDriverAddAction.java:88 | Plain-text password stored in the database. `UserBean` is constructed with `adminDriverAddForm.getPass()` (line 88) and persisted via `compDao.saveUsers(...)` (line 91). The raw password is stored in the `user` table with no hashing, which is a security and data-protection defect. (Cognito is used for authentication; the local copy of the password is unnecessary and dangerous.)

A02-3 | HIGH | AdminDriverAddAction.java:26-99 | `execute()` does not guard against a `null` `opCode`. If `adminDriverAddForm.getOp_code()` returns `null`, the two `equalsIgnoreCase` calls do not throw (they are called on the string literal, so safe), but `return_code` remains an empty string `""` throughout. `mapping.findForward("")` is then called at line 99, which returns `null` from Struts and causes a `NullPointerException` in the framework dispatcher. No default/error forward is provided for an unrecognised op-code.

A02-4 | MEDIUM | AdminDealerAction.java:16 | Leaky abstraction — static utility method on an Action class. `prepareDealerRequest` is `public static`, directly couples the DAO layer to request/session attributes, and is designed to be called from other Action classes (see usage pattern). This logic belongs in a shared service or helper class, not on an Action subclass where it bleeds DAO and session knowledge into the controller layer.

A02-5 | MEDIUM | AdminDriverAddAction.java:30-96 | Chained `if` blocks instead of `if/else if` for mutually exclusive op-codes. Lines 30 and 44 both start with `if(opCode.equalsIgnoreCase(...))` independently. If a future op-code accidentally matches both strings (impossible here, but the pattern permits it) both branches execute and `return_code` is overwritten silently. The idiomatic and safe pattern is `else if`.

A02-6 | MEDIUM | AdminDriverAddAction.java:46 | Unused local variable `compDao` acquired before the early-exit paths. `CompanyDAO compDao = CompanyDAO.getInstance()` is declared at line 46 inside the `add_general_user` block, but is only used conditionally — after the error branches at lines 63–80 have already set `return_code = "globalfailure"` and returned. The object is obtained (and any connection state initialised) regardless of whether the success path is reached. The variable is not technically dead code but the acquisition is unnecessarily early and could hold resources in error paths.

A02-7 | MEDIUM | AdminDriverAddAction.java:49 | Typo in local variable name: `restClientServce` (line 49) — missing the second `i` in "Service". This is a style/readability defect that is consistent with a broader pattern of inconsistent naming in the file.

A02-8 | MEDIUM | AdminDriverAddAction.java (multiple) | Inconsistent naming conventions within the file. The file mixes Java camelCase field access (`driverbean`, `signUpRequest`, `signUpResponse`, `opCode`) with snake_case identifiers (`return_code`, `op_code`, `email_addr`, `first_name`, `last_name`) sourced from form fields. While the form bean uses snake_case fields (itself a violation of Java conventions), the local variable `return_code` (line 28) and the method calls `getOp_code()`, `getEmail_addr()`, `getFirst_name()`, `getLast_name()` are all snake_case inside a Java class, violating standard Java naming conventions throughout.

A02-9 | MEDIUM | AdminDealerAction.java vs AdminDriverAddAction.java | Inconsistent brace style across the two files. `AdminDealerAction` uses same-line opening braces (K&R style) throughout. `AdminDriverAddAction` mixes K&R (lines 19, 21) with Allman style (lines 31, 39, 44) where opening braces appear on the next line. Within `AdminDriverAddAction` alone, lines 31 and 38–39 show the mixed style most clearly (`if` uses next-line brace but `else` uses same-line).

A02-10 | MEDIUM | AdminDriverAddAction.java:75 | Inconsistent indentation. Lines 75–79 (the inner `ActionErrors`/`ActionMessage` block) are indented with five leading spaces/tabs rather than matching the surrounding four-space or tab-based indentation of the rest of the method, producing visually misaligned code.

A02-11 | LOW | AdminDriverAddAction.java:48 | Blank line noise. Two consecutive blank lines at lines 47–48 inside a short `if` block serve no structural purpose and are inconsistent with spacing conventions in the rest of the file and in `AdminDealerAction`.

A02-12 | LOW | AdminDealerAction.java:35 | Raw `ArrayList` return type from DAO used directly. `CompanyDAO.getInstance().getAllCompany()` returns `ArrayList<CompanyBean>` and is assigned to a raw-typed-adjacent local. While generics are used, programming against `ArrayList` (a concrete type) rather than `List` is a minor abstraction leak and makes the code harder to refactor.

A02-13 | LOW | AdminDealerAction.java:14 | Import `java.util.ArrayList` — concrete collection type imported and used in method signature context instead of `java.util.List`. See A02-12.

A02-14 | INFO | AdminDriverAddAction.java:56 | Hard-coded empty string for `phoneNumber` in `UserSignUpRequest.builder()` (line 56: `.phoneNumber("")`). If phone number is intentionally optional, `null` or an explicit optional type would better communicate intent; an empty string may cause downstream validation failures in Cognito or the REST service.

A02-15 | INFO | AdminDealerAction.java:42 | Role string `"ROLE_DEALER"` is a hard-coded literal rather than using `RuntimeConf.ROLE_DEALER`. `RuntimeConf` defines this constant (and it is used in `AdminDriverAddAction` via `RuntimeConf.ROLE_SITEADMIN`), so the inconsistency creates a maintenance risk if the role name changes.
# P4 Agent A03 — AdminDriverEditAction, AdminFleetcheckAction

## Reading Evidence

### AdminDriverEditAction
- **Class:** `AdminDriverEditAction extends Action` (line 20)
- **Methods:**
  - `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` (line 22) — overrides `Action.execute`
- **Constants/Types defined:** None
- **Imports used:**
  - `com.actionform.AdminDriverEditForm`
  - `com.bean.*` (wildcard)
  - `com.cognito.bean.UserUpdateResponse`
  - `com.dao.CompanyDAO`
  - `com.dao.DriverDAO`
  - `com.dao.SubscriptionDAO`
  - `com.service.DriverService`
  - `com.util.RuntimeConf`
  - `org.apache.struts.action.*` (wildcard)
  - `javax.servlet.http.HttpServletRequest`
  - `javax.servlet.http.HttpServletResponse`
  - `javax.servlet.http.HttpSession`
  - `java.io.PrintWriter`
  - `java.util.List`

### AdminFleetcheckAction
- **Class:** `AdminFleetcheckAction extends Action` (line 16)
- **Methods:**
  - `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` (line 18) — overrides `Action.execute`
- **Constants/Types defined:** None
- **Imports used:**
  - `com.actionform.AdminFleetcheckActionForm`
  - `com.bean.QuestionBean`
  - `com.dao.ManufactureDAO`
  - `com.dao.QuestionDAO`
  - `org.apache.commons.lang.StringUtils`
  - `org.apache.struts.action.*` (wildcard)
  - `javax.servlet.http.HttpServletRequest`
  - `javax.servlet.http.HttpServletResponse`
  - `javax.servlet.http.HttpSession`
  - `java.util.ArrayList`
  - `java.util.List`

---

## Findings

A03-1 | HIGH | AdminDriverEditAction.java:4 | **Wildcard import `com.bean.*`** — importing an entire package hides exactly which bean types are used (`DriverBean`, `LicenceBean`, `AlertBean`, `DriverVehicleBean`). Wildcard imports are a build-warning-class problem (they can pull in unexpected types on recompile and obscure dependencies). The companion file `AdminFleetcheckAction.java` imports only the specific class it needs (`com.bean.QuestionBean`), making the two files inconsistent in import style.

A03-2 | HIGH | AdminDriverEditAction.java:12 | **Wildcard import `org.apache.struts.action.*`** — same issue as A03-1. `AdminFleetcheckAction.java` (line 8) also uses the same wildcard, so both files are inconsistent with single-class import discipline observed elsewhere in `AdminFleetcheckAction` (e.g., explicit `com.bean.QuestionBean`, `org.apache.commons.lang.StringUtils`). Within `AdminFleetcheckAction` the mixed practice (explicit beans, wildcard for Struts) is an intra-file inconsistency.

A03-3 | HIGH | AdminDriverEditAction.java:89 | **Unused local variable `compDao`** — `CompanyDAO compDao = CompanyDAO.getInstance();` is assigned but never read. The `CompanyDAO` is subsequently accessed only via its static methods (`CompanyDAO.addUserSubscription`, etc.) or via a separate instance obtained at line 156. This dead assignment will produce a compiler warning and indicates copy-paste error.

A03-4 | HIGH | AdminDriverEditAction.java:113 | **Redundant `response.getWriter()` call (return value discarded)** — line 113 calls `response.getWriter()` and throws away the result; line 115 calls it again and assigns the `PrintWriter`. The first call is dead/wasteful and may log a resource-management warning. The `PrintWriter` from line 113 is never flushed or closed; only the second reference (line 115) is used.

A03-5 | MEDIUM | AdminDriverEditAction.java:32–188 | **Single monolithic `execute` method with chained `if` blocks instead of `if/else if`** — the five operation-code branches (`edit_general`, `edit_general_user`, `check_licenceExist`, `edit_licence`, `edit_subscription`, `edit_vehicle`) are written as independent `if` statements rather than `if / else if / else`. Every call evaluates all six conditions even after one has matched and set `return_code`. `AdminFleetcheckAction` correctly uses `if / else if / else` (lines 35–73). This is both a style inconsistency across the two files and a minor runtime inefficiency.

A03-6 | MEDIUM | AdminDriverEditAction.java:31,57,64,96,103,119,134,139,146,178,186 | **Magic string operation codes and forward names** — string literals such as `"edit_general"`, `"edit_general_user"`, `"check_licenceExist"`, `"edit_licence"`, `"edit_subscription"`, `"edit_vehicle"`, `"success"`, `"successUser"`, `"failure"`, `"globalfailure"` are scattered through the method with no named constants. The same pattern appears in `AdminFleetcheckAction` (`"search"`, `"add"`, `"success"`, `"edit"`, `"failure"`). Neither file defines constants; this is a consistent bad practice across both files.

A03-7 | MEDIUM | AdminDriverEditAction.java:26,28 | **Inconsistent null-guard style for session attributes** — line 26 uses a ternary (`session.getAttribute(...) == null ? "" : ...`) while line 28 reverses the operand order (`session.getAttribute(...) == null ? "" : (String) session.getAttribute(...)`). Line 26 evaluates `session.getAttribute("sessCompId")` twice; line 28 also evaluates `session.getAttribute("sessionToken")` twice. Both are minor null-guard style inconsistencies within the same file and a repeated unnecessary double-lookup.

A03-8 | MEDIUM | AdminDriverEditAction.java:156 | **Second `CompanyDAO` instance obtained inside `edit_subscription` block** — `CompanyDAO dao = CompanyDAO.getInstance()` at line 156 duplicates the call already made at line 89 (the dead `compDao`). If `getInstance()` is a true singleton this is harmless but wasteful; if it allocates a new object each time it is a resource leak. Combined with the dead `compDao` (A03-3), the intent is unclear.

A03-9 | MEDIUM | AdminFleetcheckAction.java:39 | **`arrQuestions.size() == 0` should be `arrQuestions.isEmpty()`** — using `== 0` instead of `isEmpty()` is a minor style issue; `isEmpty()` is the idiomatic Java collection check and is flagged by tools such as Checkstyle and SonarQube.

A03-10 | MEDIUM | AdminFleetcheckAction.java:59 | **Concrete type `ArrayList` used instead of interface `List`** — `ArrayList<QuestionBean> arrQuestions = new ArrayList<>()` declares the variable with the concrete type. The rest of the file, and the `AdminDriverEditAction` file, use `List<...>` for all list variables. This is an intra-file style inconsistency.

A03-11 | LOW | AdminFleetcheckAction.java:67 | **Typo in error key: `"resutlerror"` vs `"resulterror"`** — line 43 adds an error under the key `"resulterror"` (search branch); line 67 adds an error under the key `"resutlerror"` (else/failure branch). These two keys will behave differently if the JSP checks a specific key name, causing the error message to silently fail to render in the else branch.

A03-12 | LOW | AdminDriverEditAction.java:128 | **Typo in message key: `"error.duplcateLicence"`** — the key is spelled `duplcate` (missing `i`). If the corresponding `ApplicationResources.properties` key is correct, this will silently fail to resolve the message. If the properties file also has the same typo the inconsistency is masked but both are still wrong.

A03-13 | LOW | AdminDriverEditAction.java | **Naming convention inconsistency: snake_case local variables mixed with camelCase** — variables such as `fname`, `lname`, `email_addr`, `pass_hash`, `app_access`, `cognito_username`, `type_id`, `fuel_type_id`, `manu_id`, `att_id`, `return_code` mix Java camelCase convention with underscored snake_case. `AdminFleetcheckAction` uses the same pattern (`type_id`, `fuel_type_id`, `manu_id`, `att_id`). This is a project-wide convention violation present in both files.

A03-14 | LOW | AdminDriverEditAction.java:150–179 | **Inconsistent indentation in `edit_subscription` block** — the block starting at line 150 uses a mix of tab stops: the outer `if` body (lines 152–154) is indented with one extra level of tabs relative to the surrounding code, while the inner `CompanyDAO` calls (lines 156–175) align to yet another tab stop. `AdminFleetcheckAction` maintains consistent 4-space-equivalent indentation throughout. This is a formatting inconsistency within `AdminDriverEditAction` and across the two files.

A03-15 | INFO | AdminDriverEditAction.java:22 | **`execute` method signature throws checked `Exception`** — declaring `throws Exception` is the contract imposed by the Struts 1 `Action` base class, so this is expected framework usage. Noted for completeness as it leaks the broadest possible checked exception type, but is not actionable without a framework upgrade.
# P4 Agent A04 — AdminFleetcheckDeleteAction, AdminFleetcheckEditAction

## Reading Evidence

### AdminFleetcheckDeleteAction
- Class: `AdminFleetcheckDeleteAction` (extends `org.apache.struts.action.Action`)
- Methods:
  - `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` (line 15)
- Constants/Types: none defined

### AdminFleetcheckEditAction
- Class: `AdminFleetcheckEditAction` (extends `org.apache.struts.action.Action`)
- Methods:
  - `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` (line 29)
  - `update(ActionMapping, HttpServletRequest, QuestionBean, String, String)` — private (line 76)
  - `create(ActionMapping, HttpServletRequest, QuestionBean, String)` — private (line 97)
  - `getFailureForward(ActionMapping, HttpServletRequest)` — private (line 107)
- Constants/Types: none defined

---

## Findings

A04-1 | CRITICAL | AdminFleetcheckDeleteAction.java:21 | `execute()` returns `null` unconditionally. After calling `QuestionDAO.delQuestionById()` the method returns `null` instead of a named `ActionForward`. Struts will receive `null` and the framework will be unable to route the response, leaving the browser with a blank/error page. Every other action in the file set (e.g. `AdminFleetcheckEditAction`) returns a meaningful `ActionForward`; this is both a functional defect and a consistency violation.

A04-2 | CRITICAL | AdminFleetcheckDeleteAction.java:20 | No authentication / authorisation guard before deleting a record. `AdminFleetcheckEditAction` (line 32–33) reads `sessCompId` from the session and uses it to scope every data operation. `AdminFleetcheckDeleteAction` performs a hard delete directly on the id supplied in the form with no session check, no ownership check, and no validation that the id belongs to the authenticated company. This exposes an insecure-direct-object-reference (IDOR) vulnerability.

A04-3 | HIGH | AdminFleetcheckDeleteAction.java:20 | The `id` value from the form is passed directly into `QuestionDAO.delQuestionById()`, which concatenates it into a raw SQL string (`"delete from question where id=" + id` — QuestionDAO.java line 183) without any sanitisation or use of a `PreparedStatement`. The action layer makes no attempt to validate or reject non-numeric input before forwarding the value to the DAO, making SQL injection trivially possible through this endpoint.

A04-4 | HIGH | AdminFleetcheckEditAction.java:35 | Unchecked cast of a session attribute to `List<CompanyBean>` with no null guard. If `"arrComp"` is absent from the session (expired, tampered, or first-time request), the cast and subsequent `.get(0)` will throw a `NullPointerException` or `ClassCastException` that propagates as an unhandled 500 error. `sessCompId` on the same line (33–34) is guarded with a null-coalesce, but `arrComp` is not.

A04-5 | HIGH | AdminFleetcheckEditAction.java:99 | `Integer.parseInt(bean.getComp_id())` is called inside `create()` with no null/empty check. `sessCompId` is initialised to `""` (empty string) when the session attribute is missing (line 33–34), so a missing session value produces a `NumberFormatException` rather than a meaningful error response.

A04-6 | MEDIUM | AdminFleetcheckEditAction.java:29-30 | Inconsistent parameter alignment in `execute()`. In `AdminFleetcheckDeleteAction` (line 15–16) the `execute` signature places all four parameters on two lines with the continuation indented to align under `ActionMapping`. In `AdminFleetcheckEditAction` the signature splits differently, placing `ActionForm` and the two servlet types on a second line indented only four spaces. This inconsistency is minor but indicates no enforced formatting standard across the two sibling classes.

A04-7 | MEDIUM | AdminFleetcheckEditAction.java:40 | `QuestionDAO.getQuestionById()` returns `ArrayList<QuestionBean>` (a concrete type). The local variable is declared as `ArrayList<QuestionBean>` (line 40) rather than `List<QuestionBean>`. Using the concrete `ArrayList` type leaks implementation details and couples the calling code to the DAO's internal collection choice; the return value is set directly on the request attribute, so callers in JSP/JSTL also implicitly depend on this concrete type.

A04-8 | MEDIUM | AdminFleetcheckEditAction.java:3 | Unused import: `java.sql.SQLException`. The `execute()` method declares `throws Exception`; `SQLException` is only thrown by the private helper methods and is re-thrown as `Exception` up the call chain. `SQLException` is never directly referenced in the import's scope, making the import redundant.

A04-9 | MEDIUM | AdminFleetcheckEditAction.java:5-6 | Unused imports: `java.util.ArrayList` and `java.util.List`. Neither `ArrayList` nor `List` is used as a declared type within `AdminFleetcheckEditAction.java` itself. `ArrayList` appears only in the return type of `QuestionDAO.getQuestionById()` (resolved by the compiler through the DAO, not through an explicit local declaration in this file), and `List` is never referenced at all in this file.

A04-10 | LOW | AdminFleetcheckDeleteAction.java (entire file) vs AdminFleetcheckEditAction.java | `AdminFleetcheckDeleteAction` contains no logging whatsoever. `AdminFleetcheckEditAction` (and all other DAOs/actions in the codebase) use `log.info()` to trace entry points and SQL. A delete operation — which is irreversible — is the most important operation to audit-log, yet it is the only action that produces no trace.

A04-11 | LOW | AdminFleetcheckEditAction.java:54 | `ManufactureDAO.getAllManufactures(sessCompId)` is called unconditionally on every POST, populating `"arrManufacturers"` on the request (line 54), even when `getFailureForward` is subsequently returned. If either `updateQuestionInfo` or `saveQuestionInfo` fails, the manufacturers list has already been fetched and set but the forward target (`"globalfailure"`) may not render it, making the fetch wasteful on the failure path.

A04-12 | LOW | AdminFleetcheckEditAction.java:58 | Field name `answer_type` in the builder call (line 58: `.answer_type(...)`) uses snake_case, inconsistent with Java naming conventions. The same pattern appears throughout `QuestionBean` fields (`type_id`, `fuel_type_id`, `manu_id`, `attachment_id`, `order_no`, `comp_id`). This is a pre-existing bean design issue but the action perpetuates it by using the builder directly rather than any mapping layer that could normalise names.
# P4 Agent A05 — AdminFleetcheckHideAction, AdminFleetcheckShowAction

## Reading Evidence

### AdminFleetcheckHideAction
- Class: `AdminFleetcheckHideAction` extends `org.apache.struts.action.Action`
- Methods: `execute` (line 19)
- Constants/Types: none defined in this file

### AdminFleetcheckShowAction
- Class: `AdminFleetcheckShowAction` extends `org.apache.struts.action.Action`
- Methods: `execute` (line 16)
- Constants/Types: none defined in this file

---

## Findings

A05-1 | CRITICAL | AdminFleetcheckHideAction.java:33 | **Swapped arguments in `hideQuestionById` call.**
The DAO method signature is `hideQuestionById(String id, String manuId, String typeId, String fuleTypeId, String compId, String attchId)`. The call on line 33 passes arguments in the order `(getId(), manu_id, type_id, fuel_type_id, att_id, sessCompId)`, which puts `att_id` into the `compId` parameter position and `sessCompId` into the `attchId` parameter position. These last two arguments are transposed. At runtime this causes the company ID to be recorded as the attachment ID and vice versa when a global question is copied to a company, silently corrupting data.

A05-2 | HIGH | AdminFleetcheckHideAction.java:3-4 | **Unused imports.**
`com.actionform.AdminFleetcheckActionForm` (line 3) and `com.dao.ManufactureDAO` (line 5) are imported but never referenced in the file. These imports will generate compiler/IDE warnings and indicate either leftover copy-paste residue or dead code from a refactor.

A05-3 | MEDIUM | AdminFleetcheckHideAction.java:22-24 | **No null-guard on session before attribute access.**
`request.getSession(false)` may return `null` if no session exists (that is its documented contract). The code immediately dereferences `session.getAttribute(...)` on line 23 without a null check. If called without an active session this will throw a `NullPointerException`, producing an unhandled 500 error rather than a controlled redirect or error response. `AdminFleetcheckShowAction` avoids this problem entirely by not using the session at all, making the two sibling actions inconsistent in their session handling.

A05-4 | MEDIUM | AdminFleetcheckHideAction.java:23-24 | **Double attribute lookup on session.**
`session.getAttribute("sessCompId")` is called twice in the ternary expression (once for the null check and once for the value). This is a minor inefficiency and readability issue; the result should be assigned to a local variable first, then tested.

A05-5 | MEDIUM | AdminFleetcheckHideAction.java (cross-file) | **Asymmetric session/company-ID usage between Hide and Show.**
`AdminFleetcheckHideAction` reads `sessCompId` from the session and passes it to the DAO. `AdminFleetcheckShowAction` calls `showQuestionById` with only the question ID and passes no company context at all. The DAO's `showQuestionById` does not accept a company ID. This asymmetry means the hide path enforces company scoping (even if the arguments are currently swapped) while the show path does not, which is a leaky abstraction — the business rule for company ownership is handled inconsistently at the action layer rather than enforced uniformly by the DAO.

A05-6 | LOW | AdminFleetcheckHideAction.java:28-31 | **Snake_case local variable names violate Java naming conventions.**
Local variables `type_id`, `fuel_type_id`, `manu_id`, and `att_id` use snake_case. Java convention (and the rest of the codebase's DAO layer, e.g., `manuId`, `typeId` in the DAO signature) uses camelCase. `AdminFleetcheckShowAction` has no local variables and so does not share this inconsistency, creating a style divergence between the two sibling files.

A05-7 | LOW | AdminFleetcheckHideAction.java:28-31 | **`att_id` abbreviation is inconsistent with the field name.**
The form field is named `attachment_id` and retrieved via `getAttachment_id()`, but the local variable is shortened to `att_id`. This inconsistency (partial abbreviation) makes the mapping harder to follow and differs from the other three local variable names which preserve the full field-name stem (`type_id`, `fuel_type_id`, `manu_id`).

A05-8 | LOW | AdminFleetcheckHideAction.java:35-37 / AdminFleetcheckShowAction.java:22-24 | **`PrintWriter` not closed after use.**
In both actions, `response.getWriter()` is obtained and written to, but the writer is never closed (no `writer.close()` call, no try-with-resources). While the servlet container will eventually close the underlying stream, not closing the writer is a resource management inconsistency and will produce compiler warnings with static-analysis tools that enforce `AutoCloseable` hygiene.

A05-9 | INFO | Both files | **Deprecated framework (Apache Struts 1).**
Both classes extend `org.apache.struts.action.Action`, which is part of Apache Struts 1. Struts 1 reached end-of-life in December 2013 and has known security vulnerabilities. This is a project-wide architectural concern visible at the code level; all action classes in the codebase inherit the same issue.
# P4 Agent A06 — AdminManufacturersAction, AdminMenuAction

## Reading Evidence

### AdminManufacturersAction
- Class: `AdminManufacturersAction extends PandoraAction` (line 16)
- Methods:
  - `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` (line 18) — public
  - `returnManufacturersJson(HttpServletResponse, String)` (line 54) — private
  - `returnBooleanJson(HttpServletResponse, Boolean)` (line 61) — private
- Constants/Types: none defined in this class
- Imports: `AdminManufacturersActionForm`, `ManufactureBean`, `ManufactureDAO`, `JSONObject` (com.json), `@Slf4j` (Lombok), `org.apache.struts.action.*`, `HttpServletRequest`, `HttpServletResponse`, `HttpSession`, `PrintWriter`

### AdminMenuAction
- Class: `AdminMenuAction extends Action` (line 15)
- Methods:
  - `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` (line 17) — public, @Override
- Constants/Types: none defined in this class
- Imports (wildcard): `com.bean.*`, `com.dao.*`, `ReportService`, `Globals`, `org.apache.struts.action.*`, `HttpServletRequest`, `HttpServletResponse`, `HttpSession`, `ArrayList`, `Locale`

---

## Findings

A06-1 | HIGH | AdminManufacturersAction.java:16 | `AdminManufacturersAction` extends `PandoraAction`, which provides session/request helper utilities (e.g., `getCompId`, `getSessionAttribute`, `getLongSessionAttribute`). None of those helpers are used; instead, raw `session.getAttribute("sessCompId")` with inline null-coalescing is duplicated directly in `execute` (line 24). This defeats the purpose of the base class abstraction and is inconsistent with the pattern `PandoraAction` was designed to enforce.

A06-2 | HIGH | AdminMenuAction.java:15 | `AdminMenuAction` extends `Action` directly, bypassing `PandoraAction` entirely, while `AdminManufacturersAction` (the sister class in the same package) extends `PandoraAction`. Both classes perform identical session-attribute extraction patterns (null checks, inline casting, default values) for `sessCompId`, `sessUserId`, `sessTimezone`, `sessionToken`, and `sessDateFormat`. Inconsistent base class choice means the shared helpers in `PandoraAction` are unavailable in `AdminMenuAction`, producing duplicated boilerplate and a leaky abstraction.

A06-3 | HIGH | AdminMenuAction.java:26 | `Integer.parseInt(sessCompId)` is called unconditionally on line 26 without a null/empty guard. `sessCompId` is initialised to `""` when the session attribute is absent (line 23), so any unauthenticated or misconfigured request will throw `NumberFormatException` at runtime, potentially leaking an unhandled exception to the caller.

A06-4 | MEDIUM | AdminManufacturersAction.java:8 | Wildcard import `org.apache.struts.action.*` is used; only `ActionMapping`, `ActionForm`, and `ActionForward` are actually needed. While not harmful, it masks which Struts types are genuinely depended upon and is inconsistent with the explicit, per-type imports used for all other packages in this file.

A06-5 | MEDIUM | AdminMenuAction.java:3-4 | Both `com.bean.*` and `com.dao.*` are wildcard imports. The beans package contains roughly 55 classes and the dao package 23 classes; only a small fraction are used (`DriverBean`, `UnitBean`, `MenuBean`; `DriverDAO`, `UnitDAO`, `ManufactureDAO`, `CompanyDAO`, `TimezoneDAO`, `DateFormatDAO`, `MenuDAO`). Wildcard imports hide the actual dependency surface, make dead-code analysis harder, and risk silent compilation breaks when new classes with conflicting names are added to those packages.

A06-6 | MEDIUM | AdminMenuAction.java:108 | The `"subscription"` branch (lines 108–111) carries an inline comment `//Not used`, indicating the code path is known dead. It still executes DAO queries (`getUserAlert`, `getUserReport`), performs request attribute writes, and forwards to `"adminsubscription"`. Dead branches with live DAO calls waste resources and represent latent maintenance risk.

A06-7 | MEDIUM | AdminManufacturersAction.java:7 | `@Slf4j` is declared on the class (line 7 / line 15), generating a `log` field, but `log` is never referenced anywhere in the file. The logger import and annotation are unused. By contrast, `AdminMenuAction` has no logger at all. This is both a dead-code issue and a cross-file style inconsistency.

A06-8 | MEDIUM | AdminManufacturersAction.java:26 | The action dispatch uses a chain of `String.equals()` comparisons (`"add"`, `"edit"`, `"delete"`, `"isVehicleAssigned"`) against a value sourced from the form without null-guarding `getAction()`. If `getAction()` returns `null`, the first `equals` call on line 26 throws `NullPointerException`. `AdminMenuAction` avoids this by defaulting to `""` on line 22, but `AdminManufacturersAction` relies on form binding to supply a non-null value with no defensive check.

A06-9 | LOW | AdminManufacturersAction.java:18-52 | Indentation is inconsistent within `execute`. The opening brace and several lines in the `"add"` branch use a tab character for the outer body (lines 21, 24), while the `"edit"`, `"delete"`, and `"isVehicleAssigned"` branches use four-space indentation. The `"isVehicleAssigned"` handler at lines 44-47 uses yet a third mixed indent (two tabs + spaces). This is a within-file formatting inconsistency.

A06-10 | LOW | AdminMenuAction.java:35 | Missing newline before the `else if` on line 35 (`}else if`) breaks the consistent `} else if` spacing pattern used on all other branches in the same method (lines 39, 45, 48, 54, etc.). Minor but a within-file style inconsistency.

A06-11 | LOW | AdminMenuAction.java:86 | `AdvertismentDAO` (misspelled — missing a second 's') is referenced on line 86. The DAO class file is also named `AdvertismentDAO.java`, so the misspelling is consistent throughout the codebase, but it represents a persistent naming-convention defect that would surface as a confusing API for any future maintainer. The corresponding bean is correctly named `AdvertisementBean.java`.

A06-12 | LOW | AdminManufacturersAction.java:57,64 | Double space before `response.getWriter()` (`PrintWriter out =  response.getWriter();`) appears in both `returnManufacturersJson` (line 57) and `returnBooleanJson` (line 64). Trivial whitespace defect but appears in two places, suggesting copy-paste origin.

A06-13 | INFO | AdminMenuAction.java:79-84 | `MenuDAO` is instantiated directly with `new MenuDAO()` (line 79) rather than via a static method or singleton pattern. All other DAOs used in the same file (`DriverDAO`, `UnitDAO`, `ManufactureDAO`, etc.) are accessed via static methods or `getInstance()`. This inconsistency in DAO access pattern suggests `MenuDAO` was not updated when the project standardised its DAO access style.

A06-14 | INFO | AdminMenuAction.java:100 | Session attribute key `"seesArrComp"` on line 100 appears to be a typo of `"sessArrComp"` (double-'e' in "sees" vs. the "sess" prefix used uniformly for all other session keys in the file: `sessCompId`, `sessUserId`, `sessTimezone`, `sessDateFormat`). If any downstream JSP or filter reads this attribute by a different spelling it would silently receive `null`.
# P4 Agent A07 — AdminOperatorAction, AdminRegisterAction

## Reading Evidence

### AdminOperatorAction

- Class: `AdminOperatorAction extends PandoraAction` (line 17)
- Fields:
  - `manufactureDAO` (line 18) — `private ManufactureDAO`, initialised via `ManufactureDAO.getInstance()`
  - `unitDAO` (line 19) — `private UnitDAO`, initialised via `UnitDAO.getInstance()`
  - `trainingDAO` (line 20) — `private TrainingDAO`, initialised via `new TrainingDAO()`
- Methods:
  - `execute` (line 22)
  - `editAction` (line 63)
  - `editUserAction` (line 68)
  - `addAction` (line 74)
  - `addUserAction` (line 93)
  - `trainingAction` (line 106)
  - `subscriptionAction` (line 115)
  - `vehicleAction` (line 123)
  - `deleteAction` (line 134)
  - `deleteUserAction` (line 140)
  - `inviteAction` (line 146)
  - `searchAction` (line 153)
  - `searchUserAction` (line 161)
- Constants/Types: None defined in this file.
- Imports: `com.bean.*`, `com.dao.*`, `lombok.extern.slf4j.Slf4j`, `org.apache.struts.action.*`, `javax.servlet.http.*`, `java.sql.SQLException`, `java.util.ArrayList`, `java.util.Collections`, `java.util.List`

---

### AdminRegisterAction

- Class: `AdminRegisterAction extends Action` (line 37)
- Fields: None declared at class level (all locals).
- Methods:
  - `execute` (line 39)
  - `isValidEmailAddress` (line 303)
- Constants/Types: None defined in this file.
- Imports: `java.util.ArrayList`, `java.util.List`, `javax.servlet.http.*`, `com.dao.LoginDAO`, `org.apache.struts.action.*` (Action, ActionErrors, ActionForm, ActionForward, ActionMapping, ActionMessage, ActionMessages), `org.springframework.http.HttpMethod`, `org.apache.log4j.Logger`, `com.util.InfoLogger`, `com.util.RuntimeConf`, `com.util.Util`, `com.bean.CompanyBean`, `com.bean.RoleBean`, `com.cognito.bean.*` (AuthenticationRequest, AuthenticationResponse, UserSignUpRequest, UserSignUpResponse, UserUpdateResponse), `com.dao.CompanyDAO`, `com.dao.RoleDAO`, `com.dao.SubscriptionDAO`, `com.service.RestClientService`, `com.actionform.AdminRegisterActionForm`

---

## Findings

A07-1 | HIGH | AdminRegisterAction.java:18 | `org.springframework.http.HttpMethod` is imported but never used anywhere in the file. This is dead import / unused dependency that also introduces a confusing Spring dependency in a Struts action class.

A07-2 | HIGH | AdminRegisterAction.java:19 | `org.apache.log4j.Logger` is imported but never used anywhere in the file. The class has no logging at all, and no `@Slf4j` or Logger field is declared.

A07-3 | HIGH | AdminRegisterAction.java:21 | `com.util.InfoLogger` is imported but never used anywhere in the file.

A07-4 | HIGH | AdminRegisterAction.java:26 | `com.cognito.bean.AuthenticationRequest` is imported but never used anywhere in the file.

A07-5 | HIGH | AdminRegisterAction.java:27 | `com.cognito.bean.AuthenticationResponse` is imported but never used anywhere in the file.

A07-6 | MEDIUM | AdminOperatorAction.java:13 | `java.util.Collections` is imported but never used anywhere in the file. Dead import.

A07-7 | MEDIUM | AdminOperatorAction.java:18-20 | Inconsistent DAO instantiation style within the same class: `ManufactureDAO` and `UnitDAO` are obtained via `getInstance()` (singleton pattern), but `TrainingDAO` is instantiated with `new TrainingDAO()`. This inconsistency either breaks the singleton contract for `TrainingDAO` or signals that `TrainingDAO` was not updated to use the factory/singleton pattern used by its peers, and it may result in multiple instances being created per action object.

A07-8 | MEDIUM | AdminOperatorAction.java:37 | No logging is performed anywhere in `AdminOperatorAction` despite the class being annotated `@Slf4j` (line 16). The `log` field generated by the annotation is never referenced. The annotation is either forgotten to be used or was added speculatively and should be removed if logging is genuinely not needed.

A07-9 | MEDIUM | AdminRegisterAction.java:37 | `AdminRegisterAction` extends `org.apache.struts.action.Action` directly, while `AdminOperatorAction` extends `PandoraAction` (a project-level base class). The register action therefore lacks any session-guard or common utility methods that `PandoraAction` provides (e.g. `getSessionAttribute`, `getRequestParam`, `getLongRequestParam`). As a result, `AdminRegisterAction` reimplements session attribute retrieval inline with repeated null-check ternary expressions (lines 42–45) rather than using the shared helper methods. This is both a style inconsistency across the two files and a leaky abstraction: low-level null-checks that should live in one place are scattered through the action.

A07-10 | MEDIUM | AdminRegisterAction.java:235 | `e.printStackTrace()` is called in the catch block (line 235) instead of using a proper logger. Stack traces written to stderr are not captured by the application's logging framework, making production diagnosis difficult. `AdminOperatorAction` uses `@Slf4j` (even if unused) yet `AdminRegisterAction` has no logging at all — a clear inconsistency between the two files.

A07-11 | MEDIUM | AdminRegisterAction.java:80 | Raw parameterised type `new ArrayList<CompanyBean>()` is declared as `ArrayList<CompanyBean> arrComp` but the variable `arrComp` is populated on line 82 and then never read again anywhere in the method or passed to the request/session. This is dead code (unreachable effect).

A07-12 | MEDIUM | AdminRegisterAction.java:78 | `CompanyBean compBean = new CompanyBean()` (line 78) is instantiated inside the register/add block, added to `arrComp` (line 82), but neither `compBean` nor `arrComp` is ever used after line 82. Both are dead local variables.

A07-13 | MEDIUM | AdminRegisterAction.java:84 | `int compId = 1` is initialised to a hard-coded sentinel value of `1` (line 84). It is later overwritten by the actual DB-returned id on lines 170 and 195, but the initial value of `1` is misleading and could silently mask an unhandled code path where neither assignment is reached. The variable should be initialised to `0` or `-1` (or declared inside the branches where it is assigned) to make the intent clear.

A07-14 | LOW | AdminRegisterAction.java:174 | The confirmation email body (lines 174–176) contains a plain-text password (`adminRegisterActionForm.getPin()`) embedded in the email content. Sending credentials in clear text via email is a security concern. Noted here as a code-quality/practice finding; severity is kept LOW in this pass as the primary concern is code quality.

A07-15 | LOW | AdminOperatorAction.java:53 | Minor formatting inconsistency: the `deleteuser` case (line 53) has no space between `driverId,` and `sessCompId`, unlike all other multi-argument call sites in the same switch block. Similarly, line 57 (`searchdriver` case) uses a tab indent rather than 8-space indent matching the rest of the switch cases, indicating the later-added cases were not formatted to match the existing style.

A07-16 | LOW | AdminRegisterAction.java:117 | Local variable `restClientServce` is a misspelling of `restClientService`. This is a style/readability issue that would also generate IDE warnings.

A07-17 | LOW | AdminRegisterAction.java:133-164 | The two error-handling branches for Cognito sign-up failure (lines 133–148 and lines 149–164) are essentially identical: both create `ActionErrors`, add the same error key `"AdminRegisterError"`, save errors, and branch on `accountAction` to return `"failAdd"` or `"failure"`. This duplicated block should be extracted into a helper method, consistent with how `AdminOperatorAction` delegates to private methods.

A07-18 | INFO | AdminRegisterAction.java:303-309 | `isValidEmailAddress` compiles a new `Pattern` object on every invocation at runtime. The pattern string is a constant; the `Pattern` should be compiled once as a `private static final` field to avoid repeated compilation overhead.
# P4 Agent A08 — AdminSendMailAction, AdminSettingsAction

## Reading Evidence

### AdminSendMailAction
- Class: `AdminSendMailAction` extends `org.apache.struts.action.Action` (line 29)
- Fields:
  - `private DriverDAO driverDao` (line 31) — instance field, initialised via `DriverDAO.getInstance()`
- Methods:
  - `execute` (line 33) — public, overrides Struts `Action.execute`
  - `sendMail` (line 77) — public, returns `boolean`
  - `isValidEmailAddress` (line 111) — public, returns `boolean`
- Constants/Types: none declared

### AdminSettingsAction
- Class: `AdminSettingsAction` extends `org.apache.struts.action.Action` (line 21)
- Fields: none declared
- Methods:
  - `execute` (line 22) — public, overrides Struts `Action.execute`
- Constants/Types: none declared

---

## Findings

A08-1 | HIGH | AdminSendMailAction.java:100–108 | **sendMail always returns true regardless of failure.** The inner `try/catch` around `Transport.send` at line 99–103 swallows the `MessagingException` silently (prints to stdout), and execution falls through to `return true` at line 108 even when the send failed. The caller at line 55 therefore can never receive `false`, making the failure branch (lines 62–64) unreachable dead code. The method signature declares `throws AddressException, MessagingException` but those exceptions are consumed internally and never propagated.

A08-2 | HIGH | AdminSendMailAction.java:89–94 | **RecipientType exception swallowed silently.** The `catch (Exception e)` block at line 92 prints to stdout and continues execution. If `InternetAddress.parse` throws, the message is sent with no recipient, which is a silent data-integrity failure.

A08-3 | HIGH | AdminSendMailAction.java:105–107 | **`catch (Throwable t)` with only `t.printStackTrace()`.** Catching `Throwable` (including `Error`) at the outermost level of `sendMail` and swallowing it silently (only printing a stack trace to stderr) means JNDI lookup failures and other fatal conditions are silently ignored, and the method still returns `true`.

A08-4 | MEDIUM | AdminSendMailAction.java:93 / AdminSendMailAction.java:102 | **`System.out.println` used for error logging.** Both exception handlers in `sendMail` write to `System.out` instead of a logging framework (e.g., Log4j/SLF4J). `AdminSettingsAction` has no logging either, but it does not swallow exceptions. Inconsistent with the rest of the codebase's likely use of a logger; these messages will not appear in application logs.

A08-5 | MEDIUM | AdminSendMailAction.java:44–45 | **Hardcoded stub email subject and body.** `subject = "Driver Invitation"` and `body = "Driver Invite body"` are literal placeholder strings baked into the action. No template, no internationalisation, no actual invite content. This looks like unfinished implementation left in production code.

A08-6 | MEDIUM | AdminSendMailAction.java:55 | **`sendMail` called with empty-string sentinel arguments for optional parameters.** The call `sendMail(subject, body, "", emailAdd, "", "")` passes empty strings for `rName`, `sName`, and `sEmail`. The method signature offers named parameters that suggest sender-name and sender-email overrides, but the method ignores them entirely and hardcodes `"info@ciiquk.com"` at line 87. The extra parameters are dead API surface.

A08-7 | MEDIUM | AdminSendMailAction.java:77–78 | **`sendMail` is `public` but should be package-private or private.** It exposes internal mail infrastructure to any caller that obtains a reference to the action. `isValidEmailAddress` at line 111 is similarly `public` on an Action class; both are implementation helpers that form a leaky abstraction — mail-sending logic belongs in a dedicated service/utility, not on a Struts action.

A08-8 | MEDIUM | AdminSendMailAction.java:117–118 | **`java.util.regex.Pattern` compiled on every call instead of a static constant.** `isValidEmailAddress` compiles the regex pattern freshly on every invocation (line 117). The pattern is a fixed literal and should be compiled once as a `private static final Pattern` field. This is a needless performance cost on every email validation.

A08-9 | MEDIUM | AdminSendMailAction.java:117–118 | **Fully-qualified class references instead of imports.** `java.util.regex.Pattern` and `java.util.regex.Matcher` are referenced with full package paths inline rather than via `import` statements, which is inconsistent with the rest of the file's import style (lines 3–27 all use explicit imports).

A08-10 | MEDIUM | AdminSettingsAction.java:48 | **Unchecked `get(0)` on a list return value with no null/empty guard.** `dao.getCompanyContactsByCompId(...).get(0)` will throw `IndexOutOfBoundsException` if the company is not found or the list is empty. There is no defensive check before accessing index 0.

A08-11 | MEDIUM | AdminSettingsAction.java:53 | **`Integer.parseInt(timezone)` with no null/format guard.** `timezone` is read directly from the form at line 34 with no null-check. If the field is null or non-numeric, this throws `NumberFormatException` at runtime.

A08-12 | MEDIUM | AdminSettingsAction.java:59–61 | **Magic-string subscription/alert identifiers scattered in action code.** String literals `"alert"`, `"sms"`, `"RedImpactAlert"`, `"RedImpactSMS"`, `"DriverDenyAlert"` appear repeated six times across lines 59–77 with no constants defined. Any typo or rename requires touching multiple locations. These should be constants or an enum.

A08-13 | LOW | AdminSettingsAction.java:39–41 | **Inconsistent spacing around `==` operator in ternary expressions.** Line 39 has `getRedImpactSMSAlert()== null` (no space before `==`) and line 40 has `getDriverDenyAlert()== null` with a double space before the field name, while line 38 and line 30 use consistent `== null` spacing. Minor formatting inconsistency within the same file.

A08-14 | LOW | AdminSendMailAction.java:109 | **Trailing end-of-method comment `// End of sendMail() Method`.** This style of comment does not appear on any other method in either file; it is inconsistent and adds no information.

A08-15 | LOW | AdminSettingsAction.java:82 | **Trailing tab character on the final line.** Line 82 contains only a tab character after the closing brace, which is inconsistent with `AdminSendMailAction.java` and standard Java source formatting.

A08-16 | LOW | AdminSendMailAction.java:31 | **Mutable singleton DAO stored as an instance field on a Struts Action.** Struts actions may be instantiated once and reused across requests. Storing `driverDao` as an instance field is not thread-safe if `DriverDAO` maintains any mutable state. `AdminSettingsAction` uses `CompanyDAO.getInstance()` locally inside `execute` — the two files are inconsistent in this pattern.

A08-17 | LOW | AdminSendMailAction.java:41 | **`emailAdd` variable declared but redundant.** `emailAdd` is assigned from `sendMailForm.getEmail()` at line 41, but `sendMailForm.getEmail()` is also called again directly at line 47 for the validation check. Either use `emailAdd` consistently for both, or call the getter once. As written, `emailAdd` is only used at line 55, creating a subtle inconsistency.

A08-18 | INFO | AdminSendMailAction.java:6–12 | **`javax.mail` API in use (JavaEE / Jakarta EE legacy).** The code depends on `javax.mail`, which is the pre-Jakarta namespace. If the runtime is Jakarta EE 9+, this will fail at deployment. No build descriptor is visible in these files to confirm the target server version, but this is a known migration risk.

A08-19 | INFO | AdminSendMailAction.java:20–23 / AdminSettingsAction.java:12–15 | **Apache Struts 1 (`org.apache.struts.action.*`) in use.** Struts 1 reached end-of-life in December 2013 and has multiple unpatched CVEs. This is an architectural-level concern noted here for completeness; it applies across the entire codebase.
# P4 Agent A09 — AdminTrainingsAction, AdminUnitAccessAction

## Reading Evidence

### AdminTrainingsAction
- Class: `AdminTrainingsAction` extends `PandoraAction` (line 14)
- Methods:
  - `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` (line 17)
- Constants/Types: none defined in this file
- Instance fields: `private TrainingDAO trainingDAO` (line 15)

### AdminUnitAccessAction
- Class: `AdminUnitAccessAction` extends `PandoraAction` (line 15)
- Methods:
  - `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` (line 17)
- Constants/Types: none defined in this file
- Instance fields: none (DAO accessed via static methods only)

---

## Findings

A09-1 | HIGH | AdminTrainingsAction.java:15 | Concrete DAO instantiated as an instance field directly in the Action class (`private TrainingDAO trainingDAO = new TrainingDAO()`). `TrainingDAO` is used as an instance (non-singleton, non-static) object, while the sibling `AdminUnitAccessAction` calls `UnitDAO` entirely through static methods. Struts 1 Action classes are singletons shared across requests; holding a mutable DAO instance field is safe only if the DAO is stateless, but the inconsistency creates a leaky-abstraction coupling: the Action is tightly coupled to the concrete `TrainingDAO` class with no interface or injection boundary. Across the two files the DAO access pattern is directly contradictory: instance field vs. static calls.

A09-2 | HIGH | AdminUnitAccessAction.java:21 | `Integer.parseInt(sessCompId)` is called without a null/blank guard. On line 19, `sessCompId` is set to `""` (empty string) if the session attribute is null. A request arriving without a `sessCompId` session attribute will produce a `NumberFormatException` that propagates as an unhandled runtime exception. The parent class `PandoraAction` provides `getCompId(HttpSession)` precisely for safe session-attribute retrieval, but it is not used here.

A09-3 | HIGH | AdminUnitAccessAction.java:29 | `UnitDAO.getUnitById(accessForm.getId()).get(0)` performs an unchecked index-0 access on the returned list. If no unit is found for the given ID, the list will be empty and this line will throw an `IndexOutOfBoundsException`. There is no null/empty-list guard.

A09-4 | MEDIUM | AdminTrainingsAction.java:23 | Session attribute `sessDateFormat` is retrieved with a direct unchecked cast: `(String) session.getAttribute("sessDateFormat")`. If the attribute is absent, `session.getAttribute` returns `null`; the cast itself will not throw, but `dateFormat` will be `null` and will be forwarded to `TrainingDAO.addTraining(..., dateFormat)` and ultimately into `DateUtil.stringToSQLDate(...)` without any null check. The parent class provides `getSessionAttribute(session, name, defaultValue)` for exactly this pattern but is not used here.

A09-5 | MEDIUM | AdminTrainingsAction.java:17–43 | `execute` always returns `null` for every branch of the switch — including the `default` branch. Returning `null` from a Struts 1 `execute` method suppresses any forward navigation, which is intentional only for AJAX-style responses. There is no comment documenting this intent, and the `default` branch is unreachable dead code in the sense that it can never produce a different outcome than the existing `case` branches (all return `null`). If a new case were added that needed a forward, the silent `null` convention would be error-prone.

A09-6 | MEDIUM | AdminUnitAccessAction.java:20 | `getRequestParam(request, "action", (String) null)` is called to retrieve the `action` parameter, correctly using the inherited helper. However, `AdminTrainingsAction` (line 25) reads the same conceptual "action" discriminator via `trainingsForm.getAction()` — i.e., through the ActionForm — rather than a direct request parameter. The two files use two different strategies to obtain the action discriminator with no consistent pattern across the action layer.

A09-7 | LOW | AdminUnitAccessAction.java:8 | `import org.apache.struts.action.ActionMapping` is imported but the `mapping` parameter of `execute` is only used on line 36 (`mapping.findForward("success")`). This is correct usage. However, `AdminTrainingsAction` imports `ActionMapping` (line 7) and uses `mapping` as a parameter but never calls any method on it (all paths return `null`). The `mapping` parameter in `AdminTrainingsAction.execute` is effectively unused, which a compiler or static analyser will flag as a dead parameter contributing to unnecessary cognitive overhead.

A09-8 | LOW | AdminTrainingsAction.java:11 | `import javax.servlet.http.HttpServletResponse` is imported and declared as a method parameter but `response` is never used inside `execute`. This is a recurring pattern in the Struts 1 action layer (the framework mandates the signature), but in several sibling action classes the import is likewise present without usage, and no `@SuppressWarnings` or comment is provided to clarify the intent. Not a defect per se, but a consistent style gap across the codebase (same in `AdminUnitAccessAction.java:11`).

A09-9 | LOW | AdminUnitAccessAction.java:19 | The `sessCompId` value is read from the session twice: once on line 19 to obtain a `String`, and again implicitly via `Integer.parseInt(sessCompId)` on line 21. Meanwhile the `String` form (`sessCompId`) is also passed directly into `accessForm.getUnit(sessCompId)` on line 26, bypassing the already-parsed `int companyId`. This dual representation (String and int of the same value) is a style inconsistency and a maintenance hazard: if the parsing logic were to change, the two representations could diverge.

A09-10 | LOW | AdminTrainingsAction.java:14 | Lombok is used in `AdminTrainingsActionForm` (imported companion form class) but `AdminTrainingsAction` itself does not use Lombok, while `AdminUnitAccessAction` also does not. This is consistent between the two action files; however, `AdminTrainingsActionForm` uses `@Getter/@Setter/@Slf4j` while `AdminUnitAccessForm` uses `@Data/@NoArgsConstructor`. The form classes paired with these actions use inconsistent Lombok annotation strategies (`@Data` vs separate `@Getter/@Setter`), which is a cross-file style inconsistency visible when reading the two action files together.
# P4 Agent A10 — AdminUnitAction, AdminUnitAssignAction

## Reading Evidence

### AdminUnitAction

- Class: `AdminUnitAction extends Action` (line 24)
- Fields:
  - `unitDAO` (private, UnitDAO, line 25)
- Methods:
  - `execute` (line 27)
- Constants/Types: none defined

### AdminUnitAssignAction

- Class: `AdminUnitAssignAction extends PandoraAction` (line 18)
- Fields: none
- Methods:
  - `execute` (line 20)
  - `writeJsonResponse` (private, line 65)
- Constants/Types: none defined

---

## Findings

A10-1 | HIGH | AdminUnitAction.java:24 | `AdminUnitAction` extends the legacy Struts `Action` base class directly, while the sibling class `AdminUnitAssignAction` (line 18) extends the project's own `PandoraAction` abstraction. `PandoraAction` provides null-safe request-param helpers (`getRequestParam`, `getSessionAttribute`) and avoids the raw null-checks scattered throughout `AdminUnitAction`. The inconsistent base class means `AdminUnitAction` duplicates defensive coding that is already centralised in `PandoraAction`, and callers of the two action classes operate against different contracts.

A10-2 | HIGH | AdminUnitAction.java:150 | In the `"service"` branch, the outer `else` block (equipId is blank) calls `Double.parseDouble(bean.getHrsTilNext())` on a freshly constructed `ServiceBean` whose `hrsTilNext` field is `null` (no default is set in the bean). This will throw a `NullPointerException` at runtime whenever the `service` action is dispatched without an `equipId`. The equivalent inner `else` block at line 132 correctly guards with `if (bean.getHrsTilNext() != null)`, making the unguarded outer-else a direct runtime defect.

A10-3 | MEDIUM | AdminUnitAction.java:31-39 | Request and session parameters are extracted with inline ternary null-guards repeated for every parameter (`request.getParameter("x") == null ? "" : request.getParameter("x")`). This pattern calls `getParameter` twice per variable (wasteful and inconsistent: some variables use a local variable for the first call and some do not). `AdminUnitAssignAction` avoids this entirely via `PandoraAction.getRequestParam`. The code style is inconsistent across the two files and within `AdminUnitAction` itself.

A10-4 | MEDIUM | AdminUnitAction.java:59 | Inside the `"delete"` branch, `UnitDAO.getAllUnitsByCompanyId(companyId)` is called as a static method. At line 211, the same method is again called statically. However, at lines 45 and 65 the same DAO is used through the instance field `unitDAO`. Mixing static and instance calls on the same DAO class is a leaky abstraction: callers are exposed to the implementation detail of which operations happen to be static vs. instance, and the inconsistency makes the DAO contract harder to reason about.

A10-5 | MEDIUM | AdminUnitAction.java:63 | `JobsDAO` is instantiated with `new JobsDAO()` three separate times (lines 63, 78, 93) within the same request dispatch, rather than being stored as a class-level field analogous to `unitDAO` (line 25). This is inconsistent with the existing DAO field pattern and creates unnecessary object churn per request.

A10-6 | MEDIUM | AdminUnitAction.java:3 | Wildcard import `import com.bean.*` is used instead of explicit per-class imports. All other imports in the file are explicit (e.g., `com.dao.UnitDAO`, `com.util.DateUtil`). `AdminUnitAssignAction` uses only explicit imports. The wildcard makes it impossible to determine from the import section alone which bean classes are actually used, complicating dead-import analysis and IDE tooling.

A10-7 | MEDIUM | AdminUnitAction.java:185-187 | The `"assignment"` action stores data in the `HttpSession` (`session.setAttribute("arrCompanies", ...)` and `session.setAttribute("arrAssignments", ...)`) rather than in the request (`request.setAttribute`). Every other action branch in the same class (and in `AdminUnitAssignAction` line 60) uses `request.setAttribute`. Storing per-request data in the session leaks state across subsequent requests and is inconsistent with the rest of the codebase.

A10-8 | LOW | AdminUnitAction.java:36-38 | Local variables use snake_case names: `job_description`, `job_title`, `job_no`, `job_id`. All other local variables in both files use camelCase (e.g., `sessCompId`, `dateFormat`, `equipId`, `searchUnit`). This violates the Java naming convention and is inconsistent within the same method.

A10-9 | LOW | AdminUnitAction.java:14 | `import java.util.ArrayList` is present and used. However, the declared return types and field types elsewhere in the file use `List` (the interface). The `ArrayList` import is only needed at lines 52 and 64 where concrete `ArrayList` types are still used rather than `List`. Using the concrete type instead of the interface is a minor style inconsistency with other parts of the file and with `AdminUnitAssignAction` which declares `List` throughout.

A10-10 | LOW | AdminUnitAssignAction.java:14 | `import java.io.IOException` is present and used only in the signature of the private helper `writeJsonResponse` (line 65). This is correct and not dead, but worth noting that the helper performs two separate `response.getWriter()` calls (lines 66–67) — each call obtains a `PrintWriter` reference rather than caching the result of the first call. This is a minor inefficiency and a style inconsistency.

A10-11 | LOW | AdminUnitAssignAction.java:15 | `import java.util.Date` is imported and used at lines 32 and 37. The `Date` class (`java.util.Date`) is a deprecated legacy API since Java 8 (superseded by `java.time`). The usage is not immediately harmful but represents a build warning under `-Xlint:deprecation` and is inconsistent with modern Java date-handling practices.

A10-12 | INFO | AdminUnitAction.java:13-16 | The entire file is built on Apache Struts 1 (`org.apache.struts.action.*`). Struts 1 reached end-of-life in 2013 and is an unsupported, deprecated framework with known security vulnerabilities. This applies to both files; `AdminUnitAssignAction` also inherits through `PandoraAction extends Action`. No code-level fix is possible without a framework migration, but the dependency represents a project-level risk.
# Pass 4 (Code Quality) — Agent A100
**Audit date:** 2026-02-26
**Assigned files:**
- `src/main/java/com/service/DriverService.java`
- `src/main/java/com/service/DriverServiceException.java`
- `src/main/java/com/service/EntityNotFoundException.java`

---

## Reading Evidence

### 1. `DriverService.java`

**Module/Class:** `com.service.DriverService`

| Element | Kind | Line |
|---|---|---|
| `theInstance` | private static field (`DriverService`) | 12 |
| `driverUnitDAO` | private instance field (`DriverUnitDAO`) | 14 |
| `getInstance()` | public static method | 16 |
| `updateAssignedVehicle(DriverVehicleBean)` | public instance method | 25 |

**Annotations:** `@Slf4j` (Lombok) at class level (line 9)
**Throws declared:** `DriverServiceException` (checked-style declaration on a `RuntimeException` subclass)
**Dependencies:** `DriverUnitDAO`, `DriverVehicleBean`, `DriverServiceException`, `java.sql.SQLException`

---

### 2. `DriverServiceException.java`

**Module/Class:** `com.service.DriverServiceException` extends `RuntimeException`

| Element | Kind | Line |
|---|---|---|
| `DriverServiceException(String message)` | public constructor | 5 |
| `DriverServiceException(String message, Throwable cause)` | public constructor | 9 |

No constants, no fields beyond what `RuntimeException` supplies.

---

### 3. `EntityNotFoundException.java`

**Module/Class:** `com.service.EntityNotFoundException` extends `RuntimeException`

| Element | Kind | Line |
|---|---|---|
| `EntityNotFoundException(Class<T> clazz, String id)` | public generic constructor | 5 |

No constants or additional fields.
Message format: `"<fully-qualified-class-name> with ID <id> not found "` (note trailing space).

---

## Findings

### A100-1 | HIGH | DriverService.java:17-21 | Broken double-checked locking — singleton is not thread-safe

The `getInstance()` method uses a partial double-checked locking pattern but is broken:
the outer `if (theInstance == null)` check is not inside a second `if` inside the
`synchronized` block, and `theInstance` is not declared `volatile`. Under the Java
Memory Model, without `volatile`, the JIT can publish a partially-constructed object;
without the inner null-check, two threads that both pass the outer guard before either
acquires the lock will each create and overwrite `theInstance`.

Compare with the correctly-implemented `DriverUnitDAO.getInstance()` in the same
codebase (which has the double `if` and a private constructor):

```java
// DriverUnitDAO — correct
if (instance == null) {
    synchronized (DriverUnitDAO.class) {
        if (instance == null) {          // <-- inner check present
            instance = new DriverUnitDAO();
        }
    }
}
```

```java
// DriverService — broken (missing inner null-check, missing volatile)
if (theInstance == null) {
    synchronized (DriverService.class) {
        theInstance = new DriverService(); // always overwrites
    }
}
```

Fix: add `volatile` to `theInstance` and add an inner null-check, matching
`DriverUnitDAO`.

---

### A100-2 | HIGH | DriverService.java:16-23 | Style inconsistency — singleton pattern differs from sibling class `ReportService`

`ReportService` in the same package follows the same broken outer-only pattern as
`DriverService`, but `DriverUnitDAO` applies the correct double-check. There are now
two different singleton implementations in the service layer, neither of which is
safe. Both need to be unified to the safe idiom. Reported here as a style/consistency
finding because the specific concurrent-safety defect is covered by A100-1.

---

### A100-3 | MEDIUM | DriverService.java:25 | Redundant `throws DriverServiceException` on a `RuntimeException` method

`DriverServiceException` extends `RuntimeException` (unchecked). Declaring it in
`throws` is not a compiler error, but it is misleading: it implies to callers that
the exception is checked and must be handled. The call site in
`AdminDriverEditAction.java:183` does not catch it, relying on the Struts `Action`
layer to swallow unchecked exceptions through `throws Exception`. The declaration
should be removed to avoid leaking the false impression of checked-exception
semantics.

---

### A100-4 | MEDIUM | DriverService.java:29 | Leaky abstraction — SQL exception message includes internal DAO detail

The error message `"Unable to update assigned vehicle for driver " + driverVehicle.getId()`
is fine, but the underlying `SQLException` is passed as the cause of
`DriverServiceException`, which is then propagated all the way to the Struts action
layer (`AdminDriverEditAction`) uncaught. The SQL state and vendor error code from
`SQLException` are therefore accessible to any code (or framework) that catches
`DriverServiceException` and inspects its cause, exposing internal database
implementation details through the service interface.

---

### A100-5 | MEDIUM | DriverService.java:9 | Unused import / unused logger — `@Slf4j` declared but `log` never referenced

The class is annotated `@Slf4j`, which instructs Lombok to generate a `private static
final Logger log` field. However, there is no call to `log.warn(...)`,
`log.error(...)`, or any other log method anywhere in `DriverService`. The annotation
(and thus the generated field) is dead code. Either a log statement should be added
in the `catch` block (e.g., `log.error(...)`) or the annotation should be removed.

---

### A100-6 | MEDIUM | DriverServiceException.java:3 | Missing `serialVersionUID` on `Serializable` subclass

`DriverServiceException` extends `RuntimeException`, which implements
`java.io.Serializable`. The class does not declare a `private static final long
serialVersionUID`. This will produce a compiler/IDE warning (`-Xlint:serial`) and
means Java will compute a UID at runtime based on class structure. Any change to the
class (adding a field, renaming a method) will silently change the UID and break
deserialization of previously-serialized instances.

Same issue applies to `EntityNotFoundException` (see A100-7).

---

### A100-7 | MEDIUM | EntityNotFoundException.java:3 | Missing `serialVersionUID` on `Serializable` subclass

Same root cause as A100-6. `EntityNotFoundException` extends `RuntimeException` and
declares no `serialVersionUID`.

---

### A100-8 | LOW | EntityNotFoundException.java:5 | Unnecessary generic type parameter `<T>` on constructor

The constructor `public <T> EntityNotFoundException(Class<T> clazz, String id)` uses
a generic type parameter `<T>` solely to type the `clazz` parameter. The generic
bound is not used in the constructor body (only `clazz.getName()` is called, which is
available on the raw `Class` type). Using `Class<?>` instead of `Class<T>` with a
free type parameter would be idiomatic, avoids an unchecked/unused type variable, and
removes a potential source of javac warnings at call sites.

---

### A100-9 | LOW | EntityNotFoundException.java:6 | Trailing space in exception message

The message template ends with `"not found "` (a trailing space after "found"). This
is a cosmetic defect that will appear in all log output, stack traces, and any UI
messages derived from the exception.

```java
super(clazz.getName() + " with ID " + id + " not found ");
//                                                       ^--- trailing space
```

---

### A100-10 | LOW | EntityNotFoundException.java:6 | `clazz.getName()` returns fully-qualified name, leaking internal package structure

`Class.getName()` returns the fully-qualified class name (e.g.,
`com.bean.DriverBean`). This exposes the internal package hierarchy in any exception
message that reaches a log file or is surfaced to a UI/API consumer.
`clazz.getSimpleName()` would give a cleaner, package-agnostic name
(e.g., `DriverBean`) that is consistent with how the class is referenced in
user-facing error messages elsewhere in the codebase.

---

### A100-11 | LOW | EntityNotFoundException.java:5 | Single-constructor exception class lacks `(String message)` and `(String message, Throwable cause)` constructors

`EntityNotFoundException` exposes only one constructor (the typed `(Class<T>, String)`
form). Standard Java exception convention (and the pattern used in the sibling class
`DriverServiceException`) is to also provide a plain `(String message)` and a
`(String message, Throwable cause)` constructor so callers have flexibility. As
written, callers are forced to pass a `Class` token regardless of context, creating
unnecessary coupling to the generic-constructor API.

---

### A100-12 | INFO | DriverService.java:12,14 | Field declaration order — static field follows instance field pattern used in `ReportService`

`ReportService` declares `private static ReportService theInstance` after its instance
DAO fields (lines 18 vs. 15-17). `DriverService` declares the static field first
(line 12) and the instance field second (line 14). Neither ordering is wrong, but the
inconsistency across the two singleton services in the same package is a minor style
issue that should be made uniform per the project's coding standards.

---

## Summary

| ID | Severity | File | Short description |
|---|---|---|---|
| A100-1 | HIGH | DriverService.java:17-21 | Broken double-checked locking / no `volatile` |
| A100-2 | HIGH | DriverService.java:16-23 | Inconsistent singleton pattern vs. `DriverUnitDAO` |
| A100-3 | MEDIUM | DriverService.java:25 | Superfluous `throws` on unchecked exception |
| A100-4 | MEDIUM | DriverService.java:29 | SQL cause leaks through service boundary |
| A100-5 | MEDIUM | DriverService.java:9 | `@Slf4j` declared but `log` never used |
| A100-6 | MEDIUM | DriverServiceException.java:3 | Missing `serialVersionUID` |
| A100-7 | MEDIUM | EntityNotFoundException.java:3 | Missing `serialVersionUID` |
| A100-8 | LOW | EntityNotFoundException.java:5 | Unnecessary free type parameter `<T>` on constructor |
| A100-9 | LOW | EntityNotFoundException.java:6 | Trailing space in exception message |
| A100-10 | LOW | EntityNotFoundException.java:6 | `getName()` exposes fully-qualified class name |
| A100-11 | LOW | EntityNotFoundException.java:5 | Missing standard exception constructors |
| A100-12 | INFO | DriverService.java:12,14 | Field declaration order inconsistent with `ReportService` |
# Pass 4 Code Quality — Agent A101
**Date:** 2026-02-26
**Assigned files:**
- `src/main/java/com/service/ReportService.java`
- `src/main/java/com/service/ReportServiceException.java`
- `src/main/java/com/service/RestClientService.java`

---

## Reading Evidence

### ReportService.java

**Class:** `com.service.ReportService`
**Annotations:** `@Slf4j` (Lombok)

**Methods:**
| Method | Line |
|--------|------|
| `getInstance()` (static) | 20 |
| `ReportService()` (private constructor) | 29 |
| `countPreOpsCompletedToday(Long compId, String timezone)` | 32 |
| `getPreOpsCheckReport(Long compId, PreOpsReportFilterBean filter, String dateFormat, String timezone)` | 41 |
| `getIncidentReport(int compId, IncidentReportFilterBean filter, String dateFormat, String timezone)` | 53 |
| `countImpactsToday(Long compId, String timezone)` | 65 |
| `getImpactReport(Long compId, ImpactReportFilterBean filter, String dateFormat, String timezone)` | 76 |
| `getSessionReport(int compId, SessionFilterBean filter, String dateFormat, String timezone)` | 90 |

**Fields:**
| Field | Line |
|-------|------|
| `private ResultDAO resultDAO` | 15 |
| `private IncidentReportDAO incidentReportDAO` | 16 |
| `private ImpactReportDAO impactReportDAO` | 17 |
| `private static ReportService theInstance` | 18 |

**Imports:**
- `com.bean.*` (wildcard)
- `com.dao.ImpactReportDAO`
- `com.dao.IncidentReportDAO`
- `com.dao.ResultDAO`
- `com.dao.SessionDAO`
- `com.util.DateUtil`
- `lombok.extern.slf4j.Slf4j`
- `java.sql.SQLException`

**Checked exceptions declared:** `ReportServiceException` on most methods.

---

### ReportServiceException.java

**Class:** `com.service.ReportServiceException extends RuntimeException`

**Methods:**
| Method | Line |
|--------|------|
| `ReportServiceException(String message)` | 4 |
| `ReportServiceException(String message, Throwable cause)` | 8 |

**No fields, no constants, no type parameters.**

---

### RestClientService.java

**Class:** `com.service.RestClientService`

**Fields / Constants:**
| Name | Line |
|------|------|
| `private static Logger log` | 33 |
| `private final String COGNITO_API_PORT = "9090"` | 35 |

**Methods:**
| Method | Line |
|--------|------|
| `authenticationRequest(AuthenticationRequest)` | 37 |
| `signUpRequest(UserSignUpRequest)` | 72 |
| `resetPassword(PasswordRequest)` | 107 |
| `confirmResetPassword(PasswordRequest)` | 142 |
| `getUser(String username, String accessToken)` | 177 |
| `getUserList(List<UserRequest> userRequestList, String accessToken)` | 213 |
| `updateUser(UserUpdateRequest)` | 250 |
| `deleteUser(String username, String sessionToken)` | 284 |

**Imports:**
- `java.net.URI`
- `java.net.URLEncoder`
- `java.util.ArrayList`
- `java.util.Arrays`
- `java.util.List`
- `org.apache.log4j.Logger`
- Various Spring `org.springframework.http.*`
- `org.springframework.web.client.RestTemplate`
- Various `com.cognito.bean.*`
- `com.util.InfoLogger`

---

## Findings

### ReportService.java

**A101-1 | HIGH | ReportService.java:20-27 | Broken double-checked locking (race condition in singleton)**

The `getInstance()` method checks `theInstance == null` outside the `synchronized` block, but re-assigns inside it without a second null-check. This is the classic broken double-checked locking pattern — two threads can both pass the outer null-check, then one initialises the instance and exits the lock, but the second thread immediately overwrites it with a fresh instance. The field is also not `volatile`, so the partially-constructed object hazard applies on JVMs with relaxed memory models.

```java
// Line 20-27 — missing inner null-check and volatile keyword
public static ReportService getInstance() {
    if (theInstance == null) {
        synchronized (ReportService.class) {
            theInstance = new ReportService();   // no second null-check
        }
    }
    return theInstance;
}
```

---

**A101-2 | MEDIUM | ReportService.java:15-17 | Mixed instantiation strategies for DAO fields**

`resultDAO` and `incidentReportDAO` are created with `new` (line 15–16), while `impactReportDAO` is obtained via `ImpactReportDAO.getInstance()` (line 17). There is no consistent pattern. This makes the class harder to test (dependencies are hardcoded) and hides the fact that `ImpactReportDAO` is itself a singleton while the others are not.

---

**A101-3 | MEDIUM | ReportService.java:8 | Unused import: `com.util.DateUtil`**

`DateUtil` is imported but never referenced anywhere in the file. This is dead import / dead code.

---

**A101-4 | MEDIUM | ReportService.java:3 | Wildcard import `com.bean.*`**

Wildcard imports obscure which types are actually used, can cause ambiguity collisions, and are a style violation in most Java coding standards. Specific imports should be used.

---

**A101-5 | MEDIUM | ReportService.java:90-99 | `getSessionReport` silently swallows checked exception contract — missing `throws` declaration**

Every other `get*` method in this class declares `throws ReportServiceException`. `getSessionReport` catches `SQLException` internally and rethrows it as `ReportServiceException` (line 97), but the method signature at line 90 does not declare `throws ReportServiceException`. Because `ReportServiceException extends RuntimeException`, this compiles, but it breaks the consistency contract of the class — callers of `getSessionReport` get no compiler warning that the call can throw, while callers of all other methods do.

---

**A101-6 | MEDIUM | ReportService.java:53 | Parameter type inconsistency: `getIncidentReport` uses `int compId` while all other methods use `Long compId`**

`countPreOpsCompletedToday`, `getPreOpsCheckReport`, `countImpactsToday`, and `getImpactReport` all accept `Long compId`. `getIncidentReport` (line 53) and `getSessionReport` (line 90) accept `int compId`. This is an inconsistent API that forces callers to cast or unbox and risks `NullPointerException` if a boxed `Long` is passed where `int` is expected in surrounding code.

---

**A101-7 | LOW | ReportService.java:67,81 | `assert` used for parameter validation in production code**

Lines 67 and 81 use Java `assert` statements to validate that `compId != null`. Java assertions are disabled by default at runtime unless the JVM is started with `-ea`. This means the null-check never fires in production. Proper null-checks (e.g., `Objects.requireNonNull`) should be used instead, or the validation should be removed. Note also that the other three methods perform no null-check at all, creating further inconsistency.

---

**A101-8 | LOW | ReportService.java:97 | Wrong error message copy-paste in `getSessionReport`**

The exception message on line 97 reads `"Unable to get impact report for compId : "`, which is copied verbatim from the impact-report methods. The method is `getSessionReport`, so the message should reference session data, not impact data. This misleads operators diagnosing errors.

---

**A101-9 | LOW | ReportService.java:13 | `@Slf4j` logger declared but never used**

The `@Slf4j` annotation (line 13) injects a `log` field via Lombok. The field is never referenced anywhere in the class body. All exception handling is done by rethrowing; no log statements exist. The annotation should be removed or log statements added at appropriate points.

---

### ReportServiceException.java

No findings. The class is minimal, correct, and follows standard exception conventions. `serialVersionUID` is absent (which would normally be a LOW/INFO finding about `serializable` warning), but as the class extends `RuntimeException` and is unlikely to be serialized, this is not flagged.

---

### RestClientService.java

**A101-10 | HIGH | RestClientService.java:297 | Deprecated `URLEncoder.encode(String)` used — encoding charset not specified**

`URLEncoder.encode(username)` at line 297 calls the single-argument overload, which is deprecated since Java 1.4 because it uses the platform's default encoding. If the platform encoding is not UTF-8 (e.g., on some Windows environments), special characters in usernames will be silently mis-encoded, producing corrupted URLs and failed deletes. The two-argument overload with explicit `"UTF-8"` (or `StandardCharsets.UTF_8` in Java 10+) must be used.

---

**A101-11 | HIGH | RestClientService.java:192-193 | Query parameters appended unsanitised to URL string — `accessToken` and `username` not URL-encoded in `getUser`**

In `getUser` (line 192), `username` and `accessToken` are concatenated directly into the URL string without encoding. If either value contains characters such as `+`, `&`, `=`, `#`, or spaces, the constructed URI will be malformed or the parameters will be silently truncated. Only `deleteUser` (line 297) encodes `username`, and even that does not encode `sessionToken`. `getUserList` (line 228) and other methods have the same pattern for `accessToken`.

---

**A101-12 | HIGH | RestClientService.java:308 | `deleteUser` always returns `"Deleted"` regardless of success or failure**

When the underlying `restTemplate.delete(uri)` call throws an exception (line 301), the catch block logs the error but the method still returns the string `"Deleted"` (line 308). The caller has no way to distinguish a successful deletion from a network failure or a 404/500 response. The return value is semantically meaningless.

---

**A101-13 | MEDIUM | RestClientService.java:33 | Logging framework inconsistency — `org.apache.log4j.Logger` used instead of SLF4J**

`ReportService.java` uses Lombok's `@Slf4j` (SLF4J). `RestClientService.java` uses `org.apache.log4j.Logger` directly (line 33), obtained through a custom `InfoLogger` wrapper. Mixing two logging frameworks in the same package is a style and maintainability problem. All classes should use the same abstraction (SLF4J).

---

**A101-14 | MEDIUM | RestClientService.java:35 | `COGNITO_API_PORT` should be `static final` (constant) not an instance `final` field**

The field `private final String COGNITO_API_PORT = "9090"` (line 35) is a compile-time constant. By convention and for efficiency, it should be `private static final`. As written, a new `String` field is allocated for every instance of the class. The name also follows `UPPER_SNAKE_CASE`, which in Java convention signals a `static final` constant — the missing `static` modifier violates that convention's expectation.

---

**A101-15 | MEDIUM | RestClientService.java:37-310 | Pervasive code duplication — header-building block repeated in every method**

The following four-line block appears verbatim (or near-verbatim) in all eight methods:

```java
ArrayList<MediaType> acceptableMediaTypes = new ArrayList<MediaType>();
acceptableMediaTypes.add(MediaType.APPLICATION_JSON);
HttpHeaders headers = new HttpHeaders();
headers.setAccept(acceptableMediaTypes);
```

This is copy-pasted eight times across the class. Any change to header construction (e.g., adding an `Authorization` header) must be made in eight places, which is a maintenance and consistency hazard.

---

**A101-16 | MEDIUM | RestClientService.java:37-310 | `RestTemplate` instantiated inside every method — no instance reuse**

A new `RestTemplate` is constructed on every method call (e.g., lines 41, 76, 111, 146, 180, 216, 253, 287). `RestTemplate` is designed to be a shared, thread-safe, reusable component. Creating a fresh instance per call bypasses connection pooling and increases GC pressure.

---

**A101-17 | MEDIUM | RestClientService.java:65,100,135,170,205,244,278,304 | `e.printStackTrace()` used instead of logging the exception to the logger**

All eight catch blocks call `e.printStackTrace()` before logging the message. `printStackTrace()` writes to `System.err`, bypassing the configured logging framework entirely. In a server environment the stack trace may appear in a different output stream from the structured log, making correlation difficult. The exception object should be passed as a second argument to `log.error(...)` instead.

---

**A101-18 | MEDIUM | RestClientService.java:39,74,109,144,179,215,252,286 | `method` variable assigned via `this.getClass().getName()` — verbose and allocates a new String per call**

Each method opens with:
```java
String method = this.getClass().getName() + " : <methodName> ";
```
`this.getClass().getName()` performs a reflective lookup and string concatenation on every call. Using the statically known class name string literal (or SLF4J's MDC) is the conventional approach.

---

**A101-19 | LOW | RestClientService.java:54,57,61 (and all similar blocks) | HTTP status comparison uses `==` on `HttpStatus` enum — style note, though currently safe**

Lines such as `if(HttpStatus.OK == result.getStatusCode())` use identity comparison `==` on `HttpStatus`. While this is safe for Spring's `HttpStatus` enum values, the idiomatic form is `result.getStatusCode().equals(HttpStatus.OK)` or `result.getStatusCode() == HttpStatus.OK` (since it is an enum). More importantly, only `200 OK` is treated as success; no other 2xx codes (e.g., `201 Created`, `204 No Content`) are handled, which could silently produce empty/default responses.

---

**A101-20 | LOW | RestClientService.java:57,92,127,162,197,234,269 | Misspelling "Succuss" in log messages**

All success log messages read `"HttpStatus Succuss"` (double-s). The correct spelling is "Success". This appears in every method except `updateUser` (line 269) which reads `"HttpStatus Success"` — itself inconsistent spelling with the rest of the file.

---

**A101-21 | LOW | RestClientService.java:207 | Wrong method name in error log in `getUser`**

Inside the `getUser` catch block (line 207), the error is logged as:
```java
log.error("authenticationRequest error:"+ e.getMessage());
```
The method name prefix should be `method` (which is `"... : getUser "`), not a hardcoded `"authenticationRequest error:"`. This is a copy-paste leftover from `authenticationRequest`.

---

**A101-22 | LOW | RestClientService.java:31 | Class has no singleton or Spring bean management — instantiation not controlled**

`RestClientService` has no `private` constructor, no singleton guard, and no Spring `@Service`/`@Component` annotation. Any caller can create multiple instances (`new RestClientService()`), each of which will spin up its own `RestTemplate` instances. This is inconsistent with `ReportService`, which enforces a singleton, and with the Spring context assumed by the use of Spring's `RestTemplate` and `HttpHeaders`.

---

**A101-23 | INFO | RestClientService.java:35 | Hardcoded port `9090` for Cognito API — not configurable**

The Cognito service port is hardcoded as `"9090"`. If this service is deployed in environments where the port differs, the class must be recompiled. This value should be injected via Spring `@Value` or an application properties entry.

---

**A101-24 | INFO | RestClientService.java:88,123,158 | URL path segments use mixed capitalisation (`/auth/SignUp`, `/auth/ResetPassword`, `/auth/ConfirmResetPassword`)**

Some URL paths use PascalCase segments (`SignUp`, `ResetPassword`, `ConfirmResetPassword`) while others use lowercase (`/auth`, `/auth/update`, `/auth/user`, `/auth/user-list`, `/auth/delete_user`). This is an inconsistent URL naming style, though whether this is a client or server defect depends on the downstream API.
# Pass 4 (Code Quality) — Agent A102
**Audit date:** 2026-02-26
**Files assigned:**
- `src/main/java/com/util/BarCode.java`
- `src/main/java/com/util/BeanComparator.java`
- `src/main/java/com/util/CharsetEncodingFilter.java`

---

## Reading Evidence

### 1. `com/util/BarCode.java`

**Class:** `BarCode` (public, non-generic)

**Constants (public static final String):**

| Name | Line | Value |
|---|---|---|
| `BARCODE_MSG` | 32 | `"msg"` |
| `BARCODE_TYPE` | 34 | `"type"` |
| `BARCODE_HEIGHT` | 36 | `"height"` |
| `BARCODE_MODULE_WIDTH` | 38 | `"mw"` |
| `BARCODE_WIDE_FACTOR` | 40 | `"wf"` |
| `BARCODE_QUIET_ZONE` | 42 | `"qz"` |
| `BARCODE_HUMAN_READABLE_POS` | 44 | `"hrp"` |
| `BARCODE_FORMAT` | 46 | `"fmt"` |
| `BARCODE_IMAGE_RESOLUTION` | 48 | `"res"` |
| `BARCODE_IMAGE_GRAYSCALE` | 50 | `"gray"` |
| `BARCODE_HUMAN_READABLE_SIZE` | 52 | `"hrsize"` |
| `BARCODE_HUMAN_READABLE_FONT` | 54 | `"hrfont"` |
| `BARCODE_HUMAN_READABLE_PATTERN` | 56 | `"hrpattern"` |

**Fields:**

| Name | Line | Type | Visibility |
|---|---|---|---|
| `log` | 30 | `Logger` | private static |

**Methods:**

| Name | Line | Visibility |
|---|---|---|
| `genBarCode(HttpServletRequest, String)` | 58 | public |
| `determineFormat(HttpServletRequest)` | 145 | protected |
| `buildCfg(HttpServletRequest)` | 162 | protected |

**Imports (unused):**
- `java.io.File` — used (line 124)
- `java.io.OutputStream` — used (line 124)
- `java.io.StringWriter` — **NOT used anywhere in the file**
- `javax.xml.transform.dom.DOMSource` — imported twice: once via wildcard-style qualified name inline at line 83 (`javax.xml.transform.dom.DOMSource`) AND as a named import at line 14
- `javax.xml.transform.stream.StreamResult` — same double-import pattern at lines 15 and 84

---

### 2. `com/util/BeanComparator.java`

**Class:** `BeanComparator` (public, implements raw `Comparator`)

**Constants:**

| Name | Line | Type | Visibility |
|---|---|---|---|
| `EMPTY_CLASS_ARRAY` | 22 | `Class[]` | private static final |
| `EMPTY_OBJECT_ARRAY` | 23 | `Object[]` | private static final |

**Fields:**

| Name | Line | Type | Visibility |
|---|---|---|---|
| `method` | 25 | `Method` | private |
| `isAscending` | 26 | `boolean` | private |
| `isIgnoreCase` | 27 | `boolean` | private |
| `isNullsLast` | 28 | `boolean` | private |

**Methods:**

| Name | Line | Visibility |
|---|---|---|
| `BeanComparator(Class<?>, String)` | 34 | public constructor |
| `BeanComparator(Class<?>, String, boolean)` | 42 | public constructor |
| `BeanComparator(Class<?>, String, boolean, boolean)` | 51 | public constructor |
| `setAscending(boolean)` | 82 | public |
| `setIgnoreCase(boolean)` | 90 | public |
| `setNullsLast(boolean)` | 98 | public |
| `compare(Object, Object)` | 107 | public |

---

### 3. `com/util/CharsetEncodingFilter.java`

**Class:** `CharsetEncodingFilter` (public, implements `Filter`)

**Fields:**

| Name | Line | Type | Visibility |
|---|---|---|---|
| `config` | 7 | `FilterConfig` | private |
| `defaultEncode` | 8 | `String` | private |

**Methods:**

| Name | Line | Visibility |
|---|---|---|
| `init(FilterConfig)` | 10 | public |
| `destroy()` | 16 | public |
| `doFilter(ServletRequest, ServletResponse, FilterChain)` | 19 | public |

---

## Findings

### BarCode.java

**A102-1 | HIGH | BarCode.java:137-138 | Swallowed exception with redundant printStackTrace after log.error**

At lines 135-141 two catch blocks each call both `log.error(...)` and `e.printStackTrace()` / `t.printStackTrace()`. `printStackTrace()` writes to `stderr` and is redundant when a logging framework is already used. More critically, the exception is silently swallowed after logging — `genBarCode` returns an empty string as if the barcode was successfully generated. Callers have no way to distinguish a normal empty result from a failure.

```java
} catch (Exception e) {
    log.error("Error while generating barcode", e);
    e.printStackTrace();          // redundant and leaks to stderr
} catch (Throwable t) {
    log.error("Error while generating barcode", t);
    t.printStackTrace();          // redundant and leaks to stderr
}
return bout.toString();           // always returns, even on failure
```

**A102-2 | HIGH | BarCode.java:123-124 | Hard-coded filesystem path constructed via reflection-based code-source location**

The output file path is assembled by combining the runtime class-source location with a relative traversal (`/../../../../../images/barcode/`). This is fragile, environment-dependent, and a security concern: input from the request (the barcode message content) is used to build the file name without sanitisation beyond the small strip logic at lines 107-121. A crafted message with path-traversal characters (e.g. `../`) remaining after stripping could write files outside the intended directory.

```java
String curerntDir = getClass().getProtectionDomain().getCodeSource().getLocation().getPath();
OutputStream out = new java.io.FileOutputStream(
    new File(curerntDir + "/../../../../../images/barcode/" + img + ".png"));
```

**A102-3 | HIGH | BarCode.java:124 | FileOutputStream is never closed — resource leak**

The `OutputStream out` opened at line 124 is passed to `BitmapCanvasProvider` but is never closed or wrapped in a try-with-resources block. The enclosing `finally` only closes `bout` (the `ByteArrayOutputStream`). If `provider.finish()` or `generateBarcode()` throws, `out` leaks a file handle.

**A102-4 | MEDIUM | BarCode.java:83-84 | Redundant fully-qualified class references duplicate existing imports**

`javax.xml.transform.dom.DOMSource` and `javax.xml.transform.stream.StreamResult` are already imported at lines 14-15, yet they are used with their full package path again at lines 83-84. This is inconsistent and could cause confusion.

```java
Source src = new javax.xml.transform.dom.DOMSource(frag);   // line 83
Result res = new javax.xml.transform.stream.StreamResult(bout); // line 84
```

**A102-5 | MEDIUM | BarCode.java:7 | Unused import: `java.io.StringWriter`**

`StringWriter` is imported but never referenced anywhere in the file.

**A102-6 | MEDIUM | BarCode.java:63 | Variable `orientation` is always 0 — effectively a dead constant**

`orientation` is declared as `int orientation = 0` at line 63 and is never modified or derived from any request parameter before being passed to `SVGCanvasProvider`, `EPSCanvasProvider`, and `BitmapCanvasProvider`. There is a constant `BARCODE_IMAGE_GRAYSCALE` defined for grayscale images but grayscale is also never read from the request — it is hardcoded as `BufferedImage.TYPE_BYTE_GRAY` at line 126. This suggests an incomplete implementation.

**A102-7 | MEDIUM | BarCode.java:50 | Declared constant `BARCODE_IMAGE_GRAYSCALE` is never used**

`BARCODE_IMAGE_GRAYSCALE` ("gray") is defined at line 50 but is never read via `request.getParameter(BARCODE_IMAGE_GRAYSCALE)` in `buildCfg` or `genBarCode`. The grayscale flag is hardcoded at line 126 (`BufferedImage.TYPE_BYTE_GRAY`), making this constant dead code.

**A102-8 | MEDIUM | BarCode.java:159 | Javadoc typo in `buildCfg`: "COnfiguration" (capital O)**

Line 159 contains `@return the newly built COnfiguration object` — mid-word capital O is a typo.

**A102-9 | LOW | BarCode.java:123 | Typo in variable name: `curerntDir` (should be `currentDir`)**

```java
String curerntDir = getClass().getProtectionDomain()...
```
`curerntDir` is a misspelling of `currentDir`.

**A102-10 | LOW | BarCode.java:58 | Inconsistent brace style: method opening brace on new line**

The `genBarCode` method (line 59) opens its brace on the same line as the signature, but the internal `try` block at line 61 has its brace on the same line while `buildCfg`'s internal logic places braces consistently. Minor, but the overall file mixes K&R and Allman brace styles.

**A102-11 | LOW | BarCode.java:160 | `@todo` annotation in Javadoc is non-standard**

Line 160: `* @todo Change to bean API` — `@todo` is not a standard Javadoc tag. Should use `// TODO:` in code or be tracked in an issue tracker.

**A102-12 | INFO | BarCode.java:17-18 | Dependency on end-of-life Apache Avalon framework**

`org.apache.avalon.framework.configuration.Configuration` and `DefaultConfiguration` are from the Apache Avalon project, which has been retired. This is a build/dependency-level concern but worth flagging for future maintainability.

---

### BeanComparator.java

**A102-13 | HIGH | BeanComparator.java:20 | Class implements raw `Comparator` without type parameter**

`public class BeanComparator implements Comparator` uses the raw type. This generates an unchecked warning and bypasses compile-time type safety. It should implement `Comparator<Object>` at minimum, or ideally `Comparator<T>` with a generic type parameter.

**A102-14 | HIGH | BeanComparator.java:164 | Raw type `Comparable` used in cast — generates unchecked warning**

At line 164, `((Comparable)c1).compareTo(c2)` uses the raw `Comparable` type. This should be `((Comparable<Object>)c1).compareTo(c2)` or restructured to avoid the unchecked cast.

```java
return ((Comparable)c1).compareTo(c2);  // raw type, unchecked cast
```

**A102-15 | MEDIUM | BeanComparator.java:70 | Raw type `Class` used for `returnClass`**

Line 70: `Class returnClass = method.getReturnType();` uses the raw `Class` type. Should be `Class<?>`.

**A102-16 | MEDIUM | BeanComparator.java:22-23 | Constants `EMPTY_CLASS_ARRAY` and `EMPTY_OBJECT_ARRAY` use raw array types with raw `Class`**

Line 22: `private static final Class[] EMPTY_CLASS_ARRAY` — `Class` should be `Class<?>[]`. These are passed to `getMethod` and `invoke` respectively, contributing to the unchecked warning surface.

**A102-17 | MEDIUM | BeanComparator.java:104 | Javadoc comment at line 104 is incorrect**

The comment at lines 103-105 reads `/* Implement the Comparable interface */`. The class implements `Comparator`, not `Comparable`. These are different interfaces. `Comparable` is for natural ordering of a class on itself; `Comparator` is an external comparison strategy.

**A102-18 | MEDIUM | BeanComparator.java:4-5 | Wildcard imports used**

Lines 4-5 use `import java.lang.reflect.*;` and `import java.util.*;`. Only `Method` from `reflect` and `Comparator` from `util` are actually needed. Wildcard imports hide what is actually used and can cause ambiguity in large codebases.

**A102-19 | LOW | BeanComparator.java:31-33 | Constructor comments use `/* */` block style instead of `/** */` Javadoc style**

The constructor comments (lines 31-33, 39-41, 47-50) use `/* */` style instead of `/** */`. They will not appear in generated Javadoc. The setter comments (lines 79-81, 87-89, 95-97, 103-105) have the same issue.

---

### CharsetEncodingFilter.java

**A102-20 | MEDIUM | CharsetEncodingFilter.java:7 | Field `config` is stored in `init()` but never read after that**

`this.config = config` is set at line 11 and cleared at line 17 (`destroy()`), but `config` is never read in `doFilter` or any helper method. The field is effectively unused during the filter's active lifetime, suggesting the implementation is incomplete (e.g. the charset init parameter is read once at startup and cached in `defaultEncode`, but `config` itself serves no further purpose and storing it is misleading).

**A102-21 | MEDIUM | CharsetEncodingFilter.java:21 | Pointless local variable `srequest` is an alias for `request`**

```java
ServletRequest srequest = request;
srequest.setCharacterEncoding(defaultEncode);
chain.doFilter(srequest, response);
```

`srequest` is assigned the same reference as `request` and is never cast or modified. The assignment is dead code; `request` could be used directly. This is likely a leftover from a previous version that performed a cast.

**A102-22 | LOW | CharsetEncodingFilter.java:3-4 | Wildcard imports used**

`import java.io.*` and `import javax.servlet.*` are wildcard imports. From `java.io` only `IOException` is needed; from `javax.servlet` only `Filter`, `FilterConfig`, `FilterChain`, `ServletRequest`, `ServletResponse`, and `ServletException` are needed.

**A102-23 | LOW | CharsetEncodingFilter.java:12-13 | Missing space around `!=` operator and before `{` brace**

```java
if(config.getInitParameter("Charset")!=null){
    defaultEncode=config.getInitParameter("Charset");
```
Both lines omit spaces around the `!=` operator, around the `=` assignment operator, and before the opening `{`. This is inconsistent with standard Java style.

---

## Summary Table

| ID | Severity | File | Line | Short Description |
|---|---|---|---|---|
| A102-1 | HIGH | BarCode.java | 135-141 | Exceptions swallowed; redundant printStackTrace alongside logger |
| A102-2 | HIGH | BarCode.java | 123-124 | Unsanitised user input used in file path construction |
| A102-3 | HIGH | BarCode.java | 124 | FileOutputStream never closed — resource leak |
| A102-4 | MEDIUM | BarCode.java | 83-84 | Redundant fully-qualified names duplicate existing imports |
| A102-5 | MEDIUM | BarCode.java | 7 | Unused import: java.io.StringWriter |
| A102-6 | MEDIUM | BarCode.java | 63 | orientation always 0; grayscale hardcoded — incomplete parameterisation |
| A102-7 | MEDIUM | BarCode.java | 50 | BARCODE_IMAGE_GRAYSCALE constant defined but never used |
| A102-8 | MEDIUM | BarCode.java | 159 | Javadoc typo: "COnfiguration" |
| A102-9 | LOW | BarCode.java | 123 | Variable name typo: curerntDir |
| A102-10 | LOW | BarCode.java | 58 | Inconsistent brace style (K&R vs Allman) |
| A102-11 | LOW | BarCode.java | 160 | Non-standard @todo Javadoc tag |
| A102-12 | INFO | BarCode.java | 17-18 | Dependency on retired Apache Avalon framework |
| A102-13 | HIGH | BeanComparator.java | 20 | Raw Comparator type — missing generic type parameter |
| A102-14 | HIGH | BeanComparator.java | 164 | Raw Comparable cast — unchecked warning |
| A102-15 | MEDIUM | BeanComparator.java | 70 | Raw Class type — should be Class<?> |
| A102-16 | MEDIUM | BeanComparator.java | 22-23 | Raw Class[] array constants |
| A102-17 | MEDIUM | BeanComparator.java | 104 | Comment says "Comparable interface" — class implements Comparator |
| A102-18 | MEDIUM | BeanComparator.java | 4-5 | Wildcard imports |
| A102-19 | LOW | BeanComparator.java | 31-50 | Constructor/setter comments use /* */ instead of /** */ Javadoc style |
| A102-20 | MEDIUM | CharsetEncodingFilter.java | 7 | Field config stored but never read after init |
| A102-21 | MEDIUM | CharsetEncodingFilter.java | 21 | Pointless alias variable srequest — dead code |
| A102-22 | LOW | CharsetEncodingFilter.java | 3-4 | Wildcard imports |
| A102-23 | LOW | CharsetEncodingFilter.java | 12-13 | Missing spaces around operators and before brace |
# Pass 4 – Code Quality | Agent A103
**Date:** 2026-02-26
**Codebase:** forkliftiqadmin
**Assigned files:**
- `src/main/java/com/util/CompanySessionSwitcher.java`
- `src/main/java/com/util/DBUtil.java`
- `src/main/java/com/util/DateUtil.java`

---

## Reading Evidence

### 1. CompanySessionSwitcher.java

**Class:** `com.util.CompanySessionSwitcher`

**Methods:**

| Method | Line |
|--------|------|
| `public static void UpdateCompanySessionAttributes(CompanyBean, HttpServletRequest, HttpSession)` | 17 |

**Types defined:** None
**Constants defined:** None
**Imports used:** `CompanyBean`, `TimezoneBean`, `CompanyDAO`, `DriverDAO`, `LoginDAO`, `TimezoneDAO`, `UnitDAO`, `ReportService`, `HttpServletRequest`, `HttpSession`

---

### 2. DBUtil.java

**Class:** `com.util.DBUtil`

**Fields:**

| Field | Line |
|-------|------|
| `private static String databaseName` | 22 |

**Methods:**

| Method | Line |
|--------|------|
| `public static Connection getConnection()` | 24 |
| `public static Connection getConnection(boolean autoCommit)` | 28 |
| `private static void ensureDatabaseNameIsSet()` | 43 |
| `@Deprecated public static void closeConnection(Connection conn)` | 57 |
| `public static <T> List<T> queryForObjects(String, PreparedStatementHandler, ResultMapper<T>)` | 61 |
| `public static <T> List<T> queryForObjectsWithRowHandler(String, PreparedStatementHandler, RowHandler<T>)` | 84 |
| `public static <T> List<T> queryForObjects(Connection, String, PreparedStatementHandler, ResultMapper<T>)` | 107 |
| `public static <T> Optional<T> queryForObject(String, ResultMapper<T>)` | 128 |
| `public static <T> Optional<T> queryForObject(String, PreparedStatementHandler, ResultMapper<T>)` | 148 |
| `public static <T> Optional<T> queryForObject(Connection, String, PreparedStatementHandler, ResultMapper<T>)` | 172 |
| `public static int updateObject(Connection, String, PreparedStatementHandler)` | 195 |
| `public static int updateObject(String, PreparedStatementHandler)` | 211 |
| `public static void executeStatementWithRollback(String, PreparedStatementHandler)` | 228 |

**Nested interfaces defined:**

| Interface | Line |
|-----------|------|
| `public interface PreparedStatementHandler` | 247 |
| `public interface ResultMapper<T>` | 251 |
| `public interface RowHandler<T>` | 255 |

**Unused imports:**
- `java.sql.Timestamp` (line 16) — imported but never referenced in the class body

---

### 3. DateUtil.java

**Class:** `com.util.DateUtil`

**Fields:**

| Field | Line |
|-------|------|
| `private static Logger log` | 27 |

**Methods:**

| Method | Line |
|--------|------|
| `private static Date stringToDate(String, String)` | 29 |
| `public static Date stringToUTCDate(String, String)` | 55 |
| `public static String stringToIsoNoTimezone(String, String)` | 60 |
| `public static Date getDaysDate(Date, int)` | 66 |
| `public static String dateToString(Date)` | 71 |
| `public static java.sql.Date stringToSQLDate(String, String)` | 76 |
| `public static String sqlDateToString(java.sql.Date, String)` | 90 |
| `public static String sqlTimestampToString(java.sql.Timestamp, String)` | 95 |
| `public static Date getStartDate(Date, String)` | 100 |
| `public static Timestamp getLocalTimestamp(String, Locale)` | 115 |
| `public static Date getLocalTime(String, Locale)` | 131 |
| `public static String formatDate(Date)` | 143 |
| `public static String formatDate(Date, String)` | 147 |
| `public static String formatDateTime(Timestamp, String)` | 153 |
| `public static Date parseDate(String)` | 159 |
| `public static Date parseDateTime(String)` | 164 |
| `public static Timestamp stringToTimestamp(String)` | 175 |
| `public static long StringTimeDifference(String, String, TimeUnit, String)` | 188 |
| `public static String GetDateNow()` | 204 |
| `public static Date toDate(LocalDate)` | 210 |
| `private static Date local2utc(Date)` | 214 |
| `public static Timestamp utc2Local(Timestamp)` | 222 |
| `public static Timestamp utc2Local(Timestamp, String)` | 227 |
| `public static String getDateFormatFromDateTimeFormat(String)` | 233 |

**Unused imports:**
- `java.sql.Connection` (line 3) — never used in class body
- `java.sql.ResultSet` (line 4) — never used in class body
- `java.sql.Statement` (line 6) — never used in class body
- `org.apache.commons.dbutils.DbUtils` (line 22) — never used in class body

---

## Findings

### CompanySessionSwitcher.java

**A103-1 | MEDIUM | CompanySessionSwitcher.java:17 | Method name violates Java naming convention**
`UpdateCompanySessionAttributes` starts with an uppercase letter. Java method names must use lowerCamelCase. The method should be named `updateCompanySessionAttributes`.

**A103-2 | MEDIUM | CompanySessionSwitcher.java:27-29 | Duplicate session attribute set for the same value**
`session.setAttribute("sessCompId", comp_id)` at line 27 and `session.setAttribute("currentCompany", comp_id)` at line 29 both store the same `comp_id` value under two different keys. Either both keys are intentionally maintained in parallel (creating silent inconsistency risk if one is updated without the other), or one is dead/redundant. This is a leaky design that duplicates state with no comment explaining the intent.

**A103-3 | LOW | CompanySessionSwitcher.java:37 | Missing space before method argument**
`DriverDAO.getTotalDriverByID(comp_id, true,tzone.getZone())` — missing space after the comma before `tzone.getZone()`. Minor style inconsistency relative to all other call sites in the same file which use a space after every comma.

**A103-4 | LOW | CompanySessionSwitcher.java:39 | Missing space before method argument**
`ReportService.getInstance().countPreOpsCompletedToday(Long.valueOf(comp_id),tzone.getZone())` — missing space after the comma before `tzone.getZone()`.

**A103-5 | LOW | CompanySessionSwitcher.java:41 | Missing space before method argument**
`ReportService.getInstance().countImpactsToday(Long.valueOf(comp_id),tzone.getZone())` — missing space after the comma before `tzone.getZone()`.

**A103-6 | LOW | CompanySessionSwitcher.java:45 | Trailing blank line inside method body before closing brace**
There is an unnecessary blank line at line 45 immediately before the closing `}` of the method body.

---

### DBUtil.java

**A103-7 | HIGH | DBUtil.java:75-77 | SQLException silently swallowed in queryForObjects; method declares throws but never throws**
`queryForObjects(String, PreparedStatementHandler, ResultMapper)` catches `SQLException`, prints the stack trace, and returns an empty list — but the method signature declares `throws SQLException`. The caller is led to believe the exception will propagate; instead it is silently eaten and an empty result is returned as if the query succeeded. The same anti-pattern is repeated in `queryForObjectsWithRowHandler` (line 98-100), the three-arg `queryForObjects` (line 119-121), `queryForObject(String, ResultMapper)` (line 140-142), `queryForObject(String, PreparedStatementHandler, ResultMapper)` (line 164-166), `queryForObject(Connection, String, PreparedStatementHandler, ResultMapper)` (line 186-188), `updateObject(Connection, String, PreparedStatementHandler)` (line 203-205), and `updateObject(String, PreparedStatementHandler)` (line 220-222). In `updateObject` variants the return of `-1` on failure is also undocumented.

**A103-8 | HIGH | DBUtil.java:128-146 | Connection resource leak in queryForObject(String, ResultMapper)**
`conn = getConnection()` is called at line 131 before the `try` block. If `conn.prepareStatement(query)` at line 134 throws, the `finally` block will still close the connection correctly — however, if `getConnection()` itself does not throw but a subsequent checked exception is thrown before entering the `try`, the pattern is fragile. More critically, in the `catch (SQLException e)` at line 140, `e.printStackTrace()` is called and execution falls through to the `finally` which closes the connection — but the method then returns `Optional.empty()` silently, hiding the error. This is the same swallowing issue as A103-7 but is isolated here because the connection allocation is placed outside the `try` block, unlike every other method in the class. This is also an **inconsistency**: all other `queryForObject` overloads allocate `conn` inside the `try` block.

**A103-9 | MEDIUM | DBUtil.java:16 | Unused import: java.sql.Timestamp**
`java.sql.Timestamp` is imported at line 16 but is never referenced anywhere in `DBUtil.java`. This is a dead import that adds noise and may cause a compiler warning.

**A103-10 | MEDIUM | DBUtil.java:122-124 | Inconsistent resource-close pattern**
The three-argument `queryForObjects(Connection, String, PreparedStatementHandler, ResultMapper)` at lines 122-124 closes `stmt` and `rs` with two separate `DbUtils.closeQuietly` calls:
```java
DbUtils.closeQuietly(stmt);
DbUtils.closeQuietly(rs);
```
Every other method in this class uses the single three-argument form `DbUtils.closeQuietly(conn, stmt, rs)` or at minimum a single call per resource type, making this the only place that uses two separate single-argument calls in a `finally` block for the same resource pair. The same pattern appears at lines 189-190 in `queryForObject(Connection, ...)`. Inconsistency introduces maintenance risk.

**A103-11 | MEDIUM | DBUtil.java:223 | Passing explicit null as third argument to DbUtils.closeQuietly**
`updateObject(String, PreparedStatementHandler)` at line 223 calls `DbUtils.closeQuietly(conn, stmt, null)`. Passing an explicit `null` where no `ResultSet` exists is harmless but misleading; it implies a `ResultSet` was expected but simply not assigned. The same pattern appears at line 242 in `executeStatementWithRollback`. These should either use the two-argument overload or a dedicated statement close, for clarity.

**A103-12 | LOW | DBUtil.java:57-59 | @Deprecated method has no Javadoc explaining the replacement**
`closeConnection` is annotated `@Deprecated` but carries no `@deprecated` Javadoc tag pointing callers to the replacement (`DbUtils.closeQuietly`). This makes the deprecation non-actionable.

**A103-13 | LOW | DBUtil.java:245-246 | Trailing blank lines between method and nested interfaces**
Lines 245-246 contain two consecutive blank lines between `executeStatementWithRollback` and the nested interface block. The rest of the file uses single blank lines to separate members.

---

### DateUtil.java

**A103-14 | HIGH | DateUtil.java:168 | Incorrect date-format pattern: lowercase `mm` used instead of `MM` for months**
In `parseDateTime`, the format string is `"yyyy-mm-dd HH:mm:ss"`. The `mm` in the date portion refers to minutes (not months). The correct pattern for months is `MM`. As a result, this method will silently produce wrong dates for any input — the month component will be parsed as minutes and the actual month will default to January. The format string should be `"yyyy-MM-dd HH:mm:ss"`.

**A103-15 | MEDIUM | DateUtil.java:188 | Method name violates Java naming convention**
`StringTimeDifference` starts with an uppercase letter. Java method names must use lowerCamelCase. The method should be named `stringTimeDifference`.

**A103-16 | MEDIUM | DateUtil.java:204 | Method name violates Java naming convention**
`GetDateNow` starts with an uppercase letter. Java method names must use lowerCamelCase. The method should be named `getDateNow`.

**A103-17 | MEDIUM | DateUtil.java:3-6 | Unused SQL imports**
`java.sql.Connection` (line 3), `java.sql.ResultSet` (line 4), and `java.sql.Statement` (line 6) are imported but never referenced in the class body. These are dead imports and will generate compiler warnings.

**A103-18 | MEDIUM | DateUtil.java:22 | Unused import: org.apache.commons.dbutils.DbUtils**
`DbUtils` is imported at line 22 but never used anywhere in `DateUtil.java`. This import does not belong in a date-utility class at all, suggesting it was copied from another file.

**A103-19 | MEDIUM | DateUtil.java:48 | System.out.println used for exception reporting instead of logger**
`stringToDate` at line 48 calls `System.out.println("Exception " + e.getMessage())` to report a `ParseException`. The class already has a `Logger` field (`log`, line 27). Using `System.out` bypasses the logging framework; the same issue is repeated at lines 84, 183, and 199 in `stringToSQLDate`, `stringToTimestamp`, and `StringTimeDifference`. The logger is used in `getLocalTimestamp` (lines 126-127) but not in these other methods — an inconsistency.

**A103-20 | MEDIUM | DateUtil.java:32 | boolean variable `parsed` is unnecessary**
In `stringToDate`, the local variable `parsed` is set to `true` or `false` purely to decide whether to try a fallback parse in the block at lines 43-50. The logic could be simplified by using a direct `null` check on `date` after the initial parse attempt. The variable adds indirection with no benefit.

**A103-21 | LOW | DateUtil.java:67 | Magic-number local variable uses non-standard naming**
`long MILLIS_IN_A_DAY = 1000 * 60 * 60 * 24` in `getDaysDate` uses SCREAMING_SNAKE_CASE, which is the Java convention for `static final` constants, not for local variables. The local variable should use camelCase (`millisInADay`), or the value should be extracted to a named class-level constant.

**A103-22 | LOW | DateUtil.java:117 | Typo in referenced constant name: DEFAUTL_TIMEZONE**
`RuntimeConf.DEFAUTL_TIMEZONE` (referenced at lines 117 and 133) is a misspelling of `DEFAULT_TIMEZONE`. The constant is defined in `RuntimeConf.java` with this same typo (line 11 of that file). Both the definition and all usages carry the misspelling. While this compiles correctly, it is a quality defect that is confusing and should be corrected uniformly.

**A103-23 | LOW | DateUtil.java:214-220 | local2utc performs a no-op timezone conversion**
In `local2utc`, the code creates a `LocalDateTime` from the system default zone, then builds a `ZonedDateTime` using the system default zone again (`ZoneId.systemDefault()` used twice, lines 217-218), then shifts to GMT. The intermediate `ZonedDateTime zdt = ldt.atZone(ZoneId.systemDefault())` could have simply used `date.toInstant()` to get to GMT directly. The double use of `systemDefault` is misleading and suggests the intent was to accept an explicit source timezone.

**A103-24 | LOW | DateUtil.java:233-240 | getDateFormatFromDateTimeFormat assumes space as separator without documentation**
The method silently assumes date and time parts are separated by a single space. If a format string uses a `T` separator (ISO 8601 style) or any other delimiter, it returns the full unmodified string without warning. This assumption is undocumented and fragile.

---

## Summary Table

| ID | Severity | File | Line | Category |
|----|----------|------|------|----------|
| A103-1 | MEDIUM | CompanySessionSwitcher.java | 17 | Naming convention |
| A103-2 | MEDIUM | CompanySessionSwitcher.java | 27-29 | Dead/duplicate state |
| A103-3 | LOW | CompanySessionSwitcher.java | 37 | Style inconsistency |
| A103-4 | LOW | CompanySessionSwitcher.java | 39 | Style inconsistency |
| A103-5 | LOW | CompanySessionSwitcher.java | 41 | Style inconsistency |
| A103-6 | LOW | CompanySessionSwitcher.java | 45 | Style inconsistency |
| A103-7 | HIGH | DBUtil.java | 75-77 (and repeated) | Exception swallowed; misleading throws declaration |
| A103-8 | HIGH | DBUtil.java | 128-146 | Inconsistent resource allocation; exception swallowed |
| A103-9 | MEDIUM | DBUtil.java | 16 | Unused import |
| A103-10 | MEDIUM | DBUtil.java | 122-124 | Inconsistent resource-close pattern |
| A103-11 | MEDIUM | DBUtil.java | 223, 242 | Passing explicit null to closeQuietly |
| A103-12 | LOW | DBUtil.java | 57-59 | Incomplete deprecation annotation |
| A103-13 | LOW | DBUtil.java | 245-246 | Style inconsistency (blank lines) |
| A103-14 | HIGH | DateUtil.java | 168 | Bug: wrong format pattern (mm vs MM) |
| A103-15 | MEDIUM | DateUtil.java | 188 | Naming convention |
| A103-16 | MEDIUM | DateUtil.java | 204 | Naming convention |
| A103-17 | MEDIUM | DateUtil.java | 3-6 | Unused imports |
| A103-18 | MEDIUM | DateUtil.java | 22 | Unused import |
| A103-19 | MEDIUM | DateUtil.java | 48, 84, 183, 199 | System.out instead of logger |
| A103-20 | MEDIUM | DateUtil.java | 32 | Unnecessary variable / dead boolean |
| A103-21 | LOW | DateUtil.java | 67 | Naming convention (local constant) |
| A103-22 | LOW | DateUtil.java | 117, 133 | Typo in constant name |
| A103-23 | LOW | DateUtil.java | 214-220 | Misleading no-op timezone conversion |
| A103-24 | LOW | DateUtil.java | 233-240 | Undocumented fragile assumption |
# Pass 4 (Code Quality) - Agent A104
**Audit date:** 2026-02-26
**Assigned files:**
- `src/main/java/com/util/HttpDownloadUtility.java`
- `src/main/java/com/util/ImpactUtil.java`
- `src/main/java/com/util/ImportExcelData.java`

---

## Reading Evidence

### 1. HttpDownloadUtility.java

**Class:** `com.util.HttpDownloadUtility`

**Fields:**
- `private static Logger log` (line 23) — Log4j Logger instance
- `private static final int BUFFER_SIZE = 4096` (line 25)
- `private static String saveFilePath = ""` (line 26)

**Methods:**
| Method | Line |
|--------|------|
| `public static void downloadFile(String fileName, String fileURL, String saveDir)` | 35 |
| `public static int sendPost(String fileName, String input, String saveDir)` | 88 |
| `public static String getSaveFilePath()` | 186 |
| `public static void setSaveFilePath(String saveFilePath)` | 190 |

**Constants defined:**
- `BUFFER_SIZE = 4096` (line 25)

**Imports used / unused:**
- `BufferedReader` — unused (no BufferedReader in the file body)
- `InputStreamReader` — unused
- `Scanner` — unused
- `List` — unused
- `Map` — unused
- `HttpsURLConnection` — unused (HTTPS connection is commented out)

---

### 2. ImpactUtil.java

**Class:** `com.util.ImpactUtil`

**Inner class:** `public static class UnhandledImpactLevelException extends IllegalArgumentException` (line 52)

**Fields (constants):**
- `private static final double G_FORCE_COEFFICIENT = 0.00388` (line 6)
- `private static final double BLUE_IMPACT_COEFFICIENT = 1` (line 7)
- `private static final double AMBER_IMPACT_COEFFICIENT = 5` (line 8)
- `private static final double RED_IMPACT_COEFFICIENT = 10` (line 9)

**Methods:**
| Method | Line |
|--------|------|
| `public static double calculateGForceOfImpact(long impactValue)` | 11 |
| `public static double calculateGForceRequiredForImpact(double impactThreshold, ImpactLevel impactLevel)` | 15 |
| `private static double getImpactLevelCoefficient(ImpactLevel impactLevel)` | 19 |
| `public static String getCSSColor(ImpactLevel impactLevel)` | 32 |
| `public static ImpactLevel calculateImpactLevel(int impactValue, int impactThreshold)` | 45 |
| `UnhandledImpactLevelException(ImpactLevel impactLevel)` (constructor) | 53 |

**Types defined:**
- `UnhandledImpactLevelException` (inner static class, line 52)

---

### 3. ImportExcelData.java

**Class:** `com.util.ImportExcelData`

**Fields:**
- `private String savePath = ""` (line 29)

**Methods:**
| Method | Line |
|--------|------|
| `public boolean upload(FormFile formFile)` | 32 |
| `public List<ArrayList<String>> read(String fileName)` | 47 |
| `public String getSavePath()` | 75 |
| `public void setSavePath(String savePath)` | 79 |
| `public boolean checkFileExits()` | 83 |

**Imports used / unused:**
- `FileInputStream` — unused
- `FileWriter` — unused
- `DecimalFormat` — unused
- `StringTokenizer` — used (line 59)
- `HSSFWorkbook` — unused
- `XSSFWorkbook` — unused
- `Sheet` — unused
- `Row` — unused
- `Cell` — unused
- `Workbook` — unused
- `ServletException` — present in throws clause only; no actual use
- `BufferedReader` — used (line 52)

---

## Findings

### HttpDownloadUtility.java

**A104-1 | HIGH | HttpDownloadUtility.java:62-73 | Resource leak: InputStream and FileOutputStream not closed in a finally block or try-with-resources**
In `downloadFile()`, `InputStream inputStream` and `FileOutputStream outputStream` are opened inside a try block (lines 62–64) and closed manually at lines 72–73. If a write or read exception is thrown between open and close, both streams leak. The same pattern is repeated in `sendPost()` at lines 159–171. Neither try block uses try-with-resources or a finally clause to guarantee closure.

**A104-2 | HIGH | HttpDownloadUtility.java:110-118 | Exception swallowed silently: write failure in sendPost() is caught, printed, and ignored**
The `catch(Exception e)` block at line 115 calls `e.printStackTrace()` and continues execution. After this catch, `con.getResponseCode()` is still called (line 120), meaning a partial/failed POST body is treated as a successful request. The same swallow pattern appears in `downloadFile()` at lines 74–77. Swallowing `Exception` hides real failures and causes misleading downstream behavior.

**A104-3 | HIGH | HttpDownloadUtility.java:26 | Mutable shared state: static field `saveFilePath` is not thread-safe**
`saveFilePath` is a `private static String` that is written in both `downloadFile()` and `sendPost()`. If these methods are called concurrently (e.g., from a web container thread pool), one call will overwrite the path set by another. The getter/setter pair (lines 186–192) makes this worse by exposing the mutation surface. The field should be a local variable returned from each method, not shared static state.

**A104-4 | MEDIUM | HttpDownloadUtility.java:93-94 | Commented-out code: hardcoded test URL and test payload**
Lines 93–94 contain commented-out test values (`http://httpbin.org/post` and a hardcoded JSON payload). These are debugging artifacts that should be removed before production code.

**A104-5 | MEDIUM | HttpDownloadUtility.java:122-126 | Commented-out code: debug System.out.println statements**
Lines 122–126 contain five commented-out `System.out.println` debug lines. These are dead code that should be removed.

**A104-6 | MEDIUM | HttpDownloadUtility.java:129-151 | Commented-out code: large debug block (header printing + error stream scanning)**
Lines 129–151 are an entirely commented-out try/catch block that prints response headers and error stream contents. This is a significant block of dead code that should be deleted, not retained as a comment.

**A104-7 | MEDIUM | HttpDownloadUtility.java:92-93 | Dead code: `fileName` parameter of sendPost() is immediately overwritten**
The `fileName` parameter declared at line 88 is unconditionally overwritten at line 90 (`fileName = "pandora-usage-dashboard"`). The caller-supplied value is never used. The parameter should be removed from the method signature or the hardcoded assignment should be removed.

**A104-8 | MEDIUM | HttpDownloadUtility.java:4-15 | Unused imports: BufferedReader, InputStreamReader, Scanner, List, Map**
Five imports are present but nothing in the file body references them. These are likely leftovers from removed or commented-out code (the commented-out Scanner/Map block at lines 129–151).

**A104-9 | MEDIUM | HttpDownloadUtility.java:17 | Unused import: HttpsURLConnection**
`javax.net.ssl.HttpsURLConnection` is imported but the HTTPS connection line (`HttpsURLConnection con = ...`) is commented out at line 98. The import is dead.

**A104-10 | MEDIUM | HttpDownloadUtility.java:50-51 | Off-by-one risk in Content-Disposition filename parsing**
The substring call `disposition.substring(index + 10, disposition.length() - 1)` assumes the value begins exactly at offset +10 from `"filename="` (i.e., it assumes a leading quote character). If the header uses no quotes or a different quoting style this produces a wrong or truncated filename. There is no validation or comment explaining the assumption.

**A104-11 | MEDIUM | HttpDownloadUtility.java:105 | Hardcoded API authentication token in source code**
The `X-AUTH-TOKEN` value `"noCwHkr7lofpFL0ZAL2EzynUBLKN1Krcs8bSunismUE"` is hardcoded as a string literal at line 105. Credentials must never be stored in source code; they should be loaded from configuration or a secrets manager.

**A104-12 | LOW | HttpDownloadUtility.java:21 | Trailing whitespace in class declaration**
Line 21 has two trailing spaces after `HttpDownloadUtility` before the opening brace: `public class HttpDownloadUtility  {`. Minor style issue.

**A104-13 | LOW | HttpDownloadUtility.java:29-84 | Inconsistent indentation in downloadFile()**
The method body uses 4-space indentation at lines 37–57 but switches to 3-space indentation for the try block at lines 60–77, then back to 3-space for the log/disconnect at lines 79–84. This is inconsistent with the rest of the class which uses tab characters.

**A104-14 | LOW | HttpDownloadUtility.java:101 | Typo in comment: "reuqest"**
Line 101 reads `//add reuqest header`. Should be "request".

---

### ImpactUtil.java

**A104-15 | MEDIUM | ImpactUtil.java:49 | Returning null instead of a typed sentinel: calculateImpactLevel() returns null for no-impact**
At line 49, `calculateImpactLevel()` returns `null` when the impact value is below all thresholds. Returning `null` for a typed enum result forces every caller to perform a null check or risk a NullPointerException. The `ImpactLevel` enum has no `NONE` value; a `null` return leaks the "no impact" concept implicitly rather than explicitly. This is a leaky abstraction.

**A104-16 | MEDIUM | ImpactUtil.java:45-48 | Parameter type mismatch between calculateGForceOfImpact and calculateImpactLevel**
`calculateGForceOfImpact` takes a `long impactValue` (line 11) but `calculateImpactLevel` takes `int impactValue` (line 45). The same conceptual quantity — an impact sensor reading — uses inconsistent types across the two methods. If the caller has a `long` value they must cast it to call `calculateImpactLevel`, silently truncating high values.

**A104-17 | LOW | ImpactUtil.java:52-55 | Package-private constructor on public inner class UnhandledImpactLevelException**
`UnhandledImpactLevelException` is declared `public static class` (line 52) but its constructor has default (package-private) visibility (line 53). External callers in other packages can reference the exception type but cannot construct it directly, which is an inconsistent encapsulation surface.

**A104-18 | LOW | ImpactUtil.java:7 | Magic constant: BLUE_IMPACT_COEFFICIENT = 1 doubles as a multiplier and a threshold boundary**
`BLUE_IMPACT_COEFFICIENT` is defined as `1` and used both in `getImpactLevelCoefficient()` (as a scaling factor) and in `calculateImpactLevel()` (as a threshold multiplier). The value `1` means "multiply by 1", making it a no-op multiplier. Its purpose is clear in context, but using a named constant whose value is `1` to represent "blue threshold" can be misleading when reading `calculateImpactLevel` — it obscures that the blue boundary is just the raw `impactThreshold` value.

---

### ImportExcelData.java

**A104-19 | HIGH | ImportExcelData.java:47-72 | Resource leak: BufferedReader never closed**
`bufRdr` is opened at line 52 but there is no `close()` call and no try-with-resources. If any iteration of the read loop throws an exception the reader leaks its file handle. The method also declares `throws IOException` but does not protect the reader with a finally block.

**A104-20 | HIGH | ImportExcelData.java:32-44 | Resource leak: FileOutputStream not closed on exception**
In `upload()`, if `outputStream.write()` throws at line 36, the catch block at line 37 suppresses the exception and the finally-like close at lines 40–43 may or may not execute — but execution falls through `catch` to the `if (outputStream != null)` check. If the constructor itself threw (line 35), `outputStream` is null so no leak, but if write throws after open, the stream is closed correctly. However, the pattern is fragile: the exception is silently swallowed (only `e.printStackTrace()`) and the method unconditionally returns `true` (line 44) even when the write failed, giving callers a false success indication.

**A104-21 | HIGH | ImportExcelData.java:44 | Incorrect return value: upload() always returns true regardless of failure**
The method `upload()` declares `boolean` return type but unconditionally returns `true` at line 44, even when the `catch` block on line 37 has caught an exception. The caller cannot detect upload failures from the return value.

**A104-22 | MEDIUM | ImportExcelData.java:19-24 | Unused imports: HSSFWorkbook, XSSFWorkbook, Workbook, Sheet, Row, Cell**
Six Apache POI imports are present (lines 19–24) but the class body contains no reference to any of them. The class name is `ImportExcelData` but it only reads CSV files via `BufferedReader`. The POI imports suggest an incomplete implementation or dead code left from a prior version.

**A104-23 | MEDIUM | ImportExcelData.java:6-7 | Unused imports: FileInputStream, FileWriter**
`FileInputStream` (line 6) and `FileWriter` (line 9) are imported but never used in the class body.

**A104-24 | MEDIUM | ImportExcelData.java:12 | Unused import: DecimalFormat**
`java.text.DecimalFormat` is imported at line 12 but never referenced.

**A104-25 | MEDIUM | ImportExcelData.java:47 | Raw type used: List<ArrayList<String>> mixes generic and raw form**
The return type and the local declaration at line 49 use `ArrayList<String>` as the generic parameter of `List`, which is fine, but the method is named `read` and processes CSV data into a two-dimensional list. The outer collection being `List<ArrayList<String>>` rather than `List<List<String>>` exposes the concrete implementation type in the public API surface, coupling callers to `ArrayList`.

**A104-26 | MEDIUM | ImportExcelData.java:54-55 | Unused variables: `row` and `col` counters are incremented but never used or returned**
Variables `row` (line 54) and `col` (line 55) are declared and incremented (lines 65 and 68) but their values are never read, returned, or logged. They are dead variables.

**A104-27 | MEDIUM | ImportExcelData.java:59 | Use of legacy StringTokenizer instead of String.split()**
`StringTokenizer` (line 59) is a legacy class superseded by `String.split()` and more modern CSV parsers. It is listed in Java documentation as a legacy class kept for compatibility. For CSV parsing it is also incorrect when fields contain quoted commas.

**A104-28 | LOW | ImportExcelData.java:83 | Typo in method name: checkFileExits() should be checkFileExists()**
The method at line 83 is named `checkFileExits` (missing the 's' in "Exists"). This is a public method, so renaming is a breaking change for any caller, but the misspelling is a clear naming convention violation.

**A104-29 | LOW | ImportExcelData.java:85 | Unnecessary use of boxed Boolean instead of primitive boolean**
At line 85, `Boolean res = false;` uses the boxed `Boolean` wrapper type where `boolean` is sufficient. There is no need for the nullable wrapper here since the variable is immediately assigned `false` and returned as a primitive-compatible value.

**A104-30 | LOW | ImportExcelData.java:83-92 | Verbose checkFileExits() can be a single-line expression**
The method allocates a `Boolean`, a `File`, and uses an `if` statement where `return new File(this.getSavePath()).exists();` would suffice. This is a style/readability issue rather than a correctness issue.

**A104-31 | LOW | ImportExcelData.java:17 | Unused import: ServletException**
`javax.servlet.ServletException` is imported and appears in the `throws` clause of `upload()` at line 32, but is never actually thrown or caught inside the method. It is a spurious checked exception declaration.

---

## Summary

| Severity | Count |
|----------|-------|
| HIGH     | 6     |
| MEDIUM   | 16    |
| LOW      | 9     |
| **Total**| **31**|

**Most critical issues overall:**
1. Resource leaks (streams not closed in finally/try-with-resources) appear in all three files.
2. Exception swallowing with `e.printStackTrace()` masks failures throughout `HttpDownloadUtility` and `ImportExcelData`.
3. A hardcoded API authentication token in `HttpDownloadUtility.sendPost()` is a security concern.
4. `ImportExcelData.upload()` unconditionally returns `true` even after a failed write.
5. `ImpactUtil.calculateImpactLevel()` returns `null` to indicate "no impact", creating mandatory null-check burden on every caller.
# Pass 4 (Code Quality) — Agent A105
**Date:** 2026-02-26
**Assigned files:**
- `src/main/java/com/util/InfoLogger.java`
- `src/main/java/com/util/RuntimeConf.java`
- `src/main/java/com/util/Util.java`

---

## Reading Evidence

### InfoLogger.java

**Module/Class:** `com.util.InfoLogger`

**Methods:**
| Method | Line |
|--------|------|
| `static {}` (static initializer) | 15 |
| `getFileURL(final String s)` | 26 |
| `static getLogger(final String c)` | 35 |
| `static logException(Logger log, final Exception e)` | 44 |

**Types/imports used:** `Logger` (log4j 1.x), `PropertyConfigurator`, `PrintWriter`, `StringWriter`, `URL`

**No constants or enums defined.**

---

### RuntimeConf.java

**Module/Class:** `com.util.RuntimeConf`

**Methods:** None (pure constants class)

**Fields (all `public static`, mostly non-final):**
| Field | Line |
|-------|------|
| `projectTitle` | 4 |
| `database` | 5 |
| `emailFrom` | 6 |
| `emailFromLinde` | 7 |
| `url` | 8 |
| `ERROR_PAGE` | 9 |
| `EXPIRE_PAGE` | 10 |
| `DEFAUTL_TIMEZONE` | 11 |
| `HOUR_METER` | 12 |
| `REGISTER_SUBJECT` | 13 |
| `UPDATE_APP_SUBJECT` | 14 |
| `UPGRADE_CONTENT` | 15 |
| `RECEIVER_EMAIL` | 16 |
| `EMAIL_IMPORT_TITLE` | 17 |
| `EMAIL_RESET_TITLE` | 18 |
| `EMAIL_COMMENT_TITLE` | 19 |
| `EMAIL_DIGANOSTICS_TITLE` | 20 |
| `API_LOGIN` | 22 |
| `API_VEHICLE` | 23 |
| `API_DRIVER` | 24 |
| `API_ATTACHMENT` | 25 |
| `API_QUESTION` | 26 |
| `API_RESULT` | 27 |
| `API_PDFRPT` | 28 |
| `API_BARCODE` | 29 |
| `API_INVALID` | 30 |
| `Load_BARCODE` | 31 |
| `UPLOAD_FOLDER` | 32 |
| `BROCHURE_FOLDER` | 33 |
| `XML_FOLDER` | 34 |
| `IMG_SRC` | 35 |
| `COMP` | 36 |
| `PDF_FOLDER` | 37 |
| `RESULT_FAIL` | 40 |
| `RESULT_OK` | 41 |
| `RESULT_INCOMPLETE` | 42 |
| `ROLE_COMP` | 44 |
| `ROLE_SYSADMIN` | 45 |
| `ROLE_DEALER` | 46 |
| `ROLE_SUBCOMP` | 47 |
| `ROLE_SITEADMIN` | 48 |
| `CHECKLIST_SECONDS` | 50 |
| `DEFAULT_SCANNERTIME` | 51 |
| `LINDEDB` | 53 |
| `LINDERPTTITLE` | 54 |
| `EMPTYLOGO` | 55 |
| `emailContent` | 57 |
| `debugEmailRecipet` | 58 |
| `APIURL` | 60 |
| `file_type` | 61 |
| `cloudImageURL` | 62 |
| `v_user` | 64 (`public static final`) |
| `HTTP_OK` | 66 (`public static final`) |

---

### Util.java

**Module/Class:** `com.util.Util`

**Methods:**
| Method | Line |
|--------|------|
| `static sendMail(String subject, String mBody, String rName, String rEmail, String sName, String sEmail)` | 32 |
| `static sendMail(String subject, String mBody, String rName, String rEmail, String sName, String sEmail, String attachment, String attachmentName)` | 73 |
| `static getHTML(String urlToRead)` | 134 |
| `static genPass(int chars)` | 159 |
| `static checkedValueRadio(String value, String dbValue)` | 179 |
| `static checkedValueCheckbox(String value, ArrayList<String> dbValue)` | 191 |
| `static ArraListToString(ArrayList<String> arrString)` | 204 (deprecated) |
| `static selectRoleBox(String value, ArrayList<RoleBean> dbValue)` | 210 |
| `static getBarcodeTimeLst(String time)` | 230 |
| `static generateRadomName()` | 258 |
| `static nthOccurrence(String str, char c, int n)` | 268 |

**Imports used (declared but no body usage):** `XMLEncoder` (line 3), `BufferedOutputStream` (line 4), `FileNotFoundException` (line 6), `EntityBean` (line 26), `XmlBean` (line 28)

---

## Findings

### InfoLogger.java

**A105-1 | HIGH | InfoLogger.java:47 | Double-printing of exception — stderr pollution and log duplication**
`logException` calls both `e.printStackTrace()` (line 47, prints to stderr) and `log.error(sw)` (line 48, logs to log4j). Every exception logged through this method will appear twice: once on stderr and once in the log file. The `e.printStackTrace()` call on line 47 is redundant and should be removed; the `StringWriter`/`PrintWriter` path already captures the full stack trace for the logger.

**A105-2 | MEDIUM | InfoLogger.java:17 | Instantiating class to obtain classloader in a static initializer**
The static initializer creates `new InfoLogger()` solely to call `getFileURL()`, which calls `this.getClass().getClassLoader()`. Inside a static context this is unnecessary; `InfoLogger.class.getClassLoader().getResource(...)` accomplishes the same without allocating an object. This is an unnecessary coupling between the static and instance concerns.

**A105-3 | MEDIUM | InfoLogger.java:26 | `getFileURL` is a public instance method used only by the static initializer**
`getFileURL` is public and instance-level but has only one caller: the static initializer at line 17. It is not called from any other class in the codebase (only `ReportAPI.java` defines its own unrelated `getFileURL()`). The method leaks an implementation detail of the initialisation path as a public API. It should be `private static`.

**A105-4 | MEDIUM | InfoLogger.java:14 | Class uses log4j 1.x API directly, bypassing the SLF4J bridge already on the classpath**
The project declares `slf4j-log4j12` and `slf4j-api` in `pom.xml`. `InfoLogger` imports and exposes raw `org.apache.log4j.Logger` objects in its public API, meaning all 45+ callers across the codebase are tightly coupled to log4j 1.x. If the logging backend changes the entire public surface of `InfoLogger` breaks. The wrapper should expose `org.slf4j.Logger` instead.

**A105-5 | LOW | InfoLogger.java:21 | Silent swallowing of `PropertyConfigurator` failure**
The catch block on line 21 calls `e.printStackTrace()` and continues. If log4j configuration fails, no logging will work correctly for the entire application lifetime. At minimum the exception message should be printed; ideally an `ExceptionInInitializerError` should be thrown so the deployment fails fast rather than silently misconfiguring logging.

**A105-6 | LOW | InfoLogger.java:31 | Javadoc typo: "specfied" should be "specified"**
Line 31: `@param c ClassName` — the description prose says "for specfied class name".

---

### RuntimeConf.java

**A105-7 | CRITICAL | RuntimeConf.java:16 | Hardcoded internal email address in source code**
`RECEIVER_EMAIL = "hui@ciifm.com"` is a real personal/internal email address committed to source with an inline comment `//live`. Credentials and routing destinations must not be in source code; this should be externalised to a configuration file or environment variable.

**A105-8 | CRITICAL | RuntimeConf.java:58 | Hardcoded debug recipient email address in source code**
`debugEmailRecipet = "hui@collectiveintelligence.com.au"` is an internal email address hardcoded in source and actively used at runtime (`MailerAction.java:122`). Same issue as A105-7.

**A105-9 | HIGH | RuntimeConf.java:60 | Hardcoded production AWS EC2 hostname in source code**
`APIURL = "http://ec2-52-5-205-104.compute-1.amazonaws.com/api/export/pdf/"` is a concrete production infrastructure URL hardcoded in source. Infrastructure addresses must be externalised so that environments can differ and to avoid leaking topology information in version control.

**A105-10 | HIGH | RuntimeConf.java:4-62 | Almost all constants are mutable (`public static` without `final`)**
Only `v_user` (line 64) and `HTTP_OK` (line 66) are `final`. All other 50+ fields are `public static String` / `public static long`, meaning any class in the JVM can overwrite them at runtime (e.g., `RuntimeConf.emailFrom = "attacker@evil.com"`). Every constant field should be `public static final`.

**A105-11 | HIGH | RuntimeConf.java:11 | Field name typo: `DEFAUTL_TIMEZONE` (should be `DEFAULT_TIMEZONE`)**
The misspelling is propagated to all call sites. Because the field is not `final` it cannot be inlined by the compiler, so a rename would require fixing all call sites. Currently used in `DateUtil.java`.

**A105-12 | HIGH | RuntimeConf.java:20 | Field name typo: `EMAIL_DIGANOSTICS_TITLE` (should be `EMAIL_DIAGNOSTICS_TITLE`)**
"DIGANOSTICS" is a misspelling of "DIAGNOSTICS". Used at runtime in `FormBuilderAction.java:80` and `FleetcheckAction.java:68`.

**A105-13 | MEDIUM | RuntimeConf.java:15 | Value typo: `UPGRADE_CONTENT = "Upgarde Request"` (should be "Upgrade")**
The string value itself contains a typo ("Upgarde"). No active callers were found in the codebase, but the constant is a public API surface and the value would appear in user-facing content if called.

**A105-14 | MEDIUM | RuntimeConf.java:31 | Naming convention violation: `Load_BARCODE` uses mixed case**
All other API constants use `ALL_UPPER_SNAKE_CASE` (e.g., `API_BARCODE`, `API_LOGIN`). `Load_BARCODE` mixes a capitalised word with an uppercase word and violates the established convention. Should be `LOAD_BARCODE`. Actively used in `BarCodeAction.java:66`.

**A105-15 | MEDIUM | RuntimeConf.java:57 | Field name uses `camelCase` instead of `UPPER_SNAKE_CASE`**
`emailContent` (line 57) and `emailFrom` (line 6), `emailFromLinde` (line 7) use camelCase while the majority of other string constants use UPPER_SNAKE_CASE (e.g., `EMAIL_RESET_TITLE`, `EMAIL_COMMENT_TITLE`). Inconsistent naming convention across the same class.

**A105-16 | MEDIUM | RuntimeConf.java:61 | Field name uses `snake_case` instead of `UPPER_SNAKE_CASE`**
`file_type` (line 61) uses lowercase snake_case while every other constant uses UPPER_SNAKE_CASE. Should be `FILE_TYPE`.

**A105-17 | MEDIUM | RuntimeConf.java:4-8 | Application identity fields contain stale/incorrect values**
`projectTitle = "PreStart"` (line 4), `database = "jdbc/PreStartDB"` (line 5), and `url = "http://prestart.collectiveintelligence.com.au/"` (line 8) reference "PreStart" — an earlier product name — while the application is deployed as "forkliftiqadmin" / "PandoraAdmin". Also `REGISTER_SUBJECT = "Pandora Registration Successful"` (line 13) and `COMP = "COLLECTIVE INTELLIGENCE"` (line 36) reflect old branding. Stale values will appear in user-facing emails and documents.

**A105-18 | MEDIUM | RuntimeConf.java:53-55 | Dead constants: `LINDEDB`, `LINDERPTTITLE`, `EMPTYLOGO` are only used in commented-out code**
`LINDEDB` appears only in `////`-commented lines in `AppAPIAction.java`. `LINDERPTTITLE` has zero active usages. `EMPTYLOGO` is used in one active call in `FleetCheckAlert.java:46` but the immediately preceding line 35 is a commented-out duplicate check using the same constant. These residual "Linde/Fleet" branching constants indicate dead feature code that was never fully removed.

**A105-19 | MEDIUM | RuntimeConf.java:14-15 | Dead constants: `UPDATE_APP_SUBJECT` and `UPGRADE_CONTENT` have no callers**
A codebase-wide search found no active usages of either constant outside their declaration. They should be removed or documented if intentionally reserved.

**A105-20 | MEDIUM | RuntimeConf.java:33-34 | Dead constants: `BROCHURE_FOLDER` and `XML_FOLDER` have no callers**
Neither constant is referenced anywhere in the active source. They should be removed.

**A105-21 | LOW | RuntimeConf.java:54 | Typo in value: `LINDERPTTITLE = "Fleet Check Alert"` — "RPT" abbreviation is opaque**
The field name suffix `RPTTITLE` mixes an unexplained abbreviation ("RPT" presumably "report") with "TITLE". The adjacent `LINDERPTTITLE` naming is inconsistent with the pattern `EMAIL_*_TITLE` used elsewhere. (Secondary concern given the constant appears to be dead — see A105-18.)

**A105-22 | LOW | RuntimeConf.java:58 | Field name typo: `debugEmailRecipet` (should be "Recipient")**
"Recipet" is a misspelling of "Recipient". Used in `MailerAction.java:122` at runtime.

**A105-23 | LOW | RuntimeConf.java:3 | No constructor suppression — class can be instantiated**
`RuntimeConf` is a pure constants class but declares no private constructor. Any caller can write `new RuntimeConf()`, which is meaningless and confusing. A private no-arg constructor should be added.

---

### Util.java

**A105-24 | HIGH | Util.java:3,26,28 | Unused imports: `XMLEncoder`, `EntityBean`, `XmlBean`**
`java.beans.XMLEncoder` is imported at line 3 but never referenced in any method body. `com.bean.EntityBean` (line 26) and `com.bean.XmlBean` (line 28) are likewise imported and never used. These are build warnings under `-Xlint:all` (which is configured in `pom.xml:93`) and indicate removed or unfinished code.

**A105-25 | HIGH | Util.java:4,6 | Unused imports: `BufferedOutputStream`, `FileNotFoundException`**
`java.io.BufferedOutputStream` (line 4) and `java.io.FileNotFoundException` (line 6) are imported but never used in any method body. Same category as A105-24.

**A105-26 | HIGH | Util.java:147 | String concatenation in a loop — quadratic memory allocation**
`getHTML` builds the HTTP response with `result += line + "\n"` inside a `while` loop (line 147). For large HTTP responses this creates O(n²) string allocations. A `StringBuilder` should be used instead.

**A105-27 | HIGH | Util.java:73-131 | `sendMail` overload (with attachment) silently ignores recipient parse failure and always returns `true`**
The overload at line 73 catches the `InternetAddress.parse` exception at line 90 and logs to stdout but does not return `false` (unlike the first overload which does return `false` at line 51). The method then continues, attempts to send with no recipient, and always returns `true` (line 130) regardless of whether the message was actually delivered. Callers receive no indication that delivery failed.

**A105-28 | MEDIUM | Util.java:191,210 | Raw `ArrayList` used in public API instead of `List`**
`checkedValueCheckbox(String, ArrayList<String>)` (line 191) and `selectRoleBox(String, ArrayList<RoleBean>)` (line 210) declare their parameters as the concrete type `ArrayList` rather than the `List` interface. This is a leaky abstraction: callers are forced to use `ArrayList` specifically, preventing use of any other `List` implementation without a cast. Parameter types should be `List<String>` and `List<RoleBean>`.

**A105-29 | MEDIUM | Util.java:204 | `@Deprecated` method `ArraListToString` has a misspelled name and no replacement documented**
The method name `ArraListToString` misspells "ArrayList" and also violates Java method naming conventions (starts with uppercase `A`). The `@Deprecated` annotation is present but no `@deprecated` Javadoc tag exists explaining what to use instead. One active caller was found (`MenuDAO.java`). The body is simply `String.join(",", arrString)`, which callers should invoke directly.

**A105-30 | MEDIUM | Util.java:159-175 | `genPass` uses `MD5` for password generation — weak randomness source**
`genPass` hashes random bytes with MD5 (line 164) and returns a hex substring. MD5 is cryptographically broken. While the primary source is `java.util.Random` (not `SecureRandom`) seeded non-cryptographically (line 160), the function is named `genPass` implying password generation. Using `java.security.SecureRandom` with a modern algorithm would be appropriate.

**A105-31 | MEDIUM | Util.java:32-131 | Both `sendMail` overloads catch `Throwable` and swallow it with `printStackTrace`**
Lines 67 and 127 catch `Throwable t` and only print the stack trace to stderr, then fall through to return `true`. This means JVM errors (e.g., `OutOfMemoryError`) are absorbed silently and the caller is told success. At minimum the catch should be narrowed to `Exception`; fatal `Error` subclasses should not be caught at all.

**A105-32 | MEDIUM | Util.java:179,191,210 | Methods `checkedValueRadio`, `checkedValueCheckbox`, `selectRoleBox` have no callers in the codebase**
A codebase-wide search found these three methods defined only in `Util.java` with no callers anywhere else. They appear to be dead utility methods likely superseded by JSP/framework tag equivalents. If unused they should be removed.

**A105-33 | MEDIUM | Util.java:258 | Method name typo: `generateRadomName` (should be `generateRandomName`)**
"Radom" is a misspelling of "Random". The method is used in `FleetCheckPDF.java`. The misspelling propagates to all call sites.

**A105-34 | LOW | Util.java:32,73 | Parameters `rName` and `sName` are accepted but never used**
Both `sendMail` overloads declare `String rName` and `String sName` parameters (recipient name, sender name) that are never read inside either method body. This is dead parameter surface that misleads callers into believing the names affect the message.

**A105-35 | LOW | Util.java:15 | Wildcard import `java.util.*`**
Line 15 uses a wildcard import rather than listing specific types. With `-Xlint:all` enabled in the build, unused import warnings may be partially masked by wildcards. Explicit imports are preferred.

**A105-36 | LOW | Util.java:23-24 | Wildcard imports `javax.mail.internet.*` and `javax.mail.*`**
Lines 23-24 use wildcard imports. Same concern as A105-35.

**A105-37 | LOW | Util.java:134-155 | `getHTML` does not close the connection on exception**
The `conn.disconnect()` and `rd.close()` calls at lines 149-150 are inside the try block and will be skipped if an exception occurs on lines 141-148. The `BufferedReader` and `HttpURLConnection` should be closed in a `finally` block or a try-with-resources statement to prevent connection/socket leaks.

**A105-38 | LOW | Util.java:50,91 | Error messages use `System.out.println` instead of logging**
Lines 50 and 91 log a message to stdout using `System.out.println`. The codebase has `InfoLogger`/log4j available; these should use the logger so errors appear in the configured log appenders rather than the servlet container's stdout stream.

**A105-39 | INFO | Util.java:108 | Attachment presence tested with `equalsIgnoreCase("")` instead of `isEmpty()`**
Line 108: `if(!attachment.equalsIgnoreCase(""))`. An empty string test is better expressed as `!attachment.isEmpty()` (or `!attachment.isBlank()`) since case comparison is irrelevant for an empty string. Minor style concern.
# Pass 4 Code Quality — Agent A106
**File:** `src/main/java/com/util/actionSubmitForm.java`
**Date:** 2026-02-26

---

## Reading Evidence

### Module / Class
- **Package:** `com.util`
- **Class:** `actionSubmitForm`
- **Extends:** `org.apache.struts.taglib.html.FormTag`

### Methods
| Method | Line |
|--------|------|
| `renderFormStartElement()` | 11 |

### Fields
| Field | Line |
|-------|------|
| `private static Logger log` | 9 |

### Types / Errors / Constants Defined
- None defined within this file. No enums, no custom exceptions, no constants.

### Imports
| Import | Line |
|--------|------|
| `javax.servlet.jsp.JspException` | 3 |
| `org.apache.log4j.Logger` | 5 |

---

## Findings

A106-1 | HIGH | src/main/java/com/util/actionSubmitForm.java:8 | **Naming convention violation — class name does not follow PascalCase.** The class is named `actionSubmitForm` but Java naming conventions require class names to use UpperCamelCase (PascalCase). The class should be named `ActionSubmitForm`. All other classes in the `com.util` package follow PascalCase (e.g., `BarCode`, `DateUtil`, `InfoLogger`), making this an isolated violation.

A106-2 | HIGH | src/main/java/com/util/actionSubmitForm.java:7 | **Dead class — whole class is declared unused.** The comment directly above the class declaration reads `//Currently Unused because of introduce of watermaker jquery lib`. The entire class has been superseded by a front-end jQuery library and is no longer exercised at runtime. Dead classes increase maintenance surface, can confuse future developers, and still pull in transitive dependencies (Apache Struts `FormTag`). The class should be removed or, at minimum, tracked in a deletion backlog.

A106-3 | MEDIUM | src/main/java/com/util/actionSubmitForm.java:27 | **Commented-out code.** The line `// renderAttribute(results, "onsubmit", getOnsubmit());` is a deliberate call that has been commented out rather than deleted. The inline `onsubmit` handler is instead hardcoded into the form tag opening string on line 13 (`'clearPlaceholders(this);'`), which is the reason for the removal. The commented line provides no explanatory value beyond that, adds noise, and should be deleted.

A106-4 | MEDIUM | src/main/java/com/util/actionSubmitForm.java:8 | **Build warning — use of deprecated Apache Struts 1 API.** `org.apache.struts.taglib.html.FormTag` is part of Apache Struts 1, which reached end-of-life and has been deprecated for many years. Extending it produces deprecation compiler warnings and ties this class to an unsupported framework. Given the class is also unused (see A106-2), the risk is contained, but it would still be flagged by any modern static-analysis or dependency-audit tool.

A106-5 | MEDIUM | src/main/java/com/util/actionSubmitForm.java:15-20 | **Exception swallowed after logging — TODO not resolved.** The `catch (JspException e)` block logs the exception via `InfoLogger.logException` but then silently continues execution, allowing `renderFormStartElement()` to return a partially-built form string rather than propagating or wrapping the error. The auto-generated `// TODO Auto-generated catch block` comment was never replaced with a deliberate error-handling strategy, indicating the catch body was never consciously designed.

A106-6 | LOW | src/main/java/com/util/actionSubmitForm.java:13 | **Use of `StringBuffer` instead of `StringBuilder`.** `StringBuffer` is synchronized and therefore slower than `StringBuilder` for single-threaded use. The local variable `results` is not shared across threads; `StringBuilder` should be used instead. This is consistent with general modern Java best practice and avoids unnecessary synchronization overhead.

A106-7 | LOW | src/main/java/com/util/actionSubmitForm.java:13 | **Irregular / inconsistent indentation inside `renderFormStartElement`.** The method body uses a deeply shifted right-hand indentation (approximately 12–13 spaces on all statements) relative to the method signature, which is indented with a standard single tab. This produces a visually skewed block that is inconsistent with every other class in the `com.util` package and with standard Java style (each level indented by 4 spaces or 1 tab relative to its enclosing block).

A106-8 | LOW | src/main/java/com/util/actionSubmitForm.java:7 | **Grammatical error in explanatory comment.** The comment reads `//Currently Unused because of introduce of watermaker jquery lib`. "introduce of" should be "introduction of", and "watermaker" appears to be a misspelling of "watermark". Minor, but comments serve as documentation and should be accurate and grammatically correct.

A106-9 | INFO | src/main/java/com/util/actionSubmitForm.java:9 | **`Logger` field declared `private static` but class is unused.** Because the entire class is dead (A106-2), the `log` field will never be initialized at runtime and the associated `InfoLogger.getLogger(...)` call will never execute. This is a secondary consequence of A106-2, noted separately for completeness.
# Pass 4 (Code Quality) — Agent A107
Audit date: 2026-02-26
Assigned files:
- src/test/java/com/calibration/UnitCalibrationImpactFilterTest.java
- src/test/java/com/calibration/UnitCalibrationTest.java

---

## Reading Evidence

### File 1: UnitCalibrationImpactFilterTest.java

**Module/Class:** `com.calibration.UnitCalibrationImpactFilterTest`

**Methods:**
| Method | Line |
|---|---|
| `before()` | 15 |
| `returnsLargestImpactPer15MinutesOfSessionIfAbove80000()` | 20 |
| `CalibrationImpactFactory(Calendar sessionStart)` (constructor, inner class) | 46 |
| `CalibrationImpactFactory.makeImpact(int minute, int value)` | 51 |

**Fields:**
| Field | Type | Line |
|---|---|---|
| `filter` | `UnitCalibrationImpactFilter` | 12 |
| `sessionStart` (inner) | `Calendar` | 43 |
| `time` (inner) | `Calendar` | 44 |

**Types defined:** `CalibrationImpactFactory` (private static inner class, line 42)

**Constants defined:** None

**Imports used:**
- `org.junit.Before`, `org.junit.Test`
- `java.sql.Timestamp`
- `java.util.*`
- `org.junit.Assert.assertEquals`

---

### File 2: UnitCalibrationTest.java

**Module/Class:** `com.calibration.UnitCalibrationTest`

**Methods:**
| Method | Line |
|---|---|
| `returnsZeroPercentCompleteIfNoImpactsAdded()` | 15 |
| `returnsTenPercentCompleteIfTenImpactsAdded()` | 23 |
| `returnsHundredPercentCompleteIfMoreThanHundredImpactsAdded()` | 33 |
| `returnsCalibratedIfCalibrationDateAndThresholdAreSet()` | 43 |
| `returnsCalibratingIfCalibrationDateIsNotSet()` | 55 |
| `returnsCalibratingIfThresholdIsNotSet()` | 66 |
| `returnsCalibratedIfThresholdSetAndResetCalibrationDateNotSet()` | 77 |
| `calculatesThresholdAsAveragePlusStandardDeviation()` | 87 |
| `makeImpacts(int count)` (private static helper) | 102 |

**Fields:** None (no instance fields; class has no `@Before` setup)

**Types defined:** None

**Constants defined:** None

**Imports used:**
- `org.junit.Test`
- `java.sql.Timestamp`
- `java.util.ArrayList`, `java.util.Arrays`, `java.util.Calendar`, `java.util.List`
- `org.junit.Assert.*`

---

## Findings

### UnitCalibrationImpactFilterTest.java

**A107-1 | LOW | UnitCalibrationImpactFilterTest.java:20 | Single test for a non-trivial filter — insufficient boundary and edge-case coverage**

`filterImpacts` has several distinct behaviours: new-session boundary detection, 15-minute sliding window rollover, the ≥80 000 threshold gate, and multiple sessions in one input list. The single test exercises only the happy path across two windows of a single session. There are no tests for: an empty input list, all impacts below the threshold (expects empty list), a single impact exactly at the threshold (80 000), multiple distinct sessions in the same input, or impacts arriving out of order (the comparator in the SUT relies on object identity `!=` for `Timestamp`, which is a latent bug — see A107-3 below). Missing boundary tests leave high-risk paths uncovered.

---

**A107-2 | MEDIUM | UnitCalibrationImpactFilterTest.java:44-45 | Inner helper `CalibrationImpactFactory` mutates shared `time` field without reset, making test data order-dependent**

`CalibrationImpactFactory.makeImpact` sets `time.set(Calendar.MINUTE, minute)` on the shared mutable `Calendar` instance (line 52). Because `Calendar.set(Calendar.MINUTE, …)` replaces only the minute component, calls where `minute` is less than the previous call's minute will silently produce a `Timestamp` that has rolled back in wall-clock time relative to the `sessionStart`. In the current test, minutes are supplied in strictly ascending order (4, 5, 8, 13, 19, 24, 36, 44), so the test passes. If any future maintainer adds an out-of-order impact, the helper will silently produce wrong timestamps without any compile-time or runtime warning. The helper should either accept a full `Calendar`/`Date` argument or document the ordering constraint explicitly.

---

**A107-3 | HIGH | UnitCalibrationImpactFilterTest.java (exercises production code at UnitCalibrationImpactFilter.java:46) | Production comparator uses reference equality (`!=`) instead of `.equals()` or `.compareTo()` for `Timestamp` objects**

The production `compareImpacts` method contains:
```java
if (i1.sessionStart != i2.sessionStart) return i1.sessionStart.compareTo(i2.sessionStart);
```
`!=` is a reference-identity check, not a value check. Two `Timestamp` objects representing the same point in time but constructed separately will be `!=` and will therefore be ordered by `compareTo` rather than being treated as belonging to the same session. The test inadvertently passes because the inner factory constructs **one** `Timestamp` per `sessionStart` and assigns it to all impacts created from the same factory instance (line 54: `new Timestamp(sessionStart.getTime().getTime())` — a new object each call, but the test only uses one factory, so all impacts share value-equal timestamps that happen to compare equal via `compareTo`). The test does not construct a scenario that would expose the reference-equality defect (e.g., two factory instances with the same `sessionStart` time). The test should be extended to cover multi-session inputs built from independent factory instances to catch this latent bug.

---

**A107-4 | LOW | UnitCalibrationImpactFilterTest.java:7 | Wildcard import `java.util.*`**

The file uses `import java.util.*;` rather than explicit per-class imports. The only `java.util` types actually used in the file are `Arrays`, `List`, and `Calendar`. Wildcard imports reduce readability and can mask accidental use of wrong types if the package adds new names. The project's other test file (`UnitCalibrationTest.java`) uses explicit imports consistently; this file should follow the same style.

---

### UnitCalibrationTest.java

**A107-5 | MEDIUM | UnitCalibrationTest.java:46-47 | `Calendar.getInstance()` called twice in a single test, producing two independent `Timestamp` values that may differ**

In `returnsCalibratedIfCalibrationDateAndThresholdAreSet` (line 43):
```java
.resetCalibrationDate(new Timestamp(Calendar.getInstance().getTime().getTime()))
.calibrationDate(new Timestamp(Calendar.getInstance().getTime().getTime()))
```
Each call to `Calendar.getInstance()` captures the current wall-clock time independently. Under normal execution they will be equal or nearly equal, but they are logically different objects representing slightly different instants. If the test is asserting a semantic invariant that depends on the *relationship* between these two dates (e.g., `calibrationDate >= resetCalibrationDate`), the two values should be derived from a single captured instant. More broadly, tests should not depend on wall-clock time at all; a fixed `Timestamp` (e.g., `new Timestamp(0)`) would make the test deterministic and self-documenting.

The same pattern appears at lines 59, 69-70. All instances carry the same risk.

---

**A107-6 | MEDIUM | UnitCalibrationTest.java:87-100 | `calculatesThresholdAsAveragePlusStandardDeviation` uses a magic expected value with no derivation comment**

The test asserts `assertEquals(1586027, unitCalibration.getCalculatedThreshold())`. The expected value `1586027` is computed from the 63-element input list but there is no comment, constant, or separate verification showing how this number was derived. If the formula changes (e.g., population vs. sample standard deviation), this value will silently diverge from intent; reviewers cannot verify correctness without independently recomputing the result. A comment showing the intermediate average and standard deviation values (or, better, a tolerance-based assertion given floating-point truncation) would make the test self-documenting.

---

**A107-7 | LOW | UnitCalibrationTest.java:11 | Wildcard import `org.junit.Assert.*` imports unused assertion methods**

`import static org.junit.Assert.*` pulls in the full assertion API. The file only uses `assertEquals`, `assertTrue`, and `assertFalse`. This is a minor style issue but is inconsistent with the spirit of explicit imports used elsewhere in the class (all `java.util` imports are explicit). Both files in this review mix wildcard and explicit imports; the project should settle on one convention.

---

**A107-8 | LOW | UnitCalibrationTest.java:102-107 | `makeImpacts` generates sequential integers starting at 0, making percentage tests rely on list-size rather than realistic data**

```java
private static List<Integer> makeImpacts(int count) {
    List<Integer> impacts = new ArrayList<>();
    for (int i = 0; i < count; ++i)
        impacts.add(i);
    return impacts;
}
```
The generated impacts are `[0, 1, 2, …, count-1]`. The tests for `calibrationPercentage` use these values but the production `calibrationPercentage` only counts list size, so the actual integer values are irrelevant. This is fine for the percentage tests. However, if `makeImpacts` is ever reused for threshold or calibration-state tests, the synthetic values (especially `0`) could produce misleading results. A brief comment explaining that the values are intentionally arbitrary integers used solely to control list length would prevent misuse.

---

**A107-9 | INFO | UnitCalibrationTest.java:33-40 | Test name says "more than hundred" but uses 111 — minor naming precision issue**

The test `returnsHundredPercentCompleteIfMoreThanHundredImpactsAdded` passes `makeImpacts(111)`. The production code treats the threshold as `>= 100` (UnitCalibration.java:45: `impacts.size() >= 100`), so a count of exactly 100 would also return 100%. No test covers the exact-100 boundary. Adding a test for exactly 100 impacts would make the boundary condition explicit and close a gap in coverage.

---

**A107-10 | INFO | UnitCalibrationImpactFilterTest.java:15-17 | `@Before` setup method is named `before()` rather than the conventional `setUp()`**

JUnit 3 convention was `setUp()`; JUnit 4+ does not require any specific name because of the `@Before` annotation, but most codebases standardise on `setUp` for `@Before` methods. The non-standard name `before()` is functional but slightly inconsistent with common team convention. No other `@Before` method was observed in the test corpus for direct comparison, so this is informational only.

---

## Summary Table

| ID | Severity | File | Line(s) | Short Description |
|---|---|---|---|---|
| A107-1 | LOW | UnitCalibrationImpactFilterTest.java | 20 | Only one test; missing boundary/edge-case coverage for filterImpacts |
| A107-2 | MEDIUM | UnitCalibrationImpactFilterTest.java | 44-52 | Shared mutable Calendar in factory makes test data order-dependent |
| A107-3 | HIGH | UnitCalibrationImpactFilterTest.java | 20 (exposes prod bug at UnitCalibrationImpactFilter.java:46) | Test does not catch reference-equality (`!=`) bug in production comparator |
| A107-4 | LOW | UnitCalibrationImpactFilterTest.java | 7 | Wildcard import `java.util.*` — inconsistent with sibling test file |
| A107-5 | MEDIUM | UnitCalibrationTest.java | 46-47, 59, 69-70 | Wall-clock timestamps sampled twice per test; tests are non-deterministic |
| A107-6 | MEDIUM | UnitCalibrationTest.java | 99 | Magic expected threshold value `1586027` with no derivation comment |
| A107-7 | LOW | UnitCalibrationTest.java | 11 | Wildcard import `org.junit.Assert.*` inconsistent with explicit java.util imports |
| A107-8 | LOW | UnitCalibrationTest.java | 102-107 | `makeImpacts` helper has no comment explaining synthetic zero-based values |
| A107-9 | INFO | UnitCalibrationTest.java | 33 | Missing exact-100 boundary test; name says "more than hundred" |
| A107-10 | INFO | UnitCalibrationImpactFilterTest.java | 15 | `@Before` method named `before()` rather than conventional `setUp()` |
# Pass 4 (Code Quality) — Agent A108
**Audit date:** 2026-02-26
**Assigned files:**
- `src/test/java/com/calibration/UnitCalibratorTest.java`
- `src/test/java/com/util/ImpactUtilTest.java`

---

## Reading Evidence

### File 1: `src/test/java/com/calibration/UnitCalibratorTest.java`

**Class:** `com.calibration.UnitCalibratorTest`

**Fields:**
- `unitCalibrator` — `UnitCalibrator` (line 12)
- `unitCalibrationGetter` — `UnitCalibrationGetter` (line 14)
- `unitCalibrationEnder` — `UnitCalibrationEnder` (line 15)

**Methods:**

| Name | Line | Annotation |
|---|---|---|
| `before()` | 18 | `@Before` |
| `SetsThresholdOfUnitWithMoreThan100ValidImpacts()` | 26 | `@Test` |
| `DoesNotSetThresholdOfUnitWithLessThan100ValidImpacts()` | 36 | `@Test` |
| `SetsNewThresholdsWithMultipleUnits()` | 46 | `@Test` |
| `makeUnitToCalibrate(int unitId, int impactCount)` | 59 | `private static` |

**Types / constants defined:** none

**Imports used:**
- `org.junit.Before`, `org.junit.Test`
- `java.sql.SQLException`
- `java.util.*`
- `static org.mockito.Mockito.*`

---

### File 2: `src/test/java/com/util/ImpactUtilTest.java`

**Class:** `com.util.ImpactUtilTest`

**Fields:** none

**Methods:**

| Name | Line | Annotation |
|---|---|---|
| `ReturnsGForceForImpact()` | 10 | `@Test` |
| `ReturnsImpactLevelOfImpact()` | 15 | `@Test` |
| `ReturnsGForceRequiredForDifferentImpactLevels()` | 22 | `@Test` |
| `ReturnsCSSColorForImpactLevel()` | 29 | `@Test` |

**Types / constants defined:** none

**Imports used:**
- `com.bean.ImpactLevel`
- `org.junit.Test`
- `static org.junit.Assert.assertEquals`

---

## Findings

### UnitCalibratorTest.java

**A108-1 | MEDIUM | UnitCalibratorTest.java:26 | Non-standard test method naming convention (PascalCase instead of camelCase)**

All four test methods (`SetsThresholdOfUnitWithMoreThan100ValidImpacts`, `DoesNotSetThresholdOfUnitWithLessThan100ValidImpacts`, `SetsNewThresholdsWithMultipleUnits`) and the setup helper use PascalCase (capitalised first letter), which is not the Java naming convention for methods. Java method names must begin with a lowercase letter per the Java Language Specification and standard style guides (Google, Oracle). The same problem appears in `ImpactUtilTest` (see A108-5). This is a style inconsistency relative to the rest of the codebase where production methods all use camelCase.

Affected lines: 26, 36, 46, 59 in `UnitCalibratorTest.java`.

---

**A108-2 | HIGH | UnitCalibratorTest.java:42 | Use of deprecated `verifyZeroInteractions()` Mockito API**

`verifyZeroInteractions(unitCalibrationEnder)` at line 42 calls a method that was deprecated in Mockito 3.x in favour of `verifyNoMoreInteractions()`. The project declares `mockito-all:1.10.19` (pom.xml line 356), so the call is not yet deprecated in the version pinned, but `mockito-all` itself is a legacy fat-jar artifact that was superseded by `mockito-core`. If the dependency is ever upgraded (the idiomatic migration path) the method becomes a compile-time deprecation warning. This should be noted as a build-warning risk tied to a known deprecated artifact.

More precisely: `mockito-all` is listed in the official Mockito changelog as a deprecated distribution from Mockito 2.x onward. Using it with `verifyZeroInteractions` combines two stale patterns in one test.

---

**A108-3 | MEDIUM | UnitCalibratorTest.java:62 | Non-deterministic test data via `Random` with no fixed seed**

`makeUnitToCalibrate` (line 60–66) constructs impact lists using `new Random()` with no fixed seed. The test `SetsThresholdOfUnitWithMoreThan100ValidImpacts` only verifies that `endCalibration` is called with `unitToCalibrate.getCalculatedThreshold()`, which is derived from the same random list, so the arithmetic is self-consistent. However, `getCalculatedThreshold()` is package-private on `UnitCalibration` (not part of any public contract), meaning the test is tightly coupled to the internal computation of `UnitCalibration.getCalculatedThreshold()` rather than asserting any concrete business value. If the threshold calculation logic changes, the test passes trivially regardless of whether the new logic is correct, because the expected value is computed by the same (possibly broken) method. Using unseeded Random also means that if a future bug is triggered only by specific impact values, it becomes difficult to reproduce.

---

**A108-4 | LOW | UnitCalibratorTest.java:7 | Wildcard import `java.util.*`**

Line 7 uses a wildcard import. The only `java.util` types used in the file are `Random`, `ArrayList`, `List`, `Arrays`, and `Collections`. Wildcard imports obscure exactly which types are in scope, may silently pick up new types added to a package in future JDK versions, and are flagged as a style violation by Checkstyle's `AvoidStarImport` rule. The project has `-Xlint:all` enabled in the compiler plugin (pom.xml line 93), which does not flag star imports at the compiler level, but they remain a style issue.

---

### ImpactUtilTest.java

**A108-5 | MEDIUM | ImpactUtilTest.java:10 | Non-standard test method naming convention (PascalCase instead of camelCase)**

All four test methods (`ReturnsGForceForImpact`, `ReturnsImpactLevelOfImpact`, `ReturnsGForceRequiredForDifferentImpactLevels`, `ReturnsCSSColorForImpactLevel`) start with an uppercase letter, violating the Java method naming convention. This is the same pattern as `UnitCalibratorTest` (A108-1), indicating this is a codebase-wide style inconsistency in the test layer.

Affected lines: 10, 15, 22, 29.

---

**A108-6 | HIGH | ImpactUtilTest.java:15 | Missing test case: `calculateImpactLevel` returns `null` for below-threshold impacts; no assertion for that branch**

`ImpactUtil.calculateImpactLevel` (production code line 49) explicitly returns `null` when `impactValue <= impactThreshold * BLUE_IMPACT_COEFFICIENT`. The test `ReturnsImpactLevelOfImpact` (lines 15–19) only exercises `BLUE`, `AMBER`, and `RED` paths. The null-return path — representing an impact below the minimum threshold — is completely unexercised. This is a significant missing-assertion gap: callers of `calculateImpactLevel` that do not null-check would throw a `NullPointerException` at runtime, and this test suite gives no coverage of that case. This is also a test quality issue since the method's contract includes a documented null return.

---

**A108-7 | MEDIUM | ImpactUtilTest.java:23 | Magic numeric literals used as test inputs with no explanation of their derivation**

The expected G-force values `2.7435`, `6.1348`, `8.6759` and the threshold input `500000` appear as bare magic numbers in `ReturnsGForceForImpact` (line 11) and `ReturnsGForceRequiredForDifferentImpactLevels` (lines 23–25). There is no comment or constant explaining that these are pre-computed from `G_FORCE_COEFFICIENT * sqrt(threshold * coefficient)`. If the production formula or coefficient changes, a reviewer cannot tell without manual recalculation whether the expected values are correct or simply stale. At minimum, constants or inline comments should document the derivation.

---

**A108-8 | LOW | ImpactUtilTest.java:30 | Inconsistent CSS color representation leaks into test assertions**

`ReturnsCSSColorForImpactLevel` (lines 29–33) asserts that `BLUE` returns the string `"blue"` and `RED` returns `"red"` (lowercase named colours) while `AMBER` returns `"#FFBF00"` (a hex code). This inconsistency in the production API — mixing named strings and hex codes — is directly reflected in the test, which enshrines the inconsistency without flagging it. The test does not assert anything wrong (the production behaviour matches), but the inconsistency in the API contract itself is surfaced here and represents a leaky abstraction: callers must know that AMBER behaves differently from the other two levels. The test is evidence of the design smell but does not guard against it being rationalised.

---

## Summary

| ID | Severity | File | Short description |
|---|---|---|---|
| A108-1 | MEDIUM | UnitCalibratorTest.java:26 | PascalCase test method names (non-standard Java convention) |
| A108-2 | HIGH | UnitCalibratorTest.java:42 | Deprecated `verifyZeroInteractions` + deprecated `mockito-all` artifact |
| A108-3 | MEDIUM | UnitCalibratorTest.java:62 | Unseeded `Random` + self-referential threshold assertion hides logic errors |
| A108-4 | LOW | UnitCalibratorTest.java:7 | Wildcard import `java.util.*` |
| A108-5 | MEDIUM | ImpactUtilTest.java:10 | PascalCase test method names (non-standard Java convention) |
| A108-6 | HIGH | ImpactUtilTest.java:15 | Missing assertion for `calculateImpactLevel` null-return (below-threshold) path |
| A108-7 | MEDIUM | ImpactUtilTest.java:23 | Magic numeric literals without derivation comments |
| A108-8 | LOW | ImpactUtilTest.java:30 | Inconsistent CSS color representation (named vs hex) enshrined in test |
# P4 Agent A11 — AdminUnitEditAction, AdminUnitImpactAction

## Reading Evidence

### AdminUnitEditAction
- Class: `AdminUnitEditAction` extends `Action` (line 19)
- Fields:
  - `unitDao` : `UnitDAO` (line 20) — instance field, private
- Methods:
  - `execute` (line 22) — public
  - `writeJsonResponse` (line 72) — private
  - `validate` (line 78) — private
- Constants/Types: none defined

### AdminUnitImpactAction
- Class: `AdminUnitImpactAction` extends `Action` (line 17)
- Fields:
  - `log` : `Logger` (line 18) — private static
- Methods:
  - `execute` (line 20) — public
- Constants/Types: none defined

---

## Findings

A11-1 | MEDIUM | AdminUnitEditAction.java:20 | **Mixed DAO access pattern — instance field vs. direct static calls.** `unitDao` is stored as a private instance field (`UnitDAO.getInstance()`) but the same singleton is also accessed directly via `UnitDAO.getInstance()` on lines 37, 41, and 45. Lines 37, 41, 45 call `UnitDAO.getInstance()` inline rather than using the cached `unitDao` field, creating an inconsistency within the same class. This is also present in `AdminUnitImpactAction` (line 32) which calls `UnitDAO.getInstance()` directly with no field at all.

A11-2 | MEDIUM | AdminUnitEditAction.java:34 | **Mixed DAO access pattern — ManufactureDAO accessed inline only.** `ManufactureDAO.getInstance().getAllManufactures(compId)` is called inline without caching the instance as a field, while `UnitDAO` has a cached field. This inconsistency in style makes field ownership unclear and could hide lifecycle issues.

A11-3 | LOW | AdminUnitImpactAction.java:18 | **Declared but never used logger.** `private static Logger log` is declared and assigned via `InfoLogger.getLogger(...)` but is never called anywhere in the class body. This is dead code and will produce a compiler/IDE unused-field warning.

A11-4 | LOW | AdminUnitImpactAction.java:26 | **Redundant null check after null-safe initialisation.** `action` is assigned on line 21 with a null-safe ternary (`== null ? "" : ...`), guaranteeing it is never null. The subsequent `if (action == null || action.equals(""))` on line 26 retains the null branch, which is unreachable. Only the `action.equals("")` branch is reachable. This is dead code within the condition.

A11-5 | LOW | AdminUnitEditAction.java:36-47 | **`opCode` emptiness check duplicated three times.** `StringUtils.isNotEmpty(opCode)` is repeated in every branch of the if/else-if chain instead of being checked once before the chain. The repeated expression is not incorrect but is a style/maintainability issue consistent across neither this file nor the rest of the codebase's pattern of single guards.

A11-6 | LOW | AdminUnitEditAction.java:10 | **Wildcard import.** `import org.apache.struts.action.*;` is a wildcard import. All other imports in the file are explicit. The wildcard is inconsistent with the file's own import style and with `AdminUnitImpactAction.java`, which uses explicit individual Struts imports (`ActionForm`, `ActionForward`, `ActionMapping` each on separate lines).

A11-7 | LOW | AdminUnitEditAction.java:26 | **Raw `ActionForm` cast without guard.** The cast `(AdminUnitEditForm) actionForm` on line 26 is performed without an `instanceof` check. If the framework ever routes a wrong form to this action the unchecked cast will throw a `ClassCastException` at runtime with no informative error message. `AdminUnitImpactAction` has the same pattern (line 24), so this is a cross-file consistency issue as well as a safety concern.

A11-8 | INFO | AdminUnitImpactAction.java:35-36 | **Else branch is effectively a no-op.** When `action` is not `reset_calibration` (or is blank), the action unconditionally forwards to `"success"`. There is no indication that a blank or unrecognised action value is treated differently from a successful reset. A caller that passes no action gets a success forward, which may mask missing or incorrect input silently.

A11-9 | INFO | AdminUnitEditAction.java:22-25 vs AdminUnitImpactAction.java:20 | **Inconsistent `execute` signature formatting across the two files.** `AdminUnitEditAction` formats the four parameters across multiple indented lines (lines 22-25), while `AdminUnitImpactAction` places all four parameters on a single long line (line 20, ~120 characters). Neither is wrong in isolation, but the inconsistency across files in the same package suggests no enforced formatting standard.
# P4 Agent A12 — AdminUnitServiceAction, AppAPIAction

## Reading Evidence

### AdminUnitServiceAction

- Class: `AdminUnitServiceAction` extends `Action` (line 17)
- Fields:
  - `log` — `private static Logger` (line 19)
- Methods:
  - `execute` (line 21) — `public ActionForward execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse) throws Exception`
- Constants/Types defined: none

### AppAPIAction

- Class: `AppAPIAction` extends `Action` (line 38)
- Fields:
  - `log` — `private static Logger` (line 40)
- Methods:
  - `execute` (line 42) — `public ActionForward execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse) throws Exception`
- Constants/Types defined: none

---

## Findings

A12-1 | HIGH | AppAPIAction.java:45-371 | **Massive commented-out code block — entire method body disabled.** Lines 45–371 consist of a single contiguous block of code commented out with `////` prefixes. This is the complete implementation of the `execute` method (login, driver, vehicle, attachment, question, result, and PDF-report handling). The only live statements are an uncommented `request.setAttribute("method", action)` reference (line 371, itself partially commented — the `setAttribute` call has its leading `//` removed but `action` variable is never set) and `return mapping.findForward("apiXml")` (line 372). The class is effectively a no-op stub left in the codebase. This indicates either an abandoned API or a feature that was disabled by bulk commenting rather than a proper feature flag, branch, or removal.

A12-2 | HIGH | AppAPIAction.java:371 | **Partially de-commented line references an undeclared variable.** Line 371 reads `request.setAttribute("method", action);` — this line has had its leading `//` removed while its surrounding block remains commented out. The variable `action` is never declared in any live (non-commented) scope of the method. This will cause a compilation failure if the line is ever uncommented cleanly, and currently signals confusion about which lines are intentionally active.

A12-3 | MEDIUM | AdminUnitServiceAction.java:27 | **Redundant null check after null-safe assignment.** Line 23 assigns `action` via a null-safe ternary: `String action = request.getParameter("action") == null ? "" : request.getParameter("action");`, guaranteeing `action` is never `null`. Line 27 then checks `if (action == null || action.equals(""))`. The `action == null` branch can never be true. The dead null guard is misleading and adds noise.

A12-4 | MEDIUM | AppAPIAction.java:4-36 | **Unused imports — dead import declarations.** Because the entire method body is commented out, none of the following imported types are referenced in any live code: `java.sql.Connection`, `java.sql.Timestamp`, `java.util.ArrayList`, `java.util.Date`, `org.apache.struts.Globals`, `org.apache.struts.util.PropertyMessageResources`, `com.bean.AttachmentBean`, `com.bean.CompanyBean`, `com.bean.DriverBean`, `com.bean.QuestionBean`, `com.bean.UnitBean`, `com.dao.CompanyDAO`, `com.dao.DriverDAO`, `com.dao.LoginDAO`, `com.dao.QuestionDAO`, `com.dao.UnitDAO`, `com.pdf.FleetCheckPDF`, `com.util.DBUtil`, `com.util.DateUtil`, `com.util.RuntimeConf`, `com.util.Util`. This will produce compiler/IDE warnings for every unused import and pollutes the dependency surface of the class.

A12-5 | MEDIUM | AdminUnitServiceAction.java:44-50 | **Magic numbers in business logic with no named constants.** The service-status thresholds `5` and `25` (hours) are used directly in inline comparisons with no symbolic names or explanatory constants. The status string for `< 5` says "less than 5 hours **or service is overdue**" but the `< 25` string says only "less than 25 hours" with no overdue mention — the asymmetry is a potential correctness issue and the magic literals make future threshold changes error-prone.

A12-6 | LOW | AppAPIAction.java:38 | **Style inconsistency — missing space before opening brace in class declaration.** `AppAPIAction.java` declares `public class AppAPIAction extends Action{` (no space before `{`), while `AdminUnitServiceAction.java` correctly writes `public class AdminUnitServiceAction extends Action {` (space before `{`). Inconsistent within the same package.

A12-7 | LOW | AppAPIAction.java:42-44 | **Inconsistent indentation in method signature.** The `execute` method opening in `AppAPIAction.java` uses a two-space indent for the method and irregular tab/space mixing across lines 42–44, deviating from the four-space / tab convention used in `AdminUnitServiceAction.java` and elsewhere in the project.

A12-8 | LOW | AdminUnitServiceAction.java:62 | **Inconsistent whitespace — trailing tab on otherwise clean line.** Line 62 (`UnitDAO.getInstance().saveService(serviceBean);`) is followed by a line containing only a tab character before the blank line, breaking the uniform blank-line style of the rest of the file.

A12-9 | INFO | AdminUnitServiceAction.java:19, AppAPIAction.java:40 | **Deprecated logging API (Apache Log4j 1.x).** Both files import `org.apache.log4j.Logger` (Log4j 1.x), which reached end-of-life in August 2015 and has known critical CVEs (e.g., CVE-2019-17571). The project should migrate to Log4j 2.x or SLF4J/Logback.

A12-10 | INFO | AdminUnitServiceAction.java:17, AppAPIAction.java:38 | **Deprecated framework — Apache Struts 1.x.** Both classes extend `org.apache.struts.action.Action`, which is the Struts 1 base class. Struts 1 reached end-of-life in December 2013 and receives no further security patches. This is a project-wide concern noted here for completeness.
# P4 Agent A13 — BarCodeAction, CalibrationAction

## Reading Evidence

### BarCodeAction

- Class: `BarCodeAction` extends `Action` (line 28)
- Fields:
  - `private UnitDAO unitDAO` (line 30) — instance-level singleton reference
- Methods:
  - `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` (line 33)
- Constants/Types defined in file: none
- External constants referenced: `RuntimeConf.API_BARCODE`, `RuntimeConf.Load_BARCODE`, `RuntimeConf.CHECKLIST_SECONDS`

### CalibrationAction

- Class: `CalibrationAction` extends `Action` (line 12)
- Fields: none
- Methods:
  - `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` (line 14)
- Constants/Types defined in file: none

---

## Findings

A13-1 | MEDIUM | BarCodeAction.java:201-210 | **Commented-out code block (debug print statements)**
Lines 201–210 contain a large block of `System.out.print` debug statements left commented out. This is dead, noise-generating commented code that should be removed before production commit. The block logs driver id, unit id, time, comp id, and individual answers.

```java
//            	System.out.print("start\n");
//            	System.out.print("driver id:"+resultBean.getDriver_id()+"\n");
// ...
//				System.out.print("end\n");
```

A13-2 | MEDIUM | BarCodeAction.java:109-110 | **Commented-out code (inline comment describing logic that was never implemented or removed)**
Lines 109–110 and 140–141 contain commented-out prose descriptions of intended logic ("compare previous and current unit, previous time and current time, if time is more than 30 mins, missing end tag, split codes"). While these may be intent comments rather than code, they duplicate each other verbatim across two locations and describe logic that is already present in the surrounding code, making them misleading and redundant noise. Should be removed or replaced with a single, clear Javadoc/block comment.

A13-3 | HIGH | BarCodeAction.java:242 | **Swallowed exception — `e.getMessage()` return value discarded**
Inside the catch block on line 242, `e.getMessage()` is called but its return value is not used (not logged, not set as attribute, not rethrown). Only `e.printStackTrace()` follows. This silently discards the error message from the user-visible response and provides no structured logging. The method `msg` string is not updated on exception, so the UI may silently succeed with empty feedback.

```java
}catch(Exception e){
    e.getMessage();   // return value discarded — no-op
    e.printStackTrace();
}
```

A13-4 | HIGH | BarCodeAction.java:50 | **Unguarded `ArrayList.get(0)` — potential `IndexOutOfBoundsException`**
`unitDAO.getUnitBySerial(serial, true)` returns an `ArrayList<UnitBean>` and `.get(0)` is called immediately without checking that the list is non-null and non-empty. If no unit matches the serial, this throws an unhandled `IndexOutOfBoundsException` that will propagate to the Struts framework as an uncontrolled 500 error.

```java
ArrayList<UnitBean> arrUnit = unitDAO.getUnitBySerial(serial, true);
String vehId = arrUnit.get(0).getId();   // no size check
```

The same pattern recurs on lines 55 (`companies.get(0)`), 198 (`arrUnit.get(0).getComp_id()`), and 220 (`companyDao.getCompanyByCompId(compId).get(0)`).

A13-5 | HIGH | BarCodeAction.java:192 | **`ResultDAO` instantiated with `new` while `UnitDAO` and `CompanyDAO` use singletons**
`ResultDAO resultDAO = new ResultDAO()` (line 192) creates a new instance each time the method executes. By contrast, `UnitDAO` (line 30) is obtained via `UnitDAO.getInstance()` and `CompanyDAO` (line 40) via `CompanyDAO.getInstance()`. This is an inconsistent object-lifecycle pattern and a leaky abstraction: it couples the action directly to DAO construction semantics and bypasses any connection pooling or caching the singleton pattern may provide.

A13-6 | MEDIUM | BarCodeAction.java:58 | **Typo in local variable name: `resutl_id`**
The variable is named `resutl_id` (line 58, repeated on line 193). The correct spelling is `result_id`. Additionally, the naming mixes `snake_case` with the otherwise mostly-camelCase convention used elsewhere (e.g., `vehId`, `compId`, `driverId`, `sendres`). This same misspelled name appears in both the `API_BARCODE` and `Load_BARCODE` branches.

A13-7 | LOW | BarCodeAction.java:81 | **Typo in user-visible error string: "Invalid Fomrat!"**
Line 81: `"Corrupted Data! Invalid Fomrat!"` — "Fomrat" should be "Format". This string is set as a request attribute (`msg`) and is likely displayed to end users.

A13-8 | LOW | BarCodeAction.java:235 | **Typo in user-visible error string: "succusfull"**
Line 235: `"Duplicated Data! Please delete the data after succusfull loading!"` — "succusfull" should be "successful".

A13-9 | MEDIUM | BarCodeAction.java:57 | **Direct instantiation of `FleetcheckAction` from within another Action class (tight coupling / leaky abstraction)**
Lines 57 and 86 instantiate `FleetcheckAction` directly inside `BarCodeAction`. Business logic (`saveResult`, `saveResultBarcode`, `sendFleetCheckAlert`) is accessed by constructing a sibling Action rather than calling a shared service/façade layer. This creates tight coupling between two web-tier Action classes; `FleetcheckAction` is being used as a service façade, exposing its internal methods as a public interface to peer classes.

```java
FleetcheckAction fleetcheckAction = new FleetcheckAction();
int resutl_id = fleetcheckAction.saveResult(...);
```

A13-10 | LOW | BarCodeAction.java:36 | **`// TODO Auto-generated method stub` left in production code**
Line 36 retains the IDE-generated TODO comment from the initial method stub. It should be removed.

A13-11 | LOW | BarCodeAction.java:28 | **Missing space before opening brace in class declaration**
Line 28: `public class BarCodeAction extends Action{` — no space before `{`. `CalibrationAction` (line 12) correctly uses `public class CalibrationAction extends Action {` with a space. Minor but a cross-file style inconsistency.

A13-12 | MEDIUM | BarCodeAction.java:85 | **Raw type usage: `new ArrayList<ResultBean>()` vs. inferred — minor; but `ResultBean` list items never type-checked**
More critically, `String[] result = barcode.split("END")` (line 84) can produce a single-element array when no "END" delimiter is present (barcode has no END) — the loop then processes potentially malformed data without guard. This is a logic robustness issue in the barcode-parsing path, not a compiler warning, but closely related to raw-type/unchecked risk.

A13-13 | INFO | CalibrationAction.java:20 | **`super.execute()` returns `null` by default in Struts `Action`**
`return super.execute(mapping, form, request, response)` (line 20) delegates to `Action.execute()`, which by Struts contract returns `null`. Returning `null` causes Struts to not forward anywhere, which may be intentional for a trigger-only action, but it is implicit. If future logic requires a forward, this pattern will silently do nothing. At minimum this warrants a comment documenting intent.

A13-14 | INFO | BarCodeAction.java:66 | **Mixed casing in `RuntimeConf` constant name: `RuntimeConf.Load_BARCODE`**
The constant `Load_BARCODE` uses mixed casing (initial uppercase then underscore then uppercase). The companion constant `API_BARCODE` (line 42) follows the standard `ALL_CAPS_SNAKE_CASE` Java constant convention. This is a style inconsistency in `RuntimeConf` surfacing visibly in this file.
# P4 Agent A14 — DealerCompaniesAction, DealerImpactReportAction

## Reading Evidence

### DealerCompaniesAction
- Class: `DealerCompaniesAction` extends `org.apache.struts.action.Action`
- Methods:
  - `execute` (line 20)
- Constants/Types: none defined in this file

### DealerImpactReportAction
- Class: `DealerImpactReportAction` extends `org.apache.struts.action.Action`
- Methods:
  - `execute` (line 19)
- Constants/Types: none defined in this file

---

## Findings

A14-1 | HIGH | DealerCompaniesAction.java:26 | Null-dereference risk with no guard on session. `request.getSession(false)` can return `null` if no session exists, and `session.getAttribute("sessCompId")` is called unconditionally on the next line. If the session is absent the method throws a `NullPointerException` rather than a controlled authentication error. By contrast, `DealerImpactReportAction` (line 23–25) applies the same `getSession(false)` pattern but at least performs a null check on the retrieved attribute value. Neither class guards against a null session itself.

A14-2 | HIGH | DealerCompaniesAction.java:26 | Unsafe `toString()` cast on session attribute. `session.getAttribute("sessCompId").toString()` will throw `NullPointerException` if the attribute is absent or the session is stale. `DealerImpactReportAction` uses the safer explicit cast `(String) session.getAttribute("sessCompId")` followed by a null check (line 24–25). The two sibling action classes are inconsistent in their defensive style, with `DealerCompaniesAction` being the less safe variant.

A14-3 | MEDIUM | DealerCompaniesAction.java:25 | Double call to `request.getParameter("action")`. The ternary expression `request.getParameter("action") == null ? "" : request.getParameter("action")` calls the method twice. The first call evaluates the null condition and the second call retrieves the value. This should be a single call with the result stored in a local variable before the comparison.

A14-4 | MEDIUM | DealerImpactReportAction.java:30 | Redundant `Long.valueOf` boxing. `Long.valueOf(sessCompId)` produces a `Long` object. The result `compId` is passed directly to `ReportService.getInstance().getImpactReport(compId, ...)` which is likely typed `long` or `Long`. Using `Long.parseLong(sessCompId)` is more idiomatic and avoids autoboxing ambiguity. This is a minor style/efficiency issue but is inconsistent with how `DealerCompaniesAction` uses `CompanyDAO.getSubCompanies(companyId)` passing the raw `String` directly.

A14-5 | MEDIUM | DealerImpactReportAction.java:25 | Exception type leaks implementation detail to callers. Throwing `new RuntimeException("Must have valid user logged in here")` from an HTTP Action class is a leaky abstraction: the message is developer-facing, not user-facing, and an uncaught `RuntimeException` in a Struts action will propagate as a 500 error with no controlled forward. A named exception or a redirect to a login forward would be more appropriate.

A14-6 | MEDIUM | DealerImpactReportAction.java:27–29 | Unused local variables `dateFormat`, `dateTimeFormat`, `timezone`. `dateFormat` is consumed at line 37 via `searchForm.getImpactReportFilter(dateFormat)`, and `dateTimeFormat` and `timezone` are passed at lines 38–39. These are all used, so this finding does not apply. (No finding raised — see A14-7 instead for the actual unused-variable concern.)

A14-7 | LOW | DealerImpactReportAction.java:32 | `ImpactReportSearchForm.timezone` field is populated from the form submission but `DealerImpactReportAction` reads `timezone` from the session (line 29) and passes it directly to `ReportService`. The form's own `timezone` field (defined in `ImpactReportSearchForm` line 23 and included in the Lombok `@Data` getter/setter) is never written by this action, meaning the session value silently overrides any timezone that the form might carry. This is a latent leaky-abstraction issue: the form declares a `timezone` field implying it is part of the search filter, but the action discards it.

A14-8 | LOW | DealerCompaniesAction.java:11–12 | Partially redundant imports. `java.util.ArrayList` is imported and used at line 29 (`new ArrayList<>()`). `java.util.List` is also imported and used at line 29 for the variable type declaration. Both are genuinely used; however the action's entire body could use `List` on the left-hand side with `new ArrayList<>()`, which it already does correctly. No unused import exists here — this is informational only. (No finding raised.)

A14-9 | LOW | DealerImpactReportAction.java:34 | Mixed static-method and singleton-instance access styles within the same method. `ManufactureDAO.getAllManufactures(sessCompId)` is called as a static method (line 33) while `UnitDAO.getInstance().getAllUnitType()` is called via a singleton instance (line 34), and `ReportService.getInstance().getImpactReport(...)` is also called via singleton (line 36). The inconsistency in access patterns suggests the DAOs have not been designed to a single convention. This is a cross-file style inconsistency visible within this action.

A14-10 | INFO | DealerCompaniesAction.java:28 | Case-insensitive action comparison via `equalsIgnoreCase("add")` is inconsistent with the rest of the codebase. Many other action classes use plain `equals` for action parameter dispatch. The use of `equalsIgnoreCase` silently accepts `"ADD"`, `"Add"`, etc., which may or may not be intentional. The inconsistency should be documented or normalised.
# P4 Agent A15 — DealerIncidentReportAction, DealerPreOpsReportAction

## Reading Evidence

### DealerIncidentReportAction
- Class: `DealerIncidentReportAction` extends `org.apache.struts.action.Action` (line 17)
- Methods:
  - `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` (line 19) — overrides `Action.execute`, throws `Exception`
- Constants/Types: none defined

### DealerPreOpsReportAction
- Class: `DealerPreOpsReportAction` extends `org.apache.struts.action.Action` (line 17)
- Methods:
  - `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` (line 19) — overrides `Action.execute`, throws `Exception`
- Constants/Types: none defined

---

## Findings

A15-1 | HIGH | DealerIncidentReportAction.java:30 vs DealerPreOpsReportAction.java:27 | **Type inconsistency for company ID across sibling classes.** `DealerIncidentReportAction` parses `sessCompId` as `int` via `Integer.parseInt(sessCompId)` (line 30) and passes it to `ReportService.getIncidentReport(int compId, ...)`. `DealerPreOpsReportAction` converts the same session attribute to `Long` via `Long.valueOf(sessCompId)` (line 27) and passes it to `ReportService.getPreOpsCheckReport(Long compId, ...)`. The underlying data is the same company ID originating from the same session key, but the two call paths use different primitive/wrapper types. This inconsistency indicates either the service layer has mismatched signatures or one of the action classes is silently narrowing (int) or unnecessarily boxing (Long) the value, creating a maintenance trap and potential overflow risk if the int path is used against a large company ID.

A15-2 | MEDIUM | DealerIncidentReportAction.java:23 | **Null session not guarded before attribute access.** `request.getSession(false)` on line 23 can return `null` if no session exists, but the result is used immediately on line 24 without a null check (`session.getAttribute(...)`). The null check on line 25 guards only the *attribute value*, not the session object itself. A request arriving with no established session will throw a `NullPointerException` rather than producing a controlled error response. The same pattern exists in `DealerPreOpsReportAction.java` line 23, making this a cross-file consistency issue in addition to a correctness defect.

A15-3 | MEDIUM | DealerPreOpsReportAction.java:23 | **Null session not guarded before attribute access (same as A15-2 in sibling class).** `request.getSession(false)` can return `null`; the return value is used on line 24 without a null check.

A15-4 | MEDIUM | DealerIncidentReportAction.java:25 | **`RuntimeException` thrown for an expected authentication failure.** Using an unchecked `RuntimeException` with the message `"Must have valid user logged in here"` to signal an unauthenticated request is an inappropriate exception type for a web-layer access-control check. This will produce an unhandled 500 error rather than a redirect to a login page, and the exception message leaks an internal expectation to any error page visible to the user. The identical pattern exists on `DealerPreOpsReportAction.java` line 25.

A15-5 | MEDIUM | DealerPreOpsReportAction.java:25 | **`RuntimeException` thrown for an expected authentication failure (same as A15-4 in sibling class).**

A15-6 | LOW | DealerIncidentReportAction.java:27-29 vs DealerPreOpsReportAction.java:28-30 | **Declaration order inconsistency between sibling classes.** In `DealerIncidentReportAction`, `companyId` is declared and assigned on line 30 *after* the three format/timezone strings (lines 27-29). In `DealerPreOpsReportAction`, `compId` is declared on line 27 *before* the format/timezone strings (lines 28-30). These two classes are structural twins; the differing variable declaration order makes the code harder to read and compare, and suggests they were edited independently rather than maintained as a pair.

A15-7 | LOW | DealerIncidentReportAction.java:17 | **Deprecated Struts 1 framework.** Both classes extend `org.apache.struts.action.Action`, which is part of Apache Struts 1. Struts 1 reached end-of-life in 2013 and has known CVEs. While this is an architectural concern rather than a per-class code defect, both files exhibit direct coupling to this deprecated API with no abstraction layer, meaning any future migration must touch every action class directly.

A15-8 | INFO | DealerIncidentReportAction.java:33-34 | **Static DAO method calls bypass any dependency-injection container.** Both classes call `ManufactureDAO.getAllManufactures(sessCompId)` and `UnitDAO.getAllUnitType()` as static methods and call `ReportService.getInstance()` as a singleton. This tight coupling to concrete static/singleton implementations makes the classes untestable in isolation and constitutes a leaky abstraction (the action layer directly names specific DAO implementation classes). The pattern is consistent across both files, so it is reported once at INFO to record the architectural observation.
# P4 Agent A16 — DealerSessionReportAction, DriverJobDetailsAction

## Reading Evidence

### DealerSessionReportAction

- **Class:** `DealerSessionReportAction` extends `org.apache.struts.action.Action` (line 17)
- **Methods:**
  - `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` (line 19) — overrides `Action.execute`
- **Constants/Types:** None defined

### DriverJobDetailsAction

- **Class:** `DriverJobDetailsAction` extends `org.apache.struts.action.Action` (line 24)
- **Methods:**
  - `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` (line 31)
- **Fields (instance):**
  - `private static Logger log` (line 26)
  - `private UnitDAO unitDao` (line 28)
  - `private DriverDAO driverDao` (line 29)
- **Constants/Types:** None defined

---

## Findings

A16-1 | HIGH | DriverJobDetailsAction.java:41 | String compared with `==` instead of `.equals()`. The expression `action == ""` on line 41 compares object references, not string content. Because `action` was already set to the empty string literal `""` on line 36 via a ternary, this reference comparison will never be `true` at runtime (the JVM does not guarantee interning of runtime-produced strings), so the null-guard/form-fallback branch (`action = form.getAction()`) is never reached even when the parameter was absent. The compound condition `action == null || action == ""` effectively degenerates to the null check only. This is a logic bug that silently discards the form's `action` value.

A16-2 | HIGH | DriverJobDetailsAction.java:45 | Unreachable null check for `action`. By line 45 `action` has already been guaranteed non-null by the ternary on line 36 (and by line 42 at the latest), so `if (action == null)` can never be true. This dead branch provides a false impression of defensive coding while affording no actual protection.

A16-3 | MEDIUM | DriverJobDetailsAction.java:44 | Commented-out `System.out.println(action)` left in production source (`//System.out.println(action);`). This is debug output that was never removed.

A16-4 | MEDIUM | DriverJobDetailsAction.java:59,65 | Two identical commented-out `request.setAttribute("driverList", ...)` lines were left in the source across separate branches (`// request.setAttribute("driverList", form.getDriverList());`). Dead/commented-out code left in both the `assign` and `assign_driver` branches without explanation.

A16-5 | MEDIUM | DriverJobDetailsAction.java:62 | `System.out.println(form.getJobTitle())` is a debug print statement left in the production `assign_driver` handler. Console output in a production action class is inappropriate; a logger is already available (`log`) but unused here.

A16-6 | MEDIUM | DriverJobDetailsAction.java:26 | The `log` field (`private static Logger log`) is declared but never used anywhere in the class body. This is dead code and will produce a compiler/IDE warning for an unused private field.

A16-7 | MEDIUM | DriverJobDetailsAction.java:52 | Raw/concrete type `ArrayList<JobDetailsBean>` used for the local variable (and presumably as the return type of `jobsDAO.getJobListByJobId`). The parameter type for `request.setAttribute` accepts `Object`, so there is no need to bind to the concrete `ArrayList` implementation; `List<JobDetailsBean>` should be used consistently, as is done on lines 57 and 63. This is an inconsistency within the same file.

A16-8 | MEDIUM | DriverJobDetailsAction.java:50 | `JobsDAO` is instantiated inline with `new JobsDAO()` inside the action method, while `UnitDAO` and `DriverDAO` are injected as instance fields (lines 28–29). This is an inconsistent dependency management pattern within the same class: two DAOs are pre-instantiated at field level and one is created ad-hoc in the method body, indicating leaky construction responsibility and making the `JobsDAO` dependency untestable/unexchangeable without changing the method.

A16-9 | LOW | DealerSessionReportAction.java:34-35 | Static method calls on DAO classes (`UnitDAO.getAllUnitsByCompanyId`, `DriverDAO.getAllDriver`) are made directly from the action layer, while `DriverJobDetailsAction` calls identical DAO functionality via instance fields (`driverDao.getAllDriver`). Across the two files the same DAO layer is accessed via two different styles (static call vs. instance method), indicating inconsistent abstraction and coupling patterns between action classes in the same package.

A16-10 | LOW | DealerSessionReportAction.java:25 | `session.getAttribute("sessCompId")` is retrieved but no null-check is applied before calling `session.getAttribute` itself — i.e., if `request.getSession(false)` returns `null` (no existing session), line 23 assigns `null` to `session` and line 24 will throw a `NullPointerException` rather than a controlled error. The RuntimeException on line 25 only fires after the NPE would have already occurred if the session is absent.

A16-11 | LOW | DriverJobDetailsAction.java:31 | `execute` is not annotated with `@Override`. `DealerSessionReportAction.execute` (line 18–19) correctly uses `@Override`, but `DriverJobDetailsAction` omits it. This is a style inconsistency across the two files for the same method override.

A16-12 | LOW | DriverJobDetailsAction.java:32-33 | The `execute` method signature has inconsistent line-break formatting compared to `DealerSessionReportAction`. In `DealerSessionReportAction` each parameter is on its own line with consistent indentation (lines 20–22). In `DriverJobDetailsAction` parameters are split across lines 32–33 with `ActionForm actionForm` on the same line as the method name and the remaining parameters on the next line, which is irregular and inconsistent across the two files.

A16-13 | INFO | DealerSessionReportAction.java:37 | `ReportService.getInstance()` is called as a singleton, while DAOs in the same file are accessed via static methods, and DAOs in `DriverJobDetailsAction` are accessed via instance fields. There is no consistent pattern for service/DAO access across the two files, which reflects broader architectural inconsistency in the action layer.
# P4 Agent A17 — ExpireAction, FleetcheckAction

## Reading Evidence

### ExpireAction
- Class: `ExpireAction` extends `Action` (line 28)
- Methods:
  - `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` (line 32)
- Constants/Types:
  - `private static Logger log` (line 30) — static logger field, not a constant

### FleetcheckAction
- Class: `FleetcheckAction` extends `Action` (line 40)
- Methods:
  - `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` (line 44)
  - `saveResult(String, String[], String[], String[], String, Long, Timestamp, String)` (line 119)
  - `saveResultBarcode(String, Map<String, String>, String, String, Timestamp, String)` (line 142)
  - `sendFleetCheckAlert(PropertyMessageResources, String, int, CompanyBean, String[])` (line 162)
- Constants/Types:
  - `private static Logger log` (line 42) — static logger field, not a constant

---

## Findings

A17-1 | HIGH | FleetcheckAction.java:56 | **Raw/unchecked cast without suppression annotation** — `ArrayList<DriverBean> sessArrDriver` is cast from `session.getAttribute("arrDriver")` at line 56 without a `@SuppressWarnings("unchecked")` annotation. The equivalent cast for `sessArrComp` at line 50 does carry the annotation; line 56 is inconsistent and will produce an unchecked cast compiler warning.

A17-2 | HIGH | FleetcheckAction.java:119 | **Leaky abstraction — public business-logic methods on an Action class** — `saveResult` and `saveResultBarcode` (lines 119, 142) and `sendFleetCheckAlert` (line 162) are declared `public`. They contain DAO instantiation and persistence logic that belongs in a service or DAO layer. Exposing them as public methods on a Struts `Action` (which is a web-tier class) leaks the persistence layer contract into the web tier's public interface and makes the class directly callable/testable in ways that bypass the Struts lifecycle.

A17-3 | MEDIUM | FleetcheckAction.java:143 | **Inconsistent variable initialisation style** — In `saveResult` (line 120) `resutl_id` is initialised to `0` at declaration. In `saveResultBarcode` (line 143) `resutl_id` is declared without initialisation (`int resutl_id;`). The pattern is inconsistent within the same file.

A17-4 | MEDIUM | FleetcheckAction.java:77 | **Inconsistent local variable naming for the same DAO type** — The `QuestionDAO` local variable is named `questionDAO` (camelCase, line 58) in the `faulty` branch and `quesionDao` (mixed case, line 77) in the `restart` branch. Both names also perpetuate the pre-existing typo "quesion" (missing 't'), but the case style differs, making the code inconsistent within the same file.

A17-5 | MEDIUM | FleetcheckAction.java:96-98 | **Pervasive typo in identifier names used as public API** — The parameter names and local variables `quesion_ids` (line 96), `anwsers` (line 97), and `resutl_id` (lines 104, 120, 137, 143, 158) contain spelling errors (`quesion` for `question`, `anwsers` for `answers`, `resutl` for `result`). These typos appear in the public method signatures of `saveResult` and `saveResultBarcode` (lines 119, 142), making them part of the public API contract. Correcting them later would be a breaking change.

A17-6 | MEDIUM | ExpireAction.java:28 | **Formatting inconsistency — missing space before brace** — `ExpireAction extends Action{` (line 28) has no space before the opening brace. `FleetcheckAction extends Action {` (line 40 of FleetcheckAction.java) has a space. This is inconsistent across the two files.

A17-7 | MEDIUM | ExpireAction.java:32-34 | **Indentation inconsistency** — The `execute` method signature (lines 32–34) uses 2-space indentation for the method declaration relative to the class body, while the method body itself is indented with a deeper mix of tabs and spaces. FleetcheckAction uses consistent 4-space indentation throughout. The inconsistency is also visible within ExpireAction itself: the `execute` declaration starts at column 3 (2 spaces) while surrounding code uses tabs.

A17-8 | MEDIUM | FleetcheckAction.java:56-57 | **NullPointerException risk — unchecked session attribute access** — `sessArrDriver` at line 56 is retrieved from the session without a null check, then immediately dereferenced at line 57 (`sessArrDriver.get(0)`). If the session attribute `arrDriver` is absent or the list is empty, this will throw a `NullPointerException` or `IndexOutOfBoundsException` at runtime with no error handling. The same pattern recurs at line 91-92 in the `else` branch.

A17-9 | LOW | ExpireAction.java:4 | **Unused import** — `java.util.ArrayList` is imported (line 4) but never referenced anywhere in `ExpireAction.java`. This is dead code and will produce a compiler warning.

A17-10 | LOW | ExpireAction.java:7 | **Unused import** — `javax.servlet.ServletException` is imported (line 7) but is never declared thrown or caught in `ExpireAction.java`. This is dead code.

A17-11 | LOW | FleetcheckAction.java:4 | **Unused import** — `java.util.Date` is imported (line 4) but `Date` is used only as the return type of `DateUtil.getLocalTime` (line 61), assigned to `currentDate`. This import is used, however `java.sql.Timestamp` (line 3) and `java.util.ArrayList` (line 5) should be verified — both are used, so they are fine. `java.util.Date` is used at line 61, so this is not unused. However, `com.bean.AnswerBean` is imported (line 33) and used (lines 123, 148) — fine. `com.bean.QuestionBean` is imported (line 31) and used — fine. `org.apache.struts.Globals` is imported (line 13) and used at line 106 — fine. Re-checking: all FleetcheckAction imports appear to be used.

A17-12 | LOW | FleetcheckAction.java:162 | **Use of boxed `Boolean` return type where primitive `boolean` suffices** — `sendFleetCheckAlert` declares its return type as `Boolean` (the boxed wrapper) and initialises `sendres` to `false`. The method never returns `null`, so the boxed type provides no benefit and introduces an unnecessary autoboxing/unboxing overhead. `Util.sendMail` presumably returns `boolean` or `Boolean`; if the former, the result is autoboxed on assignment at line 188.

A17-13 | LOW | FleetcheckAction.java:178 | **Index-based iteration over array where enhanced for-loop would suffice** — The loop at lines 178–182 uses a traditional `for (int i = 0; ...)` pattern over `emails[]` solely to access `emails[i]`. An enhanced for-each loop would be cleaner and consistent with the for-each loop used for `barcode.keySet()` at line 146 in the same file.

A17-14 | INFO | FleetcheckAction.java:58,77,136,157 | **DAO objects instantiated directly inside Action methods** — `QuestionDAO`, `ResultDAO`, and `SubscriptionDAO` are instantiated with `new` directly in the Action and its helper methods. This tightly couples the web tier to specific DAO implementations and makes unit testing without a live database impossible. By contrast, `AdvertismentDAO` in `ExpireAction` uses a singleton (`getInstance()`), showing an inconsistent DAO access pattern across the codebase.

A17-15 | INFO | ExpireAction.java:24 | **Typo in import/class name** — The import `com.dao.AdvertismentDAO` (line 24) reflects a pre-existing typo in the DAO class name (`Advertisment` instead of `Advertisement`). This is noted for completeness; the class name itself would need to be renamed to fix it.
# P4 Agent A18 — FormBuilderAction, GPSReportAction

## Reading Evidence

### FormBuilderAction

- Class: `FormBuilderAction` extends `Action` (line 37)
- Methods:
  - `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` (line 41)
- Constants/Types: None declared. The class uses `RuntimeConf.EMAIL_DIGANOSTICS_TITLE` and `RuntimeConf.emailFrom` (external constants, not defined here).

### GPSReportAction

- Class: `GPSReportAction` extends `Action` (line 17)
- Fields (instance-level):
  - `reportService` : `ReportService` (line 19)
  - `manufactureDAO` : `ManufactureDAO` (line 20)
  - `unitDAO` : `UnitDAO` (line 21)
- Methods:
  - `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` (line 24)
- Constants/Types: None declared.

---

## Findings

A18-1 | HIGH | FormBuilderAction.java:63 | Raw type used for `Enumeration` — `for(Enumeration e = request.getParameterNames(); ...)` uses the raw `Enumeration` type without a type parameter. This generates an unchecked/raw-type compiler warning and bypasses generics safety. Should be `Enumeration<String>`.

A18-2 | HIGH | FormBuilderAction.java:76 | Local variable named `EntityBean` (line 76: `EntityBean EntityBean = arrEntity.get(0);`) shadows the imported class `com.bean.EntityBean`. Using the same identifier for both a type and a variable in the same scope is a severe naming violation that confuses the compiler and any reader, and can mask type-resolution bugs.

A18-3 | HIGH | GPSReportAction.java:20-21 | Dead fields — `manufactureDAO` (line 20) and `unitDAO` (line 21) are declared as instance fields but are never actually used in the live code path. Both lines that would have used them (`searchForm.setManufacturers(...)` and `searchForm.setUnitTypes(...)`) are commented out (lines 35–36). These unused fields introduce unnecessary coupling to `ManufactureDAO` and `UnitDAO` at class-instantiation time.

A18-4 | HIGH | GPSReportAction.java:35-41 | Commented-out code block — four lines of substantive logic are left commented out:
```java
//        searchForm.setManufacturers(this.manufactureDAO.getAllManufactures(sessCompId));
//        searchForm.setUnitTypes(unitDAO.getAllUnitType());
//        ImpactReportBean impactReport = reportService.getImpactReport(compId, searchForm.getImpactReportFilter(dateFormat), dateTimeFormat, timezone);
//        request.setAttribute("impactReport", impactReport);
```
This makes the action a near-no-op (it only populates `arrAdminUnit`) and indicates unfinished or abandoned functionality left in production code.

A18-5 | MEDIUM | GPSReportAction.java:19 | Dead field — `reportService` (line 19) is declared and assigned via `ReportService.getInstance()` but is only referenced in the commented-out code on line 39. It is never used in any live code path, making it dead code that still incurs object instantiation cost.

A18-6 | MEDIUM | FormBuilderAction.java:59-60 | Non-standard local variable naming — `ParameterNames` (line 59) and `ParameterValues` (line 60) use `PascalCase`, which is the Java convention for class names, not local variables. Java convention requires `camelCase` for local variables (i.e., `parameterNames`, `parameterValues`). This is inconsistent with all other local variable names in the same method.

A18-7 | MEDIUM | FormBuilderAction.java:41-115 | Leaky abstraction / single-method god action — the entire `execute` method handles session retrieval, DAO instantiation, business logic (email construction and sending), form element assembly, sorting, and error/message management all inline with no delegation. DAO objects (`QuestionDAO`, `FormBuilderDAO`, `CompanyDAO`) are constructed directly inside the method body rather than injected or obtained via a service layer, tightly coupling the action to concrete DAO implementations.

A18-8 | MEDIUM | FormBuilderAction.java:44 vs GPSReportAction.java:25 | Inconsistent null-session handling between files — `FormBuilderAction` calls `request.getSession(false)` (line 44) but performs no null check on the returned session before immediately calling `session.getAttribute(...)` (line 46), risking a `NullPointerException` when no session exists. `GPSReportAction` (line 25–27) also calls `getSession(false)` but at least guards against a null `sessCompId`. Neither file has an explicit null check on the session object itself, but `FormBuilderAction` is more immediately dangerous because it dereferences the session unconditionally.

A18-9 | MEDIUM | FormBuilderAction.java:54-55 | Unsafe list access without size check — `questionDAO.getQuestionById(qid)` (line 54) may return an empty list; calling `.get(0)` on line 55 without verifying the list is non-empty will throw `IndexOutOfBoundsException`. The same pattern appears again at line 76 (`arrEntity.get(0)`).

A18-10 | LOW | FormBuilderAction.java:80 | Typo in constant name — `RuntimeConf.EMAIL_DIGANOSTICS_TITLE` contains a misspelling ("DIGANOSTICS" instead of "DIAGNOSTICS"). This is visible in the calling code and indicates either the constant itself is misnamed in `RuntimeConf` or there is a propagated typo.

A18-11 | LOW | FormBuilderAction.java:84 | Typo in message key string — `messages.add("fomrmsg", msg)` (line 84) contains a typo ("fomrmsg" instead of "formmsg" or "formMsg"). This is a string key used to retrieve the message in JSP, so the typo will silently cause the message to be unrenderable if the JSP uses the correct spelling.

A18-12 | LOW | FormBuilderAction.java:37 | Missing `@Override` annotation — `FormBuilderAction.execute(...)` overrides `Action.execute(...)` but does not declare `@Override` (contrast with `GPSReportAction.execute` at line 23 which correctly uses `@Override`). This is a style inconsistency across the two files and means the compiler cannot catch a signature mismatch.

A18-13 | LOW | FormBuilderAction.java:37 | Class declaration formatting — `extends Action{` has no space before the opening brace (line 37), inconsistent with `GPSReportAction.java` line 17 which writes `extends Action {` with a space. Minor but an inconsistency across files in the same package.

A18-14 | LOW | FormBuilderAction.java:41-44 | Indentation inconsistency — the `execute` method signature begins at two-space indent (line 41–43) while the method body (lines 44–115) uses a mix of 14-space and 6-space indent levels rather than consistent 4-space or tab-based indentation. The method body indentation does not align with the method declaration indent. This contrasts with `GPSReportAction`, which uses consistent 4-space indentation throughout.

A18-15 | INFO | GPSReportAction.java:32 | Unnecessary `Long` conversion — `Long compId = Long.valueOf(sessCompId)` (line 32) is computed but `compId` is only referenced in the commented-out code (line 39). With that code commented out, `compId` is an unused local variable that will generate a compiler warning.
# P4 Agent A19 — GetAjaxAction, GetXmlAction

## Reading Evidence

### GetAjaxAction
- Class: `GetAjaxAction` extends `org.apache.struts.action.Action` (line 19)
- Fields:
  - `unitDao` : `UnitDAO` (line 20) — instance-level singleton reference
- Methods:
  - `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` (line 22) — returns `ActionForward`, throws `Exception`
- Constants/Types defined: none
- Imports:
  - `java.util.ArrayList` (line 3)
  - `javax.servlet.http.HttpServletRequest` (line 5)
  - `javax.servlet.http.HttpServletResponse` (line 6)
  - `org.apache.struts.action.Action` (line 8)
  - `org.apache.struts.action.ActionForm` (line 9)
  - `org.apache.struts.action.ActionForward` (line 10)
  - `org.apache.struts.action.ActionMapping` (line 11)
  - `com.bean.XmlBean` (line 13)
  - `com.dao.DriverDAO` (line 14)
  - `com.dao.GPSDao` (line 15)
  - `com.dao.QuestionDAO` (line 16)
  - `com.dao.UnitDAO` (line 17)

### GetXmlAction
- Class: `GetXmlAction` extends `org.apache.struts.action.Action` (line 19)
- Fields:
  - `driverDAO` : `DriverDAO` (line 20) — instance-level singleton reference
- Methods:
  - `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` (line 22) — returns `ActionForward`, throws `Exception`
- Constants/Types defined: none
- Imports:
  - `java.util.ArrayList` (line 3)
  - `java.util.List` (line 4)
  - `javax.servlet.http.HttpServletRequest` (line 6)
  - `javax.servlet.http.HttpServletResponse` (line 7)
  - `javax.servlet.http.HttpSession` (line 8)
  - `org.apache.struts.action.Action` (line 10)
  - `org.apache.struts.action.ActionForm` (line 11)
  - `org.apache.struts.action.ActionForward` (line 12)
  - `org.apache.struts.action.ActionMapping` (line 13)
  - `com.bean.DriverBean` (line 15)
  - `com.dao.DriverDAO` (line 16)

---

## Findings

A19-1 | HIGH | GetAjaxAction.java:14 | `DriverDAO` is imported but never referenced anywhere in `GetAjaxAction`. `DriverDAO` is not used in any branch of the `execute` method. This is an unused import that will produce a compiler warning and causes misleading coupling.

A19-2 | MEDIUM | GetAjaxAction.java:3 | `java.util.ArrayList` is used only as the concrete instantiation type on line 28 (`new ArrayList<XmlBean>()`), but the declared variable type is also `ArrayList` rather than the `List` interface. In `GetXmlAction` line 4, `java.util.List` is imported and used as the declared type. The two files are inconsistent: `GetAjaxAction` declares `ArrayList<XmlBean> arrXml` (raw concrete type as declared variable) while `GetXmlAction` correctly declares `List<DriverBean> arrDriver`. This violates the "program to interfaces" principle and is inconsistent across the two sibling action classes.

A19-3 | MEDIUM | GetXmlAction.java:3 | `java.util.ArrayList` is imported but never used in `GetXmlAction`. The local variable `arrDriver` is declared as `List<DriverBean>` and is assigned the return value of `driverDAO.getAllDriver(...)` — no `ArrayList` is ever instantiated directly. This unused import will produce a compiler warning.

A19-4 | MEDIUM | GetAjaxAction.java:44 | Inconsistent use of `String.equals()` vs `String.equalsIgnoreCase()`. The `"getType"` (line 29), `"getPower"` (line 33), and `"getQcontent"` (line 38) branches use `equalsIgnoreCase`, but the `"last_gps"` branch on line 44 uses `equals` (case-sensitive). This is an inconsistency within the same dispatch chain and will silently fail to match `"Last_GPS"` or `"LAST_GPS"` while all other branches are case-insensitive.

A19-5 | MEDIUM | GetAjaxAction.java:47 | The `dateFormat` variable is computed (line 47) but never used. The `replaceAll("yyyy","yy").replaceAll("M","m")` result is stored in `dateFormat` but is never passed to any method call or set as a request/session attribute. The only format variable passed to `GPSDao.getUnitGPSData` is `dateTimeFormat`. This is dead (unreachable-effect) code.

A19-6 | LOW | GetAjaxAction.java:19–56 / GetXmlAction.java:19–31 | Inconsistent brace and spacing style between the two files and within `GetAjaxAction` itself. `GetXmlAction` line 19 writes `extends Action{` (no space before `{`), while the same pattern in `GetAjaxAction` line 19 writes `extends Action {` (space before `{`). Within `GetAjaxAction`, the `else if` blocks alternate between having the opening `{` on the same line as `else if` and not (e.g., line 38: `}else if(` with no spaces around `else`; lines 33 and 39 mix `} else if (` and `}else if(`). This represents inconsistent formatting within a single file and across the two sibling files.

A19-7 | LOW | GetAjaxAction.java:22–24 / GetXmlAction.java:22–24 | Both files use severely irregular indentation. The `execute` method signature is indented with 2 spaces (line 22), but the body opens at a mix of 4-space and tab indentation. Lines 25–51 mix tab-stops and spaces, and in `GetAjaxAction` the closing `}` of the class (line 57) appears at 1-tab indent while the closing `}` of the method (line 56) is at 3 tabs. The two files have no consistent indentation convention with each other or internally.

A19-8 | LOW | GetXmlAction.java:33–34 | Two trailing blank lines at the end of the file (lines 33–34) are unnecessary and inconsistent with `GetAjaxAction.java` which has no trailing blank lines.

A19-9 | INFO | GetAjaxAction.java:8–11 / GetXmlAction.java:10–13 | Both files use the Apache Struts 1.x `Action` framework (`org.apache.struts.action.*`). Struts 1 reached end-of-life in 2013 and is a deprecated API. Any build toolchain configured to warn on deprecated frameworks will flag all usages in these classes.

A19-10 | INFO | GetAjaxAction.java:42 | `QuestionDAO` is instantiated with `new QuestionDAO()` (line 42) rather than through a singleton or factory pattern. This is inconsistent with the class-level field `unitDao = UnitDAO.getInstance()` (line 20) and `GetXmlAction`'s `driverDAO = DriverDAO.getInstance()` (line 20), where singletons are used. This exposes an inconsistent object-lifecycle pattern across DAOs in the same codebase.
# P4 Agent A20 — GoResetPassAction, GoSearchAction

## Reading Evidence

### GoResetPassAction
- Class: `GoResetPassAction` extends `Action` (line 17)
- Methods:
  - `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` (line 19) — returns `ActionForward`, throws `Exception`
- Constants/Types: none defined in this file
- Imports used: `HttpServletRequest`, `HttpServletResponse`, `HttpSession`, `Action`, `ActionForm`, `ActionForward`, `ActionMapping`, `PasswordRequest`, `PasswordResponse`, `RestClientService`, `RuntimeConf`

### GoSearchAction
- Class: `GoSearchAction` (final) extends `Action` (line 21)
- Methods:
  - `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` (line 24) — returns `ActionForward`, throws `Exception`
- Constants/Types:
  - `private static Logger log` (line 22) — Log4j Logger instance
- Imports used: `HttpServletRequest`, `HttpServletResponse`, `HttpSession`, `Action`, `ActionForm`, `ActionForward`, `ActionMapping`, `Logger`, `InfoLogger`

---

## Findings

A20-1 | HIGH | GoResetPassAction.java:22 | Null-dereference risk on session. `request.getSession(false)` can return `null` when no session exists, but `session.getAttribute("accessToken")` on line 25 is called unconditionally without a null check on `session`. If there is no active session the action throws a `NullPointerException` rather than redirecting gracefully.

A20-2 | HIGH | GoSearchAction.java:27 | Null-dereference risk on session. Same pattern: `request.getSession(false)` can return `null`, but `theSession.removeAttribute("arrDriver")` is called immediately with no null guard. A request without an established session causes an unhandled `NullPointerException`.

A20-3 | MEDIUM | GoResetPassAction.java:33 | Manual service instantiation violates layering. `RestClientService` is constructed with `new RestClientService()` inside the action, tightly coupling the presentation/controller layer directly to a concrete service implementation. There is no injection or factory pattern, making the class untestable in isolation and leaking the service construction detail into the action.

A20-4 | MEDIUM | GoSearchAction.java:22 | Dead field — `log` is never used. The `Logger` instance is declared and assigned but no log statement appears anywhere in the class. This is an unused private field that produces a build/IDE warning and adds noise without benefit.

A20-5 | LOW | GoSearchAction.java:1-31 | Inconsistent blank-line / import formatting across files. `GoSearchAction.java` contains multiple consecutive blank lines between import groups (lines 2-3, 7-8, 14-16) and between individual Struts imports (lines 10-11), while `GoResetPassAction.java` uses single blank lines consistently. Both files are in the same package and should follow a uniform style.

A20-6 | LOW | GoResetPassAction.java:17 | Missing `@Override` on `execute` in `GoSearchAction`. `GoResetPassAction` correctly annotates its `execute` override with `@Override` (line 18), but `GoSearchAction` does not annotate its `execute` method (line 24). This is a style inconsistency between the two files in the same package; the annotation also guards against accidental signature mismatch.

A20-7 | LOW | GoResetPassAction.java:17 | Missing `final` modifier inconsistency. `GoSearchAction` declares the class `final` (line 21), but `GoResetPassAction` does not (line 17). Whether or not `final` is intended, the two classes in the same package should follow a consistent convention.

A20-8 | LOW | GoResetPassAction.java:27-46 | Brace placement style is inconsistent within the file. The `if` block on line 27 uses Allman-style braces (`if(...)\n{`), while the `else if` and `else` blocks mix placement. Additionally, there is inconsistent indentation within the `if` body (4-space vs tab mixing). Both files use tabs as the primary indent unit but `GoResetPassAction.java` mixes spaces and tabs in the `execute` body (lines 22-26 use 8 spaces, lines 27-46 use tabs).

A20-9 | INFO | GoResetPassAction.java:7-10 | Deprecated framework. Both files extend `org.apache.struts.action.Action` from Struts 1, which reached end-of-life and is no longer maintained. Any continued use carries unpatched security risk. This is a project-wide concern but is visible at the code level in these files.
# P4 Agent A21 — ImpactReportAction, IncidentReportAction

## Reading Evidence

### ImpactReportAction
- Class: `ImpactReportAction` extends `org.apache.struts.action.Action` (line 17)
- Fields (instance):
  - `reportService` : `ReportService` (line 19)
  - `manufactureDAO` : `ManufactureDAO` (line 20)
  - `unitDAO` : `UnitDAO` (line 21)
- Methods:
  - `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` (line 24) — overrides `Action.execute`
- Constants/Types: none defined in this file

### IncidentReportAction
- Class: `IncidentReportAction` extends `org.apache.struts.action.Action` (line 17)
- Fields: none (no instance or static fields declared)
- Methods:
  - `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` (line 20) — overrides `Action.execute`
- Constants/Types: none defined in this file

---

## Findings

A21-1 | HIGH | IncidentReportAction.java:31 | **Type mismatch for `compId` across the two parallel action classes.** `ImpactReportAction` parses `sessCompId` as `Long` (`Long.valueOf(sessCompId)`, line 32) and passes a `Long` to `ReportService.getImpactReport(Long, ...)`. `IncidentReportAction` parses the same session attribute as `int` (`Integer.parseInt(sessCompId)`, line 31) and passes an `int` to `ReportService.getIncidentReport(int, ...)`. The two report services therefore receive the company ID in different numeric types. If a company ID exceeds `Integer.MAX_VALUE` (2,147,483,647) the `int` parse in `IncidentReportAction` silently truncates the value, producing wrong results or a `NumberFormatException`. The inconsistency also signals that at least one of the two action classes is wrong about the actual database column type.

A21-2 | MEDIUM | IncidentReportAction.java:34-35 | **Static method calls on DAO singletons without obtaining the instance.** `IncidentReportAction` calls `ManufactureDAO.getAllManufactures(sessCompId)` and `UnitDAO.getAllUnitType()` as bare static calls, bypassing the singleton accessor entirely. `ImpactReportAction` (lines 35-36) correctly obtains instances first (`this.manufactureDAO.getAllManufactures(...)`, `unitDAO.getAllUnitType()`). Although both `getAllManufactures` and `getAllUnitType` are indeed declared `static` in their respective DAOs, the inconsistency between the two action classes is a style and leaky-abstraction problem: `ImpactReportAction` treats the DAOs as objects (injected via singleton), while `IncidentReportAction` treats them as utility classes, exposing the static nature of their internals and making it impossible to substitute the DAOs in tests.

A21-3 | MEDIUM | IncidentReportAction.java:39 | **`ReportService` singleton obtained inline rather than stored as a field.** `ImpactReportAction` stores `ReportService.getInstance()` in a private field (line 19) and reuses it. `IncidentReportAction` calls `ReportService.getInstance()` inline inside `execute()` (line 39) on every request. While functionally equivalent (the singleton is stable), the inconsistency between the two otherwise-parallel classes creates a maintenance hazard and signals copy-paste divergence.

A21-4 | MEDIUM | ImpactReportAction.java:19-21 | **Instance fields on a shared Struts `Action` singleton introduce a thread-safety concern.** Struts 1.x reuses a single `Action` instance across all requests. `ImpactReportAction` declares three mutable instance fields (`reportService`, `manufactureDAO`, `unitDAO`). Although in practice the assigned singletons are themselves stateless/thread-safe, declaring them as instance fields on a Struts `Action` is an unsafe pattern: any future modification that assigns a different value to these fields (e.g., for testing or reconfiguration) would cause a data race. `IncidentReportAction` avoids this by not holding any instance fields, which is the safer convention in Struts 1 actions.

A21-5 | MEDIUM | ImpactReportAction.java:27 | **Null session dereference risk before the null check.** `session.getAttribute("sessCompId")` on line 26 will throw a `NullPointerException` if `request.getSession(false)` returns `null` (i.e., no existing session). The null guard on line 27 checks `sessCompId`, not `session` itself. `IncidentReportAction` has the identical defect on line 23. Both files share this pattern, so this is a consistent but incorrect guard: the correct check should verify `session != null` before calling `session.getAttribute(...)`.

A21-6 | LOW | ImpactReportAction.java:1-15 vs IncidentReportAction.java:1-16 | **Import block ordering is inconsistent between the two files.** `ImpactReportAction` places project imports (`com.*`) before framework/JDK imports (`org.apache.*`, `javax.servlet.*`). `IncidentReportAction` places JDK/framework imports (`javax.servlet.*`, `org.apache.*`) before project imports (`com.*`). While neither ordering is wrong in isolation, the inconsistency across two closely related files in the same package violates a single, codebase-wide style convention.

A21-7 | LOW | IncidentReportAction.java:24-26 | **Brace style for the null-check `if` block differs between the two files.** `ImpactReportAction` (line 27) uses a single-line `if` without braces: `if (sessCompId == null) throw new RuntimeException(...)`. `IncidentReportAction` (lines 24-26) uses a multi-line block with braces. Both styles appear in two files that are structurally identical in purpose, which is a style inconsistency.

A21-8 | INFO | IncidentReportAction.java:33 | **Verbose local variable name `incidentReportSearchForm`.** `ImpactReportAction` uses the concise name `searchForm` (line 34) for its cast form reference. `IncidentReportAction` uses the fully-qualified name `incidentReportSearchForm`. This is minor but contributes to the general divergence in coding style between two parallel classes.
# P4 Agent A22 — LoginAction, LogoutAction

## Reading Evidence

### LoginAction
- Class: `LoginAction` (final, extends `org.apache.struts.action.Action`)
- Methods:
  - `execute` (line 23) — public, overrides `Action.execute`
  - `getLoggedInCompany` (line 73) — private static
  - `loginFailure` (line 82) — private
- Constants/Types: none defined; uses types `LoginActionForm`, `AuthenticationRequest`, `AuthenticationResponse`, `RestClientService`, `CompanyBean`, `LoginDAO`, `RuntimeConf`, `CompanySessionSwitcher`, `AdvertismentDAO`, `TimezoneDAO`, `LanguageDAO`

### LogoutAction
- Class: `LogoutAction` (non-final, extends `org.apache.struts.action.Action`)
- Methods:
  - `execute` (line 32) — public, overrides `Action.execute`
- Constants/Types:
  - `log` (line 30) — private static `org.apache.log4j.Logger` field

---

## Findings

A22-1 | HIGH | LogoutAction.java:21 | **Inconsistent logging framework across paired files.** `LoginAction` uses Lombok `@Slf4j` (backed by SLF4J, line 12–20 of LoginAction.java), while `LogoutAction` directly instantiates `org.apache.log4j.Logger` via `InfoLogger.getLogger` (line 30). The application should use a single logging facade. Mixing Log4j direct API and SLF4J creates inconsistent log routing, configuration difficulty, and may cause duplicate or missing log entries.

A22-2 | HIGH | LogoutAction.java:4 | **Unused import: `java.util.ArrayList`.** `ArrayList` is never referenced anywhere in `LogoutAction`. This is dead import / build noise; many IDEs and static analysis tools flag this as a warning.

A22-3 | HIGH | LogoutAction.java:7 | **Unused import: `javax.servlet.ServletException`.** `ServletException` is never thrown or referenced in `LogoutAction`. Dead import.

A22-4 | HIGH | LogoutAction.java:23 | **Unused import: `com.bean.AdvertisementBean`.** `AdvertisementBean` is never referenced by name in `LogoutAction`; the method `getAllAdvertisement()` returns `ArrayList<AdvertisementBean>` but the return value is passed directly to `setAttribute` without being assigned to a typed local variable. The import therefore serves no compile-time purpose and is dead.

A22-5 | MEDIUM | LogoutAction.java:28 | **Class is not `final`.** `LoginAction` (line 21) is declared `final`; `LogoutAction` is not. These are Struts action classes instantiated by the framework and should not be subclassed. The inconsistency suggests one declaration was reviewed and hardened while the other was not.

A22-6 | MEDIUM | LogoutAction.java:32–50 | **Inconsistent indentation style within file and across files.** `LogoutAction.execute` uses hard tabs for indentation (and the indentation is deeply and irregularly nested — the method body is indented to the same level as if it were a deeply nested block, with the closing brace at column 3). `LoginAction` uses 4-space indentation consistently throughout. Within `LogoutAction` itself, the method body is indented as though it is nested several extra levels beyond the class body. This is a style inconsistency both within the file and across the two files.

A22-7 | MEDIUM | LogoutAction.java:40 | **Tight coupling / leaky abstraction: `LogoutAction` directly calls static methods on `SwitchLanguageAction`.** `LogoutAction.execute` calls `SwitchLanguageAction.getCookie(...)` and `SwitchLanguageAction.getLocale(...)` (lines 40, 43). This creates a hard dependency between two sibling action classes. Cookie/locale utility logic belongs in a shared utility class, not exposed as public statics on another action. This is a leaky abstraction: internal implementation details of language switching are exposed to and consumed directly by an unrelated action.

A22-8 | MEDIUM | LoginAction.java:38 | **Mixed indentation within a single method.** Lines 38–45 (the Cognito authentication block) use hard tabs, while the rest of `LoginAction.execute` (lines 28–36 and 47–71) uses 4-space indentation. The inconsistency is visible in the raw file: `RestClientService`, `AuthenticationRequest`, `AuthenticationResponse`, and `authResponse` variable declarations are tab-indented while surrounding code is space-indented.

A22-9 | MEDIUM | LoginAction.java:56–57 | **Raw `Boolean` autoboxing for DAO results used in conditional logic.** `LoginDAO.isUserAuthority` and `LoginDAO.isAuthority` return `Boolean` (boxed). The result is stored as `Boolean isSuperAdmin` and `Boolean isDealerLogin` and immediately passed to `LoginDAO.getCompanies`. If either DAO method ever returns `null`, an unboxing `NullPointerException` will be silently thrown. Using primitive `boolean` would make intent explicit and eliminate the NPE risk; using `Boolean` is unnecessary here.

A22-10 | MEDIUM | LoginAction.java:57 | **String concatenation used to convert `int` to `String` for a DAO call.** `loggedInCompanyId+""` (line 57) is used to convert an `Integer` to a `String` for the `isAuthority` call. The idiomatic and safer approach is `String.valueOf(loggedInCompanyId)` or `loggedInCompanyId.toString()`. The pattern is inconsistent with line 77 which uses `String.valueOf(loggedInCompanyId)` for the same purpose.

A22-11 | LOW | LoginAction.java:37 | **Comment used as section delimiter rather than meaningful documentation.** `//Start Cognito Authentication Service get Access Token` and `//End Cognito` (lines 37, 45) are structural delimiters that indicate the execute method is doing too many things. The Cognito authentication block should be extracted into its own private method, which would eliminate the need for these comments and improve readability.

A22-12 | LOW | LogoutAction.java:30 | **Logger field name shadows Lombok convention.** `LoginAction` relies on Lombok `@Slf4j` which generates a field named `log`. `LogoutAction` manually declares `private static Logger log`. The field name is the same but the types differ (`org.slf4j.Logger` vs `org.apache.log4j.Logger`). Beyond the naming coincidence, `log` is declared but never actually used anywhere in the `execute` method body of `LogoutAction` — making it a dead field.

A22-13 | LOW | LoginAction.java:21 | **`org.apache.struts.action.*` wildcard import alongside specific `javax.servlet` imports.** `LoginAction` uses a wildcard import `org.apache.struts.action.*` (line 13) and `com.bean.*` (line 4) and `com.dao.*` (line 7), but uses specific imports for everything else. `LogoutAction` uses only specific imports. Wildcard imports reduce readability and may mask unintended class resolutions. Style is inconsistent between the two files.

A22-14 | INFO | LogoutAction.java:47 | **`AdvertismentDAO` class name contains a typo ("Advertisment" missing a second 'e').** The typo is present in both files (`LoginAction` line 31, `LogoutAction` line 47) and in the DAO class name itself, so it is a pre-existing systemic issue rather than an inconsistency between these two files. Noted for completeness.
# P4 Agent A23 — MailerAction, PandoraAction

## Reading Evidence

### MailerAction
- Class: `MailerAction extends Action` (line 37)
- Fields: `private static Logger log` (line 38)
- Methods:
  - `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` (line 40)
- Constants/Types defined: none
- Imports:
  - `java.net.HttpURLConnection` (line 4)
  - `java.util.ArrayList` (line 5)
  - `java.util.Calendar` (line 6)
  - `java.util.Date` (line 7)
  - `javax.servlet.ServletException` (line 9)
  - `javax.servlet.http.HttpServletRequest` (line 10)
  - `javax.servlet.http.HttpServletResponse` (line 11)
  - `org.apache.struts.Globals` (line 16)
  - `org.apache.struts.action.Action` (line 17)
  - `org.apache.struts.action.ActionForm` (line 18)
  - `org.apache.struts.action.ActionForward` (line 19)
  - `org.apache.struts.action.ActionMapping` (line 20)
  - `org.apache.log4j.Logger` (line 21)
  - `com.util.DateUtil` (line 23)
  - `com.util.InfoLogger` (line 24)
  - `com.util.RuntimeConf` (line 25)
  - `com.util.Util` (line 26)
  - `com.bean.SubscriptionBean` (line 27)
  - `com.dao.SubscriptionDAO` (line 28)
  - `com.report.*` (line 29)

### PandoraAction
- Class: `public abstract class PandoraAction extends Action` (line 9)
- Fields: `private static final String UNDEFINED_PARAM = "undefined"` (line 11)
- Methods:
  - `getLongRequestParam(HttpServletRequest, String)` (line 13)
  - `getRequestParam(HttpServletRequest, String, Long)` (line 17)
  - `getRequestParam(HttpServletRequest, String, String)` (line 24)
  - `getSessionAttribute(HttpSession, String, String)` (line 29)
  - `getLongSessionAttribute(HttpSession, String, Long)` (line 35)
  - `getCompId(HttpSession)` (line 41)
- Constants/Types: `UNDEFINED_PARAM = "undefined"` (line 11)

---

## Findings

A23-1 | CRITICAL | MailerAction.java:102 | Hardcoded credentials and hardcoded data in API payload. The JSON string passed to `ReportAPI` contains a plaintext `admin_password` ("ciiadmin") and a hardcoded `username` ("hui") as well as a hardcoded `company_id` of `1`. These credentials are baked into source code, will appear in version control history, and lock all subscription report runs to a single company. This must be externalised to `RuntimeConf` or a secrets store and `company_id` must be derived from the subscription record.

A23-2 | HIGH | MailerAction.java:85 | Typo in frequency string literal causes silent functional failure. The string `"Monthy"` is added to the frequencies list on line 85 (comment on line 83 correctly says "Monthly"). `DateUtil.java:107` compares against `"Monthly"` (correct spelling). The typo means the monthly frequency branch in `DateUtil` is never matched: no monthly date-range calculation occurs, resulting in incorrect report data for monthly subscriptions. No test or runtime error will surface this.

A23-3 | HIGH | MailerAction.java:124,132 | Exception swallowed with `e.printStackTrace()` in both send-mail catch blocks. Errors sending email are silently consumed after printing to stderr. No re-throw, no log statement at ERROR level, and no retry or alerting logic. A mail failure will appear to succeed from the caller's perspective; the log record on line 134 ("Report sent to …") will still be written even after a send failure because the log line is outside both try/catch blocks.

A23-4 | HIGH | MailerAction.java:37 | `MailerAction` extends `Action` directly instead of the project-defined base class `PandoraAction`. Every other action class in the package (`AdminManufacturersAction`, `AdminOperatorAction`, `AdminTrainingsAction`, `AdminUnitAccessAction`, `AdminUnitAssignAction`) extends `PandoraAction`, which provides centralised request/session parameter helpers. This inconsistency means `MailerAction` bypasses the shared utility methods and is coupled to raw Struts `Action` rather than the project abstraction.

A23-5 | HIGH | MailerAction.java:71-72 | Instance field access used to reach a static constant. `currentDate.DAY_OF_WEEK` and `currentDate.DAY_OF_MONTH` access static `Calendar` constants through an instance reference. In Java this is a build warning ("static field accessed via instance reference") and is misleading — it makes the values appear to depend on the instance when they are compile-time constants. The correct form is `Calendar.DAY_OF_WEEK` and `Calendar.DAY_OF_MONTH`.

A23-6 | MEDIUM | MailerAction.java:9,16 | Unused imports. `javax.servlet.ServletException` (line 9) and `org.apache.struts.Globals` (line 16) are imported but never referenced anywhere in the class body. These are dead import statements and will produce compiler warnings.

A23-7 | MEDIUM | MailerAction.java:102 | API payload constructed by string concatenation rather than a JSON library. The `input` string is assembled by raw `String` concatenation with embedded JSON literals including escaped quotes. This is brittle: special characters in any date value or future filter value will produce malformed JSON with no parse-time feedback. A JSON object builder (e.g. `org.json`, Jackson `ObjectMapper`, or Gson) should be used.

A23-8 | MEDIUM | MailerAction.java:91 | Index-based `for` loop over `ArrayList` where an enhanced `for-each` loop is idiomatic and clearer. Minor style inconsistency relative to the rest of the codebase, and slightly less safe if the list were ever refactored to a non-`RandomAccess` type.

A23-9 | MEDIUM | MailerAction.java:108 | Hard-coded array index `get(0)` to retrieve the first recipient email without any bounds or null check. If `arrUser` is empty the call will throw `IndexOutOfBoundsException` at runtime, aborting the entire batch loop iteration with no meaningful log message. The loop body has no guard for an empty user list.

A23-10 | MEDIUM | PandoraAction.java:18,30,36 | Validation uses Java `assert` statements. Assertions are disabled by default in production JVMs (unless `-ea` is passed). These checks on method preconditions will silently become no-ops in a standard deployment, meaning a blank `name` parameter will not be caught and a `NullPointerException` or incorrect behaviour will occur deeper in the call chain instead of a clear early failure. Explicit `if`/`throw IllegalArgumentException` guards are the appropriate idiom.

A23-11 | LOW | MailerAction.java:59-66 | Commented-out code fragments used as section delimiters. Lines 61 (`//get current time`), 62 (`//end`), 63 (`//get current date`), 66 (`//end`) are noise comments describing trivial operations that the code itself already expresses. The `//end` comments suggest these were once conditional blocks; removing them would improve readability.

A23-12 | LOW | MailerAction.java:97-100 | Commented-out code left in production file. Lines 97–100 contain an example SQL query fragment and two example JSON input strings:
```
//input format:
//select * from unit, session, company where ...
//[{"report_end_date":"11/01/2017"}{"report_start_date":"10/01/2017"},{"company_id":1}]
//[{"slugname":"the vlaue"},{"slugname":"the vlaue"},...]
```
These are development notes / dead documentation, not executable code, but they also disclose internal table names, column names, and an example hardcoded `company_id` and credential shape. They should be removed or moved to external documentation.

A23-13 | LOW | MailerAction.java:115 | Misspelled log message: `"file genrated = "` should be `"file generated = "`. Minor quality issue but can impede log searching.

A23-14 | LOW | MailerAction.java:43-48 | Inconsistent indentation within the `execute` method body. The method body uses a mix of two-tab and single-tab indent levels. The opening brace of the method is on the same line as the signature (line 42) yet the body statements start at a triple-indent level (lines 43–48) that does not match the consistent single-indent used in the surrounding class structure. This is inconsistent with the formatting style in `PandoraAction`, which uses standard 4-space indents throughout.

A23-15 | INFO | MailerAction.java:29 | Wildcard import `com.report.*` used. All other imports in both files are explicit. Wildcard imports can obscure which types are actually depended upon and are flagged as a warning by most static analysis tools and style checkers.
# P4 Agent A24 — PreOpsReportAction, PrintAction

## Reading Evidence

### PreOpsReportAction
- Class: `PreOpsReportAction` extends `org.apache.struts.action.Action` (line 18)
- Annotations: `@Slf4j` (Lombok, line 17)
- Fields:
  - `reportService` : `ReportService` (line 20)
  - `manufactureDAO` : `ManufactureDAO` (line 21)
  - `unitDAO` : `UnitDAO` (line 22)
- Methods:
  - `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` (line 25)
- Constants/Types: none defined

### PrintAction
- Class: `PrintAction` extends `org.apache.struts.action.Action` (line 29)
- Fields:
  - `log` : `org.apache.log4j.Logger` (static, line 31)
  - `unitDAO` : `UnitDAO` (line 32)
- Methods:
  - `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` (line 34)
- Constants/Types: none defined

---

## Findings

A24-1 | HIGH | PrintAction.java:11 | **Inconsistent logging framework** — `PrintAction` uses `org.apache.log4j.Logger` (obtained via a custom `InfoLogger.getLogger`) while `PreOpsReportAction` uses Lombok `@Slf4j` (SLF4J facade). The two files in the same package use different logging APIs, breaking uniformity and making log configuration harder to manage.

A24-2 | HIGH | PrintAction.java:46 | **`QuestionDAO` instantiated with `new` instead of singleton** — `QuestionDAO quesionDao = new QuestionDAO()` allocates a new DAO on every request, whereas `UnitDAO` (line 32) is obtained via `UnitDAO.getInstance()`. This breaks the consistent singleton pattern used everywhere else in the file and in `PreOpsReportAction` (lines 20–22), and may cause connection/resource leaks.

A24-3 | MEDIUM | PrintAction.java:46 | **Typo in local variable name** — `quesionDao` should be `questionDao`. Minor but reduces readability and differs from the type name `QuestionDAO`.

A24-4 | MEDIUM | PrintAction.java:56,100,117 | **Raw `ArrayList` construction with explicit generic type argument instead of diamond** — e.g., `new ArrayList<QuestionBean>()`, `new ArrayList<String>()`. The diamond operator (`<>`) should be used. This also applies to the return type of `quesionDao.getQuestionByUnitId` being assigned to `ArrayList<QuestionBean>` (line 47) rather than `List<QuestionBean>`, which exposes the concrete type unnecessarily.

A24-5 | MEDIUM | PrintAction.java:34-178 | **Severely inconsistent indentation** — The method body uses a mix of tabs and spaces with erratic nesting depths (the method body starts at deep indentation level matching an inner block rather than a normal method body). `PreOpsReportAction` uses clean 4-space indentation throughout. This is a cross-file style inconsistency and makes `PrintAction` hard to read.

A24-6 | MEDIUM | PrintAction.java:29 | **Missing space before `{` in class declaration** — `public class PrintAction extends Action{` lacks the conventional space before the opening brace, inconsistent with `PreOpsReportAction` (line 18: `public class PreOpsReportAction extends Action {`) and standard Java style.

A24-7 | MEDIUM | PrintAction.java:38-44 | **`sessCompId` null-check returns empty string instead of throwing/redirecting** — `PreOpsReportAction` (line 29–31) throws a `RuntimeException` when `sessCompId` is null, ensuring the session is valid before proceeding. `PrintAction` silently falls back to `""`, which will silently corrupt downstream DAO queries. This is an inconsistent and potentially dangerous abstraction leak: session-validation logic is duplicated with different semantics in the same package.

A24-8 | MEDIUM | PrintAction.java:40-44 | **Request parameters have inconsistent null-default handling** — `veh_id` and `att_id` default to `"0"` on null, while `dname`, `div_id`, and `browser` default to `""`. There is no comment or explanation for why the defaults differ, and some of these are passed directly to DAOs (line 47), where an empty string vs `"0"` may produce different SQL behaviour.

A24-9 | LOW | PrintAction.java:88-95 | **Duplicate IE browser detection logic** — The `browser.equalsIgnoreCase("ie")` check is performed three separate times for the `barcode` action (lines 60, 75, 88). The barcode-generation loop already bifurcates on `ie` per-question (lines 60–71) and then again for the end barcode (lines 75–83), and then a third time for the forward (lines 88–95). This duplication could be refactored, but is primarily a maintainability concern.

A24-10 | LOW | PrintAction.java:174 | **Typo in request attribute key** — `request.setAttribute("untiSerial", ...)` — `"untiSerial"` is a transposition of `"unitSerial"`. If any JSP references `unitSerial`, this attribute will never be found, resulting in a silent null rendering.

A24-11 | LOW | PrintAction.java:4-5 | **Unused imports** — `java.util.ArrayList` and `java.util.List` are both imported. `List` is used only for the return type of `unitDAO.getUnitById` at line 48, so it is legitimately used; however `java.util.ArrayList` is imported explicitly even though `ArrayList` could be referenced through the `java.util.List` interface. More importantly, `com.util.DateUtil` (line 26) is imported but never referenced anywhere in the file, constituting a dead/unused import.

A24-12 | LOW | PrintAction.java:31 | **`@Override` annotation missing on `execute`** — `PreOpsReportAction` correctly annotates `execute` with `@Override` (line 24). `PrintAction` omits this annotation on its `execute` method (line 34), losing the compile-time check that the signature actually overrides the parent method.

A24-13 | INFO | PrintAction.java:86,173 | **Leaky DAO-level field names exposed in view layer** — `arrVeh.get(0).getFule_type_name()` and `getType_nm()`, `getSerial_no()` use snake_case getter names that mirror raw database column names, exposed directly in the action layer and passed as request attributes to JSPs. This is a leaky abstraction: the database schema is effectively visible through the bean API all the way to the view.
# P4 Agent A25 — PrivacyAction, RegisterAction

## Reading Evidence

### PrivacyAction
- Class: `PrivacyAction` extends `org.apache.struts.action.Action` (line 14)
- Methods:
  - `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` (line 16) — returns `ActionForward`, throws `Exception`
- Constants/Types: none defined
- Imports used:
  - `javax.servlet.http.HttpServletRequest` (line 3)
  - `javax.servlet.http.HttpServletResponse` (line 4)
  - `javax.servlet.http.HttpSession` (line 5)
  - `org.apache.struts.action.Action` (line 7)
  - `org.apache.struts.action.ActionForm` (line 8)
  - `org.apache.struts.action.ActionForward` (line 9)
  - `org.apache.struts.action.ActionMapping` (line 10)
  - `com.dao.CompanyDAO` (line 12)

### RegisterAction
- Class: `RegisterAction` extends `org.apache.struts.action.Action` (line 21)
- Fields:
  - `private static Logger log` (line 23) — initialized via `InfoLogger.getLogger(...)`
  - `private DriverDAO driverDao` (line 25) — initialized via `DriverDAO.getInstance()`
- Methods:
  - `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` (line 27) — returns `ActionForward`, throws `Exception`
- Constants/Types: none defined
- Imports used:
  - `com.actionform.RegisterActionForm` (line 4)
  - `com.bean.CompanyBean` (line 5)
  - `com.bean.DriverBean` (line 6)
  - `com.bean.QuestionBean` (line 7)
  - `com.dao.DriverDAO` (line 8)
  - `com.dao.QuestionDAO` (line 9)
  - `com.util.InfoLogger` (line 10)
  - `org.apache.log4j.Logger` (line 11)
  - `org.apache.struts.action.*` (line 12, wildcard)
  - `javax.servlet.http.HttpServletRequest` (line 14)
  - `javax.servlet.http.HttpServletResponse` (line 15)
  - `javax.servlet.http.HttpSession` (line 16)
  - `java.util.ArrayList` (line 17)
  - `java.util.List` (line 18)

---

## Findings

A25-1 | LOW | PrivacyAction.java:19 | Stale TODO comment left in production code. The line `// TODO Auto-generated method stub` was inserted by an IDE scaffold and was never removed. It indicates the method body was written without cleaning up the generated placeholder, which is a maintenance and code-review hygiene issue.

A25-2 | HIGH | PrivacyAction.java:20-21 | Null-unsafe session access. `request.getSession(false)` can return `null` when no session exists, but the result is used immediately on line 21 without a null check (`session.getAttribute(...)`). If called without an active session this will throw a `NullPointerException` and produce an unhandled 500 error visible to the user. `RegisterAction` has the same pattern (line 30) but mitigates it slightly by also calling `request.getSession()` (without `false`) on line 32, which is inconsistent. Both files use the same unsafe pattern for the initial `getSession(false)` call.

A25-3 | HIGH | RegisterAction.java:32 | Double session retrieval — inconsistent and potentially hazardous. Line 30 calls `request.getSession(false)` and binds it to `session`. Line 32 then calls `request.getSession()` (no `false`), which will *create* a new session if none exists. This is inconsistent with the intent of `getSession(false)` and could silently create a new empty session, causing `sessArrComp` on line 33 (read from the original `session`) to be a different session object than the one used to read `sessCompId` on line 32. The two `getAttribute` calls are operating on potentially different session references.

A25-4 | HIGH | RegisterAction.java:33-34 | Unchecked cast and potential NullPointerException on session attribute. `sessArrComp` is cast from `Object` to `ArrayList<CompanyBean>` (raw-cast, no guard) and then immediately dereferenced with `.get(0)` on line 34 with no null check and no bounds check. If the attribute is absent, or the list is empty, this will throw an unchecked `ClassCastException` or `IndexOutOfBoundsException`, respectively, propagating as an unhandled exception.

A25-5 | MEDIUM | RegisterAction.java:33 | Raw/unchecked cast produces a compiler warning. `(ArrayList<CompanyBean>) session.getAttribute("sessArrComp")` is an unchecked cast at runtime due to type erasure. The compiler will emit an `unchecked cast` warning. The same pattern applies to line 34 where `(String)` is cast but `CompanyBean.getTemplate()` already returns `String`, making the explicit cast on that line redundant and misleading. This should use a typed accessor or suppress the warning with documentation.

A25-6 | MEDIUM | RegisterAction.java:68 | `QuestionDAO` instantiated with `new` instead of the singleton/factory pattern used elsewhere. All other DAO references in both files (`CompanyDAO.getInstance()`, `DriverDAO.getInstance()`) follow a singleton pattern. On line 68, `QuestionDAO` is instantiated with `new QuestionDAO()` directly inside the method body, bypassing whatever lifecycle, connection-pooling, or state management the DAO layer intends. This is a leaky abstraction and a layer-coupling inconsistency.

A25-7 | MEDIUM | RegisterAction.java:12 | Wildcard import. `import org.apache.struts.action.*;` is the only wildcard import in either file. All other imports (in both files) are explicit. This is a style inconsistency and makes it harder to determine which Struts Action types are actually used.

A25-8 | MEDIUM | RegisterAction.java:23 | Declared logger `log` is never used within the class. The field `private static Logger log` is assigned on line 23 but no `log.info`, `log.warn`, `log.error`, or similar call appears anywhere in `RegisterAction.java`. This is dead code and produces an "unused field" compiler/IDE warning. It also means that errors in the registration flow (duplicate name, duplicate licence, save failure) are silently swallowed with no log output.

A25-9 | LOW | RegisterAction.java:38 | Mixed naming conventions for local variables. `fname` and `lname` are abbreviated (lines 36-37), while `licence` uses a full word (line 38). The `DriverBean` setters use `first_name`, `last_name` (snake_case, lines 41-42) while other setters use camelCase (`setExpirydt`, `setLicno`, `setDepartment`, `setLocation`, `setComp_id`). The inconsistency spans both the local variable names and the bean setter naming convention within a single method.

A25-10 | LOW | RegisterAction.java:59 | Typo in ActionMessage key. The message key `"error.duplcateLicence"` (line 59) is misspelled — it should be `"error.duplicateLicence"` (missing the `i` in `duplicate`). The corresponding key on line 51 is spelled correctly as `"error.duplicateName"`. This inconsistency will silently cause the wrong or missing message to be displayed to the user when a duplicate licence is detected, as the properties file key will not match.

A25-11 | LOW | PrivacyAction.java | Missing `@Override` consistency across files. `PrivacyAction.execute` is correctly annotated with `@Override` (line 15). `RegisterAction.execute` (line 27) omits the `@Override` annotation despite overriding the same inherited method. This is a style inconsistency between the two files and means the compiler cannot warn if the method signature drifts.

A25-12 | INFO | PrivacyAction.java, RegisterAction.java | Both files use Apache Struts 1 (`org.apache.struts.action.*`) and Apache Log4j 1.x (`org.apache.log4j.Logger`). Struts 1 reached end-of-life in 2013 and Log4j 1.x reached end-of-life in 2015. Both dependencies are unmaintained and have known security vulnerabilities (Struts: multiple RCEs; Log4j 1.x: CVE-2019-17571 and others). These are not code-quality findings per se but are flagged as infrastructure-level risk visible from the imports.
# P4 Agent A26 — ResetPasswordAction, SearchAction

## Reading Evidence

### ResetPasswordAction
- Class: `ResetPasswordAction` extends `org.apache.struts.action.Action` (line 24)
- Methods:
  - `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse) : ActionForward` (line 26) — overrides `Action.execute`
- Constants/Types: None defined in this class
- Imports used: `HttpServletRequest`, `HttpServletResponse`, `HttpSession`, `Action`, `ActionErrors`, `ActionForm`, `ActionForward`, `ActionMapping`, `ActionMessage`, `ActionMessages`, `ResetPassActionForm`, `CompanyBean`, `PasswordRequest`, `PasswordResponse`, `CompanyDAO`, `RestClientService`, `RuntimeConf`, `Util`

### SearchAction
- Class: `SearchAction` extends `org.apache.struts.action.Action` (line 31)
- Methods:
  - `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse) : ActionForward` (line 37) — overrides `Action.execute`
- Constants/Types: None defined in this class
- Fields:
  - `log` — `private static Logger` (line 33)
  - `driverDao` — `private DriverDAO` (line 35), instance-level field initialised via `DriverDAO.getInstance()`
- Imports used: `ArrayList`, `List`, `ServletException`, `HttpServletRequest`, `HttpServletResponse`, `HttpSession`, `Action`, `ActionErrors`, `ActionForm`, `ActionForward`, `ActionMapping`, `ActionMessage`, `Logger`, `InfoLogger`, `SearchActionForm`, `DriverDAO`, `QuestionDAO`, `CompanyBean`, `DriverBean`, `QuestionBean`

---

## Findings

A26-1 | LOW | ResetPasswordAction.java:36 | Typo in local variable name: `restClientServce` (missing `i` — should be `restClientService`). This is a naming convention violation and reduces readability.

A26-2 | LOW | ResetPasswordAction.java:42 | Typo in message key string: `"reset.succuss"` (should be `"reset.success"`). This will silently fail to resolve the correct message key at runtime and display a raw key or blank message to the user.

A26-3 | MEDIUM | ResetPasswordAction.java:15 | Unused import: `com.actionform.ResetPassActionForm` is imported but never referenced in the class body. The `form` parameter of `execute` is never cast to `ResetPassActionForm`. This is dead import / dead code.

A26-4 | MEDIUM | ResetPasswordAction.java:16 | Unused import: `com.bean.CompanyBean` is imported but never referenced anywhere in the file.

A26-5 | MEDIUM | ResetPasswordAction.java:19 | Unused import: `com.dao.CompanyDAO` is imported but never referenced anywhere in the file.

A26-6 | MEDIUM | ResetPasswordAction.java:22 | Unused import: `com.util.Util` is imported but never referenced anywhere in the file.

A26-7 | MEDIUM | ResetPasswordAction.java:29 | Null-dereference risk: `request.getSession(false)` can return `null` if no session exists. The very next line dereferences `session` (line 33) without a null-check. If the session has expired or was never created, this will throw a `NullPointerException` at runtime.

A26-8 | MEDIUM | SearchAction.java:40 | Null-dereference risk: `request.getSession(false)` can return `null`. The result is immediately dereferenced on lines 41 and 43 without a null-check, producing the same risk as A26-7 in `ResetPasswordAction`.

A26-9 | MEDIUM | SearchAction.java:43-44 | Unchecked cast and potential `NullPointerException`/`IndexOutOfBoundsException`: `session.getAttribute("sessArrComp")` is cast to `ArrayList<CompanyBean>` without any null-check (line 43), and `sessArrComp.get(0)` (line 44) is called without verifying the list is non-null and non-empty. A missing or empty session attribute causes an unchecked-cast warning and a runtime crash.

A26-10 | LOW | SearchAction.java:43 | Raw / unchecked cast warning: `(ArrayList<CompanyBean>) session.getAttribute("sessArrComp")` performs an unchecked generic cast. The compiler will emit an `unchecked cast` warning because `HttpSession.getAttribute` returns `Object`. This will surface as a build warning.

A26-11 | LOW | SearchAction.java:7 | Unused import: `javax.servlet.ServletException` is imported but never referenced in the file. The `execute` method declares `throws Exception`, not `throws ServletException`.

A26-12 | LOW | SearchAction.java:33 | Logger field `log` is declared but never used anywhere in `SearchAction`. The class defines it (line 33) but no `log.debug/info/warn/error` calls appear in the file body. This is dead code.

A26-13 | HIGH | ResetPasswordAction.java:37 | Leaky abstraction / direct instantiation of service in action: `new RestClientService()` is constructed inline inside the action method, tightly coupling the controller layer directly to the service implementation. There is no interface or injection point, making the class untestable in isolation and violating separation of concerns.

A26-14 | HIGH | SearchAction.java:46 | Direct DAO instantiation inside action method: `new QuestionDAO()` is created inline (line 46). Combined with the instance field `driverDao = DriverDAO.getInstance()` (line 35), two different DAO acquisition patterns are mixed in the same class (constructor vs. singleton). This inconsistency is both a style violation and a leaky-abstraction issue — the action layer directly manages DAO lifecycle rather than receiving collaborators via injection.

A26-15 | LOW | ResetPasswordAction.java vs SearchAction.java | Style inconsistency across files: `ResetPasswordAction` uses 4-space indentation inside the class body (lines 29–54) mixed with tab indentation for the method signature and closing brace, producing inconsistent whitespace. `SearchAction` uses 4-space indentation consistently. Neither matches a single unified style, and trailing whitespace/blank lines differ between the two files (e.g. blank lines 35–36 in `ResetPasswordAction.java` vs. none in equivalent positions in `SearchAction`).

A26-16 | LOW | ResetPasswordAction.java:24 | Missing space before opening brace in class declaration: `extends Action{` (no space before `{`). `SearchAction` at line 31 correctly writes `extends Action {` with a space. This is an inconsistent formatting style between the two files.

A26-17 | INFO | SearchAction.java:48 | Use of `arrQues.size() > 0` instead of `!arrQues.isEmpty()` (also line 52 for `arrDriver`). While not a bug, `isEmpty()` is the idiomatic and marginally more efficient form and its absence is a minor style inconsistency within this codebase.
# P4 Agent A27 — SessionReportAction, SwitchCompanyAction

## Reading Evidence

### SessionReportAction
- Class: `SessionReportAction extends Action` (line 17)
- Methods:
  - `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` (line 19)
- Constants/Types: none defined in this class
- Imports: `SessionReportSearchForm`, `DriverDAO`, `UnitDAO`, `ReportService`, Struts `Action`/`ActionForm`/`ActionForward`/`ActionMapping`, `HttpServletRequest`, `HttpServletResponse`, `HttpSession`, `java.util.Objects`

### SwitchCompanyAction
- Class: `SwitchCompanyAction extends Action` (line 19), annotated `@Slf4j`
- Methods:
  - `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` (line 20)
- Constants/Types: none defined in this class
- Imports: `SwitchCompanyActionForm`, `CompanyBean`, `LoginDAO`, `CompanySessionSwitcher`, Lombok `@Slf4j`, Struts `Action`/`ActionForm`/`ActionForward`/`ActionMapping`, `HttpServletRequest`, `HttpServletResponse`, `HttpSession`, `java.util.List`

---

## Findings

A27-1 | HIGH | SwitchCompanyAction.java:31 | Null-pointer risk on unboxing `Boolean` session attributes. `isSuperAdmin` and `isDealerLogin` are retrieved from the session as `Boolean` (boxed) objects and immediately unboxed in the boolean expression `!isSuperAdmin && !isDealerLogin` (line 31). If either attribute is absent from the session (e.g. after session expiry or misconfiguration), the auto-unbox throws a `NullPointerException` before the guard check can protect anything. The same risk applies to `loggedInCompanyId` (line 29) if `sessAccountId` is absent and `getCompanies` is called with a null `Integer`.

A27-2 | HIGH | SessionReportAction.java:20-21 | Null session reference not guarded. `request.getSession(false)` (line 20) can return `null` when no session exists; the very next line (21) calls `session.getAttribute(...)` unconditionally. This is a latent `NullPointerException` that will surface whenever the action is reached without an active session (e.g. direct URL access after session timeout).

A27-3 | HIGH | SwitchCompanyAction.java:25 | Same unguarded null-session pattern as A27-2. `request.getSession(false)` (line 25) is not null-checked before attribute access begins on line 27.

A27-4 | MEDIUM | SwitchCompanyAction.java:36-38 | Loop exits only on last match; all matching companies silently overwrite each other with no break. If `LoginDAO.getCompanies` ever returns a list where more than one entry has the same id as `loginActionForm.getCurrentCompany()`, `CompanySessionSwitcher.UpdateCompanySessionAttributes` is called multiple times. More importantly, if no company matches the supplied id the method silently falls through and returns `"successAdmin"` without changing any session attribute, giving the caller a misleading success signal. A guard (`return mapping.findForward("failure")`) or a `break` after a successful match should be present.

A27-5 | MEDIUM | SwitchCompanyAction.java:40 | Redundant attribute copy via session round-trip. `request.setAttribute("isDealer", session.getAttribute("isDealer"))` copies a value that `CompanySessionSwitcher.UpdateCompanySessionAttributes` just placed in the session (see `CompanySessionSwitcher.java` line 43). This couples `SwitchCompanyAction` to the internal implementation detail that `CompanySessionSwitcher` stores the value under the key `"isDealer"`. If that key name changes in the utility class the action silently propagates `null` to the view without any compile-time error.

A27-6 | MEDIUM | SessionReportAction.java:30-31 | Mixed parameter types for the same conceptual `companyId`. `UnitDAO.getAllUnitsByCompanyId` receives an `int` (`compId`, line 30) while `DriverDAO.getAllDriver` receives the raw `String` (`sessCompId`, line 31) for the same company. This inconsistency in the call sites suggests either the DAOs have inconsistent signatures or the action is working around them ad hoc. Using the already-parsed `compId` throughout would be safer and clearer.

A27-7 | MEDIUM | SwitchCompanyAction.java:18 | `@Slf4j` logger declared but never used. Lombok injects a `log` field via the `@Slf4j` annotation, but no log statement appears anywhere in `SwitchCompanyAction`. The annotation is dead — no logging occurs even for the authorization failure path (line 32) or session-switch completion. This is both a dead-code issue and a missed observability point.

A27-8 | LOW | SwitchCompanyAction.java:20-23 | `execute` method is missing the `@Override` annotation. `SessionReportAction.execute` (line 18) correctly carries `@Override`, but the same method in `SwitchCompanyAction` (line 20) does not. This is an inconsistent style between the two files in the same package and removes the compile-time safety that `@Override` provides.

A27-9 | LOW | SwitchCompanyAction.java:26 | Misleading local variable name. The form is cast to `SwitchCompanyActionForm` but stored in a variable named `loginActionForm` (line 26). The type being switched is a company selection form, not a login form. This name is a residual copy-paste artifact that reduces readability and could mislead future maintainers.

A27-10 | LOW | SessionReportSearchForm.java:17-20 | Field names use `snake_case` (`vehicle_id`, `driver_id`, `start_date`, `end_date`) contrary to Java naming conventions (camelCase). Because these are Struts `ActionForm` fields bound to HTTP parameter names, the unconventional casing leaks HTTP parameter naming into the domain model and makes it harder to distinguish form fields from local variables. Referenced here because `SessionReportAction` directly depends on and uses this form.

A27-11 | INFO | SessionReportAction.java:19 | Method signature declares `throws Exception`. Both action classes declare `throws Exception` on `execute`. While this is the signature required by the Struts `Action` base class, it prevents the compiler from enforcing specific exception handling at call sites and masks distinct failure modes (e.g., `NumberFormatException` from `Integer.parseInt` on line 25, DB exceptions from DAOs). Worth noting as a build-quality indicator in the context of the broader codebase standard.
# P4 Agent A28 — SwitchLanguageAction, SwitchRegisterAction, WelcomeAction

## Reading Evidence

### SwitchLanguageAction
- Class: `SwitchLanguageAction` extends `Action` (line 18)
- Fields:
  - `log` — `private static Logger` (line 20)
- Methods:
  - `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` (line 22) — `public ActionForward`
  - `getCookie(HttpServletRequest, String)` (line 71) — `public static Cookie`
  - `getLocale(String)` (line 83) — `public static Locale`
- Constants/Types defined: none

### SwitchRegisterAction
- Class: `SwitchRegisterAction` extends `Action` (line 17)
- Fields:
  - `log` — `private static Logger` (line 18)
- Methods:
  - `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` (line 20) — `public ActionForward`
- Constants/Types defined: none

### WelcomeAction
- Class: `WelcomeAction` extends `Action` (line 33)
- Fields:
  - `log` — `private static Logger` (line 35)
- Methods:
  - `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` (line 37) — `public ActionForward`
- Constants/Types defined: none

---

## Findings

A28-1 | LOW | SwitchLanguageAction.java:20 | Unused private field `log`. The `Logger` field is declared and initialised but never called anywhere in the class body. This is dead code and will produce a compiler/IDE warning.

A28-2 | LOW | SwitchRegisterAction.java:18 | Unused private field `log`. Same pattern as A28-1 — the `Logger` is declared but never referenced. Dead field.

A28-3 | LOW | WelcomeAction.java:35 | Unused private field `log`. Same pattern as A28-1 — the `Logger` is declared but never referenced. Dead field.

A28-4 | MEDIUM | SwitchLanguageAction.java:71,83 | Leaky abstraction — utility methods `getCookie` and `getLocale` are declared `public static` on an Action class, making them part of that class's public API. `WelcomeAction` already cross-calls `SwitchLanguageAction.getCookie(...)` (WelcomeAction.java:40) and `SwitchLanguageAction.getLocale(...)` (WelcomeAction.java:43), coupling two Action classes together via static dispatch. These helpers belong in a shared utility class (e.g. `CookieUtil`, `LocaleUtil`), not on a concrete Action. This is a tight coupling / wrong-layer placement.

A28-5 | MEDIUM | SwitchRegisterAction.java:23 | Potential NullPointerException — `request.getSession(false)` can return `null` when no session exists, but the result is dereferenced without a null-check on line 25 (`session.setAttribute(...)`). Every other Action in this set uses `request.getSession()` (without `false`), which always creates a session if absent. This inconsistency will cause a `NullPointerException` for any unauthenticated or session-less request hitting the register flow.

A28-6 | LOW | SwitchLanguageAction.java:62 | Magic number — the cookie max-age is expressed as the literal arithmetic expression `24*60*60` (86400 seconds) with no named constant or explanatory comment describing the intended lifetime (one day). Inline arithmetic literals of this kind should be a named constant to convey intent and allow single-point change.

A28-7 | LOW | SwitchLanguageAction.java:18 | Minor style inconsistency — the class declaration `extends Action{` has no space before the opening brace, while `SwitchRegisterAction` (line 17) has `extends Action {` with a space. `WelcomeAction` (line 33) also has no space (`extends Action{`). The inconsistency is between the three files; within the file set there is no single agreed convention.

A28-8 | LOW | SwitchLanguageAction.java:22-69 | Inconsistent indentation inside `execute`. The method body mixes 4-space, 8-space, and 16-space indentation without a consistent pattern (visible from lines 25–68). This makes the block structure visually misleading and differs from the clean 4-space indent used in `SwitchRegisterAction`.

A28-9 | HIGH | WelcomeAction.java:3-16 | Multiple unused imports — the following imports are present but no corresponding type is used anywhere in `WelcomeAction.java`:
  - `java.io.File` (line 3)
  - `java.io.FileNotFoundException` (line 4)
  - `java.io.FileOutputStream` (line 5)
  - `java.io.InputStream` (line 6)
  - `java.io.OutputStream` (line 7)
  - `java.io.PrintWriter` (line 8)
  - `java.util.ArrayList` (line 9)
  - `javax.servlet.http.Part` (line 15)
  - `org.apache.struts.action.ActionErrors` (line 20)
  - `org.apache.struts.action.ActionMessage` (line 24)
  - `org.apache.struts.action.ActionMessages` (line 25)
  - `com.util.RuntimeConf` (line 30)
  - `com.util.Util` (line 31)

  This is a large block of dead imports, suggesting this class was created by copying from another Action and the irrelevant imports were never removed. Rated HIGH because the volume strongly implies copy-paste origin, which in turn implies functionality that was intended to be here may have been omitted.

A28-10 | INFO | SwitchLanguageAction.java:9 | Deprecated logging API — `org.apache.log4j.Logger` is used directly (all three files). Log4j 1.x reached end-of-life and contains known vulnerabilities (CVE-2019-17571 among others). All three files share this pattern; consolidation to SLF4J or Log4j 2 is recommended at the project level.

A28-11 | INFO | SwitchLanguageAction.java:100,105 | Three-argument `Locale` constructor deprecated since Java 19 — `new Locale("tr","TR","")` and `new Locale("ms","MY","")` use the `(language, country, variant)` constructor that is deprecated from Java 19 onward in favour of `Locale.of(...)`. Low urgency unless the project targets Java 19+, but worth tracking.
# P4 Agent A29 — AdminAlertActionForm, AdminDealerActionForm, AdminDriverAddForm

## Reading Evidence

### AdminAlertActionForm
- Class: `AdminAlertActionForm` extends `ActionForm` (line 7)
- Fields:
  - `private int alertId` (line 9)
  - `private String alertDesc` (line 10)
  - `private String alertCode` (line 11)
  - `private ArrayList arrVehicles` (raw type, initialised `new ArrayList()`) (line 12)
  - `private String action` (line 13)
  - `private String[] unitIds` (line 14)
  - `private String alert_id` (line 15)
  - `private int impactLevel` (line 18)
  - `private boolean isActive` (line 19)
- Methods:
  - `getAlertId()` (line 21)
  - `getAlertDesc()` (line 24)
  - `getAlertCode()` (line 27)
  - `setAlertId(int alertId)` (line 30)
  - `setAlertDesc(String alertDesc)` (line 33)
  - `setAlertCode(String alertCode)` (line 36)
  - `getArrVehicles()` (line 39)
  - `setArrVehicles(ArrayList arrVehicles)` (line 42)
  - `getAction()` (line 45)
  - `setAction(String action)` (line 48)
  - `getUnitIds()` (line 51)
  - `setUnitIds(String[] unitIds)` (line 54)
  - `getImpactLevel()` (line 57)
  - `setImpactLevel(int impactLevel)` (line 60)
  - `isActive()` (line 63)
  - `setActive(boolean isActive)` (line 66)
  - `getAlert_id()` (line 69)
  - `setAlert_id(String alert_id)` (line 72)

### AdminDealerActionForm
- Class: `AdminDealerActionForm` extends `ActionForm` (line 11)
- Annotations: `@Getter`, `@Setter`, `@NoArgsConstructor` (lines 8–10)
- Fields:
  - `private String companyId` (line 12)
- Methods: all generated by Lombok (`getCompanyId()`, `setCompanyId(String)`, no-arg constructor)

### AdminDriverAddForm
- Class: `AdminDriverAddForm` extends `ActionForm` (line 20)
- Annotations: `@Getter`, `@Setter`, `@NoArgsConstructor`, `@Slf4j` (lines 16–19)
- Fields:
  - `private Long id` (line 22)
  - `private String first_name` (line 23)
  - `private String last_name` (line 24)
  - `private String licence_number` (line 25)
  - `private String expiry_date` (line 26)
  - `private String security_number` (line 27)
  - `private String address` (line 28)
  - `private String app_access` (line 29)
  - `private String mobile` (line 30)
  - `private String email_addr` (line 31)
  - `private String pass` (line 32)
  - `private String cpass` (line 33)
  - `private String location` (line 34)
  - `private String department` (line 35)
  - `private String op_code` (line 36)
- Methods:
  - `validate(ActionMapping mapping, HttpServletRequest request)` (line 38)
  - `getDriverBean(String sessCompId)` (line 61)
  - All Lombok-generated getters/setters for each of the 15 fields above

---

## Findings

A29-1 | HIGH | AdminAlertActionForm.java:12 | Raw type `ArrayList` used without a type parameter on field `arrVehicles` and its getter/setter (lines 12, 39, 42). This suppresses all compile-time type safety and will generate an unchecked-cast warning. Should be `ArrayList<SomeType>` or preferably `List<SomeType>`.

A29-2 | MEDIUM | AdminAlertActionForm.java:15 | Field `alert_id` (snake_case, line 15) duplicates the semantic role of field `alertId` (camelCase, line 9). Both hold an alert identifier — one as `int`, the other as `String`. Having two fields for the same concept with different names and types is confusing and a potential source of bugs. The accessors `getAlert_id()` / `setAlert_id()` (lines 69–74) also break the standard Java naming convention.

A29-3 | MEDIUM | AdminAlertActionForm.java:15,69,72 | Naming convention violation: field `alert_id` and its accessors `getAlert_id()` / `setAlert_id()` use snake_case, which is inconsistent with every other field and accessor in the same class (all camelCase). This is the only occurrence of snake_case in this file.

A29-4 | MEDIUM | AdminDriverAddForm.java:23-36 | All 13 String fields use snake_case (`first_name`, `last_name`, `licence_number`, `expiry_date`, `security_number`, `email_addr`, `app_access`, `op_code`) instead of the Java standard camelCase. Lombok generates getters/setters that mirror these names (e.g. `getFirst_name()`), making the public API non-standard. The mixed convention is also inconsistent with `AdminDealerActionForm` which uses camelCase (`companyId`).

A29-5 | MEDIUM | AdminDriverAddForm.java:41,47 | Null-pointer risk in `validate()`: `first_name.equalsIgnoreCase("")` (line 41) and `last_name.equalsIgnoreCase("")` (line 47) will throw `NullPointerException` if either field is `null` (the default initial value declared on lines 23–24). The idiomatic safe form is `"".equalsIgnoreCase(first_name)` or an explicit null check. The same risk applies to the `pass`/`cpass` comparison on line 53.

A29-6 | MEDIUM | AdminDriverAddForm.java:53 | `pass.equalsIgnoreCase(cpass)` (line 53) compares passwords case-insensitively. Password equality checks should be case-sensitive (`equals`, not `equalsIgnoreCase`), otherwise "Password1" and "password1" are treated as identical, weakening security.

A29-7 | LOW | AdminAlertActionForm.java:1-75 | `AdminAlertActionForm` hand-writes all getters and setters (18 methods for 9 fields) without using Lombok, while `AdminDealerActionForm` and `AdminDriverAddForm` in the same package use `@Getter`/`@Setter`/`@NoArgsConstructor`. This inconsistency in approach adds boilerplate and maintenance burden.

A29-8 | LOW | AdminDriverAddForm.java:33 | Field `cpass` (confirm-password) is exposed via a Lombok-generated public getter `getCpass()`. Exposing the raw confirmation-password string in the public form-bean API is a minor leaky abstraction; the field is only needed transiently during validation and could be kept package-private or cleared after use.

A29-9 | LOW | AdminDriverAddForm.java:36 | Field `op_code` is declared but never referenced within this class (no usage in `validate()` or `getDriverBean()`). It may be dead code or an intentionally unused form binding, but its purpose is undocumented.

A29-10 | INFO | AdminDriverAddForm.java:80 | String concatenation used in a log statement: `log.debug("driverBean : " + driverBean)`. Prefer the SLF4J parameterised form `log.debug("driverBean : {}", driverBean)` to avoid the String concatenation cost when DEBUG logging is disabled.

A29-11 | INFO | AdminAlertActionForm.java:17 | The comment `//impact alert variables` (line 17) separates `impactLevel` and `isActive` from the other fields but no similar section comments exist for the other fields. This minor inconsistency gives the impression the class was extended incrementally without a unified structure.
# P4 Agent A30 — AdminDriverEditForm, AdminFleetcheckActionForm, AdminFleetcheckDeleteActionForm

## Reading Evidence

### AdminDriverEditForm.java

**Class:** `AdminDriverEditForm extends ActionForm`
Lombok annotations: `@Getter`, `@Setter`, `@NoArgsConstructor`

**Fields (lines 28–49):**
- `Long id` (line 28)
- `String first_name` (line 29)
- `String last_name` (line 30)
- `String licence_number` (line 31)
- `String expiry_date` (line 32)
- `String security_number` (line 33)
- `String address` (line 34)
- `String app_access` (line 35)
- `String mobile` (line 36)
- `String email_addr` (line 37)
- `String redImpactAlert` (line 38)
- `String redImpactSMSAlert` (line 39)
- `String driverDenyAlert` (line 40)
- `String pass` (line 41)
- `String cpass` (line 42)
- `String location` (line 43)
- `String department` (line 44)
- `String op_code` (line 45)
- `String pass_hash` (line 46)
- `String cognito_username` (line 47)
- `List<DriverUnitBean> vehicles` (line 49)

**Methods:**
- `getVehicle(int index)` — line 51
- `validate(ActionMapping, HttpServletRequest)` — line 61
- `isLicenceNumberInvalid(String)` — line 127 (private)
- `containSpecialCharatcter(String)` — line 133 (private)
- `getDriverVehicle(String sessCompId)` — line 139
- `getLicenseBean()` — line 149

---

### AdminFleetcheckActionForm.java

**Class:** `AdminFleetcheckActionForm extends ActionForm`
Lombok annotations: `@Getter`, `@Setter`

**Fields (lines 20–28):**
- `String action` (line 20)
- `String id` (line 21)
- `String manu_id` (line 22)
- `String type_id` (line 23)
- `String fuel_type_id` (line 24)
- `String attachment_id` (line 25)
- `ArrayList arrAdminUnitType` (line 26) — raw type
- `ArrayList arrAdminUnitFuelType` (line 27) — raw type
- `ArrayList arrAttachment` (line 28) — raw type

**Methods:**
- `AdminFleetcheckActionForm()` constructor — line 30
- `setArrAdminUnitType()` — line 37
- `setArrAdminUnitFuelType()` — line 41
- `setArrAttachment()` — line 45
- `validate(ActionMapping, HttpServletRequest)` — line 49

---

### AdminFleetcheckDeleteActionForm.java

**Class:** `AdminFleetcheckDeleteActionForm extends ValidateIdExistsAbstractActionForm`

**Fields:** none (inherits `protected String id` from parent)

**Methods:** none (inherits `validate(ActionMapping, HttpServletRequest)` from parent)

---

## Findings

A30-1 | HIGH | AdminDriverEditForm.java:14 | Unused import: `lombok.extern.slf4j.Slf4j` is imported but `@Slf4j` annotation is never applied to the class and no `log` references exist in the file. This import serves no purpose and will generate a compiler warning.

A30-2 | HIGH | AdminDriverEditForm.java:13 | Unused import: `com.util.DateUtil` is imported but never referenced anywhere in the file. Dead import.

A30-3 | HIGH | AdminDriverEditForm.java:12 | Unused import: `com.dao.CompanyDAO` is imported but never referenced anywhere in the file. Dead import.

A30-4 | HIGH | AdminDriverEditForm.java:3 | Unused import: `java.sql.SQLException` is imported but never referenced anywhere in the file. Dead import.

A30-5 | MEDIUM | AdminDriverEditForm.java:29 | Naming convention inconsistency: most fields use `snake_case` (e.g., `first_name`, `last_name`, `op_code`, `pass_hash`) while three fields on lines 38–40 (`redImpactAlert`, `redImpactSMSAlert`, `driverDenyAlert`) use `camelCase`. The indentation of these three lines also uses tabs while the surrounding fields use spaces, indicating they were added at a different time without following the established convention.

A30-6 | MEDIUM | AdminDriverEditForm.java:79 | Inline comment `//remove the password mast` (line 79) is a stale/incomplete developer note ("mast" instead of "mask") left in production code. It adds noise and should be removed or corrected into a proper Javadoc/block comment.

A30-7 | MEDIUM | AdminDriverEditForm.java:89 | Semantic mismatch in DriverBean builder call: `.first_last(this.first_name)` passes only the first name to a field named `first_last` (which semantically implies a concatenated full name). The field name in `DriverBean` is documented as a combined first+last string, yet only the first name value is provided here. This is a potential data correctness bug or at minimum a misleading field assignment.

A30-8 | MEDIUM | AdminDriverEditForm.java:133 | Method name `containSpecialCharatcter` (line 133) contains a double typo: "contain" should be "contains" and "Charatcter" should be "Character". Private method, but this degrades code readability.

A30-9 | MEDIUM | AdminFleetcheckActionForm.java:26-28 | Raw type usage: `ArrayList arrAdminUnitType`, `ArrayList arrAdminUnitFuelType`, and `ArrayList arrAttachment` all use the raw `ArrayList` type without a type parameter. This suppresses generic type safety and will produce unchecked cast / raw-type compiler warnings.

A30-10 | MEDIUM | AdminFleetcheckActionForm.java:30 | Constructor declares `throws Exception` for a form bean. `ActionForm` constructors are called reflectively by the Struts framework, which does not expect checked exceptions from `ActionForm` constructors. If the DAO calls in `setArrAdminUnitType()`, `setArrAdminUnitFuelType()`, or `setArrAttachment()` throw, Struts will receive an undeclared checked exception, likely causing an opaque runtime failure. This is a leaky abstraction: DAO-layer errors (database unavailability) escape through the form layer with no error handling or meaningful message.

A30-11 | LOW | AdminFleetcheckActionForm.java:37-46 | The three `setArrAdminUnitType()`, `setArrAdminUnitFuelType()`, and `setArrAttachment()` setter methods do not follow the JavaBeans / Lombok setter convention: they take no parameter and instead load data from a DAO. A setter named `setX()` is universally expected to accept a value of type X. The `@Getter`/`@Setter` Lombok annotations on the class will also generate additional redundant `setArrAdminUnitType(ArrayList)` etc. setters alongside these custom ones, creating duplicate and confusing setter overloads that can be misused.

A30-12 | LOW | AdminDriverEditForm.java:11 | Wildcard import `com.bean.*` is used while all other imports in the same file are explicit. Wildcard imports obscure which types are actually used and can cause future ambiguity if the `com.bean` package grows.
# P4 Agent A31 — AdminFleetcheckEditActionForm, AdminFleetcheckHideActionForm, AdminFleetcheckShowActionForm

## Reading Evidence

### AdminFleetcheckEditActionForm.java
- **Class:** `AdminFleetcheckEditActionForm extends ActionForm`
- **Annotations:** `@Getter`, `@Setter`, `@Slf4j`, `@NoArgsConstructor`
- **Methods:** None declared explicitly (all accessors generated by Lombok)
- **Fields:**
  - `private static final long serialVersionUID = -8103158863153194997L;` (line 18)
  - `private String id = null;` (line 20)
  - `private String content = null;` (line 21)
  - `private String expectedanswer = null;` (line 22)
  - `private int order_no;` (line 23)
  - `private String active = null;` (line 24)
  - `private String type_id = null;` (line 25)
  - `private String fuel_type_id = null;` (line 26)
  - `private String answer_type = null;` (line 27)
  - `private String comp_id = null;` (line 28)
  - `private ArrayList<AnswerTypeBean> arrAnswerType = new ArrayList<>();` (line 29)
  - `private String manu_id = null;` (line 30)
  - `private String attachment_id = null;` (line 31)

---

### AdminFleetcheckHideActionForm.java
- **Class:** `AdminFleetcheckHideActionForm extends ValidateIdExistsAbstractActionForm`
- **Annotations:** `@Getter`, `@Setter`
- **Methods:**
  - `validate(ActionMapping mapping, HttpServletRequest request) : ActionErrors` (lines 21–38, `@Override`)
- **Fields:**
  - `private String type_id = null;` (line 15)
  - `private String fuel_type_id = null;` (line 16)
  - `private String manu_id = null;` (line 17)
  - `private String attachment_id = null;` (line 18)

---

### AdminFleetcheckShowActionForm.java
- **Class:** `AdminFleetcheckShowActionForm extends ValidateIdExistsAbstractActionForm`
- **Annotations:** None
- **Methods:** None
- **Fields:** None

---

## Findings

A31-1 | LOW | AdminFleetcheckEditActionForm.java:8 | `@Slf4j` is imported and applied but the class contains no logging statements and no explicit methods at all. The logger is never used, producing an unused-field build warning from some static-analysis tools and unnecessary bytecode.

A31-2 | LOW | AdminFleetcheckEditActionForm.java:17 | `AdminFleetcheckEditActionForm` extends `ActionForm` directly rather than the project's `ValidateIdExistsAbstractActionForm` base class, even though it declares an identical `id` field (line 20). This duplicates the `id` field that already exists in the abstract base and bypasses the shared validation logic for that field that `AdminFleetcheckHideActionForm` and `AdminFleetcheckShowActionForm` both inherit.

A31-3 | MEDIUM | AdminFleetcheckEditActionForm.java:20 | Field `id` in `AdminFleetcheckEditActionForm` shadows the `protected String id` in `ValidateIdExistsAbstractActionForm` (if inheritance were corrected), and as-is it duplicates that field's purpose with no validation — the `validate()` method from the abstract base is never called for this form, leaving `id` unchecked.

A31-4 | LOW | AdminFleetcheckEditActionForm.java:20-31 | All field names use `snake_case` (`order_no`, `type_id`, `fuel_type_id`, `answer_type`, `comp_id`, `manu_id`, `attachment_id`, `expectedanswer`) rather than Java's conventional `camelCase`. This is inconsistent with standard Java naming conventions and with the `ValidateIdExistsAbstractActionForm` base class which uses `camelCase` internally. The same naming pattern exists in `AdminFleetcheckHideActionForm` fields (`type_id`, `fuel_type_id`, `manu_id`, `attachment_id`), indicating a codebase-wide style issue originating in these forms.

A31-5 | LOW | AdminFleetcheckEditActionForm.java:29 | Field `arrAnswerType` is declared as the concrete type `ArrayList<AnswerTypeBean>` rather than the interface type `List<AnswerTypeBean>`. This is a leaky abstraction — callers are unnecessarily coupled to the `ArrayList` implementation. Programming to interfaces (`List`) is the standard Java practice.

A31-6 | INFO | AdminFleetcheckEditActionForm.java:3 | Import `java.util.ArrayList` is used only for the field declaration type (finding A31-5). If the field were changed to `List`, an import of `java.util.List` would be needed and the `ArrayList` import would remain only for the initialiser — a minor but worth noting consequence of A31-5.

A31-7 | MEDIUM | AdminFleetcheckHideActionForm.java:27 | The error key added to `ActionErrors` for manufacturer validation is `"manufacture"` (line 27) while the field is named `manu_id`. The key is a misspelling of `"manufacturer"` (missing trailing `r`). If any JSP or message-bundle consumer references the key `"manufacturer"`, the error will be silently swallowed.

A31-8 | INFO | AdminFleetcheckHideActionForm.java:18 | Field `attachment_id` is declared in `AdminFleetcheckHideActionForm` but is never referenced in the `validate()` method. If attachment is intended to be a required input for hide operations, its validation is missing. If it is optional, the dead field still contributes to the public API surface unnecessarily.

A31-9 | INFO | AdminFleetcheckShowActionForm.java:3 | `AdminFleetcheckShowActionForm` is an empty class body — it adds no fields and no methods beyond what `ValidateIdExistsAbstractActionForm` already provides. This is a valid marker-type pattern for Struts form wiring, but warrants documentation (a brief Javadoc comment) to make the intent explicit to future maintainers.

A31-10 | LOW | AdminFleetcheckEditActionForm.java:23 | Field `order_no` is declared as primitive `int` and is the only field not initialised to `null` (it defaults to `0`). All other fields are `String` and initialised to `null`. If `order_no` is not submitted in the form post, it silently defaults to `0` rather than being detectable as absent, which may mask missing-value errors during validation. The inconsistency also makes the field stand out stylistically.
# P4 Agent A32 — AdminManufacturersActionForm, AdminRegisterActionForm, AdminSendMailActionForm

## Reading Evidence

### AdminManufacturersActionForm.java

- **Class:** `AdminManufacturersActionForm`
- **Superclass:** `org.apache.struts.action.ActionForm`
- **Annotations:** `@Getter`, `@Setter`, `@Slf4j`, `@NoArgsConstructor` (all via Lombok)
- **Methods:** None explicitly defined (all getters/setters generated by Lombok at compile time)
- **Fields:**
  - `private String manufacturerId` (line 14)
  - `private String manufacturer` (line 15)
  - `private String action` (line 16)

---

### AdminRegisterActionForm.java

- **Class:** `AdminRegisterActionForm` (`public final`)
- **Superclass:** `org.apache.struts.validator.ValidatorForm`
- **Annotations:** None
- **Fields:**
  - `private String id` (line 9)
  - `private String name` (line 10)
  - `private String address` (line 11)
  - `private String postcode` (line 12)
  - `private String email` (line 13)
  - `private String contact_no` (line 14)
  - `private String contact_fname` (line 15)
  - `private String contact_lname` (line 16)
  - `private String password` (line 17)
  - `private String pin` (line 18)
  - `private String refnm` (line 19)
  - `private String refno` (line 20)
  - `private String question` (line 21)
  - `private String answer` (line 22)
  - `private String code` (line 23)
  - `private String accountAction` (line 24)
  - `private String unit` (line 25)
  - `private String subemail` (line 26)
  - `private String timezone` (line 27)
  - `private String lan_id` (line 28)
  - `private String mobile` (line 29)
- **Methods (all hand-written):**
  - `getLan_id()` / `setLan_id(String)` — lines 31–36
  - `getName()` / `setName(String)` — lines 37–42
  - `getAddress()` / `setAddress(String)` — lines 43–48
  - `getPostcode()` / `setPostcode(String)` — lines 49–54
  - `getEmail()` / `setEmail(String)` — lines 55–60
  - `getContact_no()` / `setContact_no(String)` — lines 61–66
  - `getContact_fname()` / `setContact_fname(String)` — lines 67–72
  - `getContact_lname()` / `setContact_lname(String)` — lines 73–78
  - `getPassword()` / `setPassword(String)` — lines 79–84
  - `getPin()` / `setPin(String)` — lines 85–90
  - `getRefnm()` / `setRefnm(String)` — lines 91–96
  - `getRefno()` / `setRefno(String)` — lines 97–102
  - `getQuestion()` / `setQuestion(String)` — lines 103–108
  - `getAnswer()` / `setAnswer(String)` — lines 109–114
  - `getCode()` / `setCode(String)` — lines 115–120
  - `getId()` / `setId(String)` — lines 121–126
  - `getAccountAction()` / `setAccountAction(String)` — lines 127–132
  - `getUnit()` / `setUnit(String)` — lines 133–138
  - `getSubemail()` / `setSubemail(String)` — lines 139–144
  - `getTimezone()` / `setTimezone(String)` — lines 145–150
  - `getMobile()` / `setMobile(String)` — lines 151–156

---

### AdminSendMailActionForm.java

- **Class:** `AdminSendMailActionForm`
- **Superclass:** `org.apache.struts.validator.ValidatorForm`
- **Annotations:** None
- **Fields:**
  - `private String id` (line 7)
  - `private String email` (line 8)
  - `private String accountAction` (line 9)
- **Methods (all hand-written):**
  - `getEmail()` / `setEmail(String)` — lines 13–19
  - `getAccountAction()` / `setAccountAction(String)` — lines 21–27
  - `getId()` / `setId(String)` — lines 29–35

---

## Findings

A32-1 | HIGH | AdminRegisterActionForm.java:3 | Unused import `java.util.ArrayList`. The class declares no field, parameter, or local variable of type `ArrayList` or `List`. This import is dead and will generate an "unused import" compiler warning on any IDE or strict-warning build.

A32-2 | HIGH | AdminManufacturersActionForm.java:6 | `@Slf4j` is imported and applied but the class body is empty (no hand-written methods). No log statements can exist, meaning the generated `log` field is never used. This will produce an "unused field" warning and adds a runtime dependency (SLF4J logger initialisation) for no benefit. The annotation should be removed.

A32-3 | MEDIUM | AdminManufacturersActionForm.java:13 / AdminRegisterActionForm.java:7 / AdminSendMailActionForm.java:5 | Missing `serialVersionUID` in all three classes. `ActionForm` and `ValidatorForm` implement `java.io.Serializable`. All three classes extend these types without declaring a `private static final long serialVersionUID`. This causes a compiler/IDE warning (`-Xlint:serial`) and means the auto-generated UID will change across recompilations, silently breaking any serialised session state that is stored (e.g. in clustered or persisted HTTP sessions).

A32-4 | MEDIUM | AdminRegisterActionForm.java:14,15,16,28,61–78,31–36 | Field names `contact_no`, `contact_fname`, `contact_lname`, and `lan_id` use snake_case, violating the Java naming convention (camelCase for fields). The corresponding getters and setters mirror this violation: `getContact_no()`, `setContact_no()`, `getContact_fname()`, `setContact_fname()`, `getContact_lname()`, `setContact_lname()`, `getLan_id()`, `setLan_id()`. This is inconsistent with all other fields in the same class (e.g. `accountAction`, `subemail`, `timezone`) and with the naming style used in `AdminManufacturersActionForm` and `AdminSendMailActionForm`. Struts/BeanUtils property binding may also behave unexpectedly with underscored property names.

A32-5 | MEDIUM | AdminRegisterActionForm.java:7 vs AdminManufacturersActionForm.java:13 | Inconsistent use of Lombok. `AdminManufacturersActionForm` uses `@Getter`, `@Setter`, and `@NoArgsConstructor` to generate boilerplate, while `AdminRegisterActionForm` (21 fields, 42 hand-written accessor methods) and `AdminSendMailActionForm` (3 fields, 6 hand-written accessor methods) manually write all accessors. The hand-written approach in these two files produces ~100 lines of boilerplate that could be replaced by Lombok annotations, and creates a maintenance inconsistency across the package.

A32-6 | LOW | AdminRegisterActionForm.java:7 | `AdminRegisterActionForm` is declared `public final`, making it impossible to subclass. No other form class in this package is `final`. This is inconsistent with the rest of the codebase and may unnecessarily restrict future extension; the `final` modifier appears unintentional rather than a deliberate design decision.

A32-7 | LOW | AdminSendMailActionForm.java:37–39 | Three consecutive blank lines at the end of the class body (lines 37–39) before the closing brace. This is minor formatting noise but is inconsistent with the tighter formatting in the other two files.

A32-8 | LOW | AdminRegisterActionForm.java:19,20 | Field names `refnm` and `refno` are cryptic abbreviations with no documentation comment explaining what "ref" stands for (reference number? reference name?). Combined with the corresponding accessors `getRefnm()` / `getRefno()`, this reduces readability and maintainability. None of the other fields in the three files use similarly opaque abbreviated names.

A32-9 | INFO | AdminManufacturersActionForm.java:16 | The field `action` (line 16) has a very generic name that shadows the concept of "action" used throughout the Struts framework itself (e.g. `Action`, `ActionForm`). While not a compile error, this naming choice is a leaky abstraction: the field mixes a framework-level concept name into a domain-level DTO, making its purpose ambiguous to maintainers.
# P4 Agent A33 — AdminSettingsActionForm, AdminTrainingsActionForm, AdminUnitAccessForm

## Reading Evidence

### AdminSettingsActionForm.java
- **Class:** `AdminSettingsActionForm`
- **Superclass:** `org.apache.struts.action.ActionForm`
- **Lombok annotations:** `@Getter`, `@Setter`, `@Slf4j`, `@NoArgsConstructor`
- **Fields:**
  - `private static final long serialVersionUID = 7884549462560104854L` (line 23)
  - `private String id` (line 24)
  - `private String dateFormat` (line 25)
  - `private Integer maxSessionLength` (line 26)
  - `private String action` (line 27)
  - `private String timezone` (line 28)
  - `private String redImpactAlert` (line 29)
  - `private String redImpactSMSAlert` (line 30)
  - `private String driverDenyAlert` (line 31)
- **Methods:**
  - `validate(ActionMapping, HttpServletRequest) : ActionErrors` (line 33)

---

### AdminTrainingsActionForm.java
- **Class:** `AdminTrainingsActionForm`
- **Superclass:** `org.apache.struts.action.ActionForm`
- **Lombok annotations:** `@Getter`, `@Setter`, `@Slf4j`, `@NoArgsConstructor`
- **Fields:**
  - `private String action` (line 14)
  - `private Long driver` (line 16)
  - `private Long manufacturer` (line 17)
  - `private Long type` (line 18)
  - `private Long fuelType` (line 19)
  - `private String trainingDate` (line 20)
  - `private String expirationDate` (line 21)
  - `private Long training` (line 23)
- **Methods:** None (Lombok-generated only)
- **Note:** No `serialVersionUID` declared. No `validate()` override.

---

### AdminUnitAccessForm.java
- **Class:** `AdminUnitAccessForm`
- **Superclass:** `org.apache.struts.action.ActionForm`
- **Lombok annotations:** `@Data`, `@NoArgsConstructor`
- **Imports (unused/suspect):** `com.dao.ManufactureDAO`, `com.dao.UnitDAO`, `org.apache.commons.beanutils.BeanUtils`, `org.apache.commons.beanutils.PropertyUtils`
- **Fields:**
  - `private String id` (line 25)
  - `private boolean accessible` (line 26)
  - `private String access_type` (line 27)
  - `private String keypad_reader` (line 28)
  - `private String facility_code` (line 29)
  - `private String access_id` (line 30)
- **Methods:**
  - `validate(ActionMapping, HttpServletRequest) : ActionErrors` (line 33)
  - `getUnit(String compId) : UnitBean` (line 39)
  - `setUnit(UnitBean unitBean) : void` (line 51)
- **Note:** No `serialVersionUID` declared.

---

## Findings

A33-1 | MEDIUM | AdminTrainingsActionForm.java:13 | Missing `serialVersionUID`. `AdminTrainingsActionForm` extends `ActionForm` (which implements `Serializable`) but declares no `serialVersionUID`. This will generate a compiler/IDE warning and means the auto-generated UID can change across compilations, breaking deserialization. Both sibling forms `AdminSettingsActionForm` and `AdminUnitAccessForm` (via `@Data`) should also be compared — `AdminSettingsActionForm` does declare one (line 23), making the omission here an inconsistency across the family of form classes.

A33-2 | MEDIUM | AdminUnitAccessForm.java:23 | Missing `serialVersionUID`. `AdminUnitAccessForm` extends `ActionForm` but does not declare a `serialVersionUID`. `@Data` does not generate one. This is inconsistent with `AdminSettingsActionForm`, which correctly declares one, and will produce a build warning.

A33-3 | LOW | AdminUnitAccessForm.java:4-5 | Unused imports. `com.dao.ManufactureDAO` (line 4) and `com.dao.UnitDAO` (line 5) are imported but never referenced anywhere in the class body. These are dead imports, likely left over from an earlier implementation, and will generate compiler warnings. Similarly `org.apache.commons.beanutils.BeanUtils` (line 8) and `org.apache.commons.beanutils.PropertyUtils` (line 9) are imported but unused.

A33-4 | LOW | AdminUnitAccessForm.java:27-30 | Field naming convention violation. Fields `access_type`, `keypad_reader`, `facility_code`, and `access_id` use `snake_case`, which violates Java naming conventions (camelCase) and is inconsistent with every other field in this class (`id`, `accessible`) and with all fields in the sibling form classes. `@Data` will generate getters/setters such as `getAccess_type()` rather than `getAccessType()`, which is non-standard and can cause issues with frameworks that rely on JavaBean introspection (e.g., Struts form population, BeanUtils property mapping).

A33-5 | LOW | AdminUnitAccessForm.java:33-37 | Empty `validate()` method. The `validate()` override creates and immediately returns an empty `ActionErrors` object with no validation logic. While this may be intentional (validation handled elsewhere), it is indistinguishable from an incomplete stub and creates a false impression that validation is performed. A comment explaining the intentional absence would prevent future maintainers from adding incorrect logic here.

A33-6 | INFO | AdminTrainingsActionForm.java:13 | Missing `validate()` override. Unlike `AdminSettingsActionForm` (which validates `dateFormat`, `timezone`, and `maxSessionLength`) and `AdminUnitAccessForm` (which has a stub), `AdminTrainingsActionForm` has no `validate()` method at all. Given it carries fields such as `trainingDate` and `expirationDate` that are plausible candidates for validation, the absence may indicate incomplete implementation rather than a deliberate design choice.

A33-7 | INFO | AdminTrainingsActionForm.java:11 | `@Slf4j` annotation is present but no logging calls exist in the class. Because there are no methods in the class body (only fields), the `log` field injected by `@Slf4j` is entirely unused. This is a minor dead-code smell consistent with copy-paste from `AdminSettingsActionForm`. The same observation applies, to a lesser extent, to `AdminSettingsActionForm` itself, where `@Slf4j` is declared (line 17) but `log` is never referenced in the single `validate()` method.

A33-8 | INFO | AdminSettingsActionForm.java:37 | Prefer `isEmpty()` over `.equals("")`. The null-guarded emptiness checks throughout `validate()` use `.equals("")` (lines 37, 42) rather than the idiomatic `isEmpty()` or `StringUtils.isBlank()`. This is a minor style inconsistency — `AdminUnitAccessForm` already imports and uses `org.apache.commons.lang.StringUtils` for blank checks, while `AdminSettingsActionForm` does not, leading to an inconsistent approach across related form classes.
# P4 Agent A34 — AdminUnitAssignForm, AdminUnitChecklistForm, AdminUnitEditForm

## Reading Evidence

### AdminUnitAssignForm.java

- **Class:** `AdminUnitAssignForm`
- **Superclass:** `org.apache.struts.action.ActionForm`
- **Annotations:** `@Data`, `@NoArgsConstructor` (Lombok)
- **Methods:** None explicitly defined (all getters/setters generated by Lombok `@Data`)
- **Fields:**
  - `String id` (line 12)
  - `String unit_id` (line 13)
  - `String company_id` (line 14)
  - `String start` (line 15)
  - `String end` (line 16)
- **Imports unused:** `java.util.Date` (line 7)
- **serialVersionUID:** Absent

---

### AdminUnitChecklistForm.java

- **Class:** `AdminUnitChecklistForm`
- **Superclass:** `org.apache.struts.action.ActionForm`
- **Annotations:** None (manual getters/setters)
- **Fields:**
  - `static final long serialVersionUID = -2208616500078494492L` (line 11)
  - `int id` (line 13)
  - `int unitId` (line 14)
  - `String action` (line 15)
  - `boolean driverBased` (line 17)
- **Methods:**
  - `getId()` — line 20
  - `getUnitId()` — line 23
  - `setId(int id)` — line 27
  - `setUnitId(int unitId)` — line 30
  - `isDriverBased()` — line 33
  - `setDriverBased(boolean driverBased)` — line 36
  - `getAction()` — line 40
  - `setAction(String action)` — line 43

---

### AdminUnitEditForm.java

- **Class:** `AdminUnitEditForm`
- **Superclass:** `org.apache.struts.action.ActionForm`
- **Annotations:** `@Data` (Lombok)
- **Fields:**
  - `String id` (line 24)
  - `String name` (line 25)
  - `String location` (line 26)
  - `String department` (line 27)
  - `String type_id` (line 28)
  - `String active` (line 29)
  - `String manu_id` (line 30)
  - `String size` (line 31)
  - `String hourmeter` (line 32)
  - `String serial_no` (line 33)
  - `String fuel_type_id` (line 34)
  - `List arrAdminUnitType` (line 35) — raw type
  - `List arrAdminUnitFuelType` (line 36) — raw type
  - `List arrMenufacture` (line 37) — raw type
  - `String mac_address` (line 38)
  - `String exp_mod` (line 39)
  - `boolean accessible` (line 41)
  - `String access_type` (line 42)
  - `String keypad_reader` (line 43)
  - `String facility_code` (line 44)
  - `String access_id` (line 45)
  - `String op_code` (line 46)
  - `String weight_unit` (line 47)
- **Methods:**
  - `AdminUnitEditForm()` constructor — line 50
  - `setArrAdminUnitType()` (private) — line 56
  - `setArrAdminUnitFuelType()` (private) — line 60
  - `validate(ActionMapping, HttpServletRequest)` — line 64
  - `getUnit(String compId)` — line 110
  - `setUnit(UnitBean unitBean)` — line 136
- **serialVersionUID:** Absent

---

## Findings

A34-1 | MEDIUM | AdminUnitAssignForm.java:7 | Unused import `java.util.Date`. The `Date` type is never referenced in the file; the import is a leftover and produces a compiler warning.

A34-2 | LOW | AdminUnitAssignForm.java:12-16 | Field names use `snake_case` (`unit_id`, `company_id`) instead of Java-standard `camelCase`. Lombok `@Data` will generate getters/setters such as `getUnit_id()` which is non-standard and inconsistent with the `camelCase` fields in `AdminUnitChecklistForm` (`unitId`) and `AdminUnitEditForm`.

A34-3 | HIGH | AdminUnitAssignForm.java:11 | `ActionForm` subclass does not declare `serialVersionUID`. `ActionForm` implements `Serializable`; omitting `serialVersionUID` causes a compiler/IDE warning and makes the class fragile across recompilations or deployments involving session serialization.

A34-4 | LOW | AdminUnitChecklistForm.java:5 | Missing space before opening brace: `extends ActionForm{` (no space before `{`). Minor style inconsistency compared to other classes in the package.

A34-5 | LOW | AdminUnitChecklistForm.java:8-10 | Auto-generated empty Javadoc stub (`/** \n * \n */`) above `serialVersionUID`. This is noise with no informational value and should be removed or replaced with a meaningful comment.

A34-6 | MEDIUM | AdminUnitEditForm.java:35-37 | Three raw-type `List` fields (`arrAdminUnitType`, `arrAdminUnitFuelType`, `arrMenufacture`) are declared without generic type parameters. This suppresses compile-time type safety and generates unchecked-type warnings.

A34-7 | HIGH | AdminUnitEditForm.java:37 | Field `arrMenufacture` is a misspelling of "Manufacture" (should be `arrManufacture`). The import for `ManufactureDAO` (line 18) confirms the correct spelling is "Manufacture". The field is also declared but never populated anywhere in this file — there is no corresponding `setArrMenufacture()` call in the constructor — making it an unused/dead field as well.

A34-8 | HIGH | AdminUnitEditForm.java:18 | Import `com.dao.ManufactureDAO` is unused within this file. No call to `ManufactureDAO` appears anywhere in `AdminUnitEditForm.java`, resulting in a dead import/build warning.

A34-9 | HIGH | AdminUnitEditForm.java:46 | Field `op_code` has a getter and setter generated by `@Data` but is never referenced within the class body (not passed to `UnitBean.builder()` in `getUnit()` at lines 111-131). This is an asymmetric/dead field: it is exposed publicly but silently discarded when building the domain object, which can cause silent data loss.

A34-10 | MEDIUM | AdminUnitEditForm.java:28-47 | Multiple field names use `snake_case` (`type_id`, `manu_id`, `serial_no`, `fuel_type_id`, `mac_address`, `exp_mod`, `access_type`, `keypad_reader`, `facility_code`, `access_id`, `op_code`, `weight_unit`) while `accessible` is `camelCase`. This is internally inconsistent and diverges from Java naming conventions throughout the form.

A34-11 | HIGH | AdminUnitEditForm.java:50 | Constructor `AdminUnitEditForm()` is declared `throws Exception`. Struts instantiates `ActionForm` subclasses reflectively; a checked exception on the no-arg constructor can cause silent runtime failures during form instantiation, and the broad `Exception` declaration masks the specific cause.

A34-12 | HIGH | AdminUnitEditForm.java:11 | `ActionForm` subclass does not declare `serialVersionUID` (same issue as A34-3 for this class). `@Data` from Lombok does not generate `serialVersionUID`.

A34-13 | MEDIUM | AdminUnitEditForm.java:93 | Regex pattern `x` is named with a single-character, meaningless identifier. It should be a named constant (e.g., `DECIMAL_PATTERN`) to aid readability and maintainability.

A34-14 | MEDIUM | AdminUnitEditForm.java:101 | `validate()` calls `getUnit(null)` and injects a `List<UnitBean>` into the request attribute `"arrAdminUnit"` (lines 101-105). Populating request attributes is a side effect inside a validation method; this is unexpected, non-idiomatic Struts design and makes the method harder to test and reason about.

A34-15 | INFO | AdminUnitChecklistForm.java vs AdminUnitEditForm.java | The two files use entirely different coding styles: `AdminUnitChecklistForm` is written with manual getters/setters and no Lombok, while `AdminUnitEditForm` uses `@Data`. Within the same package there is no consistent approach, which increases maintenance burden.
# P4 Agent A35 — AdminUnitImpactForm, AdminUnitServiceForm, DealerCompaniesActionForm

## Reading Evidence

---

### AdminUnitImpactForm.java

- **Class:** `AdminUnitImpactForm`
- **Superclass:** `org.apache.struts.action.ActionForm`
- **Package:** `com.actionform`

**Fields (all private):**

| Field | Type | Line |
|---|---|---|
| `serialVersionUID` | `static final long` | 11 |
| `id` | `int` | 13 |
| `unitId` | `int` | 14 |
| `servLast` | `int` | 15 |
| `servNext` | `int` | 16 |
| `servDuration` | `int` | 17 |
| `accHours` | `double` | 18 |
| `hourmeter` | `double` | 20 |
| `action` | `String` | 22 |
| `servType` | `String` | 23 |
| `servStatus` | `String` | 24 |

**Methods:**

| Method | Line |
|---|---|
| `getId()` | 26 |
| `getUnitId()` | 29 |
| `getServLast()` | 32 |
| `getServNext()` | 35 |
| `getServDuration()` | 38 |
| `getAction()` | 41 |
| `getServType()` | 44 |
| `setId(int)` | 47 |
| `setUnitId(int)` | 50 |
| `setServLast(int)` | 53 |
| `setServNext(int)` | 56 |
| `setServDuration(int)` | 59 |
| `setAction(String)` | 62 |
| `setServType(String)` | 65 |
| `getServStatus()` | 68 |
| `setServStatus(String)` | 71 |
| `getHourmeter()` | 74 |
| `setHourmeter(double)` | 77 |
| `getAccHours()` | 80 |
| `setAccHours(double)` | 83 |

---

### AdminUnitServiceForm.java

- **Class:** `AdminUnitServiceForm`
- **Superclass:** `org.apache.struts.action.ActionForm`
- **Package:** `com.actionform`

**Fields (all private):**

| Field | Type | Line |
|---|---|---|
| `serialVersionUID` | `static final long` | 11 |
| `id` | `int` | 13 |
| `unitId` | `int` | 14 |
| `servLast` | `int` | 15 |
| `servNext` | `int` | 16 |
| `servDuration` | `int` | 17 |
| `accHours` | `double` | 18 |
| `hourmeter` | `double` | 20 |
| `action` | `String` | 22 |
| `servType` | `String` | 23 |
| `servStatus` | `String` | 24 |

**Methods:**

| Method | Line |
|---|---|
| `getId()` | 26 |
| `getUnitId()` | 29 |
| `getServLast()` | 32 |
| `getServNext()` | 35 |
| `getServDuration()` | 38 |
| `getAction()` | 41 |
| `getServType()` | 44 |
| `setId(int)` | 47 |
| `setUnitId(int)` | 50 |
| `setServLast(int)` | 53 |
| `setServNext(int)` | 56 |
| `setServDuration(int)` | 59 |
| `setAction(String)` | 62 |
| `setServType(String)` | 65 |
| `getServStatus()` | 68 |
| `setServStatus(String)` | 71 |
| `getHourmeter()` | 74 |
| `setHourmeter(double)` | 77 |
| `getAccHours()` | 80 |
| `setAccHours(double)` | 83 |

---

### DealerCompaniesActionForm.java

- **Class:** `DealerCompaniesActionForm`
- **Superclass:** `org.apache.struts.action.ActionForm`
- **Package:** `com.actionform`
- **Fields:** None
- **Methods:** None (empty class body)

---

## Findings

A35-1 | HIGH | AdminUnitServiceForm.java:11 | `serialVersionUID` value (`-2208616500078494492L`) is identical to the one in `AdminUnitImpactForm.java:11`. Two distinct `Serializable` classes sharing the same `serialVersionUID` is incorrect; it can cause silent deserialization failures or cross-class compatibility errors if serialized instances of either class are ever stored or transmitted.

A35-2 | HIGH | AdminUnitImpactForm.java / AdminUnitServiceForm.java | These two classes are byte-for-byte identical in content (same fields, same methods, same line structure, same `serialVersionUID`). One is dead/duplicate code. Either the duplication is unintentional (one class should be deleted) or each class was meant to model a distinct concept with different fields. As-is, maintaining both independently guarantees they will diverge silently over time.

A35-3 | MEDIUM | DealerCompaniesActionForm.java:1-6 | Class body is completely empty — no fields, no methods, no `serialVersionUID`. As a subclass of `ActionForm` (which implements `Serializable`), the absence of `serialVersionUID` will generate a compiler/IDE warning. An entirely empty form class serves no purpose and is likely a stub that was never completed or never cleaned up (dead code).

A35-4 | LOW | AdminUnitImpactForm.java:5 | No space before the opening brace in the class declaration (`extends ActionForm{`). All other classes in the same package use `extends ActionForm {` (with a space). Minor but inconsistent style.

A35-5 | LOW | AdminUnitServiceForm.java:5 | Same missing space before opening brace as A35-4 (`extends ActionForm{`). Both `AdminUnitImpactForm` and `AdminUnitServiceForm` share this style deviation; `DealerCompaniesActionForm` uses the correct spacing (`extends ActionForm {`).

A35-6 | LOW | AdminUnitImpactForm.java / AdminUnitServiceForm.java | The empty Javadoc comment block on `serialVersionUID` (lines 8-10 in both files) is a style noise artifact — the generated stub comment `/** \n * \n */` with no actual content provides no value and should be removed or replaced with a meaningful comment.
# P4 Agent A36 — DriverJobDetailsActionForm, FleetcheckActionForm, GPSReportSearchForm

## Reading Evidence

---

### DriverJobDetailsActionForm.java

**Class:** `DriverJobDetailsActionForm`
**Superclass:** `org.apache.struts.action.ActionForm`
**Package:** `com.actionform`

**Fields (lines 9–22):**
| Field | Type | Line |
|-------|------|------|
| `id` | `int` | 9 |
| `action` | `String` | 10 |
| `equipId` | `String` | 11 |
| `jobId` | `String` | 12 |
| `driverList` | `ArrayList` (raw) | 13 |
| `name` | `String` | 14 |
| `startTime` | `String` | 15 |
| `endTime` | `String` | 16 |
| `fromTime` | `String` | 17 |
| `toTime` | `String` | 18 |
| `instruct` | `String` | 19 |
| `jobTitle` | `String` | 20 |
| `description` | `String` | 21 |
| `driverId` | `String` | 22 |

**Methods:**
| Method | Line |
|--------|------|
| `getId()` | 24 |
| `getAction()` | 27 |
| `getEquipId()` | 30 |
| `getJobId()` | 33 |
| `getDriverList()` | 36 |
| `getName()` | 39 |
| `getStartTime()` | 42 |
| `getEndTime()` | 45 |
| `getFromTime()` | 48 |
| `getToTime()` | 51 |
| `getInstruct()` | 54 |
| `setId(int)` | 57 |
| `setAction(String)` | 60 |
| `setEquipId(String)` | 63 |
| `setJobId(String)` | 66 |
| `setDriverList(ArrayList)` | 69 |
| `setName(String)` | 72 |
| `setStartTime(String)` | 75 |
| `setEndTime(String)` | 78 |
| `setFromTime(String)` | 81 |
| `setToTime(String)` | 84 |
| `setInstruct(String)` | 87 |
| `getJobTitle()` | 90 |
| `getDescription()` | 93 |
| `setJobTitle(String)` | 96 |
| `setDescription(String)` | 99 |
| `getDriverId()` | 102 |
| `setDriverId(String)` | 105 |

**Notes:** No `serialVersionUID` declared. No commented-out code. All 14 fields have symmetric getter/setter pairs.

---

### FleetcheckActionForm.java

**Class:** `FleetcheckActionForm`
**Superclass:** `org.apache.struts.action.ActionForm`
**Package:** `com.actionform`

**Imports (unused):**
- `javax.servlet.http.HttpServletRequest` (line 3)
- `org.apache.struts.action.ActionMessage` (line 5)
- `org.apache.struts.action.ActionErrors` (line 6)
- `org.apache.struts.action.ActionMapping` (line 8)

**Fields (lines 12–18):**
| Field | Type | Line |
|-------|------|------|
| `id` | `String[]` | 12 |
| `answer` | `String[]` | 13 |
| `faulty` | `String[]` | 14 |
| `comment` | `String` | 15 |
| `veh_id` | `String` | 16 |
| `att_id` | `String` | 17 |
| `hourmeter` | `String` | 18 |

**Methods:**
| Method | Line |
|--------|------|
| `getHourmeter()` | 20 |
| `setHourmeter(String)` | 23 |
| `getId()` | 26 |
| `setId(String[])` | 29 |
| `getAnswer()` | 32 |
| `setAnswer(String[])` | 35 |
| `getComment()` | 38 |
| `setComment(String)` | 41 |
| `getVeh_id()` | 44 |
| `setVeh_id(String)` | 47 |
| `getFaulty()` | 50 |
| `setFaulty(String[])` | 53 |
| `getAtt_id()` | 56 |
| `setAtt_id(String)` | 59 |

**Notes:** No `serialVersionUID` declared. No commented-out code. All 7 fields have symmetric getter/setter pairs. Fields `veh_id` and `att_id` use snake_case naming; getters/setters mirror this (`getVeh_id`, `setVeh_id`, `getAtt_id`, `setAtt_id`).

---

### GPSReportSearchForm.java

**Class:** `GPSReportSearchForm`
**Superclass:** `org.apache.struts.action.ActionForm`
**Package:** `com.actionform`
**Annotations:** `@Data` (Lombok)

**Fields (lines 18–25):**
| Field | Type | Line |
|-------|------|------|
| `manu_id` | `Long` | 18 |
| `type_id` | `Long` | 19 |
| `start_date` | `String` | 20 |
| `end_date` | `String` | 21 |
| `unitId` | `int` | 22 |
| `manufacturers` | `List<ManufactureBean>` | 24 |
| `unitTypes` | `List<UnitTypeBean>` | 25 |

**Methods:**
| Method | Line |
|--------|------|
| `GPSReportSearchForm()` (constructor) | 27 |
| `getGPSReportFilter(String)` | 30 |

**Notes:** Getters/setters for all fields are Lombok-generated via `@Data`. No `serialVersionUID` declared. No commented-out code. Mixed naming: `manu_id`, `type_id`, `start_date`, `end_date` use snake_case; `unitId`, `manufacturers`, `unitTypes` use camelCase.

---

## Findings

A36-1 | HIGH | DriverJobDetailsActionForm.java:7 | Missing `serialVersionUID`. The class extends `ActionForm` (which implements `Serializable`) but declares no `serialVersionUID` field. This will cause a compiler/build warning and can lead to `InvalidClassException` if serialized objects are persisted or transmitted across versions.

A36-2 | HIGH | FleetcheckActionForm.java:10 | Missing `serialVersionUID`. Same issue as A36-1 — class extends `ActionForm` with no `serialVersionUID` declared.

A36-3 | HIGH | GPSReportSearchForm.java:17 | Missing `serialVersionUID`. Same issue as A36-1 — class extends `ActionForm` with no `serialVersionUID` declared.

A36-4 | MEDIUM | FleetcheckActionForm.java:16-17 | Snake_case field names `veh_id` (line 16) and `att_id` (line 17) violate Java camelCase naming convention. The getter/setter names `getVeh_id()`, `setVeh_id()`, `getAtt_id()`, `setAtt_id()` propagate this inconsistency into the public API and will not be treated as standard JavaBean properties by most frameworks (Struts, Spring, etc.).

A36-5 | MEDIUM | GPSReportSearchForm.java:18-21 | Four fields use snake_case (`manu_id`, `type_id`, `start_date`, `end_date`) while the remaining fields (`unitId`, `manufacturers`, `unitTypes`) use camelCase. This mixed naming convention within the same class is inconsistent. Lombok's `@Data` will generate non-standard accessor names (e.g., `getManu_id()`) for the snake_case fields, which Struts/Spring MVC may fail to bind correctly.

A36-6 | MEDIUM | FleetcheckActionForm.java:3-8 | Four unused imports: `HttpServletRequest` (line 3), `ActionMessage` (line 5), `ActionErrors` (line 6), and `ActionMapping` (line 8). These are not referenced anywhere in the class body. They indicate dead validation scaffolding was removed or never completed, and they produce compiler warnings.

A36-7 | MEDIUM | DriverJobDetailsActionForm.java:13 | Raw type `ArrayList` used for field `driverList` (line 13) and its getter `getDriverList()` (line 36) and setter `setDriverList(ArrayList)` (line 69). The element type is unknown, eliminating compile-time type safety and producing an unchecked-type build warning.

A36-8 | LOW | GPSReportSearchForm.java:36 | Redundant duplicate condition in `unitId` null-coalescing expression: `this.unitId == 0 || this.unitId == 0` (line 36). Both operands are identical; the second condition is dead code and the `||` has no effect. This is likely a copy-paste error; the intended second condition was probably a different sentinel value check (e.g., `this.unitId < 0`).

A36-9 | LOW | DriverJobDetailsActionForm.java:108-110 | Three consecutive blank lines at the end of the class body (lines 108–110) before the closing brace. Minor whitespace/style issue.
# P4 Agent A37 — ImpactReportSearchForm, IncidentReportSearchForm, LoginActionForm

## Reading Evidence

### 1. ImpactReportSearchForm.java

- **Class:** `ImpactReportSearchForm`
- **Superclass:** `ActionForm` (org.apache.struts.action.ActionForm) — direct extension, NOT via `ReportSearchForm`
- **Annotations:** `@Data` (Lombok)
- **serialVersionUID:** not declared

**Fields (all instance, all private):**

| Name | Type | Line |
|------|------|------|
| `manu_id` | `Long` | 18 |
| `type_id` | `Long` | 19 |
| `start_date` | `String` | 20 |
| `end_date` | `String` | 21 |
| `impact_level` | `String` | 22 |
| `timezone` | `String` | 23 |
| `manufacturers` | `List<ManufactureBean>` | 25 |
| `unitTypes` | `List<UnitTypeBean>` | 26 |
| `impactLevels` | `List<ImpactLevel>` | 27 |

**Methods:**

| Method | Line |
|--------|------|
| `ImpactReportSearchForm()` (constructor) | 29 |
| `getImpactReportFilter(String dateFormat)` | 32 |

Note: All getters/setters are Lombok-generated via `@Data`.

---

### 2. IncidentReportSearchForm.java

- **Class:** `IncidentReportSearchForm`
- **Superclass:** `ReportSearchForm` (which extends `ActionForm`)
- **Annotations:** `@Data`, `@EqualsAndHashCode(callSuper = false)`
- **serialVersionUID:** `-7959149868858265846L` (line 13)

**Fields declared in this class:** none (all fields inherited from `ReportSearchForm`: `manu_id`, `type_id`, `start_date`, `end_date`, `timezone`, `manufacturers`, `unitTypes`)

**Methods:**

| Method | Line |
|--------|------|
| `getIncidentReportFilter(String dateFormat)` | 15 |

Note: All getters/setters for inherited fields are provided by `@Data` on parent `ReportSearchForm`.

---

### 3. LoginActionForm.java

- **Class:** `LoginActionForm` (`final`)
- **Superclass:** `ValidatorForm` (org.apache.struts.validator.ValidatorForm)
- **Annotations:** `@Data`, `@EqualsAndHashCode(callSuper = true)`
- **serialVersionUID:** `-4392152148586227798L` (line 13)

**Fields (all instance, all private):**

| Name | Type | Default | Line |
|------|------|---------|------|
| `username` | `String` | `null` | 15 |
| `password` | `String` | `null` | 16 |
| `message` | `String` | `null` | 17 |
| `action` | `String` | `null` | 18 |
| `timezone` | `String` | `null` | 19 |

**Methods:**

| Method | Line |
|--------|------|
| `reset(ActionMapping mapping, HttpServletRequest request)` | 21 |
| `getTimezone()` | 26 |

Note: `getTimezone()` is an explicit override of the Lombok-generated getter. All other getters/setters are Lombok-generated via `@Data`.

---

## Findings

A37-1 | HIGH | ImpactReportSearchForm.java:17 | **Missing `serialVersionUID`**: `ImpactReportSearchForm` extends `ActionForm`, which implements `Serializable`, but declares no `serialVersionUID`. The other two forms both declare explicit `serialVersionUID` values. This omission is inconsistent and will produce a compiler/IDE warning; JVM auto-generation is fragile and can cause `InvalidClassException` across deployments.

A37-2 | HIGH | ImpactReportSearchForm.java:17-27 | **Does not extend `ReportSearchForm`**: `ImpactReportSearchForm` extends `ActionForm` directly instead of the shared `ReportSearchForm` base class, then re-declares the five identical fields (`manu_id`, `type_id`, `start_date`, `end_date`, `timezone`) and two identical list fields (`manufacturers`, `unitTypes`) that already exist in `ReportSearchForm`. This is field duplication across a family of closely related classes. `IncidentReportSearchForm` correctly uses `ReportSearchForm` as its base.

A37-3 | MEDIUM | ImpactReportSearchForm.java:34 | **Inconsistent `null` guard on `start_date`**: On line 34, the `startDate` mapping uses `StringUtils.isBlank(start_date)` (no `this.` prefix), while all other field references in the same builder call (`this.manu_id`, `this.type_id`, `this.end_date`, `this.impact_level`, `this.timezone`) use the explicit `this.` qualifier. The `IncidentReportSearchForm` version (line 19) consistently uses `this.start_date`. This is a minor style inconsistency but increases cognitive friction and could mask a scoping issue if a local variable of the same name were ever introduced.

A37-4 | MEDIUM | LoginActionForm.java:15-19 | **Mixed indentation**: Fields `username` (line 15), `action` (line 18), and `timezone` (line 19) are indented with 4 spaces, while `password` (line 16), `message` (line 17), and the `reset` and `getTimezone` method bodies use a tab character. This is visible in the raw source as mixed whitespace within the same class and is inconsistent with the other two files which use uniform 4-space indentation.

A37-5 | MEDIUM | ImpactReportSearchForm.java:25-26 | **Raw-type style in diamond operator**: `new ArrayList<ManufactureBean>()` and `new ArrayList<UnitTypeBean>()` are used instead of the shorter and idiomatic `new ArrayList<>()` (diamond inference, available since Java 7). `ReportSearchForm` (lines 27-28) has the same pattern, which suggests a project-wide inconsistency. Modern Java and most static-analysis tools flag this as unnecessary repetition of the type argument.

A37-6 | LOW | IncidentReportSearchForm.java:24 | **Trailing blank line**: The file contains a double blank line after the closing brace (lines 24-25). While harmless, it is inconsistent with `ImpactReportSearchForm.java` (one blank line after closing brace) and `LoginActionForm.java` (no trailing blank line), suggesting no enforced end-of-file style rule.

A37-7 | LOW | IncidentReportSearchForm.java:11 | **`@EqualsAndHashCode(callSuper = false)` suppresses parent fields**: `IncidentReportSearchForm` uses `callSuper = false`, meaning `equals`/`hashCode` computed by Lombok will ignore all inherited fields from `ReportSearchForm` (`manu_id`, `type_id`, `start_date`, `end_date`, `timezone`, `manufacturers`, `unitTypes`). Since `IncidentReportSearchForm` declares no fields of its own, every instance will compare as equal to every other instance regardless of field values. This is almost certainly unintentional and could cause silent bugs if instances are stored in Sets or used as Map keys.

A37-8 | INFO | LoginActionForm.java:26-46 | **`getTimezone()` overrides Lombok-generated getter with timezone-abbreviation mapping**: This is architecturally notable — `@Data` generates a getter but this explicit method silently replaces it. The mapping translates daylight-saving abbreviations (e.g. `"EDT"` → `"EST5EDT"`) to POSIX-style tz strings. The mapping is incomplete: it handles only North American zones, and there is no handling of standard-time abbreviations (`EST`, `CST`, etc.). This is not a defect per se but deserves documentation; the absence of a comment explaining why this override exists makes the intent opaque.
# P4 Agent A38 — PreOpsReportSearchForm, RegisterActionForm, ReportSearchForm

## Reading Evidence

### PreOpsReportSearchForm.java
- **Class:** `PreOpsReportSearchForm`
- **Superclass:** `ActionForm` (org.apache.struts.action.ActionForm)
- **Annotations:** `@Data` (Lombok — generates getters, setters, equals, hashCode, toString)
- **serialVersionUID:** `5162539434628110613L` (line 14)
- **Fields:**
  - `private Long manu_id` (line 15)
  - `private Long type_id` (line 16)
  - `private String start_date` (line 17)
  - `private String end_date` (line 18)
  - `private String timezone` (line 19)
  - `private List<ManufactureBean> manufacturers` (line 21, initialised `new ArrayList<>()`)
  - `private List<UnitTypeBean> unitTypes` (line 22, initialised `new ArrayList<>()`)
- **Methods:**
  - `PreOpsReportSearchForm()` — constructor, line 24
  - `getPreOpsReportFilter(String dateFormat): PreOpsReportFilterBean` — line 27

---

### RegisterActionForm.java
- **Class:** `RegisterActionForm` (`final`)
- **Superclass:** `ActionForm` (org.apache.struts.action.ActionForm)
- **Annotations:** none
- **serialVersionUID:** none declared
- **Fields:**
  - `private String firstName` (line 12, default `null`)
  - `private String lastName` (line 13, default `null`)
  - `private String expirydt` (line 14, default `null`)
  - `private String licence_no` (line 15, default `null`)
  - `private String veh_id` (line 16, default `null`)
  - `private String dept` (line 17, default `null`)
  - `private String loc` (line 18, default `null`)
  - `private String attachment` (line 19, default `null`)
- **Methods:**
  - `getAttachment(): String` — line 22
  - `setAttachment(String attachment): void` — line 25
  - `getFirstName(): String` — line 28
  - `setFirstName(String firstName): void` — line 31
  - `getLastName(): String` — line 34
  - `setLastName(String lastName): void` — line 37
  - `getExpirydt(): String` — line 41
  - `setExpirydt(String expirydt): void` — line 44
  - `getLicence_no(): String` — line 47
  - `setLicence_no(String licence_no): void` — line 50
  - `getVeh_id(): String` — line 54
  - `setVeh_id(String veh_id): void` — line 57
  - `getDept(): String` — line 61
  - `setDept(String dept): void` — line 64
  - `getLoc(): String` — line 67
  - `setLoc(String loc): void` — line 70
  - `reset(ActionMapping mapping, HttpServletRequest request): void` — line 73
  - `validate(ActionMapping mapping, HttpServletRequest request): ActionErrors` — line 79

---

### ReportSearchForm.java
- **Class:** `ReportSearchForm`
- **Superclass:** `ActionForm` (org.apache.struts.action.ActionForm)
- **Annotations:** `@Data`, `@EqualsAndHashCode(callSuper = false)`, `@NoArgsConstructor`, `@AllArgsConstructor` (Lombok)
- **serialVersionUID:** none declared
- **Fields:**
  - `protected Long manu_id` (line 21)
  - `protected Long type_id` (line 22)
  - `protected String start_date` (line 23)
  - `protected String end_date` (line 24)
  - `protected String timezone` (line 25)
  - `protected List<ManufactureBean> manufacturers` (line 27, initialised `new ArrayList<ManufactureBean>()`)
  - `protected List<UnitTypeBean> unitTypes` (line 28, initialised `new ArrayList<UnitTypeBean>()`)
- **Methods:** none explicit (all generated by Lombok)

---

## Findings

A38-1 | HIGH | PreOpsReportSearchForm.java:1 | **Inheritance not used — fields duplicated from ReportSearchForm.** `PreOpsReportSearchForm` declares the exact same five data fields (`manu_id`, `type_id`, `start_date`, `end_date`, `timezone`) and the same two list fields (`manufacturers`, `unitTypes`) as `ReportSearchForm`. `ReportSearchForm` clearly exists as a base class (its fields are `protected` for this purpose) but `PreOpsReportSearchForm` extends `ActionForm` directly instead of extending `ReportSearchForm`, resulting in full field duplication and divergence risk.

A38-2 | MEDIUM | PreOpsReportSearchForm.java:33 | **Reference comparison used on String (`== ""`).** The expression `this.timezone == ""` compares a String reference to an empty-string literal rather than using `StringUtils.isBlank()` (which is already imported and used two lines above) or `.isEmpty()`. This will never be `true` unless the JVM interns the value, making the null-guard partially ineffective.

A38-3 | MEDIUM | RegisterActionForm.java:10 | **Missing `serialVersionUID`.** `RegisterActionForm` extends `ActionForm`, which implements `Serializable`. No `serialVersionUID` is declared, so the compiler will generate a warning and deserialization will break if the class is modified between serialization and deserialization cycles.

A38-4 | MEDIUM | ReportSearchForm.java:20 | **Missing `serialVersionUID`.** `ReportSearchForm` extends `ActionForm` (`Serializable`) with no `serialVersionUID` declared, producing a compiler warning and potential deserialization instability.

A38-5 | MEDIUM | RegisterActionForm.java:73 | **Incomplete `reset()` — fields not fully cleared.** The `reset()` method only resets `firstName`, `lastName`, and `expirydt`. The remaining fields (`licence_no`, `veh_id`, `dept`, `loc`, `attachment`) are left at their previous request's values. In Struts, `reset()` is called before each request to prevent stale data from carrying over, so these fields may silently retain prior values when not submitted by the form.

A38-6 | MEDIUM | RegisterActionForm.java:82 | **NullPointerException risk in `validate()`.** `firstName.equalsIgnoreCase("")` (line 82), `lastName.equalsIgnoreCase("")` (line 86), and `licence_no.equalsIgnoreCase("")` (line 90) are called directly on instance fields whose declared default is `null`. After a `reset()` call, `firstName` and `lastName` are set to `""` but `licence_no` remains `null`; if `validate()` is called in that state, line 90 will throw a NullPointerException. Using `StringUtils.isBlank()` or reversing the comparison (e.g., `"".equalsIgnoreCase(firstName)`) would be safe alternatives.

A38-7 | LOW | RegisterActionForm.java:92 | **Wrong error key used for `licence_no` validation.** When `licence_no` is empty the error is added under the key `"lastName"` (line 92) instead of a dedicated key such as `"licence_no"`. This means the licence error will be associated with the lastName field in the view, likely causing it to be displayed in the wrong location or suppressed if a lastName error is already present.

A38-8 | LOW | RegisterActionForm.java:12 | **Inconsistent naming conventions.** Fields `firstName` and `lastName` use camelCase while `licence_no`, `veh_id`, `expirydt`, `dept`, and `loc` use snake_case or abbreviations. Accessor method names follow the field style (e.g., `getLicence_no()`, `getVeh_id()`), which violates the JavaBeans convention and may cause issues with frameworks that rely on standard property name resolution.

A38-9 | LOW | ReportSearchForm.java:27 | **Raw diamond inference style inconsistency.** `new ArrayList<ManufactureBean>()` and `new ArrayList<UnitTypeBean>()` use explicit type arguments on the constructor, while `PreOpsReportSearchForm` uses the preferred diamond operator `new ArrayList<>()`. Both compile identically but the style should be consistent across related classes.

A38-10 | LOW | PreOpsReportSearchForm.java:30 | **Double-space in condition.** Line 30 contains `this.type_id ==  null` (two spaces between `==` and `null`), a minor style inconsistency inconsistent with the surrounding code.

A38-11 | INFO | RegisterActionForm.java:10 | **Class declared `final` without documented rationale.** `RegisterActionForm` is marked `final`, preventing subclassing. The other form classes in the package are not `final`. This is not necessarily wrong but is worth documenting if intentional, or removing if it was accidental.
# P4 Agent A39 — ResetPassActionForm, SearchActionForm, SessionReportSearchForm

## Reading Evidence

### ResetPassActionForm.java
- **Class:** `ResetPassActionForm`
- **Superclass:** `org.apache.struts.action.ActionForm`
- **Fields:**
  - `private String email` (line 13)
  - `private String question` (line 14)
  - `private String answer` (line 15)
  - `private String name` (line 16)
- **Methods:**
  - `getName()` — line 18
  - `setName(String name)` — line 21
  - `getQuestion()` — line 24
  - `setQuestion(String question)` — line 27
  - `getAnswer()` — line 30
  - `setAnswer(String answer)` — line 33
  - `getEmail()` — line 37
  - `setEmail(String email)` — line 40
  - `validate(ActionMapping, HttpServletRequest)` — line 45
- **No `serialVersionUID` declared.**
- **No constants defined.**

---

### SearchActionForm.java
- **Class:** `SearchActionForm`
- **Superclass:** `org.apache.struts.action.ActionForm`
- **Fields:**
  - `private String fname` (line 18)
  - `private String veh_id` (line 19)
  - `private String attachment` (line 20)
  - `private ArrayList arrAttachment` (line 21) — raw type
- **Methods:**
  - `SearchActionForm()` constructor — line 23
  - `getArrAttachment()` — line 29
  - `setArrAttachment()` — line 33
  - `getVeh_id()` — line 38
  - `setVeh_id(String veh_id)` — line 41
  - `getFname()` — line 45
  - `setFname(String fname)` — line 48
  - `reset(ActionMapping, HttpServletRequest)` — line 52
  - `getAttachment()` — line 56
  - `setAttachment(String attachment)` — line 59
  - `validate(ActionMapping, HttpServletRequest)` — line 63
- **Imports present but unused:** `HttpSession` (line 6), `AttachmentBean` (line 13), `SubscriptionBean` (line 14)
- **No `serialVersionUID` declared.**
- **No constants defined.**

---

### SessionReportSearchForm.java
- **Class:** `SessionReportSearchForm`
- **Superclass:** `org.apache.struts.action.ActionForm`
- **Annotations:** `@Data`, `@EqualsAndHashCode(callSuper = false)`
- **Fields:**
  - `private static final long serialVersionUID = -8378135874225584484L` (line 15)
  - `private Long vehicle_id` (line 17)
  - `private Long driver_id` (line 18)
  - `private String start_date` (line 19)
  - `private String end_date` (line 20)
  - `private String timezone` (line 21)
- **Methods (explicit; Lombok generates getters/setters/equals/hashCode/toString):**
  - `getSessionReportFilter(String dateFormat)` — line 23
- **Constants:** `serialVersionUID` (line 15)

---

## Findings

A39-1 | HIGH | ResetPassActionForm.java:49 | `name.equalsIgnoreCase("")` is called without a null check. The field `name` is initialised to `null` (line 16) and there is no guarantee the setter has been called before `validate()` runs, so this will throw a `NullPointerException` at runtime. The same pattern is repeated on `email` at line 54.

A39-2 | HIGH | ResetPassActionForm.java:54 | `email.equalsIgnoreCase("")` is called without a null check — same root cause as A39-1.

A39-3 | HIGH | SearchActionForm.java:66 | `fname.equalsIgnoreCase("")` is called without a null check. The field `fname` is `null`-initialised (line 18) and `reset()` only sets it to `""` for the fname field; `veh_id` is never reset. A request that skips `reset()` will cause a `NullPointerException`.

A39-4 | HIGH | SearchActionForm.java:70 | `veh_id.equalsIgnoreCase("")` is called without a null check. `veh_id` is never assigned in `reset()` and remains `null` until the setter is called, producing a `NullPointerException` in `validate()`.

A39-5 | MEDIUM | ResetPassActionForm.java:47 | `// TODO Auto-generated method stub` comment left inside the `validate()` override. This is auto-generated boilerplate that was never cleaned up and should be removed.

A39-6 | MEDIUM | SearchActionForm.java:6 | Unused import `javax.servlet.http.HttpSession`. The symbol is never referenced in the file; this will produce a compiler warning and indicates dead import.

A39-7 | MEDIUM | SearchActionForm.java:13 | Unused import `com.bean.AttachmentBean`. The type is never referenced in this file.

A39-8 | MEDIUM | SearchActionForm.java:14 | Unused import `com.bean.SubscriptionBean`. The type is never referenced in this file.

A39-9 | MEDIUM | SearchActionForm.java:21 | `ArrayList arrAttachment` is declared as a raw type. This suppresses generic type safety and will generate an "unchecked" compiler warning. It should be parameterised (e.g., `ArrayList<AttachmentBean>` or `ArrayList<Object>`).

A39-10 | MEDIUM | SearchActionForm.java:29 | `getArrAttachment()` return type is the raw `ArrayList`, propagating the raw-type warning to all callers.

A39-11 | LOW | ResetPassActionForm.java:11 | Class `ResetPassActionForm` extends `ActionForm` (which implements `Serializable`) but declares no `serialVersionUID`. This will produce a compiler/IDE warning and may cause unexpected `InvalidClassException` during session serialisation.

A39-12 | LOW | SearchActionForm.java:17 | Class `SearchActionForm` extends `ActionForm` but declares no `serialVersionUID`, same issue as A39-11.

A39-13 | LOW | ResetPassActionForm.java:11 | Class name is missing a space before `{` — `ActionForm{` should be `ActionForm {`. Minor brace-spacing style inconsistency.

A39-14 | LOW | SearchActionForm.java:17 | Same brace-spacing inconsistency as A39-13: `ActionForm{` should be `ActionForm {`.

A39-15 | LOW | ResetPassActionForm.java:49-57 | Validate method uses `equalsIgnoreCase("")` to test for blank strings rather than `StringUtils.isBlank()` or `String.isEmpty()`, which also handles null and whitespace-only input. This is an inconsistent style when compared to `SessionReportSearchForm` (line 29) which already uses `StringUtils.isBlank()`.

A39-16 | LOW | SearchActionForm.java:19,41 | Field name `veh_id` and its getter/setter (`getVeh_id` / `setVeh_id`) use an underscore, which violates Java naming conventions for instance fields and methods (camelCase is the standard). `SessionReportSearchForm` similarly uses underscored field names (`vehicle_id`, `driver_id`, `start_date`, `end_date`) but these are partially mitigated there by Lombok. In `SearchActionForm` the underscore style is applied manually and inconsistently with `fname`.

A39-17 | INFO | SearchActionForm.java:23 | The constructor `SearchActionForm()` is declared `throws Exception`. This is an overly broad exception declaration; it prevents the Struts framework from instantiating the form bean without special handling and should be narrowed to the specific checked exception type(s) thrown by `UnitDAO`.

A39-18 | INFO | SearchActionForm.java:33 | `setArrAttachment()` is declared `throws Exception` for the same reason as A39-17. Additionally, this setter performs a DAO database call (`UnitDAO.getInstance().getAllUnitAttachment()`) on every form construction, coupling the ActionForm directly to the data layer — a design concern.

A39-19 | INFO | ResetPassActionForm.java:62-65 | Multiple trailing blank lines at the end of the class body (lines 62–65) before the closing brace. Minor whitespace hygiene issue.
# P4 Agent A40 — SubscriptionActionForm, SwitchCompanyActionForm, ValidateIdExistsAbstractActionForm

## Reading Evidence

### SubscriptionActionForm.java
- **File:** `src/main/java/com/actionform/SubscriptionActionForm.java`
- **Class:** `SubscriptionActionForm`
- **Superclass:** `org.apache.struts.action.ActionForm`
- **Annotations:** none
- **Fields:**
  - `private String[] comp_sub_id = {}` (line 13)
- **Methods:**
  - `getComp_sub_id()` → `String[]` (line 16)
  - `setComp_sub_id(String[])` → `void` (line 20)
- **Implements:** none
- **`serialVersionUID`:** absent
- **Lombok:** not used
- **Imports used:** `javax.servlet.http.HttpServletRequest`, `org.apache.struts.action.ActionMessage`, `org.apache.struts.action.ActionErrors`, `org.apache.struts.action.ActionMapping` (lines 4–9)

---

### SwitchCompanyActionForm.java
- **File:** `src/main/java/com/actionform/SwitchCompanyActionForm.java`
- **Class:** `SwitchCompanyActionForm`
- **Superclass:** `org.apache.struts.validator.ValidatorForm`
- **Annotations:** `@Data` (Lombok, line 6)
- **Modifiers:** `public final`
- **Fields:**
  - `private String currentCompany = null` (line 8)
- **Methods:** none declared (getter/setter/equals/hashCode/toString generated by `@Data`)
- **`serialVersionUID`:** absent

---

### ValidateIdExistsAbstractActionForm.java
- **File:** `src/main/java/com/actionform/ValidateIdExistsAbstractActionForm.java`
- **Class:** `ValidateIdExistsAbstractActionForm` (abstract)
- **Superclass:** `org.apache.struts.action.ActionForm`
- **Annotations:** `@Getter`, `@Setter` (Lombok, lines 13–14)
- **Fields:**
  - `protected String id = null` (line 16)
- **Methods:**
  - `validate(ActionMapping, HttpServletRequest)` → `ActionErrors` (line 19, `@Override`)
- **`serialVersionUID`:** absent
- **Known subclasses (in package):**
  - `AdminFleetcheckShowActionForm` — empty body, no extra fields
  - `AdminFleetcheckDeleteActionForm` — empty body, no extra fields
  - `AdminFleetcheckHideActionForm` — adds four fields, overrides `validate()` calling `super`

---

## Findings

A40-1 | MEDIUM | SubscriptionActionForm.java:13 | Field name `comp_sub_id` uses snake_case. Java field naming convention is lowerCamelCase (e.g., `compSubId`). The derived accessor names `getComp_sub_id()` / `setComp_sub_id()` are non-standard and differ from the camelCase accessor style used in every other action form in this package (e.g., `currentCompany`, `type_id` in the hide form). This inconsistency also means the Struts form-bean binding key `comp_sub_id` is exposed in HTTP parameters as an underscored name, coupling the wire format to the internal naming choice.

A40-2 | LOW | SubscriptionActionForm.java:4-9 | Four imports are declared (`HttpServletRequest`, `ActionMessage`, `ActionErrors`, `ActionMapping`) but none of them are used anywhere in the class body. There is no `validate()` override, no `reset()` override, and no method that references these types. These are unused imports that will produce IDE/compiler warnings.

A40-3 | LOW | SubscriptionActionForm.java:11 | `SubscriptionActionForm` extends `ActionForm` directly and uses hand-written getters/setters, while the adjacent `SwitchCompanyActionForm` extends `ValidatorForm` and uses Lombok `@Data`. No consistent base-class or accessor-generation strategy is applied across the package. The inconsistency is a style/maintenance issue.

A40-4 | LOW | SwitchCompanyActionForm.java:7 | `SwitchCompanyActionForm` is declared `final`. Struts form beans are instantiated and pooled by the framework; marking the class `final` has no practical benefit here and prevents any future subclassing without explanation or comment. This is an unusual pattern not followed by any other form in the package.

A40-5 | LOW | SwitchCompanyActionForm.java:7 | `SwitchCompanyActionForm` extends `ValidatorForm` (Struts validator integration) while all other forms in the package extend `ActionForm` or `ValidateIdExistsAbstractActionForm`. No validator XML rules appear to be defined for this form. Extending `ValidatorForm` without a corresponding validation rule set silently bypasses validation and misleads maintainers about the validation strategy in use.

A40-6 | MEDIUM | ValidateIdExistsAbstractActionForm.java:15 | The `validate()` implementation uses the hard-coded message key `"error.id"` (line 23) and hard-coded field key `"id"` (line 24). Subclasses that represent domain objects with different id semantics (e.g., a fleetcheck hide form that validates `manu_id`, `type_id`, etc.) cannot change the message key or field label without overriding the entire method. This is a leaky abstraction: the abstract class enforces a concrete UI message key that bleeds into subclass validation UX.

A40-7 | LOW | ValidateIdExistsAbstractActionForm.java:16 | The field `id` is declared `protected` rather than `private`. Because `@Getter` / `@Setter` are applied at the class level the field is already fully accessible via generated accessors. Using `protected` visibility directly exposes the field to subclasses without encapsulation, which is unnecessary given the Lombok accessor approach and inconsistent with the principle of keeping fields private.

A40-8 | LOW | SubscriptionActionForm.java, SwitchCompanyActionForm.java, ValidateIdExistsAbstractActionForm.java | All three classes extend `ActionForm` or `ValidatorForm`, both of which implement `java.io.Serializable`. None of the three classes declare a `serialVersionUID`. The Java compiler will emit an "unchecked serialization" warning for each. Twenty-seven of the thirty-six action forms in this package also lack `serialVersionUID`; the problem is systemic but each class in scope is individually flagged here.
# P4 Agent A41 — PreFlightActionServlet

## Reading Evidence

### PreFlightActionServlet

- **Class:** `PreFlightActionServlet` (line 22) — extends `ActionServlet`
- **Methods:**
  - `doGet` (line 36)
  - `doPost` (line 94)
  - `excludeFromFilter` (line 98)
- **Fields/Constants:**
  - `serialVersionUID` — `private static final long`, value `-3552000667154242244L` (line 27)
  - `log` — `private static Logger` (line 29)

---

## Findings

A41-1 | MEDIUM | PreFlightActionServlet.java:68-70 | **Commented-out code left in production.** Three lines of locale-manipulation code are commented out (`System.out.print`, `req.getSession(false).setAttribute(...)`, `req.getSession().setAttribute(...)`) including a `System.out.print` debug call. These are dead code that should be removed.

A41-2 | LOW | PreFlightActionServlet.java:43 | **Debug/noise log statement left in production.** `log.info("*****LOGGER WORKING from PreFlightActionServlet******")` is fired on every single GET request. This is a development-era "is logging alive?" probe that has no operational value and pollutes logs at runtime.

A41-3 | LOW | PreFlightActionServlet.java:79 | **Debug-style log message with no meaningful content.** `log.info("----------------- " + stPath)` uses a visual separator of dashes as the message body. The log entry is ambiguous — it is unclear whether the servlet is forwarding due to session expiry or an error. The message should state the reason for the forward (e.g., `"Forwarding to: " + stPath + " (session expired or error)"`).

A41-4 | MEDIUM | PreFlightActionServlet.java:64 / 84 | **MDC entries are never cleared (MDC leak).** `MDC.put("sessCompId", ...)` (line 64) and `MDC.put("remoteAddr", ...)` (line 84) are written but `MDC.remove()` or `MDC.clear()` is never called. In a servlet container that uses thread pools, MDC values from one request will bleed into subsequent requests that reuse the same thread.

A41-5 | LOW | PreFlightActionServlet.java:84 | **MDC populated after request processing has already begun.** `MDC.put("remoteAddr", req.getRemoteAddr())` is called after `super.doGet(req, res)` has returned (line 83-84). Any log statements emitted during `super.doGet()` will therefore lack the `remoteAddr` MDC value. The put should occur before delegating to the superclass.

A41-6 | MEDIUM | PreFlightActionServlet.java:98 | **Misleading method name — inverted semantics.** `excludeFromFilter(String path)` returns `true` when the path IS subject to the session filter (i.e., should NOT be excluded) and `false` when it should be excluded. The boolean sense is the opposite of what the name implies. This is a leaky abstraction / naming defect that makes the call-site condition `if(excludeFromFilter(path))` read as "if this path is excluded from the filter, then check for session expiry", which is logically backwards. A clearer name would be `requiresSessionCheck(path)` or `isProtectedPath(path)`.

A41-7 | LOW | PreFlightActionServlet.java:109 | **Typo in excluded path string.** `path.endsWith("swithLanguage.do")` is missing the letter 'c' — should be `switchLanguage.do`. As written, requests to `switchLanguage.do` are not in the exclusion list and will be subjected to session checks, while `swithLanguage.do` (a path that likely does not exist) is excluded instead.

A41-8 | LOW | PreFlightActionServlet.java:98-115 | **Inconsistent indentation in `excludeFromFilter`.** The method body uses a mix of four-space and irregular indentation that differs from the tab-based style used in the rest of the file. The `if`/`else if` chains are indented with six spaces inside a block that is already indented inconsistently relative to the surrounding class.

A41-9 | LOW | PreFlightActionServlet.java:3-17 | **Unused imports.** The following imports are declared but never used in the class body:
  - `java.util.Locale` (line 4)
  - `org.apache.struts.action.ActionErrors` (line 14)
  - `org.apache.struts.action.ActionMessage` (line 15)
  - `org.apache.struts.action.ActionMessages` (line 16)
  - `org.apache.struts.Globals` (line 13)
These will generate compiler warnings and indicate dead or abandoned code paths.

A41-10 | LOW | PreFlightActionServlet.java:29 | **Logger field is not `final`.** `private static Logger log` should be `private static final Logger log`. The absence of `final` means the field could theoretically be reassigned, which is unintentional and a common static-analysis warning.

A41-11 | LOW | PreFlightActionServlet.java:36 / 94 | **Missing `@Override` annotations on `doGet` and `doPost`.** Both methods override `HttpServlet` methods but carry no `@Override` annotation. Without `@Override`, a signature mismatch (e.g., from a future API change) would silently introduce a new method rather than failing at compile time.

A41-12 | INFO | PreFlightActionServlet.java:11-12 | **Dependency on Log4j 1.x API.** `org.apache.log4j.Logger` and `org.apache.log4j.MDC` are Log4j 1.x classes. Log4j 1.x reached end-of-life in 2015. Migration to SLF4J with a modern backend (e.g., Logback or Log4j 2) is recommended.
# P4 Agent A42 — AdvertisementBean, AlertBean, AnswerBean

## Reading Evidence

### AdvertisementBean.java

- **Class:** `AdvertisementBean` (implements `Serializable`)
- **Fields:**
  - `serialVersionUID` (static final long) — line 10
  - `id` (String) — line 12
  - `pic` (String) — line 13
  - `text` (String) — line 14
  - `order_no` (String) — line 15
- **Methods:**
  - `getId()` — line 17
  - `setId(String id)` — line 20
  - `getPic()` — line 23
  - `setPic(String pic)` — line 26
  - `getText()` — line 29
  - `setText(String text)` — line 32
  - `getOrder_no()` — line 35
  - `setOrder_no(String order_no)` — line 38

---

### AlertBean.java

- **Class:** `AlertBean` (annotated `@Data`, `@NoArgsConstructor`; does NOT implement `Serializable`)
- **Fields:**
  - `alert_id` (String) — line 11
  - `alert_name` (String) — line 12
  - `alert_type` (String) — line 13
  - `file_name` (String) — line 14
  - `frequency` (String) — line 15
- **Methods (explicit):**
  - `AlertBean(String alert_id, String alert_name, String alert_type, String file_name, String frequency)` — private `@Builder` constructor, line 18–24
- **Methods (Lombok-generated via `@Data`):**
  - `getAlert_id()`, `setAlert_id()`, `getAlert_name()`, `setAlert_name()`, `getAlert_type()`, `setAlert_type()`, `getFile_name()`, `setFile_name()`, `getFrequency()`, `setFrequency()`, `equals()`, `hashCode()`, `toString()`
- **Methods (Lombok-generated via `@NoArgsConstructor`):**
  - `AlertBean()` (no-arg constructor)

---

### AnswerBean.java

- **Class:** `AnswerBean` (annotated `@Data`, `@NoArgsConstructor`; implements `Serializable`)
- **Fields:**
  - `serialVersionUID` (static final long) — line 14
  - `id` (String) — line 17
  - `answer` (String) — line 18
  - `faulty` (String) — line 19
  - `quesion_id` (String) — line 20
  - `result_id` (String) — line 21
- **Methods (Lombok-generated via `@Data`):**
  - `getId()`, `setId()`, `getAnswer()`, `setAnswer()`, `getFaulty()`, `setFaulty()`, `getQuesion_id()`, `setQuesion_id()`, `getResult_id()`, `setResult_id()`, `equals()`, `hashCode()`, `toString()`
- **Methods (Lombok-generated via `@NoArgsConstructor`):**
  - `AnswerBean()` (no-arg constructor)

---

## Findings

A42-1 | MEDIUM | AdvertisementBean.java:15 | Field `order_no` uses snake_case. All other fields in this class (`id`, `pic`, `text`) use camelCase. The generated accessor names `getOrder_no()` / `setOrder_no()` (lines 35, 38) also violate standard Java Bean naming convention (should be `getOrderNo()` / `setOrderNo()`).

A42-2 | MEDIUM | AlertBean.java:11-15 | All five fields (`alert_id`, `alert_name`, `alert_type`, `file_name`, `frequency`) use snake_case, inconsistent with Java naming conventions (should be `alertId`, `alertName`, `alertType`, `fileName`, `frequency`). Lombok's `@Data` will generate non-standard accessor names (e.g., `getAlert_id()`) that violate the JavaBeans specification.

A42-3 | MEDIUM | AlertBean.java:18 | The `@Builder` annotation is placed on a private all-args constructor rather than on the class. While this is a valid Lombok pattern to combine with `@NoArgsConstructor`, it is non-idiomatic and obscures intent; the private visibility means the builder is the only way to construct a fully-populated instance without calling setters, which may surprise maintainers.

A42-4 | LOW | AlertBean.java:9 | `AlertBean` does not implement `Serializable`. The other two beans in the same package (`AdvertisementBean`, `AnswerBean`) both implement `Serializable`. If `AlertBean` instances are stored in an HTTP session, cached, or otherwise serialized, this omission will cause a runtime `NotSerializableException`.

A42-5 | LOW | AnswerBean.java:20 | Field name `quesion_id` is a misspelling of `question_id`. Beyond the typo, the field also uses snake_case rather than camelCase (should be `questionId`). The misspelling will propagate into all Lombok-generated accessors (`getQuesion_id()`, `setQuesion_id()`), making the API misleading and harder to discover.

A42-6 | LOW | AnswerBean.java:20 | Field `quesion_id` uses snake_case, inconsistent with fields `id`, `answer`, `faulty`, and `result_id` (note `result_id` also uses snake_case — see A42-7).

A42-7 | LOW | AnswerBean.java:21 | Field `result_id` uses snake_case. Together with `quesion_id` (line 20), two of the five instance fields use snake_case while `id`, `answer`, and `faulty` use camelCase (or single-word), creating an inconsistent naming style within the same class. Lombok-generated accessor `getResult_id()` / `setResult_id()` violates the JavaBeans naming specification.

A42-8 | INFO | AdvertisementBean.java:7-9 | The `serialVersionUID` Javadoc block is an empty stub (contains only whitespace between `/**` and `*/`). This is a minor quality issue but not a defect.
# P4 Agent A43 — AnswerTypeBean, AttachmentBean, ChecklistBean

## Reading Evidence

### AnswerTypeBean.java
- **Class:** `AnswerTypeBean` (line 5) — implements `Serializable`
- **Fields:**
  - `private static final long serialVersionUID = 1721165036019491023L;` (line 10)
  - `private String id = null;` (line 12)
  - `private String name = null;` (line 13)
- **Methods:**
  - `getId()` — line 15
  - `setId(String id)` — line 18
  - `getName()` — line 21
  - `setName(String name)` — line 24

---

### AttachmentBean.java
- **Class:** `AttachmentBean` (line 5) — implements `Serializable`
- **Fields:**
  - `private static final long serialVersionUID = -2969164023760074040L;` (line 10)
  - `private String id = null;` (line 12)
  - `private String name = null;` (line 13)
- **Methods:**
  - `getId()` — line 14
  - `setId(String id)` — line 17
  - `getName()` — line 20
  - `setName(String name)` — line 23

---

### ChecklistBean.java
- **Class:** `ChecklistBean` (line 3) — does NOT implement `Serializable`
- **Fields:**
  - `private int equipId;` (line 5)
  - `private boolean driverBased;` (line 6)
- **Methods:**
  - `getEquipId()` — line 8
  - `setEquipId(int equipId)` — line 11
  - `isDriverBased()` — line 14
  - `setDriverBased(boolean driverBased)` — line 17

---

## Findings

A43-1 | LOW | AnswerTypeBean.java:7-9 | Empty Javadoc block (`/** * */`) generated by IDE auto-stub. The serialVersionUID comment contains no meaningful content. Same pattern present in AttachmentBean.java:7-9. Adds noise without documentation value.

A43-2 | MEDIUM | ChecklistBean.java:3 | `ChecklistBean` is a bean class in the `com.bean` package but does not implement `java.io.Serializable`, unlike every other bean in the same package (`AnswerTypeBean`, `AttachmentBean`). If instances are ever stored in a session, passed over a network, or persisted, this will cause a runtime `NotSerializableException`. A `serialVersionUID` is also absent.

A43-3 | LOW | AnswerTypeBean.java:28-30 | Trailing blank lines (3 blank lines before closing brace). Minor style inconsistency. Same issue in `AttachmentBean.java:27-30` (4 blank lines) and `ChecklistBean.java:20-21` (2 blank lines). Inconsistent across the three files.

A43-4 | INFO | AttachmentBean.java:13-14 | Missing blank line between last field declaration (`private String name = null;`) and first method (`getId()`). `AnswerTypeBean.java` has a blank line in the same position (line 14). Minor formatting inconsistency between two otherwise identical classes.

A43-5 | INFO | ChecklistBean.java:3-4 | Opening brace for the class declaration is on a separate line (`{` on line 4), while `AnswerTypeBean` and `AttachmentBean` both use same-line braces (`public class Foo implements Serializable{`). Inconsistent brace style across the bean package.
# P4 Agent A44 — CompEntityRelBean, CompanyBean, DateFormatBean

## Reading Evidence

### CompEntityRelBean.java
- **Class:** `CompEntityRelBean` (line 3)
- **Fields:**
  - `id` : String (line 4)
  - `comp_id` : String (line 5)
  - `entity_id` : String (line 6)
  - `entityname` : String (line 7)
  - `compname` : String (line 8)
- **Methods:**
  - `getId()` — line 10
  - `setId(String id)` — line 13
  - `getComp_id()` — line 16
  - `setComp_id(String comp_id)` — line 19
  - `getEntity_id()` — line 22
  - `setEntity_id(String entity_id)` — line 25
  - `getEntityname()` — line 28
  - `setEntityname(String entityname)` — line 31
  - `getCompname()` — line 34
  - `setCompname(String compname)` — line 37
- **Notes:** No Lombok annotations; no `implements Serializable`; no `serialVersionUID`.

---

### CompanyBean.java
- **Class:** `CompanyBean implements Serializable` (line 13)
- **Annotations:** `@Data`, `@NoArgsConstructor` (lines 11–12)
- **Fields:**
  - `serialVersionUID` : long static final (line 15)
  - `id` : String (line 17)
  - `name` : String (line 18)
  - `address` : String (line 19)
  - `suburb` : String (line 20)
  - `postcode` : String (line 21)
  - `email` : String (line 22)
  - `contact_no` : String (line 23)
  - `password` : String (line 24)
  - `pin` : String (line 25)
  - `refnm` : String (line 26)
  - `refno` : String (line 27)
  - `contact_fname` : String (line 28)
  - `contact_lname` : String (line 29)
  - `question` : String (line 30)
  - `answer` : String (line 31)
  - `unit` : String (line 32)
  - `subemail` : String (line 33)
  - `timezone` : String (line 34)
  - `timezoneName` : String (line 35)
  - `dateFormat` : String (line 36)
  - `maxSessionLength` : Integer (line 37)
  - `lan_id` : String (line 38)
  - `privacy` : boolean (line 39)
  - `template` : String (line 40)
  - `authority` : String (line 41)
  - `mobile` : String (line 42)
  - `cognito_username` : String (line 43)
  - `roleIds` : String[] `@Deprecated` (line 46)
  - `roles` : List\<RoleBean\> (line 48)
- **Methods:**
  - `CompanyBean(...)` — `@Builder` private constructor, line 51–79
  - All getters/setters generated by Lombok `@Data`

---

### DateFormatBean.java
- **Class:** `DateFormatBean implements Serializable` (line 13)
- **Annotations:** `@Data`, `@NoArgsConstructor` (lines 11–12)
- **Fields:**
  - `serialVersionUID` : long static final (line 14)
  - `format` : String (line 16)
- **Methods:**
  - `DateFormatBean(String format)` — `@Builder` private constructor, line 19–21
  - `getExample()` — line 23–31
  - Getter/setter for `format` generated by Lombok `@Data`

---

## Findings

A44-1 | MEDIUM | CompEntityRelBean.java:1 | Missing `serialVersionUID`: `CompEntityRelBean` does not implement `Serializable` and declares no `serialVersionUID`. While the class itself is not marked `Serializable`, it is used as a data-transfer bean alongside other beans in the same package that do implement `Serializable`. This omission will produce a compiler/IDE warning if the class is ever serialized indirectly, and is inconsistent with the pattern in `CompanyBean` and `DateFormatBean`.

A44-2 | MEDIUM | CompEntityRelBean.java:5,6 | Snake_case field names: `comp_id` and `entity_id` use snake_case rather than camelCase (`compId`, `entityId`). The same class also has camelCase fields (`entityname`, `compname`), creating mixed naming within a single class. The sibling bean `CompanyBean` also contains snake_case fields (`contact_no`, `contact_fname`, `contact_lname`, `lan_id`, `cognito_username`), making this a cross-bean style inconsistency. Java naming conventions and the project's own partial use of camelCase (`timezoneName`, `dateFormat`, `maxSessionLength`) require camelCase for field names.

A44-3 | MEDIUM | CompanyBean.java:23,28,29,38,43 | Snake_case field names in CompanyBean: `contact_no` (line 23), `contact_fname` (line 28), `contact_lname` (line 29), `lan_id` (line 38), and `cognito_username` (line 43) use snake_case. This is inconsistent with the camelCase fields in the same class (`timezoneName`, `dateFormat`, `maxSessionLength`) and violates Java naming conventions. Because Lombok `@Data` generates getter/setter names directly from field names (e.g., `getContact_no()`), the generated API surface is also non-standard and will not be recognized by standard JavaBean introspection.

A44-4 | LOW | CompanyBean.java:51 | Builder constructor parameter names differ from field names: the `@Builder` constructor uses parameter names `date_format` (mapped to field `dateFormat`, line 74) and `max_session_length` (mapped to field `maxSessionLength`, line 75) while all other parameters shadow the field names directly. This means the Lombok-generated builder (if it were used) would expose inconsistent setter names on the builder object, and any caller using the builder API gets `date_format` and `max_session_length` instead of `dateFormat` and `maxSessionLength`.

A44-5 | LOW | CompEntityRelBean.java:1 | No Lombok annotations: `CompEntityRelBean` hand-writes ten getter/setter methods for five fields. Every other bean in the same package (`CompanyBean`, `DateFormatBean`) uses `@Data` + `@NoArgsConstructor` to generate this boilerplate. The hand-written accessors are not wrong, but they are inconsistent with the project pattern and create unnecessary maintenance surface.

A44-6 | LOW | DateFormatBean.java:27 | `Calendar.HOUR` used instead of `Calendar.HOUR_OF_DAY`: `getExample()` sets the hour using `Calendar.HOUR` (12-hour clock field). For a time of "23:59:59" the intent is clearly 24-hour time, but `Calendar.HOUR` with value 23 will silently overflow into the next 12-hour cycle. `Calendar.HOUR_OF_DAY` should be used to set hour 23 unambiguously.

A44-7 | INFO | CompanyBean.java:45-46 | `@Deprecated` field `roleIds` retained in production class: the `String[] roleIds` field is annotated `@Deprecated` but remains in the class. Its replacement (`List<RoleBean> roles`, line 48) is present. The deprecated field is never assigned in the `@Builder` constructor (line 51–79), confirming it is dead. Retaining it indefinitely adds confusion and a risk that legacy code paths silently read a null array.
# P4 Agent A45 — DriverBean, DriverJobDetailsBean, DriverTrainingBean

## Reading Evidence

### DriverBean.java

**Class:** `com.bean.DriverBean` implements `Serializable`
**Annotations:** `@Data`, `@NoArgsConstructor`

**Fields (all instance, all private):**
| Line | Field | Type |
|------|-------|------|
| 12 | `serialVersionUID` | `static final long` |
| 14 | `id` | `Long` |
| 15 | `comp_id` | `String` |
| 17 | `first_last` | `String` |
| 18 | `first_name` | `String` |
| 19 | `last_name` | `String` |
| 20 | `licno` | `String` |
| 21 | `expirydt` | `String` |
| 22 | `joindt` | `String` |
| 23 | `phone` | `String` |
| 24 | `active` | `boolean` |
| 25 | `location` | `String` |
| 26 | `department` | `String` |
| 27 | `card_no` | `String` |
| 28 | `facility_code` | `String` |
| 30 | `licence_number` | `String` |
| 31 | `expiry_date` | `String` |
| 32 | `security_number` | `String` |
| 33 | `address` | `String` |
| 34 | `app_access` | `String` |
| 35 | `mobile` | `String` |
| 36 | `email_addr` | `String` |
| 37 | `pass` | `String` |
| 38 | `cpass` | `String` |
| 39 | `pass_hash` | `String` |
| 40 | `op_code` | `String` |
| 41 | `cognito_username` | `String` |
| 42 | `accessToken` | `String` |

**Methods:**
| Line | Method |
|------|--------|
| 44–77 | `@Builder private DriverBean(Long id, String comp_id, ...)` — all-args builder constructor |
| 79–81 | `public String getName()` |

---

### DriverJobDetailsBean.java

**Class:** `com.bean.DriverJobDetailsBean`
**Annotations:** none
**Implements:** nothing (no `Serializable`)

**Fields (all instance, all private):**
| Line | Field | Type |
|------|-------|------|
| 7 | `id` | `int` |
| 8 | `action` | `String` |
| 9 | `equipId` | `String` |
| 10 | `jobId` | `String` |
| 11 | `driverList` | `ArrayList` (raw) |
| 12 | `name` | `String` |
| 13 | `startTime` | `String` |
| 14 | `endTime` | `String` |
| 15 | `fromTime` | `String` |
| 16 | `toTime` | `String` |
| 17 | `instruct` | `String` |
| 18 | `jobTitle` | `String` |
| 19 | `description` | `String` |
| 20 | `driverId` | `String` |

**Methods:**
| Line | Method |
|------|--------|
| 21–23 | `public int getId()` |
| 24–26 | `public String getAction()` |
| 27–29 | `public String getEquipId()` |
| 30–32 | `public String getJobId()` |
| 33–35 | `public ArrayList getDriverList()` (raw return type) |
| 36–38 | `public String getName()` |
| 39–41 | `public String getStartTime()` |
| 42–44 | `public String getEndTime()` |
| 45–47 | `public String getFromTime()` |
| 48–50 | `public String getToTime()` |
| 51–53 | `public String getInstruct()` |
| 54–56 | `public String getJobTitle()` |
| 57–59 | `public String getDescription()` |
| 60–62 | `public String getDriverId()` |
| 63–65 | `public void setId(int id)` |
| 66–68 | `public void setAction(String action)` |
| 69–71 | `public void setEquipId(String equipId)` |
| 72–74 | `public void setJobId(String jobId)` |
| 75–77 | `public void setDriverList(ArrayList driverList)` (raw parameter type) |
| 78–80 | `public void setName(String name)` |
| 81–83 | `public void setStartTime(String startTime)` |
| 84–86 | `public void setEndTime(String endTime)` |
| 87–89 | `public void setFromTime(String fromTime)` |
| 90–92 | `public void setToTime(String toTime)` |
| 93–95 | `public void setInstruct(String instruct)` |
| 96–98 | `public void setJobTitle(String jobTitle)` |
| 99–101 | `public void setDescription(String description)` |
| 102–104 | `public void setDriverId(String driverId)` |

---

### DriverTrainingBean.java

**Class:** `com.bean.DriverTrainingBean` implements `Serializable`
**Annotations:** `@Data`, `@NoArgsConstructor`

**Fields (all instance, all private):**
| Line | Field | Type |
|------|-------|------|
| 12 | `serialVersionUID` | `static final long` |
| 14 | `id` | `Long` |
| 15 | `driver_id` | `Long` |
| 16 | `first_name` | `String` |
| 17 | `last_name` | `String` |
| 18 | `email` | `String` |
| 19 | `unit_name` | `String` |
| 20 | `unit_id` | `Long` |
| 21 | `manufacture_id` | `Long` |
| 22 | `manufacture_name` | `String` |
| 23 | `type_id` | `Long` |
| 24 | `type_name` | `String` |
| 25 | `fuel_type_id` | `Long` |
| 26 | `fuel_type_name` | `String` |
| 27 | `training_date` | `String` |
| 28 | `expiration_date` | `String` |
| 29 | `comp_id` | `Long` |
| 30 | `comp_email` | `String` |

**Methods:**
| Line | Method |
|------|--------|
| 32–67 | `@Builder private DriverTrainingBean(Long id, Long driver_id, ...)` — all-args builder constructor |

---

## Findings

A45-1 | HIGH | DriverJobDetailsBean.java:11 | Raw type `ArrayList` used for field `driverList` with no type parameter. This suppresses compile-time type safety and produces an unchecked warning. The field, its getter (line 33), and its setter (line 75) all use the raw `ArrayList` type.

A45-2 | HIGH | DriverJobDetailsBean.java:5 | Class does not implement `Serializable` and has no `serialVersionUID`. The two sibling beans in the same package (`DriverBean`, `DriverTrainingBean`) both implement `Serializable`. If instances are ever passed through a serialization boundary (session, cache, JMS) this will fail at runtime.

A45-3 | MEDIUM | DriverBean.java:15–42 | Pervasive snake_case field names (`comp_id`, `first_last`, `first_name`, `last_name`, `card_no`, `facility_code`, `licence_number`, `expiry_date`, `security_number`, `app_access`, `email_addr`, `pass_hash`, `op_code`, `cognito_username`) mixed with one camelCase field (`accessToken` at line 42). The project appears to use snake_case as the dominant convention inside `DriverBean`, but `accessToken` breaks that pattern. Lombok's `@Data` will generate `getAccessToken()` while generating `getComp_id()`, `getFirst_name()`, etc., causing an inconsistent public API.

A45-4 | MEDIUM | DriverTrainingBean.java:33–49 | The `@Builder` constructor parameter list (`Long id, Long driver_id, ..., Long unit_id`) places `unit_id` last (line 49), whereas the corresponding field declaration appears at line 20 (before `manufacture_id`). This mismatch between declaration order and constructor parameter order is a maintenance hazard: a developer adding or removing fields may introduce a subtle off-by-one assignment error.

A45-5 | MEDIUM | DriverBean.java:20–21,30–31 | Apparent duplicate data for the same concept: `licno` (line 20) and `licence_number` (line 30) appear to represent the same entity (the driver's licence number). Similarly `expirydt` (line 21) and `expiry_date` (line 31) appear to represent the same date. A FIXME comment at line 29 explicitly acknowledges the `licno`/`licence_number` ambiguity. Having two fields for the same datum risks divergence and is a data-integrity concern.

A45-6 | LOW | DriverBean.java:29 | `// FIXME is it same than licno ?` — unresolved FIXME comment left in production code. The question it raises has not been answered or resolved in any subsequent commit visible in the repository history.

A45-7 | LOW | DriverBean.java:37–39 | Fields `pass`, `cpass`, and `pass_hash` store password-related strings. Because the class is a plain bean with `@Data`, Lombok will generate `toString()` output that includes these fields by default, potentially leaking credential material into logs. `@ToString.Exclude` should be applied to these fields.

A45-8 | LOW | DriverJobDetailsBean.java:105–107 | Two consecutive blank lines at the end of the class body (lines 105–107) before the closing brace. Minor formatting issue; inconsistent with the rest of the file which has no extra blank lines between methods.

A45-9 | INFO | DriverBean.java:17 | Field `first_last` appears to be a pre-concatenated "first last" display name. With `getName()` (line 79) already providing `first_name + " " + last_name`, `first_last` is likely redundant. If it is only populated from a database query alias and never set independently, it may be dead state.
# P4 Agent A46 — DriverUnitBean, DriverVehicleBean, DynamicBean

## Reading Evidence

### DriverUnitBean.java

**Class:** `com.bean.DriverUnitBean` implements `Serializable`
**Annotations:** `@Data`, `@NoArgsConstructor`

**Fields (lines 12–20):**
| Line | Field | Type |
|------|-------|------|
| 12 | `compId` | `Long` |
| 13 | `driverId` | `Long` |
| 14 | `unitId` | `Long` |
| 15 | `name` | `String` |
| 16 | `location` | `String` |
| 17 | `department` | `String` |
| 18 | `assigned` | `boolean` |
| 19 | `hours` | `int` |
| 20 | `trained` | `String` |

**Methods:**
| Lines | Method | Notes |
|-------|--------|-------|
| 22–33 | `DriverUnitBean(Long compId, Long driverId, Long unitId, String name, String location, String department, boolean assigned, int hours, boolean trained)` (private, `@Builder`) | Builder constructor; maps `boolean trained` to `"Yes"`/`"No"` and stores in `String trained` field |

---

### DriverVehicleBean.java

**Class:** `com.bean.DriverVehicleBean` implements `Serializable`
**Annotations:** `@Data`, `@NoArgsConstructor`

**Fields (lines 15–20):**
| Line | Field | Type |
|------|-------|------|
| 15 | `serialVersionUID` | `private static final long` = `-8541229534532258948L` |
| 17 | `compId` | `Long` |
| 18 | `id` | `Long` |
| 20 | `driverUnits` | `List<DriverUnitBean>` (initialized to `new ArrayList<>()`) |

**Methods:**
| Lines | Method | Notes |
|-------|--------|-------|
| 22–27 | `DriverVehicleBean(Long id, Long compId, List<DriverUnitBean> driverUnits)` (private, `@Builder`) | Builder constructor |

---

### DynamicBean.java

**Class:** `com.bean.DynamicBean` implements `Serializable`
**Annotations:** none

**Fields (lines 6–8):**
| Line | Field | Type | Access | Default |
|------|-------|------|--------|---------|
| 6 | `name` | `String` | package-private | `""` |
| 7 | `type` | `String` | package-private | `""` |
| 8 | `value` | `String` | package-private | `""` |

**Methods:**
| Lines | Method |
|-------|--------|
| 10–12 | `getName()` — returns `String` |
| 13–15 | `setName(String name)` — void |
| 16–18 | `getType()` — returns `String` |
| 19–21 | `setType(String type)` — void |
| 22–24 | `getValue()` — returns `String` |
| 25–27 | `setValue(String value)` — void |

---

## Findings

A46-1 | HIGH | DriverUnitBean.java:11 | Missing `serialVersionUID`. The class implements `Serializable` but declares no `serialVersionUID`. Both sibling beans (`DriverVehicleBean`) and `DynamicBean` show the same pattern is relevant; this class is the only `Serializable` implementor in this trio that omits it entirely, which will cause a compiler/IDE warning and risks `InvalidClassException` if the class is ever serialized across JVM versions.

A46-2 | MEDIUM | DriverUnitBean.java:18,20,23,32 | Field type / constructor parameter type mismatch for `trained`. The field `trained` is declared as `String` (line 20), but the `@Builder` constructor parameter for `trained` is typed as `boolean` (line 23). The constructor silently converts `boolean` → `"Yes"`/`"No"` and stores the result in the `String` field. Callers using the Lombok-generated builder receive a `boolean` parameter while the `@Data`-generated getter returns a `String`. This type inconsistency is confusing, undocumented, and could cause misuse or unexpected behaviour.

A46-3 | LOW | DriverUnitBean.java:3 | Unused import. `import lombok.Builder;` is used on the constructor (line 22), so this is not unused — however `@Builder` is applied to a *private* constructor in conjunction with `@NoArgsConstructor` and `@Data`. Placing `@Builder` on a private constructor is an unusual pattern; Lombok's standard class-level `@Builder` is the idiomatic approach. This is a style concern: the builder is functionally accessible but non-standard and may confuse maintainers.

A46-4 | MEDIUM | DynamicBean.java:5 | Missing `serialVersionUID`. The class implements `Serializable` but declares no `serialVersionUID`, which will produce a compiler/IDE warning and risks `InvalidClassException` on deserialization across builds.

A46-5 | MEDIUM | DynamicBean.java:6-8 | Fields are package-private (no access modifier). All three fields (`name`, `type`, `value`) lack an explicit access modifier, making them package-private. The class provides public getters and setters, so the intent is encapsulation, but the fields are directly readable/writable from any class in `com.bean`. They should be `private`.

A46-6 | LOW | DynamicBean.java:5 | Style — no Lombok. `DynamicBean` is a plain-old POJO with hand-written getters/setters while the two sibling beans (`DriverUnitBean`, `DriverVehicleBean`) use `@Data` and `@NoArgsConstructor`. The inconsistent style across the same package increases maintenance burden.

A46-7 | LOW | DynamicBean.java:28-29 | Trailing blank lines. Lines 28–29 are two consecutive blank lines before the closing brace (line 30), which is a minor style inconsistency relative to the rest of the codebase.
# P4 Agent A47 — EmailSubscriptionBean, EntityBean, FormBuilderBean

## Reading Evidence

### EmailSubscriptionBean.java

**Class:** `EmailSubscriptionBean` (package `com.bean`)
**Annotations:** `@Data`, `@NoArgsConstructor` (Lombok)

**Fields:**
| Field | Type | Line |
|---|---|---|
| `id` | `Long` | 11 |
| `driver_id` | `Long` | 12 |
| `email_addr1` | `String` | 13 |
| `email_addr2` | `String` | 14 |
| `email_addr3` | `String` | 15 |
| `email_addr4` | `String` | 16 |
| `op_code` | `String` | 17 |

**Methods:**
| Method | Lines | Notes |
|---|---|---|
| `EmailSubscriptionBean(Long, Long, String, String, String, String, String)` | 20–28 | Private `@Builder` all-args constructor |

---

### EntityBean.java

**Class:** `EntityBean` (package `com.bean`), implements `Serializable`

**Fields:**
| Field | Type | Line |
|---|---|---|
| `serialVersionUID` | `static final long` | 10 |
| `id` | `String` | 11 |
| `name` | `String` | 12 |
| `password` | `String` | 13 |
| `email` | `String` | 14 |
| `arrRoleBean` | `ArrayList<RoleBean>` | 15 |

**Methods:**
| Method | Lines |
|---|---|
| `getArrRoleBean()` | 17–19 |
| `setArrRoleBean(ArrayList<RoleBean>)` | 22–24 |
| `addArrRoleBean(RoleBean)` | 27–29 |
| `getId()` | 32–34 |
| `setId(String)` | 35–37 |
| `getName()` | 38–40 |
| `setName(String)` | 41–43 |
| `getPassword()` | 45–47 |
| `setPassword(String)` | 48–50 |
| `getEmail()` | 51–53 |
| `setEmail(String)` | 54–56 |

---

### FormBuilderBean.java

**Class:** `FormBuilderBean` (package `com.bean`), implements `Serializable`

**Fields:**
| Field | Type | Line |
|---|---|---|
| `serialVersionUID` | `static final long` | 11 |
| `arrElementBean` | `ArrayList<FormElementBean>` | 16 |

**Methods:**
| Method | Lines |
|---|---|
| `getArrElementBean()` | 18–20 |
| `setArrElementBean(ArrayList<FormElementBean>)` | 22–24 |
| `addArrElementBean(FormElementBean)` | 26–28 |

---

## Findings

A47-1 | MEDIUM | EmailSubscriptionBean.java:12 | Field `driver_id` uses snake_case naming. All other fields in this class also use snake_case (`email_addr1`–`email_addr4`, `op_code`). Java conventions require camelCase for field names (e.g., `driverId`, `emailAddr1`, `opCode`). This is a pervasive style violation across all 6 non-id fields (lines 12–17).

A47-2 | LOW | EmailSubscriptionBean.java:3 | `import lombok.Builder` is used but the class is also annotated `@NoArgsConstructor` with a private `@Builder` constructor manually written. Using `@Builder` on a private constructor alongside `@NoArgsConstructor` is unconventional and error-prone — Lombok's `@Builder` is typically placed at the class level. The manual private constructor duplicates what a class-level `@Builder` would generate, creating maintenance risk.

A47-3 | LOW | EntityBean.java:13 | Field `password` is stored as a plain `String`. For a bean that participates in any serialization or session scope, storing a cleartext password in a serializable object is a security hygiene concern. No evidence it is hashed or protected here.

A47-4 | LOW | EntityBean.java:15 | Raw-type-adjacent warning risk: field declared as `ArrayList<RoleBean>` (concrete type) rather than the `List<RoleBean>` interface. Same pattern on `FormBuilderBean.java:16` (`ArrayList<FormElementBean>`). Programming to the concrete `ArrayList` type rather than the `List` interface is a style violation that reduces flexibility and may produce IDE/static-analysis warnings.

A47-5 | LOW | FormBuilderBean.java:11 | `serialVersionUID` value (`3895903590422186042L`) is identical to the `serialVersionUID` in `EntityBean.java:10`. Duplicate `serialVersionUID` values across unrelated `Serializable` classes is not a runtime error but indicates the values were copy-pasted rather than generated, which defeats the purpose of the field as a unique class fingerprint.

A47-6 | LOW | FormBuilderBean.java:7 | Inconsistent indentation: class body opens with a tab-indent level that is deeper than normal (line 7 is empty but the `serialVersionUID` Javadoc block at lines 8–10 is indented with extra tabs compared to the method bodies). Minor but inconsistent with the rest of the file.

A47-7 | INFO | EntityBean.java:7–9 | Auto-generated Javadoc stub `/** * */` above `serialVersionUID` is empty/meaningless boilerplate. Same pattern at `FormBuilderBean.java:8–10` and `FormBuilderBean.java:12–15`. These stub comments add noise without value.
# P4 Agent A48 — FormElementBean, FormLibraryBean, GPSReportFilterBean

## Reading Evidence

### FormElementBean.java
- **Class:** `FormElementBean` (implements `Serializable`)
- **Fields:**
  - `private static final long serialVersionUID = -4110231449812104645L;` (line 11)
  - `private String id = "";` (line 12)
  - `private String name = "";` (line 13)
  - `private String lable = "";` (line 14)
  - `private String type = "";` (line 15)
  - `private String value = "";` (line 16)
  - `private String style = "";` (line 17)
  - `int position;` (line 18) — package-private, no initialiser
- **Methods:**
  - `getId()` — line 21
  - `setId(String id)` — line 24
  - `getPosition()` — line 28
  - `setPosition(int position)` — line 31
  - `getName()` — line 34
  - `setName(String name)` — line 37
  - `getLable()` — line 40
  - `setLable(String lable)` — line 43
  - `getType()` — line 46
  - `setType(String type)` — line 49
  - `getValue()` — line 52
  - `setValue(String value)` — line 55
  - `render()` — line 58
  - `getStyle()` — line 61
  - `setStyle(String style)` — line 64

---

### FormLibraryBean.java
- **Class:** `FormLibraryBean` (implements `Serializable`)
- **Fields:**
  - `private static final long serialVersionUID = -2617219494645726879L;` (line 13)
  - `private String id = null;` (line 17)
  - `private String type = null;` (line 18)
  - `private String question_id = null;` (line 19)
  - `private FormBuilderBean form_object = new FormBuilderBean();` (line 20)
- **Methods:**
  - `getForm_object()` — line 23
  - `setForm_content(byte[] convertObject)` — line 28
  - `getId()` — line 31
  - `setId(String id)` — line 34
  - `getType()` — line 38
  - `setType(String type)` — line 41
  - `getQuestion_id()` — line 44
  - `setQuestion_id(String question_id)` — line 47
  - `getByteArrayObject(FormBuilderBean formBuilderBean)` — line 52
  - `getFormBuilderBean(byte[] convertObject)` — line 69

---

### GPSReportFilterBean.java
- **Class:** `GPSReportFilterBean` (extends `ReportFilterBean`, annotated `@Data`, `@EqualsAndHashCode(callSuper = true)`)
- **Fields:** none declared directly (all inherited from `ReportFilterBean`: `startDate`, `endDate`, `manuId`, `typeId`, `timezone`)
- **Methods:**
  - `GPSReportFilterBean(Date startDate, Date endDate, Long manuId, Long typeId, int unitId)` — line 15 (constructor, annotated `@Builder`)

---

## Findings

A48-1 | LOW | FormElementBean.java:4 | Unused import: `java.util.ArrayList` is imported but never referenced anywhere in the class body. This will produce a compiler warning and adds unnecessary noise.

A48-2 | LOW | FormElementBean.java:14 | Misspelled field name: `lable` should be `label`. The typo is propagated through `getLable()` (line 40) and `setLable()` (line 43). Because this is a public API (getter/setter pair on a Serializable bean), renaming it is a breaking change, but the misspelling is a clear code-quality defect.

A48-3 | MEDIUM | FormElementBean.java:18 | Field `position` has package-private (default) access while all other fields in the same class are `private`. This breaks encapsulation consistency and exposes the field to the entire package without going through the getter/setter.

A48-4 | MEDIUM | FormElementBean.java:58-60 | `render()` is a dead-code stub — it unconditionally returns an empty string and contains no implementation. If it is intended as an abstract hook it should be declared `abstract` (requiring the class to be abstract) or removed. As-is it silently does nothing and misleads callers.

A48-5 | MEDIUM | FormLibraryBean.java:61-63 | Exception swallowed in `getByteArrayObject()`: the `catch (Exception e)` block calls `e.printStackTrace()` and returns `null` (the uninitialised value of `byteArrayObject`). Callers receive a silent `null` with no way to distinguish a failure from a valid result. Same pattern repeated in `getFormBuilderBean()` at line 79-81.

A48-6 | MEDIUM | FormLibraryBean.java:79-81 | Exception swallowed in `getFormBuilderBean()`: `catch (Exception e)` only calls `e.printStackTrace()` and falls through to return a freshly constructed empty `FormBuilderBean()`, silently masking deserialisation failures. The caller (line 29, `setForm_content`) cannot detect that deserialisation failed.

A48-7 | HIGH | FormLibraryBean.java:69-84 | Unsafe deserialisation: `getFormBuilderBean()` deserialises an arbitrary `byte[]` via `ObjectInputStream` with no class whitelist or validation. This is a well-known Java deserialisation vulnerability (CWE-502); if the byte array originates from an untrusted source an attacker can achieve remote code execution.

A48-8 | LOW | FormLibraryBean.java:19 | Field `question_id` uses snake_case, inconsistent with Java naming conventions and all other fields in the same class (`id`, `type`). Getter and setter (`getQuestion_id`, `setQuestion_id`) inherit the same inconsistency.

A48-9 | LOW | FormLibraryBean.java:20 | Field `form_object` uses snake_case, inconsistent with Java naming conventions. Getter is named `getForm_object()` and the asymmetric setter is named `setForm_content()` — the setter name does not follow the `set<FieldName>` convention for the field `form_object`, which will prevent standard JavaBeans introspection from pairing them correctly.

A48-10 | MEDIUM | GPSReportFilterBean.java:15-17 | Constructor parameter `unitId` (type `int`) is accepted but silently discarded — it is never passed to `super(startDate, endDate, manuId, typeId, "")` and is not stored anywhere. The parent class `ReportFilterBean` does not have a `unitId` field, so the parameter appears to have been intended for future use or is a leftover from a refactor. Either way, accepting a value that is ignored is misleading to callers.

A48-11 | LOW | GPSReportFilterBean.java:15 | Spacing inconsistency in the constructor parameter list: no space after the comma between `endDate` and `Long manuId` (`endDate,Long manuId`), unlike the other parameters which have a space after the comma.

A48-12 | INFO | FormLibraryBean.java:3-6 | Imports for `ByteArrayInputStream`, `ByteArrayOutputStream`, `ObjectInputStream`, and `ObjectOutputStream` are all used, but `ByteArrayOutputStream.close()` and `ObjectOutputStream.close()` (lines 58-59) are called without a try-with-resources block. Streams are not closed if `writeObject` throws, though in practice `ByteArrayOutputStream.close()` is a no-op. Using try-with-resources would be safer and cleaner.
# P4 Agent A49 — GPSUnitBean, ImpactBean, ImpactLevel

## Reading Evidence

### GPSUnitBean.java

- **Class:** `GPSUnitBean` (line 16)
- **Lombok annotations:** `@Data`, `@NoArgsConstructor`, `@Builder`, `@AllArgsConstructor(access = AccessLevel.PRIVATE)`
- **Methods:** None explicitly declared (all generated by Lombok)
- **Fields (lines 18–25):**
  - `String vehName` (line 18)
  - `String longitude` (line 19)
  - `String latitude` (line 20)
  - `Timestamp timeStmp` (line 21)
  - `String status` (line 22)
  - `String manufacturer` (line 23)
  - `String type` (line 24)
  - `String power` (line 25)

---

### ImpactBean.java

- **Class:** `ImpactBean` (line 12) — implements `Serializable`
- **Lombok annotations:** `@Data`, `@NoArgsConstructor`
- **Constants:**
  - `private static final long serialVersionUID = -140132772466965248L` (line 13)
- **Fields (lines 15–22):**
  - `private int equipId` (line 15)
  - `private double accHours` (line 16)
  - `private double sessHours` (line 17)
  - `private double impact_threshold` (line 18)
  - `private boolean alert_enabled` (line 19)
  - `private double percentage` (line 20)
  - `private String reset_calibration_date` (line 21)
  - `private String calibration_date` (line 22)
- **Methods:**
  - `ImpactBean(int, double, double, double, boolean, double, String, String)` — `@Builder` private constructor (lines 25–41)
  - `calculateGForceRequiredForImpact(ImpactLevel impactLevel): double` (lines 43–45)

---

### ImpactLevel.java

- **Enum:** `ImpactLevel` (line 3)
- **Methods:** None explicitly declared
- **Constants (enum values, lines 4–6):**
  - `BLUE` (line 4)
  - `AMBER` (line 5)
  - `RED` (line 6)

---

## Findings

A49-1 | HIGH | GPSUnitBean.java:16 | `GPSUnitBean` implements no `Serializable` interface, yet it is a data-transfer bean used alongside other beans (e.g. `ImpactBean`) that do implement `Serializable`. If instances are ever serialized (session storage, caching, JMS, etc.) a `NotSerializableException` will be thrown at runtime. Additionally, without `Serializable` there is no `serialVersionUID`, so the inconsistency across the bean layer is a latent defect.

A49-2 | MEDIUM | ImpactBean.java:18 | Field name `impact_threshold` uses `snake_case` instead of the `camelCase` convention used by every other field in the class (`equipId`, `accHours`, `sessHours`, `percentage`, etc.). Same issue applies to `alert_enabled` (line 19), `reset_calibration_date` (line 21), and `calibration_date` (line 22). Four of eight fields violate the Java naming convention, causing inconsistency within the same class and likely generating non-standard Lombok-generated accessors (`getImpact_threshold()` etc.).

A49-3 | MEDIUM | GPSUnitBean.java:21 | Field `timeStmp` is a misspelling / abbreviation of `timestamp`. All other field names in this class are full words (`vehName` aside). This is a minor naming inconsistency but will propagate to Lombok-generated getter/setter names (`getTimeStmp()`), making the API unclear.

A49-4 | LOW | GPSUnitBean.java:27 | Blank line with only a tab character between the last field and the closing brace — minor trailing-whitespace / extraneous-blank-line style issue consistent with an accidental edit, but inconsequential at runtime.

A49-5 | LOW | GPSUnitBean.java:18 | Field `vehName` uses an abbreviated prefix (`veh`) while all other fields use full words (`longitude`, `latitude`, `status`, `manufacturer`, `type`, `power`). Inconsistent abbreviation style within the same class.

A49-6 | INFO | ImpactLevel.java:3 | `ImpactLevel` is correctly declared as an `enum`. No style issue here; this finding records that the type is an enum (not a class with constants), which is the appropriate design.
# P4 Agent A50 — ImpactReportBean, ImpactReportFilterBean, ImpactReportGroupBean

## Reading Evidence

### ImpactReportBean.java

**Class:** `com.bean.ImpactReportBean`
**Implements:** `Serializable`
**Lombok:** `@Data`, `@NoArgsConstructor`, `@AllArgsConstructor`

**Fields:**
| Field | Type | Line |
|---|---|---|
| `serialVersionUID` | `static final long` | 16 |
| `groups` | `List<ImpactReportGroupBean>` | 18 |

**Methods (Lombok-generated; no explicit methods):**
- Constructor (no-arg) — generated by `@NoArgsConstructor`
- Constructor (all-args) — generated by `@AllArgsConstructor`
- `getGroups()` / `setGroups()` — generated by `@Data`
- `equals()`, `hashCode()`, `toString()` — generated by `@Data`

---

### ImpactReportFilterBean.java

**Class:** `com.bean.ImpactReportFilterBean`
**Extends:** `ReportFilterBean`
**Implements:** `ImpactLevelFilter`
**Lombok:** `@Data`, `@EqualsAndHashCode(callSuper = true)`

**Fields:**
| Field | Type | Line |
|---|---|---|
| `impactLevel` | `ImpactLevel` | 13 |

**Methods:**
| Method | Line |
|---|---|
| `ImpactReportFilterBean(Date, Date, Long, Long, ImpactLevel, String)` (constructor, `@Builder`) | 16 |
| `impactLevel()` (`@Override`) | 22 |

---

### ImpactReportGroupBean.java

**Class:** `com.bean.ImpactReportGroupBean`
**Implements:** `Serializable`, `Comparable<ImpactReportGroupBean>`
**Lombok:** `@Data`, `@NoArgsConstructor`

**Fields:**
| Field | Type | Line |
|---|---|---|
| `serialVersionUID` | `static final long` | 16 |
| `manufacturer` | `String` | 18 |
| `unitName` | `String` | 19 |
| `entries` | `List<ImpactReportGroupEntryBean>` | 21 |

**Methods:**
| Method | Line |
|---|---|
| `ImpactReportGroupBean()` (no-arg, generated by `@NoArgsConstructor`) | — |
| `ImpactReportGroupBean(String, String)` (private `@Builder` constructor) | 25 |
| `addEntry(ImpactReportGroupEntryBean)` | 30 |
| `compareTo(ImpactReportGroupBean)` (`@Override`) | 35 |

---

## Findings

A50-1 | HIGH | ImpactReportGroupBean.java:36 | **Incorrect `compareTo` implementation.** The method returns the sum of two `String.compareTo()` results: `this.manufacturer.compareTo(o.manufacturer) + this.unitName.compareTo(o.unitName)`. Summing two comparator integers is not a valid composite sort key — positive and negative values from the two sub-comparisons can cancel each other out, producing 0 (i.e., "equal") for objects that are not equal. For example, a manufacturer that sorts +1 paired with a unitName that sorts -1 yields 0, falsely reporting equality. The contract of `Comparable` requires a total ordering consistent with `equals`; this implementation violates it. A correct lexicographic comparison would first compare by manufacturer and only fall through to unitName on a tie.

A50-2 | HIGH | ImpactReportGroupBean.java:36 | **NullPointerException risk in `compareTo`.** Neither `this.manufacturer` nor `this.unitName` is guarded against null before `compareTo` is called on them. Because `@NoArgsConstructor` exists (line 13) and `addEntry` can be called on a default-constructed instance where those fields were never set, either field may be null at the time of comparison, causing an unchecked NPE.

A50-3 | MEDIUM | ImpactReportFilterBean.java:16 | **Missing space before `String timezone` parameter.** The constructor signature reads `ImpactLevel impactLevel,String timezone` (no space after the comma). This is a minor formatting inconsistency relative to the rest of the parameter list and the style used in the other beans.

A50-4 | MEDIUM | ImpactReportFilterBean.java:17 | **Missing space before `timezone` argument in super call.** `super(startDate, endDate, manuId, typeId,timezone)` — no space after the comma preceding `timezone`. Consistent with the constructor signature issue above but reported separately as it appears in two places.

A50-5 | MEDIUM | ImpactReportFilterBean.java (class-level) | **Missing `serialVersionUID` in a class that participates in a Serializable hierarchy.** `ImpactReportFilterBean` extends `ReportFilterBean`, which does not declare `serialVersionUID` either. While `ImpactReportFilterBean` itself does not directly declare `implements Serializable`, its superclass chain connects it to serialization. More importantly, the two sibling beans (`ImpactReportBean`, `ImpactReportGroupBean`) both explicitly declare `serialVersionUID`, establishing a pattern. The omission here will cause the compiler/IDE to emit an "implicit serialVersionUID" warning, and the auto-generated ID will change if the class structure changes, silently breaking deserialization of persisted or transmitted instances.

A50-6 | MEDIUM | ImpactReportGroupBean.java:6 | **Unused import.** `import org.apache.commons.collections.ComparatorUtils;` is present but `ComparatorUtils` is never referenced anywhere in the file. This is dead import / dead code — likely a leftover from a refactoring where a proper comparator chain was replaced by the current (broken) arithmetic approach. The build will emit an "unused import" warning.

A50-7 | LOW | ImpactReportGroupBean.java:24-28 | **`@Builder` constructor is `private` but `@NoArgsConstructor` is also present.** Lombok's `@Builder` on a private constructor means the generated builder will call a private constructor, which is intentional for immutability-oriented designs. However, the class also exposes a public no-arg constructor (via `@NoArgsConstructor`) that leaves `manufacturer` and `unitName` unset (null), and then `addEntry` mutates the `entries` list. This dual-construction path is inconsistent: callers using the builder get a fully initialised object, while callers using the no-arg constructor get a partially initialised one. The design intent is unclear and the inconsistency is a maintenance hazard.

A50-8 | LOW | ImpactReportFilterBean.java:12 | **Style inconsistency: no `@AllArgsConstructor` + explicit `@Builder` constructor, while `ImpactReportBean` uses only Lombok-generated constructors.** `ImpactReportFilterBean` manually writes its all-args constructor and annotates it with `@Builder` rather than using `@AllArgsConstructor` at the class level with a class-level `@Builder`. This is not wrong but is inconsistent with the approach used in the other two beans, which rely entirely on Lombok-generated constructors. The inconsistency will confuse maintainers about the intended construction pattern for this family of beans.

A50-9 | INFO | ImpactReportBean.java:18 | **Field initialised inline to `new ArrayList<>()` but `@AllArgsConstructor` will overwrite it.** When Lombok's `@AllArgsConstructor` generates the all-args constructor, it will accept a `List<ImpactReportGroupBean>` parameter and assign it directly to `groups`, bypassing the inline initialiser. This means the inline `= new ArrayList<>()` only takes effect via the no-arg constructor. The behaviour is technically correct but can surprise maintainers who expect the inline initialisation to always apply.
# P4 Agent A51 — ImpactReportGroupEntryBean, IncidentReportBean, IncidentReportEntryBean

## Reading Evidence

### ImpactReportGroupEntryBean.java

**Class:** `com.bean.ImpactReportGroupEntryBean` (implements `Serializable`)
**Annotations:** `@Data`, `@NoArgsConstructor`

**Fields:**
| Field | Type | Line |
|---|---|---|
| `serialVersionUID` | `static final long` | 13 |
| `id` | `Long` | 15 |
| `impactDateTime` | `String` | 16 |
| `impactValue` | `Integer` | 17 |
| `impactThreshold` | `Integer` | 18 |
| `driverName` | `String` | 19 |
| `companyName` | `String` | 20 |

**Methods:**
| Method | Visibility | Line |
|---|---|---|
| `ImpactReportGroupEntryBean(Long, String, Integer, Integer, String, String)` (builder constructor) | `private` | 23 |
| `getImpactLevel()` | `private` | 37 |
| `getGForce()` | `public` | 41 |
| `getImpactLevelCSSColor()` | `public` | 45 |

---

### IncidentReportBean.java

**Class:** `com.bean.IncidentReportBean` (implements `Serializable`)
**Annotations:** `@Data`, `@NoArgsConstructor`, `@AllArgsConstructor`

**Fields:**
| Field | Type | Line |
|---|---|---|
| `serialVersionUID` | `static final long` | 20 |
| `entries` | `List<IncidentReportEntryBean>` | 21 |

**Methods:** None explicitly defined (all generated by Lombok).

---

### IncidentReportEntryBean.java

**Class:** `com.bean.IncidentReportEntryBean` (implements `Serializable`)
**Annotations:** `@Data`, `@Builder`

**Fields:**
| Field | Type | Line |
|---|---|---|
| `serialVersionUID` | `static final long` | 11 |
| `unitName` | `String` | 13 |
| `manufacture` | `String` | 14 |
| `companyName` | `String` | 15 |
| `driverName` | `String` | 16 |
| `reportTime` | `String` | 17 |
| `injureType` | `String` | 18 |
| `witness` | `String` | 19 |
| `location` | `String` | 20 |
| `injury` | `Boolean` | 21 |
| `description` | `String` | 22 |
| `signature` | `String` | 23 |
| `event_time` | `String` | 24 |
| `near_miss` | `Boolean` | 25 |
| `incident` | `Boolean` | 26 |
| `image` | `String` | 27 |

**Methods:** None explicitly defined (all generated by Lombok).

---

## Findings

A51-1 | LOW | ImpactReportGroupEntryBean.java:37 | `getImpactLevel()` is `private`. The method follows a JavaBean getter naming convention (`get` prefix) but is private, meaning Lombok's `@Data` will not expose it and callers outside the class cannot access it. It is only used internally by `getImpactLevelCSSColor()` at line 46. While functional, this is misleading: a `get`-prefixed method that is private can confuse readers expecting a standard accessor. Consider renaming to a non-getter name (e.g., `calculateImpactLevel()`) to avoid the false accessor signal.

A51-2 | LOW | ImpactReportGroupEntryBean.java:23 | The `@Builder` constructor is `private`. Using `@Builder` on a private constructor is unconventional. Lombok's `@Builder` is normally placed on the class or a public/package constructor; placing it on a private constructor works but is non-standard and may confuse maintainers. The class also has `@NoArgsConstructor` at the class level, creating two separate construction paths. A standard pattern would be `@Builder` at the class level alongside `@NoArgsConstructor`.

A51-3 | MEDIUM | IncidentReportEntryBean.java:24-26 | Three fields use `snake_case` naming (`event_time`, `near_miss`, `incident` is camelCase, but `event_time` and `near_miss` violate Java naming conventions). All other fields in this class and in sibling beans use `camelCase`. `event_time` (line 24) and `near_miss` (line 25) should be `eventTime` and `nearMiss`. Lombok-generated getters for these fields will be `getEvent_time()` and `getNear_miss()`, which are non-standard and may break serialization frameworks that rely on standard getter naming (e.g., Jackson, JAX-B).

A51-4 | LOW | IncidentReportBean.java:17-19 | The `serialVersionUID` Javadoc comment is auto-generated boilerplate (`/** \n * \n */`) with no meaningful content. This is noise but is a minor style issue. The blank comment should either be removed or replaced with a meaningful description.

A51-5 | LOW | IncidentReportBean.java:14 | Blank line between `@AllArgsConstructor` annotation (line 13) and the `public class` declaration (line 15). Java convention places annotations immediately adjacent to the class declaration with no blank lines between them. The other two files in this set follow the correct convention.

A51-6 | LOW | IncidentReportBean.java:22-23 | Two consecutive blank lines after the `entries` field declaration (lines 22-23) with no explanation. Standard Java style uses a single blank line for separation. This is a minor formatting inconsistency relative to the other beans in the set.

A51-7 | INFO | IncidentReportEntryBean.java:14 | Field `manufacture` is likely a typo for `manufacturer`. This is a domain-level naming issue; if this name is part of a serialized API contract (JSON keys, DB column mappings) changing it may be a breaking change, but it should be tracked.
# P4 Agent A52 — IncidentReportFilterBean, JobDetailsBean, LanguageBean

## Reading Evidence

### IncidentReportFilterBean.java
- **Class:** `com.bean.IncidentReportFilterBean` (extends `ReportFilterBean`)
- **Annotations:** `@Data`, `@EqualsAndHashCode(callSuper = true)` (Lombok)
- **Fields:** none declared directly (all inherited from `ReportFilterBean`)
- **Methods:**
  - `IncidentReportFilterBean(Date startDate, Date endDate, Long manuId, Long typeId, String timezone)` — constructor, line 13 (`@Builder`)

---

### JobDetailsBean.java
- **Class:** `com.bean.JobDetailsBean`
- **Fields (all package-private):**
  - `int id` — line 5
  - `int unitId` — line 6
  - `int driverId` — line 7
  - `int duration` — line 8
  - `String status` — line 9
  - `String driverName` — line 11
  - `String jobNo` — line 12
  - `String description` — line 13
  - `String startTime` — line 14
  - `String endTime` — line 15
  - `String jobTitle` — line 16
- **Methods:**
  - `getId()` — line 18
  - `getUnitId()` — line 21
  - `getDriverId()` — line 24
  - `getDuration()` — line 27
  - `getJobNo()` — line 30
  - `getDescription()` — line 33
  - `getStartTime()` — line 36
  - `getEndTime()` — line 39
  - `getJobTitle()` — line 42
  - `setId(int)` — line 45
  - `setUnitId(int)` — line 48
  - `setDriverId(int)` — line 51
  - `setDuration(int)` — line 54
  - `setJobNo(String)` — line 57
  - `setDescription(String)` — line 60
  - `setStartTime(String)` — line 63
  - `setEndTime(String)` — line 66
  - `setJobTitle(String)` — line 69
  - `getDriverName()` — line 72
  - `setDriverName(String)` — line 75
  - `getStatus()` — line 78
  - `setStatus(String)` — line 81

---

### LanguageBean.java
- **Class:** `com.bean.LanguageBean` (implements `Serializable`)
- **Fields:**
  - `private static final long serialVersionUID = 1779643485158161640L` — line 10
  - `private String id = null` — line 11
  - `private String name = null` — line 12
  - `private String local = null` — line 19
- **Methods:**
  - `getName()` — line 13
  - `setName(String)` — line 16
  - `getLocal()` — line 21
  - `setLocal(String)` — line 24
  - `getId()` — line 28
  - `setId(String)` — line 31

---

## Findings

A52-1 | HIGH | JobDetailsBean.java:3 | Class does not implement `Serializable`. It is a data-transfer bean with only primitive and `String` fields, but if it is ever placed in an HTTP session or serialized for any reason there is no contract and no `serialVersionUID`. Other beans in the same package (`LanguageBean`) do implement `Serializable`, indicating the pattern is established here.

A52-2 | MEDIUM | JobDetailsBean.java:5-16 | All eleven fields have package-private (default) access instead of `private`. The class provides full getters and setters, so the fields should be `private` to enforce encapsulation. This is inconsistent with `LanguageBean`, which correctly declares all fields `private`.

A52-3 | MEDIUM | JobDetailsBean.java:3 | Manual boilerplate POJO: the class hand-writes 22 getters/setters with no Lombok annotation (`@Data`/`@Getter`/`@Setter`). `IncidentReportFilterBean` in the same package uses Lombok `@Data`. This style inconsistency adds maintenance burden and risk of getter/setter drift.

A52-4 | LOW | JobDetailsBean.java:84-87 | Four consecutive blank lines at the end of the class body (lines 84-87) before the closing brace. Minor style noise but inconsistent with the other files in this package.

A52-5 | LOW | LanguageBean.java:7-9 | The `serialVersionUID` Javadoc comment is a bare auto-generated stub (`/** \n * \n */`) with no content. While not harmful, it adds visual noise without value and is inconsistent with the style used elsewhere in the codebase (other fields have no Javadoc at all).

A52-6 | INFO | IncidentReportFilterBean.java:14 | Missing space before `timezone` parameter in the `super(...)` call: `super(startDate, endDate, manuId, typeId,timezone)` — no space after the comma before `timezone`. Minor style inconsistency with standard Java formatting conventions.
# P4 Agent A53 — LicenceBean, ManuTypeFuleRelBean, ManufactureBean

## Reading Evidence

### LicenceBean.java
- **Class:** `LicenceBean` (implements `Serializable`)
- **Annotations:** `@Data`, `@NoArgsConstructor`
- **Fields (all instance, all initialised to `null`):**
  - `Long driver_id` (line 13)
  - `String licence_number` (line 14)
  - `String expiry_date` (line 15)
  - `String security_number` (line 16)
  - `String address` (line 17)
  - `String op_code` (line 18)
- **Methods:**
  - `LicenceBean(Long, String, String, String, String, String)` — private all-args constructor annotated `@Builder` (lines 21–28)
  - (all getters/setters/`equals`/`hashCode`/`toString` generated by Lombok `@Data`)

---

### ManuTypeFuleRelBean.java
- **Class:** `ManuTypeFuleRelBean` (no interfaces)
- **Fields (all instance, all initialised to `null`):**
  - `String id` (line 4)
  - `String manu_id` (line 5)
  - `String type_id` (line 6)
  - `String fuel_type_id` (line 7)
  - `String typename` (line 8)
  - `String fueltypename` (line 9)
  - `String manuname` (line 10)
- **Methods (all manually written):**
  - `getManuname()` (line 12)
  - `setManuname(String)` (line 15)
  - `getId()` (line 18)
  - `setId(String)` (line 21)
  - `getTypename()` (line 25)
  - `setTypename(String)` (line 28)
  - `getFueltypename()` (line 31)
  - `setFueltypename(String)` (line 34)
  - `getManu_id()` (line 39)
  - `setManu_id(String)` (line 42)
  - `getType_id()` (line 45)
  - `setType_id(String)` (line 48)
  - `getFuel_type_id()` (line 51)
  - `setFuel_type_id(String)` (line 54)

---

### ManufactureBean.java
- **Class:** `ManufactureBean` (implements `Serializable`)
- **Annotations:** `@Data`, `@NoArgsConstructor`
- **Fields:**
  - `static final long serialVersionUID = 1390610283858544445L` (line 13)
  - `String id` (line 14)
  - `String name` (line 15)
  - `String company_id` (line 16)
- **Methods:**
  - `ManufactureBean(String, String, String)` — private all-args constructor annotated `@Builder` (lines 19–23)
  - (all getters/setters/`equals`/`hashCode`/`toString` generated by Lombok `@Data`)

---

## Findings

A53-1 | HIGH | ManuTypeFuleRelBean.java:3 | Class name contains a typo: "Fule" should be "Fuel". The correct spelling would be `ManuTypeFuelRelBean`. This typo propagates to every import, reference, and mapping that uses this class throughout the codebase.

A53-2 | HIGH | ManuTypeFuleRelBean.java:3 | Class does not implement `java.io.Serializable`. The other two bean classes in this audit (`LicenceBean`, `ManufactureBean`) both implement `Serializable`. If instances of this class are ever serialized (HTTP session, caching, JMS, etc.) the omission will cause a runtime `NotSerializableException`.

A53-3 | HIGH | ManuTypeFuleRelBean.java:3 | No `serialVersionUID` declared. Even if `Serializable` is added later, the absence of an explicit `serialVersionUID` means the JVM will auto-compute one that changes whenever the class structure changes, risking `InvalidClassException` on deserialization.

A53-4 | MEDIUM | LicenceBean.java:3 | Unused import: `lombok.Builder` is imported but the annotation is applied only to the private constructor on line 20. The import itself is technically used, however the `@Builder` annotation on a `private` constructor in a `@Data` / `@NoArgsConstructor` class is an unusual and potentially confusing pattern — the generated builder will not be publicly accessible in the normal Lombok sense and may produce a compiler warning depending on Lombok version.

A53-5 | MEDIUM | ManuTypeFuleRelBean.java:3 | Class is written with hand-rolled getters/setters (14 methods) while the other beans in this package use Lombok `@Data`. This is a style inconsistency that increases boilerplate, raises maintenance burden, and was likely the cause of the missing `equals`, `hashCode`, and `toString` implementations.

A53-6 | MEDIUM | LicenceBean.java:13-18 | Field names use `snake_case` (`driver_id`, `licence_number`, `expiry_date`, `security_number`, `op_code`) instead of the Java convention of `camelCase`. The same issue is present in `ManufactureBean.java:16` (`company_id`) and throughout `ManuTypeFuleRelBean.java` (`manu_id`, `type_id`, `fuel_type_id`). This is a project-wide style violation that also causes Lombok-generated accessor names to be non-standard (e.g., `getDriver_id()` instead of `getDriverId()`).

A53-7 | LOW | LicenceBean.java:3 | Missing `serialVersionUID`. The class implements `Serializable` (line 11) but declares no explicit `serialVersionUID`, unlike `ManufactureBean` which correctly declares one (line 13). The JVM will auto-generate a value that may change across compiler versions or class edits, breaking serialization compatibility.

A53-8 | LOW | ManuTypeFuleRelBean.java:37-38 | Blank lines 37–38 are an extra blank line between method groups with no consistent blank-line discipline in the file. Minor but contributes to inconsistent formatting relative to the other beans.

A53-9 | INFO | ManufactureBean.java:3 | `ManufactureBean` is named for a "manufacture" (a verb/noun for the act) rather than "Manufacturer" (the entity). This may cause confusion but appears to be a consistent naming choice across the codebase, so it is noted for awareness only.
# P4 Agent A54 — MenuBean, PreOpsReportBean, PreOpsReportEntryBean

## Reading Evidence

### MenuBean.java

**Class:** `com.bean.MenuBean` (implements `Serializable`)

**Fields:**
- `private String id` (line 6)
- `private String name` (line 7)
- `private String description` (line 8)
- `private String icon` (line 9)
- `private String action` (line 10)

**Methods:**
- `getAction()` — line 12
- `setAction(String action)` — line 15
- `getId()` — line 18
- `setId(String id)` — line 21
- `getName()` — line 25
- `setName(String name)` — line 28
- `getDescription()` — line 31
- `setDescription(String description)` — line 34
- `getIcon()` — line 37
- `setIcon(String icon)` — line 40

---

### PreOpsReportBean.java

**Class:** `com.bean.PreOpsReportBean` (implements `Serializable`)

**Annotations:** `@Data`, `@NoArgsConstructor`, `@AllArgsConstructor`

**Fields:**
- `private static final long serialVersionUID = -1805583864595923807L` (line 16)
- `private List<PreOpsReportEntryBean> entries = new ArrayList<>()` (line 18)

**Methods:** None explicitly declared (all generated by Lombok `@Data`, `@NoArgsConstructor`, `@AllArgsConstructor`)

---

### PreOpsReportEntryBean.java

**Class:** `com.bean.PreOpsReportEntryBean` (implements `Serializable`)

**Annotations:** `@Data`, `@NoArgsConstructor`

**Fields:**
- `private static final long serialVersionUID = 2880681360556430594L` (line 14)
- `private String unitName` (line 16)
- `private String manufacture` (line 17)
- `private String companyName` (line 18)
- `private String driverName` (line 19)
- `private String checkDateTime` (line 20)
- `private ArrayList<String> failures = new ArrayList<>()` (line 21)
- `private LocalTime duration` (line 22)
- `private String comment` (line 23)

**Methods:**
- `PreOpsReportEntryBean(String unitName, String manufacture, String companyName, String driverName, String checkDateTime, LocalTime duration, ArrayList<String> failures, String comment)` — `@Builder` constructor, private, lines 26–42

---

## Findings

A54-1 | HIGH | MenuBean.java:5 | Missing `serialVersionUID`. The class implements `Serializable` but declares no `serialVersionUID` field. This will cause a compiler/IDE warning and creates a risk of `InvalidClassException` during deserialization if the class is ever compiled by a different compiler or after any field change.

A54-2 | MEDIUM | MenuBean.java:5 | Inconsistent style vs. sibling beans. `MenuBean` hand-codes all getters and setters (10 methods, ~40 lines) while the directly adjacent beans `PreOpsReportBean` and `PreOpsReportEntryBean` use Lombok `@Data` to generate the same boilerplate. The codebase has adopted Lombok; `MenuBean` should follow the same convention.

A54-3 | MEDIUM | MenuBean.java:12–42 | Inconsistent blank-line spacing between accessor pairs. `getAction`/`setAction` (lines 12–17) has no blank line before `getId` (line 18), `setId` (lines 21–23) has a blank line before `getName` (line 25), and `setName` (lines 28–30) has no blank line before `getDescription` (line 31). Blank lines between pairs are applied erratically, making the ordering harder to scan.

A54-4 | MEDIUM | PreOpsReportEntryBean.java:17 | Probable typo in field name `manufacture` — should be `manufacturer`. The field represents the name of the manufacturer (a noun), not the act of manufacturing. This is a semantic naming error that propagates through the Lombok-generated getter (`getManufacture`) and setter, and through any JSON serialization keys bound to this field name.

A54-5 | MEDIUM | PreOpsReportEntryBean.java:21 | Field declared as concrete type `ArrayList<String>` instead of the interface type `List<String>`. Using the concrete type unnecessarily tightens the contract. The `@Builder` constructor parameter (line 32) also accepts `ArrayList<String>`. `List<String>` is the conventional and more flexible type to use for both field and parameter declarations.

A54-6 | LOW | PreOpsReportEntryBean.java:25 | `@Builder` is placed on a private constructor alongside a class-level `@NoArgsConstructor`. This combination is valid but unusual: `@Builder` on a private constructor means the generated builder is still accessible (Lombok makes the builder class package-private by default), while the constructor itself is private. If the intent is to enforce builder-only construction, the `@NoArgsConstructor` annotation contradicts that intent by also generating a public no-args constructor. If both construction paths are intentional, this should be documented.

A54-7 | LOW | PreOpsReportEntryBean.java:20 | `checkDateTime` is typed as `String` rather than a temporal type (e.g., `LocalDateTime`, `ZonedDateTime`). The field name implies a date-time value. Storing date-times as strings bypasses type safety and requires manual parsing everywhere the value is consumed. `LocalTime duration` (line 22) in the same class is correctly typed, making the inconsistency more noticeable.

A54-8 | LOW | PreOpsReportBean.java:13 | `@AllArgsConstructor` is present alongside a field that is initialized inline (`entries = new ArrayList<>()`). The all-args constructor generated by Lombok will accept an `entries` argument and overwrite the inline initializer, which is the expected behaviour — however the combination signals that the class was possibly designed for immutable construction but was later given an inline default, creating a subtle dual-path inconsistency. Given the class has only one field, `@AllArgsConstructor` provides minimal value and may be an oversight.
# P4 Agent A55 — PreOpsReportFilterBean, ProfileBean, QuestionBean

## Reading Evidence

### PreOpsReportFilterBean.java
- **Class:** `PreOpsReportFilterBean` (extends `ReportFilterBean`)
- **Annotations:** `@Data`, `@EqualsAndHashCode(callSuper = true)`
- **Fields:** None declared directly (all fields inherited from `ReportFilterBean`)
- **Methods:**
  - `PreOpsReportFilterBean(Date startDate, Date endDate, Long manuId, Long typeId, String timezone)` — line 13 (annotated `@Builder`, delegates to `super(...)`)

---

### ProfileBean.java
- **Class:** `ProfileBean`
- **Fields:** None
- **Methods:**
  - `ProfileBean()` — line 5 (default constructor, auto-generated stub)

---

### QuestionBean.java
- **Class:** `QuestionBean` (implements `Serializable`)
- **Annotations:** `@Data`, `@NoArgsConstructor`
- **Fields:**
  - `serialVersionUID` — line 14 (`private static final long`, value `-697498145689541652L`)
  - `id` — line 15 (`private String`, default `null`)
  - `content` — line 16 (`private String`, default `null`)
  - `expectedanswer` — line 17 (`private String`, default `null`)
  - `order_no` — line 18 (`private int`)
  - `active` — line 19 (`private String`, default `null`)
  - `type_id` — line 20 (`private String`, default `null`)
  - `manu_id` — line 21 (`private String`, default `null`)
  - `fuel_type_id` — line 22 (`private String`, default `null`)
  - `attachment_id` — line 23 (`private String`, default `null`)
  - `comp_id` — line 24 (`private String`, default `null`)
  - `answer_type` — line 25 (`private String`, default `null`)
  - `barCodeY` — line 26 (`private String`, default `null`)
  - `barCodeN` — line 27 (`private String`, default `null`)
  - `copied_from_id` — line 28 (`private String`, default `null`)
- **Methods:**
  - `QuestionBean(String id, String content, String expectedanswer, int order_no, String active, String type_id, String manu_id, String fuel_type_id, String attachment_id, String comp_id, String answer_type, String barCodeY, String barCodeN, String copied_from_id)` — line 31 (annotated `@Builder`, `private`)

---

## Findings

A55-1 | HIGH | ProfileBean.java:3 | Class is completely empty (no fields, no meaningful methods). The only method is the IDE-generated stub constructor with a `// TODO Auto-generated constructor stub` comment. This is dead/stub code that was never developed; the class serves no purpose and should either be completed or removed.

A55-2 | LOW | ProfileBean.java:6 | Commented-out IDE stub comment `// TODO Auto-generated constructor stub` has been left in source permanently. TODO comments must not be committed to production source without tracking items; this one indicates the constructor body was never intentionally written.

A55-3 | MEDIUM | ProfileBean.java:3 | `ProfileBean` does not implement `Serializable` and has no `serialVersionUID`. Although the class is currently empty, it is named as a bean and will likely be serialized (e.g. session, RMI, JPA). If it is ever populated, this omission becomes a build/runtime risk.

A55-4 | MEDIUM | QuestionBean.java:18 | Field `order_no` uses snake_case naming, inconsistent with the Java naming convention (camelCase). All other `int`/`String` fields in the same class and the wider codebase use camelCase. This will also produce a Lombok-generated getter/setter `getOrder_no()` / `setOrder_no()` which violates JavaBeans conventions and may break frameworks that rely on introspection (e.g. Jackson, Spring MVC).

A55-5 | MEDIUM | QuestionBean.java:17,20,21,22,23,24,25,26,27,28 | Multiple fields use snake_case names (`expectedanswer`, `type_id`, `manu_id`, `fuel_type_id`, `attachment_id`, `comp_id`, `answer_type`, `barCodeY`, `barCodeN`, `copied_from_id`). Java naming convention requires camelCase for field names. Lombok-generated accessors will reflect these non-standard names, potentially breaking JSON serialization and JavaBeans introspection.

A55-6 | LOW | PreOpsReportFilterBean.java:13 | Missing space before the `String timezone` parameter (written as `Long typeId,String timezone`). Minor style inconsistency; a space after the comma is standard Java style and is present for all other parameters in the same signature.

A55-7 | INFO | QuestionBean.java:8 | `java.util.ArrayList` is imported but never used anywhere in the class body. This is an unused import that will produce a compiler warning.
# P4 Agent A56 — QuestionContentBean, ReportFilterBean, ResultBean

## Reading Evidence

### QuestionContentBean.java

**Class:** `com.bean.QuestionContentBean` (line 12)
**Implements:** `java.io.Serializable`
**Annotations:** `@Getter`, `@Setter`, `@Builder` (Lombok)

**Fields:**
| Field | Type | Line | Default |
|---|---|---|---|
| `serialVersionUID` | `static final long` | 13 | `8571950545814110379L` |
| `id` | `String` | 15 | `null` |
| `question_id` | `String` | 16 | `null` |
| `content` | `String` | 17 | `null` |
| `language_id` | `String` | 18 | `null` |

**Methods (explicit):** None — all accessors generated by Lombok `@Getter`/`@Setter`.

---

### ReportFilterBean.java

**Class:** `com.bean.ReportFilterBean` (line 14)
**Implements:** `DateBetweenFilter`, `UnitManufactureFilter`, `UnitTypeFilter`
**Annotations:** `@Data`, `@AllArgsConstructor` (Lombok)

**Fields:**
| Field | Type | Line |
|---|---|---|
| `startDate` | `Date` | 15 |
| `endDate` | `Date` | 16 |
| `manuId` | `Long` | 17 |
| `typeId` | `Long` | 18 |
| `timezone` | `String` | 19 |

**Methods:**
| Method | Line | Notes |
|---|---|---|
| `start()` | 22 | `@Override`; returns `startDate` or `Calendar.getInstance().getTime()` |
| `end()` | 27 | `@Override`; returns `endDate` or `Calendar.getInstance().getTime()` |
| `manufactureId()` | 32 | `@Override`; returns `manuId` |
| `type()` | 37 | `@Override`; returns `typeId` |
| `timezone()` | 41 | `@Override`; returns `timezone` |

---

### ResultBean.java

**Class:** `com.bean.ResultBean` (line 15)
**Implements:** `java.io.Serializable`
**Annotations:** `@Data`, `@NoArgsConstructor` (Lombok)

**Fields:**
| Field | Type | Line | Default |
|---|---|---|---|
| `serialVersionUID` | `static final long` | 17 | `8057837640488605051L` |
| `id` | `Long` | 20 | `null` |
| `driver_id` | `Long` | 21 | `null` |
| `unit_id` | `String` | 22 | `null` |
| `comment` | `String` | 23 | `null` |
| `timestamp` | `Timestamp` | 24 | `null` |
| `time` | `String` | 25 | `null` |
| `loc` | `String` | 26 | `null` |
| `odemeter` | `String` | 27 | `null` |
| `arrAnswer` | `List<AnswerBean>` | 28 | `new ArrayList<AnswerBean>()` |
| `ans` | `Map<String, String>` | 29 | `new LinkedHashMap<String, String>()` |

**Methods:**
| Method | Line | Notes |
|---|---|---|
| `addAnswer(String queId, String anser)` | 32 | Puts entry into `ans` map |
| `addAnswer(AnswerBean answerBean)` | 36 | Adds to `arrAnswer` list |
| `isDriverIdSetted()` | 40 | Returns `true` if `driver_id` is non-null and non-zero |

---

## Findings

A56-1 | LOW | QuestionContentBean.java:15-18 | Non-standard field naming: `question_id` and `language_id` use snake_case instead of Java convention camelCase (`questionId`, `languageId`). Lombok-generated getters will be `getQuestion_id()` and `getLanguage_id()`, which are non-idiomatic and may break JSON serialization frameworks expecting `questionId`/`languageId`.

A56-2 | LOW | ReportFilterBean.java:14 | Missing `serialVersionUID`: the class implements interfaces (`DateBetweenFilter`, `UnitManufactureFilter`, `UnitTypeFilter`) and uses `@Data` (which does not add `Serializable`), but the class itself does not implement `Serializable` nor declare a `serialVersionUID`. If any downstream code serializes this bean, no explicit `serialVersionUID` will be present. This is a build warning candidate.

A56-3 | MEDIUM | ReportFilterBean.java:23,28 | Misleading default behaviour in `start()` and `end()`: when `startDate` or `endDate` is `null`, both methods silently return the current time (`Calendar.getInstance().getTime()`). This means a caller receiving a non-null `Date` from `start()`/`end()` cannot distinguish between a legitimately supplied date and a defaulted one. A `null` return (or a thrown `IllegalStateException`) would make the absence of a configured date explicit.

A56-4 | MEDIUM | ReportFilterBean.java:41-44 | Mixed indentation: lines 41-44 (`timezone()` method) use a single tab for indentation, while all other methods (lines 21-39) use four spaces. This inconsistency is visible in the raw source and indicates the method was added separately without conforming to the file's established style.

A56-5 | LOW | ResultBean.java:21-27 | Non-standard field naming: `driver_id`, `unit_id`, `loc`, `odemeter` use snake_case or non-descriptive abbreviations. `loc` lacks clarity (location? locale?). Lombok-generated accessors (`getDriver_id()`, `getUnit_id()`) are non-idiomatic Java.

A56-6 | HIGH | ResultBean.java:27 | Typo in field name `odemeter` — correct spelling is `odometer`. This is a public API surface (via Lombok `@Data` getter/setter: `getOdemeter()`/`setOdemeter()`). Renaming it is a breaking change once deployed; the misspelling is now effectively frozen unless a coordinated rename is performed across all callers.

A56-7 | MEDIUM | ResultBean.java:40 | Non-standard method name `isDriverIdSetted()` — correct English past participle is "set" (not "setted"); conventional Java naming would be `isDriverIdSet()`. This is a public method and a breaking rename.

A56-8 | LOW | ResultBean.java:41 | Use of `!=` for `Long` object comparison: `this.driver_id != 0L` compares a `Long` wrapper object to a primitive `long` using reference-equality semantics before auto-unboxing. While Java will auto-unbox here and the comparison is functionally correct, this pattern is fragile — if `driver_id` were ever `null` at that point without the earlier null guard, it would throw a `NullPointerException`. The expression is safe only because of the `&&` short-circuit, but `.equals()` or `Long.valueOf(0L).equals(this.driver_id)` would make intent explicit and avoid the boxing trap.

A56-9 | LOW | ResultBean.java:15 | Missing space before `{` in class declaration: `implements Serializable{` (no space before brace). Minor style inconsistency relative to the broader codebase norm.

A56-10 | LOW | ResultBean.java:28-29 | Raw diamond without inference: `new ArrayList<AnswerBean>()` and `new LinkedHashMap<String, String>()` explicitly repeat the type parameter. Under Java 7+ these can use the diamond operator `<>`. Not a bug, but generates an IDE/compiler "unchecked" or "unnecessary type argument" hint depending on tooling configuration.
# P4 Agent A57 — RoleBean, ServiceBean, SessionBean

## Reading Evidence

### RoleBean.java

**Class:** `com.bean.RoleBean` (implements `Serializable`)
**Annotations:** `@Data`, `@NoArgsConstructor`

**Fields (lines 14–17):**
| Line | Field | Type | Initial value |
|------|-------|------|---------------|
| 14 | `id` | `String` | `null` |
| 15 | `name` | `String` | `null` |
| 16 | `description` | `String` | `null` |
| 17 | `authority` | `String` | `null` |

**Methods (explicit — Lombok generates the rest):**
| Lines | Method | Notes |
|-------|--------|-------|
| 20–25 | `private RoleBean(String id, String name, String description, String authority)` | `@Builder`-annotated private all-args constructor |

**Lombok-generated (implicit):** `getId()`, `setId()`, `getName()`, `setName()`, `getDescription()`, `setDescription()`, `getAuthority()`, `setAuthority()`, `equals()`, `hashCode()`, `toString()`, no-args constructor.

**serialVersionUID:** line 12 — `7809198793440326887L` — present.

---

### ServiceBean.java

**Class:** `com.bean.ServiceBean` (no `implements`, no annotations)

**Fields (lines 5–16):**
| Line | Field | Type |
|------|-------|------|
| 5 | `id` | `int` |
| 6 | `unitId` | `int` |
| 7 | `servType` | `String` |
| 8 | `servLast` | `int` |
| 9 | `servNext` | `int` |
| 10 | `servDuration` | `int` |
| 11 | `accHours` | `double` |
| 12 | `servStatus` | `String` |
| 13 | `hrsTilNext` | `String` |
| 15 | `hoursTillNextService` | `double` |
| 16 | `hourmeter` | `double` |

**Methods:**
| Lines | Method |
|-------|--------|
| 18–20 | `getServLast()` |
| 22–24 | `setServLast(int servLast)` |
| 26–28 | `getServNext()` |
| 30–32 | `getServDuration()` |
| 34–36 | `setServNext(int servNext)` |
| 38–40 | `setServDuration(int servDuration)` |
| 42–44 | `getId()` |
| 46–48 | `getUnitId()` |
| 50–52 | `getServType()` |
| 54–56 | `setId(int id)` |
| 58–60 | `setUnitId(int unitId)` |
| 62–64 | `setServType(String servType)` |
| 66–68 | `getServStatus()` |
| 70–72 | `setServStatus(String servStatus)` |
| 74–76 | `getHrsTilNext()` |
| 78–80 | `setHrsTilNext(String hrsTilNext)` |
| 82–84 | `getHoursTillNextService()` |
| 86–88 | `setHoursTillNextService(double hoursTillNextService)` |
| 90–92 | `getHourmeter()` |
| 94–96 | `setHourmeter(double hourmeter)` |
| 98–100 | `getAccHours()` |
| 102–104 | `setAccHours(double accHours)` |

**serialVersionUID:** absent.

---

### SessionBean.java

**Class:** `com.bean.SessionBean` (implements `Serializable`)
**Annotations:** `@Data`, `@NoArgsConstructor`, `@Builder`, `@AllArgsConstructor(access = AccessLevel.PRIVATE)`

**Fields (lines 14–20):**
| Line | Field | Type |
|------|-------|------|
| 14 | `id` | `int` |
| 15 | `driverId` | `int` |
| 16 | `driverName` | `String` |
| 17 | `unitId` | `int` |
| 18 | `unitName` | `String` |
| 19 | `startTime` | `String` |
| 20 | `finishTime` | `String` |

**Methods (explicit — Lombok generates the rest):** none (all constructor/accessor generation delegated to Lombok).

**Lombok-generated (implicit):** getters, setters, `equals()`, `hashCode()`, `toString()`, no-args constructor, private all-args constructor, builder.

**serialVersionUID:** line 12 — `3194140344175633709L` — present.

---

## Findings

A57-1 | HIGH | ServiceBean.java:3 | `ServiceBean` does not implement `Serializable`. Both sibling beans in this package (`RoleBean`, `SessionBean`) implement `Serializable`, and beans used in a Java EE / Spring web layer are frequently placed in HTTP sessions or serialized for caching. Omitting `Serializable` is a latent runtime risk and an inconsistency with the established pattern in this package.

A57-2 | HIGH | ServiceBean.java:3 | Missing `serialVersionUID`. Because `ServiceBean` is not declared `Serializable` (see A57-1), the compiler does not warn about the absent UID, but if `Serializable` were added without an explicit UID the JVM would generate a volatile one, breaking deserialization across recompilations. The correct fix is to add both `implements Serializable` and an explicit `serialVersionUID` together.

A57-3 | MEDIUM | ServiceBean.java:13 | Field `hrsTilNext` uses an abbreviated, inconsistent name. The conceptually identical value is exposed via the getter `getHrsTilNext()` / setter `setHrsTilNext()`, while the parallel field introduced at line 15 is fully spelled out as `hoursTillNextService`. These two fields represent the same domain concept ("hours until next service") stored redundantly under two different names and two different types (`String` vs `double`), creating confusion about which is canonical. The abbreviation `hrsTilNext` also deviates from the camelCase naming convention used everywhere else in the class.

A57-4 | MEDIUM | ServiceBean.java:13+15 | Duplicate / redundant fields for the same concept. `hrsTilNext` (String, line 13) and `hoursTillNextService` (double, line 15) both appear to represent "hours until next service". Carrying the same datum twice in different types is dead-weight state: whichever is not the authoritative source is effectively dead code once the other is populated. There is no logic inside this class to keep them in sync.

A57-5 | LOW | RoleBean.java:3 | Unused import: `import lombok.Builder;`. The `@Builder` annotation is applied at line 19 on the private constructor, not at the class level, so the import is used. However, importing `lombok.Builder` individually while `@NoArgsConstructor` and `@Data` are also imported individually is consistent — no wildcard import inconsistency here. (Retracted — import is needed. No finding.)

A57-5 | LOW | ServiceBean.java:1–105 | `ServiceBean` is a hand-written POJO with 22 explicit getter/setter methods while both sibling beans (`RoleBean`, `SessionBean`) use Lombok `@Data` to generate the same boilerplate. This is a style inconsistency across the package: the two patterns (manual vs. Lombok-generated accessors) should be unified. The hand-written approach also increases maintenance burden and the risk of accidentally asymmetric getters/setters.

A57-6 | LOW | RoleBean.java:19 | `@Builder` is placed on a private constructor rather than at the class level. This is a non-idiomatic Lombok usage. The conventional pattern (used in `SessionBean`) is `@Builder` at the class level combined with `@AllArgsConstructor(access = AccessLevel.PRIVATE)`. The current placement produces equivalent bytecode but is less readable and diverges from the pattern established in `SessionBean`.

A57-7 | INFO | SessionBean.java:3 | Wildcard import `import lombok.*;` is used instead of explicit named imports. `RoleBean` imports three individual Lombok annotations explicitly. Using `import lombok.*` is inconsistent with the style in `RoleBean` and is generally discouraged as it obscures which annotations are actually in use.
# P4 Agent A58 — SessionFilterBean, SessionReportBean, SubscriptionBean

## Reading Evidence

### SessionFilterBean.java
**Class:** `com.bean.SessionFilterBean`
**Implements:** `DateBetweenFilter`, `SessionUnitFilter`, `SessionDriverFilter`
**Annotations:** `@Data`, `@Builder`

**Fields (lines 15–20):**
| Field | Type | Line |
|---|---|---|
| `companyId` | `Long` | 15 |
| `vehicleId` | `Long` | 16 |
| `driverId` | `Long` | 17 |
| `startDate` | `Date` | 18 |
| `endDate` | `Date` | 19 |
| `timezone` | `String` | 20 |

**Methods:**
| Method | Lines | Notes |
|---|---|---|
| `start()` | 23–25 | `@Override`; returns `startDate` or current time |
| `end()` | 28–30 | `@Override`; returns `endDate` or current time |
| `driverId()` | 33 | `@Override`; returns `driverId` field |
| `unitId()` | 36 | `@Override`; returns `vehicleId` field |
| `timezone()` | 38–41 | `@Override`; returns `timezone` field |

---

### SessionReportBean.java
**Class:** `com.bean.SessionReportBean`
**Implements:** `Serializable`
**Annotations:** `@Data`, `@NoArgsConstructor`, `@AllArgsConstructor`

**Fields (lines 15–17):**
| Field | Type | Line |
|---|---|---|
| `serialVersionUID` | `static final long` | 15 |
| `sessions` | `List<SessionBean>` | 17 |

**Methods:** None declared explicitly; all generated by Lombok (`@Data`, `@NoArgsConstructor`, `@AllArgsConstructor`).

---

### SubscriptionBean.java
**Class:** `com.bean.SubscriptionBean`
**Implements:** `Serializable`
**Annotations:** `@Data`, `@NoArgsConstructor`

**Fields (lines 16–22):**
| Field | Type | Line |
|---|---|---|
| `serialVersionUID` | `static final long` | 16 |
| `id` | `String` | 17 |
| `name` | `String` | 18 |
| `type` | `String` | 19 |
| `frequency` | `String` | 20 |
| `file_name` | `String` | 21 |
| `arrUser` | `ArrayList<UserBean>` | 22 |

**Methods:**
| Method | Lines | Notes |
|---|---|---|
| `SubscriptionBean(...)` (private builder constructor) | 26–34 | `@Builder` annotated private constructor |

---

## Findings

A58-1 | LOW | SessionFilterBean.java:38–41 | Mixed indentation style. Lines 38–41 use hard tabs for indentation while the rest of the file (lines 22–36) uses 4-space indentation. The `timezone()` method block is inconsistently indented compared to the other `@Override` methods above it.

A58-2 | LOW | SessionFilterBean.java:14 | Class does not implement `Serializable`. It is used as a filter/query parameter bean. While not strictly required for its current purpose, all other beans in this package implement `Serializable`. Inconsistency may cause issues if instances are ever stored in a session or transmitted remotely.

A58-3 | MEDIUM | SubscriptionBean.java:21 | Field `file_name` uses snake_case naming, violating Java naming conventions. All other fields in this class and in the codebase use camelCase. This will also cause Lombok-generated getter/setter to be named `getFile_name()` / `setFile_name()` rather than the conventional `getFileName()` / `setFileName()`, which is inconsistent with the rest of the API surface.

A58-4 | MEDIUM | SubscriptionBean.java:22 | Field `arrUser` is declared as the concrete type `ArrayList<UserBean>` rather than the interface type `List<UserBean>`. Programming to a concrete collection type instead of the interface reduces flexibility and is a style violation. The `@Builder` constructor on line 27 also accepts `ArrayList<UserBean>`, propagating the same issue.

A58-5 | LOW | SubscriptionBean.java:6–7 | Unused imports: `lombok.Builder` and `lombok.NoArgsConstructor` are listed on lines 6 and 8 respectively. `@NoArgsConstructor` is used at the class level (line 11), so that import is valid. However, `@Builder` on line 6 is applied only to the private constructor (line 25), not the class — this is an intentional but unusual pattern. The import itself is used, but the pattern of placing `@Builder` on a private constructor alongside a class-level `@NoArgsConstructor` (without `@AllArgsConstructor`) is unconventional and may confuse maintainers, as `@Builder` normally belongs at the class level.

A58-6 | LOW | SubscriptionBean.java:12 | Missing space before the opening brace in `implements Serializable{` (no space between `Serializable` and `{`). Minor style inconsistency compared to `SessionReportBean.java` line 14 which correctly writes `implements Serializable {` with a space.

A58-7 | LOW | SubscriptionBean.java:23–24 | Blank lines inside the class body between field declarations and the builder constructor are inconsistent — there is an extra blank line at line 23 and another at line 35 (trailing blank before closing brace). Minor whitespace inconsistency.

A58-8 | INFO | SessionReportBean.java:17 | Field `sessions` is initialized to `new ArrayList<>()` at the field level, but the class also declares `@AllArgsConstructor`. The all-args constructor will accept a caller-supplied `List<SessionBean>`, which may replace the default empty list. This is functional but the field-level initializer is effectively dead when the all-args constructor is used, which may mislead readers into thinking the field always starts non-null by default without considering the constructor path.
# P4 Agent A59 — TimezoneBean, UnitAssignmentBean, UnitBean

## Reading Evidence

### TimezoneBean.java
- **Class:** `com.bean.TimezoneBean`
- **Annotations:** `@Data`, `@NoArgsConstructor` (Lombok)
- **Implements:** `Serializable`
- **Methods (explicit):** None — all getters/setters/equals/hashCode/toString generated by `@Data`
- **Fields:**
  - `private static final long serialVersionUID = 6558677309215878830L;` (line 15)
  - `private String id = "";` (line 17)
  - `private String name = "";` (line 18)
  - `private String zone = "";` (line 19)

---

### UnitAssignmentBean.java
- **Class:** `com.bean.UnitAssignmentBean`
- **Annotations:** `@Data`, `@NoArgsConstructor` (Lombok)
- **Implements:** `Serializable`
- **Methods (explicit):**
  - `private UnitAssignmentBean(int id, String company_name, String start, String end, boolean isCurrent)` — `@Builder` constructor, lines 21–27
- **Fields:**
  - `private static final long serialVersionUID = -8022411544469272819L;` (line 12)
  - `private int id;` (line 14)
  - `private String company_name;` (line 15)
  - `private String start;` (line 16)
  - `private String end;` (line 17)
  - `private String current;` (line 18)

---

### UnitBean.java
- **Class:** `com.bean.UnitBean`
- **Annotations:** `@Data`, `@NoArgsConstructor` (Lombok)
- **Implements:** `Serializable`
- **Nested type:** `enum KeypadReaderModel { ROSLARE, KERI, SMART, HID_ICLASS }` (lines 66–71)
- **Methods (explicit):**
  - `private UnitBean(String id, String name, String location, String department, String type_id, String type_nm, String comp_id, String active, double size, String manu_id, String manu_name, String fuel_type_id, String fule_type_name, double hourmeter, String serial_no, String acchours, String mac_address, String exp_mod, boolean accessible, String access_type, KeypadReaderModel keypad_reader, String facility_code, String access_id, String weight_unit)` — `@Builder` constructor, lines 39–64
- **Fields:**
  - `private static final long serialVersionUID = 1250913872436247965L;` (line 11)
  - `private String id;` (line 13)
  - `private String name;` (line 14)
  - `private String location;` (line 15)
  - `private String department;` (line 16)
  - `private String type_id;` (line 17)
  - `private String type_nm;` (line 18)
  - `private String comp_id;` (line 19)
  - `private String active;` (line 20)
  - `private double size;` (line 21)
  - `private String manu_id;` (line 22)
  - `private String manu_name;` (line 23)
  - `private String fuel_type_id;` (line 24)
  - `private String fule_type_name;` (line 25)
  - `private double hourmeter;` (line 26)
  - `private String serial_no;` (line 27)
  - `private String acchours;` (line 28)
  - `private String mac_address;` (line 29)
  - `private String exp_mod;` (line 30)
  - `private boolean accessible;` (line 31)
  - `private String access_type;` (line 32)
  - `private KeypadReaderModel keypad_reader;` (line 33)
  - `private String facility_code;` (line 34)
  - `private String access_id;` (line 35)
  - `private String weight_unit;` (line 36)

---

## Findings

A59-1 | LOW | UnitAssignmentBean.java:14 | Field `id` uses primitive `int` while all other ID fields across beans use `String`. Inconsistency in ID type means a zero-value default exists and nullable semantics are lost; using `Integer` (boxed) would align with the rest of the model and allow null to represent "unset".

A59-2 | LOW | UnitAssignmentBean.java:15 | Field named `company_name` uses snake_case. Java convention is camelCase (`companyName`). All other field names in this class and sibling beans use camelCase or at least mixed conventions — snake_case here is inconsistent with the broader codebase style.

A59-3 | LOW | UnitBean.java:17,18,22,23,24,25,27,28,29,30,32,33,34,35,36 | Numerous fields use snake_case names (`type_id`, `type_nm`, `comp_id`, `manu_id`, `manu_name`, `fuel_type_id`, `fule_type_name`, `serial_no`, `acchours`, `mac_address`, `exp_mod`, `access_type`, `keypad_reader`, `facility_code`, `access_id`, `weight_unit`). Java naming conventions require camelCase for fields. This is a pervasive style inconsistency throughout `UnitBean`.

A59-4 | HIGH | UnitBean.java:25 | Field is named `fule_type_name` — this is a typo; it should be `fuel_type_name`. The corresponding constructor parameter on line 39 also uses `fule_type_name`, cementing the misspelling into the public Lombok-generated getter `getFule_type_name()` and any serialized JSON key, creating a silent API contract bug.

A59-5 | MEDIUM | UnitBean.java:20 | Field `active` is typed `String` ("Yes"/"No" or similar) rather than `boolean`/`Boolean`. The same pattern is applied to `UnitAssignmentBean.current` (line 18). Using strings for boolean state bypasses compile-time safety, requires callers to perform string comparisons, and is inconsistent with the `boolean accessible` field on line 31 of the same class, which correctly uses a primitive boolean.

A59-6 | LOW | UnitBean.java:28 | Field `acchours` is an abbreviated, non-descriptive name with no clear meaning from context (likely "accumulated hours"). Abbreviations of this kind hinder readability and maintainability.

A59-7 | LOW | UnitAssignmentBean.java:3 | `import lombok.Builder;` is present, but `@Builder` is applied only to the private constructor (line 20), not the class itself. This is an unusual pattern — the builder is private and cannot be invoked from outside the class without reflection. If the intent is to restrict direct construction, the design is valid but should be documented; if a usable builder was intended, the access modifier on the constructor is wrong. No comment or documentation explains the intent.

A59-8 | LOW | TimezoneBean.java:17,18,19 | Fields `id`, `name`, and `zone` are initialized to `""` (empty string) rather than `null`. This differs from the default initialization pattern used in `UnitBean` and `UnitAssignmentBean`, where fields default to `null`. The empty-string defaults can mask missing data (e.g., `id.isEmpty()` must be checked instead of `id == null`), creating inconsistency in null-checking patterns across beans.
# P4 Agent A60 — UnitFuelTypeBean, UnitTypeBean, UserBean

## Reading Evidence

### UnitFuelTypeBean.java

**Class:** `com.bean.UnitFuelTypeBean` (implements `Serializable`)

**Fields:**
- `private static final long serialVersionUID` — line 10
- `private String id` — line 12 (initialized to `null`)
- `private String name` — line 13 (initialized to `null`)

**Methods:**
- `getId()` — line 14
- `setId(String id)` — line 17
- `getName()` — line 20
- `setName(String name)` — line 23

---

### UnitTypeBean.java

**Class:** `com.bean.UnitTypeBean` (implements `Serializable`)

**Fields:**
- `private static final long serialVersionUID` — line 9
- `private String id` — line 10 (initialized to `""`)
- `private String name` — line 11 (initialized to `""`)

**Methods:**
- `getId()` — line 13
- `setId(String id)` — line 16
- `getName()` — line 19
- `setName(String name)` — line 22

---

### UserBean.java

**Class:** `com.bean.UserBean` (implements `Serializable`, annotated `@Data @NoArgsConstructor`)

**Fields:**
- `private static final long serialVersionUID` — line 18
- `private int iduser` — line 20
- `private String name` — line 21
- `private String email` — line 22
- `private String password` — line 23
- `private boolean enabled` — line 24
- `private String mobile` — line 25
- `private String first_name` — line 26
- `private String last_name` — line 27

**Methods:**
- `UserBean(int iduser, String name, String email, String password, boolean enabled, String mobile, String first_name, String last_name)` — line 30 (private `@Builder` constructor)
- *(All getters, setters, equals, hashCode, toString generated by Lombok `@Data`)*

---

## Findings

A60-1 | LOW | UnitFuelTypeBean.java:12-13 | Fields `id` and `name` are initialized to `null`. The structurally identical peer class `UnitTypeBean` initializes the same fields to `""`. This inconsistent field initialization convention across the two bean classes creates a style inconsistency and makes null-check behavior unpredictable for callers treating the two beans uniformly.

A60-2 | LOW | UnitTypeBean.java:24 | Trailing whitespace characters are present after the closing brace of `setName()` on line 24 (visible as extra spaces/tabs before the class-closing brace). Minor style issue; consistent with other beans in the package but worth noting.

A60-3 | MEDIUM | UserBean.java:26-27 | Field names `first_name` and `last_name` use snake_case, violating Java naming conventions (camelCase: `firstName`, `lastName`). All other fields in this class and in peer beans use camelCase. Lombok-generated accessor names will be `getFirst_name()` / `getLast_name()` which is non-standard and can cause unexpected behavior with frameworks that rely on JavaBeans naming conventions (e.g., Jackson, Spring MVC model binding).

A60-4 | LOW | UserBean.java:5 | Import `com.bean.CompanyBean.CompanyBeanBuilder` is unused. The class never references `CompanyBeanBuilder` anywhere in its body. This will produce a compile-time "unused import" warning.

A60-5 | LOW | UserBean.java:7 | Import `lombok.Builder` is imported and the annotation is used on the private constructor (line 29), but the `@Builder` annotation on a `private` constructor combined with `@NoArgsConstructor` and `@Data` is an unusual and fragile pattern. The builder is not publicly usable from outside the class in the normal Lombok builder idiom. This is not broken, but the intent is unclear and the pattern is non-idiomatic.

A60-6 | INFO | UserBean.java:41-45 | Multiple consecutive blank lines (lines 41-45) between the constructor and the class closing brace. Minor style issue; inconsistent with the compact style used in `UnitFuelTypeBean` and `UnitTypeBean`.
# P4 Agent A61 — UserCompRelBean, XmlBean

## Reading Evidence

### UserCompRelBean.java

**Class:** `com.bean.UserCompRelBean`

**Fields:**
- `private static final long serialVersionUID` — line 14
- `private String comp_id` — line 16
- `private String email` — line 17
- `private String timezone` — line 18
- `private String user_id` — line 19

**Methods:**
- `UserCompRelBean(String comp_id, String email, String timezone, String user_id)` (constructor, `@Builder`) — lines 22–27
- Getters/setters for all four fields generated by Lombok `@Data` (no explicit source lines)

**Annotations:** `@Data`, `@NoArgsConstructor` (class level); `@Builder` (constructor level)

**Implements:** `java.io.Serializable`

---

### XmlBean.java

**Class:** `com.bean.XmlBean`

**Fields:**
- `private String id` — line 4
- `private String name` — line 5

**Methods:**
- `getId()` — lines 6–8
- `setId(String id)` — lines 9–11
- `getName()` — lines 12–14
- `setName(String name)` — lines 15–17

**Annotations:** none

**Implements:** nothing

---

## Findings

A61-1 | LOW | UserCompRelBean.java:16-19 | Field names use `snake_case` (`comp_id`, `user_id`, `timezone`, `email`) rather than the Java convention of `camelCase`. Because Lombok `@Data` derives getter/setter names directly from the field names, the generated API becomes `getComp_id()` / `setComp_id()` etc., which is non-standard and inconsistent with the rest of the codebase's naming conventions.

A61-2 | LOW | UserCompRelBean.java:22 | `@Builder` is placed on the explicit all-args constructor rather than on the class. Placing `@Builder` on the class is the idiomatic Lombok usage and produces a cleaner API. The current placement is functionally equivalent but stylistically inconsistent with standard Lombok usage.

A61-3 | LOW | UserCompRelBean.java:29-33 | Five consecutive blank lines at the end of the class body (lines 29–33) serve no purpose and are a minor style inconsistency.

A61-4 | MEDIUM | XmlBean.java:3 | `XmlBean` does not implement `java.io.Serializable` and has no `serialVersionUID`. Beans used in persistence, remoting, or session contexts are expected to be serializable; the absence of `Serializable` is a potential build warning and a runtime risk if this class is ever serialized.

A61-5 | LOW | XmlBean.java:3 | `XmlBean` is a hand-written POJO with explicit getters and setters while the rest of the `com.bean` package uses Lombok (`@Data`, etc.). This stylistic inconsistency increases maintenance burden; adding `@Data` would bring the class in line with the package convention.
# P4 Agent A62 — CalibrationImpact, CalibrationJob

## Reading Evidence

### CalibrationImpact.java

**Class:** `CalibrationImpact` (package-private)
**Annotations:** `@Builder` (Lombok)

**Fields:**
| Field | Type | Line |
|-------|------|------|
| `value` | `int` | 9 |
| `time` | `Timestamp` | 10 |
| `sessionStart` | `Timestamp` | 11 |

**Methods:**
| Method | Signature | Lines |
|--------|-----------|-------|
| Constructor | `CalibrationImpact(int value, Timestamp time, Timestamp sessionStart)` | 13–17 |

---

### CalibrationJob.java

**Class:** `CalibrationJob` (public), implements `org.quartz.Job`

**Fields:** None.

**Methods:**
| Method | Signature | Lines |
|--------|-----------|-------|
| `execute` | `public void execute(JobExecutionContext jobExecutionContext)` | 11–13 |
| `calibrateAllUnits` | `public void calibrateAllUnits()` | 15–24 |

---

## Findings

A62-1 | MEDIUM | CalibrationImpact.java:8 | Class is package-private (`class CalibrationImpact`) but carries `@Builder`, which generates a public static builder class. The missing `public` modifier on the class itself is likely unintentional — the builder becomes publicly reachable from within the package but the enclosing class is not directly accessible outside it. This access-level inconsistency is a leaky abstraction.

A62-2 | MEDIUM | CalibrationImpact.java:9–11 | All three fields (`value`, `time`, `sessionStart`) have package-private (default) visibility with no `private` modifier and no accessor methods. Combined with `@Builder`, this means callers inside the package can both build and directly mutate the object, bypassing any encapsulation. Fields should be `private` (with `@Getter` if read access is needed externally).

A62-3 | LOW | CalibrationImpact.java:13–17 | `@Builder` is declared on the class, which causes Lombok to generate an all-args static factory. An explicit all-args constructor is also hand-written at lines 13–17. Lombok's `@Builder` will call this constructor, but the redundant manual constructor adds unnecessary boilerplate and creates a maintenance risk (if the field list changes, both the constructor and builder must be updated). Either remove the hand-written constructor and let Lombok generate it, or remove `@Builder` and use the constructor directly.

A62-4 | HIGH | CalibrationJob.java:12 | `Executors.newSingleThreadExecutor()` is called on every invocation of `execute()` without ever being shut down. Each Quartz trigger firing leaks an `ExecutorService` and its backing thread. Over time this will exhaust thread resources. The executor should be a long-lived instance (or the job should be rescheduled rather than spawning its own thread), and `shutdown()` must be called when no longer needed.

A62-5 | MEDIUM | CalibrationJob.java:22 | `e.printStackTrace()` is used for `SQLException` handling. This bypasses any configured logging framework (SLF4J/Log4j/etc.) that is present in the rest of the codebase, makes the stack trace unstructured and unsearchable in log aggregation systems, and silently swallows the error from the caller's perspective. A proper logger (e.g., `log.error("calibrateAllUnits failed", e)`) should be used instead.

A62-6 | MEDIUM | CalibrationJob.java:17–18 | Concrete implementation classes (`UnitCalibrationGetterInDatabase`, `UnitCalibrationEnderInDatabase`) are instantiated directly inside `calibrateAllUnits()` via `new`. This hard-codes infrastructure dependencies inside the job, making it impossible to test without a live database and violating the dependency-inversion principle. Dependencies should be injected (via constructor, Quartz `JobDataMap`, or a DI container).

A62-7 | LOW | CalibrationJob.java:6 | `import java.sql.SQLException` is used only because `calibrateAllUnits()` catches it. If the dependency-injection finding (A62-6) were addressed and the method signature changed, this import would become unused. Noted for completeness as a coupling smell tied to the direct instantiation issue.
# P4 Agent A63 — CalibrationJobScheduler, UnitCalibration

## Reading Evidence

### CalibrationJobScheduler.java

**Class:** `CalibrationJobScheduler` (implements `ServletContextListener`)

**Methods:**
| Method | Lines |
|--------|-------|
| `contextInitialized(ServletContextEvent)` | 16–33 |
| `contextDestroyed(ServletContextEvent)` | 36–38 |

**Fields/Constants:** None declared.

**Imports used:** `org.quartz.*`, `org.quartz.impl.StdSchedulerFactory`, `javax.servlet.ServletContextEvent`, `javax.servlet.ServletContextListener`, `javax.servlet.ServletException`, plus three static Quartz builder imports.

---

### UnitCalibration.java

**Class:** `UnitCalibration` (annotated `@Builder`, `@Getter`)

**Fields:**
| Field | Type | Line |
|-------|------|------|
| `unitId` | `long` (final) | 12 |
| `resetCalibrationDate` | `Timestamp` | 13 |
| `calibrationDate` | `Timestamp` | 14 |
| `threshold` | `int` | 15 |
| `impacts` | `List<Integer>` | 16 |

**Methods:**
| Method | Visibility | Lines |
|--------|-----------|-------|
| `UnitCalibration(long, Timestamp, Timestamp, int, List<Integer>)` | package-private | 18–28 |
| `isCalibrated()` | public | 30–34 |
| `unitCalibrationNeverReset()` | private | 36–38 |
| `unitCalibrationDateAndThresholdSet()` | private | 40–42 |
| `calibrationDone()` | private | 44–46 |
| `getCalculatedThreshold()` | package-private | 48–51 |
| `average()` | private | 53–57 |
| `standardDeviation(double)` | private | 59–63 |
| `calibrationPercentage()` | public | 65–69 |

---

## Findings

A63-1 | HIGH | CalibrationJobScheduler.java:31 | `e.printStackTrace()` used instead of a proper logger. Scheduler failures (e.g., misfire, configuration error) are silently swallowed after printing to stderr; there is no re-throw, no propagation to the container, and no way for the application to know that job scheduling failed. This should use a logging framework and either rethrow or fail fast.

A63-2 | HIGH | CalibrationJobScheduler.java:37 | `contextDestroyed` creates a `new ServletException("Application Stopped")` only to call `.printStackTrace()` on it. The exception is never thrown and serves no purpose — this is misleading dead-code abuse. `contextDestroyed` is the correct lifecycle hook to shut down the Quartz `Scheduler` (call `scheduler.shutdown()`), but no shutdown logic is present at all, leaking scheduler threads on undeploy.

A63-3 | MEDIUM | CalibrationJobScheduler.java:27 | Unnecessary cast: `new StdSchedulerFactory()` is assigned directly to a `SchedulerFactory` local via an explicit cast `((SchedulerFactory) new StdSchedulerFactory())`. `StdSchedulerFactory` already implements `SchedulerFactory`; the cast adds noise and hides the concrete type without benefit.

A63-4 | MEDIUM | CalibrationJobScheduler.java:27 | The `Scheduler` instance obtained in `contextInitialized` is a local variable. It is never stored in a field or the `ServletContext`, so it cannot be retrieved in `contextDestroyed` to call `scheduler.shutdown()`. This makes a clean shutdown impossible and guarantees a thread leak on webapp undeploy.

A63-5 | MEDIUM | UnitCalibration.java:48 | `getCalculatedThreshold()` is package-private (no access modifier). Given the `@Builder`/`@Getter` pattern and the other public/private members, the omission of an explicit access modifier appears unintentional and inconsistent. If this method is intended to be internal only, it should be explicitly `private`; if it is part of the public API it should be `public`.

A63-6 | MEDIUM | UnitCalibration.java:53–57 | `average()` and `standardDeviation()` (lines 59–63) do not guard against `impacts` being `null` or empty. If called when `impacts == null` or `impacts.isEmpty()`, `average()` will throw a `NullPointerException` or `ArithmeticException` (divide by zero). `getCalculatedThreshold()` (line 48) calls both without any null/empty check, making it a latent runtime failure path.

A63-7 | LOW | UnitCalibration.java:18 | The all-args constructor is package-private (no explicit access modifier). With `@Builder` present, Lombok generates its own builder that calls this constructor. The package-private visibility is likely intentional to force use of the builder, but it is not documented and is inconsistent with the omission of a visibility modifier on `getCalculatedThreshold()` (finding A63-5) — in one case the omission appears intentional, in the other it appears accidental, making the convention unclear.

A63-8 | LOW | UnitCalibration.java:68 | `calibrationPercentage()` uses the magic number `100` three times with two distinct semantic meanings: (1) the threshold count of impacts required for calibration completion, and (2) the maximum percentage value to return. These two uses happen to share the same numeric value but represent different domain concepts. The threshold count (`100`) should be extracted to a named constant (e.g., `CALIBRATION_SAMPLE_SIZE`) to separate the concepts and avoid confusion with the percentage ceiling.

A63-9 | LOW | UnitCalibration.java:13–15 | Fields `resetCalibrationDate`, `calibrationDate`, and `threshold` are declared non-final despite the class using `@Builder` and `@Getter` (no `@Setter`). They are only written in the constructor, so they are effectively immutable. Declaring them `final` would correctly express immutability and be consistent with `unitId` (line 12).
# P4 Agent A64 — UnitCalibrationEnder, UnitCalibrationEnderInDatabase

## Reading Evidence

### UnitCalibrationEnder.java

- **Type:** interface (package-private)
- **Package:** `com.calibration`
- **Fields/Constants:** none
- **Methods:**
  - `endCalibration(long unitId, int newThreshold) throws SQLException` — line 6

### UnitCalibrationEnderInDatabase.java

- **Type:** `public class` implementing `UnitCalibrationEnder`
- **Package:** `com.calibration`
- **Imports:** `com.util.DBUtil`, `java.sql.SQLException`
- **Fields/Constants:** none
- **Methods:**
  - `endCalibration(long unitId, int newThreshold) throws SQLException` (override) — lines 9–18

---

## Findings

A64-1 | LOW | UnitCalibrationEnder.java:5 | The interface has package-private visibility (no `public` modifier) while its sole implementation `UnitCalibrationEnderInDatabase` is `public`. This asymmetry means the interface cannot be referenced from outside the `com.calibration` package even though the implementation is publicly visible, making the abstraction effectively unusable as a type at the call site unless it is always used within the same package. If the interface is intended to be the stable contract that callers depend on, it should be declared `public` to match the visibility of its implementation.

A64-2 | LOW | UnitCalibrationEnderInDatabase.java:15 | `statement.setInt(1, newThreshold)` is called with an `int` parameter for `newThreshold`, but the SQL column `impact_threshold` may warrant a larger type depending on the schema. More importantly, the parameter order in the SQL string is `impact_threshold` (position 1) then `id` (position 2), and the binding order matches — however `unitId` is a `long` bound via `setLong` while the SQL placeholder uses position 2 for `WHERE id = ?`. This is correct but the mismatch between the method parameter type (`int newThreshold`) and any potential domain constraint is not validated before the DB call. This is a minor robustness observation with no immediate defect.

No further findings. The files contain no commented-out code, no dead code, no raw types, and no unchecked casts. The implementation is clean and minimal.
# P4 Agent A65 — UnitCalibrationGetter, UnitCalibrationGetterInDatabase

## Reading Evidence

### UnitCalibrationGetter.java
- **Type:** interface
- **Package:** com.calibration
- **Fields/Constants:** none
- **Methods:**
  - `getUnitsToCalibrate()` — line 7 — returns `List<UnitCalibration>`, throws `SQLException`
  - `getUnitCalibration(long unitId)` — line 8 — returns `UnitCalibration`, throws `SQLException`

### UnitCalibrationGetterInDatabase.java
- **Type:** class, implements `UnitCalibrationGetter`
- **Package:** com.calibration
- **Fields:**
  - `filter` — line 12 — `private final UnitCalibrationImpactFilter`
- **Methods:**
  - `UnitCalibrationGetterInDatabase()` — line 14 — constructor, no-arg
  - `getUnitsToCalibrate()` — line 19 — `@Override`, returns `List<UnitCalibration>`, throws `SQLException`
  - `getUnitCalibration(long unitId)` — line 32 — `@Override`, returns `UnitCalibration`, throws `SQLException`
  - `makeUnit(ResultSet result)` — line 41 — `private`, returns `UnitCalibration`, throws `SQLException`
  - `getImpactsForUnit(long unitId, Timestamp resetCalibrationDate)` — line 53 — `private`, returns `List<Integer>`, throws `SQLException`

---

## Findings

A65-1 | HIGH | UnitCalibrationGetter.java:7-8 | Leaky abstraction: the interface declares `throws SQLException` on both methods. `SQLException` is a JDBC-specific checked exception, tying every consumer of this interface to the SQL storage layer. Any caller — including those that know nothing about databases — must either catch or propagate `SQLException`. A storage-agnostic interface should declare a domain-level checked exception (or use unchecked exceptions) and let implementations translate JDBC exceptions.

A65-2 | MEDIUM | UnitCalibrationGetterInDatabase.java:38 | Returning `null` from `getUnitCalibration`: `.orElse(null)` silently converts an absent result into `null`. The interface return type is `UnitCalibration` (not `Optional<UnitCalibration>`), so callers receive no compile-time indication that null is possible and must perform defensive null checks that are easy to forget. The interface should either return `Optional<UnitCalibration>` or the implementation should throw a domain-level not-found exception.

A65-3 | MEDIUM | UnitCalibrationGetterInDatabase.java:41-51 | N+1 query pattern: `makeUnit` is used as a row-mapper callback inside `getUnitsToCalibrate`. For every row returned by the outer query, `makeUnit` calls `getImpactsForUnit` (line 49), which issues a second database query. When `getUnitsToCalibrate` returns N units, N+1 SQL statements are executed. This is a latent performance problem that will worsen as the unit table grows.

A65-4 | LOW | UnitCalibrationGetterInDatabase.java:14-16 | Hard-coded dependency: the constructor instantiates `UnitCalibrationImpactFilter` directly (`filter = new UnitCalibrationImpactFilter()`). The filter cannot be substituted — for testing or alternative implementations — without modifying this class. The filter should be injected via the constructor parameter to follow the dependency-inversion principle already implied by the `UnitCalibrationGetter` interface.

A65-5 | LOW | UnitCalibrationGetterInDatabase.java:5 | Unused import: `java.sql.Date` is imported but never referenced anywhere in the file. This is dead code and will produce a compiler/IDE warning.

A65-6 | LOW | UnitCalibrationGetterInDatabase.java:26-28 | No-op lambda passed as parameter setter: `getUnitsToCalibrate` passes `statement -> {}` (an empty lambda) to `DBUtil.queryForObjects` as the prepared-statement configurator. This is a silent no-op. If `DBUtil.queryForObjects` expects a non-trivial configurator it adds confusion; if no parameters are needed, the API design should provide an overload that omits the configurator argument. As written it is misleading boilerplate.
# P4 Agent A66 — UnitCalibrationImpactFilter, UnitCalibrationStarter

## Reading Evidence

### UnitCalibrationImpactFilter.java

**Class:** `UnitCalibrationImpactFilter` (package-private, package `com.calibration`)

**Methods:**

| Method | Visibility | Lines |
|---|---|---|
| `filterImpacts(List<CalibrationImpact> impacts)` | package-private | 6–14 |
| `splitImpactsBy15MinutesOfSession(List<CalibrationImpact> impacts)` | private | 16–43 |
| `compareImpacts(CalibrationImpact i1, CalibrationImpact i2)` | private | 45–48 |
| `getLargestImpact(List<Integer> impacts)` | private | 50–56 |

**Fields / Constants:** None defined. Magic number `80000` appears inline at line 11 with no constant declaration.

---

### UnitCalibrationStarter.java

**Interface:** `UnitCalibrationStarter` (public, package `com.calibration`)

**Methods:**

| Method | Visibility | Lines |
|---|---|---|
| `startCalibration(long unitId) throws SQLException` | public abstract | 6 |

**Fields / Constants:** None.

---

## Findings

A66-1 | HIGH | UnitCalibrationImpactFilter.java:46 | Reference equality (`!=`) used to compare two `Date` objects. `i1.sessionStart != i2.sessionStart` tests object identity, not value equality. Two distinct `Date` instances representing the same point in time will compare as not-equal, causing the sort comparator to treat same-session impacts as belonging to different sessions and producing incorrect section splits. Should use `!i1.sessionStart.equals(i2.sessionStart)` or `i1.sessionStart.compareTo(i2.sessionStart) != 0`.

A66-2 | MEDIUM | UnitCalibrationStarter.java:6 | Leaky abstraction: the interface `UnitCalibrationStarter` is an application-layer contract but declares `throws SQLException`, a JDBC implementation detail. Callers of this interface are forced to handle or propagate a persistence-layer exception, coupling them to the SQL storage implementation. The checked exception should be wrapped in an unchecked application exception (e.g. `RuntimeException` subclass) either at the interface boundary or within implementing classes.

A66-3 | MEDIUM | UnitCalibrationImpactFilter.java:33–38 | Sliding-window logic drift: when an impact falls after `sectionEnd`, the code advances `sectionEnd` by 15 minutes (`sectionEnd.add(Calendar.MINUTE, 15)`) relative to the previous section end rather than resetting from the current impact's time. If there is a gap larger than 15 minutes between impacts, the new section end is placed in the past relative to the triggering impact, meaning all subsequent impacts in that gap will each create their own solo section instead of being grouped correctly. The section end should be recalculated from the current impact's time.

A66-4 | MEDIUM | UnitCalibrationImpactFilter.java:20 | Sentinel initialisation with `new Date()`: `sessionStart` is initialised to the current wall-clock time and then compared against `impact.sessionStart` to detect a new session. This relies on the assumption that no real `CalibrationImpact` has a `sessionStart` equal to the exact moment of object construction, which is a fragile and opaque convention. A cleaner sentinel would be `null` with an explicit null-check, making the intent clear.

A66-5 | LOW | UnitCalibrationImpactFilter.java:11 | Magic number: the threshold value `80000` is used inline without a named constant. This makes the business rule opaque and difficult to locate if the threshold needs to change.

A66-6 | LOW | UnitCalibrationImpactFilter.java:3 | Wildcard import `import java.util.*` is a style violation. Explicit imports should be used to make dependencies clear and to avoid potential future name collisions.

A66-7 | LOW | UnitCalibrationImpactFilter.java:50–55 | `getLargestImpact` returns `Integer` (boxed) and initialises `largest` to the boxed literal `0`. An empty list returns `0`, which is indistinguishable from a list containing only a zero-valued impact. Returning `Optional<Integer>` or using `int` with explicit empty-list handling would be clearer. The unnecessary boxing also triggers repeated auto-boxing/unboxing inside the loop.

A66-8 | LOW | UnitCalibrationImpactFilter.java:5 | Class `UnitCalibrationImpactFilter` has package-private visibility with no accompanying Javadoc or annotation explaining why it is not `public`. If intentionally package-scoped this should be documented; if unintentional, the modifier should be added.

A66-9 | INFO | UnitCalibrationImpactFilter.java:22,40 | `currentSection` is initialised to `null` at line 22 and accessed via `Objects.requireNonNull(currentSection)` at line 40. The `requireNonNull` call throws `NullPointerException` with no message if the null path is reached, providing no diagnostic context. If this state should never occur a meaningful `IllegalStateException` with a descriptive message would be preferable.
# P4 Agent A67 — UnitCalibrationStarterInDatabase, UnitCalibrator

## Reading Evidence

### UnitCalibrationStarterInDatabase.java

**Class:** `UnitCalibrationStarterInDatabase` (public, implements `UnitCalibrationStarter`)

**Fields/Constants:** None

**Methods:**
| Method | Lines | Access |
|---|---|---|
| `startCalibration(long unitId)` | 9–16 | public |

**Notes:** Single-method implementation class. Executes a SQL UPDATE via `DBUtil.updateObject`, resetting `impact_threshold`, `alert_enabled`, `reset_calibration_date`, and nulling `calibration_date` for the given unit ID.

---

### UnitCalibrator.java

**Class:** `UnitCalibrator` (package-private)

**Fields/Constants:**
| Name | Type | Access | Line |
|---|---|---|---|
| `unitCalibrationGetter` | `UnitCalibrationGetter` | private final | 7 |
| `unitCalibrationEnder` | `UnitCalibrationEnder` | private final | 8 |

**Methods:**
| Method | Lines | Access |
|---|---|---|
| `UnitCalibrator(UnitCalibrationGetter, UnitCalibrationEnder)` | 10–14 | package-private |
| `calibrateAllUnits()` | 16–20 | package-private |
| `calibrateUnit(UnitCalibration)` | 22–26 | private |

---

## Findings

A67-1 | LOW | UnitCalibrator.java:18–19 | The enhanced-for loop body on line 19 (`calibrateUnit(unitCalibration)`) omits braces. Java style guides (Google, Oracle) require braces on all block statements even for single-line bodies to guard against future edit errors. `calibrateAllUnits` is the only place this occurs; the pattern is not consistently brace-free elsewhere in the file, so it is an inconsistency rather than a deliberate style choice.

A67-2 | INFO | UnitCalibrator.java:6 | `UnitCalibrator` is package-private (no access modifier on the class declaration). If the class is intentionally package-scoped this is fine, but it is inconsistent with `UnitCalibrationStarterInDatabase`, which is `public`. If `UnitCalibrator` is meant to be consumed only within the `com.calibration` package the visibility should be documented or confirmed; if it is meant to be a public API component the modifier is missing.

A67-3 | INFO | UnitCalibrator.java:10–14 | The constructor is package-private (no access modifier). Same observation as A67-2: confirm intentional package-scoping. If a public factory or service class outside the package needs to instantiate `UnitCalibrator`, this will silently prevent it.
# P4 Agent A68 — AuthenticationRequest, AuthenticationResponse, PasswordRequest

## Reading Evidence

### AuthenticationRequest.java

- **Class:** `AuthenticationRequest` (line 12)
- **Implements:** `java.io.Serializable`
- **Annotations:** `@Data`, `@NoArgsConstructor`
- **Fields:**
  - `serialVersionUID` : `long` (line 17)
  - `username` : `String` (line 18)
  - `password` : `String` (line 19)
  - `newPassword` : `String` (line 20)
  - `accessToken` : `String` (line 21)
- **Methods:**
  - `AuthenticationRequest(String username, String password, String newPassword, String accessToken)` — `@Builder` private constructor (lines 24–29)
  - Getters/setters/equals/hashCode/toString generated by Lombok `@Data`
  - Default no-arg constructor generated by Lombok `@NoArgsConstructor`

---

### AuthenticationResponse.java

- **Class:** `AuthenticationResponse` (line 12)
- **Does NOT implement:** `Serializable`
- **Annotations:** `@Data`, `@NoArgsConstructor`, `@JsonInclude(JsonInclude.Include.NON_NULL)`
- **Fields:**
  - `serialVersionUID` : `long` (line 16)
  - `accessToken` : `String` (line 17)
  - `sessionToken` : `String` (line 18)
  - `expiresIn` : `String` (line 19)
  - `actualDate` : `String` (line 20)
  - `expirationDate` : `String` (line 21)
  - `userData` : `UserResponse` (line 22)
  - `username` : `String` (line 23)
  - `message` : `String` (line 24)
  - `code` : `Integer` (line 25)
  - `detail` : `String` (line 26)
- **Methods:**
  - No explicit constructors or methods; all generated by Lombok `@Data` / `@NoArgsConstructor`

---

### PasswordRequest.java

- **Class:** `PasswordRequest` (line 11)
- **Implements:** `java.io.Serializable`
- **Annotations:** `@Data`, `@NoArgsConstructor`
- **Fields:**
  - `serialVersionUID` : `long` (line 15)
  - `username` : `String` (line 17)
  - `password` : `String` (line 18)
  - `confirmationCode` : `String` (line 19)
  - `oldPassword` : `String` (line 20)
  - `accessToken` : `String` (line 21)
- **Methods:**
  - `PasswordRequest(String username, String password, String confirmationCode, String oldPassword, String accessToken)` — `@Builder` private constructor (lines 24–31)
  - Getters/setters/equals/hashCode/toString generated by Lombok `@Data`
  - Default no-arg constructor generated by Lombok `@NoArgsConstructor`

---

## Findings

A68-1 | HIGH | AuthenticationResponse.java:12 | Class declares `serialVersionUID` (line 16) but does NOT implement `java.io.Serializable`. The `serialVersionUID` field has no effect and is misleading. The other two beans in this package (`AuthenticationRequest`, `PasswordRequest`) both implement `Serializable`, making this an inconsistency across the package. Either `Serializable` should be added to `AuthenticationResponse` or the orphaned `serialVersionUID` field should be removed.

A68-2 | LOW | AuthenticationRequest.java:14-16 | The Javadoc comment on `serialVersionUID` is an IDE-generated stub (`/** \n * \n */`) with no meaningful content. Identical empty stubs appear in `AuthenticationResponse.java:13-15` and `PasswordRequest.java:12-14`. These add noise without value and are a style inconsistency against files that omit such comments entirely.

A68-3 | LOW | AuthenticationRequest.java (mixed indentation) | The file mixes tab and space indentation. Fields at lines 18-21 use 4-space indentation while the constructor body at lines 25-28 uses a tab. `PasswordRequest.java` has the same mixed-indentation pattern. `AuthenticationResponse.java` is consistently tab-indented throughout. This is a style inconsistency across the package.

A68-4 | LOW | AuthenticationResponse.java:19 | Field `expiresIn` is typed as `String` but its name implies a duration/numeric value. The companion field `expirationDate` (line 21) is also `String`. Having both a duration field (`expiresIn`) and an absolute date field (`expirationDate`) with no apparent accessor differentiation is a latent design ambiguity; callers must know which to populate and there is no validation enforcing mutual exclusion or correct population.

A68-5 | INFO | AuthenticationResponse.java:20 | Field `actualDate` has an unclear semantic meaning relative to `expirationDate` (line 21). No documentation distinguishes what "actual date" refers to (issue date? server date? token creation date?). This is a naming clarity issue that could cause incorrect usage by callers.
# P4 Agent A69 — PasswordResponse, UserRequest, UserResponse

## Reading Evidence

### PasswordResponse.java
- **Class**: `PasswordResponse` (public, no interface implementation)
- **Annotations**: `@Data`, `@NoArgsConstructor`, `@JsonInclude(JsonInclude.Include.NON_NULL)`
- **Fields**:
  - Line 17: `private static final long serialVersionUID = -8677893765042629588L`
  - Line 18: `private String destination`
  - Line 19: `private String deliveryMedium`
  - Line 20: `private String message`
  - Line 21: `private String username`
  - Line 22: `private Integer code`
  - Line 23: `private String detail`
- **Methods**: None declared explicitly; Lombok `@Data` generates getters/setters/toString/equals/hashCode; `@NoArgsConstructor` generates no-arg constructor.

---

### UserRequest.java
- **Class**: `UserRequest` (public, implements `Serializable`)
- **Annotations**: `@Data`, `@NoArgsConstructor`
- **Fields**:
  - Line 16: `private static final long serialVersionUID = 126101017809040672L`
  - Line 17: `private String accessToken`
  - Line 18: `private String username`
- **Methods**:
  - Line 21–24: `private UserRequest(String accessToken, String username)` — annotated `@Builder`; assigns both fields.

---

### UserResponse.java
- **Class**: `UserResponse` (public, implements `Serializable`)
- **Annotations**: `@Data`, `@NoArgsConstructor`, `@JsonInclude(JsonInclude.Include.NON_NULL)`
- **Fields**:
  - Line 19: `private static final long serialVersionUID = 894041507646078302L`
  - Line 20: `private String username`
  - Line 21: `private String email`
  - Line 22: `private String userCreateDate`
  - Line 23: `private String userStatus`
  - Line 24: `private String lastModifiedDate`
  - Line 25: `private String name`
  - Line 26: `private String lastname`
  - Line 27: `private String phoneNumber`
  - Line 28: `private Integer code`
  - Line 29: `private String message`
  - Line 30: `private String detail`
- **Methods**: None declared explicitly; Lombok `@Data` generates getters/setters/toString/equals/hashCode; `@NoArgsConstructor` generates no-arg constructor.

---

## Findings

A69-1 | HIGH | PasswordResponse.java:12,17 | `PasswordResponse` declares `serialVersionUID` but does not implement `Serializable`. The field is unreachable by the serialization mechanism and silently unused. Either implement `java.io.Serializable` (consistent with `UserRequest` and `UserResponse`) or remove the field entirely.

A69-2 | MEDIUM | UserRequest.java:20–24 | `@Builder` is placed on a `private` all-args constructor rather than on the class. This is an unusual pattern: the generated builder is accessible but the constructor itself is private. It also conflicts with `@NoArgsConstructor` + `@Data` because Lombok's `@Data`-generated `toString`/`equals` work fine, but the presence of a manually written all-args constructor means `@Data` does not generate one, leaving the builder as the only way to construct a fully-initialised instance. The intent appears to be a builder-only construction idiom, but it should be documented or replaced with `@Builder` at the class level alongside `@AllArgsConstructor` for clarity and consistency with `UserResponse`.

A69-3 | MEDIUM | PasswordResponse.java:14–16 | Empty Javadoc block (`/** \n * \n */`) above `serialVersionUID` — auto-generated stub that was never completed. Same pattern appears in `UserRequest.java:13–15` and `UserResponse.java:17–19`. These empty comment blocks add noise without value.

A69-4 | LOW | PasswordResponse.java (class-level) | `PasswordResponse` does not implement `Serializable`, yet the other two beans in the same package (`UserRequest`, `UserResponse`) do. This is a style inconsistency across the Cognito bean package: all three serve as response/request transport objects and should have a uniform contract for serialisability.

A69-5 | LOW | UserResponse.java:26 | Field `lastname` uses a different capitalisation convention from the rest of the codebase. Java naming conventions and the field `phoneNumber` (camelCase with two words) both suggest this should be `lastName`. The inconsistency may cause unexpected JSON key naming (`"lastname"` vs the likely intended `"lastName"`) when the class is serialised.

A69-6 | LOW | UserResponse.java:22,24 | Fields `userCreateDate` and `lastModifiedDate` are typed as `String` rather than `java.time.LocalDateTime` or `java.util.Date`. Date-as-String is a recognised code-smell that eliminates type safety, makes format validation impossible at the model layer, and is inconsistent with Java best practices. This is an INFO-level design observation but warrants LOW severity because it increases the risk of silent format mismatches at runtime.
# P4 Agent A70 — UserSignUpRequest, UserSignUpResponse

## Reading Evidence

### UserSignUpRequest.java
- **Class**: `com.cognito.bean.UserSignUpRequest`
- **Implements**: `java.io.Serializable`
- **Annotations**: `@Data`, `@NoArgsConstructor`
- **Fields**:
  - `serialVersionUID` (long, static final) — line 18
  - `username` (String) — line 19
  - `password` (String) — line 20
  - `email` (String) — line 21
  - `name` (String) — line 22
  - `lastname` (String) — line 23
  - `phoneNumber` (String) — line 24
  - `givenName` (String) — line 25
- **Methods**:
  - `UserSignUpRequest(String username, String password, String email, String name, String lastname, String phoneNumber, String givenName)` — private all-args constructor annotated `@Builder`, lines 28–38; calls `super()`

---

### UserSignUpResponse.java
- **Class**: `com.cognito.bean.UserSignUpResponse`
- **Does NOT implement**: `java.io.Serializable` (field `serialVersionUID` declared but interface not declared)
- **Annotations**: `@Data`, `@NoArgsConstructor`, `@JsonInclude(JsonInclude.Include.NON_NULL)`
- **Fields**:
  - `serialVersionUID` (long, static final) — line 17
  - `username` (String) — line 18
  - `userCreatedDate` (String) — line 19
  - `lastModifiedDate` (String) — line 20
  - `enabled` (boolean) — line 21
  - `userStatus` (String) — line 22
  - `password` (String) — line 23
  - `email` (String) — line 24
  - `brokerID` (String) — line 25
  - `code` (Integer) — line 26
  - `message` (String) — line 27
  - `detail` (String) — line 28
- **Methods**: none (pure data class)

---

## Findings

A70-1 | HIGH | UserSignUpResponse.java:17 | `serialVersionUID` is declared but the class does not `implement Serializable`. The field is therefore a plain instance-visible long named `serialVersionUID` rather than the JVM serialization constant — it has no effect, will produce a compiler warning about the unused field, and is misleading. All other Response beans in the package that declare this field also omit `Serializable` (`AuthenticationResponse`, `UserUpdateResponse`), making this a systemic pattern, but it is still incorrect. Compare `UserResponse` (line 14) and `UserSignUpRequest` (line 13) which correctly declare `implements Serializable`.

A70-2 | MEDIUM | UserSignUpRequest.java:5 | Unused import `com.cognito.bean.UserRequest.UserRequestBuilder`. `UserSignUpRequest` uses its own `@Builder`-generated inner builder; the `UserRequestBuilder` import is never referenced in the file and will produce a compiler warning.

A70-3 | MEDIUM | UserSignUpRequest.java:28–38 | The `@Builder`-annotated private constructor includes a redundant `super()` call (line 30). No other builder constructor in the package (`AuthenticationRequest`, `UserRequest`) calls `super()`. This is a minor style inconsistency and is noise since `Object` default constructor is always called implicitly, but it signals a copy-paste difference from the established pattern.

A70-4 | LOW | UserSignUpRequest.java:13 | Missing space before `{` in `implements Serializable{`. Every other bean in the package that declares `implements Serializable` (`AuthenticationRequest` line 12, `UserRequest` line 11, `UserResponse` line 14) uses a space before the opening brace. Minor style inconsistency.

A70-5 | LOW | UserSignUpResponse.java:19 | Field name `userCreatedDate` does not match the naming convention used in the sibling `UserResponse` bean, which names the equivalent field `userCreateDate` (line 22 of UserResponse.java). This divergence means the two response types use different field names for the same logical attribute, complicating any code that maps or compares the two.

A70-6 | LOW | UserSignUpResponse.java:23 | `password` is exposed as a response field. Returning a password — even a temporary one — in a sign-up response is a security-hygiene concern; no other Response bean in the package (`AuthenticationResponse`, `UserResponse`, `UserUpdateResponse`) exposes a `password` field. This should be reviewed to confirm whether it is intentional (e.g., returning a generated temporary password) or an oversight.

A70-7 | INFO | UserSignUpRequest.java:25 | Field `givenName` (camelCase) is a semantic duplicate of `name` (line 22). Cognito's user pool standard attributes map `given_name` and `name` to distinct attributes, so both may be intentional, but the overlap warrants a comment or documentation to prevent future confusion. Note also that `UserUpdateRequest` stores the same concept as `given_name` (snake_case), further inconsistency across beans.
# P4 Agent A71 — UserUpdateRequest, UserUpdateResponse

## Reading Evidence

### UserUpdateRequest.java
- **Class:** `com.cognito.bean.UserUpdateRequest`
- **Annotations:** `@Data`, `@NoArgsConstructor`
- **Fields (lines 11–17):**
  - `String username` (line 11)
  - `String email` (line 12)
  - `String given_name` (line 13)
  - `String family_name` (line 14)
  - `String phone_number` (line 15)
  - `String password` (line 16)
  - `String accessToken` (line 17)
- **Methods:**
  - `UserUpdateRequest(String username, String email, String given_name, String family_name, String phone_number, String password, String accessToken)` — private `@Builder` constructor, lines 20–28
- **No `serialVersionUID`**
- **Does not implement `Serializable`**
- **Unused import:** `import lombok.Builder` is used (on constructor); however the class-level `@Builder` is absent — `@Builder` is placed on the private constructor directly, which is valid but unusual.

### UserUpdateResponse.java
- **Class:** `com.cognito.bean.UserUpdateResponse`
- **Annotations:** `@Data`, `@NoArgsConstructor`, `@JsonInclude(JsonInclude.Include.NON_NULL)`
- **Fields (lines 13–20):**
  - `String username` (line 13)
  - `String email` (line 14)
  - `String given_name` (line 15)
  - `String family_name` (line 16)
  - `String phone_number` (line 17)
  - `Integer code` (line 18)
  - `String message` (line 19)
  - `String detail` (line 20)
- **Methods:** None (Lombok-generated only)
- **No `serialVersionUID`**
- **Does not implement `Serializable`**

---

## Findings

A71-1 | MEDIUM | UserUpdateRequest.java:9 | Missing `implements Serializable` and `serialVersionUID`. Every other request bean in this package that uses `@Builder` (`UserRequest`, `UserSignUpRequest`, `AuthenticationRequest`, `PasswordRequest`) implements `Serializable` and declares a `serialVersionUID`. `UserUpdateRequest` is the only request bean that omits both, creating an inconsistency and a potential build warning from tools that enforce serialisation hygiene.

A71-2 | MEDIUM | UserUpdateResponse.java:11 | Missing `implements Serializable` and `serialVersionUID`. The sibling response beans `UserResponse`, `AuthenticationResponse`, `PasswordResponse`, and `UserSignUpResponse` all declare a `serialVersionUID` field (even those that do not explicitly implement `Serializable`, they still carry the field). `UserUpdateResponse` omits it entirely, which is inconsistent with the rest of the package and will produce a compiler/IDE warning if serialisation checks are enabled.

A71-3 | LOW | UserUpdateRequest.java:13–15 | Field names `given_name`, `family_name`, and `phone_number` use snake_case, violating the Java naming convention and the camelCase style used in every other bean in this package (e.g., `UserSignUpRequest` uses `givenName`, `phoneNumber`; `UserResponse` uses `phoneNumber`). This inconsistency likely exists because the field names must match Cognito API attribute names, but without `@JsonProperty` annotations to make the mapping explicit, the intent is obscured and the class surface exposes non-idiomatic Java field names via Lombok-generated getters (`getGiven_name()`, etc.).

A71-4 | LOW | UserUpdateResponse.java:15–17 | Same snake_case naming issue as A71-3 applies to `given_name`, `family_name`, and `phone_number` on the response side. These fields are never populated in the callers observed (`CompanyDAO`, `DriverDAO` only inspect `.getCode()`), and no `@JsonProperty` annotations are present to clarify the serialisation mapping.

A71-5 | LOW | UserUpdateRequest.java:3 | `import lombok.Builder` is present and is used (on the private constructor at line 19), which is correct. However, the class does not declare `@Builder` at the class level as the other builder-pattern beans do (`UserSignUpRequest`, `UserRequest`, `AuthenticationRequest`, `PasswordRequest`). Placing `@Builder` directly on a private constructor is a valid but non-standard pattern within this codebase, reducing readability consistency without clear documentation of the intent.

A71-6 | INFO | UserUpdateResponse.java:11 | Trailing whitespace on the class declaration line (`public class UserUpdateResponse {   ` — tab after brace). Minor style artefact, inconsistent with other response classes in the package.
# P4 Agent A72 — AdvertismentDAO, CompanyDAO

## Reading Evidence

### AdvertismentDAO.java

**Class name:** `AdvertismentDAO`

**Fields / constants:**
| Name | Type | Line |
|------|------|------|
| `log` | `private static Logger` | 18 |
| `instance` | `private static AdvertismentDAO` | 20 |

**Methods:**
| Method signature | Lines |
|-----------------|-------|
| `public static AdvertismentDAO getInstance()` | 22–31 |
| `private AdvertismentDAO()` | 33–35 |
| `public ArrayList<AdvertisementBean> getAllAdvertisement() throws Exception` | 37–75 |
| `public ArrayList<AdvertisementBean> getAdvertisementById(String id) throws Exception` | 77–117 |
| `public Boolean delAdvertisementById(String id) throws Exception` | 119–146 |
| `public boolean saveAdvertisement(AdvertisementBean advertisementBean) throws Exception` | 149–203 |
| `public boolean updateAdvertisement(AdvertisementBean advertisementBean) throws Exception` | 206–262 |

---

### CompanyDAO.java

**Class name:** `CompanyDAO`

**Fields / constants:**
| Name | Type | Line |
|------|------|------|
| `log` | `private static Logger` | 36 |
| `QUERY_USR_RPT` | `private static final String` | 38 |
| `QUERY_USR_ALERT` | `private static final String` | 40 |
| `QUERY_ALERT_LST` | `private static final String` | 42 |
| `QUERY_REPORT_LST` | `private static final String` | 44 |
| `SAVE_USER_ROLE` | `private static final String` | 46–48 |
| `UPDATE_COMPANY_ROLE` | `private static final String` | 50–54 |
| `SAVE_COMPANY_DEALER_ROLE` | `private static final String` | 56–58 |
| `SAVE_USERS` | `private static final String` | 60–61 |
| `SAVE_COGNITO_USERS` | `private static final String` | 63–64 |
| `SAVE_USERS_COMP_REL` | `private static final String` | 66–67 |
| `SAVE_COMPANY_ROLE` | `private static final String` | 69–71 |
| `SAVE_COMP` | `private static final String` | 73 |
| `QUERY_SUBCOMPANYLST_BY_ID` | `private static final String` | 75–79 |
| `QUERY_COMPANY_BY_ID` | `private static final String` | 81–85 |
| `QUERY_SUBCOMPANY_BY_ID` | `private static final String` | 87 |
| `QUERY_COMPANY_USR_BY_ID` | `private static final String` | 89–93 |
| `UPDATE_USR_PIN` | `private static final String` | 95 |
| `UPDATE_USR_INFO` | `private static final String` | 97 |
| `UPDATE_COMPANY` | `private static final String` | 99 |
| `UPDATE_COMP_INFO_UPDATE_SETTINGS` | `private static final String` | 101 |
| `QUERY_USR_ALERT_BY_TYPE` | `private static final String` | 103 |
| `COGNITO_USERNAME_BY_ID` | `private static final String` | 105 |
| `theInstance` | `private static CompanyDAO` | 107 |
| `QUERY_COUNT_USR_ALERT_BY_TYPE` | `private static final String` | 924 |

**Methods:**
| Method signature | Lines |
|-----------------|-------|
| `public synchronized static CompanyDAO getInstance()` | 109–115 |
| `private CompanyDAO()` | 117–118 |
| `public int saveCompInfo(CompanyBean compbean, String Role) throws Exception` | 122–149 |
| `public void saveUserRoles(int userId, String role) throws Exception` | 153–159 |
| `public int saveSubCompInfo(String sessCompId, CompanyBean compbean) throws Exception` | 161–175 |
| `public static List<CompanyBean> getSubCompanies(String companyId) throws Exception` | 177–199 |
| `public String getSubCompanyLst(String companyId) throws Exception` | 201–220 |
| `private List<RoleBean> GetCompanyRoles(long companyId) throws SQLException` | 222–233 |
| `public void saveUsers(int compId, UserBean userBean) throws Exception` | 239–265 |
| `public void savePermission(int driver_id, int compId) throws Exception` | 267–294 |
| `private void saveDefaultEmails(int driver_id) throws Exception` | 296–324 |
| `private void saveCompanyRoles(int companyId, String role) throws Exception` | 328–334 |
| `public void updateCompPrivacy(String compId) throws Exception` | 336–355 |
| `public boolean checkExist(String name, String dbField, String compId) throws Exception` | 357–380 |
| `public int checkUserExit(String name, String dbField, String id) throws Exception` | 382–394 |
| `public String checkCompExist(CompanyBean companyBean) throws Exception` | 396–433 |
| `public boolean resetPass(String compId, String pass) throws Exception` | 435–459 |
| `public String getCompLogo(String compId) throws Exception` | 461–486 |
| `public CompanyBean getCompanyById(String companyId) throws Exception` | 488–519 |
| `public List<CompanyBean> getCompanyByCompId(String id) throws SQLException` | 521–556 |
| `public List<CompanyBean> getCompanyContactsByCompId(String compId, int usrId, String sessionToken) throws SQLException` | 558–592 |
| `public UserUpdateResponse updateCompInfo(CompanyBean compBean, int usrId, String accessToken) throws Exception` | 594–628 |
| `public boolean updateCompSettings(CompanyBean compBean) throws Exception` | 632–653 |
| `public ArrayList<CompanyBean> getEntityComp(String entityId) throws Exception` | 655–688 |
| `public ArrayList<EntityBean> getEntityByQuestion(String qId, String type) throws Exception` | 690–720 |
| `public ArrayList<EntityBean> getAllEntity() throws Exception` | 722–768 |
| `public ArrayList<CompanyBean> getAllCompany() throws SQLException` | 770–811 |
| `public static List<AlertBean> getAlertList() throws Exception` | 813–826 |
| `public void convertCompanyToDealer(String companyId) throws Exception` | 830–845 |
| `public static List<AlertBean> getReportList() throws Exception` | 847–860 |
| `public static void addUserSubscription(String userId, String alertId) throws Exception` | 862–869 |
| `public static void deleteUserSubscription(String userId, String alertId) throws Exception` | 871–878 |
| `public List<AlertBean> getUserAlert(String id) throws Exception` | 880–892 |
| `public AlertBean getUserAlert(String id, String type, String file_name) throws SQLException` | 895–909 |
| `public List<AlertBean> getUserReport(String id) throws Exception` | 911–922 |
| `public boolean checkExistingUserAlertByType(String userId, String type) throws Exception` | 925–931 |
| `public int getCompanyMaxId() throws Exception` | 933–939 |
| `public int getUserMaxId() throws Exception` | 942–948 |

---

## Findings

A72-1 | HIGH | AdvertismentDAO.java:16 | **Class name typo — "Advertisment" missing a letter.** The class is named `AdvertismentDAO` (one 't') instead of `AdvertisementDAO`. This typo propagates to the singleton field (line 20), the logger category (line 18), the `getInstance()` method (lines 22–31), the constructor (line 33), and the bean class import contrast (`AdvertisementBean` on line 12 is spelled correctly). Any caller that uses the class name must perpetuate the misspelling, making future refactoring risky.

A72-2 | HIGH | AdvertismentDAO.java:91 | **SQL injection — `getAdvertisementById` uses string concatenation with an untrusted parameter.** The `id` value passed by the caller is concatenated directly into the query: `"select ... where id = " + id`. A `Statement` is used instead of a `PreparedStatement`, leaving the query open to SQL injection. The same pattern appears in `delAdvertisementById` (line 131).

A72-3 | HIGH | AdvertismentDAO.java:131 | **SQL injection — `delAdvertisementById` uses string concatenation with an untrusted parameter.** `"delete from advertisment where id=" + id` is executed via a plain `Statement`. No parameterised binding is used.

A72-4 | HIGH | CompanyDAO.java:367–369 | **SQL injection — `checkExist` concatenates the `dbField` column name and the `name` value directly into SQL.** `dbField` is a caller-supplied column name that cannot be parameterised by `PreparedStatement`, but `name` absolutely can and is not. The construction `"select id from company where " + dbField + " ='" + name + "'"` (and the appended `compId` on line 369) is injectable.

A72-5 | HIGH | CompanyDAO.java:385–386 | **SQL injection — `checkUserExit` concatenates caller-supplied `dbField` and `name` directly into SQL** using the same pattern as `checkExist`. No use of `PreparedStatement` for the user-supplied values.

A72-6 | HIGH | CompanyDAO.java:408–418 | **SQL injection — `checkCompExist` concatenates `companyBean.getName()`, `companyBean.getEmail()`, `companyBean.getQuestion()`, and `companyBean.getAnswer()` directly into SQL strings** using a plain `Statement`. All four fields are user-supplied and unescaped.

A72-7 | HIGH | CompanyDAO.java:471 | **SQL injection — `getCompLogo` concatenates `compId` directly into SQL.** `"select logo from company where id = " + compId` is executed through a plain `Statement`.

A72-8 | HIGH | CompanyDAO.java:670 | **SQL injection — `getEntityComp` concatenates `entityId` directly into SQL.** `sql += " where comp_entity_rel.entity_id = " + entityId` is appended without parameterisation.

A72-9 | HIGH | CompanyDAO.java:702 | **SQL injection — `getEntityByQuestion` concatenates both `qId` and `type` directly into SQL.** The query string is built with `+ qId + " and type= '" + type + "'"` using a plain `Statement`.

A72-10 | HIGH | CompanyDAO.java:745 | **SQL injection — `getAllEntity` concatenates `rs.getString(1)` (an entity ID from the outer query) directly into an inner SQL query** executed via a second plain `Statement` (`stm`). Even though this is a DB-sourced value, it is unparameterised and represents an N+1 query problem as well as a SQL injection risk if the entity table is ever populated via untrusted input.

A72-11 | MEDIUM | AdvertismentDAO.java:129 | **`delAdvertisementById` opens a `ResultSet`-capable `Statement` (TYPE_SCROLL_SENSITIVE / CONCUR_READ_ONLY) for a DELETE operation.** The scroll-sensitive cursor type is unnecessary and wasteful for a write statement. In addition, the `ResultSet rs` variable is declared (line 124) and closed in `finally` (line 142) but is never assigned — `rs.close()` is therefore a no-op guarded by a null check, adding dead code.

A72-12 | MEDIUM | AdvertismentDAO.java:37–75 | **`getAllAdvertisement` uses raw `ArrayList` return type (`ArrayList<AdvertisementBean>`) instead of `List<AdvertisementBean>`.** Both DAO files return `ArrayList` directly in several places rather than the `List` interface, exposing the concrete implementation in the public API. `CompanyDAO` mixes both styles — some methods return `List`, others return `ArrayList`.

A72-13 | MEDIUM | AdvertismentDAO.java:119 | **`delAdvertisementById` returns `Boolean` (boxed) while all other boolean-returning methods in the same class return primitive `boolean`.** Inconsistent return type; the boxed `Boolean` can return `null` theoretically, which the single `return true` statement avoids in practice but the signature implies otherwise.

A72-14 | MEDIUM | CompanyDAO.java:222 | **`GetCompanyRoles` violates Java naming convention — method name starts with an uppercase letter.** Java convention requires method names to start with a lowercase letter (`getCompanyRoles`). All other methods in both files follow lowercase-first convention.

A72-15 | MEDIUM | CompanyDAO.java:296–324 | **`saveDefaultEmails` is a private method that is never called anywhere in the file — dead code.** It sets all four email address columns to `null`, which suggests it was scaffolded and then abandoned. Its existence creates maintenance confusion.

A72-16 | MEDIUM | CompanyDAO.java:95–99 | **`UPDATE_USR_PIN`, `UPDATE_USR_INFO`, and `UPDATE_COMPANY` are declared as named constants but are never referenced anywhere in the file — dead constants.** They occupy space, mislead readers into thinking corresponding operations exist in this class, and may indicate missing functionality.

A72-17 | MEDIUM | CompanyDAO.java:247–254 | **Commented-out code block in `saveUsers`.** Lines 247–254 contain a fully commented-out `DBUtil.updateObject(SAVE_USERS, ...)` call that inserted a row into the `users` table. The constant `SAVE_USERS` (line 60) is also unreferenced as a result (see A72-16). This represents dead logic left after a Cognito migration and should be removed.

A72-18 | MEDIUM | CompanyDAO.java:488–519 | **`getCompanyById` will throw `IndexOutOfBoundsException` if the query returns no rows.** After calling `DBUtil.queryForObjects`, the method calls `results.get(0)` unconditionally (line 518) without checking whether `results` is empty. The `getCompanyByCompId` method at line 521 correctly returns the list, but this method is silently unsafe.

A72-19 | MEDIUM | AdvertismentDAO.java:193–199 | **`saveAdvertisement` only closes the connection inside the `if (null != ps)` branch in `finally`.** If `ps` is never assigned (e.g., the method returns `false` from the `advertisementBean == null` branch at line 185, or an exception occurs before `ps` is created), `DBUtil.closeConnection(conn)` is never called, leaking the connection. The `stmt` is closed unconditionally but `conn` is not.

A72-20 | MEDIUM | CompanyDAO.java:109 | **`CompanyDAO.getInstance()` uses `synchronized` on the method but not double-checked locking**, while `AdvertismentDAO.getInstance()` (lines 22–31) uses double-checked locking with `synchronized` on the class block. The two singleton implementations in the same package are inconsistent. `CompanyDAO`'s approach synchronises on every call, incurring unnecessary contention after initialisation.

A72-21 | LOW | AdvertismentDAO.java:43 | **Misleading log message — `getAllAdvertisement` logs "Inside LoginDAO Method"** instead of "Inside AdvertismentDAO Method". The same copy-paste error appears in `getAdvertisementById` (line 83), `delAdvertisementById` (line 125), and `saveAdvertisement` (line 156). `updateAdvertisement` (line 211) logs "Inside LoginDAO Method : updateManufacturer" — wrong class and wrong method name.

A72-22 | LOW | CompanyDAO.java:340 | **`updateCompPrivacy` logs "Inside LoginDAO Method"** instead of "Inside CompanyDAO Method". The same copy-paste log message error appears in `checkExist` (line 361), `checkUserExit` (line 383), `checkCompExist` (line 400), `resetPass` (line 439), `getCompLogo` (line 465), `getEntityComp` (line 659), `getEntityByQuestion` (line 694), `getAllEntity` (line 728), `addUserSubscription` (line 863), `deleteUserSubscription` (line 872), `getCompanyMaxId` (line 934), and `getUserMaxId` (line 943). Many `CompanyDAO` methods misidentify themselves as `LoginDAO` in log output, severely hampering traceability.

A72-23 | LOW | CompanyDAO.java:633 | **`updateCompSettings` logs "Inside CompanyDAO Method : updateCompInfo"** — the log tag names the wrong method (`updateCompInfo` instead of `updateCompSettings`).

A72-24 | LOW | CompanyDAO.java:622–624 | **`updateCompInfo` calls `e.printStackTrace()` before delegating to `InfoLogger.logException`.** Duplicate exception reporting to two different output streams. The same pattern occurs in `updateCompSettings` (lines 647–649). `AdvertismentDAO` also calls `e.printStackTrace()` in `getAdvertisementById` (line 106), `delAdvertisementById` (line 138), `saveAdvertisement` (line 190), and `updateAdvertisement` (line 251) alongside the structured logger.

A72-25 | LOW | AdvertismentDAO.java | **No DAO interface exists for `AdvertismentDAO`.** The class is a concrete singleton with no interface, making it impossible to mock in unit tests or swap implementations. `CompanyDAO` has the same issue. Both classes expose implementation details (raw SQL table names, JDBC patterns) through their public method signatures and log messages.

A72-26 | LOW | CompanyDAO.java:164 | **`saveSubCompInfo` declares a local SQL string `ADD_SUB_COMPANY` inline** rather than as a class-level named constant, inconsistent with the rest of `CompanyDAO` where SQL strings are defined as `private static final` constants at the top of the class.

A72-27 | LOW | CompanyDAO.java:382 | **Method name `checkUserExit` is a typo** — it should be `checkUserExists` (or `checkUserExist` to match the adjacent `checkExist`). The word "Exit" has a completely different meaning from "Exist", reducing code readability.

A72-28 | INFO | CompanyDAO.java:51 | **Typo in table name `compnay_role_rel` in SQL constants** (`UPDATE_COMPANY_ROLE` line 51, `SAVE_COMPANY_DEALER_ROLE` line 57, `SAVE_COMPANY_ROLE` line 70, and the inline query in `GetCompanyRoles` line 224). If this matches the actual database table name the application functions, but the table name itself appears to be a persistent misspelling of "company" as "compnay". This should be verified against the schema.
# P4 Agent A73 — DateFormatDAO, DriverDAO, DriverUnitDAO

## Reading Evidence

### DateFormatDAO.java
- **Class:** `DateFormatDAO` (concrete class, no interface, all static methods)
- **Fields/Constants:**
  - `private static Logger log` (line 12)
- **Methods:**
  - `getAll()` — static, line 14

---

### DriverDAO.java
- **Class:** `DriverDAO` (concrete class, no interface, mixed static/instance methods, singleton via `getInstance()`)
- **Fields/Constants:**
  - `private static Logger log` (line 35)
  - `private static final String DEFAULT_DATE_FORMAT` (line 36)
  - `private static final int NB_DAYS_WARNING_TRAINING_EXPIRATION` (line 37)
  - `private static final String UPDATE_EMAIL_SUBS_INFO_SQL` (line 39)
  - `private static final String INSERT_EMAIL_SUBS_INFO_SQL` (line 41)
  - `private static final String UPDATE_ACCESS_EMAIL_SQL` (line 43)
  - `private static final String UPDATE_ACCESS_PWD_SQL` (line 45)
  - `private static final String UPDATE_ACCESS_PWD_USER_SQL` (line 47)
  - `private static final String UPDATE_DRIVER_LICENSE_SQL` (line 49)
  - `private static final String UPDATE_GENERAL_INFO_SQL` (line 51)
  - `private static final String UPDATE_DRIVER_INFO_SQL` (line 53)
  - `private static final String UPDATE_USER_INFO_SQL` (line 55)
  - `private static final String INSERT_DRIVER_INFO_SQL` (line 57)
  - `private static final String DELETE_DRIVER_BY_ID` (line 60)
  - `private static final String DELETE_USER_BY_ID` (line 62)
  - `private static final String DELETE_USER_COGNITO_BY_ID` (line 64)
  - `private static final String DELETE_USER_ROLE_REL` (line 66)
  - `private static final String INSERT_PERMISSION_SQL` (line 68)
  - `private static final String QUERY_USER_BY_COMP` (line 71)
  - `private static final String QUERY_DRIVER_BY_COMP` (line 76)
  - `private static final String QUERY_DRIVER_BY_NAME` (line 79)
  - `private static final String QUERY_EXPIRING_TRAININGS` (line 85)
  - `private static final String QUERY_EXPIRED_TRAININGS` (line 97)
  - `private static final String QUER_ALL_EXPIRED_TRAININGS` (line 109) — note typo: QUER vs QUERY
  - `private static final String QUER_EXPIRED_TRAININGS_COMPLST` (line 122) — note typo: QUER, COMPLST
  - `private static final String QUER_EXPIRING_TRAININGS_COMPLST` (line 135) — note typo: QUER, COMPLST
  - `private static final String QUERY_DRIVER_BY_LICENCE` (line 149)
  - `private static final String QUERY_DRIVER_BY_ID` (line 154)
  - `private static final String QUERY_USER_BY_ID` (line 159)
  - `private static final String QUERY_DRIVER_EMAILS_BY_DRIVER_ID` (line 162)
  - `private static final String QUERY_CURRENT_TIME` (line 164)
  - `private static final String COGNITO_USERNAME_BY_ID` (line 166)
  - `private static DriverDAO instance` (line 168)
- **Methods:**
  - `getInstance()` — public synchronized static, line 170
  - `DriverDAO()` — private constructor, line 176
  - `checkDriverByNm(String, String, String, Long, boolean)` — public instance, line 179
  - `checkDriverByLic(String, String, Long, boolean)` — public static, line 196
  - `getDriverByNm(String, String, String, boolean)` — public instance, line 213
  - `getDriverByFullNm(String, String, boolean)` — public instance, line 252
  - `getAllDriver(String, boolean)` — public static, line 289
  - `getAllDriver(String, boolean, String)` — public static, line 293
  - `getAllUser(String, String)` — public static, line 315
  - `getAllDriverSearch(String, boolean, String, String, String)` — public static, line 352
  - `getAllUserSearch(String, String)` — public static, line 391
  - `getDriverById(Long)` — public static, line 419
  - `getUserById(Long, String)` — public static, line 449
  - `getSubscriptionByDriverId(Long)` — public static, line 480
  - `addDriverInfo(DriverBean)` — public static, line 502
  - `saveDriverInfo(DriverBean, String)` — public instance, line 540
  - `updateGeneralInfo(DriverBean)` — public static, line 577
  - `updateGeneralUserInfo(DriverBean)` — public static, line 603
  - `updateDriverLicenceInfo(LicenceBean, String)` — public static, line 630
  - `updateEmailSubsInfo(EmailSubscriptionBean)` — public static, line 649
  - `delDriverById(Long, String)` — public static, line 690
  - `delUserById(Long, String)` — public static, line 702
  - `getTotalDriverByID(String, boolean, String)` — public static, line 732
  - `getServerTime()` — private static, line 765
  - `getDriverName(Long)` — public instance, line 773
  - `getExpiringTrainings(String, String)` — public instance, line 798
  - `getExpiringTrainings(String)` — public instance (overload), line 813
  - `getExpiredTrainigs(String)` — public instance, line 828 — note typo: Trainigs
  - `getNextDriverId()` — public static, line 843
  - `getNextUserId()` — public static, line 848
  - `saveDriverCompRel(Connection, Long, String, String, String)` — private static, line 853
  - `saveDefaultEmails(Connection, Long)` — private static, line 869
  - `getALLExpiredTrainigs()` — public static, line 883 — note typo: Trainigs
  - `revokeDriverAccessOnTrainingExpiry()` — public static, line 902
  - `getExpiredTrainigsComp()` — public instance, line 920 — note typo: Trainigs
  - `getExpiringTrainigsComp()` — public instance, line 932 — note typo: Trainigs

---

### DriverUnitDAO.java
- **Class:** `DriverUnitDAO` (concrete class, no interface, singleton via `getInstance()`, mixed static/instance methods)
- **Fields/Constants:**
  - `private static final String QUERY_DRIVER_UNITS_BY_DRIVER_ID` (line 12)
  - `private static final String QUERY_UNITS_ASSIGNED` (line 13)
  - `private static final String UNASSIGN_DRIVER_UNIT` (line 14)
  - `private static final String ASSIGN_DRIVER_UNIT` (line 15)
  - `private static DriverUnitDAO instance` (line 17)
- **Methods:**
  - `getInstance()` — public static, line 19
  - `DriverUnitDAO()` — private constructor, line 30
  - `getDriverUnitsByCompAndDriver(Long, Long)` — public static, line 33
  - `saveDriverVehicle(DriverVehicleBean)` — public instance, line 49

---

## Findings

A73-1 | CRITICAL | DriverDAO.java:226 | **SQL injection** in `getDriverByNm()`: `firstName`, `lastName`, and `compId` are interpolated directly into the SQL string. A `FIXME` comment on line 225 acknowledges this but the fix was never applied. An attacker-controlled driver name or company ID can manipulate the query.

A73-2 | CRITICAL | DriverDAO.java:264 | **SQL injection** in `getDriverByFullNm()`: `fullName` and `compId` are interpolated directly into the SQL string. The same `FIXME` comment on line 263 acknowledges this but was never acted upon.

A73-3 | CRITICAL | DriverDAO.java:783 | **SQL injection** in `getDriverName()`: the `id` parameter (a `Long`) is interpolated directly into the SQL string (`"...where id=" + id`). Although `Long` limits damage here, the pattern is inconsistent and dangerous if the type ever changes.

A73-4 | CRITICAL | DriverDAO.java:748 | **SQL injection** in `getTotalDriverByID()`: `id` (a `String`) and `timezone` (a `String`) are interpolated directly into the SQL string. A caller-supplied `timezone` value can manipulate the query.

A73-5 | HIGH | DriverDAO.java:170 | **Broken singleton** — `getInstance()` is declared `synchronized` but the body uses no double-checked locking; the `instance` field is not `volatile`. Under the Java Memory Model, the reference may be observed as non-null before the object is fully constructed in another thread. Compare with `DriverUnitDAO` which uses double-checked locking (correctly, lines 19–28) but omits `volatile` there too. Neither singleton is thread-safe.

A73-6 | HIGH | DriverDAO.java:179 | **Static/instance method inconsistency**: `checkDriverByNm()` is an instance method while the identical-purpose `checkDriverByLic()` (line 196) is `static`. Similarly, `saveDriverInfo()` (line 540) is an instance method while `addDriverInfo()` (line 502), `updateGeneralInfo()` (line 577), and almost every other write method are `static`. The class exposes a singleton but most of its API is callable without the instance, making the singleton meaningless for most callers.

A73-7 | HIGH | DriverDAO.java:47 | **Dead constant** `UPDATE_ACCESS_PWD_USER_SQL` (line 47) is defined but never referenced anywhere in the class. It is dead code that may represent an incomplete or abandoned feature.

A73-8 | HIGH | DriverDAO.java:55 | **Dead constant** `UPDATE_USER_INFO_SQL` (line 55) is defined but never referenced anywhere in the class. Dead code.

A73-9 | HIGH | DriverDAO.java:906 | **Swallowed exception with `e.printStackTrace()`** inside `revokeDriverAccessOnTrainingExpiry()` (line 914–915): the `SQLException` thrown within a `forEach` lambda is caught and only printed to stderr. The caller receives no signal that one or more unit-revocation operations failed, leaving the database in a partially updated state silently.

A73-10 | HIGH | DriverDAO.java:315 | **Service call embedded in DAO** (`getAllUser()`, lines 333–334): a `RestClientService` is instantiated and invoked directly inside a DAO method to retrieve Cognito user details. DAO classes should be responsible solely for database access; mixing remote HTTP/Cognito calls violates separation of concerns and makes the method untestable in isolation. The same pattern appears in `getUserById()` (line 468), `updateGeneralUserInfo()` (line 611–621), and `delUserById()` (lines 712–713).

A73-11 | MEDIUM | DriverDAO.java:109 | **Typo in constant names**: `QUER_ALL_EXPIRED_TRAININGS` (line 109), `QUER_EXPIRED_TRAININGS_COMPLST` (line 122), and `QUER_EXPIRING_TRAININGS_COMPLST` (line 135) are missing the `Y` suffix (should be `QUERY_`). `COMPLST` should be `COMP_LIST`. The same typo appears in method names: `getExpiredTrainigs` (line 828), `getALLExpiredTrainigs` (line 883), `getExpiredTrainigsComp` (line 920), `getExpiringTrainigsComp` (line 932) — all missing the `n` in `Trainings`.

A73-12 | MEDIUM | DriverDAO.java:225 | **Unresolved FIXME comments**: two `FIXME` comments (lines 225 and 263) explicitly flag SQL injection and recommend switching to prepared statements. These were never resolved, and the SQL injection vulnerabilities they describe (see A73-1, A73-2) remain active.

A73-13 | MEDIUM | DriverDAO.java:426 | **TODO comments left unresolved**: two `TODO` comments at lines 426–426 and 456–456 question whether a driver can be associated with multiple companies and whether `queryForObject` could return multiple records. These represent known design uncertainty that has never been documented or resolved.

A73-14 | MEDIUM | DriverDAO.java:914 | **TODO Auto-generated catch block** left in production code (line 914): `// TODO Auto-generated catch block` combined with `e.printStackTrace()` indicates IDE-generated stub code that was committed without implementing proper error handling.

A73-15 | MEDIUM | DriverUnitDAO.java:17 | **Singleton `instance` field not `volatile`**: the double-checked locking pattern in `getInstance()` (lines 19–27) requires the `instance` field to be declared `volatile` to prevent the JIT/CPU from publishing an incompletely-constructed object. Without `volatile`, the pattern is broken under the Java Memory Model. The same issue exists in `DriverDAO` (line 168).

A73-16 | MEDIUM | DriverDAO.java:36 | **Wrong date format string** in `DEFAULT_DATE_FORMAT`: the value is `"dd/mm/yyyy"` (line 36) where `mm` is minutes, not months. The correct format for day/month/year is `"dd/MM/yyyy"`. This causes any date formatted with this constant to display the minute value in the month position.

A73-17 | MEDIUM | DriverDAO.java:257 | **Misleading log message** in `getDriverByFullNm()` (line 256): the log statement reads `"Inside DriverDAO Method : getDriverByNm"` but the actual method is `getDriverByFullNm`. Copy-paste error makes log tracing unreliable.

A73-18 | MEDIUM | DriverDAO.java:933 | **Misleading log message** in `getExpiringTrainigsComp()` (line 933): logs `"Inside DriverDAO Method : getExpiredTrainigsComp"` (expired) when the method retrieves *expiring* trainings.

A73-19 | MEDIUM | DateFormatDAO.java:14 | **No DAO interface**: none of the three DAO classes implement an interface. All three are concrete, directly instantiated or called statically, providing no contract for testing or substitution. This is a systemic leaky-abstraction pattern across the entire `com.dao` package (confirmed by absence of any `IDateFormatDAO`, `IDriverDAO`, or `IDriverUnitDAO` files).

A73-20 | MEDIUM | DriverDAO.java:765 | **Misleading log message** in `getServerTime()` (line 766): logs `"Inside LoginDAO DriverDAO : getServerTime"` — the class prefix `LoginDAO` is incorrect; this method is in `DriverDAO`.

A73-21 | LOW | DriverDAO.java:13 | **Wildcard import** `import com.bean.*` (line 13) followed by redundant explicit imports of individual `com.bean.*` classes (lines 25–29). This is inconsistent style and the explicit imports are dead duplicates given the wildcard already covers them.

A73-22 | LOW | DriverDAO.java:331 | **Deprecated `List.size() > 0` pattern**: line 331 uses `userRequestList.size() > 0` instead of the idiomatic and more readable `!userRequestList.isEmpty()`. Minor style issue.

A73-23 | LOW | DriverDAO.java:324 | **Raw generic type**: `new ArrayList<UserRequest>()` on line 324 uses a diamond, which is fine, but the variable type annotation `List<UserRequest> userRequestList = new ArrayList<UserRequest>()` is unnecessarily verbose when `new ArrayList<>()` suffices. More importantly, elsewhere in the same method the builder pattern is used for DB queries while this block falls back to imperative loops with manual field mapping — inconsistent internal coding style.

A73-24 | LOW | DriverDAO.java:52 | **Trailing whitespace** on line 52 (after the closing semi-colon of `UPDATE_GENERAL_INFO_SQL`). Minor but indicative of inconsistent formatting discipline.

A73-25 | LOW | DriverDAO.java:906 | **Inline SQL string** in `revokeDriverAccessOnTrainingExpiry()` (line 906): `String query = "delete from driver_unit where driver_id = ? and unit_id = ?"` is defined as a local variable inside a method body rather than as a class-level `private static final` constant, inconsistent with every other SQL statement in the class.

A73-26 | LOW | DriverUnitDAO.java:69 | **Silently ignored rollback exception**: in `saveDriverVehicle()`, when a `connection.rollback()` fails inside the catch block (lines 66–69 and 81–84), the secondary `SQLException e1` is swallowed with the comment `// Ignore the error`. The original exception is still propagated, but the failure to rollback is invisible, potentially leaving a partially-committed transaction.
# P4 Agent A74 — DyanmicBeanDAO, FormBuilderDAO

## Reading Evidence

### DyanmicBeanDAO.java

**Class:** `DyanmicBeanDAO` (package `com.dao`)

**Fields / Constants:**
| Name | Type | Line |
|------|------|------|
| `log` | `private static Logger` | 18 |

**Methods:**
| Method | Signature | Lines |
|--------|-----------|-------|
| `getDynamicBean` | `public ArrayList<DynamicBean> getDynamicBean() throws Exception` | 20–59 |

---

### FormBuilderDAO.java

**Class:** `FormBuilderDAO` (package `com.dao`)

**Fields / Constants:**
| Name | Type | Line |
|------|------|------|
| `log` | `private static Logger` | 22 |

**Methods:**
| Method | Signature | Lines |
|--------|-----------|-------|
| `getLib` | `public ArrayList<FormLibraryBean> getLib(String questionId, String type) throws SQLException` | 24–61 |
| `saveLib` | `public boolean saveLib(String entityId, String questionId, String type, FormBuilderBean formBuilderBean) throws SQLException` | 63–135 |
| `saveAnswerForm` | `public boolean saveAnswerForm(String questionId, String type, FormBuilderBean formBuilderBean) throws SQLException` | 138–208 |

---

## Findings

A74-1 | LOW | DyanmicBeanDAO.java:16 | Class name `DyanmicBeanDAO` is a misspelling of `DynamicBeanDAO`. The transposition of 'y' and 'n' is propagated into the logger string at line 18 (`"com.dao.DyanmicBeanDAO"`), the log message at line 26 which still refers to `"LoginDAO"`, and the source file name itself. All references should be renamed consistently to `DynamicBeanDAO`.

A74-2 | HIGH | FormBuilderDAO.java:37 | SQL injection vulnerability in `getLib`: the query is built by direct string concatenation of the caller-supplied parameters `questionId` and `type` — `"select id, form_object from form_library where question_id ="+questionId+" and type = '"+type+"'"`. Both parameters should be bound via `PreparedStatement` placeholders as is done in `saveLib` and `saveAnswerForm`.

A74-3 | MEDIUM | DyanmicBeanDAO.java:26 | Log message incorrectly identifies the class as `"LoginDAO"` — `log.info("Inside LoginDAO Method : getDynamicBean")`. This copy-paste error will produce misleading log output when diagnosing production issues.

A74-4 | MEDIUM | FormBuilderDAO.java:29 | Same copy-paste log message error in `getLib` — `log.info("Inside LoginDAO Method : getLib")` — should reference `FormBuilderDAO`.

A74-5 | MEDIUM | FormBuilderDAO.java:71 | Same copy-paste log message error in `saveLib` — `log.info("Inside LoginDAO Method : saveLib")` — should reference `FormBuilderDAO`.

A74-6 | MEDIUM | FormBuilderDAO.java:146 | Log message in `saveAnswerForm` reads `"Inside LoginDAO Method : saveLib"`, which is wrong on both counts: wrong class name and wrong method name. Should reference `FormBuilderDAO` and `saveAnswerForm`.

A74-7 | MEDIUM | FormBuilderDAO.java:63–135 | `saveLib` creates a `Statement stmt` (line 67) and opens it at line 75 with `conn.createStatement(...)`, but `stmt` is never used for any query — all actual queries go through `PreparedStatement ps`. The dead `Statement` wastes a database cursor, adds noise to the finally-block close, and is likely a copy-paste artefact from `getLib`. It should be removed.

A74-8 | MEDIUM | FormBuilderDAO.java:138–208 | Same dead `Statement stmt` issue in `saveAnswerForm` (lines 142, 150). Identical to A74-7.

A74-9 | LOW | FormBuilderDAO.java:79 | In `saveLib`, a `FormLibraryBean formLibraryBean = new FormLibraryBean()` is instantiated (line 79) but no data is loaded into it from the database; it is used only as a helper to call `formLibraryBean.getByteArrayObject(formBuilderBean)`. The same pattern is repeated in `saveAnswerForm` at line 154. Using a freshly-constructed, unpopulated bean as a delegate to invoke a serialization utility is a leaky abstraction — `getByteArrayObject` is a static-style utility operation that logically belongs on `FormBuilderBean` or a separate utility class, not on an empty `FormLibraryBean` instance.

A74-10 | LOW | FormBuilderDAO.java:24 | `getLib` uses a `Statement` with `TYPE_SCROLL_SENSITIVE` / `CONCUR_READ_ONLY` (line 35) but the result set is only ever read with a single `if(rs.next())` — at most one row is consumed. A scrollable cursor is heavier than a forward-only cursor and is unnecessary here; a standard `createStatement()` or `PreparedStatement` would be sufficient.

A74-11 | LOW | DyanmicBeanDAO.java:32 | `getDynamicBean` also opens a `TYPE_SCROLL_SENSITIVE` / `CONCUR_READ_ONLY` scrollable cursor (line 32) but iterates with a plain forward `while(rs.next())` loop, never using any scroll capability. A forward-only cursor is sufficient.

A74-12 | LOW | DyanmicBeanDAO.java:49 | In the catch block, the code wraps the caught `Exception` as `new SQLException(e.getMessage())` (line 49), discarding the original stack trace. The same pattern exists in `FormBuilderDAO` at lines 53, 125, and 198. Using `new SQLException(e.getMessage())` instead of `new SQLException(e)` or rethrowing the cause means the root exception and its stack trace are lost in logs and in any upstream handler.

A74-13 | INFO | FormBuilderDAO.java:1–4 | Three consecutive blank lines at the top of the file (lines 1–4 before the first import) is a minor style inconsistency compared to the single blank line convention used elsewhere in the package.

A74-14 | INFO | FormBuilderDAO.java:22 | The `log` field declaration is not indented (no leading tab/spaces), while all other field and method declarations in the class are indented with one tab. This is a minor style inconsistency.
# P4 Agent A75 — GPSDao, ImpactReportDAO

## Reading Evidence

### GPSDao.java

**Class:** `GPSDao` (line 20)

**Fields / Constants:**
| Name | Type | Modifier | Line |
|---|---|---|---|
| `log` | `Logger` | `private static` | 22 |
| `vgps_string` | `ArrayList` (raw) | package-private instance | 25 |
| `Vveh_cd` | `ArrayList` (raw) | package-private instance | 26 |
| `QUERY_UNIT_GPS` | `String` | `private static final` | 28–33 |

**Methods:**
| Method | Modifier | Return Type | Line |
|---|---|---|---|
| `getUnitGPSData(String compId, String[] unitIds, String dateFormat, String timezone)` | `public static` | `List<String>` | 35 |
| `getGPSLocations(String[] unitList)` | `public` | `void` | 74 |
| `getUnitById(String id)` | `public` | `ArrayList<UnitBean>` | 122 |
| `getVgps_string()` | `public` | `ArrayList` (raw) | 177 |
| `getVveh_cd()` | `public` | `ArrayList` (raw) | 181 |
| `setVgps_string(ArrayList vgps_string)` | `public` | `void` | 185 |
| `setVveh_cd(ArrayList vveh_cd)` | `public` | `void` | 189 |

---

### ImpactReportDAO.java

**Class:** `ImpactReportDAO` (line 11)

**Fields / Constants:**
| Name | Type | Modifier | Line |
|---|---|---|---|
| `theInstance` | `ImpactReportDAO` | `private static` | 12 |

**Methods:**
| Method | Modifier | Return Type | Line |
|---|---|---|---|
| `getInstance()` | `public static` | `ImpactReportDAO` | 14 |
| `ImpactReportDAO()` (constructor) | `private` | — | 26 |
| `countImpactsToday(Long compId, String timezone)` | `public` | `Integer` | 29 |
| `getImpactReport(Long compId, ImpactReportFilterBean filter, String format, String timezone)` | `public` | `ImpactReportBean` | 33 |

---

## Findings

A75-1 | HIGH | GPSDao.java:25–26 | Raw types on instance fields. `vgps_string` and `Vveh_cd` are declared as raw `ArrayList` with no type parameter. This suppresses generic type safety and will produce unchecked-operation compiler warnings everywhere these fields are used. Both fields store `String` values based on usage (lines 94, 105); they should be `ArrayList<String>`.

A75-2 | HIGH | GPSDao.java:38,41 | Raw-type `ArrayList` instantiations inside `getUnitGPSData`. `new ArrayList()` at lines 38 and 41 omit the type parameter, producing unchecked-operation warnings. The diamond operator or explicit type argument should be used in both cases (context makes `ArrayList<String>` and `ArrayList<GPSUnitBean>` clear from the surrounding declarations).

A75-3 | HIGH | GPSDao.java:87–88 | SQL injection via string concatenation. `getGPSLocations` builds a SQL query by directly concatenating `unitList[i]` (an untrusted caller-supplied string) into the query at line 87–88 without any parameterisation or input validation. This is a critical SQL-injection vector. `getUnitById` at line 136–139 has the same pattern, concatenating the `id` parameter directly. (Reported under this finding because both methods share the same root cause; see A75-4 for `getUnitById`.)

A75-4 | HIGH | GPSDao.java:136–139 | SQL injection via string concatenation in `getUnitById`. The `id` parameter is embedded directly into the SQL string without parameterisation, identical to A75-3. Should use a `PreparedStatement`.

A75-5 | MEDIUM | GPSDao.java:64–65 | Manual JSON serialisation via string concatenation. The GPS JSON strings in both `getUnitGPSData` (line 64) and `getGPSLocations` (line 102) are built by concatenating field values directly into a JSON string literal. If any field value contains a double-quote, backslash, or control character, the produced JSON will be malformed. A proper JSON serialisation library (already present in the project via beans/Lombok) should be used.

A75-6 | MEDIUM | GPSDao.java:74,177–191 | Instance-state-based result accumulation is a leaky abstraction. `getGPSLocations` accumulates results into instance fields `vgps_string` and `Vveh_cd`, which are then retrieved via separate getter calls (`getVgps_string`, `getVveh_cd`). This design makes `GPSDao` stateful: repeated calls accumulate into the same lists without clearing them, making results from successive invocations silently merge. The pattern is inconsistent with `getUnitGPSData` and `getUnitById`, which both return their results directly. The four accessor methods for these fields (lines 177–191) exist solely to support this anti-pattern.

A75-7 | MEDIUM | GPSDao.java:111 | `e.printStackTrace()` called in catch blocks. Both `getGPSLocations` (line 111) and `getUnitById` (line 165) call `e.printStackTrace()` after already passing the exception to `InfoLogger.logException`. This is redundant and writes to stderr rather than to the configured logging framework, defeating centralised log management.

A75-8 | MEDIUM | GPSDao.java:112 | Wrapping a generic `Exception` in a `SQLException` loses the original exception type. `throw new SQLException(e.getMessage())` discards the original exception's type and stack trace (message-only wrapping). The cause should be passed: `throw new SQLException(e.getMessage(), e)`. The same pattern occurs at line 166 in `getUnitById`.

A75-9 | MEDIUM | GPSDao.java:26 | Field name `Vveh_cd` violates Java naming conventions. Instance fields must begin with a lowercase letter per the Java Code Conventions; `Vveh_cd` begins with an uppercase `V`. This also means the setter at line 189 contains `Vveh_cd = vveh_cd` (an assignment from parameter to field using capitalization alone to distinguish them), which is error-prone.

A75-10 | LOW | GPSDao.java:25–26 | Package-private (default) visibility on instance fields `vgps_string` and `Vveh_cd`. Fields that are not intended to be accessed directly from outside the class (there are explicit getters and setters) should be `private`.

A75-11 | LOW | GPSDao.java:35 | `static` method `getUnitGPSData` on a non-singleton, non-utility class. The class has both static and instance methods, and the instance is stateful (fields `vgps_string`, `Vveh_cd`). Mixing static and instance methods with instance state is inconsistent and confusing. Either make the class a proper singleton / utility class, or make all data-access methods instance methods.

A75-12 | LOW | GPSDao.java:36 | Log message inside `getUnitGPSData` says "Inside DriverDAO Method" (line 36) — copy-paste error. The class is `GPSDao`, not `DriverDAO`. The same pattern appears in `getUnitById` at line 128, which logs "Inside LoginDAO Method". Neither message correctly identifies the actual class.

A75-13 | LOW | GPSDao.java:99 | Variable `status` (line 99) is populated from `rs.getString(6)` (`current_location`) but is never used after assignment. This is dead code / unused local variable that will produce a compiler warning.

A75-14 | LOW | GPSDao.java:39 | `StringBuilder builder` in `getUnitGPSData` (line 39) is constructed from `QUERY_UNIT_GPS` but `builder.toString()` is called directly without any append operations. The `StringBuilder` wrapping serves no purpose; the constant could be passed directly to `DBUtil.queryForObjects`.

A75-15 | INFO | GPSDao.java:20 vs ImpactReportDAO.java:11 | Naming inconsistency between DAO classes. `GPSDao` uses mixed-case "Dao" suffix while `ImpactReportDAO` uses all-caps "DAO" suffix. The project should standardise on one convention. All other DAO files in the `com.dao` package should be reviewed for consistency.

A75-16 | INFO | GPSDao.java:11 | `GPSDao` uses `org.apache.log4j.Logger` via `InfoLogger.getLogger`, while `ImpactReportDAO` uses Lombok `@Slf4j`. The project uses two different logging setup patterns across DAO classes in the same package; this should be standardised.

A75-17 | INFO | ImpactReportDAO.java:12–24 | Double-checked locking singleton pattern is used in `ImpactReportDAO`. While the implementation is correct (uses `synchronized` with double-null check), the `theInstance` field is not declared `volatile`, which can lead to subtle visibility issues on some JVMs due to instruction reordering. Declaring `theInstance` as `private static volatile ImpactReportDAO theInstance` would make the pattern fully correct.
# P4 Agent A76 — IncidentReportDAO, JobsDAO

## Reading Evidence

### IncidentReportDAO.java

**Class:** `IncidentReportDAO` (package `com.dao`)

**Fields/Constants:**
| Name | Type | Line |
|------|------|------|
| `theInstance` | `private static IncidentReportDAO` | 14 |

**Methods:**
| Method | Signature | Lines |
|--------|-----------|-------|
| `getInstance` | `public static IncidentReportDAO getInstance()` | 16–26 |
| `getIncidentReport` | `public IncidentReportBean getIncidentReport(int compId, IncidentReportFilterBean filter, String format, String timezone) throws SQLException` | 28–33 |

**Annotations:** `@Slf4j`, `@NoArgsConstructor` (class level)

---

### JobsDAO.java

**Class:** `JobsDAO` (package `com.dao`)

**Fields/Constants:**
| Name | Type | Line |
|------|------|------|
| `log` | `private static Logger` | 24 |
| `driverDAO` | `private DriverDAO` | 26 |

**Methods:**
| Method | Signature | Lines |
|--------|-----------|-------|
| `getJobList` | `public ArrayList<JobDetailsBean> getJobList(String equipId) throws Exception` | 34–98 |
| `getJobListByJobId` | `public ArrayList<JobDetailsBean> getJobListByJobId(String equipId, String jobNo) throws Exception` | 108–170 |
| `addJob` | `public boolean addJob(JobDetailsBean jobdetails) throws Exception` | 178–253 |
| `editJob` | `public boolean editJob(JobDetailsBean jobdetails) throws Exception` | 261–322 |

---

## Findings

A76-1 | CRITICAL | IncidentReportDAO.java:18 | Wrong class used as the monitor lock in the double-checked locking singleton. The `synchronized` block locks on `ImpactReportDAO.class` instead of `IncidentReportDAO.class`. This means two unrelated classes share no common monitor, so the guard is completely ineffective: two threads can both pass the outer `null` check simultaneously and each create a separate instance, breaking the singleton guarantee and potentially causing race conditions.

A76-2 | CRITICAL | JobsDAO.java:52 | SQL injection in `getJobList`. The `equipId` parameter (a `String`) is concatenated directly into the SQL query without sanitisation or use of a `PreparedStatement`. An attacker-controlled value can alter the query structure.

A76-3 | CRITICAL | JobsDAO.java:123 | SQL injection in `getJobListByJobId`. Both `equipId` and `jobNo` are concatenated directly into the SQL string using a `Statement` rather than a `PreparedStatement`. `jobNo` is a free-text string wrapped in single-quote delimiters, making classic string-injection trivial.

A76-4 | HIGH | JobsDAO.java:17 | Unused and incorrect import: `com.sun.tools.xjc.Driver` is imported but never referenced anywhere in the file. This is a JDK-internal tools API (part of the XJC JAXB compiler), not a driver for anything used here. In addition to being dead code, importing `com.sun.*` internal classes causes compiler warnings and is not portable across JDK versions/vendors.

A76-5 | HIGH | JobsDAO.java:195–201 | Race condition / non-atomic ID generation in `addJob`. The new primary key is obtained by executing `SELECT MAX(id)+1 FROM jobs` and then used in a subsequent `INSERT`. Under concurrent load two callers can read the same max value and attempt to insert duplicate IDs, causing a constraint violation or data corruption. A sequence/auto-increment or `INSERT … RETURNING id` pattern should be used instead.

A76-6 | HIGH | JobsDAO.java:213 | `job_no` column is set to the string representation of the numeric ID (`ps.setString(4, job_id)`), which is the same value as the integer primary key set in parameter 5. The intent appears to be that `job_no` is a distinct business-facing identifier, but the code conflates it with the surrogate key. This is almost certainly a logic error.

A76-7 | HIGH | JobsDAO.java:63–64 | `driverDAO.getDriverById(rs.getLong(3))` is called inside the result-set loop in `getJobList` with no null check on the returned `DriverBean`. If the driver record does not exist (e.g. the `job_allocation` row has a dangling FK or `driver_id` is NULL from the LEFT JOIN), `driver.getFirst_last()` will throw a `NullPointerException`, silently wrapped into a `SQLException` and swallowing the real cause. The same pattern recurs at line 134–135 in `getJobListByJobId`.

A76-8 | MEDIUM | JobsDAO.java:36,110 | Log messages say `"Inside LoginDAO Method"` but the class is `JobsDAO`. Copy-paste error in the log strings at lines 36 and 110 makes log triage misleading.

A76-9 | MEDIUM | JobsDAO.java:34,108 | Return type declared as `ArrayList<JobDetailsBean>` (concrete implementation) instead of `List<JobDetailsBean>`. Programming to implementation rather than interface reduces flexibility and is a style/design anti-pattern. The same issue applies to the local variable declarations at lines 38 and 112.

A76-10 | MEDIUM | JobsDAO.java:10 | `java.util.Date` is imported but never used anywhere in the file. Dead import.

A76-11 | MEDIUM | JobsDAO.java:265–267 | In `editJob`, `stmt` and `rs` are declared and `rs` is never assigned (`rs` stays `null` throughout). The `finally` block checks `rs` and `stmt` unnecessarily — `stmt` is created (`conn.createStatement(...)` at line 273) but never executed, making its allocation pointless. This is dead/vestigial code left over from copy-pasting `getJobList`/`getJobListByJobId` as a template.

A76-12 | MEDIUM | IncidentReportDAO.java:11–12 | `@Slf4j` declares a `log` field via Lombok, but that field is never used anywhere in the class. The annotation is redundant dead code. (The one place a logger would be useful — the singleton initialisation — has no logging.)

A76-13 | LOW | JobsDAO.java:28–33, 102–107, 173–177, 256–260 | Block comments use a custom `START/END` convention with author and date annotations embedded in source (`Added By: Leslie`, `Date Added: 2017-04-20`). These change-history notes belong in version-control history, not in source code. The pattern is a style inconsistency with `IncidentReportDAO.java` which uses no such comments.

A76-14 | LOW | JobsDAO.java:21–22 | Allman-style brace placement (`public class JobsDAO\n{`) is inconsistent with the more common K&R/Java-standard style used in `IncidentReportDAO.java` and the rest of the codebase. The same inconsistency appears on every method and block within `JobsDAO.java`.

A76-15 | LOW | JobsDAO.java:24 | Uses `org.apache.log4j.Logger` obtained via a custom `InfoLogger.getLogger(...)` factory. `IncidentReportDAO.java` uses Lombok `@Slf4j` (SLF4J). Two different logging approaches are in use in the same package, causing inconsistency. Log4j is also used directly rather than via the SLF4J abstraction layer.
# P4 Agent A77 — LanguageDAO, LoginDAO

## Reading Evidence

### LanguageDAO.java

**Class:** `com.dao.LanguageDAO`

**Fields/Constants:**
| Name | Type | Line |
|------|------|------|
| `log` | `static Logger` | 17 |
| `instance` | `static LanguageDAO` | 19 |

**Methods:**
| Method | Line |
|--------|------|
| `getInstance()` | 21 |
| `LanguageDAO()` (private constructor) | 32 |
| `getAllLan()` | 36 |

---

### LoginDAO.java

**Class:** `com.dao.LoginDAO`

**Fields/Constants:**
| Name | Type | Line |
|------|------|------|
| `log` | `static Logger` | 15 |
| `instance` | `static LoginDAO` | 17 |

**Methods:**
| Method | Line |
|--------|------|
| `getInstance()` | 19 |
| `LoginDAO()` (private constructor) | 30 |
| `getCompanyId(String username)` | 34 |
| `getUserId(String username)` | 40 |
| `checkLogin(String username, String password)` | 47 |
| `isUserAuthority(int userId, String authority)` | 59 |
| `isAuthority(String compId, String authority)` | 71 |
| `getCompanies(Boolean isSuperAdmin, Boolean isDealerLogin, String username, String password, int comp)` | 86 |
| `getCompanies(Boolean isSuperAdmin, Boolean isDealer, Integer company)` | 104 |
| `getSuperAdminCompanies()` | 111 |
| `getDealerCompanies(int companyId)` | 186 |
| `getSimpleCompanies(int companyId)` | 235 |

---

## Findings

A77-1 | CRITICAL | LoginDAO.java:51 | Plain-text password passed to MD5 via `checkLogin`. MD5 is a broken hash algorithm unsuitable for password storage. Passwords are transmitted as plain strings and hashed only at query time, meaning they travel in clear through the application layer. This applies also to the `getCompanies` overload at line 92.

A77-2 | HIGH | LoginDAO.java:34-43 | `getCompanyId` and `getUserId` are declared `static` on a class that implements a singleton pattern. Static methods bypass the singleton instance entirely, making the singleton pattern meaningless for these methods. The class mixes instance methods and static utility methods inconsistently throughout — some methods are `static` (lines 34, 40, 59, 71, 104, 111, 186, 235) while others are instance methods (lines 47, 86), with no logical basis for the distinction.

A77-3 | HIGH | LoginDAO.java:80 | `Integer.parseInt(compId)` inside `isAuthority` will throw an unchecked `NumberFormatException` if `compId` is null or non-numeric. The method signature accepts `String compId` rather than `int`/`Integer`, forcing a fragile runtime parse with no guard.

A77-4 | MEDIUM | LanguageDAO.java:42 | Log message says `"Inside TimezoneDAO Method : getAllLan"` but the enclosing class is `LanguageDAO`, not `TimezoneDAO`. This is a copy-paste error that will produce misleading log output.

A77-5 | MEDIUM | LanguageDAO.java:44 | Raw-parameterized `ArrayList<LanguageBean>` is used where the return type could be declared as `List<LanguageBean>`. Returning a concrete `ArrayList` leaks the implementation type through the public API. The same pattern exists with `getAllLan()` returning `ArrayList` at line 36.

A77-6 | MEDIUM | LanguageDAO.java:48 | `ResultSet.TYPE_SCROLL_SENSITIVE` is used for a forward-only sequential `while(rs.next())` loop. A scrollable, sensitive cursor is significantly more expensive than `TYPE_FORWARD_ONLY` and provides no benefit here.

A77-7 | MEDIUM | LoginDAO.java:86 | The instance-method overload of `getCompanies` (line 86) accepts `username` and `password` to re-authenticate at the company level via a second `md5(?)` query (line 92), while the static overload at line 104 accepts a pre-resolved `company` ID with no credential re-check. The two overloads represent fundamentally different authorization semantics under the same method name, which is a leaky abstraction and will confuse callers.

A77-8 | MEDIUM | LoginDAO.java:71 | `isAuthority` and `isUserAuthority` (lines 59 and 71) both log `"Inside LoginDAO Method : isAuthority"`, making it impossible to distinguish which method was called from log output alone.

A77-9 | MEDIUM | LoginDAO.java:76 | The SQL string `"compnay_role_rel"` is a misspelling of `"company_role_rel"` (letters transposed). The same misspelling appears in `getSuperAdminCompanies` (line 124), `getDealerCompanies` (lines 192, 202), and `getSimpleCompanies` (line 241). If the underlying table name is intentionally misspelled (as a DB artifact), this represents a perpetuated naming defect; if the table was later corrected, these queries will silently fail at runtime.

A77-10 | MEDIUM | LanguageDAO.java:65 | `e.printStackTrace()` is called in the catch block at line 65 in addition to `InfoLogger.logException`. Duplicate error reporting via `printStackTrace` writes to stderr outside the managed logging framework, producing inconsistent and potentially interleaved output in production environments.

A77-11 | LOW | LanguageDAO.java:62-67 | The catch block catches `Exception` (broadest possible type) and then rethrows as `SQLException`, discarding the original exception type. This wrapping is lossy: a `RuntimeException` or `NullPointerException` becomes indistinguishable from a database error. The method signature `throws Exception` at line 36 is also broader than necessary given only DB operations are performed.

A77-12 | LOW | LanguageDAO.java | The singleton `instance` field (line 19) is not declared `volatile`. The double-checked locking pattern used in `getInstance()` (lines 22-29) requires `volatile` on the instance field to be correct under the Java Memory Model; without it, a partially-constructed object can be observed by another thread.

A77-13 | LOW | LoginDAO.java:17 | Same issue as A77-12: `LoginDAO.instance` (line 17) is not declared `volatile`, making the double-checked locking in `getInstance()` (lines 19-28) unsafe under the Java Memory Model.

A77-14 | LOW | LoginDAO.java:127 | The `getSuperAdminCompanies` query orders by `company.name, c.name DESC` — mixing an implicit `ASC` on the primary sort key with an explicit `DESC` on the secondary. This is likely unintentional and will cause unexpected ordering of sub-company results.

A77-15 | INFO | LanguageDAO.java:50 | Raw SQL `"select id,name from language"` is logged at INFO level (line 51). Logging full SQL at INFO in production generates noise and may expose schema details in log aggregation systems. DEBUG level would be more appropriate.
# P4 Agent A78 — ManufactureDAO, MenuDAO

## Reading Evidence

### ManufactureDAO.java
**Class:** `com.dao.ManufactureDAO`

**Fields / Constants:**
| Name | Type | Line |
|------|------|------|
| `log` | `private static Logger` | 19 |
| `QUERY_MANUFACTURE_SQL` | `private static final String` | 21–22 |
| `QUERY_VEHICLE_BY_MANUFACTURE_SQL` | `private static final String` | 24–25 |
| `theInstance` | `private static ManufactureDAO` | 27 |

**Methods:**
| Method | Modifier | Line |
|--------|----------|------|
| `getInstance()` | `public synchronized static ManufactureDAO` | 29 |
| `ManufactureDAO()` (constructor) | `private` | 37 |
| `getAllManufactures(String companyId)` | `public static List<ManufactureBean>` | 40 |
| `getManufactureById(String id)` | `public ArrayList<ManufactureBean>` | 60 |
| `delManufacturById(String id)` | `public static Boolean` | 99 |
| `checkManuByNm(String name, String id)` | `public boolean` | 137 |
| `saveManufacturer(ManufactureBean)` | `public static boolean` | 174 |
| `updateManufacturer(ManufactureBean)` | `public static boolean` | 210 |
| `getManu_type_fuel_rel(String manuId)` | `public ArrayList<ManuTypeFuleRelBean>` | 247 |
| `checkManu_type_fuel_rel(ManuTypeFuleRelBean)` | `public boolean` | 291 |
| `saveManu_type_fuel_rel(ManuTypeFuleRelBean)` | `public boolean` | 335 |
| `delManu_type_fuel_rel(String relId)` | `public boolean` | 373 |
| `isVehicleAssignedToManufacturer(String manufacturerId)` | `public static boolean` | 404 |

---

### MenuDAO.java
**Class:** `com.dao.MenuDAO`

**Fields / Constants:**
| Name | Type | Line |
|------|------|------|
| `log` | `private static Logger` | 19 |

**Methods:**
| Method | Modifier | Line |
|--------|----------|------|
| `getAllMenu(String lanCode)` | `public ArrayList<MenuBean>` | 21 |
| `getRoleMenu(ArrayList<String> arrRole, String lanCode)` | `public ArrayList<MenuBean>` | 66 |
| `saveRoleMenu(String roleId, String menuId)` | `public void` | 112 |
| `delRoleMenu(String roleId)` | `public Boolean` | 139 |

---

## Findings

A78-1 | HIGH | ManufactureDAO.java:40–58 | **Static method bypasses singleton — broken singleton pattern.** The class establishes a singleton via `getInstance()` (line 29) with a private constructor, but `getAllManufactures`, `delManufacturById`, `saveManufacturer`, `updateManufacturer`, and `isVehicleAssignedToManufacturer` are all declared `static` and can be called directly without going through the singleton. The remaining methods (`getManufactureById`, `checkManuByNm`, `getManu_type_fuel_rel`, etc.) are non-static instance methods that require an instance. This inconsistency means callers use two entirely different invocation patterns for the same class — some call `ManufactureDAO.methodName(...)` statically and others call `ManufactureDAO.getInstance().methodName(...)`. The singleton pattern provides no value and the design is incoherent.

A78-2 | CRITICAL | ManufactureDAO.java:72 | **SQL injection in `getManufactureById`.** The `id` parameter is concatenated directly into the SQL string: `"select id,name from manufacture where id = " + id`. No `PreparedStatement` is used. Although `id` is likely numeric in practice, there is no validation and the raw `Statement` approach is exploitable.

A78-3 | CRITICAL | ManufactureDAO.java:149–151 | **SQL injection in `checkManuByNm`.** Both `name` and `id` are concatenated directly into the SQL string: `"select id from manufacture where name = '" + name + "'"` and `sql += " and id !=" + id`. A `PreparedStatement` must be used for both parameters.

A78-4 | CRITICAL | ManufactureDAO.java:263 | **SQL injection in `getManu_type_fuel_rel`.** The `manuId` parameter is concatenated directly into a multi-join SQL string: `" where manu_id = " + manuId`. No `PreparedStatement` is used.

A78-5 | CRITICAL | MenuDAO.java:34–36 | **SQL injection in `getAllMenu`.** The `lanCode` parameter is embedded directly in the SQL string: `"... and lan_code = '"+lanCode+"'"`. No `PreparedStatement` is used.

A78-6 | CRITICAL | MenuDAO.java:79–82 | **SQL injection in `getRoleMenu`.** Both `Util.ArraListToString(arrRole)` (inlined into `role_id in(...)`) and `lanCode` are concatenated directly into the SQL string without parameterization. Building an `IN` clause from unsanitized list content is exploitable.

A78-7 | CRITICAL | MenuDAO.java:124 | **SQL injection in `saveRoleMenu`.** Both `roleId` and `menuId` are concatenated directly into an `INSERT` statement: `"insert into role_menu_rel (role_id,menu_id) values ("+roleId+","+menuId+")"`. A `PreparedStatement` must be used.

A78-8 | CRITICAL | MenuDAO.java:151 | **SQL injection in `delRoleMenu`.** The `roleId` parameter is concatenated directly into a `DELETE` statement: `"delete from role_menu_rel where role_id \t="+roleId"`. A `PreparedStatement` must be used.

A78-9 | HIGH | ManufactureDAO.java:83–84,126–127,159–160,199,235,362,392 | **Dual exception reporting (`InfoLogger.logException` + `e.printStackTrace()`).** Multiple catch blocks both call `InfoLogger.logException(log, e)` and then call `e.printStackTrace()`. The stack trace will be printed to `stderr` in addition to whatever the logger handles, producing duplicate output. One or the other should be used, not both.

A78-10 | HIGH | ManufactureDAO.java:408 | **`ResultSet` resource leak in `isVehicleAssignedToManufacturer`.** `rs` is declared but never added to the `finally` block. The variable is assigned at line 417 but the `finally` block (lines 424–429) only closes `ps` and the connection; `rs` is never closed, leaking a database cursor.

A78-11 | HIGH | ManufactureDAO.java:127 | **`conn.rollback()` can throw NPE.** In `delManufacturById`, if `DBUtil.getConnection(false)` itself throws (i.e., `conn` is still `null`), the catch block calls `conn.rollback()` on line 127, which will throw a `NullPointerException` and mask the original exception.

A78-12 | MEDIUM | ManufactureDAO.java:183–205 | **Connection not closed on normal exit path in `saveManufacturer`.** The `finally` block closes the connection only inside `if (null != ps)`. If `ps` is never assigned (e.g., `manufactureBean` is null and the early `return false` is reached before any PreparedStatement is created, or an exception occurs before `ps` is set), `DBUtil.closeConnection(conn)` is never called. The same structural defect appears in `updateManufacturer` (line 219–241), `checkManu_type_fuel_rel` (line 329), `saveManu_type_fuel_rel` (line 364), and `delManu_type_fuel_rel` (line 395). The connection close must be unconditional in the `finally` block.

A78-13 | MEDIUM | ManufactureDAO.java:102 | **Misleading log message in `delManufacturById`.** The log reads `"Inside LoginDAO Method : delManufacturById"` but the class is `ManufactureDAO`. The same copy-paste error appears in `checkManuByNm` (line 141), `saveManufacturer` (line 178), `updateManufacturer` (line 214), `getManu_type_fuel_rel` (line 252), `checkManu_type_fuel_rel` (line 296), `saveManu_type_fuel_rel` (line 339), and `delManu_type_fuel_rel` (line 377). All log messages in `ManufactureDAO` that reference "LoginDAO" are incorrect.

A78-14 | MEDIUM | MenuDAO.java:26 | **Misleading log message in `getAllMenu`.** The log reads `"Inside TimezoneDAO Method : getAllMenu"` but the class is `MenuDAO`. The same error appears in `getRoleMenu` (line 71). Both should reference `MenuDAO`.

A78-15 | MEDIUM | ManufactureDAO.java:27–35 | **Singleton `getInstance()` is dead code.** The singleton infrastructure (`theInstance`, `getInstance()`, private constructor) exists, yet the methods that callers would use are predominantly `static` and do not use the instance. The instance methods (`getManufactureById`, `checkManuByNm`, etc.) could be made static like the rest, and the singleton infrastructure removed entirely, or all methods should become instance methods accessed through the singleton. In its current state `getInstance()` is never needed to call any method.

A78-16 | MEDIUM | ManufactureDAO.java:66 | **Raw diamond type with explicit type argument.** `new ArrayList<ManufactureBean>()` is used in several places in `getManufactureById` and elsewhere; this is fine, but the return type declares `ArrayList<ManufactureBean>` where the interface `List` is already used in `getAllManufactures`. Return type inconsistency (`ArrayList` vs `List`) across methods in the same class leaks the concrete implementation type unnecessarily.

A78-17 | MEDIUM | MenuDAO.java:3 | **Unused import.** `java.lang.reflect.Array` is imported but never referenced anywhere in `MenuDAO.java`. This import should be removed.

A78-18 | MEDIUM | MenuDAO.java:117 | **`ResultSet rs` declared but never written in `saveRoleMenu`.** The variable `rs` is declared (line 117) and closed in the `finally` block (line 133), but `saveRoleMenu` never executes a query and `rs` is never assigned. The `rs.close()` in the `finally` block is guarded by `null != rs` so no NPE occurs, but the variable declaration is dead code that misleads the reader.

A78-19 | LOW | ManufactureDAO.java:410 | **`Integer` used instead of `int` for a local counter.** `Integer count = 0;` in `isVehicleAssignedToManufacturer` (line 410) uses the boxed type unnecessarily. It is used only in a comparison `count > 0` where auto-unboxing occurs. A plain `int` is sufficient and avoids any potential auto-unbox NPE risk.

A78-20 | LOW | ManufactureDAO.java:143 | **Typo in local variable name.** `boolean exsit = false;` in `checkManuByNm` (line 143) — the variable name should be `exist`.

A78-21 | LOW | MenuDAO.java:149 | **Tab character embedded in SQL string literal.** The delete statement `"delete from role_menu_rel where role_id \t="+roleId` contains a literal tab character between `role_id` and `=`. While harmless in SQL, it indicates copy-paste or accidental keystroke and should be a regular space.
# P4 Agent A79 — QuestionDAO, ResultDAO, RoleDAO

## Reading Evidence

### QuestionDAO.java

**Class:** `QuestionDAO` (non-final, instantiable)

**Fields / Constants:**
| Name | Line | Type | Notes |
|---|---|---|---|
| `log` | 26 | `static Logger` | Initialized via `InfoLogger.getLogger("com.dao.QuesionDAO")` — note typo in logger name |
| `unitDao` | 28 | `UnitDAO` | Instance field, assigned `UnitDAO.getInstance()` |

**Methods:**
| Method | Line | Static | Visibility |
|---|---|---|---|
| `getQuesLanId(String compId)` | 30 | no | public |
| `getQuestionByUnitId(String unitId, String attchId, String compId, boolean barcode)` | 64 | no | public |
| `getQuestionByCategory(String manuId, String typeId, String fuelTypeId, String attchId, String compId)` | 128 | yes | public static |
| `delQuestionById(String id)` | 174 | yes | public static |
| `hideQuestionById(String id, String manuId, String typeId, String fuleTypeId, String compId, String attchId)` | 197 | yes | public static |
| `showQuestionById(String id)` | 210 | yes | public static |
| `copyQuestionToCompId(String id, String manuId, String typeId, String fuleTypeId, String compId, String attchId)` | 216 | yes | private static |
| `getQuestionById(String id)` | 263 | yes | public static |
| `getQuestionContentById(String qId, String lanId)` | 311 | no | public |
| `saveQuestionInfo(QuestionBean questionBean, String lanId, int compId)` | 363 | yes | public static |
| `saveQuestionContent(QuestionContentBean qeustionContentBean)` | 436 | yes | public static |
| `updateQuestionInfo(QuestionBean questionBean)` | 516 | yes | public static |
| `getMaxQuestionId(String manuId, String typeId, String fuelTypeId, String compId)` | 555 | yes | public static |
| `getAllAnswerType()` | 595 | yes | public static |

---

### ResultDAO.java

**Class:** `ResultDAO` (non-final, instantiable)

**Fields / Constants:**
| Name | Line | Type | Notes |
|---|---|---|---|
| `log` | 18 | `static Logger` | Initialized via `InfoLogger.getLogger("com.dao.ResultDAO")` |

**Methods:**
| Method | Line | Static | Visibility |
|---|---|---|---|
| `saveResult(ResultBean resultBean, String compId)` | 20 | no | public |
| `countResultsCompletedToday(Long compId, String timezone)` | 124 | no | public |
| `getPreOpsCheckReport(Long compId, PreOpsReportFilterBean filter, String dateFormat, String timezone)` | 128 | no | public |
| `getChecklistResultInc(Long driverId, Date sDate, Date eDate)` | 132 | no | public |
| `getChecklistResultById(int resultId)` | 166 | no | public |
| `getOverallStatus(Long resultId, String unitId)` | 202 | no | public |
| `printErrors(Long resultId, boolean pdfTag)` | 245 | no | public |
| `checkDuplicateResult(String driverId, String unitId, Timestamp time)` | 283 | no | public |

---

### RoleDAO.java

**Class:** `RoleDAO` (non-final, instantiable)

**Fields / Constants:**
| Name | Line | Type | Notes |
|---|---|---|---|
| `log` | 17 | `static Logger` | Initialized via `InfoLogger.getLogger("com.dao.RoleDAO")` |

**Methods:**
| Method | Line | Static | Visibility |
|---|---|---|---|
| `getRoles()` | 19 | no | public |

---

## Findings

A79-1 | CRITICAL | QuestionDAO.java:42 | **SQL Injection — `getQuesLanId`**: `compId` is interpolated directly into the SQL string: `"select lan_id from company where id = " + compId`. This string parameter is not validated before concatenation; a malicious caller could pass arbitrary SQL. Use a `PreparedStatement` with a parameter placeholder instead.

A79-2 | CRITICAL | QuestionDAO.java:82-94 | **SQL Injection — `getQuestionByUnitId`**: Multiple caller-supplied parameters (`unitId`, `compId`, `attchId`, `lanId`) are interpolated directly into the SQL string via string concatenation. No sanitization is applied. Use a `PreparedStatement`.

A79-3 | CRITICAL | QuestionDAO.java:183 | **SQL Injection — `delQuestionById`**: `id` (a `String` parameter) is concatenated into a DELETE statement: `"delete from question where id=" + id`. Should use a `PreparedStatement`.

A79-4 | CRITICAL | QuestionDAO.java:275 | **SQL Injection — `getQuestionById`**: `id` is concatenated into the SELECT: `"select id,content,... from question where id = " + id`. Should use a `PreparedStatement`.

A79-5 | CRITICAL | ResultDAO.java:145 | **SQL Injection — `getChecklistResultInc`**: `driverId`, `sDate`, and `eDate` are all concatenated directly into the SQL string. `sDate` and `eDate` are `java.util.Date` objects whose `.toString()` output is used verbatim in the query. Use parameterized queries.

A79-6 | CRITICAL | ResultDAO.java:179 | **SQL Injection — `getChecklistResultById`**: `resultId` (an `int`) is concatenated into the SQL. While an `int` type reduces exploitability, the pattern is inconsistent with the rest of the codebase where `PreparedStatement` is used, and the method should still use a placeholder.

A79-7 | CRITICAL | ResultDAO.java:61,85,113 | **SQL Injection in rollback/cleanup paths — `saveResult`**: The cleanup DELETE statements `"delete from result where id = " + result_id` use concatenation, and `result_id` is an `int` (lower direct risk) but the inline-SQL-in-catch pattern is unsafe and leaks DAO internals into error handling.

A79-8 | CRITICAL | ResultDAO.java:74 | **SQL Injection — `saveResult` answer insert**: The `content` string retrieved from the database is concatenated back into a second SQL string: `"...'" + content + "',..."`. A stored value containing a single quote would break the query and could be exploited as a second-order SQL injection. Use a `PreparedStatement` parameter for `content`.

A79-9 | CRITICAL | ResultDAO.java:91 | **SQL Injection — `saveResult` answer_type lookup**: `answer.getQuesion_id()` is concatenated directly into a SELECT: `"select answer_type.name from question,answer_type where question.id =" + answer.getQuesion_id() + ...`. Use a `PreparedStatement`.

A79-10 | CRITICAL | ResultDAO.java:214,225 | **SQL Injection — `getOverallStatus`**: Both SQL strings concatenate `resultId` (a `Long`). While `Long` is not directly exploitable, consistency and safety require parameterized queries.

A79-11 | CRITICAL | ResultDAO.java:259 | **SQL Injection — `printErrors`**: `resultId` is concatenated into the SQL string.

A79-12 | CRITICAL | ResultDAO.java:294-295 | **SQL Injection — `checkDuplicateResult`**: `driverId`, `unitId`, and `time` (a `java.sql.Timestamp` whose `.toString()` is used) are all concatenated into the SQL string. Use a `PreparedStatement`.

A79-13 | HIGH | QuestionDAO.java:26 | **Typo in logger category name**: The logger is registered as `"com.dao.QuesionDAO"` (missing the `t` in `Question`). This means log output will appear under a misspelled category, making filtering by class name unreliable and potentially silencing log appenders configured for the correct name.

A79-14 | HIGH | QuestionDAO.java:254-257 | **Resource leak in `copyQuestionToCompId` finally block**: The `conn` is only closed inside the `if (null != ps)` guard. If `ps` is never assigned (i.e., an exception is thrown before `conn.prepareStatement(...)` is called), `conn` will not be closed. The connection close must occur unconditionally in `finally`, independent of the `ps` null check. The same pattern exists in `updateQuestionInfo` (line 547-550).

A79-15 | HIGH | QuestionDAO.java:547-550 | **Resource leak in `updateQuestionInfo` finally block**: Same issue as A79-14 — `DbUtils.closeQuietly(conn)` is nested inside `if (null != ps)`. If `conn.prepareStatement(...)` throws before `ps` is assigned, the connection leaks.

A79-16 | HIGH | QuestionDAO.java:376 | **Incorrect use of sequence in `saveQuestionInfo`**: `"select nextval('question_id_seq') from question"` appends `FROM question`, meaning the sequence is advanced once per existing row rather than once. The correct PostgreSQL idiom is `SELECT nextval('question_id_seq')` with no `FROM` clause. This can exhaust the sequence rapidly and cause ID collisions if the `question` table is empty (returning zero rows means `id` stays at the default of `1`).

A79-17 | HIGH | ResultDAO.java:113-114 | **Exception swallowed and no re-throw in `saveResult` catch block**: The catch block performs a compensating DELETE, logs, and returns `0`. It does not re-throw. Callers receive `0` for both "duplicate result" (line 54) and "unexpected exception" paths with no way to distinguish them, masking errors.

A79-18 | MEDIUM | QuestionDAO.java:30-62 | **Inconsistent static/instance method design**: Most methods on `QuestionDAO` are `static` and use no instance state, yet the class is instantiable and is instantiated by `ResultDAO` (line 27, line 212) purely to call the instance method `getQuesLanId`. `getQuesLanId` itself uses no instance state and should be `static`, eliminating the need for instantiation. The `unitDao` instance field (line 28) is only used by `getQuestionByUnitId`, which is the sole instance method calling it — all others are static.

A79-19 | MEDIUM | QuestionDAO.java:35,69,177,267,316,369,442,521,560,600 | **Misleading log messages throughout `QuestionDAO`**: Most methods log `"Inside LoginDAO Method : <methodName>"` instead of `"Inside QuestionDAO Method : <methodName>"`. This makes log-based diagnostics misleading. Only `getQuestionByCategory` (line 129) and `copyQuestionToCompId` (line 221) use the correct DAO name.

A79-20 | MEDIUM | ResultDAO.java:29 | **Misleading log message in `saveResult`**: Logs `"Inside LoginDAO Method : saveResult"` rather than `"Inside ResultDAO Method : saveResult"`.

A79-21 | MEDIUM | ResultDAO.java:136,170 | **Misleading log messages in `ResultDAO`**: `getChecklistResultInc` logs `"Inside LoginDAO Method : getChecklistResultInc"` and `getChecklistResultById` logs `"Inside LoginDAO Method : getChecklistResult"` — both should reference `ResultDAO`.

A79-22 | MEDIUM | RoleDAO.java:23 | **Misleading log message in `getRoles`**: Logs `"Inside LoginDAO Method : getRoles"` — should reference `RoleDAO`.

A79-23 | MEDIUM | QuestionDAO.java:436 | **Typo in parameter name `qeustionContentBean`**: The parameter is spelled `qeustionContentBean` throughout `saveQuestionContent`. This propagates into the method body and is a maintenance hazard.

A79-24 | MEDIUM | QuestionDAO.java:559 | **Declared but never used local variable `ps` in `getMaxQuestionId`**: `PreparedStatement ps` is declared at line 559 as a field-like local but is assigned inline at line 571 without being declared `null` first, and is never closed in the `finally` block. This is a resource leak — the `PreparedStatement` created on line 571 is not closed.

A79-25 | MEDIUM | ResultDAO.java:56 | **Non-standard variable name casing `ArrAnswer`**: The local variable is named `ArrAnswer` (PascalCase), violating Java naming conventions for local variables. Should be `arrAnswer`.

A79-26 | MEDIUM | ResultDAO.java:149,185 | **Non-standard variable name casing `Resultbean`**: Local variables `Resultbean` use PascalCase in both `getChecklistResultInc` (line 149) and `getChecklistResultById` (line 185). Should be `resultBean`.

A79-27 | MEDIUM | QuestionDAO.java:340 | **Magic string `" "` (single space) returned as fallback content**: In `getQuestionContentById`, when no content is found, an `XmlBean` is added with `name` set to `" "` (a single space). Callers cannot reliably distinguish "no content found" from a legitimate single-space value. A `null` or empty string, or a domain-level exception, would be clearer.

A79-28 | MEDIUM | RoleDAO.java:25 | **Raw type use — `new ArrayList<RoleBean>()`**: While the diamond operator is used in nearby DAOs (e.g., `QuestionDAO` uses `new ArrayList<>()`), `RoleDAO` uses the explicit type argument `new ArrayList<RoleBean>()` which is not a raw type per se but is inconsistent with the modern diamond style used elsewhere, and line 46-47 puts close calls on single lines without braces — style inconsistency noted below.

A79-29 | LOW | RoleDAO.java:46-48 | **Inconsistent brace style and spacing**: The `finally` block uses single-line `if` statements without braces (`if(null != rs) {rs.close();}`) in contrast to the multi-line brace style used in `QuestionDAO` and `ResultDAO`. Spacing around `=` and `(` also differs (e.g., `conn=DBUtil.getConnection()` vs. `conn = DBUtil.getConnection()` in other DAOs).

A79-30 | LOW | RoleDAO.java:48 | **Inconsistent connection-closing utility**: `RoleDAO.getRoles()` closes the connection using `DBUtil.closeConnection(conn)`, while every other DAO uses `DbUtils.closeQuietly(conn)` from Apache Commons. This is a leaky abstraction — `DBUtil.closeConnection` is a custom wrapper whose null-safety and exception-suppression behavior may differ from the library utility.

A79-31 | LOW | QuestionDAO.java:153 | **Inline comment states obvious**: `// Set the parameters twice since we have conditionStr 2 times in the query` references `conditionStr`, a variable name that does not exist in this method (the variable is `whereBuilder`). The comment is stale/copy-pasted from a prior refactoring.

A79-32 | LOW | ResultDAO.java:41,144,178,293 | **`//noinspection SqlResolve` suppression annotations**: Four SQL strings are annotated to suppress IDE SQL resolution warnings. While this is not a build error, it indicates the IDE cannot verify the SQL schema references, which silently bypasses a layer of static analysis. These should be removed if unnecessary or the schema references resolved.

A79-33 | LOW | QuestionDAO.java:447 | **`String sql = ""`**: Initializing `sql` to an empty string rather than `null` can hide cases where neither branch assigns `sql` before use; however in this method all branches do assign it, so the risk is low. The `stmt` created at line 446 is also opened but never used in this method (only `ps` is used after the initial branch), representing a wasted resource allocation.

A79-34 | LOW | QuestionDAO.java:446 | **Unused `Statement stmt` in `saveQuestionContent`**: A `Statement` object is created via `conn.createStatement(...)` at line 446 but is never used in the method body (all queries use `PreparedStatement ps`). It consumes a database cursor and is closed in `finally`, but its creation is entirely superfluous.
# P4 Agent A80 — SessionDAO, SubscriptionDAO, TimezoneDAO

## Reading Evidence

### SessionDAO.java
- **Class:** `SessionDAO` (package `com.dao`)
- **Fields/Constants:** none
- **Methods:**
  - `getSessions(int companyId, SessionFilterBean filter, String dateFormat, String timezone) : SessionReportBean` — lines 10–15 (public static)

---

### SubscriptionDAO.java
- **Class:** `SubscriptionDAO` (package `com.dao`)
- **Fields/Constants:**
  - `private static Logger log` — line 22
- **Methods:**
  - `getAllReport(ArrayList<String> frequencies) : ArrayList<SubscriptionBean>` — lines 24–84 (public instance)
  - `checkCompFleetAlert(String comId) : String` — lines 87–120 (public instance)
  - `saveDefualtSubscription(int compId) : boolean` — lines 122–151 (public instance)
  - `getSubscriptionByName(final String name) : SubscriptionBean` — lines 154–170 (public static)

---

### TimezoneDAO.java
- **Class:** `TimezoneDAO` (package `com.dao`)
- **Fields/Constants:**
  - `private static Logger log` — line 17
  - `private static TimezoneDAO theInstance` — line 19
- **Methods:**
  - `getInstance() : TimezoneDAO` — lines 21–31 (public static, double-checked locking singleton)
  - `TimezoneDAO()` — lines 33–35 (private constructor)
  - `getAllTimezone() : ArrayList<TimezoneBean>` — lines 37–76 (public instance)
  - `getAll() : List<TimezoneBean>` — lines 78–117 (public static)
  - `getTimezone(int tzoneId) : TimezoneBean` — lines 119–158 (public static)

---

## Findings

A80-1 | HIGH | SubscriptionDAO.java:39 | SQL injection via string concatenation in `getAllReport`. The `frequencies` list elements are interpolated directly into the SQL string (`extra += " frequency = '" + frequencies.get(i) + "' or"`). A caller-supplied frequency value is embedded without sanitisation or parameterisation. A `PreparedStatement` with `IN (?, ?, …)` should be used instead.

A80-2 | HIGH | SubscriptionDAO.java:99 | SQL injection via string concatenation in `checkCompFleetAlert`. The parameter `comId` is declared as `String` and concatenated directly into the query: `"... and c.comp_id ='" + comId + "'"`. A parameterised query is required.

A80-3 | HIGH | TimezoneDAO.java:133 | SQL injection via string concatenation in `getTimezone`. The integer parameter `tzoneId` is concatenated directly: `"... where id=" + tzoneId`. Although typed as `int` this is still unsafe style; `PreparedStatement` with `setInt` should be used consistently.

A80-4 | MEDIUM | SubscriptionDAO.java:51 | Hardcoded `LIMIT 1` in `getAllReport`. The method name and signature suggest it returns all matching subscriptions (`ArrayList<SubscriptionBean>`), but the query silently constrains results to one row. This is a logic error / leaky abstraction — callers receive a list but will always get at most one element with no indication that truncation has occurred.

A80-5 | MEDIUM | SubscriptionDAO.java:166 | Wrong exception type used in `getSubscriptionByName`. When the subscription is not found the code throws `new EntityNotFoundException(DriverBean.class, name)` — passing `DriverBean.class` instead of `SubscriptionBean.class`. This will produce misleading error messages at runtime.

A80-6 | MEDIUM | TimezoneDAO.java:78-117 | `getAll()` is a near-exact duplicate of `getAllTimezone()` (lines 37–76). Both execute identical SQL, build the same list, and share the same log message ("Inside TimezoneDAO Method : getAllTimezone"). The only differences are that `getAll()` is `static` (bypassing the singleton) and returns `List` instead of `ArrayList`. This dead/duplicated code should be consolidated; one method should delegate to the other.

A80-7 | MEDIUM | SubscriptionDAO.java:131 | `saveDefualtSubscription` opens a `Statement` with `ResultSet.TYPE_SCROLL_SENSITIVE` / `ResultSet.CONCUR_READ_ONLY` cursor settings even though the method performs only an `INSERT` (no `ResultSet` is ever used). The `ResultSet rs` variable is declared and null-checked in the `finally` block but is never assigned, meaning the `finally` close for `rs` is dead code. A plain `conn.createStatement()` is appropriate here.

A80-8 | LOW | SubscriptionDAO.java:127 | Typo in public API: method name `saveDefualtSubscription` misspells "Default" as "Defualt". Because this is a public method it forms part of the external API and the spelling error will propagate to all callers.

A80-9 | LOW | SubscriptionDAO.java:29 | Copy-paste log message: `getAllReport` logs `"Inside LoginDAO Method : getAllReport"` (says "LoginDAO", not "SubscriptionDAO"). Same issue in `checkCompFleetAlert` line 92 and `saveDefualtSubscription` line 127 — all three instance methods identify themselves as being inside `LoginDAO`.

A80-10 | LOW | SubscriptionDAO.java:31 | Raw-type diamond on `new ArrayList<SubscriptionBean>()` should use the diamond operator `<>` (Java 7+). Same pattern repeated at lines 58, 65. Minor build warning.

A80-11 | LOW | TimezoneDAO.java:45 | Raw-type diamond: `new ArrayList<TimezoneBean>()` should use `<>`. Same issue at lines 86 (in `getAll`).

A80-12 | LOW | SubscriptionDAO.java:72 | Double exception reporting: `e.printStackTrace()` is called after `InfoLogger.logException(log, e)` in every `catch` block across `getAllReport` (line 72), `checkCompFleetAlert` (line 108), and `saveDefualtSubscription` (line 140). The same pattern appears in `TimezoneDAO` (lines 66–67, 107–108, 148–149). `printStackTrace` emits to `stderr` bypassing the logging framework and should be removed.

A80-13 | LOW | TimezoneDAO.java:19 | Singleton field `theInstance` is not declared `volatile`. The double-checked locking pattern used in `getInstance()` (lines 21–31) requires `volatile` on the field to be correct under the Java Memory Model; without it the partially-constructed instance can be observed by other threads.

A80-14 | INFO | TimezoneDAO.java:37 | `getAllTimezone()` is a public instance method on a singleton class, while `getAll()` and `getTimezone()` are static. The mixed instance/static access pattern is inconsistent and makes it unclear whether the singleton lifecycle is meaningful for this class at all.

A80-15 | INFO | SubscriptionDAO.java:24 | `getAllReport`, `checkCompFleetAlert`, and `saveDefualtSubscription` are instance methods, but `getSubscriptionByName` (line 154) is static. `SessionDAO.getSessions` (SessionDAO.java:10) is also static with no instance state. The mixing of instance and static method styles across and within these DAO classes is inconsistent.
# P4 Agent A81 — TrainingDAO, UnitDAO

## Reading Evidence

### TrainingDAO.java

**Class:** `com.dao.TrainingDAO`

**Fields/Constants:**
- `private static Logger log` (line 21) — Log4j logger instance

**Methods:**
| Method | Lines |
|--------|-------|
| `getTrainingByDriver(Long driverId, String dateFormat)` | 23–53 |
| `addTraining(DriverTrainingBean trainingBean, String dateFormat)` | 55–68 |
| `deleteTraining(Long trainingId)` | 70–74 |
| `sendTrainingExpiryDailyEmail()` | 76–117 |
| `sendTrainingExpiryWeeklyEmail()` | 119–169 |

---

### UnitDAO.java

**Class:** `com.dao.UnitDAO`

**Fields/Constants:**
| Name | Lines |
|------|-------|
| `private static Logger log` | 23 |
| `private static UnitDAO theInstance` | 24 |
| `private static final String INSERT_UNIT_ASSIGNMENT` | 48–50 |
| `private static final String DELETE_UNIT_ASSIGNMENT` | 78 |
| `private static final String QUERY_ASSIGN_DATE_OVERLAP_CHECK` | 91–96 |
| `private static final String QUERY_COUNT_UNIT_BY_NAME` | 116–117 |
| `private static final String QUERY_COUNT_UNIT_BY_SERIAL_NO` | 146–147 |
| `private static final String QUERY_COUNT_UNIT_BY_MAC_ADDRESS` | 179–180 |
| `private static final String INSERT_UNIT_INFO` | 438–440 |
| `private static final String UPDATE_UNIT` | 467–470 |
| `private static final String UPDATE_UNIT_ACCESS` | 513–515 |
| `private static final String QUERY_IMPACT_BY_UNIT` | 817–820 |

**Methods:**
| Method | Lines |
|--------|-------|
| `getInstance()` | 26–35 |
| `UnitDAO()` (private constructor) | 37–38 |
| `getAssignments(String sessCompId, String equipId, String dateFormat)` | 40–46 |
| `addAssignment(String subCompanyId, String unitId, String startDate, String endDate, String dateFormat)` | 52–76 |
| `deleteAssignment(String id)` | 80–89 |
| `isAssignmentOverlapping(String unitId, Date startDate, Date endDate)` | 98–114 |
| `checkUnitByNm(String compId, String name, String id, boolean activeStatus)` | 119–144 |
| `checkUnitBySerial(String serialNo, String id, boolean activeStatus, String compId)` | 149–177 |
| `checkUnitByMacAddr(String macAddr, String id)` | 182–197 |
| `getUnitBySerial(String serial_no, Boolean activeStatus)` | 199–240 |
| `getAllUnitsByCompanyId(int compId)` | 242–250 |
| `getUnitMaxId()` | 252–286 |
| `getUnitById(String id)` | 288–291 |
| `getUnitNameByComp(String compId, Boolean activeStatus)` | 293–338 |
| `delUnitById(String id)` | 340–362 |
| `getAllUnitType()` | 364–399 |
| `getAllUnitFuelType()` | 401–436 |
| `saveUnitInfo(UnitBean unitbean)` | 442–465 |
| `updateUnitInfo(UnitBean unitbean)` (private) | 472–511 |
| `saveUnitAccessInfo(UnitBean unitbean)` | 517–528 |
| `getTotalUnitByID(String id, Boolean activeStatus)` | 530–571 |
| `getAllUnitAttachment()` | 573–608 |
| `getType(String manu_id)` | 610–651 |
| `getPower(String manu_id, String type_id)` | 653–697 |
| `saveService(ServiceBean bean)` | 699–759 |
| `getServiceByUnitId(String unitId)` | 761–815 |
| `getImpactByUnitId(Long unitId)` | 822–831 |
| `getChecklistSettings(String unitId)` | 833–873 |
| `resetCalibration(int equipId)` | 875–877 |
| `updateChecklistSettings(ChecklistBean bean)` | 879–907 |
| `getSessionHoursCalilbration(String reset_cal_date, String equipId)` | 909–956 |
| `getAllUnitSearch(String compId, Boolean activeStatus, String searchUnit)` | 958–965 |

---

## Findings

A81-1 | HIGH | TrainingDAO.java:20 | No DAO interface. `TrainingDAO` is a concrete class with no interface, violating the repository/DAO abstraction pattern. Callers are coupled directly to the implementation, making substitution or testing impossible without subclassing.

A81-2 | HIGH | UnitDAO.java:22 | No DAO interface. `UnitDAO` is a concrete singleton with no interface. Same leaky-abstraction problem as TrainingDAO — callers must depend on the concrete class.

A81-3 | HIGH | UnitDAO.java:212 | SQL injection vulnerability in `getUnitBySerial`: the `serial_no` parameter is interpolated directly into the SQL string (`"where serial_no = '" + serial_no + "'"`) using `Statement.executeQuery` instead of a `PreparedStatement`. Any caller-controlled value can manipulate the query.

A81-4 | HIGH | UnitDAO.java:311 | SQL injection vulnerability in `getUnitNameByComp`: `compLst` (derived from `compId` or `cDAO.getSubCompanyLst(compId)`) is concatenated directly into the SQL string without parameterisation.

A81-5 | HIGH | UnitDAO.java:349 | SQL injection vulnerability in `delUnitById`: the `id` parameter is concatenated directly into the UPDATE statement (`"where id=" + id`) using a raw `Statement`.

A81-6 | HIGH | UnitDAO.java:548 | SQL injection vulnerability in `getTotalUnitByID`: `compLst` is concatenated into the SQL string without parameterisation, same pattern as A81-4.

A81-7 | HIGH | UnitDAO.java:627–628 | SQL injection vulnerability in `getType`: `manu_id` is concatenated directly into the SELECT (`"where manu_id = " + manu_id`) after only an empty-string-to-"0" substitution, which provides no sanitisation against injection.

A81-8 | HIGH | UnitDAO.java:667–670 | SQL injection vulnerability in `getPower`: both `manu_id` and `type_id` are concatenated directly into the SQL string without parameterisation.

A81-9 | MEDIUM | TrainingDAO.java:76 | Inconsistent whitespace in method signature: `public  void sendTrainingExpiryDailyEmail()` has a double space between `public` and `void`. Minor but indicative of inconsistent editing.

A81-10 | MEDIUM | TrainingDAO.java:80 | Lambda parameter named `UserCompRelBean` (line 80, repeated at line 124) shadows the type name `UserCompRelBean`. The parameter should follow camelCase convention (e.g., `compRel` or `userCompRelBean`). This causes a compiler/IDE warning and reduces readability.

A81-11 | MEDIUM | TrainingDAO.java:107–114 | Exception swallowing inside `forEach` lambdas in both `sendTrainingExpiryDailyEmail` and `sendTrainingExpiryWeeklyEmail`: `SQLException`, `AddressException`, and `MessagingException` are caught and only `e.printStackTrace()` is called — the comment `// TODO Auto-generated catch block` was never addressed. Errors are silently discarded; the outer method does not learn that email sending failed for a given company.

A81-12 | MEDIUM | UnitDAO.java:203 | Misleading log message in `getUnitBySerial`: `log.info("Inside LoginDAO Method : getUnitBySerial")` — the log string says "LoginDAO" but this is `UnitDAO`. This copy-paste error appears throughout the file (see also lines 256, 289, 297, 343, 368, 405, 443, 478, 534, 577, 614, 657) making log-based diagnostics unreliable.

A81-13 | MEDIUM | UnitDAO.java:40–114 | Mixed static/instance methods on a singleton. `getAssignments`, `addAssignment`, `deleteAssignment`, `isAssignmentOverlapping`, `getAllUnitsByCompanyId`, `getUnitById`, `getAllUnitType`, `saveUnitAccessInfo`, `getTotalUnitByID` are declared `public static` while other methods are instance methods — yet the class implements the singleton pattern. This is incoherent: static callers bypass the singleton contract, and the mixture makes the API confusing.

A81-14 | MEDIUM | UnitDAO.java:43–44 | `Long.valueOf(sessCompId)` and `Long.valueOf(equipId)` (and many similar conversions throughout the file) produce autoboxed values that are immediately unboxed, generating compiler warnings about unnecessary boxing/unboxing. The idiomatic replacement is `Long.parseLong(...)`.

A81-15 | MEDIUM | UnitDAO.java:909 | Method name `getSessionHoursCalilbration` contains a typo ("Calilbration" instead of "Calibration"). This is a public API misspelling.

A81-16 | MEDIUM | UnitDAO.java:347 | In `delUnitById`, the `Statement` is created with `ResultSet.TYPE_SCROLL_SENSITIVE, ResultSet.CONCUR_READ_ONLY` cursor flags (line 347) but is only used to execute an UPDATE — the flags are pointless and misleading.

A81-17 | LOW | TrainingDAO.java:94 | Typo in user-facing email content: "revoked" is spelled correctly but "vechile" should be "vehicle". This appears in the daily expiry alert email body.

A81-18 | LOW | TrainingDAO.java:91 | Locale/region detection uses `timezone.contains("US/")` and `timezone.contains("Canada/")` to toggle between "training" and "licence". This is a fragile heuristic embedded in a DAO method — locale logic does not belong in the data-access layer.

A81-19 | LOW | UnitDAO.java:788–792 | Silent data normalisation in `getServiceByUnitId`: the database value `"setDur"` is silently remapped to `"setIntval"` on read. No comment explains the business reason. This hidden transformation can confuse future maintainers and indicates an inconsistency between stored and expected values that should be resolved at the database or mapping layer.

A81-20 | LOW | UnitDAO.java:262 | `getUnitMaxId` computes `max(id) + 1` and returns it as a suggested next ID (line 268: `count = rs.getInt(1) + 1`). This is a race-condition-prone ID generation strategy; two concurrent callers can receive the same "next" ID. The log message also says "Inside LoginDAO Method : getAllUnit" which is wrong on both counts (class and method name).

A81-21 | LOW | UnitDAO.java:3 | Wildcard import `com.bean.*` obscures exactly which bean types are used. All other imports in the file are explicit.
# P4 Agent A82 — CDL, Cookie, CookieList

## Reading Evidence

### CDL.java
- **Class:** `CDL` (package `com.json`)
- **Fields/Constants:** None
- **Methods:**
  - `getValue(JSONTokener x)` — private static, line 55
  - `rowToJSONArray(JSONTokener x)` — public static, line 95
  - `rowToJSONObject(JSONArray names, JSONTokener x)` — public static, line 131
  - `rowToString(JSONArray ja)` — public static, line 144
  - `toJSONArray(String string)` — public static, line 181
  - `toJSONArray(JSONTokener x)` — public static, line 192
  - `toJSONArray(JSONArray names, String string)` — public static, line 204
  - `toJSONArray(JSONArray names, JSONTokener x)` — public static, line 217
  - `toString(JSONArray ja)` — public static, line 245
  - `toString(JSONArray names, JSONArray ja)` — public static, line 265

### Cookie.java
- **Class:** `Cookie` (package `com.json`)
- **Fields/Constants:** None
- **Methods:**
  - `escape(String string)` — public static, line 47
  - `toJSONObject(String string)` — public static, line 81
  - `toString(JSONObject jo)` — public static, line 118
  - `unescape(String string)` — public static, line 150

### CookieList.java
- **Class:** `CookieList` (package `com.json`)
- **Fields/Constants:** None
- **Methods:**
  - `toJSONObject(String string)` — public static, line 49
  - `toString(JSONObject jo)` — public static, line 71

---

## Findings

A82-1 | HIGH | CDL.java:1, Cookie.java:1, CookieList.java:1 | Vendored third-party source. All three files carry the copyright notice "Copyright (c) 2002 JSON.org", are attributed "@author JSON.org", and are versioned "@version 2010-12-24". They are verbatim copies of the org.json reference implementation. The correct approach is to declare `org.json:json` (or a newer equivalent such as `com.fasterxml.jackson`) as a Maven/Gradle dependency and delete these source files. Keeping vendored copies of a third-party library prevents receiving upstream security patches and inflates the owned-code surface.

A82-2 | MEDIUM | CDL.java:58, CDL.java:68, CDL.java:145, CDL.java:270, Cookie.java:50, Cookie.java:119, Cookie.java:152, CookieList.java:75 | `StringBuffer` used instead of `StringBuilder`. `StringBuffer` is thread-synchronized but these are local variables with no shared-state requirement. Every instance should be `StringBuilder` for correct modern Java idiom and marginally better performance. This is characteristic of code that has not been updated since Java 1.4 era (consistent with the 2010 version date).

A82-3 | MEDIUM | CookieList.java:73 | Raw type `Iterator` used without a generic type parameter (`Iterator keys = jo.keys()`). This will produce an "unchecked or unsafe operations" compiler warning. The variable should be typed as `Iterator<String>` if the `keys()` method supports it, or the result cast explicitly and the warning suppressed with justification.

A82-4 | LOW | CDL.java:55 | `@throws JSONException` listed in Javadoc for `getValue` but the exception type is not in the method throws clause in a way that could be inferred; the broader issue is that all three Javadoc `@throws` tags across the files omit a description string (e.g., `@throws JSONException` with no explanation of the condition). This is a minor documentation quality issue inherited from the upstream source.

A82-5 | LOW | Cookie.java:56-57 | Cast `(char)((c >>> 4) & 0x0f)` passed to `Character.forDigit(int digit, int radix)`. The first parameter of `Character.forDigit` is `int`; the explicit `(char)` cast is unnecessary and potentially confusing. This is a style issue from the original org.json source.

A82-6 | INFO | CDL.java:105 | Trailing whitespace on line 105 (`for (;;) {` followed by spaces). Minor style issue.
# P4 Agent A83 — HTTP, HTTPTokener, JSONArray

## Reading Evidence

### HTTP.java
- **Class:** `HTTP` (public, no-instance-constructor utility class)
- **Package:** `com.json`
- **License header:** JSON.org MIT-style license, copyright 2002, version 2010-12-24
- **Fields/Constants:**
  - `public static final String CRLF = "\r\n"` (line 37)
- **Methods:**
  - `public static JSONObject toJSONObject(String string) throws JSONException` — line 71
  - `public static String toString(JSONObject jo) throws JSONException` — line 127
- **Imports:** `java.util.Iterator`
- **Notes:** Uses raw `Iterator` (line 128). Uses `StringBuffer` instead of `StringBuilder` (line 130). Inline section labels (`// Response`, `// Request`, `// Fields`) appear on lines 79, 88, 95 — these are navigational comments, not commented-out code.

---

### HTTPTokener.java
- **Class:** `HTTPTokener extends JSONTokener` (public)
- **Package:** `com.json`
- **License header:** JSON.org MIT-style license, copyright 2002, version 2010-12-24
- **Fields/Constants:** None declared directly (inherits from `JSONTokener`)
- **Methods:**
  - `public HTTPTokener(String string)` — line 39
  - `public String nextToken() throws JSONException` — line 49
- **Notes:** Uses `StringBuffer` (line 52) instead of `StringBuilder`. No raw types, no commented-out code.

---

### JSONArray.java
- **Class:** `JSONArray` (public)
- **Package:** `com.json`
- **License header:** JSON.org MIT-style license, copyright 2002, version 2012-04-20
- **Imports:** `java.io.IOException`, `java.io.StringWriter`, `java.io.Writer`, `java.lang.reflect.Array`, `java.util.ArrayList`, `java.util.Collection`, `java.util.Iterator`, `java.util.Map`
- **Fields:**
  - `private final ArrayList myArrayList` (line 88) — raw type
- **Constructors:**
  - `public JSONArray()` — line 94
  - `public JSONArray(JSONTokener x) throws JSONException` — line 103
  - `public JSONArray(String source) throws JSONException` — line 143
  - `public JSONArray(Collection collection)` — line 152 — raw type parameter
  - `public JSONArray(Object array) throws JSONException` — line 167
- **Methods (get/opt/put/utility):**
  - `public Object get(int index) throws JSONException` — line 188
  - `public boolean getBoolean(int index) throws JSONException` — line 206
  - `public double getDouble(int index) throws JSONException` — line 229
  - `public int getInt(int index) throws JSONException` — line 249
  - `public JSONArray getJSONArray(int index) throws JSONException` — line 269
  - `public JSONObject getJSONObject(int index) throws JSONException` — line 286
  - `public long getLong(int index) throws JSONException` — line 304
  - `public String getString(int index) throws JSONException` — line 323
  - `public boolean isNull(int index)` — line 337
  - `public String join(String separator) throws JSONException` — line 350
  - `public int length()` — line 369
  - `public Object opt(int index)` — line 380
  - `public boolean optBoolean(int index)` — line 395
  - `public boolean optBoolean(int index, boolean defaultValue)` — line 409
  - `public double optDouble(int index)` — line 426
  - `public double optDouble(int index, double defaultValue)` — line 440
  - `public int optInt(int index)` — line 457
  - `public int optInt(int index, int defaultValue)` — line 470
  - `public JSONArray optJSONArray(int index)` — line 485
  - `public JSONObject optJSONObject(int index)` — line 499
  - `public long optLong(int index)` — line 513
  - `public long optLong(int index, long defaultValue)` — line 526
  - `public String optString(int index)` — line 543
  - `public String optString(int index, String defaultValue)` — line 556
  - `public JSONArray put(boolean value)` — line 570
  - `public JSONArray put(Collection value)` — line 582 — raw type parameter
  - `public JSONArray put(double value) throws JSONException` — line 595
  - `public JSONArray put(int value)` — line 609
  - `public JSONArray put(long value)` — line 621
  - `public JSONArray put(Map value)` — line 633 — raw type parameter
  - `public JSONArray put(Object value)` — line 646
  - `public JSONArray put(int index, boolean value) throws JSONException` — line 661
  - `public JSONArray put(int index, Collection value) throws JSONException` — line 676 — raw type
  - `public JSONArray put(int index, double value) throws JSONException` — line 692
  - `public JSONArray put(int index, int value) throws JSONException` — line 707
  - `public JSONArray put(int index, long value) throws JSONException` — line 722
  - `public JSONArray put(int index, Map value) throws JSONException` — line 737 — raw type
  - `public JSONArray put(int index, Object value) throws JSONException` — line 755
  - `public Object remove(int index)` — line 778
  - `public JSONObject toJSONObject(JSONArray names) throws JSONException` — line 794
  - `public String toString()` — line 817
  - `public String toString(int indentFactor) throws JSONException` — line 837
  - `public Writer write(Writer writer) throws JSONException` — line 853
  - `Writer write(Writer writer, int indentFactor, int indent) throws JSONException` — line 870 (package-private)

---

## Findings

A83-1 | HIGH | HTTP.java, HTTPTokener.java, JSONArray.java | **Vendored third-party source code.** All three files carry the JSON.org copyright header and are verbatim (or near-verbatim) copies of the `org.json` library (artifact `org.json:json`). Vendoring third-party source into `com.json` prevents Maven from managing the dependency version, makes security patching invisible, and bloats the project source tree. The correct fix is to remove these files and declare `org.json:json` (or the preferred alternative `com.fasterxml.jackson.core:jackson-databind` / `org.json:json`) as a Maven dependency in `pom.xml`.

A83-2 | MEDIUM | HTTP.java:128 | **Raw type `Iterator`** used without generic type parameter (`Iterator keys = jo.keys()`). This produces an unchecked-cast warning at build time and loses type safety. Should be `Iterator<String>` if `JSONObject.keys()` returns a typed iterator, or suppressed with justification if the underlying API is ungenericised.

A83-3 | MEDIUM | HTTP.java:130 | **`StringBuffer` used instead of `StringBuilder`** (`StringBuffer sb = new StringBuffer()`). `StringBuffer` is synchronized and carries unnecessary overhead in a single-threaded context. `StringBuilder` is the modern replacement and is preferred for all new code (same issue in `HTTPTokener.java` line 52 and `JSONArray.java` line 352).

A83-4 | MEDIUM | JSONArray.java:88 | **Raw type `ArrayList`** for the backing store (`private final ArrayList myArrayList`). Should be `ArrayList<Object>`. This causes pervasive unchecked-operation warnings throughout the class wherever elements are retrieved or inserted.

A83-5 | MEDIUM | JSONArray.java:152,582,633,676,737 | **Raw-type `Collection` and `Map` parameters** on five constructor/method signatures (`JSONArray(Collection)`, `put(Collection)`, `put(Map)`, `put(int, Collection)`, `put(int, Map)`). All should be parameterised as `Collection<?>` / `Map<?,?>` to suppress unchecked warnings and express intent clearly.

A83-6 | LOW | JSONArray.java:596 | **Deprecated `new Double(value)` constructor** used (`Double d = new Double(value)`). `Double.valueOf(value)` is the correct replacement and benefits from caching. Same pattern at line 693 (`new Double(value)`), line 610 (`new Integer(value)`), line 708 (`new Integer(value)`), line 622 (`new Long(value)`), line 723 (`new Long(value)`). All six usages will produce deprecation warnings under Java 9+.

A83-7 | LOW | JSONArray.java:817-823 | **`toString()` swallows exceptions and returns `null`**. The method catches all `Exception` and silently returns `null` without logging. Callers that do not null-check the return value will receive a `NullPointerException` downstream. The upstream `join()` method already declares `throws JSONException`, so the only practical failure is an invalid number; a `null` return is an unsafe contract for `toString()`.
# P4 Agent A84 — JSONException, JSONML, JSONObject

## Reading Evidence

### JSONException.java
- **Class:** `JSONException extends Exception`
- **Lines:** 28
- **Methods (3):**
  - `JSONException(String message)` — line 16
  - `JSONException(Throwable cause)` — line 20
  - `getCause()` — line 25
- **Key constants:** `serialVersionUID = 0` (line 9)
- **Author/version tag:** `@author JSON.org`, `@version 2010-12-24`

### JSONML.java
- **Class:** `JSONML` (all static utility methods)
- **Lines:** 467
- **License header:** JSON.org MIT-style license, lines 3–25 ("shall be used for Good, not Evil" variant)
- **Methods (6):**
  - `parse(XMLTokener, boolean, JSONArray)` — private static, line 49
  - `toJSONArray(String)` — public static, line 250
  - `toJSONArray(XMLTokener)` — public static, line 267
  - `toJSONObject(XMLTokener)` — public static, line 285
  - `toJSONObject(String)` — public static, line 303
  - `toString(JSONArray)` — public static, line 314
  - `toString(JSONObject)` — public static, line 396
- **Key constants:** none; uses `XML.LT`, `XML.SLASH`, `XML.BANG`, `XML.QUEST`, `XML.GT`, `XML.EQ` from companion class
- **Author/version tag:** `@author JSON.org`, `@version 2012-03-28`

### JSONObject.java
- **Class:** `JSONObject` (with private inner class `Null`)
- **Lines:** 1593
- **License header:** JSON.org MIT-style license, lines 3–25 ("shall be used for Good, not Evil" variant)
- **Key constants:** `public static final Object NULL` (line 145)
- **Key field:** `private final Map map` (line 136) — raw type
- **Constructors (8):**
  - `JSONObject()` — line 151
  - `JSONObject(JSONObject, String[])` — line 165
  - `JSONObject(JSONTokener)` — line 182
  - `JSONObject(Map)` — line 240
  - `JSONObject(Object)` — line 274
  - `JSONObject(Object, String[])` — line 291
  - `JSONObject(String)` — line 313
  - `JSONObject(String, Locale)` — line 324
- **Public/package-private methods (approx. 44):**
  - `accumulate`, `append`, `doubleToString`, `get`, `getBoolean`, `getDouble`, `getInt`, `getJSONArray`, `getJSONObject`, `getLong`, `getNames(JSONObject)`, `getNames(Object)`, `getString`, `has`, `increment`, `isNull`, `keys`, `length`, `names`, `numberToString`, `opt`, `optBoolean` (×2), `optDouble` (×2), `optInt` (×2), `optJSONArray`, `optJSONObject`, `optLong` (×2), `optString` (×2), `populateMap` (private), `put` (×6 overloads), `putOnce`, `putOpt`, `quote` (×2), `remove`, `stringToValue`, `testValidity`, `toJSONArray`, `toString` (×2), `valueToString`, `wrap`, `write` (×2), `writeValue`, `indent`
- **Author/version tag:** `@author JSON.org`, `@version 2012-07-02`

---

## Findings

A84-1 | HIGH | JSONException.java:9, JSONObject.java (whole file), JSONML.java (whole file) | **Vendored third-party source (15 files) that should be a Maven dependency.** The entire `com.json` package (15 `.java` files including `JSONException`, `JSONML`, `JSONObject`, `JSONArray`, `JSONTokener`, `XML`, `XMLTokener`, etc.) is a verbatim copy of the `org.json` reference implementation from JSON.org. Author tags read `@author JSON.org` and version dates span 2002–2012. The correct approach is to remove all 15 files and declare the standard Maven artifact instead:
```xml
<dependency>
    <groupId>org.json</groupId>
    <artifactId>json</artifactId>
    <version>20231013</version>  <!-- or latest stable -->
</dependency>
```
Vendoring this library prevents security patches from being picked up and inflates the source tree with ~2 000 lines of library code that must be maintained manually. No `org.json` dependency entry was found in `pom.xml`.

A84-2 | MEDIUM | JSONObject.java:136,152,241,243,245,331,598,618,704,727,959 | **Pervasive raw-type usage produces compiler warnings throughout JSONObject.** The backing store is declared `private final Map map` (line 136) and constructed as `new HashMap()` (lines 152, 241) without generic type parameters. This propagates raw `Iterator`, `Map.Entry`, `Enumeration`, and `Class` usages across the file. Examples:
  - `Iterator i = map.entrySet().iterator();` (line 243)
  - `Map.Entry e = (Map.Entry)i.next();` (line 245)
  - `Enumeration keys = bundle.getKeys();` (line 331)
  - `Iterator iterator = jo.keys();` (line 598)
  - `Class klass = object.getClass();` (lines 618, 959)
  - `Iterator keys = this.keys();` (lines 704, 727, 1551, 1564)
Every raw-type use generates an unchecked-cast or raw-type compiler warning. These would be `Map<String,Object>`, `HashMap<String,Object>`, `Iterator<String>`, etc. in a properly typed version.

A84-3 | MEDIUM | JSONObject.java:1028,1084 | **Raw-type parameters on public `put` overloads.** `put(String key, Collection value)` (line 1028) and `put(String key, Map value)` (line 1084) accept unparameterised `Collection` and `Map`, producing unchecked warnings and weakening the public API contract.

A84-4 | LOW | JSONObject.java:1043,1057,1071,1279,1281 | **Deprecated boxed-constructor calls.** `new Double(value)` (line 1043), `new Integer(value)` (line 1057), `new Long(value)` (line 1071), `new Long(string)` (line 1279), and `new Integer(myLong.intValue())` (line 1281) use deprecated `new Wrapper(primitive)` constructors that have been deprecated since Java 9 and slated for removal. The replacements are `Double.valueOf(...)`, `Integer.valueOf(...)`, and `Long.valueOf(...)`.

A84-5 | LOW | JSONML.java:318,340 | **Raw `Iterator` type in `toString(JSONArray)` and `toString(JSONObject)`.** `Iterator keys;` is declared without type parameter (lines 318 and 340). Generates raw-type compiler warnings.

A84-6 | LOW | JSONML.java:321,397 | **`StringBuffer` used instead of `StringBuilder`.** Both `toString(JSONArray)` (line 321) and `toString(JSONObject)` (line 397) use `StringBuffer sb = new StringBuffer()`. These methods are not accessed from multiple threads; `StringBuilder` is the correct non-synchronized alternative and avoids unnecessary locking overhead.

A84-7 | LOW | JSONException.java:10,25 | **Redundant `cause` field shadows `Throwable.cause`.** `JSONException` declares `private Throwable cause` (line 10) and overrides `getCause()` (line 25) to return it. The `Exception` superclass already manages a cause chain via `initCause` / `getCause`. The `JSONException(Throwable cause)` constructor calls `super(cause.getMessage())` (line 21) rather than `super(cause)`, which loses the original exception type in the cause chain and bypasses `Throwable`'s built-in cause handling. This can confuse stack-trace analysis and debuggers.

A84-8 | INFO | JSONObject.java:1 — JSONException.java:1 — JSONML.java:1 | **Package renamed from `org.json` to `com.json`.** The source is otherwise identical to the published org.json library but placed in package `com.json`. This means any external library or future upgrade that references `org.json` classes will not be compatible with this vendored copy, requiring manual re-integration of any patches.
# P4 Agent A85 — JSONString, JSONStringer, JSONTokener

## Reading Evidence

### JSONString.java

**Type:** Interface

**Interface name:** `JSONString` (package `com.json`)

**Methods:**
| Method | Line |
|--------|------|
| `public String toJSONString()` | 17 |

**Fields/Constants:** None

---

### JSONStringer.java

**Type:** Class — extends `JSONWriter`

**Class name:** `JSONStringer` (package `com.json`)

**License header:** JSON.org MIT-style license, copyright 2006

**Methods:**
| Method | Line |
|--------|------|
| `public JSONStringer()` (constructor) | 63 |
| `public String toString()` | 75 |

**Fields/Constants:** None declared directly (all fields are inherited from `JSONWriter`)

---

### JSONTokener.java

**Type:** Class

**Class name:** `JSONTokener` (package `com.json`)

**License header:** JSON.org MIT-style license, copyright 2002

**Fields:**
| Field | Type | Line |
|-------|------|------|
| `character` | `private long` | 43 |
| `eof` | `private boolean` | 44 |
| `index` | `private long` | 45 |
| `line` | `private long` | 46 |
| `previous` | `private char` | 47 |
| `reader` | `private Reader` | 48 |
| `usePrevious` | `private boolean` | 49 |

**Methods:**
| Method | Line |
|--------|------|
| `public JSONTokener(Reader reader)` (constructor) | 57 |
| `public JSONTokener(InputStream inputStream)` (constructor) | 73 |
| `public JSONTokener(String s)` (constructor) | 83 |
| `public void back()` | 93 |
| `public static int dehexchar(char c)` | 110 |
| `public boolean end()` | 123 |
| `public boolean more()` | 133 |
| `public char next()` | 148 |
| `public char next(char c)` | 187 |
| `public String next(int n)` | 206 |
| `public char nextClean()` | 230 |
| `public String nextString(char quote)` | 251 |
| `public String nextTo(char delimiter)` | 308 |
| `public String nextTo(String delimiters)` | 329 |
| `public Object nextValue()` | 353 |
| `public char skipTo(char to)` | 400 |
| `public JSONException syntaxError(String message)` | 432 |
| `public String toString()` | 442 |

---

## Findings

A85-1 | HIGH | JSONString.java, JSONStringer.java, JSONTokener.java (entire com.json package) | Vendored third-party source — the entire `com.json` package (15 files: CDL, Cookie, CookieList, HTTP, HTTPTokener, JSONArray, JSONException, JSONML, JSONObject, JSONString, JSONStringer, JSONTokener, JSONWriter, XML, XMLTokener) is a verbatim copy of the `org.json` reference implementation. `pom.xml` contains no `org.json:json` Maven dependency. This library is available as `org.json:json` on Maven Central and should be declared as a dependency instead of being vendored in source. Vendoring obscures the dependency, prevents automatic version tracking, and blocks security tooling (e.g., Dependabot, OWASP Dependency-Check) from detecting vulnerabilities in the library.

A85-2 | MEDIUM | JSONTokener.java:253, JSONTokener.java:309, JSONTokener.java:331, JSONTokener.java:378 | Use of raw `StringBuffer` instead of `StringBuilder`. `StringBuffer` is synchronized and carries unnecessary overhead in single-threaded parsing contexts. With `-Xlint:all` enabled in the Maven compiler plugin these usages produce deprecation/performance warnings. The idiomatic replacement is `StringBuilder`.

A85-3 | LOW | JSONTokener.java:73-75 | Constructor `JSONTokener(InputStream inputStream)` wraps the stream with `new InputStreamReader(inputStream)` using the platform default charset rather than an explicit charset (e.g., `StandardCharsets.UTF_8`). JSON is defined as UTF-8 by RFC 8259; relying on the platform default charset can produce incorrect parsing on non-UTF-8 platforms and triggers a `-Xlint:all` compiler warning about implicit charset use.

A85-4 | LOW | JSONString.java:17 | Interface method declares redundant `public` modifier. Interface methods are implicitly public; the explicit modifier is unnecessary noise and can be flagged by static analysis tools.
# P4 Agent A86 — JSONWriter, XML, XMLTokener

## Reading Evidence

### JSONWriter.java

**Class:** `JSONWriter` (public class, line 59)

**Fields/Constants:**
- `private static final int maxdepth = 200` (line 60)
- `private boolean comma` (line 66)
- `protected char mode` (line 76)
- `private final JSONObject stack[]` (line 81)
- `private int top` (line 86)
- `protected Writer writer` (line 91)

**Methods:**
| Method | Line |
|---|---|
| `public JSONWriter(Writer w)` (constructor) | 96 |
| `private JSONWriter append(String string)` | 110 |
| `public JSONWriter array()` | 141 |
| `private JSONWriter end(char mode, char c)` | 158 |
| `public JSONWriter endArray()` | 180 |
| `public JSONWriter endObject()` | 190 |
| `public JSONWriter key(String string)` | 202 |
| `public JSONWriter object()` | 234 |
| `private void pop(char c)` | 254 |
| `private void push(JSONObject jo)` | 275 |
| `public JSONWriter value(boolean b)` | 292 |
| `public JSONWriter value(double d)` | 302 |
| `public JSONWriter value(long l)` | 312 |
| `public JSONWriter value(Object object)` | 324 |

**License header:** JSON.org, copyright 2006.

---

### XML.java

**Class:** `XML` (public class, line 36)

**Fields/Constants:**
- `public static final Character AMP` (line 39) — `new Character('&')`
- `public static final Character APOS` (line 42) — `new Character('\'')`
- `public static final Character BANG` (line 45) — `new Character('!')`
- `public static final Character EQ` (line 48) — `new Character('=')`
- `public static final Character GT` (line 51) — `new Character('>')`
- `public static final Character LT` (line 54) — `new Character('<')`
- `public static final Character QUEST` (line 57) — `new Character('?')`
- `public static final Character QUOT` (line 60) — `new Character('"')`
- `public static final Character SLASH` (line 63) — `new Character('/')`

**Methods:**
| Method | Line |
|---|---|
| `public static String escape(String string)` | 76 |
| `public static void noSpace(String string)` | 109 |
| `private static boolean parse(XMLTokener x, JSONObject context, String name)` | 130 |
| `public static Object stringToValue(String string)` | 303 |
| `public static JSONObject toJSONObject(String string)` | 365 |
| `public static String toString(Object object)` | 381 |
| `public static String toString(Object object, String tagName)` | 393 |

**License header:** JSON.org, copyright 2002.

---

### XMLTokener.java

**Class:** `XMLTokener extends JSONTokener` (public class, line 33)

**Fields/Constants:**
- `public static final java.util.HashMap entity` (line 39) — raw type `HashMap`; populated in static initializer (lines 41–48) with amp, apos, gt, lt, quot mappings.

**Methods:**
| Method | Line |
|---|---|
| `public XMLTokener(String s)` (constructor) | 54 |
| `public String nextCDATA()` | 63 |
| `public Object nextContent()` | 92 |
| `public Object nextEntity(char ampersand)` | 127 |
| `public Object nextMeta()` | 154 |
| `public Object nextToken()` | 219 |
| `public boolean skipPast(String to)` | 301 |

**License header:** JSON.org, copyright 2002.

---

## Findings

A86-1 | HIGH | JSONWriter.java:1–327, XML.java:1–507, XMLTokener.java:1–365 | Vendored third-party source: all three files are org.json library classes (JSONWriter, XML, XMLTokener) re-packaged under `com.json`. Copyright headers explicitly state `@author JSON.org`. The org.json library is available as a standard Maven artifact (`org.json:json`). Vendoring source copies means the project misses upstream security patches and bug fixes, and creates maintenance burden. These files should be removed and replaced with a Maven dependency on `org.json:json`.

A86-2 | MEDIUM | XMLTokener.java:39,42 | Raw type usage: `public static final java.util.HashMap entity` is declared and instantiated (`new java.util.HashMap(8)`) without type parameters. This will produce an unchecked-assignment compiler warning on any Java 5+ build. Should be `HashMap<String, Character>`.

A86-3 | MEDIUM | XML.java:39–63 | Deprecated constructor usage: all nine `Character` constants (e.g., `new Character('&')` at line 39) use the `Character(char)` constructor which has been deprecated since Java 9. Preferred form is `Character.valueOf('&')`. Will produce deprecation warnings on modern JDK builds.

A86-4 | MEDIUM | JSONWriter.java:303 | Deprecated constructor usage: `new Double(d)` at line 303 uses the `Double(double)` constructor, deprecated since Java 9. Should use `Double.valueOf(d)`.

A86-5 | MEDIUM | XML.java:317,337,339 | Deprecated constructor usage: `new Integer(0)` (line 317), `new Long(string)` (line 337), and `new Integer(myLong.intValue())` (line 339) use boxing constructors deprecated since Java 9. Should use `Integer.valueOf(...)` and `Long.valueOf(...)`.

A86-6 | LOW | XML.java:77,395 | `StringBuffer` used instead of `StringBuilder`: `escape()` (line 77) and `toString(Object, String)` (line 395) both use `StringBuffer`. `StringBuffer` is synchronized and incurs unnecessary overhead in single-threaded contexts; `StringBuilder` is the modern replacement.

A86-7 | LOW | XMLTokener.java:66 | Same issue: `nextCDATA()` uses `StringBuffer` (line 66) where `StringBuilder` would be appropriate.

A86-8 | LOW | XMLTokener.java:128 | Same issue: `nextEntity()` uses `StringBuffer` (line 128).

A86-9 | LOW | XMLTokener.java:247,266 | Same issue: `nextToken()` uses `StringBuffer` at lines 247 and 266.

A86-10 | LOW | XMLTokener.java:94 | Same issue: `nextContent()` declares `StringBuffer sb` (line 94).

A86-11 | LOW | XML.java:400 | Raw type usage: `Iterator keys` (line 400) is declared without a type parameter in `toString(Object, String)`. Should be `Iterator<String>`. Produces an unchecked compiler warning.
# P4 Agent A87 — FleetCheckPDF, PreStartPDF

## Reading Evidence

### FleetCheckPDF.java

**Class:** `FleetCheckPDF` (extends `PreStartPDF`)
**Package:** `com.pdf`

**Fields/Constants:**
| Name | Type | Line | Notes |
|------|------|------|-------|
| `log` | `static Logger` | 29 | Instance logger via `InfoLogger.getLogger` |
| `pdfurl` | `String` | 30 | Instance field, never used in this class |
| `unitDAO` | `UnitDAO` | 31 | Singleton reference |
| `driverDao` | `DriverDAO` | 32 | Singleton reference |

**Methods:**
| Method | Line |
|--------|------|
| `FleetCheckPDF(String compId, Date from, Date to, String docRoot)` — constructor | 34 |
| `createTable(Document document)` — overrides parent | 47 |

---

### PreStartPDF.java

**Class:** `PreStartPDF`
**Package:** `com.pdf`

**Fields/Constants:**
| Name | Type | Line | Notes |
|------|------|------|-------|
| `result` | `protected String` | 29 | Output file path |
| `title` | `protected String` | 30 | Report title |
| `image` | `protected String` | 31 | Banner image path |
| `from` | `protected Date` | 32 | Date range start |
| `to` | `protected Date` | 33 | Date range end |
| `compId` | `protected String` | 34 | Company ID |
| `catFont` | `protected static Font` | 35 | Header font 18pt bold |
| `redFont` | `protected static Font` | 36 | Red font 12pt normal |
| `subFont` | `protected static Font` | 37 | Sub-heading font 16pt bold |
| `hrFont` | `protected static Font` | 38 | Table header font 12pt bold |
| `hdFont` | `protected static Font` | 39 | Table data font 10pt normal |
| `smallBold` | `protected static Font` | 40 | Small bold font 10pt bold |

**Methods:**
| Method | Line |
|--------|------|
| `PreStartPDF(String compId, Date from, Date to)` — constructor | 42 |
| `createPdf()` — public, returns String | 54 |
| `addContent(Document document)` — private | 68 |
| `createTable(Document document)` — public, overridden by subclass | 77 |
| `addMetaData(Document document)` — private | 98 |
| `addTitlePage(Document document)` — private | 105 |
| `addFooter(Document document)` — private | 116 |
| `createList(Section subCatPart)` — private | 125 |
| `addEmptyLine(Paragraph paragraph, int number)` — private | 133 |
| `addImage(Document document)` — private | 139 |
| `getImage()` / `setImage(String)` | 149 / 153 |
| `getResult()` / `setResult(String)` | 157 / 161 |
| `getTitle()` / `setTitle(String)` | 165 / 169 |
| `getFrom()` / `setFrom(Date)` | 173 / 177 |
| `getTo()` / `setTo(Date)` | 181 / 185 |

---

## Findings

A87-1 | HIGH | PreStartPDF.java:77–96 | **Dead/placeholder implementation of `createTable`.** The base-class `createTable` contains a hardcoded stub table with literal strings ("Cell with colspan 3", "row 1; cell 1", etc.) and no real business logic. It is designed to be overridden, but because the method is `public` and non-abstract it can be called on a raw `PreStartPDF` instance and will silently emit nonsense content into any PDF. The class should either declare the method `abstract` (making `PreStartPDF` abstract) or throw `UnsupportedOperationException` to prevent accidental misuse.

A87-2 | HIGH | PreStartPDF.java:125–131 | **Dead method `createList`.** `createList(Section subCatPart)` is never called anywhere in either file. It contains only placeholder `ListItem` text ("First point", "Second point", "Third point") and appears to be leftover scaffolding code from a tutorial or template. It should be removed.

A87-3 | HIGH | FleetCheckPDF.java:100 | **`ResultDAO` instantiated with `new` inside a loop.** `new ResultDAO()` is constructed on every iteration of the outer driver loop (line 99), while both `UnitDAO` and `DriverDAO` use the singleton pattern. This is inconsistent, potentially expensive, and likely to create resource/connection issues under load. `ResultDAO` should be obtained via a singleton or at minimum moved outside the loop.

A87-4 | HIGH | FleetCheckPDF.java:160–164 | **Inverted empty-result logic produces false "no data" row.** `emptyflag` is initialised to `true` (line 89). If the driver list is non-empty but every driver has zero matching results the flag stays `true` and the "No Fleetcheck is performed" row is correctly appended. However if the driver list is null/empty the code sets `emptyflag = false` (line 94) and then falls through to the `if (emptyflag)` check — the empty-data message is suppressed, not shown. The existing "No Driver is registered" cell is added, but the `emptyflag = false` branch means that row is only ever protected from being double-appended; the flag's semantics are unclear and inverted relative to what a reader would expect ("empty" should mean no data was found, not that data was found). This logic is error-prone and will confuse maintainers.

A87-5 | MEDIUM | FleetCheckPDF.java:30 | **Unused field `pdfurl`.** The field is assigned a complex expression involving `getProtectionDomain().getCodeSource().getLocation()` but is never read in this class or (through inheritance) the parent. It is dead weight that also executes a non-trivial expression at object construction time on every instantiation.

A87-6 | MEDIUM | FleetCheckPDF.java:103–113 | **`Boolean first` / `if (first)` block is always true and its condition is never reset meaningfully.** `first` is set to `Boolean.TRUE` at line 103. The `if (first)` guard at line 107 is always entered. Inside the inner loop `first` is set to `false` (line 142) but the `if (first)` check is outside the inner loop and is never evaluated again after the first iteration of the outer block. The variable serves no real purpose and should be removed.

A87-7 | MEDIUM | FleetCheckPDF.java:119–120 | **Stray double semicolon (;;).** Line 119 ends with `)).getName();` and line 120 is a standalone `;`. This is a no-op empty statement but is a style error and signals copy-paste sloppiness.

A87-8 | MEDIUM | FleetCheckPDF.java:127 | **Typo in user-visible string: "Safty" should be "Safety".** The string `"*Safty Check incomplete"` is displayed directly in the PDF output.

A87-9 | MEDIUM | FleetCheckPDF.java:58 | **Typo in column header: "Vehcile" should be "Vehicle".** This is a user-visible column header rendered in the PDF.

A87-10 | MEDIUM | PreStartPDF.java:113 | **Commented-out code `//document.newPage();`.** A call to `document.newPage()` is commented out inside `addTitlePage`. Either it is needed and was accidentally left disabled, or it is dead and should be deleted.

A87-11 | MEDIUM | PreStartPDF.java:147 | **`addImage` builds an empty `Paragraph` and calls `addEmptyLine` but never adds the paragraph to the document.** The blank line intended as spacing after the banner image is created and populated but then discarded (not passed to `document.add`). The banner image is added but the trailing spacer is silently dropped.

A87-12 | MEDIUM | FleetCheckPDF.java:165–168 | **`e.printStackTrace()` used alongside the project logger.** The exception is logged via `InfoLogger.logException` and then also printed to `stderr` with `e.printStackTrace()`. The project clearly has a logging framework; the raw `printStackTrace()` call bypasses it and can expose stack traces in production logs or stdout.

A87-13 | LOW | FleetCheckPDF.java:119 | **Unchecked/raw-type cast `(UnitBean) unitDAO.getUnitById(...).get(0)`.** `getUnitById` returns a raw `List` (or `List<Object>`). The cast to `UnitBean` is unchecked. If the DAO ever returns an unexpected type, this produces a `ClassCastException` at runtime with no type-safety guarantee at compile time.

A87-14 | LOW | PreStartPDF.java:118 | **Copyright footer uses a Java Unicode escape literal in a plain string.** The string `"Copyright \\u00A9 2012-2018 ..."` contains the escaped sequence `\\u00A9` (i.e., a backslash followed by `u00A9`), not the copyright symbol `©`. The PDF will display the raw characters `\u00A9` rather than the intended symbol.

A87-15 | LOW | FleetCheckPDF.java:32 | **Naming inconsistency: `driverDao` vs convention elsewhere.** The field is named `driverDao` while the class pattern (seen in `unitDAO`) uses uppercase `DAO`. This is a minor naming inconsistency across the two DAO references in the same class.

A87-16 | LOW | PreStartPDF.java:3–26 | **Unused imports in PreStartPDF.** The following imports are never referenced in the class body: `Anchor` (line 8), `Chapter` (line 11), `List` / `ListItem` (lines 17–18 — only used in the dead `createList` method), `Section` (line 21). Removing the dead `createList` method (see A87-2) would make `List`, `ListItem`, and `Section` fully unused. `Anchor` and `Chapter` are already unused.

A87-17 | INFO | PreStartPDF.java:48–52 | **Javadoc on `createPdf` refers to "movies".** The Javadoc comment (`"Creates a PDF with information about the movies"`) is copy-pasted from an iText tutorial and is not relevant to this domain. The `@param filename` tag also does not match the actual method signature (no parameter named `filename`).
# P4 Agent A88 — DriverAccessRevokeJob, DriverAccessRevokeJobScheduler, TrainingExpiryDailyEmailJob

## Reading Evidence

### DriverAccessRevokeJob.java
- **Class:** `DriverAccessRevokeJob` (implements `org.quartz.Job`)
- **Fields/Constants:** none
- **Methods:**
  - `execute(JobExecutionContext jobExecutionContext)` — line 15
  - `revokeDriverAccessOnTrainingExpiry()` — line 19

### DriverAccessRevokeJobScheduler.java
- **Class:** `DriverAccessRevokeJobScheduler` (implements `javax.servlet.ServletContextListener`)
- **Fields/Constants:** none
- **Methods:**
  - `contextInitialized(ServletContextEvent servletContextEvent)` — line 17
  - `contextDestroyed(ServletContextEvent servletContextEvent)` — line 38

### TrainingExpiryDailyEmailJob.java
- **Class:** `TrainingExpiryDailyEmailJob` (implements `org.quartz.Job`)
- **Fields/Constants:** none
- **Methods:**
  - `execute(JobExecutionContext jobExecutionContext)` — line 14
  - `sendTrainingExpiryDailyEmail()` — line 18

---

## Findings

A88-1 | HIGH | TrainingExpiryDailyEmailJobSchedueler.java:18 | **Misspelled class name: `TrainingExpiryDailyEmailJobSchedueler`** — the word "Scheduler" is misspelled as "Schedueler" in the class name. This class is registered in `web.xml` line 40, so the typo is present in production configuration. The three other scheduler classes all use the correct spelling (`DriverAccessRevokeJobScheduler`, `TrainingExpiryWeeklyEmailJobScheduler`). This is an inconsistency that will cause confusion and makes the class hard to find by name.

A88-2 | HIGH | TrainingExpiryDailyEmailJobSchedueler.java:26 | **Wrong Quartz group name on trigger identity** — the trigger's group is hardcoded as `"driverAccessRevoke"` (copied from `DriverAccessRevokeJobScheduler`) instead of `"trainingExpiryDailyEmail"`. The job detail uses group `"trainingExpiryDailyEmail"` (line 23) and `forJob` references that group (line 28), but the trigger's own `.withIdentity` group is `"driverAccessRevoke"`. This is a copy-paste defect; the Quartz trigger is registered under the wrong group, making scheduler administration and monitoring misleading.

A88-3 | MEDIUM | DriverAccessRevokeJob.java:16 | **Thread-pool leak — unbounded `newSingleThreadExecutor()` per execution** — `Executors.newSingleThreadExecutor()` creates a new `ExecutorService` on every job firing but the executor is never shut down. The same pattern appears identically in `TrainingExpiryDailyEmailJob.java:15`. Each fire creates a thread pool that is abandoned without calling `shutdown()`, leaking threads and associated resources over time. A shared, application-scoped executor (or simply calling the method directly on the Quartz worker thread) should be used instead.

A88-4 | MEDIUM | TrainingExpiryDailyEmailJob.java:20 | **Typo in local variable name: `traingDAO`** — the variable is declared as `TrainingDAO traingDAO` (missing the 'i' in "training"). This is a cosmetic defect but reduces readability and is inconsistent with the class name `TrainingDAO`.

A88-5 | MEDIUM | DriverAccessRevokeJob.java:19 / TrainingExpiryDailyEmailJob.java:18 | **Inconsistent DAO access pattern** — `DriverAccessRevokeJob` calls `DriverDAO.revokeDriverAccessOnTrainingExpiry()` as a **static** method, while `TrainingExpiryDailyEmailJob` instantiates `new TrainingDAO()` and calls an **instance** method. Neither approach is intrinsically wrong, but the inconsistency across two nearly identical job classes in the same package is a leaky abstraction and makes the codebase harder to reason about. All DAO calls within the `com.quartz` package should follow a single uniform access pattern.

A88-6 | MEDIUM | DriverAccessRevokeJobScheduler.java:28 / TrainingExpiryDailyEmailJobSchedueler.java:31 | **Unnecessary cast to `SchedulerFactory`** — both scheduler classes cast `new StdSchedulerFactory()` to `(SchedulerFactory)` before calling `getScheduler()`. `StdSchedulerFactory` already implements `SchedulerFactory`; the explicit cast is redundant, adds noise, and suggests the code was written with a misunderstanding of the type hierarchy.

A88-7 | MEDIUM | DriverAccessRevokeJobScheduler.java:39 / TrainingExpiryDailyEmailJobSchedueler.java:42 | **`contextDestroyed` misuses `ServletException` as a logging mechanism** — both scheduler classes implement `contextDestroyed` by constructing a `new ServletException("Application Stopped")` and calling `.printStackTrace()` on it. `ServletException` is an exception class, not a logging utility. This prints a spurious stack trace to stderr on every normal application shutdown, pollutes logs, and does not actually shut down the Quartz scheduler (which should be stopped here to avoid thread leaks on redeploy). The scheduler instance is also not stored in a field so it cannot be stopped in this method.

A88-8 | LOW | DriverAccessRevokeJob.java:23 / TrainingExpiryDailyEmailJob.java:22 | **`e.printStackTrace()` used for exception handling** — both job classes catch `SQLException` and call `e.printStackTrace()`. This bypasses any configured logging framework, makes errors invisible in production log aggregators, and provides no context about which job failed. A proper logger (e.g., SLF4J) should be used, consistent with the DAO layer which already uses `log.info(...)`.

A88-9 | LOW | DriverAccessRevokeJobScheduler.java:32 / TrainingExpiryDailyEmailJobSchedueler.java:35 | **`SchedulerException` swallowed with `e.printStackTrace()`** — if the Quartz scheduler fails to initialise or schedule the job (e.g., due to a duplicate trigger key or missing Quartz properties), the exception is silently swallowed after printing to stderr. The application continues to run without the job being scheduled, which would cause silent failures (no access revocation, no expiry emails) with no alerting mechanism.

A88-10 | LOW | DriverAccessRevokeJob.java:15 / TrainingExpiryDailyEmailJob.java:14 | **`JobExecutionContext` parameter is unused** — the `execute` method receives a `JobExecutionContext` but neither job uses it. The parameter name should at least be annotated or follow a convention indicating intentional non-use (e.g., renaming to match the override contract); more importantly, it signals that neither job accesses job data map parameters, which may limit future configurability. This is informational but consistent across both jobs.

A88-11 | INFO | TrainingExpiryDailyEmailJob.java:27-28 | **Trailing blank line** — the file contains a double blank line at the end (lines 28-29), unlike `DriverAccessRevokeJob.java` which ends cleanly at line 27. Minor style inconsistency.
# Pass 4 (Code Quality) — Agent A89

**Audit date:** 2026-02-26
**Assigned files:**
- `src/main/java/com/quartz/TrainingExpiryDailyEmailJobSchedueler.java`
- `src/main/java/com/quartz/TrainingExpiryWeeklyEmailJob.java`
- `src/main/java/com/quartz/TrainingExpiryWeeklyEmailJobScheduler.java`

---

## Reading Evidence

### File 1: TrainingExpiryDailyEmailJobSchedueler.java

**Class:** `com.quartz.TrainingExpiryDailyEmailJobSchedueler`
**Implements:** `javax.servlet.ServletContextListener`

**Methods:**
| Method | Line |
|--------|------|
| `contextInitialized(ServletContextEvent)` | 20 |
| `contextDestroyed(ServletContextEvent)` | 41 |

**Types/Constants defined:** None

**Imports used:**
- `javax.servlet.ServletContextEvent` (used)
- `javax.servlet.ServletContextListener` (used)
- `javax.servlet.ServletException` (used — but only to construct-and-discard an exception object)
- `org.quartz.CronTrigger` (used)
- `org.quartz.JobDetail` (used)
- `org.quartz.Scheduler` (used)
- `org.quartz.SchedulerException` (used)
- `org.quartz.SchedulerFactory` (used)
- `org.quartz.impl.StdSchedulerFactory` (used)
- static imports: `cronSchedule`, `newJob`, `newTrigger` (used)

---

### File 2: TrainingExpiryWeeklyEmailJob.java

**Class:** `com.quartz.TrainingExpiryWeeklyEmailJob`
**Implements:** `org.quartz.Job`

**Methods:**
| Method | Line |
|--------|------|
| `execute(JobExecutionContext)` | 14 |
| `sendTrainingExpiryWeeklyEmail()` | 18 |

**Types/Constants defined:** None

**Imports used:**
- `java.sql.SQLException` (used)
- `java.util.concurrent.Executors` (used)
- `org.quartz.Job` (used)
- `org.quartz.JobExecutionContext` (used)
- `com.dao.TrainingDAO` (used)

**Local variables:**
- `traingDAO` (line 20) — misspelled local variable name

---

### File 3: TrainingExpiryWeeklyEmailJobScheduler.java

**Class:** `com.quartz.TrainingExpiryWeeklyEmailJobScheduler`
**Implements:** `javax.servlet.ServletContextListener`

**Methods:**
| Method | Line |
|--------|------|
| `contextInitialized(ServletContextEvent)` | 20 |
| `contextDestroyed(ServletContextEvent)` | 41 |

**Types/Constants defined:** None

**Imports used:**
- Same set as `TrainingExpiryDailyEmailJobSchedueler.java` — all used.

---

## Findings

### A89-1 | HIGH | TrainingExpiryDailyEmailJobSchedueler.java:18 | Class name misspelling: "Schedueler" instead of "Scheduler"

The class is named `TrainingExpiryDailyEmailJobSchedueler` — "Schedueler" is a misspelling of "Scheduler". The companion class for the same pattern is correctly named `TrainingExpiryWeeklyEmailJobScheduler`. This inconsistency makes the codebase harder to navigate, breaks naming symmetry, and would force any web.xml or configuration referencing this class by name to perpetuate the typo.

---

### A89-2 | HIGH | TrainingExpiryDailyEmailJobSchedueler.java:42 | contextDestroyed instantiates and immediately discards a ServletException instead of shutting down the scheduler

```java
new ServletException("Application Stopped").printStackTrace();
```

`contextDestroyed` is the lifecycle hook for orderly shutdown. Instead of stopping the Quartz `Scheduler` (via `scheduler.shutdown()`), it creates a `ServletException` object solely to call `printStackTrace()` on it — the exception is never thrown and the scheduler is never stopped. This means the Quartz scheduler thread pool continues running after the servlet context is destroyed, leaking threads. The same defect exists identically in `TrainingExpiryWeeklyEmailJobScheduler.java:42` (see A89-3) and in `DriverAccessRevokeJobScheduler.java:39` (out of scope but same pattern).

---

### A89-3 | HIGH | TrainingExpiryWeeklyEmailJobScheduler.java:42 | contextDestroyed instantiates and immediately discards a ServletException instead of shutting down the scheduler

Exact same defect as A89-2. `contextDestroyed` prints a throwaway `ServletException` stack trace rather than calling `scheduler.shutdown()`. The scheduler instance is not stored as a field, so there is no way to reach it from `contextDestroyed` at all — both issues (no field storage and wrong shutdown logic) compound one another.

---

### A89-4 | HIGH | TrainingExpiryDailyEmailJobSchedueler.java:31 | Scheduler instance not retained; contextDestroyed cannot shut it down

```java
Scheduler scheduler = ((SchedulerFactory) new StdSchedulerFactory()).getScheduler();
```

The `scheduler` reference is a local variable scoped to `contextInitialized`. There is no instance field to hold it, so `contextDestroyed` has no handle to call `scheduler.shutdown()`. The same structural defect applies to `TrainingExpiryWeeklyEmailJobScheduler.java:31` (A89-5).

---

### A89-5 | HIGH | TrainingExpiryWeeklyEmailJobScheduler.java:31 | Scheduler instance not retained; contextDestroyed cannot shut it down

Same defect as A89-4. The `scheduler` local variable is lost after `contextInitialized` returns, making graceful shutdown impossible.

---

### A89-6 | MEDIUM | TrainingExpiryDailyEmailJobSchedueler.java:31 | Unnecessary cast: StdSchedulerFactory already implements SchedulerFactory

```java
Scheduler scheduler = ((SchedulerFactory) new StdSchedulerFactory()).getScheduler();
```

`StdSchedulerFactory` directly implements `SchedulerFactory`, so the explicit cast to `SchedulerFactory` is redundant. The same pattern appears in `TrainingExpiryWeeklyEmailJobScheduler.java:31`. This is a build warning in most IDEs ("unnecessary cast") and creates misleading visual noise. The identical cast also appears in `DriverAccessRevokeJobScheduler.java:28` (out of scope).

---

### A89-7 | MEDIUM | TrainingExpiryWeeklyEmailJobScheduler.java:26 | Trigger group name is "driverAccessRevoke" — copied from a different job

```java
.withIdentity("trainingExpiryWeeklyEmailJobTrigger", "driverAccessRevoke")
```

The trigger's group is `"driverAccessRevoke"`, which is the group name belonging to the `DriverAccessRevokeJob` family, not the training expiry weekly email job. The same copy-paste error exists in `TrainingExpiryDailyEmailJobSchedueler.java:26`. This means both training expiry triggers are registered under the wrong Quartz group, which will cause confusion in monitoring/management tools and could cause group-level operations (pause, resume, delete group) to affect the wrong jobs.

---

### A89-8 | MEDIUM | TrainingExpiryDailyEmailJobSchedueler.java:26 | Trigger group name is "driverAccessRevoke" — copied from a different job

```java
.withIdentity("trainingExpiryDailyEmailJobTrigger", "driverAccessRevoke")
```

Same copy-paste error as A89-7. The daily email trigger is filed under the `driverAccessRevoke` group instead of a group consistent with its job identity (e.g., `"trainingExpiryDailyEmail"`).

---

### A89-9 | MEDIUM | TrainingExpiryWeeklyEmailJob.java:20 | Misspelled local variable name: "traingDAO" instead of "trainingDAO"

```java
TrainingDAO traingDAO = new TrainingDAO();
traingDAO.sendTrainingExpiryWeeklyEmail();
```

`traingDAO` is a misspelling of `trainingDAO`. The identical misspelling exists in `TrainingExpiryDailyEmailJob.java:20` (out of scope but same pattern). This is a style/readability defect and indicates copy-paste without review.

---

### A89-10 | MEDIUM | TrainingExpiryWeeklyEmailJob.java:15 | Executor created per invocation with no shutdown, causing thread leak

```java
Executors.newSingleThreadExecutor().execute(this::sendTrainingExpiryWeeklyEmail);
```

A new `ExecutorService` is created every time `execute()` is called but is never shut down (no `shutdown()` or `shutdownNow()` call). `newSingleThreadExecutor()` creates a thread pool backed by an unbounded queue; without shutdown, the thread lingers until GC — which for non-daemon threads may prevent JVM exit. If the job fires repeatedly (e.g., on a test server with overlapping triggers), a new executor accumulates each time. The same defect is in `TrainingExpiryDailyEmailJob.java:15` (out of scope).

---

### A89-11 | MEDIUM | TrainingExpiryDailyEmailJobSchedueler.java:35-37 | SchedulerException swallowed with only a stack trace; scheduler fails silently

```java
} catch (SchedulerException e) {
    e.printStackTrace();
}
```

If scheduling fails (e.g., duplicate job key, misfire policy error), the exception is printed to stderr and silently discarded. The application continues without the job being scheduled, with no visible indication to operators beyond a stack trace that may not be noticed. The same pattern is in `TrainingExpiryWeeklyEmailJobScheduler.java:35-37`. A logged error or re-throw as a `RuntimeException` would be more appropriate in a lifecycle listener.

---

### A89-12 | MEDIUM | TrainingExpiryWeeklyEmailJob.java:22-24 | SQLException swallowed with only a stack trace; email send failures are silent

```java
} catch (SQLException e) {
    e.printStackTrace();
}
```

Database/email failures during the scheduled job execution are silently swallowed after printing to stderr. There is no logging, alerting, or Quartz `JobExecutionException` wrapping. The identical pattern is in `TrainingExpiryDailyEmailJob.java:22-24` (out of scope).

---

### A89-13 | LOW | TrainingExpiryWeeklyEmailJob.java:18 | sendTrainingExpiryWeeklyEmail() is public but should be private or package-private

```java
public void sendTrainingExpiryWeeklyEmail() {
```

The method is a private implementation detail invoked via a method reference from `execute()`. Declaring it `public` exposes it as part of the class's API surface, allowing external callers to bypass the Quartz scheduling mechanism entirely. It should be at most package-private. The same applies to `TrainingExpiryDailyEmailJob.sendTrainingExpiryDailyEmail()` (out of scope).

---

### A89-14 | LOW | TrainingExpiryWeeklyEmailJobScheduler.java:1-44 | Class is a near-identical copy of TrainingExpiryDailyEmailJobSchedueler with only job class and cron expression differing

Both scheduler classes share exactly the same structure: implement `ServletContextListener`, instantiate a `StdSchedulerFactory`, build a `JobDetail` and `CronTrigger`, schedule and start — with the same broken `contextDestroyed`. This is a textbook duplication candidate. A single parameterised base class or factory method would eliminate the duplicated bugs and make future fixes apply in one place.

---

### A89-15 | INFO | TrainingExpiryDailyEmailJobSchedueler.java:9 | Import javax.servlet.ServletException is used only to construct a throwaway object

```java
import javax.servlet.ServletException;
```

This import is technically "used" (line 42), but the usage itself is a defect (A89-2). If A89-2 is fixed by removing the bogus `new ServletException(...).printStackTrace()` line, this import becomes unused and should be removed.

---
# Pass 4 (Code Quality) — Agent A90

**Audit date:** 2026-02-26
**Assigned files:**
1. `src/main/java/com/querybuilder/StatementPreparer.java`
2. `src/main/java/com/querybuilder/assignment/AssignmentByCompanyAndUnitIdQuery.java`
3. `src/main/java/com/querybuilder/filters/DateBetweenFilter.java`

---

## Reading Evidence

### 1. `StatementPreparer.java`

**Class:** `com.querybuilder.StatementPreparer`

**Fields:**
- `statement` — `PreparedStatement` (private, line 8)
- `index` — `int` (private, line 9)

**Methods:**
| Method | Line |
|--------|------|
| `StatementPreparer(PreparedStatement statement)` (constructor) | 11 |
| `addDate(Date value) throws SQLException` | 16 |
| `addLong(long value) throws SQLException` | 20 |
| `addString(String value) throws SQLException` | 24 |
| `addInteger(int value) throws SQLException` | 28 |

**Types imported:** `java.sql.PreparedStatement`, `java.sql.SQLException`, `java.util.Date`

**Constants defined:** none

---

### 2. `AssignmentByCompanyAndUnitIdQuery.java`

**Class:** `com.querybuilder.assignment.AssignmentByCompanyAndUnitIdQuery`

**Fields:**
- `query` — `String` (private static final, line 14)
- `companyId` — `long` (private final, line 20)
- `unitId` — `long` (private final, line 21)

**Methods:**
| Method | Line |
|--------|------|
| `AssignmentByCompanyAndUnitIdQuery(long companyId, long unitId)` (constructor) | 23 |
| `query(String dateFormat) throws SQLException` | 28 |
| `mapResults(String dateFormat, ResultSet resultSet) throws SQLException` | 32 |
| `prepareStatement(PreparedStatement statement) throws SQLException` | 42 |

**Constants defined:** `query` (SQL string constant, line 14)

---

### 3. `DateBetweenFilter.java`

**Interface:** `com.querybuilder.filters.DateBetweenFilter`

**Methods (all abstract):**
| Method | Line |
|--------|------|
| `start()` → `Date` | 6 |
| `end()` → `Date` | 7 |
| `timezone()` → `String` | 8 |

**Types imported:** `java.util.Date`

**Constants defined:** none

---

## Findings

### A90-1 | MEDIUM | `StatementPreparer.java`:5 | Deprecated `java.util.Date` used in public API

`StatementPreparer.addDate(Date value)` accepts `java.util.Date`, which has been deprecated in modern Java in favour of `java.time` types (`LocalDate`, `Instant`, etc.). The method internally wraps it as `java.sql.Date` via `value.getTime()`, exposing callers to the legacy date API. `DateBetweenFilter` (line 3–7) also uses `java.util.Date` for its `start()` / `end()` contract, propagating the same issue across the filter pipeline.

---

### A90-2 | MEDIUM | `DateBetweenFilter.java`:1 | Interface leaks `java.util.Date` across public contract

The `DateBetweenFilter` interface declares `start()` and `end()` returning `java.util.Date`. This is a leaky abstraction: every implementor and every consumer is forced into the deprecated `java.util.Date` type. The `timezone()` method exists to compensate for the lack of timezone information in `java.util.Date`, which is itself a symptom of the wrong type being used. Migrating to `java.time.Instant` or `java.time.ZonedDateTime` would subsume `timezone()` into the type.

---

### A90-3 | MEDIUM | `DateBetweenFilterHandler.java`:21 | Commented-out production SQL

Line 21 of `DateBetweenFilterHandler.java` (a file that is the primary consumer of `DateBetweenFilter`) contains a commented-out SQL fragment that was the prior implementation of the between-dates branch:

```java
//        if (filterBetweenTwoDates()) return String.format(" AND %s::DATE BETWEEN ? AND ?", fieldName);
```

This is dead, commented-out code in a production source file. It should be removed; version history preserves the prior form.

---

### A90-4 | HIGH | `DateBetweenFilterHandler.java`:19–31 | Parameter-bind logic is inconsistent with SQL placeholders for single-date branches

`getQueryFilter()` generates:
- `filterStartOnly()` → SQL has **1** `?` (the date)
- `filterEndOnly()` → SQL has **1** `?` (the date)
- `filterBetweenTwoDates()` → SQL has **3** `?` (timezone string, start date, end date)

`prepareStatement()` (lines 28–31) binds:
```java
if(filter.timezone() != null) preparer.addString(filter.timezone());
if (filter.start() != null) preparer.addDate(filter.start());
if (filter.end() != null) preparer.addDate(filter.end());
```

For the `filterStartOnly()` case, the timezone is still bound if non-null even though the generated SQL has no `?` for it. This will cause a parameter-count mismatch at runtime when `filter.timezone() != null` and only a start date is present. The same mismatch applies to the `filterEndOnly()` case. The binding logic does not mirror the conditional structure of `getQueryFilter()`.

---

### A90-5 | LOW | `AssignmentByCompanyAndUnitIdQuery.java`:14 | SQL constant named `query` conflicts with public method name `query`

The private static final field is named `query` (line 14) and the public method is also named `query` (line 28). Although Java permits this (field vs. method namespace), the naming collision is confusing and violates the convention of distinguishing constants by their `UPPER_SNAKE_CASE` name (e.g., `QUERY` or `SQL`). This pattern is used correctly elsewhere in the codebase (e.g., `ImpactsByCompanyIdQuery.REPORT_QUERY`).

---

### A90-6 | LOW | `AssignmentByCompanyAndUnitIdQuery.java`:35 | Builder setter uses snake_case (`company_name`) violating Java naming conventions

The builder call `.company_name(...)` (line 35) uses a snake_case method name. This originates in `UnitAssignmentBean` where the field `company_name` (snake_case) is declared. Lombok generates the builder setter with the same name, resulting in a non-idiomatic Java method name. All other bean fields in the same class (`id`, `start`, `end`, `isCurrent`) use camelCase. The field should be named `companyName` with the builder method `.companyName(...)` to match Java conventions and the rest of the codebase (other beans use `companyName` consistently).

---

### A90-7 | LOW | `StatementPreparer.java`:13 | Inconsistent initialisation style for `index`

In the constructor (line 13), `index` is initialised as a bare statement `index = 0;` without the `this.` qualifier, while `statement` on the preceding line uses `this.statement = statement;`. For a field whose name does not shadow the constructor parameter, omitting `this.` is harmless, but the inconsistency within the same constructor body is a minor style issue.

---

### A90-8 | LOW | `DateBetweenFilterHandler.java`:29 | Inconsistent spacing around `if` condition

Line 29 is written as `if(filter.timezone() != null)` (no space between `if` and `(`), while every other `if` statement in the same file (lines 18, 28, 30, 31, etc.) uses `if (...)` with a space. This is a minor but concrete style inconsistency within the same file.

*(Note: `DateBetweenFilterHandler.java` is not an assigned file but it is the sole non-trivial consumer of the two assigned filter files; this finding is included as contextual evidence of the interface's downstream impact.)*

---

## Summary

| ID | Severity | File | Short description |
|----|----------|------|-------------------|
| A90-1 | MEDIUM | StatementPreparer.java:5 | Deprecated `java.util.Date` in public API |
| A90-2 | MEDIUM | DateBetweenFilter.java:1 | Interface leaks deprecated `java.util.Date` across public contract |
| A90-3 | MEDIUM | DateBetweenFilterHandler.java:21 | Commented-out production SQL |
| A90-4 | HIGH | DateBetweenFilterHandler.java:19–31 | Parameter-bind logic inconsistent with SQL placeholders for single-date branches |
| A90-5 | LOW | AssignmentByCompanyAndUnitIdQuery.java:14 | SQL constant named `query` clashes with method name; should be UPPER_SNAKE_CASE |
| A90-6 | LOW | AssignmentByCompanyAndUnitIdQuery.java:35 | Builder setter `company_name` violates Java camelCase naming convention |
| A90-7 | LOW | StatementPreparer.java:13 | Inconsistent `this.` qualifier usage in constructor |
| A90-8 | LOW | DateBetweenFilterHandler.java:29 | Missing space between `if` and `(` — inconsistent with rest of file |
# Pass 4 (Code Quality) - Agent A91
**Date:** 2026-02-26
**Assigned files:**
- `src/main/java/com/querybuilder/filters/DateBetweenFilterHandler.java`
- `src/main/java/com/querybuilder/filters/FilterHandler.java`
- `src/main/java/com/querybuilder/filters/ImpactLevelFilter.java`

---

## Reading Evidence

### 1. `FilterHandler.java`

- **Type:** Interface `com.querybuilder.filters.FilterHandler`
- **Methods:**
  - `getQueryFilter()` — line 8
  - `prepareStatement(StatementPreparer preparer) throws SQLException` — line 10
- **Constants / fields defined:** none
- **Imports:** `com.querybuilder.StatementPreparer`, `java.sql.SQLException`

---

### 2. `ImpactLevelFilter.java`

- **Type:** Interface `com.querybuilder.filters.ImpactLevelFilter`
- **Methods:**
  - `impactLevel()` — line 6 (returns `com.bean.ImpactLevel`)
- **Constants / fields defined:** none
- **Imports:** `com.bean.ImpactLevel`

---

### 3. `DateBetweenFilterHandler.java`

- **Type:** Class `com.querybuilder.filters.DateBetweenFilterHandler implements FilterHandler`
- **Fields:**
  - `private final DateBetweenFilter filter` — line 8
  - `private final String fieldName` — line 9
- **Methods:**
  - `DateBetweenFilterHandler(DateBetweenFilter filter, String fieldName)` (constructor) — line 11
  - `getQueryFilter()` — line 17 (override)
  - `prepareStatement(StatementPreparer preparer) throws SQLException` — line 27 (override)
  - `ignoreFilter()` (private) — line 34
  - `filterStartOnly()` (private) — line 38
  - `filterEndOnly()` (private) — line 42
  - `filterBetweenTwoDates()` (private) — line 46
- **Constants / errors defined:** none
- **Imports:** `com.querybuilder.StatementPreparer`, `java.sql.SQLException`

---

## Findings

### A91-1 | HIGH | DateBetweenFilterHandler.java:21 | Commented-out code left in production source

Line 21 contains a commented-out SQL fragment that was the previous implementation of the between-dates branch:

```java
//        if (filterBetweenTwoDates()) return String.format(" AND %s::DATE BETWEEN ? AND ?", fieldName);
```

This is dead commented-out code. It documents a deliberate change in SQL strategy (switching from a simple cast to a timezone-aware expression) but it was not removed after the replacement was validated. Leaving it in creates confusion about which expression is authoritative and can mislead future maintainers into thinking the simpler form may still be valid.

---

### A91-2 | HIGH | DateBetweenFilterHandler.java:29-31 | Parameter binding mismatch: timezone is bound unconditionally but the query placeholder only exists for the between-dates branch

`prepareStatement` (lines 27-32) always binds `filter.timezone()` whenever it is non-null, regardless of which SQL branch was selected by `getQueryFilter()`. The timezone `?` placeholder is only present in the `filterBetweenTwoDates()` SQL (line 22); it is absent from the `filterStartOnly()` (line 19) and `filterEndOnly()` (line 20) SQL strings.

If `filter.timezone()` is non-null and `filter.end()` is null (start-only path), `prepareStatement` will bind a timezone string as the first parameter, then bind the start date as the second parameter. The SQL only has one placeholder (`>= ?`), meaning the extra bind will either throw a `SQLException` at runtime or silently corrupt the parameter index shared with subsequent handlers.

Concrete scenario:
- `filter.timezone() = "America/Chicago"`, `filter.start() = <date>`, `filter.end() = null`
- `getQueryFilter()` returns `" AND field >= ?"` (1 placeholder)
- `prepareStatement` binds index 1 = `"America/Chicago"`, index 2 = `<date>` — index 2 has no corresponding `?`

This is a latent runtime correctness bug whenever timezone is set and only a single date bound is supplied.

---

### A91-3 | MEDIUM | DateBetweenFilterHandler.java:29 | Inconsistent spacing style in `if` statement

Line 29 uses `if(filter.timezone() != null)` with no space between `if` and the opening parenthesis, while lines 28, 30, and 31 all use `if (...)` with a space. This is a style inconsistency within the same method.

```java
if (ignoreFilter()) return;           // line 28 — space present
if(filter.timezone() != null) ...     // line 29 — space absent
if (filter.start() != null) ...       // line 30 — space present
if (filter.end() != null) ...         // line 31 — space present
```

---

### A91-4 | MEDIUM | DateBetweenFilterHandler.java:34-36 | `ignoreFilter()` can never be true — `filter` is a `final` field set in the constructor, making the null guard misleading

The constructor (line 11) accepts a `DateBetweenFilter filter` parameter and assigns it to the `final` field `this.filter`. There is no null check at construction time. If a caller passes `null` for `filter`, the field is permanently null and every call to `filterStartOnly()`, `filterEndOnly()`, and `filterBetweenTwoDates()` will throw a `NullPointerException` before `ignoreFilter()` can short-circuit them — because those private methods are called in `getQueryFilter()` only after `ignoreFilter()` returns false, but `ignoreFilter()` calls `filter == null` which is fine. Actually the NPE path is safe in `getQueryFilter()`.

However, in `prepareStatement` (line 28), the guard `if (ignoreFilter()) return;` correctly prevents NPE. The issue is the asymmetry: the contract suggests a null filter is a valid "no-op" input, but there is no null check on `filter` at construction time. Callers may be confused about whether null is valid. This is a leaky abstraction — the null-tolerance policy is implicit and undocumented, and the guard exists in one method only because `filter` is directly field-accessed via the `DateBetweenFilter` interface methods in the private helpers (`filter.start()`, etc.), which would NPE if `filter` were null and `ignoreFilter()` somehow returned false. The guard is only safe because it is checked first, but this is a fragile invariant with no constructor-level enforcement.

---

### A91-5 | LOW | ImpactLevelFilter.java (whole file) | Single-method interface has no corresponding `FilterHandler` contract

`ImpactLevelFilter` is a filter data interface (like `DateBetweenFilter`) but it does **not** extend `FilterHandler`. `DateBetweenFilter`, `SessionDriverFilter`, `SessionUnitFilter`, `UnitManufactureFilter`, and `UnitTypeFilter` all follow the same pattern: a plain data interface paired with a separate `*FilterHandler` implementing `FilterHandler`. `ImpactLevelFilter` follows this pattern correctly on its own.

This finding is informational: the naming pattern is symmetric and correct. No issue.

*(Finding withdrawn — correct design, not a problem.)*

---

### A91-5 | LOW | FilterHandler.java:10 | Interface contract inconsistency — `prepareStatement` declares `throws SQLException` but one implementation omits it

`FilterHandler.prepareStatement` declares `throws SQLException` (line 10). All implementations in the package declare the same throws clause **except** `ImpactLevelFilterHandler` (line 32 of that file), which omits it. While a narrower throws clause on an override is legal Java, it creates a visible style inconsistency within this tightly cohesive package and may mislead callers who pattern-match on the interface signature. Callers iterating `List<FilterHandler>` must handle `SQLException` per the interface contract, which is correct; the missing `throws` on the concrete class is merely an inconsistency, not a bug.

---

### A91-6 | INFO | DateBetweenFilterHandler.java:22 | Hard-coded timezone literal `'UTC'` in SQL fragment reduces flexibility

The SQL expression `%s at time zone 'UTC'` (line 22) hard-codes the source timezone of the stored timestamp as `UTC`. This assumption is correct only if all stored timestamps are in UTC. If the storage timezone ever changes, this SQL must be updated manually. The target timezone is correctly parameterized (`timezone(?, ...)`). This is a minor design note rather than a defect — it is acceptable if UTC storage is an invariant of the schema — but it is worth flagging for documentation.

---

## Summary Table

| ID    | Severity | File                              | Line | Short Description                                                    |
|-------|----------|-----------------------------------|------|----------------------------------------------------------------------|
| A91-1 | HIGH     | DateBetweenFilterHandler.java     | 21   | Commented-out old SQL expression left in production source           |
| A91-2 | HIGH     | DateBetweenFilterHandler.java     | 29–31| Timezone parameter bound on start-only/end-only paths that have no `?` placeholder for it |
| A91-3 | MEDIUM   | DateBetweenFilterHandler.java     | 29   | Missing space after `if` keyword, inconsistent with rest of method   |
| A91-4 | MEDIUM   | DateBetweenFilterHandler.java     | 11,34| Null filter accepted at construction but no constructor-level guard; null-tolerance is implicit |
| A91-5 | LOW      | FilterHandler.java / ImpactLevelFilterHandler.java | 10 / 32 | `throws SQLException` omitted on `ImpactLevelFilterHandler.prepareStatement` override, inconsistent with all other handler implementations |
| A91-6 | INFO     | DateBetweenFilterHandler.java     | 22   | Hard-coded `'UTC'` source timezone in SQL reduces adaptability       |
# Pass 4 Code Quality — Agent A92

**Audit date:** 2026-02-26
**Assigned files:**
- `src/main/java/com/querybuilder/filters/ImpactLevelFilterHandler.java`
- `src/main/java/com/querybuilder/filters/SessionDriverFilter.java`
- `src/main/java/com/querybuilder/filters/SessionDriverFilterHandler.java`

---

## Reading Evidence

### File 1: `ImpactLevelFilterHandler.java`

**Class:** `com.querybuilder.filters.ImpactLevelFilterHandler`
**Implements:** `FilterHandler`

**Fields:**
- `filter` — `ImpactLevelFilter` (private final, line 6)
- `impactFieldName` — `String` (private final, line 7)
- `thresholdFieldName` — `String` (private final, line 8)

**Methods:**
| Name | Line | Visibility |
|---|---|---|
| `ImpactLevelFilterHandler(ImpactLevelFilter, String, String)` | 10 | public (constructor) |
| `getQueryFilter()` | 17 | public (override) |
| `prepareStatement(StatementPreparer)` | 32 | public (override) |
| `ignoreFilter()` | 36 | private |

**Types referenced:** `ImpactLevelFilter`, `FilterHandler`, `StatementPreparer`, `ImpactLevel` (enum via `filter.impactLevel()`) with values `RED`, `AMBER`, `BLUE`

**Constants/literals:** Magic multipliers `10` and `5` used inline in SQL strings (lines 21–25)

---

### File 2: `SessionDriverFilter.java`

**Interface:** `com.querybuilder.filters.SessionDriverFilter`

**Methods:**
| Name | Line |
|---|---|
| `driverId()` | 4 |

**Returns:** `Long`

---

### File 3: `SessionDriverFilterHandler.java`

**Class:** `com.querybuilder.filters.SessionDriverFilterHandler`
**Implements:** `FilterHandler`

**Fields:**
- `filter` — `SessionDriverFilter` (private final, line 8)
- `driverIdFieldName` — `String` (private final, line 9)

**Methods:**
| Name | Line | Visibility |
|---|---|---|
| `SessionDriverFilterHandler(SessionDriverFilter, String)` | 11 | public (constructor) |
| `getQueryFilter()` | 17 | public (override) |
| `prepareStatement(StatementPreparer)` | 23 | public (override) |
| `ignoreFilter()` | 28 | private |

---

## Findings

A92-1 | LOW | ImpactLevelFilterHandler.java:18 | `ignoreFilter()` logic is inverted in `getQueryFilter()`. The guard condition at line 18 is named `ignoreFilter()` yet when it returns `true` the method does NOT ignore the filter — it returns a hardcoded fallback SQL fragment (`AND %s > %s`). Every other `FilterHandler` implementation (e.g. `SessionDriverFilterHandler`, `SessionUnitFilterHandler`, `DateBetweenFilterHandler`) returns `""` (empty string) when `ignoreFilter()` is true, meaning "apply no filter". Here, returning a non-empty SQL clause when the filter is null/unset is semantically inconsistent with the contract established by the rest of the pattern, and the name `ignoreFilter()` is therefore misleading for the branch taken at line 18.

A92-2 | MEDIUM | ImpactLevelFilterHandler.java:21,23,25 | Magic numbers `10` and `5` are embedded as bare integer literals directly inside SQL format strings. These multipliers define the RED/AMBER/BLUE threshold boundaries and carry significant business logic; they are not named, documented, or extracted to named constants. Any change to the threshold algorithm requires hunting through raw strings. Compare with `SessionDriverFilterHandler` and `SessionUnitFilterHandler` which have no such literals. Named constants (e.g. `RED_MULTIPLIER`, `AMBER_MULTIPLIER`) should be used.

A92-3 | LOW | ImpactLevelFilterHandler.java:32-34 | `prepareStatement()` has an empty body. The interface `FilterHandler` declares `prepareStatement` as a method that may throw `SQLException`; all sibling handlers either add bind parameters or explicitly short-circuit. An empty body is correct here only because the SQL for impact level uses column references rather than `?` placeholders — but there is no comment explaining why, making it appear like an incomplete implementation (a future maintainer may add `?` placeholders to the SQL strings and forget to update this method).

A92-4 | LOW | ImpactLevelFilterHandler.java:17-29 | Inconsistent formatting style compared to sibling files. `ignoreFilter()` body at line 36-38 uses a multi-line brace style, while `SessionDriverFilterHandler.java` line 28 and `SessionUnitFilterHandler.java` line 28 place the entire `ignoreFilter()` body on a single line (`private boolean ignoreFilter() { return ...; }`). Within `getQueryFilter()`, the guard clause at line 18 is on one line with no braces, while the `switch` block uses standard multi-line formatting. These are minor but represent inconsistent style across what is otherwise a uniform pattern of small handler classes.

A92-5 | INFO | ImpactLevelFilterHandler.java:26-28 | The `default` branch of the `switch` on `ImpactLevel` (line 26) returns `""`. The `ImpactLevel` enum has exactly three values: `BLUE`, `AMBER`, `RED` — all handled by named `case` branches. The `default` is therefore currently unreachable dead code. If the enum gains a new value in future, silently returning an empty string (i.e., applying no filter) could be a data-exposure bug. A `default` that either throws `IllegalArgumentException` or logs/asserts would be safer, but at minimum the dead-code nature of the branch should be noted.

A92-6 | INFO | SessionDriverFilter.java:1-5 | `SessionDriverFilter` is structurally identical to `SessionUnitFilter` (both are single-method interfaces returning `Long`). This is not necessarily wrong — the distinct types enforce type safety at call sites — but it is worth noting for any future refactoring toward a generic parameterized `IdFilter<T>` abstraction if the pattern continues to proliferate.
# Pass 4 (Code Quality) — Agent A93
**Date:** 2026-02-26
**Audit run folder:** `C:/Projects/cig-audit/repos/forkliftiqadmin/audit/2026-02-26-01/`

---

## Assigned Files

1. `src/main/java/com/querybuilder/filters/SessionUnitFilter.java`
2. `src/main/java/com/querybuilder/filters/SessionUnitFilterHandler.java`
3. `src/main/java/com/querybuilder/filters/StringContainingFilterHandler.java`

---

## Reading Evidence

### File 1: `SessionUnitFilter.java`

- **Type:** `interface SessionUnitFilter` (package `com.querybuilder.filters`)
- **Methods:**
  - `unitId()` — line 4 (abstract, returns `Long`)
- **Constants/Fields:** none
- **Implements:** nothing (marker-style single-method interface)

---

### File 2: `SessionUnitFilterHandler.java`

- **Type:** `class SessionUnitFilterHandler` (package `com.querybuilder.filters`)
- **Implements:** `FilterHandler`
- **Fields:**
  - `filter` — `SessionUnitFilter`, `private final`, line 8
  - `unitIdFieldName` — `String`, `private final`, line 9
- **Methods:**
  - `SessionUnitFilterHandler(SessionUnitFilter filter, String unitIdFieldName)` — constructor, line 11
  - `getQueryFilter()` — line 17 (`@Override`)
  - `prepareStatement(StatementPreparer preparer)` — line 23 (`@Override`, `throws SQLException`)
  - `ignoreFilter()` — line 28 (`private boolean`)
- **Constants:** none

---

### File 3: `StringContainingFilterHandler.java`

- **Type:** `class StringContainingFilterHandler` (package `com.querybuilder.filters`)
- **Implements:** `FilterHandler`
- **Fields:**
  - `searchText` — `String`, `private final`, line 10
  - `fieldNames` — `List<String>`, `private final`, line 11
- **Methods:**
  - `StringContainingFilterHandler(String searchText, String... fieldNames)` — constructor, line 13
  - `getQueryFilter()` — line 19 (`@Override`)
  - `prepareStatement(StatementPreparer preparer)` — line 33 (`@Override`, `throws SQLException`)
- **Constants:** none

---

## Findings

### A93-1 | LOW | SessionUnitFilterHandler.java:28 | Single-line private method body inconsistent with surrounding multi-line style

The `ignoreFilter()` method at line 28 collapses the entire method onto a single line:

```java
private boolean ignoreFilter() { return filter == null || filter.unitId() == null; }
```

The identical companion class `SessionDriverFilterHandler` (line 28) uses the exact same single-line format, making this a systemic pattern rather than an isolated choice — however, `DateBetweenFilterHandler` expands `ignoreFilter()` across three lines with a standard method body. There is no project-wide style guide enforcing either form, resulting in inconsistent formatting across the sibling handler classes in the same package.

---

### A93-2 | LOW | StringContainingFilterHandler.java:34 | Loop variable `i` is unused — counter-based for loop should be an enhanced for loop

In `prepareStatement`, a traditional indexed `for` loop is used but the loop variable `i` is never used inside the body — `fieldNames.get(i)` is never called; only `searchText` is passed to `addString`:

```java
for (int i = 0; i < fieldNames.size(); ++i)
    preparer.addString(searchText);
```

The index `i` serves no purpose. This should be an enhanced for-each loop (or `Collections.nCopies` / `IntStream`) to clearly express intent, eliminate the unused variable, and avoid potential off-by-one confusion for future readers. This also represents a minor build-warning candidate in strict lint configurations (unused variable).

---

### A93-3 | MEDIUM | StringContainingFilterHandler.java:13-14 | Constructor silently mutates `searchText` — leaky/surprising abstraction

The constructor accepts `searchText` as the caller's raw string but immediately wraps it with `%…%` wildcards before storing it:

```java
public StringContainingFilterHandler(String searchText, String... fieldNames) {
    this.searchText = "%" + searchText + "%";
    ...
}
```

There is no documentation (Javadoc or inline comment) explaining this transformation. A caller passing `"abc"` will find that the stored `searchText` is `"%abc%"`, but there is no way to retrieve or inspect the transformed value. The mutation is invisible from the public API and constitutes an internal implementation detail leaking through constructor side-effects. A `null` input for `searchText` would also produce the string `"%null%"` (a `NullPointerException` is not thrown), silently producing an unintended SQL `ILIKE '%null%'` query.

---

### A93-4 | MEDIUM | StringContainingFilterHandler.java:19-30 | `getQueryFilter()` returns different structural forms for single vs. multiple fields without consistent trailing space/format

For one field:
```java
return String.format(" AND %s ILIKE ? ", fieldNames.get(0));
```
For multiple fields the method builds a `StringBuilder` manually. The single-field path adds a trailing space after `?`; the multi-field path appends `") "` (one trailing space). These are consistent with each other in the trailing space, but the divergence between using `String.format` for one case and a manual `StringBuilder` with a hardcoded `delete` offset for the other case means:

- The `delete(filter.length() - 4, filter.length())` call at line 27 strips the trailing `" OR "` (4 characters). This is a magic-number deletion that is fragile — if the separator string `" OR "` is ever changed (e.g., to `" or "` or `" || "`), the deletion length must be updated separately or the SQL will be corrupted. This is a latent correctness risk.

---

### A93-5 | LOW | SessionUnitFilterHandler.java:19 | SQL fragment contains asymmetric padding spaces

```java
return String.format(" AND %s = ? ", unitIdFieldName);
```

The fragment has a leading space and a trailing space after `?`. The same pattern appears in `SessionDriverFilterHandler`. While consistent between those two classes, it differs from `DateBetweenFilterHandler` (line 19-22) which omits the trailing space after `?` in its single-field formats (e.g., `" AND %s >= ?"`). Inconsistent whitespace padding in SQL fragments across the filter handler family can make query debugging harder.

---

### A93-6 | INFO | SessionUnitFilter.java:1-5 | Interface is a single-method functional interface but is not annotated `@FunctionalInterface`

`SessionUnitFilter` declares exactly one abstract method (`unitId()`). In Java 8+, single-abstract-method interfaces are eligible for lambda usage. Annotating with `@FunctionalInterface` would enforce this contract at compile time and document intent. The omission is not a defect but is an opportunity cost. The sibling `SessionDriverFilter` (not in scope) presumably has the same omission.

---

### A93-7 | LOW | SessionUnitFilterHandler.java:18,24 | `ignoreFilter()` called twice per public method — redundant double-guard pattern with no caching

Both `getQueryFilter()` (line 18) and `prepareStatement()` (line 24) each call `ignoreFilter()` independently. Since `filter` and `filter.unitId()` are both `final` fields set at construction time, the result of `ignoreFilter()` is constant for the lifetime of the object. Calling it twice per method is harmless but adds a micro-inefficiency and duplicates logic that could be resolved once (e.g., at construction). The same pattern exists identically in `SessionDriverFilterHandler`. This is a systemic style issue across the sibling handler classes.

---

## Summary Table

| ID    | Severity | File                              | Line(s) | Issue                                                              |
|-------|----------|-----------------------------------|---------|--------------------------------------------------------------------|
| A93-1 | LOW      | SessionUnitFilterHandler.java     | 28      | Single-line method body inconsistent with `DateBetweenFilterHandler` style |
| A93-2 | LOW      | StringContainingFilterHandler.java | 34–35  | Unused loop variable `i`; indexed for-loop should be enhanced for-each |
| A93-3 | MEDIUM   | StringContainingFilterHandler.java | 13–14  | Silent `%…%` mutation of `searchText` in constructor; `null` input produces `"%null%"` |
| A93-4 | MEDIUM   | StringContainingFilterHandler.java | 27      | Magic-number `delete(length-4)` to strip `" OR "` — fragile separator removal |
| A93-5 | LOW      | SessionUnitFilterHandler.java     | 19      | Asymmetric trailing-space padding in SQL fragment vs. `DateBetweenFilterHandler` siblings |
| A93-6 | INFO     | SessionUnitFilter.java            | 3       | Single-method interface missing `@FunctionalInterface` annotation  |
| A93-7 | LOW      | SessionUnitFilterHandler.java     | 18,24   | `ignoreFilter()` called twice per method; constant result could be computed once at construction |
# Pass 4 (Code Quality) — Agent A94

**Audit date:** 2026-02-26
**Agent:** A94
**Files reviewed:**
- `src/main/java/com/querybuilder/filters/UnitManufactureFilter.java`
- `src/main/java/com/querybuilder/filters/UnitManufactureFilterHandler.java`
- `src/main/java/com/querybuilder/filters/UnitTypeFilter.java`

---

## Reading Evidence

### File 1: UnitManufactureFilter.java

- **Type:** Interface
- **Full name:** `com.querybuilder.filters.UnitManufactureFilter`
- **Methods:**
  - `manufactureId()` — line 4 (abstract, returns `Long`)
- **Constants/types defined:** none
- **Imports:** none

---

### File 2: UnitManufactureFilterHandler.java

- **Type:** Class
- **Full name:** `com.querybuilder.filters.UnitManufactureFilterHandler`
- **Implements:** `FilterHandler`
- **Fields:**
  - `filter` — line 8, type `UnitManufactureFilter`, `private` (non-final)
  - `fieldName` — line 9, type `String`, `private final`
- **Methods:**
  - `UnitManufactureFilterHandler(UnitManufactureFilter filter, String fieldName)` — constructor, line 11
  - `getQueryFilter()` — line 16, returns `String`
  - `prepareStatement(StatementPreparer preparer)` — line 22, throws `SQLException`
  - `ignoreFilter()` — line 27, returns `boolean`, `private`
- **Constants/types defined:** none
- **Imports:** `com.querybuilder.StatementPreparer`, `java.sql.SQLException`

---

### File 3: UnitTypeFilter.java

- **Type:** Interface
- **Full name:** `com.querybuilder.filters.UnitTypeFilter`
- **Methods:**
  - `type()` — line 4 (abstract, returns `Long`)
- **Constants/types defined:** none
- **Imports:** none

---

## Findings

### A94-1 | MEDIUM | UnitManufactureFilterHandler.java:8 | Field `filter` is not `final`

The field `filter` on line 8 is declared `private UnitManufactureFilter filter` without the `final` modifier. Every other handler in this package — `UnitTypeFilterHandler` (line 8), `SessionUnitFilterHandler` (line 8), `SessionDriverFilterHandler` (line 8), and `ImpactLevelFilterHandler` (line 6) — declares the same conceptual field as `private final`. The handler has no setter and the field is only ever written in the constructor, so the missing `final` is an oversight. This is inconsistent style within the package and removes the immutability guarantee that the rest of the pattern relies on.

---

### A94-2 | MEDIUM | UnitManufactureFilterHandler.java:16 | `getQueryFilter()` is missing `@Override`

The `getQueryFilter()` method on line 16 implements `FilterHandler.getQueryFilter()` but has no `@Override` annotation. The immediately following method `prepareStatement` on line 22 carries `@Override`. In `UnitTypeFilterHandler`, both interface methods are consistently annotated with `@Override`. The missing annotation means the compiler cannot catch an accidental signature mismatch and the code is inconsistent with the rest of the package.

---

### A94-3 | LOW | UnitTypeFilter.java:4 | Interface method name `type()` is semantically weak

The single method declared by `UnitTypeFilter` is named `type()`. Every other filter interface in this package uses a descriptive noun that includes the domain entity: `manufactureId()`, `unitId()`, `driverId()`, `impactLevel()`. The name `type()` does not convey what kind of type is being filtered, making the interface harder to implement correctly without reading surrounding context. Consistent with naming conventions used elsewhere in the package, a name such as `unitTypeId()` would be clearer.

---

### A94-4 | LOW | UnitManufactureFilter.java:4 | Interface method name `manufactureId()` contains a misspelling

The method is named `manufactureId()` when the domain term is "manufacturer" (a noun denoting the entity). "Manufacture" is a verb or the act of manufacturing, not the entity itself. The same misspelling appears in the class name `UnitManufactureFilter` and `UnitManufactureFilterHandler`. While consistent within these three files, it is a misspelling that will propagate to every class that implements the interface and every call site that invokes the method.

---
# Pass 4 – Code Quality | Agent A95
Date: 2026-02-26
Assigned files:
- `src/main/java/com/querybuilder/filters/UnitTypeFilterHandler.java`
- `src/main/java/com/querybuilder/impacts/ImpactsByCompanyIdQuery.java`
- `src/main/java/com/querybuilder/impacts/ImpactsCountByCompanyIdQuery.java`

---

## Reading Evidence

### File 1 — `UnitTypeFilterHandler.java`

**Class:** `com.querybuilder.filters.UnitTypeFilterHandler`
**Implements:** `FilterHandler`

| Member | Kind | Line |
|--------|------|------|
| `filter` | private final field (`UnitTypeFilter`) | 8 |
| `fieldName` | private final field (`String`) | 9 |
| `UnitTypeFilterHandler(UnitTypeFilter, String)` | constructor | 11 |
| `getQueryFilter()` | public method (`String`) — `@Override` | 17 |
| `prepareStatement(StatementPreparer)` | public method (`void`) — `@Override`, throws `SQLException` | 23 |
| `ignoreFilter()` | private method (`boolean`) | 28 |

Types/constants defined: none.

---

### File 2 — `ImpactsByCompanyIdQuery.java`

**Class:** `com.querybuilder.impacts.ImpactsByCompanyIdQuery`

| Member | Kind | Line |
|--------|------|------|
| `BASE_QUERY` | private static final field (`String`) | 6 |
| `COUNT_QUERY` | package-private static final field (`String`) | 13 |
| `REPORT_QUERY` | package-private static final field (`String`) | 18 |
| `report(long, ImpactReportFilterBean)` | public static factory method | 23 |
| `count(long, String)` | public static factory method | 27 |

Types/constants defined: `BASE_QUERY`, `COUNT_QUERY`, `REPORT_QUERY` (SQL string constants).

---

### File 3 — `ImpactsCountByCompanyIdQuery.java`

**Class:** `com.querybuilder.impacts.ImpactsCountByCompanyIdQuery`

| Member | Kind | Line |
|--------|------|------|
| `companyId` | private final field (`long`) | 9 |
| `timezone` | private final field (`String`) | 10 |
| `ImpactsCountByCompanyIdQuery(long, String)` | package-private constructor | 12 |
| `query()` | public method (`Integer`), throws `SQLException` | 17 |
| `prepareStatement(PreparedStatement)` | private method (`void`), throws `SQLException` | 23 |

Types/constants defined: none.

---

## Findings

### A95-1 | MEDIUM | `UnitTypeFilterHandler.java:8` | Missing `@Override` on `getQueryFilter()`

`UnitTypeFilterHandler.prepareStatement` carries `@Override` (line 22) but `getQueryFilter()` (line 16–20) also carries `@Override`. However, the structural peer `UnitManufactureFilterHandler.getQueryFilter()` (line 16) is **missing** its `@Override` annotation while `prepareStatement` has it (line 21). This is an inconsistency across the filter-handler family rather than an issue within this file itself, but comparing the two: `UnitTypeFilterHandler` correctly annotates both overriding methods. No issue within this file — see A95-2 for the peer inconsistency.

> Self-correction: `UnitTypeFilterHandler` has `@Override` on both methods (lines 16 and 22). This file is correct. Finding withdrawn; see A95-2.

---

### A95-1 | LOW | `UnitTypeFilterHandler.java` (cross-file: `UnitManufactureFilterHandler.java:16`) | Missing `@Override` on sibling handler's `getQueryFilter()`

`UnitManufactureFilterHandler.getQueryFilter()` at line 16 omits the `@Override` annotation, while the structurally identical `UnitTypeFilterHandler.getQueryFilter()` includes it. Both implement `FilterHandler`. The omission is a style inconsistency in the same package and suppresses compiler verification that the method actually overrides the interface method. Reported here because it is visible only through comparison with the assigned file.

---

### A95-2 | MEDIUM | `UnitTypeFilterHandler.java:8` | `filter` field can never be `null` in practice — null guard in `ignoreFilter()` is misleading

The constructor at line 11 accepts `UnitTypeFilter filter` with no null check and assigns it directly to `this.filter`. The caller (`ImpactsReportByCompanyIdQuery`, line 26) always passes a non-null `ImpactReportFilterBean` (which also implements `UnitTypeFilter`). The null guard `filter == null` inside `ignoreFilter()` (line 29) therefore represents dead defensive code that signals a design ambiguity: either the constructor should validate and reject null (making the guard unnecessary), or the class genuinely needs to accept null (in which case the constructor's parameter should be documented). The identical pattern exists in `UnitManufactureFilterHandler`. The ambiguity makes the contract of the class unclear.

---

### A95-3 | MEDIUM | `ImpactsByCompanyIdQuery.java:13-14` | `COUNT_QUERY` and `REPORT_QUERY` are package-private (`static final`) but logically internal implementation details

`COUNT_QUERY` (line 13) and `REPORT_QUERY` (line 18) have no access modifier, making them package-private. They are raw SQL strings that are accessed directly by `ImpactsCountByCompanyIdQuery` (line 18) and `ImpactsReportByCompanyIdQuery` (line 42) respectively. Exposing raw SQL strings at package scope is a leaky abstraction: the SQL is an internal implementation detail that sibling classes reach into directly rather than going through a method. This creates tight coupling — changing the SQL requires knowing which external classes depend on the constant. Making them `private` and providing access via a method (which `ImpactsByCompanyIdQuery` already does for the outer factory methods `report()` and `count()`) would encapsulate the detail properly.

---

### A95-4 | LOW | `ImpactsByCompanyIdQuery.java:7-8` | Missing space before string concatenation creates a latent SQL syntax risk

At line 7–8, the SQL string fragments are concatenated as:
```
"FROM v_impacts vi " +
"LEFT JOIN unit_company uc ON uc.unit_id = vi.unit_id AND" +
"  uc.start_date <= ..."
```
The `AND` at the end of line 7 is immediately followed by a newline and two spaces at the start of the next fragment. While this produces valid SQL (the two spaces serve as the required whitespace separator), the pattern is inconsistent with all other line-break joins in `BASE_QUERY` and `COUNT_QUERY` where trailing spaces are placed at the end of the preceding fragment (e.g., `"FROM v_impacts vi "`, `"WHERE ..."`, etc.). A future editor adding a clause after the `AND` token at line 7 and following the surrounding style (trailing space on prior line) would accidentally drop the separator space. A trailing space on line 7 (`"AND "`) would be the consistent form.

---

### A95-5 | MEDIUM | `ImpactsByCompanyIdQuery.java:27` | Missing spaces around parameters in `count()` method signature

```java
public static ImpactsCountByCompanyIdQuery count(long companyId,String timezone) {
    return new ImpactsCountByCompanyIdQuery(companyId,timezone);
```
Both the parameter list (`,String`) and the constructor call (`,timezone`) are missing the standard space after the comma. The `report()` method directly above (line 23) and all other method signatures in the codebase use `", "` spacing. This is a minor style inconsistency but directly violates Java coding conventions.

---

### A95-6 | HIGH | `ImpactsCountByCompanyIdQuery.java:17` | Method returns boxed `Integer` instead of primitive `int`

```java
public Integer query() throws SQLException {
```
The method returns `Integer` (boxed), but always produces a concrete value — it resolves with `orElse(0)` (line 20), so `null` can never be returned. Using the boxed type adds unnecessary autoboxing overhead and communicates to callers that `null` is a possible return value, which it is not. The return type should be `int`. This is consistent with the analogous `ImpactsReportByCompanyIdQuery.query()` which correctly returns the concrete type `ImpactReportBean`.

---

### A95-7 | LOW | `ImpactsByCompanyIdQuery.java:15` | Double blank line between `COUNT_QUERY` and `REPORT_QUERY` constant declarations

Lines 15–17 contain two consecutive blank lines between the `COUNT_QUERY` and `REPORT_QUERY` constant declarations. Standard Java style (Oracle / Google) uses a single blank line between class-level declarations of the same kind. This is a minor formatting inconsistency; no other field block in the three audited files uses double blank lines.

---

### A95-8 | INFO | `ImpactsCountByCompanyIdQuery.java:24-27` | `companyId` is bound to two separate parameters by positional repetition

```java
statement.setLong(1, companyId);
statement.setLong(2, companyId);
statement.setString(3, timezone);
statement.setString(4, timezone);
```
The `COUNT_QUERY` uses `companyId` twice (`vi.comp_id = ? OR uc.company_id = ?`) and `timezone` twice. Both duplications are intentional and correct. This is an informational note only: there is no named-parameter abstraction, so a future change to the query that adds or reorders parameters will require careful manual synchronisation with this method. No defect exists currently.

---

## Summary

| ID | Severity | File | Issue |
|----|----------|------|-------|
| A95-1 | LOW | UnitManufactureFilterHandler.java:16 (sibling) | Missing `@Override` on `getQueryFilter()` — inconsistency vs UnitTypeFilterHandler |
| A95-2 | MEDIUM | UnitTypeFilterHandler.java:8,29 | Null guard on `filter` in `ignoreFilter()` is misleading — contract ambiguity |
| A95-3 | MEDIUM | ImpactsByCompanyIdQuery.java:13,18 | Package-private SQL constants are a leaky abstraction |
| A95-4 | LOW | ImpactsByCompanyIdQuery.java:7-8 | Inconsistent whitespace around `AND` at line break in SQL string |
| A95-5 | MEDIUM | ImpactsByCompanyIdQuery.java:27 | Missing spaces after commas in `count()` signature and body |
| A95-6 | HIGH | ImpactsCountByCompanyIdQuery.java:17 | `query()` returns boxed `Integer` instead of primitive `int` |
| A95-7 | LOW | ImpactsByCompanyIdQuery.java:15-17 | Double blank line between constant declarations |
| A95-8 | INFO | ImpactsCountByCompanyIdQuery.java:24-27 | Duplicate positional parameter bindings — no named-parameter abstraction |
# Pass 4 (Code Quality) – Agent A96
**Date:** 2026-02-26
**Auditor:** A96
**Files assigned:**
- `src/main/java/com/querybuilder/impacts/ImpactsReportByCompanyIdQuery.java`
- `src/main/java/com/querybuilder/incidents/IncidentReportByCompanyIdQuery.java`
- `src/main/java/com/querybuilder/preops/PreOpsByCompanyIdQuery.java`

---

## Reading Evidence

### File 1: `ImpactsReportByCompanyIdQuery.java`

**Package:** `com.querybuilder.impacts`
**Class:** `ImpactsReportByCompanyIdQuery`

Fields:
- `private final long companyId` (line 18)
- `private List<FilterHandler> filterHandlers` (line 19)

Constructor:
- `ImpactsReportByCompanyIdQuery(long companyId, ImpactReportFilterBean filter)` – line 21 (package-private)

Methods:
- `public ImpactReportBean query(String timezone, String dateFormat)` – line 31
- `private String getQuery()` – line 39
- `private void prepareStatement(PreparedStatement statement)` – line 45
- `private List<ImpactReportGroupBean> getResults(String timezone, String dateFormat, ResultSet rs)` – line 52

Types used/referenced: `ImpactReportBean`, `ImpactReportFilterBean`, `ImpactReportGroupBean`, `ImpactReportGroupEntryBean`, `FilterHandler`, `StatementPreparer`, `DBUtil`, `DateUtil`
Constants defined: none
Errors declared: `SQLException`

---

### File 2: `IncidentReportByCompanyIdQuery.java`

**Package:** `com.querybuilder.incidents`
**Class:** `IncidentReportByCompanyIdQuery`

Fields:
- `private static final String BASE_QUERY` (line 22)
- `private final int companyId` (line 29)
- `private List<FilterHandler> filterHandlers` (line 30)

Constructor:
- `public IncidentReportByCompanyIdQuery(int companyId, IncidentReportFilterBean filter)` – line 32 (public)

Methods:
- `public IncidentReportBean query(String timezone, String dateFormat)` – line 41
- `private String getQuery()` – line 47
- `private void prepareStatement(PreparedStatement statement)` – line 54
- `private IncidentReportEntryBean mapResult(String timezone, String dateFormat, ResultSet result)` – line 61

Types used/referenced: `IncidentReportBean`, `IncidentReportEntryBean`, `IncidentReportFilterBean`, `FilterHandler`, `DateBetweenFilterHandler`, `UnitManufactureFilterHandler`, `UnitTypeFilterHandler`, `StatementPreparer`, `DBUtil`, `DateUtil`, `RuntimeConf`
Constants defined: `BASE_QUERY` (private static final, line 22)
Errors declared: `SQLException`

---

### File 3: `PreOpsByCompanyIdQuery.java`

**Package:** `com.querybuilder.preops`
**Class:** `PreOpsByCompanyIdQuery`

Fields / Constants:
- `private static final String BASE_QUERY` (line 6)
- `static final String COUNT_QUERY` (line 9) – package-private
- `static final String REPORT_QUERY` (line 13) – package-private

Constructor: none (implicit default public no-arg constructor)

Methods:
- `public static PreOpsReportByCompanyIdQuery report(long companyId, PreOpsReportFilterBean filter)` – line 16
- `public static PreOpsCountByCompanyIdQuery count(long companyId, String timezone)` – line 20

Types used/referenced: `PreOpsReportFilterBean`, `PreOpsReportByCompanyIdQuery`, `PreOpsCountByCompanyIdQuery`

---

## Findings

### A96-1 | MEDIUM | ImpactsReportByCompanyIdQuery.java:21 | Package-private constructor inconsistent with sibling classes

`ImpactsReportByCompanyIdQuery` has a package-private (default-access) constructor, which is consistent with its factory pattern via `ImpactsByCompanyIdQuery.report()`. However, `IncidentReportByCompanyIdQuery` (line 32) exposes a `public` constructor directly, with no factory class gating access. This is a cross-module inconsistency: the impacts and preops subsystems use the factory + package-private constructor pattern, while the incidents subsystem bypasses it with a public constructor. Callers in the incidents subsystem can instantiate the query class directly without going through a factory, making the design inconsistent and harder to evolve uniformly.

---

### A96-2 | HIGH | IncidentReportByCompanyIdQuery.java:29 | `companyId` typed as `int` instead of `long`

The `companyId` field in `IncidentReportByCompanyIdQuery` is declared as `int` (line 29), while every other query class in the codebase (`ImpactsReportByCompanyIdQuery` line 18, `PreOpsReportByCompanyIdQuery` line 23, `PreOpsCountByCompanyIdQuery` line 10, `ImpactsCountByCompanyIdQuery` line 9) declares it as `long`. In `prepareStatement` (line 56–57) it is passed to `preparer.addLong()`, which silently widens the `int` to `long`. This is not a runtime error today but represents a type inconsistency: if company IDs ever exceed `Integer.MAX_VALUE` (2,147,483,647), or if the database column is BIGINT, values will be silently truncated at the API boundary before being widened again, producing incorrect query results.

---

### A96-3 | MEDIUM | IncidentReportByCompanyIdQuery.java:68-69 | Builder setter names use `snake_case`, violating Java naming conventions

The builder calls at lines 68–69 use `.event_time(...)` and `.near_miss(...)` and `.incident(...)` as setter names. These correspond to fields `event_time`, `near_miss`, and `incident` in `IncidentReportEntryBean` (confirmed in the bean at lines 24–26), which are themselves named in `snake_case`. Java naming conventions (JLS §6.1) require field and method names to use `camelCase`. Lombok's `@Builder` generates setter names directly from field names, so the root defect is in the bean declaration, but the call site in this file directly exposes the violation. The field `reportTime` also exists in the bean (line 17) but is never populated by this query's builder, which may be a dead field (see A96-5).

---

### A96-4 | LOW | PreOpsByCompanyIdQuery.java:20 | Missing space before `String` parameter in `count()` method signature

Line 20: `public static PreOpsCountByCompanyIdQuery count(long companyId,String timezone )` is missing a space after the comma between `companyId,` and `String`. The same pattern appears in `ImpactsByCompanyIdQuery.java` line 27: `count(long companyId,String timezone)`. Both diverge from the standard Java style of a single space after each comma in parameter lists. Minor but a consistent style lapse repeated across the factory classes.

---

### A96-5 | MEDIUM | IncidentReportEntryBean.java:17 (via IncidentReportByCompanyIdQuery.java:62-77) | `reportTime` field in `IncidentReportEntryBean` is never set by the query mapper

The `IncidentReportEntryBean` declares a `private String reportTime` field (bean line 17). The `mapResult` method in `IncidentReportByCompanyIdQuery` (lines 62–77) constructs the bean via builder but never calls `.reportTime(...)`. No other builder call in this file sets it either. If this field is used downstream by serialization or report rendering, it will always be `null`, producing silent data gaps. If it is genuinely unused, it is dead field that adds noise to the data model.

---

### A96-6 | LOW | ImpactsReportByCompanyIdQuery.java:19 | `filterHandlers` field is not declared `final`

`filterHandlers` (line 19) is assigned once in the constructor and never reassigned. It should be declared `final` to make the immutability intent explicit and prevent accidental reassignment. The same issue exists in `IncidentReportByCompanyIdQuery` line 30 and `PreOpsReportByCompanyIdQuery` line 24. All three classes share this omission.

---

### A96-7 | LOW | IncidentReportByCompanyIdQuery.java:75-76 | URL concatenation with potentially null database value

Lines 75–76 unconditionally concatenate `RuntimeConf.cloudImageURL` with `result.getString("signature")` and `result.getString("image")`. If either column is `NULL` in the database, `ResultSet.getString()` returns Java `null`, and string concatenation produces the literal string `"https://s3.amazonaws.com/forkliftiq360/image/null"`, which is a malformed URL that will silently propagate to API consumers. A null check or use of `Optional` should guard these concatenations.

---

### A96-8 | INFO | PreOpsByCompanyIdQuery.java:5-23 | Factory class is instantiable but should not be

`PreOpsByCompanyIdQuery` is a pure factory/namespace class — it has no instance state and only provides static factory methods and package-private constants. It lacks a private constructor, so the implicit public no-arg constructor allows instantiation (`new PreOpsByCompanyIdQuery()`), which serves no purpose. The same observation applies to `ImpactsByCompanyIdQuery`. A private no-arg constructor would prevent meaningless instantiation.

---

### A96-9 | LOW | PreOpsByCompanyIdQuery.java:14 | `REPORT_QUERY` contains a bare `%s` placeholder — no validation of the format argument

`REPORT_QUERY` (line 13–14) is defined as `"SELECT * " + BASE_QUERY + " %s ORDER BY result_id"`. The `%s` is filled by `String.format(PreOpsByCompanyIdQuery.REPORT_QUERY, filters)` in `PreOpsReportByCompanyIdQuery.getQuery()` (line 44). If the `filters` `StringBuilder` is empty (no filter handlers add content), the resulting SQL contains a bare space between the WHERE clause and `ORDER BY`, which is valid SQL but unintentional whitespace. More importantly, the pattern trusts that `filters` contains only safe SQL fragments generated internally — this is acceptable given the filter handler architecture, but the lack of any documentation comment on the constant makes the `%s` contract invisible to future maintainers.

---

### A96-10 | MEDIUM | ImpactsReportByCompanyIdQuery.java:35 | `Collections.sort()` used instead of `List.sort()` on a mutable list

Line 35 calls the static `Collections.sort(impactReportGroups)` on a concrete `ArrayList`. Since Java 8, the preferred idiom is `impactReportGroups.sort(null)` or `impactReportGroups.sort(Comparator.naturalOrder())`, which dispatches through the list's own `sort` method and can be optimized by the JVM. `Collections.sort()` is not deprecated but is the older pattern; all three sibling report classes should use the modern form consistently.
# Pass 4 (Code Quality) — Agent A97
**Date:** 2026-02-26
**Auditor:** A97

---

## Reading Evidence

### File 1: `PreOpsCountByCompanyIdQuery.java`
**Full path:** `src/main/java/com/querybuilder/preops/PreOpsCountByCompanyIdQuery.java`

- **Class:** `PreOpsCountByCompanyIdQuery` (package `com.querybuilder.preops`)
- **Fields:**
  - `companyId` — `private final long` (line 10)
  - `timezone` — `private final String` (line 11)
- **Methods:**
  - `PreOpsCountByCompanyIdQuery(long companyId, String timezone)` — constructor, line 13 (package-private)
  - `query()` — `public Integer`, line 18
  - `prepareStatement(PreparedStatement statement)` — `private void`, line 24
- **Types/Constants defined:** none (constants consumed from `PreOpsByCompanyIdQuery`)
- **Imports used:** `StatementPreparer`, `DBUtil`, `PreparedStatement`, `SQLException`

---

### File 2: `PreOpsReportByCompanyIdQuery.java`
**Full path:** `src/main/java/com/querybuilder/preops/PreOpsReportByCompanyIdQuery.java`

- **Class:** `PreOpsReportByCompanyIdQuery` (package `com.querybuilder.preops`)
- **Fields:**
  - `companyId` — `private final long` (line 23)
  - `filterHandlers` — `private List<FilterHandler>` (line 24) — not `final`
- **Methods:**
  - `PreOpsReportByCompanyIdQuery(long companyId, PreOpsReportFilterBean filter)` — constructor, line 26 (package-private)
  - `query(String timezone, String dateFormat)` — `public PreOpsReportBean`, line 35
  - `getQuery()` — `private String`, line 41
  - `prepareStatement(PreparedStatement statement)` — `private void`, line 47
  - `getResults(String timezone, String dateFormat, ResultSet rs)` — `private List<PreOpsReportEntryBean>`, line 55
- **Types/Constants defined:** none
- **Imports used:** all 12 imports appear to be used

---

### File 3: `SessionsByCompanyIdQuery.java`
**Full path:** `src/main/java/com/querybuilder/session/SessionsByCompanyIdQuery.java`

- **Class:** `SessionsByCompanyIdQuery` (package `com.querybuilder.session`)
- **Fields:**
  - `companyId` — `private int` (line 18) — not `final`
  - `filterHandlers` — `private List<FilterHandler>` (line 19) — not `final`
- **Methods:**
  - `SessionsByCompanyIdQuery(int companyId, SessionFilterBean filter)` — constructor, line 21 (private)
  - `query(String timezone, String dateFormat)` — `public SessionReportBean`, line 30
  - `getQuery()` — `private String`, line 40
  - `prepareStatement(PreparedStatement statement)` — `private void`, line 50
  - `getResults(String timezone, String dateFormat, ResultSet rs)` — `private SessionBean`, line 57
  - `report(int companyId, SessionFilterBean filter)` — `public static SessionsByCompanyIdQuery`, line 69 (factory method)
- **Types/Constants defined:** none (SQL query built inline in `getQuery()`)
- **Imports used:** wildcard import `com.querybuilder.filters.*` (line 7)

---

## Findings

### A97-1 | MEDIUM | `SessionsByCompanyIdQuery.java:18` | Field `companyId` not declared `final`

`SessionsByCompanyIdQuery.companyId` is assigned once in the constructor and never mutated, but is not declared `final`. The two analogous fields in `PreOpsCountByCompanyIdQuery` (line 10) and `PreOpsReportByCompanyIdQuery` (line 23) are both declared `private final long`. The session class breaks the established pattern and removes the compiler-enforced immutability guarantee.

---

### A97-2 | MEDIUM | `SessionsByCompanyIdQuery.java:19` | Field `filterHandlers` not declared `final`; inconsistent with sibling classes

`SessionsByCompanyIdQuery.filterHandlers` is not `final`. The equivalent fields in `PreOpsReportByCompanyIdQuery` (line 24) and `ImpactsReportByCompanyIdQuery` (line 19) are also not `final`, so this is a cross-module consistency issue shared by all three report-query classes. The field is assigned exactly once (in the constructor) and never reassigned; all three should be `final`.

---

### A97-3 | MEDIUM | `SessionsByCompanyIdQuery.java:18` | `companyId` typed as `int` while all peer query classes use `long`

`PreOpsCountByCompanyIdQuery.companyId` (line 10) and `PreOpsReportByCompanyIdQuery.companyId` (line 23) are `long`. The impacts counterparts also use `long`. `SessionsByCompanyIdQuery` uses `int` for the same conceptual identifier. This is a style/type inconsistency across the query-builder layer. A company ID stored as a `long` elsewhere could silently overflow when passed into `int`-typed parameters.

---

### A97-4 | MEDIUM | `SessionsByCompanyIdQuery.java:7` | Wildcard import `com.querybuilder.filters.*`

Line 7 uses `import com.querybuilder.filters.*;`. The equivalent filter imports in `PreOpsReportByCompanyIdQuery` (lines 7–10) are explicit named imports. Wildcard imports obscure which types are actually in use, complicate static analysis, and create a risk of accidental name collisions with future additions to the package.

---

### A97-5 | LOW | `SessionsByCompanyIdQuery.java:46` | Missing whitespace before `ORDER BY` clause causes malformed SQL

In `getQuery()`, line 46 appends `"order by session_start_time desc"` directly after the dynamic filter content without a leading space:

```java
query.append("order by session_start_time desc");
```

Line 42 ends the base `WHERE` clause with `= ?)` and line 44 appends each filter handler's output. If all filters produce empty strings the resulting SQL reads `...= ?)order by...` with no separating space, which is a syntax error at runtime. The analogous `REPORT_QUERY` in `PreOpsByCompanyIdQuery` (line 14) uses `" %s ORDER BY result_id"` with leading and trailing spaces protecting against exactly this issue.

---

### A97-6 | LOW | `SessionsByCompanyIdQuery.java:41-46` | SQL query string built inline rather than as a named constant

`PreOpsCountByCompanyIdQuery` and `PreOpsReportByCompanyIdQuery` delegate their SQL to named constants in `PreOpsByCompanyIdQuery` (`COUNT_QUERY`, `REPORT_QUERY`). `SessionsByCompanyIdQuery` builds its SQL inline inside `getQuery()` with no shared constant or companion class. This is architecturally inconsistent with the established pattern (facade class holding constants + separate query-execution classes) and makes the SQL harder to locate and test independently.

---

### A97-7 | LOW | `SessionsByCompanyIdQuery.java:41-46` | SQL keyword casing inconsistent with rest of codebase

The inline SQL in `getQuery()` uses lowercase keywords: `select`, `from`, `where`, `order by`. All SQL constants across `PreOpsByCompanyIdQuery`, `ImpactsByCompanyIdQuery`, etc. use uppercase SQL keywords (`SELECT`, `FROM`, `WHERE`, `ORDER BY`). Mixed casing is a style inconsistency that reduces readability.

---

### A97-8 | LOW | `PreOpsCountByCompanyIdQuery.java:24-30` | `companyId` bound three times without explanation

`prepareStatement` calls `preparer.addLong(companyId)` three times in succession (lines 26–28), corresponding to the three `?` placeholders in `BASE_QUERY` (`comp_id = ?`, `assigned_company_id = ?`, `unit_company_id = ?`). There is no comment linking each binding to its placeholder. This pattern is fragile: if the query is modified the number of bindings may silently fall out of sync. The same concern applies to `PreOpsReportByCompanyIdQuery.prepareStatement` (lines 49–51). This is a LOW documentation/maintainability issue rather than a defect.

---

### A97-9 | LOW | `PreOpsReportByCompanyIdQuery.java:77` | Use of `Objects.requireNonNull` as an assertion rather than a guard

Line 77 uses `Objects.requireNonNull(entry).getFailures().add(...)` to suppress a null-pointer analysis warning. `entry` can only be `null` on the very first row before it is assigned (lines 67–75 guarantee it is assigned whenever `prevResultId != resultId`), but the logical flow does ensure it is non-null at line 77 for any row the loop reaches. However, relying on `requireNonNull` as a runtime assertion rather than restructuring the loop (e.g., returning early or merging the null-check) produces a `NullPointerException` with no useful message if the assumption ever breaks, and signals intent poorly.

---

### A97-10 | INFO | `SessionsByCompanyIdQuery.java:21` | Constructor is `private`; only accessible via the `report` factory method

The constructor (line 21) is `private`, unlike the package-private constructors of `PreOpsCountByCompanyIdQuery` (line 13) and `PreOpsReportByCompanyIdQuery` (line 26). `SessionsByCompanyIdQuery` exposes a static factory `report(...)` (line 69) analogous to `PreOpsByCompanyIdQuery.report(...)`. The approaches are architecturally different: one class is responsible for both the factory and the execution (session), while the preops/impacts pattern separates those into a facade class and execution classes. This is an INFO-level architectural inconsistency; not a defect in isolation but part of the wider inconsistency flagged in A97-6.

---

## Summary

| ID     | Severity | File                                   | Issue                                                                  |
|--------|----------|----------------------------------------|------------------------------------------------------------------------|
| A97-1  | MEDIUM   | SessionsByCompanyIdQuery.java:18       | `companyId` field not `final`                                          |
| A97-2  | MEDIUM   | SessionsByCompanyIdQuery.java:19       | `filterHandlers` field not `final` (also affects preops/impacts peers) |
| A97-3  | MEDIUM   | SessionsByCompanyIdQuery.java:18       | `companyId` typed `int` vs `long` in all peer classes                  |
| A97-4  | MEDIUM   | SessionsByCompanyIdQuery.java:7        | Wildcard import instead of explicit imports                            |
| A97-5  | LOW      | SessionsByCompanyIdQuery.java:46       | Missing leading space before `ORDER BY` — potential SQL syntax error   |
| A97-6  | LOW      | SessionsByCompanyIdQuery.java:41-46    | SQL built inline instead of in a named constant/facade class           |
| A97-7  | LOW      | SessionsByCompanyIdQuery.java:41-46    | SQL keyword lowercase vs uppercase convention in rest of codebase      |
| A97-8  | LOW      | PreOpsCountByCompanyIdQuery.java:26-28 | Three repeated `companyId` bindings with no comment linking to query   |
| A97-9  | LOW      | PreOpsReportByCompanyIdQuery.java:77   | `Objects.requireNonNull` used as assertion rather than guard           |
| A97-10 | INFO     | SessionsByCompanyIdQuery.java:21       | Private constructor + embedded factory deviates from facade pattern    |
# Pass 4 (Code Quality) — Agent A98
**Audit date:** 2026-02-26
**Files reviewed:**
- `src/main/java/com/querybuilder/unit/UnitsByCompanyIdQuery.java`
- `src/main/java/com/querybuilder/unit/UnitsByIdQuery.java`

---

## Reading Evidence

### File 1: `UnitsByCompanyIdQuery.java`

**Class:** `com.querybuilder.unit.UnitsByCompanyIdQuery`

**Constants defined:**
| Name | Line | Value summary |
|------|------|---------------|
| `BASE_QUERY` (private static final String) | 14 | SELECT from `v_units` with comp_id / unit_company sub-query |

**Fields:**
| Name | Type | Line |
|------|------|------|
| `companyId` | `int` | 19 |
| `orderBy` | `String` | 20 |
| `activeUnitsOnly` | `String` | 21 |
| `filter` | `StringContainingFilterHandler` | 22 |

**Methods:**
| Method | Line | Visibility |
|--------|------|-----------|
| `UnitsByCompanyIdQuery(int companyId)` (constructor) | 24 | private |
| `prepare(int companyId)` | 29 | public static |
| `orderBy(String orderBy)` | 33 | public |
| `activeUnitsOnly()` | 38 | public |
| `containing(String text)` | 43 | public |
| `query()` | 48 | public |
| `prepareStatement(PreparedStatement statement)` | 59 | private |
| `mapResult(ResultSet result)` | 67 | private |

**Imports used:** `UnitBean`, `StatementPreparer`, `StringContainingFilterHandler`, `DBUtil`, `PreparedStatement`, `ResultSet`, `SQLException`, `List`

---

### File 2: `UnitsByIdQuery.java`

**Class:** `com.querybuilder.unit.UnitsByIdQuery`

**Constants defined:**
| Name | Line | Value summary |
|------|------|---------------|
| `query` (private static final String) | 14 | `SELECT * FROM v_units WHERE id = ?` |

**Fields:**
| Name | Type | Line |
|------|------|------|
| `unitId` | `long` | 16 |

**Methods:**
| Method | Line | Visibility |
|--------|------|-----------|
| `UnitsByIdQuery(long unitId)` (constructor) | 18 | private |
| `prepare(int unitId)` | 22 | public static |
| `query()` | 26 | public |
| `prepareStatement(PreparedStatement statement)` | 32 | private |
| `getResult(ResultSet result)` | 37 | public (effectively private via method reference only) |

**Imports used:** `UnitBean`, `StatementPreparer`, `DBUtil`, `StringUtils`, `PreparedStatement`, `ResultSet`, `SQLException`, `List`

---

## Findings

### UnitsByCompanyIdQuery.java

**A98-1 | LOW | UnitsByCompanyIdQuery.java:20-21 | Fields used as mutable SQL fragment accumulators instead of booleans**

`orderBy` and `activeUnitsOnly` are declared as `String` fields initialised to `""` and are used purely as SQL snippet holders. Their actual intent is a predicate flag (`activeUnitsOnly`) and a sort column string (`orderBy`). Using raw strings in this way conflates "not set" with an empty string, making `null` vs `""` semantics invisible and making the class harder to reason about. `activeUnitsOnly` in particular would be clearer as a `boolean` field that is appended to the query only inside `query()`, consistent with how `filter` is tested for `null` before use.

**A98-2 | LOW | UnitsByCompanyIdQuery.java:22 | Field declared as concrete type instead of interface**

`filter` is declared as `StringContainingFilterHandler` (a concrete class) rather than the `FilterHandler` interface it implements. This couples the class unnecessarily to the concrete implementation; declaring it as `FilterHandler` would be consistent with coding to interfaces and would allow other filter types to be accepted in future.

**A98-3 | MEDIUM | UnitsByCompanyIdQuery.java:33-35 | SQL injection risk via unsanitised `orderBy` string interpolation**

The `orderBy(String orderBy)` builder method directly concatenates the caller-supplied string into the SQL query:
```java
this.orderBy = " order by " + orderBy;
```
The resulting fragment is then appended to the query string at line 53 with no validation or whitelisting. Because this value is not passed through a `PreparedStatement` parameter placeholder it is not protected against SQL injection. Any caller that forwards user input here (e.g. a sort-column request parameter) opens a SQL injection vector.

**A98-4 | LOW | UnitsByCompanyIdQuery.java:61-62 | `companyId` stored as `int` but bound as `long`**

`companyId` is declared as `int` (line 19) but `StatementPreparer.addLong()` (which calls `setLong`) is used to bind it at lines 61-62. This implicit widening is harmless at runtime but is inconsistent with the field declaration and signals either that `addInt` should be used or that the field type should be `long`. The inconsistency also appears in the `prepare` factory: the parameter is `int companyId`, mirroring the field.

**A98-5 | MEDIUM | UnitsByCompanyIdQuery.java:51-52 | Brace-less `if` body (style)**

```java
if (filter != null)
    query.append(filter.getQueryFilter());
```
The same pattern appears at lines 63-64. While syntactically valid, the project uses braces elsewhere (e.g. the `@Builder` constructor in `UnitBean`). Brace-less single-statement `if` bodies are a well-known source of maintenance bugs. Both occurrences should use braces for consistency.

---

### UnitsByIdQuery.java

**A98-6 | LOW | UnitsByIdQuery.java:14 | Constant `query` violates Java naming convention for constants**

```java
private static final String query = "SELECT * FROM v_units WHERE id = ?";
```
Java convention (JLS / Oracle style guide) requires `static final` constants to use `UPPER_SNAKE_CASE`. The field should be named `QUERY` or `BASE_QUERY`. Contrast with `UnitsByCompanyIdQuery` in the same package, which correctly names its constant `BASE_QUERY` (line 14 of that file).

**A98-7 | MEDIUM | UnitsByIdQuery.java:14 | `SELECT *` used instead of explicit column list**

The query selects all columns from `v_units` with `SELECT *`. This is a maintenance hazard: any column added to or removed from the view will silently break or expand `mapResult` with no compile-time notice. `UnitsByCompanyIdQuery` in the same package uses an explicit column list. The two files are inconsistent and `SELECT *` is the worse pattern.

**A98-8 | MEDIUM | UnitsByIdQuery.java:22-23 | Type narrowing in public factory: parameter is `int`, field is `long`**

```java
public static UnitsByIdQuery prepare(int unitId) {   // line 22
    return new UnitsByIdQuery(unitId);                // widens int -> long
```
The private constructor (line 18) accepts `long unitId` and the field is `long`. The public factory accepts `int`. Any caller passing a valid `long` unit ID that exceeds `Integer.MAX_VALUE` cannot use this factory without a cast, introducing a silent truncation risk if the caller inadvertently uses `int` arithmetic before calling `prepare`. The factory parameter should be `long` to match the field.

**A98-9 | LOW | UnitsByIdQuery.java:56-57, 59-60 | `result.getString(...)` called twice per column**

```java
.access_type(StringUtils.isNotBlank(result.getString("access_type")) ?
        result.getString("access_type").trim() : null)
.keypad_reader(StringUtils.isNotBlank(result.getString("keypad_reader")) ?
        UnitBean.KeypadReaderModel.valueOf(result.getString("keypad_reader").trim()) : null)
```
Each column is read from the `ResultSet` twice in the same expression (once to test blankness, once to use the value). While JDBC drivers typically permit this, it is wasteful and inconsistent — all other columns are read once. A local variable should be used to read each column once.

**A98-10 | LOW | UnitsByIdQuery.java:6 | Unused import `org.apache.commons.lang.StringUtils`**

`StringUtils` from `org.apache.commons.lang` (Commons Lang 2.x) is used at lines 56 and 59. However, the project should verify whether `commons-lang` (2.x) or `commons-lang3` (3.x, package `org.apache.commons.lang3`) is the declared dependency, as mixing the two causes a build warning or runtime failure. This import also couples the mapper to a third-party utility for a task (`isNotBlank` + `trim`) that could be handled with a small private helper, reducing the external dependency footprint in a data-mapping class.

**A98-11 | INFO | UnitsByIdQuery.java:37 | Result-mapping method named `getResult` while peer class uses `mapResult`**

`UnitsByIdQuery.getResult` (line 37) versus `UnitsByCompanyIdQuery.mapResult` (line 67). Both methods serve the identical role of mapping a `ResultSet` row to a `UnitBean`. The inconsistent naming within the same package makes the codebase harder to navigate and understand. One consistent name should be adopted across all query classes in this package.

---

## Summary

| ID | Severity | File | Short description |
|----|----------|------|-------------------|
| A98-1 | LOW | UnitsByCompanyIdQuery.java:20-21 | String fields used as SQL fragment accumulators instead of booleans |
| A98-2 | LOW | UnitsByCompanyIdQuery.java:22 | Concrete type used instead of `FilterHandler` interface |
| A98-3 | MEDIUM | UnitsByCompanyIdQuery.java:33-35 | SQL injection via unsanitised `orderBy` string interpolation |
| A98-4 | LOW | UnitsByCompanyIdQuery.java:19,61-62 | `int` field bound via `addLong` — type inconsistency |
| A98-5 | MEDIUM | UnitsByCompanyIdQuery.java:51-52,63-64 | Brace-less `if` bodies — maintenance hazard |
| A98-6 | LOW | UnitsByIdQuery.java:14 | Constant `query` not in `UPPER_SNAKE_CASE` |
| A98-7 | MEDIUM | UnitsByIdQuery.java:14 | `SELECT *` instead of explicit column list |
| A98-8 | MEDIUM | UnitsByIdQuery.java:22-23 | Factory parameter `int` narrows `long` field — truncation risk |
| A98-9 | LOW | UnitsByIdQuery.java:56-57,59-60 | Each column read twice from `ResultSet` in ternary expression |
| A98-10 | LOW | UnitsByIdQuery.java:6 | Verify Commons Lang version (2.x vs 3.x); consider removing third-party dependency |
| A98-11 | INFO | UnitsByIdQuery.java:37 | Result-mapper method name inconsistent with peer class (`getResult` vs `mapResult`) |
# Pass 4 (Code Quality) — Agent A99
**Files audited:**
- `src/main/java/com/report/FleetCheckAlert.java`
- `src/main/java/com/report/PreFlightReport.java`
- `src/main/java/com/report/ReportAPI.java`

---

## Reading Evidence

### FleetCheckAlert.java
**Class:** `FleetCheckAlert extends PreFlightReport`

**Fields:**
- `private static Logger log` (line 18) — static logger

**Methods:**
| Method | Line |
|--------|------|
| `FleetCheckAlert(PropertyMessageResources p)` (constructor) | 21 |
| `FleetCheckAlert()` (constructor) | 26 |
| `getLogo(String compId)` | 42 |
| `appendHtmlAlertCotent(String compId)` | 58 |
| `setContent(int resultId)` | 80 |

**Commented-out blocks:**
- `getLindeLogo(String compId)` — lines 31–40
- `appendHtmlAlertCotentLinde(String compId)` — lines 69–79
- `setLindeContent(int resultId)` — lines 170–225

**Types/constants defined:** none locally (uses `RuntimeConf`, `InfoLogger`, etc. from other packages)

---

### PreFlightReport.java
**Class:** `PreFlightReport`

**Fields:**
- `protected String subject` (line 17)
- `protected String title` (line 18)
- `protected Date eDate` (line 19)
- `protected Date sDate` (line 20)
- `protected String frequency` (line 21)
- `protected String content` (line 22)
- `protected String sEmail` (line 23)
- `protected String rEmail` (line 24)
- `protected String htmlCotent` (line 25)
- `PropertyMessageResources pm` (line 26) — package-private (no access modifier)

**Methods:**
| Method | Line |
|--------|------|
| `PreFlightReport()` (constructor) | 29 |
| `PreFlightReport(PropertyMessageResources p)` (constructor) | 35 |
| `PreFlightReport(Date eDate, String frequency, PropertyMessageResources p)` (constructor) | 40 |
| `getPm()` | 49 |
| `setPm(PropertyMessageResources pm)` | 53 |
| `getHtmlCotent()` | 57 |
| `setHtmlCotent(String htmlCotent)` | 61 |
| `appendHtmlCotent()` | 65 |
| `appendHtmlAlertCotent()` | 77 |
| `getTitle()` | 89 |
| `setTitle(String title)` | 92 |
| `getSubject()` | 95 |
| `setSubject(String subject)` | 98 |
| `getContent()` | 101 |
| `setContent(String compId)` | 105 |
| `getFrequency()` | 110 |
| `setFrequency(String frequency)` | 113 |
| `getsEmail()` | 116 |
| `setsEmail(String sEmail)` | 119 |
| `getrEmail()` | 122 |
| `setrEmail(String rEmail)` | 125 |
| `geteDate()` | 128 |
| `seteDate(Date eDate)` | 131 |
| `getsDate()` | 134 |
| `setsDate(Date sDate)` | 137 |
| `caculatesDate()` | 141 |
| `getDriverName(Long driverId)` | 146 |
| `getUnitName(String unitId)` | 159 |

**Commented-out blocks:**
- `getDriverNameLinde(String driver_id)` — lines 152–157
- `getUnitNameLinde(String unitId)` — lines 165–170

**Imports unused:** `MessageResources` (line 5), `CompanyDAO` (line 8), `Util` (line 13), `UnitBean` (line 15)

---

### ReportAPI.java
**Class:** `ReportAPI`

**Fields:**
- `protected String subject` (line 11)
- `protected String title` (line 12)
- `protected String content` (line 14)
- `protected String sEmail` (line 15)
- `protected String rEmail` (line 16)
- `protected String fileURL` (line 17)
- `protected String name` (line 18)
- `protected String input` (line 19)
- `protected int responseCode` (line 20)

**Methods:**
| Method | Line |
|--------|------|
| `getResponseCode()` | 22 |
| `setResponseCode(int responseCode)` | 26 |
| `ReportAPI(String name, String input)` (constructor) | 30 |
| `downloadPDF()` | 38 |
| `getExportDir(String dirctory)` | 46 |
| `getSubject()` | 51 |
| `setSubject(String subject)` | 55 |
| `getTitle()` | 59 |
| `setTitle(String title)` | 63 |
| `getContent()` | 68 |
| `setContent(String content)` | 72 |
| `getsEmail()` | 76 |
| `setsEmail(String sEmail)` | 80 |
| `getrEmail()` | 84 |
| `setrEmail(String rEmail)` | 88 |
| `getFileURL()` | 92 |
| `setFileURL(String fileURL)` | 96 |
| `getName()` | 100 |
| `setName(String name)` | 104 |

**Unused imports:** `RuntimeConf` (line 6), `Util` (line 7)

---

## Findings

### FleetCheckAlert.java

**A99-1 | MEDIUM | FleetCheckAlert.java:31–40 | Commented-out code: `getLindeLogo` method**
A full method body is left commented out. Dead commented-out code makes the class harder to read and maintain; it should be removed from version control or tracked via a branch/ticket.

**A99-2 | MEDIUM | FleetCheckAlert.java:69–79 | Commented-out code: `appendHtmlAlertCotentLinde` method**
Another full method left commented out. Same concern as A99-1.

**A99-3 | MEDIUM | FleetCheckAlert.java:170–225 | Commented-out code: `setLindeContent` method**
A large (55-line) commented-out method block. This is the largest dead code block in the file and significantly obscures the active code.

**A99-4 | HIGH | FleetCheckAlert.java:95 | Unsafe array access before null/empty check**
`arrResult.get(0)` is accessed at line 95 (and again at line 100) before the null/size guard at line 105. If `arrResult` is null or empty the code throws an unchecked `NullPointerException` / `IndexOutOfBoundsException`. The guard `if(arrResult!=null && arrResult.size()>0)` arrives too late, after the data has already been used to build the table header.

**A99-5 | HIGH | FleetCheckAlert.java:151 | Wrong variable used in odometer conditional**
At line 147 the location column is conditionally appended when `!location.equalsIgnoreCase("")`. At line 151 the odometer column guard reads `!location.equalsIgnoreCase("0")` — it tests `location` instead of `odemeter`. This mirrors the header check at line 100 (`arrResult.get(0).getOdemeter()`) but uses the wrong variable in the row loop, meaning the odometer cell is controlled by whether the location string is `"0"` rather than whether the odometer value is `"0"`.

**A99-6 | LOW | FleetCheckAlert.java:58 | Typo in method name: `appendHtmlAlertCotent`**
The word "Content" is spelled "Cotent" throughout the codebase (also in the parent class). This is a pervasive naming convention violation. Tracked once here with a cross-reference to A99-10 and A99-15.

**A99-7 | LOW | FleetCheckAlert.java:60 | Hardcoded localhost URL in production code**
`"http://localhost:8090/"` is embedded in the CSS fetch call inside `appendHtmlAlertCotent`. Same pattern exists in the parent class (`PreFlightReport.appendHtmlCotent`, line 68, and `appendHtmlAlertCotent`, line 79). If the application is deployed to any host other than localhost port 8090 the CSS will fail to load silently.

**A99-8 | LOW | FleetCheckAlert.java:164 | Dual exception logging**
`InfoLogger.logException(log, e)` and `e.printStackTrace()` are both called for the same exception (lines 163–164). `printStackTrace()` writes to stderr without context; the structured logger call is sufficient on its own.

---

### PreFlightReport.java

**A99-9 | LOW | PreFlightReport.java:5 | Unused import: `MessageResources`**
`org.apache.struts.util.MessageResources` is imported but never referenced in the file.

**A99-10 | LOW | PreFlightReport.java:8 | Unused import: `CompanyDAO`**
`com.dao.CompanyDAO` is imported but not used anywhere in `PreFlightReport`.

**A99-11 | LOW | PreFlightReport.java:13 | Unused import: `Util`**
`com.util.Util` is imported but not referenced in `PreFlightReport`.

**A99-12 | LOW | PreFlightReport.java:15 | Unused import: `UnitBean`**
`com.bean.UnitBean` is imported but not referenced in `PreFlightReport`. It was likely used by the commented-out `getUnitNameLinde` method.

**A99-13 | MEDIUM | PreFlightReport.java:26 | Package-private field `pm` should be `protected`**
The field `PropertyMessageResources pm` has no access modifier. All subclasses in the `com.report` package (e.g. `FleetCheckAlert`) access it directly. The intended visibility is `protected` (like the other shared fields); missing the modifier is an unintentional narrowing of access scope.

**A99-14 | MEDIUM | PreFlightReport.java:152–157, 165–170 | Commented-out code: `getDriverNameLinde` and `getUnitNameLinde`**
Two methods are left commented out. Same concern as A99-1/A99-2/A99-3.

**A99-15 | LOW | PreFlightReport.java:25,57,61,65,77 | Pervasive typo: `htmlCotent` / `getHtmlCotent` / `setHtmlCotent` / `appendHtmlCotent`**
The field name and all associated accessor/mutator methods and `append*` methods spell "Content" as "Cotent". This spans both `PreFlightReport` and `FleetCheckAlert` and violates standard Java naming conventions.

**A99-16 | LOW | PreFlightReport.java:44 | Typo in method name: `caculatesDate`**
The method name is spelled `caculatesDate` rather than `calculateSDate` or `calculateStartDate`. Inconsistent with camelCase expectations and the word "calculate" is misspelled.

**A99-17 | LOW | PreFlightReport.java:116,122,128,134 | Non-standard getter/setter names for lowercase-first-letter fields**
`getsEmail` / `setsEmail` and `getrEmail` / `setrEmail` do not follow the JavaBeans convention (should be `getSEmail`/`setSEmail` and `getREmail`/`setREmail`). This may break frameworks (Struts, JSP EL, Jackson) that rely on standard bean introspection.

**A99-18 | LOW | PreFlightReport.java:105–108 | `setContent(String compId)` base implementation is dead code**
The base-class `setContent(String compId)` simply returns 0 and is never called polymorphically from outside. `FleetCheckAlert` overrides a *different* signature (`setContent(int resultId)`), so the base method is effectively unused and misleading as a contract.

**A99-19 | LOW | PreFlightReport.java:161 | Double semicolon (;;) at end of statement**
Line 161: `String unitName = UnitDAO.getInstance().getUnitById(unitId).get(0).getName();;` — a stray extra semicolon. While harmless at runtime this is a minor style error indicating the code was not reviewed carefully.

**A99-20 | LOW | PreFlightReport.java:68,79 | Hardcoded localhost URL**
Same issue as A99-7 — `"http://localhost:8090/"` is hardcoded in both `appendHtmlCotent` (line 68) and `appendHtmlAlertCotent` (line 79). See A99-7 for impact description.

---

### ReportAPI.java

**A99-21 | LOW | ReportAPI.java:6 | Unused import: `RuntimeConf`**
`com.util.RuntimeConf` is imported but not referenced anywhere in `ReportAPI`.

**A99-22 | LOW | ReportAPI.java:7 | Unused import: `Util`**
`com.util.Util` is imported but not referenced anywhere in `ReportAPI`.

**A99-23 | LOW | ReportAPI.java:46 | Typo in parameter name: `dirctory`**
The parameter of `getExportDir` is named `dirctory` instead of `directory`. The parameter is also entirely unused inside the method body (the method ignores it and always returns `java.io.tmpdir`), making it doubly misleading.

**A99-24 | MEDIUM | ReportAPI.java:46–49 | `getExportDir` parameter is unused — dead parameter**
`getExportDir(String dirctory)` accepts a directory path argument but unconditionally returns `System.getProperty("java.io.tmpdir")`, ignoring the argument entirely. The parameter is vestigial and creates a false contract: callers believe they can influence the export directory but cannot.

**A99-25 | LOW | ReportAPI.java:76,84 | Non-standard getter/setter names for lowercase-first-letter fields**
Same naming issue as A99-17 — `getsEmail`/`setsEmail` and `getrEmail`/`setrEmail` do not follow JavaBeans convention. Both `ReportAPI` and `PreFlightReport` repeat this pattern independently, indicating no shared base or interface enforces consistent naming.

**A99-26 | MEDIUM | ReportAPI.java:10–20 | Fields `subject`, `title`, `content`, `sEmail`, `rEmail` are declared but never used within the class**
`ReportAPI` declares and exposes getters/setters for `subject`, `title`, `content`, `sEmail`, `rEmail`, and `fileURL`, but none of these fields are read inside the class itself (only `name`, `input`, and `responseCode` participate in actual logic). The class carries significant dead state. If subclasses are the intended consumers the fields should be documented as such.

---

## Summary Table

| ID | Severity | File | Line(s) | Category |
|----|----------|------|---------|----------|
| A99-1 | MEDIUM | FleetCheckAlert.java | 31–40 | Commented-out code |
| A99-2 | MEDIUM | FleetCheckAlert.java | 69–79 | Commented-out code |
| A99-3 | MEDIUM | FleetCheckAlert.java | 170–225 | Commented-out code |
| A99-4 | HIGH | FleetCheckAlert.java | 95,100 | Unsafe access before null guard |
| A99-5 | HIGH | FleetCheckAlert.java | 151 | Wrong variable in conditional |
| A99-6 | LOW | FleetCheckAlert.java | 58 | Typo in method name |
| A99-7 | LOW | FleetCheckAlert.java | 60 | Hardcoded localhost URL |
| A99-8 | LOW | FleetCheckAlert.java | 163–164 | Dual exception logging |
| A99-9 | LOW | PreFlightReport.java | 5 | Unused import |
| A99-10 | LOW | PreFlightReport.java | 8 | Unused import |
| A99-11 | LOW | PreFlightReport.java | 13 | Unused import |
| A99-12 | LOW | PreFlightReport.java | 15 | Unused import |
| A99-13 | MEDIUM | PreFlightReport.java | 26 | Missing `protected` modifier |
| A99-14 | MEDIUM | PreFlightReport.java | 152–170 | Commented-out code |
| A99-15 | LOW | PreFlightReport.java | 25,57,61,65,77 | Pervasive typo in identifiers |
| A99-16 | LOW | PreFlightReport.java | 141 | Typo in method name |
| A99-17 | LOW | PreFlightReport.java | 116,122,128,134 | Non-standard JavaBeans naming |
| A99-18 | LOW | PreFlightReport.java | 105–108 | Dead base method |
| A99-19 | LOW | PreFlightReport.java | 161 | Double semicolon |
| A99-20 | LOW | PreFlightReport.java | 68,79 | Hardcoded localhost URL |
| A99-21 | LOW | ReportAPI.java | 6 | Unused import |
| A99-22 | LOW | ReportAPI.java | 7 | Unused import |
| A99-23 | LOW | ReportAPI.java | 46 | Typo in parameter name |
| A99-24 | MEDIUM | ReportAPI.java | 46–49 | Unused/misleading parameter |
| A99-25 | LOW | ReportAPI.java | 76,84 | Non-standard JavaBeans naming |
| A99-26 | MEDIUM | ReportAPI.java | 10–20 | Declared fields never used in class |
# Pass 4 Code Quality Audit — Agent C01
**Audit date:** 2026-02-26
**Scope:** Configuration / build / properties files

---

## Reading Evidence

### pom.xml
- groupId: `com.collectiveintelligence`, artifactId: `pandoraAdmin`, version: `1.0.0-SNAPSHOT`, packaging: `war`
- Properties: `slf4j-version=1.6.6`, `poi-version=3.8`, `avalon-version=4.3.1`
- Profiles: `local`, `dev`, `uat` (activeByDefault=true), `prod`
  - dev profile: hardcoded Tomcat URL `http://forklift360.canadaeast.cloudapp.azure.com:8080/manager/text`
  - uat profile: hardcoded Tomcat URL `http://ec2-54-86-82-22.compute-1.amazonaws.com:8080/manager/text`
  - prod profile: `<tomcat.url></tomcat.url>` (empty)
- Plugins: maven-eclipse-plugin 2.9, maven-compiler-plugin 2.5.1 (source/target 1.8), maven-war-plugin 3.2.2, tomcat7-maven-plugin 2.2
- Key dependencies (selected):
  - struts-core/taglib/tiles 1.3.10
  - commons-beanutils 1.9.3 AND commons-beanutils-bean-collections 1.8.3 (mixed versions)
  - commons-fileupload 1.2.1
  - jaxb-api 2.3.0, jaxb-impl 2.1, jaxb-xjc 2.0EA3 (three different JAXB coordinates, mixed versions)
  - log4j 1.2.16
  - jackson-annotations/core/databind 2.10.1
  - spring-web 4.0.2.RELEASE
  - lombok 1.18.0
  - poi (all 4 artifacts) 3.8
  - itextpdf 5.4.2
  - guava 25.1-jre
  - servlet-api 2.5 (provided)
  - tomcat-jasper 8.5.30 (provided)

### settings.xml
- Defines two server entries with plaintext passwords:
  - `TomcatServerUat` — username: `maven`, password: `C!1admin`
  - `TomcatServerAzure` — username: `maven`, password: `pyx1s!96`

### bitbucket-pipelines.yml
- Uses Docker image `maven:3.6.1`
- Single default pipeline step: `mvn -B verify`
- No branch-specific pipelines; no deployment pipeline separation

### environment.dev.properties / environment.uat.properties / environment.prod.properties
- All three files contain exactly one key: `logDir=/var/local/pandora/logs`
- All three values are identical

### log4j.properties
- Root logger: `log4j.rootLogger = INFO, rollingFile` — rolling file appender only (no console)
- `rollingFile`: RollingFileAppender, `${logDir}/info.log`, MaxFileSize=10MB, MaxBackupIndex=10
- `log4j.debug=true` is set (line 39) — enables log4j internal debugging output to stdout
- JDBC loggers configured: `jdbc.audit` INFO, `jdbc.resultset` INFO, `jdbc.sqlonly` DEBUG, `jdbc.sqltiming` DEBUG, `jdbc.connection` FATAL
- sql/sqltiming/jdbc/connection FileAppenders: all with `Append=false` (file truncated on restart)
- sql.log and sqltiming.log: level DEBUG — logs all SQL and timing to disk
- File is structurally split: lines 1-27 are the real configuration block; lines 31-94 begin with `!` (log4j `!` comment style) containing a second configuration block whose property definitions ARE parsed by log4j (they are active, not dead)

### MessageResources.properties (default/base)
- ~518 lines; ~230 keys
- Notable: `gps.unit.title` and `gps.company.title` etc. defined twice (lines 487-493 and 509-516) — duplicate keys
- Notable keys present: `error.duplicateCompEnity`, `error.norole`, `error.date_format`, `error.timezone`, `error.max_session_length`, `error.incorrect.reset`, `error.incorrect.reset.cognito`, `error.cognito`, `button.assign`, `button.save`, `button.print.report`, `button.close`, `button.list`, `button.hide`, `button.show`, `button.convert`, `button.print.barcode`, `button.load.barcode`, `report.location`, `report.odemeter`, `job.*`, `preops.*`, `sessionreport.*`, `settings.timezone`, `comp.title`, `dealer.*`, `driver.ttitle`

### MessageResources_en.properties
- ~412 lines; subset of base keys
- Missing vs base: `error.duplicateCompEnity`, `error.norole`, `error.date_format`, `error.timezone`, `error.max_session_length`, `error.incorrect.reset`, `error.incorrect.reset.cognito`, `error.cognito`, `error.pass` (absent), `button.assign`, `button.save`, `button.send`, `button.print.report`, `button.close`, `button.list`, `button.hide`, `button.show`, `button.convert`, `button.print.barcode`, `button.load.barcode`, `comp.title` (absent), `dealer.*` keys, `driver.ttitle`, `driver.apin`, `driver.acpn`, various `report.*`, `job.*`, `preops.*`, `impact.*`, `sessionreport.*`, `login.forgetpass`, `unit.weightunit`, `unit.pounds.abbr`, `unit.kilograms.abbr`, `manufacturer.name`, `manufacturers.title`

### MessageResources_en_AU.properties
- ~430 lines; closely similar to en_GB
- Missing vs base: same large set as en_GB (see en_GB notes)
- `impact.driver.name` present in base but absent in en_AU
- Duplicate `report.status` key at lines 331 and 336 (same as base and other en variants)

### MessageResources_en_GB.properties
- ~430 lines
- `question.diagnosis` absent (line 294 stops at `question.answerN`)
- Missing vs base: same pattern as en_AU

### MessageResources_en_US.properties
- ~431 lines; adds `error.timezone` (line 82) — the only en_* variant that has it
- `driver.apin` and `driver.acpn` present (unlike en and en_GB/AU)
- `comp.title` present
- Still missing: `error.duplicateCompEnity`, `error.norole`, `error.date_format`, `error.max_session_length`, `error.incorrect.reset`, `error.incorrect.reset.cognito`, `error.cognito`, `button.assign`, `button.save`, `button.print.report`, etc.

### MessageResources_ms.properties (Malay)
- ~381 lines; translated content
- Missing vs base: `report.noDriver`, `footer.privacy`, `footer.term`, `login.forgetpass`, `comp.title`, `user`, `driver.joindate`, `driver.ttitle`, `driver.ltitle`, `driver.lnum`, `driver.lexpiry`, `driver.lsecnum`, `driver.ladd`, `driver.atitle`, `driver.aapp`, `driver.apin`, `driver.acpn`, `unit.currenthour`, `unit.macadd`, `unit.expmod`, `unit.weightunit`, etc.
- `impact.company.title` absent (only `impact.unit.title`, `impact.manufacturer.title` present)
- Several malformed key=value lines: `admin.comment.succuss Komen = ...` (line 334 — missing `=` sign, space in key), `msg.formbuilder Borang = ...` (line 346 — same issue), `Bahasa Soalan = admin.question.language` (line 350 — key/value reversed)
- `admin.upgrade.title` present (not in base)
- GPS keys absent

### MessageResources_tr.properties (Turkish)
- ~384 lines; translated content
- `ERROR.TYPE` (line 71) — key in uppercase, will not match `error.type` lookups (case-sensitive)
- `error.duplicateName` (line 51) — malformed: `error.duplicateName zaten Sisteminizi i\u00e7inde = Ad ...` (value bleeds into key name, missing proper `=` separator)
- `error.duplicateSerial` (line 52) — similar malformed entry
- Missing: `msg.form`, `login.forgetpass`, `comp.title`, `driver.ttitle`, `driver.ltitle`, `driver.lnum`, `driver.lexpiry`, `driver.lsecnum`, `driver.ladd`, `driver.atitle`, `driver.aapp`, `driver.apin`, `driver.acpn`, `unit.currenthour`, `unit.macadd`, `unit.expmod`, `unit.weightunit`, etc.
- `msg.upgrade` and `button.upgrade` and `admin.upgrade.title` present (not in base)
- GPS keys and sessionreport keys absent

### MessageResources_zh_CN.properties (Chinese Simplified)
- ~387 lines; translated content
- Missing vs base: `msg.form` absent (line 39 only has `msg.upgrade` and `msg.form`... actually `msg.form` IS present at line 39)
- Missing: `login.forgetpass`, `comp.title`, `driver.ttitle`, `driver.ltitle/lnum/lexpiry/lsecnum/ladd`, `driver.atitle/aapp/apin/acpn`, `unit.currenthour/macadd/expmod/weightunit`, `sessionreport.*`, various
- `msg.upgrade` and `button.upgrade` and `admin.upgrade.title` present (not in base)
- GPS keys absent from main block (only in mid-file impact block)
- `subscriptionemail` absent

### web.xml
- Servlet version: 2.4 (j2ee schema, very old)
- Custom ActionServlet: `com.actionservlet.PreFlightActionServlet`
- Filters: `CharsetEncodingFilter` on `/*`
- Listeners: CalibrationJobScheduler, DriverAccessRevokeJobScheduler, TrainingExpiryDailyEmailJobSchedueler (typo in class name), TrainingExpiryWeeklyEmailJobScheduler
- Session timeout: 30 minutes
- Error page: only one — catches `java.lang.Exception`, redirects to `/error/error.html`; no HTTP error code pages (404, 500)
- No `<security-constraint>` or `<login-config>` elements
- Taglib declarations present for struts beans/html/logic/nested/tiles

### struts-config.xml
- DTD: Struts 1.3
- 41 form-beans; 3 global exceptions (SQLException, IOException, ServletException)
- ~55 action mappings
- Notable: `/swithLanguage` (typo: missing 'c' — should be `/switchLanguage`)
- `adminRegActionForm` (line 24 in form-beans) maps to `com.actionform.AdminRegisterActionForm` — same class as `adminRegisterActionForm` (line 11); duplicate form-bean registrations for same class
- `/admindriverlicencevalidateexist` action at line 324-331 has no forwards defined — empty action
- `/calibration` action at line 582-583 has no forwards defined — empty action
- `preOpsReportSearchForm` at line 520: missing `scope` and `validate` attributes (unlike similar report actions)
- Message resources: `properties.MessageResources` (correct path for classpath resolution)

### tiles-defs.xml
- DTD: Tiles 1.3
- ~50 definitions; mostly extending `adminDefinition` or `loginDefinition`
- `adminHomeDefinition` referenced in struts-config.xml forwards (`admindashboard`) but not defined in tiles-defs.xml
- `adminCompDefinition` referenced in struts-config.xml (`admincomp` forward) but not defined in tiles-defs.xml

### validation.xml
- Validates: `loginActionForm`, `adminRegisterActionForm`, `AdminDriverEditForm`
- `AdminDriverEditForm` (line 60) uses form name with capital 'A' and 'D' — Struts form names are case-sensitive; actual form-bean is `adminDriverEditForm` (lowercase) — mismatch will silently skip validation
- Password minimum length: 4 characters — very weak

### validator-rules.xml
- Standard Struts 1.3 validator rules file (unmodified from framework default)
- CVS header still present ($Header, $Revision, $Date)

---

## Findings

### CRITICAL

**C01-1 | CRITICAL | settings.xml:9 | Plaintext server passwords committed to version control**
`settings.xml` contains plaintext passwords for two Tomcat deployment servers directly in the repository:
- `TomcatServerUat` password: `C!1admin`
- `TomcatServerAzure` password: `pyx1s!96`
These credentials should be stored in a user-local `~/.m2/settings.xml` and never committed to the repository. Anyone with read access to the repository has these credentials.

**C01-2 | CRITICAL | pom.xml:10 | SNAPSHOT version used for production artifact**
The project version is `1.0.0-SNAPSHOT`. SNAPSHOT versions are non-reproducible — Maven may pull different code on successive builds. Production deployments should use a fixed release version. The UAT profile is `activeByDefault=true`, so every unqualified build deploys a SNAPSHOT to UAT.

---

### HIGH

**C01-3 | HIGH | pom.xml:186-189 | commons-fileupload 1.2.1 is critically outdated with known CVEs**
`commons-fileupload:1.2.1` was released circa 2008 and has multiple critical vulnerabilities including CVE-2014-0050 (DoS via crafted Content-Type header) and CVE-2016-3092 (DoS). The current release is 1.5+. This library handles multipart file uploads in the application.

**C01-4 | HIGH | pom.xml:203 | itextpdf 5.4.2 is outdated with known security vulnerabilities**
`itextpdf:5.4.2` (circa 2012) has known vulnerabilities and is well behind current releases. iText 5.x itself reached end-of-life and has unpatched CVEs. PDF generation code should be updated.

**C01-5 | HIGH | pom.xml:293-296 | log4j 1.2.16 is end-of-life with known security issues**
`log4j:1.2.16` is the legacy Log4j 1.x branch which reached end-of-life in August 2015 and has known vulnerabilities (CVE-2019-17571 — SocketServer deserialization RCE, CVE-2022-23302/23303/23305). No security patches will be issued. Migration to Log4j 2.x or Logback is required.

**C01-6 | HIGH | src/main/resources/properties/log4j.properties:39 | log4j internal debug mode enabled in all environments**
`log4j.debug=true` causes Log4j to print its internal initialisation and routing details to stdout/stderr on every application start. This is a developer diagnostic setting and should not be present in any deployed environment. It leaks configuration information.

**C01-7 | HIGH | src/main/resources/properties/MessageResources_ms.properties:334,346,350 | Malformed property key=value lines — values will silently load as wrong keys or be ignored**
Three lines in the Malay resource file have broken syntax:
- Line 334: `admin.comment.succuss Komen = telah dihantar...` — space in the key; Java Properties will parse `admin.comment.succuss` as key = `Komen = telah dihantar...` (rest as value), discarding the intended key.
- Line 346: `msg.formbuilder Borang = telah berjaya dicipta` — same issue.
- Line 350: `Bahasa Soalan = admin.question.language` — key and value are reversed; the key `Bahasa Soalan` (with space) is unresolvable and the real key `admin.question.language` will fall through to the default bundle.
These errors mean Malay-locale users will see missing or incorrect UI strings.

**C01-8 | HIGH | src/main/resources/properties/MessageResources_tr.properties:71 | Turkish `ERROR.TYPE` key is uppercase — will never match**
The key `ERROR.TYPE` at line 71 is fully uppercase. Java Properties keys are case-sensitive. Struts will look up `error.type` (all lowercase). This entry will never be matched, so Turkish users see the fallback English message or a missing-key placeholder for the vehicle type validation error.

**C01-9 | HIGH | src/main/webapp/WEB-INF/validation.xml:60 | Form name case mismatch — `AdminDriverEditForm` will never be validated**
`validation.xml` declares a form named `AdminDriverEditForm` (mixed case), but the struts-config.xml form-bean is declared as `adminDriverEditForm` (lowercase `a` and `d`). Struts validator form name matching is case-sensitive. As a result, the `first_name` and `last_name` required-field validations on driver add/edit are silently skipped, allowing empty driver names through to the server.

---

### MEDIUM

**C01-10 | MEDIUM | pom.xml:176-179 | Mismatched commons-beanutils versions (1.9.3 vs 1.8.3)**
`commons-beanutils:1.9.3` and `commons-beanutils-bean-collections:1.8.3` are declared together. The `bean-collections` artifact was merged into the main `commons-beanutils` jar from 1.9.x onward. Having both at different versions risks classpath conflicts and the older artifact may shadow or conflict with the newer one.

**C01-11 | MEDIUM | pom.xml:257-269 | Three different JAXB dependencies at three different versions**
- `jaxb-api:2.3.0` (javax.xml.bind)
- `jaxb-impl:2.1` (javax.xml — non-standard groupId)
- `jaxb-xjc:2.0EA3` (javax.xml — early-access pre-release)
These are from different groupIds and span a wide version range (2.0EA3 through 2.3.0). `jaxb-xjc:2.0EA3` is a pre-release artifact from ~2006. The non-standard `javax.xml` groupId for impl/xjc artifacts is incorrect; the canonical groupIds are `com.sun.xml.bind`. This configuration is likely to cause runtime JAXB version conflicts.

**C01-12 | MEDIUM | pom.xml:87-90 | maven-compiler-plugin 2.5.1 is very outdated**
Version 2.5.1 was released in 2012. The current release is 3.x. Version 2.5.1 may produce deprecation warnings and lacks support for newer javac options. The `<compilerArgument>-Xlint:all</compilerArgument>` combined with `<showWarnings>false</showWarnings>` is self-contradictory — all lint warnings are requested but display is suppressed.

**C01-13 | MEDIUM | pom.xml:72-85 | maven-eclipse-plugin is deprecated and should not be in production builds**
`maven-eclipse-plugin:2.9` is retired/deprecated (Apache retired it). It serves no purpose in a CI build and adds unnecessary overhead. It should be removed or moved to a developer-only profile.

**C01-14 | MEDIUM | pom.xml:44-48 | UAT profile is activeByDefault=true — unintended deployments possible**
The `uat` profile is `activeByDefault=true`. Any invocation of `mvn` without an explicit `-P` flag will activate the UAT profile, meaning `mvn package` or `mvn install` will attempt to deploy to the UAT Tomcat server. This increases the risk of accidental UAT deployments from developer machines.

**C01-15 | MEDIUM | src/main/resources/properties/log4j.properties:71,76,85,92 | JDBC log appenders use Append=false — log data is destroyed on each restart**
The `sql`, `sqltiming`, `jdbc`, and `connection` FileAppenders are all configured with `Append=false`. This means every application restart truncates all four log files, destroying historical SQL/JDBC log data. For debugging purposes this is almost certainly unintentional.

**C01-16 | MEDIUM | src/main/resources/properties/log4j.properties:56,60 | SQL and timing loggers at DEBUG level in all environments**
`jdbc.sqlonly` and `jdbc.sqltiming` are configured at DEBUG level. Every SQL statement and its timing is written to disk in all environments including production. This generates significant I/O, may log sensitive query parameters, and has a performance impact.

**C01-17 | MEDIUM | src/main/webapp/WEB-INF/web.xml:3-6 | Servlet spec version 2.4 is severely outdated**
`web.xml` declares `version="2.4"` using the `java.sun.com/xml/ns/j2ee` namespace (J2EE 1.4, released 2003). The application is deployed on Tomcat 8.5 (servlet 3.1). Staying at 2.4 prevents use of annotations-based configuration, async servlets, and other modern features, and causes deprecation warnings during deployment.

**C01-18 | MEDIUM | src/main/webapp/WEB-INF/web.xml:51-54 | No HTTP error code pages configured**
Only a Java exception error page is defined (`java.lang.Exception` → `/error/error.html`). There are no `<error-page>` entries for HTTP status codes 404 (Not Found) or 500 (Internal Server Error). Unhandled HTTP errors will expose the default Tomcat error page, which may reveal server version and stack trace information.

**C01-19 | MEDIUM | src/main/webapp/WEB-INF/struts-config.xml:62 | Typo in action path: `/swithLanguage` (missing 'c')**
The action path is `/swithLanguage` instead of `/switchLanguage`. Any JSP or link that correctly spells `/switchLanguage.do` will receive a 404. The corresponding `/goSerach` action (line 179) also contains a typo (`Serach` vs `Search`), though it is consistently spelled in the config.

**C01-20 | MEDIUM | src/main/webapp/WEB-INF/struts-config.xml:24 | Duplicate form-bean registration for AdminRegisterActionForm**
`adminRegisterActionForm` (line 11) and `adminRegActionForm` (line 24) both point to `com.actionform.AdminRegisterActionForm`. Having two form-bean names for the same class is confusing and indicates one entry is redundant. The `/adminRegister` action uses `adminRegActionForm`, while the validation.xml validates `adminRegisterActionForm` — these are different names, so validation may not apply to the actual action.

**C01-21 | MEDIUM | src/main/webapp/WEB-INF/tiles-defs.xml | Referenced tile definitions missing: `adminHomeDefinition`, `adminCompDefinition`**
struts-config.xml references the tile `adminHomeDefinition` (forward `admindashboard` in `/adminmenu`) and `adminCompDefinition` (forward `admincomp` in `/adminmenu`) but neither definition exists in tiles-defs.xml. Navigating to these forwards at runtime will throw a Tiles `DefinitionsFactoryException` or equivalent error.

**C01-22 | MEDIUM | src/main/resources/properties/MessageResources.properties:487-493,509-516 | Duplicate GPS keys in default bundle**
Keys `gps.unit.title`, `gps.company.title`, `gps.manufacturer.title`, `gps.driver.name`, `gps.datetime.title`, `gps.level.title`, `gps.report.header` are defined twice in `MessageResources.properties` (first at lines ~487-493, then again at lines ~509-516). Java Properties silently takes the last value. The duplication indicates copy-paste error.

**C01-23 | MEDIUM | src/main/webapp/WEB-INF/validation.xml:55-57 | Company registration password minimum length is only 4 characters**
The `adminRegisterActionForm` validation sets `minlength=4` for the `password` field. A 4-character minimum is insufficient for any security requirement. The admin access password and driver access password are the primary credentials protecting company data.

---

### LOW

**C01-24 | LOW | pom.xml:34,45 | Internal server hostnames/IPs embedded in pom.xml**
The dev and UAT Tomcat URLs are hardcoded in pom.xml: `http://forklift360.canadaeast.cloudapp.azure.com:8080/...` and `http://ec2-54-86-82-22.compute-1.amazonaws.com:8080/...`. While not passwords, these expose internal infrastructure topology in the repository. They should be externalised to the settings.xml server configuration or CI environment variables.

**C01-25 | LOW | pom.xml:56 | prod profile has empty `<tomcat.url>`**
The `prod` profile declares `<tomcat.url></tomcat.url>` with no value. If the prod profile is activated, the Tomcat plugin will fail with a configuration error rather than refusing to deploy. This should either be removed or documented.

**C01-26 | LOW | bitbucket-pipelines.yml:6 | Pipeline uses unpinned Maven image tag `maven:3.6.1`**
The pipeline image `maven:3.6.1` is a floating tag that may change if rebuilt. For reproducible CI builds, a digest-pinned image should be used (e.g. `maven:3.6.1@sha256:...`). Additionally, there are no branch-specific pipelines — every branch runs the same `mvn -B verify` without any deployment gating.

**C01-27 | LOW | src/main/resources/properties/log4j.properties:1-94 | File has two overlapping configuration blocks separated by comment-style `!` lines**
Lines 1-27 define the real appender configuration. Lines 31-94 begin with `!` delimiters but contain active `log4j.*` property definitions that ARE parsed (log4j properties files treat `!` as a line comment in the same way as `#`). The active JDBC logger definitions (lines 48-65) and their appenders (lines 69-94) in the second block do take effect. This dual-block structure makes the file confusing and difficult to maintain.

**C01-28 | LOW | src/main/resources/properties/MessageResources_tr.properties:51-52 | Malformed key=value entries in Turkish bundle**
Lines 51-52 contain property definitions where text has been inserted between the key name and the `=` separator:
- Line 51: `error.duplicateName zaten Sisteminizi i\u00e7inde = Ad ba\u015fka bir deneyin.`
Java Properties parser will interpret `error.duplicateName zaten Sisteminizi i\u00e7inde` as the full key (including spaces), meaning `error.duplicateName` will not be found. Turkish users will see the default-locale message for duplicate name errors.

**C01-29 | LOW | src/main/resources/properties/MessageResources.properties | Duplicate `report.status` key**
`report.status` is defined twice in the base bundle (lines 371 and 376) and identically duplicated in en, en_AU, en_GB, en_US bundles. The second definition silently overrides the first. This is a copy-paste artefact from the `report.expired` / `report.expiring` block.

**C01-30 | LOW | src/main/webapp/WEB-INF/web.xml:40 | Listener class name contains typo: `TrainingExpiryDailyEmailJobSchedueler`**
The class name `com.quartz.TrainingExpiryDailyEmailJobSchedueler` has a misspelling (`Schedueler` instead of `Scheduler`). If the actual class file has the same spelling the application will work, but the inconsistency suggests the class name itself is misspelled, which is a maintainability concern.

**C01-31 | LOW | src/main/webapp/WEB-INF/struts-config.xml:324-331 | `/admindriverlicencevalidateexist` action has no forwards**
This action mapping has no `<forward>` children. If the action returns a non-null forward name, Struts will throw an exception. This may be intentional (AJAX endpoint that writes directly to response), but the absence of any explicit annotation or comment makes it unclear.

**C01-32 | LOW | src/main/webapp/WEB-INF/validator-rules.xml:6-8 | CVS header artefacts remain in validator-rules.xml**
Lines 6-8 contain CVS `$Header`, `$Revision`, `$Date` expansion markers from the original Apache Struts source file. These are cosmetic remnants but indicate the file was copied verbatim from the framework distribution without cleanup.

---

### INFO

**C01-33 | INFO | pom.xml:13 | SLF4J version 1.6.6 is outdated**
SLF4J `1.6.6` was released in 2012; the current stable is 2.x. While not a critical security issue, updating would align the logging facade with modern practices.

**C01-34 | INFO | pom.xml:14 | Apache POI version 3.8 is outdated**
`poi-version=3.8` dates from 2012. Current release is 5.x. Older POI versions have known security issues with maliciously crafted Office files.

**C01-35 | INFO | environment.dev.properties / environment.uat.properties / environment.prod.properties | All three environment files are identical**
All three files contain only `logDir=/var/local/pandora/logs` with the same value. There is no environment-specific differentiation. Either the property filtering mechanism is not being fully used, or additional environment-specific properties (DB URLs, API endpoints, feature flags) are being managed elsewhere and are not visible in this repository.

**C01-36 | INFO | src/main/resources/properties/MessageResources_ms.properties | Malay bundle missing GPS report keys**
The Malay bundle does not contain any `gps.*` keys (gps.unit.title, gps.company.title, etc.). Malay-locale users accessing GPS report pages will see the fallback default-bundle (English) values. The same applies to `sessionreport.*` keys.

**C01-37 | INFO | src/main/resources/properties/MessageResources_tr.properties | Turkish bundle missing GPS and sessionreport keys**
Same as above for Turkish locale.

**C01-38 | INFO | src/main/resources/properties/MessageResources_zh_CN.properties | Chinese bundle missing GPS and sessionreport keys**
Same as above for Chinese (Simplified) locale.

**C01-39 | INFO | src/main/webapp/WEB-INF/struts-config.xml | `/calibration` action has no forwards**
`<action path="/calibration" type="com.action.CalibrationAction">` (lines 582-583) has no forwards. Same note as C01-31 — may be intentional for an internal scheduler callback, but undocumented.

**C01-40 | INFO | src/main/webapp/WEB-INF/validation.xml | Very few forms have client-side validation defined**
Only `loginActionForm`, `adminRegisterActionForm`, and `AdminDriverEditForm` (broken — see C01-9) have validation rules. The majority of the ~41 form-beans have no validation.xml rules, relying entirely on manual validation in Action classes.
