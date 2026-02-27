# Pass 1 Security Audit — Agent APP49

**Date:** 2026-02-27
**Repo:** forkliftiqapp
**Agent ID:** APP49

---

## Step 1 — Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

Checklist states "Branch: main" — actual branch is "master". Discrepancy recorded. Branch is "master" as expected per instructions; audit proceeds.

---

## Step 2 — Files Audited

1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/adapter/AbsRecyclerAdapter.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/adapter/PrestartCheckListAdapter.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/adapter/SelectDriverAdapter.java`

---

## Step 3 — Reading Evidence

### File 1: AbsRecyclerAdapter.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.ui.adapter.AbsRecyclerAdapter<T>`

**Class declaration:** `public abstract class AbsRecyclerAdapter<T> extends Adapter<ViewHolder>`

**Fields:**
- `private Context context` (line 19)
- `private List<T> datas` (line 20)
- `private int resId` (line 21)
- `private OnItemClickListener onItemClickListener` (line 23)

**Public methods (with line numbers):**
- `AbsRecyclerAdapter(Context context, int resId)` — constructor, line 25
- `void setDatas(List<T> datas)` — line 31
- `List<T> getDatas()` — line 36
- `int getItemCount()` — line 41 (override)
- `MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType)` — line 47 (override)
- `void onBindViewHolder(@NonNull ViewHolder holder, int position)` — line 54 (override)
- `abstract void bindDatas(MyViewHolder holder, T data, int position)` — line 58
- `void setOnItemClickListener(OnItemClickListener onItemClickListener)` — line 100

**Inner class:** `public class MyViewHolder extends ViewHolder implements View.OnClickListener, View.OnLongClickListener` (line 60)

**MyViewHolder fields:**
- `private Map<Integer, View> mapCache = new HashMap<>()` (line 62)
- `private View layoutView` (line 63)

**MyViewHolder public methods:**
- `MyViewHolder(View layoutView)` — constructor, line 65
- `View getView(int id)` — line 72
- `void onClick(View v)` — line 84 (override)
- `boolean onLongClick(View v)` — line 91 (override)

**Interface:** `public interface OnItemClickListener` (line 96) with method `void onItemClick(View v, int position)` (line 97)

**Imports:** android.support.v7.widget (legacy support library, not AndroidX)

---

### File 2: PrestartCheckListAdapter.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.ui.adapter.PrestartCheckListAdapter`

**Class declaration:** `public class PrestartCheckListAdapter extends AbsRecyclerAdapter<String>`

**Fields:**
- `private PreStartCheckListPresenter presenter` (line 15)
- `private EquipmentPrestartFragment ui` (line 16)

**Public methods (with line numbers):**
- `void setPreStartCheckListPresenter(PreStartCheckListPresenter presenter, EquipmentPrestartFragment ui)` — line 18
- `PrestartCheckListAdapter(Context context, int resId)` — constructor, line 24
- `void bindDatas(MyViewHolder holder, String data, final int position)` — line 29 (override)

**Notable references:**
- `ui.qustionItemArrayList.get(position).id` — line 35: direct public field access on the Fragment
- `presenter.mapAnswers.put(question_id, item)` — lines 43, 55: direct public field access on the Presenter
- `presenter.mapAnswers.get(question_id)` — line 60: direct public field access on the Presenter
- Third-party import: `info.hoang8f.android.segmented.SegmentedGroup` (line 12)
- Answer strings: hardcoded literals `"NO"` (line 42) and `"YES"` (line 51)

---

### File 3: SelectDriverAdapter.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.ui.adapter.SelectDriverAdapter`

**Class declaration:** `public class SelectDriverAdapter extends AbsRecyclerAdapter<User>`

**Fields:**
- `private SelectDriverPresenter presenter` (line 11)

**Public methods (with line numbers):**
- `SelectDriverAdapter(Context context, int resId, SelectDriverPresenter presenter)` — constructor, line 13
- `void bindDatas(MyViewHolder holder, User item, int position)` — line 19 (override)

**Notable references:**
- `item.fullName()` — line 21: renders operator full name into a TextView
- `item.getPhotoUrl()` — line 24: retrieves a photo URL from the User object and passes it to `presenter.showImage()`; URL is fetched from the User model without any visible validation

---

## Step 4 — Security Review by Checklist Section

### Section 1 — Signing and Keystores

No issues found. These are UI adapter files with no reference to signing configuration, keystores, passwords, or credential management. Not applicable to this file set.

### Section 2 — Network Security

**Finding — LOW — Unvalidated URL passed to image loader (SelectDriverAdapter.java, line 24)**

