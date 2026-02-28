cat: 'C:/Projects/cig-audit/repos/mark3-pvd/audit/2026-02-28-01/p4-*-temp.md': No such file or directory
# Pass 4 Agent A01 — Code Quality

**Audit run:** 2026-02-28-01
**Branch:** master
**Repo root:** C:/Projects/cig-audit/repos/mark3-pvd
**Assigned files:** `run_tests`, `netcfg.json`, `.gitignore`

---

## Reading Evidence

### `run_tests`

**File purpose:** A POSIX shell script that runs the compiled test binary `FleetFocus` and post-processes its output by colourising lines based on their content (PASS, FAIL, DEBUG, WARN).

**Functions/methods:** None defined. The script is a single pipeline with no functions.

**Constants defined:** None. ANSI escape codes are embedded as string literals inline in the `awk` program.

**Types/errors defined:** None.

**Full content (9 lines):**

```sh
#!/bin/sh
./FleetFocus | awk '
    /PASS/ {print "\033[32m" $0 "\033[0m"}    # Green for PASS
    /FAIL/ {print "\033[31m" $0 "\033[0m"}    # Red for FAIL
    /DEBUG/ {print $0}                         # Leave debug as-is (yellow from handler)
    /WARN/ {print $0}                          # Leave warn as-is (magenta from handler)
    !/PASS|FAIL|DEBUG|WARN/ {print $0}        # Other lines unchanged
'
```

Line 1: shebang `#!/bin/sh`
Line 2–8: Single pipeline — `./FleetFocus` piped into an inline `awk` program.

---

### `netcfg.json`

**File purpose:** A JSON configuration file providing default Wi-Fi provisioning credentials (SSID and password). The file is embedded in the Qt resource bundle (`mk3.qrc` line 29) at compile time and listed in the `DISTFILES` variable of both `mk3.pro` (line 192) and `mk3-test.pro` (line 200). Git history shows it was introduced in commit `5fdc821` ("Implement default Wifi SSID & Pass (MK3-289)") and modified in `2adcd83` ("Fix missing SSID and password").

**Functions/methods:** None (data file).

**Constants/types/errors:** None (data file).

**Keys defined:**

| Line | Key | Value |
|------|-----|-------|
| 2 | `password` | `P@ssMK3!` |
| 3 | `ssid` | `cigSecureConnect` |

---

### `.gitignore`

**File purpose:** Tells git which files and patterns to exclude from version control in this repository.

**Functions/methods:** None (configuration file).

**Constants/types/errors:** None (configuration file).

**Rules defined (7 effective lines):**

| Line | Pattern | Effect |
|------|---------|--------|
| 1 | `Makefile` | Ignores the generated production Makefile |
| 2 | `FleetFocus` | Ignores the compiled test/production binary |
| 3 | `.*` | Ignores all dot-files/directories |
| 5 | `/tmp` | Ignores the `/tmp` directory at repo root |
| 7 | `!.gitignore` | Re-includes `.gitignore` itself (negates line 3) |
| 8 | `*.bak` | Ignores all `.bak` backup files |

Note: Line 4 and line 6 are blank separator lines.

---

## Findings

---

**A01-1** · CRITICAL · Plaintext credential committed to version control and compiled into firmware

**Description:** `netcfg.json` contains a plaintext Wi-Fi password (`P@ssMK3!`) and SSID (`cigSecureConnect`) committed to the repository (first introduced in commit `5fdc821`, modified in `2adcd83`). The file is also bundled into the Qt resource archive via `mk3.qrc` (line 29), meaning the credential is compiled directly into every firmware binary. Any party with repository read access or a firmware binary can trivially extract the credential using `strings` or Qt resource tools. The credential cannot be rotated without a code change and a new commit, and the old value remains permanently in git history. This is a provisioning or default network credential that has no business being stored in version control or baked into firmware.

**Fix:** (1) Remove `netcfg.json` from the repository immediately and rotate the password. (2) Add `netcfg.json` to `.gitignore`. (3) Remove `netcfg.json` from `mk3.qrc` and from `DISTFILES` in both `.pro` files. (4) Inject the credential at device provisioning time (written to protected on-device storage, not compiled in). (5) Purge the file from git history using `git filter-repo --path netcfg.json --invert-paths` or an equivalent tool, then force-push and notify all collaborators to re-clone.

---

**A01-2** · HIGH · `run_tests` script has no error handling and silently swallows test-runner failures

**Description:** The script uses `#!/bin/sh` and contains no `set -e`, `set -o pipefail`, or any explicit exit-code propagation. The test binary `./FleetFocus` is piped directly into `awk`. In any POSIX shell without `pipefail`, the exit status of the entire pipeline is that of the last command (`awk`), not of `./FleetFocus`. If `./FleetFocus` crashes, exits non-zero, or cannot be found, the script still exits 0 as long as `awk` exits 0. This means CI or any automated caller will see a success even when all tests have crashed. Additionally, if `./FleetFocus` does not exist in the current working directory (the script is run from a directory other than the one containing the binary) it fails with a non-actionable `./FleetFocus: not found` message with no diagnostic context.

**Fix:** (1) Replace `#!/bin/sh` with `#!/bin/bash` (or use `set -o pipefail` if `sh` must be kept, though `pipefail` is not specified by POSIX). (2) Add `set -euo pipefail` at the top of the script. (3) Capture and propagate the exit code of `./FleetFocus` explicitly, e.g.:

```bash
#!/bin/bash
set -euo pipefail
./FleetFocus | awk '...'
exit "${PIPESTATUS[0]}"
```

(4) Add a guard to verify the binary exists before running it.

---

**A01-3** · MEDIUM · `run_tests` uses a relative path to the test binary

**Description:** The script invokes the test binary as `./FleetFocus` (a path relative to the current working directory at the time the script is run). If the script is executed from any directory other than the one containing the compiled `FleetFocus` binary, it will fail. There is no documentation, comment, or guard indicating the required working directory. The `.gitignore` ignores `FleetFocus` (the binary) but the script assumes it is co-located with itself. The Makefile.test confirms the binary is produced in the same root as `run_tests`, but this is an implicit coupling.

**Fix:** Derive the binary path relative to the script's own location rather than the caller's working directory. For example:

```bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
"${SCRIPT_DIR}/FleetFocus" | awk '...'
```

---

**A01-4** · MEDIUM · `netcfg.json` embeds no schema version and has no validation mechanism

**Description:** `netcfg.json` contains two fields (`ssid`, `password`) with no schema version field, no required-field marker, and no indication of expected value constraints (e.g., SSID must be 1–32 bytes, WPA2 password must be 8–63 bytes). The application code in `wifi.cpp` and `globalconfigs.cpp` validates Wi-Fi parameters at the point of use, but there is no validation path visible for the values loaded from `netcfg.json` itself (no `.cpp` or `.h` file references `netcfg.json` by name). If either key is absent, has an empty value, or has an invalid length, the failure mode is silent or undefined. The absence of a schema version means any future addition of new configuration fields provides no forward- or backward-compatibility signal.

**Fix:** Add a `"version"` field to `netcfg.json` (e.g., `"version": 1`). Add explicit parsing and validation of the file in the code that consumes it, checking that both `ssid` and `password` are present, non-empty, and within specification limits. Return a clear error if validation fails.

---

**A01-5** · MEDIUM · `.gitignore` rule `.*` is overly broad and masks developer tooling files

**Description:** The pattern `.*` on line 3 matches every dot-file and dot-directory at every level of the repository, including — but not limited to — `.env`, `.env.local`, IDE project files (`.idea/`, `.vscode/`), and secret key files (`.ssh/`, `.netrc`). While the rule `!.gitignore` on line 7 correctly re-includes `.gitignore` itself, any other configuration or tooling file that developers may legitimately want to track (e.g., `.clang-format`, `.editorconfig`, `.clang-tidy`) is silently excluded. Developers may not notice that their tooling configuration files are not being tracked, leading to inconsistent development environments across the team.

**Fix:** Replace the single `.*` wildcard with an explicit allowlist/denylist approach. Keep denying clearly sensitive patterns, and explicitly allow known tooling dot-files that should be tracked:

```
# Explicitly ignore sensitive files
.env
.env.*
.netrc

# Allow tracked dot-files
!.gitignore
!.clang-format
!.editorconfig
```

---

**A01-6** · LOW · `.gitignore` ignores `Makefile` but not `Makefile.test`

**Description:** Line 1 of `.gitignore` ignores `Makefile` (the generated production Makefile). However, `Makefile.test` (the generated test Makefile) is not ignored and is tracked in the repository. `Makefile.test` is a fully generated file produced by `qmake -o Makefile.test mk3-test.pro` and contains machine-specific absolute paths (e.g., `/home/ryanharm/git/sdk/qt/...`, `/home/ryanharm/git/mark3-pvd/...`) embedded throughout. Committing generated files with developer-specific absolute paths pollutes the repository history, causes spurious diffs on every developer machine, and leaks details about the development environment layout.

**Fix:** Add `Makefile.test` to `.gitignore` and remove it from the repository index (`git rm --cached Makefile.test`).

---

**A01-7** · LOW · `Makefile.test` (tracked file) contains hardcoded developer home directory paths

**Description:** Although `Makefile.test` is not one of the three directly assigned files, it is a tracked file in the repository and its presence is directly caused by the gap in `.gitignore` noted in A01-6. The file contains multiple absolute paths rooted in `/home/ryanharm/git/...`, including SDK paths and build output directories. These paths are specific to a single developer's workstation. Any other developer or CI system must regenerate this file or patch all paths before building tests. This is a leaky abstraction — the build system's internal layout is exported into version control.

**Fix:** Add `Makefile.test` to `.gitignore` (see A01-6). Document the `qmake` command to regenerate it in a `README` or build script. All developers regenerate it locally; it is never committed.

---

**A01-8** · LOW · `run_tests` script has no usage comment or documentation

**Description:** The script is nine lines long with no header comment explaining its purpose, prerequisites (the `FleetFocus` binary must be pre-built), how to build it, or what the coloured output means. A new developer reading the repository has no context for when or how to run it, whether it is meant to be run manually or by a CI step, or what a passing run looks like.

**Fix:** Add a short comment block at the top of the script:

```sh
#!/bin/sh
# run_tests - Execute the compiled FleetFocus test binary and colourise output.
# Prerequisites: build the test binary first with: make -f Makefile.test
# Usage: ./run_tests
# Exit code mirrors the exit code of the FleetFocus binary (requires bash + pipefail).
```

---

**A01-9** · INFO · `netcfg.json` is listed in `DISTFILES` but no source code reads it

**Description:** `netcfg.json` is listed in the `DISTFILES` variable of both `mk3.pro` and `mk3-test.pro`, and is included in `mk3.qrc` (compiled into the Qt resource bundle). However, no `.cpp` or `.h` file in the repository references `netcfg.json` by name, nor does any code read from the `qrc:/netcfg.json` resource path. It is possible the file is read via a generic path that was not found in this search, or that the feature that reads it was removed while the file itself was not cleaned up. This is dead configuration — a file that is compiled into every firmware image but appears to serve no live code path.

**Fix:** Audit whether any code actually loads `netcfg.json` at runtime. If no code reads it, remove it from `mk3.qrc`, from `DISTFILES` in both `.pro` files, and from the repository. If code does read it, add a source-level comment or search tag so it can be located by future auditors.

---

**A01-10** · INFO · `run_tests` awk patterns are case-sensitive and may miss mixed-case output

**Description:** The `awk` patterns `/PASS/`, `/FAIL/`, `/DEBUG/`, `/WARN/` are all uppercase and case-sensitive. If any test or log output uses mixed case (e.g., `Pass`, `fail`, `Warning`), those lines will fall through to the uncolourised default case (`!/PASS|FAIL|DEBUG|WARN/`). This is a minor robustness gap rather than a security issue, but it can result in failures being displayed without the red colouring that would make them immediately visible.

**Fix:** Use case-insensitive matching in awk (`/[Pp][Aa][Ss][Ss]/` or `tolower($0) ~ /pass/`) or document the required output format contract in the test framework.

---

## Summary Table

| ID | Severity | Title |
|----|----------|-------|
| A01-1 | CRITICAL | Plaintext credential committed to version control and compiled into firmware |
| A01-2 | HIGH | `run_tests` has no error handling and silently swallows test-runner failures |
| A01-3 | MEDIUM | `run_tests` uses a relative path to the test binary |
| A01-4 | MEDIUM | `netcfg.json` embeds no schema version and has no validation mechanism |
| A01-5 | MEDIUM | `.gitignore` rule `.*` is overly broad and masks developer tooling files |
| A01-6 | LOW | `.gitignore` ignores `Makefile` but not `Makefile.test` |
| A01-7 | LOW | `Makefile.test` (tracked file) contains hardcoded developer home directory paths |
| A01-8 | LOW | `run_tests` script has no usage comment or documentation |
| A01-9 | INFO | `netcfg.json` is listed in `DISTFILES` but no source code reads it |
| A01-10 | INFO | `run_tests` awk patterns are case-sensitive and may miss mixed-case output |
# Pass 4 Agent A02 — Code Quality

**Audit run:** 2026-02-28-01
**Branch:** master
**Files reviewed:** `mk3.pro`, `mk3-test.pro`

---

## Reading Evidence

### mk3.pro

**Purpose:** Main Qt application project file for the FleetFocus production build. Controls what source, header, UI, and resource files are compiled into the `FleetFocus` binary.

| Setting | Line(s) | Value |
|---|---|---|
| `DEFINES += "TEST_MODE=0"` | 6 | Disables test mode for production build |
| `QT` modules | 8 | `core gui serialport serialbus bluetooth network` |
| `QT += widgets` (conditional) | 10 | Added when Qt major version > 4 |
| `linux:` block — `INCLUDEPATH` | 13–14 | `../sdk/kernel_include`, `../sdk/3rd/include` |
| `linux:` block — `LIBS` | 15 | `-L../sdk/3rd/lib` |
| `RCC_DIR` | 18 | `tmp/rcc` |
| `MOC_DIR` | 19 | `tmp/moc` |
| `UI_DIR` | 20 | `tmp/ui` |
| `OBJECTS_DIR` | 21 | `tmp/obj` |
| `TARGET` | 23 | `FleetFocus` |
| `TEMPLATE` | 24 | `app` |
| `DEFINES += QT_DEPRECATED_WARNINGS` | 30 | Enables deprecation warnings |
| `SOURCES` | 38–96 | 57 source files |
| `HEADERS` | 98–157 | 59 header entries (includes one duplicate) |
| `FORMS` | 160–184 | 23 UI form files |
| `RESOURCES` | 186–187 | `mk3.qrc` |
| `TRANSLATIONS` | 189 | `lang_es_ES.ts` |
| `DISTFILES` | 191–192 | `netcfg.json` |

**Commented-out define (line 35):**
```
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000
```

**Defines:**
- `TEST_MODE=0` (line 6)
- `QT_DEPRECATED_WARNINGS` (line 30)

---

### mk3-test.pro

**Purpose:** Qt test project file for the FleetFocus unit test build. Mirrors the production project but adds the `testlib` Qt module, the `UNIT_TEST` define, and four test source/header file pairs from `test/`.

| Setting | Line(s) | Value |
|---|---|---|
| `DEFINES += "TEST_MODE=0"` | 6 | Same as production — test mode disabled at macro level |
| `DEFINES += UNIT_TEST` | 7 | Enables unit-test code paths |
| `QT` modules | 9 | `core gui serialport serialbus bluetooth network testlib` |
| `QT += widgets` (conditional) | 11 | Added when Qt major version > 4 |
| `linux:` block — `INCLUDEPATH` | 13–14 | `../sdk/kernel_include`, `../sdk/3rd/include` |
| `linux:` block — `LIBS` | 15 | `-L../sdk/3rd/lib` |
| `RCC_DIR` | 19 | `tmp/rcc` |
| `MOC_DIR` | 20 | `tmp/moc` |
| `UI_DIR` | 21 | `tmp/ui` |
| `OBJECTS_DIR` | 22 | `tmp/obj` |
| `TARGET` | 24 | `FleetFocus` |
| `TEMPLATE` | 25 | `app` |
| `DEFINES += QT_DEPRECATED_WARNINGS` | 31 | Enables deprecation warnings |
| `SOURCES` | 39–100 | 61 source files (57 production + 4 test) |
| `HEADERS` | 102–165 | 63 header entries (59 production entries + 4 test, includes one duplicate) |
| `FORMS` | 168–192 | 23 UI form files (identical to production) |
| `RESOURCES` | 194–195 | `mk3.qrc` |
| `TRANSLATIONS` | 197 | `lang_es_ES.ts` |
| `DISTFILES` | 199–200 | `netcfg.json` |

**Commented-out define (line 36):**
```
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000
```

**Defines:**
- `TEST_MODE=0` (line 6)
- `UNIT_TEST` (line 7)
- `QT_DEPRECATED_WARNINGS` (line 31)

**Test-specific sources/headers (lines 40–43 / 103–106):**
- `test/test_ota.cpp` / `test/test_ota.h`
- `test/test_dialog.cpp` / `test/test_dialog.h`
- `test/test_backgroundworker.cpp` / `test/test_backgroundworker.h`
- `test/test_canbus.cpp` / `test/test_canbus.h`

---

## Findings

**A02-1** · MEDIUM · Duplicate HEADERS entry: `utils/logger.h` in both project files

**Description:** `utils/logger.h` appears twice in the `HEADERS` list in both `mk3.pro` (lines 112 and 122) and `mk3-test.pro` (lines 120 and 130). While qmake silently ignores duplicates and this does not cause a build failure, it indicates the file lists were assembled by successive concatenation rather than managed as a whole. It may cause redundant MOC processing depending on the Qt version and tool.

**Fix:** Remove the second occurrence of `utils/logger.h` from the `HEADERS` block in both `mk3.pro` and `mk3-test.pro`.

---

**A02-2** · MEDIUM · Hardcoded relative SDK path outside the repository tree

**Description:** Both project files include a `linux:` block (lines 12–16 in `mk3.pro`; lines 13–17 in `mk3-test.pro`) that adds `../sdk/kernel_include` and `../sdk/3rd/include` to `INCLUDEPATH` and `../sdk/3rd/lib` to `LIBS`. The path `../sdk/` is a sibling directory of the repository root that does not exist in the audited checkout (confirmed absent from `C:/Projects/cig-audit/repos/`). This creates an invisible build dependency on an undocumented directory layout on the developer's machine. Any developer or CI system that clones only this repository will silently get missing-include errors on Linux builds, potentially masking header resolution problems.

**Fix:** Document the required SDK checkout location in a `README` or `BUILD.md`. Consider using a qmake variable (e.g. `SDK_ROOT`) that can be overridden on the command line (`qmake SDK_ROOT=/path/to/sdk`), or use a `.prf` feature file so the dependency is explicit and version-controlled.

---

**A02-3** · MEDIUM · Test project TARGET name collides with production TARGET

**Description:** Both `mk3.pro` and `mk3-test.pro` set `TARGET = FleetFocus` (line 23 / line 24 respectively). If both projects are built in the same shadow-build directory, the test binary will overwrite the production binary without warning. In a CI pipeline that builds both projects this can silently ship a test binary to the deployment stage.

**Fix:** Set `TARGET = FleetFocusTest` (or similar) in `mk3-test.pro` to produce a distinctly named binary.

---

**A02-4** · LOW · `TEST_MODE=0` define is misleading in the test project

**Description:** `mk3-test.pro` defines `TEST_MODE=0` on line 6, identical to the production project, while simultaneously defining `UNIT_TEST` on line 7. If `TEST_MODE` is intended to gate test-only code paths (distinct from `UNIT_TEST`), the value `0` in the test project is contradictory. If `TEST_MODE` is not used for this purpose, carrying it into the test project with the same value adds confusion about what distinguishes the two build configurations at the macro level.

**Fix:** Either remove `TEST_MODE=0` from `mk3-test.pro` if it is irrelevant to the test build, or set it to `1` if it is supposed to activate test-specific code paths. Add a comment explaining the intended distinction between `TEST_MODE` and `UNIT_TEST`.

---

**A02-5** · LOW · Commented-out `QT_DISABLE_DEPRECATED_BEFORE` define is boilerplate noise

**Description:** Both files carry the QtCreator-generated comment block (lines 33–35 in `mk3.pro`; lines 33–36 in `mk3-test.pro`) with a commented-out `#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000`. This is copy-paste boilerplate from project creation in 2018 and has never been activated. Combined with the active `QT_DEPRECATED_WARNINGS` define, the project emits warnings for deprecated APIs but does not enforce that deprecated APIs are absent. In a codebase targeting embedded Linux hardware this means deprecation warnings can accumulate unnoticed.

**Fix:** Either remove the comment block entirely to reduce noise, or enable `QT_DISABLE_DEPRECATED_BEFORE` for the Qt version in use to make the build fail on deprecated API usage. At minimum, document explicitly why it remains disabled.

---

**A02-6** · LOW · Inconsistent indentation in SOURCES block between the two project files

**Description:** In `mk3.pro`, the first entry in `SOURCES` uses 8-space indentation (`        main.cpp`, line 39), while all subsequent entries use 4-space indentation (e.g. `    mytranslator.cpp`, line 40). This same asymmetry is replicated in `mk3-test.pro`. The inconsistency suggests `main.cpp` was the original auto-generated entry and all later files were appended with a different editor setting. This is a cosmetic issue but indicates the project files are not reviewed as part of code review.

**Fix:** Normalise all SOURCES entries to 4-space indentation. The corrected first line should read `    main.cpp \`.

---

**A02-7** · LOW · `OBJECTS_DIR`, `MOC_DIR`, `RCC_DIR`, `UI_DIR` share the same `tmp/` prefix with no platform conditioning

**Description:** Both project files write intermediate files to `tmp/rcc`, `tmp/moc`, `tmp/ui`, and `tmp/obj` (lines 18–21 / 19–22). Because both projects share the same relative path and the production and test binaries use the same `TARGET` name, a `make clean` in a shared shadow build can remove intermediate files from both builds simultaneously. On Windows this path is relative to the `.pro` file location, meaning parallel builds of the two projects will collide if invoked from the same directory.

**Fix:** Use distinct subdirectories per project, for example `tmp_test/` in `mk3-test.pro`, or rely on Qt's shadow build mechanism and remove the explicit `*_DIR` overrides.

---

**A02-8** · INFO · `FleetIQ360App_5.2.2F.h` present in `test/` but not referenced in either project file

**Description:** The file `test/FleetIQ360App_5.2.2F.h` exists on disk inside the `test/` directory but is not listed in `HEADERS` or `SOURCES` in either `mk3.pro` or `mk3-test.pro`. This suggests it may be a leftover artefact from a previous release or an accidentally committed file. It is not a build defect but it is dead weight in the repository.

**Fix:** Determine whether `test/FleetIQ360App_5.2.2F.h` is still needed. If not, remove it from the repository to keep the `test/` directory clean.

---

**A02-9** · INFO · Style inconsistency: section ordering differs between the two files

**Description:** Both files follow the same overall structure (DEFINES, QT, platform block, build dirs, TARGET/TEMPLATE, SOURCES, HEADERS, FORMS, RESOURCES, TRANSLATIONS, DISTFILES). However, `mk3-test.pro` places `DEFINES += UNIT_TEST` (line 7) before the `QT` assignment rather than grouping all DEFINES together or placing them after QT as done in `mk3.pro`. This minor ordering inconsistency makes it harder to diff the two files and to confirm they are otherwise identical.

**Fix:** Group `DEFINES += UNIT_TEST` together with `DEFINES += "TEST_MODE=0"` and `DEFINES += QT_DEPRECATED_WARNINGS` in a single DEFINES section for clarity.

---

## Summary Table

| ID | Severity | Title |
|---|---|---|
| A02-1 | MEDIUM | Duplicate `utils/logger.h` entry in HEADERS in both project files |
| A02-2 | MEDIUM | Hardcoded relative SDK path (`../sdk/`) outside repository tree |
| A02-3 | MEDIUM | Test project TARGET collides with production TARGET (`FleetFocus`) |
| A02-4 | LOW | `TEST_MODE=0` in test project is contradictory / misleading |
| A02-5 | LOW | Commented-out `QT_DISABLE_DEPRECATED_BEFORE` boilerplate in both files |
| A02-6 | LOW | Inconsistent indentation on first SOURCES entry in both files |
| A02-7 | LOW | Shared `tmp/` intermediate directories cause collision between the two builds |
| A02-8 | INFO | `test/FleetIQ360App_5.2.2F.h` exists on disk but is unreferenced in any project file |
| A02-9 | INFO | Minor section-ordering inconsistency between `mk3.pro` and `mk3-test.pro` |
# Pass 4 Agent A03 — Code Quality

**Audit run:** 2026-02-28-01
**Branch:** master
**Files reviewed:**
- `app/backgroundworker.h`
- `app/backgroundworker.cpp`
- `app/checklist.h`
- `app/checklist.cpp`

---

## 1. Reading Evidence

### `app/backgroundworker.h`

**Classes defined:**

- `OtaWorker` (line 38) — QObject subclass responsible for OTA firmware decompression.
- `BackgroundWorker` (line 62) — QObject subclass; central coordinator for all background hardware and network operations.

**Types / enums defined:**

| Name | Kind | Location |
|------|------|----------|
| `OtaWorker::QuitMode` | — | (not here; see BackgroundWorker) |
| `BackgroundWorker::QuitMode` | enum | line 66 — values: `QuitReboot`, `QuitPowerOff`, `QuitApp` |
| `BackgroundWorker::EthernetInterface` | enum (private) | line 100 — values: `EthModem`, `EthWifi` |

**`OtaWorker` methods (with line numbers):**

| Method | Line |
|--------|------|
| `OtaWorker(QObject *parent = nullptr)` (constructor) | 42 |
| `unpack()` | 43 |

**`OtaWorker` member variables:**

| Name | Type | Line |
|------|------|------|
| `m_isRunning` | `QAtomicInteger<quint32>` (public) | 45 |
| `m_mutex` | `QMutex` (private) | 58 |

**`BackgroundWorker` methods (all, with line numbers):**

| Method | Visibility | Line |
|--------|------------|------|
| `BackgroundWorker(QObject *parent = nullptr)` (constructor) | public | 68 |
| `setUI(Dialog *ui)` | public | 69 |
| `networkStatus()` | public inline | 70 |
| `initHash()` | private | 102 |
| `ignitionStateChanged(bool on)` | private | 103 |
| `parseLeaderCmd(const QByteArray &ba, bool local)` | private | 104 |
| `dispatchLeaderCmd(CIGCONF::LeaderCmdType type, const QByteArray &header, const QByteArray &content)` | private | 105 |
| `sendGmtpMessage(CIGCONF::GmtpMessage msg, const QByteArray &ba = QByteArray())` | private | 106 |
| `powerTimerEvent()` | private | 107 |
| `onTimerEvent()` | private | 108 |
| `changePowerState()` | private | 109 |
| `updateFile(const QString &file)` | private | 110 |
| `updateSelf(bool wait = false)` | private | 111 |
| `updateFromRamdisk()` | private | 112 |
| `timeChanged()` | private | 113 |
| `quit(const QuitMode qm)` | private | 114 |
| `quitWaitForAcks(const QuitMode qm)` | private | 115 |
| `printDateBatt()` | private | 116 |
| `getKernelBuildDate()` | private | 117 |
| `convert2UTC(QString tzone, quint64 time)` | private | 118 |
| `pointInPolygon(int polyCorners, CIGCONF::position me, CIGCONF::position *points)` | private | 119 |
| `degrees2radians(double degrees)` | private | 120 |
| `testGeofence(qint32 lat, qint32 lon)` | private | 121 |
| `checkAppCrash()` | private | 122 |
| `checkSdSpace()` | private | 123 |
| `checkFotaFail()` | private | 124 |
| `dataTest()` | private | 126 |
| `ethernetStateChanged(EthernetInterface interface, bool state)` | private | 128 |
| `sendGmtpWifiPos()` | private | 129 |
| `onAllAcksSent()` | private | 131 |
| `handleModemConnection()` | private | 132 |
| `handleNtpSynchronization(EthernetInterface interface, bool newState, bool &reconnect)` | private | 133 |
| `handleWiFiConnection()` | private | 134 |
| `monitTimer()` | private | 136 |
| `initialiseCanbus1()` | private | 138 |
| `initialiseCanbus2()` | private | 139 |

**`BackgroundWorker` signals (line numbers):**

| Signal | Line |
|--------|------|
| `powerStateChanged(CIGCONF::PowerState state)` | 80 |
| `reboot()` | 81 |
| `lockScreen(CIGCONF::MaintLockedCode code, bool remote)` | 82 |
| `ambertImpactScreen()` | 83 |
| `cardAuthorised(bool yes, quint64 id)` | 84 |
| `updateStatusInfo(...)` | 85 |
| `cmdMsgReceived(CIGCONF::BroadcastMessage m)` | 86 |
| `onDemandStarted(...)` | 87 |
| `onDemandExtended(...)` | 88 |
| `onDemandEnded(...)` | 89 |
| `sigLanguageChanged()` | 90 |
| `cmdLogin(quint64 id)` | 91 |
| `unpackOta()` | 92 |
| `cameraSettingsUpdated()` | 93 |

---

### `app/backgroundworker.cpp`

**Free functions defined:**

| Function | Line |
|----------|------|
| `streamUncompress(QByteArray &chunk, z_stream &strm, bool &finished)` | 49 |
| `crc16(quint16& state, const QByteArray &chunk)` | 130 |

**Method definitions (with line numbers in .cpp):**

| Method | Line |
|--------|------|
| `OtaWorker::OtaWorker(QObject *parent)` | 144 |
| `OtaWorker::unpack()` | 146 |
| `BackgroundWorker::BackgroundWorker(QObject *parent)` | 264 |
| `BackgroundWorker::initHash()` | 341 |
| `BackgroundWorker::parseLeaderCmd(const QByteArray &ba, bool local)` | 442 |
| `BackgroundWorker::dispatchLeaderCmd(LeaderCmdType type, const QByteArray &header, const QByteArray &content)` | 512 |
| `BackgroundWorker::sendGmtpMessage(GmtpMessage msg, const QByteArray &extra)` | 2128 |
| `BackgroundWorker::degrees2radians(double degrees)` | 2446 |
| `BackgroundWorker::pointInPolygon(int polyCorners, CIGCONF::position me, CIGCONF::position *points)` | 2450 |
| `BackgroundWorker::testGeofence(qint32 lat, qint32 lon)` | 2470 |
| `BackgroundWorker::setUI(Dialog *ui)` | 2533 |
| `BackgroundWorker::ignitionStateChanged(bool on)` | 2575 |
| `BackgroundWorker::powerTimerEvent()` | 2604 |
| `BackgroundWorker::changePowerState()` | 2645 |
| `BackgroundWorker::onTimerEvent()` | 2913 |
| `BackgroundWorker::updateFile(const QString &file)` | 2920 |
| `BackgroundWorker::updateSelf(bool wait)` | 2943 |
| `BackgroundWorker::updateFromRamdisk()` | 2960 |
| `BackgroundWorker::timeChanged()` | 2969 |
| `BackgroundWorker::quitWaitForAcks(const QuitMode qm)` | 2977 |
| `BackgroundWorker::onAllAcksSent()` | 2990 |
| `BackgroundWorker::quit(const QuitMode qm)` | 2998 |
| `BackgroundWorker::printDateBatt()` | 3040 |
| `BackgroundWorker::convert2UTC(QString tzone, quint64 time)` | 3060 |
| `BackgroundWorker::getKernelBuildDate()` | 3070 |
| `BackgroundWorker::dataTest()` | 3111 |
| `BackgroundWorker::ethernetStateChanged(EthernetInterface interface, bool state)` | 3121 |
| `BackgroundWorker::handleModemConnection()` | 3158 |
| `BackgroundWorker::handleWiFiConnection()` | 3168 |
| `BackgroundWorker::handleNtpSynchronization(EthernetInterface interface, bool newState, bool &reconnect)` | 3173 |
| `BackgroundWorker::sendGmtpWifiPos()` | 3193 |
| `BackgroundWorker::checkAppCrash()` | 3243 |
| `BackgroundWorker::checkSdSpace()` | 3261 |
| `BackgroundWorker::monitTimer()` | 3300 |
| `BackgroundWorker::checkFotaFail()` | 3316 |
| `BackgroundWorker::initialiseCanbus1()` | 3351 |
| `BackgroundWorker::initialiseCanbus2()` | 3372 |

---

### `app/checklist.h`

**Class defined:** `Checklist` (line 6)

**Nested types:**

| Name | Kind | Location |
|------|------|----------|
| `Checklist::CheckItem` | struct (with anonymous union) | lines 9–21 |

`CheckItem` fields:
- Anonymous union containing:
  - Anonymous struct with bitfields: `quint32 qId : 31`, `quint32 doNotRandomize : 1`
  - `quint32 questionId`
- `CIGCONF::ChecklistType type`
- `quint8 questionLen`
- `char question[CHECKLIST_QUESTION_LEN_100+1]`

**`Checklist` methods:**

| Method | Visibility | Line |
|--------|------------|------|
| `Checklist()` (constructor) | public | 23 |
| `isValidCheckItem(const CheckItem &item)` (static inline) | public | 25 |
| `readChecklist()` | public | 27 |
| `saveChecklist()` | public | 30 |
| `clear()` | public | 31 |
| `shuffleChecklist()` | public | 32 |
| `checkItem(int index, bool query = false) const` | public | 34 |
| `setCheckItem(int index, const CheckItem &item)` | public | 35 |
| `checksum() const` | public | 36 |
| `readChecklist50()` | private | 39 |
| `readChecklist100()` | private | 40 |
| `copyAllRandomPreop(CheckItem *randomPreop)` | private | 41 |

**`Checklist` member variables:**

| Name | Type | Line |
|------|------|------|
| `m_checkItems[CHECKLIST_MAX_IDX]` | `CheckItem` | 43 |
| `m_checkItems_shuffled[CHECKLIST_MAX_IDX]` | `CheckItem` | 44 |
| `m_dirty` | `bool` | 45 |
| `m_isShuffled` | `bool` | 46 |

---

### `app/checklist.cpp`

**Method definitions:**

| Method | Line |
|--------|------|
| `Checklist::Checklist()` | 9 |
| `Checklist::readChecklist()` | 13 |
| `Checklist::readChecklist50()` | 22 |
| `Checklist::readChecklist100()` | 65 |
| `Checklist::saveChecklist()` | 139 |
| `Checklist::clear()` | 172 |
| `Checklist::setCheckItem(int index, const CheckItem &item)` | 178 |
| `Checklist::checksum() const` | 188 |
| `Checklist::shuffleChecklist()` | 198 |
| `Checklist::copyAllRandomPreop(CheckItem *randomPreop)` | 227 |
| `Checklist::checkItem(int index, bool query) const` | 238 |

---

## 2. Findings

---

**A03-1** · HIGH · `streamUncompress` uses a `static` local variable for cross-call state

**Description:** `streamUncompress` (backgroundworker.cpp line 58) uses `static bool headerSkipped = false;` to track whether the Qt qCompress 4-byte header has been skipped. Because it is a static local, the variable is shared across all call sites and all threads. If `OtaWorker::unpack()` were ever invoked concurrently on two threads, or if the function is called from a second context before a previous decompress cycle fully resets the flag, the header-skip logic would misbehave and corrupt the output. Even in the single-call path the flag is reset in multiple `return` paths but never inside a destructor or RAII guard, so any future early-return code path risks leaving it in the wrong state. The correct approach is to pass this flag as part of the `z_stream` wrapper or as an explicit parameter, not as a hidden static.

**Fix:** Remove the `static` qualifier and pass `headerSkipped` as a plain local that is passed by reference alongside `z_stream`, or embed it in a small context struct. Alternatively, since Qt's own 4-byte header is only ever prepended to the first chunk, unconditionally strip it before the first `inflateInit` call in `OtaWorker::unpack()` and remove the flag entirely.

---

**A03-2** · HIGH · Dead function `dataTest()` is production-compiled and self-schedules

**Description:** `BackgroundWorker::dataTest()` (backgroundworker.cpp lines 3111–3119) sends arbitrary incrementing GMTP messages over the production connection and reschedules itself indefinitely via `QTimer::singleShot`. Its only call site is a commented-out line at line 2796 (`//QTimer::singleShot(1000, [this](){dataTest();});`). The function itself is not guarded by `#ifdef`, so it is compiled into the release binary, is reachable via the call at line 3118 (self-recursion through singleShot), and is exposed to any code that might accidentally uncomment line 2796. A self-scheduling debug function that transmits data over the modem link must not exist in production code.

**Fix:** Delete `dataTest()` from both the header declaration (backgroundworker.h line 126) and the implementation, and remove the commented-out call site at line 2796.

---

**A03-3** · HIGH · Unreachable `break` after `return true` in multiple `dispatchLeaderCmd` cases

**Description:** Several `switch` cases in `dispatchLeaderCmd` contain `return true;` followed immediately by `break;` on the next line (backgroundworker.cpp lines 1876–1877 for `CMD_OPRNDM`, lines 1887–1888 for `CMD_SHOWNAMES`). The `break` statements are unreachable dead code. This pattern indicates the cases were likely refactored from fall-through to early-return form without cleaning up. While not a runtime bug in these two cases, it is misleading to future maintainers and may mask accidental omission of `return` in other nearby cases.

**Fix:** Remove the unreachable `break;` statements at lines 1877 and 1888.

---

**A03-4** · MEDIUM · Qt deprecated API: `QNetworkConfigurationManager` and `QRegExp`

**Description:** Two Qt 5 APIs that are deprecated in Qt 5.15 and removed in Qt 6 are used:
1. `QNetworkConfigurationManager` is `#include`d in backgroundworker.h (line 7) and `QNetworkConfiguration` is included in backgroundworker.cpp (line 31). Neither class is referenced anywhere in the visible code of these two files; the includes appear to be dead. Both classes are fully removed in Qt 6.
2. `QRegExp` is used in `getKernelBuildDate()` at backgroundworker.cpp line 3090. `QRegExp` is deprecated since Qt 5.0 in favour of `QRegularExpression` and removed in Qt 6.

**Fix:**
1. Remove the `#include <QNetworkConfigurationManager>` from backgroundworker.h and `#include <QNetworkConfiguration>` from backgroundworker.cpp if they are genuinely unused; otherwise replace with `QNetworkInformation` (Qt 6) or a platform-specific alternative.
2. Replace `QRegExp rx(...)` with `QRegularExpression rx(...)` and update the match call accordingly.

---

**A03-5** · MEDIUM · Large commented-out code blocks throughout both files

**Description:** Significant sections of live-logic code have been commented out rather than removed, creating noise and risk of accidental reactivation:

- backgroundworker.h lines 141 (`//EM070::BleCentral *m_bleCentral;`) and 151 (`//BleExpansion *m_bleExpansion;`) — member declarations commented out; corresponding allocation code in the `.cpp` is also commented.
- backgroundworker.cpp lines 264–265, 274 — BLE member initialiser lines commented out in the constructor.
- backgroundworker.cpp lines 2680–2697 — entire `BleCentral`/`BleExpansion` initialisation block (17 lines) commented out inside `changePowerState()`.
- backgroundworker.cpp lines 2854–2856 — BleExpansion disable block commented out.
- backgroundworker.cpp lines 2971–2972 — `m_bleExpansion->setCurrentTime` call commented out in `timeChanged()`.
- backgroundworker.cpp lines 3003–3005 — `m_bleExpansion->setEnabled(false)` commented out in `quit()`.
- backgroundworker.cpp line 2796 — `QTimer::singleShot(1000, [this](){dataTest();});` commented-out debug launch.
- backgroundworker.cpp line 2881 — `QProcess::startDetached("/etc/pvd/mobile -p")` commented out.
- backgroundworker.cpp lines 723–724, 738–740 — double-commented relay-query branches (`//if (!m_bleExpansion)` then `if (!m_canExpansion)`) in `CMD_RLY1` and `CMD_RLY2`.
- backgroundworker.cpp lines 1165–1167, 1191–1193 — BLE shock threshold and period setters commented out.
- backgroundworker.cpp lines 2139, 2147–2148, 2150–2153 — commented `m_bleExpansion` calls inside `GMTP_AUTH_SHOCK` handling.
- backgroundworker.cpp lines 2660, 2665 — commented brightness and log calls.
- backgroundworker.cpp line 2727 — commented gmtpHotStartReconnect connect.
- checklist.h line 28 — declaration `//void saveChecklist50();` commented out.
- checklist.cpp lines 109–137 — entire `saveChecklist50()` implementation (29 lines) commented out.

**Fix:** Remove all commented-out code blocks. If the BLE expansion path is intentionally disabled pending hardware availability, use a `#ifdef HAVE_BLE_EXPANSION` guard or delete the code with a note in git commit history. Commented-out production code should not reside in the main branch.

---

**A03-6** · MEDIUM · `m_isShuffled` member is declared but never written or read

**Description:** `Checklist::m_isShuffled` is declared as a private `bool` in checklist.h (line 46) and is initialised to nothing (not listed in the constructor initialiser list — meaning it defaults to an indeterminate value since no `= false` initialiser is present in the in-class declaration). The variable is never read or written anywhere in checklist.cpp. It appears to be a leftover from an earlier design that checked whether `shuffleChecklist()` had been called.

**Fix:** Either remove `m_isShuffled` entirely or initialise it in the constructor (`m_isShuffled(false)`) and use it as a guard inside `checkItem()` to avoid returning shuffled data before `shuffleChecklist()` has been called. As currently written, `checkItem()` defers the shuffle decision to `gCfg->preopRandom()` which is a valid alternative, making the member entirely redundant.

---

**A03-7** · MEDIUM · `Checklist` constructor does not initialise `m_isShuffled` or the array members

**Description:** The `Checklist` constructor (checklist.cpp line 9) initialises only `m_dirty(false)`. The member `m_isShuffled` (bool) receives no initialisation and contains indeterminate data until written. The two `CheckItem` arrays `m_checkItems` and `m_checkItems_shuffled` are not initialised in the constructor either; they are zeroed lazily inside `readChecklist50()` and `readChecklist100()`. If `checkItem()` or `checksum()` is called before `readChecklist()`, they operate on uninitialised memory.

**Fix:** Add a `memset` of both arrays and initialise `m_isShuffled` in the constructor body, e.g.:
```cpp
Checklist::Checklist() : m_dirty(false), m_isShuffled(false)
{
    memset(m_checkItems, 0, sizeof(m_checkItems));
    memset(m_checkItems_shuffled, 0, sizeof(m_checkItems_shuffled));
}
```

---

**A03-8** · MEDIUM · `shuffleChecklist()` rotate boundary is off by one

**Description:** `Checklist::shuffleChecklist()` at checklist.cpp line 219 calls:
```cpp
std::rotate(&randomPreop[0], &randomPreop[rotateNum], &randomPreop[numberOfRandomPreop-1]);
```
The `end` iterator passed to `std::rotate` is `&randomPreop[numberOfRandomPreop-1]`, which points to the last element rather than one-past-the-end. This means the final element in the `randomPreop` array is never rotated — it stays fixed regardless of `rotateNum`. The correct end iterator is `&randomPreop[numberOfRandomPreop]`. This is a subtle off-by-one that produces a non-uniform rotation of the checklist questions.

**Fix:** Change the call to:
```cpp
std::rotate(&randomPreop[0], &randomPreop[rotateNum], &randomPreop[numberOfRandomPreop]);
```

---

**A03-9** · MEDIUM · `convert2UTC` has dead code and is effectively a stub

**Description:** `BackgroundWorker::convert2UTC` (backgroundworker.cpp lines 3060–3068) handles only the `"PDT"` timezone and falls through to `return time` for all others. A `//TODO: add other kernel build timezone here.` comment sits below an unreachable `else` branch. The only consumer is `getKernelBuildDate()`. In practice the function adds 7 hours only if the kernel was built in Pacific Daylight Time, producing a wrong UTC conversion for any other kernel build timezone (e.g., PST, EST, UTC). The `else` clause at line 3065 is always reached when the timezone is not PDT, making the `if/else` structure misleading.

**Fix:** Either expand the timezone table to cover all expected cases, or — preferably — parse the kernel build date with `QDateTime::fromString` using an explicit Qt timezone offset rather than a string abbreviation lookup. Remove the dead comment.

---

**A03-10** · MEDIUM · `CMD_RLY1` and `CMD_RLY2` contain unreachable `QueryCmd` response branches

**Description:** In `dispatchLeaderCmd`, both `CMD_RLY1` (lines 719–734) and `CMD_RLY2` (lines 736–750) first check `if (type == QueryCmd) return false;` at the top of each case, then unconditionally fall through to a second `if (type == QueryCmd)` block that formats and returns a response. The second `QueryCmd` check can never be reached because execution already returned false at the first check. This appears to be leftover code from a previous design that allowed querying the relay state.

**Fix:** Remove the dead `if (type == QueryCmd)` response blocks (lines 727–729 and 743–745) from both relay cases, or remove the early `return false` if querying is intentionally desired.

---

**A03-11** · LOW · Mixed type conventions: `uint8_t` used alongside `quint8` in `checklist.cpp`

**Description:** `Checklist::copyAllRandomPreop` (checklist.cpp line 229) uses the C stdint type `uint8_t` for `tempCtr` while all other integer variables throughout both checklist files use Qt's `quint8`, `quint16`, `quint32` types. This minor inconsistency suggests the function was added by a different author or copied from non-Qt code without normalisation.

**Fix:** Replace `uint8_t tempCtr = 0;` with `quint8 tempCtr = 0;` to maintain consistent Qt-style typing throughout the file.

---

**A03-12** · LOW · `query == true` comparison style inconsistency in `checkItem()`

**Description:** `Checklist::checkItem()` (checklist.cpp line 239) compares `if (query == true)` rather than the idiomatic `if (query)`. Every other boolean check throughout both files uses the idiomatic form. The `== true` comparison triggers a compiler warning with `-Wbool-compare` on some toolchains.

**Fix:** Change `if (query == true)` to `if (query)`.

---

**A03-13** · LOW · `convert2UTC` takes `QString` by value instead of const reference

**Description:** `BackgroundWorker::convert2UTC(QString tzone, quint64 time)` (backgroundworker.h line 118, backgroundworker.cpp line 3060) passes the timezone string by value. Since the string is not modified inside the function, passing by `const QString &` avoids an unnecessary heap allocation for the implicit copy.

**Fix:** Change the signature to `quint64 convert2UTC(const QString &tzone, quint64 time)`.

---

**A03-14** · LOW · Indentation inconsistency in `backgroundworker.cpp`

**Description:** Several locations mix tab and space indentation:
- Lines 1837–1838 (`case CMD_LANG:` block closing) use a tab character where the rest of the file uses 4-space indentation.
- Lines 2835 (`//PwmBacklight::setBrightness(10);`) uses a tab.
- `testGeofence()` body (lines 2472–2530) uses 12-space leading indentation rather than the 4-space baseline used everywhere else, with inconsistent intermediate levels.

These inconsistencies suggest the code was pasted from different sources without reformatting.

**Fix:** Run the file through the project's code formatter (clang-format or Qt Creator's auto-format) to normalise all indentation to 4 spaces.

---

**A03-15** · LOW · `OtaWorker::m_isRunning` is a `public` data member

**Description:** `OtaWorker::m_isRunning` (backgroundworker.h line 45) is declared `public` with the `m_` prefix that signals it should be a private member. It is accessed directly from `BackgroundWorker::updateSelf()` (backgroundworker.cpp line 2954) with `m_otaWorker->m_isRunning`, bypassing encapsulation. While the `m_` prefix convention for private members is used consistently everywhere else in the header, this member is intentionally (or accidentally) made public.

**Fix:** Either make `m_isRunning` private and add a public accessor method `bool isRunning() const { return m_isRunning; }`, or — if direct atomic access from the owning class is the intent — document the design decision explicitly.

---

**A03-16** · LOW · `handleNtpSynchronization` always aborts NTP regardless of interface direction

**Description:** `BackgroundWorker::handleNtpSynchronization()` (backgroundworker.cpp lines 3173–3191) contains:
```cpp
if (!newState || interface == EthWifi || interface == EthModem) {
    m_ntpSync->abortConnection();
}
```
Since `interface` can only ever be `EthModem` or `EthWifi`, the condition `interface == EthWifi || interface == EthModem` is always true; this means `m_ntpSync->abortConnection()` is called unconditionally on every invocation regardless of `newState`. The `!newState` sub-condition is therefore dead. This appears to be a logic error introduced when the function was refactored out of `ethernetStateChanged`.

**Fix:** Clarify the intent. If NTP should be aborted only when network goes down, change the condition to `if (!newState)`. If NTP should be restarted on every interface change (the behaviour below), the abort is correct but the comment and condition should be simplified to remove the confusing dead sub-clause.

---

## 3. Summary Table

| ID | Severity | Title |
|----|----------|-------|
| A03-1 | HIGH | `streamUncompress` uses shared `static` variable for cross-call state |
| A03-2 | HIGH | Dead debug function `dataTest()` compiled into production binary |
| A03-3 | HIGH | Unreachable `break` after `return true` in `dispatchLeaderCmd` |
| A03-4 | MEDIUM | Qt deprecated API: `QNetworkConfigurationManager` and `QRegExp` |
| A03-5 | MEDIUM | Large commented-out code blocks throughout both files |
| A03-6 | MEDIUM | `m_isShuffled` declared but never written or read |
| A03-7 | MEDIUM | `Checklist` constructor leaves `m_isShuffled` and array members uninitialised |
| A03-8 | MEDIUM | `shuffleChecklist()` rotate end-iterator is off by one |
| A03-9 | MEDIUM | `convert2UTC` is a stub with dead code and a misleading `else` branch |
| A03-10 | MEDIUM | Unreachable `QueryCmd` response branches in `CMD_RLY1` and `CMD_RLY2` |
| A03-11 | LOW | Mixed type conventions: `uint8_t` used alongside `quint8` in checklist.cpp |
| A03-12 | LOW | `query == true` comparison style inconsistency in `checkItem()` |
| A03-13 | LOW | `convert2UTC` takes `QString` by value instead of const reference |
| A03-14 | LOW | Indentation inconsistency (mixed tabs/spaces) in backgroundworker.cpp |
| A03-15 | LOW | `OtaWorker::m_isRunning` is a `public` data member with `m_` prefix |
| A03-16 | LOW | `handleNtpSynchronization` condition always aborts NTP; `!newState` sub-clause is dead |
# Pass 4 Agent A04 — Code Quality

**Audit run:** 2026-02-28-01
**Branch:** master
**Files reviewed:**
- `app/cigconfigs.h`
- `app/crctable.cpp`
- `app/driverlist.h`
- `app/driverlist.cpp`

---

## Reading Evidence

### `app/cigconfigs.h`

**Module:** Global configuration header — no class, namespace `CIGCONF` wraps enums and structs.

**Functions/methods defined:** None (header-only, no functions).

**Macros defined (global scope, lines 8–77):**

| Macro | Line |
|---|---|
| `LFF_VERSION` | 8 |
| `SFF_VERSION` | 9 |
| `UFF_VERSION` | 10 |
| `ENG_VERSION` | 11 |
| `F_BUILD` | 12 |
| `C_BUILD` | 13 |
| `BROADCASTMSG_TEXT_LEN` | 15 |
| `GMTP_ID_LEN` | 17 |
| `GMTP_SERVER_CNT` | 18 |
| `SERVER_ADDR_LEN` | 19 |
| `MODEM_DIAL_NUMBER_LEN` | 20 |
| `MODEM_APN_LEN` | 21 |
| `MODEM_APN_USER_LEN` | 22 |
| `MODEM_ICCID_LEN` | 23 |
| `MODEM_APN_PASSWORD_LEN` | 24 |
| `MAX_POLY_POINTS` | 26 |
| `MAX_POLY` | 27 |
| `CHECKLIST_TIME_SLOTS` | 29 |
| `CHECKLIST_MAX_IDX` | 30 |
| `CHECKLIST_QUESTION_LEN` | 31 |
| `CHECKLIST_ITEM_SIZE` | 32 |
| `CHECKLIST_QUESTION_LEN_100` | 33 |
| `CHECKLIST_ITEM_SIZE_100` | 34 |
| `DRIVER_MAX_ID_IDX` | 36 |
| `MASTER_MAX_ID_IDX` | 37 |
| `SUPER_MAX_ID_IDX` | 38 |
| `TECH_MAX_ID_IDX` | 39 |
| `CAN_MAX_HW_PGN` | 42 |
| `CAN_MAX_PGN_IDX` | 43 |
| `CAN_MAX_SPN_IDX` | 44 |
| `CAN_MAX_LINK_IDX` | 45 |
| `CAN_MAX_ATT_IDX` | 46 |
| `CAN_ATT_NAME_LEN` | 47 |
| `CAN_MSG_TYPE` | 48 |
| `CAN_MSG_DLC` | 49 |
| `CAN_SIG_STATUS` | 50 |
| `ON_DEMAND_DURATION` | 53 |
| `WIFI_MAX_NETWORKS` | 56 |
| `WIFI_CONF_FILE` | 57 |
| `FILE_DRIVER_IDS` | 64 |
| `FILE_MASTER_IDS` | 65 |
| `FILE_SUPER_IDS` | 66 |
| `FILE_TECH_IDS` | 67 |
| `FILE_CHECKLIST` | 68 |
| `FILE_CHECKLIST_100` | 69 |
| `FILE_FLEETMS_FW` | 70 |
| `FILE_FLEETMS_FW_RD` | 71 |
| `FILE_LOGIN_SCREEN` | 72 |
| `FILE_LOGIN_SCREEN_RD` | 73 |
| `FILE_ONCEPERDAY_PREOP_IDS` | 74 |
| `DIR_GMTP_MSG` | 76 |
| `SHOW_ALL_MASTER_MENU` (inside namespace block) | 81 |

**Enums (all inside `namespace CIGCONF`):**

| Enum | Line |
|---|---|
| `MasterMenuOptions` | 83 |
| `PowerState` | 86 |
| `ConfigErrorCode` | 88 |
| `FtpErrorCode` | 90 |
| `LeaderCmdType` | 93 |
| `UnlockReasonScreen` | 95 |
| `RealImpact` | 97 |
| `DigitalInputMode` | 99 |
| `LeaderCmd` | 101 |
| `GmtpMessage` | 128 |
| `CheckReason` | 135 |
| `CheckResponses` | 136 |
| `ChecklistType` | 137 |
| `OnDemandCmdType` | 139 |
| `OnDemandCmdSrc` | 140 |
| `MaintLockedCode` | 142 |
| `ShowTimeFormat` | 150 |
| `BleExpansionDI` | 156 |
| `BleExpansionRelay` | 157 |
| `BleExpansionConnectionStatus` | 158 |
| `CanProtocol` | 160 |
| `CanAttributeType` | 162 |
| `WifiPosSource` | 171 |
| `CameraMode` | 173 |

**Structs (all inside `namespace CIGCONF`):**

| Struct | Line |
|---|---|
| `CanMsgLink` | 175 |
| `CanMsgPara` | 180 |
| `CanSigPara` | 188 |
| `CigCanConfig` | 195 |
| `BroadcastMessage` | 245 |
| `WifiNetwork` | 254 |
| `PreopDriverId` | 260 |
| `DriverId` | 265 |
| `MasterId` | 270 |
| `gpsPosStruct` | 276 |
| `polygonStruct` | 281 |
| `position` | 287 |
| `AccessPoint` | 295 |
| `CheckResponse` | 304 |

---

### `app/crctable.cpp`

**Module:** CRC lookup tables — no class, no header.

**Functions defined:** None.

**Constants defined:**

| Symbol | Type | Line |
|---|---|---|
| `crc32Table` | `const quint32[256]` | 6 |
| `crc16Table` | `const quint16[16]` | 41 |

**Forward declarations (lines 3–4):** Both arrays are forward-declared as `extern` before their definitions in the same translation unit.

---

### `app/driverlist.h`

**Class:** `DriverList` (line 9)

**Public methods declared:**

| Method | Line |
|---|---|
| `DriverList()` (constructor) | 12 |
| `readDriverIds()` | 14 |
| `readMasterIds()` | 15 |
| `readSuperIds()` | 16 |
| `readTechIds()` | 17 |
| `saveDriverIds()` | 18 |
| `saveMasterIds()` | 19 |
| `saveSuperIds()` | 20 |
| `saveTechIds()` | 21 |
| `readPreopDriverIds()` | 22 |
| `savePreopDriverIds()` | 23 |
| `driverIds() const` | 25 |
| `masterIds() const` | 26 |
| `superIds() const` | 27 |
| `techIds() const` | 28 |
| `preopDriverIds() const` | 29 |
| `driverId(int) const` | 31 |
| `masterId(int) const` | 32 |
| `masterIdById(quint64) const` | 33 |
| `superId(int) const` | 34 |
| `techId(int) const` | 35 |
| `setDriverId(int, quint64, QString)` | 37 |
| `setMasterId(int, quint64, quint8, QString)` | 38 |
| `setSuperId(int, quint64)` | 39 |
| `setTechId(int, quint64, QString)` | 40 |
| `containsDriverId(quint64) const` | 42 |
| `containsMasterId(quint64, quint8) const` | 50 |
| `containsSuperId(quint64) const` | 63 |
| `containsTechId(quint64) const` | 69 |
| `addDriverId(quint64, QString)` | 77 |
| `addSuperId(quint64)` | 78 |
| `addTechId(quint64, QString)` | 79 |
| `addPreopDriverId(quint64, quint32)` | 80 |
| `removeDriverId(quint64)` | 82 |
| `removeMasterId(quint64)` | 83 |
| `removeSuperId(quint64)` | 84 |
| `removeTechId(quint64)` | 85 |
| `clearDriverIds()` | 87 |
| `clearMasterIds()` | 88 |
| `clearSuperIds()` | 89 |
| `clearTechIds()` | 90 |
| `clearPreopDriverIds()` | 91 |
| `driverChecksum() const` | 93 |
| `masterChecksum() const` | 94 |
| `superChecksum() const` | 95 |
| `techChecksum() const` | 96 |
| `superIsEmpty()` | 98 |
| `getMasterIdIndex(quint64)` | 100 |
| `getDriverIdIndex(quint64)` | 101 |
| `getTechIdIndex(quint64)` | 102 |
| `getPreopDriverIdIndex(quint64)` | 103 |
| `getPreopDriverId(quint64)` | 104 |

**Private member variables:**

| Member | Line |
|---|---|
| `m_driverIds` (`QList<DriverId>`) | 108 |
| `m_masterIds` (`QList<MasterId>`) | 109 |
| `m_superIds` (`QList<quint64>`) | 110 |
| `m_techIds` (`QList<DriverId>`) | 111 |
| `m_preopDriverIds` (`QList<PreopDriverId>`) | 112 |
| `m_driverIdsDirty` (`bool`) | 113 |
| `m_masterIdsDirty` (`bool`) | 114 |
| `m_superIdsDirty` (`bool`) | 115 |
| `m_techIdsDirty` (`bool`) | 116 |
| `m_preopDriverDirty` (`bool`) | 117 |

---

### `app/driverlist.cpp`

**Functions/methods defined:**

| Method | Line |
|---|---|
| `DriverList::DriverList()` | 8 |
| `DriverList::readDriverIds()` | 16 |
| `DriverList::saveDriverIds()` | 45 |
| `DriverList::readMasterIds()` | 66 |
| `DriverList::saveMasterIds()` | 97 |
| `DriverList::readSuperIds()` | 120 |
| `DriverList::saveSuperIds()` | 136 |
| `DriverList::readTechIds()` | 155 |
| `DriverList::saveTechIds()` | 184 |
| `DriverList::readPreopDriverIds()` | 205 |
| `DriverList::savePreopDriverIds()` | 233 |
| `DriverList::setDriverId(int, quint64, QString)` | 267 |
| `DriverList::setMasterId(int, quint64, quint8, QString)` | 285 |
| `DriverList::setSuperId(int, quint64)` | 304 |
| `DriverList::setTechId(int, quint64, QString)` | 317 |
| `DriverList::getDriverIdIndex(quint64)` | 335 |
| `DriverList::addDriverId(quint64, QString)` | 344 |
| `DriverList::getMasterIdIndex(quint64)` | 370 |
| `DriverList::addSuperId(quint64)` | 379 |
| `DriverList::getTechIdIndex(quint64)` | 395 |
| `DriverList::addTechId(quint64, QString)` | 404 |
| `DriverList::getPreopDriverIdIndex(quint64)` | 430 |
| `DriverList::getPreopDriverId(quint64)` | 445 |
| `DriverList::addPreopDriverId(quint64, quint32)` | 455 |
| `DriverList::removeDriverId(quint64)` | 489 |
| `DriverList::removeMasterId(quint64)` | 511 |
| `DriverList::removeSuperId(quint64)` | 529 |
| `DriverList::removeTechId(quint64)` | 543 |
| `DriverList::clearDriverIds()` | 560 |
| `DriverList::clearMasterIds()` | 566 |
| `DriverList::clearSuperIds()` | 572 |
| `DriverList::clearTechIds()` | 578 |
| `DriverList::clearPreopDriverIds()` | 584 |
| `DriverList::driverChecksum() const` | 590 |
| `DriverList::masterChecksum() const` | 601 |
| `DriverList::superChecksum() const` | 613 |
| `DriverList::techChecksum() const` | 624 |
| `DriverList::superIsEmpty()` | 635 |
| `DriverList::masterIdById(quint64) const` | 645 |

---

## Findings

---

**A04-1** · HIGH · `crctable.cpp` has no corresponding header file

**Description:** `crctable.cpp` declares and defines `crc32Table` and `crc16Table` but there is no `crctable.h`. Both consumers (`globalconfigs.cpp` and `backgroundworker.cpp`) repeat `extern const quint32 crc32Table[]` and `extern const quint16 crc16Table[]` declarations inline inside their function bodies. This is a leaky abstraction: the declaration contract is implicit and scattered, making it trivially easy for a future caller to declare the wrong type, wrong element count, or wrong linkage. If the table type ever changes, no compiler error will be produced at the declaration sites.

**Fix:** Create `app/crctable.h` that declares both arrays with `extern const`, include it in `crctable.cpp`, `globalconfigs.cpp`, and `backgroundworker.cpp`, and remove the in-function `extern` declarations.

---

**A04-2** · HIGH · `#define SHOW_ALL_MASTER_MENU 255` placed inside a namespace block

**Description:** At line 81 of `cigconfigs.h`, a `#define` is written between the `namespace CIGCONF {` opening brace and the first `enum`. C preprocessor macros are not scoped by namespaces; the macro is effectively global and the namespace placement gives a false impression that it is namespaced. The value 255 duplicates `UnassignedMasterMenu = 255` from the `MasterMenuOptions` enum defined two lines later, creating two symbols with the same semantic meaning. Searches in the codebase find `SHOW_ALL_MASTER_MENU` used only inside `cigconfigs.h` itself (it is not referenced in any other `.cpp` or `.h` outside this file), confirming it is dead.

**Fix:** Remove the macro. If the value is genuinely needed, add a `ShowAllMasterMenu = 255` enumerator to `MasterMenuOptions` and use that enumerator.

---

**A04-3** · HIGH · `LeaderCmd` enum ordering broken — `CMD_UNKNOWN = 0xff` is not the last enumerator

**Description:** In `cigconfigs.h` lines 101–126, `CMD_UNKNOWN = 0xff` is assigned at line 120, but at least 25 additional enumerators (`CMD_TGFNCE`, `CMD_SCRSAV`, ..., `CMD_CAMERAFLIP`) are appended after it on lines 121–125. Because `CMD_UNKNOWN` uses an explicit value `0xff` (255) and the subsequent enumerators continue numerically from 256 onward, the enumerators after `CMD_UNKNOWN` silently overflow an `int` in the range 256–280. More critically, any `switch` or comparison that uses `CMD_UNKNOWN` as a sentinel "unknown command" value is broken: legitimate commands added after `CMD_UNKNOWN` will never match the sentinel and will be misrouted as unknown. This is a protocol/logic defect introduced by appending new commands without repositioning `CMD_UNKNOWN`.

**Fix:** Move `CMD_UNKNOWN = 0xff` to the end of the enum (or use it only as a runtime initializer, not as an enum member). Assign the newly added commands before `CMD_UNKNOWN` in the sequential value range, or use a separate constant for the sentinel so that the numeric gap cannot arise.

---

**A04-4** · MEDIUM · `CanAttributeType` contains two `Last`-style sentinel enumerators

**Description:** `cigconfigs.h` lines 162–169 define `CanAttributeType` with both `CanAttributeLast` (value 1) and `CanAttributeLast2` (value 5). Having two sentinels with names implying "the last value" is contradictory and confusing. A search confirms `CanAttributeLast2` appears only in `cigconfigs.h` and in CAN handler files, but the naming conveys no clear semantic difference. This is a dead-code / naming smell that indicates a past extension was done without cleaning up the original sentinel.

**Fix:** Rename or remove the older sentinel. If both are genuinely needed as range boundaries for separate sub-ranges, rename them with explicit meaning (e.g., `CanAttributeBasicLast`, `CanAttributeExtendedLast`).

---

**A04-5** · MEDIUM · `CigCanConfig` contains a large anonymous union with many `unused` members that hold real layout

**Description:** `cigconfigs.h` lines 207–243 define an anonymous union inside `CigCanConfig`. The first union member is an array of structs with fields all named `unused3` through `unused10`. This structure is clearly load-bearing for the binary layout of the config block — its presence controls the size and alignment of the union — but the naming actively conceals this. Any engineer reading the code may assume the fields can be freely removed or reordered, leading to silent config corruption. The `void *unused2` pointer at line 192 inside `CanSigPara` carries a comment "set to nullptr", making it a permanent padding placeholder with no type safety.

**Fix:** Replace `unusedN` field names with descriptive names prefixed `_reserved` (e.g., `_reserved_attLegacy`) and add a `static_assert` on the size of `CigCanConfig` to catch accidental layout changes. Replace `void *unused2` with an explicit `quint64 _reserved` or a suitably-typed field.

---

**A04-6** · MEDIUM · Hardcoded Linux filesystem paths in a Qt-targeting header

**Description:** `cigconfigs.h` lines 57 and 64–76 contain hardcoded absolute POSIX paths such as `/etc/wpa_supplicant.conf`, `/home/dlist.txt`, `/mnt/sd/FleetIQ360App`, and `/mnt/ramdisk/login.png`. These paths encode the exact production filesystem layout of the embedded Linux target directly into a shared header. Any build for a development host, unit-test harness, or future hardware revision will silently use wrong paths unless all callers add their own overrides. The paths are also split across two logical groups (modem/network paths and file paths) with no clear separation.

**Fix:** Move filesystem path configuration to a runtime-configurable source (e.g., a config singleton, a compile-time platform layer, or at minimum a separate `platform_paths.h` that is not included in unit-test builds). If the paths must remain as macros, isolate them in a dedicated platform header that is excluded from host-side test compilations via a feature flag.

---

**A04-7** · MEDIUM · `getPreopDriverIdIndex` contains a spurious function-declaration statement

**Description:** `driverlist.cpp` line 433 reads:
```cpp
CIGCONF::PreopDriverId getPreopDriverId(quint64 id);
```
This is a local function declaration placed inside the body of `DriverList::getPreopDriverIdIndex`. It does not call the function and has no effect; the compiler treats it as a forward declaration of a free function and immediately discards it. The statement appears to be copy-paste debris from an earlier draft. It compiles without error only because function declarations are syntactically valid as statements in C++, but it is entirely dead code and obscures the intent of the surrounding loop.

**Fix:** Remove line 433 from `getPreopDriverIdIndex`.

---

**A04-8** · MEDIUM · Commented-out debug block in `addPreopDriverId`

**Description:** `driverlist.cpp` lines 473–483 contain a `#if 0` block that includes a `qDebug()` debug dump using `ByteArray::asprintf`. This dead block was clearly debug scaffolding. The reference to `ByteArray::asprintf` (a non-standard helper) also means the block cannot compile as-is if the `#if 0` were ever removed, making it unmaintainable dead code.

**Fix:** Remove the `#if 0` block entirely. If the debug output is needed, use a proper `qCDebug` category guarded by a logging level rather than a preprocessor block.

---

**A04-9** · MEDIUM · `savePreopDriverIds` uses `QFile` instead of `QSaveFile`, unlike all other save methods

**Description:** All other `save*Ids` methods in `driverlist.cpp` (lines 45–203) use `QSaveFile`, which provides atomic write-then-rename semantics, protecting against file corruption on power loss. `savePreopDriverIds` (line 233) uses a plain `QFile`, meaning a power interruption during the write leaves a truncated or partial file. This is inconsistent with the established pattern in the same class and represents a reliability regression specifically for the once-per-day preop ID list, which is the newest feature.

**Fix:** Replace `QFile` with `QSaveFile` in `savePreopDriverIds` and call `file.commit()` as done in the other save methods.

---

**A04-10** · MEDIUM · `savePreopDriverIds` uses deprecated `endl` manipulator

**Description:** `driverlist.cpp` line 260 uses `endl` with `QTextStream`. In Qt 5.14+, `Qt::endl` is the preferred form and the bare `endl` form (which resolves to `std::endl`) causes an implicit flush on every line, degrading write performance and mixing std and Qt stream semantics. All other save methods write raw `QByteArray` without `QTextStream`, making this the only method using the Qt text stream API and `endl`.

**Fix:** Replace `endl` with `Qt::endl`, or better, rewrite `savePreopDriverIds` to use `QByteArray` accumulation consistent with the other save methods, eliminating the `QTextStream` dependency entirely.

---

**A04-11** · MEDIUM · `m_preopDriverDirty` not initialised in constructor

**Description:** `DriverList::DriverList()` (`driverlist.cpp` line 8) initialises `m_driverIdsDirty`, `m_masterIdsDirty`, `m_superIdsDirty`, and `m_techIdsDirty` to `false` in the member-initialiser list. `m_preopDriverDirty` (declared at `driverlist.h` line 117) is omitted from the initialiser list. Its value at construction time is indeterminate (undefined behaviour in C++). If `savePreopDriverIds` is called before any mutation, the dirty-flag check at line 236 may evaluate to `true` on an uninitialised bool, causing a spurious write.

**Fix:** Add `m_preopDriverDirty(false)` to the constructor initialiser list.

---

**A04-12** · LOW · `driverlist.h` unnecessarily includes `<QDebug>`

**Description:** `driverlist.h` line 7 includes `<QDebug>`. No method in the header uses `qDebug()` or any debug type. The include is unused in the header and is pulled in transitively by every translation unit that includes `driverlist.h`. `<QDebug>` is a heavyweight Qt header.

**Fix:** Remove `#include <QDebug>` from `driverlist.h`. If debug output is needed in `driverlist.cpp`, include `<QDebug>` there instead.

---

**A04-13** · LOW · `containsDriverId` / `containsMasterId` / `containsSuperId` / `containsTechId` use a ternary that is always true when the loop body is reached

**Description:** Each `contains*` method (e.g., `driverlist.h` line 45) ends with `return id != 1 ? true : false;` after finding a matching entry. The expression `id != 1 ? true : false` is exactly `id != 1`. More importantly, the logic appears designed to exclude the sentinel ID value `1`, yet returning `false` when a matching entry exists with `id == 1` is surprising and undocumented. There is no comment explaining why `id == 1` is special. The ternary form also triggers `-Wlogical-op` or style warnings on some compilers.

**Fix:** Replace the ternary with `return (id != 1);` and add a comment explaining the special-case meaning of ID value 1 (e.g., "id 1 is reserved as a null/unset sentinel"). If id 1 is never expected in the lists, add an assertion.

---

**A04-14** · LOW · `driverChecksum` / `masterChecksum` / `superChecksum` / `techChecksum` use C-style casts

**Description:** `driverlist.cpp` lines 594–595, 604–607, 617–618, 627–628 use `(quint32)d.id` and `(quint32)(d.id >> 32)` C-style casts to truncate `quint64` values. These are semantically `static_cast<quint32>(...)` but the C-style cast form suppresses compiler warnings and bypasses the type-system checks that `static_cast` preserves.

**Fix:** Replace all `(quint32)` C-style casts in the checksum methods with `static_cast<quint32>(...)`.

---

**A04-15** · LOW · `crctable.cpp` forward-declares its own definitions

**Description:** `crctable.cpp` lines 3–4 contain:
```cpp
extern const quint32 crc32Table[];
extern const quint16 crc16Table[];
```
immediately before defining those same arrays. This self-referential forward declaration adds no value (the definitions are visible at link time regardless) and appears to be a workaround for the absence of a proper header. If the array sizes or types ever diverge between declaration and definition, the compiler may not catch the mismatch.

**Fix:** Remove the forward declarations from `crctable.cpp` once a proper `crctable.h` header is created (see A04-1). The definitions alone are sufficient within the translation unit.

---

**A04-16** · LOW · `OnDemandCmdType` enum has redundant explicit zero value

**Description:** `cigconfigs.h` line 139:
```cpp
enum OnDemandCmdType {OnDemandStart, OnDemandExtend = 1, OnDemandEnd = 2};
```
`OnDemandStart` is implicitly 0, so no explicit value is needed. `OnDemandExtend = 1` is also redundant since it is the sequential value. Only `OnDemandEnd = 2` would be needed if the intent was to emphasise the values. The inconsistency across the three enumerators (implicit, explicit-same, explicit-same) is a style defect.

**Fix:** Either remove all explicit values (`{OnDemandStart, OnDemandExtend, OnDemandEnd}`) if the values are not protocol-significant, or add explicit values to all three enumerators for clarity.

---

**A04-17** · INFO · `DriverId` struct is reused for tech IDs instead of having a dedicated type

**Description:** `cigconfigs.h` line 265 defines `DriverId` and it is used for both driver and tech ID lists (`m_driverIds`, `m_techIds`). This means the type name in stack traces, debug output, and future refactoring provides no distinction between driver entries and tech entries. It is a minor semantic clarity issue.

**Fix:** Consider a `using TechId = DriverId;` alias or a dedicated `TechId` struct to improve readability and enable future divergence of the two types.

---

## Summary Table

| ID | Severity | Title | File(s) |
|---|---|---|---|
| A04-1 | HIGH | `crctable.cpp` has no header file | `crctable.cpp` |
| A04-2 | HIGH | `#define SHOW_ALL_MASTER_MENU` inside namespace / dead code | `cigconfigs.h:81` |
| A04-3 | HIGH | `CMD_UNKNOWN = 0xff` breaks `LeaderCmd` enum ordering | `cigconfigs.h:120` |
| A04-4 | MEDIUM | `CanAttributeType` has two confusingly-named sentinel enumerators | `cigconfigs.h:164,169` |
| A04-5 | MEDIUM | `CigCanConfig` has layout-critical fields named `unusedN` | `cigconfigs.h:205-242` |
| A04-6 | MEDIUM | Hardcoded Linux filesystem paths in shared header | `cigconfigs.h:57,64-76` |
| A04-7 | MEDIUM | Spurious function-declaration statement inside `getPreopDriverIdIndex` | `driverlist.cpp:433` |
| A04-8 | MEDIUM | Commented-out `#if 0` debug block in `addPreopDriverId` | `driverlist.cpp:473-483` |
| A04-9 | MEDIUM | `savePreopDriverIds` uses `QFile` instead of `QSaveFile` | `driverlist.cpp:244` |
| A04-10 | MEDIUM | `savePreopDriverIds` uses deprecated `endl` | `driverlist.cpp:260` |
| A04-11 | MEDIUM | `m_preopDriverDirty` not initialised in constructor | `driverlist.cpp:8` |
| A04-12 | LOW | `<QDebug>` unnecessarily included in `driverlist.h` | `driverlist.h:7` |
| A04-13 | LOW | `contains*` methods use verbose ternary with undocumented special case for `id == 1` | `driverlist.h:42-75` |
| A04-14 | LOW | C-style casts in checksum methods | `driverlist.cpp:594-628` |
| A04-15 | LOW | `crctable.cpp` self-forward-declares its own definitions | `crctable.cpp:3-4` |
| A04-16 | LOW | `OnDemandCmdType` has inconsistent explicit values | `cigconfigs.h:139` |
| A04-17 | INFO | `DriverId` struct reused for tech IDs without type alias | `cigconfigs.h:265` |
# Pass 4 Agent A05 — Code Quality

**Audit run:** 2026-02-28-01
**Branch:** master
**Assigned files:**
- `app/globalconfigs.h`
- `app/globalconfigs.cpp`
- `app/globalconfigsfilemanager.h` / `.cpp` — **FILE NOT FOUND** (confirmed absent, see Finding A05-1)

---

## 1. Reading Evidence

### 1.1 `app/globalconfigs.h`

**Class:** `GlobalConfigs` (inherits `QObject`, decorated with `Q_OBJECT`)

**Macro defined in this file:**
| Macro | Line | Value |
|---|---|---|
| `gCfg` | 13 | `GlobalConfigs::instance()` |

**Public methods / inline accessors (all defined in the header):**

| Method | Line |
|---|---|
| `explicit GlobalConfigs(QObject *parent = nullptr)` | 20 |
| `static GlobalConfigs *instance()` | 21 |
| `static quint32 crc32(const void *buf, int len)` | 22 |
| `void readConfigs()` | 24 |
| `void saveConfigs()` | 25 |
| `void saveOpdDriverList()` | 26 |
| `void resetConfigs(bool resetAll = false)` | 27 |
| `quint32 keepAliveTime() const` | 30 |
| `bool setKeepAliveTime(quint32 time)` | 31 |
| `quint32 shutdownTime() const` | 40 |
| `bool setShutdownTime(quint32 time)` | 41 |
| `QByteArray gmtpId() const` | 50 |
| `bool setGmtpId(const QByteArray &id)` | 51 |
| `CIGCONF::MaintLockedCode maintCode() const` | 60 |
| `quint64 maintDriverId() const` | 61 |
| `quint32 maintTimestamp() const` | 62 |
| `bool setMaintCode(CIGCONF::MaintLockedCode code)` | 64 |
| `quint64 unlockId() const` | 81 |
| `bool setUnlockId(quint64 id)` | 82 |
| `QByteArray dialNumber() const` | 87 |
| `bool setDialNumber(const QByteArray &number)` | 88 |
| `QByteArray apn() const` | 97 |
| `bool setApn(const QByteArray &apn)` | 98 |
| `QByteArray apnUser() const` | 107 |
| `bool setApnUser(const QByteArray &user)` | 108 |
| `QByteArray apnPassword() const` | 117 |
| `bool setApnPassword(const QByteArray &password)` | 118 |
| `QByteArray gmtpServerAddress(int index) const` | 127 |
| `bool setGmtpServerAddress(int index, const QByteArray &addr)` | 128 |
| `quint16 gmtpServerPort(int index) const` | 137 |
| `bool setGmtpServerPort(int index, quint16 port)` | 138 |
| `quint64 expansionModMac() const` | 147 |
| `bool setExpansionModMac(quint64 mac)` | 148 |
| `void resetSimCardID()` | 157 |
| `QByteArray getSimCardID() const` | 158 |
| `bool setSimCardID(const QByteArray &iccid)` | 159 |
| `QList<CIGCONF::DriverId> driverIds() const` | 168 |
| `QList<CIGCONF::MasterId> masterIds() const` | 169 |
| `QList<quint64> superIds() const` | 170 |
| `QList<CIGCONF::DriverId> techIds() const` | 171 |
| `QList<CIGCONF::PreopDriverId> preopDriverIds() const` | 172 |
| `CIGCONF::DriverId driverId(int index) const` | 174 |
| `CIGCONF::MasterId masterId(int index) const` | 175 |
| `CIGCONF::MasterId masterIdById(quint64 id) const` | 176 |
| `quint64 superId(int index) const` | 177 |
| `CIGCONF::DriverId techId(int index) const` | 178 |
| `bool setDriverId(int index, quint64 id, QString name)` | 180 |
| `bool setMasterId(int index, quint64 id, quint8 option, QString name)` | 181 |
| `bool setSuperId(int index, quint64 id)` | 182 |
| `bool setTechId(int index, quint64 id, QString name)` | 183 |
| `bool containsDriverId(quint64 id) const` | 185 |
| `bool containsMasterId(quint64 id, quint8 permissions=0) const` | 186 |
| `bool containsSuperId(quint64 id) const` | 187 |
| `bool containsTechId(quint64 id) const` | 188 |
| `bool addDriverId(quint64 id, QString name)` | 190 |
| `bool addSuperId(quint64 id)` | 191 |
| `bool addTechId(quint64 id, QString name)` | 192 |
| `bool addPreopDriverId(quint64 id, quint32 timestamp)` | 193 |
| `bool removeDriverId(quint64 id)` | 195 |
| `bool removeMasterId(quint64 id)` | 196 |
| `bool removeSuperId(quint64 id)` | 197 |
| `bool removeTechId(quint64 id)` | 198 |
| `void clearDriverIds()` | 200 |
| `void clearMasterIds()` | 201 |
| `void clearSuperIds()` | 202 |
| `void clearTechIds()` | 203 |
| `void clearPreopDriverIds()` | 204 |
| `int getMasterIdIndex(quint64 id)` | 206 |
| `int getDriverIdIndex(quint64 id)` | 207 |
| `int getTechIdIndex(quint64 id)` | 208 |
| `int getPreopDriverIdIndex(quint64 id)` | 209 |
| `CIGCONF::PreopDriverId getPreopDriverId(quint64 id)` | 210 |
| `bool preopOncePerDayEn() const` | 212 |
| `bool setPreopOncePerDayEn(bool en)` | 213 |
| `QString getDriverName(quint64 id)` | 220 |
| `bool superIsEmpty()` | 233 |
| `quint8 digitalInputMode1() const` | 235 |
| `quint8 digitalInputMode2() const` | 236 |
| `quint8 digitalInputMode3() const` | 237 |
| `quint8 digitalInputMode4() const` | 238 |
| `void setDigInputMode(quint8, quint8, quint8, quint8)` | 240 |
| `quint32 seenDebounceTime() const` | 248 |
| `quint32 seenHoldTime() const` | 249 |
| `bool setSeenParam(quint32 debounce, quint32 hTime)` | 250 |
| `quint8 convorStatus() const` | 257 |
| `quint64 convorId() const` | 258 |
| `bool setConvor(quint8 convor, quint64 id)` | 259 |
| `quint8 fullLockoutEnable() const` | 270 |
| `bool setFullLockoutEnable(quint8 lockOutEnable)` | 271 |
| `quint32 fullLockoutTimeout() const` | 277 |
| `bool setFullLockoutTimeout(quint32 lockOutTimeout)` | 278 |
| `quint8 unlkScr() const` | 284 |
| `bool setUnlkScr(quint8 scr)` | 285 |
| `quint8 scrSavMode() const` | 294 |
| `bool setScrSavMode(quint8 mode)` | 295 |
| `quint16 checkTimeSlot(int index) const` | 304 |
| `bool setCheckTimeSlot(int index, quint16 hm)` | 305 |
| `quint16 checklistTimeout() const` | 314 |
| `bool setChecklistTimeout(quint16 time)` | 315 |
| `quint64 lastTimeServerUpdate() const` | 324 |
| `bool setLastTimeServerUpdate(quint64 ts)` | 325 |
| `qint64 timeError() const` | 330 |
| `bool setTimeError(qint64 ts)` | 331 |
| `quint32 lastPreopOncePerDayTimestamp() const` | 336 |
| `bool setlastPreopOncePerDayTimestamp(quint32 ts)` | 337 |
| `quint32 lastCheckTimestamp() const` | 344 |
| `bool setLastCheckTimestamp(quint32 ts)` | 345 |
| `quint64 lastCheckDriverId() const` | 352 |
| `bool setLastCheck(quint64 id, quint32 ts)` | 353 |
| `void clearChecklist()` | 361 |
| `Checklist::CheckItem checkItem(int index, bool query = false)` | 362 |
| `bool setCheckItem(int index, const Checklist::CheckItem item)` | 363 |
| `int nextValidCheckItemIndex(int start = 0, bool queryOrigList = false)` | 367 |
| `void shuffleChecklist()` | 374 |
| `quint8 preopRandom() const` | 375 |
| `bool setPreopRandom(quint8 isRandom)` | 376 |
| `quint32 shockThreshold() const` | 382 |
| `bool setShockThreshold(quint32 data)` | 383 |
| `quint32 shockRedImpact() const` | 389 |
| `bool setShockRedImpact(quint32 data)` | 390 |
| `quint32 shockPeriod() const` | 396 |
| `bool setShockPeriod(quint32 data)` | 397 |
| `quint32 shockTimer() const` | 403 |
| `bool setShockTimer(quint32 data)` | 404 |
| `qint16 timeZoneInMinutes() const` | 410 |
| `bool setTimeZoneInMinutes(qint16 zone)` | 411 |
| `QByteArray timeServerAddress() const` | 419 |
| `bool setTimeServerAddress(const QByteArray &addr)` | 420 |
| `quint32 gpsUpdateTime() const` | 429 |
| `bool setGpsUpdateTime(quint32 time)` | 430 |
| `qint16 gpsDistanceMark() const` | 439 |
| `bool setGpsDistanceMark(qint16 mark)` | 440 |
| `quint16 satNum() const` | 449 |
| `bool setSatNum(quint16 n)` | 450 |
| `quint16 idleTimeout() const` | 459 |
| `bool setIdleTimeout(quint16 time)` | 460 |
| `quint16 getGmtpWaitTimeout() const` | 466 |
| `bool setGmtpWaitTimeout(quint16 time)` | 467 |
| `bool idleInputPolarity() const` | 473 |
| `bool setIdleInputPolarity(bool high)` | 474 |
| `quint8 idleInputSource() const` | 480 |
| `bool setIdleInputSource(quint8 src)` | 481 |
| `CIGCONF::polygonStruct polygon(int n) const` | 490 |
| `quint8 polygonNPoints(int n) const` | 492 |
| `bool setPolygonNPoints(int n, quint8 vect)` | 493 |
| `quint32 polygonLatitude(int n, int vect) const` | 502 |
| `bool setPolygonLatitude(int n, int vect, quint32 lat)` | 503 |
| `quint32 polygonLongitude(int n, int vect) const` | 512 |
| `bool setPolygonLongitude(int n, int vect, quint32 lon)` | 513 |
| `quint32 configVersion() const` | 524 |
| `quint8 backlight() const` | 526 |
| `quint32 checksum() const` | 527 |
| `CIGCONF::ConfigErrorCode configErrorCode() const` | 529 |
| `void readPreopDriverIds()` | 531 |
| `void readDriverIds()` | 532 |
| `void readMasterIds()` | 533 |
| `void readSuperIds()` | 534 |
| `void readTechIds()` | 535 |
| `void readChecklist()` | 536 |
| `quint32 driverChecksum() const` | 537 |
| `quint32 masterChecksum() const` | 538 |
| `quint32 superChecksum() const` | 539 |
| `quint32 questionChecksum() const` | 540 |
| `quint32 timestamp() const` | 542 |
| `quint32 localTimestamp() const` | 543 |
| `QDateTime localTime() const` | 545 |
| `quint64 clockTime() const` | 547 |
| `QString preopCommentString() const` | 557 |
| `void setPreopCommentString(QString msg)` | 558 |
| `QString UnlkReasonString() const` | 560 |
| `void setUnlkReasonString(QString msg)` | 561 |
| `CIGCONF::RealImpact UnlkOption() const` | 563 |
| `void setUnlkOption(CIGCONF::RealImpact option)` | 564 |
| `quint64 currentDriverId() const` | 566 |
| `void setCurrentDriverId(quint64 id)` | 567 |
| `quint64 fwVersion()` | 569 |
| `QString fwVersionString()` | 570 |
| `quint32 onDemandStartTime() const` | 573 |
| `quint32 onDemandEndTime() const` | 574 |
| `quint64 onDemandSmId() const` | 575 |
| `void setOnDemand(quint32 start, quint32 end, quint64 id)` | 577 |
| `void clearOnDemand()` | 583 |
| `bool onDemandActive()` | 585 |
| `bool onDemandVehicleEnabled()` | 586 |
| `bool setWifiNetwork(quint32 index, const QByteArray &ssid, const QByteArray &pw)` | 588 |
| `CIGCONF::WifiNetwork wifiNetwork(quint32 index) const` | 589 |
| `bool setWifiCountry(const QByteArray &country)` | 591 |
| `QByteArray wifiCountry() const` | 592 |
| `void clearWifiConfig()` | 594 |
| `quint8 wifiPos()` | 596 |
| `quint16 wifiPosInterval()` | 597 |
| `CIGCONF::WifiPosSource wifiPosSource()` | 598 |
| `bool setWifiPos(const quint8 n, const quint16 interval, const CIGCONF::WifiPosSource src)` | 599 |
| `bool isRs232AccessoryActive()` | 606 |
| `qint16 debugMsg() const` | 608 |
| `void setDebugMsg(qint16 n)` | 609 |
| `qint16 debugSpn() const` | 611 |
| `void setDebugSpn(qint16 n)` | 612 |
| `quint32 geofenceState() const` | 614 |
| `void setGeofenceState(quint32 state)` | 615 |
| `quint8 showDriverName() const` | 617 |
| `bool setShowDriverName(quint8 show)` | 618 |
| `bool GPSMsgLogEn() const` | 624 |
| `void setGPSMsgLogEn(bool en)` | 625 |
| `quint8 showPreopComment() const` | 630 |
| `void setShowPreopComment(quint8 show)` | 631 |
| `quint8 amberImpactAlertActive() const` | 636 |
| `void setAmberImpactAlertActive(quint8 state)` | 637 |
| `quint8 idleLockout() const` | 642 |
| `bool setIdleLockout(quint8 en)` | 643 |
| `quint8 showPreopSummary() const` | 649 |
| `void setShowPreopSummary(quint8 show)` | 650 |
| `quint8 unlockMode() const` | 655 |
| `void setUnlockMode(quint8 mode)` | 656 |
| `quint8 forceChecklist() const` | 661 |
| `bool setForceChecklist(quint8 force)` | 662 |
| `quint8 showTime() const` | 669 |
| `void setShowTime(quint8 format)` | 670 |
| `quint8 vdiMode() const` | 675 |
| `void setVdiMode(quint8 mode)` | 676 |
| `CIGCONF::CameraMode cameraMode() const` | 681 |
| `void setCameraMode(CIGCONF::CameraMode mode)` | 682 |
| `quint8 cameraFlip() const` | 687 |
| `void setCameraFlip(quint8 flip)` | 688 |
| `QByteArray lastSessionDriver() const` | 693 |
| `QByteArray lastSessionStart() const` | 694 |
| `QByteArray lastSessionEnd() const` | 695 |
| `void setLastSessionDriver(const QByteArray& driver)` | 696 |
| `void setLastSessionStart(const QByteArray& start)` | 700 |
| `void setLastSessionEnd(const QByteArray& end)` | 704 |

**Signals:**
| Signal | Line |
|---|---|
| `superListChanged(bool empty)` | 710 |
| `convorStatusChanged()` | 711 |
| `preopOncePerDayStatusChanged()` | 712 |

**Private methods:**
| Method | Line |
|---|---|
| `bool readStaticConfig()` | 771 |
| `void saveStaticConfig()` | 772 |
| `void readDynamicConfig()` | 774 |
| `void saveDynamicConfig()` | 775 |
| `void readOdConfig()` | 777 |
| `void saveOdConfig()` | 778 |
| `void readVORConfig()` | 785 |
| `void saveVORConfig()` | 786 |
| `void readGeofenceConfig()` | 816 |
| `void saveGeofenceConfig()` | 817 |

**Private structs (nested / file-local):**
| Name | Lines |
|---|---|
| `ConfigsData` | 715–758 |
| `ConfigsDataExt` | 760–762 |
| `OnDemandData` | 764–769 |
| `ConvorData` | 780–783 |
| `DigitalInputCfg` | 788–793 |
| `FullLockoutData` | 835–838 |

**Private member variables:**
`m_configs`, `m_configsExt`, `m_odConfig`, `m_driverList`, `m_checklist`, `m_configErrorCode`, `m_VORConfig`, `m_dINConfig`, `m_currentDriverId`, `m_unlockId`, `m_lastTimeServerUpdate`, `m_timeError`, `m_unlkMessage`, `m_unlkOption`, `m_gpsDistanceMark`, `m_satNum`, `m_polygon[]`, `m_screenSaverMode`, `gmtpWaitTimeout`, `m_networks`, `m_country`, `m_wifiPos`, `m_wifiPosInterval`, `m_wifiPosSource`, `m_fmsDirty`, `m_dynDirty`, `m_gfnceDirty`, `m_debugMsg`, `m_debugSpn`, `m_geofenceState`, `m_convorId`, `m_seenDebounceTime`, `m_seenHoldTime`, `m_fullLockout`, `m_preopComment`, `m_preopRandom`, `m_showDriverName`, `m_isGPSMsgLogEn`, `m_showPreopComment`, `m_amberImpactAlertState`, `simICCID[]`, `m_preopOncePerDayEn`, `m_idleLockoutEnabled`, `m_showPreopSummary`, `m_unlockMode`, `m_forceChecklist`, `m_showTime`, `m_vdiMode`, `m_cameraMode`, `m_cameraFlip`, `m_lastSessionDriver`, `m_lastSessionStart`, `m_lastSessionEnd`

---

### 1.2 `app/globalconfigs.cpp`

**Functions defined (with line numbers):**

| Function | Line |
|---|---|
| `GlobalConfigs::GlobalConfigs(QObject *parent)` | 26 |
| `GlobalConfigs *GlobalConfigs::instance()` | 33 |
| `quint32 GlobalConfigs::crc32(const void *data, int len)` | 38 |
| `void GlobalConfigs::readConfigs()` | 51 |
| `void GlobalConfigs::saveConfigs()` | 110 |
| `void GlobalConfigs::saveOpdDriverList()` | 126 |
| `void GlobalConfigs::resetConfigs(bool resetAll)` | 131 |
| `bool GlobalConfigs::readStaticConfig()` | 265 |
| `void GlobalConfigs::saveStaticConfig()` | 420 |
| `void GlobalConfigs::readDynamicConfig()` | 510 |
| `void GlobalConfigs::saveDynamicConfig()` | 556 |
| `void GlobalConfigs::readOdConfig()` | 587 |
| `void GlobalConfigs::saveOdConfig()` | 618 |
| `bool GlobalConfigs::setSuperId(int index, quint64 id)` | 639 |
| `bool GlobalConfigs::addSuperId(quint64 id)` | 649 |
| `bool GlobalConfigs::removeSuperId(quint64 id)` | 659 |
| `void GlobalConfigs::readVORConfig()` | 669 |
| `void GlobalConfigs::saveVORConfig()` | 690 |
| `bool GlobalConfigs::setWifiNetwork(quint32 index, const QByteArray &ssid, const QByteArray &pw)` | 709 |
| `bool GlobalConfigs::setWifiCountry(const QByteArray &country)` | 723 |
| `void GlobalConfigs::clearWifiConfig()` | 733 |
| `void GlobalConfigs::saveGeofenceConfig()` | 749 |
| `void GlobalConfigs::readGeofenceConfig()` | 778 |

**File-level macros defined in `.cpp`:**

| Macro | Line | Value |
|---|---|---|
| `TEST_LOC_SZ` | 11 | (empty body — no value) |
| `FMS_INI_FILE` | 13 | `"fms.ini"` |
| `DYN_INI_FILE` | 14 | `"dyn.ini"` |
| `FMS_CONFIG_FILE` | 15 | `"fmscfg.dat"` |
| `OD_CONFIG_FILE` | 16 | `"odcfg.dat"` |
| `VOR_CONFIG_FILE` | 17 | `"vor.cfg"` |
| `GFNCE_CONFIG_FILE` | 18 | `"gfnce.cfg"` |
| `MAGIC_CODE` | 19 | `0xA53F3456` |
| `OD_VERSION` | 20 | `1` |

**`using` directive:** `using namespace CIGCONF;` at line 24.

---

### 1.3 `app/globalconfigsfilemanager.h` / `.cpp`

These files **do not exist** in the repository. A `Glob` search for `**/globalconfigsfilemanager*` returned no results. This is noted as Finding A05-1.

---

## 2. Findings

---

**A05-1** · INFO · `globalconfigsfilemanager.h` / `.cpp` do not exist

**Description:** The audit assignment references `app/globalconfigsfilemanager.h` and `app/globalconfigsfilemanager.cpp` as files to review. Neither file exists anywhere in the repository. This was also confirmed by the Pass 3 agent. File I/O is implemented directly inside `GlobalConfigs`, with no separate file-manager abstraction layer. The absence of the files may indicate: (a) the files were planned but never created; (b) they were deleted and the work was inlined; or (c) they are referenced by a stale task description.

**Fix:** Confirm with the team whether a file-manager abstraction was intentionally removed or was never implemented. If the split is still planned, create the files. If not, remove the reference from documentation and the build system.

---

**A05-2** · LOW · Dead macro `TEST_LOC_SZ` (cpp line 11)

**Description:** `#define TEST_LOC_SZ` is defined at `globalconfigs.cpp` line 11 with an empty body. It is never referenced anywhere else in the repository. It appears to be a leftover from a development or test build that was never cleaned up.

**Fix:** Remove the unused `#define TEST_LOC_SZ` line entirely.

---

**A05-3** · LOW · Commented-out code block — reverted MK3-296 logic (cpp lines 164–181)

**Description:** A large commented-out block (18 lines) at `globalconfigs.cpp` lines 164–181 contains the full implementation of an intentionally reverted feature (MK3-296: leading-zero GMTP ID generation). The comment header says `/** Reverted 06Mar24`. While the reverted date is noted, the dead code adds noise, obscures intent, and is now tracked in version control history.

**Fix:** Remove the commented-out block entirely. The VCS history preserves the reverted code if it is ever needed again.

---

**A05-4** · LOW · Commented-out code — minor residual comments (cpp lines 186–187, 194–196, 203–205, 212, 227–228, 243)

**Description:** Multiple single-line and small multi-line commented-out statements are scattered throughout `resetConfigs()` (cpp lines 186, 187, 194–196, 203–205, 212, 227–228) and `saveConfigs()` (line 120) and `resetConfigs()` (line 243). Examples:
- Line 120: `//saveOdConfig();`
- Lines 186–187: `// m_configs.maint.driverId = 0;` / `// m_configs.maint.timestamp = 0;`
- Lines 194–196: `// m_configs.checklistTimeout = 0;` etc.
- Line 243: `//setMasterId(0, 0x2002f5b, CIGCONF::UnassignedMasterMenu, "");`

These commented-out statements are redundant (the `memset` above already zeros the struct) or represent disabled functionality with no explanation. They create maintenance confusion.

**Fix:** Remove all residual commented-out statements. Add an explanatory comment if a deliberate default is being preserved.

---

**A05-5** · LOW · Commented-out `qDebug` in `saveDynamicConfig()` (cpp line 583)

**Description:** `// qDebug() << Q_FUNC_INFO << "Saved dynamic config.";` at line 583 is commented out, unlike the equivalent log statements in every other save function. This is inconsistent with the surrounding code style, where every other `save*Config()` function emits a `qDebug` success message.

**Fix:** Either restore the `qDebug` call (consistent with `saveStaticConfig()`, `saveOdConfig()`, etc.) or document why it is intentionally suppressed.

---

**A05-6** · MEDIUM · Member prefix inconsistency — `gmtpWaitTimeout` and `simICCID` lack `m_` prefix

**Description:** Every private member variable in `GlobalConfigs` uses the `m_` prefix (e.g., `m_fmsDirty`, `m_configs`, `m_screenSaverMode`). Two members violate this convention:
- `gmtpWaitTimeout` (header line 814 / used in cpp lines 236, 365, 470)
- `simICCID[MODEM_ICCID_LEN]` (header line 849 / used in cpp lines 157–165 via the public `getSimCardID()` / `setSimCardID()` / `resetSimCardID()`)

Both are accessed directly in public inline methods, making the inconsistency visible through the public interface.

**Fix:** Rename to `m_gmtpWaitTimeout` and `m_simICCID` (or `m_simIccid` following Qt camelCase conventions) throughout the header and implementation.

---

**A05-7** · MEDIUM · `getDriverName()` uses `gCfg` macro to call back on itself (header lines 220–231)

**Description:** The inline public method `getDriverName(quint64 id)` (header lines 220–231) calls `gCfg->containsTechId(id)`, `gCfg->techIds()`, etc., where `gCfg` expands to `GlobalConfigs::instance()`. The method is called on the singleton, and then internally re-acquires the singleton to call its own public methods. This is a circular self-reference through the global accessor: `this->getDriverName()` → `GlobalConfigs::instance()->containsTechId()`. The correct form would simply use `this->` or call the member objects directly.

**Fix:** Replace all `gCfg->` calls inside `getDriverName()` with direct calls on `this` (e.g., `containsTechId(id)`, `techIds().at(getTechIdIndex(id)).name`).

---

**A05-8** · MEDIUM · `setConvor()` uses `gCfg` self-reference inside member function (header line 265)

**Description:** `setConvor(quint8 convor, quint64 id)` (header lines 259–267) calls `gCfg->setLastCheckTimestamp(0)` inside its body. As with A05-7, `gCfg` is `GlobalConfigs::instance()`, so the method is calling back on itself through the global accessor rather than via `this`.

**Fix:** Replace `gCfg->setLastCheckTimestamp(0)` with `setLastCheckTimestamp(0)` or `this->setLastCheckTimestamp(0)`.

---

**A05-9** · MEDIUM · `onDemandActive()` and `onDemandVehicleEnabled()` use `gCfg` self-reference (header lines 585–586)

**Description:** Both methods expand `gCfg` to `GlobalConfigs::instance()` and then call other methods on the singleton, while they are themselves member functions of that same singleton. Same pattern as A05-7 and A05-8.

**Fix:** Replace `gCfg->` with direct method calls, e.g., `superIsEmpty()` and `onDemandStartTime()` etc.

---

**A05-10** · LOW · `resetConfigs()` calls `memset` on wrong type for `m_configsExt` (cpp line 140)

**Description:** `resetConfigs()` at cpp line 140 performs:
```cpp
memset(&m_configs, 0, sizeof(ConfigsDataExt));
```
This is a copy-paste error. The first argument is `&m_configs` (of type `ConfigsData`) but the size used is `sizeof(ConfigsDataExt)`. Since `ConfigsDataExt` is a 1-byte struct (`quint8 unlkScr`) this is harmless in practice (it only zeroes the first byte of `m_configs`, which was already zeroed by the preceding `memset`), but it never resets `m_configsExt` at all. The intended call should be `memset(&m_configsExt, 0, sizeof(ConfigsDataExt))`.

**Fix:** Change line 140 to:
```cpp
memset(&m_configsExt, 0, sizeof(ConfigsDataExt));
```

---

**A05-11** · HIGH · `readConfigs()` partial-read fallback branch uses an already-attempted `QFile` (cpp lines 63–90)

**Description:** In `readConfigs()`, if `readStaticConfig()` returns `false`, a second attempt is made to read `FMS_CONFIG_FILE` (`fmscfg.dat`) using binary layout. The two files are distinct (`fms.ini` vs `fmscfg.dat`), so this is intentional fallback logic. However, there is an architectural defect: the fallback branch sets `m_configErrorCode = ConfigSizeError` (line 65) before opening the file, then overwrites it with `ConfigCrcError` (line 79) before validating the magic/CRC. If the magic code or CRC check fails, `resetConfigs()` is called (which resets `m_configErrorCode` indirectly via `memset`) but the error code set at line 79 (`ConfigCrcError`) was already overwritten by `resetConfigs()` resetting `m_configs`. After `resetConfigs()`, the code falls through to line 92 (`m_configErrorCode = NoConfigError`), incorrectly reporting a clean state after a CRC failure.

**Fix:** Preserve the error code after calling `resetConfigs()` by setting it again after the `return` statements, or restructure the error-code assignments so `m_configErrorCode` is set after `resetConfigs()` returns in all error paths. Additionally, make `resetConfigs()` not clear `m_configErrorCode`.

---

**A05-12** · MEDIUM · `readGeofenceConfig()` — unused variable `it` declared outside the loop (cpp line 780)

**Description:** `readGeofenceConfig()` at cpp line 780 declares `int it;` and then uses it as the loop counter in a C-style `for (it = 0; it < bas.size(); it++)` loop (line 794). The `it` variable has function scope but is only used inside the loop. Modern C++ style (and Qt convention) declares the loop variable in the `for` initialiser.

**Fix:** Change the loop to `for (int it = 0; it < bas.size(); it++)` and remove the outer declaration.

---

**A05-13** · LOW · Naming convention inconsistency — `UnlkReasonString()` and `UnlkOption()` use PascalCase for non-constructor public methods (header lines 560, 563)

**Description:** Qt coding convention and the prevailing style throughout this class uses lowerCamelCase for public method names (e.g., `maintCode()`, `dialNumber()`, `checklistTimeout()`). The two methods `UnlkReasonString()` and `UnlkOption()` (header lines 560 and 563) use PascalCase, as does `GPSMsgLogEn()` (line 624). This is inconsistent with every other accessor in the class.

**Fix:** Rename to `unlkReasonString()`, `unlkOption()`, and `gpsMsgLogEn()` (or `isGpsMsgLogEn()` following Qt bool-property convention). Update all call sites.

---

**A05-14** · LOW · `bool` members stored as `quint8` — type mismatch and potential signed/unsigned warnings (header lines 851, 853–855, 858)

**Description:** Several fields that semantically hold boolean on/off state are stored as `quint8` rather than `bool`:
- `m_preopOncePerDayEn` (line 850) declared `bool`, but written in `resetConfigs()` as `m_preopOncePerDayEn = 0` and read from file as `(quint8)args[1].toUInt()`.
- `m_idleLockoutEnabled` (line 851): declared `quint8`, but the reset code assigns `false` (cpp line 252): `m_idleLockoutEnabled = false;`
- `m_showPreopSummary`, `m_unlockMode`, `m_forceChecklist`, `m_showTime`, `m_vdiMode` (lines 852–856) are all `quint8` but semantically flags or small enumerations.

The assignment `m_idleLockoutEnabled = false` (cpp line 252) is an implicit conversion from `bool` to `quint8`, which is defined behaviour but triggers `-Wconversion` on stricter build configurations. The inconsistency between `bool` declaration (`m_preopOncePerDayEn`) and `quint8` usage (file I/O casting) is a latent type-mismatch smell.

**Fix:** Decide on a consistent representation. Pure boolean flags should be `bool`. Multi-value flags that map to file-stored integers should be the appropriate integer type. Remove the `= false` initialisation of a `quint8` member.

---

**A05-15** · LOW · `QString` pass-by-value in several public setter methods (header lines 180–183, 220, 558, 561)

**Description:** Several public setters accept `QString` by value instead of by `const QString &`:
- `setDriverId(int index, quint64 id, QString name)` (line 180)
- `setMasterId(int index, quint64 id, quint8 option, QString name)` (line 181)
- `setTechId(int index, quint64 id, QString name)` (line 183)
- `addDriverId(quint64 id, QString name)` (line 190)
- `addTechId(quint64 id, QString name)` (line 192)
- `setPreopCommentString(QString msg)` (line 558)
- `setUnlkReasonString(QString msg)` (line 561)

Each call site causes an unnecessary copy of the `QString` object on the call stack.

**Fix:** Change the parameter type to `const QString &` in all of the above signatures.

---

**A05-16** · MEDIUM · `readStaticConfig()` uses `while(1)` with a single-empty-line break condition (cpp line 274)

**Description:** The loop `while (1) { ... if (ba.isEmpty()) break; ... }` in `readStaticConfig()` (and identically in `readDynamicConfig()`, cpp line 519) uses an infinite loop with an implicit EOF/empty-line break. `QFile::readLine()` returns an empty `QByteArray` both on EOF and on an actual blank line within the file. This means a blank line in `fms.ini` silently terminates parsing of the rest of the file, discarding any settings below the blank line without warning. The correct approach is to check `QFile::atEnd()`.

**Fix:** Replace `while (1)` with `while (!file.atEnd())` and remove the `if (ba.isEmpty()) break;` guard (keeping the `if (args.size() != 2) continue;` guard to skip truly blank lines).

---

**A05-17** · LOW · `dec` and `endl` stream manipulators are deprecated in Qt 5.15+ (cpp lines 434 onwards)

**Description:** `saveStaticConfig()` and `saveDynamicConfig()` make extensive use of `dec` and `endl` as `QTextStream` manipulators (e.g., cpp lines 434–502, 570–579). In Qt 5.15, `dec`, `endl`, and related manipulators were deprecated in favour of `Qt::dec`, `Qt::endl`, etc. Building with `-Wdeprecated-declarations` (default for Qt 5.15+) will produce warnings for every occurrence.

**Fix:** Replace `dec` with `Qt::dec` and `endl` with `Qt::endl` (or `'\n'`) throughout `saveStaticConfig()` and `saveDynamicConfig()`.

---

**A05-18** · LOW · C-style casts in `readStaticConfig()` (cpp lines 284, 300, 335–337, 339, 343–347, 359–410)

**Description:** `readStaticConfig()` uses C-style casts (`(quint8)`, `(quint16)`, `(quint32)`, `(qint16)`, `(CIGCONF::WifiPosSource)`, `(CIGCONF::CameraMode)`, `(CIGCONF::MaintLockedCode)`) extensively when assigning values parsed from the INI file (e.g., `(quint8)args[1].toUInt()` on lines 284, 335, 336, 339, etc.). C-style casts suppress compiler narrowing warnings and bypass type-safety checks.

**Fix:** Replace C-style casts with `static_cast<quint8>(...)` and the equivalent Qt integer types. For enum casts (`CIGCONF::WifiPosSource`, etc.), validate the integer value is within the enum range before casting.

---

**A05-19** · LOW · `readGeofenceConfig()` mixes `qint32` parse result into `quint32` polygon field without validation (cpp lines 803–807)

**Description:** In `readGeofenceConfig()` (cpp lines 801–807):
```cpp
qint32 lon = pol[2].trimmed().toLong();
qint32 lat = pol[3].trimmed().toLong();
m_polygon[n].polyVertices[vect].latitude = lat;
m_polygon[n].polyVertices[vect].longitude = lon;
```
`latitude` and `longitude` in `gpsPosStruct` are `qint32`, but in the header, `polygonLatitude()` / `polygonLongitude()` return `quint32` and the setters accept `quint32`. There is an implicit signed/unsigned mismatch at every point where the polygon data moves through the public API. This is likely to produce `-Wsign-compare` or `-Wconversion` warnings on stricter builds.

**Fix:** Decide on a single type for coordinates throughout (`qint32` is the correct type for signed latitude/longitude values). Update `gpsPosStruct` fields, the getter return types, setter parameter types, and the save/read functions to use `qint32` consistently.

---

**A05-20** · MEDIUM · No bounds checking on `gmtpServerAddress(int index)` and `gmtpServerPort(int index)` getters (header lines 127, 137)

**Description:** The getter methods `gmtpServerAddress(int index)` and `gmtpServerPort(int index)` (header lines 127 and 137) perform no bounds check on `index`. An out-of-range `index` causes an array out-of-bounds access on `m_configs.gmtpServer[index]`. The corresponding setters validate `index >= 0 && index < GMTP_SERVER_CNT`, but the getters do not. Callers who pass an unchecked `index` (e.g., in `saveStaticConfig()` loop) are relying on the caller to be correct. The same pattern exists for `checkTimeSlot(int index)` (line 304) and `polygon(int n)` / `polygonNPoints(int n)` / `polygonLatitude()` / `polygonLongitude()` (lines 490–519).

**Fix:** Add bounds assertions (`Q_ASSERT(index >= 0 && index < GMTP_SERVER_CNT)`) or range-checked access to all array-indexed getters.

---

## 3. Summary Table

| ID | Severity | Title |
|---|---|---|
| A05-1 | INFO | `globalconfigsfilemanager.h/.cpp` do not exist |
| A05-2 | LOW | Dead macro `TEST_LOC_SZ` |
| A05-3 | LOW | Large commented-out reverted-feature block (MK3-296, cpp lines 164–181) |
| A05-4 | LOW | Residual commented-out code in `resetConfigs()` / `saveConfigs()` |
| A05-5 | LOW | `qDebug` success log commented out in `saveDynamicConfig()` |
| A05-6 | MEDIUM | Missing `m_` prefix on `gmtpWaitTimeout` and `simICCID` |
| A05-7 | MEDIUM | `getDriverName()` uses `gCfg` self-reference instead of `this` |
| A05-8 | MEDIUM | `setConvor()` uses `gCfg` self-reference instead of `this` |
| A05-9 | MEDIUM | `onDemandActive()` / `onDemandVehicleEnabled()` use `gCfg` self-reference |
| A05-10 | LOW | `resetConfigs()` memset targets wrong object for `ConfigsDataExt` |
| A05-11 | HIGH | Error code incorrectly reset to `NoConfigError` after CRC failure in `readConfigs()` |
| A05-12 | MEDIUM | `readGeofenceConfig()` — loop variable `it` declared outside the loop |
| A05-13 | LOW | Inconsistent PascalCase on `UnlkReasonString()`, `UnlkOption()`, `GPSMsgLogEn()` |
| A05-14 | LOW | Boolean fields stored as `quint8`; `bool` field initialised with `false` assigned to `quint8` |
| A05-15 | LOW | `QString` parameters passed by value instead of `const QString &` |
| A05-16 | MEDIUM | `while(1)` parse loop breaks on first blank line, silently dropping rest of config file |
| A05-17 | LOW | Deprecated Qt `dec` / `endl` manipulators in `QTextStream` output |
| A05-18 | LOW | Pervasive C-style casts in `readStaticConfig()` |
| A05-19 | LOW | Signed/unsigned mismatch for polygon coordinate types across public API |
| A05-20 | MEDIUM | No bounds checking on array-indexed getter methods |
# Pass 4 Agent A06 — Code Quality

**Audit run:** 2026-02-28-01
**Branch:** master
**Files reviewed:**
- `comm/bleexpansion.h`
- `comm/bleexpansion.cpp`
- `comm/bleexpansionuuid.h`
- `comm/bleexpansionuuid.cpp` (companion definition file, read for full context)

---

## Reading Evidence

### `comm/bleexpansion.h`

**Class:** `BleExpansion` (inherits `QObject`)

| Function / Method | Line | Visibility |
|---|---|---|
| `explicit BleExpansion(EM070::BleCentral *bleCentral)` | 32 | public |
| `void setEnabled(bool enable)` | 34 | public |
| `const QByteArray &deviceName() const` | 36 | public inline |
| `const QByteArray &bleVersion() const` | 37 | public inline |
| `const QByteArray &mainVersion() const` | 38 | public inline |
| `const QByteArray &manufacture() const` | 39 | public inline |
| `const QByteArray &modelNumber() const` | 40 | public inline |
| `bool digitalInput(CIGCONF::BleExpansionDI di) const` | 42 | public inline |
| `bool relayOutput(CIGCONF::BleExpansionRelay relay) const` | 44–46 | public inline |
| `void setRelayOutput(CIGCONF::BleExpansionRelay relay, bool state)` | 47 | public |
| `void setShockThreshold(quint32 threshold)` | 49 | public |
| `void setShockPeriod(quint32 period)` | 50 | public |
| `bool isShockQueueEmpty()` | 52 | public inline |
| `ShockEvent shockEvent()` | 53 | public inline |
| `void setCurrentTime(const QDateTime &time)` | 55 | public |
| `bool generateShockMessage(bool force)` | 57 | public |
| `void accessible(bool yes)` *(signal)* | 60 | signal |
| `void inputStateChanged(CIGCONF::BleExpansionDI input, bool state)` *(signal)* | 61 | signal |
| `void shockOccurred()` *(signal)* | 62 | signal |
| `void amberImpactOccurred()` *(signal)* | 63 | signal |
| `void redImpactOccurred()` *(signal)* | 64 | signal |
| `void timerEvent(QTimerEvent *)` | 67 | protected override |
| `void setAccessible(bool yes)` | 103 | private |
| `void readDeviceInfo()` | 104 | private |
| `void resetInputTimer()` | 105 | private |
| `void resetOutput()` | 106 | private |
| `void initRelays()` | 107 | private |
| `void clearShockEvent()` | 108 | private |
| `void popShockEvent(const QByteArray &ba)` | 109 | private |
| `void allowShockCountNotify(bool yes)` | 110 | private |
| `void characteristicRead(const quint128 &uuid, const QByteArray &ba)` | 111 | private |
| `void characteristicWritten(const quint128 &uuid, const QByteArray &ba)` | 112 | private |
| `void descriptorRead(const quint128 &uuid, const QByteArray &ba)` | 113 | private |
| `void descriptorWritten(const quint128 &uuid, const QByteArray &ba)` | 114 | private |

**Types / Unions / Nested structs defined in `bleexpansion.h`:**

| Name | Kind | Lines |
|---|---|---|
| `BleExpansion::ShockEvent` | nested struct | 27–30 |
| `BleExpansion::RtcTime` | private union (char[10] + packed struct) | 71–83 |
| `BleExpansion::WritePending` | private union (quint32 + bitfield struct) | 85–101 |

**Member variables:** `m_bleCentral`, `m_timerId`, `m_accessible`, `m_shockCountNotifyEnabled`, `m_pending`, `m_previousPending`, `m_deviceName`, `m_bleVersion`, `m_mainVersion`, `m_manufacture`, `m_modelNumber`, `m_shockMaxMagnitude`, `m_digitalInput[4]`, `m_outputRelay[2]`, `m_shockThreshold`, `m_shockPeriod`, `m_shockTimestamp`, `m_shockEvent1`, `m_readingShocks`, `m_shockEvents`, `m_popTimer`.

---

### `comm/bleexpansionuuid.h`

**Class:** `BleExpansionUuid` (utility/namespace-like class, no base)

| Function / Method | Line | Visibility |
|---|---|---|
| `static inline bool equals128(const quint128 *v1, const quint128 *v2)` | 9–17 | public static inline |

**Static data members (all `private static quint128`):**

`authUuid` (20), `deviceName` (21), `appearance` (22), `bleVersion` (23), `mainVersion` (24), `manufactureName` (25), `modelNumber` (26), `currentRtc` (27), `inputTimerReset` (28), `inputD0`–`inputD3` (29–32), `inputPullUp0`–`inputPullUp3` (33–36), `outputReset` (37), `outputRelay0`–`outputRelay1` (38–39), `relay0Timeout`–`relay1Timeout` (40–41), `outputD0`–`outputD3` (42–45), `openCollector0`–`openCollector3` (46–49), `shockCount` (50), `shockPeek` (51), `shockPop` (52), `shockThreshold` (53), `shockPeriod` (54), `shockMaxMagnitude` (55), `shockCountNotifyDesc` (56).

**Friend declaration:** `friend class BleExpansion;` (line 58).

---

### `comm/bleexpansion.cpp`

**Preprocessor macros defined:**

| Macro | Value | Line |
|---|---|---|
| `AUTH_CODE` | `"uS8MgpklMx"` | 9 |
| `MAX_SHOCK_COUNT` | `10000` | 11 |
| `RELAY1_TIMEOUT` | `60` | 12 |
| `RELAY2_TIMEOUT` | `60` | 13 |

**Function definitions (line numbers are the definition start):**

| Function | Line |
|---|---|
| `BleExpansion::BleExpansion` (constructor) | 17 |
| `BleExpansion::timerEvent` | 43 |
| `BleExpansion::setEnabled` | 76 |
| `BleExpansion::setAccessible` | 81 |
| `BleExpansion::setRelayOutput` | 114 |
| `BleExpansion::readDeviceInfo` | 140 |
| `BleExpansion::setCurrentTime` | 154 |
| `BleExpansion::resetInputTimer` | 175 |
| `BleExpansion::resetOutput` | 184 |
| `BleExpansion::clearShockEvent` | 193 |
| `BleExpansion::popShockEvent` | 200 |
| `BleExpansion::generateShockMessage` | 237 |
| `BleExpansion::setShockThreshold` | 254 |
| `BleExpansion::initRelays` | 265 |
| `BleExpansion::setShockPeriod` | 289 |
| `BleExpansion::allowShockCountNotify` | 300 |
| `BleExpansion::characteristicRead` | 308 |
| `BleExpansion::characteristicWritten` | 427 |
| `BleExpansion::descriptorRead` | 508 |
| `BleExpansion::descriptorWritten` | 518 |

---

## Findings

---

**A06-1** · HIGH · `descriptorRead` is implemented but never connected

**Description:** `BleExpansion::descriptorRead` is declared at header line 113 and implemented at `bleexpansion.cpp` line 508. However, the constructor (lines 29–34) only connects four `BleCentral` signals: `characteristicChanged`, `characteristicRead`, `characteristicWritten`, `descriptorWritten`, and `accessible`. There is no `connect` call for `BleCentral::descriptorRead`. The `descriptorRead` slot is therefore dead — it can never be invoked at runtime. The `m_shockCountNotifyEnabled` flag that depends on it (lines 511–514) can therefore only ever be set through `descriptorWritten`, and the `descriptorRead` path is silently unreachable. This is both dead code and a latent bug if the read path is ever relied upon.

**Fix:** Either add `connect(m_bleCentral, &BleCentral::descriptorRead, this, &BleExpansion::descriptorRead);` in the constructor, or remove the `descriptorRead` method entirely if only the write confirmation path is needed.

---

**A06-2** · HIGH · `allowShockCountNotify` is defined but never called

**Description:** `BleExpansion::allowShockCountNotify(bool yes)` is declared private (header line 110) and implemented at `bleexpansion.cpp` line 300. A full search of the repository finds no call site for this function. The `m_shockCountNotifyEnabled` flag it manages is also never read from outside the notification-descriptor callbacks. The BLE CCCD notification path for `shockCount` is therefore permanently disabled, meaning the firmware relies entirely on polling (the 1-second timer) to detect shock events rather than the notification mechanism that was apparently planned.

**Fix:** Either wire `allowShockCountNotify` into the `setAccessible(true)` path and handle the resulting `characteristicChanged` notifications, or remove the method and the `m_shockCountNotifyEnabled` member to reflect the chosen polling design.

---

**A06-3** · HIGH · `resetInputTimer` and `resetOutput` are defined but never called

**Description:** Both `BleExpansion::resetInputTimer()` (header line 105, impl line 175) and `BleExpansion::resetOutput()` (header line 106, impl line 184) are private methods with no call sites anywhere in the repository. The `WritePending` bitfield contains corresponding bits `inputTimerReset` (bit 1) and `outputReset` (bit 6) that are set inside these methods, but because the methods are never invoked, those bits are permanently zero and their acknowledgement branches in `characteristicWritten` (lines 494–504) are also unreachable dead code.

**Fix:** Remove both methods and their corresponding `WritePending` bitfield entries, or document and implement the conditions under which they should be triggered.

---

**A06-4** · MEDIUM · Commented-out code block in `initRelays` (lines 284–286)

**Description:** Three lines of commented-out code appear at the end of `initRelays`:

```cpp
//m_pending.bitMap.outputRelay = 1;
//        m_bleCentral->writeCharacteristic(BleExpansionUuid::outputRelay0, ba);
//        SerialLogger::log(QString("[EXPMOD:RLY] Relay 1 %1\r\n").arg(state?"closed":"opened").toLatin1());
```

These lines were replaced by the `setRelayOutput` calls on lines 281–282 but left in place. The fragment is also syntactically incomplete (references `ba` and `state` that are out of scope at that point), meaning it could not even be uncommented without further edits.

**Fix:** Delete the three commented-out lines.

---

**A06-5** · MEDIUM · `MAX_SHOCK_COUNT` macro defined but never used

**Description:** `#define MAX_SHOCK_COUNT 10000` appears at `bleexpansion.cpp` line 11. No usage of this constant exists anywhere in the file or the wider codebase. The `m_shockEvents` queue is unbounded; the hardware shock counter is a 16-bit value read from a BLE characteristic. It is unclear whether this constant was intended as a queue size cap or as a guard in `popShockEvent`. Its presence without use is misleading and may indicate an unimplemented safety limit.

**Fix:** Either apply the constant as an upper bound on `m_shockEvents.size()` (or on the shock counter read-back) or remove the macro.

---

**A06-6** · MEDIUM · `m_shockMaxMagnitude` is written but never read

**Description:** `m_shockMaxMagnitude` is declared at header line 131 and assigned at `bleexpansion.cpp` line 422 when the BLE characteristic is read. However, it is never subsequently used — not in `popShockEvent`, `generateShockMessage`, nor exposed via any getter. The corresponding UUID (`BleExpansionUuid::shockMaxMagnitude`) is read from the peripheral at startup (line 151) purely to populate this variable. The field appears to have been retained for a planned feature (e.g., normalising shock magnitude or setting an upper alert threshold) that was never implemented.

**Fix:** Either expose `m_shockMaxMagnitude` through a getter and use it in threshold comparisons, or remove the member, the `readCharacteristic` call for `shockMaxMagnitude`, and the handling branch in `characteristicRead`.

---

**A06-7** · MEDIUM · `AUTH_CODE` is a plain-text hardcoded secret in source

**Description:** Line 9 of `bleexpansion.cpp` defines:

```cpp
#define AUTH_CODE   "uS8MgpklMx"
```

This value is passed directly as the BLE authorisation code to `m_bleCentral->setAuthorizationCode(...)` in the constructor (line 40). It is stored verbatim in the compiled binary and committed in version control. Any party with access to the repository or the binary can recover the peripheral authentication credential.

**Fix:** Do not store credentials as string literals in source. Load the auth code from a protected key store, a provisioned device identity, or a configuration protected by OS-level access controls. At minimum, move it out of a public macro into a more restricted scope.

---

**A06-8** · MEDIUM · Double-semicolons on relay-correction lines create silent no-ops

**Description:** Lines 377 and 385 of `bleexpansion.cpp` each have a trailing double semicolon:

```cpp
setRelayOutput(CIGCONF::BleExpRelay1, m_outputRelay[0]);;   // line 377
setRelayOutput(CIGCONF::BleExpRelay2, m_outputRelay[1]);;   // line 385
```

While a stray `;` is syntactically harmless as an empty statement in C++, it is a style defect that signals a copy-paste error or incomplete edit, and some compiler warning configurations (`-Wextra` with pedantic settings) will flag it. More importantly, both lines are inside the relay-discrepancy correction block but the double semicolon suggests the code was hastily edited and may have originally contained a missing `else` branch or an additional side-effect call.

**Fix:** Remove the extra semicolons.

---

**A06-9** · MEDIUM · `RtcTime` uses GCC-specific `__attribute__((packed))` on an anonymous struct inside a union

**Description:** The `RtcTime` union (header lines 71–83) uses:

```cpp
} DateTime __attribute__ ((packed));
```

`__attribute__((packed))` is a GCC/Clang extension not available in MSVC. The union overlays a `char[10]` array against a struct of `quint8`/`quint16` fields. Even without the attribute, accessing the struct members through `rtc.DateTime.year` on a platform where `quint16` requires 2-byte alignment would be undefined behaviour if the union's base address is odd. Mixing union-based type-punning with packed structs is not portable C++ and may produce misaligned-read UB on ARM platforms depending on the allocator.

**Fix:** Replace the union/packed-struct with explicit `qToLittleEndian`/byte-array writes to remove both the portability and the UB risk.

---

**A06-10** · MEDIUM · `reinterpret_cast` on potentially unaligned BLE byte buffers

**Description:** Multiple locations dereference `reinterpret_cast<const quint32 *>(ba.constData())` directly:

- `popShockEvent` line 204: `event.timestamp = *(reinterpret_cast<const quint32 *>(ba.constData()))`
- `popShockEvent` line 205: `event.magnitude = *(reinterpret_cast<const quint32 *>(ba.constData() + 4))`
- `characteristicRead` line 422: `m_shockMaxMagnitude = *(reinterpret_cast<const quint32 *>(ba.constData()))`
- `characteristicWritten` lines 474 and 481: same pattern for threshold/period confirmation

`QByteArray::constData()` returns a `const char *` whose alignment is only guaranteed to be 1-byte. On ARM Cortex-A/M targets where the BLE stack may supply non-4-byte-aligned buffers, dereferencing a `quint32 *` from such a pointer is undefined behaviour (unaligned access trap or silent tearing depending on MCU configuration).

**Fix:** Use `qFromLittleEndian<quint32>(ba.constData())` or `memcpy` into a local `quint32` to perform safe unaligned reads.

---

**A06-11** · MEDIUM · `WritePending` bitfield uses signed `int` for bit members

**Description:** The `WritePending::bitMap` struct (header lines 87–100) declares all bit-field members as `int` (signed), e.g.:

```cpp
int currentTime     : 1;
int shockEventClear : 1;
```

A 1-bit signed integer has only two representable values: `0` and `-1`. Assigning `1` to a 1-bit signed bitfield yields implementation-defined behaviour in C++03 and is still potentially surprising in C++11+. The code uses assignments like `m_pending.bitMap.currentTime = 1` throughout, which will always store `-1` in a 1-bit signed field on two's-complement platforms, but comparing or printing the value produces unexpected results.

**Fix:** Change all bitfield member types to `unsigned int` (or `quint32`) to make single-bit values behave as booleans with values 0 and 1.

---

**A06-12** · LOW · `isShockQueueEmpty` and `shockEvent` are non-`const` public inline methods lacking `const` correctness

**Description:** `isShockQueueEmpty()` (header line 52) could logically be `const` — it only calls `m_shockEvents.isEmpty()`. It is not declared `const`. `shockEvent()` (line 53) does mutate the queue (dequeue), so `const` is not applicable there, but the absence of `const` on `isShockQueueEmpty` is a minor style defect.

**Fix:** Add `const` qualifier to `isShockQueueEmpty`.

---

**A06-13** · LOW · `BleExpansionUuid` UUID constants declared without `const`

**Description:** All 37 UUID constants in `BleExpansionUuid` are declared `static quint128` — mutable by any code in scope — rather than `static const quint128`. The `friend class BleExpansion` declaration makes all private members accessible to `BleExpansion`, which means any method of `BleExpansion` can inadvertently modify a UUID constant. Given the definitions in `bleexpansionuuid.cpp` are used only as read-only lookup keys, they should be const.

**Fix:** Change all `static quint128` members in `BleExpansionUuid` to `static const quint128` and update the `bleexpansionuuid.cpp` definitions accordingly.

---

**A06-14** · LOW · `equals128` performs pointer arithmetic past the end of `quint128` without size guarantee

**Description:** `BleExpansionUuid::equals128` (header lines 9–17) casts two `const quint128 *` pointers to `const quint32 *` and iterates four times with `++p1`/`++p2`. This assumes `sizeof(quint128) == 16` and that the layout is exactly four contiguous `quint32` values. Qt's `quint128` is a typedef for a compiler-specific 128-bit integer type (or a struct on platforms without native 128-bit support). If the struct representation has padding, the comparison silently fails. Qt provides `QBluetoothUuid::toUInt128()` which returns a well-defined struct; however, there is no static assertion verifying this assumption.

**Fix:** Add `static_assert(sizeof(quint128) == 16, "quint128 size mismatch");` inside `equals128`, or use `memcmp(v1, v2, sizeof(quint128))` which is both safer and more readable.

---

**A06-15** · LOW · `setRelayOutput` logs a debug warning on inaccessible state but continues execution

**Description:** At `bleexpansion.cpp` line 117:

```cpp
if (!m_accessible)
    qDebug() << "setRelayOutput(" << relay << ", " << state << ") not accessible";
```

The function does **not** return after logging. It falls through to update `m_outputRelay[0]` or `m_outputRelay[1]` (lines 123, 131) even when not accessible, but does not write to the BLE characteristic. This silent state divergence means the local shadow state (`m_outputRelay`) is updated as if the write succeeded, but the peripheral is not written. When accessibility is later restored, `initRelays` will push the cached state to the peripheral, which partly mitigates this, but the debug-only log with no early return is a style inconsistency with every other method in the class (all of which do `if (!m_accessible) return;`).

**Fix:** Consistently apply the early-return guard, or replace with `qWarning()` to surface the issue at a non-debug build level.

---

**A06-16** · LOW · `appearance` UUID is declared and defined but never used

**Description:** `BleExpansionUuid::appearance` is declared in `bleexpansionuuid.h` line 22 and defined in `bleexpansionuuid.cpp` line 9. No code in `bleexpansion.cpp` (or anywhere else in the repository) reads or writes the `appearance` characteristic. It is dead data.

**Fix:** Remove the `appearance` declaration and definition.

---

**A06-17** · LOW · Output UUIDs `outputD0`–`outputD3` and `openCollector0`–`openCollector3` are never referenced in `bleexpansion.cpp`

**Description:** Eight UUID constants — `outputD0`, `outputD1`, `outputD2`, `outputD3`, `openCollector0`, `openCollector1`, `openCollector2`, `openCollector3` — are declared in `bleexpansionuuid.h` and defined in `bleexpansionuuid.cpp`, but are never referenced in `bleexpansion.cpp`. The corresponding `WritePending` bitfield allocates bits for `output` (4 bits) and `openCollector` (4 bits) but no code ever sets or clears these bits. This suggests a partially implemented feature for driving digital outputs and open-collector outputs.

**Fix:** Either implement the digital output and open-collector write/read paths, or remove the UUID constants and `WritePending` bit allocations to keep the code consistent with what is actually used.

---

**A06-18** · INFO · `inputPullUp0`–`inputPullUp3` UUIDs are defined but never used in `bleexpansion.cpp`

**Description:** The four pull-up configuration UUIDs (`inputPullUp0`–`inputPullUp3`, `bleexpansionuuid.h` lines 33–36) are defined but never referenced in `bleexpansion.cpp`. The `WritePending` bitfield reserves 4 bits for `inputPullup` (header line 90), but no code sets or clears these bits.

**Fix:** Implement pull-up configuration writes if required by the hardware protocol, or remove the unused UUID constants and bitfield entries.

---

**A06-19** · INFO · `relay0Timeout` and `relay1Timeout` use magic constants `RELAY1_TIMEOUT`/`RELAY2_TIMEOUT` both set to `60` with no units documented

**Description:** Macros `RELAY1_TIMEOUT` (value `60`) and `RELAY2_TIMEOUT` (value `60`) are defined at lines 12–13 without any comment indicating the unit (seconds? milliseconds? BLE ticks?). The values are written as a 16-bit little-endian integer to the relay timeout characteristics. A reader cannot determine from source alone what timeout duration is configured.

**Fix:** Add a comment stating the unit (e.g., `// seconds`) next to the macro definitions.

---

**A06-20** · INFO · `m_previousPending` is not initialised in the constructor member-initialiser list

**Description:** `m_previousPending` is declared at header line 123 but does not appear in the constructor initialiser list (`bleexpansion.cpp` lines 17–26). `m_pending.val` is explicitly zeroed at line 27, but `m_previousPending` receives no initialisation — its value at construction is indeterminate until the first write acknowledgement. If `timerEvent` fires before any write is acknowledged, the stale comparison on line 50 (`m_previousPending == m_pending.val`) may suppress the "Failed to write" warning spuriously.

**Fix:** Add `m_previousPending(0)` to the constructor's member-initialiser list.

---

**A06-21** · INFO · `m_shockCountNotifyEnabled` is not initialised in the constructor member-initialiser list

**Description:** `m_shockCountNotifyEnabled` is declared at header line 120 but is absent from the constructor initialiser list. It is set to `false` inside `setAccessible(true)` at line 98, but if any BLE event arrives before `setAccessible` is called (unlikely but technically possible during connection setup), the field value is indeterminate.

**Fix:** Add `m_shockCountNotifyEnabled(false)` to the constructor's member-initialiser list.

---

**A06-22** · INFO · `m_digitalInput[4]` is not zero-initialised in the constructor

**Description:** `m_digitalInput[4]` (header line 132) is not initialised in the constructor initialiser list or in the constructor body. The array holds the last-known state of the four digital inputs. Before any BLE read completes, `digitalInput()` will return garbage. On most Qt-embedded targets the heap is zeroed, but this is not a language guarantee.

**Fix:** Initialise the array either as `m_digitalInput{}` in the member-initialiser list or add a `memset` in the constructor body.

---

## Summary Table

| ID | Severity | Title |
|---|---|---|
| A06-1 | HIGH | `descriptorRead` slot implemented but never connected |
| A06-2 | HIGH | `allowShockCountNotify` defined but never called |
| A06-3 | HIGH | `resetInputTimer` and `resetOutput` defined but never called |
| A06-4 | MEDIUM | Commented-out code block in `initRelays` (lines 284–286) |
| A06-5 | MEDIUM | `MAX_SHOCK_COUNT` macro defined but never used |
| A06-6 | MEDIUM | `m_shockMaxMagnitude` written but never read |
| A06-7 | MEDIUM | `AUTH_CODE` is a hardcoded plain-text secret in source |
| A06-8 | MEDIUM | Double-semicolons on relay-correction lines (lines 377, 385) |
| A06-9 | MEDIUM | `RtcTime` uses non-portable GCC `__attribute__((packed))` |
| A06-10 | MEDIUM | `reinterpret_cast` on potentially unaligned BLE byte buffers |
| A06-11 | MEDIUM | `WritePending` bitfield uses signed `int` for 1-bit members |
| A06-12 | LOW | `isShockQueueEmpty` missing `const` qualifier |
| A06-13 | LOW | `BleExpansionUuid` UUID constants not declared `const` |
| A06-14 | LOW | `equals128` lacks size assertion for `quint128` layout |
| A06-15 | LOW | `setRelayOutput` logs debug but does not early-return when inaccessible |
| A06-16 | LOW | `appearance` UUID declared, defined, and never used |
| A06-17 | LOW | `outputD0`–`outputD3` and `openCollector0`–`openCollector3` UUIDs unused |
| A06-18 | INFO | `inputPullUp0`–`inputPullUp3` UUIDs defined but never used |
| A06-19 | INFO | Relay timeout macros lack unit documentation |
| A06-20 | INFO | `m_previousPending` not initialised in constructor initialiser list |
| A06-21 | INFO | `m_shockCountNotifyEnabled` not initialised in constructor initialiser list |
| A06-22 | INFO | `m_digitalInput[4]` not zero-initialised in constructor |
# Pass 4 Agent A07 — Code Quality

**Audit run:** 2026-02-28-01
**Branch:** master
**Files reviewed:**
- `comm/bleinputhandler.h`
- `comm/bleinputhandler.cpp`
- `comm/canexpansion.h`
- `comm/canexpansion.cpp`

---

## Reading Evidence

### comm/bleinputhandler.h

**Class:** `BleInputHandler` (extends `QObject`)

**Enums / Types defined:**
| Name | Values |
|------|--------|
| `DigitalFormat` (public enum) | `SessionFormat`, `UsageFormat`, `OnDemandFormat` |
| `InputState` (private struct) | fields: `bool state`, `quint32 sessionOnTime`, `quint32 sessionOffTime`, `quint32 usageOnTime`, `quint32 usageOffTime`, `quint32 sessionRisings`, `quint32 usageRisings`, `quint64 clock` |

**Methods (all in `BleInputHandler`):**

| Method | Line | Visibility |
|--------|------|------------|
| `BleInputHandler(CanExpansion *canExpansion)` (constructor) | 20 | public |
| `updateIgnition(CIGCONF::PowerState state)` | 22 | public |
| `updateBleInput(CIGCONF::BleExpansionDI input, bool state)` | 23 | public |
| `changeBleState(bool connected)` | 24 | public |
| `updateIdleTimer()` | 26 | public |
| `digitalInputs(DigitalFormat format, bool autoReset)` | 28 | public |
| `idleTimeout()` | 31 | signal |
| `sendGmtpMessage(CIGCONF::GmtpMessage msg, const QByteArray &extra)` | 32 | signal |
| `resetStates()` | 35 | private |
| `onTimerEvent()` | 36 | private |
| `sendSeenSafeReport(bool state)` | 37 | private |

**Member variables:**
- `m_canExpansion` (`CanExpansion *`)
- `m_timer` (`QTimer *`)
- `m_digInputModeTimer` (`QTimer *`)
- `m_ignition` (`InputState`)
- `m_bleInputs[4]` (`InputState`)
- `m_bypassReset` (`bool`)
- `m_bleConnected` (`bool`)
- `m_seenState` (`bool`)
- `m_lastSeenReport` (`quint64`)
- `m_seenSecond` (`bool`)
- `m_seenTimestamp` (`quint32`)

---

### comm/bleinputhandler.cpp

**Functions (all in `BleInputHandler`):**

| Function | Line |
|----------|------|
| `BleInputHandler(CanExpansion *canExpansion)` — constructor | 7 |
| `resetStates()` | 25 |
| `updateIgnition(CIGCONF::PowerState state)` | 40 |
| `onTimerEvent()` | 81 |
| `sendSeenSafeReport(bool state)` | 92 |
| `updateBleInput(CIGCONF::BleExpansionDI input, bool state)` | 115 |
| `changeBleState(bool connected)` | 178 |
| `updateIdleTimer()` | 201 |
| `digitalInputs(DigitalFormat format, bool autoReset)` | 257 |

---

### comm/canexpansion.h

**Class:** `CanExpansion` (extends `QObject`)

**Enums / Types defined:**
| Name | Description |
|------|-------------|
| `ShockEvent` (public struct) | fields: `quint32 timestamp`, `quint32 magnitude`, `quint64 driverId`, `quint8 satelliteCount`, `quint32 lastLongitude`, `quint32 lastLatitude`, `quint16 speed`, `quint32 sumOfDistance`, `quint16 course`, `quint32 longitude`, `quint32 latitude`, `quint32 distance`, `bool isIgnitionOn` |

**Methods:**

| Method | Line | Visibility |
|--------|------|------------|
| `CanExpansion(EM070::CanBus *canBus, EM070::PowerSupply *ps)` (constructor) | 42 | public |
| `setEnabled(bool enable)` | 44 | public |
| `deviceName() const` | 46 | public inline |
| `bleVersion() const` | 47 | public inline |
| `mainVersion() const` | 48 | public inline |
| `manufacture() const` | 49 | public inline |
| `modelNumber() const` | 50 | public inline |
| `relayOutput(CIGCONF::BleExpansionRelay relay) const` | 52 | public inline |
| `setRelayOutput(CIGCONF::BleExpansionRelay relay, bool state)` | 55 | public |
| `relayTimeout(CIGCONF::BleExpansionRelay relay) const` | 57 | public inline |
| `setRelayTimeout(CIGCONF::BleExpansionRelay relay, quint16 timeout_in_sec)` | 60 | public |
| `setCurrentTime(quint32 time)` | 62 | public |
| `digitalInput(CIGCONF::BleExpansionDI di) const` | 64 | public inline |
| `setShockThreshold(quint32 threshold)` | 66 | public |
| `setShockPeriod(quint32 period)` | 67 | public |
| `isShockQueueEmpty()` | 69 | public inline |
| `shockEvent()` | 70 | public inline |
| `generateShockMessage(bool force)` | 72 | public |
| `setGnssReceiver(EM070::GnssReceiver* gnss)` | 74 | public |
| `inputStateChanged(CIGCONF::BleExpansionDI input, bool state)` | 77 | signal |
| `shockOccurred()` | 78 | signal |
| `amberImpactOccurred()` | 79 | signal |
| `redImpactOccurred()` | 80 | signal |
| `accessible(bool yes)` | 81 | signal |
| `expModInfo(QByteArray mainVersion)` | 82 | signal |
| `inactiveNotification(bool inactive, quint32 secs)` | 83 | signal |
| `relayStateChanged(bool relay1, bool relay2)` | 84 | signal |
| `initialise()` | 87 | private |
| `updateBusConfig()` | 88 | private |
| `readCanFrame(quint32 id, const QByteArray &ba)` | 89 | private |
| `packetHandler()` | 90 | private |
| `writeFrame()` | 91 | private |
| `timeout()` | 92 | private |
| `sendPacket(uint16_t cmd, const QByteArray &ba)` | 94 | private |
| `initRelays()` | 96 | private |
| `clearShockEvent()` | 97 | private |
| `popShockEvent(const QByteArray &ba)` | 98 | private |

**Member variables:**
- `m_canBus` (`EM070::CanBus *`)
- `m_powerSupply` (`EM070::PowerSupply *`)
- `m_gnssReceiver` (`EM070::GnssReceiver *`)
- `m_timer` (`QTimer *`)
- `m_initTimer` (`QTimer *`)
- `m_rx` (`QByteArray`)
- `m_tx` (`QByteArray`)
- `m_active` (`bool`)
- `m_lastActive` (`bool`)
- `m_inactiveCount` (`quint32`)
- `m_deviceName` (`QByteArray`)
- `m_bleVersion` (`QByteArray`)
- `m_mainVersion` (`QByteArray`)
- `m_manufacture` (`QByteArray`)
- `m_modelNumber` (`QByteArray`)
- `m_digitalInput[4]` (`bool`) — **declared but never written in canexpansion.cpp**
- `m_outputRelay[2]` (`bool`)
- `m_outputRelayTimeout[2]` (`quint16`)
- `m_shockThreshold` (`quint32`)
- `m_shockPeriod` (`quint32`)
- `m_redImpactCounter` (`qint32`)
- `m_shockTimestamp` (`quint32`)
- `m_shockEvent1` (`ShockEvent`)
- `m_shockEvents` (`QQueue<ShockEvent>`)

**Constants defined (canexpansion.cpp, file-scope `#define`):**

| Macro | Value | Comment |
|-------|-------|---------|
| `CMD_DEVICE_NAME` | 1001 | |
| `CMD_BLE_FWVER` | 8 | |
| `CMD_MAIN_FWVER` | 10 | |
| `CMD_MFR_NAME` | 1002 | |
| `CMD_MODEL_NUMBER` | 1003 | |
| `CMD_RTC_TIME` | 26 | |
| `CMD_DIGIN_STATE0..3` | 31,35,39,43 | |
| `CMD_RELAY_RESET` | 48 | |
| `CMD_RELAY_STATE0/1` | 50,54 | |
| `CMD_RELAY_TIMEOUT0/1` | 52,56 | |
| `CMD_SHOCK_COUNT` | 75 | |
| `CMD_SHOCK_PEEK` | 78 | |
| `CMD_SHOCK_POP` | 80 | |
| `CMD_SHOCK_THRESHOLD` | 82 | |
| `CMD_SHOCK_PERIOD` | 84 | |
| `CMD_SHOCK_MAGMAX` | 86 | |
| `CMD_SHOCK_NOTIFY` | 1004 | |
| `UPDATE_DEFER` | 500 | |
| `MAX_BUFFER_SIZE` | 256 | |
| `MK3_ID` | 0x3C1 | |
| `SLIP_END/ESC/ESC_END/ESC_ESC` | 0xC0,0xDB,0xDC,0xDD | |
| `FROM_MK3_HEADER` | 0x01 | |
| `TO_MK3_HEADER` | 0x81 | |
| `CMD_WRITE_FLAG` | 0x8000 | |
| `REDIMPACT_SHOCKMSG_TIME` | 3 | |
| `REDIMPACT_COUNTER_OFF` | -1 | |
| `TIMER` | 2000 | |
| `INACTIVE_TIME` | 2 | |

---

## Findings

---

**A07-1** · HIGH · Dead member: `m_digitalInput[4]` declared in `CanExpansion` but never written

**Description:** `canexpansion.h` line 119 declares `bool m_digitalInput[4]` and line 64 exposes a `digitalInput()` accessor. However, `canexpansion.cpp` never writes to `m_digitalInput` — the digital-input state is emitted only via the `inputStateChanged` signal and is tracked inside `BleInputHandler`. The accessor therefore always returns the zero-initialised value (`false`). Any caller that uses `CanExpansion::digitalInput()` receives stale, permanently-false data. (Contrast with `bleexpansion.h/.cpp`, which maintains its own identical member and does write to it correctly.)

**Fix:** Either populate `m_digitalInput[index]` when `inputStateChanged` is emitted inside `packetHandler()`, or remove the member and the `digitalInput()` accessor from the public API and update any callers to use the signal instead.

---

**A07-2** · HIGH · Static local state in `readCanFrame` and `packetHandler` breaks re-entrancy and testability

**Description:**
- `readCanFrame()` (canexpansion.cpp line 130): `static bool esc = false;` persists across calls. If the CAN bus is reset or `CanExpansion` is destroyed and recreated, the escape-flag is never cleared, so the next SLIP stream may be decoded incorrectly.
- `packetHandler()` (canexpansion.cpp line 251–252): `static quint16 sm = 0; static quint16 shocks_read = 0;` are the sole state-machine registers for the init handshake and shock-drain loop. Because they are function-local statics they are shared across all instances and survive object destruction. In a single-instance embedded target this is unlikely to cause a runtime fault, but it is architecturally broken: unit tests cannot reset the state machine, and a second `CanExpansion` instance would corrupt the first's handshake.

**Fix:** Promote `esc`, `sm`, and `shocks_read` to private member variables of `CanExpansion` (initialised in the constructor). Add their reset to any `setEnabled(false)` / re-initialisation path.

---

**A07-3** · MEDIUM · Commented-out code left in production sources

**Description:**
- `canexpansion.h` line 118: `//quint32     m_shockMaxMagnitude;` — commented-out member declaration.
- `canexpansion.cpp` line 234: `//SerialLogger::log(QString("[%1 " + m_canBus->canBusDevice()->errorString() + "]\r\n").arg(m_canBus->canBusDevice()->framesToWrite()).toLatin1());` — entire debug-logging line inside `writeFrame()`.
- `canexpansion.cpp` line 123: `//if (m_busConfig.enabled)` — a guard expression replaced by `if (enabled)` on the very next line; the old version is still present.

**Fix:** Delete all three commented-out lines. If `m_shockMaxMagnitude` is genuinely unused it should be removed entirely; if it will be needed it should be tracked in a TODO/issue rather than left as dead markup in the header.

---

**A07-4** · MEDIUM · `qDebug()` statement left in production code

**Description:** `canexpansion.cpp` line 659:
```cpp
qDebug() << "EXPMOD Shock" << event.timestamp << event.magnitude;
```
This is inside `popShockEvent()`, which executes on every shock detection. `qDebug()` output is compiled in by default in release builds unless `QT_NO_DEBUG_OUTPUT` is explicitly defined, leaking internal telemetry data to any connected debug console and adding unnecessary overhead on the target hardware.

**Fix:** Remove the `qDebug()` line. The `SerialLogger::log()` call on the line immediately below provides sufficient structured diagnostic output through the controlled logging subsystem.

---

**A07-5** · MEDIUM · Mixed integer type for `sendPacket` command parameter (`uint16_t` vs `quint16`)

**Description:** The private declaration of `sendPacket` in `canexpansion.h` line 94 uses the raw C type `uint16_t`:
```cpp
void sendPacket(uint16_t cmd, const QByteArray &ba);
```
Every other integer in both files uses Qt's portable types (`quint16`, `quint32`, etc.). The rest of the codebase is consistent in using Qt types. This inconsistency is exacerbated by the fact that `sendPacket` is called with expressions such as `CMD_RELAY_STATE0 | CMD_WRITE_FLAG`, where `CMD_WRITE_FLAG` is defined as `0x8000` (an `int` macro), causing the result to be implicitly narrowed through a mixed-type OR before being passed.

**Fix:** Change the parameter type to `quint16` to match the rest of the file. If the OR-with-`CMD_WRITE_FLAG` pattern is intentional (setting the high bit to indicate a write), replace the raw `int` macro with a typed constant (`static const quint16 CMD_WRITE_FLAG = 0x8000;`) to make the narrowing explicit.

---

**A07-6** · MEDIUM · `updateBleInput` does not bounds-check the `input` index

**Description:** `bleinputhandler.cpp` line 117:
```cpp
int index = input - CIGCONF::BleExpDI1;
InputState &is = m_bleInputs[index];
```
`CIGCONF::BleExpansionDI` is an unscoped enum starting at `BleExpDI1 = 0`. If `input` is ever passed a value outside `[BleExpDI1, BleExpDI4]` (e.g., from a future enum extension or a programming error in a caller), `index` will be negative or >= 4 and the array access will be out-of-bounds with undefined behaviour. The same unchecked arithmetic appears in `canexpansion.h` line 64 (`digitalInput()`).

**Fix:** Add a bounds assertion or early-return guard:
```cpp
int index = input - CIGCONF::BleExpDI1;
if (index < 0 || index >= 4) return;
```
Alternatively use `Q_ASSERT` for debug builds.

---

**A07-7** · MEDIUM · Empty `switch` cases in `packetHandler` with no documentation

**Description:** `canexpansion.cpp` lines 330–465 contain nine `case` labels (`CMD_RELAY_RESET`, `CMD_RELAY_STATE0`, `CMD_RELAY_STATE1`, `CMD_RELAY_TIMEOUT0`, `CMD_RELAY_TIMEOUT1`, `CMD_RTC_TIME`, `CMD_SHOCK_THRESHOLD`, `CMD_SHOCK_PERIOD`, `CMD_SHOCK_MAGMAX`, `CMD_SHOCK_NOTIFY`) that have empty bodies with no comment. It is impossible to determine whether these are intentional no-ops (acknowledgement frames where no action is required), planned future work, or overlooked implementations. This ambiguity is a maintenance hazard.

**Fix:** Add a brief comment to each empty case explaining the intent, for example:
```cpp
case CMD_RTC_TIME:
    // Write-only; no response payload expected.
    break;
```

---

**A07-8** · LOW · Inconsistent `relayOutput` / `relayTimeout` accessor guard logic

**Description:** `canexpansion.h` lines 52–59:
```cpp
bool relayOutput(CIGCONF::BleExpansionRelay relay) const {
    return (relay == CIGCONF::BleExpRelay2 ? m_outputRelay[1] : m_outputRelay[0]);
}
quint16 relayTimeout(CIGCONF::BleExpansionRelay relay) const {
    return (relay == CIGCONF::BleExpRelay2 ? m_outputRelayTimeout[1] : m_outputRelayTimeout[0]);
}
```
Both accessors use a ternary where any value that is not `BleExpRelay2` silently maps to relay 1. An invalid relay enum value would return relay-1 data rather than triggering a diagnostic. This is the same structural problem as A07-6. The `BleExpansionRelay` enum has exactly two values so it is low severity today, but the silent-fallback pattern is fragile.

**Fix:** Replace the ternary with an explicit index calculation (`relay - CIGCONF::BleExpRelay1`) and add an assertion, or use a switch with a default that asserts/returns a sentinel.

---

**A07-9** · LOW · `updateIdleTimer()` is `public` but is an implementation detail

**Description:** `bleinputhandler.h` line 26: `updateIdleTimer()` is declared `public`. Inspecting the call sites, `updateIdleTimer()` is only called from `resetStates()` (an internal method) and indirectly from the constructor. It is exposed publicly with no documented reason. Callers outside the class that invoke it at the wrong time could corrupt the idle-timer state.

**Fix:** Move `updateIdleTimer()` to the `private` section unless there is a documented external caller that requires it.

---

**A07-10** · LOW · `bool on = (state == CIGCONF::NormalPowerState) ? true : false;` — redundant ternary

**Description:** `bleinputhandler.cpp` line 42:
```cpp
bool on = (state == CIGCONF::NormalPowerState) ? true : false;
```
The comparison expression already yields a `bool`. The `? true : false` suffix is redundant and a common style warning in static analysis tools.

**Fix:** Simplify to:
```cpp
bool on = (state == CIGCONF::NormalPowerState);
```

---

**A07-11** · LOW · Trailing whitespace and brace/formatting inconsistencies

**Description:**
- `canexpansion.cpp` line 232: `void CanExpansion::writeFrame()` — the opening brace is on the same line as the first variable declaration (`{   int len;`), which is unique in the file and inconsistent with every other function definition.
- `canexpansion.cpp` line 147: trailing whitespace after `packetHandler();` inside `readCanFrame`.
- `canexpansion.cpp` line 525: trailing whitespace after the closing brace of `initRelays()`.
- `bleinputhandler.cpp` line 142: trailing whitespace after `m_digInputModeTimer->start(...)`.
- `bleinputhandler.cpp` line 289: trailing whitespace before the blank line inside `digitalInputs()`.

These are minor but indicate the files have not been passed through a consistent formatter.

**Fix:** Run `clang-format` (or the project's chosen formatter) over both files and configure the CI pipeline to enforce formatting on commit.

---

**A07-12** · LOW · `QTimer` forward-declared in `canexpansion.h` but also `#include <QTimer>` present

**Description:** `canexpansion.h` line 19 contains a forward declaration `class QTimer;`, but line 11 already `#include <QTimer>`. The forward declaration is therefore redundant. (`bleinputhandler.h` has the same pattern: forward-declares `QTimer` at line 12 despite not including the header — that usage is correct as a forward declaration only, but should be verified against Qt's inclusion requirements for inline use.)

**Fix:** Remove the redundant `class QTimer;` forward declaration from `canexpansion.h` since the full header is already included. In `bleinputhandler.h` the forward declaration is appropriate (the type is only used as a pointer), so it should be retained.

---

**A07-13** · INFO · Magic number `500` used directly in `initialise()`

**Description:** `canexpansion.cpp` line 94: `m_timer->start(500);`. The constant `TIMER` is defined as `2000` on line 58, and `UPDATE_DEFER` as `500` on line 40. The poll interval for the main 2-second cycle is started with the literal `500` rather than a named constant. While `UPDATE_DEFER` happens to have the same value, using the literal hides the intent (is this 500 ms by coincidence or by design to match `UPDATE_DEFER`?).

**Fix:** If the 500 ms poll interval is intentional and independent of `UPDATE_DEFER`, define a separate named constant (e.g., `POLL_INTERVAL 500`). If it is the same concept, replace the literal with `UPDATE_DEFER`.

---

## Summary Table

| ID | Severity | Title |
|----|----------|-------|
| A07-1 | HIGH | Dead member `m_digitalInput[4]` declared but never written in `CanExpansion` |
| A07-2 | HIGH | Static local variables in `readCanFrame` / `packetHandler` break re-entrancy |
| A07-3 | MEDIUM | Commented-out code left in production sources (3 sites) |
| A07-4 | MEDIUM | `qDebug()` statement left in production `popShockEvent()` |
| A07-5 | MEDIUM | Mixed `uint16_t` / `quint16` type for `sendPacket` command parameter |
| A07-6 | MEDIUM | `updateBleInput` array index not bounds-checked |
| A07-7 | MEDIUM | Nine empty `switch` cases in `packetHandler` with no explanatory comment |
| A07-8 | LOW | Accessor ternary silently maps invalid relay enum to relay 1 |
| A07-9 | LOW | `updateIdleTimer()` is public but is an internal implementation detail |
| A07-10 | LOW | Redundant `? true : false` ternary in `updateIgnition` |
| A07-11 | LOW | Trailing whitespace and brace-placement inconsistencies |
| A07-12 | LOW | Redundant `class QTimer` forward declaration in `canexpansion.h` |
| A07-13 | INFO | Magic literal `500` in `initialise()` should be a named constant |
# Pass 4 Agent A08 — Code Quality

**Audit run:** 2026-02-28-01
**Branch:** master
**Files reviewed:**
- `comm/canmonitor.h`
- `comm/canmonitor.cpp`
- `comm/canstatehandler.h`
- `comm/canstatehandler.cpp`

---

## 1. Reading Evidence

### 1.1 `comm/canmonitor.h`

**Class:** `CanMonitor` (inherits `QObject`)

| Function / Method | Line |
|---|---|
| `CanMonitor(EM070::CanBus *canBus)` (constructor) | 20 |
| `readCanConfig()` | 22 |
| `readOldCanConfig()` | 23 |
| `saveCanConfig()` | 24 |
| `calculateCanCrc()` | 25 |
| `canCrc32() const` (inline) | 28 |
| `setEnabled(bool enable)` | 30 |
| `clearCanConfig()` | 32 |
| `canBusConfig() const` | 33 |
| `setCanBusConfig(const QByteArray &config)` | 34 |
| `canPgnConfig() const` | 35 |
| `setCanPgnConfig(const QByteArray &config)` | 36 |
| `canSpnConfig() const` | 37 |
| `setCanSpnConfig(const QByteArray &config)` | 38 |
| `canAttConfig() const` | 39 |
| `setCanAttConfig(const QByteArray &config)` | 40 |
| `canLinConfig() const` | 41 |
| `setCanLinConfig(const QByteArray &config)` | 42 |
| `canBydConfig() const` | 43 |
| `setCanBydConfig(const QByteArray &config)` | 44 |
| `canLin2Config() const` | 45 |
| `setCanLin2Config(const QByteArray &config)` | 46 |
| `isXferEnabled() const` (inline) | 48 |
| `attributeName(quint8 index) const` (inline) | 49 |
| `attributeType(quint8 index) const` (inline) | 50 |
| `setVdiAccess(bool access, bool inhibit)` | 52 |
| `enableVdi(bool enable)` | 53 |
| **signals:** `resetCanStates(bool resetLast)` | 60 |
| **signals:** `stateUpdated(quint8 index, quint32 state)` | 61 |
| `isValidPgnConfig(const PgnConfig &config) const` (inline private) | 108 |
| `isValidSpnConfig(const SpnConfig &config) const` (inline private) | 109 |
| `isValidAttribute(const AttConfig &config) const` (inline private) | 110 |
| `childSpnIndexes(quint8 pgnIndex) const` | 111 |
| `findPgnIndex(quint32 rspId, quint32 reqId = 0) const` | 112 |
| `newPgnIndex() const` | 113 |
| `attributePollingRate(quint32 namePattern) const` | 114 |
| `createRequest(quint8 spnIndex, quint32 pollingRate)` | 115 |
| `updateBusConfig()` | 117 |
| `updateRequests()` | 118 |
| `readCanFrame(quint32 id, const QByteArray &ba)` | 120 |
| `updateState(quint8 spnIndex, quint64 data)` | 121 |
| `updateSpnState(quint8 spnIndex, quint64 data)` | 122 |
| `initVdi()` | 124 |
| `configureVdiAccessRequest()` | 125 |
| `perfTimer()` | 147 |

**Private structs defined in header:**

| Struct | Lines |
|---|---|
| `BusConfig` | 64–69 |
| `PgnConfig` | 71–79 |
| `SpnConfig` | 81–92 |
| `AttConfig` | 94–106 |

**Private data members:**

| Member | Type |
|---|---|
| `m_canBus` | `EM070::CanBus *` |
| `m_timer` | `QTimer *` |
| `m_file` | `QFile` |
| `m_canCrc32` | `quint32` |
| `m_enabled` | `bool` |
| `m_busConfig` | `BusConfig` |
| `m_pgnConfigs[CAN_MAX_PGN_IDX]` | `PgnConfig[]` |
| `m_spnConfigs[CAN_MAX_SPN_IDX]` | `SpnConfig[]` |
| `m_attConfigs[CAN_MAX_ATT_IDX]` | `AttConfig[]` |
| `m_attrToSpn` | `QMap<quint8, quint8>` |
| `m_spnState[CAN_MAX_SPN_IDX]` | `quint32[]` |
| `m_perfCounter` | `quint32` |
| `m_perfTimer` | `QTimer *` |
| `m_vdiAccess` | `bool` |
| `m_vdiInhibit` | `bool` |

---

### 1.2 `comm/canmonitor.cpp`

**File-scope structs (migration helpers):**

| Struct | Lines | Purpose |
|---|---|---|
| `SpnConfig0` | 53–61 | Original `cancfg.dat` SPN layout (quint16 spn) |
| `SpnConfig1` | 64–72 | Version 1 `cancfgnew.dat` SPN layout (quint32 spn) |

**File-scope `#define` macros:**

| Macro | Line | Value |
|---|---|---|
| `PERF_MON` | 13 | `0` |
| `CAN_CONF_FILE_OLD` | 15 | `"cancfg.dat"` |
| `CAN_CONF_FILE` | 16 | `"cancfgnew.dat"` |
| `RULE_SEAT_U/L` | 18–19 | `LE_INT` patterns |
| `RULE_TRAC_U/L` | 20–21 | `LE_INT` patterns |
| `RULE_HYDR_U/L` | 22–23 | `LE_INT` patterns |
| `RULE_HYDL_U/L` | 24–25 | `LE_INT` patterns |
| `RULE_HRS_U/L` | 26–27 | `LE_INT` patterns |
| `RULE_BACD_U/L` | 28–29 | `LE_INT` patterns |
| `RULE_BLAN_U/L` | 30–31 | `LE_INT` patterns |
| `RULE_SEAT_RATE` | 33 | `(2 * 1000)` |
| `RULE_TRAC_RATE` | 34 | `(2 * 1000)` |
| `RULE_HYDR_RATE` | 35 | `(2 * 1000)` |
| `RULE_HYDL_RATE` | 36 | `(2 * 1000)` |
| `RULE_BLAN_RATE` | 37 | `(2 * 1000)` |
| `RULE_HRS_RATE` | 38 | `(1*60*1000)` |
| `RULE_BACD_RATE` | 39 | `(1*60*1000)` |
| `LIN_CANID_OFFSET` | 41 | `0x10` |
| `LIN_ADDR_OFFSET` | 42 | `0x4000` |
| `BYD_CANID_XOR` | 44 | `0x380` |
| `BYD_ADDR_OFFSET` | 45 | `0x0B000000` |
| `UPDATE_DEFER` | 47 | `3000` |

**Functions defined in canmonitor.cpp:**

| Function | Line |
|---|---|
| `CanMonitor::CanMonitor(CanBus *canbus)` | 74 |
| `CanMonitor::perfTimer()` | 101 |
| `CanMonitor::readCanConfig()` | 107 |
| `CanMonitor::readOldCanConfig()` | 209 |
| `CanMonitor::saveCanConfig()` | 265 |
| `CanMonitor::setEnabled(bool enable)` | 295 |
| `CanMonitor::calculateCanCrc()` | 310 |
| `CanMonitor::findPgnIndex(quint32 rspId, quint32 reqId) const` | 418 |
| `CanMonitor::newPgnIndex() const` | 437 |
| `CanMonitor::childSpnIndexes(quint8 pgnIndex) const` | 447 |
| `CanMonitor::clearCanConfig()` | 469 |
| `CanMonitor::canBusConfig() const` | 488 |
| `CanMonitor::setCanBusConfig(const QByteArray &config)` | 498 |
| `CanMonitor::canPgnConfig() const` | 531 |
| `CanMonitor::setCanPgnConfig(const QByteArray &config)` | 566 |
| `CanMonitor::canSpnConfig() const` | 615 |
| `CanMonitor::setCanSpnConfig(const QByteArray &config)` | 642 |
| `CanMonitor::canAttConfig() const` | 705 |
| `CanMonitor::setCanAttConfig(const QByteArray &config)` | 752 |
| `CanMonitor::canLinConfig() const` | 828 |
| `CanMonitor::setCanLinConfig(const QByteArray &config)` | 857 |
| `CanMonitor::canBydConfig() const` | 947 |
| `CanMonitor::setCanBydConfig(const QByteArray &config)` | 976 |
| `CanMonitor::canLin2Config() const` | 1064 |
| `CanMonitor::setCanLin2Config(const QByteArray &config)` | 1097 |
| `CanMonitor::attributePollingRate(quint32 namePattern) const` | 1193 |
| `CanMonitor::createRequest(quint8 spnIndex, quint32 pollingRate)` | 1231 |
| `CanMonitor::updateBusConfig()` | 1301 |
| `CanMonitor::updateRequests()` | 1313 |
| `CanMonitor::readCanFrame(quint32 id, const QByteArray &ba)` | 1369 |
| `CanMonitor::updateState(quint8 spnIndex, quint64 data)` | 1474 |
| `CanMonitor::updateSpnState(quint8 spnIndex, quint64 data)` | 1526 |
| `CanMonitor::initVdi()` | 1600 |
| `CanMonitor::setVdiAccess(bool access, bool inhibit)` | 1616 |
| `CanMonitor::configureVdiAccessRequest()` | 1627 |
| `CanMonitor::enableVdi(bool enable)` | 1648 |

---

### 1.3 `comm/canstatehandler.h`

**Class:** `CanStateHandler` (inherits `QObject`)

**Enum defined:**

| Enum | Values | Line |
|---|---|---|
| `DigitalFormat` | `SessionFormat`, `UsageFormat`, `OnDemandFormat` | 14 |

**Methods:**

| Function / Method | Line |
|---|---|
| `CanStateHandler(CanMonitor *canMonitor)` (constructor) | 16 |
| `updateIdleTimer()` | 17 |
| `canStates(DigitalFormat format, bool autoReset)` | 18 |
| `resetStates(bool resetLast)` | 19 |
| **signals:** `idleTimeout()` | 22 |
| `updateState(quint8 index, quint32 state)` (private) | 45 |

**Private struct defined in header:**

| Struct | Lines |
|---|---|
| `CanState` | 25–43 |

**Private data members:**

| Member | Type |
|---|---|
| `m_canStates[CAN_MAX_ATT_IDX]` | `CanState[]` |
| `m_canMonitor` | `CanMonitor *` |
| `m_timer` | `QTimer *` |

---

### 1.4 `comm/canstatehandler.cpp`

**Functions defined:**

| Function | Line |
|---|---|
| `CanStateHandler::CanStateHandler(CanMonitor *monitor)` | 14 |
| `CanStateHandler::updateState(quint8 index, quint32 state)` | 24 |
| `CanStateHandler::resetStates(bool resetLast)` | 73 |
| `CanStateHandler::updateIdleTimer()` | 91 |
| `CanStateHandler::canStates(DigitalFormat format, bool autoReset)` | 117 |

---

## 2. Findings

---

**A08-1** · MEDIUM · Large block of commented-out debug code inside `calculateCanCrc()`

**Description:** Lines 312–336 of `canmonitor.cpp` contain a commented-out struct definition and seven commented-out `memcpy`/`SerialLogger` lines inside the `calculateCanCrc()` function body. These were apparently left over from a debugging session that explored an alternative CRC computation strategy. The volume of dead comment noise obscures the active code path and makes the function difficult to read at a glance.

```cpp
// canmonitor.cpp lines 312–336
        /*struct {
            BusConfig busConfig;
            ...
        } config;*/

        //memset(&config, 0, sizeof(config));
        //memcpy(&config.busConfig, ...);
        ...
        //m_canCrc32 = GlobalConfigs::crc32(&config, sizeof(config));
```

**Fix:** Delete all commented-out code between lines 312 and 336. If the alternative code path is ever needed, version control history preserves it.

---

**A08-2** · LOW · Commented-out code in `setEnabled()` and `updateState()`

**Description:**
- `canmonitor.cpp` line 304: `//emit resetCanStates();` — a signal emission is silenced inside `setEnabled()`.
- `canmonitor.cpp` line 1476: `//qDebug() << "updateState(..."` — diagnostic log left commented out.
- `canmonitor.cpp` line 1528: `//qDebug() << "updateSpnState(..."` — same pattern.

These are individually minor but create confusion about whether the emit on line 304 was intentionally removed or accidentally silenced.

**Fix:** Remove the commented-out `qDebug` lines. For the silenced signal emission, add a code comment explaining the deliberate omission or restore it if it was accidentally removed.

---

**A08-3** · LOW · Commented-out code in `canstatehandler.cpp` (`memset` call, line 80)

**Description:** `canstatehandler.cpp` line 80 contains `//memset(m_canStates, 0, sizeof(m_canStates));` immediately after the selective-reset loop. The active code was refactored to be selective but the original bulk `memset` was never deleted.

```cpp
// canstatehandler.cpp line 80
    //memset(m_canStates, 0, sizeof(m_canStates));
```

**Fix:** Delete the commented-out line.

---

**A08-4** · MEDIUM · Disabled feature macro `DEPENDS_ON_TRIGGER` left as a comment block

**Description:** `canstatehandler.cpp` lines 8–12 contain a `TODO` comment followed by `//#define DEPENDS_ON_TRIGGER`. The macro is referenced at three more points in the file (lines 30–33, 80–86, 129–135) via `#ifdef`/`#ifndef` guards. The feature is unconditionally disabled at compile time — the disabled path is never compiled — yet the entire conditional framework is retained. This inflates cognitive complexity with code that is always dead in production builds.

**Fix:** Either commit to removing `DEPENDS_ON_TRIGGER` and its guarded blocks, or restore the macro and the TODO to an issue tracker and remove the comment block. Do not leave permanently-disabled conditional compilation blocks in production source.

---

**A08-5** · MEDIUM · Dead `#if 0` block in `updateSpnState()` — unreachable alternative algorithm

**Description:** `canmonitor.cpp` lines 1540–1545 wrap an alternative bit-extraction algorithm in `#if 0`:

```cpp
#if 0
    // LSB first for offset
    spnData = data >> spnConfig.offset;
    spnData &= spnMask;
#else
    // MSB first for offset
    ...
#endif
```

The `#if 0` block will never be compiled. Its presence suggests an experimental change was never cleaned up.

**Fix:** Delete the `#if 0` block and the surrounding `#if 0 / #else / #endif` scaffolding, leaving only the active `#else` branch. The comment "MSB first for offset" should be retained inline.

---

**A08-6** · LOW · Dead `#if 1` block in `clearCanConfig()` — always-active conditional

**Description:** `canmonitor.cpp` lines 478–482 contain:

```cpp
#if 1   // default setting to do
    m_busConfig.protocol = LindeExtended;
    m_busConfig.baudRate = 250000;
    m_busConfig.enabled  = true;
#endif
```

An `#if 1` block is always compiled. The comment "default setting to do" implies this was meant to be temporary. The conditional wrapper is misleading because it implies the block could be disabled.

**Fix:** Remove the `#if 1` / `#endif` wrapper and leave the three assignment statements as unconditional code, or promote the literals to named constants.

---

**A08-7** · MEDIUM · Magic number `64` for idle input source embedded in `updateIdleTimer()`

**Description:** `canstatehandler.cpp` line 99 compares `gCfg->idleInputSource()` against the literal `64`. The comment on lines 93–96 explains the meaning: "64 means input is CAN SEAT state." This is a protocol/specification constant that should be named.

```cpp
if (!gCfg->idleTimeout() || !gCfg->currentDriverId() ||
        gCfg->idleInputSource() != 64) {
```

**Fix:** Define `constexpr int CAN_IDLE_INPUT_SOURCE_SEAT = 64;` (or equivalent) in `cigconfigs.h` and replace the literal.

---

**A08-8** · MEDIUM · Magic numbers for VDI CAN IDs and byte payloads in `updateRequests()` and `configureVdiAccessRequest()`

**Description:** Several raw CAN identifiers and payload bytes appear as bare integer literals with no named constant:

- `canmonitor.cpp` line 1361: `m_canBus->addRequest(0x000, ba, 1000)` — VDI enable node message to ID `0x000`.
- `canmonitor.cpp` lines 1638–1643: payload bytes `0x05`, `0x01`, `0x00` representing access-mode states sent to ID `0x215` (line 1635, also a magic number).
- `canmonitor.cpp` line 1242: `6 << 26 | 234 << 16 | 255 << 8` — J1939 request PGN components with raw field values.

These are protocol-specific constants that are impossible to understand without the specification. Their repetition across encode and decode paths also risks inconsistency if the values ever change.

**Fix:** Define named constants (e.g., `VDI_ENABLE_NODE_ID`, `VDI_ACCESS_REQUEST_ID`, `VDI_ACCESS_INHIBIT_BYTE`, `J1939_REQUEST_PRIORITY`, `J1939_REQUEST_PF`, `J1939_REQUEST_PS`) and replace all occurrences.

---

**A08-9** · MEDIUM · Unreachable `return 0` statement at end of `attributePollingRate()`

**Description:** `canmonitor.cpp` lines 1224–1228:

```cpp
    default:
        return 0;
    }

    return 0;   // <-- unreachable
```

The `switch` covers every path including `default: return 0`. The statement after the closing brace of the switch is never reached. Compilers with `-Wunreachable-code` will warn on this.

**Fix:** Delete the trailing `return 0;` on line 1228.

---

**A08-10** · LOW · Commented-out `RULE_HRS_RATE` and `RULE_BACD_RATE` commented-out alternative values

**Description:** `canmonitor.cpp` lines 38–39:

```cpp
#define RULE_HRS_RATE       (1*60*1000)//(10 * 60 * 1000)
#define RULE_BACD_RATE      (1*60*1000)//(10 * 60 * 1000)
```

The original 10-minute values are retained as inline comments after the active 1-minute values. This implies a recent tuning change where the old value was never cleaned up. The inline comment is adjacent to the macro value in a way that risks misreading the effective value.

**Fix:** Delete the `// (10 * 60 * 1000)` suffixes. If the reasoning for the change is important, record it in a commit message or a separate code comment on the next line.

---

**A08-11** · HIGH · Private wire-protocol structs exposed in public header, creating tight coupling

**Description:** `canmonitor.h` defines four private structs — `BusConfig`, `PgnConfig`, `SpnConfig`, and `AttConfig` — in the `private:` section of the class header. These structs encode the exact on-disk binary layout of the CAN configuration file (field widths, alignment attributes, protocol-specific overlap via unions). Because these struct definitions live in the header, any translation unit that `#include`s `canmonitor.h` is compiled with knowledge of the full binary format.

`canstatehandler.h` similarly declares its private `CanState` struct (with its `time`/`count` union) in the header rather than in an implementation-local file.

This is a leaky abstraction: the internal serialisation layout becomes an implicit part of the public interface. Any change to a struct field (e.g., widening `SpnConfig::spn` from `quint32` to `quint64` in version 2) forces recompilation of every dependent TU even if the public API is unchanged, and risks ABI surprises if the struct is ever passed across a library boundary.

**Fix:** Move `BusConfig`, `PgnConfig`, `SpnConfig`, `AttConfig` (and `CanState`) to an anonymous namespace or a forward-declared private implementation struct (`Pimpl`) inside the `.cpp` files. The public header should expose only opaque handles or typed enumerations. At minimum, document with a prominent comment that these structs are serialised to disk and must not be changed without a format-version bump.

---

**A08-12** · LOW · Naming inconsistency: constructor parameter `canbus` vs. member `m_canBus`

**Description:** In `canmonitor.cpp` line 74, the constructor parameter is spelled `canbus` (lower camel, no separator), while the stored member is `m_canBus` (camel with capital B). The Qt-style convention used throughout the rest of the codebase spells multi-word identifiers with an upper-case word boundary. The constructor parameter should follow the same convention for readability.

**Fix:** Rename the constructor parameter from `canbus` to `canBus` to match the member naming convention.

---

**A08-13** · LOW · Inconsistent brace style for single-statement `if` bodies in `enableVdi()`

**Description:** `canmonitor.cpp` lines 1650–1656:

```cpp
void CanMonitor::enableVdi(bool enable)
{
    if (enable)
    {
        initVdi();
    } else {
        clearCanConfig();
    }
}
```

The `if` body uses Allman style (opening brace on its own line) while the `else` body uses K&R style (opening brace on same line). The rest of the file consistently uses K&R for class methods. This is purely a style inconsistency.

**Fix:** Normalise to K&R style: `if (enable) {` on the same line as the condition.

---

**A08-14** · LOW · Typo in comment: "idenitifer" (twice) and "consistant"

**Description:**
- `canmonitor.h` line 84: `// SPN idenitifer` (should be "identifier").
- `canmonitor.cpp` line 56: `// SPN idenitifer` (same typo in `SpnConfig0`).
- `canmonitor.cpp` line 1020: `// but address 0 is an exception which is consistant` (should be "consistent").

**Fix:** Correct the three spelling errors.

---

**A08-15** · MEDIUM · Signed/unsigned comparison and implicit narrowing in `readCanFrame()` loop index

**Description:** `canmonitor.cpp` lines 1375–1385:

```cpp
int pgnIndex;
for (pgnIndex = 0; pgnIndex < CAN_MAX_PGN_IDX; ++pgnIndex) {
```

`pgnIndex` is declared as `int` (signed), but `CAN_MAX_PGN_IDX` is a preprocessor integer constant (effectively `int`-typed in this context). Immediately after the loop, the same `pgnIndex` (now possibly equal to `CAN_MAX_PGN_IDX`) is compared with `CAN_MAX_PGN_IDX` and then used to index `m_pgnConfigs[]` (line 1377), which accepts `int`. However, in `childSpnIndexes()` and related helpers the index type is `quint8`, and `findPgnIndex()` returns `quint8`. The inconsistency — some helpers return/accept `quint8` and some use `int` — means index values are silently narrowed at call sites. With `CAN_MAX_PGN_IDX = 10` and `CAN_MAX_SPN_IDX = 20` the narrowing is safe today, but this is fragile.

**Fix:** Standardise on a single index type for all PGN/SPN index variables. Using `int` for loop variables and explicit `static_cast<quint8>` at boundaries is acceptable; the important fix is consistency. Consider a `using PgnIndex = quint8;` type alias to make intent explicit.

---

**A08-16** · LOW · `qDebug()` left active in hot receive path (`updateState()`, line 1522)

**Description:** `canmonitor.cpp` line 1522:

```cpp
qDebug() << "CAN Name/State:" << attr.name << attState;
```

This `qDebug()` call is in the `updateState()` method that is invoked on every received CAN frame that triggers an attribute change. In a production build without `QT_NO_DEBUG_OUTPUT`, this will emit to stderr (or a debug sink) on every state change, potentially flooding logs and degrading performance. The companion lines at 1476 and 1528 were at least commented out; this one was not.

**Fix:** Either wrap the call in `#ifdef QT_DEBUG` or remove it. If it is intentionally left for field diagnosis, route it through `SerialLogger` (already used elsewhere in this file) so it can be gated by a runtime flag.

---

## 3. Summary Table

| ID | Severity | Title |
|---|---|---|
| A08-1 | MEDIUM | Large commented-out struct and memcpy block in `calculateCanCrc()` |
| A08-2 | LOW | Commented-out signal emit and qDebug lines in `setEnabled()`/`updateState()` |
| A08-3 | LOW | Commented-out bulk `memset` in `resetStates()` |
| A08-4 | MEDIUM | Permanently-disabled `DEPENDS_ON_TRIGGER` conditional compilation |
| A08-5 | MEDIUM | Dead `#if 0` alternative algorithm in `updateSpnState()` |
| A08-6 | LOW | Misleading `#if 1` wrapper in `clearCanConfig()` |
| A08-7 | MEDIUM | Magic number `64` for CAN SEAT idle-input source |
| A08-8 | MEDIUM | Magic numbers for VDI CAN IDs and J1939 request frame components |
| A08-9 | MEDIUM | Unreachable `return 0` after switch in `attributePollingRate()` |
| A08-10 | LOW | Commented-out alternative rate values inline on `#define` lines |
| A08-11 | HIGH | Private wire-protocol structs exposed in public headers (leaky abstraction) |
| A08-12 | LOW | Naming inconsistency: constructor parameter `canbus` vs member `m_canBus` |
| A08-13 | LOW | Inconsistent brace style in `enableVdi()` |
| A08-14 | LOW | Typos in comments: "idenitifer" and "consistant" |
| A08-15 | MEDIUM | Signed/unsigned index-type inconsistency across PGN/SPN helpers |
| A08-16 | LOW | Active `qDebug()` in hot CAN-frame receive path (`updateState()`) |

**Totals:** 1 HIGH, 6 MEDIUM, 9 LOW
# Pass 4 Agent A09 — Code Quality

**Audit run:** 2026-02-28-01
**Branch:** master
**Reviewer:** Pass 4 Agent A09
**Files reviewed:**
- `comm/ftpclient.h`
- `comm/ftpclient.cpp`
- `comm/gmtpchat.h`
- `comm/gmtpchat.cpp`

---

## Reading Evidence

### `comm/ftpclient.h`

**Class:** `FtpClient` (extends `QObject`)

**Public methods:**

| Line | Signature |
|------|-----------|
| 17 | `explicit FtpClient(BackgroundWorker *parent)` |
| 18 | `void download(const QUrl &url)` |
| 19 | `void startTransfer()` |
| 21 | `void writeQueue()` |
| 22 | `void readQueue()` |
| 24 | `void setPowerState(CIGCONF::PowerState state)` |

**Signals:**

| Line | Signature |
|------|-----------|
| 27 | `void fileUpdated(const QString &fileName)` |
| 28 | `void sendGmtpMessage(CIGCONF::GmtpMessage msg, const QByteArray &extra)` |
| 29 | `void nextTransfer()` |

**Private methods:**

| Line | Signature |
|------|-----------|
| 32 | `void readData()` |
| 33 | `void downloadFinished()` |
| 34 | `void setReport(CIGCONF::FtpErrorCode errorCode)` |
| 35 | `void popQueue()` |

**Private members:**

| Line | Name | Type |
|------|------|------|
| 37 | `m_worker` | `BackgroundWorker *` |
| 38 | `m_manager` | `QNetworkAccessManager *` |
| 39 | `m_url` | `QUrl` |
| 40 | `m_file` | `QSaveFile` |
| 41 | `m_fileSize` | `quint32` |
| 43 | `m_transferInProgress` | `bool` |
| 45 | `m_queue` | `QQueue<QUrl>` |
| 46 | `m_retries` | `quint32` |
| 47 | `m_queueFile` | `bool` |
| 48 | `m_powerState` | `CIGCONF::PowerState` |

**Types / constants defined in `ftpclient.cpp`:**

| Line | Name | Value |
|------|------|-------|
| 14 | `MAX_FILE_SIZE` | `16 * 1024 * 1024` (16 MiB) |
| 15 | `FTP_QUEUE_FILE` | `"/home/ftpqueue.txt"` |
| 16 | `FTP_RETRIES` | `5` |

---

### `comm/gmtpchat.h`

**Class:** `GmtpChat` (extends `QObject`)

**Enums:**

| Name | Values |
|------|--------|
| `Priority` | `NormalPriority = 0`, `HighPriority = 1` (line 18) |
| `PduType` | `PduId = 1`, `PduData = 2`, `PduIdExt = 3`, `PduDataExt = 4`, `PduAck = 5` (line 19) |

**Public methods:**

| Line | Signature |
|------|-----------|
| 21 | `explicit GmtpChat(ModemChat *parent)` |
| 22 | `void setPowerState(CIGCONF::PowerState state)` |
| 23 | `void connectServer()` |
| 24 | `void sendMessage(const QByteArray &msgData, Priority priority = NormalPriority)` |
| 25 | `void sendAck(quint16 msgId)` |
| 26 | `void clearGMTPMsgQueue()` |
| 27 | `bool sleeping()` (inline) |
| 28 | `void setEthernetState(bool up)` (inline) |
| 29 | `bool acksRemaining()` (inline) |

**Signals:**

| Line | Signature |
|------|-----------|
| 32 | `void cmdReceived(const QByteArray &ba)` |
| 33 | `void socketStateChanged(bool state)` |
| 34 | `void allMessagesSent()` |
| 35 | `void allAcksSent()` |
| 36 | `void gmtpHotStartReconnect()` |
| 37 | `void disconnectSocket()` |

**Private methods:**

| Line | Signature |
|------|-----------|
| 40 | `void readToQueue()` |
| 41 | `void writeQueue(bool recent)` |
| 42 | `void onConnected()` |
| 43 | `void onDisconnected()` |
| 44 | `void reconnectServer()` |
| 45 | `void readSocket()` |
| 46 | `void writeSocket()` |
| 47 | `void bytesWritten(qint64 bytes)` |
| 49 | `QByteArray packedMessage(const QByteArray &msgData, PduType type = PduDataExt, quint16 ackId = 0)` |
| 50 | `void setOnIgnitionOffDisconnect(bool state)` |
| 51 | `void disconnectFromHost()` |

**Private members:**

| Line | Name | Type |
|------|------|------|
| 53 | `m_modemChat` | `ModemChat *` |
| 54 | `m_tcpSocket` | `QTcpSocket *` |
| 55 | `m_socketTimer` | `QTimer *` |
| 56 | `m_uploadTimer` | `QTimer *` |
| 57 | `m_ackTimer` | `QTimer *` |
| 58 | `m_powerState` | `CIGCONF::PowerState` |
| 60 | `m_serverIndex` | `int` |
| 61 | `m_gmtpFileIndexes` | `QList<quint32>` |
| 63 | `m_uploadMessages` | `QQueue<QByteArray>` |
| 64 | `m_recentMessages` | `QQueue<QByteArray>` |
| 65 | `m_ackMessages` | `QQueue<QByteArray>` |
| 67 | `m_sendingMessage` | `QByteArray` |
| 68 | `m_downloadMessage` | `QByteArray` |
| 70 | `m_msgId` | `quint16` |
| 71 | `m_ackId` | `quint16` |
| 72 | `m_retryCount` | `quint8` |
| 73 | `m_reconnectCount` | `quint8` |
| 74 | `m_idSent` | `bool` |
| 75 | `m_connect` | `bool` |
| 76 | `m_ethState` | `bool` |
| 77 | `m_onIgnitionOffDisconnect` | `bool` |
| 78 | `m_mutexConnectToHost` | `QMutex` |
| 79 | `m_mutexWriteSocket` | `QMutex` |
| 80 | `m_mutexDisconnectFromHost` | `QMutex` |

**Constants defined in `gmtpchat.cpp`:**

| Line | Name | Value |
|------|------|-------|
| 16 | `MAX_MESSAGE_CNT` | `1000` |
| 17 | `MAX_RETRIES` | `3` |
| 18 | `DEF_MSOCKET_TIMEOUT` | `10000` (ms) |
| 19 | `MAX_GMTP_RECONNECT_CNT` | `20` |

---

## Findings

---

**A09-1** · HIGH · `ByteArray::asprintf` re-uses invalidated `va_list`

**Description:** In `utils/bytearray.h` (used extensively in both files), `ByteArray::asprintf` calls `va_start`/`va_end`, then calls `vsprintf` with the same `ap` after `va_end` has already been called on it (the two-pass pattern is broken: `va_end` is called after `vsnprintf` but before `vsprintf`, making the second use of `ap` undefined behaviour per C11 7.16). Every `ByteArray::asprintf(...)` call in `ftpclient.cpp` (lines 71, 89, 96, 206, 208, 259, 275) and `gmtpchat.cpp` (lines 67, 201, 231, 352, 415, 457, 482, 498) is therefore producing undefined behaviour at runtime. This is a latent data-corruption bug that may silently truncate or garble log/GMTP messages.

**Fix:** In `ByteArray::asprintf`, call `va_start` a second time before the `vsprintf` call (add `va_start(ap, cformat)` before `vsprintf` and a matching `va_end(ap)` after it), or rewrite using `QByteArray::asprintf` (Qt 5.5+) which handles this correctly.

---

**A09-2** · HIGH · Large commented-out code blocks leave dead logic in `gmtpchat.cpp`

**Description:** Several substantial blocks of logic have been commented out but left in the source, creating noise and indicating unresolved design decisions:
- Lines 89–106: An entire `if/else` branch for `m_onIgnitionOffDisconnect` hot-start reconnect logic is commented out inside `connectServer()`. The surrounding braces and the `// }` closing markers remain, indicating this was originally a structural else-branch.
- Lines 187–191: The companion power-state guard in `onDisconnected()` is also commented out.
- Lines 136 in `reconnectServer()`: `//m_modemChat->detach();` — a replaced call left as a comment rather than removed.
- Line 97 in `connectServer()`: `//SerialLogger::log(...)` — a debug log line.
- Lines 267, 315, 328, 337 in `gmtpchat.cpp`: Multiple `SerialLogger::log` hex-dump calls commented out.

The `setOnIgnitionOffDisconnect` private method (lines 516–519) and the `m_onIgnitionOffDisconnect` member variable exist solely to support the commented-out logic. They are otherwise dead code.

**Fix:** Either restore the intended logic behind the comment-out and remove the guards, or delete the commented-out blocks, the `setOnIgnitionOffDisconnect` method, and the `m_onIgnitionOffDisconnect` member entirely. Prefer deletion — version control preserves history.

---

**A09-3** · MEDIUM · `writeQueue()` / `readQueue()` are public on `FtpClient` with no documented contract

**Description:** `FtpClient::writeQueue()` and `FtpClient::readQueue()` are declared `public` in the header (lines 21–22). Internally they manipulate the transfer queue and persistence file; calling them externally in the wrong order (e.g., `readQueue()` while a transfer is in progress) would corrupt `m_retries` and the queue state. There is no documented reason for these to be public — inspection of the codebase shows they are only called from within `FtpClient` itself (`startTransfer()` calls `readQueue()`; `setPowerState()` calls `writeQueue()`).

**Fix:** Demote both methods to `private`.

---

**A09-4** · MEDIUM · `FtpClient::startTransfer()` is public but is only ever called via the `nextTransfer` signal

**Description:** `startTransfer()` is declared `public` (line 19) and is connected to `nextTransfer` internally (constructor line 26). No external caller exists in the codebase. Calling it externally while `m_transferInProgress` is true is silently a no-op; calling it from a different thread would be a data race. The method should be private (or a private slot).

**Fix:** Declare `startTransfer()` as a `private` slot (add it under a `private slots:` section or use the `connect` with a lambda).

---

**A09-5** · MEDIUM · `PduType` enum exposed in `GmtpChat` public interface but belongs to internal wire protocol

**Description:** `GmtpChat::PduType` (`PduId`, `PduData`, `PduIdExt`, `PduDataExt`, `PduAck`) is a public enum (header line 19) that describes the GMTP wire-protocol PDU type field. It is used only internally by `packedMessage()` and `readSocket()`. Exposing it in the public interface leaks the wire-format details to callers and creates an unnecessary coupling point.

**Fix:** Move `PduType` to the private section of the class declaration, or forward-declare it in the `.cpp` file as a file-local enum.

---

**A09-6** · MEDIUM · Magic number `6` repeated throughout `gmtpchat.cpp` without a named constant

**Description:** The GMTP PDU header size (2 bytes type + 2 bytes msg ID + 2 bytes length = 6 bytes) appears as the bare integer `6` in at least seven locations: lines 333, 342, 349, 353, 372, 468, 469, 474, 475. There is no named constant such as `GMTP_HEADER_SIZE`. If the header layout ever changes, all sites must be found and updated manually.

**Fix:** Define `static constexpr int GMTP_HEADER_SIZE = 6;` (or a `#define`) and replace every literal `6` that refers to the PDU header with that constant.

---

**A09-7** · MEDIUM · `GmtpChat::sendAck()` is public but invokes internal protocol machinery

**Description:** `sendAck(quint16 msgId)` is a public method (header line 25). It constructs a `PduAck` PDU and queues it for transmission. Callers need to know server-assigned message IDs — a protocol-level detail — to use it correctly. Inspecting the codebase, `sendAck` is called only from `readSocket()` (line 347), which is itself private. The public exposure creates an unnecessary surface for misuse.

**Fix:** Demote `sendAck` to `private`. The ACK response is an implementation detail of the receive loop.

---

**A09-8** · MEDIUM · Double semicolon on `writeQueue` local variable declaration (`ftpclient.cpp` line 124)

**Description:** Line 124 reads `QFile file(FTP_QUEUE_FILE);;` — two consecutive semicolons. This is syntactically harmless (the second `;` is an empty statement) but is a style error that indicates copy-paste or editing slippage and may confuse static analysis tools.

**Fix:** Remove the duplicate semicolon.

---

**A09-9** · MEDIUM · `readSocket()` silently discards unknown PDU types one byte at a time

**Description:** In `gmtpchat.cpp` lines 371–373, when a received PDU type is neither `PduDataExt` nor `PduAck`, the code removes exactly one byte (`ba.remove(0,1)`) and retries. This is a framing-resync heuristic. No log message is emitted; no error counter is incremented. A corrupt or unexpected PDU type will cause the loop to spin silently, consuming the buffer byte-by-byte. This masks protocol errors and makes field diagnosis very difficult.

**Fix:** Log a warning (at least at `SerialLogger` level) when an unexpected type is encountered, and consider recording a metric or emitting a diagnostic signal. If the protocol guarantees well-formed frames, consider aborting and reconnecting instead.

---

**A09-10** · LOW · `m_serverIndex` typed as `int` while compared against `GMTP_SERVER_CNT` (unsigned)

**Description:** `m_serverIndex` is declared as `int` (header line 60), but it is used in an unsigned comparison against `GMTP_SERVER_CNT` (value 3) at `gmtpchat.cpp` line 129 (`if (++m_serverIndex >= GMTP_SERVER_CNT)`). A signed/unsigned comparison warning will be generated by compilers with `-Wsign-compare`. While it cannot go negative in practice, the type mismatch is inconsistent with the surrounding `quint8`/`quint16` usage.

**Fix:** Change `m_serverIndex` to `int` with an explicit `static_cast<int>(GMTP_SERVER_CNT)` comparison, or change it to `quint8` / `quint32` to match the unsigned context.

---

**A09-11** · LOW · Inline method bodies in `gmtpchat.h` mix logic with class declaration

**Description:** Three public methods are defined inline in the header (lines 27–29): `sleeping()`, `setEthernetState(bool)`, and `acksRemaining()`. While `sleeping()` and `acksRemaining()` are trivial getters, `setEthernetState` contains a side-effect (emitting `disconnectSocket()`) with a guarded branch. Inline logic in headers makes the interface harder to read and can surprise callers who do not expect a signal emission from a setter.

**Fix:** Move `setEthernetState` to the `.cpp` file. Keep the two pure getters inline only if consistency with the rest of the codebase demands it.

---

**A09-12** · LOW · `using namespace CIGCONF` at file scope in `gmtpchat.cpp`

**Description:** Line 20 of `gmtpchat.cpp` declares `using namespace CIGCONF;` at file scope. This pulls every name from that namespace into the translation unit, increasing the risk of accidental name shadowing or collisions as the namespace grows. The remainder of the codebase (including `ftpclient.cpp`) uses the fully qualified `CIGCONF::` prefix consistently.

**Fix:** Remove the `using namespace CIGCONF;` directive and qualify all references with `CIGCONF::`, consistent with the rest of the codebase.

---

**A09-13** · LOW · Commented-out code in `ftpclient.cpp` lines 38–39

**Description:** Inside `FtpClient::download()`, lines 38–39 contain:
```cpp
//setReport(CIGCONF::FtpGenericError);
```
This commented-out call was presumably the original behaviour when the network is not available: report an error immediately. The code was silently removed, leaving only a `return` with no notification. The comment has no associated ticket reference or explanation.

**Fix:** Either restore the `setReport` call with appropriate justification, or delete the comment. Add a code comment explaining why no error is reported when the network is down (i.e., the URL is queued and will retry later).

---

**A09-14** · LOW · `reconnectCount` overflow silently wraps

**Description:** `m_reconnectCount` is `quint8` (max 255, header line 73). In `reconnectServer()` (line 134), the check is `if (m_reconnectCount > MAX_GMTP_RECONNECT_CNT)` (20). After triggering, it resets to 0 (line 135) then immediately increments to 1 (line 140), so the logic works today. However, if the reset were removed or the check changed, `quint8` wraps at 256. Using `quint8` for a counter compared against an `int` constant also generates a compiler sign/size warning. Additionally `m_reconnectCount` is initialised to `1` in the constructor (not `0`), which means the very first connection attempt already counts as reconnect attempt #1, which is misleading.

**Fix:** Initialise `m_reconnectCount` to `0`. Consider using `quint32` or `int` to avoid overflow-related surprises.

---

**A09-15** · LOW · `FtpClient::downloadFinished()` line 259 — GMTP message key mismatch

**Description:** At line 259, the "no more retries" GMTP monitoring message is keyed as `"FTPF_DL_NO_MORE_RETRIES"` but the accompanying log message at line 258 says `"File transfer failed ... no more retries"`. However, this branch is reached only when `m_retries < FTP_RETRIES` (i.e., there *are* retries remaining — it is the retry-in-progress path). The GMTP key name `FTPF_DL_NO_MORE_RETRIES` is semantically incorrect for this branch; that key is used when retries are exhausted (which is the branch at line 253–256 that uses no such key). The misleading constant name will confuse server-side log analysis.

**Fix:** Rename the monitoring message key to `FTPF_DL_RETRY` or similar to accurately describe the retry-in-progress case.

---

**A09-16** · INFO · Timer interval constants are bare integer literals in constructor

**Description:** In `GmtpChat`'s constructor (`gmtpchat.cpp` lines 41–43), three timers are assigned intervals: `5000` ms (socket timer), `1000` ms (upload timer), `10000` ms (ACK timer). Only the ACK timer value is captured in the named constant `DEF_MSOCKET_TIMEOUT` (which equals `10000` — but this constant is used in `reconnectServer()` / `connectServer()` for the socket reconnect timer, not the ACK timer). The `5000` and `1000` values are truly bare literals with no named constant.

**Fix:** Introduce named constants (e.g., `GMTP_SOCKET_TIMEOUT_MS = 5000`, `GMTP_UPLOAD_INTERVAL_MS = 1000`) and use them in place of the literals.

---

**A09-17** · INFO · `GmtpChat::signal gmtpHotStartReconnect()` is declared but never emitted

**Description:** The signal `gmtpHotStartReconnect()` (header line 36) is never emitted anywhere in the codebase — the only location that would emit it is inside the commented-out block at `gmtpchat.cpp` lines 91–93. The signal declaration is dead code that cannot be used until the hot-start logic is restored.

**Fix:** Either restore the hot-start reconnect logic or remove the signal declaration.

---

## Summary Table

| ID | Severity | Title |
|----|----------|-------|
| A09-1 | HIGH | `ByteArray::asprintf` re-uses invalidated `va_list` (UB) |
| A09-2 | HIGH | Large commented-out code blocks with dead `setOnIgnitionOffDisconnect` |
| A09-3 | MEDIUM | `writeQueue()`/`readQueue()` unnecessarily public on `FtpClient` |
| A09-4 | MEDIUM | `FtpClient::startTransfer()` unnecessarily public |
| A09-5 | MEDIUM | `PduType` wire-protocol enum exposed in public interface |
| A09-6 | MEDIUM | Magic number `6` (PDU header size) repeated without named constant |
| A09-7 | MEDIUM | `sendAck()` unnecessarily public; leaks protocol details |
| A09-8 | MEDIUM | Double semicolon at `ftpclient.cpp` line 124 |
| A09-9 | MEDIUM | Silent byte-by-byte resync on unknown PDU type in `readSocket()` |
| A09-10 | LOW | `m_serverIndex` signed/unsigned mismatch with `GMTP_SERVER_CNT` |
| A09-11 | LOW | Inline side-effect method `setEthernetState` in header |
| A09-12 | LOW | `using namespace CIGCONF` at file scope in `gmtpchat.cpp` |
| A09-13 | LOW | Commented-out `setReport` call in `FtpClient::download()` |
| A09-14 | LOW | `m_reconnectCount` initialised to 1, `quint8` overflow risk |
| A09-15 | LOW | GMTP monitoring key `FTPF_DL_NO_MORE_RETRIES` used on retry-in-progress path |
| A09-16 | INFO | Bare timer interval literals in `GmtpChat` constructor |
| A09-17 | INFO | Signal `gmtpHotStartReconnect()` declared but never emitted |
# Pass 4 Agent A10 — Code Quality

**Audit run:** 2026-02-28-01
**Branch:** master
**Files reviewed:**
- `comm/modemchat.h`
- `comm/modemchat.cpp`
- `comm/ntpsync.h`
- `comm/ntpsync.cpp`

---

## Reading Evidence

### `comm/modemchat.h`

**Class:** `ModemChat` (inherits `QObject`)

**Enum defined:**
| Enum | Values |
|------|--------|
| `NetworkState` | `NetworkStopped(0)`, `NetworkHome(1)`, `NetworkSearching(2)`, `NetworkDenied(3)`, `NetworkUnknown(4)`, `NetworkRoaming(5)` |

**Struct defined (private):**
| Struct | Fields |
|--------|--------|
| `apnData` | `QString apn`, `QString apnUser`, `QString apnPassword` |

**Public methods / accessors:**
| Line | Name |
|------|------|
| 24 | `ModemChat(EM070::ModemPort *modemPort)` (constructor) |
| 25 | `void portStateChanged(bool open)` |
| 26 | `void setGnssEnabled(bool enable)` |
| 27 | `void rssiRefresh()` |
| 28 | `void qmiCheck()` |
| 29 | `void networkCheck()` |
| 30 | `void updateApn()` |
| 31 | `void detach(bool send = true)` |
| 32 | `void requestDetach()` |
| 34 | `const QByteArray &cgmi() const` |
| 35 | `const QByteArray &cgmm() const` |
| 36 | `const QByteArray &cgmr() const` |
| 37 | `const QByteArray &cgsn() const` |
| 38 | `const QByteArray &iccid() const` |
| 39 | `const QByteArray &rssi() const` |
| 40 | `const QByteArray &mobileOperator() const` |
| 41 | `const QByteArray &moni() const` |
| 42 | `NetworkState networkState() const` |
| 43 | `bool isEthernetReady() const` |

**Private methods:**
| Line | Name |
|------|------|
| 56 | `void sendChat(bool timeout = false)` |
| 57 | `void popChat()` |
| 58 | `void pushChat(const QByteArray &chat)` |
| 59 | `void noResponse()` |
| 60 | `void parseResponse(bool result, const QByteArrayList &content)` |
| 61 | `void selectAPN()` |
| 62 | `void updateEthernetState(bool connected)` |
| 63 | `void reconnectNetwork()` |
| 64 | `void onUqmiProcessComplete(int exitCode, QProcess::ExitStatus exitStatus)` |
| 65 | `void onProcessTimeout()` |
| 66 | `void resetReconnectFlag()` |
| 69 | `int args(const QByteArrayList &content, QGenericArgument val1, QGenericArgument val2, QGenericArgument val3, QGenericArgument val4)` |

**Constants (macros in modemchat.cpp):**
| Macro | Value | Meaning |
|-------|-------|---------|
| `RETRY_WAIT` | 500 | ms between retries |
| `RETRIES_PER_SEC` | 1000/500 = 2 | retries per second |
| `ACK_TIMEOUT` | 3000 | ms to wait for AT response |
| `RSSI_INTERVAL` | 10000 | ms between RSSI polls |
| `QMI_INTERVAL` | 2000 | ms between QMI polls |
| `NETWORK_INTERVAL` | 2000 | ms between network checks |
| `NETWORK_TIMEOUT` | 90 | ticks (= 180 s) before detach |
| `MONOGOTO_PREFIX_SIZE` | 5 | ICCID prefix length for Monogoto |
| `MAX_QMI_FAILURE_COUNT` | 7 | max successive QMI failures |
| `PROCESS_MAX_WAIT_TIMEOUT` | 10000 | ms to wait for uqmi process start |
| `MAX_CGDCONT` | 5 | max APN-set retries |

---

### `comm/ntpsync.h`

**Class:** `NtpSync` (inherits `QObject`)

**Public methods:**
| Line | Name |
|------|------|
| 14 | `NtpSync(ModemChat *parent)` (constructor) |
| 15 | `void connectServer()` |
| 16 | `void abortConnection()` |

**Signals:**
| Line | Name |
|------|------|
| 19 | `void synchronized(bool yes)` |

**Private methods:**
| Line | Name |
|------|------|
| 22 | `void writeSocket()` |
| 23 | `void readSocket()` |

**Constants (macros in ntpsync.cpp):**
| Macro | Value | Meaning |
|-------|-------|---------|
| `EPOCH_DIFF` | `0x83aa7e80UL` | Seconds between NTP epoch (1900) and Unix epoch (1970) |

---

## Findings

---

**A10-1** · HIGH · Large commented-out block in `portStateChanged` obscures active code path selection

**Description:** Lines 85-101 in `modemchat.cpp` contain a multi-line commented-out `if/else` block that was apparently the predecessor to the current runtime branch selected in `parseResponse` after `AT+CGMM` is received. The commented block mixes initialization commands that now appear elsewhere with subtly different ordering. Its continued presence creates confusion about intent: it is unclear whether the dead block is aspirational, superseded, or a rollback option. It also misrepresents the actual startup sequence to any reader.

```cpp
// comm/modemchat.cpp lines 85-101
// if (m_modemPort->isWwx()) {
//     m_chatCmds << "AT+CGDCONT?"
//                << "AT#MONI"
//                << "AT+CSQ";
// } else {
//     m_chatCmds << "AT+CSQ"
//             << "AT+CGCONTRDP="
//            << "AT+CGDCONT?"
//            << "AT#PDPAUTH?"
//            << "AT+COPS?"
//            << "AT+CGATT?"
//            << "AT+CGREG?"
//            << "AT#MONI"
//            << "AT+CSQ"
//            << "AT#ECM?"
//            << "AT#ECMC?";
//}
```

**Fix:** Remove the commented-out block entirely. If needed for reference, it is preserved in version control history.

---

**A10-2** · MEDIUM · Additional scattered commented-out code throughout `modemchat.cpp`

**Description:** Multiple other commented-out lines are spread throughout the file and create noise:

- Line 110-111: `// m_ethernetState = false;` / `// emit ethernetStateChanged(false);` — superseded by `updateEthernetState(false)` on line 112 but left in place.
- Lines 320, 342-344: `//QProcess::execute(...)` and `//m_qmiTimer->start(...)` / `//m_rssiTimer->start(...)` inside `updateApn()` and `detach()`.
- Lines 503-504: `// selectAPN();` / `// QProcess::execute(...)` inside `parseResponse` for `AT+CGDCONT?`.
- Lines 609-610: `// m_ethernetState = true;` / `// emit ethernetStateChanged(true);` in `AT#ECMC?` handler.
- Lines 615: `// m_ethernetState = false;` in same handler.
- Lines 674-685: Commented-out `pushChat` calls inside the `+CGEV:` handler.
- Line 224-225: Commented-out `m_chatCmds << "AT#MONI"` / `sendChat()` in `updateEthernetState`.

**Fix:** Purge all commented-out statements. Where genuinely uncertain code is being held in reserve, move it to a named helper or document the reason it is retained with a TODO/FIXME tag with a ticket reference.

---

**A10-3** · MEDIUM · AT-command strings and modem vendor mnemonics leak into the public interface

**Description:** The public methods `detach()`, `requestDetach()`, `updateApn()`, `rssiRefresh()`, and `qmiCheck()` are named after modem operations or internal AT-command concepts. The public accessors `cgmi()`, `cgmm()`, `cgmr()`, `cgsn()`, `iccid()`, and `moni()` directly expose AT-command names (CGMI, CGMM, CGMR, CGSN, ICCID, MONI) as the public API of the class. Callers are required to know what `cgmr` or `moni` mean, which are raw modem AT-command names. This is a leaky abstraction: the hardware-protocol layer bleeds through to any consumer of `ModemChat`.

**Fix:** Rename public accessors and methods to domain-meaningful names. Examples: `cgmi()` -> `manufacturerId()`, `cgmm()` -> `modelId()`, `cgmr()` -> `revisionId()`, `cgsn()` -> `imei()`, `moni()` -> `cellInfo()`. Rename `detach()` / `requestDetach()` to `disconnectNetwork()` / `requestNetworkDisconnect()`.

---

**A10-4** · MEDIUM · `args()` uses `QGenericArgument` / `Q_ARG` for a purely internal parsing helper — inappropriate API

**Description:** `ModemChat::args()` (header line 69, impl line 696) uses the Qt meta-object `QGenericArgument` mechanism (`Q_ARG`, `val.name()`, `val.data()`) to pass typed output parameters. This mechanism is designed for `QMetaObject::invokeMethod` dynamic dispatch and is explicitly noted in the Qt docs as not type-safe. The class's own header comment (`// to save the parsing time, only QByteArray/QString/int/bool are supported`) acknowledges the limitation. A plain overload set or a small `struct` would be safer and clearer.

**Fix:** Replace the `args()` helper with either (a) a set of typed overloads, (b) a `struct ParseResult` return type, or (c) a small template helper that avoids `QGenericArgument` entirely. At minimum, document the constraint more prominently and add a `static_assert` or runtime check that rejects unsupported types rather than silently misinterpreting them.

---

**A10-5** · MEDIUM · Shadow variable `isWwx` declared inside `AT#USBCFG?` branch obscures outer declaration

**Description:** In `parseResponse()`, `isWwx` is declared at line 371 for use throughout the function. Inside the `AT#USBCFG?` handler at line 440, a second `bool isWwx = m_modemPort->isWwx();` is declared, shadowing the outer variable. The inner re-declaration is redundant (same value) and on a compiler with `-Wshadow` this produces a warning.

```cpp
// Line 371 (outer):
bool isWwx = m_modemPort->isWwx();
// ...
// Line 440 (inner shadow, inside if-block for AT#USBCFG?):
bool isWwx = m_modemPort->isWwx();
```

**Fix:** Remove the inner `bool isWwx` declaration at line 440; the outer `isWwx` is already in scope and holds the same value.

---

**A10-6** · MEDIUM · Logic bug: `bool` validation in `args()` uses `||` instead of `&&` — always true

**Description:** In `modemchat.cpp` at line 749:

```cpp
if (val >= 0 || val <= 1)
    * (bool *) valDatas[i] = val;
else
    return i;
```

The condition `val >= 0 || val <= 1` is a tautology — it is always true for any integer (every integer is either >= 0 or <= 1). The intent is clearly to accept only values 0 or 1, which requires `val >= 0 && val <= 1`. The `else` branch that rejects out-of-range values is therefore dead/unreachable code.

**Fix:** Change `||` to `&&`:
```cpp
if (val >= 0 && val <= 1)
    * (bool *) valDatas[i] = val;
else
    return i;
```

---

**A10-7** · MEDIUM · `updateApn()` has inconsistent indentation — `else` branch body not indented

**Description:** The `else` branch of `updateApn()` at lines 321-333 is not indented relative to the enclosing `if/else`, making the code's structure misleading:

```cpp
void ModemChat::updateApn()
{
    if (m_modemPort->isWwx()) {
        pushChat("AT+CGDCONT?");
        //QProcess::execute(...);
    } else {
    pushChat("AT#ECMC?");   // <- should be indented
    pushChat("AT#ECM?");
    ...
    sendChat();
}
}
```

The closing brace alignment is also wrong: the function's closing `}` appears on a line by itself at column 0 after the `else` block's `}`, which compiles correctly but is highly misleading.

**Fix:** Re-indent the `else` block body consistently. Both branches should use 4-space (or one tab) indentation. Run the file through `clang-format` with the project's style settings.

---

**A10-8** · LOW · Magic number `0x0b` in `writeSocket()` with no named constant or comment

**Description:** In `ntpsync.cpp` line 65:

```cpp
ba[0] = 0x0b;
```

This byte encodes the NTP packet LI/VN/Mode field: LI=0 (no warning), VN=1 (version 1), Mode=3 (client). The value `0x0b` is opaque and non-obvious. Any reader maintaining the code must know NTP packet structure to understand it.

**Fix:** Replace with a named constant and comment:
```cpp
// NTP packet: LI=0 (no leap warning), VN=1, Mode=3 (client)
static const quint8 NTP_LI_VN_MODE = 0x0b;
ba[0] = NTP_LI_VN_MODE;
```
Also note that NTP version 1 is ancient; NTP version 4 (`0x1b`) is standard. Consider whether the server supports v1.

---

**A10-9** · LOW · Magic number `123` (NTP port) used inline without a named constant

**Description:** In `ntpsync.cpp` line 50 and referenced in the log message at line 62:

```cpp
m_udpSocket->connectToHost(gCfg->timeServerAddress(), 123);
```

Port 123 is the well-known NTP port, but it should be a named constant for readability and maintainability.

**Fix:** Define `static const quint16 NTP_PORT = 123;` and use it in both the `connectToHost` call and the log message.

---

**A10-10** · LOW · Magic number `48` (NTP packet size) used without a named constant

**Description:** In `ntpsync.cpp` lines 64 and 75:

```cpp
QByteArray ba(48, 0);  // line 64
if (ba.size() < 48)    // line 75
```

48 bytes is the fixed NTP packet size. Having it as a bare literal in two places risks a discrepancy if one is ever changed.

**Fix:** Define `static const int NTP_PACKET_SIZE = 48;` and use it consistently.

---

**A10-11** · LOW · Comment in `connectServer()` has incorrect polarity — `// -1 means time has in sync yet`

**Description:** In `ntpsync.cpp` line 31:

```cpp
// -1 means time has in sync yet
if (m_syncTimes < 0) {
```

The comment appears to be a garbled version of "time has already synced" or "time is in sync". The word "yet" makes the sentence ambiguous/incorrect. The sentinel value -1 meaning "already synced" is a non-obvious convention.

**Fix:** Correct the comment: `// m_syncTimes == -1 means synchronisation already completed`. Consider replacing the sentinel `-1` with a named constant `static const int SYNC_COMPLETE = -1;` or a separate `bool m_synced` flag for clarity.

---

**A10-12** · LOW · `abortConnection()` silently resets `m_syncTimes` to 0 only when positive — inconsistent reset

**Description:** In `ntpsync.cpp` lines 54-58:

```cpp
void NtpSync::abortConnection()
{
    if (m_syncTimes > 0)
        m_syncTimes = 0;
    m_timer->stop();
}
```

If `m_syncTimes` is already 0 (never started) or -1 (already synced), the reset is skipped or suppressed. An abort when `m_syncTimes == -1` leaves the "already synced" sentinel in place; the next call to `connectServer()` would immediately re-emit `synchronized(true)` without actually connecting. Whether this is the desired behaviour is not documented.

**Fix:** Document the intended post-conditions of `abortConnection()` explicitly. If a full reset is desired (i.e., allow re-synchronisation after abort), set `m_syncTimes = 0` unconditionally. If re-sync after abort should be inhibited once already synced, add an explanatory comment.

---

**A10-13** · LOW · `MAX_QMI_FAILURE_COUNT` defined but never used

**Description:** In `modemchat.cpp` line 18:

```cpp
#define MAX_QMI_FAILURE_COUNT (7) //Approximately n x 2s timeout = n*2s successive failure
```

A search of the file shows this constant is never referenced anywhere in `modemchat.cpp` or `modemchat.h`. It appears to be dead configuration left from a previous implementation of QMI failure counting that was removed.

**Fix:** Remove the unused macro, or implement the failure counter logic it was intended to support.

---

**A10-14** · LOW · `m_networkState` member is never initialised in the constructor

**Description:** In `modemchat.h` the member `NetworkState m_networkState` is declared at line 94. The constructor initialiser list in `modemchat.cpp` (lines 24-40) does not initialise `m_networkState`. Because `NetworkState` is a plain `enum` (not `enum class`), it defaults to an indeterminate integer value if the object is allocated on the heap or in uninitialized storage. Any call to `networkState()` before `parseResponse` processes a `+CGREG?` response returns an undefined value.

**Fix:** Add `m_networkState(NetworkUnknown)` to the constructor initialiser list.

---

**A10-15** · LOW · `BE_INT` macro in `ntpsync.cpp` — first argument is a signed `char` used in a left-shift

**Description:** `ntpsync.cpp` line 78-79 uses `BE_INT(ba[32], ...)`. `ba` is a `QByteArray`; its `operator[]` returns `char`, which is signed on most platforms. The macro definition (`utils/bytearray.h` line 7) performs `(c1) << 24` — left-shifting a potentially negative signed `char` by 24 is undefined behaviour in C++ if `c1` is negative (i.e., byte value > 127). Only `c2`, `c3`, `c4` are cast to `uchar` inside the macro; `c1` is not.

```cpp
#define BE_INT(c1, c2, c3, c4)  ((c1) << 24 | (uchar)(c2) << 16 | (uchar)(c3) << 8 | (uchar)(c4))
```

**Fix:** Cast `c1` to `uchar` (or `quint8`) inside the macro before the shift:
```cpp
#define BE_INT(c1, c2, c3, c4)  ((uchar)(c1) << 24 | (uchar)(c2) << 16 | (uchar)(c3) << 8 | (uchar)(c4))
```

---

**A10-16** · LOW · `rssiRefresh()` enqueues commands but only calls `sendChat()` when queue size is exactly 2

**Description:** In `modemchat.cpp` lines 132-137:

```cpp
void ModemChat::rssiRefresh()
{
    m_chatCmds << "AT+CSQ";
    m_chatCmds << "AT#MONI";

    if (m_chatCmds.size() == 2)
        sendChat();
}
```

`sendChat()` is only called if the queue contained exactly zero commands before this function ran (i.e., size becomes exactly 2). If the queue already had any pending commands, the new commands are appended silently and `sendChat()` is not called from here. While `sendChat()` is called from `parseResponse()` after each command completes, the check `== 2` is fragile: if `rssiRefresh()` were ever modified to enqueue a third command, the `sendChat()` trigger would silently stop working.

**Fix:** Replace `m_chatCmds.size() == 2` with `m_chatCmds.size() == 2` being replaced by a named pre-count check:
```cpp
bool wasEmpty = m_chatCmds.isEmpty();
m_chatCmds << "AT+CSQ" << "AT#MONI";
if (wasEmpty)
    sendChat();
```

---

**A10-17** · INFO · Struct `apnData` uses lowercase name, inconsistent with Qt/project PascalCase convention

**Description:** In `modemchat.h` line 50, the private struct is named `apnData` (camelCase starting with lowercase), while all other types in the codebase use PascalCase (e.g., `ModemChat`, `NetworkState`, `NtpSync`). Qt coding style recommends PascalCase for all type names.

**Fix:** Rename to `ApnData` to match the surrounding naming convention.

---

**A10-18** · INFO · `vsprintf` call in `ByteArray::asprintf` (used by `modemchat.cpp`) uses a recycled `va_list` after `va_end`

**Description:** `utils/bytearray.h` lines 19-25 (used by `modemchat.cpp` via `ByteArray::asprintf`):

```cpp
va_start(ap, cformat);
size = vsnprintf(nullptr, 0, cformat, ap);
va_end(ap);

QByteArray ba;
ba.resize(size);
vsprintf(ba.data(), cformat, ap);  // ap was already va_end'd
```

After `va_end(ap)`, the `va_list` `ap` is indeterminate; passing it to `vsprintf` is undefined behaviour. A second `va_start` / `va_end` pair is required. This is a pre-existing issue in a utility used by this module.

**Fix:** Add a second `va_start(ap, cformat)` before the `vsprintf` call and a matching `va_end(ap)` after it.

---

## Summary Table

| ID | Severity | Title |
|----|----------|-------|
| A10-1 | HIGH | Large commented-out block in `portStateChanged` obscures code path |
| A10-2 | MEDIUM | Additional scattered commented-out code throughout modemchat.cpp |
| A10-3 | MEDIUM | AT-command names leak into public interface (leaky abstraction) |
| A10-4 | MEDIUM | `args()` uses `QGenericArgument` inappropriately for internal parsing |
| A10-5 | MEDIUM | Shadow variable `isWwx` redeclared inside AT#USBCFG? handler |
| A10-6 | MEDIUM | Logic bug in `args()`: tautological OR makes bool validation dead code |
| A10-7 | MEDIUM | `updateApn()` has incorrect indentation in `else` branch |
| A10-8 | LOW | Magic number `0x0b` NTP LI/VN/Mode byte with no named constant |
| A10-9 | LOW | Magic number `123` (NTP port) used inline |
| A10-10 | LOW | Magic number `48` (NTP packet size) repeated without named constant |
| A10-11 | LOW | Incorrect/garbled comment for sentinel value in `connectServer()` |
| A10-12 | LOW | `abortConnection()` inconsistently resets `m_syncTimes` |
| A10-13 | LOW | `MAX_QMI_FAILURE_COUNT` defined but never used (dead macro) |
| A10-14 | LOW | `m_networkState` not initialised in constructor |
| A10-15 | LOW | `BE_INT` macro shifts signed `char` — undefined behaviour for bytes > 127 |
| A10-16 | LOW | `rssiRefresh()` uses fragile queue-size check instead of was-empty check |
| A10-17 | INFO | Struct `apnData` uses non-PascalCase name |
| A10-18 | INFO | `ByteArray::asprintf` uses `va_list` after `va_end` (UB in shared utility) |
# Pass 4 Agent A11 — Code Quality

**Audit run:** 2026-02-28-01
**Branch:** master
**Files reviewed:**
- `main.cpp` (repo root: `C:/Projects/cig-audit/repos/mark3-pvd/main.cpp`)
- `mytranslator.h` (repo root: `C:/Projects/cig-audit/repos/mark3-pvd/mytranslator.h`)
- `mytranslator.cpp` (repo root: `C:/Projects/cig-audit/repos/mark3-pvd/mytranslator.cpp`)

---

## Reading Evidence

### `main.cpp`

**File purpose:** Application entry point. Initialises the Qt application, installs a key event filter, loads the locale, registers Qt meta-types, starts GPIO configuration via shell commands, creates the main `Dialog` UI, and spins up the `BackgroundWorker` on a dedicated `QThread`.

**Functions / methods:**

| Line | Name | Signature |
|------|------|-----------|
| 24 | `hideBootProgress` | `void hideBootProgress()` |
| 38 | `configureCrashLogging` | `void configureCrashLogging()` |
| 71 | `main` | `int main(int argc, char *argv[])` |

**Types / enums / constants defined:**

| Line | Kind | Name | Value |
|------|------|------|-------|
| 17 | Preprocessor macro (commented out) | `CONSTRAINED_MEMORY_TEST` | — |
| 20 | Preprocessor macro (conditional) | `MEMSZ` | `10*1024*1024` |
| 21 | Static global array (conditional) | `mem` | `static quint8 mem[MEMSZ]` |

**Namespace in scope:** `using namespace EM070;` (line 15)

---

### `mytranslator.h`

**File purpose:** Public interface for the application's translation subsystem. Declares the global `QTranslator` object and all free functions that load, update, query, and remove locale files.

**Functions declared:**

| Line | Name | Signature |
|------|------|-----------|
| 15 | `loadLocalLanguage` | `void loadLocalLanguage(void)` |
| 16 | `updateLocalLanguage` | `void updateLocalLanguage(const QString &arg1)` |
| 17 | `getCurrentLanguage` | `QString getCurrentLanguage(void)` |
| 18 | `queryLanguage` | `int queryLanguage(void)` |
| 19 | `setLanguage` | `int setLanguage(int local)` |
| 20 | `removeTranslator` | `void removeTranslator()` |

**Types / constants defined:**

| Line | Kind | Name | Value |
|------|------|------|-------|
| 11 | `const QString` (non-`inline`, header-level) | `langEnglish` | `"EN"` |
| 12 | `const QString` (non-`inline`, header-level) | `langSpanish` | `"ES"` |
| 14 | `extern` global object | `mTranslator` | `QTranslator` |

---

### `mytranslator.cpp`

**File purpose:** Implementation of the translation subsystem. Manages reading/writing a plain-text `local.dat` file to persist the selected language, and loading the corresponding Qt `.qm` translation file listed in the embedded `lang.dat` resource.

**Functions defined:**

| Line | Name | Notes |
|------|------|-------|
| 15 | `loadLocalLanguage` | Reads `local.dat`, looks up entry in `lang.dat`, installs `mTranslator`. Deletes `local.dat` if language not found. |
| 74 | `updateLocalLanguage` | Looks up language in `lang.dat`, installs `mTranslator`, writes `local.dat`. Removes file on miss. |
| 132 | `getCurrentLanguage` | Returns the two-letter language code for the active locale, defaulting to `langEnglish`. |
| 167 | `queryLanguage` | Maps language string to `QLocale::Language` integer; returns `-1` on unknown. |
| 177 | `setLanguage` | Calls `updateLocalLanguage` if locale differs from current; returns `-1` on unknown locale. |
| 190 | `removeTranslator` | Removes `mTranslator` from the application via `QCoreApplication::removeTranslator`. |

**Types / constants defined:**

| Line | Kind | Name | Value |
|------|------|------|-------|
| 7 | `const QString` (file-scope) | `localFile` | `"local.dat"` |
| 8 | `const QString` (file-scope) | `langFile` | `":/lang.dat"` |
| 10 | Global object definition | `mTranslator` | `QTranslator mTranslator;` |

---

## Findings

---

**A11-1** · MEDIUM · Global `QTranslator` object exposed through a header

**Description:** `mTranslator` is declared `extern` in `mytranslator.h` (line 14) and defined at translation-unit scope in `mytranslator.cpp` (line 10). Every translation unit that includes `mytranslator.h` can read or write the translator directly, bypassing the API. More critically, `QTranslator` inherits `QObject`, and `QObject` instances must not be constructed before `QApplication` exists. Because `mTranslator` is a namespace-scope (pre-`main`) object its constructor runs at static-initialisation time, before `QApplication a(argc, argv)` on line 78 of `main.cpp`. On platforms where Qt's internal state is not yet ready this is undefined behaviour.

**Fix:** Remove the `extern` declaration from the header. Make `mTranslator` a function-local static or a private member of a small `TranslatorManager` singleton initialised after `QApplication`. Expose only the six existing free-function signatures (which are already sufficient for all callers).

---

**A11-2** · LOW · Header-level `const QString` constants cause ODR issues across translation units

**Description:** `langEnglish` and `langSpanish` are defined as `const QString` at namespace scope directly in `mytranslator.h` (lines 11–12). Unlike `const int` or `constexpr`, `QString` is not an integral constant and is not `inline`. Every translation unit that includes this header gets its own definition (though the linker typically merges them under the One-Definition Rule). More important, each TU pays the cost of constructing and destructing a `QString` at static-init and static-deinit time. This is an anti-pattern for Qt applications.

**Fix:** Replace with `constexpr char` arrays or `inline const QString` (Qt 5.10+ / C++17), or move them to a `.cpp`-level `static const`. For example:

```cpp
// mytranslator.h
constexpr char langEnglish[] = "EN";
constexpr char langSpanish[] = "ES";
```

---

**A11-3** · LOW · `configureCrashLogging()` is a fully implemented function that is permanently commented out

**Description:** `configureCrashLogging()` (lines 38–69 of `main.cpp`) is a complete function that writes a shell script to `/mnt/sd/app_monitor` and starts it with `QProcess::startDetached`. Its call site on line 101 is commented out with no associated TODO or bug-reference comment. The function is compiled into the binary but never called, constituting dead code. The embedded shell script also leaks the internal product name `FleetFocus` into the binary image.

**Fix:** If crash-logging monitoring is not required for this release, remove both the function definition and its commented-out call site. If it is intended for a future release, add a JIRA/issue reference in the comment and guard it under an appropriate `#ifdef` (e.g., `#ifdef ENABLE_CRASH_MONITOR`).

---

**A11-4** · LOW · `CONSTRAINED_MEMORY_TEST` dead-code block is compiled in unconditionally (false branch always taken)

**Description:** Lines 17–22 and 102–105 of `main.cpp` define a preprocessor-guarded memory-stress test that allocates a 10 MB static array and locks it with `mlock`. The controlling macro `CONSTRAINED_MEMORY_TEST` is permanently commented out (line 17: `//#define CONSTRAINED_MEMORY_TEST`). The guarded block can never be entered. This is a development artifact that should not remain in the repository on the `master` / release branch.

**Fix:** Remove the `#define`, the `#ifdef` blocks, the static `mem` array, and the `#include <sys/mman.h>` if it is only needed by that block. If the test is still needed, move it to the test project (`mk3-test.pro`) rather than the production build.

---

**A11-5** · LOW · Commented-out GPIO shell command on line 108

**Description:** Line 108 of `main.cpp` contains a commented-out alternative approach for exporting GPIO 37:

```cpp
//int ret = QProcess::execute("echo 37 > /sys/class/gpio/export");
```

The equivalent shell-safe version immediately follows on line 109. The commented-out line is dead code and its stale variable `ret` (which was never checked) also indicates the original implementation was incomplete.

**Fix:** Remove the commented-out line. The active version on line 109 is the correct implementation.

---

**A11-6** · MEDIUM · `QTextStream::setCodec` is deprecated in Qt 5 and removed in Qt 6

**Description:** `setCodec("UTF-8")` is called on every `QTextStream` instance in `mytranslator.cpp` (lines 22, 29, 84, 115, 140, 147). `QTextStream::setCodec(const char *)` was deprecated in Qt 5.15 and removed in Qt 6. The project's `.pro` file (`mk3.pro`, line 30) enables `QT_DEPRECATED_WARNINGS`, meaning every build targeting Qt 5.15+ will emit compiler warnings for these six call sites. There is also a commented-out entry in `mk3.pro` (line 35) suggesting a future migration to Qt 6 has been considered.

**Fix:** Replace with `QTextStream::setEncoding(QStringConverter::Utf8)` (Qt 6 API). If Qt 5 compatibility must be retained, use a version-guarded wrapper:

```cpp
#if QT_VERSION < QT_VERSION_CHECK(6, 0, 0)
    stream.setCodec("UTF-8");
#else
    stream.setEncoding(QStringConverter::Utf8);
#endif
```

---

**A11-7** · LOW · `qsrand` / `qrand` are deprecated Qt APIs

**Description:** `qsrand(QDateTime::currentSecsSinceEpoch())` is called in `main.cpp` line 99. `qsrand` and its companion `qrand` (used in `ui/checkquestiondialog.cpp` line 24) were deprecated in Qt 5.15. They wrap the C `srand`/`rand` functions, which are not thread-safe. With `QT_DEPRECATED_WARNINGS` enabled in `mk3.pro`, these produce build warnings.

**Fix:** Replace with `QRandomGenerator::global()->seed(...)` and `QRandomGenerator::global()->bounded(...)` respectively. Seeding the global generator is optional (it is auto-seeded from the OS); callers should simply call `QRandomGenerator::global()->bounded(n)` in place of `qrand() % n`.

---

**A11-8** · LOW · `endl` manipulator deprecated in Qt 5.15 / Qt 6 context

**Description:** `out << lang << endl;` on line 116 of `mytranslator.cpp` uses Qt's `endl` manipulator (imported via `<QTextStream>`). Qt's `endl` (distinct from `std::endl`) was deprecated in Qt 5.14. With `QT_DEPRECATED_WARNINGS` active, this is a build warning.

**Fix:** Replace with `Qt::endl` (available from Qt 5.14):

```cpp
out << lang << Qt::endl;
```

---

**A11-9** · INFO · Inconsistent naming convention: parameter `arg1` in public API

**Description:** The public function `updateLocalLanguage(const QString &arg1)` (header line 16, implementation line 74) uses the auto-generated Qt slot parameter name `arg1` rather than a descriptive name. All other parameters in the file use meaningful names (`lang`, `local`, `filename`). This reduces readability and is inconsistent with the rest of the codebase.

**Fix:** Rename the parameter to something descriptive, for example `languageCode` or `langCode`, in both the header declaration and the implementation.

---

**A11-10** · INFO · `loadLocalLanguage` closes `local` in only one branch; open file may be leaked on error path

**Description:** In `loadLocalLanguage` (lines 55–63 of `mytranslator.cpp`), the `QFile local` is closed only in the `isFound == true` branch. In the `isFound == false` branch the file is deleted via `local.remove()`. `QFile::remove()` does implicitly close on some Qt versions, but this behaviour is undocumented as guaranteed and differs from the explicit `close()` in the success path, creating an inconsistency that makes correctness reasoning harder.

**Fix:** Call `local.close()` unconditionally before the `if(isFound)` block, then call `local.remove()` in the false branch. This matches the pattern used in `updateLocalLanguage` (line 124) and makes the control flow symmetrical.

---

**A11-11** · INFO · `gCfg` macro defined in included header creates a leaky abstraction in `globalconfigs.h`

**Description:** `globalconfigs.h` (line 13) defines:

```cpp
#define gCfg GlobalConfigs::instance()
```

This macro is included transitively by a large portion of the codebase. Every call site that writes `gCfg->someMethod()` expands to `GlobalConfigs::instance()->someMethod()`, silently calling the singleton accessor on every use. Although this is not directly in the audited files, `main.cpp` pulls it in through `app/backgroundworker.h`. The macro hides the singleton pattern, prevents IDE navigation and refactoring, and makes it impossible to inject a mock for unit testing.

**Fix:** Remove the macro. Provide a named free function `GlobalConfigs *globalConfigs()` (or simply use `GlobalConfigs::instance()` at call sites). Where unit-testability is required, pass the instance as a constructor parameter.

---

## Summary Table

| ID | Severity | Title |
|----|----------|-------|
| A11-1 | MEDIUM | Global `QTranslator` object exposed through a header (pre-`QApplication` construction risk) |
| A11-2 | LOW | Header-level `const QString` constants — ODR concern and static-init overhead |
| A11-3 | LOW | `configureCrashLogging()` fully implemented but permanently commented out (dead code) |
| A11-4 | LOW | `CONSTRAINED_MEMORY_TEST` dead-code block left in production branch |
| A11-5 | LOW | Commented-out GPIO shell command on line 108 of `main.cpp` |
| A11-6 | MEDIUM | `QTextStream::setCodec` deprecated (Qt 5.15) / removed (Qt 6) — 6 call sites |
| A11-7 | LOW | `qsrand` / `qrand` deprecated in Qt 5.15; not thread-safe |
| A11-8 | LOW | `endl` manipulator deprecated in Qt 5.14 |
| A11-9 | INFO | Opaque parameter name `arg1` in public API `updateLocalLanguage` |
| A11-10 | INFO | `loadLocalLanguage` closes `QFile local` only in the success branch |
| A11-11 | INFO | `gCfg` macro in `globalconfigs.h` leaks singleton pattern across codebase |
# Pass 4 Agent A12 — Code Quality

**Audit run:** 2026-02-28-01
**Branch:** master
**Assigned files:**
- `platform/aescrypto.h`
- `platform/aescrypto.cpp`
- `platform/blecentral.h`
- `platform/blecentral.cpp`

---

## Reading Evidence

### `platform/aescrypto.h`

**Class:** `EM070::AesCrypto`

| Method / Member | Line | Notes |
|---|---|---|
| `static QByteArray encrypt(const QByteArray &in)` | 16 | Public static |
| `static QByteArray descrypt(const QByteArray &in)` | 17 | Public static (note: typo — should be `decrypt`) |
| `bool enableMtp()` | 20 | Private instance method |
| `QByteArray aes(const QByteArray &in, bool encrypt)` | 21 | Private instance method |
| `static bool m_mtpEnabled` | 22 | Private static member |

**Types / Enums / Constants:** none defined in the header.

**Namespace:** `EM070`

---

### `platform/aescrypto.cpp`

| Method | Line |
|---|---|
| `AesCrypto::enableMtp()` | 20 |
| `AesCrypto::aes(const QByteArray &in, bool encrypt)` | 63 |
| `AesCrypto::encrypt(const QByteArray &in)` | 150 |
| `AesCrypto::descrypt(const QByteArray &in)` | 156 |

**Constants / macros defined:**

| Symbol | Line | Value |
|---|---|---|
| `AF_ALG` | 10 | `38` (fallback `#ifndef` guard) |
| `SOL_ALG` | 13 | `279` (fallback `#ifndef` guard) |

**Platform guards:** all ARM-specific socket/crypto code wrapped in `#ifdef __arm__` (lines 2–6, 24–58, 67–145).

**Notable literals:**
- Hardcoded AES CBC IV at line 124: `"\x3d\xaf\xba\x42\x9d\x9e\xb4\x30\xb4\x22\xda\x80\x2c\x9f\xac\x41"` (16 bytes, fixed for all calls)
- Magic status bitmask at line 49: `0x1000014`, `0x3`

---

### `platform/blecentral.h`

**Classes (all in namespace `EM070`):**

1. **`CharacteristicInfo`** (inherits `QObject`) — lines 13–28
2. **`DescriptorInfo`** (inherits `QObject`) — lines 30–43
3. **`BleCentral`** (inherits `QObject`) — lines 45–126

**`CharacteristicInfo` methods:**

| Method | Line |
|---|---|
| Constructor `CharacteristicInfo(const QLowEnergyCharacteristic &, QLowEnergyService *)` | 17 |
| `QBluetoothUuid uuid() const` | 20 |
| `bool isReadable() const` | 21 |
| `bool isWritable() const` | 22 |
| `const QLowEnergyCharacteristic &characteristic() const` | 23 |
| `QLowEnergyService *parentService() const` | 24 |

**`DescriptorInfo` methods:**

| Method | Line |
|---|---|
| Constructor `DescriptorInfo(const QLowEnergyDescriptor &, CharacteristicInfo *)` | 34 |
| `QBluetoothUuid uuid() const` | 37 |
| `const QLowEnergyDescriptor &descriptor() const` | 38 |
| `const CharacteristicInfo *parentInfo() const` | 39 |

**`BleCentral` methods:**

| Method | Line | Type |
|---|---|---|
| Constructor `BleCentral(QObject *parent = nullptr)` | 51 | Public |
| `~BleCentral()` | 52 | Public |
| `void setEnabled(bool enable)` | 54 | Public |
| `void setPeripheralAddress(const quint64 &address)` | 56 | Public |
| `void setAuthorizationCode(const quint128 &uuid, const QByteArray &code)` | 57 | Public |
| `State state() const` | 59 | Public |
| `QByteArrayList servicesUuid() const` | 61 | Public |
| `QByteArrayList characteristicsUuid() const` | 62 | Public |
| `QByteArrayList descriptionsUuid() const` | 63 | Public |
| `bool readCharacteristic(const quint128 &uuid)` | 65 | Public |
| `bool writeCharacteristic(const quint128 &uuid, const QByteArray &ba)` | 66 | Public |
| `bool readDescriptor(const quint128 &uuid)` | 67 | Public |
| `bool writeDescriptor(const quint128 &uuid, const QByteArray &ba)` | 68 | Public |
| `const DescriptorInfo *descriptionInfo(const quint128 &uuid)` | 88 | Private |
| `const CharacteristicInfo *characteristicInfo(const quint128 &uuid)` | 89 | Private |
| `void startDeviceDiscovery()` | 91 | Private |
| `void connectToDevice()` | 92 | Private |
| `void addDevice(const QBluetoothDeviceInfo &)` | 95 | Private |
| `void deviceDiscoveryFinished()` | 96 | Private |
| `void deviceDiscoveryError(QBluetoothDeviceDiscoveryAgent::Error)` | 97 | Private |
| `void deviceConnected()` | 100 | Private |
| `void deviceDisconnected()` | 101 | Private |
| `void addService(const QBluetoothUuid &newService)` | 102 | Private |
| `void serviceDiscoveryFinished()` | 103 | Private |
| `void serviceStateChanged(QLowEnergyService::ServiceState newState)` | 106 | Private |

**Signals:**

| Signal | Line |
|---|---|
| `void accessible(bool yes)` | 71 |
| `void error(QBluetoothDeviceDiscoveryAgent::Error newError)` | 74 |
| `void error(QLowEnergyController::Error newError)` | 77 |
| `void error(QLowEnergyService::ServiceError newError)` | 80 |
| `void characteristicChanged(const quint128 &uuid, const QByteArray &newValue)` | 81 |
| `void characteristicRead(const quint128 &uuid, const QByteArray &value)` | 82 |
| `void characteristicWritten(const quint128 &uuid, const QByteArray &newValue)` | 83 |
| `void descriptorRead(const quint128 &uuid, const QByteArray &value)` | 84 |
| `void descriptorWritten(const quint128 &uuid, const QByteArray &newValue)` | 85 |

**Enum:**

| Enum | Values | Line |
|---|---|---|
| `BleCentral::State` | `Disabled, Discovering, Ready` | 49 |

**`#define` constants (`blecentral.cpp`):**

| Symbol | Line | Value |
|---|---|---|
| `DISCOVERY_RETRY_WAIT` | 7 | `3000` |
| `RECONNECT_RETRY_WAIT` | 8 | `2000` |
| `WAIT_FOR_CONNECTED` | 9 | `10000` |
| `WAIT_FOR_READY` | 10 | `30000` |

---

## Findings

---

**A12-1** · HIGH · Hardcoded AES IV — fixed IV destroys CBC security

**Description:** `aescrypto.cpp` line 124 embeds a literal 16-byte IV directly in the source:
```cpp
memcpy(iv->iv, "\x3d\xaf\xba\x42\x9d\x9e\xb4\x30\xb4\x22\xda\x80\x2c\x9f\xac\x41", 16);
```
CBC mode requires a unique, unpredictable IV for every encryption operation. Using the same IV for every call means that two identical plaintexts will always produce identical ciphertexts, and an adversary who observes multiple messages can detect repeated content. It also facilitates chosen-plaintext attacks. Even though the key is hardware-derived (MTP), the fixed IV leaks structural information. This is a well-known cryptographic misuse classified under CWE-329 (Not Using a Random IV with CBC Mode).

**Fix:** Generate a cryptographically random 16-byte IV per encryption call (e.g., via `/dev/urandom` or `RAND_bytes`), prepend it to the ciphertext, and read it back before decryption. Do not store or reuse the IV across calls.

---

**A12-2** · HIGH · Typo in public API: `descrypt` instead of `decrypt`

**Description:** `aescrypto.h` line 17 declares `static QByteArray descrypt(const QByteArray &in)`. This is a misspelling of `decrypt`. Although functionally minor, this identifier is part of the public API surface. Any caller already written against this name will silently continue with the misspelled symbol, and no compiler warning is raised. This also makes the API confusing to every future reader who must determine whether `descrypt` is intentional or erroneous.

**Fix:** Rename to `decrypt` throughout (`aescrypto.h` line 17 and `aescrypto.cpp` line 156). Update all call sites. If backward compatibility matters, add a deprecated alias.

---

**A12-3** · HIGH · `AesCrypto::aes()` silently returns empty `QByteArray` on non-ARM builds

**Description:** The entire implementation body of `AesCrypto::aes()` (lines 67–145) and `AesCrypto::enableMtp()` (lines 24–58) is guarded by `#ifdef __arm__`. On any non-ARM host (desktop build, CI, unit-test environment) both `encrypt()` and `descrypt()` silently return an empty `QByteArray`. There is no compile-time or run-time indication to the caller that the operation produced no output. This means data silently passes through as empty bytes on non-target builds, which could mask correctness defects in higher-level code.

**Fix:** Add a `static_assert` or `#error` for unsupported architectures, or emit a `qWarning()` / `Q_UNREACHABLE()` at the non-ARM fallback return so callers can detect the no-op at runtime. If a desktop stub is intentional, document it explicitly and have it return an error indicator rather than empty data.

---

**A12-4** · MEDIUM · C-style casts in `aescrypto.cpp`

**Description:** Lines 32–33 and 78–79 use C-style casts to strip `const` from string literals for `::strcpy`:
```cpp
::strcpy((char *) sa.salg_type, "skcipher");
::strcpy((char *) sa.salg_name, "mtp");
```
Line 116 uses a C-style cast to dereference control message data:
```cpp
* (__u32 *) CMSG_DATA(cmsg) = encrypt ? ALG_OP_ENCRYPT : ALG_OP_DECRYPT;
```
Line 122 similarly casts `CMSG_DATA(cmsg)` to `struct af_alg_iv *`. C-style casts bypass type-safety checks and hide the intent of the conversion (const-cast vs. reinterpret-cast vs. static-cast). They are a known source of subtle bugs and are flagged by `-Wold-style-cast`.

**Fix:** Replace C-style casts with explicit C++ casts (`reinterpret_cast`, `const_cast`, `static_cast`) appropriate to each context. For the `strcpy` calls, use `strncpy` (or safer Qt equivalents) with the correctly-typed buffer.

---

**A12-5** · MEDIUM · `strcpy` into fixed-size `sockaddr_alg` fields without bounds check

**Description:** Lines 32–33 and 78–79 use `::strcpy` to write into `sa.salg_type` and `sa.salg_name`, which are fixed-size character arrays (14 and 64 bytes respectively per `linux/if_alg.h`). While the literal strings used here (`"skcipher"`, `"mtp"`, `"cbc(aes)"`) are safely short, the pattern is dangerous and fragile: there is no bounds enforcement. A future developer who changes the algorithm name string to something longer will introduce a stack buffer overflow with no warning.

**Fix:** Replace `::strcpy` with `::strncpy` (or `std::memcpy`) paired with an explicit size limit equal to the field capacity, or use a safe wrapper that asserts the length at compile time.

---

**A12-6** · MEDIUM · Return value of `sendmsg()` and `read()` ignored in `aescrypto.cpp`

**Description:** Lines 134–135 and lines 140–141 call `sendmsg()` and `read()` without checking the return value:
```cpp
sendmsg(tfd, &msg, MSG_MORE);
read(tfd, ba.data() + i, 1024);
```
A failure of either call would silently produce a `QByteArray` containing uninitialised or stale data, which would then be passed back to the caller as if encryption had succeeded. This is a correctness and potential security issue: the caller cannot distinguish a successful encryption from a partial or failed one.

**Fix:** Check the return values of `sendmsg()` and `read()`. On error or short read/write, close the file descriptors, log an appropriate message, and return an empty or error-signalling `QByteArray`.

---

**A12-7** · MEDIUM · `AesCrypto` mixes static public API with instance state (`m_mtpEnabled`)

**Description:** `AesCrypto::encrypt()` and `AesCrypto::descrypt()` are public `static` methods, yet they internally construct a temporary `AesCrypto` instance (`AesCrypto aesCrypto`) to call the non-static `aes()` method. Meanwhile, `m_mtpEnabled` is a `static` member shared across all instances. This design is incoherent: the class simultaneously acts as a stateless utility (`static` public interface) and a stateful singleton (`static bool m_mtpEnabled`). The inconsistency makes the ownership and initialization semantics unclear and makes the class non-testable.

**Fix:** Decide on one design. If the class is meant to be a stateless utility, make `aes()`, `enableMtp()`, and `m_mtpEnabled` all static and remove the unnecessary instance creation. If it is meant to be a stateful object, remove `static` from the public interface and require callers to manage the object lifetime.

---

**A12-8** · MEDIUM · Commented-out code blocks in `blecentral.cpp`

**Description:** Multiple commented-out code blocks remain in production source:

- Line 30: `//connect(m_reconnectTimer, &QTimer::timeout, this, &BleCentral::connectToDevice);` — original reconnect logic replaced by a lambda, old connection left as a comment.
- Line 37: `);//&BleCentral::startDeviceDiscovery);` — inline comment fragment at the end of the lambda lambda block, residue of a previous refactor.
- Line 85: `//SerialLogger::log("[BLE:STATE] Starting device discovery\r\n");` — disabled logging statement.
- Lines 158, 161: `//if (m_previousAddress != m_device.address()) {` and `//}` — address-change guard removed but left commented.
- Lines 266, 272: Two `SerialLogger::log` calls disabled.

Commented-out code is a maintenance liability: it obscures intent, confuses reviewers, and can mislead static analysis tools.

**Fix:** Remove all commented-out code. If the address-change optimisation (lines 158/161) is intentionally deferred, document it with a `// TODO:` comment referencing a ticket. Use version control history rather than source comments to preserve old logic.

---

**A12-9** · MEDIUM · `SerialLogger::log()` called unconditionally at constructor time

**Description:** `blecentral.cpp` line 31 calls `SerialLogger::log("Reconnect timeout\r\n")` in the constructor body, immediately after a commented-out `connect()` call. This log statement appears to be debugging residue from the refactor that replaced `connectToDevice` with the inline lambda. It fires every time a `BleCentral` object is constructed, polluting the serial log with a message that has no associated event.

**Fix:** Remove the orphaned `SerialLogger::log("Reconnect timeout\r\n")` statement on line 31. If the intent is to log when the reconnect timer fires, move the log call inside the lambda body.

---

**A12-10** · MEDIUM · Duplicate `SerialLogger::log` call in `addDevice()`

**Description:** `blecentral.cpp` lines 115 and 121 both call `SerialLogger::log("[BLE:STATE] Device found MAC=...")` with identical content. Line 115 runs for every BLE device found (before the address filter), and line 121 runs again immediately after confirming the device address matches. This means the matching device address is logged twice with the same message, potentially causing confusion during log analysis.

**Fix:** Remove the duplicate on line 121 or differentiate the two messages (e.g., line 115: `"Device seen"`, line 121: `"Target device matched"`).

---

**A12-11** · MEDIUM · `requestConnectionUpdate()` called twice with identical parameters

**Description:** Identical `QLowEnergyConnectionParameters` blocks are set up and applied at both `deviceConnected()` (lines 185–189) and `serviceStateChanged()` when all services are discovered (lines 295–299):
```cpp
QLowEnergyConnectionParameters p;
p.setIntervalRange(15, 15);
p.setLatency(5);
p.setSupervisionTimeout(5000);
m_controller->requestConnectionUpdate(p);
```
This is a verbatim code duplication. The rationale for requesting the same parameters at two different lifecycle points is not documented. If the parameters ever need to change, they must be updated in two places.

**Fix:** Extract the connection parameters into a private helper method (e.g., `applyConnectionParameters()`) and call it from both locations. Optionally document why the update is repeated after service discovery.

---

**A12-12** · LOW · Magic number bitmasks in `enableMtp()` undocumented

**Description:** `aescrypto.cpp` lines 49 and 54 use magic integer constants with no explanatory comment:
```cpp
if (status == 0xffff || (status & 0x1000014)) { ... }
if ((status & 0x3) == 0x3) { ... }
```
The meaning of these bitmask values cannot be determined without reading the referenced kernel driver source (`nuc970-crypto.c`). Only a partial comment (lines 43–47) points to the driver, but the actual bit-field semantics are not explained.

**Fix:** Define named constants or enumerators for each bitmask (e.g., `MTP_STATUS_ERROR_MASK`, `MTP_STATUS_ENABLED_MASK`) and add a brief comment explaining what each bit represents per the kernel driver documentation.

---

**A12-13** · LOW · `AesCrypto` public header exposes no platform guard or capability check

**Description:** `aescrypto.h` presents a clean platform-neutral interface, but the implementation silently no-ops on non-ARM builds (see A12-3). There is no `#ifdef`, `Q_OS_LINUX`, or capability-query method in the header to signal to callers whether AES operations will actually work. A caller on a non-ARM host has no compile-time indication of this limitation.

**Fix:** Add a `static bool isSupported()` method (or equivalent `#if` guard) to the header so callers can detect at compile time or runtime whether the crypto subsystem is operational on the current platform.

---

**A12-14** · LOW · `BleCentral` `#define` timing constants should be `static constexpr`

**Description:** `blecentral.cpp` lines 7–10 define four timing constants using the C preprocessor:
```cpp
#define DISCOVERY_RETRY_WAIT    3000
#define RECONNECT_RETRY_WAIT    2000
#define WAIT_FOR_CONNECTED      10000
#define WAIT_FOR_READY          30000
```
Preprocessor macros have no type, no scope, and bypass the C++ type system. They cannot be inspected in a debugger and are replaced everywhere without regard to context.

**Fix:** Replace with `static constexpr int` (or `static constexpr std::chrono::milliseconds`) defined at the top of the `.cpp` file or in the class definition if they need to be accessed from tests.

---

**A12-15** · LOW · `m_serviceIndex` is uninitialized in the constructor member-initialization list

**Description:** `blecentral.h` declares `int m_serviceIndex` at line 125. The constructor in `blecentral.cpp` (lines 14–40) initializes `m_discoveryTimer`, `m_reconnectTimer`, `m_discoveryAgent`, `m_controller`, and `m_state` in its member-initialization list, but `m_serviceIndex` is not listed. It is first assigned at line 253 inside `serviceDiscoveryFinished()`. On compilers that do not zero-initialize plain members, `m_serviceIndex` holds an indeterminate value between object construction and the first call to `serviceDiscoveryFinished()`, which is a latent defect.

**Fix:** Add `m_serviceIndex(0)` to the constructor's member-initialization list.

---

**A12-16** · INFO · `cbuf` size calculation assumes `af_alg_iv.iv` overhead is exactly 4 bytes

**Description:** `aescrypto.cpp` line 99 allocates the control message buffer as:
```cpp
char cbuf[CMSG_SPACE(4) + CMSG_SPACE(20)];
```
The value `20` is `sizeof(struct af_alg_iv) + 16` = `4 + 16`. This relies on the implicit assumption that `struct af_alg_iv` (which contains `__u32 ivlen` and a flexible array `__u8 iv[]`) has exactly 4 bytes of overhead. This is true on current Linux ARM targets, but the calculation is fragile: it could silently break if the kernel struct layout changes or if compiled for a target with different alignment rules.

**Fix:** Replace `20` with `sizeof(struct af_alg_iv) + 16` to express the intent explicitly.

---

## Summary Table

| ID | Severity | Title |
|---|---|---|
| A12-1 | HIGH | Hardcoded AES IV — fixed IV destroys CBC security |
| A12-2 | HIGH | Typo in public API: `descrypt` instead of `decrypt` |
| A12-3 | HIGH | `AesCrypto::aes()` silently returns empty `QByteArray` on non-ARM builds |
| A12-4 | MEDIUM | C-style casts in `aescrypto.cpp` |
| A12-5 | MEDIUM | `strcpy` into fixed-size `sockaddr_alg` fields without bounds check |
| A12-6 | MEDIUM | Return values of `sendmsg()` and `read()` ignored |
| A12-7 | MEDIUM | `AesCrypto` mixes static public API with instance state (`m_mtpEnabled`) |
| A12-8 | MEDIUM | Commented-out code blocks in `blecentral.cpp` |
| A12-9 | MEDIUM | Orphaned `SerialLogger::log()` call in `BleCentral` constructor |
| A12-10 | MEDIUM | Duplicate `SerialLogger::log` call in `addDevice()` |
| A12-11 | MEDIUM | `requestConnectionUpdate()` duplicated verbatim at two lifecycle points |
| A12-12 | LOW | Magic number bitmasks in `enableMtp()` undocumented |
| A12-13 | LOW | `AesCrypto` public header exposes no platform guard or capability check |
| A12-14 | LOW | `BleCentral` timing `#define` constants should be `static constexpr` |
| A12-15 | LOW | `m_serviceIndex` uninitialized in constructor member-initialization list |
| A12-16 | INFO | `cbuf` size calculation uses implicit `af_alg_iv` overhead assumption |

**Totals:** 3 HIGH, 8 MEDIUM, 4 LOW, 1 INFO
# Pass 4 Agent A13 — Code Quality

**Audit run:** 2026-02-28-01
**Branch:** master
**Files reviewed:**
- `platform/canbus.h`
- `platform/canbus.cpp`
- `platform/gnssreceiver.h`
- `platform/gnssreceiver.cpp`

---

## Reading Evidence

### `platform/canbus.h`

**Class:** `EM070::CanBus` (extends `QObject`)

**Enums / Types / Constants:**

| Kind | Name | Location |
|------|------|----------|
| Enum | `CanDeviceId { CAN2, CAN1 }` | Line 16 |
| Struct | `Request { QCanBusFrame frame; quint32 interval; qint32 timer; }` | Lines 18–23 |

**Methods (public unless noted):**

| Line | Signature | Notes |
|------|-----------|-------|
| 25 | `explicit CanBus(CanDeviceId id = CAN1, QObject *parent = nullptr)` | Constructor |
| 26 | `~CanBus()` | Destructor |
| 28 | `void initialize()` | |
| 30 | `void setXferEnabled(bool enable)` | |
| 31 | `bool isXferEnabled() const` | Inline |
| 33 | `void setPower(bool on)` | |
| 34 | `bool isEnabled() const` | Inline |
| 36 | `bool setBaudRate(int baudRate)` | |
| 37 | `int baudRate() const` | Inline |
| 39 | `void addRequest(quint32 id, const QByteArray &ba, quint32 interval)` | |
| 40 | `QList<Request> getRequests()` | Non-const, returns by value |
| 41 | `void clearRequests()` | |
| 43 | `void addFilter(quint32 identifier)` | |
| 44 | `void clearFilters()` | |
| 45 | `void applyFilters()` | |
| 47 | `void writeFrameDirect(quint32 id, const QByteArray &ba)` | |
| 49 | `void removeRequests(quint32 id)` | |
| 54 | `void error(QCanBusDevice::CanBusError canBusError)` | Signal |
| 55 | `void read(quint32 identifier, const QByteArray &ba)` | Signal |
| 58 | `void sendRequest()` | Protected |
| 61 | `void readFrame()` | Private |
| 62 | `void handleError(QCanBusDevice::CanBusError error)` | Private |

**Commented-out code in header:**
- Line 22: `//int timerId;` — commented-out struct field inside `Request`
- Line 51: `//QCanBusDevice* canBusDevice() const {return m_canBusDevice;}` — commented-out accessor

---

### `platform/canbus.cpp`

**Macros / Constants defined:**

| Name | Value | Line |
|------|-------|------|
| `REQUEST_TIMER` | `100` | 14 |
| `CANBUS_DEBUG` | `0` | 15 |

**Methods (all are implementations of `EM070::CanBus`):**

| Line | Signature |
|------|-----------|
| 17 | `CanBus::CanBus(CanDeviceId id, QObject *parent)` |
| 28 | `CanBus::~CanBus()` |
| 34 | `void CanBus::initialize()` |
| 51 | `void CanBus::sendRequest()` |
| 89 | `void CanBus::setXferEnabled(bool enable)` |
| 105 | `void CanBus::setPower(bool on)` |
| 178 | `bool CanBus::setBaudRate(int baudRate)` |
| 193 | `void CanBus::addRequest(quint32 id, const QByteArray &ba, quint32 interval)` |
| 208 | `void CanBus::clearRequests()` |
| 214 | `void CanBus::addFilter(quint32 identifier)` |
| 219 | `void CanBus::clearFilters()` |
| 224 | `void CanBus::applyFilters()` |
| 258 | `void CanBus::writeFrameDirect(quint32 id, const QByteArray &ba)` |
| 264 | `void CanBus::readFrame()` |
| 274 | `void CanBus::handleError(QCanBusDevice::CanBusError canBusError)` |
| 285 | `void CanBus::removeRequests(quint32 id)` |

**Commented-out code in .cpp:**
- Line 116: `//return;` inside `setPower()` after gpio36 open failure
- Line 120: `//return;` inside `setPower()` after gpio38 open failure
- Line 148: `// return;` inside `setPower()` after `ip link set` failure

---

### `platform/gnssreceiver.h`

**Class:** `EM070::GnssReceiver` (extends `QObject`)

**Macros / Constants:**

| Name | Value | Line |
|------|-------|------|
| `MAX_POINTS` | `8` | 7 |

**Methods (public unless noted):**

| Line | Signature | Notes |
|------|-----------|-------|
| 17 | `explicit GnssReceiver(QObject *parent = nullptr)` | Constructor |
| 18 | `void portStateChanged(bool open)` | |
| 19 | `void reset()` | |
| 20 | `void changeUpdateTime()` | |
| 22 | `quint8 satelliteCount() const` | Inline |
| 23 | `qint32 latitude() const` | Inline |
| 24 | `qint32 longitude() const` | Inline |
| 25 | `qint32 lastLatitude() const` | Inline |
| 26 | `qint32 lastLongitude() const` | Inline |
| 27 | `qint16 speed() const` | Inline |
| 28 | `qint16 course() const` | Inline |
| 29 | `quint32 distance() const` | Inline |
| 30 | `quint32 sumOfDistance() const` | Inline |
| 31 | `quint32 altitude() const` | Inline |
| 32 | `bool locked() const` | Inline |
| 33 | `quint32 hpe() const` | Inline — performs HDOP-to-accuracy conversion inline |
| 34 | `quint32 hdop() const` | Inline |
| 35 | `qint64 age()` | Non-const |
| 36 | `quint8 warn() const` | Inline |
| 37 | `void setWarn(quint8 n)` | Inline |
| 38 | `quint8 quality() const` | Inline |
| 39 | `void setQuality(quint8 n)` | Inline |
| 40 | `quint16 markerCnt() const` | Inline |
| 41 | `void setMarkerCnt(quint16 n)` | Inline |
| 42 | `quint32 pathLatitude(int n)` | |
| 43 | `void setPathLatitude(int n, quint32 lat)` | |
| 44 | `quint32 pathLongitude(int n)` | |
| 45 | `void setPathLongitude(int n, quint32 lon)` | |
| 46 | `void gpsDebugPrint()` | |
| 47 | `bool inPoly2(const CIGCONF::gpsPosStruct *gpsPos, const CIGCONF::polygonStruct *polygon)` | **Declared, never defined — dead/broken** |
| 48 | `bool pointInPolygon(int polyCorners, CIGCONF::position me, CIGCONF::position *points)` | |
| 49 | `double degrees2radians(double degrees)` | |
| 51 | `void timerEvent(QTimerEvent *)` | Protected |
| 54 | `void sendGmtpMessage(CIGCONF::GmtpMessage msg, const QByteArray &extra = QByteArray())` | Signal |
| 57 | `void readData()` | Private |
| 58 | `void parseData(const QByteArray &ba)` | Private |
| 59 | `void cumulateDistance()` | Private |
| 60 | `static quint32 calculateDistance(qint32 lat1, qint32 lng1, qint32 lat2, qint32 lng2)` | Private static |

---

### `platform/gnssreceiver.cpp`

**Macros / Constants:**

| Name | Value | Line |
|------|-------|------|
| `FILE_GNSS_PORT` | `"/dev/ttyUSB1"` | 11 |
| `EARTH_R` | `6371000UL` | 13 |

**Methods:**

| Line | Signature |
|------|-----------|
| 17 | `GnssReceiver::GnssReceiver(QObject *parent)` |
| 44 | `void GnssReceiver::timerEvent(QTimerEvent *event)` |
| 51 | `void GnssReceiver::portStateChanged(bool open)` |
| 72 | `void GnssReceiver::readData()` |
| 101 | `void GnssReceiver::parseData(const QByteArray &ba)` |
| 192 | `void GnssReceiver::reset()` |
| 212 | `void GnssReceiver::changeUpdateTime()` |
| 222 | `void GnssReceiver::cumulateDistance()` |
| 339 | `quint32 GnssReceiver::calculateDistance(qint32 lat1, qint32 lng1, qint32 lat2, qint32 lng2)` |
| 369 | `quint32 GnssReceiver::pathLatitude(int n)` |
| 380 | `void GnssReceiver::setPathLatitude(int n, quint32 lat)` |
| 390 | `quint32 GnssReceiver::pathLongitude(int n)` |
| 401 | `void GnssReceiver::setPathLongitude(int n, quint32 lon)` |
| 409 | `void GnssReceiver::gpsDebugPrint()` |
| 424 | `double GnssReceiver::degrees2radians(double degrees)` |
| 428 | `bool GnssReceiver::pointInPolygon(int polyCorners, CIGCONF::position me, CIGCONF::position *points)` |
| 448 | `qint64 GnssReceiver::age()` |

**Commented-out code in .cpp:**
- Line 216: `//m_timerId = startTimer(gCfg->gpsUpdateTime() * 1000);` in `changeUpdateTime()`
- Line 224: `//qDebug() << ...` in `cumulateDistance()`
- Lines 123–126: Commented-out MK2 relay/geofence block inside `parseData()`
- Lines 314–317: Commented-out `MK2 RELAY CONTROL OP` block (first instance) in `cumulateDistance()`
- Lines 324–326: Commented-out `MK2 RELAY CONTROL OP` block (second instance) in `cumulateDistance()`
- Line 331: `//sendGmtpMessage(CIGCONF::GMTP_GPSE);` at bottom of `cumulateDistance()`

---

## Findings

---

**A13-1** · HIGH · `inPoly2()` declared in public interface but never implemented

**Description:** `gnssreceiver.h` line 47 declares `bool inPoly2(const CIGCONF::gpsPosStruct *gpsPos, const CIGCONF::polygonStruct *polygon)` as a public method. No definition exists anywhere in the codebase. Any translation unit that calls this method will fail to link. The declaration pollutes the public API with a broken contract and signals an incomplete or abandoned feature. This is classic dead/broken code — the linker will catch it at build time if called, but callers may rely on its presence in headers.

**Fix:** Either implement the function body in `gnssreceiver.cpp` or remove the declaration from `gnssreceiver.h` entirely. If it is intended future work, move it to a clearly-marked private stub or a separate feature branch.

---

**A13-2** · HIGH · `changeUpdateTime()` is functionally broken — timer restart is commented out

**Description:** `gnssreceiver.cpp` line 216 shows `//m_timerId = startTimer(gCfg->gpsUpdateTime() * 1000);` is commented out. The method kills the existing timer but never restarts it. Consequently, any caller invoking `changeUpdateTime()` (e.g., `backgroundworker.cpp` line 1275) permanently stops GPS update reporting without any indication of error. The public method name implies a configuration change, not a shutdown, making this a silent, misleading behaviour defect.

**Fix:** Uncomment line 216 in `gnssreceiver.cpp` so that `changeUpdateTime()` kills and restarts the timer with the updated period. If the intent is truly to stop reporting, rename the method to `stopUpdates()` and document accordingly.

---

**A13-3** · MEDIUM · Suppressed `return` statements after fatal GPIO failures in `setPower()`

**Description:** `canbus.cpp` lines 116, 120, and 148 each contain a commented-out `//return;` after critical failures: GPIO file open failures (lines 116, 120) and `ip link set` subprocess failure (line 148). When these failures occur, execution continues silently as if the setup succeeded. If gpio36 or gpio38 cannot be opened, write calls at lines 127–130 and 169–172 operate on a closed file handle. If the `ip link set` command fails, `connectDevice()` is still called, potentially on an interface that was never configured.

**Fix:** Uncomment and restore the `return` statements at lines 116, 120, and 148 so that `setPower()` aborts on unrecoverable hardware errors. At minimum, a function-level return should follow each critical failure, consistent with the already-present `qCritical()` log calls.

---

**A13-4** · MEDIUM · Signed/unsigned comparison: `quint32 last = -1` in `applyFilters()`

**Description:** `canbus.cpp` line 232 initialises `quint32 last = -1`. Assigning `-1` to an unsigned type is implementation-defined-safe in C++ (it wraps to `UINT_MAX`), but it is a style violation and triggers compiler warnings with `-Wsign-conversion` or `-Wall`. The intent is to represent "no previous value", which is a sentinel that happens to work only because no valid CAN ID equals `UINT_MAX`. This is fragile and non-obvious.

**Fix:** Replace with `quint32 last = UINT_MAX;` using the named constant, and add a comment explaining the sentinel value. Alternatively, use `std::optional<quint32>` to express "no prior value" without relying on a magic sentinel.

---

**A13-5** · MEDIUM · Magic number `47757857` in `calculateDistance()` with no explanation

**Description:** `gnssreceiver.cpp` lines 349 and 357 use the literal `47757857` as a scaling factor. The surrounding comment (`// dlng / 10000000 * PI / 180 * R << 32`) explains the intent, but the magic constant itself is the pre-computed product of `(1/10000000) * (PI/180) * 6371000 * 2^32` (approximately). Without this derivation in the code, maintainers cannot verify correctness, and the constant `EARTH_R` defined on line 13 is never used in the calculation despite its presence.

**Fix:** Replace `47757857` with a named compile-time constant or a `constexpr` expression that makes the derivation explicit, e.g.:
```cpp
// (PI / 180 / 10000000) * EARTH_R * (1 << 32)
constexpr qint64 kLatLngScaleFactor = 47757857;
```
Also either use `EARTH_R` in the derivation or remove the unused macro.

---

**A13-6** · MEDIUM · `EARTH_R` macro defined but never used

**Description:** `gnssreceiver.cpp` line 13 defines `#define EARTH_R 6371000UL` but this constant is never referenced anywhere in the file. `calculateDistance()` uses the hardcoded magic number `47757857` which implicitly incorporates the Earth radius. The unused macro misleads readers into thinking the radius is applied symbolically when it is not.

**Fix:** Remove the `EARTH_R` macro, or integrate it into a named `constexpr` expression for `kLatLngScaleFactor` (see A13-5) so the radius is both visible and used.

---

**A13-7** · MEDIUM · Leaky abstraction: CAN protocol bit constants exposed in `applyFilters()`

**Description:** `canbus.cpp` lines 241–249 directly manipulate raw CAN framing bits: `(1 << 29)` to detect extended frame format, mask values `0x3ffff00` and `0x3ff`, and the `MatchExtendedFormat` / `MatchBaseFormat` constants. These hardware-protocol details are embedded in the implementation without named constants or explanatory abstractions. The value `0x3ffff00` is particularly opaque — it is not a standard CAN mask and its derivation is not documented.

**Fix:** Replace magic bit masks with named constants (e.g., `kCanExtendedFrameBit`, `kExtendedFrameIdMask`, `kBaseFrameIdMask`) defined at file or class scope with comments explaining their purpose and derivation.

---

**A13-8** · MEDIUM · `getRequests()` is non-const and returns a mutable copy of internal state

**Description:** `canbus.h` line 40 declares `QList<Request> getRequests()` as non-const with no `const` qualifier. The method returns a full copy of `m_requests` by value. Callers cannot call this on a `const CanBus` reference, making it impossible to use in read-only contexts. The naming convention `getX()` is inconsistent with the rest of the class, which uses Qt-style accessors without the `get` prefix (e.g., `baudRate()`, `isXferEnabled()`).

**Fix:** Declare the method `const` and rename it to `requests()` to match the existing naming convention: `QList<Request> requests() const { return m_requests; }`.

---

**A13-9** · MEDIUM · Commented-out legacy MK2 relay control blocks in `cumulateDistance()`

**Description:** `gnssreceiver.cpp` contains two commented-out blocks of legacy MK2 relay control code at lines 314–317 and 324–326, both marked `/** MK2 RELAY CONTROL OP ... **/`. An additional commented-out block at lines 123–126 of `parseData()` also references legacy relay/geofence logic. These blocks reference undefined symbols (`RELAY3_MODE`, `RELAY3_MODE_GFNCE_NO`, `BSP_RLY3_STATE`, `BSP_RLY3_SET`, `BSP_RLY3_CLR`) and represent dead legacy code that should have been removed, not commented out. They increase maintenance burden and cause reader confusion about the current state of relay control.

**Fix:** Remove all commented-out legacy relay control blocks from `parseData()` and `cumulateDistance()`. If relay integration is needed in the future, it should be re-implemented cleanly against the current hardware abstraction layer, not resurrected from commented-out MK2 code.

---

**A13-10** · MEDIUM · `timerEvent()` handler is an empty stub — misleading dead code

**Description:** `gnssreceiver.cpp` lines 44–49 define `GnssReceiver::timerEvent(QTimerEvent *event)` with a guard `if (m_timerId != event->timerId()) return;` followed by an empty body. The handler starts the timer in `portStateChanged()` (line 60) but does nothing when the timer fires. This is dead code — the timer slot does not exist, and `timerEvent` is the Qt fallback mechanism. A reader may incorrectly assume periodic work occurs here.

**Fix:** Either remove `timerEvent()` entirely and implement a `QTimer`-based slot (consistent with the `CanBus` pattern), or add the intended periodic behaviour inside the handler body. At minimum, if the handler is intentionally empty, add a comment explaining why.

---

**A13-11** · LOW · `age()` is not declared `const` despite having no side effects

**Description:** `gnssreceiver.h` line 35 declares `qint64 age()` without the `const` qualifier, even though the method only reads `m_timestamp` and calls `QDateTime::currentMSecsSinceEpoch()`. All other read-only accessors in the same class are correctly declared `const`. This inconsistency prevents `age()` from being called on a `const GnssReceiver` reference and breaks const-correctness throughout the API.

**Fix:** Add `const` to the declaration: `qint64 age() const;` and to the definition in `gnssreceiver.cpp`.

---

**A13-12** · LOW · `Request::timer` field type mismatch: `qint32` vs `quint32 interval`

**Description:** In `canbus.h` lines 20–22, `Request::interval` is `quint32` but `Request::timer` is `qint32`. In `canbus.cpp` line 69, timer is decremented (`request.timer -= REQUEST_TIMER`) and compared against zero (`if (request.timer <= 0)`). The mixed signed/unsigned types are inconsistent; if `interval` is assigned to `timer` (line 204: `request.timer = interval`), a large `quint32` interval value could produce undefined behaviour or sign wrap when stored in `qint32`.

**Fix:** Make both fields the same type. Since the countdown logic requires signed comparison against zero, either change `interval` to `qint32` or keep both as `quint32` and use an explicit `== 0` comparison (ensuring the unsigned value wraps predictably by enforcing `REQUEST_TIMER` divides evenly into all valid intervals).

---

**A13-13** · LOW · Inconsistent indentation and brace style in `pointInPolygon()`

**Description:** `gnssreceiver.cpp` lines 428–446 (`pointInPolygon`) uses 2-space indentation and inconsistent spacing (notably the trailing spaces on lines 430, 444), while the rest of the file uses 4-space indentation with K&R-style braces. This suggests the function was copied from an external source without reformatting. The opening comment `//oddNodes = 1 means within the polygon` is also inconsistently positioned (inline with the opening brace on the same line).

**Fix:** Reformat `pointInPolygon()` to match the 4-space indentation convention used throughout the rest of `gnssreceiver.cpp`. Run `clang-format` with the project's `.clang-format` config if available.

---

**A13-14** · LOW · `#include <math.h>` and `#include <QtMath>` both present in `gnssreceiver.cpp`

**Description:** `gnssreceiver.cpp` lines 8–9 include both `<QtMath>` and `<math.h>`. `<QtMath>` already provides Qt wrappers around standard math functions, and `<math.h>` (C-style header) is redundant. Mixing C-style `<math.h>` with C++ headers is a style violation and can cause macro/function name conflicts in some toolchains.

**Fix:** Remove `#include <math.h>` from `gnssreceiver.cpp`. All required math functions (`M_PI`, `qCos`, `qSqrt`, etc.) are available via `<QtMath>`.

---

**A13-15** · LOW · `sendRequest()` declared `protected` but serves as a private timer slot

**Description:** `canbus.h` line 58 declares `sendRequest()` as `protected`. The method is connected exclusively as a `QTimer::timeout` slot (line 48 of `canbus.cpp`) and is not intended to be called or overridden by subclasses. `CanBus` is not designed as a base class (no virtual destructor, no other virtual methods). Exposing the timer slot as `protected` needlessly widens the access surface.

**Fix:** Move `sendRequest()` to the `private` section of `CanBus`. If subclassing is ever required, promote it back to `protected` deliberately.

---

**A13-16** · INFO · Commented-out struct field `//int timerId` in `Request`

**Description:** `canbus.h` line 22 contains `//int timerId;` commented out inside the `Request` struct. This suggests an earlier design where each request managed its own timer ID. The field is entirely unused and the comment has no explanatory text.

**Fix:** Remove the commented-out field. If the alternative design is of historical interest, document it in a git commit message rather than in source code.

---

**A13-17** · INFO · Commented-out `canBusDevice()` accessor in `canbus.h`

**Description:** `canbus.h` line 51 contains `//QCanBusDevice* canBusDevice() const {return m_canBusDevice;}` commented out. Exposing the raw `QCanBusDevice` pointer in the public interface would break encapsulation, so the accessor was presumably removed, but the commented line was left behind.

**Fix:** Remove the commented-out line entirely.

---

## Summary Table

| ID | Severity | Category | Location | Short Title |
|----|----------|----------|----------|-------------|
| A13-1 | HIGH | Dead / Broken Code | `gnssreceiver.h:47` | `inPoly2()` declared but never implemented |
| A13-2 | HIGH | Dead / Broken Code | `gnssreceiver.cpp:216` | `changeUpdateTime()` permanently stops GPS — timer restart commented out |
| A13-3 | MEDIUM | Error Handling | `canbus.cpp:116, 120, 148` | Suppressed `return` statements after fatal GPIO/subprocess failures |
| A13-4 | MEDIUM | Build Warning | `canbus.cpp:232` | Signed/unsigned: `quint32 last = -1` |
| A13-5 | MEDIUM | Magic Numbers | `gnssreceiver.cpp:349, 357` | Magic number `47757857` — derivation undocumented |
| A13-6 | MEDIUM | Dead Code | `gnssreceiver.cpp:13` | `EARTH_R` macro defined but never used |
| A13-7 | MEDIUM | Leaky Abstraction | `canbus.cpp:241–249` | Raw CAN protocol bit masks without named constants |
| A13-8 | MEDIUM | Style / API | `canbus.h:40` | `getRequests()` non-const and inconsistently named |
| A13-9 | MEDIUM | Commented-out Code | `gnssreceiver.cpp:123–126, 314–317, 324–326` | Legacy MK2 relay control blocks never removed |
| A13-10 | MEDIUM | Dead Code | `gnssreceiver.cpp:44–49` | `timerEvent()` is an empty stub — misleading dead code |
| A13-11 | LOW | Const-correctness | `gnssreceiver.h:35` | `age()` not declared `const` |
| A13-12 | LOW | Type Safety | `canbus.h:20–22` | `Request::timer` (qint32) vs `Request::interval` (quint32) mismatch |
| A13-13 | LOW | Style | `gnssreceiver.cpp:428–446` | Inconsistent indentation in `pointInPolygon()` |
| A13-14 | LOW | Style | `gnssreceiver.cpp:9` | Redundant C-style `<math.h>` alongside `<QtMath>` |
| A13-15 | LOW | Access Control | `canbus.h:58` | `sendRequest()` declared `protected` but should be `private` |
| A13-16 | INFO | Commented-out Code | `canbus.h:22` | Commented-out `timerId` field in `Request` struct |
| A13-17 | INFO | Commented-out Code | `canbus.h:51` | Commented-out `canBusDevice()` accessor |
# Pass 4 Agent A14 — Code Quality

**Audit run:** 2026-02-28-01
**Branch:** master
**Assigned files:**
- `platform/internalrfid.h`
- `platform/internalrfid.cpp`
- `platform/internalrtc.h`
- `platform/internalrtc.cpp`

---

## Reading Evidence

### `platform/internalrfid.h`

**Class:** `EM070::InternalRfid` (inherits `QObject`)

| Function / Method | Line |
|---|---|
| `InternalRfid(QObject *parent = 0)` | 14 |
| `void setEnabled(bool enabled)` | 15 |
| `void response()` (signal) | 18 |
| `void cardData(quint64, quint16, quint32, QByteArray &)` (signal) | 19 |
| `void error(const QString &text)` (signal) | 20 |
| `void readData()` (private) | 23 |
| `void parseData()` (private) | 24 |

**Members:** `QSerialPort *m_serialPort`, `QByteArray m_receiver`

**Types / Constants / Enums defined:** none (all macros are in the `.cpp`)

---

### `platform/internalrfid.cpp`

**Macros defined:**

| Name | Value | Line |
|---|---|---|
| `FILE_SERIAL_PORT` | `"/dev/ttyS2"` | 7 |
| `RECEIVER_MAX_SIZE` | `128` | 8 |

**Functions implemented:**

| Function | Line |
|---|---|
| `InternalRfid::InternalRfid(QObject *parent)` | 12 |
| `InternalRfid::setEnabled(bool enabled)` | 38 |
| `InternalRfid::readData()` | 51 |
| `InternalRfid::parseData()` | 67 |

---

### `platform/internalrtc.h`

**Class:** `EM070::InternalRtc` (no base class; purely static interface)

| Function / Method | Line |
|---|---|
| `static void setRtcTime(QDateTime dateTime = QDateTime())` | 11 |
| `static void setSystemTime()` | 12 |
| `static quint64 euiAddress()` | 13 |

**Types / Constants / Enums defined:** none

---

### `platform/internalrtc.cpp`

**Macros defined:**

| Name | Value | Line |
|---|---|---|
| `FILE_RTC_DEVICE` | `"/dev/rtc1"` | 5 |
| `FILE_RTC_EUI` | `"/sys/devices/platform/nuc970-i2c0/i2c-0/0-006f/eui"` | 6 |

**Functions implemented:**

| Function | Line |
|---|---|
| `InternalRtc::setRtcTime(QDateTime dateTime)` | 10 |
| `InternalRtc::setSystemTime()` | 24 |
| `InternalRtc::euiAddress()` | 31 |

---

## Findings

---

**A14-1** · HIGH · `::stime()` is a deprecated/removed POSIX syscall

**Description:** `internalrtc.cpp` line 15 calls `::stime(&sec)`, guarded by `#ifdef __arm__`. `stime()` was removed from POSIX.1-2008 and is absent from glibc 2.31+ (Linux kernel 5.1+). On a modern toolchain this call will fail to compile or silently link against an unavailable symbol. It also requires the process to run as root (CAP_SYS_TIME), raising privilege concerns. The correct replacement is `clock_settime(CLOCK_REALTIME, ...)`.

**Fix:** Replace `::stime(&sec)` with a `clock_settime` call:
```cpp
struct timespec ts { static_cast<time_t>(sec), 0 };
::clock_settime(CLOCK_REALTIME, &ts);
```
Include `<time.h>` / `<ctime>` and remove the `stime` dependency. Verify the process holds `CAP_SYS_TIME` rather than running as root.

---

**A14-2** · HIGH · Device paths hard-coded as `#define` macros leak into binary and are not configurable at runtime for `internalrtc.cpp`

**Description:** `internalrtc.cpp` defines `FILE_RTC_DEVICE` (`/dev/rtc1`) and `FILE_RTC_EUI` (`/sys/devices/platform/nuc970-i2c0/i2c-0/0-006f/eui`) as plain `#define` macros (lines 5-6). Unlike `internalrfid.cpp` which at least provides a `QT_RFID_SERIAL_PORT` environment-variable override, the RTC paths have no override mechanism. The `sysfs` path embeds the exact hardware bus topology (`nuc970-i2c0`, bus address `0-006f`), making the binary non-portable and impossible to test on a development host without modifying source. This is a leaky abstraction: implementation detail of hardware topology is baked into the compiled artifact.

**Fix:** Promote both paths to `static constexpr QLatin1String` constants (or `QStringLiteral`) and add environment-variable overrides mirroring the pattern already used in `InternalRfid`. For the `sysfs` EUI path, consider reading the path from a platform configuration file rather than hard-coding bus topology.

---

**A14-3** · MEDIUM · Device path `FILE_SERIAL_PORT` hard-coded as `#define` macro in `internalrfid.cpp`

**Description:** `internalrfid.cpp` line 7 defines `FILE_SERIAL_PORT` as `"/dev/ttyS2"` via a C preprocessor macro. Although an environment variable override exists (`QT_RFID_SERIAL_PORT`), the macro itself is a raw `#define` rather than a typed constant, providing no type safety. The macro name is misleading because `FILE_` prefix suggests a file-system path constant, whereas Qt serial port APIs take a port name string.

**Fix:** Replace the `#define` with a `static constexpr QLatin1String` or `static const QString` in the translation unit, keeping the env-var override logic. Rename to reflect its purpose, e.g., `DefaultRfidPortName`.

---

**A14-4** · MEDIUM · `RECEIVER_MAX_SIZE` defined as untyped `#define` macro

**Description:** `internalrfid.cpp` line 8 defines `RECEIVER_MAX_SIZE 128` as a plain `#define`. This provides no type information (it could be used as `int`, `size_t`, or any numeric type without warning) and pollutes the preprocessor namespace.

**Fix:** Replace with `static constexpr int ReceiverMaxSize = 128;` (or `qsizetype`) so the constant has an explicit type and respects C++ scoping rules.

---

**A14-5** · MEDIUM · `QProcess::execute()` used with a concatenated string command — injection risk and deprecated API pattern

**Description:** `internalrtc.cpp` lines 21 and 27 construct a shell command by string concatenation (`QString cmd("hwclock -w -f "); cmd += QStringLiteral(FILE_RTC_DEVICE);`) and pass it to `QProcess::execute(QString)`. The single-argument overload of `QProcess::execute` is deprecated since Qt 5.15 in favour of `QProcess::execute(const QString &program, const QStringList &arguments)`. Additionally, passing a single concatenated string relies on the Qt implementation splitting arguments, which can mishandle paths containing spaces. While `FILE_RTC_DEVICE` is a compile-time constant here, the pattern is fragile and generates deprecation warnings on Qt 5.15+.

**Fix:** Refactor to:
```cpp
QProcess::execute(QStringLiteral("hwclock"), { QStringLiteral("-w"), QStringLiteral("-f"), QStringLiteral(FILE_RTC_DEVICE) });
```
This eliminates the deprecation warning and makes argument boundaries explicit.

---

**A14-6** · MEDIUM · `qDebug()` production log in `parseData()` emits raw card data on every read

**Description:** `internalrfid.cpp` line 79 unconditionally calls `qDebug() << "Read internal card data: " << ba;` inside `parseData()`, which fires on every RFID card presentation. In a production build where `QT_NO_DEBUG_OUTPUT` is not defined, this writes potentially sensitive card data (facility code, card number in hex) to the application log, creating an uncontrolled information disclosure path.

**Fix:** Wrap the statement in a `#ifdef QT_DEBUG` guard, or replace it with a conditional `qCDebug` category that can be toggled at runtime without a rebuild:
```cpp
qCDebug(lcRfid) << "Read internal card data:" << ba;
```
Ensure that card data logging is explicitly disabled in the production build configuration.

---

**A14-7** · MEDIUM · Signal `cardData` passes `QByteArray &` (non-const reference) — unsafe across queued connections

**Description:** Both `InternalRfid` (header line 19) and `WiegandRfid` (`wiegandrfid.h` line 20) declare the `cardData` signal with a `QByteArray &readerOutput` parameter (non-const lvalue reference). Qt signals delivered over a queued connection (across threads) cannot marshal non-const references — the value is silently treated as a copy but the API promises a reference. This is a latent bug: if the connection type is ever changed to `Qt::QueuedConnection` or the objects are moved to separate threads, the reference semantics silently break. It also violates Qt signal best-practice (signals should use `const T &` or pass by value).

**Fix:** Change the signal signature to `const QByteArray &readerOutput` (const reference) or `QByteArray readerOutput` (by value) in both `InternalRfid` and `WiegandRfid`, and update all `emit` call sites accordingly.

---

**A14-8** · LOW · Constructor default argument uses `= 0` instead of `= nullptr`

**Description:** `internalrfid.h` line 14 declares `explicit InternalRfid(QObject *parent = 0)`. Using the integer literal `0` as a null pointer constant is valid C++ but considered poor style since C++11; `nullptr` is the correct typed null-pointer constant and is already used pervasively in the rest of the codebase.

**Fix:** Change `= 0` to `= nullptr` in `InternalRfid`'s constructor declaration and definition.

---

**A14-9** · LOW · Stale `#include <QDebug>` with unconditional use — should be conditional

**Description:** `internalrfid.cpp` line 4 includes `<QDebug>` unconditionally. Given that the only use is the `qDebug()` call at line 79 (see A14-6), if that call is wrapped in a `#ifdef QT_DEBUG` guard, the include must also be guarded or moved to a debug-only block to avoid the header being pulled into release builds unnecessarily.

**Fix:** Resolve A14-6 first; then guard or remove the `<QDebug>` include to match the guarded call site.

---

**A14-10** · LOW · `setSystemTime()` has misleading comment implying it should never be called

**Description:** `internalrtc.h` line 12 contains the comment `// no need to call this as which will be done on OS booting`. The grammar is broken ("as which will be done") and the statement contradicts the function's public visibility — if callers truly should never call it, the function should be `private` or removed. Exposing it publicly while commenting that it should not be called is a documentation inconsistency and an invitation for misuse.

**Fix:** If the function is genuinely only called by OS boot scripts (not by application code), remove it from the public header or mark it `private`. If it is legitimately callable at runtime, rewrite the comment to explain when it is appropriate to call it.

---

**A14-11** · LOW · Inconsistent alignment of `#R` branch local variable declarations in `parseData()`

**Description:** `internalrfid.cpp` lines 98-107: the `#R` branch declares `QList<QByteArray> bas` inside the `else if` block, while other branches use only inline expressions. The variable name `bas` (plural of `ba`) is cryptic. This is a minor style inconsistency but reduces readability in an already dense parsing function.

**Fix:** Rename `bas` to `parts` or `fields` for clarity. Consider extracting the entire parsing of each card-format variant into named private helper methods.

---

**A14-12** · LOW · Missing `long` cast for `::stime` argument type mismatch on 64-bit ARM

**Description:** `internalrtc.cpp` line 14 stores `dateTime.toSecsSinceEpoch()` (returns `qint64`) into `long sec`. On LP64 platforms (64-bit Linux), `long` and `qint64` are both 64-bit, so this is fine. However, on ILP32 (32-bit ARM — the guarded `#ifdef __arm__` target), `long` is 32-bit and will overflow after 2038-01-19 (the Year-2038 problem). `::stime` takes `const time_t *`; on 32-bit ARM with a modern kernel and `time_t` defined as 64-bit (`CONFIG_COMPAT_32BIT_TIME`), using `long` rather than `time_t` is the wrong type.

**Fix:** Declare `time_t sec = static_cast<time_t>(dateTime.toSecsSinceEpoch());` to use the correct type regardless of platform word size. This also becomes moot if `stime` is replaced per A14-1.

---

## Summary Table

| ID | Severity | Title |
|---|---|---|
| A14-1 | HIGH | `::stime()` is a deprecated/removed POSIX syscall |
| A14-2 | HIGH | RTC device paths hard-coded with no runtime override |
| A14-3 | MEDIUM | Serial port path defined as untyped `#define` macro |
| A14-4 | MEDIUM | `RECEIVER_MAX_SIZE` defined as untyped `#define` macro |
| A14-5 | MEDIUM | `QProcess::execute(QString)` deprecated single-argument form used |
| A14-6 | MEDIUM | Unconditional `qDebug()` emits raw card data in production |
| A14-7 | MEDIUM | Signal `cardData` passes non-const `QByteArray &` — unsafe for queued connections |
| A14-8 | LOW | Constructor default argument uses `= 0` instead of `= nullptr` |
| A14-9 | LOW | `<QDebug>` included unconditionally; should match guarded call site |
| A14-10 | LOW | `setSystemTime()` has misleading and grammatically broken comment |
| A14-11 | LOW | Cryptic variable name `bas` and style inconsistency in `parseData()` |
| A14-12 | LOW | `long sec` type is wrong on 32-bit ARM — Year-2038 exposure |

**Total findings: 12** (2 HIGH, 5 MEDIUM, 5 LOW)
# Pass 4 Agent A15 — Code Quality

**Audit run:** 2026-02-28-01
**Branch:** master
**Files reviewed:**
- `platform/modemport.h`
- `platform/modemport.cpp`
- `platform/powersupply.h`
- `platform/powersupply.cpp`

---

## Reading Evidence

### `platform/modemport.h`

**Class:** `EM070::ModemPort` (inherits `QObject`)

| Line | Name | Kind |
|------|------|------|
| 14 | `explicit ModemPort(QObject *parent = nullptr)` | constructor |
| 15 | `bool sendCmd(const QByteArray &cmd)` | public method |
| 16 | `void resetModem()` | public method |
| 17 | `void setEnabled(bool enable)` | public method |
| 18 | `void setEcho(bool enable)` | public inline method |
| 19 | `bool isWwx()` | public inline method |
| 20 | `void setWwx(bool isWwx)` | public inline method |
| 23 | `void portStateChanged(bool open)` | signal |
| 24 | `void response(bool ok, const QByteArrayList &content)` | signal |
| 27 | `void openPort()` | private method |
| 28 | `void portError()` | private method |
| 29 | `void readData()` | private method |
| 30 | `void parseData(const QByteArray &line)` | private method |

**Members:**

| Line | Name | Type |
|------|------|------|
| 32 | `m_serialPort` | `QSerialPort *` |
| 33 | `m_timer` | `QTimer *` |
| 34 | `m_tryTimes` | `int` |
| 35 | `m_receiver` | `QByteArray` |
| 36 | `m_response` | `QByteArrayList` |
| 37 | `m_cmdLine` | `QByteArray` |
| 38 | `m_echo` | `bool` |
| 39 | `m_wwx` | `bool` |

**Types/enums/constants defined:** none in this header.

---

### `platform/modemport.cpp`

**Macros defined:**

| Line | Name | Value |
|------|------|-------|
| 7 | `FILE_MODEM_PORT_WWX` | `"/dev/ttyUSB2"` |
| 8 | `FILE_MODEM_PORT` | `"/dev/ttyUSB3"` |

**Functions:**

| Line | Name |
|------|------|
| 12 | `ModemPort::ModemPort(QObject *parent)` |
| 50 | `void ModemPort::resetModem()` |
| 68 | `void ModemPort::setEnabled(bool enable)` |
| 90 | `void ModemPort::openPort()` |
| 108 | `void ModemPort::portError()` |
| 125 | `bool ModemPort::sendCmd(const QByteArray &cmd)` |
| 139 | `void ModemPort::readData()` |
| 168 | `void ModemPort::parseData(const QByteArray &line)` |

---

### `platform/powersupply.h`

**Class:** `EM070::PowerSupply` (inherits `QObject`)

**Enums:**

| Line | Name | Enumerators |
|------|------|-------------|
| 16 | `BlankMode` | `UnBlank = 0`, `BlankPowerDown = 4` |
| 17 | `ChargeState` | `NotCharging = 0`, `PreCharging = 1`, `FastCharging = 2`, `ChargeDone = 3` |
| 18 | `ChargeFault` | `NoFault = 0`, `InputFault = 1`, `ThermalShutdown = 2`, `ChargeTimerExpired = 3` |

**Public methods:**

| Line | Name | Kind |
|------|------|------|
| 19 | `explicit PowerSupply(QObject *parent = nullptr)` | constructor |
| 21 | `bool isIgnitionOn() const` | inline getter |
| 23 | `bool isPowerGood() const` | inline getter |
| 24 | `bool isBatteryAvailable() const` | inline getter |
| 25 | `ChargeState chargeState() const` | inline getter |
| 26 | `ChargeFault chargeFault() const` | inline getter |
| 27 | `quint16 voltage() const` | inline getter |
| 28 | `qint16 current() const` | inline getter |
| 29 | `quint16 temperature() const` | inline getter |
| 30 | `quint16 remainingCapacity() const` | inline getter |
| 31 | `quint16 designCapacity() const` | inline getter |
| 32 | `quint16 timeToEmpty() const` | inline getter |
| 33 | `quint16 timeToFull() const` | inline getter |
| 35 | `static void reboot()` | static method |
| 36 | `static void poweroff()` | static method |
| 37 | `static void setBlankMode(BlankMode mode)` | static method |
| 38 | `static void setTouchPower(bool on)` | static method |
| 39 | `static void charge(bool enable)` | static method |
| 40 | `static void setBatteryEnabled(bool enable)` | static method |

**Signals:**

| Line | Name |
|------|------|
| 43 | `void ignitionStateChanged(bool on)` |
| 44 | `void batteryStatusRead(bool avail, int state, int fault, quint16 voltage, qint16 current, quint16 temp, quint16 remainingCapacity)` |

**Private methods:**

| Line | Name |
|------|------|
| 47 | `void readIgnitionState()` |
| 48 | `void readChargerStatus()` |
| 49 | `void readGaugeStatus()` |

**Private members:**

| Line | Name | Type | Comment |
|------|------|------|---------|
| 51 | `m_ignitionFile` | `QFile` | |
| 52 | `m_notifier` | `QSocketNotifier *` | |
| 53 | `m_timer` | `QTimer *` | |
| 55 | `m_ignitionOn` | `bool` | |
| 56 | `m_powerGood` | `bool` | |
| 57 | `m_batteryAvailable` | `bool` | false means VBat < Vsysmin |
| 58 | `m_chargeState` | `ChargeState` | |
| 59 | `m_chargeFault` | `ChargeFault` | |
| 60 | `m_voltage` | `quint16` | in mV |
| 61 | `m_current` | `qint16` | in mA |
| 62 | `m_temperature` | `quint16` | in Celsius degree |
| 63 | `m_remainingCapacity` | `quint16` | in % |
| 64 | `m_designCapacity` | `quint16` | in mAH |
| 65 | `m_timeToEmpty` | `quint16` | in minitues [sic] |
| 66 | `m_timeToFull` | `quint16` | in minitues [sic] |

---

### `platform/powersupply.cpp`

**Macros defined:**

| Line | Name | Value |
|------|------|-------|
| 8 | `QUERY_INTERVAL` | `6000` |
| 10 | `FILE_IGNITION` | `"/sys/devices/platform/nuc970-gpio.0/gpio/gpio225/value"` |
| 11 | `FILE_FB_BLANK` | `"/sys/devices/platform/nuc970-lcd/graphics/fb0/blank"` |
| 12 | `FILE_TOUCH_POWER` | `"/sys/touchscreen/power_state"` |
| 13 | `FILE_CHARGE_EN` | `"/sys/class/gpio/gpio160/value"` |
| 14 | `FILE_BATFET_DISABLE` | `"/sys/devices/platform/nuc970-i2c0/i2c-0/0-006b/power_supply/bq24190-charger/f_batfet_disable"` |
| 15 | `FILE_PG_STAT` | `"/sys/devices/platform/nuc970-i2c0/i2c-0/0-006b/power_supply/bq24190-charger/f_pg_stat"` |
| 16 | `FILE_VSYS_STAT` | `"/sys/devices/platform/nuc970-i2c0/i2c-0/0-006b/power_supply/bq24190-charger/f_vsys_stat"` |
| 17 | `FILE_CHRG_STAT` | `"/sys/devices/platform/nuc970-i2c0/i2c-0/0-006b/power_supply/bq24190-charger/f_chrg_stat"` |
| 18 | `FILE_CHRG_FAULT` | `"/sys/devices/platform/nuc970-i2c0/i2c-0/0-006b/power_supply/bq24190-charger/f_chrg_fault"` |
| 19 | `FILE_NTC_FAULT` | `"/sys/devices/platform/nuc970-i2c0/i2c-0/0-006b/power_supply/bq24190-charger/f_ntc_fault"` |
| 20 | `FILE_GAUGE_REGS` | `"/sys/devices/platform/nuc970-i2c0/i2c-0/0-0055/show_regs"` |

**Functions:**

| Line | Name |
|------|------|
| 24 | `PowerSupply::PowerSupply(QObject *parent)` |
| 53 | `void PowerSupply::readIgnitionState()` |
| 65 | `void PowerSupply::readChargerStatus()` |
| 123 | `void PowerSupply::readGaugeStatus()` |
| 181 | `void PowerSupply::reboot()` |
| 208 | `void PowerSupply::poweroff()` |
| 214 | `void PowerSupply::setBlankMode(BlankMode mode)` |
| 229 | `void PowerSupply::setTouchPower(bool on)` |
| 240 | `void PowerSupply::charge(bool enable)` |
| 251 | `void PowerSupply::setBatteryEnabled(bool enable)` |

---

## Findings

---

**A15-1** · MEDIUM · Commented-out code in `ModemPort::sendCmd` (modemport.cpp:132)

**Description:** Line 132 contains a commented-out `SerialLogger::log` call for outgoing modem commands:
```cpp
//SerialLogger::log("[MODEM:SEND] " + cmd + "\r\n");
```
Similarly, line 171 in `parseData` has a commented-out log for received modem data:
```cpp
//SerialLogger::log("[MODEM:RECV] " + line + "\r\n");
```
These blocks were apparently disabled deliberately (since `m_echo` was added as an alternative mechanism), but the dead code remains in the source. A companion commented-out block also exists at modemport.cpp:29:
```cpp
//m_wwx = true;
```
This appears to be a leftover from a port-detection experiment where `m_wwx` was supposed to be set automatically when `FILE_MODEM_PORT` did not exist, but that behavior was suppressed without explanation.

**Fix:** Remove all three commented-out code lines (modemport.cpp:29, 132, 171). If any of these represent intentional design decisions (e.g., disabling the wwx auto-detection), document the rationale in a comment rather than leaving dead code.

---

**A15-2** · MEDIUM · Commented-out code in `PowerSupply::readGaugeStatus` (powersupply.cpp:130–131)

**Description:** Lines 130–131 contain a commented-out early-return guard:
```cpp
// if (!m_batteryAvailable)
//    return;
```
The surrounding block comment (lines 125–129) explains *why* the guard was disabled — to allow charging even when the battery is fully discharged — but the dead code lines still remain in source, creating noise and ambiguity.

**Fix:** Remove the commented-out `if` block. If the comment block explaining the rationale is still valid, keep it as a plain prose comment without the dead code lines.

---

**A15-3** · LOW · Commented-out code in `PowerSupply::parseData` — modem response terms (modemport.cpp:195–199)

**Description:** Lines 195–199 contain a block of commented-out `startsWith` conditions that were apparently considered but not implemented:
```cpp
//            line.startsWith("BUSY") ||
//            line.startsWith("RING") ||
//            line.startsWith("NO CARRIER") ||
//            line.startsWith("NO ANSWER") ||
//            line.startsWith("NO DIALTONE") ||
```
These suggest dial-up/voice-call handling was considered and then abandoned. They carry no explanatory note.

**Fix:** Remove the commented-out lines. If these responses are genuinely not expected on the data-only modem interface in use, a brief comment stating "voice call responses not applicable" is clearer than dead code.

---

**A15-4** · LOW · Commented-out code in `PowerSupply::reboot` — shell script embedded in comment (powersupply.cpp:183–203)

**Description:** The body of `reboot()` is preceded by a multi-line comment (lines 183–203) that reproduces the entire content of the `/etc/pvd/reboot` shell script inline. While this is informational, it duplicates maintenance-sensitive logic that lives in an external script. If the script changes, the comment will silently drift out of sync.

**Fix:** Replace the verbatim script reproduction with a brief prose description (e.g., "Calls /etc/pvd/reboot which shuts down the modem and network interfaces before rebooting the system"). Reference a documentation location or the script path for readers who want full details.

---

**A15-5** · MEDIUM · Hardware sysfs paths hard-coded as `#define` macros in implementation file (powersupply.cpp:10–20)

**Description:** Ten hardware-specific sysfs paths are defined as `#define` macros at the top of `powersupply.cpp`. These paths encode the SoC part number (`nuc970`), I2C bus topology (`i2c-0/0-006b`), GPIO numbers (`gpio160`, `gpio225`), and charger chip model (`bq24190`). Any board revision or kernel driver update that changes a sysfs path requires edits to this file. There is no mechanism to override paths at compile time or runtime for different board variants.

Examples:
```cpp
#define FILE_IGNITION       "/sys/devices/platform/nuc970-gpio.0/gpio/gpio225/value"
#define FILE_CHARGE_EN      "/sys/class/gpio/gpio160/value"
#define FILE_BATFET_DISABLE "/sys/devices/platform/nuc970-i2c0/i2c-0/0-006b/power_supply/bq24190-charger/f_batfet_disable"
```

**Fix:** Collect the sysfs path strings into a named constant struct or a dedicated `platform_paths.h` header, or make them compile-time configurable via a build variable. As a minimum, group them with a comment indicating the target hardware revision so the scope of change is explicit.

---

**A15-6** · LOW · Device node paths hard-coded as `#define` macros in implementation file (modemport.cpp:7–8)

**Description:** The modem serial port device paths are defined as `#define` macros at the top of the `.cpp` file:
```cpp
#define FILE_MODEM_PORT_WWX "/dev/ttyUSB2"
#define FILE_MODEM_PORT     "/dev/ttyUSB3"
```
There is also a non-ARM fallback hard-coded as the string literal `"COM4"` on line 33, with no macro. These paths are tied to a specific USB enumeration order that can vary between kernel versions or USB attachment sequences.

**Fix:** Promote these to named constants in the header or a shared platform configuration header. The `"COM4"` literal on line 33 should also be named and placed alongside the other port definitions. Consider supporting runtime override via the existing `QT_MOBILE_SERIAL_PORT` environment variable mechanism for both port variants.

---

**A15-7** · MEDIUM · `QProcess::startDetached` called with a combined command-and-argument string (modemport.cpp:61)

**Description:** `resetModem()` invokes:
```cpp
QProcess::startDetached("/etc/pvd/mobile -r");
```
The single-string overload of `QProcess::startDetached` was deprecated in Qt 5.15 in favour of the overload that takes the program path and a separate `QStringList` of arguments. Using the deprecated single-string form is a build warning source on Qt 5.15+ and will be removed in Qt 6.

**Fix:** Replace with the two-argument form:
```cpp
QProcess::startDetached("/etc/pvd/mobile", {"-r"});
```

---

**A15-8** · LOW · Magic numbers used in `readGaugeStatus` without symbolic names (powersupply.cpp:145–175)

**Description:** `readGaugeStatus` uses a series of `mid(N)` calls with bare integer offsets (5, 10, 14, 7, 6, 6, 6) to parse fixed-position fields from a comma-separated register dump string. These offsets correspond to the byte lengths of field-name prefixes in the sysfs output (e.g., `"volt="` is 5 chars, `"current_now="` is 12 chars). No comment names the corresponding field labels, making the parsing logic opaque and fragile.

Additionally, the voltage thresholds on lines 148 and 150 (`4100` and `4300` mV) are bare integer literals with no named constants or comments explaining what charge levels they represent.

**Fix:** Define named constants or an inline comment for each `mid` offset that identifies the prefix being skipped. For example:
```cpp
constexpr int VOLT_PREFIX_LEN = 5; // "volt="
```
Similarly, define named constants for the charge threshold voltages:
```cpp
constexpr int CHARGE_ENABLE_THRESHOLD_MV  = 4100;
constexpr int CHARGE_DISABLE_THRESHOLD_MV = 4300;
```

---

**A15-9** · LOW · `BlankMode` enum gap between `UnBlank` (0) and `BlankPowerDown` (4) (powersupply.h:16)

**Description:** The enum is declared as:
```cpp
enum BlankMode {UnBlank, BlankPowerDown = 4};
```
Values 1, 2, and 3 are implicit holes in the enum range. The `setBlankMode` implementation ignores the enum value entirely for the non-`UnBlank` case and always writes `"4"` to the framebuffer blank sysfs node:
```cpp
default:
    file.write("4");
    break;
```
This means any caller who constructs a `BlankMode` with a value of 1, 2, or 3 (possible via a cast) will silently write `"4"` rather than the intended value. The Linux framebuffer blank interface supports values 0–4 (FB_BLANK_UNBLANK through FB_BLANK_POWERDOWN), so values 1–3 are valid and meaningful intermediates that the enum design implies should be reachable but are not.

**Fix:** Either enumerate all meaningful FB_BLANK values (0 = unblank, 1 = normal blank, 2 = vsync suspend, 3 = hsync suspend, 4 = powerdown) or document explicitly that only `UnBlank` and `BlankPowerDown` are supported by this hardware. The `switch` in `setBlankMode` should use the actual enum value when writing the sysfs file rather than the hard-coded `"4"`.

---

**A15-10** · LOW · `m_timer->start(QUERY_INTERVAL)` called twice in `readGaugeStatus` (powersupply.cpp:120, 178)

**Description:** `readChargerStatus` calls `readGaugeStatus` on line 117, then immediately calls `m_timer->start(QUERY_INTERVAL)` on line 120 to schedule the next poll. However, `readGaugeStatus` itself also calls `m_timer->start(QUERY_INTERVAL)` at line 178. Because `readGaugeStatus` is only ever called from `readChargerStatus`, the timer is restarted twice per poll cycle. The second start (line 120 in `readChargerStatus`) is a no-op because `QTimer::start` on an already-active single-shot timer that has not fired simply resets the interval — but the intent is obscured and the placement is misleading.

**Fix:** Remove the `m_timer->start(QUERY_INTERVAL)` call from inside `readGaugeStatus` (line 178). The timer restart belongs in `readChargerStatus` only, after all status reads are complete.

---

**A15-11** · LOW · Inconsistent `inline` method style in `modemport.h` (modemport.h:18–20)

**Description:** Three inline methods in the `ModemPort` header have inconsistent formatting. `setEcho` at line 18 omits the space before the opening brace and uses no space after the function signature:
```cpp
void setEcho(bool enable) {m_echo = enable;}
```
`isWwx` at line 19 has a trailing semicolon after the closing brace, which is valid C++ but inconsistent:
```cpp
bool isWwx() {return m_wwx;};
```
The `PowerSupply` inline getters in `powersupply.h` are consistently formatted with spaces inside braces (e.g., `{return m_ignitionOn;}`). The style difference between the two headers in the same namespace is a minor consistency issue.

**Fix:** Apply consistent inline formatting. For `modemport.h`, add spaces around the body content and remove the spurious trailing semicolon on `isWwx`:
```cpp
void setEcho(bool enable) { m_echo = enable; }
bool isWwx() { return m_wwx; }
void setWwx(bool isWwx) { m_wwx = isWwx; }
```

---

**A15-12** · LOW · Typo in `powersupply.h` member comments: "minitues" (powersupply.h:65–66)

**Description:** The inline comments on lines 65 and 66 read:
```cpp
quint16 m_timeToEmpty;      // in minitues
quint16 m_timeToFull;       // in minitues
```
"minitues" is a misspelling of "minutes".

**Fix:** Correct to "minutes" on both lines.

---

**A15-13** · INFO · `qDebug()` trace left in production code paths (modemport.cpp:102, 118, 131, 170)

**Description:** Four `qDebug()` calls remain in `ModemPort`:
- Line 102: `qDebug() << "ModemPort open";`
- Line 118: `qDebug() << "ModemPort closed";`
- Line 131: `qDebug() << "ModemPort >" << m_cmdLine;` (logs every outgoing AT command)
- Line 170: `qDebug() << "ModemPort <" << line;` (logs every received line)

Lines 131 and 170 will produce high-frequency output on every AT command transaction. In release builds without `QT_NO_DEBUG_OUTPUT` defined, this constitutes unnecessary I/O and potential log volume concern.

**Fix:** Guard high-frequency debug traces (lines 131 and 170) with `#ifdef QT_DEBUG` or replace with the existing `SerialLogger` mechanism controlled by `m_echo`, so they are not emitted in production firmware builds.

---

## Summary Table

| ID | Severity | Location | Short Title |
|----|----------|----------|-------------|
| A15-1 | MEDIUM | modemport.cpp:29, 132, 171 | Commented-out code: log calls and wwx auto-detect |
| A15-2 | MEDIUM | powersupply.cpp:130–131 | Commented-out early-return guard in readGaugeStatus |
| A15-3 | LOW | modemport.cpp:195–199 | Commented-out modem response terms (BUSY, RING, etc.) |
| A15-4 | LOW | powersupply.cpp:183–203 | Verbatim shell script reproduced in comment |
| A15-5 | MEDIUM | powersupply.cpp:10–20 | Hardware sysfs paths hard-coded as #define macros |
| A15-6 | LOW | modemport.cpp:7–8, 33 | Device node paths hard-coded as #define macros |
| A15-7 | MEDIUM | modemport.cpp:61 | Deprecated QProcess::startDetached single-string overload |
| A15-8 | LOW | powersupply.cpp:145–175 | Magic numbers in sysfs field offset parsing and voltage thresholds |
| A15-9 | LOW | powersupply.h:16, powersupply.cpp:218–226 | BlankMode enum gap; implementation ignores enum value |
| A15-10 | LOW | powersupply.cpp:120, 178 | Timer restarted twice per poll cycle |
| A15-11 | LOW | modemport.h:18–20 | Inconsistent inline method style (trailing semicolon, missing spaces) |
| A15-12 | LOW | powersupply.h:65–66 | Typo "minitues" in member comments |
| A15-13 | INFO | modemport.cpp:102, 118, 131, 170 | High-frequency qDebug() calls left in production code paths |
# Pass 4 Agent A16 — Code Quality

**Audit run:** 2026-02-28-01
**Branch:** master
**Repo root:** `C:/Projects/cig-audit/repos/mark3-pvd`
**Files reviewed:**
- `platform/pwmbacklight.h`
- `platform/pwmbacklight.cpp`
- `platform/pwmbeeper.h`
- `platform/pwmbeeper.cpp`
- `platform/seriallogger.h`
- `platform/seriallogger.cpp`

---

## Reading Evidence

### `platform/pwmbacklight.h`

**Class:** `EM070::PwmBacklight` (extends `QObject`)

| Name | Kind | Line |
|------|------|------|
| `State` | enum | 15 |
| `State::NoChange` | enum value | 15 |
| `State::Brighter` | enum value | 15 |
| `State::Darker` | enum value | 15 |
| `PwmBacklight(QObject *parent)` | constructor | 16 |
| `~PwmBacklight()` | destructor | 17 |
| `setAutoBrightness(bool enable)` | public method | 18 |
| `isAutoBrightness() const` | public inline method | 19 |
| `brightness()` | public static method | 21 |
| `setBrightness(quint8 val)` | public static method | 22 |
| `luxRead(int lux)` | signal | 25 |
| `timerEvent(QTimerEvent *)` | protected override | 28 |
| `parse(int lux)` | private method | 31 |
| `adjust(int lux)` | private method | 32 |
| `readLux()` | private method | 33 |
| `m_alsPowerFile` | `QFile` member | 35 |
| `m_alsLuxFile` | `QFile` member | 36 |
| `m_brightnessMap` | `QMap<int,int>` member | 37 |
| `m_luxQueue` | `QQueue<int>` member | 38 |
| `m_autoBrightness` | `bool` member | 39 |
| `m_timerId` | `int` member | 40 |
| `m_state` | `State` member | 41 |
| `m_stateCount` | `quint8` member | 42 |
| `m_currentLux` | `int` member | 43 |

**Constants / macros defined in `pwmbacklight.cpp`:**

| Name | Value | Line |
|------|-------|------|
| `FILE_BRIGHTNESS` | sysfs path string | 6 |
| `FILE_ALS_POWER` | sysfs path string | 7 |
| `FILE_ALS_RANGE` | sysfs path string | 8 |
| `FILE_ALS_LUX` | sysfs path string | 9 |
| `TIMER_INTERVAL` | `250` (ms) | 11 |
| `TWO_SECONDS` | `7` (tick count) | 12 |
| `THREE_SECONDS` | `11` (tick count) | 13 |
| `MAX_QUEUE_SIZE` | `20` | 15 |
| `X1P1(v)` | threshold macro | 17 |
| `X1P2(v)` | threshold macro | 18 |

---

### `platform/pwmbeeper.h`

**Class:** `EM070::PwmBeeper` (extends `QObject`)

| Name | Kind | Line |
|------|------|------|
| `BeepType` | enum | 15 |
| `BeepType::BeepOn` | enum value | 15 |
| `BeepType::BeepSilent` | enum value | 15 |
| `BeepType::BeepOff` | enum value | 15 |
| `PwmBeeper(bool autoDelete, QObject *parent)` | constructor | 18 |
| `~PwmBeeper()` | destructor | 19 |
| `setFrequency(quint16 frequency)` | public inline method | 20 |
| `beep(quint16 milliseconds)` | public method | 21 |
| `beep(quint16 frequency, quint16 milliseconds)` | public method | 22 |
| `beep(qint16 count, quint16 msecOn, quint16 msecOff)` | public method | 23 |
| `stop()` | public method | 24 |
| `timeout()` | private slot | 27 |
| `setBeep(bool on)` | private method | 28 |
| `m_timerOn` | `QTimer *` member | 30 |
| `m_timerOff` | `QTimer *` member | 31 |
| `m_file` | `QFile` member | 32 |
| `m_autoDelete` | `bool` member | 33 |
| `m_frequency` | `quint16` member | 34 |
| `m_beeping` | `bool` member | 35 |
| `m_count` | `qint16` member | 36 |
| `m_msecOn` | `quint16` member | 37 |
| `m_msecOff` | `quint16` member | 38 |

**Constants / macros defined in `pwmbeeper.cpp`:**

| Name | Value | Line |
|------|-------|------|
| `FILE_BEEPER` | `"/dev/input/event3"` | 8 |

---

### `platform/seriallogger.h`

**Class:** `SerialLogger` (no base class, pure-static utility)

| Name | Kind | Line |
|------|------|------|
| `log(const QByteArray &message)` | public static method | 9 |
| `setSerialPort(EM070::UserPort *serial)` | public static method | 10 |
| `m_serial` | `static EM070::UserPort *` member | 13 |

**Constants / macros defined in `seriallogger.cpp`:**

| Name | Value | Line |
|------|-------|------|
| `ENABLE_SL_FILE` | `0` | 5 |
| `SERIAL_LOG_FILE` | `"/mnt/sd/sl.log"` | 6 |

---

## Findings

---

**A16-1** · HIGH · Broken include guard in `pwmbacklight.h`

**Description:** Line 1 of `pwmbacklight.h` opens with `#ifndef PWMBACKLIGHT_H`, but line 2 defines `BRIGHTNESS_H` instead of `PWMBACKLIGHT_H`. These two macros are completely independent, so the guard never fires: on any second inclusion within the same translation unit the preprocessor evaluates `#ifndef PWMBACKLIGHT_H` as true (the macro was never defined), re-processes the entire header, and redeclares `class PwmBacklight` — a hard compiler error. The name `BRIGHTNESS_H` also appears to be a leftover from a previous file name or copy-paste from an earlier draft.

**Fix:** Change line 2 from `#define BRIGHTNESS_H` to `#define PWMBACKLIGHT_H` so it matches the guard on line 1. Alternatively, replace the entire traditional guard with `#pragma once`.

---

**A16-2** · MEDIUM · Dead `BeepType` enum in public API (`pwmbeeper.h:15`)

**Description:** `enum BeepType {BeepOn, BeepSilent, BeepOff}` is declared public at line 15 of `pwmbeeper.h`. No `beep()` overload, no internal method, and no call site in the codebase (confirmed by repository-wide search) references `BeepType` or any of its values. The three `beep()` overloads use `quint16` and `qint16` raw integers. The presence of a public, unused enum in a hardware driver creates ambiguity: integrators may attempt to pass `BeepType` values to `beep()` and find no matching overload. `BeepSilent` implies a distinct beep mode that is entirely unimplemented.

**Fix:** If `BeepType` is not planned for near-term use, remove the enum entirely. If it is intended to replace the raw-integer API, implement the corresponding overload (`void beep(BeepType type, quint16 milliseconds)`) and deprecate the `bool`-based internal `setBeep()`.

---

**A16-3** · MEDIUM · Large commented-out brightness map block (`pwmbacklight.cpp:48–59`)

**Description:** Lines 48–59 contain a 12-entry `m_brightnessMap` initialisation block wrapped in a `/* ... */` comment. The comment was replaced by the two-entry linear map on lines 60–61. The old table is completely dead and will never execute. The values inside it (e.g. `2047 >> 3` = 255, brightness levels up to 2047) suggest a different hardware configuration from the one currently deployed. Dead blocks of this size obscure the maintenance history and may mislead future developers into believing the old table is still relevant.

**Fix:** Remove the commented-out block entirely. If the old brightness curve has historical value, preserve it in version control history or in a named git commit message rather than inline in the source.

---

**A16-4** · MEDIUM · Commented-out call on `setAutoBrightness` (`pwmbacklight.cpp:115`)

**Description:** Line 115 reads:
```cpp
m_currentLux = readLux();//m_brightnessMap.key(brightness(), 4000);
```
The inline comment `//m_brightnessMap.key(brightness(), 4000)` is a commented-out expression that was the original initialiser for `m_currentLux`. It is appended directly to the active statement, making the line hard to parse at a glance. The old expression also read the brightness sysfs file and reverse-looked it up in the map — a round-trip that could fail silently — so the replacement is correct, but the dead code should be removed.

**Fix:** Delete the commented fragment, leaving only `m_currentLux = readLux();`.

---

**A16-5** · MEDIUM · `X1P1` and `X1P2` macros carry stale commented-out magic numbers (`pwmbacklight.cpp:17–18`)

**Description:** Both threshold macros embed two alternative magic-number constants side-by-side, with one commented out:
```cpp
#define X1P1(v)  ((v) * 333/*281*/ >> 8)
#define X1P2(v)  ((v) * 333/*307*/ >> 8)
```
The values `281` and `307` (the original 1.1× and 1.2× approximations in Q8 fixed-point) were replaced by the shared value `333`, which approximates neither 1.1 nor 1.2 correctly (333/256 ≈ 1.301). The stale alternatives are embedded inline as comments making the macros obscure. The macro names (`X1P1` = ×1.1, `X1P2` = ×1.2) now misrepresent the actual multiplier used at runtime.

**Fix:** Decide on the correct multiplier for each threshold, update the constants, name them clearly (e.g. `BRIGHTER_RATIO_Q8`, `DARKER_RATIO_Q8`), remove the dead alternatives, and add a comment explaining the fixed-point arithmetic.

---

**A16-6** · MEDIUM · `ENABLE_SL_FILE` permanently disabled compile-time flag (`seriallogger.cpp:5`)

**Description:** `#define ENABLE_SL_FILE 0` permanently disables the file-logging branch on lines 18–30 at compile time. The dead branch includes a `static QFile` that is never constructed, and the path `/mnt/sd/sl.log` is never opened. Permanently-disabled `#if 0`-style blocks that remain in production code are a maintenance hazard: they age without testing, their APIs drift from the live code, and they consume reader attention. The `SERIAL_LOG_FILE` macro on line 6 is also effectively dead.

**Fix:** If file logging is not planned for any near-term build configuration, remove lines 5–6 and lines 18–30 entirely. If it is a debug feature that may be re-enabled, convert it to a proper build-system option (a CMake/qmake `DEFINES` flag) so it can be toggled without editing source, and add a build-configuration note in the file header.

---

**A16-7** · LOW · C-style cast in `pwmbeeper.cpp:77`

**Description:** Line 77 uses a C-style pointer cast:
```cpp
m_file.write((const char *) &event, sizeof(struct input_event));
```
C-style casts in C++ bypass type-system checks and are invisible to static analysers. In this context the cast from `struct input_event *` to `const char *` is the conventional way to serialise a kernel struct to a byte stream, but the explicit `sizeof(struct input_event)` separately increases the risk of a size mismatch if the struct type were ever changed.

**Fix:** Replace with `reinterpret_cast<const char *>(&event)` to make intent explicit. Consider also using `sizeof(event)` instead of `sizeof(struct input_event)` to keep size and object in sync.

---

**A16-8** · LOW · `input_event` struct partially uninitialized in `pwmbeeper.cpp:66–75`

**Description:** The `struct input_event event` declared at line 66 is never zero-initialized. The kernel `input_event` struct contains a `timeval time` field (two `long` members) that is not set before the struct is written to the device file. On most platforms the kernel ignores this field when reading from userspace, but writing stack garbage to a device file is an inadvertent information-disclosure of stack memory contents to any kernel-side observer or sniffer on the input subsystem. The code also does not initialise the `type` field to zero before branching on `on`, so the `type` field is set correctly but only after the `event` variable is allocated with indeterminate contents.

**Fix:** Zero-initialize the struct at declaration: `struct input_event event = {};`. This guarantees all fields are zero before the relevant ones are set.

---

**A16-9** · LOW · `TWO_SECONDS` and `THREE_SECONDS` names are misleading (`pwmbacklight.cpp:12–13`)

**Description:**
```cpp
#define TWO_SECONDS   7    // (7 + 1) * 250
#define THREE_SECONDS 11   // (11 + 1) * 250
```
The comment explains the derivation: `(count + 1) * TIMER_INTERVAL`. `(7+1)*250 = 2000 ms` and `(11+1)*250 = 3000 ms`. The names correctly describe the intent, but the encoding as a raw count (not a duration) means the constants are implicitly coupled to `TIMER_INTERVAL`. If `TIMER_INTERVAL` is ever changed the time duration changes without any compile-time error, and the macro names will silently lie.

**Fix:** Define the thresholds in terms of `TIMER_INTERVAL`:
```cpp
#define TWO_SECONDS_TICKS   (2000 / TIMER_INTERVAL - 1)
#define THREE_SECONDS_TICKS (3000 / TIMER_INTERVAL - 1)
```
This makes the coupling explicit and keeps the values automatically consistent.

---

**A16-10** · LOW · `SerialLogger` is a non-constructible static class without a deleted constructor

**Description:** `SerialLogger` has only static public methods and a single static private data member, making it a pure static-utility class. However, it has no deleted default constructor. Any code could accidentally write `SerialLogger logger;` and instantiate a useless object. The class also does not inherit from `QObject` but uses `EM070::UserPort` in its interface — the `EM070` namespace is used in the header without a forward declaration of the namespace itself, which requires `userport.h` to transitively pull in everything needed.

**Fix:** Add `SerialLogger() = delete;` to the private section to prevent instantiation. Consider making the class `final` if subclassing is also unintended.

---

**A16-11** · LOW · `setBrightness` and `brightness` open and close a file on every call (`pwmbacklight.cpp:179–201`)

**Description:** Both `brightness()` (line 179) and `setBrightness()` (line 191) construct a local `QFile`, open it, perform one read or write, and implicitly close it on destruction — every time they are called. For brightness reads this matters less (they are called infrequently), but `setBrightness` is called from `adjust()`, which is called from the 250 ms timer tick whenever the lux level changes. Opening and closing a sysfs node on every write adds unnecessary system-call overhead compared to holding an open file descriptor (as is already done for `m_alsPowerFile` and `m_alsLuxFile`).

**Fix:** Either promote the brightness sysfs file to a persistent `QFile` member on `PwmBacklight` (analogous to `m_alsPowerFile`) or, since `brightness()` and `setBrightness()` are static, maintain a `static QFile` within the translation unit opened once on first use.

---

**A16-12** · LOW · Trailing whitespace in `parse()` — extra space before `)` (`pwmbacklight.cpp:140`)

**Description:** Line 140 reads `if (m_state != Brighter )` with a stray space before the closing parenthesis. This is a minor style inconsistency; no other conditional in the file has this pattern.

**Fix:** Remove the extra space: `if (m_state != Brighter)`.

---

**A16-13** · INFO · Magic number `8` inside `parse()` with no named constant (`pwmbacklight.cpp:162–169`)

**Description:** Lines 162–169 use the literal `8` as the minimum queue depth and the divisor for averaging:
```cpp
if (size < 8)
    return;
int sum = 0;
for (int i = size - 8; i < size; ++i)
    sum += m_luxQueue.at(i);
adjust(sum >> 3);    // sum / 8
```
`8` corresponds to 8 × 250 ms = 2 seconds of samples, matching the `TWO_SECONDS` concept but expressed as a raw integer in three separate places. `sum >> 3` is the divide-by-8, but is not obviously connected to the `8` above.

**Fix:** Introduce a named constant (e.g. `#define AVG_WINDOW_SIZE 8`) and replace all three occurrences. Replace `sum >> 3` with `sum / AVG_WINDOW_SIZE` or add an explanatory comment.

---

**A16-14** · INFO · `SerialLogger::m_serial` initialised with `0` not `nullptr` (`seriallogger.cpp:8`)

**Description:** Line 8 initialises the static pointer with the integer literal `0`:
```cpp
EM070::UserPort *SerialLogger::m_serial = 0;
```
Modern C++ style uses `nullptr` for null pointer constants. Using `0` is not incorrect but is stylistically inconsistent with the rest of the codebase which uses Qt types and is compiled as C++11 or later.

**Fix:** Replace `= 0` with `= nullptr`.

---

## Summary Table

| ID | Severity | Category | Location | Short Title |
|----|----------|----------|----------|-------------|
| A16-1 | HIGH | Build / Guard | `pwmbacklight.h:1-2` | Broken include guard (`PWMBACKLIGHT_H` vs `BRIGHTNESS_H`) |
| A16-2 | MEDIUM | Dead Code | `pwmbeeper.h:15` | `BeepType` enum declared but never used |
| A16-3 | MEDIUM | Dead Code | `pwmbacklight.cpp:48-59` | Large commented-out brightness map block |
| A16-4 | MEDIUM | Dead Code | `pwmbacklight.cpp:115` | Commented-out expression inline on active statement |
| A16-5 | MEDIUM | Dead Code / Correctness | `pwmbacklight.cpp:17-18` | `X1P1`/`X1P2` macros carry stale alternatives; multiplier mismatches names |
| A16-6 | MEDIUM | Dead Code | `seriallogger.cpp:5-6,18-30` | `ENABLE_SL_FILE` permanently zero; file-log branch is dead code |
| A16-7 | LOW | Style | `pwmbeeper.cpp:77` | C-style cast instead of `reinterpret_cast` |
| A16-8 | LOW | Correctness | `pwmbeeper.cpp:66-75` | `input_event` struct not zero-initialized before write |
| A16-9 | LOW | Style / Maintenance | `pwmbacklight.cpp:12-13` | `TWO_SECONDS`/`THREE_SECONDS` are tick-counts implicitly tied to `TIMER_INTERVAL` |
| A16-10 | LOW | Style | `seriallogger.h` | Pure-static class missing deleted constructor |
| A16-11 | LOW | Performance | `pwmbacklight.cpp:179-201` | Brightness sysfs file opened/closed on every read and write |
| A16-12 | LOW | Style | `pwmbacklight.cpp:140` | Stray space before `)` in condition |
| A16-13 | INFO | Readability | `pwmbacklight.cpp:162-169` | Magic number `8` used three times with no named constant |
| A16-14 | INFO | Style | `seriallogger.cpp:8` | Static pointer initialised with `0` instead of `nullptr` |
# Pass 4 Agent A17 — Code Quality

**Audit run:** 2026-02-28-01
**Branch:** master
**Repo root:** `C:/Projects/cig-audit/repos/mark3-pvd`
**Files reviewed:**
- `platform/userport.h` + `platform/userport.cpp`
- `platform/wiegandrfid.h` + `platform/wiegandrfid.cpp`
- `platform/wifi.h` + `platform/wifi.cpp`

---

## Reading Evidence

### `platform/userport.h`

**Class:** `EM070::UserPort` (extends `QObject`)

| Method / Member | Line |
|---|---|
| `explicit UserPort(QObject *parent = nullptr)` | 15 |
| `void response(const QByteArray &ba)` | 16 |
| `void setBaudRate(QSerialPort::BaudRate baudRate)` | 18 |
| signal: `void cmdReceived(const QByteArray &ba)` | 21 |
| private: `void readData()` | 24 |
| private: `QSerialPort *m_serialPort` | 26 |
| private: `QByteArray m_receiver` | 27 |

**Types / constants defined:** none beyond class members.

**Includes:**
- `<QObject>` (line 4)
- `<QSerialPort>` (line 5)
- Forward declaration `class QSerialPort;` (line 7) — redundant after `#include <QSerialPort>`

---

### `platform/userport.cpp`

| Function | Line |
|---|---|
| `UserPort::UserPort(QObject *parent)` | 15 |
| `UserPort::readData()` | 54 |
| `UserPort::response(const QByteArray &ba)` | 78 |
| `UserPort::setBaudRate(QSerialPort::BaudRate baudRate)` | 88 |

**Macros / constants defined:**
- `FILE_USER_PORT "/dev/ttyS1"` (line 5)

**Conditional blocks:**
- `#if (TEST_MODE == 1)` at lines 7–11 and 44–51 and 83–85 — introduces `QSocketNotifier *notifier` as a file-scope (global) raw pointer.

---

### `platform/wiegandrfid.h`

**Class:** `EM070::WiegandRfid` (extends `QObject`)

| Method / Member | Line |
|---|---|
| `explicit WiegandRfid(QObject *parent = 0)` | 14 |
| `void setEnabled(bool enable)` | 15 |
| `static quint64 wiegandData(quint8 facility, quint32 number)` | 17 |
| signal: `void cardData(quint64 wiegand, quint16 facility, quint32 number, QByteArray &readerOutput)` | 20 |
| signal: `void error(const QString &text)` | 21 |
| private: `void activated()` | 24 |
| private: `QFile m_cardReadyFile` | 26 |
| private: `QSocketNotifier *m_notifier` | 27 |

**Types / constants defined:** none beyond class members.

---

### `platform/wiegandrfid.cpp`

| Function | Line |
|---|---|
| `WiegandRfid::WiegandRfid(QObject *parent)` | 11 |
| `WiegandRfid::activated()` | 24 |
| `WiegandRfid::setEnabled(bool enable)` | 106 |
| `WiegandRfid::wiegandData(quint8 facility, quint32 number)` | 111 |

**Macros / constants defined:**
- `FILE_CARD_READY "/sys/devices/platform/wiegand-gpio.0/card_ready"` (line 5)
- `FILE_CARD_DATA  "/sys/devices/platform/wiegand-gpio.0/card_data"` (line 6)
- `FILE_RAW_DATA   "/sys/devices/platform/wiegand-gpio.0/raw_data"` (line 7)

**Commented-out block:** 37-bit Wiegand decode, lines 83–96.

---

### `platform/wifi.h`

**Class:** `EM070::Wifi` (extends `QObject`)

| Method / Member | Line |
|---|---|
| `explicit Wifi(EM070::UserPort *userPort)` | 26 |
| `~Wifi() {}` | 27 |
| `void writeConf()` | 29 |
| `void restart()` | 30 |
| `bool status()` — inline, returns `m_status` | 32 |
| `bool startPositioning()` | 34 |
| `void parseResponse(const QByteArray &ba)` | 36 |
| `QList<CIGCONF::AccessPoint> accessPoints()` — inline | 38 |
| `void setCellularState(bool state)` | 40 |
| `void setPowerState(CIGCONF::PowerState state)` | 42 |
| signal: `void ethernetStateChanged(bool ready)` | 46 |
| signal: `void wifiReconnectionFailed()` | 47 |
| signal: `void wifiScanFinished(QList<CIGCONF::AccessPoint> list)` | 48 |
| private: `void attemptReconnectToWifi()` | 51 |
| private: `void checkStatus()` | 52 |
| private: `void scanAccessPoints()` | 53 |
| private: `void scanFinished(int exitCode, QProcess::ExitStatus exitStatus)` | 54 |
| private data members | 56–69 |

**Types / constants defined:** none beyond class members (uses imported `CIGCONF::AccessPoint`, `CIGCONF::PowerState`).

**Includes:**
- `"../app/cigconfigs.h"` (line 4)
- `<QObject>` (line 5)
- `<QByteArray>` (line 6)
- `<QList>` **(line 7 — first occurrence)**
- `<QProcess>` (line 8)
- `<QNetworkConfigurationManager>` (line 9)
- `<QTimer>` (line 10)
- `<QList>` **(line 11 — DUPLICATE)**
- Forward declaration `class QTimer;` (line 13) — redundant after `#include <QTimer>`

---

### `platform/wifi.cpp`

| Function | Line |
|---|---|
| `Wifi::Wifi(UserPort *userPort)` | 16 |
| `Wifi::writeConf()` | 46 |
| `Wifi::restart()` | 82 |
| `Wifi::checkStatus()` | 96 |
| `Wifi::setCellularState(bool state)` | 146 |
| `Wifi::attemptReconnectToWifi()` | 153 |
| `Wifi::startPositioning()` | 191 |
| `Wifi::parseResponse(const QByteArray &ba)` | 211 |
| `Wifi::scanAccessPoints()` | 250 |
| `Wifi::scanFinished(int exitCode, QProcess::ExitStatus exitStatus)` | 266 |
| `Wifi::setPowerState(CIGCONF::PowerState state)` | 297 |

**Macros / constants defined:**
- `SCAN_WATCHDOG (300*1000)` (line 13)
- `RECONNECT_TIMEOUT (210000)` (line 14)

**Commented-out blocks:**
- `cigconfigs.h` include, line 5
- Old SIGNAL/SLOT connect for `QProcess::finished`, line 35
- WiFi nmcli reconnection block, lines 174–188
- RSSI format guard in `parseResponse`, lines 229–231
- Debug output in `scanFinished`, lines 284–287
- Debug output in `parseResponse`, line 247

---

## Findings

---

**A17-1** · LOW · Duplicate `#include <QList>` in `wifi.h`
**Description:** `wifi.h` includes `<QList>` twice: once at line 7 and again at line 11. While include guards inside Qt headers make this harmless at compile time, it is a clear copy-paste error that adds noise for readers and can cause warnings with some static analysis tools.
**Fix:** Remove the duplicate `#include <QList>` at line 11 of `platform/wifi.h`.

---

**A17-2** · LOW · Redundant forward declarations after full includes
**Description:** `userport.h` line 7 forward-declares `class QSerialPort;` after already `#include <QSerialPort>`-ing the full header at line 5. Similarly, `wifi.h` line 13 forward-declares `class QTimer;` after already including `<QTimer>` at line 10. Forward declarations after full includes are dead text and can confuse readers about the intended dependency.
**Fix:** Remove `class QSerialPort;` from `platform/userport.h` line 7 and `class QTimer;` from `platform/wifi.h` line 13.

---

**A17-3** · LOW · Deprecated `parent = 0` default argument instead of `nullptr`
**Description:** `WiegandRfid`'s constructor in `wiegandrfid.h` line 14 uses `QObject *parent = 0` as a default argument. This is a pre-C++11 idiom; the rest of the codebase (e.g. `UserPort` at `userport.h` line 15) consistently uses `nullptr`. This inconsistency creates a minor style regression.
**Fix:** Change `explicit WiegandRfid(QObject *parent = 0)` to `explicit WiegandRfid(QObject *parent = nullptr)` in `platform/wiegandrfid.h` line 14.

---

**A17-4** · MEDIUM · `wifiReconnectionFailed` signal declared but never emitted — connected slot silently dead
**Description:** `wifi.h` line 47 declares the `wifiReconnectionFailed()` signal. `backgroundworker.cpp` line 2806 connects it to `m_modemPort->resetModem()`. However, the only `emit wifiReconnectionFailed()` call (inside `attemptReconnectToWifi()`) was commented out as part of the larger reconnection block at `wifi.cpp` line 179. As a result, modem reset on WiFi failure never occurs; the caller believes this recovery path is active when it is not.
**Fix:** Either implement the reconnection logic so that `emit wifiReconnectionFailed()` is reached, or remove the signal declaration, remove the `connect()` in `backgroundworker.cpp`, and document clearly that WiFi-failure-triggered modem reset is not yet implemented.

---

**A17-5** · MEDIUM · `wifiScanFinished` signal declared but never emitted — GPS positioning data never delivered
**Description:** `wifi.h` line 48 declares `wifiScanFinished(QList<CIGCONF::AccessPoint>)`. `backgroundworker.cpp` line 2807 connects it to `sendGmtpMessage(CIGCONF::GMTP_WIFIPOS)`. No `emit wifiScanFinished(...)` call exists anywhere in `wifi.cpp`. `scanFinished()` populates `m_accessPoints` but never fires this signal; the positioning system can never deliver a WiFi position fix.
**Fix:** Add `emit wifiScanFinished(m_accessPoints)` at the end of `Wifi::scanFinished()` (after the access-point list is fully populated) and after `parseResponse()` completes a scan cycle (the `ba.at(0) == '>'` branch in line 219).

---

**A17-6** · MEDIUM · `m_status` permanently `false` — `status()` accessor is useless
**Description:** `wifi.h` line 32 exposes `bool status() { return m_status; }`. `m_status` is initialised to `false` in the constructor (`wifi.cpp` line 19) and is never written again anywhere in the file. No code path sets it to `true`. Any caller relying on `status()` to know whether the WiFi subsystem is functional will always receive `false`. (Confirmed by grep: no `m_status = true` or `m_status = false` assignment exists beyond initialisation.)
**Fix:** Either remove `m_status` and `status()` if they serve no purpose, or wire `m_status` to be set `true` when `m_configurationManager` is successfully initialised and `false` on failure, mirroring the pattern used for `m_wifiStatus`.

---

**A17-7** · MEDIUM · Commented-out WiFi reconnection block leaves `attemptReconnectToWifi()` functionally empty
**Description:** `wifi.cpp` lines 174–188 contain a large commented-out block that was the core reconnection logic: starting `nmcli`, waiting for it to finish, and handling failure. What remains live in `attemptReconnectToWifi()` only kills the DHCP process and returns — there is no actual reconnection attempt. The function name strongly implies active remediation, but the body provides none. This is a leaky abstraction: callers (`checkStatus()`) believe reconnection was attempted.
**Fix:** Either restore the reconnection logic (replacing the deprecated `nmcli` path with a working alternative such as `wpa_cli reconnect` or direct `dhclient`), or rename the function to reflect its actual behaviour (e.g., `releaseDhcpLease()`) and update callers accordingly. Remove the dead comment block once the intent is resolved.

---

**A17-8** · MEDIUM · Commented-out 37-bit Wiegand decode leaves an unsupported card format with no error reporting
**Description:** `wiegandrfid.cpp` lines 83–96 contain a commented-out `if (bits == 37)` block for decoding HID 37-bit Wiegand cards. With the block disabled, 37-bit cards fall through to the `if (bits >= 26)` catch-all at line 98, which emits `cardData(wiegand, 0, 0, ba)` (facility=0, number=0) followed immediately by `emit error(ba)` at line 103. This means 37-bit HID cards are treated as decode failures rather than as an unsupported-but-known format, and the error message contains only raw binary data, not a useful diagnostic.
**Fix:** Either re-enable and fix the 37-bit decode path (the commented code contains a type mismatch: `facility` is `quint16` inside but the signal and `wiegandData()` accept `quint8`/`quint16` — verify the field widths and correct them), or add an explicit `bits == 37` branch that emits a descriptive `error()` string such as `"37-bit HID format not supported"` instead of raw card data. Remove the commented block.

---

**A17-9** · LOW · C-style casts in `wiegandrfid.cpp` Wiegand decode logic
**Description:** `wiegandrfid.cpp` lines 71–72 use C-style casts `(quint8)(w >> 16)` and `(quint16)w` to extract facility and card number from the 34-bit Wiegand word. C-style casts suppress all compiler warnings about truncation and are stylistically inconsistent with the rest of the Qt codebase which generally avoids them.
**Fix:** Replace with `static_cast<quint8>(w >> 16)` and `static_cast<quint16>(w)` to make the intended truncation explicit and compiler-visible.

---

**A17-10** · LOW · Test-mode global raw pointer `notifier` leaks into translation unit scope
**Description:** `userport.cpp` lines 9–10 declare `QSocketNotifier *notifier` as a file-scope global raw pointer guarded by `#if (TEST_MODE == 1)`. The pointer is assigned inside the constructor but is never deleted and is never wrapped in a smart pointer. Even in test mode, if the `UserPort` object is destroyed and recreated, the old notifier is orphaned. Additionally, a bare global pointer is unidiomatic in Qt code where `QObject` parented children are the norm.
**Fix:** Move `notifier` into the `UserPort` class as a `QSocketNotifier *m_testNotifier` member (still `#if TEST_MODE` guarded), constructed with `this` as parent so Qt's object tree handles its lifetime. Remove the global declaration.

---

**A17-11** · LOW · `wifi.h` includes `<QNetworkConfigurationManager>` — deprecated Qt Network Bearer API exposed in public header
**Description:** `QNetworkConfigurationManager` and `QNetworkConfiguration` are part of the Qt Network Bearer API that was deprecated in Qt 5.15 and removed in Qt 6. Including this header in the public `wifi.h` forces all consumers of `Wifi` to transitively depend on a deprecated API. The implementation detail (`m_configurationManager`) belongs in the `.cpp` file and should be forward-declared or hidden.
**Fix:** Forward-declare `QNetworkConfigurationManager` in `wifi.h` (or use a PIMPL), move `#include <QNetworkConfigurationManager>` and `#include <QNetworkConfiguration>` to `wifi.cpp` only. Longer term, migrate off `QNetworkConfigurationManager` to `QNetworkInformation` (Qt 6) or a direct kernel interface.

---

**A17-12** · LOW · `wifi.cpp` line 5 has a commented-out `#include "../app/cigconfigs.h"`
**Description:** `wifi.cpp` line 5 reads `//#include "../app/cigconfigs.h"`. This header is included transitively via `wifi.h` (which includes `"../app/cigconfigs.h"` at line 4), so the direct include was presumably removed when the header was added to `wifi.h`. The dead comment adds confusion about whether `cigconfigs.h` is required here.
**Fix:** Delete the commented-out include at `wifi.cpp` line 5.

---

**A17-13** · LOW · Commented-out old-style SIGNAL/SLOT connect left in `wifi.cpp`
**Description:** `wifi.cpp` line 35 contains a commented-out `connect(m_ps, SIGNAL(...), ...)` call. The modern `QOverload` form on the next line (line 36) is the intended and active connection. The dead comment creates confusion about which form is in use.
**Fix:** Delete `wifi.cpp` line 35.

---

**A17-14** · LOW · Inconsistent indentation in `wifi.cpp` `writeConf()` body
**Description:** Inside the `if`/`else` block of `writeConf()` (lines 65–74), the `if` branch uses consistent `\t`-indented `out <<` lines, but the `else` branch (lines 69–73) drops back to the enclosing indentation level for the `out <<` statements, making the block harder to read and diff.
**Fix:** Indent the `else` branch body to one level deeper than the `else` keyword, consistent with the `if` branch.

---

**A17-15** · LOW · `wifi.cpp` `checkStatus()` uses `BearerEthernet` to classify `wlan0` — semantic mismatch
**Description:** `wifi.cpp` line 118 checks `cfg.bearerType() == QNetworkConfiguration::BearerEthernet` to identify the wlan0 interface. WiFi connections have bearer type `BearerWLAN`, not `BearerEthernet`. This check may never match (or may match a wired interface by accident), meaning `wifiConnected` could remain `false` even when wlan0 is up. The `name().contains(wifiInterfaceName)` guard narrows the risk but does not compensate for the wrong bearer type.
**Fix:** Change the bearer type check to `QNetworkConfiguration::BearerWLAN`, or remove it and rely solely on `cfg.name().contains(wifiInterfaceName)` combined with `cfg.state() == QNetworkConfiguration::Active`.

---

**A17-16** · INFO · Multiple scattered `qDebug()` calls remain in production paths
**Description:** `wiegandrfid.cpp` lines 42, 60, 74, 99 and `wifi.cpp` lines 111, 158, 169, 256, 260, 268 emit `qDebug()` output unconditionally in production code paths (not behind `#ifdef QT_DEBUG` or `Q_LOGGING_CATEGORY`). On an embedded device this can flood the serial console or system journal. Some of the messages also include raw card data values (line 42: `ba`, line 60: `ba`) which could expose credential-adjacent information in logs.
**Fix:** Wrap debug prints in `Q_LOGGING_CATEGORY` / `qCDebug` with a named category so they can be disabled at runtime. At minimum, protect them with `#ifdef QT_DEBUG`. Remove or redact prints that include raw card data bytes.

---

## Summary Table

| Finding | Severity | Short Title | File(s) | Line(s) |
|---|---|---|---|---|
| A17-1 | LOW | Duplicate `#include <QList>` | `wifi.h` | 7, 11 |
| A17-2 | LOW | Redundant forward declarations after full includes | `userport.h`, `wifi.h` | 7; 13 |
| A17-3 | LOW | `parent = 0` instead of `nullptr` | `wiegandrfid.h` | 14 |
| A17-4 | MEDIUM | `wifiReconnectionFailed` signal never emitted — modem reset silently disabled | `wifi.h`, `wifi.cpp` | 47; 174–188 |
| A17-5 | MEDIUM | `wifiScanFinished` signal never emitted — positioning data never delivered | `wifi.h`, `wifi.cpp` | 48; 266–295 |
| A17-6 | MEDIUM | `m_status` permanently `false` — `status()` accessor always wrong | `wifi.h`, `wifi.cpp` | 32; 19 |
| A17-7 | MEDIUM | Commented-out reconnect block leaves `attemptReconnectToWifi()` functionally empty | `wifi.cpp` | 153–188 |
| A17-8 | MEDIUM | Commented-out 37-bit Wiegand decode causes 37-bit HID cards to fail silently | `wiegandrfid.cpp` | 83–96 |
| A17-9 | LOW | C-style casts in Wiegand 34-bit decode | `wiegandrfid.cpp` | 71–72 |
| A17-10 | LOW | Test-mode global raw pointer `notifier` leaks into TU scope | `userport.cpp` | 9–10, 45 |
| A17-11 | LOW | Deprecated `QNetworkConfigurationManager` in public header | `wifi.h` | 9, 58 |
| A17-12 | LOW | Commented-out `#include` in `wifi.cpp` | `wifi.cpp` | 5 |
| A17-13 | LOW | Dead old-style SIGNAL/SLOT connect comment | `wifi.cpp` | 35 |
| A17-14 | LOW | Inconsistent indentation in `writeConf()` else-branch | `wifi.cpp` | 69–73 |
| A17-15 | LOW | `BearerEthernet` used to classify `wlan0` — wrong bearer type | `wifi.cpp` | 118 |
| A17-16 | INFO | Unconditional `qDebug()` in production paths, some emit raw card data | `wiegandrfid.cpp`, `wifi.cpp` | multiple |
# Pass 4 Agent A18 — Code Quality

**Audit run:** 2026-02-28-01
**Branch:** master
**Files reviewed:**
- `ui/amberimpactalertdialog.h` + `ui/amberimpactalertdialog.cpp`
- `ui/authoriseddialog.h` + `ui/authoriseddialog.cpp`
- `ui/broadcastuidialog.h` + `ui/broadcastuidialog.cpp`

---

## 1. Reading Evidence

### 1.1 AmberImpactAlertDialog

**File:** `ui/amberimpactalertdialog.h` / `ui/amberimpactalertdialog.cpp`

**Class:** `AmberImpactAlertDialog` (extends `QDialog`)

**Methods / functions (with line numbers):**

| Location | Signature |
|---|---|
| h:15 / cpp:6 | `explicit AmberImpactAlertDialog(QWidget *parent = nullptr)` |
| h:16 / cpp:14 | `~AmberImpactAlertDialog()` |
| h:18 / cpp:49 | `bool isOpen() const` |
| h:19 / cpp:31 | `void closeWindow()` |
| h:20 / cpp:19 | `void languageChanged()` |
| h:23 (public slot) / cpp:54 | `void amberAlertDialogShowEvent(bool isLocked)` |
| h:26 (protected) / cpp:25 | `void mouseReleaseEvent(QMouseEvent *)` |
| h:27 (protected) / cpp:39 | `void showEvent(QShowEvent *event = 0)` |

**Types / enums / constants defined:** none beyond those inherited from `QDialog`.

**Private members:**
- `Ui::AmberImpactAlertDialog *ui` (h:30)
- `bool dialogOpenFlag` (h:31)

---

### 1.2 AuthorisedDialog

**File:** `ui/authoriseddialog.h` / `ui/authoriseddialog.cpp`

**Class:** `AuthorisedDialog` (extends `QDialog`)

**Methods / functions (with line numbers):**

| Location | Signature |
|---|---|
| h:17 / cpp:13 | `explicit AuthorisedDialog(QWidget *parent = 0)` |
| h:18 / cpp:44 | `~AuthorisedDialog()` |
| h:19 / cpp:56 | `void setHasChecklist(bool yes)` |
| h:20 / cpp:67 | `void setDriverId(quint64 id)` |
| h:21 / cpp:178 | `void setTime(const QString s)` |
| h:22 / cpp:211 | `void setPower(bool on)` |
| h:23 / cpp:217 | `void updateCamera()` |
| h:33 (protected) / cpp:71 | `void showEvent(QShowEvent *)` |
| h:34 (protected) / cpp:113 | `void hideEvent(QHideEvent *)` |
| h:43 (private) / cpp:148 | `bool debounce()` |
| h:44 (private) / cpp:120 | `void screensaverOff()` |
| h:45 (private) / cpp:138 | `void screensaverPressed()` |
| h:46 (private) / cpp:50 | `void onButtonConfirmStart()` |
| h:47 (private) / cpp:130 | `void screensaverOn()` |
| h:48 (private) / cpp:188 | `void setCamera(bool on, bool flip)` |
| h:54 (private slot) / cpp:172 | `void rstLogout()` |
| h:55 (private slot) / cpp:156 | `void onLogoutRequest()` |

**Signals:**
- `void userLogout()` (h:30)

**Types / enums / constants defined:**
- `#define RESET_TIMEOUT 2000` (cpp:11)

**Private members:**
- `bool m_waking` (h:37)
- `Ui::AuthorisedDialog *ui` (h:38)
- `OptionalCheckConfirmationDialog *m_optionalCheckConfirmationDialog` (h:39)
- `QTimer *m_resetTimer` (h:40)
- `quint32 m_lastPress` (h:41)
- `quint64 m_pendingDriverId` (h:42)
- `bool m_showCamera` (h:50)
- `bool m_power` (h:51)

---

### 1.3 BroadcastUIDialog

**File:** `ui/broadcastuidialog.h` / `ui/broadcastuidialog.cpp`

**Class:** `BroadcastUIDialog` (extends `QDialog`)

**Methods / functions (with line numbers):**

| Location | Signature |
|---|---|
| h:19 / cpp:4 | `explicit BroadcastUIDialog(QWidget *parent = nullptr)` |
| h:20 / cpp:19 | `~BroadcastUIDialog()` |
| h:22 / cpp:24 | `void setUIParam(CIGCONF::BroadcastMessage m)` |
| h:32 (private slot) / cpp:48 | `void onYes()` |
| h:33 (private slot) / cpp:54 | `void onNo()` |
| h:34 (private slot) / cpp:60 | `void onOK()` |

**Signals:**
- `void messageClosed(CIGCONF::BroadcastMessage m)` (h:25)

**Enums defined:**
- `enum MessageResult { MsgResultOK, MsgResultYes, MsgResultNo, MsgResultTimeout, MsgResultLogout, MsgResultNoDriver }` (h:17)

**Private members:**
- `Ui::BroadcastUIDialog *ui` (h:28)
- `QTimer *m_timer` (h:29)

---

## 2. Findings

---

**A18-1** · HIGH · `BroadcastUIDialog::m_timer` allocated without parent — potential memory leak

**Description:** In `broadcastuidialog.cpp` line 7, `m_timer` is constructed as `new QTimer` with no parent argument. Every other `QTimer` allocation in the `ui/` directory uses `new QTimer(this)`, which means the Qt object tree will automatically delete the timer when the dialog is destroyed. Without a parent, the timer is not owned by the object tree and must be deleted manually. The destructor (`cpp:19–22`) only calls `delete ui` and never deletes `m_timer`, so the timer is leaked on every `BroadcastUIDialog` destruction.

**Fix:** Change `m_timer(new QTimer)` to `m_timer(new QTimer(this))` at `broadcastuidialog.cpp:7`. This registers the timer in the Qt object tree and removes the need for a manual `delete`.

---

**A18-2** · HIGH · `messageClosed` signal declared but never emitted — silent API contract failure

**Description:** `BroadcastUIDialog` declares `void messageClosed(CIGCONF::BroadcastMessage m)` at `broadcastuidialog.h:25`. This signal is never emitted anywhere in the codebase (verified by full-repository search). The three button slots (`onYes`, `onNo`, `onOK`) and the timer lambda all call `emit done(MsgResultXxx)`, which invokes the inherited `QDialog::finished(int)` signal rather than `messageClosed`. Any caller that connects to `messageClosed` will never receive a notification, silently discarding message results. The actual consumer in `dialog.cpp:133` connects to `BroadcastUIDialog::finished`, confirming `messageClosed` is unreachable dead code that creates a misleading public API surface.

**Fix:** Remove the `messageClosed` signal declaration from `broadcastuidialog.h`. If a typed result notification carrying back the `BroadcastMessage` is needed in future, re-introduce it and emit it from each slot. Add a comment near the `done()` calls noting that callers should connect to `QDialog::finished(int)` and cast the result to `BroadcastUIDialog::MessageResult`.

---

**A18-3** · MEDIUM · `MessageResult` values `MsgResultLogout` and `MsgResultNoDriver` emitted externally, not by the owning class

**Description:** The `MessageResult` enum values `MsgResultLogout` and `MsgResultNoDriver` are never emitted inside `BroadcastUIDialog` itself. They are fired from `dialog.cpp:135` (`emit m_broadcastDialog->done(BroadcastUIDialog::MsgResultLogout)`) and `dialog.cpp:1165` (`onBroadcastDialogDone(BroadcastUIDialog::MsgResultNoDriver)`). Calling `emit` on another object's signal is a Qt anti-pattern: it bypasses the owning class's encapsulation, couples the external class to internal state transitions, and makes the control flow non-obvious. It can also produce unexpected re-entrancy if the signal is connected with `Qt::DirectConnection`.

**Fix:** Add dedicated public slots or methods to `BroadcastUIDialog` — e.g., `void forceLogoutClose()` and `void forceNoDriverClose()` — that call `emit done(MsgResultLogout)` and `emit done(MsgResultNoDriver)` respectively from within the class. The external caller in `dialog.cpp` should invoke these methods instead of reaching into the object to emit its signals.

---

**A18-4** · MEDIUM · `showEvent` default argument `= 0` is deprecated C++11 / Qt style inconsistency

**Description:** `amberimpactalertdialog.h:27` declares `void showEvent(QShowEvent *event = 0)`. Using integer literal `0` as a default value for a pointer parameter is deprecated C++ style; the correct form is `= nullptr`. This pattern also appears on the same line using a tab-indented style that differs from the spaces-indented body of the same header. `authoriseddialog.h:33` uses `void showEvent(QShowEvent *)` (no default at all), which is the correct override form. `broadcastuidialog.h` omits `showEvent` entirely. Providing a default argument on a virtual override is misleading: the base class `QDialog::showEvent` has no default, so callers always pass the event; the default is never used and serves only to confuse.

**Fix:** Remove the `= 0` default from `amberimpactalertdialog.h:27`. Change `0` to `nullptr` as a secondary improvement wherever legacy `= 0` defaults appear across the `ui/` directory. Align all `showEvent` overrides to the form `void showEvent(QShowEvent *event) override;`.

---

**A18-5** · MEDIUM · `AuthorisedDialog` constructor uses `= 0` for parent parameter; `AmberImpactAlertDialog` uses `= nullptr` — inconsistent within the same file set

**Description:** `authoriseddialog.h:17` declares `explicit AuthorisedDialog(QWidget *parent = 0)` whereas `amberimpactalertdialog.h:15` and `broadcastuidialog.h:19` both use `= nullptr`. Within the same logical group of dialog classes, two different null-pointer representations are used. This is a style inconsistency that will produce compiler warnings under `-Wzero-as-null-pointer-constant` on modern compilers.

**Fix:** Standardise all constructor default parent arguments to `= nullptr` across the `ui/` dialog class headers.

---

**A18-6** · MEDIUM · `AuthorisedDialog::setCamera` contains a leftover `qDebug` trace statement in production code

**Description:** `authoriseddialog.cpp:190` contains `qDebug() << "setCamera(" << on << "," << flip << ")";`. This diagnostic trace fires on every camera state transition, which can occur frequently (on every screensaver toggle, hide/show event, and power change). Debug output in production code adds unnecessary I/O overhead and can expose internal state information in production logs.

**Fix:** Remove the `qDebug` call, or wrap it in `#ifdef QT_DEBUG` / `#endif` so it compiles out in release builds.

---

**A18-7** · MEDIUM · `AmberImpactAlertDialog` includes `<QDebug>` but never calls `qDebug`

**Description:** `amberimpactalertdialog.cpp:4` includes `<QDebug>`, but no `qDebug()` call exists anywhere in the file. This is a dead include left over from development. Unused includes add noise and marginally increase compile time.

**Fix:** Remove `#include <QDebug>` from `amberimpactalertdialog.cpp`.

---

**A18-8** · MEDIUM · `AmberImpactAlertDialog::languageChanged` not called from `Dialog::onLanguageChanged` — localisation gap

**Description:** `dialog.cpp` calls `languageChanged()` on eight child dialogs during language switching (lines 1275–1282), but `m_amberImpactAlertDialog->languageChanged()` is absent from that list. `AmberImpactAlertDialog` has its own `languageChanged()` implementation (`amberimpactalertdialog.cpp:19–23`) that re-translates two labels. If the user changes language while the amber alert dialog is open or has been shown before, those labels will remain in the previous language.

**Fix:** Add `m_amberImpactAlertDialog->languageChanged();` to the `Dialog::onLanguageChanged` handler alongside the other dialog calls.

---

**A18-9** · LOW · `AmberImpactAlertDialog::showEvent` duplicates translation strings already in `languageChanged`

**Description:** `amberimpactalertdialog.cpp:43–44` (inside `showEvent`) and `amberimpactalertdialog.cpp:21–22` (inside `languageChanged`) contain identical `tr(...)` calls for the same two labels. This duplication means any future change to the displayed text must be made in two places, risking divergence.

**Fix:** Refactor `showEvent` to call `languageChanged()` rather than repeating the `tr(...)` assignments. This makes `languageChanged` the single source of truth for translated strings.

---

**A18-10** · LOW · `AuthorisedDialog::onLogoutRequest` compares button text to a translated string to determine dialog state

**Description:** `authoriseddialog.cpp:160` uses `ui->btnLogout->text() == tr("Confirm?")` to test whether the button is in its first-click or second-click (confirm) state. This couples state detection to the localised display text. If the translated string for "Confirm?" in any language contains leading/trailing whitespace or differs in punctuation, the comparison will silently fail and the logout confirmation flow will break. It also makes the component untestable without mocking the translation engine.

**Fix:** Introduce a private `bool m_logoutPending` member that is set to `true` on the first click and reset to `false` by `rstLogout()` and on successful logout. Use `m_logoutPending` as the state gate instead of comparing button text.

---

**A18-11** · LOW · `AuthorisedDialog::setTime` takes `const QString s` by value — unnecessary copy

**Description:** `authoriseddialog.h:21` declares `void setTime(const QString s)`. Passing `QString` by `const` value provides no benefit over passing by `const QString &`; it creates a copy of the string on every call with no additional safety guarantee.

**Fix:** Change the signature to `void setTime(const QString &s)` in both the header and the implementation.

---

**A18-12** · LOW · `AuthorisedDialog::showEvent` sets widget geometry with hard-coded pixel coordinates

**Description:** `authoriseddialog.cpp:82–96` uses hard-coded absolute pixel positions (e.g., `resize(800,321)`, `move(355,170)`) to reposition labels depending on whether the driver name is displayed. Hard-coded pixel layout is fragile: it breaks on any display resolution other than the targeted 800x480 and is unaffected by Qt's layout system. This is a maintainability concern rather than a security issue.

**Fix:** Replace hard-coded geometry calls with a QLayout-based approach (e.g., a `QVBoxLayout` / `QStackedWidget` that shows or hides the driver name label while the other widgets reflow automatically).

---

**A18-13** · LOW · `AuthorisedDialog::showEvent` sets a non-translated hard-coded English string `"Welcome, "`

**Description:** `authoriseddialog.cpp:79` constructs the driver name label text as `"Welcome, " + driverName`. The string literal `"Welcome, "` is not wrapped in `tr(...)`, so it is not subject to translation even when the UI language is changed.

**Fix:** Change the assignment to `ui->lblDriverName->setText(tr("Welcome, ") + driverName)` or, preferably, use `tr("Welcome, %1").arg(driverName)` which is safer for languages where word order differs.

---

**A18-14** · LOW · `BroadcastUIDialog::setUIParam` takes `CIGCONF::BroadcastMessage` by value — unnecessary copy of a potentially non-trivial struct

**Description:** `broadcastuidialog.h:22` declares `void setUIParam(CIGCONF::BroadcastMessage m)`. If `BroadcastMessage` contains a `QString` member (which it does — `m.text` is accessed on cpp:26), passing by value copies the entire struct including the string allocation on every call.

**Fix:** Change the parameter to `const CIGCONF::BroadcastMessage &m`.

---

## 3. Summary Table

| ID | Severity | File(s) | Short Title |
|---|---|---|---|
| A18-1 | HIGH | `broadcastuidialog.cpp:7` | `m_timer` allocated without parent — memory leak |
| A18-2 | HIGH | `broadcastuidialog.h:25` / `.cpp` | `messageClosed` signal declared but never emitted |
| A18-3 | MEDIUM | `broadcastuidialog.h:17` / `dialog.cpp:135,1165` | `MsgResultLogout`/`MsgResultNoDriver` emitted externally via `emit obj->signal()` |
| A18-4 | MEDIUM | `amberimpactalertdialog.h:27` | `showEvent` default argument `= 0` — deprecated null pointer style |
| A18-5 | MEDIUM | `authoriseddialog.h:17` | Constructor uses `= 0` vs `= nullptr` — inconsistent across file set |
| A18-6 | MEDIUM | `authoriseddialog.cpp:190` | Leftover `qDebug` trace in production `setCamera` path |
| A18-7 | MEDIUM | `amberimpactalertdialog.cpp:4` | Unused `#include <QDebug>` |
| A18-8 | MEDIUM | `dialog.cpp` / `amberimpactalertdialog.cpp` | `languageChanged()` never called on `AmberImpactAlertDialog` during language switch |
| A18-9 | LOW | `amberimpactalertdialog.cpp:43–44` | Translation strings duplicated in `showEvent` and `languageChanged` |
| A18-10 | LOW | `authoriseddialog.cpp:160` | Logout state detected by comparing translated button text |
| A18-11 | LOW | `authoriseddialog.h:21` / `.cpp:178` | `setTime` takes `QString` by value instead of `const QString &` |
| A18-12 | LOW | `authoriseddialog.cpp:82–96` | Hard-coded pixel geometry in `showEvent` |
| A18-13 | LOW | `authoriseddialog.cpp:79` | Hard-coded English string `"Welcome, "` not passed through `tr()` |
| A18-14 | LOW | `broadcastuidialog.h:22` / `.cpp:24` | `setUIParam` takes `BroadcastMessage` by value instead of const reference |
# Pass 4 Agent A19 — Code Quality

**Audit run:** 2026-02-28-01
**Branch:** master
**Files reviewed:**
- `ui/checkcompleteddialog.h` + `ui/checkcompleteddialog.cpp`
- `ui/checkconfirmationdialog.h` + `ui/checkconfirmationdialog.cpp`
- `ui/checkquestiondialog.h` + `ui/checkquestiondialog.cpp`

---

## Reading Evidence

### `ui/checkcompleteddialog.h`

**Class:** `CheckCompletedDialog` (extends `QDialog`)

| Symbol | Kind | Line |
|--------|------|------|
| `CheckCompletedDialog(QWidget *parent = 0)` | constructor (public) | 17 |
| `~CheckCompletedDialog()` | destructor (public) | 18 |
| `languageChanged(void)` | method (public) | 20 |
| `isTimerActive()` | method (public) | 21 |
| `stopTimer()` | method (public) | 22 |
| `setCheckResponses(QList<CIGCONF::CheckResponse> &)` | inline method (public) | 23 |
| `openPreopNotes()` | signal | 31 |
| `showEvent(QShowEvent *event = 0)` | method (protected) | 33 |
| `ui` | member (`Ui::CheckCompletedDialog *`) | 36 |
| `m_timer` | member (`QTimer *`) | 37 |
| `m_checkResponses` | member (`QList<CIGCONF::CheckResponse>`) | 38 |

**Types/constants used:** `CIGCONF::CheckResponse` (from `app/cigconfigs.h`)

---

### `ui/checkcompleteddialog.cpp`

**Class:** `CheckCompletedDialog`

| Symbol | Kind | Line |
|--------|------|------|
| `CheckCompletedDialog(QWidget *parent)` | constructor | 7 |
| `~CheckCompletedDialog()` | destructor | 62 |
| `languageChanged()` | method | 67 |
| `showEvent(QShowEvent *event)` | method | 75 |
| `isTimerActive()` | method | 135 |
| `stopTimer()` | method | 140 |

**Macros defined:**
- `NO_ACTIVITY_TIME` — `10000` (milliseconds), defined at line 5

---

### `ui/checkconfirmationdialog.h`

**Class:** `CheckConfirmationDialog` (extends `QDialog`)

| Symbol | Kind | Line |
|--------|------|------|
| `CheckConfirmationDialog(QWidget *parent = 0)` | constructor (public) | 16 |
| `~CheckConfirmationDialog()` | destructor (public) | 17 |
| `confirm(bool yes)` | method (public) | 19 |
| `setQuestion(const QString &question)` | method (public) | 20 |
| `languageChanged(void)` | method (public) | 21 |
| `ui` | member (`Ui::CheckConfirmationDialog *`) | 24 |

No types, enums, or constants defined in this file.

---

### `ui/checkconfirmationdialog.cpp`

**Class:** `CheckConfirmationDialog`

| Symbol | Kind | Line |
|--------|------|------|
| `CheckConfirmationDialog(QWidget *parent)` | constructor | 4 |
| `~CheckConfirmationDialog()` | destructor | 24 |
| `confirm(bool yes)` | method | 29 |
| `setQuestion(const QString &question)` | method | 40 |
| `languageChanged()` | method | 45 |

The file is fully implemented with 54 lines of active code; no commented-out blocks are present.

---

### `ui/checkquestiondialog.h`

**Class:** `CheckQuestionDialog` (extends `QDialog`)

| Symbol | Kind | Line |
|--------|------|------|
| `CheckQuestionDialog(QWidget *parent = 0)` | constructor (public) | 17 |
| `~CheckQuestionDialog()` | destructor (public) | 18 |
| `question() const` | inline accessor (public) | 20 |
| `setQuestion(const QString &question, bool critical = false)` | method (public) | 21 |
| `shown()` | signal | 28 |
| `showEvent(QShowEvent *event)` | method (protected) | 31 |
| `ui` | member (`Ui::CheckQuestionDialog *`) | 34 |
| `m_question` | member (`QString`) | 35 |

No types, enums, or constants defined in this file.

---

### `ui/checkquestiondialog.cpp`

**Class:** `CheckQuestionDialog`

| Symbol | Kind | Line |
|--------|------|------|
| `CheckQuestionDialog(QWidget *parent)` | constructor | 4 |
| `~CheckQuestionDialog()` | destructor | 14 |
| `setQuestion(const QString &question, bool critical)` | method | 19 |
| `showEvent(QShowEvent *event)` | method | 39 |

---

## Findings

---

**A19-1** · HIGH · Deprecated `qrand()` used in `CheckQuestionDialog::setQuestion`

**Description:** `checkquestiondialog.cpp` line 24 calls `qrand() % 2` to randomly swap the YES/NO button positions. `qrand()` was deprecated in Qt 5.10 and is not available in Qt 6 without a compatibility shim. The replacement is `QRandomGenerator::global()->bounded(2)`. Beyond the deprecation issue, the intent of randomly swapping button positions on every question display is itself a usability concern (it prevents muscle-memory confirmation), but the immediate code-quality defect is the use of a deprecated API.

**Fix:** Replace `qrand() % 2` with `QRandomGenerator::global()->bounded(2)` and add `#include <QRandomGenerator>` to the translation unit.

---

**A19-2** · MEDIUM · Leaky abstraction — internal timer details exposed in `CheckCompletedDialog` public interface

**Description:** `checkcompleteddialog.h` declares `isTimerActive()` and `stopTimer()` as public methods, directly surfacing the existence and state of the internal `m_timer` to callers. At `dialog.cpp` lines 877–878 the caller must first query `isTimerActive()` before calling `stopTimer()`, reproducing guard logic that belongs inside the class. The `stopTimer()` implementation in `checkcompleteddialog.cpp` (lines 140–143) already performs the `isActive()` check internally, making the external check at the call site redundant. Exposing timer mechanics in the public API makes it harder to change the auto-dismiss mechanism in future without cascading changes to callers.

**Fix:** Remove `isTimerActive()` from the public interface. `stopTimer()` is idempotent (it already guards internally), so callers should call it unconditionally. Alternatively, rename the pair to a higher-level concept such as `cancelAutoDismiss()`.

---

**A19-3** · MEDIUM · Inconsistent member naming: `setCheckResponses` takes a non-const reference

**Description:** In `checkcompleteddialog.h` line 23 the inline setter is declared as `void setCheckResponses(QList<CIGCONF::CheckResponse> &responses)` — a non-const lvalue reference. This implies the method may modify the caller's list, which it does not (it merely copies into `m_checkResponses`). The other two dialog classes use `const QString &` for analogous setter parameters (`setQuestion` in both `CheckConfirmationDialog` and `CheckQuestionDialog`). The non-const reference is misleading and prevents callers from passing temporary or const objects.

**Fix:** Change the parameter to `const QList<CIGCONF::CheckResponse> &responses`.

---

**A19-4** · MEDIUM · Duplicated UI text setup between `languageChanged()` and `showEvent()` in `CheckCompletedDialog`

**Description:** `checkcompleteddialog.cpp` sets the same four UI strings (`label_2`, `btnSend_2`, `btnRepeat_2`, `btnNotes_2`) in both `languageChanged()` (lines 68–72) and `showEvent()` (lines 81–84). The duplication means any future translation change must be applied in two places and creates a risk of divergence. `CheckConfirmationDialog` and `CheckQuestionDialog` do not share this problem — they separate concerns cleanly.

**Fix:** Have `showEvent()` call `languageChanged()` for the text-setting portion, eliminating the duplicate block.

---

**A19-5** · LOW · Inconsistent constructor default-argument style across the three classes

**Description:** All three header files declare constructors with `QWidget *parent = 0` (null pointer as integer literal). Qt conventions and the C++11 standard prefer `nullptr`. `CheckCompletedDialog` and `CheckConfirmationDialog` also use `= 0` for the `showEvent` default parameter. `CheckQuestionDialog` (line 31) omits the default for `showEvent`, which is inconsistent with `CheckCompletedDialog` (line 33) and `Dialog` (line 93). None of the files uses `= nullptr`.

**Fix:** Replace all `= 0` pointer defaults with `= nullptr` throughout the three header files.

---

**A19-6** · LOW · `NO_ACTIVITY_TIME` macro defined in `.cpp` rather than as a typed constant

**Description:** `checkcompleteddialog.cpp` line 5 defines `NO_ACTIVITY_TIME` as a bare `#define` with value `10000`. This bypasses the type system (no `int` or `constexpr int` context), cannot be referenced from tests or related code without re-defining it, and contributes to the leaky-timer-abstraction problem noted in A19-2. The other two dialog files use no such macros.

**Fix:** Replace with a `static constexpr int kNoActivityTimeMs = 10000;` at class or file scope within `checkcompleteddialog.cpp`, or promote it to a named constant in `cigconfigs.h` if the timeout is a product-level configuration value.

---

**A19-7** · LOW · `showEvent` default parameter `= 0` on a protected override

**Description:** `checkcompleteddialog.h` line 33 declares `void showEvent(QShowEvent *event = 0)`. Adding a default argument to a virtual override (from `QWidget::showEvent(QShowEvent *)`) is unusual, potentially misleading, and the `= 0` form is discouraged in C++11 and later (see A19-5). The base class virtual does not declare a default argument for this parameter. `CheckQuestionDialog` correctly omits the default (line 31).

**Fix:** Remove the `= 0` default from the `showEvent` override declaration in `checkcompleteddialog.h`.

---

**A19-8** · INFO · Missing `languageChanged()` declaration in `CheckQuestionDialog`

**Description:** Both `CheckCompletedDialog` and `CheckConfirmationDialog` expose a public `languageChanged()` method used by the parent `Dialog` to update UI text when the language setting changes. `CheckQuestionDialog` has no `languageChanged()` method at all. Its `setQuestion()` method does call `tr("YES")` and `tr("NO")`, but those translations are only applied when a new question is set, not when the language changes mid-session. This is likely an oversight rather than intentional design.

**Fix:** Add a `languageChanged()` method to `CheckQuestionDialog` that re-applies `tr("YES")`/`tr("NO")` to the buttons, matching the pattern of the sibling classes.

---

## Summary Table

| ID | Severity | Title |
|----|----------|-------|
| A19-1 | HIGH | Deprecated `qrand()` in `CheckQuestionDialog::setQuestion` |
| A19-2 | MEDIUM | Leaky abstraction — timer details in `CheckCompletedDialog` public interface |
| A19-3 | MEDIUM | `setCheckResponses` takes non-const reference, inconsistent with sibling setters |
| A19-4 | MEDIUM | Duplicate UI text setup in `languageChanged()` and `showEvent()` |
| A19-5 | LOW | `= 0` pointer defaults should be `= nullptr` throughout |
| A19-6 | LOW | `NO_ACTIVITY_TIME` defined as untyped `#define` macro |
| A19-7 | LOW | `showEvent` protected override carries redundant default argument `= 0` |
| A19-8 | INFO | `CheckQuestionDialog` missing `languageChanged()` inconsistent with siblings |

**Total findings: 8** (1 HIGH, 3 MEDIUM, 3 LOW, 1 INFO)
# Pass 4 Agent A20 — Code Quality

**Audit run:** 2026-02-28-01
**Branch:** master
**Files reviewed:**
- `ui/checkstartdialog.h` + `ui/checkstartdialog.cpp`
- `ui/commentdialog.h` + `ui/commentdialog.cpp`
- `ui/dialog.h` + `ui/dialog.cpp`

---

## Reading Evidence

### `ui/checkstartdialog.h`

**Class:** `CheckStartDialog` (extends `QDialog`)

| Symbol | Kind | Line |
|--------|------|------|
| `CheckStartDialog(QWidget *parent = 0)` | Constructor | 15 |
| `~CheckStartDialog()` | Destructor | 16 |
| `setMandatory(bool mandatory)` | Public method | 17 |
| `languageChanged(void)` | Public method | 18 |
| `ui` | Private member (`Ui::CheckStartDialog*`) | 25 |

No enums, types, or constants defined in this file.

---

### `ui/checkstartdialog.cpp`

| Symbol | Kind | Line |
|--------|------|------|
| `CheckStartDialog::CheckStartDialog(QWidget*)` | Constructor | 5 |
| `CheckStartDialog::~CheckStartDialog()` | Destructor | 18 |
| `CheckStartDialog::setMandatory(bool)` | Method | 23 |
| `CheckStartDialog::languageChanged()` | Method | 34 |

---

### `ui/commentdialog.h`

**Class:** `CommentDialog` (extends `QDialog`)

**Macros / Constants:**

| Name | Value | Line |
|------|-------|------|
| `NO_ACTIVITY_TIME` | `10000` | 12 |
| `MAX_CHARACTER` | `100` | 13 |

**Enum:**

| Name | Enumerators | Line |
|------|-------------|------|
| `CommentDialogType` | `Unlock`, `Preop` | 15 |

**Methods:**

| Symbol | Kind | Line |
|--------|------|------|
| `CommentDialog(CommentDialogType, QWidget*)` | Constructor | 26 |
| `~CommentDialog()` | Destructor | 27 |
| `UpdateTextInput(QString, onScreenKeyboard::CtrlButton)` | Public method | 29 |
| `onkeyboardClosed()` | Public method | 30 |
| `onUnlkReasonSelected()` | Public method | 31 |
| `languageChanged()` | Public method | 32 |
| `debounce()` | Private method | 37 |
| `reset()` | Private method | 38 |
| `showWidgets()` | Private method | 39 |
| `showEvent(QShowEvent*)` | Protected override | 47 |
| `hideEvent(QHideEvent*)` | Protected override | 48 |
| `run_keyboard_lineEdit()` | Private slot | 51 |
| `onDone()` | Private slot | 52 |
| `onSkip()` | Private slot | 53 |

**Members:** `ui`, `lineEditkeyboard`, `m_timer`, `m_lastPress`, `m_dlgType`, `m_unlkReasonDlg`

---

### `ui/commentdialog.cpp`

| Symbol | Kind | Line |
|--------|------|------|
| `CommentDialog::CommentDialog(...)` | Constructor | 9 |
| `CommentDialog::~CommentDialog()` | Destructor | 36 |
| `CommentDialog::hideEvent(QHideEvent*)` | Override | 41 |
| `CommentDialog::showWidgets()` | Private | 46 |
| `CommentDialog::showEvent(QShowEvent*)` | Override | 91 |
| `CommentDialog::onkeyboardClosed()` | Public | 98 |
| `CommentDialog::UpdateTextInput(...)` | Public | 104 |
| `CommentDialog::run_keyboard_lineEdit()` | Private slot | 121 |
| `CommentDialog::onDone()` | Private slot | 134 |
| `CommentDialog::onSkip()` | Private slot | 168 |
| `CommentDialog::debounce()` | Private | 188 |
| `CommentDialog::reset()` | Private | 199 |
| `CommentDialog::onUnlkReasonSelected()` | Public | 205 |
| `CommentDialog::languageChanged()` | Public | 214 |

---

### `ui/dialog.h`

**Class:** `Dialog` (extends `QDialog`)

**Signals:**

| Signal | Line |
|--------|------|
| `driverChanged(quint64)` | 79 |
| `lastCheckDriverChanged(quint64)` | 80 |
| `screenLocked(CIGCONF::MaintLockedCode)` | 81 |
| `setRelayOut(bool, bool)` | 82 |
| `setRelay2Out(bool)` | 83 |
| `sendGmtpMessage(CIGCONF::GmtpMessage, const QByteArray&)` | 84 |
| `resetCanStates(bool)` | 85 |
| `forceBroadcastUIClose()` | 86 |
| `log(QByteArray&)` | 87 |
| `updatePreopTimer(QString)` | 88 |
| `amberDialogAboutToShow(bool)` | 89 |

**Public methods (declared):**

| Symbol | Line |
|--------|------|
| `Dialog(QWidget *parent = 0)` | 44 |
| `~Dialog()` | 45 |
| `onPowerChanged(CIGCONF::PowerState)` | 47 |
| `onReboot()` | 48 |
| `onBleReady(bool)` | 49 |
| `onNetworkReady(bool)` | 50 |
| `onCardAuthorised(bool, quint64)` | 51 |
| `onCmdLogin(quint64)` | 52 |
| `onIdleTimeout()` | 53 |
| `lockScreen(CIGCONF::MaintLockedCode, bool)` | 54 |
| `ambertImpactScreen()` | 55 |
| `updateLux(int)` | 57 |
| `updateStatus(...)` | 58 |
| `updateBatteryStatus(...)` | 59 |
| `updateExpModInfo(QByteArray)` | 60 |
| `onBroadcastMsgReceived(CIGCONF::BroadcastMessage)` | 61 |
| `showInformationScreen()` | 62 |
| `updateLoginImage()` | 63 |
| `quickPowerUpdate(bool)` | 64 |
| `onDemandStarted(...)` | 66 |
| `onDemandExtended(...)` | 67 |
| `onDemandEnded(...)` | 68 |
| `onLanguageChanged(void)` | 70 |
| `updateCamera()` | 72 |

**Private methods (declared in header):**

| Symbol | Line |
|--------|------|
| `onPinCode()` | 99 |
| `onCardSwiped(...)` | 100 |
| `onPinDialogAccepted()` | 102 |
| `onAuthorisedDialogAccepted()` | 103 |
| `onAuthorisedUserLogout()` | 104 |
| `onOptionalCheckConfirmed()` | 105 |
| `onCheckStartDialogAccepted()` | 106 |
| `onCheckQuestionDialogFinished(int)` | 107 |
| `onCheckConfirmationDialogFinished(int)` | 108 |
| `onCheckCompletedDialogAccepted()` | 109 |
| `onCheckCompletedDialogRejected()` | 110 |
| `onUnlockedDialogAccepted()` | 111 |
| `onProcessUnlock()` | 112 |
| `onPreopCommentDone()` | 113 |
| `onBroadcastDialogDone(int)` | 114 |
| `isValidId(quint64)` | 116 |
| `isChecklistEmpty(bool)` | 117 |
| `bypassChecklist()` | 118 |
| `clearWidgets()` | 119 |
| `login(quint64)` | 121 |
| `postLogin()` | 122 |
| `postMaintenanceLogin()` | 123 |
| `logout()` | 124 |
| `openMenuDialog()` | 125 |
| `startCheck(bool)` | 127 |
| `sendStartCheck()` | 128 |
| `superListUpdated(bool)` | 130 |
| `updateOnDemand()` | 131 |
| `convorStatusUpdated()` | 133 |
| `isOnDemandExpired()` | 135 |
| `fullLockStart()` | 137 |
| `updateFullLock()` | 138 |
| `updateTime()` | 140 |
| `writeMsgToQueue(CIGCONF::BroadcastMessage)` | 201 |
| `displayNextBroadcastMessage()` | 202 |
| `clearMsgQueue()` | 203 |
| `initOnScreenPreopTimer(quint16)` | 207 |
| `showCustomTimeFormat(quint32)` | 208 |
| `adjustPreopDialogs(bool)` | 212 |
| `updateBLEConSpinner(quint8)` | 214 |

**Private slot:**

| Symbol | Line |
|--------|------|
| `on_pushButton_clicked()` | 96 |

**Inner struct:**

| Name | Fields | Line |
|------|--------|------|
| `BroadcastMessageResponse` | `id`, `driverId`, `dispTimestamp` | 191–195 |

---

### `ui/dialog.cpp` — implemented functions

| Symbol | Line |
|--------|------|
| `Dialog::Dialog(...)` | 39 |
| `Dialog::~Dialog()` | 207 |
| `Dialog::updateBLEConSpinner(quint8)` | 212 |
| `Dialog::showInformationScreen()` | 228 |
| `Dialog::mouseReleaseEvent(QMouseEvent*)` | 238 |
| `Dialog::showEvent(QShowEvent*)` | 245 |
| `Dialog::updateLoginImage()` | 261 |
| `Dialog::onPinCode()` | 269 |
| `Dialog::onCardSwiped(...)` | 277 |
| `Dialog::onPinDialogAccepted()` | 319 |
| `Dialog::onAuthorisedDialogAccepted()` | 325 |
| `Dialog::onAuthorisedUserLogout()` | 332 |
| `Dialog::onCheckStartDialogAccepted()` | 339 |
| `Dialog::onCheckQuestionDialogFinished(int)` | 345 |
| `Dialog::onCheckConfirmationDialogFinished(int)` | 359 |
| `Dialog::onCheckCompletedDialogAccepted()` | 395 |
| `Dialog::onCheckCompletedDialogRejected()` | 449 |
| `Dialog::onUnlockedDialogAccepted()` | 461 |
| `Dialog::onProcessUnlock()` | 481 |
| `Dialog::onPreopCommentDone()` | 513 |
| `Dialog::onBroadcastDialogDone(int)` | 517 |
| `Dialog::login(quint64)` | 543 |
| `Dialog::openMenuDialog()` | 577 |
| `Dialog::postLogin()` | 590 |
| `Dialog::postMaintenanceLogin()` | 659 |
| `Dialog::logout()` | 674 |
| `Dialog::lockScreen(CIGCONF::MaintLockedCode, bool)` | 691 |
| `Dialog::ambertImpactScreen()` | 728 |
| `Dialog::startCheck(bool)` | 733 |
| `Dialog::sendStartCheck()` | 767 |
| `Dialog::isValidId(quint64)` | 773 |
| `Dialog::isChecklistEmpty(bool)` | 781 |
| `Dialog::bypassChecklist()` | 792 |
| `Dialog::clearWidgets()` | 875 |
| `Dialog::onPowerChanged(CIGCONF::PowerState)` | 899 |
| `Dialog::onReboot()` | 927 |
| `Dialog::onBleReady(bool)` | 934 |
| `Dialog::onNetworkReady(bool)` | 950 |
| `Dialog::updateStatus(...)` | 955 |
| `Dialog::onCardAuthorised(bool, quint64)` | 960 |
| `Dialog::onCmdLogin(quint64)` | 980 |
| `Dialog::onIdleTimeout()` | 986 |
| `Dialog::updateLux(int)` | 1008 |
| `Dialog::updateBatteryStatus(...)` | 1013 |
| `Dialog::updateExpModInfo(QByteArray)` | 1018 |
| `Dialog::superListUpdated(bool)` | 1023 |
| `Dialog::updateOnDemand()` | 1037 |
| `Dialog::onDemandStarted(...)` | 1069 |
| `Dialog::onDemandExtended(...)` | 1086 |
| `Dialog::onDemandEnded(...)` | 1106 |
| `Dialog::isOnDemandExpired()` | 1125 |
| `Dialog::convorStatusUpdated()` | 1135 |
| `Dialog::onBroadcastMsgReceived(CIGCONF::BroadcastMessage)` | 1155 |
| `Dialog::writeMsgToQueue(CIGCONF::BroadcastMessage)` | 1169 |
| `Dialog::displayNextBroadcastMessage()` | 1177 |
| `Dialog::clearMsgQueue()` | 1203 |
| `Dialog::initOnScreenPreopTimer(quint16)` | 1209 |
| `Dialog::adjustPreopDialogs(bool)` | 1225 |
| `Dialog::showCustomTimeFormat(quint32)` | 1249 |
| `Dialog::onLanguageChanged()` | 1260 |
| `Dialog::on_pushButton_clicked()` | 1285 |
| `Dialog::updateTime()` | 1291 |
| `Dialog::quickPowerUpdate(bool)` | 1314 |
| `Dialog::updateCamera()` | 1321 |

---

## Findings

---

**A20-1** · HIGH · `fullLockStart` and `updateFullLock` declared but never implemented

**Description:** `dialog.h` lines 137–138 declare two private methods, `fullLockStart()` and `updateFullLock()`, that have no corresponding definition anywhere in `dialog.cpp` or any other translation unit. The feature they were intended to implement — presumably a "full lockout" timer-driven UI update flow — is instead handled inline with direct `gCfg->fullLockoutEnable()` / `gCfg->fullLockoutTimeout()` checks scattered through the codebase. Leaving unimplemented declarations in the header is a latent build and maintenance hazard: any future caller of these methods will fail to link, and readers cannot tell whether the omission is intentional.

**Fix:** Either implement both methods or remove both declarations from `dialog.h` and confirm the full-lockout logic that was meant to call them is fully covered by the existing inline guards.

---

**A20-2** · MEDIUM · `onPreopCommentDone()` is a declared handler with an empty body

**Description:** `dialog.h` line 113 declares `onPreopCommentDone()` as a private method. Its implementation at `dialog.cpp` lines 513–515 is a completely empty stub:

```cpp
void Dialog::onPreopCommentDone() {

}
```

The method is never connected to any signal. The pre-op comment accept/reject paths in the constructor (lines 122–127) use separate lambdas that call `onCheckCompletedDialogAccepted()` and `m_checkCompletedDialog->open()` directly, making `onPreopCommentDone()` unreachable dead code. Its presence implies an incomplete refactoring.

**Fix:** Remove the declaration from `dialog.h` and the empty definition from `dialog.cpp`. If the intended handler logic was never ported, document what behavior is missing and implement it.

---

**A20-3** · MEDIUM · `onOptionalCheckConfirmed()` declared but never implemented or called

**Description:** `dialog.h` line 105 declares private method `onOptionalCheckConfirmed()`. There is no definition of this method anywhere in `dialog.cpp`, and no `connect()` call or direct invocation of it exists in the codebase. This is a second unimplemented private method alongside `fullLockStart` and `updateFullLock`, indicating a pattern of stale declarations left from abandoned feature work.

**Fix:** Remove the declaration from `dialog.h`. If optional-check-confirmed logic is genuinely needed, implement and connect it.

---

**A20-4** · MEDIUM · Commented-out multi-line code block in `onCheckQuestionDialogFinished`

**Description:** `dialog.cpp` lines 349–357 contain a large commented-out block inside `onCheckQuestionDialogFinished`:

```cpp
/*m_checkConfirmationDialog->confirm(m_checkSelectedYes);
m_checkConfirmationDialog->setQuestion(m_checkQuestionDialog->question());
m_checkConfirmationDialog->open();
if (m_survTo)
{
    m_overlay->show();
    m_overlay->raise();
}*/
```

This represents the original two-step confirmation flow that was bypassed when the design was simplified to skip the intermediate confirmation dialog. The dead code causes confusion about whether `CheckConfirmationDialog` is still part of the active flow, and whether `CheckConfirmationDialog::confirm()` and `CheckConfirmationDialog::setQuestion()` still need to be maintained.

**Fix:** Delete the commented-out block. If `CheckConfirmationDialog` is now fully unused in the normal question flow, audit whether the class and its connections (lines 104–105, 1227–1228) can also be removed.

---

**A20-5** · MEDIUM · Commented-out `#include` and log call for `SerialLogger`

**Description:** `dialog.cpp` line 21 has `//#include "platform/seriallogger.h"` and line 312 has `//SerialLogger::log("[MONIT] Login attempt while exp mod comms not ready");`. The logger appears to have been deactivated without a replacement. The commented include is particularly problematic because it hides whether `SerialLogger` is still a valid, maintained module.

**Fix:** Remove both commented-out lines. If structured logging is still needed for this code path, replace with the active logging mechanism used elsewhere (e.g., `qDebug` or the `log()` signal).

---

**A20-6** · MEDIUM · Commented-out `QTimer::singleShot` lock call in constructor

**Description:** `dialog.cpp` line 204 contains:

```cpp
//QTimer::singleShot(0, [this](){if (gCfg->maintCode() != CIGCONF::MaintNormal) lockScreen(gCfg->maintCode());});
```

This duplicates the `showEvent` logic at line 257. The commented form also omits the `remote` parameter (`false`) that the live call passes. Leaving this in place suggests an incomplete decision about the preferred initialization path.

**Fix:** Remove the commented line; the live `showEvent` implementation already handles initial lock state.

---

**A20-7** · MEDIUM · Commented-out `onIdleTimeout` early return for VOR status

**Description:** `dialog.cpp` lines 992–993:

```cpp
//    if (gCfg->convorStatus())
//        return;
```

This guard was silently removed from `onIdleTimeout`. Without this guard, an idle timeout while the vehicle is in "Vehicle Out of Service" (VOR/convor) mode will log the driver out via `logout()`, which conflicts with the convor session behavior enforced elsewhere (e.g., `lockScreen` returns early on convor, `login` routes convor users to `m_vorwarningDialog`). The comment gives no explanation for why this guard was disabled.

**Fix:** Determine the correct intended behavior for idle timeout under convor status. Either restore the guard with an explanatory comment or remove the commented lines and document the decision.

---

**A20-8** · MEDIUM · Commented-out wiegand recalculation in `onCardSwiped`

**Description:** `dialog.cpp` line 308:

```cpp
//quint64 wiegand = EM070::WiegandRfid::wiegandData(facility, number);
```

This shadowed local was commented out at an unknown time. The variable name matches the parameter name, and the `facility`/`number` parameters are now suppressed with `Q_UNUSED` (lines 279–280). The function parameter list still carries `quint16 facility` and `quint32 number` which are never used. This is misleading; readers may assume the facility/number values are validated.

**Fix:** Remove the commented line and the two unused parameters from the `onCardSwiped` signature (both declaration in `dialog.h` line 100 and definition in `dialog.cpp` line 277). Update the two call sites accordingly.

---

**A20-9** · LOW · Typo in public method name `ambertImpactScreen`

**Description:** `dialog.h` line 55 declares `void ambertImpactScreen()`. The name contains a spurious `t` — it should be `amberImpactScreen`. All callers (and the implementation at `dialog.cpp` line 728) use the same typo, so there is no current compile error, but the name is confusing and inconsistent with related identifiers such as `amberDialogAboutToShow` and `AmberImpactAlertDialog`.

**Fix:** Rename `ambertImpactScreen` to `amberImpactScreen` across the declaration, definition, and all call sites.

---

**A20-10** · LOW · Naming inconsistency: `UpdateTextInput` violates `camelCase` convention

**Description:** In `CommentDialog`, the public method `UpdateTextInput` (`commentdialog.h` line 29) uses `PascalCase`, inconsistent with every other method in the same class (`onkeyboardClosed`, `onUnlkReasonSelected`, `languageChanged`, `run_keyboard_lineEdit`, `onDone`, `onSkip`, `debounce`, `reset`, `showWidgets`). There is also `onkeyboardClosed` (lowercase `k`) versus the typical Qt `onFooBar` pattern, but the `UpdateTextInput` inconsistency is the most prominent.

**Fix:** Rename `UpdateTextInput` to `updateTextInput` throughout (declaration, definition, and the `connect` call in the constructor at `commentdialog.cpp` line 23).

---

**A20-11** · LOW · `onkeyboardClosed` and `onUnlkReasonSelected` are public but should be private

**Description:** `commentdialog.h` lines 30–31 declare `onkeyboardClosed()` and `onUnlkReasonSelected()` as `public`. Both methods are internal response handlers connected to child/grandchild widget signals in the constructor. Nothing outside `CommentDialog` calls them directly. Exposing them as public widens the class interface unnecessarily and risks accidental external invocation.

**Fix:** Move both methods to the `private slots:` section alongside `run_keyboard_lineEdit`, `onDone`, and `onSkip`.

---

**A20-12** · LOW · `showEvent` default-argument override is a deprecated Qt pattern

**Description:** `commentdialog.h` line 47 declares `void showEvent(QShowEvent *event = 0)` with a default null argument. The same pattern appears in `checkstartdialog.h` (via the base) and `dialog.h` line 93. Qt virtual event handlers are never invoked with a null pointer by the framework; the default argument exists only because `commentdialog.cpp` line 202 calls `showEvent()` with no arguments from `reset()`. Providing a default argument to an overriding virtual is a code smell: it can silently fail to call the base class's override chain correctly and triggers `-Woverloaded-virtual` warnings on some compilers.

**Fix:** Remove the default argument from the override declaration. In `reset()`, replace the no-argument call to `showEvent()` with a direct call to `showWidgets()`, which is the actual work being re-triggered.

---

**A20-13** · LOW · `QWidget *parent = 0` should use `nullptr`

**Description:** All three headers use `QWidget *parent = 0` as the constructor default (`checkstartdialog.h` line 15, `commentdialog.h` line 26, `dialog.h` line 44). Qt 5 and Qt 6 both deprecate raw `0` in favor of `nullptr` for pointer defaults. The rest of the codebase mixes both forms (e.g., `commentdialog.h` already uses `nullptr` for `parent` in some internal declarations).

**Fix:** Replace `= 0` with `= nullptr` in all three constructor declarations for consistency with the C++11 style used elsewhere in the project.

---

**A20-14** · LOW · Magic number `2*60*1000` for broadcast message beeper interval

**Description:** `dialog.cpp` line 1198:

```cpp
m_messageTimer->start(2*60*1000);
```

This inline computation (two minutes in milliseconds) is not named or explained. Unlike `NO_ACTIVITY_TIME` (which is a named macro in `commentdialog.h`), this value is embedded directly in the logic with no symbolic label, making it harder to discover or adjust.

**Fix:** Define a named constant, e.g., `constexpr int BROADCAST_BEEPER_INTERVAL_MS = 2 * 60 * 1000;`, and use it at the call site.

---

**A20-15** · LOW · String comparison used as state machine discriminator in `onDone`/`onSkip`

**Description:** `commentdialog.cpp` lines 147 and 173 gate the confirm action by comparing the button label text to a translated string:

```cpp
if (ui->btnDone->text() == tr("Confirm?")) { ... }
if (ui->btnSkipButton->text() == tr("Confirm?")) { ... }
```

Using a localised UI string as the state variable is fragile: a translation change, a font renderer substitution, or a future l10n fix for the `"Confirm?"` string (e.g., making it language-specific) would silently break the two-tap confirmation flow without a compile error. The same issue affects the `onSkip` path.

**Fix:** Introduce a private boolean flag (e.g., `m_confirmPending`) that is set when the first tap is received and cleared on timer reset. Use that flag instead of text comparison to gate the confirm action.

---

**A20-16** · INFO · `Dialog` is a 1,325-line orchestrator tightly coupling 15+ child dialogs

**Description:** `Dialog` directly owns and wires 15 child dialog objects (`m_pinDialog`, `m_authorisedDialog`, `m_checkStartDialog`, `m_checkQuestionDialog`, `m_checkConfirmationDialog`, `m_checkCompletedDialog`, `m_lockedDialog`, `m_unlockedDialog`, `m_messageDialog`, `m_informationDialog`, `m_onDemandDialog`, `m_unlockReasonDlg`, `m_preopCommentDlg`, `m_broadcastDialog`, `m_supervisorDialog`, `m_languageDialog`, `m_amberImpactAlertDialog`, `m_vorwarningDialog`), three hardware driver objects, four `QTimer` objects, and carries all application state. Each new dialog class is a concrete type exposed directly as a private member; there is no abstraction layer between `Dialog` and the child widgets it orchestrates. While this is a known legacy architecture, it makes unit testing, feature flagging, and any future UI recomposition disproportionately expensive.

**Fix:** No immediate action required for correctness. For long-term maintainability, consider extracting state machines (e.g., the checklist flow, the lock/unlock flow) into separate controller objects and injecting child dialogs through interfaces rather than owning them directly.

---

**A20-17** · INFO · Acknowledged TODO: `gCfg` not guarded for multi-thread access

**Description:** `dialog.cpp` lines 35–37:

```cpp
/*
 * TODO: all functions of gCfg might be guarded as they are used in multithread
 */
```

This comment acknowledges a known concurrency risk that has not been addressed. It is tracked here for completeness; the thread-safety analysis of `gCfg` is out of scope for this pass.

**Fix:** Raise as a separate task; address in a dedicated concurrency audit pass.

---

## Summary Table

| ID | Severity | Title |
|----|----------|-------|
| A20-1 | HIGH | `fullLockStart` / `updateFullLock` declared but never implemented |
| A20-2 | MEDIUM | `onPreopCommentDone()` is an empty stub never connected to any signal |
| A20-3 | MEDIUM | `onOptionalCheckConfirmed()` declared but never implemented or called |
| A20-4 | MEDIUM | Commented-out multi-line confirmation dialog block in `onCheckQuestionDialogFinished` |
| A20-5 | MEDIUM | Commented-out `SerialLogger` include and log call |
| A20-6 | MEDIUM | Commented-out duplicate `QTimer::singleShot` lock call in constructor |
| A20-7 | MEDIUM | Commented-out VOR status guard in `onIdleTimeout` with unexplained intent |
| A20-8 | MEDIUM | Commented-out wiegand recalculation leaves two parameters permanently unused |
| A20-9 | LOW | Typo `ambertImpactScreen` (spurious `t`) in public API |
| A20-10 | LOW | `UpdateTextInput` uses PascalCase inconsistent with rest of class |
| A20-11 | LOW | `onkeyboardClosed` and `onUnlkReasonSelected` are public but should be private slots |
| A20-12 | LOW | `showEvent` default-argument override is a deprecated / warning-prone pattern |
| A20-13 | LOW | Constructor `parent` defaults use `= 0` instead of `= nullptr` |
| A20-14 | LOW | Magic number `2*60*1000` for broadcast beeper timer interval |
| A20-15 | LOW | Translated button label string used as state-machine discriminator in `onDone`/`onSkip` |
| A20-16 | INFO | `Dialog` tightly couples 15+ child dialogs in a 1,325-line God-class |
| A20-17 | INFO | Acknowledged unresolved TODO for `gCfg` multi-thread safety |

**Totals:** 1 HIGH, 6 MEDIUM, 7 LOW, 2 INFO
# Pass 4 Agent A21 — Code Quality

**Audit run:** 2026-02-28-01
**Branch:** master
**Files reviewed:**
- `ui/informationdialog.h` + `ui/informationdialog.cpp`
- `ui/keyfilter.h` + `ui/keyfilter.cpp`
- `ui/languagedialog.h` + `ui/languagedialog.cpp`

---

## Reading Evidence

### `ui/informationdialog.h`

**Class:** `InformationDialog : public QDialog`

| Line | Member / Function |
|------|-------------------|
| 21 | `explicit InformationDialog(QWidget *parent = 0)` — constructor |
| 22 | `~InformationDialog()` — destructor |
| 23 | `void updateInformationScreen()` |
| 24 | `void setLux(int lux)` |
| 25 | `void setStatus(QByteArray IO, bool Rly1, bool Rly2, QByteArray can, const QByteArray &rssi, const QByteArray &moni, bool netStat, bool mdemStat, bool wifiStat, qint8 sat, qint32 lat, qint32 lon)` |
| 26 | `void setConfigParam()` |
| 27 | `void setBatteryStatus(bool avail, int state, int fault, quint16 voltage, qint16 current, quint16 temp, quint16 remainingCapacity)` |
| 28 | `void setExpModInfo(QByteArray mainVersion)` |
| 29 | `void setSuperMasterStatus()` |
| 30 | `void setVOR()` |
| 31 | `void setLastWiegand(quint64 id)` |
| 32 | `void languageChanged()` |
| 35 | `void showEvent(QShowEvent *)` — protected override |
| 36 | `void hideEvent(QHideEvent *)` — protected override |

**Private members:**
- `Ui::InformationDialog *ui` (line 39)
- `QMap<int, QString> m_chargeStatusMap` (line 40)
- `QMap<int, QString> m_chargeFaultMap` (line 41)
- `QTimer *m_updateConfigTmr` (line 42)

**Types / constants defined in implementation:**
- `#define UPDATE_CONFIG_TIMER_MS 5000` (informationdialog.cpp, line 9)

---

### `ui/informationdialog.cpp`

| Line | Function |
|------|----------|
| 11  | `InformationDialog::InformationDialog(QWidget *parent)` — constructor |
| 89  | `void InformationDialog::hideEvent(QHideEvent *)` |
| 94  | `void InformationDialog::showEvent(QShowEvent *)` |
| 101 | `InformationDialog::~InformationDialog()` |
| 106 | `void InformationDialog::setLux(int lux)` |
| 111 | `void InformationDialog::setStatus(QByteArray IO, bool Rly1, bool Rly2, QByteArray can, const QByteArray &rssi, const QByteArray &moni, bool netStat, bool modemStat, bool wifiStat, qint8 sat, qint32 lat, qint32 lon)` |
| 126 | `void InformationDialog::setBatteryStatus(bool avail, int state, int fault, quint16 voltage, qint16 current, quint16 temp, quint16 remainingCapacity)` |
| 137 | `void InformationDialog::setConfigParam()` |
| 195 | `void InformationDialog::setExpModInfo(QByteArray mainVersion)` |
| 200 | `void InformationDialog::setSuperMasterStatus()` |
| 220 | `void InformationDialog::setVOR()` |
| 228 | `void InformationDialog::setLastWiegand(quint64 id)` |
| 233 | `void InformationDialog::updateInformationScreen()` |
| 240 | `void InformationDialog::languageChanged()` |

---

### `ui/keyfilter.h`

**Class:** `KeyFilter : public QObject`

| Line | Member / Function |
|------|-------------------|
| 13 | `explicit KeyFilter(QObject *parent = nullptr)` — constructor |
| 13 | `static bool isPowerKeyPressed()` — static inline accessor |
| 16 | `signal: void showInfoDialog()` |
| 18 | `bool eventFilter(QObject *obj, QEvent *event)` — protected override |
| 21 | `static bool m_powerKeyPressed` — static private member |
| 22 | `QSet<int> m_pressedKeys` — private member |
| 24 | `QTimer *m_timer` — private member |
| 25 | `int m_leftKeyCount` |
| 26 | `int m_rightKeyCount` |
| 27 | `int m_upKeyCount` |
| 28 | `int m_downKeyCount` |
| 29 | `bool m_leftKeyPressed` |
| 30 | `bool m_rightKeyPressed` |
| 31 | `bool m_upKeyPressed` |
| 32 | `bool m_downKeyPressed` |
| 34 | `void resetKeyCount()` — private |
| 35 | `void incrementKeyCount(int key)` — private |
| 36 | `int getKeyCount(int key)` — private |
| 37 | `void resetKeyCounter(int key)` — private |
| 38 | `bool getPressState(int key)` — private |
| 39 | `void setPressState(int key, bool state)` — private |

---

### `ui/keyfilter.cpp`

| Line | Function |
|------|----------|
| 6   | `bool KeyFilter::m_powerKeyPressed = false` — static member definition |
| 8   | `KeyFilter::KeyFilter(QObject *parent)` — constructor |
| 20  | `bool KeyFilter::eventFilter(QObject *obj, QEvent *event)` |
| 66  | `void KeyFilter::resetKeyCount()` |
| 76  | `void KeyFilter::incrementKeyCount(int key)` |
| 101 | `int KeyFilter::getKeyCount(int key)` |
| 114 | `void KeyFilter::resetKeyCounter(int key)` |
| 126 | `void KeyFilter::setPressState(int key, bool state)` |
| 145 | `bool KeyFilter::getPressState(int key)` |

---

### `ui/languagedialog.h`

**Class:** `LanguageDialog : public QDialog`

| Line | Member / Function |
|------|-------------------|
| 15 | `explicit LanguageDialog(QWidget *parent = nullptr)` — constructor |
| 16 | `~LanguageDialog()` |
| 17 | `void languageChanged()` |
| 18 | `void startScreenTimeout()` |
| 21 | `signal: void sigLanguageChanged()` |
| 24 | `slot: void on_btnEnglish_clicked()` — private slot |
| 25 | `slot: void on_btnSpanish_clicked()` — private slot |
| 26 | `slot: void on_btnQuit_clicked()` — private slot |
| 29 | `void showEvent(QShowEvent *event = 0)` — protected override |
| 32 | `Ui::LanguageDialog *ui` — private member |
| 33 | `QTimer *m_timer` — private member |
| 34 | `bool debounce()` — private |
| 35 | `quint32 m_lastPress` — private member |

**Constants defined in implementation:**
- `#define NO_ACTIVITY_TIME (10000)` (languagedialog.cpp, line 10)

---

### `ui/languagedialog.cpp`

| Line | Function |
|------|----------|
| 12 | `LanguageDialog::LanguageDialog(QWidget *parent)` — constructor |
| 25 | `LanguageDialog::~LanguageDialog()` |
| 30 | `void LanguageDialog::on_btnEnglish_clicked()` |
| 42 | `void LanguageDialog::on_btnSpanish_clicked()` |
| 54 | `void LanguageDialog::on_btnQuit_clicked()` |
| 59 | `void LanguageDialog::showEvent(QShowEvent *event)` |
| 65 | `bool LanguageDialog::debounce()` |
| 76 | `void LanguageDialog::languageChanged()` |
| 84 | `void LanguageDialog::startScreenTimeout()` |

---

## Findings

---

**A21-1** · HIGH · Deprecated `qChecksum` signature — potential length mismatch and Qt 6 breakage

**Description:** `informationdialog.cpp` line 74 calls:
```cpp
quint16 checksum = qChecksum(string.toLatin1().constData(), string.size());
```
Two distinct problems exist here. First, `string` is a `QString`; `string.size()` returns the number of UTF-16 code units, not the number of Latin-1 bytes produced by `.toLatin1()`. For any version string containing only ASCII characters these numbers coincide, but the distinction is latent and would cause an over-read the moment a non-ASCII character appears. Second, the two-argument `qChecksum(const char*, uint)` overload was deprecated in Qt 5.9 and removed in Qt 6. The project `.pro` file contains `QT_DEPRECATED_WARNINGS`, meaning this call already triggers a compiler warning on Qt 5.9+.

**Fix:** Store the `QByteArray` in a named local, pass its own `.size()`, and use the Qt 5.9+ three-argument overload that accepts a `QChecksumsType` so the call compiles cleanly on both Qt 5 and Qt 6:
```cpp
QByteArray la = string.toLatin1();
quint16 checksum = qChecksum(la.constData(), static_cast<uint>(la.size()));
```

---

**A21-2** · MEDIUM · `setStatus` parameter name inconsistency between declaration and definition

**Description:** The header declaration at `informationdialog.h:25` names the modem-status parameter `mdemStat`, while the implementation at `informationdialog.cpp:111` names it `modemStat`. Although this does not affect compilation (parameter names in declarations are advisory), it is a maintenance hazard: readers of the header see an abbreviated name that does not match the implementation, and grep/cross-reference tools may miss usages.

**Fix:** Align the parameter name to the more descriptive form used in the implementation. Change `informationdialog.h:25` to use `modemStat` consistently.

---

**A21-3** · MEDIUM · Leaky abstraction — `setStatus` takes 12 positional arguments

**Description:** `InformationDialog::setStatus` at `informationdialog.h:25` / `informationdialog.cpp:111` accepts 12 positional arguments covering relay states, CSQ, network/modem/WiFi status, MONI, digital IO, CAN data, and GPS coordinates. This is far beyond the commonly accepted limit of 4–5 parameters and forces every call site to supply all 12 values in the correct order with no compiler protection against transposition of same-typed arguments (e.g., `bool Rly1, bool Rly2` followed by three more booleans). The coupling between the caller (which assembles all hardware status at once) and the dialog's display concerns is maximal.

**Fix:** Introduce a value-type status struct (e.g., `struct DeviceStatus`) that groups related fields. The `setStatus` call becomes `setStatus(const DeviceStatus &)`, callers populate the struct by name, and the dialog remains decoupled from the order of hardware fields.

---

**A21-4** · MEDIUM · Hardcoded hardware revision string with TODO comment

**Description:** `informationdialog.cpp:42` contains:
```cpp
// TODO: currently doesn't support
ui->labelHwVer->setText("EM-070-02-B");
```
The hardware version is a hardcoded literal with an unresolved TODO. Because this string is also used in the `qChecksum` calculation (lines 69–74) that generates the barcode on the System tab, deploying on hardware with a different PCB revision silently produces a wrong barcode without any runtime error.

**Fix:** Read the hardware version from a device file, configuration source, or compile-time define that reflects the actual deployed revision. At minimum, promote the string to a named constant and remove the stale TODO or file a tracked issue.

---

**A21-5** · MEDIUM · `languagedialog.h` — `showEvent` declares a non-standard default argument

**Description:** `languagedialog.h:29` declares:
```cpp
void showEvent(QShowEvent *event = 0);
```
The base class `QWidget::showEvent(QShowEvent *)` has no default argument. Providing a default argument on an override is both a style violation and potentially confusing: it implies `showEvent()` can be called with no argument, which is never done. The C++ standard permits this but most static analysers flag it as a defect.

**Fix:** Remove the `= 0` default from the override declaration:
```cpp
void showEvent(QShowEvent *event) override;
```
Add `override` while editing to make the override relationship explicit.

---

**A21-6** · MEDIUM · `languagedialog.h` — missing `#include <QTimer>` for member type

**Description:** `languagedialog.h:33` declares `QTimer *m_timer` but the header does not include `<QTimer>`. The code compiles only because `ui_languagedialog.h` or another transitively-included header happens to pull in `QTimer`. This is a fragile dependency on include order.

**Fix:** Add `#include <QTimer>` to `languagedialog.h` directly.

---

**A21-7** · LOW · `KeyFilter` constructor only initialises `m_leftKeyPressed`; three bool members left uninitialised

**Description:** `keyfilter.cpp:8–18` — the constructor initialiser list is:
```cpp
m_timer(new QTimer(this)),
m_leftKeyCount(0),
m_rightKeyCount(0),
m_upKeyCount(0),
m_downKeyCount(0),
m_leftKeyPressed(false)
```
The three members `m_rightKeyPressed`, `m_upKeyPressed`, and `m_downKeyPressed` (declared at `keyfilter.h:30–32`) are not listed. Because `KeyFilter` inherits from `QObject` (which does not zero-initialise its subclass members), these booleans have indeterminate values until the first call to `setPressState`. The `getPressState` function reads them before any initialisation if a key release event arrives before the first press of that key, producing undefined behaviour.

**Fix:** Add all three to the initialiser list:
```cpp
m_leftKeyPressed(false),
m_rightKeyPressed(false),
m_upKeyPressed(false),
m_downKeyPressed(false)
```

---

**A21-8** · LOW · Commented-out `qDebug` blocks left in production code

**Description:** `keyfilter.cpp` contains five commented-out debug lines:
- Line 129: `// qDebug() << "KeyFilter::Key_Left: State=" << state;`
- Line 132: `// qDebug() << "KeyFilter::Key_Up: State=" << state;` (mislabelled as `Key_Up` for the `Key_Right` branch)
- Line 135: `// qDebug() << "KeyFilter::Key_Up: State=" << state;`
- Line 138: `// qDebug() << "KeyFilter::Key_Down: State=" << state;`
- Line 141: `// qDebug() << "KeyFilter::others:" << key << " State=" << state;`

These add visual noise, and the mislabelled `Key_Up` comment on line 132 (inside the `Key_Right` branch) is actively misleading to anyone who re-enables debug logging.

**Fix:** Remove all commented-out debug lines. If conditional debug output is needed, use `qCDebug` with a named category controlled by `QLoggingCategory` so it can be enabled at runtime without code changes.

---

**A21-9** · LOW · Inconsistent naming convention — `InformationDialog` constructor uses `QWidget *parent = 0` instead of `nullptr`

**Description:** `informationdialog.h:21` declares:
```cpp
explicit InformationDialog(QWidget *parent = 0);
```
The rest of the codebase (`KeyFilter`, `LanguageDialog`) uses `nullptr`. Using `0` as a null pointer constant is legal C++ but deprecated style since C++11 and is flagged by `-Wzero-as-null-pointer-constant` on modern GCC/Clang.

**Fix:** Change to `QWidget *parent = nullptr` to be consistent with the other classes in this directory.

---

**A21-10** · LOW · `languagedialog.h` — `showEvent` default argument uses `0` instead of `nullptr`

**Description:** `languagedialog.h:29`:
```cpp
void showEvent(QShowEvent *event = 0);
```
This is the same style issue as A21-9 but compounded by the unnecessary default argument (see A21-5). Both problems should be resolved together.

**Fix:** Remove the default argument and use `nullptr` style if any default is ever warranted.

---

**A21-11** · LOW · `InformationDialog` parameter naming violates project convention — capitalised parameter names

**Description:** `setStatus` uses `bool Rly1, bool Rly2` (capitalised, abbreviated) and `QByteArray IO` (all caps) while the remainder of the codebase uses `lowerCamelCase` for parameters. This inconsistency makes the function signature stand out as having originated from a different style guide and increases the risk of future misreads.

**Fix:** Rename to `bool relay1, bool relay2, QByteArray ioState` (or equivalent lower-camel forms) in both header and implementation.

---

**A21-12** · LOW · `languagedialog.cpp` — file opened in `languageChanged()` but never closed on the success path

**Description:** `languagedialog.cpp:306–309`:
```cpp
QFile file("/sys/class/net/wlan0/address");
if (!file.open(QIODevice::ReadOnly)) {
    ui->lblMacAddress_2->setText(tr("na"));
}
```
The file is opened only to test whether the WiFi interface exists; on success the file is left open and the `QFile` destructor eventually closes it. This is not a resource leak per se (RAII closes it), but the intent is clearly only to check existence. Additionally, `setConfigParam()` (lines 164–169) correctly opens, reads, and closes the same file. This code in `languageChanged()` duplicates the existence check unnecessarily. If `languageChanged()` is called repeatedly (it is — on every `showEvent`), this opens and silently leaks the file descriptor for the lifetime of each `QFile` stack object.

**Fix:** Remove the duplicate file-open test from `languageChanged()`. The "na" fallback for the WiFi MAC address label is already handled adequately in `setConfigParam()`, which is called from both `showEvent()` and the periodic timer.

---

**A21-13** · INFO · `InformationDialog` stylesheet embedded as a string literal in constructor

**Description:** `informationdialog.cpp:20–36` defines a multi-line `QString styleSheet` directly in the constructor. While functional, embedding display styling in C++ source couples appearance to compiled code and makes it impossible to adjust the UI skin without recompiling.

**Fix:** Move the stylesheet to a Qt resource file (`.qss`) loaded at runtime via `QFile`, or define it in the `.ui` designer file where it can be reviewed visually.

---

**A21-14** · INFO · `KeyFilter` models per-key state as four parallel scalar fields rather than a map or array

**Description:** `keyfilter.h` declares eight separate member variables (`m_leftKeyCount`, `m_rightKeyCount`, `m_upKeyCount`, `m_downKeyCount`, `m_leftKeyPressed`, `m_rightKeyPressed`, `m_upKeyPressed`, `m_downKeyPressed`) and `keyfilter.cpp` replicates the same `if/else if` chain six times across `incrementKeyCount`, `getKeyCount`, `resetKeyCounter`, `getPressState`, and `setPressState`. This design violates DRY, contributed to the uninitialised-member bug (A21-7), and would require changes in eight places if a fifth key were added.

**Fix:** Replace the eight fields with `QMap<int, int> m_keyCounts` and `QMap<int, bool> m_keyPressed` (keyed by `Qt::Key`). The five helper methods collapse to two or three lines each, and initialisation is automatic.

---

## Summary Table

| ID | Severity | Category | File | Line(s) | Title |
|----|----------|----------|------|---------|-------|
| A21-1 | HIGH | Deprecated API / correctness | `ui/informationdialog.cpp` | 74 | `qChecksum` uses deprecated 2-arg overload with mismatched length |
| A21-2 | MEDIUM | Inconsistency | `ui/informationdialog.h` / `.cpp` | 25 / 111 | `setStatus` parameter name `mdemStat` vs `modemStat` |
| A21-3 | MEDIUM | Leaky abstraction | `ui/informationdialog.h` | 25 | `setStatus` has 12 positional parameters |
| A21-4 | MEDIUM | Dead / hardcoded data | `ui/informationdialog.cpp` | 42 | Hardcoded hardware revision with unresolved TODO |
| A21-5 | MEDIUM | Style / correctness | `ui/languagedialog.h` | 29 | `showEvent` override declares non-standard default argument |
| A21-6 | MEDIUM | Missing include | `ui/languagedialog.h` | 33 | `QTimer` used but not included in header |
| A21-7 | LOW | Uninitialised member | `ui/keyfilter.cpp` | 8–18 | Three `bool` press-state members not initialised in constructor |
| A21-8 | LOW | Commented-out code | `ui/keyfilter.cpp` | 129,132,135,138,141 | Five commented-out `qDebug` lines (one mislabelled) |
| A21-9 | LOW | Style | `ui/informationdialog.h` | 21 | `parent = 0` should be `parent = nullptr` |
| A21-10 | LOW | Style | `ui/languagedialog.h` | 29 | `event = 0` should use `nullptr` (see also A21-5) |
| A21-11 | LOW | Naming convention | `ui/informationdialog.h` / `.cpp` | 25 / 111 | Capitalised parameter names `Rly1`, `Rly2`, `IO` violate camelCase convention |
| A21-12 | LOW | Resource management | `ui/languagedialog.cpp` | 306–309 | File opened in `languageChanged()` only for existence check; duplicate of `setConfigParam()` logic |
| A21-13 | INFO | Maintainability | `ui/informationdialog.cpp` | 20–36 | Stylesheet embedded as string literal in constructor |
| A21-14 | INFO | Design / DRY | `ui/keyfilter.h` / `.cpp` | multiple | Eight parallel scalar fields instead of a keyed collection |
# Pass 4 Agent A22 — Code Quality

**Audit run:** 2026-02-28-01
**Branch:** master
**Files reviewed:**
- `ui/lockeddialog.h` + `ui/lockeddialog.cpp`
- `ui/messagedialog.h` + `ui/messagedialog.cpp`
- `ui/onScreenKeyboard.h` + `ui/onScreenKeyboard.cpp`

---

## Reading Evidence

### `ui/lockeddialog.h` + `ui/lockeddialog.cpp`

**Class:** `LockedDialog` (extends `QDialog`)

**Public methods (header line numbers):**

| Location | Signature |
|---|---|
| h:18 | `explicit LockedDialog(QWidget *parent = 0)` — constructor |
| h:19 | `~LockedDialog()` — destructor |
| h:20 | `void setLockedReason(CIGCONF::MaintLockedCode lockedCode)` |
| h:21 | `void languageChanged(void)` |
| h:22 | `void setTimeRemaining(quint32 secs)` |
| h:23 | `void clearTimerText()` |
| h:24 | `void stopTimer()` |
| h:25 | `void startTimer()` |

**Signals:**

| Location | Signature |
|---|---|
| h:32 | `void fullLockoutTimerEnded(bool on1, bool on2)` |
| h:33 | `void beeperOn()` |

**Protected methods:**

| Location | Signature |
|---|---|
| h:36 | `void mouseReleaseEvent(QMouseEvent *)` — inline, calls `accept()` |

**Private methods:**

| Location | Signature |
|---|---|
| h:40 | `void updateFullLock()` |
| h:41 | `void fullLockStart()` |

**Private members:**

- `Ui::LockedDialog *ui` — h:39
- `QTimer *m_fullLockTimer` — h:43
- `quint32 m_timeCntr` — h:44

**Conditional compilation:**
- `#ifdef UNIT_TEST` — h:27–29: `friend class TestDialog`

**Types used from external header (`app/cigconfigs.h`):**

`CIGCONF::MaintLockedCode` enum (defined at cigconfigs.h:142–148):

| Enumerator | Value |
|---|---|
| `MaintNormal` | `0x00` |
| `MaintIdle` | `0xea` |
| `MaintCriticalQuestion` | `0xfb` |
| `MaintRedImpact` | `0xfd` |
| `MaintSurveyTimeout` | `0xfe` |

**Implementation function line numbers (cpp):**

| Line | Function |
|---|---|
| 6 | `LockedDialog::LockedDialog(QWidget *parent)` |
| 16 | `LockedDialog::~LockedDialog()` |
| 21 | `void LockedDialog::startTimer()` |
| 30 | `void LockedDialog::stopTimer()` |
| 36 | `void LockedDialog::setLockedReason(CIGCONF::MaintLockedCode lockedCode)` |
| 61 | `void LockedDialog::languageChanged()` |
| 66 | `void LockedDialog::clearTimerText()` |
| 70 | `void LockedDialog::setTimeRemaining(quint32 secs)` |
| 77 | `void LockedDialog::fullLockStart()` |
| 84 | `void LockedDialog::updateFullLock()` |

---

### `ui/messagedialog.h` + `ui/messagedialog.cpp`

**Class:** `MessageDialog` (extends `QDialog`)

**Enum defined in class scope (h:18–27):**

`MessageType`:

| Enumerator | Implicit value |
|---|---|
| `NoMessage` | 0 |
| `ExpansionConnecting` | 1 |
| `WaitForAuthorised` | 2 |
| `NotAuthorised` | 3 |
| `OnDemandNotAuthorised` | 4 |
| `PowerOff` | 5 |
| `Reboot` | 6 |
| `VehicleOutOfService` | 7 |

**Public methods (header line numbers):**

| Location | Signature |
|---|---|
| h:29 | `explicit MessageDialog(QWidget *parent = 0)` — constructor |
| h:30 | `~MessageDialog()` — destructor |
| h:31 | `void openWithMessage(MessageType type)` — inline; calls `setMessageType(type); open()` |
| h:33 | `void setMessageType(MessageType type)` |
| h:34 | `MessageType messageType() const` — inline getter |

**Protected methods:**

| Location | Signature |
|---|---|
| h:37 | `void hideEvent(QHideEvent *)` |

**Private members:**

- `Ui::MessageDialog *ui` — h:40
- `QTimer *m_timer` — h:42
- `QMovie *m_movie` — h:43
- `MessageType m_messageType` — h:44

**Macro constants (cpp):**

| Name | Value | Location |
|---|---|---|
| `WAIT_AUTH_TIME` | `10000` | cpp:7 |
| `NOT_AUTH_TIME` | `5000` | cpp:8 |

**Implementation function line numbers (cpp):**

| Line | Function |
|---|---|
| 10 | `MessageDialog::MessageDialog(QWidget *parent)` |
| 30 | `MessageDialog::~MessageDialog()` |
| 35 | `void MessageDialog::hideEvent(QHideEvent *)` |
| 42 | `void MessageDialog::setMessageType(MessageType type)` |

---

### `ui/onScreenKeyboard.h` + `ui/onScreenKeyboard.cpp`

**Class:** `onScreenKeyboard` (extends `QWidget`) — note non-standard lower-camel class name

**Enums defined in class scope (h:17–19):**

`KeyToggleState`:

| Enumerator | Implicit value |
|---|---|
| `Normal` | 0 |
| `Upper` | 1 |
| `Lower` | 2 |

`CaseButton`:

| Enumerator | Implicit value |
|---|---|
| `AllButtons` | 0 |
| `CapsButton` | 1 |
| `ShiftButton` | 2 |
| `SymbolButton` | 3 |

`CtrlButton`:

| Enumerator | Implicit value |
|---|---|
| `None` | 0 |
| `Backspace` | 1 |
| `Delete` | 2 |

**Public members:**

- `QPushButton *enterButton` — h:22 (public raw pointer; never initialized in constructor; never referenced anywhere in the codebase)

**Public methods (header line numbers):**

| Location | Signature |
|---|---|
| h:20 | `explicit onScreenKeyboard(QWidget *parent = 0)` — constructor |
| h:21 | `~onScreenKeyboard()` — destructor |
| h:24 | `void setInitialText(QString str)` |
| h:25 | `void languageChanged(void)` |

**Private slots:**

| Location | Signature |
|---|---|
| h:28 | `void keyboardHandler()` |
| h:29 | `void on_btnShift_clicked(bool checked)` |
| h:30 | `void on_btnEnter_clicked()` |
| h:31 | `void on_btnBack_clicked()` |
| h:32 | `void on_btnCaps_toggled(bool checked)` |
| h:33 | `void on_btnHideKeyboard_clicked()` |
| h:34 | `void on_btnDelete_clicked()` |

**Signals:**

| Location | Signature |
|---|---|
| h:36 | `void updateText(QString str, CtrlButton ctrl)` |
| h:37 | `void onScreenKeyboardClose()` |

**Protected methods:**

| Location | Signature |
|---|---|
| h:40 | `void closeEvent(QCloseEvent *event)` |

**Private methods:**

| Location | Signature |
|---|---|
| h:43 | `void toggle()` |
| h:44 | `QString dualCharCase(QString ch, int toggleState)` |
| h:45 | `QString singleCharCase(QString ch, int toggleState)` |
| h:46 | `void setCaseButton(CaseButton btn, bool set)` |

**Private members:**

- `Ui::onScreenKeyboard *ui` — h:47
- `QString outputText` — h:48
- `QString m_capsStylesheet` — h:49
- `QString m_symbolStylesheet` — h:50
- `QString m_shiftStylesheet` — h:51

**Implementation function line numbers (cpp):**

| Line | Function |
|---|---|
| 5 | `onScreenKeyboard::onScreenKeyboard(QWidget *parent)` |
| 56 | `void onScreenKeyboard::setInitialText(QString str)` |
| 61 | `void onScreenKeyboard::keyboardHandler()` |
| 102 | `onScreenKeyboard::~onScreenKeyboard()` |
| 107 | `void onScreenKeyboard::closeEvent(QCloseEvent *event)` |
| 113 | `void onScreenKeyboard::on_btnShift_clicked(bool checked)` |
| 119 | `QString onScreenKeyboard::singleCharCase(QString ch, int toggleState)` |
| 127 | `QString onScreenKeyboard::dualCharCase(QString ch, int toggleState)` |
| 145 | `void onScreenKeyboard::toggle()` |
| 184 | `void onScreenKeyboard::on_btnEnter_clicked()` |
| 192 | `void onScreenKeyboard::on_btnBack_clicked()` |
| 197 | `void onScreenKeyboard::on_btnCaps_toggled(bool checked)` |
| 202 | `void onScreenKeyboard::on_btnHideKeyboard_clicked()` |
| 209 | `void onScreenKeyboard::setCaseButton(CaseButton btn, bool set)` |
| 243 | `void onScreenKeyboard::on_btnDelete_clicked()` |
| 248 | `void onScreenKeyboard::languageChanged()` |

---

## Findings

---

**A22-1** · HIGH · `onScreenKeyboard` class name violates Qt/C++ naming convention

**Description:** The class is named `onScreenKeyboard` with a lowercase leading letter, which violates the established Qt and C++ convention of PascalCase for class names (e.g., `OnScreenKeyboard`). This is not merely stylistic: the Qt `Q_OBJECT` macro, `moc` toolchain, and IDE tooling all assume PascalCase class names, and the inconsistency creates confusion throughout the codebase. The companion `Ui::onScreenKeyboard` namespace alias and the `.ui` file name also inherit the non-standard casing, making the inconsistency pervasive. Every other class in the codebase (`LockedDialog`, `MessageDialog`, `CommentDialog`, etc.) uses PascalCase.

**Fix:** Rename the class to `OnScreenKeyboard`, update the `.h`, `.cpp`, `.ui`, and all callers accordingly. This is a straightforward mechanical rename; no behavioral changes are required.

---

**A22-2** · HIGH · `enterButton` — uninitialized public raw pointer (undefined behavior on any dereference)

**Description:** `QPushButton *enterButton` is declared as a public data member of `onScreenKeyboard` (h:22) but is never assigned in the constructor or anywhere else in the class implementation. The UI form names the enter button `btnEnter`, accessed internally via `ui->btnEnter`. A grep across the entire source tree shows that no caller ever assigns or dereferences `enterButton`. The pointer therefore holds an indeterminate (garbage) value for the entire lifetime of any `onScreenKeyboard` instance. Any future caller who attempts to use `enterButton` (e.g., to connect a signal) will trigger undefined behavior resulting in a crash or silent data corruption.

**Fix:** Either (a) remove `enterButton` entirely if it is not needed, or (b) assign it in the constructor body: `enterButton = ui->btnEnter;` and document the intended use. If the purpose is to allow callers to connect to the enter button's signals, add a public accessor method `QPushButton* enterButtonWidget() const { return ui->btnEnter; }` and keep the member private.

---

**A22-3** · HIGH · Backslash key emits the text of `Buttonr` instead of a backslash character

**Description:** In `keyboardHandler()` (cpp:75–77), when the pressed button's text is `"\\"`, the handler sets:
```cpp
outputText = ui->Buttonr->text();
```
This emits whatever letter is currently displayed on the `r` key (either `"r"` or `"R"` depending on shift/caps state) instead of a backslash character `"\"`. This is a logic error: the backslash key will never produce a backslash in user input. The likely cause is an erroneous copy-paste from nearby code during development. The `"&&"` special case immediately above it (cpp:72–74) correctly sets `outputText = "&"`, demonstrating the intended pattern was `outputText = "\\"`.

**Fix:** Replace `outputText = ui->Buttonr->text();` with `outputText = "\\";` so that the backslash key emits a backslash character.

---

**A22-4** · MEDIUM · `dualCharCase()` is dead code — defined but never called

**Description:** `QString onScreenKeyboard::dualCharCase(QString ch, int toggleState)` is declared in the header (h:44) and fully implemented in the cpp (cpp:127–143). It contains 10 explicit branches handling the number-row dual-label keys (e.g., `"!\n0"`, `"@\n1"`, etc.). A search of the entire codebase shows it is never invoked. The `toggle()` function only calls `singleCharCase()` for alphabetic keys, and `keyboardHandler()` processes multi-character keys inline without using this helper. The function is therefore completely unreachable dead code.

**Fix:** Remove `dualCharCase()` from both the header and implementation. If the intent was to factor the multi-character key logic out of `keyboardHandler()`, refactor accordingly and connect the call sites.

---

**A22-5** · MEDIUM · `MaintLockedCode` uses arbitrary magic hex values with no documentation

**Description:** The `MaintLockedCode` enum (cigconfigs.h:142–148) assigns non-contiguous magic hexadecimal values to its enumerators (`MaintIdle = 0xea`, `MaintCriticalQuestion = 0xfb`, `MaintRedImpact = 0xfd`, `MaintSurveyTimeout = 0xfe`). These values are used as a `switch` discriminant in `LockedDialog::setLockedReason()` (cpp:38–58) and presumably as wire-protocol or storage codes elsewhere. There is no comment explaining the origin or significance of these values, making it impossible to verify correctness, add new codes safely, or catch encoding mismatches. `MaintNormal = 0x00` is also defined but never handled in the `switch` — it falls through to the `default` case.

**Fix:** Add a comment above the enum explaining the source and semantics of the assigned values (e.g., "values match the protocol byte defined in firmware spec section X"). If `MaintNormal` is a valid expected state, add an explicit `case CIGCONF::MaintNormal:` branch to `setLockedReason()`.

---

**A22-6** · MEDIUM · `SymbolButton` enumerator declared but never used

**Description:** The `CaseButton` enum in `onScreenKeyboard` (h:18) declares four values: `AllButtons`, `CapsButton`, `ShiftButton`, and `SymbolButton`. The `setCaseButton()` implementation (cpp:209–241) handles `CapsButton` and `ShiftButton` explicitly, and `AllButtons` via the `default` branch. `SymbolButton` has no corresponding `case` in the `switch` and is never passed to `setCaseButton()` anywhere in the codebase — it is an entirely dead enumerator that suggests an unimplemented feature was planned but never completed.

**Fix:** Either implement the `SymbolButton` case in `setCaseButton()` and wire up the UI symbol-toggle button, or remove the `SymbolButton` enumerator and any corresponding unused UI elements.

---

**A22-7** · MEDIUM · `PowerOff` movie file path missing `.gif` extension

**Description:** In `MessageDialog::setMessageType()` (cpp:113), the `PowerOff` case sets:
```cpp
m_movie->setFileName(":/image/icons/movie/wait-power-off");
```
Every other case that uses a `QMovie` appends `.gif` to the resource path (e.g., `":/image/icons/movie/wait-ble.gif"`, `":/image/icons/movie/wait-until-restart.gif"`). The missing extension means `QMovie` will fail to load the resource because Qt's resource system uses the exact path as specified, and the file registered in the `.qrc` almost certainly ends in `.gif`. The `PowerOff` dialog will silently display no animation.

**Fix:** Change the path to `":/image/icons/movie/wait-power-off.gif"` (verify the actual resource file name in the `.qrc` manifest and align accordingly).

---

**A22-8** · LOW · Non-standard class naming propagates into `Ui` namespace and `.ui` file

**Description:** Because the class is named `onScreenKeyboard` rather than `OnScreenKeyboard`, the Qt Designer-generated `Ui::onScreenKeyboard` namespace and the `ui_onScreenKeyboard.h` generated file inherit the non-standard casing. This makes it harder for static analysis tools and IDEs to distinguish class names from variable names, and violates the expectation that `Ui::` namespace members match PascalCase class names. (Related to A22-1 but separately observable as a build-artefact quality issue.)

**Fix:** Address as part of the A22-1 rename.

---

**A22-9** · LOW · `LockedDialog` internal timer `m_fullLockTimer` and counter `m_timeCntr` have no encapsulation boundary against misuse via `startTimer()`/`stopTimer()` public API

**Description:** `startTimer()` and `stopTimer()` are public methods (h:24–25) that directly manipulate `m_fullLockTimer`. There is no guard preventing a caller from calling `startTimer()` multiple times, which the implementation partially handles with `!m_fullLockTimer->isActive()` (cpp:26), but `stopTimer()` calls `clearTimerText()` as a side effect (cpp:32–33) which alters UI state. Callers have no way to query whether the timer is active without checking timer internals indirectly. The timer is an implementation detail that leaks into the public API.

**Fix:** Document the preconditions and side effects of `startTimer()` and `stopTimer()` in the header, or refactor the timer management into a single `setTimerActive(bool)` method with clear semantics and no hidden UI side effects.

---

**A22-10** · LOW · `updateFullLock()` post-decrement on `quint32` produces unsigned underflow on final tick

**Description:** The shutdown logic in `updateFullLock()` (cpp:87) uses:
```cpp
if (!m_timeCntr--)
```
This post-decrements `m_timeCntr` after the zero-check. When `m_timeCntr` reaches zero, the condition fires and `stopTimer()` is called — correct. However, because `quint32` is unsigned, the post-decrement on the iteration where `m_timeCntr == 0` wraps `m_timeCntr` to `0xFFFFFFFF` before `stopTimer()` is reached. If `stopTimer()` were ever not called (e.g., due to a future code change), the counter would wrap to a very large value. The comment on cpp:86 ("This will immediately close both relays if Timeout Parameter is zero") also describes a separate edge case: if `fullLockoutTimeout()` returns 0, the first tick immediately fires `fullLockoutTimerEnded`, which is the intended behavior, but the comment does not explain the wrap risk.

**Fix:** Use an explicit comparison: `if (m_timeCntr == 0) { ... } else { m_timeCntr--; setTimeRemaining(m_timeCntr); }` to avoid unsigned wrap and make the zero-timeout edge case explicit.

---

**A22-11** · LOW · `WAIT_AUTH_TIME` and `NOT_AUTH_TIME` are file-scope `#define` macros rather than typed constants

**Description:** `messagedialog.cpp` (cpp:7–8) defines:
```cpp
#define WAIT_AUTH_TIME  10000
#define NOT_AUTH_TIME   5000
```
These are untyped preprocessor macros with no scope, no type safety, and no visibility from the header. They are integer literals (milliseconds) with no documenting comment. Any future inclusion of this translation unit's internal constants in a unit test or via copy-paste will silently use the wrong type (e.g., 32-bit int rather than the `int` expected by `QTimer::start()`).

**Fix:** Replace with `static constexpr int kWaitAuthTimeMs = 10000;` and `static constexpr int kNotAuthTimeMs = 5000;` as private static members of `MessageDialog`, or at minimum as `constexpr` file-scope variables with a `// ms` comment.

---

**A22-12** · LOW · `keyboardHandler()` uses a C-style cast instead of `qobject_cast`

**Description:** `keyboardHandler()` (cpp:63) casts `sender()` using a C-style cast:
```cpp
QPushButton *button = (QPushButton *)sender();
```
All buttons connected to this slot are `QPushButton` instances, so the cast is safe in practice. However, C-style casts bypass Qt's object model and will silently return a corrupt pointer if the slot is ever accidentally connected to a non-`QPushButton` signal source. The Qt-correct pattern is `qobject_cast<QPushButton *>(sender())` which returns `nullptr` on type mismatch and allows a null check.

**Fix:** Replace with:
```cpp
QPushButton *button = qobject_cast<QPushButton *>(sender());
if (!button) return;
```

---

**A22-13** · INFO · `m_symbolStylesheet` member is declared but never read or written in a meaningful way

**Description:** `m_symbolStylesheet` (h:50) is declared as a private `QString` member of `onScreenKeyboard`. It is never assigned and never read anywhere in the implementation. The `SymbolButton` case of `setCaseButton()` is also absent (see A22-6), confirming this field was part of an unimplemented symbol-mode feature. The field adds dead state to every instance.

**Fix:** Remove `m_symbolStylesheet` along with `SymbolButton` as part of the A22-6 cleanup, or implement the symbol mode fully.

---

**A22-14** · INFO · `onScreenKeyboard` constructor has a blank line inside the initializer block (cpp:21–22)

**Description:** Lines 21–22 of `onScreenKeyboard.cpp` contain a blank line in the middle of the `connect()` call sequence inside the constructor body. While harmless, it inconsistently separates the `p` key connection from the rest of the top row (lines 11–20), which may mislead a reader into thinking the blank line has significance. The rest of the constructor groups rows with single blank lines between rows, which is the correct intent.

**Fix:** Remove the extra blank line between the `Buttonp` connection (line 20) and the start of the home-row connections (line 23), or keep one blank line consistently between keyboard rows.

---

## Summary Table

| ID | Severity | Title |
|---|---|---|
| A22-1 | HIGH | `onScreenKeyboard` class name violates Qt/C++ PascalCase convention |
| A22-2 | HIGH | `enterButton` — uninitialized public raw pointer (UB on any dereference) |
| A22-3 | HIGH | Backslash key emits `Buttonr` text instead of `"\\"` — logic error |
| A22-4 | MEDIUM | `dualCharCase()` defined but never called — dead code |
| A22-5 | MEDIUM | `MaintLockedCode` uses undocumented magic hex values |
| A22-6 | MEDIUM | `SymbolButton` enumerator declared but never implemented or used |
| A22-7 | MEDIUM | `PowerOff` movie resource path missing `.gif` extension |
| A22-8 | LOW | Non-standard class casing propagates into `Ui` namespace and generated files |
| A22-9 | LOW | Public `startTimer()`/`stopTimer()` API leaks timer implementation details |
| A22-10 | LOW | `quint32` post-decrement in `updateFullLock()` wraps to `0xFFFFFFFF` on zero tick |
| A22-11 | LOW | `WAIT_AUTH_TIME` / `NOT_AUTH_TIME` are untyped `#define` macros |
| A22-12 | LOW | C-style cast in `keyboardHandler()` should be `qobject_cast` |
| A22-13 | INFO | `m_symbolStylesheet` member is dead state — never assigned or read |
| A22-14 | INFO | Spurious blank line in `onScreenKeyboard` constructor body |

**Totals:** 3 HIGH, 4 MEDIUM, 5 LOW, 2 INFO
# Pass 4 Agent A23 — Code Quality

**Audit run:** 2026-02-28-01
**Branch:** master
**Repo root:** C:/Projects/cig-audit/repos/mark3-pvd
**Assigned files:**
- `ui/ondemanddialog.h` + `ui/ondemanddialog.cpp`
- `ui/optionalcheckconfirmationdialog.h` + `ui/optionalcheckconfirmationdialog.cpp`
- `ui/pindialog.h` + `ui/pindialog.cpp`

---

## Reading Evidence

### `ui/ondemanddialog.h`

**Class:** `OnDemandDialog` (extends `QDialog`)

**Methods / line numbers:**

| Line | Signature | Notes |
|------|-----------|-------|
| 20 | `explicit OnDemandDialog(QWidget *parent = 0)` | Constructor |
| 21 | `~OnDemandDialog()` | Destructor |
| 23 | `void setSuperMasterId(quint64 id)` | Inline setter |
| 24 | `void reset()` | Public reset |
| 25 | `void setTimeRemaining(quint32 secs)` | Public updater |
| 26 | `QString showCustomTimeFormat(quint32 time)` | Public utility |
| 29 | `void onDemandStarted(quint32, quint32, quint64, CIGCONF::OnDemandCmdSrc)` | Signal |
| 30 | `void onDemandExtended(quint32, quint32, quint64, CIGCONF::OnDemandCmdSrc)` | Signal |
| 31 | `void onDemandEnded(quint32, quint64, CIGCONF::OnDemandCmdSrc)` | Signal |
| 34 | `void showEvent(QShowEvent *event = 0)` | Protected override |
| 36 | `void onStart()` | Protected slot |
| 37 | `void onExtend()` | Protected slot |
| 38 | `void onEnd()` | Protected slot |
| 41 | `bool debounce()` | Private helper |

**Members:**

| Line | Name | Type |
|------|------|------|
| 42 | `ui` | `Ui::OnDemandDialog *` |
| 44 | `m_timer` | `QTimer *` |
| 45 | `m_lastPress` | `quint32` |
| 46 | `m_smId` | `quint64` |

**Types / constants defined:** None directly; uses `CIGCONF::OnDemandCmdSrc` from `app/cigconfigs.h`.

---

### `ui/ondemanddialog.cpp`

**Methods / line numbers:**

| Line | Signature |
|------|-----------|
| 9 | `OnDemandDialog::OnDemandDialog(QWidget *parent)` |
| 26 | `OnDemandDialog::~OnDemandDialog()` |
| 31 | `void OnDemandDialog::showEvent(QShowEvent *event)` |
| 57 | `void OnDemandDialog::onStart()` |
| 74 | `void OnDemandDialog::onExtend()` |
| 91 | `void OnDemandDialog::onEnd()` |
| 106 | `bool OnDemandDialog::debounce()` |
| 117 | `void OnDemandDialog::reset()` |
| 123 | `QString OnDemandDialog::showCustomTimeFormat(quint32 time)` |
| 131 | `void OnDemandDialog::setTimeRemaining(quint32 secs)` |

**Constants defined:**

| Line | Name | Value |
|------|------|-------|
| 7 | `NO_ACTIVITY_TIME` | `10000` (ms) |

---

### `ui/optionalcheckconfirmationdialog.h`

**Class:** `OptionalCheckConfirmationDialog` (extends `QDialog`)

**Methods / line numbers:**

| Line | Signature | Notes |
|------|-----------|-------|
| 15 | `explicit OptionalCheckConfirmationDialog(QWidget *parent = 0)` | Constructor |
| 16 | `~OptionalCheckConfirmationDialog()` | Destructor |
| 17 | `void onRefreshLanguage(void)` | Public language refresh |
| 24 | `void hideEvent(QHideEvent *)` | Protected override |
| 25 | `void showEvent(QShowEvent *event = 0)` | Protected override |

**Members:**

| Line | Name | Type |
|------|------|------|
| 20 | `ui` | `Ui::OptionalCheckConfirmationDialog *` |
| 21 | `m_timer` | `QTimer *` |

**Types / constants defined:** None.

---

### `ui/optionalcheckconfirmationdialog.cpp`

**Methods / line numbers:**

| Line | Signature |
|------|-----------|
| 6 | `OptionalCheckConfirmationDialog::OptionalCheckConfirmationDialog(QWidget *parent)` |
| 19 | `void OptionalCheckConfirmationDialog::showEvent(QShowEvent *event)` |
| 31 | `void OptionalCheckConfirmationDialog::hideEvent(QHideEvent *)` |
| 36 | `OptionalCheckConfirmationDialog::~OptionalCheckConfirmationDialog()` |
| 41 | `void OptionalCheckConfirmationDialog::onRefreshLanguage(void)` |

**Constants / magic numbers:**

| Line | Value | Meaning |
|------|-------|---------|
| 28 | `5000` | Dialog auto-dismiss timeout (ms), bare literal in `m_timer->start(5000)` |

---

### `ui/pindialog.h`

**Class:** `PinDialog` (extends `QDialog`)

**Methods / line numbers:**

| Line | Signature | Notes |
|------|-----------|-------|
| 17 | `explicit PinDialog(QWidget *parent = 0)` | Constructor |
| 18 | `~PinDialog()` | Destructor |
| 20 | `quint32 pinCode() const` | Public — returns raw PIN digits as integer |
| 21 | `void clearPinCode()` | Public |
| 22 | `void languageChanged()` | Public |
| 25 | `void showEvent(QShowEvent *)` | Protected override |
| 26 | `void hideEvent(QHideEvent *)` | Protected override |
| 29 | `void keyPressed()` | Private slot |

**Members:**

| Line | Name | Type |
|------|------|------|
| 31 | `ui` | `Ui::PinDialog *` |
| 32 | `m_timer` | `QTimer *` |

**Types / constants defined:** None in header.

---

### `ui/pindialog.cpp`

**Methods / line numbers:**

| Line | Signature |
|------|-----------|
| 12 | `PinDialog::PinDialog(QWidget *parent)` |
| 42 | `PinDialog::~PinDialog()` |
| 47 | `void PinDialog::keyPressed()` |
| 87 | `void PinDialog::hideEvent(QHideEvent *)` |
| 92 | `void PinDialog::showEvent(QShowEvent *)` |
| 97 | `quint32 PinDialog::pinCode() const` |
| 112 | `void PinDialog::clearPinCode()` |
| 118 | `void PinDialog::languageChanged()` |

**Constants defined:**

| Line | Name | Value |
|------|------|-------|
| 9 | `PIN_MAX_LENGTH` | `5` |
| 10 | `ACTIVITY_TIME` | `30000` (ms) |

---

## Findings

---

**A23-1** · MEDIUM · `onEnd()` updates `m_lastPress` redundantly after `debounce()` already did so

**Description:** In `ondemanddialog.cpp`, the `debounce()` helper (line 106–115) already assigns `m_lastPress = now` before returning `true`. However, `onEnd()` (line 103) then assigns `m_lastPress = gCfg->clockTime()` a second time unconditionally, after the timer restart. This redundant write is absent in `onStart()` (line 57–72) and `onExtend()` (line 74–89), making the three handlers inconsistent. The double-write is harmless in isolation but indicates a copy-paste omission during `onEnd()` authoring and could confuse future maintainers about the debounce contract.

**Fix:** Remove the redundant `m_lastPress = gCfg->clockTime();` assignment at `ondemanddialog.cpp:103`. The debounce pattern for all three action handlers should be identical: call `debounce()`, act on button state, restart `m_timer`.

---

**A23-2** · MEDIUM · `onStart()` and `onExtend()` omit the post-action `m_lastPress` update, while `onEnd()` has it — asymmetric debounce state

**Description:** As a direct consequence of A23-1, `onStart()` and `onExtend()` do not explicitly refresh `m_lastPress` after completing their action, whereas `onEnd()` does. Because `debounce()` already updates `m_lastPress`, the behaviour is identical in practice for all three handlers. The asymmetry creates a false implication that `onEnd()` requires special cooldown handling that `onStart()`/`onExtend()` do not, which is misleading to anyone reading the code.

**Fix:** Adopt a single, consistent style: either rely entirely on `debounce()` to maintain `m_lastPress` (recommended — remove the stray line in `onEnd()`) or have all three handlers refresh it explicitly after the action block. The former matches the pattern used by `AuthorisedDialog`, `SupervisorDialog`, and `CommentDialog` in the same codebase.

---

**A23-3** · MEDIUM · `reset()` calls `showEvent()` directly, bypassing the Qt event system

**Description:** `ondemanddialog.cpp:120` calls `showEvent()` directly as a regular C++ function call rather than allowing Qt to emit the event naturally. `showEvent()` is documented in Qt as a virtual event handler that Qt dispatches; calling it directly couples `reset()` to the current implementation of `showEvent()` and will silently bypass any base-class behaviour in `QDialog::showEvent()`. While the immediate `showEvent()` body does not call `QDialog::showEvent(event)` itself (and so passes `nullptr`/`0` for the default-argument `event = 0`), the pattern is fragile: if `showEvent()` is ever updated to call `event->accept()` or similar, the null pointer will cause undefined behaviour.

**Fix:** Replace the direct call with the intended side-effects: extract the state-reset logic in `showEvent()` into a private `refreshUi()` helper and call that helper from both `showEvent()` and `reset()`. This is the pattern used elsewhere (e.g., `languageChanged()` / `onRefreshLanguage()`).

---

**A23-4** · MEDIUM · `onStart()` and `onExtend()` action handlers are `protected`, not `private`

**Description:** `ondemanddialog.h` (lines 36–38) declares `onStart()`, `onExtend()`, and `onEnd()` in the `protected` section. These three methods are pure internal slot handlers connected to button clicks in the constructor; they are not intended to be overridden or called by subclasses. Across the rest of the UI layer, comparable button-click slots (`rstLogout`, `onLogoutRequest` in `AuthorisedDialog`; language selection slots in `LanguageDialog`; confirm-action slots in `SupervisorDialog`) are uniformly placed in `private` or `private slots`. Declaring them `protected` widens the interface unnecessarily and exposes authentication-sensitive actions (start/extend/end an on-demand session) to subclass override.

**Fix:** Move `onStart()`, `onExtend()`, and `onEnd()` into the `private` section (or a `private slots:` subsection) of `OnDemandDialog`. No callers outside the class exist.

---

**A23-5** · MEDIUM · `PIN_MAX_LENGTH` defined in `.cpp` is not used; actual limit comes from the UI designer's `maxLength` property

**Description:** `pindialog.cpp:9` defines `#define PIN_MAX_LENGTH 5`, but `keyPressed()` (line 64) reads the PIN length limit from `ui->lineEdit->maxLength()` — a value set in the Qt Designer `.ui` file — and stores it in a local variable `maxLength`. The `PIN_MAX_LENGTH` macro is never referenced anywhere in `pindialog.cpp` or anywhere else in the codebase. This means the true maximum PIN length is controlled by a property embedded in a binary `.ui` resource, invisible in code review and not enforced by the named constant. If a developer changes `PIN_MAX_LENGTH` expecting the dialog to enforce a different length, nothing changes at runtime.

**Fix:** Either (a) remove `#define PIN_MAX_LENGTH 5` entirely and document in a comment that `ui->lineEdit->maxLength()` is the authoritative source set in the `.ui` designer file, or (b) enforce `PIN_MAX_LENGTH` at runtime by calling `ui->lineEdit->setMaxLength(PIN_MAX_LENGTH)` in the constructor and removing the reliance on the designer property for this security-relevant limit. Option (b) is strongly preferred because it makes the PIN length constraint visible and auditable in code.

---

**A23-6** · LOW · `static` local variable used for debounce in `PinDialog::keyPressed()` instead of a member variable

**Description:** `pindialog.cpp:51` uses `static quint64 last = 0;` for debouncing key presses. Using function-level `static` variables means the debounce state is shared across all instances of `PinDialog` (if more than one were ever created) and is never reset when a `PinDialog` instance is destroyed and recreated. Every other dialog in the codebase that implements debouncing (`OnDemandDialog`, `AuthorisedDialog`, `SupervisorDialog`, `CommentDialog`, `LanguageDialog`) uses an instance-level member variable `m_lastPress`. The inconsistency also means the debounce state persists across separate invocations of the same `PinDialog` instance, potentially causing the very first key press of a new session to be silently dropped if the dialog is shown shortly after the previous dismissal.

**Fix:** Replace the `static` local with a member variable `quint64 m_lastPress` (consistent with the rest of the codebase), initialise it to `0` in the constructor, and reset it in `clearPinCode()` or `showEvent()`. Change the type from `quint64` to `quint32` for consistency with `m_lastPress` elsewhere, or confirm that `clockTime()` returns a value requiring 64-bit range.

---

**A23-7** · LOW · `showCustomTimeFormat()` is public but is only a display-formatting helper

**Description:** `ondemanddialog.h:26` declares `showCustomTimeFormat(quint32 time)` as `public`. The method is a pure formatting utility that converts a second-count to `HH:MM:SS` string. It is only called from within `OnDemandDialog::setTimeRemaining()` (cpp:136) and from `Dialog::showCustomTimeFormat()` (a separately defined duplicate in `dialog.cpp:1249`). Making it `public` unnecessarily enlarges the class API surface and duplicates a utility that already exists in `Dialog`. The name itself is also misleading: the verb "show" implies a side-effecting display operation, whereas the method is a pure computation returning a `QString`.

**Fix:** Change the visibility to `private` (it has no external callers on `OnDemandDialog` objects). Rename to `formatDuration()` or `secondsToTimeString()` to accurately reflect its pure-function nature. Consider whether the duplicate in `Dialog` should be unified into a shared static helper.

---

**A23-8** · LOW · `onRefreshLanguage()` in `OptionalCheckConfirmationDialog` duplicates `showEvent()` body verbatim

**Description:** `optionalcheckconfirmationdialog.cpp:41–48` (`onRefreshLanguage()`) is a character-for-character copy of the UI text-setting block in `showEvent()` (lines 22–28). Any future change to the dialog's display strings must be made in two places. The `showEvent()` body does not call `onRefreshLanguage()`, so the two copies can drift. This is a classic DRY violation. The corresponding pattern in other dialogs (e.g., `LockedDialog::languageChanged()`, `PinDialog::languageChanged()`) correctly calls into a single update method.

**Fix:** In `showEvent()`, replace the text-setting block with a call to `onRefreshLanguage()`, leaving only `m_timer->start(5000)` as the additional line in `showEvent()`. This ensures a single source of truth for the display strings.

---

**A23-9** · LOW · Magic number `5000` in `OptionalCheckConfirmationDialog::showEvent()`

**Description:** `optionalcheckconfirmationdialog.cpp:28` calls `m_timer->start(5000)` with an unexplained bare integer. The inline comment (`// wait 5 second before closing the dialog`) partially explains the intent, but the value is not given a named constant. Every other dialog in the same directory that uses a similar auto-dismiss timer defines a named macro (`NO_ACTIVITY_TIME`, `ACTIVITY_TIME`, `RESET_TIMEOUT`, `WAIT_AUTH_TIME`). The magic number is inconsistent with established style and makes future adjustment of the timeout harder to locate.

**Fix:** Add `#define ACTIVITY_TIME 5000` (or an appropriately named constant) at the top of the `.cpp` file and replace the literal with the constant, consistent with the style of `ondemanddialog.cpp`, `pindialog.cpp`, and `supervisordialog.cpp`.

---

**A23-10** · LOW · Unused `#include <QDebug>` in `optionalcheckconfirmationdialog.cpp`

**Description:** `optionalcheckconfirmationdialog.cpp:4` includes `<QDebug>`, but no `qDebug()` call or `QDebug` usage appears anywhere in the file. This is a leftover from a development or debugging session. Unnecessary includes slow incremental builds and signal to auditors and maintainers that debug instrumentation may have been removed without cleanup.

**Fix:** Remove `#include <QDebug>` from `optionalcheckconfirmationdialog.cpp`.

---

**A23-11** · LOW · Unused `#include <QThread>` in `pindialog.cpp`

**Description:** `pindialog.cpp:6` includes `<QThread>`, but no `QThread` symbol is used anywhere in the file. Like the `QDebug` issue above, this is dead include residue, likely left over from an earlier implementation attempt. The comment at line 49–51 mentions an application-wide event filter was considered ("Tried application wide event filter") — the `QThread` include may be a remnant of that approach.

**Fix:** Remove `#include <QThread>` from `pindialog.cpp`.

---

**A23-12** · LOW · Unused `#include <QDebug>` in `pindialog.cpp`

**Description:** `pindialog.cpp:4` includes `<QDebug>`, but no `qDebug()` or `QDebug` reference exists anywhere in the file.

**Fix:** Remove `#include <QDebug>` from `pindialog.cpp`.

---

**A23-13** · LOW · `showCustomTimeFormat()` uses signed `qint32` for hour/minute/second decomposition of `quint32` input

**Description:** `ondemanddialog.cpp:124–126` declares `h`, `m`, and `s` as `qint32` while computing from a `quint32` input. For very large values of `time` (near `UINT32_MAX`, approximately 4.29 billion seconds / ~136 years), the division `time/3600` yields a value of up to ~1,193,046 — well within `qint32` range — so no actual overflow occurs in practice. However, the intermediate computation `time - (3600*h)` on line 125 passes a `qint32` value (`h`) back into arithmetic with `quint32` (`time`), which involves an implicit signed/unsigned conversion. Additionally, `3600*h` with a `qint32` `h` is evaluated as signed multiplication where `3600 * 1193046` = ~4.295 billion, which overflows `qint32` (max ~2.147 billion). This causes undefined behaviour for the intermediate expression when `time` is near `UINT32_MAX`. While such values are operationally implausible for a remaining-session timer, the type mismatch is a latent code quality defect.

**Fix:** Declare `h`, `m`, and `s` as `quint32` to match the input type and eliminate implicit signed/unsigned conversion warnings:
```cpp
quint32 h = time / 3600;
quint32 m = (time - (3600 * h)) / 60;
quint32 s = time - (3600 * h) - (m * 60);
```

---

**A23-14** · INFO · `QApplication::processEvents()` call in `PinDialog::keyPressed()` is a code smell

**Description:** `pindialog.cpp:82` calls `QApplication::processEvents()` before `accept()` when the PIN reaches maximum length. The comment (lines 75–78) explains that this is needed to repaint the asterisk mask label before the dialog closes. Calling `processEvents()` from within a slot is generally considered a code smell in Qt: it can cause re-entrant event delivery, unexpected signal emission, and unpredictable widget state during the interim event processing. The correct Qt idiom is to use a zero-delay `QTimer::singleShot(0, this, &PinDialog::accept)` instead, which defers `accept()` to the next event loop iteration after the current event processing completes, ensuring the repaint happens naturally.

**Fix:** Replace:
```cpp
QApplication::processEvents();
accept();
```
with:
```cpp
QTimer::singleShot(0, this, &PinDialog::accept);
```
This allows Qt to process the pending repaint event before triggering the dialog close, without the risks of synchronous re-entrant event dispatch.

---

**A23-15** · INFO · `showEvent(QShowEvent *event = 0)` default-argument pattern inconsistent with newer Qt style

**Description:** `ondemanddialog.h:34` and `optionalcheckconfirmationdialog.h:25` declare `showEvent` with a default argument `= 0`. This is an older Qt4-era style. Other dialogs in the same directory (`pindialog.h:25`, `authoriseddialog.h:33`) correctly declare `showEvent(QShowEvent *)` without a default argument, matching the base class signature. The default-argument form is not wrong — Qt will dispatch the event correctly — but it is inconsistent and can mislead readers into thinking the function can legitimately be called with no argument (which is what `reset()` in `ondemanddialog.cpp:120` exploits, passing a null pointer to `event`). This connects back to A23-3.

**Fix:** Remove the `= 0` default argument from all `showEvent` and `hideEvent` declarations in the assigned files to match the Qt base-class signature and codebase majority style.

---

## Summary Table

| ID | Severity | File | Line(s) | Title |
|----|----------|------|---------|-------|
| A23-1 | MEDIUM | `ondemanddialog.cpp` | 103 | Redundant `m_lastPress` update in `onEnd()` after `debounce()` already wrote it |
| A23-2 | MEDIUM | `ondemanddialog.cpp` | 57–104 | Asymmetric debounce state: `onEnd()` extra update absent in `onStart()`/`onExtend()` |
| A23-3 | MEDIUM | `ondemanddialog.cpp` | 120 | `reset()` calls `showEvent()` directly, passing implicit null event pointer |
| A23-4 | MEDIUM | `ondemanddialog.h` | 36–38 | Action handlers `onStart/onExtend/onEnd` declared `protected` instead of `private` |
| A23-5 | MEDIUM | `pindialog.cpp` | 9, 64 | `PIN_MAX_LENGTH` defined but never used; actual limit is the UI designer property |
| A23-6 | LOW | `pindialog.cpp` | 51 | `static` local for debounce instead of instance member — inconsistent with all other dialogs |
| A23-7 | LOW | `ondemanddialog.h` | 26 | `showCustomTimeFormat()` is `public` but is a private formatting utility |
| A23-8 | LOW | `optionalcheckconfirmationdialog.cpp` | 22–28, 43–48 | `onRefreshLanguage()` duplicates `showEvent()` body verbatim — DRY violation |
| A23-9 | LOW | `optionalcheckconfirmationdialog.cpp` | 28 | Magic number `5000` instead of named constant for auto-dismiss timeout |
| A23-10 | LOW | `optionalcheckconfirmationdialog.cpp` | 4 | Unused `#include <QDebug>` |
| A23-11 | LOW | `pindialog.cpp` | 6 | Unused `#include <QThread>` |
| A23-12 | LOW | `pindialog.cpp` | 4 | Unused `#include <QDebug>` |
| A23-13 | LOW | `ondemanddialog.cpp` | 124–126 | Signed `qint32` used for `quint32` decomposition; potential UB for extreme inputs |
| A23-14 | INFO | `pindialog.cpp` | 82–83 | `QApplication::processEvents()` in slot is a re-entrancy code smell |
| A23-15 | INFO | `ondemanddialog.h`, `optionalcheckconfirmationdialog.h` | 34, 25 | `showEvent(QShowEvent *event = 0)` default-argument inconsistent with Qt style and base class |
# Pass 4 Agent A24 — Code Quality

**Audit run:** 2026-02-28-01
**Branch:** master
**Assigned files:**
- `ui/preopscreenoverlay.h` + `ui/preopscreenoverlay.cpp`
- `ui/supervisordialog.h` + `ui/supervisordialog.cpp`
- `ui/unlockeddialog.h` + `ui/unlockeddialog.cpp`

---

## Reading Evidence

### `ui/preopscreenoverlay.h`

**Class:** `PreopScreenOverlay` (extends `QDialog`)

| Method / Member | Line | Notes |
|---|---|---|
| `explicit PreopScreenOverlay(QWidget *parent = 0)` | 15 | Constructor |
| `~PreopScreenOverlay()` | 16 | Destructor |
| `void onUpdatePreopTimer(QString time)` | 18 | Public slot-like updater |
| `Ui::PreopScreenOverlay *ui` | 21 | Private UI pointer |

**Types/Enums/Constants defined:** None.

---

### `ui/preopscreenoverlay.cpp`

| Method | Line | Notes |
|---|---|---|
| `PreopScreenOverlay::PreopScreenOverlay(QWidget *parent)` | 4 | Constructor — calls `setupUi` |
| `PreopScreenOverlay::onUpdatePreopTimer(QString time)` | 11 | Sets label text with `tr("Time Remaining")` |
| `PreopScreenOverlay::~PreopScreenOverlay()` | 16 | Destructor — deletes `ui` |

**Types/Enums/Constants defined:** None.

---

### `ui/supervisordialog.h`

**Class:** `SupervisorDialog` (extends `QDialog`)

| Member / Method | Line | Notes |
|---|---|---|
| `explicit SupervisorDialog(QWidget *parent = nullptr)` | 20 | Constructor |
| `~SupervisorDialog()` | 21 | Destructor |
| `void setMasterOptions(CIGCONF::MasterId m)` | 23 | Takes `MasterId` struct by value |
| `void setTransportOptions()` | 24 | Configures transport-mode button visibility |
| `void startMasterSession()` (signal) | 31 | Emitted to trigger master login |
| `void startMaintenanceSession()` (signal) | 32 | Emitted to trigger maintenance login |
| `void onVORUpdate()` (signal) | 33 | Signal with `on` prefix (non-standard) |
| `bool debounce()` | 37 | Private — debounce guard |
| `void reset()` | 38 | Private — resets button text and timer |
| `void showEvent(QShowEvent *event = 0)` | 49 | Protected virtual override with default arg |
| `void onUnlkVehicle()` | 52 | Private slot |
| `void onNormalDriverAccess()` | 53 | Private slot |
| `void onActivateVOR()` | 54 | Private slot |
| `void openConfirmationDialog()` | 55 | Private slot |
| `void on_btnMaintenanceMode_clicked()` | 56 | Auto-connected private slot |

**Private data members:**
- `Ui::SupervisorDialog *ui` (line 36)
- `QTimer *m_timer` (line 40)
- `QTimer *m_resetTimer` (line 41)
- `quint32 m_lastPress` (line 42)
- `CIGCONF::MasterId m_master` (line 43)
- `VORConfirmationDialog *m_vorConfirmationDialog` (line 44)
- `WarningDialog *m_maintWarningDialog` (line 45)
- `WarningDialog *m_warningDialog` (line 46)

**Macro constants defined (in .cpp):**
- `NO_ACTIVITY_TIME` = 10000 (line 7)
- `RESET_TIME` = 2000 (line 8)

---

### `ui/supervisordialog.cpp`

| Method | Line | Notes |
|---|---|---|
| `SupervisorDialog::SupervisorDialog(QWidget *parent)` | 10 | Constructor — wires all connects |
| `SupervisorDialog::~SupervisorDialog()` | 47 | Destructor |
| `SupervisorDialog::showEvent(QShowEvent *event)` | 52 | Populates UI text and starts inactivity timer |
| `SupervisorDialog::onUnlkVehicle()` | 88 | Two-tap confirm; emits `startMasterSession` |
| `SupervisorDialog::onNormalDriverAccess()` | 106 | Two-tap confirm; opens warning dialog AND emits `startMasterSession` directly |
| `SupervisorDialog::openConfirmationDialog()` | 126 | Two-tap confirm; opens VOR confirmation dialog |
| `SupervisorDialog::onActivateVOR()` | 144 | Toggles VOR state |
| `SupervisorDialog::debounce()` | 155 | Returns false if < 200 ms since last press |
| `SupervisorDialog::reset()` | 166 | Resets `m_lastPress` and calls `showEvent` |
| `SupervisorDialog::setMasterOptions(CIGCONF::MasterId m)` | 172 | Logs options and sets button visibility via bitmask |
| `SupervisorDialog::setTransportOptions()` | 202 | Hard-codes transport button visibility |
| `SupervisorDialog::on_btnMaintenanceMode_clicked()` | 211 | Two-tap confirm; opens maintenance warning dialog |

---

### `ui/unlockeddialog.h`

**Class:** `UnlockedDialog` (extends `QDialog`)

| Member / Method | Line | Notes |
|---|---|---|
| `enum Mode { UnlockNoChecklist, UnlockChecklist, UnlockOnly }` | 15 | Public enum |
| `explicit UnlockedDialog(QWidget *parent = 0)` | 17 | Constructor |
| `~UnlockedDialog()` | 18 | Destructor |
| `void setMode(Mode m)` | 20 | Configures label visibility per mode |
| `void languageChanged()` | 21 | Refreshes translated strings |
| `Ui::UnlockedDialog *ui` | 28 | Private UI pointer |

**Types/Enums/Constants defined:**
- `enum Mode { UnlockNoChecklist, UnlockChecklist, UnlockOnly }` (line 15)

---

### `ui/unlockeddialog.cpp`

| Method | Line | Notes |
|---|---|---|
| `UnlockedDialog::UnlockedDialog(QWidget *parent)` | 5 | Constructor — sets icon, connects btnOk |
| `UnlockedDialog::~UnlockedDialog()` | 18 | Destructor |
| `UnlockedDialog::setMode(Mode m)` | 23 | Switches on `Mode` enum |
| `UnlockedDialog::languageChanged()` | 42 | Sets `label_3` text to `tr("OK")` |

---

## Findings

---

**A24-1** · HIGH · `startMasterSession` emitted twice in `onNormalDriverAccess`

**Description:** In `supervisordialog.cpp` lines 113–115, `onNormalDriverAccess()` calls `m_warningDialog->open()` and then immediately emits `startMasterSession()` and calls `accept()` — all in the same code path. The `m_warningDialog` (a `Transport`-type `WarningDialog`) is connected in the constructor (lines 33–36) to also `emit startMasterSession()` and `accept()` when its `accepted` signal fires. Because `open()` is used (non-blocking modal), the warning dialog's `accepted` path can complete after the dialog closes, meaning `startMasterSession` is emitted once from the slot directly and then potentially a second time from the `m_warningDialog::accepted` connection. This results in `postLogin()` being invoked twice in the parent `Dialog`, causing double-session initiation.

```cpp
// supervisordialog.cpp:111-115
if (ui->btnNormalDriver->text() == tr("Confirm?")) {
    qDebug() << "current driver id " << gCfg->currentDriverId();
    m_warningDialog->open();       // opens non-blocking; accepted also fires startMasterSession
    emit startMasterSession();     // also fires immediately — duplicate
    accept();
}
// constructor lines 33-36:
connect(m_warningDialog, &WarningDialog::accepted, this, [this](){
    emit startMasterSession();
    accept();
});
```

**Fix:** Remove the direct `emit startMasterSession(); accept();` lines from `onNormalDriverAccess()` and rely solely on the `m_warningDialog::accepted` connection. The pattern used for `on_btnMaintenanceMode_clicked()` (which only calls `m_maintWarningDialog->open()` and lets the `accepted` connection do the work) is the correct model.

---

**A24-2** · HIGH · `m_warningDialog->open()` called but dialog is never confirmed — session starts unconditionally

**Description:** As a consequence of A24-1, the Normal Driver Access path at lines 113–115 calls `emit startMasterSession()` and `accept()` unconditionally, without waiting for the user to confirm or dismiss the `WarningDialog`. The warning dialog is shown as a visual notification, but the session has already started before the user has had a chance to read and acknowledge it. This defeats the purpose of the warning confirmation step.

**Fix:** Remove the immediate `emit startMasterSession(); accept();` from `onNormalDriverAccess()`. Let the `m_warningDialog::accepted` handler (constructor lines 33–36) be the sole path that progresses the session, consistent with the maintenance mode pattern.

---

**A24-3** · MEDIUM · `MasterMenuOptions` enum used as bitmask without `Q_DECLARE_FLAGS`

**Description:** `cigconfigs.h` line 83 defines `MasterMenuOptions` as a plain `enum` with power-of-two values intended for bitwise combination (`UnlockVehicle=1`, `NormalDriverAccess=2`, `ActivateVOR=4`, `MaintenanceMode=8`). `supervisordialog.cpp` lines 180–198 apply bitwise AND (`&`) directly against these enumerators and against `m.option` (typed `quint8`). Qt provides `Q_DECLARE_FLAGS` and `Q_DECLARE_OPERATORS_FOR_FLAGS` to create a type-safe `QFlags<>` wrapper for exactly this pattern. Without it, the compiler will emit warnings on some Qt/C++ configurations ("result of OR on enum values is not an enum value"), and the flag combination is not type-safe — an arbitrary `quint8` value is accepted without error.

```cpp
// cigconfigs.h:83-84
enum MasterMenuOptions {UnlockVehicle=1, NormalDriverAccess=2, ActivateVOR=4,
                        MaintenanceMode=8, DefaultMasterMenu=7, UnassignedMasterMenu=255};

// supervisordialog.cpp:180
if (m.option & CIGCONF::ActivateVOR)   // m.option is quint8, not MasterMenuOptions
```

**Fix:** Declare a `QFlags` type in `cigconfigs.h`:
```cpp
Q_DECLARE_FLAGS(MasterMenuFlags, MasterMenuOptions)
Q_DECLARE_OPERATORS_FOR_FLAGS(CIGCONF::MasterMenuFlags)
```
Change `MasterId::option` from `quint8` to `CIGCONF::MasterMenuFlags`, and update `setMasterOptions` to accept the flag type.

---

**A24-4** · MEDIUM · `MasterId` struct passed by value into `setMasterOptions` — tight coupling to internal layout

**Description:** `SupervisorDialog::setMasterOptions(CIGCONF::MasterId m)` (supervisordialog.h line 23, supervisordialog.cpp line 172) accepts the full `MasterId` struct by value. `SupervisorDialog` only needs two fields: `m.option` (for button visibility) and `m.id` (for VOR activation in `onActivateVOR`). Passing the entire struct couples the dialog tightly to the internal layout of `MasterId`, meaning any future change to that struct (e.g., adding a `QString name` field that becomes expensive to copy, or restructuring `id`) directly affects the dialog API. The name member of `MasterId` is never used within `SupervisorDialog`.

**Fix:** Either pass the two needed values separately (`quint64 masterId, quint8 options`) or pass by const reference (`const CIGCONF::MasterId &m`). Passing by const reference is the minimal change and avoids the unnecessary copy of the `QString name` member on every call.

---

**A24-5** · MEDIUM · `showEvent` overrides a virtual function but declares a default argument

**Description:** `supervisordialog.h` line 49 and `warningdialog.h` line 30 declare `showEvent(QShowEvent *event = 0)`. Adding a default argument to an override of a virtual function is legal C++ but is a recognised anti-pattern: the default is resolved statically based on the pointer type, not the dynamic type. When called through a `QWidget*` or `QDialog*` pointer, the base class default (which has no default) is used; when called directly as `showEvent()` (as done in `supervisordialog.cpp` lines 97, 117, 135, 169), the derived-class default of `nullptr` is silently passed. This creates inconsistent and confusing call semantics, and is the root cause of `Q_UNUSED(event)` being needed at line 54 to suppress the warning.

**Fix:** Remove the `= 0` default from the `showEvent` override in the header. Extract the body of `showEvent` into a private helper (e.g., `void refreshUI()`) and call that helper directly in the places that currently call `showEvent()` without an argument.

---

**A24-6** · MEDIUM · `onVORUpdate` signal uses `on` prefix — naming convention violation

**Description:** `supervisordialog.h` line 33 declares the signal `void onVORUpdate()`. Qt's convention, and the convention used throughout this codebase, is that `on`-prefixed methods are slots (responses to signals), not signals themselves. Using `on` as a signal name creates readability confusion: a reader seeing `connect(..., &SupervisorDialog::onVORUpdate, ...)` is likely to mistake the signal for a slot. The other two signals in the same class (`startMasterSession`, `startMaintenanceSession`) correctly follow the verb-phrase convention.

**Fix:** Rename the signal to `vorStatusChanged()` or `vorUpdated()` and update the connection in `dialog.cpp` line 182 accordingly.

---

**A24-7** · LOW · `PreopScreenOverlay` and `UnlockedDialog` constructors use `= 0` instead of `= nullptr`

**Description:** `preopscreenoverlay.h` line 15 and `unlockeddialog.h` line 17 declare constructors with `QWidget *parent = 0`. `supervisordialog.h` line 20 correctly uses `= nullptr`. Using `0` as a null pointer constant is a C++03 idiom; `nullptr` (C++11) is the correct form for modern Qt/C++ projects and avoids potential ambiguity in overload resolution. The inconsistency also indicates these headers have not been updated alongside the rest of the codebase.

**Fix:** Replace `= 0` with `= nullptr` in the constructor declarations of `PreopScreenOverlay` and `UnlockedDialog`.

---

**A24-8** · LOW · `NO_ACTIVITY_TIME` and `RESET_TIME` defined as bare `#define` macros

**Description:** `supervisordialog.cpp` lines 7–8 define `NO_ACTIVITY_TIME 10000` and `RESET_TIME 2000` as preprocessor macros. These are file-scoped constants with no namespace, no type information, and no debugger visibility. They should be typed constants.

```cpp
#define NO_ACTIVITY_TIME    10000
#define RESET_TIME          2000
```

**Fix:** Replace with typed constants inside the class or as `static constexpr int` in the translation unit:
```cpp
static constexpr int NO_ACTIVITY_TIME = 10000;
static constexpr int RESET_TIME       = 2000;
```

---

**A24-9** · LOW · Mixed tabs and spaces indentation in `supervisordialog.cpp` and `supervisordialog.h`

**Description:** `supervisordialog.cpp` uses 4-space indentation throughout most of the file, but lines 17–18 (constructor initialiser list), line 8 (`RESET_TIME` macro), and several lines in `showEvent`, `onUnlkVehicle`, `onNormalDriverAccess`, `openConfirmationDialog`, `onActivateVOR`, `debounce`, `reset`, and `on_btnMaintenanceMode_clicked` use hard tab characters. `supervisordialog.h` line 49 (`void showEvent`) uses a hard tab while all surrounding lines use 4 spaces. All files also contain Windows-style `\r\n` line endings (`^M` in the raw file). The three other assigned files (`preopscreenoverlay.cpp/h`, `unlockeddialog.cpp/h`) are consistently 4-space indented.

**Fix:** Normalise `supervisordialog.cpp` and `supervisordialog.h` to 4-space indentation throughout and convert line endings to LF-only to match the rest of the UI source files. An `.editorconfig` rule would prevent recurrence.

---

**A24-10** · LOW · `UnlockedDialog::languageChanged` updates `label_3` (auto-generated name) instead of `btnOk`

**Description:** `unlockeddialog.cpp` line 44 sets `ui->label_3->setText(tr("OK"))`. The widget `label_3` is an automatically-generated Qt Designer name with no semantic meaning. The constructor at line 12 sets the icon on `ui->btnOk`, which is the actual OK button. Setting the text of an opaquely-named `label_3` rather than the button itself means that: (a) `label_3` and `btnOk` can display different text, and (b) any redesign of the `.ui` file that renumbers or renames the auto-generated label will silently break the `languageChanged()` call at runtime with no compile-time error.

**Fix:** Rename `label_3` in `unlockeddialog.ui` to `lblOkText` (or remove it if it overlaps visually with `btnOk`), and reference it by the semantic name. Alternatively, if the label is the visible text companion of `btnOk`, update `languageChanged()` to also set `ui->btnOk->setText(tr("OK"))` to keep them in sync.

---

**A24-11** · LOW · `qDebug()` left in production path of `onNormalDriverAccess` and `setMasterOptions`

**Description:** `supervisordialog.cpp` line 112 contains `qDebug() << "current driver id " << gCfg->currentDriverId();` inside the confirmed-second-tap branch of `onNormalDriverAccess()`. Lines 174–176 contain a `qDebug()` call in `setMasterOptions()` that logs the master ID and option bits in hex. These debug statements log security-relevant information (driver identifiers, supervisor credential option bitmasks) to the application debug output on every supervisor action, which may surface in production logs or serial consoles.

**Fix:** Remove the `qDebug()` at line 112. For `setMasterOptions`, replace the debug log with a conditional `qCDebug(categoryName)` that is compiled out in release builds, or remove it entirely.

---

**A24-12** · INFO · `#endif` guard label mismatch in `supervisordialog.h`

**Description:** `supervisordialog.h` line 59 has `#endif // SUPERVISOR_H` but the include guard is defined as `SUPERVISORDIALOG_H` (line 2). The comment is purely informational and has no effect on compilation, but it creates confusion for anyone scanning include guard names and does not match the `_H` suffix pattern used in the rest of the codebase.

**Fix:** Change line 59 to `#endif // SUPERVISORDIALOG_H`.

---

## Summary Table

| ID | Severity | Title |
|---|---|---|
| A24-1 | HIGH | `startMasterSession` emitted twice in `onNormalDriverAccess` |
| A24-2 | HIGH | Warning dialog shown but session starts without waiting for user confirmation |
| A24-3 | MEDIUM | `MasterMenuOptions` bitmask used without `Q_DECLARE_FLAGS` |
| A24-4 | MEDIUM | `MasterId` struct passed by value — leaky abstraction / unnecessary coupling |
| A24-5 | MEDIUM | `showEvent` virtual override declares default argument |
| A24-6 | MEDIUM | Signal `onVORUpdate` uses reserved `on` prefix |
| A24-7 | LOW | `= 0` null pointer in constructors instead of `= nullptr` |
| A24-8 | LOW | `NO_ACTIVITY_TIME` / `RESET_TIME` as untyped `#define` macros |
| A24-9 | LOW | Mixed tabs/spaces and CRLF line endings in `supervisordialog` files |
| A24-10 | LOW | `languageChanged()` targets auto-named `label_3` instead of semantic widget name |
| A24-11 | LOW | `qDebug()` logs security-relevant IDs in production path |
| A24-12 | INFO | `#endif` guard label mismatch in `supervisordialog.h` |
# Pass 4 Agent A25 — Code Quality

**Audit run:** 2026-02-28-01
**Branch:** master
**Auditor:** Agent A25
**Pass:** 4 — Code Quality

---

## 1. Reading Evidence

### 1.1 `ui/unlockreasondialog.h`

**Class:** `UnlockReasonDialog` (inherits `QDialog`)

| Element | Kind | Line |
|---------|------|------|
| `UnlockReasonDialog(QWidget *parent = 0)` | Constructor (public) | 16 |
| `~UnlockReasonDialog()` | Destructor (public) | 17 |
| `QString getReason()` | Public method | 18 |
| `void languageChanged(void)` | Public method | 19 |
| `Ui::UnlockReasonDialog *ui` | Private member | 22 |
| `void setReason()` | Private slot | 23 |
| `QString m_reason` | Private member | 24 |

Types/enums/constants defined: none.

Header guard macro: `UNLOCKREASONDIALOG_H` (guard comment at line 27 incorrectly reads `UNLOCKEDDIALOG_H`).

---

### 1.2 `ui/unlockreasondialog.cpp`

| Element | Kind | Lines |
|---------|------|-------|
| `UnlockReasonDialog::UnlockReasonDialog(QWidget *parent)` | Constructor | 5–32 |
| `UnlockReasonDialog::~UnlockReasonDialog()` | Destructor | 34–37 |
| `void UnlockReasonDialog::setReason()` | Private slot | 39–43 |
| `QString UnlockReasonDialog::getReason()` | Public method | 45–48 |
| `void UnlockReasonDialog::languageChanged(void)` | Public method | 50–71 |

Constants/magic values: none.

---

### 1.3 `ui/vorconfirmationdialog.h`

**Class:** `VORConfirmationDialog` (inherits `QDialog`)

| Element | Kind | Line |
|---------|------|------|
| `VORConfirmationDialog(QWidget *parent = 0)` | Constructor (public) | 15 |
| `~VORConfirmationDialog()` | Destructor (public) | 16 |
| `void isBeingTurnOn(bool on)` | Public method | 18 |
| `Ui::VORConfirmationDialog *ui` | Private member | 21 |
| `QTimer *m_timer` | Private member | 22 |
| `void hideEvent(QHideEvent *)` | Protected override | 25 |
| `void showEvent(QShowEvent *event = 0)` | Protected override | 26 |

Types/enums/constants defined: none.

---

### 1.4 `ui/vorconfirmationdialog.cpp`

| Element | Kind | Lines |
|---------|------|-------|
| `VORConfirmationDialog::VORConfirmationDialog(QWidget *parent)` | Constructor | 6–17 |
| `VORConfirmationDialog::showEvent(QShowEvent *event)` | Protected override | 19–23 |
| `VORConfirmationDialog::hideEvent(QHideEvent *)` | Protected override | 25–28 |
| `VORConfirmationDialog::~VORConfirmationDialog()` | Destructor | 30–33 |
| `void VORConfirmationDialog::isBeingTurnOn(bool on)` | Public method | 35–58 |

Magic numbers: `10000` (line 22 — 10-second timer).

---

### 1.5 `ui/vorwarningdialog.h`

**Class:** `VORWarningDialog` (inherits `QDialog`)

| Element | Kind | Line |
|---------|------|------|
| `VORWarningDialog(QWidget *parent = 0)` | Constructor (public) | 15 |
| `~VORWarningDialog()` | Destructor (public) | 16 |
| `Ui::VORWarningDialog *ui` | Private member | 19 |
| `QTimer *m_timer` | Private member | 20 |
| `void hideEvent(QHideEvent *)` | Protected override | 23 |
| `void showEvent(QShowEvent *event = 0)` | Protected override | 24 |

Types/enums/constants defined: none.

---

### 1.6 `ui/vorwarningdialog.cpp`

| Element | Kind | Lines |
|---------|------|-------|
| `VORWarningDialog::VORWarningDialog(QWidget *parent)` | Constructor | 5–15 |
| `VORWarningDialog::showEvent(QShowEvent *event)` | Protected override | 17–59 |
| `VORWarningDialog::hideEvent(QHideEvent *)` | Protected override | 61–64 |
| `VORWarningDialog::~VORWarningDialog()` | Destructor | 66–69 |

Magic numbers: `30000` (line 57 — 30-second timer).

---

## 2. Findings

---

**A25-1** · HIGH · Inverted boolean semantics in `isBeingTurnOn(bool on)`

**Description:** The public method `VORConfirmationDialog::isBeingTurnOn(bool on)` has inverted boolean semantics. The parameter name `isBeingTurnOn` reads as "is VOR being turned on", yet the implementation tests `if (!on)` to show the "turn ON" UI and `else` (i.e., `on == true`) to show the "turn OFF" UI. In plain terms: passing `true` produces the "turn OFF" confirmation and passing `false` produces the "turn ON" confirmation — the opposite of what the name implies.

The sole call site in `supervisordialog.cpp:132` passes `gCfg->convorStatus()`, which is non-zero when VOR is already active. Passing `1` (VOR currently on) therefore invokes the "turn OFF" branch, which happens to be the operationally correct flow (the user wants to toggle it off), but only because the inversion at the call site and the inversion in the implementation cancel each other out. Any future caller reading the method name and signature will expect `true` = "turning on" and will wire it correctly — but then get the wrong UI.

This is a logic-error / dead semantic: the method is named as a predicate query (`isBeing...`) but acts as a command setter, with its boolean parameter silently inverted relative to its name.

**Fix:** Rename the method to `setVORBeingTurnedOn(bool turningOn)` and correct the body so that `turningOn == true` shows the "turn ON" UI and `turningOn == false` shows the "turn OFF" UI. Update `supervisordialog.cpp:132` accordingly — the call should pass `!gCfg->convorStatus()` (i.e., VOR is currently off, so it is being turned on) to match the corrected semantics.

---

**A25-2** · MEDIUM · Method named as boolean predicate but used as a setter (misnaming / leaky abstraction)

**Description:** `isBeingTurnOn` (line 18 of `vorconfirmationdialog.h`) follows the `is...` naming convention that in C++ and Qt is reserved for boolean query functions returning `bool`. This method returns `void` and configures internal UI state. Callers reading the header cannot determine from the signature alone whether this is a getter or a setter. This constitutes a leaky abstraction: the public interface exposes the VOR on/off state as a raw bool rather than an enum or a named intent, and uses a misleading predicate name.

**Fix:** Replace the raw `bool` parameter with a scoped enum, e.g.:

```cpp
enum class VORAction { TurnOn, TurnOff };
void configureForAction(VORAction action);
```

This makes call sites self-documenting and removes the naming confusion entirely.

---

**A25-3** · MEDIUM · Deprecated Qt4 default constructor argument syntax (`QWidget *parent = 0`)

**Description:** All three dialog header files declare constructors with `QWidget *parent = 0` (null integer literal as a pointer default):

- `unlockreasondialog.h:16`
- `vorconfirmationdialog.h:15`
- `vorwarningdialog.h:15`

Similarly, `showEvent(QShowEvent *event = 0)` uses `= 0` in:

- `vorconfirmationdialog.h:26`
- `vorwarningdialog.h:24`

Using integer `0` as a null pointer constant is deprecated in C++11 and later and produces compiler warnings under `-Wzero-as-null-pointer-constant`. The correct idiom is `nullptr`.

**Fix:** Replace all `= 0` default pointer arguments with `= nullptr` across the three headers. The `showEvent` default argument is additionally questionable (see A25-4 below).

---

**A25-4** · MEDIUM · Default argument on `showEvent` overrides creates dead parameter path

**Description:** Both `VORConfirmationDialog::showEvent(QShowEvent *event = 0)` (h:26) and `VORWarningDialog::showEvent(QShowEvent *event = 0)` (h:24) declare a default argument on an override of a Qt protected virtual. Qt's event system always supplies a non-null `QShowEvent *` when it calls `showEvent`. The default argument `= 0` means a caller could invoke `dialog->showEvent()` directly (without an event object), which would produce undefined behaviour inside Qt's event dispatching chain and is never the intended usage. The matching `Q_UNUSED(event)` in `VORConfirmationDialog::showEvent` (cpp:21) makes this even clearer — the parameter is unused, so there is no legitimate reason to expose a default.

**Fix:** Remove the default argument from both `showEvent` overrides. The correct signature is `void showEvent(QShowEvent *event) override;`. Mark both overrides with `override` to catch future base-class signature changes.

---

**A25-5** · MEDIUM · Magic numbers for timer durations

**Description:** Timer start values are embedded as bare integer literals with no named constant:

- `vorconfirmationdialog.cpp:22` — `m_timer->start(10000)` (10-second auto-reject)
- `vorwarningdialog.cpp:57` — `m_timer->start(30000)` (30-second auto-reject, with an inline comment)

These magic numbers make it impossible to find or change all timeout values from a single location. The 10-second timeout in the confirmation dialog has no comment at all; a maintainer must derive its significance. The VOR confirmation dialog auto-rejects after 10 seconds, which is a safety-relevant timeout that could be accidentally changed.

**Fix:** Define named constants, either as `static constexpr int` members or in a shared constants header:

```cpp
static constexpr int kVORConfirmTimeoutMs  = 10'000;   // vorconfirmationdialog
static constexpr int kVORWarningTimeoutMs  = 30'000;   // vorwarningdialog
```

Replace the bare literals with the named constants and add a comment on `kVORConfirmTimeoutMs` explaining its safety rationale.

---

**A25-6** · LOW · Inconsistent `#include` of `QTimer` — missing from `vorconfirmationdialog.h`

**Description:** Both `VORConfirmationDialog` and `VORWarningDialog` hold a `QTimer *m_timer` private member. `vorwarningdialog.h` does not include `<QTimer>` directly (it is included only in the `.cpp`), and neither does `vorconfirmationdialog.h`. Both headers depend on a forward declaration being satisfied by a transitive include. If the include order in any translation unit changes, the headers will fail to compile in isolation. This is a fragility, not an immediate defect, but it violates the rule that each header should compile standalone.

**Fix:** Add `#include <QTimer>` (or at minimum `QT_FORWARD_DECLARE_CLASS(QTimer)`) to both `vorconfirmationdialog.h` and `vorwarningdialog.h`.

---

**A25-7** · LOW · Incorrect header guard comment in `unlockreasondialog.h`

**Description:** The closing `#endif` comment at line 27 of `unlockreasondialog.h` reads:

```cpp
#endif // UNLOCKEDDIALOG_H
```

but the guard macro defined at line 1 is `UNLOCKREASONDIALOG_H`. The comment is a copy-paste artefact and does not match the actual guard name.

**Fix:** Change line 27 to `#endif // UNLOCKREASONDIALOG_H`.

---

**A25-8** · LOW · Inline HTML template string hard-coded in `showEvent` — maintainability hazard

**Description:** `VORWarningDialog::showEvent` (cpp:25–53) constructs a multi-paragraph HTML string by concatenating six raw `QString` fragment literals, each containing full HTML 4.0 boilerplate including a `<!DOCTYPE>` declaration, inline `<style>`, and per-paragraph `<span>` wrappers. This HTML is hard-coded in an event handler that fires every time the dialog is shown, meaning the string allocation and construction happen on every show event. The content also hard-codes the font family `'MS Shell Dlg 2'` (Windows-specific shell font), which is inconsistent with the Ubuntu font specified inside the same snippet.

Additionally, the HTML construction is entirely separate from the translatable text strings (`text1`, `text2`, `text3`), but the HTML wrapper cannot itself be translated — if the UI ever needs different formatting per language, the function would require structural changes.

**Fix:** Move the static HTML wrapper text into the `.ui` file as the default rich-text content of `textEdit`, and replace the `showEvent` body with only the three `setText` calls for the translatable strings. Alternatively, use a `QTextDocument` with proper `setHtml` only once at construction and update only the translatable segments on language change.

---

**A25-9** · LOW · `setReason()` uses `sender()` cast without type guard

**Description:** `UnlockReasonDialog::setReason()` (cpp:41) casts `sender()` directly to `QPushButton *` without any runtime type check:

```cpp
m_reason = ((QPushButton *)sender())->text();
```

`QObject::sender()` returns `QObject *`. A C-style cast to `QPushButton *` bypasses Qt's type system. If the slot were ever accidentally connected to a non-`QPushButton` signal emitter, this would be undefined behaviour. The correct Qt idiom is `qobject_cast<QPushButton *>(sender())` with a null guard.

**Fix:** Replace with:

```cpp
QPushButton *btn = qobject_cast<QPushButton *>(sender());
if (btn) {
    m_reason = btn->text();
    emit accept();
}
```

---

**A25-10** · LOW · `override` keyword absent on all virtual overrides

**Description:** None of the overriding virtual methods in the three classes use the `override` specifier:

- `VORConfirmationDialog::hideEvent`, `showEvent` (h:25–26)
- `VORWarningDialog::hideEvent`, `showEvent` (h:23–24)

Without `override`, a typo in the method signature (e.g., wrong parameter type) silently creates a new virtual function rather than overriding the base class, and the base-class version is called instead. This is a standard C++11 best-practice violation.

**Fix:** Add `override` to all four method declarations in both headers.

---

**A25-11** · INFO · Style inconsistency: mixed indentation in `vorconfirmationdialog.cpp`

**Description:** `vorconfirmationdialog.cpp` mixes space-indentation (4 spaces, lines 35–57) with tab-indentation (lines 48 and 57 close-brace lines). The `isBeingTurnOn` function body at line 48 (`} else {`) and line 57 (`}`) uses a tab character while the surrounding code uses spaces. This is a minor style inconsistency indicating two different authors or editors touched this function.

**Fix:** Normalise the file to use 4-space indentation throughout, consistent with the rest of the `.cpp` files in the `ui/` directory.

---

**A25-12** · INFO · Typo in UI label name: `lblCornfirm` (missing 'f' in "confirm")

**Description:** `vorconfirmationdialog.cpp` references `ui->lblCornfirm` (lines 38, 41, 43, 50, 52) — the widget name in the `.ui` file is misspelled as `Cornfirm` instead of `Confirm`. This is a cosmetic defect in the form designer but it propagates into the C++ identifier, making the code harder to search and review.

**Fix:** Rename the widget in `vorconfirmationdialog.ui` from `lblCornfirm` to `lblConfirm` and update all references in the `.cpp` file. This requires a regeneration of the `ui_vorconfirmationdialog.h` auto-generated header.

---

## 3. Summary Table

| ID | Severity | Title | Location |
|----|----------|-------|----------|
| A25-1 | HIGH | Inverted boolean semantics in `isBeingTurnOn(bool on)` | `vorconfirmationdialog.h:18`, `vorconfirmationdialog.cpp:35–58` |
| A25-2 | MEDIUM | Method named as boolean predicate but used as a setter | `vorconfirmationdialog.h:18` |
| A25-3 | MEDIUM | Deprecated `= 0` null pointer default arguments | `unlockreasondialog.h:16`, `vorconfirmationdialog.h:15,26`, `vorwarningdialog.h:15,24` |
| A25-4 | MEDIUM | Default argument on `showEvent` override enables undefined-behaviour call path | `vorconfirmationdialog.h:26`, `vorwarningdialog.h:24` |
| A25-5 | MEDIUM | Magic numbers for safety-relevant timer durations | `vorconfirmationdialog.cpp:22`, `vorwarningdialog.cpp:57` |
| A25-6 | LOW | `<QTimer>` not included in headers that declare `QTimer *` members | `vorconfirmationdialog.h`, `vorwarningdialog.h` |
| A25-7 | LOW | Incorrect `#endif` guard comment | `unlockreasondialog.h:27` |
| A25-8 | LOW | Hard-coded inline HTML template built in `showEvent` on every show | `vorwarningdialog.cpp:25–53` |
| A25-9 | LOW | C-style cast of `sender()` without type guard | `unlockreasondialog.cpp:41` |
| A25-10 | LOW | `override` specifier absent on all virtual overrides | `vorconfirmationdialog.h:25–26`, `vorwarningdialog.h:23–24` |
| A25-11 | INFO | Mixed tab/space indentation in `vorconfirmationdialog.cpp` | `vorconfirmationdialog.cpp:48,57` |
| A25-12 | INFO | Typo `lblCornfirm` in widget name | `vorconfirmationdialog.cpp:38,41,43,50,52` |
# Pass 4 Agent A26 — Code Quality

**Audit run:** 2026-02-28-01
**Branch:** master
**Repo root:** C:/Projects/cig-audit/repos/mark3-pvd
**Agent scope:** ui/warningdialog, utils/barcode128, utils/bytearray, utils/logger, utils/zconf (3P), utils/zlib (3P)

---

## 1. Reading Evidence

### `ui/warningdialog.h`

**Class:** `WarningDialog` (extends `QDialog`)

**Enum defined:**
- `WarningDialogType` — values: `VOR`, `Transport`, `Maintenance` (line 10, file-scope, not inside the class)

**Member variables:**
- `Ui::WarningDialog *ui` (line 21)
- `QTimer *m_timer` (line 22)
- `WarningDialogType m_type` (line 23)

**Methods declared:**

| Line | Signature |
|------|-----------|
| 17 | `explicit WarningDialog(WarningDialogType type, QWidget *parent = 0)` |
| 18 | `~WarningDialog()` |
| 24 | `QString showVorWarning()` (private) |
| 25 | `QString showTransportWarning()` (private) |
| 26 | `QString showMaintenanceWarning()` (private) |
| 29 | `void hideEvent(QHideEvent *)` (protected override) |
| 30 | `void showEvent(QShowEvent *event = 0)` (protected override) |

---

### `ui/warningdialog.cpp`

**Functions / methods defined:**

| Line | Signature |
|------|-----------|
| 5  | `WarningDialog::WarningDialog(WarningDialogType type, QWidget *parent)` — constructor |
| 18 | `void WarningDialog::showEvent(QShowEvent *event)` |
| 47 | `QString WarningDialog::showTransportWarning()` |
| 84 | `QString WarningDialog::showVorWarning()` |
| 120 | `QString WarningDialog::showMaintenanceWarning()` |
| 156 | `void WarningDialog::hideEvent(QHideEvent *)` |
| 161 | `WarningDialog::~WarningDialog()` |

No types, enums, or constants defined in the `.cpp` file.

---

### `utils/barcode128.h`

**Classes defined:**

**`BarcodeChar`**

| Line | Signature |
|------|-----------|
| 10 | `BarcodeChar()` — default constructor |
| 17 | `BarcodeChar(const BarcodeChar &other)` — copy constructor |
| 24 | `BarcodeChar(int value, QString name, QString pattern)` — value constructor |
| 31 | `BarcodeChar &operator=(const BarcodeChar &other)` |

Private members: `int m_value`, `QString m_name`, `QString m_pattern`
Friend: `class Barcode128`

**`Barcode128`**

| Line | Signature |
|------|-----------|
| 50 | `Barcode128(const QString &info, int height = 100, int sizeMult = 2)` — constructor |
| 51 | `~Barcode128()` |
| 52 | `static int width(const QString &info, int sizeMult)` |
| 54 | `QPixmap pixmap()` |
| 57 | `void initChar(int value, const QString &name, const QString &pattern)` (private) |
| 58 | `void initChars()` (private) |
| 59 | `void encodeChar(const BarcodeChar &ch)` (private) |
| 60 | `void drawBlackVerticalLineAtPos()` (private) |
| 61 | `void drawEmptyVerticalLineAtPos()` (private) |

Private members: `QMap<int, BarcodeChar> m_valueToChar`, `QMap<QString, BarcodeChar> m_nameToChar`, `QImage *m_image`, `int m_pos`, `int m_sizeMult`

---

### `utils/barcode128.cpp`

**Macros / constants defined:**

| Line | Name | Value |
|------|------|-------|
| 5 | `START_CODE` | `104` |
| 6 | `END_CODE` | `106` |
| 7 | `MODULO_VAL` | `103` |

**Functions / methods defined:**

| Line | Signature |
|------|-----------|
| 9  | `Barcode128::Barcode128(const QString &info, int height, int sizeMult)` |
| 39 | `Barcode128::~Barcode128()` |
| 45 | `QPixmap Barcode128::pixmap()` |
| 53 | `void Barcode128::initChar(int value, const QString &name, const QString &pattern)` |
| 61 | `void Barcode128::initChars()` — contains `#if START_CODE == 103` / `#elif START_CODE == 104` / `#else // todo type c` branches |
| 283 | `void Barcode128::encodeChar(const BarcodeChar &ch)` |
| 298 | `void Barcode128::drawBlackVerticalLineAtPos()` |
| 309 | `void Barcode128::drawEmptyVerticalLineAtPos()` |
| 320 | `int Barcode128::width(const QString &info, int sizeMult)` |

**Duplicate key in `initChars()` (Code B / `START_CODE == 104` branch):**
- Line 184: `initChar(12, "0", "10110011100")` — inserts key `"0"` into `m_nameToChar`
- Line 188: `initChar(16, "0", "10011101100")` — immediately overwrites key `"0"` in `m_nameToChar`

The same duplicate appears in the `START_CODE == 103` branch (lines 76 and 80).

---

### `utils/bytearray.h` (header-only)

**Macros defined:**

| Line | Macro |
|------|-------|
| 6 | `LE_INT(c1, c2, c3, c4)` |
| 7 | `BE_INT(c1, c2, c3, c4)` |
| 8 | `LE_SHORT(c1, c2)` |
| 9 | `BE_SHORT(c1, c2)` |
| 11 | `BE_LONG(c1, c2, c3, c4, c5, c6, c7, c8)` |

**Class:** `ByteArray`

| Line | Signature |
|------|-----------|
| 16 | `static QByteArray asprintf(const char *cformat, ...)` |
| 30 | `static int sscanf(const QByteArray &ba, const char *cformat, ...)` |

No enums or constants defined in the class body.

---

### `utils/logger.h`

**Enum defined:**
- `LogLevel` (file-scope, line 8): `LogDebug`, `LogInfo`, `LogWarning`, `LogCritical`, `LogFatal`, `LogNone`

**Class:** `Logger`

Static members: `Logger *m_instance`, `QMutex m_mutex`

Instance members: `QFile m_file`, `QTextStream m_outStream`, `LogLevel m_logThreshold`, `QtMessageHandler m_oldHandler`

| Line | Signature |
|------|-----------|
| 13 | `static Logger* instance()` |
| 14 | `void close()` |
| 15 | `void setLogThreshold(LogLevel level)` |
| 16 | `LogLevel logThreshold() const` |
| 17 | `void log(LogLevel level, const QString &message)` |
| 20 | `Logger()` (protected constructor) |
| 21 | `virtual ~Logger()` |
| 22 | `static void logMessageHandler(QtMsgType type, const QMessageLogContext &context, const QString &msg)` (protected) |

---

### `utils/logger.cpp`

**Macro / constant defined:**

| Line | Name | Value |
|------|------|-------|
| 8 | `LOG_FILE_DIR` | `"/mnt/sd"` |

**Functions / methods defined:**

| Line | Signature |
|------|-----------|
| 13 | `Logger::Logger()` — constructor |
| 46 | `Logger::~Logger()` |
| 54 | `Logger *Logger::instance()` |
| 62 | `void Logger::close()` |
| 70 | `void Logger::setLogThreshold(LogLevel level)` |
| 75 | `LogLevel Logger::logThreshold() const` |
| 80 | `void Logger::log(LogLevel level, const QString &msg)` |
| 117 | `void Logger::logMessageHandler(QtMsgType type, const QMessageLogContext &context, const QString &msg)` |

---

### `utils/zconf.h` and `utils/zlib.h`

Both are upstream zlib 1.3.1 (January 22nd, 2024). No project-specific additions, modifications, or extra symbols were found. No findings generated for these files.

---

## 2. Findings

---

**A26-1** · CRITICAL · `ByteArray::asprintf` uses `va_list` after `va_end` — undefined behaviour

**Description:**
In `utils/bytearray.h` lines 16–27, `asprintf` calls `va_start(ap, cformat)` to measure the required buffer size with `vsnprintf(..., 0, ...)`, then calls `va_end(ap)`. After `va_end`, the `va_list` object `ap` is indeterminate. The subsequent call to `vsprintf(ba.data(), cformat, ap)` on line 25 reuses the already-ended `va_list`, which is undefined behaviour per C99/C++11 §7.16. On ARM targets (the deployment platform) the ABI passes arguments in registers that `va_end` may trash or zero; the resulting `vsprintf` may produce garbage output, read unmapped memory, or crash. This function is called in at least 30 production `.cpp` files throughout the codebase.

**Fix:** Declare a second `va_list ap2`, call `va_copy(ap2, ap)` before `va_end(ap)`, then use `ap2` for the second format call, ending with `va_end(ap2)`. Alternatively, replace the entire function with `QByteArray::asprintf()` (available since Qt 5.5) which is safe and removes the custom variadic wrapper entirely.

---

**A26-2** · HIGH · `ByteArray::asprintf` allocates buffer without space for NUL terminator

**Description:**
In `utils/bytearray.h` line 24, `ba.resize(size)` allocates exactly `size` bytes, where `size` is the return value of `vsnprintf(nullptr, 0, ...)`. The POSIX specification for `vsnprintf` states that the return value is the number of characters that would have been written *excluding* the terminating NUL byte. `QByteArray::resize(n)` allocates `n` bytes; `vsprintf` on line 25 then writes `size` characters plus a NUL terminator, writing one byte past the end of the allocated buffer. This is a one-byte heap overflow on every call. Even if the downstream Qt code never reads past `size` bytes, the heap corruption is real and exploitable.

**Fix:** Change `ba.resize(size)` to `ba.resize(size + 1)`, then after the `vsprintf` call truncate the trailing NUL with `ba.resize(size)` if a NUL-free `QByteArray` is required. Or, as above, replace with `QByteArray::asprintf()`.

---

**A26-3** · HIGH · `Logger::instance()` is not thread-safe — double-checked locking missing

**Description:**
In `utils/logger.cpp` lines 54–60, `Logger::instance()` checks `m_instance == nullptr` and, if so, constructs a new `Logger`. There is no mutex guard around this check-and-assign sequence. If two threads call `instance()` simultaneously before the singleton is constructed, both may observe `m_instance == nullptr` and both construct a `Logger`, leaking one instance, installing two `qInstallMessageHandler` callbacks in sequence, and overwriting `m_oldHandler`. The static `m_mutex` is used correctly inside `log()`, but the singleton initialisation itself is unprotected. The `close()` function (lines 62–68) has the same problem in reverse: it deletes and nullifies `m_instance` without holding the mutex, racing with concurrent `log()` calls that have already loaded the pointer but not yet entered their own `QMutexLocker`.

**Fix:** Protect the `instance()` body with a `QMutexLocker locker(&m_mutex)` guard. Alternatively, replace the manual singleton with a function-local static (`static Logger inst; return &inst;`), which is guaranteed to be initialised once under C++11's magic-statics rules without any explicit locking. Apply the same mutex guard to `close()`.

---

**A26-4** · MEDIUM · Duplicate key `"0"` in `Barcode128::initChars()` makes one barcode character unreachable

**Description:**
In `utils/barcode128.cpp` inside both the `#if START_CODE == 103` branch (lines 76 and 80) and the active `#elif START_CODE == 104` branch (lines 184 and 188), `initChar` is called twice with the name `"0"`. The second call (`value=16, name="0"`) silently overwrites the first (`value=12, name="0"`) in `m_nameToChar` because `QMap::insert` replaces existing keys. Value 12 in Code B is the comma `,`; value 16 is the digit `0`. The net effect is that the digit `0` encodes correctly (value 16 is the right barcode-128 Code B mapping for `'0'`), but value 12 (`,`) can never be looked up by character name from `m_nameToChar`. If any caller ever attempts to encode a comma by name lookup it will silently get the `"0"` entry instead. Additionally, value 12 in Code A is the comma but the Code A table mistakenly uses `"0"` as well, suggesting a copy-paste error during table transcription.

**Fix:** Replace the second `initChar(12, "0", ...)` call with the correct character name. In Code B the character with value 12 is `,` (ASCII 44). Change line 184 of the Code B branch to `initChar(12, ",", "10110011100")`. Apply the equivalent correction to the Code A branch.

---

**A26-5** · MEDIUM · `WarningDialog` HTML generation is massively duplicated — single-character change risk

**Description:**
In `ui/warningdialog.cpp`, the three private methods `showTransportWarning()` (lines 47–82), `showVorWarning()` (lines 84–118), and `showMaintenanceWarning()` (lines 120–154) are structurally identical. Each reconstructs all six HTML fragment strings (`html1_start`, `html1_end`, `html2_start`, `html2_end`, `html3_start`, `html3_end`) in full, then builds the combined message using the same `reserve` + eight `append` calls. The only variation between the three methods is the content of `text1` (the vehicle-mode description). This is a textbook duplication risk: any change to the HTML template (e.g. a font name, CSS rule, or structure change) must be applied in three separate places consistently. It also inflates the binary and translation surface unnecessarily.

**Fix:** Refactor to a single private helper, e.g. `QString buildWarningHtml(const QString &text1, const QString &text2, const QString &text3)`, and have each of the three public-facing methods call it with the appropriate `text1`. `text2` and `text3` are already identical across all three variants and need only be defined once.

---

**A26-6** · MEDIUM · `WarningDialogType` enum is file-scope, not class-scope

**Description:**
In `ui/warningdialog.h` line 10, `enum WarningDialogType {VOR, Transport, Maintenance}` is declared at global namespace scope, not inside `WarningDialog`. The enumerator names `VOR`, `Transport`, and `Maintenance` are injected into the global namespace. `Transport` and `Maintenance` are common English words with a high collision risk in any future global symbol or platform SDK inclusion. `VOR` is the ICAO aviation acronym for VHF Omnidirectional Range and may conflict with third-party aviation or avionics libraries.

**Fix:** Move the enum inside the `WarningDialog` class body (or use `enum class WarningDialogType` as a scoped enum in C++11), and update the three call sites in `warningdialog.cpp`'s `switch` statement to use the qualified form `WarningDialog::VOR`, etc.

---

**A26-7** · LOW · `showEvent` override uses deprecated `QWidget *parent = 0` default parameter style

**Description:**
In `ui/warningdialog.h` line 30, the protected override `void showEvent(QShowEvent *event = 0)` declares a default argument of `0` (implicit null pointer) for the event parameter. The same pattern appears on line 17 for the constructor's `parent` parameter. Using integer literal `0` instead of `nullptr` is pre-C++11 style; the Qt documentation recommends `nullptr` from Qt 5 onward. The default-argument on `showEvent` is also misleading because Qt's event system always passes a valid, non-null `QShowEvent *` to overridden `showEvent`; a default argument implies the override can be called with no event, which it should not be.

**Fix:** Replace `= 0` with `= nullptr` on the constructor parameter (line 17) and remove the default argument entirely from the `showEvent` declaration (line 30), since overrides should match the base class signature exactly.

---

**A26-8** · LOW · `BeepType` enum defined but none of its values are used anywhere in the codebase

**Description:**
`platform/pwmbeeper.h` (line 15) defines a nested enum `PwmBeeper::BeepType` with values `BeepOn`, `BeepSilent`, and `BeepOff`. A grep across all `.cpp` files in the repository finds zero references to any of these enum values. The enum is not used internally within `PwmBeeper` itself — the beeper state is tracked via `bool m_beeping` and `void setBeep(bool on)`. This is dead code that adds confusion about the intended control API and may indicate an abandoned refactoring.

**Fix:** Remove the `BeepType` enum declaration from `platform/pwmbeeper.h`. If a future multi-state beep API is intended, implement and use it before committing.

---

**A26-9** · LOW · `Barcode128::initChars()` has an unimplemented Type C branch left with a comment

**Description:**
In `utils/barcode128.cpp` line 279, the preprocessor branch `#else // todo type c` is empty. If `START_CODE` were ever set to `105` (Code C mode), `initChars()` would run without inserting any characters, leaving both `QMap`s empty. Encoding would silently produce an all-zeros-value barcode rather than an error. The comment `// todo type c` documents a known incomplete implementation with no associated issue or deadline.

**Fix:** Add either a `static_assert` or a `#error` directive inside the `#else` branch to produce a compile-time failure if `START_CODE` is set to an unsupported value. This converts the silent runtime failure into a build-time error.

---

**A26-10** · LOW · `ByteArray::asprintf` comment documents unsafety but does not prevent use

**Description:**
`utils/bytearray.h` lines 15 and 29 contain comments stating "actually, do not recommend as not type safe" and "not recommend too". These comments acknowledge known problems (also found as CRITICAL and HIGH issues above) but do not discourage use at the call site and do not carry a deprecation marker. The function is called in over 30 production `.cpp` files. Self-deprecating comments without enforced deprecation provide no protection.

**Fix:** Add `[[deprecated("Use QByteArray::asprintf() instead")]]` or the Qt equivalent `Q_DECL_DEPRECATED_X(...)` to the function signatures. This produces a compiler warning at every call site, driving migration. Remove the functions once all call sites are updated.

---

**A26-11** · INFO · Mixed indentation (tabs vs spaces) in `warningdialog.h`

**Description:**
`ui/warningdialog.h` mixes tab characters (lines 22, 29, 30) with four-space indentation (lines 17–18, 21, 24–26). This is a minor style inconsistency that does not affect correctness but reduces readability and may cause diff noise.

**Fix:** Normalise to the project's chosen style (four spaces, as used in the majority of the codebase) using an editor formatter or `expand`.

---

## 3. Summary Table

| ID | Severity | File(s) | Short Title |
|----|----------|---------|-------------|
| A26-1 | CRITICAL | `utils/bytearray.h:25` | `asprintf` reuses `va_list` after `va_end` — UB |
| A26-2 | HIGH | `utils/bytearray.h:24` | Buffer allocation off by one — heap overflow on every call |
| A26-3 | HIGH | `utils/logger.cpp:54-68` | `Logger::instance()` / `close()` not thread-safe |
| A26-4 | MEDIUM | `utils/barcode128.cpp:184,188` | Duplicate key `"0"` in `initChars()` — one entry unreachable |
| A26-5 | MEDIUM | `ui/warningdialog.cpp:47-154` | Three-way HTML generation duplication — maintenance hazard |
| A26-6 | MEDIUM | `ui/warningdialog.h:10` | `WarningDialogType` enum in global namespace — name pollution |
| A26-7 | LOW | `ui/warningdialog.h:17,30` | Deprecated `= 0` null pointer style; misleading default on `showEvent` |
| A26-8 | LOW | `platform/pwmbeeper.h:15` | `BeepType` enum entirely unused — dead code |
| A26-9 | LOW | `utils/barcode128.cpp:279` | Unimplemented Type C branch — silent empty-map failure |
| A26-10 | LOW | `utils/bytearray.h:15,29` | Unsafety comment without deprecation attribute |
| A26-11 | INFO | `ui/warningdialog.h` | Mixed tab/space indentation |
