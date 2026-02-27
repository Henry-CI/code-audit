# Pass 1 Security Audit — forkliftiqapp
**Agent ID:** XML01
**Date:** 2026-02-27
**Auditor scope:** LibCommon XML resources; App anim/color/drawable XML files

---

## Step 1 — Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

**Discrepancy noted:** The checklist header states `Branch: main`. The actual branch is `master`. Audit proceeds on `master` as confirmed.

---

## Step 2 — Checklist Reference

Full checklist read at: `/c/Projects/cig-audit/audit-skills/PASS1-CHECKLIST-forkliftiqapp.md`

Checklist sections applicable to XML resource files:
- Section 2: Network Security — WebView usage in layout XML (JavaScript enabled, `setAllowFileAccess`, URL whitelisting)
- Section 4: Input and Intent Handling — WebView configuration in layouts
- All other sections (Signing, Data Storage, Authentication, Libraries, Platform) are not directly evidenced by drawable/anim/color/values XML resources; those sections are addressed by other agents reviewing Java source, Gradle, and Manifest files.

---

## Step 3 & 4 — Files Read with Evidence

### LibCommon XML Resources

#### `/c/Projects/cig-audit/repos/forkliftiqapp/LibCommon/src/main/res/color/text_color_light_white.xml`
- Type: Color state list (selector)
- States defined: `state_selected="true"` → `#ffffff`; `state_enabled="false"` → `@color/text_disabled_dark`; default → `@color/text_light`
- No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/LibCommon/src/main/res/drawable/bg_gray_frame_fill_white.xml`
- Type: Shape drawable (selector wrapping a shape)
- Defines: white fill (`#FFFFFF`), 1px gray stroke (`#bbbbbb`), 0dp corners
- No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/LibCommon/src/main/res/drawable/bg_oval.xml`
- Type: Shape drawable (`android:shape="oval"`)
- Defines: solid fill with `@color/colorPrimary`
- No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/LibCommon/src/main/res/drawable/bg_oval_red.xml`
- Type: Shape drawable (`android:shape="oval"`)
- Defines: solid fill `#FF0000`
- No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/LibCommon/src/main/res/drawable/dialog_title_background.xml`
- Type: Shape drawable (selector wrapping a shape)
- Defines: solid `@color/colorPrimary`, top-left 2dp radius, top-right 2dp radius, no bottom radius
- No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/LibCommon/src/main/res/drawable/error_dialog_button_background.xml`
- Type: State drawable (selector)
- Delegates to `@drawable/error_dialog_button_background_pressed` (state_pressed) and `@drawable/error_dialog_button_background_released` (default)
- No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/LibCommon/src/main/res/drawable/error_dialog_button_background_pressed.xml`
- Type: Shape drawable (selector wrapping a shape)
- Defines: semi-transparent gray fill (`#11AAAAAA`), 1dp radius corners
- No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/LibCommon/src/main/res/drawable/error_dialog_button_background_released.xml`
- Type: Shape drawable (selector wrapping a shape)
- Defines: fully transparent fill (`#00FFFFFF`), 1dp radius corners
- No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/LibCommon/src/main/res/drawable/hollow_orange_button_text.xml`
- Type: Color state list (selector)
- States: disabled+not-pressed → `#ffb4b4b4`; disabled+pressed → `#ffb4b4b4`; selected+not-pressed → `#FFFFFF`; selected+pressed → `#FFFFFF`; not-selected+pressed → `#FFFFFF`; not-selected+not-pressed → `@color/colorPrimary`; default → `@color/colorPrimary`
- No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/LibCommon/src/main/res/drawable/orange_hollow_dialog_button.xml`
- Type: State drawable (selector)
- Delegates to `@drawable/orange_hollow_dialog_button_pressed` for state_pressed and state_selected; `@drawable/orange_hollow_dialog_button_released` for default
- No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/LibCommon/src/main/res/drawable/orange_hollow_dialog_button_pressed.xml`
- Type: Shape drawable (selector wrapping a shape)
- Defines: solid `@color/colorPrimary` fill, 1dp stroke of `@color/colorPrimary`, 0dp corners
- No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/LibCommon/src/main/res/drawable/orange_hollow_dialog_button_released.xml`
- Type: Shape drawable (selector wrapping a shape)
- Defines: transparent fill (`#00FFFFFF`), 1dp stroke of `@color/colorPrimary`, 0dp corners
- No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/LibCommon/src/main/res/layout/base_error_dialog.xml`
- Type: Layout (LinearLayout, vertical)
- Views: `AMTextView` (title, id `error_dialog_titleTextView`), `AMTextView` (message, id `error_dialog_errorTextView`), `AMTextView` (close button, id `error_dialog_closeTextView`)
- No WebView. No sensitive data fields. Static dialog layout only.
- No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/LibCommon/src/main/res/layout/base_themed_dialog.xml`
- Type: Layout (LinearLayout, vertical)
- Views: FrameLayout title bar with three `AMTextView` elements (title, left, right); empty RelativeLayout content area
- No WebView. No sensitive data fields.
- No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/LibCommon/src/main/res/layout/base_themed_dialog_full_screen.xml`
- Type: Layout (LinearLayout, vertical, match_parent × match_parent)
- Views: FrameLayout title bar (60dp) with three `AMTextView` elements; empty RelativeLayout content area (match_parent × match_parent)
- No WebView. No sensitive data fields.
- No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/LibCommon/src/main/res/layout/custom_progress_dialog.xml`
- Type: Layout (LinearLayout, vertical)
- Views: ProgressBar (indeterminate spinner) and `AMTextView` ("Loading...")
- No WebView. No sensitive data fields.
- No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/LibCommon/src/main/res/layout/notes_dialog.xml`
- Type: Layout (LinearLayout, vertical)
- Views: Title bar (`AMTextView` id `notes_dialog_titleTextView`), `AMEditText` (id `notes_dialog_editText`, hint "Your text here"), Cancel and Save `AMButton` elements
- The EditText field is a free-text notes input. No `inputType` attribute is set, which means it defaults to plain text — acceptable for a notes field. No `android:password` or credential-entry characteristics.
- No WebView. No security-relevant content beyond noting the absence of an explicit `inputType`.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/LibCommon/src/main/res/layout/signature_dialog.xml`
- Type: Layout (LinearLayout, vertical, fill_parent × fill_parent)
- Views: `AMTextView` ("Please sign below"), custom `com.yy.libcommon.DrawingView` (id `signature_dialog_drawingView`), Cancel / Clear / Save `AMButton` elements
- The DrawingView captures a finger-drawn signature. The security risk (where the captured bitmap is stored or transmitted) is in the Java code, not the layout XML.
- No WebView. No security-relevant content visible in this file.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/LibCommon/src/main/res/layout/themed_dialog_single_list_item.xml`
- Type: Layout (LinearLayout, horizontal) — a list row item
- Views: inner LinearLayout with `AMTextView` (id `themed_dialog_single_list_item_textView`), `AMTextView` subtext (id `themed_dialog_single_list_item_subtextView`, gone), `ImageView` tick (id `themed_dialog_single_list_item_imageView`, gone)
- No WebView. No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/LibCommon/src/main/res/layout/themed_single_list_dialog.xml`
- Type: Layout (LinearLayout, vertical)
- Views: `AMTextView` top label (gone by default), `ListView` (id `themed_single_list_dialog_listView`)
- No WebView. No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/LibCommon/src/main/res/layout/web_activity.xml`
- Type: Layout (LinearLayout, vertical) — **CONTAINS WebView**
- Views: `WebView` (id `web_view`, match_parent × match_parent), `TextView` (id `failed_text`, error message, initially visible), `com.natasa.progresspercent.LineProgress` (id `line_progress_bar`, 2dp height)
- **Security note (Informational):** A `WebView` is present in this layout. The layout XML alone does not configure JavaScript, file access, or URL loading — these are controlled in the backing Java Activity/Fragment class. The WebView security posture must be assessed in the associated Java code (WebActivity or equivalent). Flagging here for cross-reference by the Java audit agents.
- No JavaScript-enabling attributes, no `setAllowFileAccess`, and no URL hardcoded in this XML. Risk level of this file alone: **Informational** — requires Java code review to fully assess.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/LibCommon/src/main/res/layout/yes_no_dialog.xml`
- Type: Layout (LinearLayout, vertical)
- Views: Title bar (`AMTextView` id `yes_no_dialog_titleTextView`), body `AMTextView` (id `yes_no_dialog_detailsTextView`, default text "Are you sure you want to save this?"), two `AMButton` elements labeled "RESUME CALL" and "EXIT CALL"
- The button labels ("RESUME CALL" / "EXIT CALL") suggest this dialog is reused for call-management confirmation flows. No credential input fields.
- No WebView. No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/LibCommon/src/main/res/values/attrs.xml`
- Type: Attribute declarations
- Declares: `ToggleImageButton` styleable (`android:checked`, `checkedBackground` integer, `uncheckedBackground` integer); `AMTextView` styleable (`ttf_type` string)
- No URLs, secrets, or security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/LibCommon/src/main/res/values/colors.xml`
- Type: Color resource definitions
- Colors defined: `colorPrimary` (`#28B8B7`), `text_black`, `text_dark`, `text_grey`, `text_light`, `text_disabled_dark`, `text_disabled`, `default_list_divider`, `light_list_divider`
- No hardcoded API keys, tokens, or credentials. Pure UI palette.
- No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/LibCommon/src/main/res/values/dimens.xml`
- Type: Dimension resource definitions
- Defines: `base_list_height` (54dp), `base_list_icon_height` (32dp), `base_list_item_title_text` (20sp), `base_list_item_sub_text` (15sp), `base_list_item_padding` (15dp), `default_dialog_width` (300dp), `default_dialog_height` (260dp), `small_dialog_width` (260dp), `default_list_divider_height` (1px)
- No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/LibCommon/src/main/res/values/strings.xml`
- Type: String resource definitions
- Strings defined: `app_name` ("LibCommon"), and UI labels: `all`, `ok`, `proceed`, `retry`, `ignore`, `skip`, `loading`, `saving`, `deleting`, `cancel`, `options`, `search`, `error`, `success`, `done`, `warning`
- No hardcoded URLs, API endpoints, credentials, or sensitive data.
- No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/LibCommon/src/main/res/values/styles.xml`
- Type: Style definitions
- Defines: `orange_hollow_dialog_button` style (parent `@android:style/Widget.Button`), setting background, textColor, textSize, padding, gravity
- No security-relevant content.

---

### App anim/color/drawable XML Files

#### `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/res/anim/fragment_slide_in_from_left.xml`
- Type: Translate animation
- Attributes: duration 600ms, fromXDelta `-100.0%p`, toXDelta `0.0`, decelerate interpolator
- No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/res/anim/fragment_slide_out_from_left.xml`
- Type: Translate animation
- Attributes: duration 600ms, fromXDelta `0.0`, toXDelta `-100.0%p`, decelerate interpolator
- No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/res/color/text_color_selector_radio_button.xml`
- Type: Color state list (selector)
- States: `state_checked="true"` → `@color/color_blue`; `state_checked="false"` → `@color/text_grey`; default → `@color/text_light`
- No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/res/drawable/bg_blue_frame_fill_grey.xml`
- Type: Shape drawable
- Defines: gray fill (`#f0f0f0`), 1dip radius corners, 1dip teal stroke (`#20c997`)
- No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/res/drawable/bg_dark_frame_fill_white.xml`
- Type: Shape drawable (selector wrapping a shape)
- Defines: white fill (`#FFFFFF`), 1px dark gray stroke (`#999999`), 0dp corners
- No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/res/drawable/bg_edittext.xml`
- Type: State drawable (selector)
- Delegates to `@drawable/bg_edittext_normal` (state_window_focused=false) and `@drawable/bg_edittext_focused` (state_focused=true)
- No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/res/drawable/bg_edittext_focused.xml`
- Type: Shape drawable
- Defines: white fill, 1dip radius corners, 2dip blue stroke (`#66afe9`) for focused state
- No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/res/drawable/bg_edittext_normal.xml`
- Type: Shape drawable
- Defines: white fill, 1dip radius corners, 1dip teal stroke (`#20c997`) for normal state
- No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/res/drawable/bg_frame_gray.xml`
- Type: Shape drawable (selector wrapping a shape)
- Defines: transparent fill (`#00FFFFFF`), 1dp gray stroke (`#cccccc`), 0dp corners
- No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/res/drawable/bg_gray_frame_fill_white.xml`
- Type: Shape drawable (selector wrapping a shape)
- Defines: white fill (`#FFFFFF`), 1px gray stroke (`#bbbbbb`), 0dp corners
- Identical content to `LibCommon/src/main/res/drawable/bg_gray_frame_fill_white.xml` — resource duplication, not a security issue.
- No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/res/drawable/bottom_line.xml`
- Type: Layer-list drawable
- Defines: a single layer with transparent fill and gray stroke (`#e0e0e0`), offset top/left/right by -2dp to simulate a bottom border only
- No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/res/drawable/bottom_line_dash.xml`
- Type: Layer-list drawable
- Defines: same bottom-border technique as `bottom_line.xml` but stroke color references `@color/dashboard_divider`
- No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/res/drawable/checklist_btn_selector.xml`
- Type: State drawable (selector)
- States: `state_checked="true"` → `@drawable/switch_on`; `state_checked="false"` → `@drawable/switch_off`
- No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/res/drawable/ci_bg_gray_frame_round_fill_gray.xml`
- Type: State drawable (selector with shape)
- States: enabled → gray fill (`#fbfbfb`), 1dp gray stroke (`#999999`), 2dp corners; disabled → darker gray fill (`#e0e0e0`), same stroke
- No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/res/drawable/ci_bg_gray_frame_round_fill_white.xml`
- Type: State drawable (selector with shape)
- States: enabled → near-white fill (`#fbfbfb`), 1px gray stroke (`#999999`), 2dp corners; disabled → gray fill (`#cccccc`), same stroke
- No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/res/drawable/dashboard_edit.xml`
- Type: State drawable (selector)
- States: `state_window_focused="false"` → `@color/color_dashboard_edit_text_bg`; `state_focused="true"` → `@color/color_dashboard_edit_text_bg`; default → same color. (Commented-out alternative references `@drawable/dashboard_edittext_focused`.)
- No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/res/drawable/dashboard_edittext_focused.xml`
- Type: Shape drawable
- Defines: white fill, 3dip corners, 1dip light teal stroke (`#E6ECEC`)
- No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/res/drawable/dashboard_statics_groupbtn_selector.xml`
- Type: State drawable (selector)
- States: `state_checked="true"` → `@drawable/radio_on`; `state_checked="false"` → `@drawable/radio_off`
- No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/res/drawable/error_dialog_button_background.xml`
- Type: State drawable (selector)
- Delegates to `@drawable/error_dialog_button_background_pressed` (state_pressed) and `@drawable/error_dialog_button_background_released` (default)
- Identical content to `LibCommon/src/main/res/drawable/error_dialog_button_background.xml` — resource duplication, not a security issue.
- No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/res/drawable/error_dialog_button_background_pressed.xml`
- Type: Shape drawable (selector wrapping a shape)
- Defines: semi-transparent gray fill (`#11AAAAAA`), 1dp radius corners
- Identical content to `LibCommon` equivalent. No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/res/drawable/error_dialog_button_background_released.xml`
- Type: Shape drawable (selector wrapping a shape)
- Defines: transparent fill (`#00FFFFFF`), 1dp radius corners
- Identical content to `LibCommon` equivalent. No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/res/drawable/jobs_title_radio_btn_selector.xml`
- Type: State drawable (selector)
- States: `state_checked="true"` → `@color/color_dashboard_radio_group_bg`; no false/default state (falls through to transparent)
- No security-relevant content.

#### `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/res/drawable/tab_button.xml`
- Type: State drawable (selector)
- States: `state_checked="true"` → `@color/ci_dark_blue`; `state_checked="false"` → `@color/color_blue`
- No security-relevant content.

---

## Step 5 — Checklist Review

### Section 1 — Signing and Keystores
Not applicable to XML resource files. No findings from assigned files.

### Section 2 — Network Security

**WebView present in layout:** `web_activity.xml` (LibCommon module) contains a `<WebView>` element (id `web_view`).

- The XML layout does not set any WebView configuration attributes. WebView configuration in Android is done entirely in Java code via `WebSettings`, not in layout XML.
- **Action required for Java audit agents:** The backing Activity or Fragment that inflates `web_activity.xml` must be examined for:
  - `setJavaScriptEnabled(true)` — if set without URL whitelisting, this is a High finding.
  - `setAllowFileAccess(true)` or `setAllowContentAccess(true)` — elevated risk if combined with JavaScript.
  - `WebViewClient.shouldOverrideUrlLoading()` — verify URL validation is performed.
  - Whether URLs loaded are validated against an allowlist or are user-controllable.
- No hardcoded URLs, API endpoints, or IP addresses found in any of the assigned XML resource files (including `strings.xml`).

**Finding (Informational — XML scope):** WebView widget is declared in `LibCommon/src/main/res/layout/web_activity.xml`. Security configuration must be confirmed in the associated Java class. Cross-reference needed.

### Section 3 — Data Storage
Not applicable to the assigned XML resource files (no SharedPreferences, file I/O, or SQLite in XML). No findings from assigned files.

### Section 4 — Input and Intent Handling

**WebView in layout:** See Section 2 above. The layout-level finding is informational; the actual risk depends on Java code.

**No deep link / intent-filter declarations** are present in the assigned XML files (those would appear in `AndroidManifest.xml`, not resource XMLs).

No security-relevant findings from assigned files beyond the WebView cross-reference flagged above.

### Section 5 — Authentication and Session
Not applicable to XML resource files. No findings from assigned files.

### Section 6 — Third-Party Libraries
**Third-party widget present in layout:** `web_activity.xml` references `com.natasa.progresspercent.LineProgress` (id `line_progress_bar`). This is the PercentProgress library noted in the checklist as a library of interest. Version and CVE status must be confirmed in `build.gradle` by the Gradle audit agent.

No other third-party library references found in assigned XML files beyond standard Android SDK and LibCommon internal classes (`com.yy.libcommon.*`).

### Section 7 — Google Play and Android Platform
Not applicable to drawable/anim/color/values XML resource files. No findings from assigned files.

---

## Summary of Findings

| ID | Severity | File | Description |
|----|----------|------|-------------|
| XML01-F01 | Informational | `LibCommon/src/main/res/layout/web_activity.xml` | WebView widget declared. JavaScript enablement, file access, and URL validation must be confirmed in the backing Java Activity class. |
| XML01-F02 | Informational | `LibCommon/src/main/res/layout/web_activity.xml` | References `com.natasa.progresspercent.LineProgress` (PercentProgress library). Version and CVE status to be confirmed by Gradle audit agent. |
| XML01-F03 | Informational | Branch | Checklist header states `Branch: main`; actual branch is `master`. Discrepancy recorded. Audit proceeded on `master`. |

**No Medium, High, or Critical findings** were identified within the assigned XML resource files.

**No hardcoded secrets, API keys, URLs, or credentials** were found in any assigned file.

**No security-misconfiguring XML attributes** (e.g., `android:debuggable`, `android:usesCleartextTraffic`, `android:exported`, `android:allowBackup`) are present in the assigned resource files. Those attributes are in `AndroidManifest.xml` and `build.gradle`, which are outside this agent's scope.

---

*End of XML01 Pass 1 report.*