`presenter.showImage(item.getPhotoUrl(), iv)` passes a URL retrieved from the `User` model directly to the presenter's image loading method without any validation at the adapter layer. The URL origin and scheme (HTTP vs HTTPS) are not checked here. If `getPhotoUrl()` can return an HTTP URL or an attacker-controlled value (e.g., via a compromised API response), the image loader would silently make a cleartext or malicious network request. The validation responsibility is deferred entirely to `presenter.showImage()`; no evidence of validation is visible in this file.

No other network-related issues found in the three files.

### Section 3 — Data Storage

No issues found. These adapter files do not interact with SharedPreferences, file I/O, SQLite, or external storage. No credentials or sensitive data are stored. Not applicable to this file set.

### Section 4 — Input and Intent Handling

**Finding — LOW — Direct public field access bypasses encapsulation (PrestartCheckListAdapter.java, lines 35, 43, 55, 60)**

The adapter directly accesses public fields on both the Fragment (`ui.qustionItemArrayList`) and the Presenter (`presenter.mapAnswers`). While this is an architectural concern rather than a direct exploitable vulnerability, the lack of accessor control means any code referencing these objects can arbitrarily modify prestart checklist answers and question data without going through any validation logic in the Presenter. If an attacker could influence these public data structures through another path (e.g., a rogue adapter or reflection), checklist answer integrity could be compromised silently.

No WebView usage found. No deep link handlers found. No Intent construction found. Not applicable to this file set beyond the finding above.

### Section 5 — Authentication and Session

No issues found. These adapter files contain no authentication logic, token handling, or session management. Not applicable to this file set.

### Section 6 — Third-Party Libraries

**Finding — INFO — Legacy Android Support Library in use (AbsRecyclerAdapter.java, lines 5–6)**

Imports reference `android.support.v7.widget.RecyclerView` (the legacy Android Support Library) rather than `androidx.recyclerview.widget.RecyclerView` (AndroidX). The Android Support Library reached end-of-life in 2018 and receives no further security patches. This is a systemic issue visible across all three adapter files. All three extend or use `AbsRecyclerAdapter`, which is built on the deprecated support library.

**Finding — INFO — Third-party segmented control library (PrestartCheckListAdapter.java, line 12)**

Import: `info.hoang8f.android.segmented.SegmentedGroup`. This is the `android-segmented` library by hoang8f. This library is not maintained and has had no releases since approximately 2015 (over 10 years). Per the checklist note referencing abandoned libraries, this constitutes an abandoned dependency. No known CVEs are on record, but the lack of maintenance means security issues would not be patched.

No direct dependency declarations are present in these source files; full library audit requires review of `build.gradle`.

### Section 7 — Google Play and Android Platform

**Finding — LOW — Deprecated API: Legacy Support Library (AbsRecyclerAdapter.java, lines 5–6)**

Use of `android.support.*` imports instead of `androidx.*` is deprecated. Google Play and Android tooling have required AndroidX migration since 2019. This affects maintainability and the ability to receive security updates from upstream RecyclerView components.

**Finding — INFO — `@SuppressLint("UseSparseArrays")` suppression (AbsRecyclerAdapter.java, line 61)**

The `HashMap<Integer, View>` used as a view cache in `MyViewHolder` is flagged by Android Lint as a performance issue (`UseSparseArrays`). The suppression annotation silences this warning rather than addressing it. This is a performance note, not a security finding, but the suppression habit is worth flagging.

No AsyncTask usage found. No `startActivityForResult` usage found. No runtime permission requests found in these files.

---

## Step 5 — Summary of Findings

| Severity | File | Line(s) | Finding |
|----------|------|---------|---------|
| LOW | SelectDriverAdapter.java | 24 | User photo URL passed to image loader without scheme or origin validation at adapter layer |
| LOW | PrestartCheckListAdapter.java | 35, 43, 55, 60 | Direct access to public fields on Fragment and Presenter bypasses encapsulation; checklist answer data can be modified without validation |
| LOW | AbsRecyclerAdapter.java | 5–6 | Legacy Android Support Library (end-of-life 2018) instead of AndroidX; no further security patches |
| INFO | PrestartCheckListAdapter.java | 12 | Abandoned third-party library `info.hoang8f.android.segmented`; no maintenance since ~2015 |
| INFO | AbsRecyclerAdapter.java | 61 | `@SuppressLint("UseSparseArrays")` suppresses Lint warning rather than addressing it |

**No Critical or High findings in the assigned files.**

---

## Step 6 — Branch Discrepancy Note

The checklist header specifies `Branch: main`. The actual default branch of this repository is `master`. All audit work was performed on `master`. This discrepancy should be corrected in the checklist template.
