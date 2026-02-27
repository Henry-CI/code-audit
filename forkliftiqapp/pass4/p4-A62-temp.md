# Pass 4 Code Quality — Agent A62
**Audit run:** 2026-02-26-01
**Auditor:** A62
**Files reviewed:**
1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/EquipmentListFragment.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/EquipmentPrestartFragment.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/IncidentFragment.java`

---

## Section 1: Reading Evidence

### File 1: EquipmentListFragment.java

**Class:** `EquipmentListFragment`
Extends: `FleetFragment`
Implements: `AbsRecyclerAdapter.OnItemClickListener`, `EquipmentSelectForkPresenter.ShowResultCallBack`

**Fields (with visibility):**
- `private SelectForkAdapter myAdapter` (line 43)
- `private EquipmentSelectForkPresenter presenter` (line 44)
- `public List<String> urlList = new ArrayList<>()` (line 45)
- `public static GetEquipmentResultArray getEquipmentResultArray` (line 46)
- `static boolean equipmentChanged` (line 47)
- `static int equipmentSelected` (line 48)
- `EquipmentActivity activity` (line 49 — package-private)

**Methods (exhaustive):**
| Method | Line | Visibility |
|---|---|---|
| `onCreateView(LayoutInflater, ViewGroup, Bundle)` | 53 | public (override) |
| `onDestroy()` | 59 | public (override) |
| `initViews()` | 64 | public |
| `setRecyclerViewdata(List<EquipmentItem>)` | 94 | private |
| `onItemClick(View, int)` | 103 | public (override) |
| `selectEquipment(int)` | 108 | public |
| `getTrainingExpiryDate(List<TrainingItem>, int)` | 159 | private |
| `goToCurrentEquipmentNext(int)` | 175 | private |
| `showNext()` | 184 | private |
| `uiUpdateEquipmentList(GetEquipmentResultArray)` | 191 | public (override) |
| `onRightButton(View)` | 206 | public (override) |
| `onMiddleButton(View)` | 216 | public (override) |

**Types/constants/enums defined:** None in this file.
**Static import:** `EquipmentActivity.LOCATION_SETTINGS_REQUEST_GPS` (line 40)

---

### File 2: EquipmentPrestartFragment.java

**Class:** `EquipmentPrestartFragment`
Extends: `FleetFragment`
Implements: `AbsRecyclerAdapter.OnItemClickListener`

**Fields:**
- `private static String TAG = EquipmentPrestartFragment.class.getSimpleName()` (line 35)
- `private PrestartCheckListAdapter myAdapter` (line 36)
- `public ArrayList<PreStartQuestionItem> qustionItemArrayList = new ArrayList<>()` (line 38)
- `private PreStartCheckListPresenter presenter` (line 39)
- `private String myCommentStr = ""` (line 41)

**Methods (exhaustive):**
| Method | Line | Visibility |
|---|---|---|
| `onCreateView(LayoutInflater, ViewGroup, Bundle)` | 45 | public (override) |
| `setRecyclerViewdata(PreStartQuestionResultArray)` | 50 | public |
| `initViews()` | 60 | public |
| `setDriverInfoHeader()` | 107 | private |
| `showNext()` | 120 | public |
| `onLeftButton(View)` | 125 | public (override) |
| `onMiddleButton(View)` | 135 | public (override) |
| `onRightButton(View)` | 143 | public (override) |
| `onHiddenChanged(boolean)` | 150 | public (override) |
| `onItemClick(View, int)` | 155 | public (override) |

**Types/constants/enums defined:** None.

---

### File 3: IncidentFragment.java

**Class:** `IncidentFragment`
Extends: `FleetFragment`
Implements: (none additional)

**Fields:**
- `private ToggleImageButton incident_checkbox` (line 40)
- `private ToggleImageButton near_miss_checkbox` (line 41)
- `private TextView incident_date` (line 42)
- `private TextView incident_time` (line 43)
- `private EditText description` (line 44)
- `private IncidentActivity incidentActivity` (line 45)
- `private TextView equipment_name` (line 46)
- `private Calendar incidentCal` (line 48)
- `private CompanyDateFormatter companyDateFormatter` (line 49)
- `private ServerDateFormatter serverDateFormatter` (line 50)
- `private Boolean dateSet` (line 51)
- `private Boolean timeSet` (line 52)
- `private EquipmentItem equipmentItem` (line 54)
- `private ArrayList<EquipmentItem> equipmentList = new ArrayList<>()` (line 55)

**Methods (exhaustive):**
| Method | Line | Visibility |
|---|---|---|
| `showEquipmentName()` | 57 | private |
| `showEquipmentNameList()` | 62 | private |
| `loadEquipment(Runnable)` | 93 | private |
| `onCreateView(LayoutInflater, ViewGroup, Bundle)` | 128 | public (override) |
| `initViews()` | 134 | public |
| `initValue()` | 197 | private |
| `showTimePicker()` | 212 | private |
| `showDatePicker()` | 230 | private |
| `updateTime()` | 246 | private |
| `updateDate()` | 250 | private |
| `onRightButton(View)` | 255 | public (override) |

**Types/constants/enums defined:** None.

---

## Section 2 & 3: Findings

---

### A62-1 — HIGH: `equipmentSelected` is an unused dead field (static)

**File:** `EquipmentListFragment.java`, line 48
**Category:** Dead code

`static int equipmentSelected` is declared at class level and is never read or written anywhere in the codebase (confirmed by full project grep). Because it is package-private static, it is technically accessible from sibling classes, but no class references it. Dead static state in a UI class carries memory and confusion risk that grows across the Activity lifecycle.

```java
// Line 47-48
static boolean equipmentChanged;
static int equipmentSelected;   // never referenced anywhere
```

---

### A62-2 — HIGH: `public static GetEquipmentResultArray getEquipmentResultArray` — static mutable state on a Fragment

**File:** `EquipmentListFragment.java`, line 46
**Category:** Leaky abstraction / design defect

A `public static` mutable field on a Fragment is a serious design problem. External code (`EquipmentDriverAccessPresenter`, `AddEquipmentFragment`) accesses `EquipmentListFragment.getEquipmentResultArray` directly as a global variable. Fragment instances are created and destroyed by the Android back-stack; tying shared state to a specific Fragment's static field creates dangling reference risks, is not thread-safe, and breaks the intended MVP/presenter layering. The data should live in a ViewModel, shared presenter, or repository.

```java
public static GetEquipmentResultArray getEquipmentResultArray;  // line 46
```

External references found:
- `EquipmentDriverAccessPresenter.java:121` — reads `EquipmentListFragment.getEquipmentResultArray`
- `EquipmentDriverAccessPresenter.java:125` — iterates `EquipmentListFragment.getEquipmentResultArray.arrayList`

---

### A62-3 — HIGH: `public List<String> urlList` — public mutable field on Fragment (leaky abstraction)

**File:** `EquipmentListFragment.java`, line 45
**Category:** Leaky abstraction

`urlList` is a `public` instance field on the Fragment. It is read by `SelectForkAdapter` via `presenter.ui.urlList`, meaning the adapter couples directly to the Fragment's internal list field. This bypasses encapsulation entirely. The field is never populated within `EquipmentListFragment.java` itself (it remains an empty `ArrayList`), raising the additional possibility it is a vestigial structure left over from a refactoring.

```java
public List<String> urlList = new ArrayList<>();  // line 45, never populated in this file
```

---

### A62-4 — MEDIUM: Unused import `android.provider.Settings`

**File:** `EquipmentListFragment.java`, line 5
**Category:** Dead code / build warning

`android.provider.Settings` is imported but never referenced within the file. The static import of `LOCATION_SETTINGS_REQUEST_GPS` (line 40) references `EquipmentActivity`, not `Settings` directly, so this import is wholly unused and will generate an IDE/lint unused-import warning.

```java
import android.provider.Settings;  // line 5 — unused
```

---

### A62-5 — MEDIUM: Unused import `android.content.Intent` in EquipmentPrestartFragment

**File:** `EquipmentPrestartFragment.java`, line 3
**Category:** Dead code / build warning

`android.content.Intent` is imported but is never used within the file. The only external activity launch in the fragment (`onRightButton`, line 144) does instantiate an `Intent`, so the import is needed — however closer inspection shows the `Intent` is used (line 144). Re-check: line 144 — `Intent intent = new Intent(getContext(), WebActivity.class)` — the import IS used. Disregard this finding; the import is valid.

*(Self-correction: A62-5 withdrawn — `Intent` is used on line 144.)*

---

### A62-5 — MEDIUM: Unused import `android.support.v4.app.Fragment` in EquipmentPrestartFragment

**File:** `EquipmentPrestartFragment.java`, line 7
**Category:** Dead code / build warning

`android.support.v4.app.Fragment` is imported at line 7. Within the file, a local variable named `fragment` is declared at line 69 but its type is inferred by the RHS `new UniversityGuideFragment()`. The variable is declared as `Fragment fragment = new UniversityGuideFragment()`, so this import IS used as the declared type. Import is valid.

*(Self-correction: A62-5 withdrawn again — `Fragment` is used on line 69.)*

---

### A62-5 — MEDIUM: `static boolean equipmentChanged` — package-private static flag couples sibling Fragments

**File:** `EquipmentListFragment.java`, line 47
**Category:** Leaky abstraction / style

`equipmentChanged` is package-private static state used as an inter-Fragment signal flag: `AddEquipmentFragment` imports it via a static import (`import static au.com.collectiveintelligence.fleetiq360.ui.fragment.EquipmentListFragment.equipmentChanged`) and sets it to `true` (AddEquipmentFragment.java:446). The receiving Fragment reacts to it in `uiUpdateEquipmentList` (line 192-194). This is a fragile communication pattern. Fragment-to-Fragment communication should use a shared ViewModel, the host Activity, or an event bus. The static flag can also be read before the Fragment is ready if the Fragment is reconstructed.

---

### A62-6 — MEDIUM: `TAG` field is non-final — should be `private static final String TAG`

**File:** `EquipmentPrestartFragment.java`, line 35
**Category:** Style inconsistency / build warning

The `TAG` field is declared as `private static String TAG` (mutable), not `private static final String TAG` (standard Android idiom). Every other TAG field examined across the project uses `final`. Android Lint will flag this.

```java
private static String TAG = EquipmentPrestartFragment.class.getSimpleName();  // missing final
```

---

### A62-7 — MEDIUM: Hardcoded log tag `"Info_header"` instead of using the class `TAG` constant

**File:** `EquipmentPrestartFragment.java`, line 109
**Category:** Style inconsistency

`setDriverInfoHeader()` uses a hardcoded string literal `"Info_header"` as the log tag rather than the `TAG` constant declared on line 35. This is inconsistent with `onItemClick()` on line 156 which correctly uses `TAG`. Hardcoded tags make log filtering unreliable.

```java
Log.d("Info_header", "Timezone " + ...);  // line 109 — should be Log.d(TAG, ...)
```

---

### A62-8 — MEDIUM: Production debug logging left in `setDriverInfoHeader()` and `onItemClick()`

**File:** `EquipmentPrestartFragment.java`, lines 109 and 156
**Category:** Dead code / build warning (production log leakage)

Two `Log` statements remain active in production code:

1. Line 109: `Log.d("Info_header", "Timezone " + tz.getDisplayName(...) + " Timezone id :: " + tz.getID())` — diagnostic timezone dump, called every time the prestart screen is shown.
2. Line 156: `Log.e(TAG, "onItemClick() returned: index：" + position)` — uses `Log.e` (error level) for a routine click event, which is semantically wrong. Error-level logging should be reserved for error conditions.

The second log also contains a Unicode fullwidth colon (`：`, U+FF1A) in the message string, indicating it was likely copy-pasted from a Chinese-locale development environment, which may cause log parsing inconsistencies.

```java
Log.d("Info_header", "Timezone "+ tz.getDisplayName(false, TimeZone.SHORT)+" Timezone id :: " +tz.getID()); // line 109
Log.e(TAG, "onItemClick() returned: index：" + position);  // line 156
```

---

### A62-9 — MEDIUM: Region-specific business logic gated on timezone string matching `"America"`

**File:** `EquipmentPrestartFragment.java`, lines 111-114
**Category:** Leaky abstraction / hardcoded locale logic

The visibility of the `training` UI element is conditionally shown only if the device's timezone ID contains the string `"America"`. This is region-detection via timezone ID string matching, which is fragile (e.g., it misses `US/Eastern`, `Canada/Eastern`, `America/Indiana/*`-style IDs that may or may not trigger this, and could false-positive for any future American-region install). Region-specific feature flags should come from the server or a proper configuration source, not from inspecting the local device timezone.

```java
if (tz.getID().contains("America"))   // line 111
    mRootView.findViewById(R.id.training).setVisibility(...trained ? View.INVISIBLE : View.VISIBLE);
else
    mRootView.findViewById(R.id.training).setVisibility(View.INVISIBLE);
```

---

### A62-10 — MEDIUM: `onHiddenChanged(boolean)` overrides with no body — empty override

**File:** `EquipmentPrestartFragment.java`, lines 150-152
**Category:** Dead code

`onHiddenChanged` is overridden and immediately calls `super.onHiddenChanged(hidden)` with no other logic. The parent class `FleetFragment` does not override `onHiddenChanged` (confirmed by grep), so this is a no-op override of the `Fragment` base class. It adds noise and suggests an intent that was never implemented.

```java
@Override
public void onHiddenChanged(boolean hidden) {
    super.onHiddenChanged(hidden);   // lines 150-152 — pure no-op
}
```

---

### A62-11 — MEDIUM: `@SuppressLint("ClickableViewAccessibility")` without documented justification

**File:** `IncidentFragment.java`, line 133
**Category:** Build warning suppression

`@SuppressLint("ClickableViewAccessibility")` suppresses the accessibility lint warning for the `description` field's `OnTouchListener` (lines 171-178). The touch listener sets `focusable` flags but does not implement `performClick()`. This is a genuine accessibility defect (keyboard/accessibility users cannot interact with the field). Suppressing lint without a documented rationale hides the issue rather than resolving it.

```java
@SuppressLint("ClickableViewAccessibility")   // line 133 — suppresses real accessibility problem
public void initViews() {
    ...
    description.setOnTouchListener(new View.OnTouchListener() {
        @Override
        public boolean onTouch(View v, MotionEvent event) {
            v.setFocusable(true);
            v.setFocusableInTouchMode(true);
            return false;   // performClick() never called
        }
    });
```

---

### A62-12 — MEDIUM: `initViews()` sets `incident_checkbox` and `near_miss_checkbox` twice

**File:** `IncidentFragment.java`, lines 163-165 and 198-199
**Category:** Style inconsistency / redundant code

`incident_checkbox.setChecked(...)` and `near_miss_checkbox.setChecked(...)` are called in `initViews()` (lines 163-165), and then called again immediately in `initValue()` (lines 198-199), which is called at the end of `initViews()` (line 194). The first pair of calls is redundant and can lead to confusion about which call "wins."

```java
// initViews(), lines 163-165
incident_checkbox.setChecked(incidentActivity.impactParameter.incident);
near_miss_checkbox.setChecked(incidentActivity.impactParameter.near_miss);
...
initValue();   // line 194

// initValue(), lines 198-199
incident_checkbox.setChecked(incidentActivity.impactParameter.incident);
near_miss_checkbox.setChecked(incidentActivity.impactParameter.near_miss);
```

---

### A62-13 — MEDIUM: `Boolean` (boxed) used instead of primitive `boolean` for `dateSet` and `timeSet`

**File:** `IncidentFragment.java`, lines 51-52
**Category:** Style inconsistency / potential NullPointerException

`dateSet` and `timeSet` are declared as `Boolean` (boxed object type) rather than the primitive `boolean`. They are initialized to `false` in both branches of the `if` on lines 147-152, so they are not actually nullable by design. However, because the type is `Boolean`, unboxing during comparisons (e.g., `if (!dateSet)` on line 261) will throw a `NullPointerException` if the field is ever `null` — for example, if `initViews()` is called without hitting either branch of the null-check guard. There is no corresponding `@Nullable` annotation to communicate the intent.

```java
private Boolean dateSet;   // line 51 — should be primitive boolean
private Boolean timeSet;   // line 52 — should be primitive boolean
```

---

### A62-14 — LOW: `onItemClick(View, int)` body is indented inside an extra blank block in `EquipmentListFragment`

**File:** `EquipmentListFragment.java`, lines 103-106
**Category:** Style inconsistency

The body of `onItemClick` has an extraneous level of indentation inside the method body, making it appear as though there is a nested block where none exists.

```java
@Override
public void onItemClick(View v, final int position) {
                                                       // blank line with extra indent
        selectEquipment(position);
}
```

---

### A62-15 — LOW: Inconsistent brace style for `selectEquipment` and `getTrainingExpiryDate`

**File:** `EquipmentListFragment.java`, lines 108-109, 164-165
**Category:** Style inconsistency

The opening brace for `selectEquipment` (line 109) and the `for`-loop body (lines 164-168) appear on a new line (Allman style), while all other methods in the same class use K&R style (brace on same line). This inconsistency is specific to these two methods and is not present in `EquipmentPrestartFragment` or `IncidentFragment`.

```java
public void selectEquipment(final int position)
{                                                  // Allman — inconsistent with rest of class
    ...
    for (int i = 0; i < training.size() ; i++)
    {                                              // Allman
```

---

### A62-16 — LOW: Hardcoded user-facing error strings in `EquipmentListFragment` instead of string resources

**File:** `EquipmentListFragment.java`, lines 133 and 143
**Category:** Style inconsistency

The training expiry error messages are hardcoded English strings concatenated at runtime, while other user-facing strings in the same class correctly use `getString(R.string.error)` and `getString(R.string.warning)` for their titles. The body messages are not externalised to `strings.xml`, making them untranslatable.

```java
String message = driverName + ", your driver's licence/training is expired. ...";  // line 133
String message = driverName + " your driver's licence/training  will expire in " + diffInDays + " days. ...";  // line 143
```

Note also: line 143 contains a double space between "training" and "will" (`training  will`), indicating a typographic error in the hardcoded string.

---

### A62-17 — LOW: `qustionItemArrayList` — misspelled public field name

**File:** `EquipmentPrestartFragment.java`, line 38
**Category:** Style inconsistency

The field is named `qustionItemArrayList` (missing the 'e' in "question"). Because it is `public` and directly accessed by `PrestartCheckListAdapter` (line 35 of that file), renaming it requires a coordinated change across two classes. The misspelling has propagated into the adapter's source.

```java
public ArrayList<PreStartQuestionItem> qustionItemArrayList = new ArrayList<>();  // line 38
```

---

### A62-18 — LOW: `getTrainingExpiryDate` creates a new `ServerDateFormatter` on every invocation

**File:** `EquipmentListFragment.java`, line 160
**Category:** Style inconsistency / minor inefficiency

`ServerDateFormatter` (a date-parsing utility) is instantiated inside `getTrainingExpiryDate` on every call. `IncidentFragment` correctly keeps `serverDateFormatter` and `companyDateFormatter` as instance fields (lines 49-50). The same pattern should be used in `EquipmentListFragment` for consistency and to avoid repeated object allocation on item selection.

```java
private Date getTrainingExpiryDate(List<TrainingItem> training, int position) {
    ServerDateFormatter dateFormatter = new ServerDateFormatter();  // line 160 — new instance each call
```

---

### A62-19 — INFO: `EquipmentActivity.LOCATION_SETTINGS_REQUEST_GPS` is statically imported but not used in `EquipmentListFragment`

**File:** `EquipmentListFragment.java`, line 40
**Category:** Dead code (unused import)

The constant `LOCATION_SETTINGS_REQUEST_GPS` is statically imported from `EquipmentActivity` (line 40) but is never referenced within `EquipmentListFragment.java`. The constant is defined in `FleetActivity` (its true owner) and used in `FleetFragment`; pulling it into this Fragment via a static import adds a spurious coupling. Android Lint will report this as an unused import.

```java
import static au.com.collectiveintelligence.fleetiq360.ui.activity.EquipmentActivity.LOCATION_SETTINGS_REQUEST_GPS;
// line 40 — never referenced in this file
```

---

### A62-20 — INFO: `MyApplication` is imported in `EquipmentListFragment` but never referenced

**File:** `EquipmentListFragment.java`, line 34
**Category:** Dead code (unused import)

`au.com.collectiveintelligence.fleetiq360.ui.application.MyApplication` is imported but no call to `MyApplication` appears anywhere in the file body.

```java
import au.com.collectiveintelligence.fleetiq360.ui.application.MyApplication;  // line 34 — unused
```

---

## Summary Table

| ID | Severity | File | Line(s) | Category | Synopsis |
|---|---|---|---|---|---|
| A62-1 | HIGH | EquipmentListFragment | 48 | Dead code | `equipmentSelected` static field never read or written anywhere |
| A62-2 | HIGH | EquipmentListFragment | 46 | Leaky abstraction | `public static` mutable Fragment field used as global data store by presenter |
| A62-3 | HIGH | EquipmentListFragment | 45 | Leaky abstraction | `public` mutable `urlList` field directly accessed by adapter; never populated |
| A62-5 | MEDIUM | EquipmentListFragment | 47 | Leaky abstraction | Package-private static flag used for inter-Fragment signalling |
| A62-6 | MEDIUM | EquipmentPrestartFragment | 35 | Style / build warning | `TAG` not declared `final` |
| A62-7 | MEDIUM | EquipmentPrestartFragment | 109 | Style inconsistency | Hardcoded log tag `"Info_header"` instead of `TAG` constant |
| A62-8 | MEDIUM | EquipmentPrestartFragment | 109, 156 | Dead code / log leakage | Production debug logs; `Log.e` misused for routine click; Unicode colon in string |
| A62-9 | MEDIUM | EquipmentPrestartFragment | 111-114 | Leaky abstraction | Region feature flag via timezone ID string match (`"America"`) |
| A62-10 | MEDIUM | EquipmentPrestartFragment | 150-152 | Dead code | `onHiddenChanged` override is a pure no-op |
| A62-11 | MEDIUM | IncidentFragment | 133 | Build warning suppression | `@SuppressLint("ClickableViewAccessibility")` hides real accessibility defect |
| A62-12 | MEDIUM | IncidentFragment | 163-165, 198-199 | Redundant code | Checkbox state set twice in `initViews` and `initValue` |
| A62-13 | MEDIUM | IncidentFragment | 51-52 | Style / potential NPE | Boxed `Boolean` instead of primitive `boolean` for `dateSet`/`timeSet` |
| A62-14 | LOW | EquipmentListFragment | 103-106 | Style | Extraneous indentation in `onItemClick` body |
| A62-15 | LOW | EquipmentListFragment | 108-109, 164 | Style | Mixed brace style (Allman vs K&R) in two methods |
| A62-16 | LOW | EquipmentListFragment | 133, 143 | Style | Hardcoded user-facing strings; double-space typo in expiry warning message |
| A62-17 | LOW | EquipmentPrestartFragment | 38 | Style | `qustionItemArrayList` — misspelled public field name propagated to adapter |
| A62-18 | LOW | EquipmentListFragment | 160 | Style / minor inefficiency | `ServerDateFormatter` instantiated per-call instead of as instance field |
| A62-19 | INFO | EquipmentListFragment | 40 | Dead code | Unused static import of `LOCATION_SETTINGS_REQUEST_GPS` |
| A62-20 | INFO | EquipmentListFragment | 34 | Dead code | Unused import of `MyApplication` |
