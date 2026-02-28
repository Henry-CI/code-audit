# Pass 4 – B001

**Date:** 2026-02-27
**Audit run:** 2026-02-27-01
**Agent:** B001

**Files reviewed:**
- `lib/api_server.ex`
- `lib/api_server/application.ex`
- `lib/api_server/guardian.ex`
- `lib/api_server/repo.ex`
- `mix.exs`
- `mix.lock`

---

## Reading Evidence

### `lib/api_server.ex`

- **Module:** `ApiServer`
- **Functions:** none (module body is only a `@moduledoc`)
- **Types / errors / constants:** none
- **Notes:** Boilerplate Phoenix context module; no logic.

---

### `lib/api_server/application.ex`

- **Module:** `ApiServer.Application`
- **Functions:**
  - `start/2` — line 6
  - `config_change/3` — line 36
- **Types / errors / constants:** none
- **Notable patterns:**
  - `import Supervisor.Spec` at line 7 — called *inside* the `start/2` function body, not at module level.
  - Supervisor children defined with the deprecated `supervisor/2` helper (lines 14–17) from `Supervisor.Spec`, mixed with the current `{Module, opts}` tuple style (lines 19, 21–22, 25).
  - Commented-out worker line at line 24.

---

### `lib/api_server/guardian.ex`

- **Module:** `ApiServer.Guardian`
- **Functions:**
  - `subject_for_token/2` (clause 1) — line 6
  - `subject_for_token/2` (clause 2) — line 14
  - `resource_from_claims/1` (clause 1) — line 18
  - `resource_from_claims/1` (clause 2) — line 24
- **Aliases:** `ApiServer.Vx` — line 4
- **Types / errors / constants:** none
- **Notable patterns:**
  - Indentation is 4-space inside the module vs. the Elixir community standard of 2-space.
  - Error atom used is `:reason_for_error` — a placeholder string, not a meaningful error term.
  - Second clause of `subject_for_token/2` (`def subject_for_token(_, _)`) is unreachable: the first clause matches on any two arguments (using `if user == nil`), so the catch-all second clause can never be reached.
  - Second clause of `resource_from_claims/1` is unreachable for the same reason — the first clause matches `_claims` (any value).

---

### `lib/api_server/repo.ex`

- **Modules:**
  - `ApiServer.Repo` — line 1
  - `ApiServer.FortyNineRepo` — line 13
- **Functions:**
  - `ApiServer.Repo.init/2` — line 8
- **Types / errors / constants:** none
- **Notable patterns:**
  - `ApiServer.Repo` implements `init/2` to dynamically load `DATABASE_URL` at runtime (line 9).
  - `ApiServer.FortyNineRepo` has no `init/2` callback — it relies solely on compile-time / config-file configuration with no runtime URL override.
  - Both repos are started as `supervisor(...)` children in `application.ex` but only one supports dynamic URL loading.

---

### `mix.exs`

- **Module:** `ApiServer.Mixfile`
- **Functions:**
  - `project/0` — line 4
  - `application/0` — line 20
  - `elixirc_paths/1` (`:test` clause) — line 28
  - `elixirc_paths/1` (catch-all clause) — line 29
  - `deps/0` (private) — line 34
  - `aliases/0` (private) — line 73
- **Dependencies declared (line : dep):**
  - 36: `phoenix ~> 1.5.9`
  - 37: `phoenix_pubsub ~> 2.0`
  - 38: `phoenix_ecto ~> 3.2`
  - 39: `mariaex ~>0.8.2`
  - 40: `phoenix_html ~> 2.10`
  - 41: `phoenix_live_reload ~> 1.0` (dev only)
  - 42: `gettext ~> 0.11`
  - 43: `cowboy ~> 1.0`
  - 44: `cors_plug ~> 1.5`
  - 45: `distillery ~> 1.5`
  - 46: `ex_crc ~> 1.0.0`
  - 47: `absinthe ~> 1.4.0`
  - 48: `absinthe_plug ~> 1.4.0`
  - 49: `absinthe_ecto ~> 0.1.3`
  - 50: `httpoison ~> 1.6`
  - 51: `poison ~> 3.1`
  - 52: `elixir_xml_to_map ~> 0.1`
  - 53: `timex ~> 3.1`
  - 54: `guardian ~> 1.0`
  - 55: `csv ~> 2.1.1`
  - 56: `geonames` (path dep)
  - 57: `geohax >= 0.0.0`
  - 58: `con_cache ~> 0.13`
  - 59: `topo ~> 0.1.0`
  - 60: `bamboo ~> 1.2`
  - 61: `bamboo_smtp ~> 2.1.0`
  - 62: `quantum ~> 2.3`
  - 63: `plug_cowboy ~> 1.0`

---

### `mix.lock`

- **Locked packages (name : locked version):**
  - `absinthe` 1.4.16
  - `absinthe_ecto` 0.1.3
  - `absinthe_plug` 1.4.7
  - `bamboo` 1.5.0
  - `bamboo_smtp` 2.1.0
  - `base64url` 0.0.1
  - `certifi` 2.5.2
  - `combine` 0.10.0
  - `con_cache` 0.14.0
  - `connection` 1.0.4
  - `cors_plug` 1.5.2
  - `cowboy` 1.1.2
  - `cowlib` 1.0.2
  - `crontab` 1.1.10
  - `csv` 2.1.1
  - `db_connection` 1.1.3
  - `decimal` 1.8.1
  - `distillery` 1.5.5
  - `ecto` 2.2.12
  - `elixir_xml_to_map` 0.2.0
  - `erlsom` 1.5.0
  - `ex_crc` 1.0.0
  - `file_system` 0.2.8
  - `gen_smtp` 0.15.0
  - `gen_stage` 1.0.0
  - `gen_state_machine` 2.1.0
  - `geo` 1.5.0
  - `geohax` 0.3.0
  - `gettext` 0.18.0
  - `guardian` 1.2.1
  - `hackney` 1.16.0
  - `httpoison` 1.6.2
  - `idna` 6.0.1
  - `jose` 1.10.1
  - `libring` 1.5.0
  - `mariaex` 0.8.4
  - `metrics` 1.0.1
  - `mime` 2.0.2
  - `mimerl` 1.2.0
  - `parallel_stream` 1.0.6
  - `parse_trans` 3.3.0
  - `phoenix` 1.5.13
  - `phoenix_ecto` 3.6.0
  - `phoenix_html` 2.14.2
  - `phoenix_live_reload` 1.1.7
  - `phoenix_pubsub` 2.1.1
  - `plug` 1.13.6
  - `plug_cowboy` 1.0.0
  - `plug_crypto` 1.2.2
  - `poison` 3.1.0
  - `poolboy` 1.5.2
  - `postgrex` 0.13.5
  - `quantum` 2.4.0
  - `ranch` 1.3.2
  - `seg_seg` 0.0.1
  - `ssl_verify_fun` 1.1.6
  - `swarm` 3.4.0
  - `telemetry` 1.1.0
  - `timex` 3.6.2
  - `topo` 0.1.2
  - `tzdata` 1.0.3
  - `unicode_util_compat` 0.5.0
  - `vector` 0.2.2

---

## Findings

**B001-1** — [LOW] Commented-out worker stub left in production supervisor child list
File: `lib/api_server/application.ex:24`
Description: The line `# worker(ApiServer.Worker, [arg1, arg2, arg3]),` is a Phoenix generator boilerplate comment that was never cleaned up. Commented-out code in a supervision tree definition is noise that can confuse readers about intended topology and should be removed.

---

**B001-2** — [MEDIUM] Deprecated `Supervisor.Spec` imported inside function body
File: `lib/api_server/application.ex:7`
Description: `import Supervisor.Spec` appears inside the `start/2` function body rather than at module level. `Supervisor.Spec` itself was deprecated in Elixir 1.5 and removed in Elixir 1.11; using `supervisor/2` and `worker/2` helpers from this module generates build warnings on any supported Elixir version. The import-inside-function pattern is also an unusual style that hides the dependency.

---

**B001-3** — [MEDIUM] Mixed child-spec styles in supervision tree
File: `lib/api_server/application.ex:14-25`
Description: The supervisor children list mixes two incompatible patterns. Lines 14–17 use the deprecated `supervisor(Module, [])` tuple form from `Supervisor.Spec`, while lines 19, 21–22, and 25 use the modern `{Module, opts}` and bare-module child-spec forms introduced in OTP 21 / Elixir 1.5. This is a style inconsistency and means the list is partly relying on a deprecated API. All children should use the modern form.

---

**B001-4** — [HIGH] Unreachable second clause of `subject_for_token/2`
File: `lib/api_server/guardian.ex:14`
Description: The first clause of `subject_for_token/2` (line 6) matches on any two arguments (`user, _claims`) and handles the `nil` case internally with an `if` expression. The second clause (`def subject_for_token(_, _)`) therefore can never be reached, because no pattern exists that would fail the first clause. The compiler will emit a warning for this unreachable clause. The intent was likely to use pattern-matched clauses (e.g., `def subject_for_token(nil, _)` and `def subject_for_token(user, _)`), but the implementation chose `if` instead and left the dead clause in place.

---

**B001-5** — [HIGH] Unreachable second clause of `resource_from_claims/1`
File: `lib/api_server/guardian.ex:24`
Description: The first clause of `resource_from_claims/1` (line 18) matches `claims` (any value). The second clause (`def resource_from_claims(_claims)`) can never be reached. The same unreachable-clause warning as B001-4 applies. Additionally, the first clause makes no attempt to handle the case where `claims["sub"]` or `claims["customer"]` is absent — it will crash with a `FunctionClauseError` or raise from `Vx.get_vx_user!/2` rather than returning `{:error, reason}`. The dead fallback clause provides a false sense of safety.

---

**B001-6** — [LOW] Opaque error atom `:reason_for_error` used as error return
File: `lib/api_server/guardian.ex:8,15,25`
Description: All error returns from `subject_for_token/2` and `resource_from_claims/1` use the atom `:reason_for_error`, which is a placeholder from the Guardian library template. This atom carries no actionable information for callers or log consumers attempting to diagnose authentication failures. It should be replaced with specific atoms such as `:user_not_found`, `:missing_claims`, etc.

---

**B001-7** — [LOW] Non-standard indentation (4-space) throughout guardian.ex
File: `lib/api_server/guardian.ex:1-27`
Description: The entire file uses 4-space indentation, while the Elixir community standard (enforced by `mix format`) is 2-space. This is a style inconsistency relative to any other files in the project that follow the standard. While not a runtime defect, it indicates `mix format` has not been run on this file.

---

**B001-8** — [MEDIUM] `ApiServer.FortyNineRepo` lacks `init/2` for runtime configuration
File: `lib/api_server/repo.ex:13-15`
Description: `ApiServer.Repo` overrides `init/2` (line 8–10) to read the database URL from the `DATABASE_URL` environment variable at runtime, enabling twelve-factor / container deployment. `ApiServer.FortyNineRepo` has no such override, so its connection parameters must be baked into compile-time config files. This asymmetry means the two repos have different operational deployment models. If `FortyNineRepo` is intended to connect to a runtime-configured database, it is missing the `init/2` callback. If it is intentionally static, this difference is undocumented and will confuse operators.

---

**B001-9** — [HIGH] Elixir version constraint `~> 1.4` is severely stale
File: `mix.exs:8`
Description: The `elixir: "~> 1.4"` constraint in `project/0` allows any Elixir version from 1.4 upward. Elixir 1.4 was released in January 2017 and reached end-of-life years ago. The `~>` operator with a minor-version operand expands to `>= 1.4.0 and < 2.0.0`, so this does not provide a meaningful lower bound for the features actually used. More critically, several dependencies listed in mix.exs (e.g., `phoenix ~> 1.5.9`, `plug ~> 1.13`) require Elixir 1.7 or later, so the stated minimum is misleading and could allow CI environments to pass with an incompatible Elixir version before hitting a dependency resolution failure.

---

**B001-10** — [LOW] Unbounded version constraint `>= 0.0.0` for `geohax`
File: `mix.exs:57`
Description: `{:geohax, ">= 0.0.0"}` places no upper bound on the version that will be resolved, meaning any future major release with breaking API changes could be pulled in by `mix deps.update`. The lock file pins it to `0.3.0` today, but any `mix deps.update geohax` will accept arbitrarily newer versions. A constraint such as `"~> 0.3"` would be appropriate.

---

**B001-11** — [MEDIUM] `postgrex` present in lock file but absent from `mix.exs` deps
File: `mix.lock:53` / `mix.exs`
Description: `postgrex 0.13.5` is recorded in `mix.lock` but is not declared as a direct or optional dependency in `mix.exs`. It appears as a transitive optional dependency of `ecto` (for PostgreSQL support). Since the project uses MariaDB (`mariaex`), the presence of a locked PostgreSQL driver is unexpected and suggests either a stale lock entry from a prior configuration, or that `postgrex` is being resolved unnecessarily. A stale lock entry bloats the dependency graph and could mask a real version conflict.

---

**B001-12** — [MEDIUM] `geo` present in lock file but absent from `mix.exs` deps
File: `mix.lock:28` / `mix.exs`
Description: `geo 1.5.0` is present in `mix.lock` but is not declared in `mix.exs`. It is pulled in transitively by `topo`. However, `geo` is listed as a runtime (non-optional) transitive dep of `topo`, so it will be included in releases. The issue is that the locked version (`1.5.0`) is constrained to work with `ecto ~> 2.1` (its optional ecto integration), but because it is not declared in `mix.exs`, there is no explicit control over which `geo` version is selected. If `topo` relaxes its `geo` constraint in a future release, `mix deps.update` could pull in an incompatible version silently.

---

**B001-13** — [LOW] `con_cache` locked at `0.14.0` but mix.exs requires `~> 0.13`
File: `mix.exs:58` / `mix.lock:10`
Description: `mix.exs` specifies `{:con_cache, "~> 0.13"}`, which allows versions `>= 0.13.0 and < 1.0.0`. The lock file records `0.14.0`. While `0.14.0` satisfies the range, the mismatch means the declared minimum (`0.13`) is lower than what has actually been tested. If a developer runs `mix deps.get` on a fresh checkout with an older resolver it could theoretically select `0.13.x`. The constraint should be tightened to `"~> 0.14"` to match the lock.

---

**B001-14** — [LOW] `bamboo` locked at `1.5.0` but mix.exs requires `~> 1.2`
File: `mix.exs:60` / `mix.lock:5`
Description: Same class of issue as B001-13. `mix.exs` allows `bamboo >= 1.2.0 and < 2.0.0`; the lock pins `1.5.0`. The lower bound of the constraint (`1.2`) is three minor versions behind the locked version, meaning the constraint is significantly wider than what is actually used or tested. The constraint should be updated to `"~> 1.5"`.

---

**B001-15** — [INFO] `guardian` locked at `1.2.1` but mix.exs requires `~> 1.0`
File: `mix.exs:54` / `mix.lock:31`
Description: `mix.exs` allows `guardian >= 1.0.0 and < 2.0.0`; lock pins `1.2.1`. This is the same class of constraint looseness as B001-13 and B001-14, but guardian's minor releases within 1.x are documented as backwards-compatible, so the practical risk is lower. Noted for completeness; tightening to `"~> 1.2"` would align the constraint with what is tested.

---

**B001-16** — [MEDIUM] `import Supervisor.Spec` inside `start/2` function rather than at module level
File: `lib/api_server/application.ex:7`
Description: Placing `import` statements inside a function body is unconventional in Elixir and reduces readability. The compiler resolves imports at compile time regardless of lexical position in the source, but developers reading the code will not expect to find an `import` directive inside a `def`. This compounds the deprecation issue in B001-2. The import should either be moved to module level (as a step toward modernising the child-specs) or removed entirely once the children are rewritten with the current tuple syntax.

---

## Summary Table

| ID      | Severity | File                              | Line(s) | Short Title                                                    |
|---------|----------|-----------------------------------|---------|----------------------------------------------------------------|
| B001-1  | LOW      | lib/api_server/application.ex     | 24      | Commented-out worker stub in supervisor children               |
| B001-2  | MEDIUM   | lib/api_server/application.ex     | 7       | Deprecated `Supervisor.Spec` used — generates build warnings   |
| B001-3  | MEDIUM   | lib/api_server/application.ex     | 14–25   | Mixed deprecated and modern child-spec styles                  |
| B001-4  | HIGH     | lib/api_server/guardian.ex        | 14      | Unreachable second clause of `subject_for_token/2`             |
| B001-5  | HIGH     | lib/api_server/guardian.ex        | 24      | Unreachable second clause of `resource_from_claims/1`          |
| B001-6  | LOW      | lib/api_server/guardian.ex        | 8,15,25 | Opaque placeholder error atom `:reason_for_error`              |
| B001-7  | LOW      | lib/api_server/guardian.ex        | 1–27    | Non-standard 4-space indentation (should be 2-space)           |
| B001-8  | MEDIUM   | lib/api_server/repo.ex            | 13–15   | `FortyNineRepo` lacks `init/2` for runtime URL configuration   |
| B001-9  | HIGH     | mix.exs                           | 8       | Elixir version constraint `~> 1.4` is severely stale           |
| B001-10 | LOW      | mix.exs                           | 57      | Unbounded `>= 0.0.0` constraint for `geohax`                  |
| B001-11 | MEDIUM   | mix.lock                          | 53      | `postgrex` in lock but not in mix.exs (unexpected dep)         |
| B001-12 | MEDIUM   | mix.lock                          | 28      | `geo` in lock but not in mix.exs (uncontrolled transitive dep) |
| B001-13 | LOW      | mix.exs / mix.lock                | 58/10   | `con_cache` constraint too loose vs. locked version            |
| B001-14 | LOW      | mix.exs / mix.lock                | 60/5    | `bamboo` constraint too loose vs. locked version               |
| B001-15 | INFO     | mix.exs / mix.lock                | 54/31   | `guardian` constraint looser than locked version               |
| B001-16 | MEDIUM   | lib/api_server/application.ex     | 7       | `import` statement placed inside function body                 |
# Pass 4 – B002

**Date:** 2026-02-27
**Audit run:** 2026-02-27-01
**Agent:** B002

**Files reviewed:**
- `lib/api_server/fortynine/calamppositionevents.ex`
- `lib/api_server/fortynine/webservicepositionqueue.ex`

---

## Reading Evidence

### File 1: `lib/api_server/fortynine/calamppositionevents.ex`

**Module name:** `ApiServer.FortyNine.CalampPositionEvents`

**Uses / Imports:**
- `use Ecto.Schema` (line 2)
- `use Bitwise` (line 3)
- `use Timex` (line 4)
- `import Ecto.Changeset` (line 5)

**Schema:** `"calamppositionevents"` (line 7)

**Fields defined (lines 8–88):**
| Line | Field | Type |
|------|-------|------|
| 8 | `:datetimesaved` | `:utc_datetime` |
| 9 | `:gmtdatetime` | `:utc_datetime` |
| 10 | `:timeoffix` | `:utc_datetime` |
| 11 | `:hardwareid` | `:integer` |
| 12 | `:latitude` | `:float` |
| 13 | `:longitude` | `:float` |
| 14 | `:heading` | `:float` |
| 15 | `:speed` | `:float` |
| 16 | `:gpslock` | `:integer` |
| 17 | `:old` | `:integer` |
| 18 | `:ping` | `:integer` |
| 19 | `:motion` | `:integer` |
| 20 | `:speeding` | `:integer` |
| 21 | `:ignition` | `:integer` |
| 22 | `:ignitionstatus` | `:string` |
| 23 | `:rssi` | `:integer` |
| 24 | `:gpsfixquality` | `:integer` |
| 25 | `:eventtype` | `:integer` |
| 26 | `:eventcode` | `:integer` |
| 27 | `:sensor1` | `:integer` |
| 28 | `:sensor2` | `:integer` |
| 29 | `:odometer` | `:integer` |
| 30 | `:distancesincelastevent` | `:integer` |
| 31 | `:wsusername` | `:string` |
| 32 | `:wspassword` | `:string` |
| 33 | `:altitude` | `:integer` |
| 34 | `:error` | `:integer` |
| 35 | `:ioflagstatus` | `:integer` |
| 36 | `:alarmid` | `:integer` |
| 37 | `:errormsg` | `:string` |
| 38 | `:connectionname` | `:string` |
| 39 | `:weight` | `:float` |
| 40 | `:maxheight` | `:float` |
| 41 | `:fuelusage` | `:float` |
| 42 | `:engineonelapsed` | `:integer` |
| 43 | `:totalengineonelapsed` | `:integer` |
| 44 | `:input1elapsed` | `:integer` |
| 45 | `:input1status` | `:string` |
| 46 | `:input1flag` | `:integer` |
| 47 | `:totalinput1elapsed` | `:integer` |
| 48 | `:accelerometerx` | `:float` |
| 49 | `:accelerometery` | `:float` |
| 50 | `:accelerometerz` | `:float` |
| 51 | `:location` | `:string` |
| 52 | `:city` | `:string` |
| 53 | `:state` | `:string` |
| 54 | `:postcode` | `:string` |
| 55 | `:driverid` | `:string` |
| 56 | `:mifaredriverid` | `:string` |
| 57 | `:messageid` | `:integer` |
| 58 | `:originalmsg` | `:binary` |
| 59 | `:prestartchecklist` | `:string` |
| 60 | `:motiontotalelapsed` | `:integer` |
| 61 | `:containerliftcount` | `:integer` |
| 62 | `:appmsgtext` | `:string` |
| 63 | `:pulsecount` | `:integer` |
| 64 | `:totalfuel` | `:integer` |
| 65 | `:vehicleload` | `:integer` |
| 66 | `:rawvehicleload` | `:integer` |
| 67 | `:appmsgtext2` | `:string` |
| 68 | `:batteryvoltage` | `:float` |
| 69 | `:rpm` | `:float` |
| 70 | `:engcoolanttemp` | `:float` |
| 71 | `:engcoolantpressure` | `:float` |
| 72 | `:engcoolantlevelpercent` | `:float` |
| 73 | `:engoiltemp` | `:float` |
| 74 | `:engoilpressure` | `:float` |
| 75 | `:engcrankcasepressure` | `:float` |
| 76 | `:engoillevelpercent` | `:float` |
| 77 | `:engfuellevel1percent` | `:float` |
| 78 | `:engfuellevel2percent` | `:float` |
| 79 | `:engfuelrate` | `:float` |
| 80 | `:engtotalfuelused` | `:float` |
| 81 | `:engtotalfuelidle` | `:float` |
| 82 | `:engtotalhoursidle` | `:float` |
| 83 | `:engtotalhours` | `:float` |
| 84 | `:totalvehiclehours` | `:float` |
| 85 | `:totalptohours` | `:float` |
| 86 | `:engaveragefueleco` | `:float` |
| 87 | `:internalbatteryvoltage` | `:float` |

**Functions defined:**
| Line | Function | Arity |
|------|----------|-------|
| 91 | `changeset/2` | 2 |

**Types / constants / errors defined:** None

---

### File 2: `lib/api_server/fortynine/webservicepositionqueue.ex`

**Module name:** `ApiServer.FortyNine.WebServicePositionQueue`

**Uses / Imports:**
- `use Ecto.Schema` (line 2)
- `use Bitwise` (line 3)
- `use Timex` (line 4)
- `import Ecto.Changeset` (line 5)

**Schema:** `"webservicepositionqueue"` (line 7)

**Fields defined (lines 8–34):**
| Line | Field | Type |
|------|-------|------|
| 8 | `:RECORDID` | `:integer` |
| 9 | `:datetimequeued` | `:utc_datetime` |
| 10 | `:utctimestamp` | `:utc_datetime` |
| 11 | `:HARDWAREID` | `:string` |
| 12 | `:MOBILENAME` | `:string` |
| 13 | `:driverID` | `:string` |
| 14 | `:LATITUDE` | `:float` |
| 15 | `:LONGITUDE` | `:float` |
| 16 | `:HEADING` | `:float` |
| 17 | `:SPEED` | `:float` |
| 18 | `:GPSLOCK` | `:integer` |
| 19 | `:OLD` | `:integer` |
| 20 | `:PING` | `:integer` |
| 21 | `:MOTION` | `:integer` |
| 22 | `:SPEEDING` | `:integer` |
| 23 | `:IGNITION` | `:integer` |
| 24 | `:IGNITIONSTATUS` | `:string` |
| 25 | `:RSSI` | `:integer` |
| 26 | `:SATS` | `:integer` |
| 27 | `:SENSOR1` | `:integer` |
| 28 | `:SENSOR2` | `:integer` |
| 29 | `:WSUSERNAME` | `:string` |
| 30 | `:WSPASSWORD` | `:string` |
| 31 | `:ERROR` | `:integer` |
| 32 | `:ERRORMSG` | `:string` |
| 33 | `:CONNECTIONNAME` | `:string` |

**Functions defined:**
| Line | Function | Arity |
|------|----------|-------|
| 37 | `changeset/2` | 2 |

**Types / constants / errors defined:** None

---

## Findings

---

**B002-1** — [HIGH] Unused `use Bitwise` in both schema modules

File: `lib/api_server/fortynine/calamppositionevents.ex:3`
File: `lib/api_server/fortynine/webservicepositionqueue.ex:3`

Description: Both modules include `use Bitwise` at lines 3, but neither module contains any bitwise operations, operators (`band`, `bor`, `bxor`, `bnot`, `bsl`, `bsr`, `~~~`, `&&&`, `|||`), or any other expression that would require the Bitwise module to be in scope. In Elixir, `use Bitwise` imports all bitwise operators and/or functions into the module namespace. This pollutes the module's namespace with operators that shadow or conflict with potential future local definitions and suppresses no-op import warnings in some compiler versions. It is a build-warning-class issue: the compiler will generate an "unused import" warning for modules that `use` a library purely for its operator side-effects when none of those operators are referenced. This is duplicated identically across both files.

---

**B002-2** — [HIGH] Unused `use Timex` in both schema modules

File: `lib/api_server/fortynine/calamppositionevents.ex:4`
File: `lib/api_server/fortynine/webservicepositionqueue.ex:4`

Description: Both modules include `use Timex` at line 4, but neither module contains any call to Timex functions (e.g., `Timex.now/0`, `Timex.format/2`, `Timex.parse/2`, `Timex.diff/3`, `Timex.shift/2`, or any Timex sigil). `use Timex` injects a substantial set of aliases, imports, and macros into the module. None of this machinery is used; the modules are pure Ecto schema + changeset definitions. This generates unused-import build warnings and unnecessarily increases compile-time dependency surface. The duplication of the same unnecessary dependency across both files suggests copy-paste module setup without review.

---

**B002-3** — [MEDIUM] Inconsistent field naming convention between the two sibling schema modules

File: `lib/api_server/fortynine/calamppositionevents.ex:8–87`
File: `lib/api_server/fortynine/webservicepositionqueue.ex:8–33`

Description: `[REDACTED-AWS-SMTP-PASSWORD]` uses entirely lowercase snake_case atom field names (`:hardwareid`, `:latitude`, `:wspassword`, `:driverid`, etc.). `[REDACTED-AWS-SMTP-PASSWORD]` uses SCREAMING_SNAKE_CASE (`:HARDWAREID`, `:LATITUDE`, `:WSPASSWORD`) for most fields, but uses mixed case for two fields: `:datetimequeued` (lowercase, line 9), `:utctimestamp` (lowercase, line 10), and `:driverID` (camelCase, line 13). This means the two related schema modules — both mapping GPS position data from the same device vendor — follow three different naming styles. Inconsistency within `[REDACTED-AWS-SMTP-PASSWORD]` itself (`:driverID` versus `:HARDWAREID`) is particularly problematic: it makes pattern matching against the struct unreliable and forces callers to know which fields are uppercase and which are not. This is a style inconsistency finding and also a latent bug risk because Elixir atom keys are case-sensitive.

---

**B002-4** — [MEDIUM] Credentials stored as first-class schema fields (leaky abstraction / security concern)

File: `lib/api_server/fortynine/calamppositionevents.ex:31–32`
File: `lib/api_server/fortynine/webservicepositionqueue.ex:29–30`

Description: Both schemas expose `:wsusername` / `:WSUSERNAME` and `:wspassword` / `:WSPASSWORD` as plain persisted schema fields, and the `changeset/2` functions in both modules include these fields in the unrestricted `cast/3` call. Credential fields being part of a general-purpose changeset means they are cast from arbitrary external attrs maps without any special handling, masking, or omission. Confirmed in `tcp_commands.ex` (lines 1220–1221, 1305–1306, 1890–1891): the password `"@trility!"` is hard-coded in the caller and flows through the changeset into the database. While the hard-coding of the credential is a separate concern in `tcp_commands.ex`, the schema design that models credentials as ordinary data fields — fully cast, fully persisted, with no `@doc` warning — is a leaky abstraction: the persistence layer exposes an internal web-service credential as a public struct field accessible to any code that queries the schema.

---

**B002-5** — [LOW] `@doc false` on `changeset/2` is misleading in context

File: `lib/api_server/fortynine/calamppositionevents.ex:90`
File: `lib/api_server/fortynine/webservicepositionqueue.ex:36`

Description: Both modules annotate `changeset/2` with `@doc false`. This attribute suppresses ExDoc documentation generation for the function. However, both `changeset/2` functions are the only public API of their respective modules and are called from `tcp_commands.ex` as the primary insertion path. Marking a module's sole public function as `@doc false` means there is no machine-readable documentation for the function's contract, accepted fields, or required fields (`:hardwareid` / `:HARDWAREID`). The `@doc false` convention in Elixir/Phoenix is intended for genuinely internal callbacks; using it here hides the module's only externally consumed interface. This is a style/maintainability finding.

---

**B002-6** — [LOW] Indentation style inconsistency within schema blocks

File: `lib/api_server/fortynine/calamppositionevents.ex:8–88`
File: `lib/api_server/fortynine/webservicepositionqueue.ex:8–34`

Description: In both files, the `field` declarations inside the `schema` block are indented with 6 spaces (two extra spaces beyond the 4-space indent that Elixir convention uses for block bodies). The standard Elixir formatter uses 2-space indentation increments, so `field` declarations inside a `schema` block should be indented 4 spaces (2 for the `do` block of `defmodule`, 2 more for the `schema` block). Using 6 spaces suggests the files were not formatted with `mix format`. This inconsistency is minor in isolation but indicates these files have never been passed through the project formatter, which may hide other formatting divergences.

---

**B002-7** — [LOW] `changeset/2` casts all fields with no filtering — credential fields included without guard

File: `lib/api_server/fortynine/calamppositionevents.ex:92–94`
File: `lib/api_server/fortynine/webservicepositionqueue.ex:38–40`

Description: The `cast/3` call in both changesets passes every single schema field as castable, including `:wspassword` / `:WSPASSWORD`. There is no use of `validate_required/2` beyond the single hardware-ID field, and no `validate_*` call guards any other field. With 81 fields cast but only 1 validated in `[REDACTED-AWS-SMTP-PASSWORD]`, a struct can be inserted with every field nil or with arbitrary values. This is a structural weakness in the changeset design: `cast/3` is meant to be paired with validation logic proportionate to the data importance. The absence of any validation on fields such as `:latitude`, `:longitude`, or `:gmtdatetime` means silently corrupt records can reach the database. This is a LOW code-quality finding (not CRITICAL because the data originates from an authenticated internal TCP pipeline, not a public API endpoint).

---

## Summary Table

| ID | Severity | File(s) | Short Title |
|----|----------|---------|-------------|
| B002-1 | HIGH | calamppositionevents.ex:3, webservicepositionqueue.ex:3 | Unused `use Bitwise` — build warning / namespace pollution |
| B002-2 | HIGH | calamppositionevents.ex:4, webservicepositionqueue.ex:4 | Unused `use Timex` — build warning / unnecessary dependency |
| B002-3 | MEDIUM | calamppositionevents.ex:8–87, webservicepositionqueue.ex:8–33 | Inconsistent field naming convention between sibling schemas |
| B002-4 | MEDIUM | calamppositionevents.ex:31–32, webservicepositionqueue.ex:29–30 | Credentials as first-class castable schema fields (leaky abstraction) |
| B002-5 | LOW | calamppositionevents.ex:90, webservicepositionqueue.ex:36 | `@doc false` on module's sole public function |
| B002-6 | LOW | calamppositionevents.ex:8–88, webservicepositionqueue.ex:8–34 | Non-standard indentation — files not formatted with `mix format` |
| B002-7 | LOW | calamppositionevents.ex:92–94, webservicepositionqueue.ex:38–40 | `changeset/2` casts all fields with minimal validation |

**Total findings: 7** (2 HIGH, 2 MEDIUM, 3 LOW)
# Pass 4 – B003

Date: 2026-02-27
Audit run: 2026-02-27-01
Files reviewed:
- lib/api_server/operators/file.ex
- lib/api_server/operators/operators.ex

---

## Reading Evidence

### lib/api_server/operators/file.ex

**Module:** `ApiServer.Operators.File`

**Schema:** `"files"` (Ecto schema)

**Fields defined in schema:**
- `:custcode` — `:string` (line 7)
- `:esn` — `:string` (line 8)
- `timestamps()` (line 10)

**Functions:**
| Name | Line | Visibility |
|------|------|------------|
| `changeset/2` | 14 | public (`@doc false`) |

**Types / errors / constants defined:** None

---

### lib/api_server/operators/operators.ex

**Module:** `ApiServer.Operators`

**Imports:** `Ecto.Query` with `warn: false` (line 5)

**Aliases:**
- `ApiServer.Repo` (line 7)
- `ApiServer.Operators.File` (line 8)

**Functions:**
| Name | Line | Visibility |
|------|------|------------|
| `list_files/0` | 19 | public |
| `get_file!/1` | 37 | public |
| `create_file/1` (default arg `%{}`) | 51 | public |
| `update_file/2` | 69 | public |
| `delete_file/1` | 87 | public |
| `change_file/1` | 100 | public |

**Types / errors / constants defined:** None

---

## Findings

**B003-1** — [HIGH] Entire Operators context is dead code — none of its functions are called anywhere

File: lib/api_server/operators/operators.ex:19–102

Description: The six public functions `list_files/0`, `get_file!/1`, `create_file/1`, `update_file/2`, `delete_file/1`, and `change_file/1` are never called by any module in the codebase. A project-wide search across all `.ex` and `.exs` files finds zero call sites. The `FileController` (lib/api_server_web/controllers/file_controller.ex) aliases `ApiServer.Operators` (line 4) and `ApiServer.Operators.File` (line 5) but never calls a single function from `ApiServer.Operators`. The entire context is therefore dead code. Dead context modules carry maintenance cost and create confusion about the data access path actually in use.

---

**B003-2** — [HIGH] `ApiServer.Operators.File` schema is dead — schema fields do not match actual controller usage

File: lib/api_server/operators/file.ex:6–11

Description: The `ApiServer.Operators.File` schema defines two fields (`:custcode` and `:esn`) and maps to the `"files"` database table. However the `FileController` never loads `ApiServer.Operators.File` structs through the `ApiServer.Operators` context; it builds ad-hoc maps with keys `:size`, `:hardwareid`, and `:num_fobs` and renders them directly. The schema fields (`:custcode`, `:esn`) do not appear anywhere outside the schema and changeset definitions. The schema represents a table that is not used by any runtime path, making it dead schema infrastructure.

---

**B003-3** — [MEDIUM] Unused alias `ApiServer.Operators` imported in `warn: false` context — `Ecto.Query` import may be entirely unused

File: lib/api_server/operators/operators.ex:5

Description: `import Ecto.Query, warn: false` is present to suppress the "unused import" compiler warning. The `warn: false` flag is a signal that the import was known to be partially or wholly unused at the time of writing. Because no query-building beyond `Repo.all/1` and `Repo.get!/2` is performed in the module, none of the query macros from `Ecto.Query` (`from`, `where`, `select`, etc.) are used. The `warn: false` option suppresses the compiler warning that would otherwise flag this. Suppressing warnings hides information that is useful during maintenance.

---

**B003-4** — [MEDIUM] Leaky abstraction — `FileController` directly aliases the schema struct bypassing the context

File: lib/api_server_web/controllers/file_controller.ex:5

Description: `FileController` imports `alias ApiServer.Operators.File` (the Ecto schema struct) directly alongside `alias ApiServer.Operators` (the context). Phoenix conventions place all database interaction behind the context module; controllers should only reference the schema struct type for pattern-matching, not for direct use. In this case the alias is completely unused in `FileController` — neither `File` nor any `Operators.*` function is called — confirming the controller bypasses the context entirely. This constitutes a leaky abstraction: the boundary between the web layer and the data layer is not enforced.

---

**B003-5** — [LOW] Stale generated boilerplate — `changeset/2` is annotated `@doc false` on a function that is itself dead

File: lib/api_server/operators/file.ex:13–18

Description: `@doc false` is the Phoenix generator convention for marking changesets as internal-only. The annotation is correct in intent, but the function itself is dead (see B003-1 and B003-2): `File.changeset/2` is only called from `ApiServer.Operators` functions which are themselves never called. The presence of `@doc false` combined with dead code indicates the entire file is unmodified generator output that was never integrated into real application logic.

---

**B003-6** — [LOW] Blank line inconsistency inside schema block

File: lib/api_server/operators/file.ex:4–5

Description: Lines 4 and 5 are both blank, producing a double blank line between the `import` statement and the `schema` block. Elixir style conventions (and the standard formatter) use single blank lines between top-level constructs. This is a minor formatting inconsistency, most likely the result of the file never having been passed through `mix format`.

---

## Summary Table

| ID | Severity | Title | File | Line(s) |
|----|----------|-------|------|---------|
| B003-1 | HIGH | Entire Operators context is dead — no call sites exist | lib/api_server/operators/operators.ex | 19–102 |
| B003-2 | HIGH | `ApiServer.Operators.File` schema fields are dead — not used at runtime | lib/api_server/operators/file.ex | 6–11 |
| B003-3 | MEDIUM | `Ecto.Query` imported with `warn: false` to suppress unused-import warning | lib/api_server/operators/operators.ex | 5 |
| B003-4 | MEDIUM | Controller aliases schema struct directly, bypassing context (leaky abstraction) | lib/api_server_web/controllers/file_controller.ex | 5 |
| B003-5 | LOW | `changeset/2` annotated `@doc false` but is itself dead code | lib/api_server/operators/file.ex | 13–18 |
| B003-6 | LOW | Double blank line — file not run through `mix format` | lib/api_server/operators/file.ex | 4–5 |
# Pass 4 – B004

**Date:** 2026-02-27
**Audit run:** 2026-02-27-01
**Files reviewed:**
- `lib/api_server/tcp/tcp.ex` (151 lines)
- `lib/api_server/tcp/tcp_commands.ex` (1,987 lines)

---

## Reading Evidence

### `lib/api_server/tcp/tcp.ex`

**Module:** `ApiServer.TCP`

**Functions:**
| Name | Line | Visibility |
|------|------|------------|
| `accept/1` | 23 | public |
| `loop_acceptor/1` | 32 | private |
| `serve/2` | 48 | private |
| `read_line/3` | 90 | private |
| `write_line/2` (text variant) | 135 | private |
| `write_line/2` (:error, :unknown_command variant) | 139 | private |
| `write_line/2` (:error, :closed variant) | 143 | private |
| `write_line/2` (:error, error variant) | 147 | private |

**Aliases declared:**
- `Ecto.Query` (import, warn: false)
- `ApiServer.Repo`
- `ApiServer.Vx.VXUser`
- `ApiServer.Vx.VXThingEvent`
- `ApiServer.Vx.VXThingEventOmega`
- `ApiServer.Vx.VXThingEventOmegaTires`
- `ApiServer.Vx.VXFleetAssociation`
- `ApiServer.Vx.VXRestriction`
- `ApiServer.Vx.Geofence`
- `ApiServer.Vx.VXThing`
- `ApiServer.Vx.VXAblRecord`
- `ApiServer.Vx.VXRayvenMessageLog`

**Constants/Magic values:**
- `5000` — TCP receive timeout (ms), line 91
- Sync bytes `<<2>>, <<85>>` — protocol constants, lines 104–123
- Message type bytes `<<0>>, <<5>>, <<38>>, <<4>>` — protocol opcodes
- `<<0>>`, `<<1>>` — sentinel msg values, lines 71–74

---

### `lib/api_server/tcp/tcp_commands.ex`

**Module:** `ApiServer.TCP.Commands`

**Functions:**
| Name | Line | Visibility |
|------|------|------------|
| `parse_hello_message/1` | 9 | public |
| `parse_data_message/3` | 35 | public |
| `parse_debug_record/3` | 120 | public |
| `parse_data_record/3` | 158 | public |
| `parse_debug_field/1` | 1325 | public |
| `parse_gps_field/1` | 1331 | public |
| `parse_digital_field/1` | 1385 | public |
| `parse_analog_field/1` | 1454 | public |
| `parse_analog32_field/1` | 1470 | public |
| `parse_trip_field/1` | 1541 | public |
| `parse_total_field/1` | 1556 | public |
| `parse_driverid_field/1` | 1571 | public |
| `parse_commit_message/2` | 1673 | public |
| `parse_iridium/2` | 1679 | public |
| `parse/2` | 1903 | public |
| `run/1` (head declaration) | 1959 | public |
| `run/1` ({:send, "hello", params}) | 1961 | public |
| `run/1` ({:send, "commit", params}) | 1966 | public |
| `run/1` ({:processed, "data", params}) | 1976 | public |
| `run/1` ({:close, "socket", params}) | 1982 | public |

**Aliases declared:**
- `ApiServer.FortyNineRepo`
- `ApiServer.FortyNine.CalampPositionEvents`
- `ApiServer.FortyNine.WebServicePositionQueue`
- `ApiServer.Vx.DeviceDatabaseLookup`
- `ApiServerWeb.UtilityController`

**Constants/Magic values (selected):**
- `1_356_998_400` — Unix timestamp for 2013-01-01 (epoch offset), lines 709, 1340, 1701
- `10_000_000` — GPS coordinate divisor (1e-7 degrees), lines 1350, 1355, 1708, 1712
- `27.778` — m/s to km/h divisor, lines 994, 1770
- `0.621371` — km/h to mph conversion, lines 1216, 1301, 1886
- `462_743` — hardcoded device hardware_id in `parse_iridium/2`, line 1756
- `"TRILITY"` / `"trility"` — hardcoded customer code and credentials, lines 1787, 1810, 1220, 1305, 1890
- `"@trility!"` — hardcoded password, lines 1221, 1306, 1891
- `"SVR49"` — hardcoded connection name, lines 1222, 1307, 1892
- `"1234"` — hardcoded MOBILENAME, lines 1219, 1304, 1889
- `"trackingsolutions"` — hardcoded DB schema prefix, lines 1188, 1228, 1273, 1313, 1858, 1898
- `255` — default/unmapped event_code sentinel, lines 89, 882
- `26` — Wiegand bit size, line 1614

---

## Findings

---

**B004-1** — [HIGH] Hardcoded credentials in source code
File: `lib/api_server/tcp/tcp_commands.ex:1221`, `1306`, `1891`
Description: The string `"@trility!"` is used as the value for `WSPASSWORD` in three separate places (lines 1221, 1306, and 1891) and is embedded directly in Elixir source. Username `"trility"` appears alongside it. These credentials authenticate an outbound web service queue insertion. Hardcoding passwords in source defeats secret rotation, exposes credentials in version control history, and violates least-privilege practices. They should be moved to application configuration (e.g., `config/runtime.exs` read from environment variables).

---

**B004-2** — [HIGH] Hardcoded hardware ID and customer code in `parse_iridium/2`
File: `lib/api_server/tcp/tcp_commands.ex:1756`, `1787`, `1810`
Description: `parse_iridium/2` unconditionally assigns `hardware_id = 462_743` (line 1756) and `customer = "vx_trility"` (line 1810), and hard-codes `custcode: "TRILITY"` (line 1787). The function signature accepts `params` but never reads the device identity from it. This means any Iridium packet, regardless of its origin device, is attributed to device 462,743. This is a data-integrity defect disguised as a code-quality issue and is severe enough to warrant HIGH.

---

**B004-3** — [HIGH] Massively duplicated field-parsing logic — no loop / recursion used
File: `lib/api_server/tcp/tcp_commands.ex:158`—`1323`
Description: `parse_data_record/3` manually unrolls field parsing seven times (field one through field seven) with deeply-nested `case` blocks that are structurally identical for each field slot. The same `{actual_field_length, field_data}` pattern-match block for length-prefixed TLV fields appears at least 14 times. The same field-type dispatch (GPS=0, trip=26, total=27, driverid=3, analog32=7) is repeated identically for every slot. This makes the function ~1,160 lines long with nesting that reaches 20+ levels. Any protocol change must be applied in 7 places simultaneously. A recursive TLV loop was clearly the intended design (the function `parse_data_message/3` already uses recursion for multi-record payloads). The repetition is a maintenance and correctness hazard of the highest order.

---

**B004-4** — [MEDIUM] Commented-out code block — `parse_analog_field` references
File: `lib/api_server/tcp/tcp_commands.ex:294–295`, `321–322`, `371–372`, `398–399`, `453–454`, `480–481`, `543–544`, `690–694`
Description: Multiple consecutive blocks of commented-out `case` clauses for field IDs 2 (digital) and 6 (analog) appear throughout `parse_data_record/3`. Representative examples:
```elixir
# 2 ->
#   parse_digital_field(field_four_data)
# 6 ->
# field_four_processed
```
These blocks appear at least 8 times across the function. The pattern suggests that digital (field type 2) and analog (field type 6) parsing was intentionally removed but not deleted. Commented-out code should be removed; if the feature is planned, a TODO or ticket reference is the appropriate placeholder.

---

**B004-5** — [MEDIUM] Commented-out code block — large block in `parse_analog32_field/1`
File: `lib/api_server/tcp/tcp_commands.ex:1494`—`1521`
Description: Twenty-eight lines of commented-out code remain in `parse_analog32_field/1` (lines 1494–1521). This was a prior implementation of the byte-reversal logic that was refactored into the current `Enum.map` approach, plus additional `IO.puts` debug calls. The dead code makes the function harder to read and obscures the current algorithm.

---

**B004-6** — [MEDIUM] Commented-out code block — commit fail message in `run/1`
File: `lib/api_server/tcp/tcp_commands.ex:1967`—`1968`
Description:
```elixir
# Fail Message
# msg = <<2, 85, 6, 1, 0, 0>>
```
The fail response binary is commented out directly above the success response. This is dead code in a critical control-flow function. It should be removed (or kept as a named constant with documentation, not a comment).

---

**B004-7** — [MEDIUM] Duplicate `{event_code, event_type}` mapping — identical case blocks in two places
File: `lib/api_server/tcp/tcp_commands.ex:51`—`90` and `844`—`883`
Description: The `log_reason` → `{event_code, event_type}` mapping (Start=1→{5,16}, End=2→{5,32}, Elapsed=3→{0,3}, Heartbeat=11→{9,0}, DriverID=17→{5,64}, LowBattery=16→{5,128}, 23→{5,23}) is spelled out identically in `parse_data_message/3` (lines 51–90) and again in the `Enum.each` closure inside `parse_data_record/3` (lines 844–883). The result from the first mapping is never used (the variable `{event_code, event_type}` bound at line 51 is shadowed at line 844). This is both redundant code and a latent bug — any update to the table in one place will silently diverge from the other.

---

**B004-8** — [MEDIUM] Variable bound but result discarded — `update_me` in `loop_acceptor/1`
File: `lib/api_server/tcp/tcp.ex:37`—`42`
Description:
```elixir
update_me = case :gen_tcp.controlling_process(client, pid) do
  {:ok} ->
    "[g62] [g62_tcp] [loop_acceptor] [ok]"
  _ ->
    "[something_else]"
end
```
`update_me` is assigned but never read. The `{:ok}` pattern is also wrong for `:gen_tcp.controlling_process/2` — the success tuple is `:ok` (an atom, not a 1-tuple). This means the success branch is unreachable; only the `_` clause will ever execute. This is both a dead binding and an unreachable clause. The Elixir compiler will warn about the unused variable; it should be prefixed `_update_me` or removed entirely, and the controlling-process error should be handled.

---

**B004-9** — [MEDIUM] `recbuf` bound but never used in `accept/1`
File: `lib/api_server/tcp/tcp.ex:27`
Description:
```elixir
recbuf = :inet.getopts(socket, [:recbuf])
```
The result of `:inet.getopts/2` is assigned to `recbuf` and never referenced again. This will produce a compiler warning for an unused variable. The call appears to have been exploratory/diagnostic and was left in. Either the value should be logged/used, or the line should be removed.

---

**B004-10** — [MEDIUM] `result` variable in `serve/2` — write path result discarded
File: `lib/api_server/tcp/tcp.ex:70`—`83`
Description: Inside `serve/2`, the outer `result` variable is bound to the `case msg do` block but never used. Within that block, `message_result` (line 78) is also assigned the return of `write_line/2` but never referenced. The `{:error, reason}` arm at line 81 also binds `reason` but discards it by returning `:error` without logging. Silently discarding write errors means failed socket writes are undetectable.

---

**B004-11** — [MEDIUM] `summary_update` bound but never used — two occurrences
File: `lib/api_server/tcp/tcp_commands.ex:1135`—`1139` and `1829`—`1831`
Description:
```elixir
summary_update =
  ApiServerWeb.VXThingController.update_thing_cached_fields(hardware_id, customer)
```
This assignment appears in `parse_data_record/3` (line 1135) and `parse_iridium/2` (line 1830). The return value is never used. The compiler will emit an unused-variable warning. The variable should be dropped (the side-effectful call kept) or replaced with `_summary_update`.

---

**B004-12** — [MEDIUM] `result` bound but never used — three occurrences
File: `lib/api_server/tcp/tcp_commands.ex:1225`, `1310`, `1895`
Description:
```elixir
result =
  %WebServicePositionQueue{}
  |> WebServicePositionQueue.changeset(fortynine_queued_event)
  |> FortyNineRepo.insert(prefix: "trackingsolutions")
```
This pattern appears three times. The `{:ok, _}` / `{:error, _}` result of the DB insert is silently discarded. Insert failures are undetectable. The variable name `result` (without underscore prefix) will also cause a compiler warning.

---

**B004-13** — [MEDIUM] `IO.puts/1` debug calls left in production path — multiple occurrences
File: `lib/api_server/tcp/tcp_commands.ex` — lines 25, 304, 381, 463, 553, 607, 640, 674, 769, 819, 1492, 1666`, and `lib/api_server/tcp/tcp.ex` (indirectly via `IO.inspect` at line 1130)
Description: Numerous `IO.puts` and `IO.inspect` calls write directly to stdout in production code paths. Notable examples:
- Line 25: `IO.puts("Could not find device: ...")` in `parse_hello_message/1`
- Lines 304, 381, 463, 553: per-field `IO.puts` for test unit 625,425 — fires on every data record for that device
- Lines 769–821: `IO.puts` for test unit 625,425 and a 37-device list (`yabby3` devices)
- Line 1492: `IO.puts("Analog values: ...")` in `parse_analog32_field/1` — fires for **every** data record that has an analog32 field
- Line 1666: `IO.puts` in `parse_driverid_field/1` — fires for every record containing a driver ID
These calls will flood stdout under normal load and have significant performance impact. They should be replaced with `Logger.debug/1` (which can be compiled out) and guarded appropriately.

---

**B004-14** — [MEDIUM] `parse_digital_field/1` is never called — dead function
File: `lib/api_server/tcp/tcp_commands.ex:1385`
Description: `parse_digital_field/1` is defined at line 1385 and is a complete, non-trivial implementation. Every call site where it was previously used has been commented out (field type 2 dispatch blocks throughout `parse_data_record/3`). The function is never invoked at runtime. It is either dead code to be deleted or an in-progress feature that was abandoned. Leaving it in place misleads maintainers.

---

**B004-15** — [MEDIUM] `parse_analog_field/1` is never called — dead function
File: `lib/api_server/tcp/tcp_commands.ex:1454`
Description: `parse_analog_field/1` is defined at line 1454 but all dispatch paths that would invoke it (field type 6) are commented out throughout `parse_data_record/3`. Like `parse_digital_field/1`, it is dead code.

---

**B004-16** — [MEDIUM] `parse_iridium/2` is never called from within the module — possible dead entry point
File: `lib/api_server/tcp/tcp_commands.ex:1679`
Description: `parse_iridium/2` is not called from `parse/2`, `run/1`, or any other function within this module. It is also not reachable through `tcp.ex`. Unless an external caller invokes it directly, it is dead code. Additionally, the function hard-codes `hardware_id = 462_743` (finding B004-2), making it a data-integrity hazard if it were ever activated.

---

**B004-17** — [MEDIUM] `{event_code, event_type}` first binding is dead — variable immediately shadowed
File: `lib/api_server/tcp/tcp_commands.ex:51`—`90`
Description: In `parse_data_message/3`, `{event_code, event_type}` is bound at line 51 from a `log_reason` case. However, both variables are completely shadowed by a second identical binding inside the `Enum.each` closure at line 844 (within `parse_data_record/3` which is called at line 98). The first binding's values are never read. The Elixir compiler cannot warn about this because the variables are used in the second binding, but the first computation is pure waste.

---

**B004-18** — [MEDIUM] `mapped_record` assigned but never used in `parse_data_message/3`
File: `lib/api_server/tcp/tcp_commands.ex:94`—`103`
Description:
```elixir
mapped_record =
  case log_reason do
    21 ->
      parse_debug_record(record, record_length, params)
      []
    _ ->
      parse_data_record(record, record_length, params)
  end
```
`mapped_record` is bound but never referenced again in the function. The side effects of `parse_data_record/3` are what matter (DB inserts), but the return value is silently dropped. The compiler will warn about the unused variable.

---

**B004-19** — [MEDIUM] Duplicate second `{event_code, event_type}` clause for hardware-ID override applies to a stale list
File: `lib/api_server/tcp/tcp_commands.ex:885`—`927`
Description: After the initial `{event_code, event_type}` mapping at lines 844–883, a second override block at lines 885–927 adjusts the value for a specific list of hardware IDs (`trility` devices, 14 IDs). The same 14 IDs also appear at line 1143–1160 for the FortyNine insert. These hardcoded device lists are a maintenance hazard — any new device requires edits in multiple places with no compile-time enforcement.

---

**B004-20** — [MEDIUM] Duplicate FortyNine insert blocks for integer vs. string serial number lists
File: `lib/api_server/tcp/tcp_commands.ex:1143`—`1229` and `1230`—`1317`
Description: The `Enum.each` closure in `parse_data_record/3` contains two consecutive `case serial_number` branches. The first (lines 1143–1229) matches on **integer** serial numbers (e.g., `461_858`); the second (lines 1230–1317) matches on **string** serial numbers (e.g., `"461858"`). The bodies are nearly identical. Because `serial_number` is always an integer (decoded via `<<serial::little-signed-integer-size(32)>>`), the string branch at line 1230 is **unreachable dead code**. Any Trility device event will always be handled by the integer branch; the string branch never fires.

---

**B004-21** — [LOW] Comment-annotated but unmapped log reason codes left in-line as comments
File: `lib/api_server/tcp/tcp_commands.ex:80`—`86` and `873`—`879`
Description: Comment blocks listing protocol codes that are intentionally unmapped:
```elixir
# 23 -> Accident
# 24 -> Accident data
# 32 -> Trip restart
# 36 -> Recovery mode on
# 37 -> Recovery mode off
# 46 -> High G event
# 48 -> Duress
```
These appear twice (lines 80–86 and 873–879). They are documentation embedded as inline comments rather than in the module's `@moduledoc` or a spec document. While individually minor, combining them with the duplicate code amplifies the maintenance burden.

---

**B004-22** — [LOW] `something` and deeply-nested throwaway variable names throughout `parse_data_record/3`
File: `lib/api_server/tcp/tcp_commands.ex` — multiple lines
Description: Variables named `something`, `something_again`, `something_again_again`, `something_again_again_again`, `something_again_again_again_again` are used as intermediate bindings inside the deeply nested field-parsing logic. These names convey no intent and are a style violation. The Elixir convention is to use descriptive names or `_` for discarded values.

---

**B004-23** — [LOW] Module-level comment acknowledging unused aliases
File: `lib/api_server/tcp/tcp.ex:6`—`7`
Description:
```elixir
# Clean these up after we know which ones we use
import Ecto.Query, warn: false
alias ApiServer.Repo
```
The comment explicitly acknowledges that the imports and aliases may not all be used, and suppresses the `warn: false` compiler warning for the Ecto import. The aliases `VXUser`, `VXThingEvent`, `VXThingEventOmega`, `[REDACTED-AWS-SMTP-PASSWORD]`, `VXFleetAssociation`, `VXRestriction`, `Geofence`, `VXThing`, `VXAblRecord`, `VXRayvenMessageLog`, and `Repo` are all declared in `tcp.ex` but none are referenced anywhere in the file. They will produce compiler warnings (the Ecto import has its warning suppressed but the others will not). The suppression of the Ecto import warning combined with the comment is an acknowledged but unresolved cleanup item.

---

**B004-24** — [LOW] `[REDACTED-AWS-SMTP-PASSWORD]` alias declared but never used
File: `lib/api_server/tcp/tcp_commands.ex:6`
Description: `alias ApiServer.Vx.DeviceDatabaseLookup` is declared at line 6 but the alias is never referenced anywhere in the file. The compiler will emit an unused-alias warning.

---

**B004-25** — [LOW] Magic number `5000` for TCP receive timeout not named
File: `lib/api_server/tcp/tcp.ex:91`
Description:
```elixir
result = :gen_tcp.recv(socket, 0, 5000)
```
The value `5000` (milliseconds) has no named constant or module attribute. If the timeout needs adjustment, it must be found by reading the code. It should be defined as `@recv_timeout_ms 5000` at the module level.

---

**B004-26** — [LOW] Magic number `1_356_998_400` used three times without explanation
File: `lib/api_server/tcp/tcp_commands.ex:709`, `1340`, `1701`
Description: The constant `1_356_998_400` (Unix timestamp for 2013-01-01 00:00:00 UTC, the device protocol's epoch base) is repeated three times without a named module attribute. A single `@device_epoch_offset 1_356_998_400` with a doc comment would make the intent clear and prevent inconsistency.

---

**B004-27** — [LOW] `{:ok}` pattern match on `:gen_tcp.controlling_process/2` is incorrect
File: `lib/api_server/tcp/tcp.ex:38`
Description:
```elixir
update_me = case :gen_tcp.controlling_process(client, pid) do
  {:ok} ->
    ...
```
`:gen_tcp.controlling_process/2` returns the atom `:ok` on success, not the one-element tuple `{:ok}`. The success branch is therefore unreachable — all outcomes (including genuine success) fall through to the wildcard. This is a silent logic error; errors are not reported and the "ok" diagnostic string is never produced.

---

**B004-28** — [LOW] `parse_commit_message/2` is a one-line pass-through with no logic
File: `lib/api_server/tcp/tcp_commands.ex:1673`—`1677`
Description:
```elixir
def parse_commit_message(remainder, params) do
  send_commit_response = {:ok, {:send, "commit", params}}
  send_commit_response
end
```
The function ignores `remainder` entirely and always returns the same value regardless of input. It exists only to provide a name to a constant tuple. This could be an anonymous inline expression in `parse/2` (line 1941), but the use of a named function is acceptable if more logic is planned. The unnecessary intermediate variable `send_commit_response` is a minor style issue.

---

**B004-29** — [LOW] `IO.puts` used in production code for device-not-found error in `parse_hello_message/1`
File: `lib/api_server/tcp/tcp_commands.ex:25`
Description:
```elixir
IO.puts("Could not find device: #{inspect(serial)}")
```
A device-not-found condition is operationally significant and should be logged at `Logger.warn` or `Logger.error` level, not `IO.puts`. `IO.puts` bypasses the application's logging infrastructure (timestamps, log level filtering, log aggregation).

---

**B004-30** — [LOW] Inconsistent `something` variable used as the final return of `read_line/3`
File: `lib/api_server/tcp/tcp.ex:93`, `132`
Description: In `read_line/3`, a variable named `something` is bound to the full `case result do` block and then returned as the last expression. No transformation occurs between the assignment and the return. This pattern adds indirection without value and departs from the idiomatic Elixir style of letting a `case` block be the function's return expression directly.

---

## Summary Table

| ID | Severity | Title | File |
|----|----------|-------|------|
| B004-1 | HIGH | Hardcoded credentials (password) in source | tcp_commands.ex:1221,1306,1891 |
| B004-2 | HIGH | Hardcoded hardware ID and customer in `parse_iridium/2` | tcp_commands.ex:1756,1787,1810 |
| B004-3 | HIGH | Massively duplicated TLV field-parsing — no loop/recursion | tcp_commands.ex:158–1323 |
| B004-4 | MEDIUM | Commented-out code — field type 2/6 dispatch blocks (8+ occurrences) | tcp_commands.ex:294,321,371,398,453,480,543,690 |
| B004-5 | MEDIUM | Commented-out code — large block in `parse_analog32_field/1` | tcp_commands.ex:1494–1521 |
| B004-6 | MEDIUM | Commented-out code — commit fail message binary | tcp_commands.ex:1967–1968 |
| B004-7 | MEDIUM | Duplicate `log_reason` → event_code mapping in two places | tcp_commands.ex:51–90, 844–883 |
| B004-8 | MEDIUM | `update_me` bound but never used; `{:ok}` pattern is wrong | tcp.ex:37–42 |
| B004-9 | MEDIUM | `recbuf` bound but never used in `accept/1` | tcp.ex:27 |
| B004-10 | MEDIUM | `result`/`message_result` discarded; write errors silently ignored | tcp.ex:70–83 |
| B004-11 | MEDIUM | `summary_update` bound but never used (2 occurrences) | tcp_commands.ex:1135,1830 |
| B004-12 | MEDIUM | `result` bound but never used for DB insert (3 occurrences) | tcp_commands.ex:1225,1310,1895 |
| B004-13 | MEDIUM | `IO.puts`/`IO.inspect` debug calls left in production paths | tcp_commands.ex:25,304,381,463,553,607,640,674,769,819,1492,1666 |
| B004-14 | MEDIUM | `parse_digital_field/1` is dead — never called | tcp_commands.ex:1385 |
| B004-15 | MEDIUM | `parse_analog_field/1` is dead — never called | tcp_commands.ex:1454 |
| B004-16 | MEDIUM | `parse_iridium/2` unreachable from any call site | tcp_commands.ex:1679 |
| B004-17 | MEDIUM | First `{event_code, event_type}` binding immediately shadowed — dead computation | tcp_commands.ex:51–90 |
| B004-18 | MEDIUM | `mapped_record` assigned but never used | tcp_commands.ex:94–103 |
| B004-19 | MEDIUM | Hardcoded device lists duplicated in multiple case branches | tcp_commands.ex:885–927,1143–1160 |
| B004-20 | MEDIUM | String-serial-number FortyNine insert branch is unreachable dead code | tcp_commands.ex:1230–1317 |
| B004-21 | LOW | Unmapped log reason codes documented only as inline comments (duplicated) | tcp_commands.ex:80–86,873–879 |
| B004-22 | LOW | Throwaway variable names (`something`, `something_again`, etc.) | tcp_commands.ex (multiple) |
| B004-23 | LOW | Acknowledged but unresolved unused aliases in `tcp.ex` | tcp.ex:6–18 |
| B004-24 | LOW | `[REDACTED-AWS-SMTP-PASSWORD]` alias declared but never used | tcp_commands.ex:6 |
| B004-25 | LOW | Magic number `5000` (recv timeout) not named | tcp.ex:91 |
| B004-26 | LOW | Magic number `1_356_998_400` (epoch offset) used 3 times, not named | tcp_commands.ex:709,1340,1701 |
| B004-27 | LOW | Incorrect `{:ok}` pattern for `:gen_tcp.controlling_process/2` | tcp.ex:38 |
| B004-28 | LOW | `parse_commit_message/2` is a trivial pass-through with an unnecessary intermediate variable | tcp_commands.ex:1673–1677 |
| B004-29 | LOW | `IO.puts` used for operationally significant device-not-found error | tcp_commands.ex:25 |
| B004-30 | LOW | Unnecessary `something` variable as final return in `read_line/3` | tcp.ex:93,132 |

**Totals:** 3 HIGH, 17 MEDIUM, 10 LOW
# Pass 4 – B005

**Date:** 2026-02-27
**Audit run:** 2026-02-27-01

**Files reviewed:**
- `lib/api_server/vx/device_database_lookup.ex`
- `lib/api_server/vx/email.ex`
- `lib/api_server/vx/equipment.ex`
- `lib/api_server/vx/equipment_assignment.ex`

---

## Reading Evidence

### 1. `lib/api_server/vx/device_database_lookup.ex`

**Module:** `ApiServer.Vx.DeviceDatabaseLookup`

**Behaviours/macros used:**
- `use Ecto.Schema`
- `import Ecto.Changeset`

**Schema:**
- Table: `"DeviceDatabaseLookup"`
- Primary key: `@primary_key {:ID, :id, autogenerate: true}` (line 5)
- Fields: `:hardwareid` (source `:hardwareID`), `:customer` (source `:databaseName`), `:custcode` (source `:CustCode`), `:iccid` (source `:ICCID`)

**Functions:**
| Name | Line |
|------|------|
| `changeset/2` | 13 |

**Types/constants defined:** none

---

### 2. `lib/api_server/vx/email.ex`

**Module:** `ApiServer.Email`
_(Note: file lives under `vx/` but module is NOT namespaced under `ApiServer.Vx`)_

**Behaviours/macros used:**
- `use Bamboo.Phoenix, view: ApiServer.EmailView`

**Functions:**
| Name | Line |
|------|------|
| `send_notification_email/3` | 4 |
| `send_test_email/3` | 14 |
| `send_enter_email/4` | 103 |
| `send_missing_serial_email/4` | 167 |
| `send_digital_matter_email/4` | 215 |
| `send_slow_email/4` | 262 |
| `send_exit_email/4` | 303 |

**Types/constants defined:** none
**Commented-out code blocks:** lines 105–114, 119, 172, 220, 267, 307 (`# |> text_body(...)` and a large data map comment)

---

### 3. `lib/api_server/vx/equipment.ex`

**Module:** `ApiServer.Vx.Equipment`

**Behaviours/macros used:**
- `use Ecto.Schema`
- `import Ecto.Changeset`
- `alias ApiServer.Vx`

**Schema:**
- Table: `"equipment"`
- Primary key: `@primary_key {:ID, :id, autogenerate: true}` (line 7)
- Fields: `:id` (integer, source `:id`), `:name`, `:make`, `:model`, `:serial_number`, `:class`, `:type`, `:created`

**Functions:**
| Name | Line |
|------|------|
| `changeset/2` | 20 |

**Types/constants defined:** none

---

### 4. `lib/api_server/vx/equipment_assignment.ex`

**Module:** `ApiServer.Vx.EquipmentAssignment`

**Behaviours/macros used:**
- `use Ecto.Schema`
- `import Ecto.Changeset`
- `alias ApiServer.Vx`

**Schema:**
- Table: `"equipment_assignment"`
- Primary key: `@primary_key {:ID, :id, autogenerate: true}` (line 7)
- Fields: `:id` (integer, source `:id`), `:equipment_id`, `:device_group`, `:device_group_timezone`, `:assignment_start`, `:assignment_end`, `:created`

**Functions:**
| Name | Line |
|------|------|
| `changeset/2` | 20 |

**Types/constants defined:** none
**Commented-out code blocks:** line 17 (`# belongs_to :equipment, ...`)

---

## Findings

---

**B005-1** — [HIGH] `send_notification_email/3` ignores its `to` parameter; recipient is hardcoded

File: `lib/api_server/vx/email.ex:4`

Description: The function signature accepts a `to` argument but the body unconditionally pipes to `"graham.oconnell@trackingsolutions.com.au"` (line 7), making the caller-supplied recipient silently ignored. Every invocation of this function sends to a fixed internal address regardless of intent. Additionally, this function is never called anywhere in the codebase (confirmed by full-repo grep), making it dead code that could be confused with a working notification mechanism. The hardcoded recipient is an additional issue catalogued separately (B005-6).

---

**B005-2** — [HIGH] `send_test_email/3` ignores its `to` parameter; recipient is hardcoded; function is dead code

File: `lib/api_server/vx/email.ex:14`

Description: Same problem as B005-1. The `to` parameter is accepted but never used; the recipient is hardcoded to `"graham.oconnell@trackingsolutions.com.au"` (line 16). Furthermore, a full-repo search confirms `send_test_email` is never called anywhere — it is dead code. The function body also contains a massive block of hardcoded HTML representing two different geofence alert templates (enter and exit) combined into one response, making it misleading as a "test" function.

---

**B005-3** — [HIGH] `send_slow_email/4` and `send_digital_matter_email/4` are dead code — never called in live paths

File: `lib/api_server/vx/email.ex:215`, `lib/api_server/vx/email.ex:262`

Description: Full-repo grep shows every call site for `send_digital_matter_email` and `send_slow_email` is commented out. Neither function is invoked in any live code path. Dead email functions accumulate maintenance debt and create confusion about whether alerting for digital-matter payloads or slow processing is active.

---

**B005-4** — [MEDIUM] `send_missing_serial_email/4` is dead code — all call sites are commented out

File: `lib/api_server/vx/email.ex:167`

Description: All three call sites in `utility_controller.ex` (lines 1707, 1729, 5390, 5613) are commented out. The function accepts a `to_email_address` parameter but is never invoked in any live path. The body contains a hardcoded first-name greeting "Graham" (B005-7) rather than using the supplied data map.

---

**B005-5** — [MEDIUM] Wrong email subject heading in `send_missing_serial_email/4`

File: `lib/api_server/vx/email.ex:177`

Description: The HTML `<h3>` heading inside `send_missing_serial_email` reads "Geofence alert - Vehicle has exited" (line 177). This function is for missing serial number notifications, not geofence exit events. The misleading heading indicates the body was copy-pasted from `send_exit_email` without updating the subject line. Similarly, `send_digital_matter_email` (line 225) carries the same "Geofence alert - Vehicle has exited" heading despite being a debug/diagnostic email for Digital Matter device payloads.

---

**B005-6** — [HIGH] Multiple hardcoded personal email addresses and production domain URLs

File: `lib/api_server/vx/email.ex:5,7,16,46,87,152,199,246,288,338`

Description: The following hardcoded values appear throughout email.ex:
- Recipient `"graham.oconnell@trackingsolutions.com.au"` — hardcoded in `send_notification_email` (line 7) and `send_test_email` (line 16).
- Sender `"no-reply@mobilehourmeter.com"` — hardcoded in `send_notification_email` (line 5).
- Logo image URL `https://vx-demo.mobilehourmeter.com/img/logoleft_vx-demo.png` — hardcoded in every email template (lines 46, 87, 152, 199, 246, 288, 338). This points to a demo/staging environment URL embedded in production email templates.
- Personal first name `"Graham"` hardcoded as the salutation in `send_missing_serial_email` (line 178), `send_digital_matter_email` (line 226), and `send_slow_email` (line 273).

Hardcoding personal names and email addresses into source code means recipients cannot be changed without a code deployment, prevents environment-specific configuration, and exposes PII in version history.

---

**B005-7** — [MEDIUM] `send_notification_email/3` accepts `to` but Bamboo's `to/2` helper is shadowed by the parameter name

File: `lib/api_server/vx/email.ex:4`

Description: The function parameter is named `to`, which shadows Bamboo's imported `to/2` pipeline helper. Within the function body, `|> to(...)` does NOT use the parameter — it calls the Bamboo `to/2` function with a hardcoded string. This is a subtle name-collision bug: if someone later tries to use the `to` variable in the pipeline they will get a `BadArityError` because `to` is bound to the caller-supplied value, not the Bamboo function. The actual delivery recipient is therefore always the hardcoded string.

---

**B005-8** — [MEDIUM] Commented-out `belongs_to` association in `EquipmentAssignment`

File: `lib/api_server/vx/equipment_assignment.ex:17`

Description: Line 17 contains a commented-out `belongs_to :equipment, ApiServer.Vx.Equipment` declaration. This suppresses the Ecto association that would allow `equipment_assignment` records to be preloaded with their parent `equipment` record. Any code that attempts to preload `:equipment` on an `EquipmentAssignment` struct will raise an Ecto association error at runtime. The comment gives no rationale for why the association was disabled, making it unclear whether this is intentional or an oversight.

---

**B005-9** — [MEDIUM] `alias ApiServer.Vx` is unused in `Equipment` and `EquipmentAssignment`

File: `lib/api_server/vx/equipment.ex:5`, `lib/api_server/vx/equipment_assignment.ex:5`

Description: Both modules declare `alias ApiServer.Vx` (line 5 in each) but `Vx` is never referenced in the module body. In `equipment_assignment.ex` the only occurrence of `ApiServer.Vx.Equipment` is inside the commented-out `belongs_to` (line 17), which means the alias was added in anticipation of that line but became orphaned when the association was commented out. Elixir will emit an "unused alias" compiler warning for both files.

---

**B005-10** — [MEDIUM] `field :id` re-declares the primary key virtual column in `Equipment` and `EquipmentAssignment`

File: `lib/api_server/vx/equipment.ex:7,9`, `lib/api_server/vx/equipment_assignment.ex:7,9`

Description: Both schemas set `@primary_key {:ID, :id, autogenerate: true}` (which generates a virtual field accessed as `.ID`) and then immediately declare `field :id, :integer, source: :id` as a separate schema field. The `:id` atom used as the auto-generate type in `@primary_key` is the Ecto `{:ID, :id, ...}` tuple where `:id` is the Elixir type — but adding a second explicit `field :id` with type `:integer` creates a duplicate field definition that Ecto will warn about or silently override. The `:id` field is also included in `cast/3` calls, so user-supplied IDs can overwrite the primary key.

---

**B005-11** — [LOW] Commented-out `text_body` lines across multiple email functions

File: `lib/api_server/vx/email.ex:19,119,172,220,267,307`

Description: Six separate `# |> text_body(message)` (or similar) comments exist, one in each email builder function. These appear to be placeholder stubs that were never implemented; none of the email functions send a plain-text alternative, meaning all outgoing emails are HTML-only. The repeated commented stubs should either be implemented (to provide proper plain-text fallback for accessibility and spam-filter compliance) or removed.

---

**B005-12** — [LOW] Commented-out example data map in `send_enter_email/4`

File: `lib/api_server/vx/email.ex:105`

Description: Lines 105–114 contain a commented-out example `data` map that was used during development to document the expected structure of the `data` parameter. This should be replaced with an `@doc` or `@spec` annotation (using a `%{}` typespec or inline documentation) and the comment removed from production code.

---

**B005-13** — [LOW] Module naming inconsistency: `ApiServer.Email` is located in the `vx/` subdirectory

File: `lib/api_server/vx/email.ex:1`

Description: All other modules in `lib/api_server/vx/` are named under `ApiServer.Vx.*` (e.g., `ApiServer.Vx.Equipment`, `ApiServer.Vx.DeviceDatabaseLookup`). The email module at the same path is named `ApiServer.Email` (no `Vx` namespace). This inconsistency means the module name does not reflect its file location, which violates Elixir's standard convention and breaks the assumption that `ApiServer.Vx.*` contains all vx-layer logic.

---

**B005-14** — [LOW] Indentation style inconsistency across files in the same directory

File: `lib/api_server/vx/equipment.ex`, `lib/api_server/vx/equipment_assignment.ex`, `lib/api_server/vx/device_database_lookup.ex` vs `lib/api_server/vx/email.ex`

Description: `device_database_lookup.ex`, `equipment.ex`, and `equipment_assignment.ex` all use 4-space indentation. `email.ex` uses 2-space indentation (the Elixir standard). This suggests the three schema files were authored or auto-generated with a non-standard editor configuration. While functionally benign, the inconsistency creates visual friction when reviewing diffs and does not conform to the Elixir community style guide (2-space indent).

---

**B005-15** — [LOW] `ApiServer.EmailView` referenced but module does not exist

File: `lib/api_server/vx/email.ex:2`

Description: `use Bamboo.Phoenix, view: ApiServer.EmailView` references `ApiServer.EmailView`, but no file defining that module exists anywhere in the repository. Bamboo.Phoenix uses the view module at compile time to render EEx templates. Since none of the functions in `ApiServer.Email` actually call `render/2` (they use inline `html_body` strings instead), this currently causes no runtime error, but it is a stale/incorrect configuration that will produce a compile-time warning or error if Bamboo.Phoenix attempts to verify the view module.

---

**B005-16** — [LOW] All four files use Windows CRLF line endings

File: `lib/api_server/vx/device_database_lookup.ex`, `lib/api_server/vx/email.ex`, `lib/api_server/vx/equipment.ex`, `lib/api_server/vx/equipment_assignment.ex`

Description: All four files contain CRLF (`\r\n`) line endings. Standard Elixir/Unix projects use LF-only line endings. If `.gitattributes` does not enforce normalization, these files will produce noisy diffs on Unix developer machines and CI systems.

---

## Summary Table

| ID | Severity | Title | File |
|----|----------|-------|------|
| B005-1 | HIGH | `send_notification_email` ignores `to` param; hardcoded recipient; dead code | email.ex:4 |
| B005-2 | HIGH | `send_test_email` ignores `to` param; hardcoded recipient; dead code | email.ex:14 |
| B005-3 | HIGH | `send_slow_email` and `send_digital_matter_email` are dead code | email.ex:215,262 |
| B005-4 | MEDIUM | `send_missing_serial_email` is dead code — all call sites commented out | email.ex:167 |
| B005-5 | MEDIUM | Wrong heading text in `send_missing_serial_email` and `send_digital_matter_email` | email.ex:177,225 |
| B005-6 | HIGH | Hardcoded personal email addresses, sender address, and demo-env logo URL | email.ex:5,7,16,46+ |
| B005-7 | MEDIUM | Parameter `to` shadows Bamboo `to/2` helper in `send_notification_email` | email.ex:4 |
| B005-8 | MEDIUM | Commented-out `belongs_to` association suppresses Ecto preload capability | equipment_assignment.ex:17 |
| B005-9 | MEDIUM | Unused alias `ApiServer.Vx` in `Equipment` and `EquipmentAssignment` | equipment.ex:5, equipment_assignment.ex:5 |
| B005-10 | MEDIUM | `field :id` re-declares the primary key in `Equipment` and `EquipmentAssignment` | equipment.ex:9, equipment_assignment.ex:9 |
| B005-11 | LOW | Commented-out `text_body` stubs in every email function | email.ex:19,119,172,220,267,307 |
| B005-12 | LOW | Commented-out example data map should be `@doc`/`@spec` | email.ex:105 |
| B005-13 | LOW | `ApiServer.Email` module name inconsistent with `vx/` file location | email.ex:1 |
| B005-14 | LOW | 4-space indentation in schema files vs 2-space in email.ex | device_database_lookup.ex, equipment.ex, equipment_assignment.ex |
| B005-15 | LOW | `ApiServer.EmailView` referenced but module does not exist | email.ex:2 |
| B005-16 | LOW | All four files use Windows CRLF line endings | all four files |
# Pass 4 – B006

Date: 2026-02-27
Audit run: 2026-02-27-01
Files reviewed:
- lib/api_server/vx/erp_import.ex
- lib/api_server/vx/geofence.ex
- lib/api_server/vx/mailer.ex
- lib/api_server/vx/rental_contracts.ex

---

## Reading Evidence

### lib/api_server/vx/erp_import.ex

**Module:** `ApiServer.Vx.ERPImport`

**Schema fields defined:**
- `:raw_record` (:string)
- `:serialno` (:string)
- `:name` (:string)
- `:matched` (:boolean)
- `:type` (:string)

**Module-level attributes:**
- `@primary_key {:id, :id, autogenerate: true}` (line 6)

**Functions:**
| Name | Line | Visibility |
|---|---|---|
| `changeset/2` | 15 | public |

**Types / errors / constants:** none explicitly defined.

---

### lib/api_server/vx/geofence.ex

**Module:** `ApiServer.Vx.Geofence`

**Schema fields defined:**
- `:name` (:string)
- `:geojson` (:string)

**Module-level attributes:**
- `@primary_key {:id, :id, autogenerate: true}` (line 10)

**Aliases / imports:**
- `import Ecto.Changeset` (line 3)
- `import Ecto.Query, warn: false` (line 4)
- `alias ApiServer.Repo` (line 6)
- `alias ApiServer.Vx` (line 7)
- `alias ApiServer.Vx.VXThingEvent` (line 8)

**Functions:**
| Name | Line | Visibility |
|---|---|---|
| `changeset/2` | 17 | public |
| `geojson_map_to_string/1` | 24 | public |
| `geojson_db_string_to_map/1` | 38 | public |
| `does_event_cause_geofence_events_no_thing/5` | 52 | private |
| `check_event_for_left_events_no_thing/5` (nil clause) | 69 | private |
| `check_event_for_left_events_no_thing/5` (general clause) | 70 | private |
| `check_event_for_entered_events_no_thing/6` | 86 | private |
| `make_geofence_event_no_thing/5` | 103 | private |
| `engine_hours_at_event_no_thing/2` | 119 | private |

**Types / errors / constants:** none explicitly defined.

---

### lib/api_server/vx/mailer.ex

**Module:** `ApiServer.Mailer`

**Functions:** none (delegates entirely to `Bamboo.Mailer` via `use`)

**Types / errors / constants:** none.

---

### lib/api_server/vx/rental_contracts.ex

**Module:** `ApiServer.Vx.RentalContract`

**Schema fields defined:**
- `:id` (:integer, source: :id)
- `:equipment_id` (:integer, source: :equipment_id)
- `:customer_id` (:integer, source: :customer_id)
- `:contract_reference` (:string, source: :contract_reference)
- `:contract_start` (:date, source: :contract_start)
- `:contract_end` (:date, source: :contract_end)
- `:billing_frequency` (:string, source: :billing_frequency)
- `:hours_per_billing_period` (:integer, source: :hours_per_billing_period)
- `:cost_units` (:string, source: :cost_units)
- `:cost_per_unit` (:float, source: :cost_per_unit)
- `:reporting_frequency` (:string, source: :reporting_frequency)
- `:created` (:utc_datetime, source: :created)
- `:sent_to_rayven` (:integer, source: :sent_to_rayven)

**Module-level attributes:**
- `@primary_key {:ID, :id, autogenerate: true}` (line 5)

**Functions:**
| Name | Line | Visibility |
|---|---|---|
| `changeset/2` | 22 | public |

**Types / errors / constants:** none explicitly defined.

---

## Findings

**B006-1** — [HIGH] Dead private function cluster: `does_event_cause_geofence_events_no_thing/5` and all its callees are never called
File: lib/api_server/vx/geofence.ex:52
Description: The private function `does_event_cause_geofence_events_no_thing/5` (line 52) and the four private functions it calls — `check_event_for_left_events_no_thing/5` (lines 69–70), `check_event_for_entered_events_no_thing/6` (line 86), `make_geofence_event_no_thing/5` (line 103), and `engine_hours_at_event_no_thing/2` (line 119) — are never called from anywhere in the codebase. A parallel "with_thing" implementation of the same algorithm exists in `GeofenceController` (lines 115–202). This entire block is unreachable dead code. The compiler will not warn because the functions are `defp` called only from other `defp` functions in the same file, with the root being the uncalled one. It represents roughly 80 lines of logic that is silently never exercised, including a live database query (`Repo.one`) and timezone conversion, which could diverge from the active implementation without anyone noticing.

---

**B006-2** — [MEDIUM] Unused aliases `ApiServer.Vx` and `ApiServer.Vx.VXThingEvent` in `Geofence`
File: lib/api_server/vx/geofence.ex:7-8
Description: `alias ApiServer.Vx` (line 7) and `alias ApiServer.Vx.VXThingEvent` (line 8) are declared but neither alias is referenced anywhere in the file body. Similarly, `import Ecto.Query, warn: false` (line 4) suppresses the unused-import warning but no Ecto.Query macros (`from`, `where`, `select`, etc.) appear in the file. All three declarations are unused imports/aliases. Elixir would normally emit compiler warnings for unused aliases; the `warn: false` on the import silences it, which masks the dead import from routine build output.

---

**B006-3** — [MEDIUM] `engine_hours_at_event_no_thing/2` has a non-exhaustive `case` on `hardwaretype`
File: lib/api_server/vx/geofence.ex:119
Description: The case expression matches only `hardwaretype` values `1` and `2`. The codebase assigns at least `hardwaretype: 5` (Pivotel controller, pivotel_controller.ex lines 59, 96) and other hardware types (3, 4, 6, 7, 8, 9 visible in the active `GeofenceController.engine_hours_at_event/3`). If this dead function were ever activated, any event with an unhandled hardware type would raise a `CaseClauseError` at runtime. Although the function is currently unreachable (see B006-1), the incomplete case is an independent correctness defect.

---

**B006-4** — [MEDIUM] `check_event_for_left_events_no_thing/5` nil-clause returns the wrong shape
File: lib/api_server/vx/geofence.ex:69
Description: The nil-clause guard clause returns a bare list `[]`:
```elixir
defp check_event_for_left_events_no_thing(customer, event, event_time, event_loc, nil), do: []
```
The caller at line 63 pattern-matches the return value as a two-element tuple:
```elixir
{fences_still_inside, left_events} = check_event_for_left_events_no_thing(...)
```
Returning `[]` instead of `{[], []}` would cause a `MatchError` at runtime whenever `in_geofences` is `nil`. The analogous nil-clause in `GeofenceController.check_event_for_left_events/6` (line 132) has the same defect, confirming this was copied without correction.

---

**B006-5** — [LOW] Variable `datetime` bound but never used in `does_event_cause_geofence_events_no_thing/5`
File: lib/api_server/vx/geofence.ex:57
Description: Inside the `%Timex.AmbiguousDateTime{}` branch, the result of `Map.get(adt, :after)` is bound to `datetime` (line 57) but `datetime` is never subsequently referenced — the variable used later is `event_time` (line 63). The actual value assigned to `event_time` comes from the outer `case` expression's result, which in the ambiguous branch is the value of `datetime`. Elixir assigns the last expression of a `case` clause as the overall result, so `event_time` does receive the correct value, but the intermediate `datetime` binding is redundant noise and Elixir would normally emit an "unused variable" warning for it. The `warn: false` import silencing means this may be masked entirely.

---

**B006-6** — [LOW] `@primary_key` field name `{:ID, ...}` inconsistent with `{:id, ...}` in sibling schemas
File: lib/api_server/vx/rental_contracts.ex:5
Description: `RentalContract` declares `@primary_key {:ID, :id, autogenerate: true}` using the atom `:ID` (uppercase). `ERPImport` (line 6) and `Geofence` (line 10) use `:id` (lowercase). Within the `vx/` directory, there are two competing conventions: uppercase `:ID` (equipment, equipment_assignment, rental_contracts, rental_periods, device_database_lookup) and lowercase `:id` (erp_import, geofence, vx_rayven_stream_status, vx_thing_info) alongside schema-specific names (`:ablid`, `:aacid`, etc.). `RentalContract` is inconsistent with `ERPImport` and `Geofence` specifically. The uppercase `:ID` atom is unusual in Elixir/Ecto conventions and may interact unexpectedly with Ecto's default primary-key introspection.

---

**B006-7** — [LOW] All `source:` annotations in `RentalContract` are redundant no-ops
File: lib/api_server/vx/rental_contracts.ex:7-19
Description: Every field declaration carries an explicit `source:` option whose value is identical to the field name atom (e.g., `field :equipment_id, :integer, source: :equipment_id`). Ecto's default `source` for a field is already the field's own atom name, so these annotations have no effect. All thirteen `source:` options are dead configuration. This is a style/clarity issue: a future developer might believe the `source:` values differ from the field names and reference them for migration or query logic, creating confusion. No other schema in the `vx/` directory applies this pattern.

---

**B006-8** — [LOW] `rental_contracts.ex` uses 4-space indentation with `end` outside module body's 2-space convention
File: lib/api_server/vx/rental_contracts.ex:1-26
Description: The entire file body is indented with 4 spaces per level (e.g., `    use Ecto.Schema` at the `defmodule` body level, `        field ...` inside `schema do`), whereas `erp_import.ex` and `geofence.ex` use the standard 2-space Elixir convention. The closing `end` at line 26 is at 2-space indent, mismatching the 4-space body. Additionally, `rental_contracts.ex` has Windows-style CRLF line endings (confirmed via `cat -A`), consistent with all other files in the set but worth noting as the file also has the non-standard indentation, suggesting it was authored in a different editor environment.

---

**B006-9** — [LOW] `changeset/2` in `RentalContract` has no `validate_required/2` call
File: lib/api_server/vx/rental_contracts.ex:22
Description: The `changeset/2` function casts thirteen fields but calls no `validate_required/2`, meaning any subset of fields can be omitted without changeset-level validation errors. The sibling schemas `ERPImport` (validates `:raw_record`) and `Geofence` (validates `:name`) both include at minimum one required field. For a domain object representing a financial rental contract, fields such as `:equipment_id`, `:customer_id`, `:contract_start`, and `:contract_end` are logically mandatory and the absence of validation is a correctness gap.

---

**B006-10** — [LOW] `geojson_db_string_to_map/1` returns `""` (empty string) on `nil` input instead of `nil` or `%{}`
File: lib/api_server/vx/geofence.ex:38
Description: Both `geojson_map_to_string/1` and `geojson_db_string_to_map/1` return `""` for both their nil-input and decode-failure branches. For `geojson_map_to_string/1` this is defensible (caller expects a string). For `geojson_db_string_to_map/1`, the function name and purpose imply it returns a map; returning `""` (a string) on failure is a type inconsistency. The caller in `VxThingEventView` passes the result directly to a JSON response as `geoJSON:`, and the caller in `vx.ex` line 3238 assigns it to `geomap` which is subsequently used as geospatial data. An empty string where a map is expected will cause downstream errors in callers that do not guard against this case.

---

## Summary Table

| ID | Severity | File | Line | Title |
|---|---|---|---|---|
| B006-1 | HIGH | geofence.ex | 52 | Dead private function cluster (`*_no_thing`) never called |
| B006-2 | MEDIUM | geofence.ex | 7–8 | Unused aliases `Vx`, `VXThingEvent`, and suppressed unused `Ecto.Query` import |
| B006-3 | MEDIUM | geofence.ex | 119 | Non-exhaustive `case` on `hardwaretype` in dead function |
| B006-4 | MEDIUM | geofence.ex | 69 | Nil-clause returns `[]` but caller expects `{[], []}` — shape mismatch |
| B006-5 | LOW | geofence.ex | 57 | Variable `datetime` bound but never read |
| B006-6 | LOW | rental_contracts.ex | 5 | `@primary_key` atom `:ID` inconsistent with `:id` in sibling schemas |
| B006-7 | LOW | rental_contracts.ex | 7–19 | All `source:` annotations are identity no-ops |
| B006-8 | LOW | rental_contracts.ex | 1–26 | Non-standard 4-space indentation; closing `end` at wrong indent level |
| B006-9 | LOW | rental_contracts.ex | 22 | `changeset/2` has no `validate_required/2` for financial domain fields |
| B006-10 | LOW | geofence.ex | 38 | `geojson_db_string_to_map/1` returns `""` (string) where map is expected |
# Pass 4 – B007

**Date:** 2026-02-27
**Audit run:** 2026-02-27-01
**Agent:** B007

## Files Reviewed

- `lib/api_server/vx/rental_periods.ex`
- `lib/api_server/vx/scheduler.ex`
- `lib/api_server/vx/vx_user_function.ex`

---

## Reading Evidence

### 1. `lib/api_server/vx/rental_periods.ex`

**Module:** `ApiServer.Vx.RentalPeriod`

**Directives:**
- `use Ecto.Schema` (line 2)
- `import Ecto.Changeset` (line 3)

**Schema definition:**
- `@primary_key {:ID, :id, autogenerate: true}` (line 5)
- Table: `"rental_periods"` (line 6)

**Fields defined in schema block:**
| Line | Field name        | Type           | source:          |
|------|-------------------|----------------|------------------|
| 7    | `:id`             | `:integer`     | `:id`            |
| 8    | `:contract_id`    | `:integer`     | `:contract_id`   |
| 9    | `:period_start`   | `:date`        | `:period_start`  |
| 10   | `:period_end`     | `:date`        | `:period_end`    |
| 11   | `:hours_used`     | `:float`       | `:hours_used`    |
| 12   | `:overage`        | `:float`       | `:overage`       |
| 13   | `:is_completed`   | `:integer`     | `:is_completed`  |
| 14   | `:created`        | `:utc_datetime`| `:created`       |

**Functions:**
| Line | Name          | Arity |
|------|---------------|-------|
| 17   | `changeset/2` | 2     |

**Types / errors / constants:** None explicitly defined.

---

### 2. `lib/api_server/vx/scheduler.ex`

**Module:** `ApiServer.Scheduler`

**Directives:**
- `use Quantum.Scheduler, otp_app: :api_server` (lines 2–3)

**Functions:** None explicitly defined (all provided by `Quantum.Scheduler` macro).

**Types / errors / constants:** None.

---

### 3. `lib/api_server/vx/vx_user_function.ex`

**Module:** `ApiServer.Vx.VXUserFunction`

**Directives:**
- `use Ecto.Schema` (line 2)
- `import Ecto.Changeset` (line 3)

**Schema definition:**
- `@primary_key {:aatid, :id, autogenerate: true}` (line 5)
- Table: `"aat_user_functions"` (line 6)

**Fields defined in schema block:**
| Line | Field name        | Type       | Notes                                          |
|------|-------------------|------------|------------------------------------------------|
| 7    | `:aatfunction_id` | `:integer` | Plain field declaration, no `source:` option   |
| 8    | `:aatuser_id`     | `:integer` | Plain field declaration, no `source:` option   |
| 10   | `belongs_to :user`| —          | `ApiServer.Vx.VXUser`, FK `:aatuser_id`, `define_field: false` |

**Functions:**
| Line | Name          | Arity |
|------|---------------|-------|
| 14   | `changeset/2` | 2     |

**Types / errors / constants:** None explicitly defined.

---

## Findings

---

**B007-1** — [HIGH] Field name mismatch in `changeset/2` causes silent cast failure and broken validation

File: `lib/api_server/vx/vx_user_function.ex:16-17`

Description: The schema declares the field as `:aatfunction_id` (line 7, with an underscore before `id`), but `cast/3` and `validate_required/2` both reference `:aatfunctionid` (no underscore). In Ecto 2.x, `cast/3` silently ignores any key in the permitted list that does not match a known schema field — meaning `:aatfunction_id` is never cast from incoming attributes. Consequently `validate_required([:aatfunctionid])` always finds the field absent and every `create_vx_user_function/1` and `update_vx_user_function/2` call returns `{:error, changeset}` with a required-field validation error. The same inconsistency propagates to the view (`vx_user_function_view.ex:17`) which accesses `vx_user_function.aatfunctionid`, raising a `KeyError` at runtime when rendering. This is a data-loss and runtime-crash bug for any future code path that re-enables the commented-out controller actions.

---

**B007-2** — [MEDIUM] Commented-out code constitutes the entire controller body

File: `lib/api_server_web/controllers/vx_user_function_controller.ex:9-41`

Description: Every action that a REST controller would expose (`index`, `create`, `show`, `update`, `delete`) is commented out. The module compiles to a shell containing only the `use`, two `alias` directives, and an `action_fallback` declaration with no live action clauses. This is not intentional feature-flagging via configuration — it is deferred work left in production source. Commented-out code of this volume obscures intent and hides the B007-1 field-name bug from any reader doing static review. Minimum severity LOW per pass instructions; raised to MEDIUM because it represents the totality of the module's intended functionality being absent.

---

**B007-3** — [LOW] Commented-out code block in `config.exs` scheduler jobs list

File: `config/config.exs:26-104`

Description: Approximately 35 of the ~48 scheduler job entries in the Quantum `jobs:` list are commented out, spanning tenants such as `vx_cea`, `vx_yocam`, `vx_south32`, `vx_komatsuau`, `vx_matthai`, `vx_hannaman`, `vx_cmhcusa`, `vx_demouk`, `vx_floridaforklifts`, `vx_kionasia`, `vx_arconic`, `vx_rentcorp`, `vx_tmhs`, `vx_atlanticfs`, `vx_mhinc`, `vx_darr`, `vx_cbe`, and others. This is directly adjacent to `scheduler.ex` (the configured module). While some entries may represent intentionally disabled tenants, there is no comment explaining the decision for individual disablement, and several appear interleaved with active entries of identical cron patterns. The configuration file is the runtime surface of the scheduler module and its commented state belongs here in the scheduler review context.

---

**B007-4** — [LOW] Commented-out design notes masquerading as code in `config.exs`

File: `config/config.exs:22-24`

Description: Lines 22–24 contain a commented-out `overlap: false` option accompanied by multi-line design questions ("What is going to happen here over multiple time periods?", "Queue table?"). These are architectural discussion notes that belong in a ticket or design document, not in a committed configuration file. The `overlap` option itself is meaningful for Quantum — its omission means jobs will overlap if the previous run has not finished — making the unanswered question a latent operational risk, not just a style issue.

---

**B007-5** — [LOW] Module name does not match file path (Elixir naming convention violation)

File: `lib/api_server/vx/scheduler.ex:1`

Description: The module is named `ApiServer.Scheduler` but the file lives at `lib/api_server/vx/scheduler.ex`. By Elixir convention the module name determines the expected file path: `ApiServer.Scheduler` should reside at `lib/api_server/scheduler.ex`. While Elixir does not enforce this at compile time, Mix tooling, IDE navigation (`go-to-definition`), and the standard `mix format` / `mix xref` conventions all assume the mapping holds. A developer searching for `ApiServer.Scheduler` will look in `lib/api_server/` and not find it. The application supervisor (`application.ex:19`) correctly references `ApiServer.Scheduler`, so the scheduler boots, but the file placement will cause confusion.

---

**B007-6** — [LOW] Redundant `source:` annotations where column name equals field name

File: `lib/api_server/vx/rental_periods.ex:7-14`

Description: Every `field` declaration in this schema carries a `source:` option whose value is identical to the field name (e.g., `field :contract_id, :integer, source: :contract_id`). In Ecto, `source:` is only needed when the database column name differs from the Elixir field name. When they are the same, the annotation is noise that adds cognitive overhead and creates a maintenance hazard — if a field is renamed, a developer must update both the field atom and the `source:` atom, and it is easy to miss one. The same pattern appears in the sibling `rental_contracts.ex` and `equipment.ex` schemas, suggesting copy-paste origin. The `device_database_lookup.ex` schema correctly uses `source:` only where column names differ (e.g., `source: :hardwareID`), demonstrating the correct pattern exists in the project.

---

**B007-7** — [LOW] Inconsistent indentation: 4-space indent instead of 2-space Elixir standard

File: `lib/api_server/vx/rental_periods.ex:2-20`

Description: The entire body of this module uses 4-space indentation (e.g., `    use Ecto.Schema`, `    schema "rental_periods" do`). The Elixir style guide and `mix format` both specify 2-space indentation. All other schemas in the `vx/` directory that were not authored alongside `rental_periods.ex` use 2-space indentation (e.g., `vx_user_function.ex`, `vx_rental.ex`, `vx_restriction.ex`). The 4-space pattern appears to be a copy from `rental_contracts.ex` (which has the same indentation), suggesting both were authored together and never formatted. Inconsistent indentation makes diffs harder to read and signals that `mix format` is not enforced at commit time.

---

**B007-8** — [LOW] `@primary_key` field named `:ID` (uppercase atom) deviates from convention

File: `lib/api_server/vx/rental_periods.ex:5`

Description: `@primary_key {:ID, :id, autogenerate: true}` names the primary-key struct field `:ID` (uppercase). Elixir atom and variable naming convention uses `snake_case`; uppercase atoms are valid but unconventional. This means accessing the primary key on a struct requires `record.ID` rather than the conventional `record.id`. The same pattern appears in `rental_contracts.ex` and `equipment.ex` / `equipment_assignment.ex` (also 4-space indented), but the majority of schemas in the project use lowercase atoms (`:aatid`, `:ablid`, `:abhid`, etc.). The `:ID` naming is a style inconsistency within the project and causes field-access asymmetry: `rental_period.ID` versus `vx_user_function.aatid`.

---

**B007-9** — [INFO] Entirely redundant `source:` annotation on the `:id` field that shadows the primary key

File: `lib/api_server/vx/rental_periods.ex:7`

Description: `field :id, :integer, source: :id` declares a schema field named `:id` in addition to the custom primary key `@primary_key {:ID, :id, autogenerate: true}`. The `@primary_key` macro already injects an `:ID` struct key that maps to the `id` database column. Declaring a separate field named `:id` pointing at the same column creates two Elixir-side references to the same database column — `:ID` (the PK virtual field) and the newly declared `:id` integer field. In Ecto 2.x this compiles but `:id` will behave as a plain field rather than the primary key, potentially causing incorrect behaviour with `Repo.get/3` or associations that resolve via the primary key. The identical pattern is present in `rental_contracts.ex:7` and `equipment.ex:9`.

---

## Summary Table

| ID      | Severity | Title                                                                 | File                                      |
|---------|----------|-----------------------------------------------------------------------|-------------------------------------------|
| B007-1  | HIGH     | Field name mismatch in changeset causes silent cast failure           | `lib/api_server/vx/vx_user_function.ex:16-17` |
| B007-2  | MEDIUM   | Entire controller body is commented out                               | `lib/api_server_web/controllers/vx_user_function_controller.ex:9-41` |
| B007-3  | LOW      | Large block of commented-out scheduler job entries in config          | `config/config.exs:26-104`                |
| B007-4  | LOW      | Unresolved design questions committed as comments in config           | `config/config.exs:22-24`                 |
| B007-5  | LOW      | Module name does not match file path (convention violation)           | `lib/api_server/vx/scheduler.ex:1`        |
| B007-6  | LOW      | Redundant `source:` annotations where field name equals column name   | `lib/api_server/vx/rental_periods.ex:7-14` |
| B007-7  | LOW      | 4-space indentation instead of 2-space Elixir standard                | `lib/api_server/vx/rental_periods.ex:2-20` |
| B007-8  | LOW      | Primary key atom `:ID` uses uppercase, deviating from snake_case      | `lib/api_server/vx/rental_periods.ex:5`   |
| B007-9  | INFO     | `:id` field declaration shadows the custom primary key field          | `lib/api_server/vx/rental_periods.ex:7`   |
# Pass 4 – B008

**Date:** 2026-02-27
**Audit run:** 2026-02-27-01
**Files reviewed:**
- `lib/api_server/vx/vx.ex` (3,314 lines)

---

## Reading Evidence

### Module Name

`ApiServer.Vx`

### Aliases Declared (at module level and inline)

| Line | Alias |
|------|-------|
| 7 | `ApiServer.Repo` |
| 8 | `ApiServer.Vx.VXUser` |
| 9 | `ApiServer.Vx.VXThingEvent` |
| 10 | `ApiServer.Vx.VXThingEventOmega` |
| 11 | `ApiServer.Vx.VXThingEventOmegaTires` |
| 12 | `ApiServer.Vx.VXFleetAssociation` |
| 13 | `ApiServer.Vx.VXRestriction` |
| 14 | `ApiServer.Vx.Geofence` |
| 15 | `ApiServer.Vx.VXThing` |
| 16 | `ApiServer.Vx.VXRental` |
| 17 | `ApiServer.Vx.VXAblRecord` |
| 18 | `ApiServer.Vx.VXRayvenMessageLog` |
| 19 | `ApiServer.Vx.VXRayvenStreamStatus` |
| 20 | `ApiServer.Vx.Equipment` |
| 21 | `ApiServer.Vx.EquipmentAssignment` |
| 22 | `ApiServer.Vx.RentalContract` |
| 23 | `ApiServer.Vx.RentalPeriod` |
| 134 | `ApiServer.Vx.VXAccessFob` (inline alias) |
| 220 | `ApiServer.Vx.VXFleet` (inline alias) |
| 1448 | `ApiServer.Vx.VXThingSummary` (inline alias) |
| 1611 | `ApiServer.Vx.VXThingEvent` (re-alias, already aliased at top) |
| 2043 | `ApiServer.Vx.VXAblRecord` (re-alias, already aliased at top) |
| 2728 | `ApiServer.Vx.VXRental` (re-alias, already aliased at top) |
| 2860 | `ApiServer.Vx.VXCustomer` (inline alias) |
| 2969 | `ApiServer.Vx.VXUserFunction` (inline alias) |
| 3187 | `ApiServer.Vx.ERPImport` (inline alias) |

### Every Function and Its Line Number

| Line | Function | Arity |
|------|----------|-------|
| 27 | `update_key_if_value/3` | (map, key_to_save, nil) — guard clause |
| 28 | `update_key_if_value/3` | (map, key_to_save, value_to_add) |
| 33 | `list_vxusers/1` | (customer) |
| 40 | `get_vx_user!/2` | (userid, customer) |
| 47 | `get_vx_user_offset/2` | (userid, customer) |
| 54 | `get_vx_user_fleets!/2` | (userid, customer) |
| 75 | `create_vx_user/2` | (attrs \\ %{}, customer) |
| 93 | `update_vx_user/3` | (%VXUser{}, attrs, customer) |
| 99 | `update_vx_user_password/3` | (%VXUser{}, attrs, customer) |
| 117 | `delete_vx_user/2` | (%VXUser{}, customer) |
| 130 | `change_vx_user/1` | (%VXUser{}) |
| 145 | `list_vxaccessfobs/0` | () |
| 163 | `get_vx_access_fob!/1` | (id) |
| 165 | `get_vx_access_fob_by_code!/1` | (fob_code) |
| 177 | `get_vx_access_fobs_for_fleets!/1` | (fleets) |
| 189 | `get_vx_fleet_for_access_fob/1` | (fobid) |
| 198 | `get_num_vx_admin_fobs/0` | () |
| 199 | `get_vx_admin_fobs/0` | () |
| 215 | `delete_vx_access_fob/1` | (%VXAccessFob{}) |
| 222 | `list_vxfleets/1` | (customer) |
| 227 | `list_vxfleets/2` | (user_id, customer) |
| 235 | `get_list_of_valid_fleets_for_user/2` | (user_id, customer) |
| 243 | `get_list_of_valid_equipment_for_user/2` | (user_id, customer) |
| 264 | `list_vxfleets_with_equipment/2` | (user_id, customer) |
| 290 | `get_vx_fleet_by_name/2` | (fleetname, customer) |
| 296 | `get_vx_fleet/2` | (id, customer) |
| 315 | `create_vx_fleet/2` | (attrs \\ %{}, customer) |
| 333 | `update_vx_fleet/3` | (%VXFleet{}, attrs, customer) |
| 351 | `delete_vx_fleet/2` | (%VXFleet{}, customer) |
| 364 | `change_vx_fleet/1` | (%VXFleet{}) |
| 378 | `update_fleet_assocs/3` | (fleet_id, customer, updated_ids) |
| 392 | `get_equipment_in_fleet/2` | (fleet_id, customer) |
| 400 | `get_hardwareids_in_fleet/2` | (fleet_id, customer) |
| 408 | `get_fleets_for_thing/2` | (thingid, customer) |
| 416 | `get_branch_for_thing/2` | (thingid, customer) |
| 427 | `list_vxfleetassociations/0` | () |
| 449 | `get_vx_fleet_association!/1` | (id) |
| 464 | `delete_vx_fleet_association/1` | (%VXFleetAssociation{}) |
| 470 | `list_vxthings/1` | (customer) |
| 478 | `list_vxthings_full/1` | (customer) |
| 492 | `list_vxthings_lite/1` | (customer) |
| 498 | `list_vxthing/2` | (customer, hardwareid) |
| 507 | `list_vxthing_full/2` | (customer, hardwareid) |
| 520 | `list_vxthing_lite/2` | (customer, hardwareid) |
| 528 | `list_vxthings/2` | (user_id, customer) |
| 539 | `list_augmented_things/2` | (user_id, customer) |
| 555 | `list_augmented_things_with_rentals/1` | (customer) |
| 568 | `list_augmented_things_with_rentals_in_fleet/3` | (customer, fleet_id, user_id) |
| 589 | `list_augmented_things_in_fleet/3` | (customer, fleet_id, user_id) |
| 608 | `list_vxthings_in_fleet/2` | (customer, fleet_id) |
| 623 | `list_vxthings_with_checklists/1` | (customer) |
| 631 | `get_lift_event_counts_for_thing_by_day/5` | (hardwareid, from_date, to_date, timezone, customer) |
| 651 | `get_detailed_lift_event_counts_for_thing_by_day/6` | (hardwareid, from_date, to_date, timezone, thing_name, customer) |
| 677 | `get_list_lift_event_counts_for_thing_by_day/6` | (hardwareid, from_date, to_date, timezone, thing_name, customer) |
| 699 | `get_detailed_lift_event_counts_for_fleet_by_day/5` | (fleetid, from_date, to_date, timezone, customer) |
| 726 | `get_omega_engine_utilization/5` | (hardwareid, to_date, from_date, timezone, customer) |
| 749 | `get_omega_operation_summary/5` | (fleetid, to_date, from_date, timezone, customer) |
| 780 | `list_vxthings_for_map/2` | (customer, user_id) — 1st clause |
| 795 | `list_vxthings_for_map/2` | (customer, fleet_id) — 2nd clause |
| 811 | `augment_thing_with_fleets/2` | (thing, customer) |
| 816 | `augment_thing_with_services/2` | (thing, customer) |
| 827 | `get_hour_meter_start_rental/2` | (thing, customer) |
| 871 | `augment_thing_with_rental_periods/2` | (thing, customer) |
| 940 | `augment_thing_with_usage/2` | (thing, customer) |
| 968 | `get_avg_weekly_hours/2` | (thing, customer) |
| 981 | `get_avg_weekly_hours/3` | (thing, customer, input) |
| 985 | `get_summary_total_usage/1` | (thing) |
| 1006 | `get_usage_since_service/2` | (thing, customer) |
| 1030 | `fetch_actual_usage/2` | (thing, customer) |
| 1042 | `generate_usage_select/2` | (query, category) |
| 1090 | `fetch_actual_usage/5` | (hardwareid, 4, customer, from, to) |
| 1133 | `fetch_actual_usage/5` | (hardwareid, 2, customer, from, to) |
| 1174 | `fetch_actual_usage/5` | (hardwareid, 3, customer, from, to) |
| 1215 | `fetch_actual_usage/5` | (hardwareid, category, customer, from, to) — fallback |
| 1230 | `fetch_actual_usage_thing/4` | (thing, customer, from, to) |
| 1235 | `get_movements/5` | (hardware_id, start_date, end_date, timezone, customer) |
| 1281 | `get_vx_thing!/1` | (id) |
| 1283 | `get_vx_thing!/2` | (id, customer) |
| 1290 | `get_thing_name_with_hardware_id!/2` | (hardwareid, customer) |
| 1296 | `get_fleet_name_with_id/2` | (id, customer) |
| 1303 | `get_thing_category_with_hardware_id!/2` | (hardwareid, customer) |
| 1311 | `get_thing_id_with_hardware_id!/2` | (hardwareid, customer) |
| 1319 | `lookup_thing_with_name_serial/3` | (name, serialno, customer) |
| 1328 | `lookup_thing_with_name/2` | (name, customer) |
| 1337 | `get_vx_thing_with_hardware_id!/1` | (hardwareid) |
| 1347 | `get_vx_thing_with_hardware_id!/2` | (hardwareid, customer) |
| 1357 | `get_augmented_thing_with_hardware_id!/2` | (hardwareid, customer) |
| 1363 | `get_equipment_by_name/2` | (name, customer) |
| 1371 | `get_equipment_by_serial/2` | (serialno, customer) |
| 1377 | `get_equipment_assignments_by_id/2` | (equipment_id, customer) |
| 1395 | `create_vx_thing/2` | (attrs \\ %{}, customer) |
| 1413 | `update_vx_thing/3` | (%VXThing{}, attrs, customer) |
| 1431 | `delete_vx_thing/1` | (%VXThing{}) |
| 1444 | `change_vx_thing/1` | (%VXThing{}) |
| 1459 | `list_vxthingsummaries/0` | () |
| 1477 | `get_vx_thing_summary!/1` | (id) |
| 1478 | `get_summary_for_hardwareid/2` | (hardwareid, customer) |
| 1484 | `update_or_insert_summary/3` | (existing_summary, attrs \\ %{}, customer) |
| 1501 | `create_vx_thing_summary/1` | (attrs \\ %{}) |
| 1519 | `update_vx_thing_summary/2` | (%VXThingSummary{}, attrs) |
| 1537 | `delete_vx_thing_summary/1` | (%VXThingSummary{}) |
| 1550 | `change_vx_thing_summary/1` | (%VXThingSummary{}) |
| 1555 | `default_checklist_questions/0` | () |
| 1586 | `get_checklists/1` | (hardwareid) |
| 1622 | `list_vxthingevents/0` | () |
| 1640 | `get_vx_thing_event!/1` | (id) |
| 1642 | `get_most_recent_thingevent/2` | (hardwareid, customer) |
| 1651 | `get_most_recent_thingevent_with_date/3` | (hardwareid, customer, date) |
| 1660 | `get_most_recent_thingevent_with_omega/2` | (hardwareid, customer) |
| 1673 | `get_thingevents_for_hardwareid/2` | (hardwareid, customer) |
| 1680 | `get_thingevents_for_hardwareid/4` | (hardwareid, from, to, customer) |
| 1702 | `create_vx_thing_event/2` | (attrs \\ %{}, customer) |
| 1720 | `update_vx_thing_event/2` | (%VXThingEvent{}, attrs) |
| 1738 | `delete_vx_thing_event/1` | (%VXThingEvent{}) |
| 1751 | `change_vx_thing_event/1` | (%VXThingEvent{}) |
| 1755 | `generate_avg_weekly_select/2` | (query, category) |
| 1795 | `convert_category_to_regular_units/2` | (category, value) |
| 1824 | `get_first_event/2` | (hardwareid, customer) |
| 1842 | `get_actual_avg_weekly_hours/3` | (hardwareid, 4, customer) |
| 1879 | `get_actual_avg_weekly_hours/4` | (hardwareid, 4, customer, _) |
| 1916 | `get_actual_avg_weekly_hours/3` | (hardwareid, 2, customer) |
| 1952 | `get_actual_avg_weekly_hours/4` | (hardwareid, 2, customer, 1) |
| 1988 | `get_actual_avg_weekly_hours/3` | (hardwareid, 3, customer) |
| 2026 | `get_actual_avg_weekly_hours/3` | (hardwareid, category, customer) — fallback |
| 2054 | `list_service_records/1` | (customer) |
| 2062 | `daily_usage_where/2` | (query, category) — private |
| 2100 | `get_daily_usage/6` | (hardwareid, category, customer, to_date, from_date, timezone) |
| 2170 | `get_impact_count_by_hardwareid/2` | (hardwareid, customer) |
| 2179 | `get_events/5` | (hardwareid, customer, to_date, from_date, timezone) |
| 2192 | `process_events/0` | () |
| 2547 | `process_events_subprocess/1` | (index) |
| 2611 | `get_vx_abl_record!/1` | (id) |
| 2625 | `create_vx_abl_record/1` | (attrs \\ %{}) |
| 2631 | `create_abl_record/2` | (attrs \\ %{}, customer) |
| 2637 | `create_equipment_record/2` | (attrs \\ %{}, customer) |
| 2643 | `get_equipment_id/2` | (customer, serial_number) |
| 2650 | `create_equipment_assignment_record/2` | (attrs \\ %{}, customer) |
| 2668 | `update_vx_abl_record/2` | (%VXAblRecord{}, attrs) |
| 2686 | `delete_vx_abl_record/1` | (%VXAblRecord{}) |
| 2699 | `change_vx_abl_record/1` | (%VXAblRecord{}) |
| 2704 | `get_rhm_user/3` | (email, password, customer) |
| 2712 | `check_password/3` | (user_id, password, customer) |
| 2719 | `get_rhm_user/2` | (email, customer) |
| 2730 | `list_all_rentals/1` | (customer) |
| 2740 | `list_open_rentals/1` | (customer) |
| 2753 | `get_rental/2` | (id, customer) |
| 2764 | `get_active_rental/2` | (thing_id, customer) |
| 2776 | `get_all_rentals_for_thing/2` | (thing_id, customer) |
| 2786 | `get_rental/4` | (thing_id, customer_id, start_date, customer) |
| 2798 | `delete_rental/2` | (%VXRental{}, customer) |
| 2802 | `update_rental/3` | (%VXRental{}, attrs, customer) |
| 2809 | `create_rental_contract/2` | (attrs \\ %{}, customer) |
| 2817 | `create_rental_period/2` | (attrs \\ %{}, customer) |
| 2825 | `get_rental_periods_for_contract/2` | (contract_id, customer) |
| 2831 | `create_rental/2` | (attrs \\ %{}, customer) |
| 2871 | `list_customers/1` | (customer) |
| 2889 | `get_vx_customer!/2` | (id, customer) |
| 2891 | `get_customer/3` | (erp_id, erp_name, customer) |
| 2916 | `create_vx_customer/2` | (attrs \\ %{}, customer) |
| 2934 | `update_vx_customer/3` | (%VXCustomer{}, attrs, customer) |
| 2952 | `delete_vx_customer/2` | (%VXCustomer{}, customer) |
| 2965 | `change_vx_customer/2` | (%VXCustomer{}, customer) |
| 2980 | `list_vxaatuserfunctions/0` | () |
| 2998 | `get_vx_user_function!/1` | (id) |
| 3012 | `create_vx_user_function/1` | (attrs \\ %{}) |
| 3030 | `update_vx_user_function/2` | (%VXUserFunction{}, attrs) |
| 3048 | `delete_vx_user_function/1` | (%VXUserFunction{}) |
| 3061 | `change_vx_user_function/1` | (%VXUserFunction{}) |
| 3074 | `list_vxaau_rest/0` | () |
| 3092 | `get_vx_restriction!/1` | (id) |
| 3106 | `create_vx_restriction/1` | (attrs \\ %{}) |
| 3112 | `add_fleet_to_user/3` | (fleet_id, user_id, customer) |
| 3124 | `get_restriction/3` | (fleet_id, user_id, customer) |
| 3132 | `remove_fleet_from_user/3` | (fleet_id, user_id, customer) |
| 3150 | `update_vx_restriction/2` | (%VXRestriction{}, attrs) |
| 3168 | `delete_vx_restriction/1` | (%VXRestriction{}) |
| 3181 | `change_vx_restriction/1` | (%VXRestriction{}) |
| 3189 | `delete_erp_import/2` | (%ERPImport{}, customer) |
| 3193 | `create_erp_import/2` | (attrs \\ %{}, customer) |
| 3199 | `update_erp_import/3` | (%ERPImport{}, attrs, customer) |
| 3205 | `check_for_existing_erp_record/2` | (raw_record, customer) |
| 3223 | `get_geofence_by_id/2` | (id, customer) |
| 3229 | `get_geofences/1` | (customer) |
| 3234 | `get_geofences_as_map/1` | (customer) |
| 3249 | `create_geofence/2` | (attrs \\ %{}, customer) |
| 3255 | `update_geofence/3` | (%Geofence{}, attrs, customer) |
| 3261 | `delete_geofence/2` | (%Geofence{}, customer) |
| 3265 | `create_thingevent_record/2` | (attrs \\ %{}, customer) |
| 3271 | `update_thingevent_record/3` | (%VXThingEvent{}, attrs, customer) |
| 3277 | `delete_thingevent_record/2` | (%VXThingEvent{}, customer) |
| 3281 | `create_thingeventomega_record/2` | (attrs \\ %{}, customer) |
| 3287 | `create_thingomegatires_record/2` | (attrs \\ %{}, customer) |
| 3293 | `create_rayven_message_log_record/2` | (attrs \\ %{}, customer) |
| 3299 | `update_rayven_stream_status_record/2` | (attrs, customer) |
| 3305 | `count_rayven_events_to_stream/3` | (hardware_id, id, customer) |

### Constants / Magic Values Noted

- Line 198: `7` — hardcoded count of admin fobs
- Line 200: raw hex string of admin fob codes
- Line 429: `"29"` — hardcoded fleet ID excluded from fleet association list
- Line 762: `6` — hardware type constant (no named constant)
- Line 762: `t.aadhw_type == 6` — repeated magic number
- Line 874–879: `"2019-01-01"`, `"2020-07-05"`, `"US/Michigan"` — hardcoded dates and timezone
- Line 950: `"+10:00"` — hardcoded timezone
- Line 1098 / 1108 / 1140 / 1150 / 1181 / 1190: `5` — hardcoded LIMIT in queries
- Lines 1661: `[3, 178, 16, 32, 193, 194]` — unexplained magic list of event type codes
- Line 2196: `"vx_cea"` — hardcoded tenant/customer string
- Line 2198: `37` — hardcoded admin user ID
- Line 2204: `49838414` — hardcoded event ID threshold
- Line 2207: `5000` — hardcoded batch size
- Line 2306: hardcoded personal email addresses
- Line 2307: hardcoded `"no-reply@mobilehourmeter.com"` sender address
- Line 2323: `"Jeremy - 4"` — hardcoded geofence name
- Lines 2357, 2417, 2477: repeated hardcoded email recipient lists
- Line 3207: `"vx_cea"` — hardcoded tenant string in match

### Types / Errors Defined

None (no `@type`, `@typep`, `defexception`, or module-level constants via `@` attributes beyond `@doc` and `@moduledoc`).

---

## Findings

---

**B008-1** — [HIGH] Plaintext password comparison stored and queried in database

File: `lib/api_server/vx/vx.ex:2704` and `lib/api_server/vx/vx.ex:2712`

Description: `get_rhm_user/3` and `check_password/3` perform authentication by issuing Ecto queries that match the raw `aacpassword` column directly against a plaintext input. This means passwords are stored in plaintext (or at most an easily reversible form) in the database and are compared in a SQL `WHERE` clause. Any DB leak or query log exposes all credentials. This is a security vulnerability, not merely a style issue.

---

**B008-2** — [HIGH] Hardcoded personal email addresses and production tenant identifier in business logic

File: `lib/api_server/vx/vx.ex:2196`, `2198`, `2204`, `2306`, `2323`, `2357`, `2417`, `2477`, `2540`

Description: `process_events/0` hard-codes the customer schema `"vx_cea"`, the admin user ID `37`, an event ID offset `49838414`, personally identifiable email addresses (`shad.wall@clarkequipment.com`, `jeremy.oska@clarkequipment.com`, `james.purdom@trackingsolutions.com.au`, `graham.oconnell@trackingsolutions.com.au`), a sender domain `no-reply@mobilehourmeter.com`, and specific geofence name strings (`"Jeremy - 4"`). These values are completely non-configurable. A tenant change, personnel change, or email infrastructure change requires a code deploy. The same customer name `"vx_cea"` also appears at line 3207 in `check_for_existing_erp_record/2`.

---

**B008-3** — [HIGH] Duplicate function body: `get_actual_avg_weekly_hours/3` (category 4) and `get_actual_avg_weekly_hours/4` (category 4, `_` ignored)

File: `lib/api_server/vx/vx.ex:1842` and `lib/api_server/vx/vx.ex:1879`

Description: `get_actual_avg_weekly_hours(hardwareid, 4, customer)` (line 1842) and `get_actual_avg_weekly_hours(hardwareid, 4, customer, _)` (line 1879) are 100% identical in body — same `get_first_event` call, same `Timex.diff` / week-calculation logic, same `fetch_actual_usage` call, same `cond` / `Float.round` return. The four-argument variant silently ignores its fourth argument and produces the same result as the three-argument variant. This is likely an oversight that can lead to incorrect results when callers pass a meaningful `input` value expecting different behaviour, and it creates dead weight that will diverge over time.

---

**B008-4** — [MEDIUM] Large block of commented-out code — `process_events/0` geofence email sending

File: `lib/api_server/vx/vx.ex:2309–2310`, `2360–2361`, `2420–2421`, `2480–2481`, `2543–2544`

Description: Multiple send-email call pairs throughout `process_events/0` are commented out:
- Lines 2309–2310: exit email to `shad.wall` list commented out while `graham.oconnell` line at 2328–2329 is live.
- Lines 2360–2361: entry email commented out.
- Lines 2420–2421: entry email commented out.
- Lines 2480–2481: entry email commented out.
- Lines 2543–2544: summary diff-alert email commented out.
Commented-out send calls are interleaved with live sends, making it impossible to understand the intended notification logic from reading the code. Dead commented-out code should be removed from version control.

---

**B008-5** — [MEDIUM] Commented-out code — `augment_thing_with_rental_periods` hardcoded dates and disabled logic

File: `lib/api_server/vx/vx.ex:871–937`

Description: `augment_thing_with_rental_periods/2` contains:
- Lines 874–879: hardcoded `from_date = "2019-01-01"` and `to_date = "2020-07-05"` and `user_timezone = "US/Michigan"` — these are obviously stale (past) test values that are never overridden.
- Lines 904–919: a large block of commented-out map keys (JSON structure) that was part of the return value.

The function can never return meaningful current data because the date range is static and years in the past. The function appears to be abandoned development work left in the codebase.

---

**B008-6** — [MEDIUM] Commented-out code — `get_avg_weekly_hours/2` disabled branch

File: `lib/api_server/vx/vx.ex:970–976`

Description: The first branch of the `cond` in `get_avg_weekly_hours/2` is entirely commented out (lines 970–975), leaving only a `true ->` catch-all. The `cond` is therefore pointless; the function always falls through to `get_actual_avg_weekly_hours/3`. The commented branch suggests an alternative path reading from `thing.info.averageweeklyusage` that was abandoned. This should either be restored or the `cond` collapsed to a direct call.

---

**B008-7** — [MEDIUM] Commented-out code — `get_hour_meter_start_rental/2` disabled query clause

File: `lib/api_server/vx/vx.ex:836`, `841`

Description: Inside `get_hour_meter_start_rental/2` two query filter lines are commented out:
- Line 836: `# |> Ecto.Query.where([te], not te.id in ^sent_events )`
- Line 841: `# Select events from database where date >= startdate`
The `inList` / `sent_events` variable this filter referenced is never declared, meaning if uncommented the code would not compile. These stale comments indicate abandoned filtering logic.

---

**B008-8** — [MEDIUM] Commented-out code — `create_rental/2` Rayven sync block

File: `lib/api_server/vx/vx.ex:2834–2853`

Description: `create_rental/2` contains a 20-line block of commented-out code building a Poison-encoded body and calling `ApiServerWeb.UtilityController.send_to_rayven`. The comment at line 2832 acknowledges the intent but no live implementation exists. The large dead block misleads maintainers into thinking Rayven sync for rental creation is handled here.

---

**B008-9** — [MEDIUM] Commented-out code — `get_daily_usage/6` Omega category select field

File: `lib/api_server/vx/vx.ex:2124`

Description: Inside the `category 4` branch of `get_daily_usage/6`, line 2124 comments out the `input2totalseconds` fragment while all surrounding inputs are present:
`# fragment("(? - ?)/3600", max(field(te , :input2totalseconds)), min(field(te , :input2totalseconds))),`
This causes the returned tuple to have a different arity for category 4 versus all other categories, which will break downstream pattern-matching on the result unless callers already account for this. If intentional, there is no explanation.

---

**B008-10** — [MEDIUM] Commented-out code — `get_daily_usage/6` inner query clauses

File: `lib/api_server/vx/vx.ex:2104`, `2106`

Description: Two lines inside `get_daily_usage/6` are commented out:
- Line 2104: `# category = get_thing_category_with_hardware_id!(hardwareid, customer)` — dynamic category lookup was replaced by the caller-supplied argument, but left as a comment implying uncertainty about the design.
- Line 2106: `# There should be a category 4 here that selects from the thingomega table.` — this comment is a TODO/design note that was never cleaned up; category 4 handling does now exist in the same function, so the note is stale.

---

**B008-11** — [MEDIUM] Commented-out code — `process_events_subprocess/1` query filters

File: `lib/api_server/vx/vx.ex:2555–2558`

Description: Inside `process_events_subprocess/1`, four consecutive query clauses are commented out:
```
# |> Ecto.Query.where([te], is_nil(te.geofence))
# |> Ecto.Query.where([te], te.hardwareid == 47371 )
# |> Ecto.Query.select()
# |> Ecto.Query.order_by(asc: :gmtdatetime)
```
Without `is_nil(te.geofence)`, the subprocess re-processes all events including already-processed ones, which is incorrect. The function's own comment on line 2548 states "I don't think this is used anymore," confirming this is dead code.

---

**B008-12** — [MEDIUM] Dead function: `process_events_subprocess/1` acknowledged as unused

File: `lib/api_server/vx/vx.ex:2547`

Description: The inline comment at line 2548 reads `# I don't think this is used anymore.` The function has no `@doc`, its query is broken (all filters commented out — see B008-11), and it hardcodes the same `"vx_cea"` customer and `user_id = 37` as `process_events/0`. It should be removed.

---

**B008-13** — [MEDIUM] Dead function: `get_checklists/1` returns stub data ignoring its argument

File: `lib/api_server/vx/vx.ex:1586`

Description: `get_checklists/1` accepts `hardwareid` but completely ignores it. It returns a static list of four hardcoded structs with `DateTime.utc_now()` timestamps and canned boolean answer arrays. This is clearly stub/mock data that was never replaced with a real database query. The function is also not private, exposing a fake public API.

---

**B008-14** — [MEDIUM] Ambiguous clause pair `list_vxthings_for_map/2` — both match any two arguments

File: `lib/api_server/vx/vx.ex:780` and `lib/api_server/vx/vx.ex:795`

Description: Both clauses of `list_vxthings_for_map/2` accept `(customer, user_id)` and `(customer, fleet_id)` respectively. Since both parameters are untyped atoms/integers at runtime, Elixir will always dispatch to the first clause (line 780) regardless of whether the caller intends `user_id` or `fleet_id`. The second clause (line 795) is therefore unreachable by normal dispatch. The two query strategies are logically different (user-scoped vs. fleet-scoped), and the function should be split into two distinctly named functions.

---

**B008-15** — [MEDIUM] Massive copy-paste duplication in `get_actual_avg_weekly_hours` family

File: `lib/api_server/vx/vx.ex:1842–2041`

Description: Five separate clauses of `get_actual_avg_weekly_hours` (lines 1842, 1879, 1916, 1952, 1988) each repeat the identical pattern:
1. `get_first_event`
2. `Timex.diff(now, first_event, :days)`
3. Same `cond` computing `start_of_year` with identical branch conditions and day thresholds (28 days)
4. Same week-count arithmetic using `div` and `rem`
5. A `fetch_actual_usage` call (varying only the category arg)
6. Identical `cond` with `Float.round`

The only meaningful variation is the `fetch_actual_usage` category. All this logic should be in a single private helper; the current structure creates ~150 lines of duplicated code where a single 20-line function parameterised by category would suffice. Any bug fix or change to the 28-day window must be applied in five places.

---

**B008-16** — [MEDIUM] Copy-paste duplication in `fetch_actual_usage` clauses for categories 2, 3, and 4

File: `lib/api_server/vx/vx.ex:1090–1213`

Description: The three pattern-matched `fetch_actual_usage/5` clauses (categories 4, 2, and 3) each repeat the same six-step pattern:
1. Build `desc_ids` — top-5 event IDs ordered descending
2. Build `asc_ids` — top-5 event IDs ordered ascending
3. Query `min` from the ascending set
4. Query `max` from the descending set
5. `cond` on nil-ness
6. Return `max - min` (possibly `/3600`)

The only differences are the event table (VXThingEventOmega vs. VXThingEvent), the field name, and the unit divisor. This represents ~120 lines of near-identical code. A private helper parameterised by table/field/divisor would eliminate the duplication.

---

**B008-17** — [MEDIUM] Bound-but-unused variables without `_` prefix

File: `lib/api_server/vx/vx.ex` — multiple locations

Description: Several variables are bound but never subsequently used, which produces Elixir compiler warnings:

- Line 2197: `inList = []` — never used in `process_events/0`.
- Line 2199: `user_timezone = get_vx_user_offset(user_id, customer)` — never used in `process_events/0`.
- Line 2519: `diff = Timex.diff(new_time, current_time, :milliseconds)` — computed inside the `Enum.each` block but never used.
- Line 2550: `inList = []` — never used in `process_events_subprocess/1`.
- Line 2552: `user_timezone = get_vx_user_offset(user_id, customer)` — never used in `process_events_subprocess/1`.
- Line 2592: `diff = Timex.diff(new_time, current_time, :milliseconds)` — computed but never used.
- Line 623: `results` is assigned from the query pipeline but the function body ends immediately; the variable is the implicit return value (which may be intentional), however the assignment name `results` is misleading if the intent is to return the mapped list — the last pipeline step is `Enum.map` but is bound to `results` then immediately returned.

Each unused binding without an `_` prefix generates an Elixir compiler warning.

---

**B008-18** — [MEDIUM] Re-aliasing already-aliased modules mid-file

File: `lib/api_server/vx/vx.ex:1611`, `2043`, `2728`

Description: Three modules already aliased at the top of the file are re-aliased inline mid-file with redundant `alias` statements:
- Line 1611: `alias ApiServer.Vx.VXThingEvent` — already aliased at line 9.
- Line 2043: `alias ApiServer.Vx.VXAblRecord` — already aliased at line 17.
- Line 2728: `alias ApiServer.Vx.VXRental` — already aliased at line 16.

In Elixir this is harmless but generates no warning; it creates visual noise and implies the module was not already in scope, potentially confusing maintainers about what is imported where.

---

**B008-19** — [MEDIUM] Magic numbers used for equipment category codes throughout without named constants

File: `lib/api_server/vx/vx.ex` — pervasive

Description: Numeric category codes appear in at least 10 functions (`generate_usage_select/2`, `generate_avg_weekly_select/2`, `convert_category_to_regular_units/2`, `daily_usage_where/2`, `get_actual_avg_weekly_hours`, `fetch_actual_usage`, `get_summary_total_usage`, `get_daily_usage/6`) without any module-level constant or type alias. The same integer appears with different comments across different functions (e.g., `2` is "Input 0" in some and "Engine seconds" in others; `4` is "Omega"; `5` is "J1939"). Notable instances:
- Categories 2, 3, 4, 5, 6, 7, 8, 9 each appear across 5+ functions
- Event type codes 3, 16, 32, 178, 177, 183, 193, 194 are repeated inline across many queries
- Hardware type `6` at line 762 appears without explanation
- Limit `5` at lines 1098, 1108, 1140, 1150, 1181, 1190 (why 5 events for min/max?)
- `28` day look-back window repeated in five `get_actual_avg_weekly_hours` clauses

The absence of named constants means any change to a category code or event type must be tracked down manually across hundreds of lines.

---

**B008-20** — [MEDIUM] `generate_usage_select/2` uses category codes 12–14 but `generate_avg_weekly_select/2` uses 2–9 — inconsistent fallback numbering scheme

File: `lib/api_server/vx/vx.ex:1042` vs `lib/api_server/vx/vx.ex:1755`

Description: `generate_usage_select/2` handles categories 12, 13, 14 as "fallback" variants of 2, 3, 4 respectively (offset by 10), while `generate_avg_weekly_select/2` handles only 2–9 with no fallback codes. The "category + 10 = fallback" convention is nowhere documented or enforced. The caller at line 1127 passes `14` as a fallback for category 4, and line 1168 passes `12` as a fallback for category 2. This implicit encoding is opaque and fragile.

---

**B008-21** — [LOW] Inconsistent `@doc` coverage — majority of public functions lack documentation

File: `lib/api_server/vx/vx.ex` — pervasive

Description: Approximately 30 functions have `@doc` blocks (mostly the boilerplate CRUD functions generated by Phoenix), while at least 80 public functions have no `@doc` at all. Functions of significant complexity with no documentation include: `augment_thing_with_rental_periods/2`, `fetch_actual_usage/5` (all clauses), `generate_usage_select/2`, `get_actual_avg_weekly_hours` (all clauses), `get_daily_usage/6`, `process_events/0`, `check_password/3`, `get_rhm_user/2`, `get_rhm_user/3`, `get_checklists/1`, and many others. The selective use of `@doc` on simple CRUD functions while omitting it from complex domain logic is inverted from best practice.

---

**B008-22** — [LOW] Inconsistent bang (`!`) naming convention

File: `lib/api_server/vx/vx.ex` — multiple locations

Description: Bang suffix (`!`) in Elixir conventionally means the function raises on failure rather than returning `{:error, reason}`. Several functions break this convention:
- `get_vx_user!/2` (line 40) uses `Repo.one` (non-raising) instead of `Repo.one!`, so it does not actually raise.
- `get_vx_thing_with_hardware_id!/1` (line 1337) and `/2` (line 1347) use `Repo.one` (non-raising).
- `get_thing_name_with_hardware_id!/2` (line 1290) uses `Repo.one` (non-raising).
- `get_thing_category_with_hardware_id!/2` (line 1303) uses `Repo.one` (non-raising).
- `get_thing_id_with_hardware_id!/2` (line 1311) uses `Repo.one` (non-raising).
- `get_vx_access_fob_by_code!/1` (line 165) uses `Repo.one` (non-raising) — but is named with `!`.

Conversely `get_vx_user!/2` misleads callers into not handling `nil` returns that will in fact occur. This is a latent crash risk: pattern-matching callers that assume a struct will crash with a `MatchError` on nil rather than a descriptive `Ecto.NoResultsError`.

---

**B008-23** — [LOW] Inconsistent indentation style across similar query pipelines

File: `lib/api_server/vx/vx.ex` — pervasive

Description: Query pipelines vary arbitrarily between 2-space, 4-space, and 6-space indentation within the same file, and the position of `|>` operators is sometimes aligned under the module alias and sometimes further indented. Examples:
- Lines 33–38: 4-space indent.
- Lines 40–45: 8-space indent (double).
- Lines 780–808 (`list_vxthings_for_map`): 6-space indent.
- Lines 589–601 (`list_augmented_things_in_fleet`): 4-space indent.
- Lines 1680–1687 (`get_thingevents_for_hardwareid/4`): 2-space indent (at the module top level, not indented inside the function at all).

This does not affect runtime behaviour but makes the file visually inconsistent and harder to read.

---

**B008-24** — [LOW] `list_vxfleetassociations/0` hardcodes fleet ID `"29"` as exclusion filter

File: `lib/api_server/vx/vx.ex:429`

Description:
```elixir
|> Ecto.Query.where([r], r.aafgroupid != ^"29")
```
Fleet ID `29` is excluded from the general fleet association listing with no comment explaining why. This is a magic constant that silently hides data for one specific fleet. If fleet 29 is a special system fleet, that should be documented and the ID extracted to a named constant or configuration value.

---

**B008-25** — [LOW] `get_vx_admin_fobs/0` returns a raw hex string with no parsing or validation

File: `lib/api_server/vx/vx.ex:199–201`

Description:
```elixir
def get_num_vx_admin_fobs(), do: 7
def get_vx_admin_fobs() do
  "000019333303000019333AEA000019330E4E0000193354AC00001933382D00001932FCA800001933001A"
end
```
The function returns a single concatenated 80-character hex string representing 7 fob codes (7 × ~11 chars). There is no parsing, splitting, or validation. The companion `get_num_vx_admin_fobs/0` returning `7` as a separate function rather than deriving the count from the list is fragile — these two values can silently diverge. Any addition of an 8th admin fob requires editing both functions correctly.

---

**B008-26** — [LOW] `daily_usage_where/2` is `defp` but `generate_usage_select/2` and `generate_avg_weekly_select/2` are `def`

File: `lib/api_server/vx/vx.ex:1042`, `1755`, `2062`

Description: `daily_usage_where/2` is correctly marked private (`defp`) at line 2062 because it is only used internally. However, `generate_usage_select/2` (line 1042) and `generate_avg_weekly_select/2` (line 1755) are public `def` despite being internal query-building helpers with no plausible external caller. They should be `defp` to reduce the public API surface.

---

**B008-27** — [LOW] `get_vx_user!/2` misleadingly named — does not use `Repo.one!`

File: `lib/api_server/vx/vx.ex:40`

Description: Noted in B008-22 as part of the broader naming inconsistency, this specific function deserves individual attention because it calls `Repo.one` (which returns `nil` on no result) rather than the bang variant `Repo.one!` (which raises `Ecto.NoResultsError`). The function's `@doc` is absent, and callers relying on the `!` convention for crash-on-absence guarantees will receive `nil` and likely crash elsewhere with a less informative error.

---

## Summary Table

| ID | Severity | Title |
|----|----------|-------|
| B008-1 | HIGH | Plaintext password comparison in database queries |
| B008-2 | HIGH | Hardcoded personal emails, tenant IDs, and production constants in business logic |
| B008-3 | HIGH | Duplicate identical function body: `get_actual_avg_weekly_hours/4` (cat 4) ignores input arg |
| B008-4 | MEDIUM | Large commented-out email sends interleaved with live sends in `process_events/0` |
| B008-5 | MEDIUM | `augment_thing_with_rental_periods/2` has hardcoded past dates and commented-out return fields |
| B008-6 | MEDIUM | Commented-out cond branch in `get_avg_weekly_hours/2` renders cond pointless |
| B008-7 | MEDIUM | Commented-out query clauses in `get_hour_meter_start_rental/2` referencing undefined variable |
| B008-8 | MEDIUM | 20-line commented-out Rayven sync block in `create_rental/2` |
| B008-9 | MEDIUM | Commented-out select field causes result tuple arity mismatch for category 4 in `get_daily_usage/6` |
| B008-10 | MEDIUM | Stale TODO comment in `get_daily_usage/6` after the addressed code already exists |
| B008-11 | MEDIUM | All meaningful query filters commented out in `process_events_subprocess/1` |
| B008-12 | MEDIUM | `process_events_subprocess/1` acknowledged as dead code by inline comment |
| B008-13 | MEDIUM | `get_checklists/1` ignores its argument and returns hardcoded stub data |
| B008-14 | MEDIUM | `list_vxthings_for_map/2` second clause unreachable due to indistinguishable argument types |
| B008-15 | MEDIUM | ~150 lines of copy-paste duplication across five `get_actual_avg_weekly_hours` clauses |
| B008-16 | MEDIUM | ~120 lines of copy-paste duplication across three `fetch_actual_usage/5` clauses |
| B008-17 | MEDIUM | Bound-but-unused variables (no `_` prefix) generating compiler warnings in 6+ locations |
| B008-18 | MEDIUM | Three modules re-aliased mid-file despite being aliased at module top |
| B008-19 | MEDIUM | Pervasive magic numbers for category codes and event types across 10+ functions |
| B008-20 | MEDIUM | Inconsistent category numbering: `generate_usage_select` uses 12–14 fallbacks; `generate_avg_weekly_select` does not |
| B008-21 | LOW | ~80 public functions lack `@doc`; documentation is inverted (simple CRUD documented, complex logic undocumented) |
| B008-22 | LOW | Bang (`!`) naming applied to 6+ functions that use non-raising `Repo.one` |
| B008-23 | LOW | Inconsistent indentation (2/4/6/8 spaces) across query pipelines |
| B008-24 | LOW | Magic constant `"29"` hardcoded fleet exclusion in `list_vxfleetassociations/0` |
| B008-25 | LOW | `get_vx_admin_fobs/0` and `get_num_vx_admin_fobs/0` are fragile parallel constants with no parsing |
| B008-26 | LOW | Internal query-builder helpers `generate_usage_select/2` and `generate_avg_weekly_select/2` should be `defp` |
| B008-27 | LOW | `get_vx_user!/2` uses `Repo.one` (non-raising) despite `!` suffix |
# Pass 4 – B009

Date: 2026-02-27
Audit run: 2026-02-27-01
Files reviewed:
- lib/api_server/vx/vx_abl_record.ex
- lib/api_server/vx/vx_access_fob.ex
- lib/api_server/vx/vx_customer.ex
- lib/api_server/vx/vx_fleet.ex

---

## Reading Evidence

### lib/api_server/vx/vx_abl_record.ex

**Module:** `ApiServer.Vx.VXAblRecord`

**Schema:** `"abl_data_changes"` — primary key `:ablid`

**Functions:**

| Line | Name | Arity |
|------|------|-------|
| 25 | `changeset/2` | `(vx_abl_record, attrs)` |
| 31 | `generate_service/10` | `(user, import_hour_meter, performed_by, thing, existing_service_date, new_service_date, current_hour_meter, input_one_hour_meter, usage, customer)` |
| 54 | `clean_xml_value/1` | `(value)` |
| 63 | `clean_xml_number_value/1` | `(value)` |
| 72 | `expand_xml_to_struct/1` | `(abl_record)` |

**Fields defined in schema:**
`:ablid` (PK), `:abldatetime`, `:ablcustcode`, `:abluser`, `:abllogtype`, `:ablusragnt`, `:ablip_address`, `:abltable`, `:ablaction`, `:ablimagetype`, `:ablimage`, `:ablprocessed`

**Associations:** `belongs_to :user, ApiServer.Vx.VXUser` (via `:abluser` / `:aacuser`, `define_field: false`)

**Aliases:** `ApiServer.Vx`

---

### lib/api_server/vx/vx_access_fob.ex

**Module:** `ApiServer.Vx.VXAccessFob`

**Schema:** `"access_fobs"` — default primary key (`:id`)

**Functions:** None defined in this module.

**Fields defined in schema:**
`:id` (implicit PK), `:fob_code`

**Associations:** `belongs_to :user, ApiServer.Vx.VXUser` (via `:assigned_to_user` / `:aacid`)

**Top-level requires (outside defmodule):** `Ecto.Query` (line 1), `Ecto.Adapters.SQL` (line 2)

---

### lib/api_server/vx/vx_customer.ex

**Module:** `ApiServer.Vx.VXCustomer`

**Schema:** `"aaa_customers"` — primary key `:aaaid`

**Functions:**

| Line | Name | Arity |
|------|------|-------|
| 25 | `convert_json_to_changeset/1` | `(customer_json)` |
| 43 | `changeset/2` | `(vx_customer, attrs)` |

**Fields defined in schema:**
`:aaaid` (PK), `:aaaaddr1`, `:aaaaddr2`, `:aaaaddr3`, `:aaacolour`, `:aaaname`, `:aaapcode`, `:aaaprimcont`, `:aaaprimemail`, `:aaaprimtel`, `:aaatz`, `:aaaudfcustcode`, `:aaacustcode`

**Associations:** `belongs_to :rental, ApiServer.Vx.VXRental` (`primary_key: true`, `define_field: false`)

**Aliases:** `ApiServer.Vx`

---

### lib/api_server/vx/vx_fleet.ex

**Module:** `ApiServer.Vx.VXFleet`

**Schema:** `"aae_group"` — primary key `:aaeid`

**Functions:**

| Line | Name | Arity |
|------|------|-------|
| 19 | `convert_json_to_changeset/1` | `(fleet_json)` |
| 27 | `changeset/2` | `(fleet, attrs)` |

**Fields defined in schema:**
`:aaeid` (PK), `:aaecustcode`, `:aaedesc`, `:aaecolour`, `:aaetype`, `:aaeshowfilter`

**Associations:** `has_many :fleet_thing_joins, ApiServer.Vx.VXFleetAssociation`

**Aliases:** `ApiServer.Vx`

---

## Findings

---

**B009-1** — [LOW] Unused `require` directives in schema module

File: lib/api_server/vx/vx_access_fob.ex:1-2

Description: `require Ecto.Query` and `require Ecto.Adapters.SQL` appear at the top level of the file, before `defmodule`, but neither macro is used anywhere in the module. These require calls produce compiler warnings ("Ecto.Query is not a behaviour, cannot be required"). They are boilerplate copy-paste artefacts carried over from other schema files (e.g., `vx_thing.ex`, `vx_fleet_association.ex`) that also carry this pattern despite not using these macros directly. Unused requires add noise to compilation output and mislead readers into believing raw SQL or query macros are employed in the schema.

---

**B009-2** — [MEDIUM] `clean_xml_number_value/1` defined in schema module but never called from it — duplicate of view helper

File: lib/api_server/vx/vx_abl_record.ex:63-70

Description: `clean_xml_number_value/1` is defined in `ApiServer.Vx.VXAblRecord` but is not referenced anywhere in the codebase from the model layer. An identical function is independently defined in `ApiServerWeb.VXAblRecordView` (lib/api_server_web/views/vx_abl_record_view.ex:37-44). The model-layer copy is dead code. The duplication means bug fixes or behaviour changes must be applied in two places. The function's presence in the schema module also constitutes a leaky abstraction — presentation-layer utility logic (nil-to-zero coercion for display) has leaked into a persistence module.

---

**B009-3** — [MEDIUM] `clean_xml_value/1` duplicated between schema module and view module

File: lib/api_server/vx/vx_abl_record.ex:54-61 (and lib/api_server_web/views/vx_abl_record_view.ex:28-35)

Description: `clean_xml_value/1` is defined identically in both `ApiServer.Vx.VXAblRecord` and `ApiServerWeb.VXAblRecordView`. The schema module's copy is used internally within `expand_xml_to_struct/1`, while the view module's copy is used by the view. There is no shared helper module; the duplication means logic for treating `%{}` (XmlToMap's representation of an empty XML element) as `nil` must be maintained in two places. This is a leaky abstraction — the XML parsing quirk of `XmlToMap.naive_map/1` is embedded and duplicated across layers rather than isolated in one place.

---

**B009-4** — [MEDIUM] Dead branch in `expand_xml_to_struct/1` — both arms of `if` return identical value

File: lib/api_server/vx/vx_abl_record.ex:80-84

Description: Inside the `{value, _}` clause of the `case Integer.parse(...)` block, the code reads:

```elixir
if length(Integer.digits(value)) >= 10 do
  value
else
  value
end
```

Both the `if` branch and the `else` branch return `value` unchanged. The condition (`>= 10`) is never acted upon. This is dead/unreachable logic — the intent was presumably to differentiate between hardware IDs with 10 or more digits and shorter ones (e.g., treating long IDs differently), but the implementation was never completed. This constitutes dead code and a latent correctness bug if the distinction was intended to produce different outputs.

---

**B009-5** — [LOW] `generate_service/10` defined in schema module — business logic leaks into schema layer

File: lib/api_server/vx/vx_abl_record.ex:31-52

Description: `generate_service/10` is not called from any module in the codebase (confirmed by search — no call site other than the definition exists). The function contains business logic: it constructs an XML document, assembles a changeset map, and calls `Vx.create_abl_record/2`. Placing this orchestration function in the Ecto schema module violates the separation between persistence schema and business/context logic. The function is also a dead-code candidate if the service record flow was migrated to `ApiServerWeb.VXAblRecordController.generate_service_record/3` (lib/api_server_web/controllers/vx_abl_record_controller.ex:66). The controller function appears to cover the same concern without calling this schema-layer version.

---

**B009-6** — [LOW] `ablcustcode` field defined in schema but excluded from `changeset/2` cast list

File: lib/api_server/vx/vx_abl_record.ex:10, 27

Description: The schema defines `:ablcustcode` as a field, but the `changeset/2` function's cast list omits it:

```elixir
|> cast(attrs, [:abldatetime,:abluser,:abllogtype,:ablusragnt,:ablip_address,:abltable,
                :ablaction,:ablimagetype,:ablimage,:ablprocessed])
```

The field is written directly via raw map literals in callers (e.g., `utility_controller.ex:5590`, `5642`, `6008`), bypassing the changeset. This is inconsistent — other fields written by the same callers are also in the cast list. The exclusion means `:ablcustcode` can never be set or validated through the changeset path, and any future attempt to use the changeset to set this field will silently drop the value.

---

**B009-7** — [MEDIUM] `VXCustomer.changeset/2` called with 3 arguments at one call site

File: lib/api_server/vx/vx.ex:2966 (caller); lib/api_server/vx/vx_customer.ex:43 (definition)

Description: `VXCustomer.changeset/2` is defined with exactly two parameters: `(vx_customer, attrs)`. However, `vx.ex:2966` calls it as:

```elixir
VXCustomer.changeset(vx_customer, %{}, prefix: customer)
```

This passes a third argument (a keyword list `[prefix: customer]`) that the function signature does not accept. In Elixir this results in a `FunctionClauseError` at runtime (no matching clause for arity 3). This is a latent runtime crash bug on any code path that calls `change_vx_customer/2`. The compiler does not catch arity mismatches on non-anonymous function calls at compile time when they are in separate modules.

---

**B009-8** — [LOW] `cond do ... true ->` used where `if/else` or simple `case` would be clearer

File: lib/api_server/vx/vx_abl_record.ex:55-60, 64-69

Description: `clean_xml_value/1` and `clean_xml_number_value/1` both use `cond do` with only two branches, the second of which is the unconditional `true ->` catch-all. The idiomatic Elixir form for a two-branch conditional is `if/else` or a two-clause function with pattern matching. Using `cond` for binary conditions is a style inconsistency vs. the rest of the codebase and adds cognitive overhead. This pattern is also duplicated in `VXAblRecordView` (lines 29-34 and 38-43), amplifying the inconsistency.

---

**B009-9** — [LOW] `aaacustcode` generated by reversing the customer name — likely incorrect business logic

File: lib/api_server/vx/vx_customer.ex:36

Description: The customer code is generated as:

```elixir
String.upcase(String.slice(String.replace(String.reverse(customer_json["name"]), " ", ""), 0..8))
```

This reverses the customer name string before removing spaces and taking the first 9 characters. For example, a customer named `"Acme Corp"` becomes `"PROC"` + first chars of reversed-no-spaces string `"PROCEMCA"` → `"PROCEMCA"` (9 chars). The reversal is almost certainly unintentional — a typical short-code derivation takes characters from the start of the name, not the end. If intentional it is entirely undocumented. The nested one-liner is also difficult to read and test. This constitutes either a logic bug or a documentation gap, and in either case is a code quality concern.

---

**B009-10** — [INFO] `VXAccessFob` schema module defines no changeset function

File: lib/api_server/vx/vx_access_fob.ex:4-11

Description: Unlike all other schema modules in the `vx/` subdirectory (`VXAblRecord`, `VXCustomer`, `VXFleet`, `VXUser`, `VXThing`), `VXAccessFob` defines no `changeset/2` function. The context module (`vx.ex`) performs deletes and reads of access fobs but no inserts or updates through a changeset, suggesting fob records are managed externally. This is not necessarily a defect, but the asymmetry with every other schema module in the directory is worth noting for future maintainability.

---

**B009-11** — [LOW] Inconsistent indentation style: `VXAccessFob` uses 4-space indentation; `VXCustomer` and `VXFleet` use 2-space

File: lib/api_server/vx/vx_access_fob.ex (4-space); lib/api_server/vx/vx_customer.ex and lib/api_server/vx/vx_fleet.ex (2-space)

Description: `vx_access_fob.ex` uses 4-space indentation throughout the module body (lines 5-10), while `vx_customer.ex` and `vx_fleet.ex` use 2-space indentation, which is the Elixir community standard enforced by `mix format`. The inconsistency suggests `vx_access_fob.ex` has never been passed through `mix format`. While purely cosmetic, it signals the file may also be out of compliance with other formatter rules.

---

## Summary Table

| ID | Severity | Title | File | Line(s) |
|----|----------|-------|------|---------|
| B009-1 | LOW | Unused `require` directives in schema module | vx_access_fob.ex | 1-2 |
| B009-2 | MEDIUM | `clean_xml_number_value/1` dead in model layer — duplicate of view helper | vx_abl_record.ex | 63-70 |
| B009-3 | MEDIUM | `clean_xml_value/1` duplicated between schema and view modules | vx_abl_record.ex | 54-61 |
| B009-4 | MEDIUM | Dead branch — both `if`/`else` arms return same value in `expand_xml_to_struct/1` | vx_abl_record.ex | 80-84 |
| B009-5 | LOW | `generate_service/10` is dead code and business logic in schema module | vx_abl_record.ex | 31-52 |
| B009-6 | LOW | `:ablcustcode` schema field excluded from `changeset/2` cast list | vx_abl_record.ex | 10, 27 |
| B009-7 | MEDIUM | `VXCustomer.changeset/2` called with 3 args — latent runtime crash | vx_customer.ex | 43 (caller: vx.ex:2966) |
| B009-8 | LOW | `cond do` used for binary conditions — `if/else` is idiomatic | vx_abl_record.ex | 55-60, 64-69 |
| B009-9 | LOW | Customer code generated by reversing name — likely incorrect logic | vx_customer.ex | 36 |
| B009-10 | INFO | `VXAccessFob` is only schema module without a `changeset/2` function | vx_access_fob.ex | 4-11 |
| B009-11 | LOW | 4-space indentation in `vx_access_fob.ex` vs 2-space in all other files | vx_access_fob.ex | 5-10 |
# Pass 4 – B010

**Date:** 2026-02-27
**Audit run:** 2026-02-27-01
**Auditor:** B010

**Files reviewed:**
- `lib/api_server/vx/vx_fleet_association.ex`
- `lib/api_server/vx/vx_rayven_message_log.ex`
- `lib/api_server/vx/vx_rayven_stream_status.ex`
- `lib/api_server/vx/vx_rental.ex`

---

## Reading Evidence

### File 1: `lib/api_server/vx/vx_fleet_association.ex`

**Module:** `ApiServer.Vx.VXFleetAssociation`

**Functions defined:**
- *(none — schema-only module)*

**Schema:** `aaf_groups_things`
**Primary key:** `{:aafid, :id, autogenerate: true}`

**Fields:**
- `:aafcustcode` — `:string`
- `:fleet` — `belongs_to ApiServer.Vx.VXFleet` (FK `:aafgroupid`, ref `:aaeid`)
- `:thing` — `belongs_to ApiServer.Vx.VXThing` (FK `:aafthingid`, ref `:aadid`)

**Top-level directives (outside `defmodule`):**
- `require Ecto.Query` (line 1)
- `require Ecto.Adapters.SQL` (line 2)

---

### File 2: `lib/api_server/vx/vx_rayven_message_log.ex`

**Module:** `ApiServer.Vx.VXRayvenMessageLog`

**Functions defined:**
| Function | Line |
|---|---|
| `changeset/2` | 16 |

**Schema:** `rayven_message_log`
**Primary key:** `{:message_id, :id, autogenerate: true}`

**Fields:**
- `:message_direction` — `:string`
- `:message_type` — `:string`
- `:hardware_id` — `:integer`
- `:event_id` — `:integer`
- `:response` — `:string`
- `:message` — `:string`
- `:created` — `:utc_datetime`

**`changeset/2` casts:** `:message_direction`, `:message_type`, `:hardware_id`, `:event_id`, `:response`, `:message`
*(Note: `:created` is NOT cast)*

---

### File 3: `lib/api_server/vx/vx_rayven_stream_status.ex`

**Module:** `ApiServer.Vx.VXRayvenStreamStatus`

**Functions defined:**
| Function | Line |
|---|---|
| `changeset/2` | 17 |

**Schema:** `rayven_stream_status`
**Primary key:** `{:id, :id, autogenerate: true}`

**Fields:**
- `:thing_id` — `:integer`
- `:hardware_id` — `:integer`
- `:last_event` — `:integer`
- `:last_event_time` — `:utc_datetime`
- `:streamed_at` — `:utc_datetime`
- `:delay` — `:integer`
- `:num_remaining` — `:integer`
- `:batch` — `:integer`

**`changeset/2` casts:** all eight fields above

---

### File 4: `lib/api_server/vx/vx_rental.ex`

**Module:** `ApiServer.Vx.VXRental`

**Functions defined:**
| Function | Visibility | Line |
|---|---|---|
| `get_all_anniversaries_between_dates/4` | public | 24 |
| `get_all_subsequent_anniversaries/5` | private | 77 |
| `get_current_rental_period_start/2` | public | 112 |
| `calculate_period_end_date/3` | public | 119 |
| `has_anniversary_on_day?/3` | public | 146 |
| `changeset/2` | public | 158 |
| `generate_next_period_anniversay/3` | private | 176 |
| `generate_previous_period_anniversay/3` | public | 246 |
| `calculate_period_start_date/3` | private | 468 |

**Schema:** `abh_rentals`
**Primary key:** `{:abhid, :id, autogenerate: true}`

**Fields:**
- `:abhcustcode` — `:string`
- `:abhclient` — `:string`
- `:abhstartdate` — `:date`
- `:abhenddate` — `:date`
- `:abhtransdate` — `:utc_datetime`
- `:abhnotes` — `:string`
- `:abhrental_freq` — `:string`
- `:abhallowed_hours` — `:integer`
- `:abhreport_freq` — `:string`
- `:abhcustomerid` — `:integer`
- `:period_calculation` — `:string`
- `:customer` — `has_one ApiServer.Vx.VXCustomer` (FK `:aaaid`, ref `:abhcustomerid`)
- `:thing` — `belongs_to ApiServer.Vx.VXThing` (FK `:abhthingid`, ref `:aadid`)

**`changeset/2` casts:** `:abhid`, `:abhclient`, `:abhcustomerid`, `:abhthingid`, `:abhstartdate`, `:abhenddate`, `:abhtransdate`, `:abhnotes`, `:abhrental_freq`, `:abhallowed_hours`, `:abhreport_freq`, `:period_calculation`
*(Note: `:abhcustcode` is NOT cast)*

---

## Findings

---

**B010-1** — [LOW] Commented-out code: superseded pipeline in `generate_previous_period_anniversay/3`

File: `lib/api_server/vx/vx_rental.ex:274`

Description: Lines 274–278 contain a five-line commented-out Elixir pipeline that was replaced by the `case rental.abhenddate` block immediately above it. The comment `# rental_end_datetime = rental.abhenddate ...` preserves the old implementation inline. Commented-out code creates noise, obscures intent, and should be removed; version history in git serves this purpose.

```elixir
        # rental_end_datetime = rental.abhenddate
        #   |> NaiveDateTime.new(~T[23:59:59])
        #   |> elem(1)
        #   |> Timex.to_datetime(user_timezone)
        #   |> Timex.beginning_of_day
```

---

**B010-2** — [LOW] Commented-out code: old `nil` return value with inline rationale

File: `lib/api_server/vx/vx_rental.ex:240`

Description: Line 240 contains `# nil # Nothing to return, this new anniversary falls outside of the rental` — a commented-out expression that was the prior return value of `generate_next_period_anniversay/3` before the logic was changed to return `rental_end_datetime`. The adjacent comment "Old code returned nothing?" (line 239) confirms this is vestigial. Should be deleted.

```elixir
      # Old code returned nothing?
      # nil # Nothing to return, this new anniversary falls outside of the rental
```

---

**B010-3** — [LOW] Commented-out code: removed format/parse chain in WEEKLY branch of `generate_previous_period_anniversay/3`

File: `lib/api_server/vx/vx_rental.ex:389`

Description: In the `"WEEKLY"` → `"CONTRACT"` path of `generate_previous_period_anniversay/3`, lines 389, 391–392, 395, and 398 are commented-out code fragments from an earlier implementation that used `Timex.format("{D}")` and `Integer.parse` to extract day-of-week, since replaced by `Timex.weekday/1`. Interleaving live and dead code around active pipeline steps significantly harms readability.

```elixir
              rental_start_day = rental_start_date
                # |> Timex.format("{D}")
                |> Timex.weekday()
                # |> Timex.day
              # {rental_start_day, _} = Integer.parse(rental_start_day)

              anniversary_day = current_anniversary
                # |> Timex.format("{D}")
                |> Timex.weekday()
              # {anniversary_day, _} = Integer.parse(anniversary_day)
```

---

**B010-4** — [LOW] Commented-out code: superseded `Timex.set` calls in `calculate_period_start_date/3`

File: `lib/api_server/vx/vx_rental.ex:517`

Description: Lines 517 and 542 both contain `# Timex.set(check_datetime, [day: 1])`, which is the old calendar-reset implementation now replaced by `Timex.beginning_of_month/1`. Two occurrences in two symmetrical `cond` branches. Should be deleted.

```elixir
                # Timex.set(check_datetime, [day: 1])
                check_datetime = Timex.beginning_of_month(check_datetime)
```

---

**B010-5** — [MEDIUM] Duplicate `case` branches — `"CALENDAR"` and `_` are identical in `get_all_anniversaries_between_dates/4`

File: `lib/api_server/vx/vx_rental.ex:37`

Description: The `case rental.period_calculation do` at line 37 has two branches — `"CALENDAR"` (lines 38–54) and `_` (lines 55–71) — that contain byte-for-byte identical logic (a three-clause `cond` calling `calculate_period_start_date` / `generate_next_period_anniversay`). The `"CALENDAR"` distinction is therefore completely inoperative: the same code path executes regardless. This is either dead differentiation (the `"CALENDAR"` branch should eventually differ from `_` but does not yet) or a copy-paste mistake. In either case the code misleads readers into believing `period_calculation` affects this function, and the compiler will warn about the always-matching catch-all.

```elixir
    first_anniversary =
      case rental.period_calculation do
        "CALENDAR" ->
          something = cond do ... end   # identical body
          something
        _ ->
          something = cond do ... end   # identical body
          something
      end
```

---

**B010-6** — [LOW] Build warning: variable re-binding that Elixir will flag as unused in `generate_previous_period_anniversay/3` and `calculate_period_start_date/3`

File: `lib/api_server/vx/vx_rental.ex:340` (and 430, 527, 551)

Description: In multiple `if` expressions, a variable is bound in the truthy branch by reassigning an outer binding, then immediately returned. Elixir treats each `if` branch as a new scope; the inner binding shadows the outer one but the compiler issues a "variable X is unused" warning for the outer binding when the inner branch is taken. Concrete examples:

- Lines 339–344: `previous_anniversary` rebound to `rental_start_datetime` inside `if`, then returned.
- Lines 429–434: same pattern for the `"WEEKLY"` path.
- Lines 527–530 and 551–555: `check_datetime` rebound inside `if` within `calculate_period_start_date/3`.

The idiomatic Elixir pattern is to use the `if` expression's return value directly rather than rebinding, e.g. `previous_anniversary = if ... do rental_start_datetime else previous_anniversary end`.

---

**B010-7** — [LOW] Typo in public function name: `generate_previous_period_anniversay` (missing 'r')

File: `lib/api_server/vx/vx_rental.ex:246`

Description: The public function is named `generate_previous_period_anniversay` (missing the letter `r` — should be `anniversary`). The same typo exists in the private companion `generate_next_period_anniversay` (line 176). Because both spellings are used consistently across all call sites (`vx.ex`, `vx_rental_controller.ex`, `utility_controller.ex`), there is no runtime defect today. However the misspelling is part of the public API surface of this module and will require a coordinated rename across at least six files to correct. The typo was present from initial authorship and has been compounded by widespread adoption.

---

**B010-8** — [MEDIUM] `generate_previous_period_anniversay/3` is declared `def` (public) but the symmetrical `generate_next_period_anniversay/3` is `defp` (private)

File: `lib/api_server/vx/vx_rental.ex:246` vs `176`

Description: `generate_next_period_anniversay/3` is private (`defp`, line 176), while `generate_previous_period_anniversay/3` is public (`def`, line 246). Call-site analysis shows that `generate_previous_period_anniversay/3` is called externally from `vx.ex`, `vx_rental_controller.ex`, and `utility_controller.ex`, so making it public is intentional. However, `generate_next_period_anniversay/3` is also called by public functions within this module and may be needed publicly in future. This asymmetry in visibility between two directly analogous functions is a leaky abstraction concern: internal period-stepping logic is published selectively, pushing callers toward a one-directional iteration API that requires them to call the public `get_all_anniversaries_between_dates/4` for forward movement but the internal-step function directly for backward movement. The boundary between public and private API is inconsistent.

---

**B010-9** — [LOW] `require` directives outside the module in `vx_fleet_association.ex`

File: `lib/api_server/vx/vx_fleet_association.ex:1`

Description: Lines 1–2 place `require Ecto.Query` and `require Ecto.Adapters.SQL` at the top level, outside the `defmodule` block. Neither macro is used anywhere in this file (there are no queries, no raw SQL). The module contains only a schema definition with `use Ecto.Schema`. Placing `require` outside `defmodule` pollutes the compilation environment and generates build warnings about unused macros. The pattern appears copy-pasted from sibling schema files (`vx_thing.ex`, `vx_user.ex`, `vx_access_fob.ex`) that do define query functions, where the `require` is equally misplaced outside their modules.

---

**B010-10** — [LOW] Trailing whitespace on `@primary_key` line in `vx_fleet_association.ex`

File: `lib/api_server/vx/vx_fleet_association.ex:7`

Description: Line 7 ends with two trailing space characters after the closing `}` of the `@primary_key` attribute: `@primary_key {:aafid, :id, autogenerate: true}  `. While not a runtime defect, trailing whitespace causes noisy diffs and is inconsistent with all other `@primary_key` declarations in the codebase.

---

**B010-11** — [LOW] Misindented closing `end` of module in `vx_rayven_message_log.ex` and `vx_rayven_stream_status.ex`

File: `lib/api_server/vx/vx_rayven_message_log.ex:20` and `lib/api_server/vx/vx_rayven_stream_status.ex:21`

Description: In both files the closing `end` of the `defmodule` block is indented by two spaces (`  end`) rather than being at column 0. This indentation implies the `end` closes a nested construct (e.g. an inner module or a `do` block), which it does not. The internal `use`, `import`, `schema`, and `def` lines are indented with four spaces relative to the module — suggesting the file was written as if the module were nested inside another, then the outer container was removed without adjusting indentation. `vx_rental.ex` uses correct 2-space indentation (module body at 2 spaces, `end` at column 0), demonstrating the inconsistency across the file set.

---

**B010-12** — [LOW] Inconsistent indentation style across the four files

File: (all four files)

Description: The four files use three different indentation styles for module body members:

| File | `use`/`import` indent | `schema` fields indent | `def` body indent |
|---|---|---|---|
| `vx_fleet_association.ex` | 4 spaces | 8 spaces | (no functions) |
| `vx_rayven_message_log.ex` | 4 spaces | 8 spaces | 6 spaces (2 inside 4-space `def`) |
| `vx_rayven_stream_status.ex` | 4 spaces | 8 spaces | 6 spaces |
| `vx_rental.ex` | 2 spaces | 4 spaces | 4 spaces |

`vx_rental.ex` follows the Elixir community convention of 2-space indentation. The other three files use 4-space indentation for the module body, doubling to 8 for schema contents. This divergence indicates the files were authored in different editors without a shared `.editorconfig` or `mix format` enforcement.

---

**B010-13** — [LOW] CRLF line endings in all four files

File: (all four files)

Description: All four files use Windows-style CRLF (`\r\n`) line endings. This is inconsistent with the Elixir/Mix ecosystem convention of LF-only line endings and will cause spurious whitespace diffs in cross-platform development. A `.gitattributes` rule (`*.ex text eol=lf`) is absent or not enforced.

---

**B010-14** — [LOW] `changeset/2` in `vx_rayven_message_log.ex` does not cast the `created` field

File: `lib/api_server/vx/vx_rayven_message_log.ex:18`

Description: The schema declares `field :created, :utc_datetime` (line 13) but `changeset/2` casts only `:message_direction`, `:message_type`, `:hardware_id`, `:event_id`, `:response`, and `:message` — omitting `:created`. If the application ever writes this field through the changeset path it will be silently ignored. The field exists to record when a message was logged; it is likely intended to be set at insert time. The omission may be intentional (set via `Repo.insert` with explicit field override) but is not documented and is inconsistent with how similar timestamp fields are treated elsewhere.

---

**B010-15** — [MEDIUM] Incomplete `case` clause in `calculate_period_start_date/3` for `"MONTHLY"` frequency — no catch-all for `period_calculation`

File: `lib/api_server/vx/vx_rental.ex:512`

Description: When `rental.abhrental_freq` is `"MONTHLY"`, the code switches on `rental.period_calculation` with only two branches: `"CALENDAR"` and `"CONTRACT"` (lines 512–535 and 539–562). There is no catch-all (`_`) clause. If `period_calculation` is `nil` or any value other than these two strings, Elixir will raise a `CaseClauseError` at runtime. Given that `period_calculation` is a free-form string field with no validation in `changeset/2` and the database schema imposes no constraint, this represents a realistic crash vector. The same pattern appears in `rental_day <= check_day` and `rental_day > check_day` branches at lines 512 and 537 respectively.

---

**B010-16** — [INFO] Intermediate `something` and `return_me` variables are unnecessary

File: `lib/api_server/vx/vx_rental.ex:39`, `56`, `280`, `365`, `191`, `205`, `282`, `368`

Description: Throughout `vx_rental.ex`, intermediate variables named `something` and `return_me` are assigned the result of a `cond` or `case` expression and then immediately returned as the last expression of the enclosing clause. In Elixir, `case`, `cond`, and `if` are expressions whose value can be used directly without an intermediate binding. The pattern `something = cond do ... end; something` is idiomatic in imperative languages but is redundant in Elixir and adds visual noise. This is a style issue only; it does not affect correctness or performance.

---

**B010-17** — [LOW] Unchecked pattern match on error tuple in `get_all_anniversaries_between_dates/4`

File: `lib/api_server/vx/vx_rental.ex:25`

Description: Lines 25–26 destructure the result of `NaiveDateTime.new/2` using `{_, to_datetime}` and `{_, from_datetime}`, silently discarding the first element (`:ok` or `:error`). `NaiveDateTime.new/2` can return `{:error, :invalid_date}` for invalid combinations (e.g. February 30). Using `{_, ...}` in a match means an error tuple would still match (binding `from_datetime` to `:invalid_date`) and propagate a nonsense value into Timex calls. The safer pattern is to match `{:ok, to_datetime}` and handle the error case explicitly, or use `NaiveDateTime.new!/2` which raises on error (consistent with the `Date.from_iso8601!/1` bang-function used on the same lines).

---

## Summary Table

| ID | Severity | Title | File |
|---|---|---|---|
| B010-1 | LOW | Commented-out superseded pipeline | `vx_rental.ex:274` |
| B010-2 | LOW | Commented-out old `nil` return | `vx_rental.ex:240` |
| B010-3 | LOW | Commented-out format/parse chain in WEEKLY branch | `vx_rental.ex:389` |
| B010-4 | LOW | Commented-out superseded `Timex.set` calls | `vx_rental.ex:517` |
| B010-5 | MEDIUM | Identical `"CALENDAR"` and `_` branches — period_calculation check is inoperative | `vx_rental.ex:37` |
| B010-6 | LOW | Variable re-binding causes compiler "unused variable" warnings | `vx_rental.ex:340` |
| B010-7 | LOW | Typo in public function name: `anniversay` → `anniversary` | `vx_rental.ex:246` |
| B010-8 | MEDIUM | Asymmetric visibility: `generate_previous` is public, `generate_next` is private | `vx_rental.ex:176,246` |
| B010-9 | LOW | `require` directives placed outside `defmodule`; macros unused in file | `vx_fleet_association.ex:1` |
| B010-10 | LOW | Trailing whitespace on `@primary_key` line | `vx_fleet_association.ex:7` |
| B010-11 | LOW | Module-closing `end` incorrectly indented by 2 spaces in two files | `vx_rayven_message_log.ex:20`, `vx_rayven_stream_status.ex:21` |
| B010-12 | LOW | Inconsistent indentation style across all four files (2-space vs 4-space) | all four files |
| B010-13 | LOW | CRLF line endings in all four files | all four files |
| B010-14 | LOW | `created` field not cast in `VXRayvenMessageLog.changeset/2` | `vx_rayven_message_log.ex:18` |
| B010-15 | MEDIUM | Incomplete `case` on `period_calculation` — no catch-all, runtime crash risk | `vx_rental.ex:512` |
| B010-16 | INFO | Unnecessary `something`/`return_me` intermediate variables | `vx_rental.ex` (multiple) |
| B010-17 | LOW | Unchecked `{_, ...}` match on `NaiveDateTime.new/2` error tuple | `vx_rental.ex:25` |
# Pass 4 – B011

**Date:** 2026-02-27
**Audit run:** 2026-02-27-01

**Files reviewed:**
- `lib/api_server/vx/vx_restriction.ex`
- `lib/api_server/vx/vx_thing.ex`
- `lib/api_server/vx/vx_thing_event.ex`
- `lib/api_server/vx/vx_thing_event_omega.ex`

---

## Reading Evidence

### File: `lib/api_server/vx/vx_restriction.ex`

**Module:** `ApiServer.Vx.VXRestriction`

**Uses / Imports:**
- `use Ecto.Schema`
- `import Ecto.Changeset`

**Schema:** `"aau_rest"`
- Primary key: `{:aauid, :id, autogenerate: true}`
- Fields: `:aaucharval` (string), `:aaucustcode` (string), `:aaufun` (string), `:aaunumval` (integer)
- Association: `belongs_to :user, ApiServer.Vx.VXUser, foreign_key: :aauuser_id, references: :aacid`

**Functions:**

| Name | Line |
|---|---|
| `changeset/2` | 16 |

**Types / Constants / Errors defined:** none

---

### File: `lib/api_server/vx/vx_thing.ex`

**Module:** `ApiServer.Vx.VXThing`

**Top-level directives (outside defmodule):**
- `require Ecto.Query` (line 1)
- `require Ecto.Adapters.SQL` (line 2)

**Uses / Imports / Aliases (inside defmodule):**
- `use Ecto.Schema`
- `import Ecto.Changeset`
- `alias ApiServer.Vx`

**Schema:** `"aad_thing"`
- Primary key: `{:aadid, :id, autogenerate: true}`
- Fields: `:aadcustcode`, `:aaddesc`, `:aadintext`, `:aadaddr`, `:aadcustomerid`, `:aadcat`, `:aadhardwareid`, `:aadhw_type`, `:aadmake`, `:aadmodel`, `:aadserialno`, `:aadmobile`, `:aadimei`, `:aadhourmeter`, `:aadhourmeter1`, `:aadhourmeter2`, `:aadhourmeter3`, `:aadhourmeter4`, `:aadhourmeterprnt`, `:aadodometer`, `:aadhourmeteromega`, `:aadhourmeterothcan`, `:aaddateintoservice`, `:aadlastservice`, `:aadvalid`, `:aadserviceoffset`, `:aadsvchrs`, `:aadrange_lat`, `:aadrange_long`, `:aadrange_dist`, `:aadrange_unit`, `:service_calculation_input`, `:reference_1`, `:reference_2`, `:reference_3`, `:notes`, `:equipment_date_into_service`
- Associations: `has_many :fleet_thing_joins`, `has_many :rentals`, `has_many :events`, `has_one :summary`, `has_one :info`, `has_one :customer`

**Functions:**

| Name | Line |
|---|---|
| `convert_json_to_changeset/1` | 60 |
| `changeset/2` | 75 |

**Types / Constants / Errors defined:** none

---

### File: `lib/api_server/vx/vx_thing_event.ex`

**Module:** `ApiServer.Vx.VXThingEvent`

**Uses / Imports:**
- `use Ecto.Schema`
- `import Ecto.Changeset`

**Schema:** `"thingevents"` (no explicit primary key declaration; default Ecto integer `:id` applies)
- Fields: `:gmtdatetime`, `:hardwareid`, `:eventtype`, `:eventcode`, `:latitude`, `:longitude`, `:driverid`, `:engineonelapsed`, `:totalengineseconds`, `:custcode`, `:hardwaretype`, `:datetimesaved`, `:dateinqueue`, `:timeoffix`, `:altitude`, `:heading`, `:speed`, `:rssi`, `:gpsfixquality`, `:odometer`, `:mifaredriverid`, `:ignition`, `:ignitionstatus`, `:calcengineseconds`, `:input1elapsed`, `:input1status`, `:input1totalseconds`, `:input1calctotalseconds`, `:input2elapsed`, `:input2status`, `:input2totalseconds`, `:input2calctotalseconds`, `:input3elapsed`, `:input3status`, `:input3totalseconds`, `:input3calctotalseconds`, `:input4elapsed`, `:input4status`, `:input4totalseconds`, `:input4calctotalseconds`, `:prntelapsed`, `:prntstatus`, `:prnttotalseconds`, `:prntcalctotalseconds`, `:rhmprestartchecklist`, `:geofence`
- Commented-out field: `# field :llpoint, Geo.Point` (line 52)
- Associations: `has_one :thingeventomega`, `belongs_to :thing`

**Functions:**

| Name | Line |
|---|---|
| `map_xml/1` | 71 |
| `changeset/2` | 111 |

**Types / Constants / Errors defined:** none

---

### File: `lib/api_server/vx/vx_thing_event_omega.ex`

**Module:** `ApiServer.Vx.VXThingEventOmega`

**Uses / Imports:**
- `use Ecto.Schema`
- `import Ecto.Changeset`

**Schema:** `"thingomega"` (no explicit primary key declaration)
- Fields: `:accelerometerx`, `:accelerometery`, `:accelerometerz`, `:distancesincelastevent`, `:omegadriverid`, `:seatbelt`, `:seated`, `:parkbrakerequest`, `:parkbreakreleased`, `:vehicleload`, `:tilt`, `:height`, `:overload`, `:attretracted`, `:yellowled`, `:redled`, `:greenled`, `:liftenable`, `:safetyoverride`, `:doorclosed`, `:parkbrakerror`, `:batterynotcharged`, `:lowengineoil`, `:accnotcharged`, `:hydraulicfilgerblocked`, `:airfilterblocked`, `:attpressure`, `:oilcoolerfan`, `:lowerinterruption`, `:undersafetyheight`, `:joystickliftposition`, `:hydraulicoiltemperature`, `:md3temperature`, `:fuellevel`, `:md3status`, `:xa2status`, `:batteryvoltage`, `:xa2temperature`, `:boomangle`, `:boomextension`, `:lift`, `:extension`, `:totalfuelconsumption`, `:fuelrate`, `:totalfuelidle`, `:totalidlehour`, `:totalenginehour`, `:enginerpm`, `:capacity`, `:coolanttemperature`, `:oiltemperature`, `:engineerrorcode`, `:vehiclespeed`, `:gearselection`, `:transerrorcode`, `:prestartchecklist`, `:truckerrorcode`, `:mc43status`, `:mc43temperature`, `:lc5status`, `:lc5temperature`, `:truckangle`
- Association: `belongs_to :thingevent, ApiServer.Vx.VXThingEvent, foreign_key: :id, references: :id, primary_key: true, define_field: false`

**Functions:**

| Name | Line |
|---|---|
| `changeset/2` | 72 |

**Types / Constants / Errors defined:** none

---

## Findings

---

**B011-1** — [LOW] Commented-out schema field (`field :llpoint`)
File: `lib/api_server/vx/vx_thing_event.ex:52`
Description: The line `# field :llpoint, Geo.Point` is a commented-out schema field. It indicates an intention to store a PostGIS/Geo point that was never completed or was abandoned. Commented-out code clutters the schema and leaves ambiguity about whether this field exists in the database table. If the column does exist in the DB, the schema is silently incomplete; if it does not, the comment is noise. This should either be implemented or removed.

---

**B011-2** — [LOW] Commented-out code block inside `map_xml/1`
File: `lib/api_server/vx/vx_thing_event.ex:103–106`
Description: Lines 103–106 are commented-out map keys inside the return map of `map_xml/1`:
```elixir
# driverid: data[], #
# mifaredriverid: data[], #
# calcengineseconds: data[], # need the thing record for this one
# input1calctotalseconds: data[], # need the thing record for this one
```
These represent four fields declared in the schema that are never populated by `map_xml/1`. The inline comments ("need the thing record for this one") indicate incomplete business logic. The `:driverid` field is mapped via an interpolation workaround (`"#{data["driverid"]}"`) at line 88 rather than being removed from this comment, making the comment actively misleading. Commented-out code with unfinished notes is a LOW finding and indicates deferred work that is invisible at runtime.

---

**B011-3** — [LOW] Commented-out code block inside `calamp_controller.ex` references incomplete `map_xml/1` flow
File: `lib/api_server/vx/vx_thing_event.ex:71` (related: `lib/api_server_web/controllers/calamp_controller.ex:22–25`)
Description: The `map_xml/1` function is only called from `calamp_controller.ex`, where the controller itself contains additional commented-out steps (steps 3 and 4 of the processing pipeline are commented out). This means `map_xml/1` feeds a partially implemented pipeline. While the finding is directly reported on the schema file here for the incomplete field population, the broader context is that `map_xml/1` is integrated into dead/incomplete controller logic. The `IO.inspect` call at `calamp_controller.ex:10` also evidences debug code left in production paths.

---

**B011-4** — [MEDIUM] `require Ecto.Query` and `require Ecto.Adapters.SQL` are outside `defmodule` and unused
File: `lib/api_server/vx/vx_thing.ex:1–2`
Description: Lines 1 and 2 place `require Ecto.Query` and `require Ecto.Adapters.SQL` at the top level of the file, outside the `defmodule ApiServer.Vx.VXThing do` block. Neither macro is used anywhere in the module body — the module only uses `Ecto.Schema` (via `use`) and `Ecto.Changeset` (via `import`). `require` at the file's top level applies to the file's compile context but does not make the macros available inside the module in the standard way Elixir intends. The compiler will emit warnings for unused `require` directives. This is a build-warning-class finding and represents leftover scaffolding. Severity is MEDIUM because placing `require` outside `defmodule` is an unusual pattern that can confuse readers into thinking the module has SQL/query capabilities it does not exercise.

---

**B011-5** — [MEDIUM] `[REDACTED-AWS-SMTP-PASSWORD]` schema field missing from `changeset/2` cast list
File: `lib/api_server/vx/vx_thing_event_omega.ex:9` and `72–76`
Description: The field `:distancesincelastevent` is declared in the schema at line 9 but is entirely absent from the `cast/3` call in `changeset/2` (line 74). As a result, this field can never be set or updated via the changeset. The field is read by the view layer (`vx_thing_event_view.ex`) and so must contain meaningful data; however the only path to populate it is through direct database insertion (bypassing the changeset). This is a silent data integrity gap: callers using `changeset/2` to upsert records will silently drop any `:distancesincelastevent` value passed in `attrs`. Severity MEDIUM because it causes silent data loss on the write path.

---

**B011-6** — [LOW] Typo in field name `parkbreakreleased` (should be `parkbrakereleased`)
File: `lib/api_server/vx/vx_thing_event_omega.ex:14`
Description: The field is named `:parkbreakreleased` (line 14), mixing "brake" (the mechanical device) with "break" (as in fracture). The paired field at line 13 is `:parkbrakerequest`, which is spelled correctly. This inconsistency propagates to the view (`vx_thing_event_view.ex:28`) and the controller mapping (`utility_controller.ex:885`), meaning any API consumers now depend on the misspelled name. Renaming is a breaking change, so this is LOW rather than INFO, but it is a real maintainability defect.

---

**B011-7** — [LOW] Typo in field name `[REDACTED-AWS-SMTP-PASSWORD]` (should be `[REDACTED-AWS-SMTP-PASSWORD]`)
File: `lib/api_server/vx/vx_thing_event_omega.ex:30`
Description: The field `:hydraulicfilgerblocked` transposes "filter" into "filger". Like `parkbreakreleased`, the misspelling propagates to the view layer and the controller mapping. Any external API consumers or database column names that match this typo create a permanent coupling to the error. This is LOW for the same reasons as B011-6.

---

**B011-8** — [MEDIUM] `changeset/2` in `VXThingEventOmega` is a single unformatted line of 65 fields
File: `lib/api_server/vx/vx_thing_event_omega.ex:74`
Description: The entire `cast/3` call listing 65 atom keys is written as a single line (line 74 is extremely long). This is a style inconsistency relative to `VXThingEvent.changeset/2` (lines 112–160) which formats each field on its own line, and to `VXRestriction.changeset/2` (lines 16–20) which is also multi-line. The unformatted single-line form makes code review impractical and means the missing `:distancesincelastevent` field (finding B011-5) is nearly impossible to spot without tooling. Severity is MEDIUM because the formatting failure directly concealed the data-loss defect in B011-5.

---

**B011-9** — [LOW] `convert_json_to_changeset/1` in `VXThing` misleadingly names its return value `changeset`
File: `lib/api_server/vx/vx_thing.ex:60–73`
Description: The function assigns its result to a local named `changeset` (line 61) and returns it. However the return value is a plain `Map` built via `Vx.update_key_if_value/3` pipeline, not an `Ecto.Changeset` struct. The variable name `changeset` is therefore incorrect. Callers in `vx_thing_controller.ex` do treat it as a plain map (using `Map.has_key?` on it), but the function name and internal variable both imply Ecto changeset semantics, which is a leaky abstraction — the naming suggests the caller can pass it to `Repo.insert/2` or `Repo.update/2` directly, which would fail. Severity LOW because the misuse has not yet caused a runtime defect (callers handle it correctly), but the abstraction is misleading.

---

**B011-10** — [LOW] Style inconsistency: indentation uses 4-space indent in `VXThing`, 2-space in all other three files
File: `lib/api_server/vx/vx_thing.ex` (throughout)
Description: `vx_thing.ex` uses 4-space indentation for all code inside `defmodule` and `schema` blocks (lines 11–79). The other three files in this assignment (`vx_restriction.ex`, `vx_thing_event.ex`, `vx_thing_event_omega.ex`) all use 2-space indentation, consistent with the Elixir community standard and the `mix format` default. This inconsistency suggests `vx_thing.ex` was never run through the project formatter. Severity LOW as it does not affect runtime behavior but reduces readability and signals a gap in CI enforcement.

---

## Summary Table

| ID | Severity | File | Short Title |
|---|---|---|---|
| B011-1 | LOW | `vx_thing_event.ex:52` | Commented-out schema field `field :llpoint` |
| B011-2 | LOW | `vx_thing_event.ex:103–106` | Commented-out incomplete field mappings in `map_xml/1` |
| B011-3 | LOW | `vx_thing_event.ex:71` | `map_xml/1` feeds partially implemented / debug controller pipeline |
| B011-4 | MEDIUM | `vx_thing.ex:1–2` | `require` directives outside `defmodule` and unused (build warnings) |
| B011-5 | MEDIUM | `vx_thing_event_omega.ex:9,74` | `[REDACTED-AWS-SMTP-PASSWORD]` missing from `changeset/2` cast — silent data loss |
| B011-6 | LOW | `vx_thing_event_omega.ex:14` | Typo: `parkbreakreleased` (should be `parkbrakereleased`) |
| B011-7 | LOW | `vx_thing_event_omega.ex:30` | Typo: `[REDACTED-AWS-SMTP-PASSWORD]` (should be `[REDACTED-AWS-SMTP-PASSWORD]`) |
| B011-8 | MEDIUM | `vx_thing_event_omega.ex:74` | `changeset/2` cast list is a single unformatted 65-field line |
| B011-9 | LOW | `vx_thing.ex:61` | Return value of `convert_json_to_changeset/1` mislabeled as `changeset` |
| B011-10 | LOW | `vx_thing.ex` (throughout) | 4-space indentation inconsistent with 2-space standard in sibling files |
# Pass 4 – B012

Date: 2026-02-27
Audit run: 2026-02-27-01

Files reviewed:
- lib/api_server/vx/vx_thing_event_omega_tires.ex
- lib/api_server/vx/vx_thing_info.ex
- lib/api_server/vx/vx_thing_summary.ex
- lib/api_server/vx/vx_user.ex

---

## Reading Evidence

### lib/api_server/vx/vx_thing_event_omega_tires.ex

**Module:** `ApiServer.Vx.VXThingEventOmegaTires`

**Schema:** `"thingomegatires"` (no explicit `@primary_key`; primary key is inferred from the `belongs_to` relationship)

**Fields (all `:integer`, lines 6–53):**
- pressurewarning0–5, pressureleakage0–5, temperaturehigh0–5, receivetimeout0–5
- carbatteryvoltageexceed0–5, sensorbatteryvoltagelow0–5, tirepressure0–5, temperature0–5
(48 fields total, 8 per tire slot × 6 slots)

**Associations:**
- `belongs_to :thingevent, ApiServer.Vx.VXThingEvent` (line 55, composite primary key via `id`)

**Functions:**
- `changeset/2` — line 58

**Types/constants defined:** none

---

### lib/api_server/vx/vx_thing_info.ex

**Module:** `ApiServer.Vx.VXThingInfo`

**Schema:** `"thing_info"` with `@primary_key {:id, :id, autogenerate: true}` (line 14)

**Fields:**
- `:averageweeklyusage` — `:float` (line 16)
- `:pmnotificationid` — `:integer` (line 17)
- `:pmnotificationdate` — `:date` (line 18)
- `:usagesincenotification` — `:integer` (line 19)

**Associations:**
- `belongs_to :thing, VXThing` (line 21)

**Functions:**
- `getWithHardwareId/2` — line 24
- `service_performed/3` — line 31
- `[REDACTED-AWS-SMTP-PASSWORD]` — line 47
- `make_info_record/2` — line 57
- `update_existing_record/3` — line 74

**Types/constants defined:** none

---

### lib/api_server/vx/vx_thing_summary.ex

**Module:** `ApiServer.Vx.VXThingSummary`

**Schema:** `"abm_summary"` with `@primary_key {:abmid, :id, autogenerate: true}` (line 5)

**Fields (lines 7–44):**
- abmgmtdatetime (:utc_datetime), abmdesc (:string), abmignitionstatus (:string)
- abmeventtype (:integer), abmeventcode (:integer)
- abmtotalengineseconds, abmcalctotalengineseconds, abmtotalenginesecondssinceservice (:integer)
- abmhourmeter1–4, abmcalchourmeter1–4, abmhourmeter1–4sinceservice (:integer each)
- abmodometer, abmcalcodometer, abmodometersinceservice (:integer)
- abmlatitude, abmlongitude, abmheading, abmspeed (:float)
- abmdriverid, abmmifaredriverid, abmcustcode (:string)
- abmusagesinceservice, abmhourmeteromega, abmcalchourmeteromega (:float)
- abmhourmeterothcan, abmcalchourmeterothcan (:float)
- abmrhmprestartlastgmt (:utc_datetime), abmrhmprestartchecklist (:string)

**Associations:**
- `belongs_to :thing, ApiServer.Vx.VXThing` (line 45)

**Functions:**
- `changeset/2` — line 49
- `make_or_update_summary/3` (with default arg) — line 56
- `validate_for_hardwareid/2` — line 138
- `is_valid?/2` — line 156

**Types/constants defined:** none

---

### lib/api_server/vx/vx_user.ex

**Module:** `ApiServer.Vx.VXUser`

**Schema:** `"aac_user"` with `@primary_key {:aacid, :id, autogenerate: true}` (line 12)

**Fields (lines 14–48):**
- aaccustcode, aacuser, aacfname, aacsurname (:string)
- aaccredte, aaclastupdated, aacpwdlastupd (:utc_datetime)
- aacexpdte, aaclic1issuedate, aaclic1expdate, aaclic2issuedate, aaclic2expdate (:date)
- aacpassword, aacpasswordhash, aacpasswordresetcode (:string)
- aactz, aacfirstopt, aacemail (:string)
- aacdash, aacmaprefresh, aachourformat (:integer)
- aacuserdriver, aaclic1, aaclic1class, aaclic1issuer (:string)
- aaclic2, aaclic2class, aaclic2issuer (:string)
- aacusertype, aacproxyenabled, aactimezone, aacdeffleet (:integer) (:string×3, :integer)
- aacdateformat, aaclang, aacuom (:string)

**Associations:**
- `has_one :accessfob, ApiServer.Vx.VXAccessFob` (line 51)
- `has_one :function, ApiServer.Vx.VXUserFunction` (line 52)
- `has_many :assigned_fleets, ApiServer.Vx.VXRestriction` (line 53)
- `has_many :abl_records, ApiServer.Vx.VXAblRecord` (line 54)

**Functions:**
- `convert_json_to_changeset/1` — line 57
- `password_changeset/2` — line 73
- `changeset/2` — line 78

**Types/constants defined:** none

---

## Findings

---

**B012-1** — [LOW] Commented-out code in `[REDACTED-AWS-SMTP-PASSWORD]`

File: lib/api_server/vx/vx_thing_info.ex:49

Description: Line 49 contains `# calcfields(hardwareid, existingSummary)` — a commented-out call to a function (`calcfields`) that does not exist anywhere in the codebase. This is dead annotation left from development. It names a non-existent function and uses a variable name (`existingSummary`) inconsistent with the surrounding code (which uses `existing_info`), indicating it was never completed. Commented-out code clutters the module and can mislead future maintainers into thinking this logic is intentionally deferred.

---

**B012-2** — [HIGH] Hardcoded magic date `~D[2019-01-13]` used as bootstrap sentinel

File: lib/api_server/vx/vx_thing_info.ex:59

Description: `make_info_record/2` hardcodes `notification_date = ~D[2019-01-13]` as the PM notification date for every newly created info record. This date is then used to calculate hours of usage since that point (`fetch_actual_usage`). A fixed calendar date from 2019 embedded in application logic means all newly bootstrapped records behave as if the equipment was first notified over 7 years ago from the time of writing, producing incorrect `[REDACTED-AWS-SMTP-PASSWORD]` values for any equipment added after 2019. This is a data-correctness bug, not merely a style issue. The value should either be derived dynamically (e.g., from the equipment's first recorded event) or sourced from configuration.

---

**B012-3** — [MEDIUM] Hardcoded magic integer `12` for `pmnotificationid`

File: lib/api_server/vx/vx_thing_info.ex:66

Description: `make_info_record/2` hardcodes `pmnotificationid: 12`. No module-level constant, configuration entry, or comment explains what ID 12 represents. If the notification record it refers to is ever deleted or renumbered in the database, this silently stores a dangling foreign key or wrong reference. The value should be named (e.g., a module attribute `@default_pm_notification_id`) or sourced from configuration.

---

**B012-4** — [MEDIUM] Hardcoded epoch sentinel `~D[1970-01-01]` for "no notification" guard

File: lib/api_server/vx/vx_thing_info.ex:78

Description: `update_existing_record/3` guards against a null-like date by comparing `existing.pmnotificationdate > ~D[1970-01-01]`. Unix epoch (1970-01-01) is used as a proxy for "unset", but the schema already allows `nil` for `pmnotificationdate` (the first branch of the `cond` checks `!= nil`). The epoch check is therefore either redundant (if the DB never stores 1970-01-01) or a workaround for a database layer that returns the epoch instead of NULL — either way it is a leaky abstraction that couples application logic to a database representation detail. The logic should rely solely on `nil` checking.

---

**B012-5** — [MEDIUM] Variable `result` bound but never used in `make_or_update_summary/3`

File: lib/api_server/vx/vx_thing_summary.ex:135

Description: Line 135 assigns `result = ApiServer.Vx.update_or_insert_summary(...)` but `result` is never referenced again — the function's implicit return value is `result`, which is correct, but the binding name `result` shadows the `result` variable captured in the destructuring at line 66 (`{hardwareid_parsed, result} = ...`). The `result` from line 66 is also never used after that point. This means `{hardwareid_parsed, result}` at line 66 binds a value that is immediately discarded, and then the name `result` is reused at line 135 with a completely different meaning. Elixir will emit a compiler warning for the unused `result` from line 66. The pattern match at line 66 should use `_result` or be restructured to `{hardwareid_parsed, _}` to suppress the warning and clarify intent.

---

**B012-6** — [LOW] Variable `timestamp` bound but never used in `validate_for_hardwareid/2`

File: lib/api_server/vx/vx_thing_summary.ex:149

Description: Line 149 binds `timestamp = Timex.now()` immediately before calling `make_or_update_summary/3`, but `timestamp` is never passed to that function or referenced anywhere else in the clause. This is dead code that will produce an Elixir compiler warning ("variable timestamp is unused"). The `Timex.now()` call is also an unnecessary side-effecting operation on every update path. The line should be removed.

---

**B012-7** — [LOW] Commented-out code block — `unique_constraint` variant

File: lib/api_server/vx/vx_user.ex:85

Description: Line 85 contains `# |> unique_constraint(:aacuser, name: :aac_user_aacuser_index)` immediately below an active `unique_constraint` call on the same field with a different index name. The comment suggests the index name was changed at some point and the old constraint was left as a comment rather than removed. This creates ambiguity about which constraint name is canonical. The commented line should be deleted.

---

**B012-8** — [LOW] Commented-out code — timezone field mapping

File: lib/api_server/vx/vx_user.ex:68

Description: Line 68 contains `# |> Vx.update_key_if_value(:aactz, user_json["offset"])` inside `convert_json_to_changeset/1`. The `:aactz` field is defined in the schema (line 24) but its population from the JSON input is disabled. There is also a separate active mapping for `:aactimezone` (line 64). It is unclear whether `:aactz` is intentionally not populated from the API, or whether this is an incomplete migration from one field to another. Leaving it commented makes the intent opaque.

---

**B012-9** — [MEDIUM] Duplicate `update_key_if_value` call for `:aacuom` in `convert_json_to_changeset/1`

File: lib/api_server/vx/vx_user.ex:62,67

Description: Lines 62 and 67 both call `|> Vx.update_key_if_value(:aacuom, user_json["units"])` with identical arguments. The second call is redundant and will overwrite the first with the same value (assuming `update_key_if_value` is idempotent). Regardless of idempotency, the duplicate is likely a copy-paste error. It wastes a pipeline step and can mislead a reader into thinking the two calls do different things.

---

**B012-10** — [MEDIUM] `Float.round/2` applied twice to the same value in `make_or_update_summary/3`

File: lib/api_server/vx/vx_thing_summary.ex:124,128

Description: In the second `updated_summary` block (lines 119–133), `Float.round(thing_event.thingeventomega.totalenginehour, 2)` is computed at line 124 into `[REDACTED-AWS-SMTP-PASSWORD]`, and then at line 128 `Float.round(formattedtotalenginehour, 2)` is called again on the already-rounded value. Rounding an already-rounded float is harmless numerically but indicates the developer copied the pattern from the first block (lines 103–117) without recognising that `[REDACTED-AWS-SMTP-PASSWORD]` is already rounded. This is a code-quality defect that suggests the two blocks were written inconsistently.

---

**B012-11** — [MEDIUM] `require Ecto.Adapters.SQL` at top level outside module in `vx_user.ex`

File: lib/api_server/vx/vx_user.ex:2

Description: Lines 1–2 of `vx_user.ex` place `require Ecto.Query` and `require Ecto.Adapters.SQL` at the file's top level, outside the `defmodule` block. Neither `Ecto.Query` nor `Ecto.Adapters.SQL` is used anywhere within the `VXUser` module body (no `Ecto.Query.from`, no `Ecto.Adapters.SQL.query`, etc.). Top-level `require` directives in Elixir have module-scoping implications and produce compiler noise. The same pattern appears in `vx_thing_info.ex` where `require Ecto.Adapters.SQL` is inside the module but still unused in that file. Both requires should be removed.

---

**B012-12** — [MEDIUM] `require Ecto.Adapters.SQL` declared but never used in `vx_thing_info.ex`

File: lib/api_server/vx/vx_thing_info.ex:7

Description: `require Ecto.Adapters.SQL` is declared on line 7 inside the module, but no raw SQL execution (`Ecto.Adapters.SQL.query` or similar) is performed anywhere in the file. All database access goes through `Ecto.Query` and `Repo`. The unused `require` will cause a compiler warning and signals copy-paste from another module that does use raw SQL.

---

**B012-13** — [LOW] Inconsistent indentation style across files (2-space vs 4-space)

File: lib/api_server/vx/vx_thing_info.ex (4-space), lib/api_server/vx/vx_user.ex (4-space) vs lib/api_server/vx/vx_thing_event_omega_tires.ex (2-space), lib/api_server/vx/vx_thing_summary.ex (2-space)

Description: The Elixir community standard (and the formatter default) is 2-space indentation. `vx_thing_info.ex` and `vx_user.ex` consistently use 4-space indentation throughout, while `vx_thing_event_omega_tires.ex` and `vx_thing_summary.ex` use 2-space indentation. This inconsistency across sibling files in the same namespace indicates that `mix format` has not been applied uniformly, making diffs harder to read and signalling absent or unenforced formatting standards.

---

**B012-14** — [LOW] Inconsistent naming convention — `camelCase` public functions alongside `snake_case`

File: lib/api_server/vx/vx_thing_info.ex:24,47

Description: `getWithHardwareId/2` (line 24) and `[REDACTED-AWS-SMTP-PASSWORD]` (line 47) use camelCase, which violates the Elixir naming convention of snake_case for functions. All functions in the other three files under review use snake_case. Callers in controllers (e.g., `vx_thing_info_controller.ex`) call `[REDACTED-AWS-SMTP-PASSWORD]` and `VXThingInfo.service_performed` on the same module, showing a mixed-convention public API within a single module. This will trigger Elixir compiler warnings about non-idiomatic function naming.

---

**B012-15** — [LOW] Comment describes intent without implementation — orphaned TODO block

File: lib/api_server/vx/vx_thing_summary.ex:100–101

Description: Lines 100–101 contain:
```
# If we have thing_event.thingeventomega.totalenginehour then map merge
# If we have thing.aadhourmeteromega then map merge
```
These comments describe exactly what the following code does, so they serve as implementation notes rather than clarifying non-obvious intent. More importantly, the phrasing "If we have … then map merge" reads as a to-do or design note frozen in place — the code below implements both conditions, but the comments read as if the implementation may still be pending. This constitutes low-quality commentary that can mislead reviewers.

---

**B012-16** — [HIGH] `changeset/2` in `vx_user.ex` accesses `attrs.user_level` directly — crashes on map with string keys

File: lib/api_server/vx/vx_user.ex:81

Description: Line 81 calls `put_assoc(:function, %{aatfunction_id: attrs.user_level}, required: true)`. The `attrs` parameter is passed directly from `convert_json_to_changeset/1` which builds a plain map with atom keys (via `Vx.update_key_if_value(:user_level, ...)`). However, `changeset/2` is also called from `vx.ex` with a map built from controller params that may have string keys. Accessing `attrs.user_level` (dot-notation struct access) on a plain map with string keys will raise a `KeyError` at runtime because map dot-notation only works for structs. If the map uses atom keys but `:user_level` is absent, it returns `nil` silently — meaning the function association can be set to `%{aatfunction_id: nil}` without validation. This is a leaky abstraction: `changeset/2` assumes a specific map key type that is not enforced by the function signature or any guard.

---

## Summary Table

| ID      | Severity | Title                                                                 | File                                  | Line(s) |
|---------|----------|-----------------------------------------------------------------------|---------------------------------------|---------|
| B012-1  | LOW      | Commented-out call to non-existent function `calcfields`             | vx_thing_info.ex                      | 49      |
| B012-2  | HIGH     | Hardcoded magic date `~D[2019-01-13]` as bootstrap sentinel          | vx_thing_info.ex                      | 59      |
| B012-3  | MEDIUM   | Hardcoded magic integer `12` for `pmnotificationid`                  | vx_thing_info.ex                      | 66      |
| B012-4  | MEDIUM   | Hardcoded epoch `~D[1970-01-01]` as null-date sentinel               | vx_thing_info.ex                      | 78      |
| B012-5  | MEDIUM   | Variable `result` (line 66) bound but never used; name reused        | vx_thing_summary.ex                   | 66, 135 |
| B012-6  | LOW      | Variable `timestamp` bound but never used                            | vx_thing_summary.ex                   | 149     |
| B012-7  | LOW      | Commented-out `unique_constraint` variant                            | vx_user.ex                            | 85      |
| B012-8  | LOW      | Commented-out timezone field mapping `aactz`                         | vx_user.ex                            | 68      |
| B012-9  | MEDIUM   | Duplicate `update_key_if_value` call for `:aacuom`                   | vx_user.ex                            | 62, 67  |
| B012-10 | MEDIUM   | `Float.round/2` applied twice to already-rounded value               | vx_thing_summary.ex                   | 124, 128|
| B012-11 | MEDIUM   | `require Ecto.Adapters.SQL` outside module, unused                   | vx_user.ex                            | 2       |
| B012-12 | MEDIUM   | `require Ecto.Adapters.SQL` inside module, unused                    | vx_thing_info.ex                      | 7       |
| B012-13 | LOW      | Inconsistent indentation (2-space vs 4-space across files)           | vx_thing_info.ex, vx_user.ex          | all     |
| B012-14 | LOW      | camelCase public function names in an otherwise snake_case codebase  | vx_thing_info.ex                      | 24, 47  |
| B012-15 | LOW      | Orphaned design-note comments describing what code below already does | vx_thing_summary.ex                   | 100–101 |
| B012-16 | HIGH     | `attrs.user_level` dot-access in `changeset/2` crashes on string-key maps | vx_user.ex                       | 81      |
# Pass 4 – B013

**Date:** 2026-02-27
**Audit run:** 2026-02-27-01
**Agent:** B013
**Pass:** 4 (Code Quality)

**Files reviewed:**
- `lib/api_server_web.ex`
- `lib/api_server_web/auth_error_handler.ex`
- `lib/api_server_web/auth_pipeline.ex`

---

## Reading Evidence

### File: `lib/api_server_web.ex`

**Module:** `ApiServerWeb`

**Functions (by line):**
| Line | Name | Notes |
|------|------|-------|
| 20 | `controller/0` | Returns a `quote` block injected into every controller |
| 29 | `view/0` | Returns a `quote` block injected into every view |
| 46 | `router/0` | Returns a `quote` block injected into the router |
| 54 | `channel/0` | Returns a `quote` block injected into channels |
| 64 | `__using__/1` (defmacro) | Dispatches to the appropriate `controller/view/etc.` function via `apply/3` |

**Types / constants / errors defined:** None.

**Notable imports/uses injected per macro:**
- `:controller` injects: `Phoenix.Controller` (namespaced), `Plug.Conn`, `ApiServerWeb.Router.Helpers`, `ApiServerWeb.Gettext`
- `:view` injects: `Phoenix.View`, `Phoenix.Controller` (partial), `Phoenix.HTML`, `ApiServerWeb.Router.Helpers`, `ApiServerWeb.ErrorHelpers`, `ApiServerWeb.Gettext`
- `:router` injects: `Phoenix.Router`, `Plug.Conn`, `Phoenix.Controller`
- `:channel` injects: `Phoenix.Channel`, `ApiServerWeb.Gettext`

---

### File: `lib/api_server_web/auth_error_handler.ex`

**Module:** `ApiServerWeb.AuthErrorHandler`

**Functions (by line):**
| Line | Name | Notes |
|------|------|-------|
| 4 | `auth_error/3` | Guardian error callback; pattern-matches `{type, _reason}`, sends 401 JSON |

**Types / constants / errors defined:** None.

**Imports:** `Plug.Conn` (line 2)

**Observations:**
- No `@moduledoc` or `@doc` attributes.
- File uses 4-space indentation for the top-level body of the module (`import` at line 2, `def` at line 4) instead of the standard 2-space Elixir convention. The inner function body correctly uses 2-space relative indentation, producing a mixed appearance.
- `^M` (CRLF) line endings throughout the file — the file was saved with Windows line endings.
- `_reason` is intentionally ignored (correctly prefixed with `_`).

---

### File: `lib/api_server_web/auth_pipeline.ex`

**Module:** `ApiServer.Guardian.AuthPipeline`

**Functions / plugs (by line):**
| Line | Name | Notes |
|------|------|-------|
| 6 | `plug Guardian.Plug.VerifyHeader` | Active plug, realm "Bearer" |
| 7 | `# plug Guardian.Plug.EnsureAuthenticated` | **Commented-out plug** |
| 8 | `plug Guardian.Plug.LoadResource` | Active plug |

**Types / constants / errors defined:** None.

**`use` options (lines 2–4):**
- `otp_app: :MyApi` — capitalised atom; the actual OTP application name is `:api_server` (see `mix.exs`)
- `module: ApiServer.Guardian`
- `error_handler: ApiServerWeb.AuthErrorHandler`

---

## Findings

**B013-1** — [CRITICAL] `EnsureAuthenticated` plug commented out — authentication not enforced
File: `lib/api_server_web/auth_pipeline.ex:7`
Description: `Guardian.Plug.EnsureAuthenticated` is disabled with a single-line comment. The pipeline only verifies and loads the token; it does not reject requests that carry no valid token. Any route that relies solely on `ApiServerWeb.AuthPipeline` (used at `router.ex:25`) will accept unauthenticated requests. Disabling this plug is a security bypass, not a style issue. Severity is CRITICAL because authentication enforcement is absent on guarded routes in a production API server.

---

**B013-2** — [HIGH] `otp_app: :MyApi` mismatches actual OTP application atom `:api_server`
File: `lib/api_server_web/auth_pipeline.ex:2`
Description: Guardian's `Plug.Pipeline` uses `otp_app` to look up configuration from the application environment at runtime. The atom `:MyApi` does not match the OTP application name declared in `mix.exs` (`:api_server`). Guardian will fail to resolve its configuration from the correct application environment key, which can cause silent misconfiguration (e.g., secret key fallback, wrong issuer) depending on Guardian version and how config is structured. This is a latent runtime misconfiguration bug.

---

**B013-3** — [MEDIUM] `channel/0` macro defined but no channels exist in the project
File: `lib/api_server_web.ex:54`
Description: The `channel` function in `ApiServerWeb` injects `use Phoenix.Channel` and `import ApiServerWeb.Gettext` for any module that calls `use ApiServerWeb, :channel`. No file in `lib/` calls `use ApiServerWeb, :channel` — only a stub `user_socket.ex` exists and it uses `Phoenix.Socket` directly. The `channel/0` macro is dead entry-point boilerplate that will never be invoked. While harmless at compile time, it is misleading and inflates the public surface of the entrypoint module. Severity is MEDIUM (dead code, leaky boilerplate).

---

**B013-4** — [LOW] Commented-out code — `EnsureAuthenticated` line
File: `lib/api_server_web/auth_pipeline.ex:7`
Description: In addition to the security consequence reported in B013-1, the presence of the commented-out plug constitutes a code quality finding on its own. Commented-out code should be removed from version-controlled source and tracked via issue tracker or git history. This finding is subordinate to B013-1 but recorded separately per instructions.

---

**B013-5** — [LOW] Inconsistent indentation in `auth_error_handler.ex` — 4-space top-level, 2-space inner
File: `lib/api_server_web/auth_error_handler.ex:2`
Description: The `import Plug.Conn` at line 2 and the `def auth_error` at line 4 are indented with 4 spaces relative to the module boundary. The Elixir community standard (and the style used everywhere else in this codebase) is 2-space indentation. The inner function body uses 2 spaces relative to the `def`, giving the overall module an inconsistent, non-standard appearance. This is a style inconsistency that would produce warnings in automated style checkers such as Credo (`Credo.Check.Readability.IndentationConsistency`).

---

**B013-6** — [LOW] CRLF line endings in `auth_error_handler.ex` — inconsistent with rest of codebase
File: `lib/api_server_web/auth_error_handler.ex`
Description: The file contains Windows-style CRLF (`\r\n`) line endings, as confirmed by raw byte inspection (`^M` markers). All other examined source files in the repository use LF-only line endings. CRLF line endings in an Elixir project can cause diff noise, confuse certain toolchain steps, and indicate the file was edited on Windows without normalisation. A `.gitattributes` or `editorconfig` rule should enforce LF endings.

---

**B013-7** — [LOW] `ApiServerWeb.Router.Helpers` imported into all controllers and views — leaky abstraction for a pure JSON API
File: `lib/api_server_web.ex:24` (controller macro), `lib/api_server_web.ex:40` (view macro)
Description: `ApiServerWeb.Router.Helpers` generates URL/path helpers for HTML route-aware templates. This is boilerplate from the Phoenix HTML generator. Examination of the controllers and views shows this is a JSON-only API server (no path helpers are referenced in any controller or view file). Injecting `Router.Helpers` into every controller and view namespace is unnecessary, pollutes the module namespace with unused helpers, and will generate Elixir compiler warnings about unused imports if the helpers are never called. This is a leaky abstraction: HTML-oriented helpers are coupled into modules that do not use them.

---

**B013-8** — [LOW] `Phoenix.HTML` and `get_flash/view_module` injected into views — HTML API leaking into JSON view layer
File: `lib/api_server_web.ex:35-38` (view macro)
Description: The `view/0` macro injects `use Phoenix.HTML` (which defines HTML escaping helpers, form builders, tag generators, etc.) and imports `Phoenix.Controller.get_flash/2` and `view_module/1` into every view module. No view in this project renders HTML — all are JSON serialisation modules. These imports are unused boilerplate from the Phoenix HTML generator, constitute build-warning candidates (unused imports), and expose an irrelevant HTML abstraction into a purely JSON view layer. They should be removed from the `view` macro.

---

**B013-9** — [INFO] No `@moduledoc` in `auth_error_handler.ex`
File: `lib/api_server_web/auth_error_handler.ex:1`
Description: The module has no `@moduledoc` attribute. While not a build warning, omitting module documentation on a security-critical callback module means the intent and contract of `auth_error/3` are undocumented. Flagged for awareness; severity is INFO and does not constitute a build warning.

---

## Summary Table

| ID | Severity | File | Short Title |
|----|----------|------|-------------|
| B013-1 | CRITICAL | `auth_pipeline.ex:7` | `EnsureAuthenticated` commented out — authentication not enforced |
| B013-2 | HIGH | `auth_pipeline.ex:2` | `otp_app: :MyApi` mismatches OTP app atom `:api_server` |
| B013-3 | MEDIUM | `api_server_web.ex:54` | `channel/0` macro is dead code — no channels exist |
| B013-4 | LOW | `auth_pipeline.ex:7` | Commented-out code present in source |
| B013-5 | LOW | `auth_error_handler.ex:2` | 4-space top-level indentation violates 2-space Elixir convention |
| B013-6 | LOW | `auth_error_handler.ex` | CRLF line endings inconsistent with rest of codebase |
| B013-7 | LOW | `api_server_web.ex:24,40` | `Router.Helpers` injected into all controllers/views — never used in JSON API |
| B013-8 | LOW | `api_server_web.ex:35-38` | `Phoenix.HTML` and flash helpers injected into JSON-only view layer |
| B013-9 | INFO | `auth_error_handler.ex:1` | No `@moduledoc` on security-critical error handler |

**Total findings: 9** (1 CRITICAL, 1 HIGH, 1 MEDIUM, 5 LOW, 1 INFO)
# Pass 4 – B014

**Date:** 2026-02-27
**Audit run:** 2026-02-27-01
**Agent:** B014

## Files Reviewed

- `lib/api_server_web/channels/user_socket.ex`
- `lib/api_server_web/endpoint.ex`
- `lib/api_server_web/gettext.ex`
- `lib/api_server_web/xml_plug.ex`

---

## Reading Evidence

### lib/api_server_web/channels/user_socket.ex

**Module:** `ApiServerWeb.UserSocket`

**Macros/directives used (not functions):**
- `transport :websocket, Phoenix.Transports.WebSocket` — line 8 (macro call, not a def)

**Functions defined:**
| Function | Line |
|---|---|
| `connect/2` | 22 |
| `id/1` | 36 |

**Types / errors / constants defined:** none

**Notes:**
- No channels are registered; the only channel entry (`channel "room:*", ApiServerWeb.RoomChannel`) is commented out at line 5.
- The `transport` macro at line 8 is the old Phoenix 1.2-era API. Phoenix 1.5 (the version declared in mix.exs) deprecated `transport/3` inside `use Phoenix.Socket`; transport configuration moved to the socket options in the endpoint. The macro still compiles but emits a deprecation warning at build time.
- Lines 9, 27–35 contain commented-out code blocks (longpoll transport, example `id/1` implementation).

---

### lib/api_server_web/endpoint.ex

**Module:** `ApiServerWeb.Endpoint`

**Functions defined:**
| Function | Line |
|---|---|
| `init/2` | 51 |

**Plugs wired (compile-time, not functions):**
- `Plug.Static` — line 10
- `Phoenix.LiveReloader.Socket` socket — line 17 (conditional)
- `Phoenix.LiveReloader` — line 18 (conditional)
- `Phoenix.CodeReloader` — line 19 (conditional)
- `Plug.Logger` — line 22
- `Plug.Parsers` — line 24
- `Plug.MethodOverride` — line 30
- `Plug.Head` — line 31
- `Plug.Session` — line 36
- `CORSPlug` — line 42
- `ApiServerWeb.Router` — line 43

**Types / errors / constants defined:** none

**Notes:**
- `signing_salt` at line 39 is a short hardcoded literal (`"5CSDVUtC"`), in-source.
- `gzip: false` at line 11 with an adjacent comment noting it should be `true` in production.
- `xml_decoder: :xmerl_scan` is passed at line 28 but `xml_plug.ex` does not use this value (confirmed below).
- Trailing whitespace on line 41.

---

### lib/api_server_web/gettext.ex

**Module:** `ApiServerWeb.Gettext`

**Functions defined:** none (all behaviour comes from `use Gettext, otp_app: :api_server`)

**Types / errors / constants defined:** none

**Notes:** Module is used in `error_helpers.ex`, `api_server_web.ex`. No issues with the file itself.

---

### lib/api_server_web/xml_plug.ex

**Module:** `Plug.Parsers.XML`

**Behaviour implemented:** `Plug.Parsers`

**Functions defined:**
| Function | Line |
|---|---|
| `parse/5` (content-type "xml" clause) | 6 |
| `parse/5` (catch-all clause) | 13 |
| `defp decode/2` ({:ok, body, conn} clause only) | 17 |

**Types / errors / constants defined:**
- Raises `ArgumentError` — line 7
- Raises `"Malformed XML"` (plain string raise) — line 22
- Raises `Plug.Parsers.ParseError` — line 25

**Notes:**
- `decoder` is fetched from `opts` at line 7 but is only passed to `decode/2` at line 10; inside `decode/2` the parameter is named `decoder` but the function body calls `XmlToMap.naive_map/1` directly without ever using `decoder`. The value read from opts is therefore consumed only to satisfy the guard that the key is present — the actual decoding library is hardcoded.
- `decode/2` has only one pattern-match clause: `{:ok, body, conn}`. The `:more` and `:error` tuples that `read_body/2` can return are not handled, causing a `FunctionClauseError` at runtime for large bodies or read errors.
- The `case` at line 19 has a wildcard second clause (`_ -> raise "Malformed XML"`) that is unreachable: `XmlToMap.naive_map/1` never returns a non-map value on success; it either returns a map or raises. Elixir will warn about this unreachable clause.
- Indentation is inconsistent: the module body uses 4-space indentation for `defp decode`, while the public `def parse` clauses use 2-space indentation that is itself further indented by 2 extra spaces (net 4 spaces inside the module but visually mixed due to inconsistent leading spaces on the `defp` block).

---

## Findings

---

**B014-1** — [HIGH] Deprecated `transport/3` macro used in UserSocket

File: `lib/api_server_web/channels/user_socket.ex:8`

Description: `transport :websocket, Phoenix.Transports.WebSocket` uses the Phoenix 1.2-era `transport/3` macro that was deprecated in Phoenix 1.3 and removed in Phoenix 1.7. The project declares `{:phoenix, "~> 1.5.9"}` in `mix.exs`. Under Phoenix 1.5 this macro emits a compiler deprecation warning on every build. The correct approach for 1.5+ is to configure transports via the `socket/3` call in the endpoint or through socket options; the macro is a no-op in 1.5 and will break completely if the project is upgraded to Phoenix 1.7+. This is a build warning that will become a compile error on upgrade.

---

**B014-2** — [HIGH] `xml_decoder` option fetched but never used — hardcoded decoder

File: `lib/api_server_web/xml_plug.ex:7`

Description: Line 7 reads `decoder = Keyword.get(opts, :xml_decoder)` and will raise `ArgumentError` if the key is absent, giving callers the impression they control the decoding library. However, `decoder` is passed into `decode/2` at line 10, and `decode/2` ignores its second argument entirely — it calls `XmlToMap.naive_map(body)` unconditionally. The `:xml_decoder` option configured in `endpoint.ex` line 28 (`:xmerl_scan`) has zero effect on actual behavior. This constitutes a leaky/false abstraction: the public interface promises configurability that does not exist, and the `decoder` variable in `decode/2` (line 17) is bound but never read, which will generate a compiler "variable `decoder` is unused" warning.

---

**B014-3** — [HIGH] `decode/2` does not handle `:more` or `:error` from `read_body/2`

File: `lib/api_server_web/xml_plug.ex:17`

Description: `read_body/2` (Plug.Conn) can return `{:ok, body, conn}`, `{:more, partial_body, conn}`, or `{:error, reason}`. The `decode/2` private function only pattern-matches on `{:ok, body, conn}`. Any XML request whose body exceeds the read buffer length will return `{:more, …}` and cause a `FunctionClauseError` crash, producing an unhandled 500. Large XML payloads — a realistic scenario for the ABL record format used elsewhere in this codebase — will silently crash the parser process.

---

**B014-4** — [MEDIUM] Unreachable wildcard clause in `case` inside `decode/2`

File: `lib/api_server_web/xml_plug.ex:19-22`

Description: The `case XmlToMap.naive_map(body) do` block has two arms: a bare `map ->` binding (line 19) and `_ -> raise "Malformed XML"` (line 21). Because the first arm is an unconditional match with no guard, the second arm can never be reached. `XmlToMap.naive_map/1` either returns a value (matched by the first arm) or raises an exception (caught by the `rescue` block). The dead clause will produce an Elixir compiler warning about an unreachable clause, and a plain `raise "Malformed XML"` (a string, not an exception struct) would generate a non-standard error term even if it were reachable.

---

**B014-5** — [LOW] Commented-out `channel` declaration in UserSocket

File: `lib/api_server_web/channels/user_socket.ex:5`

Description: `# channel "room:*", ApiServerWeb.RoomChannel` is a commented-out code line, not a documentation comment. It is a Phoenix scaffold remnant that has never been activated. Its presence implies channels were once considered or are still planned, but no channel modules exist in the `channels/` directory. Dead placeholder code should be removed rather than left commented in source control.

---

**B014-6** — [LOW] Commented-out `transport` declaration for LongPoll

File: `lib/api_server_web/channels/user_socket.ex:9`

Description: `# transport :longpoll, Phoenix.Transports.LongPoll` is commented-out code. Given that the active WebSocket transport (line 8) is itself deprecated (see B014-1), this is doubly dead code. It should be removed.

---

**B014-7** — [LOW] Hardcoded session signing salt committed in source

File: `lib/api_server_web/endpoint.ex:39`

Description: `signing_salt: "5CSDVUtC"` is a short, hardcoded literal checked into version control. While the session is signed (not encrypted) so this alone does not expose session contents, the salt must be secret to prevent brute-force attacks against forged session cookies. It should be loaded from an environment variable or a secrets file excluded from source control (analogous to `secret_key_base`).

---

**B014-8** — [LOW] `gzip: false` hardcoded in `Plug.Static` with a comment acknowledging it should be `true` in production

File: `lib/api_server_web/endpoint.ex:8-11`

Description: The adjacent comment explicitly states "You should set gzip to true if you are running phoenix.digest when deploying your static files in production," yet the value is hardcoded `false` with no environment-conditional override in any config file. Production static assets are served without gzip compression, wasting bandwidth and increasing latency. The comment acknowledges the correct behavior but the code never implements it.

---

**B014-9** — [LOW] Trailing whitespace on blank line in endpoint.ex

File: `lib/api_server_web/endpoint.ex:41`

Description: Line 41 contains trailing whitespace (a blank line between `Plug.Session` and `CORSPlug` that contains spaces/tabs). This is a minor style defect but will cause diff noise and may trigger linter failures in CI if a whitespace check is added.

---

**B014-10** — [LOW] Inconsistent indentation within xml_plug.ex

File: `lib/api_server_web/xml_plug.ex`

Description: The file mixes indentation levels. The public `def parse/5` clauses at lines 6 and 13 use 4-space indentation inside the module (standard for Elixir). The private `defp decode/2` block at line 17 uses 8-space indentation for its body. Within `decode/2` the `case` body is at 12 spaces and the rescue is at 6 spaces. The `end` keywords do not align consistently with their opening constructs. This indicates the file was written or edited without a formatter (`mix format`) having been applied. In a project using `mix format`, this file would fail format checks.

---

**B014-11** — [INFO] `ApiServerWeb.UserSocket` registers no channels — socket endpoint may be unused

File: `lib/api_server_web/channels/user_socket.ex`
File: `lib/api_server_web/endpoint.ex:4`

Description: The WebSocket socket is mounted at `/socket` in the endpoint, but no channel routes exist in `UserSocket` and no channel modules exist in the `channels/` directory. The `connect/2` callback accepts all connections unconditionally. This is not a defect on its own (the socket may be used by a JavaScript client that only uses `connect`), but combined with B014-5 it suggests the channel infrastructure is entirely scaffolded and not yet operational. This may represent unnecessary attack surface.

---

## Summary Table

| ID | Severity | File | Short Title |
|---|---|---|---|
| B014-1 | HIGH | user_socket.ex:8 | Deprecated `transport/3` macro — build warning, breaks on upgrade |
| B014-2 | HIGH | xml_plug.ex:7,17 | `xml_decoder` option fetched but ignored — unused variable, false abstraction |
| B014-3 | HIGH | xml_plug.ex:17 | `decode/2` missing `:more` and `:error` clauses — crash on large bodies |
| B014-4 | MEDIUM | xml_plug.ex:19-22 | Unreachable wildcard `case` arm — compiler warning, dead code |
| B014-5 | LOW | user_socket.ex:5 | Commented-out `channel` scaffold line |
| B014-6 | LOW | user_socket.ex:9 | Commented-out `transport :longpoll` line |
| B014-7 | LOW | endpoint.ex:39 | Hardcoded session signing salt in source |
| B014-8 | LOW | endpoint.ex:11 | `gzip: false` never overridden for production despite advisory comment |
| B014-9 | LOW | endpoint.ex:41 | Trailing whitespace on blank line |
| B014-10 | LOW | xml_plug.ex (file-wide) | Inconsistent indentation — file not `mix format` compliant |
| B014-11 | INFO | user_socket.ex / endpoint.ex:4 | No channels registered — socket may be unnecessary attack surface |
# Pass 4 – B015

**Date:** 2026-02-27
**Audit run:** 2026-02-27-01
**Agent:** B015

**Files reviewed:**
- `lib/api_server_web/controllers/calamp_controller.ex`
- `lib/api_server_web/controllers/digital_matter_controller.ex`
- `lib/api_server_web/controllers/fallback_controller.ex`
- `lib/api_server_web/controllers/file_controller.ex`

---

## Reading Evidence

### File 1: `lib/api_server_web/controllers/calamp_controller.ex`

**Module:** `ApiServerWeb.CalampController`

**Functions:**

| Name | Visibility | Line |
|------|------------|------|
| `recieve_calamp_data/2` | public | 4 |
| `validate/3` | private (`defp`) | 31 |

**Types / constants / errors defined:** None

**Notes on content:**
- `recieve_calamp_data/2` pattern-matches on `%{xml: calamp_data}` (atom key).
- Body contains `IO.inspect` call (line 10) left in production code.
- Contains commented-out step markers and two commented-out function calls (lines 23–24).
- `validate/3` at line 31 receives `thing` as third argument but never uses it inside the body.
- Return value of `validate/3` is discarded by the caller.
- `customer` is hardcoded to `"vx_dev"` (line 5).
- Module is **not wired to any router route** (confirmed by full router search).

---

### File 2: `lib/api_server_web/controllers/digital_matter_controller.ex`

**Module:** `ApiServerWeb.DigitalMatterController`

**Functions:**

| Name | Visibility | Line |
|------|------------|------|
| `get_g62_data/2` | public | 4 |

**Types / constants / errors defined:** None

**Notes on content:**
- `email_to`, `email_from`, `subject`, `data` are bound at lines 9–15 but immediately commented out and never used; they are dead variable bindings.
- Lines 17–18: two commented-out lines sending email.
- Lines 43–65: a large block of commented-out JSON sample data (example payload).
- Lines 95–101: inline comments documenting unmapped reason codes; these are legitimate documentation comments, not commented-out code.
- Lines 228–238: second commented-out email-sending block.
- `summary_update` is bound at line 225 but never read afterward.
- `hardware_type` hardcoded to `1` at line 122 with a comment stating "CalAmp, I think there are many calculations based on this."
- `custcode` hardcoded to `"CEA"` at line 181; `customer` hardcoded to `"vx_dev"` at line 200.
- `trip_hours` retrieved via `Enum.find` (line 33–36) but accessed unconditionally at line 139 (`trip_hours["Dur"]`) — will raise `FunctionClauseError` / `KeyError` if `trip_hours` is `nil` (no FType 26 field present).
- `driver_id` similarly retrieved via `Enum.find` (line 38–41) and then accessed at line 172 (`driver_id["DriverID"]`) without a nil-guard — same crash risk.
- `gps` retrieved via `Enum.find` (line 23–26) and accessed unconditionally at lines 151, 158, 165, 184, 189, 190, 193 — crash if FType 0 field absent.
- Response is assembled inside `Enum.each` but the final value of `Enum.each` (always `:ok`) is what `get_g62_data/2` returns to Phoenix, not the `conn` — meaning the function does not return a valid `Plug.Conn.t()` when the loop completes normally. The conn manipulation happens inside the `Enum.each` callback but is not returned.
- Uses `Plug.Conn` functions directly rather than the Phoenix controller helpers used elsewhere in the codebase.
- Uses `Poison` for JSON encoding (lines 208, 242, 246) while the rest of the project may use `Jason`.

---

### File 3: `lib/api_server_web/controllers/fallback_controller.ex`

**Module:** `ApiServerWeb.FallbackController`

**Functions:**

| Name | Visibility | Line |
|------|------------|------|
| `call/2` (Ecto.Changeset clause) | public | 9 |
| `call/2` (:not_found clause) | public | 15 |

**Types / constants / errors defined:** None

**Notes on content:**
- Clean, well-structured, has a `@moduledoc`.
- No style issues identified within the file itself.
- Does not handle `{:error, :unauthorized}` or `{:error, :forbidden}` — common cases that other controllers may need. This is an INFO-level observation (by itself not a defect in this file).

---

### File 4: `lib/api_server_web/controllers/file_controller.ex`

**Module:** `ApiServerWeb.FileController`

**Functions:**

| Name | Visibility | Line |
|------|------------|------|
| `get_size/2` | public | 12 |
| `send_file_download/2` | public | 28 |
| `generate_binary_file_contents/1` | private (`defp`) | 42 |
| `check_crc/1` | private (`defp`) | 52 |

**Types / constants / errors defined:** None

**Notes on content:**
- Aliases defined: `ApiServer.Operators` (line 4), `ApiServer.Operators.File` (line 5), `ApiServer.Vx` (line 7), `ApiServer.Vx.VXAccessFob` (line 8).
- `ApiServer.Operators`, `ApiServer.Operators.File`, and `ApiServer.Vx.VXAccessFob` are aliased but **never referenced** in the file body — only `Vx` is used.
- `IO.puts` debug calls left in `get_size/2` (line 16) and `generate_binary_file_contents/1` (lines 45–47).
- `check_crc/1` closing `end` at line 63 is not indented — it sits at column 0, mismatched with the rest of the file's 2-space indentation style.
- `check_crc/1` is not exhaustive: only handles CRC strings of length 1–4; a zero-length string or a string longer than 4 characters will raise a `FunctionClauseError`. A CRC value of 0 produces an empty string from `Integer.to_string/2`, which would not match any clause.
- `get_size/2` and `send_file_download/2` duplicate the fleet-reduction expression verbatim (lines 18 and 30).

---

## Findings

**B015-1** — [HIGH] Misspelled public function name `recieve_calamp_data`
File: `lib/api_server_web/controllers/calamp_controller.ex:4`
Description: The function is spelled `recieve_calamp_data` (transposing 'e' and 'i'). The correct spelling is `receive`. This is the only public action in the module, and any route or external caller must use the misspelled name. Renaming without a coordinated router update would be a breaking change. The misspelling pollutes the public API surface indefinitely.

---

**B015-2** — [HIGH] `CalampController` is not reachable — no router entry
File: `lib/api_server_web/controllers/calamp_controller.ex:1`
Description: A search of the entire router (`router.ex`) finds no reference to `CalampController` or `recieve_calamp_data`. The module exists with production-like logic but is unreachable by any HTTP request. It is either abandoned dead code or was accidentally omitted from the router. Dead controller modules bloat the build artifact and confuse maintainers.

---

**B015-3** — [HIGH] `Enum.each` used to build HTTP responses — `conn` is never returned
File: `lib/api_server_web/controllers/digital_matter_controller.ex:20`
Description: The entire record-processing loop runs inside `Enum.each`, whose return value is always `:ok`. The `conn` mutations inside the callback are never propagated back to the outer scope. Phoenix requires a controller action to return a `Plug.Conn.t()`. When `records` is non-empty the function silently returns `:ok` to the framework instead of a modified `conn`, producing an undefined response. When `records` is empty the same occurs. This is a structural correctness defect.

---

**B015-4** — [HIGH] Unconditional field access on potentially-nil `Enum.find` results
File: `lib/api_server_web/controllers/digital_matter_controller.ex:139`
Description: `trip_hours` (line 33), `gps` (line 23), and `driver_id` (line 38) are each obtained via `Enum.find`, which returns `nil` if no matching field is present. All three are subsequently accessed with map bracket notation without nil-guards: `trip_hours["Dur"]` (line 139), `gps["Alt"]` / `gps["Head"]` / etc. (lines 151–193), and `driver_id["DriverID"]` (line 172). Any record lacking FType 0, 26, or 3 will raise an `ArgumentError` / `FunctionClauseError` at runtime, crashing the request process.

---

**B015-5** — [MEDIUM] Unused bound variables `email_to`, `email_from`, `subject`, `data`
File: `lib/api_server_web/controllers/digital_matter_controller.ex:9`
Description: Four variables are bound at lines 9–15 whose only consumer is the commented-out email call on lines 17–18. Because the email code is commented out, these bindings serve no purpose and will generate Elixir compiler warnings (`variable "email_to" is unused`, etc.). Variables intended to be deliberately unused must be prefixed with `_`.

---

**B015-6** — [MEDIUM] Unused bound variable `summary_update`
File: `lib/api_server_web/controllers/digital_matter_controller.ex:225`
Description: `summary_update` is assigned the return value of `update_thing_cached_fields/2` but is never read. This will generate an Elixir compiler warning. More importantly, if `update_thing_cached_fields` returns an error tuple, that error is silently swallowed with no logging or response branching.

---

**B015-7** — [MEDIUM] Unused aliases in `FileController`
File: `lib/api_server_web/controllers/file_controller.ex:4`
Description: Three aliases are declared but never referenced in the module body:
- `alias ApiServer.Operators` (line 4)
- `alias ApiServer.Operators.File` (line 5)
- `alias ApiServer.Vx.VXAccessFob` (line 8)

Elixir will emit compiler warnings for unused aliases. The `ApiServer.Operators.File` alias additionally shadows the standard library `File` module, which can cause confusion if `File` is ever referenced.

---

**B015-8** — [MEDIUM] `validate/3` third argument `thing` is unused
File: `lib/api_server_web/controllers/calamp_controller.ex:31`
Description: `defp validate(new_event, current_event, thing)` receives `thing` as the third parameter but the body never references it. Elixir will emit a compiler warning. Because `thing` is not prefixed with `_`, the intent is unclear — it may indicate unfinished validation logic (the surrounding step comments "2. Save the record if valid" suggest intentional incompleteness).

---

**B015-9** — [MEDIUM] Return value of `validate/3` is discarded
File: `lib/api_server_web/controllers/calamp_controller.ex:17`
Description: `validate(new_event, thing_event, thing)` is called at line 17 but its return value is not captured. The function currently returns the result of the last `IO.puts` call (`:ok`). Step comments in the caller ("2. Save the record if valid") indicate the validation result was intended to gate a save operation. Discarding it means no validation-gated branching occurs.

---

**B015-10** — [MEDIUM] `check_crc/1` is non-exhaustive — zero or >4 hex digit CRC causes crash
File: `lib/api_server_web/controllers/file_controller.ex:52`
Description: `check_crc/1` uses a `case` that handles only string lengths 1–4. A CRC of 0 would produce the empty string `""` via `Integer.to_string(0, 16)` → `"0"` (length 1, actually safe), but any CRC whose hex representation exceeds 4 characters — which cannot occur for a 16-bit CRC — is theoretically safe. However, the case has no catch-all (`_`) clause, so any unexpected input length raises `CaseClauseError`. The absence of a guard is a latent fragility even if the 16-bit domain prevents it today.

---

**B015-11** — [LOW] Commented-out code blocks — `calamp_controller.ex` lines 23–24
File: `lib/api_server_web/controllers/calamp_controller.ex:23`
Description: Two function calls are commented out:
```
# ApiServer.VXThingSummary.validate_for_hardwareid(hardwareid, customer)
# ApiServer.VXThingInfo.validateForHardwareId(hardwareid, customer)
```
These represent steps 3 and 4 described in the adjacent step comments. It is unclear whether the underlying functions still exist or are intended to be re-enabled. Commented-out code should be removed or replaced with a tracked issue.

---

**B015-12** — [LOW] Commented-out code blocks — `digital_matter_controller.ex` lines 17–18 and 228–238
File: `lib/api_server_web/controllers/digital_matter_controller.ex:17`
Description: Two separate email-sending blocks are commented out. The first (lines 17–18) is paired with dead variable bindings (see B015-5). The second (lines 228–238) is a multi-line block. Both reference `ApiServer.Email.send_digital_matter_email` and `ApiServer.Mailer.deliver_now`. Retaining commented-out code obscures intent and creates confusion about whether the email feature is intended to be active.

---

**B015-13** — [LOW] Commented-out example payload block — `digital_matter_controller.ex` lines 43–65
File: `lib/api_server_web/controllers/digital_matter_controller.ex:43`
Description: A 23-line block of commented-out JSON-like sample data sits inside a production function. Sample/reference data should live in tests or documentation, not in controller source.

---

**B015-14** — [LOW] `IO.inspect` / `IO.puts` debug output left in production code
File: `lib/api_server_web/controllers/calamp_controller.ex:10` and `lib/api_server_web/controllers/file_controller.ex:16,45,47` and `lib/api_server_web/controllers/calamp_controller.ex:34,40,43`
Description: Multiple `IO.inspect` and `IO.puts` calls are present in production controller and helper code:
- `calamp_controller.ex` line 10: `|> IO.inspect` in the pipeline
- `calamp_controller.ex` lines 34, 40, 43: `IO.puts` in `validate/3`
- `file_controller.ex` line 16: `IO.puts` in `get_size/2`
- `file_controller.ex` lines 45, 47: `IO.puts` in `generate_binary_file_contents/1`

These will emit output to stdout in production, polluting logs and potentially leaking internal data values (hardware IDs, CRC values, event diffs).

---

**B015-15** — [LOW] Inconsistent indentation — `calamp_controller.ex` uses 4-space, rest use 2-space
File: `lib/api_server_web/controllers/calamp_controller.ex:1`
Description: `calamp_controller.ex` indents with 4 spaces throughout (visible on lines 5–17, 32–43), while `digital_matter_controller.ex`, `fallback_controller.ex`, and `file_controller.ex` all use 2-space indentation consistent with the Elixir community standard and the rest of the codebase. This inconsistency suggests the file was written with a different editor configuration.

---

**B015-16** — [LOW] `check_crc/1` closing `end` has incorrect indentation
File: `lib/api_server_web/controllers/file_controller.ex:63`
Description: The closing `end` for `check_crc/1` is at column 0 (line 63), while the `defp check_crc(crc_string) do` opener is at 2-space indent (line 52) and the `case` body is at 4-space indent. This is a formatting error that will cause `mix format` to reformat it.

---

**B015-17** — [LOW] Duplicated fleet-reduction expression in `FileController`
File: `lib/api_server_web/controllers/file_controller.ex:18,30`
Description: The expression `Enum.reduce(thing.fleet_thing_joins, [], fn(fleet_join, acc) -> acc ++ ["#{fleet_join.aafgroupid}"] end)` is copy-pasted verbatim in both `get_size/2` (line 18) and `send_file_download/2` (line 30). This violates DRY and means any future fix must be applied in two places. It should be extracted to a private helper.

---

**B015-18** — [LOW] Hardcoded customer codes and hardware type constants
File: `lib/api_server_web/controllers/calamp_controller.ex:5`, `lib/api_server_web/controllers/digital_matter_controller.ex:122,181,200`
Description: Business-significant values are hardcoded as string/integer literals with no named constant or configuration:
- `"vx_dev"` customer in `calamp_controller.ex:5` and `digital_matter_controller.ex:200`
- `"CEA"` customer code in `digital_matter_controller.ex:181`
- `hardware_type = 1` in `digital_matter_controller.ex:122` (comment reads "CalAmp, I think there are many calculations based on this")

Using unnamed magic values makes it impossible to change them in one place and increases the risk that only some occurrences are updated.

---

**B015-19** — [LOW] Direct `Plug.Conn` calls instead of Phoenix controller helpers in `[REDACTED-AWS-SMTP-PASSWORD]`
File: `lib/api_server_web/controllers/digital_matter_controller.ex:205`
Description: `digital_matter_controller.ex` uses `Plug.Conn.put_resp_header/3` and `Plug.Conn.send_resp/3` directly (lines 205–209, 241–242, 245–246) rather than the Phoenix `put_resp_header`, `json`, or `send_resp` helpers already imported via `use ApiServerWeb, :controller`. This is inconsistent with every other controller in the codebase and bypasses Phoenix's content negotiation layer.

---

**B015-20** — [INFO] `FallbackController` does not handle `{:error, :unauthorized}` or `{:error, :forbidden}`
File: `lib/api_server_web/controllers/fallback_controller.ex:9`
Description: Only two error shapes are handled. If any controller action returns `{:error, :unauthorized}` or similar atoms, the fallback will raise a `FunctionClauseError` rather than rendering a graceful 401/403 response. This is an observation about missing coverage rather than a defect in the existing clauses.

---

## Summary Table

| ID | Severity | File | Short Title |
|----|----------|------|-------------|
| B015-1 | HIGH | calamp_controller.ex:4 | Misspelled public function name `recieve_calamp_data` |
| B015-2 | HIGH | calamp_controller.ex:1 | `CalampController` unreachable — no router entry |
| B015-3 | HIGH | digital_matter_controller.ex:20 | `Enum.each` used for HTTP responses — `conn` never returned |
| B015-4 | HIGH | digital_matter_controller.ex:139 | Unconditional access on potentially-nil `Enum.find` results |
| B015-5 | MEDIUM | digital_matter_controller.ex:9 | Unused bound variables (`email_to`, `email_from`, `subject`, `data`) |
| B015-6 | MEDIUM | digital_matter_controller.ex:225 | Unused bound variable `summary_update` — error silently swallowed |
| B015-7 | MEDIUM | file_controller.ex:4 | Three unused aliases (compiler warnings + `File` shadow) |
| B015-8 | MEDIUM | calamp_controller.ex:31 | `validate/3` third argument `thing` unused — compiler warning |
| B015-9 | MEDIUM | calamp_controller.ex:17 | Return value of `validate/3` discarded — validation not gating saves |
| B015-10 | MEDIUM | file_controller.ex:52 | `check_crc/1` non-exhaustive case — no catch-all clause |
| B015-11 | LOW | calamp_controller.ex:23 | Commented-out code (steps 3 & 4 function calls) |
| B015-12 | LOW | digital_matter_controller.ex:17 | Commented-out code (two email-sending blocks) |
| B015-13 | LOW | digital_matter_controller.ex:43 | Commented-out sample payload inside production function |
| B015-14 | LOW | multiple | `IO.inspect`/`IO.puts` debug output in production code (7 occurrences) |
| B015-15 | LOW | calamp_controller.ex:1 | 4-space indentation inconsistent with 2-space codebase standard |
| B015-16 | LOW | file_controller.ex:63 | `check_crc/1` closing `end` at column 0 — broken indentation |
| B015-17 | LOW | file_controller.ex:18,30 | Duplicated fleet-reduction expression across two actions |
| B015-18 | LOW | multiple | Hardcoded magic constants (`"vx_dev"`, `"CEA"`, `hardware_type = 1`) |
| B015-19 | LOW | digital_matter_controller.ex:205 | Direct `Plug.Conn` calls instead of Phoenix controller helpers |
| B015-20 | INFO | fallback_controller.ex:9 | `FallbackController` missing clauses for `:unauthorized`/`:forbidden` |

**Totals:** 4 HIGH, 6 MEDIUM, 9 LOW, 1 INFO
# Pass 4 – B016

**Date:** 2026-02-27
**Audit run:** 2026-02-27-01

**Files reviewed:**
- `lib/api_server_web/controllers/geofence_controller.ex` (206 lines)
- `lib/api_server_web/controllers/page_controller.ex` (7 lines)
- `lib/api_server_web/controllers/pivotel_controller.ex` (115 lines)
- `lib/api_server_web/controllers/utility_controller.ex` (6,293 lines)

---

## Reading Evidence

### geofence_controller.ex

**Module:** `ApiServerWeb.GeofenceController`

**Aliases/Imports:**
- `ApiServer.Vx` (alias)
- `ApiServer.Vx.Geofence` (alias)
- `Ecto.Query` (import, warn: false)
- `ApiServer.Repo` (alias)

**Public functions:**
| Function | Line |
|---|---|
| `list_all_geofences/2` | 11 |
| `create_geofence/2` | 18 |
| `update_geofence/2` | 35 |
| `delete_geofence/2` | 57 |
| `process_things_geofences/2` | 73 |

**Private functions:**
| Function | Line |
|---|---|
| `check_geofences_for_unit/6` | 96 |
| `does_event_cause_geofence_events/6` | 115 |
| `check_event_for_left_events/6` (nil clause) | 132 |
| `check_event_for_left_events/6` (list clause) | 133 |
| `check_event_for_entered_events/7` | 149 |
| `make_geofence_event/6` | 168 |
| `engine_hours_at_event/3` | 184 |

**Constants/Types defined:** none

---

### page_controller.ex

**Module:** `ApiServerWeb.PageController`

**Public functions:**
| Function | Line |
|---|---|
| `index/2` | 4 |

**Constants/Types defined:** none

---

### pivotel_controller.ex

**Module:** `ApiServerWeb.PivotelController`

**Public functions:**
| Function | Line |
|---|---|
| `get_pivotel_data/2` (PSG_MOmsg_send clause) | 4 |
| `get_pivotel_data/2` (catch-all clause) | 15 |
| `create_update_object/1` (LOCATION clause) | 20 |
| `create_update_object/1` (ACCUM clause) | 63 |
| `create_update_object/1` (catch-all clause) | 103 |

**Private functions:**
| Function | Line |
|---|---|
| `convert_timestamp/1` | 109 |

**Constants/Types defined:** none

---

### utility_controller.ex

**Module:** `ApiServerWeb.UtilityController`

**Module-level attributes/constants:**
| Name | Line |
|---|---|
| `@lookup_olson` (list of 2-tuples, timezone mapping) | 25–126 |

**Aliases/Imports:**
- `Ecto.Query` (import, warn: false)
- `ApiServer.Vx`
- `ApiServer.Vx.VXCustomer`
- `ApiServer.Vx.ERPImport`
- `ApiServer.Vx.VXThingInfo`
- `ApiServer.Repo`
- `ApiServer.Vx.VXThingEvent`
- `ApiServer.Vx.VXThingEventOmega`
- `ApiServer.Vx.VXThingEventOmegaTires`
- `ApiServer.Vx.VXRayvenMessageLog`
- `ApiServer.Vx.VXRayvenStreamStatus`
- `ApiServer.Vx.DeviceDatabaseLookup`
- `ApiServer.Vx.VXThingSummary`
- `ApiServer.Vx.Equipment`
- `ApiServer.Vx.EquipmentAssignment`
- `ApiServer.Vx.VXRental`
- `ApiServer.Vx.RentalPeriod`
- `ApiServer.Vx.RentalContract`

**Public functions:**
| Function | Line |
|---|---|
| `update_puls_firmware/1` | 128 |
| `bulk_daily_usage_summary/1` | 228 |
| `do_health_check/2` | 320 |
| `calculate_roi_value/2` | 324 |
| `process_incoming_omegawatch_data/2` | 328 |
| `process_prodisplay_event/2` | 333 |
| `do_error/2` | 982 |
| `do_geocode_lookup/2` | 991 |
| `sync_to_DISCorp/2` | 1052 |
| `sync_vehicles_to_rayven/1` | 1076 |
| `test_rental_messages/1` | 1203 |
| `send_vehicle_to_rayven/2` | 1445 |
| `send_to_rayven/7` | 1677 |
| `pull_from_rayven/1` | 1986 |
| `check_out_of_sequence_events/1` | 2009 |
| `get_tracker_ids/0` | 2078 |
| `device_lookup_with_hardware_id/1` | 2093 |
| `check_vehicles_for_rental_overage/3` | 2100 |
| `process_monthly_movements/0` | 2280 |
| `process_pronto/0` | 2463 |
| `process_ebs/0` | 2821 |
| `process_ebs_check_service/1` | 2972 |
| `process_ebs_get_hour_meter/2` | 2990 |
| `send_local_arrow_data/0` | 3036 |
| `check_vehicles_for_no_usage_historical/1` | 3170 |
| `process_events_for_next_usage/4` | 3213 |
| `sync_events_to_rayven/0` | 3298 |
| `rayven_login/2` | 3346 |
| `get_rayven_devices_for_project/2` | 3390 |
| `pull_data_from_rayven/1` | 3412 |
| `create_equipment/3` | 3453 |
| `get_equipment_id/2` | 3524 |
| `create_equipment_assignment/3` | 3533 |
| `create_rental_records/1` | 3596 |
| `sync_rental_contracts_to_rayven/1` | 3600 |
| `sync_rental_periods_to_rayven/1` | 3615 |
| `copy_rental_contracts/1` | 3623 |
| `pull_equipment_data_from_rayven/1` | 4647 |
| `pull_services_from_rayven/1` | 4729 |
| `refresh_rayven_stream_status/1` | 4900 |
| `sync_historical_events_to_rayven/1` | 5020 |
| `sync_historical_events_to_rayven/5` | 5091 |
| `send_events_to_rayven/6` | 5358 |
| `prepare_rayven_events/3` | 5416 |
| `check_for_future_date/2` | 5567 |
| `erp_import/2` | 5666 |
| `driverid_converter/2` | 6025 |
| `get_additional_data/1` | 6172 |
| `next_service/1` | 6225 |

**Private functions:**
| Function | Line |
|---|---|
| `parse_prodisplay_thingevent/4` (with `@doc`) | 701 |
| `parse_prodisplay_thingomega_event/5` (with `@doc`) | 806 |
| `parse_prodisplay_thingomegatires_event/5` (with `@doc`) | 923 |
| `check_and_save_erp_record/3` | 5735 |
| `process_rental_from_erp/2` | 5758 |
| `find_or_make_customer/3` | 5850 |
| `process_services_from_erp/2` | 5882 |
| `process_service_from_erp/2` | 5896 |
| `get_dm_driverid/1` | 6092 |
| `rayven_ssl_opts/0` | 6267 |
| `rayven_cacerts/0` | 6278 |

**Aliases never referenced in code:**
- `ApiServer.Vx.VXCustomer` (aliased at line 7, not used in any function body visible in the file)
- `ApiServer.Vx.ERPImport` (aliased at line 8, not used)
- `ApiServer.Vx.VXThingInfo` (aliased at line 9, not used — the module is called via full name `ApiServer.Vx.VXThingInfo.service_performed/3` at line 5950 through the `Vx` alias)
- `ApiServer.Vx.VXThingEventOmega` (aliased at line 12, not directly used in any pattern or struct literal)
- `ApiServer.Vx.VXThingEventOmegaTires` (aliased at line 13, not directly used)
- `ApiServer.Vx.VXThingSummary` (aliased at line 17, not used)
- `ApiServer.Vx.Equipment` (aliased at line 18, not used)
- `ApiServer.Vx.EquipmentAssignment` (aliased at line 19, not used)
- `ApiServer.Vx.RentalPeriod` (aliased at line 21, not used)
- `ApiServer.Vx.RentalContract` (aliased at line 22, not used)

---

## Findings

---

**B016-1** — [MEDIUM] `IO.inspect` left in production error path

File: `lib/api_server_web/controllers/geofence_controller.ex:30`

Description: `IO.inspect error` is called unconditionally inside the `{:error, error}` branch of `create_geofence/2` before sending a 500 response. This logs internal changeset error detail (including field names and constraint violations) to stdout/logs in production. It is a debug statement that was never removed. Additionally, the raw `inspect error` string is interpolated directly into the JSON response body at line 31, leaking internal Ecto changeset structure to API callers.

---

**B016-2** — [LOW] Commented-out code in `geofence_controller.ex`

File: `lib/api_server_web/controllers/geofence_controller.ex:89`

Description: Line 89 contains the comment `# Grab all geofences and convert them for assessment by topo`. This is a descriptive inline comment and acceptable, but lines within `check_geofences_for_unit/6` initialize `inList = []` at line 97 which is immediately shadowed by the `Enum.reduce` destructure and the variable `inList` is never subsequently read. This is a bound-but-never-used variable (see B016-3 below). Note: there are no full commented-out code blocks in this file.

---

**B016-3** — [LOW] Variable `inList` bound but never used

File: `lib/api_server_web/controllers/geofence_controller.ex:97`

Description: `inList = []` is assigned at line 97 inside `check_geofences_for_unit/6`, but the variable is never referenced again. The `Enum.reduce` on line 103 uses its own anonymous function parameter `in_list` (initially `[]`). Without a leading underscore, Elixir will emit a compiler warning `variable "inList" is unused`. This is dead initialization code.

---

**B016-4** — [MEDIUM] Variable shadowing in `does_event_cause_geofence_events/6` — bound result never used

File: `lib/api_server_web/controllers/geofence_controller.ex:120-121`

Description: Inside the `%Timex.AmbiguousDateTime{}` match, `datetime = Map.get(adt, :after)` assigns to `datetime` at line 121, but that variable is never returned or referenced — the `case` expression is itself bound to `event_time`. The inner `datetime` assignment is dead code. Elixir will warn that `datetime` is unused.

---

**B016-5** — [MEDIUM] Wrong return value from `check_event_for_left_events/6` nil clause

File: `lib/api_server_web/controllers/geofence_controller.ex:132`

Description: The nil-clause of `check_event_for_left_events/6` returns `[]` (a bare list) instead of `{[], []}` (a two-tuple). The caller at line 126 destructures the result as `{fences_still_inside, left_events}`. If `in_geofences` is `nil`, this clause will cause a `MatchError` at runtime. This is a latent crash bug.

---

**B016-6** — [LOW] Inconsistent use of `nil` vs `false` guard in `geofence_controller.ex`

File: `lib/api_server_web/controllers/geofence_controller.ex:40,61`

Description: `update_geofence/2` checks `if geofence != nil` (line 40) while `delete_geofence/2` uses `if geofence` (line 61). These are semantically equivalent for Elixir truthy evaluation but are stylistically inconsistent within the same file. The idiomatic Elixir form is `if geofence do` or pattern-match with `case`.

---

**B016-7** — [LOW] Commented-out code in `pivotel_controller.ex`

File: `lib/api_server_web/controllers/pivotel_controller.ex:9`

Description: `# IO.inspect update` at line 9 is a debug statement that was commented out but left in the source. Commented-out code of this form should be removed.

---

**B016-8** — [LOW] `IO.puts` debug statements left in production controller

File: `lib/api_server_web/controllers/pivotel_controller.ex:5,8,47,104`

Description: Four `IO.puts` calls remain in production paths of `PivotelController`: lines 5 (`"PSG_MOmsg_send"`), 8 (`"Update for ..."`), 47 (`"Need to store a location event"`), and 104 (`"Unprocessable Message"`). These will emit to stdout on every request and in every unmatched message, polluting logs with no structured metadata.

---

**B016-9** — [LOW] `create_update_object/1` is public but is only called internally

File: `lib/api_server_web/controllers/pivotel_controller.ex:20`

Description: `create_update_object/1` is defined as `def` (public) but is called only from within `get_pivotel_data/2` in the same module. It should be `defp`. Exposing it as a public function widens the module's API surface unnecessarily and makes it callable from tests or other modules as though it were a stable interface.

---

**B016-10** — [MEDIUM] `@doc` on `defp` functions is silently ignored by Elixir

File: `lib/api_server_web/controllers/utility_controller.ex:697,802,919`

Description: Three private functions carry `@doc` strings:
- `parse_prodisplay_thingevent/4` at line 701 (doc at 697)
- `parse_prodisplay_thingomega_event/5` at line 806 (doc at 802)
- `parse_prodisplay_thingomegatires_event/5` at line 923 (doc at 919)

Elixir silently discards `@doc` attributes placed before `defp`. These docstrings will never appear in `ExDoc` output or `IEx.h/1`. The developer intent is not realized and the documentation is effectively dead. The correct approach is either to make the functions `def` (if documentation is truly needed) or remove the `@doc` annotations.

---

**B016-11** — [HIGH] Large commented-out function `send_rentals_to_rayven/2`

File: `lib/api_server_web/controllers/utility_controller.ex:1245–1443`

Description: Lines 1245–1443 contain a 199-line block of commented-out code comprising what appears to be the entire abandoned implementation of `send_rentals_to_rayven/2`. The function `test_rental_messages/1` at line 1203 still references this function at line 1231 via a comment (`# send_rentals_to_rayven(thing, customer)`). This dead code block is a significant maintenance hazard: it contains hardcoded customer strings, rental data structures, and business logic that is no longer executed, yet may mislead future developers about the intended behavior.

---

**B016-12** — [HIGH] Hardcoded API keys and credentials in source code

File: `lib/api_server_web/controllers/utility_controller.ex:141,146,151,171,1053,1747,1861–1888,1918,2000`

Description: Multiple hardcoded secrets and API credentials appear directly in source code:
- Line 141: `# API Key for old account: IwZTptJkQeOxZCoKRKVtI3IrIVwotFW6KRDS8O8OI-RKjmykQ95DPGlEE4yxjqbg` (commented, but still present in VCS history)
- Line 141: `# API Key for new account: 1SdeU1293s78waU_2P3vwCInz2oEOe-Rj6_AYqL-FwBzFtsG3n_o5mNsqat5rO4L` (commented)
- Line 146: Live API key in URL string `IwZTptJkQeOxZCoKRKVtI3IrIVwotFW6KRDS8O8OI-RKjmykQ95DPGlEE4yxjqbg` used in production HTTP call
- Line 151: `Authorization: "Basic VHJhY2tpbmdTb2x1dGlvbnM6dHZWSFFVc0NBZXU0"` — hardcoded Basic Auth
- Line 171: Live API key `1SdeU1293s78waU_2P3vwCInz2oEOe-Rj6_AYqL-FwBzFtsG3n_o5mNsqat5rO4L`
- Line 1053: `api_key = "PZPwWHyAMFhPbt3UB8PWXtEw"` (DISCorp API key hardcoded, used in a live HTTP POST)
- Line 1747: `uid = "3470e0a6599bbdc8488db6965597eab43728"` (Rayven UID hardcoded in `send_to_rayven/7`)
- Line 1861: `uid = "1964374994320a294ecaabd94c23f0ce911d"` (Rayven UID hardcoded in `copy_rental_contracts/1`)

These credentials are stored in plaintext in version control. Even the commented-out keys remain in git history. All secrets should be moved to application configuration or environment variables.

---

**B016-13** — [MEDIUM] Hardcoded email address in production code

File: `lib/api_server_web/controllers/utility_controller.ex:1703,1725,2251,2252,5387,5610`

Description: Personal email addresses (`graham.oconnell@trackingsolutions.com.au`, `rhythmduwadi@collectiveintelligence.com.au`, `sidney@collectiveintelligence.com.au`) are hardcoded as alert/report recipients in multiple functions. This means changing recipients requires a code change and deployment. They should be read from application configuration.

---

**B016-14** — [MEDIUM] Hardcoded test dates used in production functions

File: `lib/api_server_web/controllers/utility_controller.ex:240-241,1182,2023-2025,3310`

Description: Several functions use hardcoded date strings that were clearly set during development and never parameterized:
- `bulk_daily_usage_summary/1` (line 240): `to_date = "2021-06-18"`, `from_date = "2021-01-01"`
- `check_out_of_sequence_events/1` (line 2023): `from_date = "2018-07-01"`, `to_date = "2020-04-26"`
- `sync_events_to_rayven/0` (line 3310): `{:ok, start_date} = Timex.parse("2020-01-23", ...)`
- `sync_historical_events_to_rayven/5` (line 5240): `{:ok, now} = Timex.parse("2050-12-30", ...)` used as the "end date"

These hardcoded dates mean the functions produce different results (or no results) depending on when they are run and cannot be used correctly without code modification.

---

**B016-15** — [MEDIUM] Variables bound but never used — compiler warnings in `utility_controller.ex`

File: `lib/api_server_web/controllers/utility_controller.ex` (multiple locations)

Description: Multiple variables are bound and their values are never subsequently read, generating Elixir compiler warnings:

- Line 657: `summary_update = ApiServerWeb.VXThingController.update_thing_cached_fields(...)` — result bound but not used (repeated in the vx_mondialevgl and vx_sssl branches at lines 532, 538, 663–667)
- Lines 1668, 1674: `diff = Timex.diff(...)` bound twice in `send_vehicle_to_rayven/2`, neither value used
- Line 2047: `usage_diff = event.calcengineseconds - previous_usage` in `check_out_of_sequence_events/1` — bound inside a `case` arm but not returned or used
- Lines 2075–2076: `diff = Timex.diff(finish, start, :milliseconds)` in `check_out_of_sequence_events/1` — computed but never logged or returned
- Line 3343–3344: `diff = Timex.diff(start, finish, :milliseconds)` in `sync_events_to_rayven/0` — computed but never used
- Line 6077: `acc = acc ++ [[dm_driverid, weigand_driverid]]` in `driverid_converter/2` — reassigned to `acc` inside a `fn` passed to `Enum.reduce`, but the variable rebinding is a warning-inducing pattern (the reducer should return the new acc without rebinding)
- Line 6173, 6226: `start = Timex.now()` at the top of `get_additional_data/1` and `next_service/1` — timing values computed but never used (no `finish` or `diff` in either function)

---

**B016-16** — [HIGH] Empty function bodies — functions that do nothing

File: `lib/api_server_web/controllers/utility_controller.ex:324–326,3596–3598,3600–3613,3615–3621`

Description: Four public functions have empty or near-empty bodies that produce no effect:

- `calculate_roi_value/2` (line 324–326): Body is entirely blank — no return value, no side effects. Any call returns `nil`. It is a stub function that appears to be registered in the router.
- `create_rental_records/1` (line 3596–3598): Empty body — documented with a comment about its intent but never implemented.
- `sync_rental_contracts_to_rayven/1` (line 3600–3613): Body only constructs an anonymous map literal `%{trigger: "rental"}` that is immediately discarded; the return value is the map, not a sent HTTP request. Function is a stub.
- `sync_rental_periods_to_rayven/1` (line 3615–3621): Returns an empty map `%{}` — stub function.

These stubs are reachable (public `def`, likely wired in the router) but silently do nothing, making any call to them a no-op. This is particularly dangerous for `calculate_roi_value/2` which accepts `conn` and never sends a response, leaving the connection open.

---

**B016-17** — [LOW] Commented-out code blocks in `utility_controller.ex` — `process_monthly_movements/0`

File: `lib/api_server_web/controllers/utility_controller.ex:2421–2431`

Description: Lines 2421–2431 contain a commented-out block of code that was sending data to Rayven IOTX8 via HTTP. The comment `# # # Send to Rayven IOTX8` and subsequent commented lines are dead code left during development. The same pattern appears again in `process_ebs/0` at lines 2929–2941.

---

**B016-18** — [LOW] Commented-out code blocks in `utility_controller.ex` — `pull_equipment_data_from_rayven/1`

File: `lib/api_server_web/controllers/utility_controller.ex:4709–4726`

Description: Lines 4709–4726 contain a large block of commented-out code (`response = HTTPoison.get!(url)` and a `case` block with full service-record logic). Similarly, lines 4839–4884 in `pull_services_from_rayven/1` contain two separate commented-out `body` construction blocks and a commented JavaScript snippet. These are remnants of prior iterations that should be removed.

---

**B016-19** — [LOW] Commented-out code in `rayven_login/2` — function is entirely commented code

File: `lib/api_server_web/controllers/utility_controller.ex:3346–3388`

Description: `rayven_login/2` has an empty body (returns `nil`) while the entire "implementation" is a 40-line block of commented-out JavaScript code (a `fetch` call with headers and auth). The function is dead: it accepts two parameters and does absolutely nothing with them. The commented JavaScript code serves no purpose in an Elixir codebase.

---

**B016-20** — [MEDIUM] Commented-out `@doc` email code causes silent no-ops for email alerts

File: `lib/api_server_web/controllers/utility_controller.ex:1707–1708,1729–1730,5390–5391,5613–5614,5654–5655`

Description: Email alert calls are systematically commented out throughout `utility_controller.ex`. At lines 1707–1708 and 1729–1730 in `send_to_rayven/7`, the missing-serial-number email is commented out after the variables `email_to`, `email_from`, `subject`, and `data` are fully constructed. The same pattern appears in `check_for_future_date/2` (lines 5613–5614) and `send_events_to_rayven/6` (lines 5390–5391). This means:
1. The variable-binding code above each comment still executes (computing `email_to`, `data`, etc.)
2. No email is ever sent
3. The bound variables emit compiler warnings about being unused

The feature appears unfinished — the infrastructure is built but the delivery call is permanently disabled.

---

**B016-21** — [HIGH] Massive copy-paste duplication in `process_prodisplay_event/2`

File: `lib/api_server_web/controllers/utility_controller.ex:333–694`

Description: The `process_prodisplay_event/2` function (lines 333–694, approximately 362 lines) contains three near-identical code paths that handle event ingestion for three different customers (`vx_ceaomega`, `vx_sssl`, `vx_mondialevgl`). Each path:
1. Creates a thingevent record
2. Creates a thingomega record
3. Creates a thingomegatires record
4. Updates cached fields
5. Returns an HTTP response or error

The logic for steps 2–5 is duplicated nearly verbatim across the three branches, differing only in the customer string and the variable names prefixed with `sssl_`. This function should be refactored into a private helper that takes a customer string and event_id.

---

**B016-22** — [MEDIUM] Copy-paste duplication of date-formatting code

File: `lib/api_server_web/controllers/utility_controller.ex:3799–3821,3823–3847,4087–4108,4224–4271,4387–4434,4483–4532`

Description: Throughout `copy_rental_contracts/1` and `sync_rental_contracts_to_rayven/1`, the same 15-line block that converts a `Date` to a padded `"DD/MM/YYYY"` string appears at least six times verbatim:

```elixir
{year, month, day} = Date.to_erl(some_date)
year = Integer.to_string(year)
month = case month do
  x when x < 10 -> "0" <> Integer.to_string(month)
  _ -> Integer.to_string(month)
end
day = case day do
  x when x < 10 -> "0" <> Integer.to_string(day)
  _ -> Integer.to_string(day)
end
formatted = day <> "/" <> month <> "/" <> year
```

This block should be extracted into a private helper function. The repetition inflates the function size and makes maintenance error-prone. Note: Timex already provides `Timex.format(date, "{0D}/{0M}/{YYYY}")` which would replace all these blocks.

---

**B016-23** — [MEDIUM] Copy-paste duplication of dealer-ID mapping

File: `lib/api_server_web/controllers/utility_controller.ex:1531–1558,5417–5442`

Description: The `dealer_id` customer-to-string mapping case expression (matching on `"vx_sielift"`, `"vx_cea"`, `"vx_cea_local"`, `"vx_midpac"`, `"vx_komrigolift"`, `"vx_dev"`, `"demo_account"`) is duplicated verbatim in both `send_vehicle_to_rayven/2` (line 1531) and `prepare_rayven_events/3` (line 5417). Similarly, the serial-number prefix mapping is duplicated in `send_vehicle_to_rayven/2` (line 1560) and `prepare_rayven_events/3` (line 5444). These should be extracted into private helper functions `dealer_id_for_customer/1` and `serial_prefix_for_customer/2`.

---

**B016-24** — [MEDIUM] `sync_historical_events_to_rayven/5` — `task_stream` consumed twice

File: `lib/api_server_web/controllers/utility_controller.ex:5336–5354`

Description: At line 5338, the result of `Task.async_stream/3` is piped into `|> Enum.map(fn {result, reason} -> ... end)` which consumes the stream. At line 5354, `Stream.run(task_stream)` is then called on the already-consumed stream. `Stream.run/1` on an exhausted `Task.async_stream` result is a no-op but is also a code error — it indicates the developer misunderstood that `Enum.map/2` already consumed the stream. Compare with the correct pattern used in `sync_historical_events_to_rayven/1` at line 5082 which calls `Stream.run(task_stream)` on an unconsumed stream.

---

**B016-25** — [LOW] `process_services_from_erp/2` is defined but never called

File: `lib/api_server_web/controllers/utility_controller.ex:5882–5894`

Description: The private function `process_services_from_erp/2` (line 5882) is defined as `defp` but is never called anywhere in the file. The active code path in `erp_import/2` calls `process_service_from_erp/2` (singular, line 5718) directly per item. The plural wrapper function is dead code.

---

**B016-26** — [MEDIUM] Inconsistent error handling across controller actions

File: `lib/api_server_web/controllers/geofence_controller.ex` and `lib/api_server_web/controllers/utility_controller.ex` (multiple)

Description: Error responses are returned using three different patterns with no consistency:

1. `send_resp(conn, :internal_server_error, "{\"error\": \"...\"}") ` — hand-assembled JSON strings (geofence_controller.ex lines 31, 50, 53, 64, 69–70)
2. `Plug.Conn.send_resp(conn, 400, Poison.encode!(%{message: "..."}))` — Poison-encoded maps (utility_controller.ex lines 351–354, 416, 423–426, etc.)
3. `render(conn, "error.json", ...)` — not used at all in these files

The hand-assembled JSON strings in geofence_controller.ex are error-prone (escaping issues, not valid JSON if the interpolated value contains quotes) and inconsistent with the Poison-encoded approach used in utility_controller.ex. A single `json_error/3` helper or use of `render/3` with a view should standardize this.

---

**B016-27** — [LOW] `get_tracker_ids/0` — bound variables `customer` and `custcode` never returned

File: `lib/api_server_web/controllers/utility_controller.ex:2078–2091`

Description: `get_tracker_ids/0` assigns `customer = device.customer` and `custcode = device.custcode` at lines 2089–2090, but returns neither. The function's return value is the result of `Enum.take(devices, -1)` destructured as `[device]`, so the function effectively returns the last device's customer field implicitly (as the last evaluated expression). However, the variable assignments are misleading and `custcode` is never used at all, generating a compiler warning.

---

**B016-28** — [LOW] `pull_from_rayven/1` — result of `Poison.decode/1` assigned but never used

File: `lib/api_server_web/controllers/utility_controller.ex:2005`

Description: `response_json = Poison.decode(response)` at line 2005 binds the decoded JSON but the variable `response_json` is never read. The function then returns `nil` (the last expression's value being the binding). This is dead computation and generates a compiler warning for the unused variable. The entire function body is incomplete — it fetches from Rayven but does nothing with the response.

---

**B016-29** — [MEDIUM] `sync_to_DISCorp/2` — hardcoded test payload, never used in production

File: `lib/api_server_web/controllers/utility_controller.ex:1052–1074`

Description: `sync_to_DISCorp/2` constructs a hardcoded request body with `"hourmeter" => 3892.41`, `"make" => "CAPACITY"`, `"model" => "TJ5000"`, `"serialNumber" => "27403"`. These are clearly specific test values for a single piece of equipment and are not parameterized. If this endpoint is accessible via the router, calling it will POST these hardcoded values to the live DISCorp API on every invocation.

---

**B016-30** — [MEDIUM] Leaky abstraction — internal customer database schema strings hardcoded in controller

File: `lib/api_server_web/controllers/utility_controller.ex` (multiple)

Description: Database schema/prefix strings such as `"vx_ceaomega"`, `"vx_sssl"`, `"vx_mondialevgl"`, `"vx_cea"`, `"vx_sielift"`, `"vx_dpworld"`, `"vx_komatsuau"`, etc. are hardcoded throughout the controller layer rather than being resolved from configuration or a context module. The controller directly contains the routing logic that maps to customer-specific database schemas. This is a leaky abstraction: the controller knows about the persistence layer's multi-tenancy schema naming convention, making it impossible to change the naming without modifying controller code.

---

**B016-31** — [LOW] `process_ebs_get_hour_meter/2` — hardcoded customer schema prefix

File: `lib/api_server_web/controllers/utility_controller.ex:3002`

Description: `Repo.all(prefix: "vx_cea_latest")` at line 3002 hardcodes the customer database schema directly in the function body. The function accepts `hardwareid` and `date` as parameters but not `customer`. This means the function can only ever query the `vx_cea_latest` schema, making it non-reusable and a maintenance hazard if the schema name changes.

---

**B016-32** — [MEDIUM] `Task.async_stream` result destructured as `{result, reason}` — incorrect tuple shape

File: `lib/api_server_web/controllers/utility_controller.ex:5338`

Description: The `Enum.map` at line 5338 destructures each stream result as `fn {result, reason} -> ... end`. However, `Task.async_stream` yields `{:ok, value}` or `{:exit, reason}` tuples (not `{result, reason}`). The pattern `{result, reason}` will match `{:ok, value}` with `result = :ok` and `reason = value`, and match `{:exit, reason}` with `result = :exit`. The `:ok` case branch then checks `result == :ok`, which works by accident but is misleading. This pattern also silently swallows task exit errors by not propagating them — the error branch only logs to IO.

---

---

## Summary Table

| ID | Severity | Short Title | File |
|---|---|---|---|
| B016-1 | MEDIUM | `IO.inspect` in production error path + internal error in response | geofence_controller.ex:30–31 |
| B016-2 | LOW | Commented-out debug note (minor) | geofence_controller.ex:89 |
| B016-3 | LOW | `inList` bound but never used (compiler warning) | geofence_controller.ex:97 |
| B016-4 | MEDIUM | `datetime` bound but never used inside AmbiguousDateTime match | geofence_controller.ex:121 |
| B016-5 | MEDIUM | `check_event_for_left_events/6` nil clause returns wrong type — latent crash | geofence_controller.ex:132 |
| B016-6 | LOW | Inconsistent nil check style (`!= nil` vs truthy) | geofence_controller.ex:40,61 |
| B016-7 | LOW | Commented-out `IO.inspect` left in source | pivotel_controller.ex:9 |
| B016-8 | LOW | `IO.puts` debug statements in production paths | pivotel_controller.ex:5,8,47,104 |
| B016-9 | LOW | `create_update_object/1` should be `defp` | pivotel_controller.ex:20 |
| B016-10 | MEDIUM | `@doc` on `defp` functions silently ignored by Elixir | utility_controller.ex:697,802,919 |
| B016-11 | HIGH | 199-line commented-out function `send_rentals_to_rayven/2` | utility_controller.ex:1245–1443 |
| B016-12 | HIGH | Hardcoded API keys and credentials in source | utility_controller.ex:141,146,151,171,1053,1747 |
| B016-13 | MEDIUM | Hardcoded personal email addresses as alert recipients | utility_controller.ex:1703,2251,5387 |
| B016-14 | MEDIUM | Hardcoded test/historical dates in production functions | utility_controller.ex:240,2023,3310,5240 |
| B016-15 | MEDIUM | Multiple bound-but-never-used variables (compiler warnings) | utility_controller.ex (multiple) |
| B016-16 | HIGH | Empty stub functions accepting `conn` — never send response | utility_controller.ex:324,3596,3600,3615 |
| B016-17 | LOW | Commented-out Rayven HTTP calls in `process_monthly_movements/0` and `process_ebs/0` | utility_controller.ex:2421,2929 |
| B016-18 | LOW | Commented-out code blocks in `pull_equipment_data_from_rayven/1` and `pull_services_from_rayven/1` | utility_controller.ex:4709,4839 |
| B016-19 | LOW | `rayven_login/2` is an empty function with only commented-out JavaScript | utility_controller.ex:3346 |
| B016-20 | MEDIUM | Email delivery calls systematically commented out — silent no-ops with unused variable warnings | utility_controller.ex:1707,1729,5390,5613,5654 |
| B016-21 | HIGH | Massive copy-paste duplication in `process_prodisplay_event/2` (~3 near-identical branches) | utility_controller.ex:333–694 |
| B016-22 | MEDIUM | Date-formatting block (`DD/MM/YYYY`) copy-pasted 6+ times | utility_controller.ex:3799,3823,4087,4224,4387,4483 |
| B016-23 | MEDIUM | Dealer-ID and serial-prefix mapping duplicated across two functions | utility_controller.ex:1531,5417 |
| B016-24 | MEDIUM | `task_stream` consumed by `Enum.map` then `Stream.run` called on exhausted stream | utility_controller.ex:5338,5354 |
| B016-25 | LOW | `process_services_from_erp/2` defined but never called (dead private function) | utility_controller.ex:5882 |
| B016-26 | MEDIUM | Inconsistent error response format across controllers (hand-built JSON vs Poison vs render) | geofence_controller.ex, utility_controller.ex |
| B016-27 | LOW | `get_tracker_ids/0` — `custcode` bound but never used | utility_controller.ex:2090 |
| B016-28 | LOW | `pull_from_rayven/1` — decoded response bound but never read | utility_controller.ex:2005 |
| B016-29 | MEDIUM | `sync_to_DISCorp/2` — hardcoded test payload POSTed to live API | utility_controller.ex:1052 |
| B016-30 | MEDIUM | Customer DB schema strings hardcoded throughout controller — leaky abstraction | utility_controller.ex (pervasive) |
| B016-31 | LOW | `process_ebs_get_hour_meter/2` — hardcoded customer schema `"vx_cea_latest"` | utility_controller.ex:3002 |
| B016-32 | MEDIUM | `Task.async_stream` result destructured with incorrect tuple pattern | utility_controller.ex:5338 |

**Total findings: 32**
- CRITICAL: 0
- HIGH: 5 (B016-11, B016-12, B016-16, B016-21, and shared severity with B016-5 raised to MEDIUM)
- MEDIUM: 14
- LOW: 13
- INFO: 0
# Pass 4 – B017

Date: 2026-02-27
Audit run: 2026-02-27-01
Agent: B017

Files reviewed:
- lib/api_server_web/controllers/vx_abl_record_controller.ex
- lib/api_server_web/controllers/vx_access_fob_controller.ex
- lib/api_server_web/controllers/vx_customer_controller.ex

---

## Reading Evidence

### lib/api_server_web/controllers/vx_abl_record_controller.ex

**Module:** `ApiServerWeb.VXAblRecordController`

**Aliases:**
- `ApiServer.Vx` (line 4)
- `ApiServer.Vx.VXAblRecord` (line 5)

**Functions:**

| Name | Line | Visibility |
|------|------|------------|
| `create/2` | 9 | public |
| `show/2` | 18 | public |
| `update/2` | 23 | public |
| `delete/2` | 31 | public |
| `rhm_service_records/2` | 38 | public |
| `generate_service_record/3` | 66 | public |

**Types / Constants / Errors:** None defined.

**Notes:**
- `generate_service_record/3` takes `conn`, `thing`, and `new_service_date` as arguments. It is not a Phoenix action (not dispatched from the router); it is called directly from `ApiServerWeb.VXThingController.update_thing/2` (confirmed in vx_thing_controller.ex line 272).
- Line 13: uses old-style path helper `vx_abl_record_path/3`. This is correct for Phoenix 1.5.9 (project dependency confirmed in mix.exs).
- Lines 42–47: `cond` used for a two-branch boolean check.
- Lines 49–54: `cond` used for a two-branch boolean check.
- Lines 56–63: multi-pass `Enum.filter` pipeline.
- Line 58: anonymous function uses `fn(record)` form (with parens).
- Lines 96–107 and 109–120: intermediate `to_return` variable assigned and immediately returned in both `cond` branches — redundant binding.
- Lines 143–146: variables `hours_to_service`, `estimated_service_date`, `estimated_service_hours` bound but `estimated_service_date` and `estimated_service_hours` are always empty strings (dead data injected into XML).
- Line 73: `:inet_parse.ntoa` — Erlang private/internal module function used directly.
- Line 171: `{status, _result} = Vx.create_abl_record(...)` — result discarded with `_result`.

---

### lib/api_server_web/controllers/vx_access_fob_controller.ex

**Module:** `ApiServerWeb.VXAccessFobController`

**Aliases:**
- `ApiServer.Vx` (line 4)
- `ApiServer.Vx.VXAccessFob` (line 5)

**Functions:**

| Name | Line | Visibility |
|------|------|------------|
| `index/2` | 9 | public |
| `show/2` | 14 | public |
| `delete/2` | 19 | public |

**Types / Constants / Errors:** None defined.

**Notes:**
- Minimal controller: no `create` or `update` actions, only `index`, `show`, and `delete`.
- `index/2` calls `Vx.list_vxaccessfobs/0` with no tenant/customer scoping. All other controllers in this codebase scope data by `customer` extracted from JWT claims.

---

### lib/api_server_web/controllers/vx_customer_controller.ex

**Module:** `ApiServerWeb.VXCustomerController`

**Aliases:**
- `ApiServer.Vx` (line 4)
- `ApiServer.Vx.VXCustomer` (line 5)

**Functions:**

| Name | Line | Visibility |
|------|------|------------|
| `index/2` | 9 | public |
| `create/2` | 16 | public |
| `show/2` | 32 | public |
| `update/2` | 39 | public |
| `delete/2` | 51 | public |

**Types / Constants / Errors:** None defined.

**Notes:**
- `create/2` uses `with/else` to handle errors inline (lines 21–29).
- `update/2` uses bare `with` without `else`, inconsistent with `create/2`.
- `update/2` (line 45) discards the updated struct (`_vx_customer`) and then re-fetches the record from the database at line 46 to pass to the renderer — a redundant round-trip.
- `create/2` line 27: `IO.inspect error` — debug call left in production code.
- `create/2` line 28: raw JSON string constructed via string interpolation instead of using a proper encoder.
- `delete/2` line 56: responds with `send_resp(conn, :ok, "{}")` — differs from all other controllers' `delete` actions which respond with `:no_content` and empty body `""`.
- `create/2` line 21: the `with` match binds `customer` (the created `%VXCustomer{}`) shadowing the outer `customer` variable (the JWT claim string, line 17). Both variables share the same name in the same scope.

---

## Findings

**B017-1** — [MEDIUM] `IO.inspect` debug call left in production code

File: lib/api_server_web/controllers/vx_customer_controller.ex:27

Description: `IO.inspect error` is called unconditionally on every error path of `create/2`. This causes internal Ecto changeset details to be written to stdout (the application log) in all environments including production. It leaks internal schema structure and clutters logs. It is a remnant of a debugging session that was never removed.

---

**B017-2** — [MEDIUM] Raw JSON error body assembled via string interpolation instead of encoder

File: lib/api_server_web/controllers/vx_customer_controller.ex:28

Description: The error response body is constructed as:
```elixir
"{\"error\": \"error creating customer\", \"reason\": \"#{inspect error.errors}\" }"
```
`inspect/1` of an Ecto changeset error keyword list produces Elixir-formatted output (e.g., `[field: {"msg", []}]`), not valid JSON values. If any error message string contains a double-quote or a backslash the output will be malformed JSON, breaking any API client that attempts to parse the response. The same anti-pattern appears in `vx_thing_controller.ex` but is a distinct finding here. `Jason.encode!/1` or `Poison.encode!/1` (already a project dependency) should be used.

---

**B017-3** — [MEDIUM] Variable name shadowing: `customer` rebound inside `with` in `create/2`

File: lib/api_server_web/controllers/vx_customer_controller.ex:21

Description: The `with` clause matches `{:ok, %VXCustomer{} = customer}`, rebinding the name `customer` to the newly created struct. The outer `customer` (the tenant-identifier string from JWT claims, line 17) is still in scope. Within the `with` body the struct is used correctly, but the naming collision makes the code misleading and error-prone: a reader or future editor must carefully track which `customer` is which. The pattern `_vx_customer` used in `update/2` line 45 shows awareness that the match result may be discarded, but no such care was taken in `create/2`.

---

**B017-4** — [LOW] Inconsistent error handling pattern between `create/2` and `update/2` in same controller

File: lib/api_server_web/controllers/vx_customer_controller.ex:21,45

Description: `create/2` uses `with/else` and handles `{:error, error}` explicitly (lines 25–29). `update/2` uses a bare `with` (line 45) with no `else` clause, delegating failures to `FallbackController`. These are the same class of operation on the same resource. Inconsistent error-handling strategy within a single controller makes the failure behaviour of `update/2` opaque and divergent from `create/2`. One approach should be used throughout.

---

**B017-5** — [LOW] `delete/2` responds `:ok` with `"{}"` instead of `:no_content` with `""`

File: lib/api_server_web/controllers/vx_customer_controller.ex:56

Description: `VXCustomerController.delete/2` returns HTTP 200 with a JSON body `{}`. Every other `delete` action in the controller suite (`[REDACTED-AWS-SMTP-PASSWORD]`, `[REDACTED-AWS-SMTP-PASSWORD]`, `VXFleetController`, `VXRentalController`, `VXUserController`, etc.) returns HTTP 204 No Content with an empty body, which is the RESTful convention. This inconsistency breaks any client or automated test that expects 204 on successful deletion.

---

**B017-6** — [LOW] Redundant database round-trip in `update/2`

File: lib/api_server_web/controllers/vx_customer_controller.ex:45-47

Description: After successfully updating a customer, the updated struct returned by `Vx.update_vx_customer/3` is discarded (`_vx_customer`) and the record is immediately re-fetched from the database by calling `Vx.get_vx_customer!/2` again (line 46) with the same ID. This is a redundant database query on every successful update. If the update result already contains the full, updated struct it should be passed directly to the renderer.

---

**B017-7** — [LOW] Intermediate `to_return` variable bound only to be immediately returned

File: lib/api_server_web/controllers/vx_abl_record_controller.ex:100-106, 113-119

Description: In `generate_service_record/3`, both `current_hour_meter` and `input_one_hour_meter` are computed using the same pattern:
```elixir
to_return = case thing.summary.abmXxx do
  nil -> nil
  _   -> round(...)
end
to_return
```
The intermediate binding `to_return` serves no purpose; the `case` expression is itself the value. This is needless noise that reduces readability without any functional benefit.

---

**B017-8** — [LOW] `estimated_service_date` and `estimated_service_hours` are always empty strings (dead data in XML output)

File: lib/api_server_web/controllers/vx_abl_record_controller.ex:145-146, 158-159

Description: Lines 145–146 bind:
```elixir
estimated_service_date = ""
estimated_service_hours = ""
```
These variables are immediately interpolated into the XML payload at lines 158–159 and are never populated. The XML schema includes `<estimated_service_date>` and `<estimated_service_hours>` elements that are always empty. This is either dead/incomplete logic (the values were intended to be computed but never were) or dead XML fields consuming space and misleading consumers of the audit log records.

---

**B017-9** — [LOW] `generate_service_record/3` is a public function acting as a private utility

File: lib/api_server_web/controllers/vx_abl_record_controller.ex:66

Description: `generate_service_record/3` is not a Phoenix action — it is not reachable via any router entry and is not invoked via `action_fallback`. It is called by a completely different controller (`VXThingController.update_thing/2`, confirmed at vx_thing_controller.ex line 272) using a fully qualified module reference. Defining it as a `def` (public) rather than a `defp` (private) has no practical effect here because controllers cannot import each other's privates, but exposing an implementation-detail function as a public API on a controller module is a leaky abstraction. The logic should live in the `ApiServer.Vx` context module, not in a controller.

---

**B017-10** — [LOW] `VXAccessFobController.index/2` performs no tenant scoping

File: lib/api_server_web/controllers/vx_access_fob_controller.ex:10

Description: `index/2` calls `Vx.list_vxaccessfobs()` with no arguments. Every other list/index action in the neighboring controllers (`VXCustomerController.index/2`, `VXAblRecordController.rhm_service_records/2`, etc.) extracts a `customer` claim from the JWT and passes it to scope the query. If `Vx.list_vxaccessfobs/0` does not enforce tenant isolation internally, this endpoint leaks fob records across all tenants to any authenticated user.

---

**B017-11** — [INFO] `cond` with only two branches where `if` would be clearer

File: lib/api_server_web/controllers/vx_abl_record_controller.ex:42-47, 49-54, 96-107, 109-120, 122-140

Description: Several `cond` expressions in `rhm_service_records/2` and `generate_service_record/3` have exactly two branches — a condition and a `true ->` catch-all. In Elixir the idiomatic form for two-branch conditionals is `if`/`else`. While not a defect, the widespread use of `cond` for binary decisions is a style inconsistency relative to the rest of the codebase (e.g., `vx_thing_controller.ex` uses `if` for the same pattern) and reduces immediate readability. Severity set to INFO as it does not affect correctness or safety.

---

## Summary Table

| ID | Severity | File | Short Title |
|----|----------|------|-------------|
| B017-1 | MEDIUM | vx_customer_controller.ex:27 | `IO.inspect` debug call in production error path |
| B017-2 | MEDIUM | vx_customer_controller.ex:28 | Raw JSON error body assembled via `inspect` — potentially malformed |
| B017-3 | MEDIUM | vx_customer_controller.ex:21 | `customer` variable shadowed inside `with` match |
| B017-4 | LOW | vx_customer_controller.ex:21,45 | Inconsistent error handling between `create/2` and `update/2` |
| B017-5 | LOW | vx_customer_controller.ex:56 | `delete/2` returns 200 `{}` instead of 204 No Content |
| B017-6 | LOW | vx_customer_controller.ex:45-47 | Redundant database re-fetch after successful update |
| B017-7 | LOW | vx_abl_record_controller.ex:100-119 | Needless intermediate `to_return` bindings |
| B017-8 | LOW | vx_abl_record_controller.ex:145-146 | `estimated_service_date`/`hours` always empty — dead data in XML |
| B017-9 | LOW | vx_abl_record_controller.ex:66 | `generate_service_record/3` is a leaky public cross-controller function |
| B017-10 | LOW | vx_access_fob_controller.ex:10 | `index/2` performs no tenant scoping on fob listing |
| B017-11 | INFO | vx_abl_record_controller.ex (multiple) | `cond` used for two-branch conditionals throughout |
# Pass 4 – B018

**Date:** 2026-02-27
**Audit run:** 2026-02-27-01
**Agent:** B018
**Pass:** 4 – Code Quality

**Files reviewed:**
- `lib/api_server_web/controllers/vx_fleet_association_controller.ex`
- `lib/api_server_web/controllers/vx_fleet_controller.ex`
- `lib/api_server_web/controllers/vx_rental_controller.ex`
- `lib/api_server_web/controllers/vx_restriction_controller.ex`

---

## Reading Evidence

### File 1: `lib/api_server_web/controllers/vx_fleet_association_controller.ex`

**Module:** `ApiServerWeb.VXFleetAssociationController`

**Aliases:**
- `ApiServer.Vx` (line 4)
- `ApiServer.Vx.VXFleetAssociation` (line 5)

**Directives:**
- `use ApiServerWeb, :controller` (line 2)
- `action_fallback ApiServerWeb.FallbackController` (line 7)

**Functions:**

| Name | Line | Arity | Notes |
|------|------|-------|-------|
| `index/2` | 9 | 2 | Lists all fleet associations |
| `show/2` | 14 | 2 | Gets one fleet association by id |
| `delete/2` | 19 | 2 | Deletes one fleet association by id |

**Types/Errors/Constants defined:** None

---

### File 2: `lib/api_server_web/controllers/vx_fleet_controller.ex`

**Module:** `ApiServerWeb.VXFleetController`

**Aliases:**
- `ApiServer.Vx` (line 4)
- `ApiServer.Vx.VXFleet` (line 5)

**Directives:**
- `use ApiServerWeb, :controller` (line 2)
- `action_fallback ApiServerWeb.FallbackController` (line 7)

**Functions:**

| Name | Line | Arity | Notes |
|------|------|-------|-------|
| `create/2` | 9 | 2 | Original scaffold create action; uses `vx_fleet_path/3` |
| `get_fleets/2` | 19 | 2 | Admin clause — matches `%{"admin" => "1"}` |
| `get_fleets/2` | 27 | 2 | Default clause — matches any params |
| `get_fleets_with_equipment/2` | 35 | 2 | Returns fleets with embedded equipment list |
| `create_fleet/2` | 68 | 2 | Production fleet create with duplicate-name check |
| `delete_fleet/2` | 91 | 2 | Deletes fleet by customer + id |
| `get_equipment_in_fleet/2` | 105 | 2 | Returns equipment list for a fleet |
| `manage_fleet/2` | 110 | 2 | Updates fleet membership associations |
| `update_fleet/2` | 119 | 2 | Updates fleet metadata |

**Types/Errors/Constants defined:** None

---

### File 3: `lib/api_server_web/controllers/vx_rental_controller.ex`

**Module:** `ApiServerWeb.VXRentalController`

**Aliases:**
- `ApiServer.Vx` (line 4)
- `ApiServer.Vx.VXRental` (line 5)

**Directives:**
- `use ApiServerWeb, :controller` (line 2)
- `action_fallback ApiServerWeb.FallbackController` (line 7)

**Functions:**

| Name | Line | Arity | Notes |
|------|------|-------|-------|
| `get_rentals/2` | 9 | 2 | Closed-rentals clause — matches `%{"customer" => _, "closed" => "1"}` |
| `get_rentals/2` | 30 | 2 | Default clause — open rentals |
| `get_midpac_style_rental_report/2` | 51 | 2 | Anniversary-based report; contains commented-out code |
| `get_rental_anniversaries/2` | 110 | 2 | Per-equipment anniversary data |
| `create_rental/2` | 158 | 2 | Creates a rental record |
| `update_rental/2` | 174 | 2 | Updates a rental record |
| `delete_rental/2` | 191 | 2 | Deletes a rental record |
| `rhm_active_rental/2` | 206 | 2 | Returns the active rental for a hardware ID; contains dead assignment |

**Types/Errors/Constants defined:** None

---

### File 4: `lib/api_server_web/controllers/vx_restriction_controller.ex`

**Module:** `ApiServerWeb.VXRestrictionController`

**Aliases:**
- `ApiServer.Vx` (line 4)
- `ApiServer.Vx.VXRestriction` (line 5)

**Directives:**
- `use ApiServerWeb, :controller` (line 2)
- `action_fallback ApiServerWeb.FallbackController` (line 7)

**Functions:** None — module body is empty.

**Types/Errors/Constants defined:** None

---

## Findings

---

**B018-1** — [HIGH] Dead assignment in `rhm_active_rental/2`: computed values discarded before render

File: `lib/api_server_web/controllers/vx_rental_controller.ex:218`

Description: In the `_->` branch of `rhm_active_rental/2`, three values (`period_start`, `period_usage`, `overage`) are computed and then applied to `active_rental` via `Map.put_new/3` (lines 222–226). However, the result of that pipeline is never bound to a variable — it is silently discarded. The subsequent `render/4` call on line 229 passes `active_rental` unchanged (without the computed fields). The client therefore receives a rental object missing `period_start`, `period_usage`, and `overage`, even though the business logic explicitly calculated them. The corresponding `get_rentals/2` clauses (lines 17–25 and 37–45) do bind the enriched struct. This is a functional regression: the active-rental endpoint silently omits the overage data it advertises.

```elixir
# Lines 222-229 — pipeline result is dropped; active_rental is rendered unmodified
active_rental
|> Map.put_new(:period_start, period_start)
|> Map.put_new(:period_usage, period_usage)
|> Map.put_new(:overage, overage)

render(conn, "rhm_rental.json", %{vx_rental: active_rental, customer: customer})
```

---

**B018-2** — [MEDIUM] Commented-out code in `get_midpac_style_rental_report/2`

File: `lib/api_server_web/controllers/vx_rental_controller.ex:66`

Description: Line 66 contains a commented-out expression that was an alternative implementation of augmented thing lookup:

```elixir
# {thing, usage_data} = Vx.get_augmented_thing_with_hardware_id!(rental.thing.aadhardwareid, customer)
```

The commented line is inside the body of an active function and references a binding (`usage_data`) that was presumably used elsewhere. Leaving it obscures the intended design and may indicate an incomplete refactor. It should be removed or the intent documented in a code comment, not left as dead source.

---

**B018-3** — [MEDIUM] Commented-out code in `get_rentals/2` (closed-rentals clause)

File: `lib/api_server_web/controllers/vx_rental_controller.ex:10`

Description: Line 10 contains a commented-out `user` binding:

```elixir
# user = ApiServer.Guardian.Plug.current_resource(conn)
```

This is the second of two `get_rentals/2` clauses; the open-rentals clause (line 30) does not have this comment. The residual commented code suggests the user resource was once fetched and is no longer needed in this path, but was never cleaned up. It should be removed.

---

**B018-4** — [MEDIUM] Empty controller shell with unused aliases — `[REDACTED-AWS-SMTP-PASSWORD]`

File: `lib/api_server_web/controllers/vx_restriction_controller.ex:1`

Description: The module is an empty shell: it declares `use ApiServerWeb, :controller`, `action_fallback`, and aliases for `ApiServer.Vx` and `ApiServer.Vx.VXRestriction`, but defines zero action functions. The router has no routes pointing to this controller (confirmed by searching `router.ex`). The corresponding view (`VXRestrictionView`) and context functions (`list_vx_restrictions`, `get_vx_restriction!`, etc. in `vx.ex`) are fully implemented, meaning either the HTTP surface was deliberately never exposed, or the controller was started and abandoned. Both aliases are unused, which will produce compiler warnings (`alias ApiServer.Vx` and `alias ApiServer.Vx.VXRestriction` are never referenced). The module should either be completed and routed, or deleted entirely.

---

**B018-5** — [MEDIUM] Deprecated path helper `vx_fleet_path/3` — Phoenix 1.5 generates `Routes.*_path`

File: `lib/api_server_web/controllers/vx_fleet_controller.ex:13`

Description: The `create/2` action calls `vx_fleet_path(conn, :show, vx_fleet)` to build the `Location` header. In Phoenix 1.5 (the version pinned in `mix.exs`), the generated helper is `ApiServerWeb.Router.Helpers.vx_fleet_path/3`, accessed via `Routes.vx_fleet_path/3` when `Routes` is aliased. The bare unqualified form `vx_fleet_path/3` relies on importing `ApiServerWeb.Router.Helpers` somewhere in the `:controller` macro chain. While this may work at runtime, it is the pre-1.3 import-based calling convention; Phoenix 1.4+ deprecated the import in favor of explicit `Routes.*` references. This will produce a compiler warning in newer Phoenix versions and obscures where the helper originates.

---

**B018-6** — [MEDIUM] Dead function `create/2` in `VXFleetController` — not routed, superseded by `create_fleet/2`

File: `lib/api_server_web/controllers/vx_fleet_controller.ex:9`

Description: `create/2` (lines 9–16) is a scaffold-generated action that creates a fleet via `Vx.create_vx_fleet(vx_fleet_params)`. There is no route in `router.ex` that maps any HTTP method + path to `VXFleetController, :create`. The production fleet-creation endpoint uses `VXFleetController, :create_fleet` instead (PUT `/rhm/:customer/fleet/`). The dead `create/2` function is never called, adds noise, and will trigger a compiler warning about unreachable code if the router is analysed statically. It also uses a different (one-argument) `Vx.create_vx_fleet/1` arity than `create_fleet/2` uses (`Vx.create_vx_fleet/2`), indicating the scaffold was never updated to match the production context API.

---

**B018-7** — [MEDIUM] `[REDACTED-AWS-SMTP-PASSWORD]` is not routed — module is effectively dead code

File: `lib/api_server_web/controllers/vx_fleet_association_controller.ex:1`

Description: A search of `router.ex` shows no routes targeting `[REDACTED-AWS-SMTP-PASSWORD]`. The three actions (`index/2`, `show/2`, `delete/2`) are never reachable via HTTP. A separate fleet-association path is managed through `VXFleetController.manage_fleet/2`. The controller may have been an earlier CRUD scaffold that was superseded. As with `[REDACTED-AWS-SMTP-PASSWORD]`, the file should be deleted or the routes added intentionally.

---

**B018-8** — [LOW] `create_rental/2` error branch — catch-all `_ ->` match on `changeset.errors` is a no-op

File: `lib/api_server_web/controllers/vx_rental_controller.ex:167`

Description: The error path of `create_rental/2` is:

```elixir
{:error, changeset} ->
  case changeset.errors do
    _ ->
      send_resp(conn, :internal_server_error, "...")
  end
```

The `case changeset.errors do _ -> ...` construct matches every possible value of `changeset.errors` unconditionally and executes a single branch. It is equivalent to ignoring `changeset.errors` entirely. It gives the appearance of dispatching on error types but does not. This is dead branching logic; it should either be removed (leaving just `send_resp`) or replaced with real per-error-type handling.

---

**B018-9** — [LOW] Inconsistent error response HTTP status: `delete_fleet/2` and `delete_rental/2` use `:ok` (200) on success while peer operations use `:no_content` (204)

File: `lib/api_server_web/controllers/vx_fleet_controller.ex:96` and `lib/api_server_web/controllers/vx_rental_controller.ex:196`

Description: `VXFleetAssociationController.delete/2` (line 22) correctly returns HTTP 204 No Content via `send_resp(conn, :no_content, "")`. By contrast, `VXFleetController.delete_fleet/2` (line 96) and `VXRentalController.delete_rental/2` (line 196) both return HTTP 200 OK with a `{}` body on successful deletion. REST convention for successful DELETE with no response body is 204. The inconsistency means clients cannot rely on a uniform status code for DELETE success across these endpoints.

---

**B018-10** — [LOW] Style inconsistency: raw JSON strings as error bodies vs. structured responses

File: `lib/api_server_web/controllers/vx_fleet_controller.ex:77,86,98,101,129,132` and `lib/api_server_web/controllers/vx_rental_controller.ex:169,184,187,198,201,216`

Description: Error responses in `VXFleetController` and `VXRentalController` are hand-constructed JSON strings (e.g. `"{\"error\": \"error inserting update\", \"reason\": \"#{inspect result}\" }"`). `[REDACTED-AWS-SMTP-PASSWORD]` uses `action_fallback` with the Phoenix `FallbackController` pattern for error handling, which generates structured responses. The inconsistency means error shapes are not uniform. Additionally, using `inspect/1` on a changeset (lines 86 and 129 in fleet controller; lines 169 and 184 in rental controller) exposes internal Ecto changeset struct details to API consumers, which is a leaky abstraction.

---

**B018-11** — [LOW] `get_midpac_style_rental_report/2` — `usage_data` bound but never used after commented-out alternative

File: `lib/api_server_web/controllers/vx_rental_controller.ex:115`

Description: In `get_rental_anniversaries/2` (line 115):

```elixir
{thing, usage_data} = Vx.get_augmented_thing_with_hardware_id!(hardwareid, customer)
```

`usage_data` is bound but never referenced in the function body. The `_` prefix convention is not used. This will generate a compiler warning `variable "usage_data" is unused`. The fact that the parallel commented-out call in `get_midpac_style_rental_report/2` (line 66) also binds `usage_data` suggests this was intended to be used but the feature was never completed.

---

**B018-12** — [LOW] Double blank lines and inconsistent spacing throughout `VXFleetController`

File: `lib/api_server_web/controllers/vx_fleet_controller.ex:17,25,65,66`

Description: Lines 17–18, 25–26, 65–67 contain double blank lines between function definitions. Elixir convention (and the Elixir formatter) uses a single blank line between top-level function definitions. Several `def` heads also have inconsistent spacing before the opening `%{}` in their parameter lists (e.g. line 19: `def get_fleets(conn,  %{"admin" => "1"})` — double space before `%`; line 110: `def manage_fleet(conn,  %{...})`; line 119: `def update_fleet(conn,  %{...})`). This suggests the file has never been run through `mix format`.

---

**B018-13** — [LOW] `get_fleets/2` (admin clause) does not bind `_params` — bound parameter name exposes intent mismatch

File: `lib/api_server_web/controllers/vx_fleet_controller.ex:19`

Description: The admin clause head is `def get_fleets(conn, %{"admin" => "1"})`. This implicitly discards any other parameters in the map. The fallback clause uses `_params` (line 27). While this is not a compiler error, the admin clause silently ignores any other query parameters that may be present in the request, which may be surprising and represents a minor inconsistency in the guard convention used.

---

## Summary Table

| ID | Severity | Title | File(s) |
|----|----------|-------|---------|
| B018-1 | HIGH | Dead assignment in `rhm_active_rental/2`: enriched struct discarded, client receives unenriched data | `vx_rental_controller.ex:222` |
| B018-2 | MEDIUM | Commented-out code in `get_midpac_style_rental_report/2` | `vx_rental_controller.ex:66` |
| B018-3 | MEDIUM | Commented-out code in `get_rentals/2` (closed clause) | `vx_rental_controller.ex:10` |
| B018-4 | MEDIUM | Empty controller shell with unused aliases — `[REDACTED-AWS-SMTP-PASSWORD]` | `vx_restriction_controller.ex:1` |
| B018-5 | MEDIUM | Deprecated/unqualified path helper `vx_fleet_path/3` | `vx_fleet_controller.ex:13` |
| B018-6 | MEDIUM | Dead function `create/2` — no route, superseded by `create_fleet/2` | `vx_fleet_controller.ex:9` |
| B018-7 | MEDIUM | `[REDACTED-AWS-SMTP-PASSWORD]` entirely unrouted — all three actions are dead code | `vx_fleet_association_controller.ex:1` |
| B018-8 | LOW | Catch-all `case changeset.errors do _ ->` is a no-op in `create_rental/2` | `vx_rental_controller.ex:167` |
| B018-9 | LOW | DELETE success uses `:ok` (200) instead of `:no_content` (204) — inconsistent with `[REDACTED-AWS-SMTP-PASSWORD]` | `vx_fleet_controller.ex:96`, `vx_rental_controller.ex:196` |
| B018-10 | LOW | Hand-built JSON error strings expose Ecto internals via `inspect/1` — leaky abstraction | `vx_fleet_controller.ex`, `vx_rental_controller.ex` |
| B018-11 | LOW | `usage_data` bound but never used — will produce compiler warning | `vx_rental_controller.ex:115` |
| B018-12 | LOW | Double blank lines and inconsistent spacing — file never run through `mix format` | `vx_fleet_controller.ex` |
| B018-13 | LOW | Admin clause of `get_fleets/2` silently drops all non-`admin` params | `vx_fleet_controller.ex:19` |

**Totals:** 1 HIGH, 6 MEDIUM, 6 LOW
# Pass 4 – B019

**Date:** 2026-02-27
**Audit run:** 2026-02-27-01
**Agent:** B019

**Files reviewed:**
- `lib/api_server_web/controllers/vx_thing_controller.ex` (863 lines)
- `lib/api_server_web/controllers/vx_thing_event_controller.ex` (117 lines)
- `lib/api_server_web/controllers/vx_thing_info_controller.ex` (27 lines)

---

## Reading Evidence

### `ApiServerWeb.VXThingController`

**Module:** `ApiServerWeb.VXThingController`

**Uses/Aliases:**
- `use ApiServerWeb, :controller`
- `use Timex`
- `alias ApiServer.Vx`
- `alias ApiServer.Vx.VXThing`
- `action_fallback ApiServerWeb.FallbackController`

**Public functions (with line numbers):**

| # | Function | Line |
|---|----------|------|
| 1 | `get_checklists/2` (customer, hardwareid) | 10 |
| 2 | `get_movements/2` (customer, hardwareid, day, timezone) | 16 |
| 3 | `get_hardware_with_checklists/2` (customer) | 21 |
| 4 | `get_pm_data/2` (customer, hardwareid) | 30 |
| 5 | `get_all_pm_data/2` (customer) | 36 |
| 6 | `get_fleet_map/2` clause 1 (customer, fleetname) | 44 |
| 7 | `get_fleet_map/2` clause 2 (customer, fleetid) | 51 |
| 8 | `get_fleet_map/2` clause 3 (fleetid only) | 56 |
| 9 | `get_fleet_map/2` clause 4 (catch-all) | 64 |
| 10 | `create/2` (vx_thing params) | 74 |
| 11 | `show/2` (id/hardwareid) | 83 |
| 12 | `delete/2` (id) | 88 |
| 13 | `rhm_get_thing/2` (customer, hardwareid) | 95 |
| 14 | `rhm_get_thing_usage/2` (hardwareid, from, to, timezone) | 100 |
| 15 | `rhm_get_things_usage/2` (fleetid, from, to, timezone) | 111 |
| 16 | `rhm_get_thing_events/2` (hardwareid, from, to, timezone) | 144 |
| 17 | `rhm_get_things/2` clause 1 (customer, fleet_id) | 153 |
| 18 | `rhm_get_things/2` clause 2 (customer) | 161 |
| 19 | `rhm_get_things_with_usage/2` clause 1 (fleet_id) | 169 |
| 20 | `rhm_get_things_with_usage/2` clause 2 (catch-all) | 176 |
| 21 | `rhm_get_things_names/2` (customer) | 223 |
| 22 | `rhm_get_thing_records/2` (empty map) | 231 |
| 23 | `create_thing/2` (thing params) | 240 |
| 24 | `update_thing/2` (thing params) | 254 |
| 25 | `monday_hour_meters/2` (from, to, customers) | 377 |
| 26 | `get_next_monday_between_dates/4` | 438 |
| 27 | `combined_engine_usage/2` (format=csv, from, to, customers) | 453 |
| 28 | `pape_export/2` clause 1 (format=csv) | 603 |
| 29 | `pape_export/2` clause 2 (catch-all) | 617 |
| 30 | `sielift_export/2` clause 1 (format=json, fleet_id) | 724 |
| 31 | `sielift_export/2` clause 2 (format=json) | 735 |
| 32 | `sielift_export/2` clause 3 (catch-all) | 746 |
| 33 | `update_thing_cached_fields/2` (hardwareid, customer) | 850 |
| 34 | `get_timezones/2` | 859 |

**Private functions:**

| # | Function | Line |
|---|----------|------|
| 1 | `things_with_usage/2` | 184 |
| 2 | `get_data_for_pape_export/1` | 285 |
| 3 | `ifnilzero/1` clause 1 (nil) | 622 |
| 4 | `ifnilzero/1` clause 2 (value) | 623 |
| 5 | `get_data_for_sielift_export/3` | 625 |

**Constants/Types defined:** None explicitly. No `@type`, `@spec`, or module-level `@` constants.

---

### `ApiServerWeb.VXThingEventController`

**Module:** `ApiServerWeb.VXThingEventController`

**Uses/Aliases:**
- `use ApiServerWeb, :controller`
- `alias ApiServer.Vx`
- `alias ApiServer.Vx.VXThingEvent`
- `action_fallback(ApiServerWeb.FallbackController)`

**Public functions:**

| # | Function | Line |
|---|----------|------|
| 1 | `index/2` | 9 |
| 2 | `create/2` (vx_thing_event params) | 14 |
| 3 | `show/2` (id) | 24 |
| 4 | `update/2` (id, vx_thing_event params) | 29 |
| 5 | `delete/2` (id) | 38 |
| 6 | `write_partial_record/3` (customer, hardware_id, update) | 46 |
| 7 | `add_calculated_fields/2` (record_to_add, customer) | 74 |
| 8 | `get_current_omega_status/2` (conn, hardwareid) | 111 |

**Private functions:**

| # | Function | Line |
|---|----------|------|
| 1 | `calculated_hourmeter/2` | 103 |

**Constants/Types defined:** None.

---

### `ApiServerWeb.VXThingInfoController`

**Module:** `ApiServerWeb.VXThingInfoController`

**Uses/Aliases:**
- `use ApiServerWeb, :controller`
- `alias ApiServer.Vx`
- `alias ApiServer.Vx.VXThingInfo`
- `action_fallback ApiServerWeb.FallbackController`

**Public functions:**

| # | Function | Line |
|---|----------|------|
| 1 | `fix_infos/2` (customer) | 9 |
| 2 | `get_info/2` (id, customer) | 17 |
| 3 | `do_fix_info/2` (hardwareid, customer) | 24 |

**Constants/Types defined:** None.

---

## Findings

**B019-1** — [LOW] Commented-out code: `combined_engine_usage` function body (large block)
File: `lib/api_server_web/controllers/vx_thing_controller.ex:300`
Description: Lines 300–373 contain an entire commented-out `def combined_engine_usage/2` function body (73 lines). The live version of this function appears at line 453. The commented-out block retains a hardcoded customer list of 48 production tenant names, IO.puts debug statements, dead render calls, and file-write logic. This is dead code that leaks internal tenant names, provides misleading historical context, and makes the file significantly harder to read. Severity is LOW (not CRITICAL) because it is genuinely unreachable, but the tenant-name disclosure warrants attention.

---

**B019-2** — [LOW] Commented-out code: `combined_engine_usage` inner `Enum.each` block
File: `lib/api_server_web/controllers/vx_thing_controller.ex:534`
Description: Lines 534–586 inside the live `combined_engine_usage/2` function are a large commented-out `Enum.each` block (53 lines) containing an alternative implementation with file I/O (`File.open!`, `IO.write`) and render calls. This block was replaced by the surrounding `Enum.flat_map` but was never removed. It bloats the function body and embeds confusing alternative logic inline.

---

**B019-3** — [LOW] Commented-out code: `sielift_export_local` function
File: `lib/api_server_web/controllers/vx_thing_controller.ex:780`
Description: Lines 780–847 are a fully commented-out `def sielift_export_local/1` function (68 lines). It contains file-write logic (`File.open!`, `IO.write`) operating on a hardcoded filename `"on-time performance 2.csv"`. This function was never removed after the live `sielift_export` family replaced it. In addition to dead code it contains a hardcoded local filesystem path, which is a leaky abstraction concern.

---

**B019-4** — [LOW] Commented-out code: inline debug comment in `rhm_get_things_usage/2`
File: `lib/api_server_web/controllers/vx_thing_controller.ex:138`
Description: Lines 138–139 contain a commented-out `conn |> render(...)` call that represents an abandoned JSON response path for `rhm_get_things_usage`. This is a remnant of the decision to switch the endpoint from JSON to CSV and was never cleaned up. While small, it is a code-quality finding per Pass 4 rules.

---

**B019-5** — [LOW] Commented-out debug `IO.puts` statements left in production code
File: `lib/api_server_web/controllers/vx_thing_controller.ex:38,58,68,113,146,180,530,589`
Description: Multiple `# IO.puts` lines are scattered throughout `vx_thing_controller.ex` (at least 8 locations). These are leftover debug statements that were silenced rather than removed. While harmless at runtime, they clutter the code and mask intent. Each site: line 38 (`get_all_pm_data`), line 58 (`get_fleet_map` clause 3), line 68 (`get_fleet_map` catch-all), line 113 (`rhm_get_things_usage`), line 146 (`rhm_get_thing_events`), line 180 (`rhm_get_things_with_usage`), line 530 (`combined_engine_usage` inner), line 589 (`combined_engine_usage` outer).

---

**B019-6** — [MEDIUM] `get_fleet_map/2` clause 1 silently ignores the `fleetname` parameter
File: `lib/api_server_web/controllers/vx_thing_controller.ex:44`
Description: The function clause `get_fleet_map(conn, %{"customer" => customer, "fleetname" => fleetname})` matches on `fleetname` in the pattern but then calls `Vx.list_vxthings_for_map(customer, user_id)` — using the authenticated `user_id` from claims instead of `fleetname`. The matched `fleetname` variable is never used. This is a behavioral bug: callers who pass a `fleetname` expect fleet-scoped filtering; instead they receive user-scoped results silently. The Elixir compiler will emit a warning for the unused `fleetname` variable, making this a build-warning-level issue as well as a logic defect.

---

**B019-7** — [MEDIUM] `rhm_get_things/2` parameter shadowing: `customer` param overwritten by JWT claim
File: `lib/api_server_web/controllers/vx_thing_controller.ex:153`
Description: Both clauses of `rhm_get_things/2` match `%{"customer" => customer, ...}` from the request params, then immediately rebind `customer` to `ApiServer.Guardian.Plug.current_claims(conn)["customer"]`. The same pattern appears in `rhm_get_things_names/2` (line 223–224). The client-supplied `customer` value is accepted by the pattern match and then silently discarded. This is an implicit trust boundary: the function signature suggests the caller controls the customer, but the implementation always uses the JWT claim. This is misleading and could be a security concern if routing assumptions ever change. The unused bound variable from the pattern match will also generate a compiler warning.

---

**B019-8** — [MEDIUM] `things_with_usage/2` calls `Timex.now()` twice; first result is immediately discarded
File: `lib/api_server_web/controllers/vx_thing_controller.ex:185`
Description: `now = Timex.now()` is assigned at line 185 and again at line 189 (identical statement). The first binding is dead — the variable `now` is rebound before it is used. The final usage of `now` at line 192 (`Timex.now(user_timezone)`) does not use the earlier binding at all; it creates a third `now_utc` variable. The duplicated assignment suggests a copy-paste error. The first `now = Timex.now()` binding at line 185 is completely unused, which will generate a compiler warning for the shadowed variable.

---

**B019-9** — [HIGH] `rhm_get_things_usage/2` returns CSV while all sibling endpoints return JSON — undocumented format inconsistency
File: `lib/api_server_web/controllers/vx_thing_controller.ex:111`
Description: Every other `rhm_get_*` function in this controller renders a JSON response via the view layer (`render(conn, "*.json", ...)`). `rhm_get_things_usage/2` is the sole exception: it bypasses the view, sets `Content-Type: text/csv`, and streams raw CSV via `send_resp/3`. The commented-out block at lines 138–139 confirms this was a deliberate late-stage change, but no surrounding documentation or router-level annotation marks this endpoint as returning CSV. Callers expecting JSON will receive unhandled text. The inconsistency also means this endpoint is excluded from any uniform JSON error-handling or content-negotiation middleware applied to the other `rhm_get_*` routes. (Confirmed from prior pass context.)

---

**B019-10** — [MEDIUM] `combined_engine_usage/2` uses `Poison.encode!` directly instead of the view layer
File: `lib/api_server_web/controllers/vx_thing_controller.ex:591`
Description: `combined_engine_usage/2` builds a data structure and serializes it with `Poison.encode!` then calls `send_resp(200, poison_encoded)` directly, bypassing Phoenix's view/render pipeline. The same anti-pattern appears in `monday_hour_meters/2` (line 431–435) and `get_timezones/2` (line 861). This means no content-type header is set, the response bypasses any plug-level response transformations, and there is no separation between serialization and presentation. The rest of the controller exclusively uses `render(conn, "*.json", ...)`. These three functions are inconsistent with the controller's own convention and with the rest of the codebase.

---

**B019-11** — [MEDIUM] `update_thing/2` directly calls into two other controllers as side effects
File: `lib/api_server_web/controllers/vx_thing_controller.ex:272`
Description: When a service date changes, `update_thing/2` calls `ApiServerWeb.VXAblRecordController.generate_service_record(conn, thing, changeset.aadlastservice)` and `ApiServer.Vx.VXThingInfo.service_performed(...)`. Calling one controller's function from another controller is a leaky abstraction: business logic that should live in the `ApiServer.Vx` context is encoded as a side effect inside an HTTP controller action. If `generate_service_record` fails or raises, the error is unhandled (no `with`, no rescue), leaving the `update_thing` response in an indeterminate state. Additionally, passing the live `conn` struct into `[REDACTED-AWS-SMTP-PASSWORD]` means the called function has access to the full HTTP connection of the parent request.

---

**B019-12** — [MEDIUM] `create_thing/2` error response uses raw `send_resp` with hand-rolled JSON string (non-standard error format)
File: `lib/api_server_web/controllers/vx_thing_controller.ex:250`
Description: On failure, `create_thing/2` responds with `send_resp(conn, :internal_server_error, "{\"error\": \"error inserting update\", \"reason\": \"#{inspect changeset}\" }")`. The same pattern appears in `update_thing/2` at lines 278 and 282. These hand-rolled JSON strings use `inspect/1` to serialize an Ecto changeset, which produces Elixir term syntax (not valid JSON) as the `reason` value. This means the `reason` field in the error response is not parseable JSON. All other error paths in the codebase use `action_fallback` / `FallbackController`. These three ad-hoc error responses are inconsistent and produce malformed JSON responses to API consumers.

---

**B019-13** — [LOW] `combined_engine_usage/2` variable `meta_data` is bound but never used
File: `lib/api_server_web/controllers/vx_thing_controller.ex:472`
Description: `meta_data = [hardwareid, customer]` is assigned at line 472 inside the `Enum.flat_map` over things. The variable is never referenced again; `mapped_usage` is what is returned. This is a dead assignment that will generate a compiler warning (`variable "meta_data" is unused`).

---

**B019-14** — [LOW] `get_data_for_pape_export/1` comment header is stale/misleading
File: `lib/api_server_web/controllers/vx_thing_controller.ex:285`
Description: The three functions `get_checklists/2` (line 11), `get_pm_data/2` (line 31), and `get_all_pm_data/2` (line 37) all carry the comment `# Get all checklists for this hardwareid`. The comment is copy-pasted from `get_checklists` and is wrong for `get_pm_data` and `get_all_pm_data`, which retrieve PM data (preventive maintenance), not checklists. While minor, stale comments mislead future readers about the intent of the function.

---

**B019-15** — [LOW] `ifnilzero/1` is defined but never called within the file
File: `lib/api_server_web/controllers/vx_thing_controller.ex:622`
Description: The private helper `ifnilzero/1` is defined at lines 622–623 but there is no call site anywhere in `vx_thing_controller.ex`. If it is not called from any other module (controllers cannot be `import`ed from outside in normal Phoenix usage), this is dead code. The Elixir compiler will emit a warning for the unused private function.

---

**B019-16** — [MEDIUM] `get_info/2` in `[REDACTED-AWS-SMTP-PASSWORD]` binds result to `info` and always returns `{}`
File: `lib/api_server_web/controllers/vx_thing_info_controller.ex:17`
Description: `get_info/2` calls `VXThingInfo.validateForHardwareId(...)`, binds the result to `info`, then discards it and responds with `send_resp(conn, :ok, "{}")`. The client receives an empty JSON object regardless of whether validation succeeded, failed, or returned data. The unused `info` variable will generate a compiler warning. This is confirmed from prior pass context. Callers of this endpoint have no way to know the outcome of the validation call.

---

**B019-17** — [MEDIUM] `write_partial_record/3` and `add_calculated_fields/2` are public functions on a Phoenix controller — leaky abstraction
File: `lib/api_server_web/controllers/vx_thing_event_controller.ex:46`
Description: `write_partial_record/3` and `add_calculated_fields/2` are defined as `def` (public) on a Phoenix controller module. They do not accept a `conn` and are not HTTP actions; they are internal data-processing helpers called from other controllers. Making them `public` on a controller leaks business logic into the web layer's public API. `write_partial_record/3` is called from `VXThingController.update_thing_cached_fields/2` via `VXThingController` which is itself called from `[REDACTED-AWS-SMTP-PASSWORD]` — a circular dependency pattern. These functions belong in the `ApiServer.Vx` context, not on a web controller.

---

**B019-18** — [LOW] `write_partial_record/3` uses `IO.puts` and `IO.inspect` for error logging in production code
File: `lib/api_server_web/controllers/vx_thing_event_controller.ex:62`
Description: The `case` on `Vx.create_vx_thing_event/2` uses `IO.puts("Inserted")` on success (line 62) and `IO.inspect(changeset)` on error (line 67). These are `stdout` calls with no structured logging, no log level control, and no ability to be filtered or aggregated by a log management system. The success branch also binds `te` (the created record) and discards it. In a production Elixir/Phoenix application `Logger` should be used instead.

---

**B019-19** — [LOW] `add_calculated_fields/2` reassigns `record_to_add` inside an `if` branch with no effect outside the branch
File: `lib/api_server_web/controllers/vx_thing_event_controller.ex:82`
Description: Inside the `if` at line 77, `record_to_add = Map.put(record_to_add, :totalengineseconds, 0)` rebinds `record_to_add` locally within the `if` branch. In Elixir, the result of an `if` expression is the return value of the executed branch, but here the `if` expression's return value is not used — the outer scope's `record_to_add` binding is not updated. Consequently, if `totalengineseconds` is nil and `aadhourmeter` is set, the corrected value (0) is printed in the `IO.puts` but the nil value is still passed to `calculated_hourmeter/2` at line 87. This is a silent logic bug: the branch appears to fix the nil but the fix does not propagate.

---

**B019-20** — [LOW] `[REDACTED-AWS-SMTP-PASSWORD]` indentation uses 4-space indent while the other two controllers use 2-space indent
File: `lib/api_server_web/controllers/vx_thing_info_controller.ex:1`
Description: The entire `vx_thing_info_controller.ex` file uses 4-space indentation, which is inconsistent with Elixir community style (2 spaces) and with the 2-space indentation used in `vx_thing_controller.ex` and `vx_thing_event_controller.ex`. While not a runtime defect, this style inconsistency indicates the file was edited with a different editor configuration and has never been normalized.

---

**B019-21** — [MEDIUM] `action_fallback` inconsistent invocation style across files
File: `lib/api_server_web/controllers/vx_thing_event_controller.ex:7`
Description: `vx_thing_controller.ex` and `vx_thing_info_controller.ex` write `action_fallback ApiServerWeb.FallbackController` (no parentheses). `vx_thing_event_controller.ex` writes `action_fallback(ApiServerWeb.FallbackController)` (with parentheses). This is a minor style inconsistency but reflects a lack of a shared formatter configuration being enforced across the controller files.

---

**B019-22** — [HIGH] `combined_engine_usage/2` `case` on `category` has no catch-all clause — will crash on unexpected category values
File: `lib/api_server_web/controllers/vx_thing_controller.ex:495`
Description: The `case category do` block at lines 495–506 only handles values 2, 3, 4, 5, and 6. If `category` is nil, 0, 1, 7, or any other value, Elixir will raise a `CaseClauseError` at runtime, crashing the request process with a 500 and no structured error response. `Vx.get_thing_category_with_hardware_id!/2` uses the bang convention suggesting it raises on not-found, but a missing or unrecognized category in the data would still produce an unmatched category integer. The same pattern in `get_data_for_sielift_export/3` at lines 643–654 has the identical missing catch-all.

---

## Summary Table

| ID | Severity | Title | File | Line |
|----|----------|-------|------|------|
| B019-1 | LOW | Commented-out `combined_engine_usage` function body | vx_thing_controller.ex | 300 |
| B019-2 | LOW | Commented-out `Enum.each` block inside `combined_engine_usage` | vx_thing_controller.ex | 534 |
| B019-3 | LOW | Commented-out `sielift_export_local` function | vx_thing_controller.ex | 780 |
| B019-4 | LOW | Commented-out JSON render remnant in `rhm_get_things_usage` | vx_thing_controller.ex | 138 |
| B019-5 | LOW | Commented-out `IO.puts` debug statements (8 sites) | vx_thing_controller.ex | 38,58,68,113,146,180,530,589 |
| B019-6 | MEDIUM | `get_fleet_map` clause 1 ignores matched `fleetname` param | vx_thing_controller.ex | 44 |
| B019-7 | MEDIUM | `rhm_get_things` silently shadows and discards request `customer` param | vx_thing_controller.ex | 153 |
| B019-8 | MEDIUM | `things_with_usage` double-binds `now`; first binding unused | vx_thing_controller.ex | 185 |
| B019-9 | HIGH | `rhm_get_things_usage` returns CSV while all siblings return JSON | vx_thing_controller.ex | 111 |
| B019-10 | MEDIUM | `combined_engine_usage`, `monday_hour_meters`, `get_timezones` bypass view layer | vx_thing_controller.ex | 591,431,861 |
| B019-11 | MEDIUM | `update_thing` calls sibling controller functions as side effects | vx_thing_controller.ex | 272 |
| B019-12 | MEDIUM | `create_thing`/`update_thing` error paths use hand-rolled invalid JSON | vx_thing_controller.ex | 250,278,282 |
| B019-13 | LOW | `meta_data` variable bound but never used in `combined_engine_usage` | vx_thing_controller.ex | 472 |
| B019-14 | LOW | Stale/copy-pasted comments in `get_pm_data` and `get_all_pm_data` | vx_thing_controller.ex | 31,37 |
| B019-15 | LOW | `ifnilzero/1` private helper defined but never called | vx_thing_controller.ex | 622 |
| B019-16 | MEDIUM | `get_info/2` discards result, always returns `{}` | vx_thing_info_controller.ex | 17 |
| B019-17 | MEDIUM | `write_partial_record` and `add_calculated_fields` are public on a controller | vx_thing_event_controller.ex | 46,74 |
| B019-18 | LOW | `write_partial_record` uses `IO.puts`/`IO.inspect` instead of Logger | vx_thing_event_controller.ex | 62,67 |
| B019-19 | LOW | `add_calculated_fields` local rebind of `record_to_add` has no effect | vx_thing_event_controller.ex | 82 |
| B019-20 | LOW | `vx_thing_info_controller.ex` uses 4-space indent (rest of codebase uses 2) | vx_thing_info_controller.ex | 1 |
| B019-21 | MEDIUM | `action_fallback` call style inconsistent across three files | vx_thing_event_controller.ex | 7 |
| B019-22 | HIGH | `case category` in `combined_engine_usage` has no catch-all — crashes on unknown category | vx_thing_controller.ex | 495,643 |
# Pass 4 – B020

**Date:** 2026-02-27
**Audit run:** 2026-02-27-01
**Agent:** B020

**Files reviewed:**
- `lib/api_server_web/controllers/vx_thing_omega_controller.ex`
- `lib/api_server_web/controllers/vx_thing_summary_controller.ex`
- `lib/api_server_web/controllers/vx_user_controller.ex`
- `lib/api_server_web/controllers/vx_user_function_controller.ex`

---

## Reading Evidence

### File 1: `lib/api_server_web/controllers/vx_thing_omega_controller.ex`

**Module:** `ApiServerWeb.VXThingOmegaController`

**Uses/Aliases:**
- `use ApiServerWeb, :controller` (line 2)
- `use Timex` (line 3)
- `alias ApiServer.Vx` (line 5)
- `alias ApiServer.Vx.VXThing` (line 6)
- `action_fallback ApiServerWeb.FallbackController` (line 8)

**Functions:**

| Function | Line | Signature |
|---|---|---|
| `get_container_lift_report/2` | 10 | `(conn, %{"hardwareid", "from", "to"})` |
| `get_lift_summary_report/2` (clause 1) | 22 | `(conn, %{"hardwareid", "from", "to"})` |
| `get_lift_list_report/2` | 33 | `(conn, %{"hardwareid", "from", "to"})` |
| `get_lift_summary_report/2` (clause 2) | 44 | `(conn, %{"fleetid", "from", "to"})` |
| `get_operation_summary_report/2` | 53 | `(conn, %{"fleetid", "from", "to"})` |
| `get_engine_utilization_report/2` | 63 | `(conn, %{"hardwareid", "from", "to"})` |

**Types/Constants/Errors defined:** None

**Notes:**
- `VXThing` alias (line 6) is never referenced in the module body.
- `user_id` is bound in every function but is only used as an argument to `get_vx_user_offset/2`. The variable is re-bound with the same full module path (`ApiServer.Guardian.Plug.current_claims(conn)["sub"]`) in all six functions — no helper extraction.
- `get_operation_summary_report/2` (line 58) and `get_engine_utilization_report/2` (line 68) pass arguments to context functions as `(id, to_date, from_date, ...)` — note `to_date` comes before `from_date` in the call, matching the context function signatures at `vx.ex:749` and `vx.ex:726`.
- `get_container_lift_report/2` (line 16) and the other functions pass `(from_date, to_date, ...)` order — a surface-level inconsistency in the call site argument ordering that mirrors an inconsistency in the context API itself.

---

### File 2: `lib/api_server_web/controllers/vx_thing_summary_controller.ex`

**Module:** `ApiServerWeb.VXThingSummaryController`

**Uses/Aliases:**
- `use ApiServerWeb, :controller` (line 2)
- `alias ApiServer.Vx` (line 4)
- `alias ApiServer.Vx.VXThingSummary` (line 5)
- `action_fallback ApiServerWeb.FallbackController` (line 7)

**Functions:**

| Function | Line | Signature |
|---|---|---|
| `index/2` | 9 | `(conn, _params)` |
| `create/2` | 14 | `(conn, %{"vx_thing_summary" => ...})` |
| `show/2` | 23 | `(conn, %{"id" => id})` |
| `update/2` | 28 | `(conn, %{"id" => id, "vx_thing_summary" => ...})` |
| `delete/2` | 36 | `(conn, %{"id" => id})` |
| `do_fix_summary/2` | 45 | `(hardwareid, customer)` — not a Phoenix action |

**Types/Constants/Errors defined:** None

**Notes:**
- `VXThingSummary` alias is used: in pattern matches at lines 15 and 31; directly via `VXThingSummary.validate_for_hardwareid/2` at line 46.
- `do_fix_summary/2` does not follow the Phoenix action convention of `(conn, params)`. It is a public helper called from `vx_thing_controller.ex:852`.
- `create/2` at line 18 uses the deprecated Phoenix 1.5-era bare path helper `vx_thing_summary_path/3` rather than `Routes.vx_thing_summary_path/3`.

---

### File 3: `lib/api_server_web/controllers/vx_user_controller.ex`

**Module:** `ApiServerWeb.VXUserController`

**Uses/Aliases:**
- `use ApiServerWeb, :controller` (line 2)
- `alias ApiServer.Vx` (line 4)
- `alias ApiServer.Vx.VXUser` (line 5)
- `action_fallback ApiServerWeb.FallbackController` (line 7)

**Functions:**

| Function | Line | Signature |
|---|---|---|
| `create/2` | 9 | `(conn, %{"vx_user" => ...})` |
| `lookup_customer_from_conn/1` | 18 | `(conn)` |
| `login/2` | 41 | `(conn, %{"customer", "password", "email"})` |
| `change_password/2` | 59 | `(conn, %{"current_password", "new_password"})` |
| `get_users/2` | 82 | `(conn, %{"customer" => _customer})` |
| `get_user_with_email/2` | 89 | `(conn, %{"email", "customer"})` |
| `update_key_if_value/3` (clause 1 – nil guard) | 99 | `(map, key_to_save, nil)` |
| `update_key_if_value/3` (clause 2) | 100 | `(map, key_to_save, value_to_add)` |
| `update_user/2` (clause 1 – with user) | 104 | `(conn, %{"customer", "user"})` |
| `update_user/2` (clause 2 – no user key) | 127 | `(conn, %{"customer"})` |
| `create_user/2` | 131 | `(conn, %{"customer", "user"})` |
| `delete_user/2` | 153 | `(conn, %{"customer", "id"})` |
| `get_user_fleets/2` | 168 | `(conn, %{"user_id"})` |
| `manage_user_fleets/2` | 180 | `(conn, %{"user_id", "allowed_fleets"})` |

**Types/Constants/Errors defined:** None

**Notes:**
- `IO.inspect get_req_header(conn, "origin")` at line 19 is debug output left in production code.
- `create/2` (line 13) uses deprecated bare path helper `vx_user_path/3`.
- `login/2`: `user = user` at line 47 is a no-op self-assignment before `Map.put_new/3`.
- `login/2`: `cust_from_origin` (line 42) is computed but only used at line 52 (`put_session(:customer, cust_from_origin)`) — the `customer` param from the request is trusted for JWT signing (line 45) while `cust_from_origin` is only stored in the session, creating a split-authority pattern.
- `get_users/2` (line 82): `_customer` in the pattern (line 82) means the route-supplied `customer` parameter is silently discarded; `customer` is re-derived from JWT claims. The discarded parameter is not prefixed with `_` in the pattern match itself (it uses `_customer`), which is acceptable.
- `get_user_with_email/2` (line 89): destructures the result of `get_rhm_user/2` as `[user | _]` without handling the empty-list case — if the query returns `[]`, this raises a `MatchError` at runtime.
- Multiple `send_resp` JSON strings at lines 73, 117, 119, 147 contain a malformed suffix: `}\" }` — the closing brace of the JSON object is followed by an extraneous escaped-quote and space before the final `}`, producing invalid JSON on the wire.
- `change_password/2` (line 71–74): the `case changeset.errors do _ -> ...` block has only a catch-all clause — the `case` is a no-op and could be replaced by a simple expression.
- `update_key_if_value/3` is a public utility function with no callers visible in this file (not a Phoenix action). It is not referenced elsewhere in the controllers and has no `@doc`.

---

### File 4: `lib/api_server_web/controllers/vx_user_function_controller.ex`

**Module:** `ApiServerWeb.VXUserFunctionController`

**Uses/Aliases:**
- `use ApiServerWeb, :controller` (line 2)
- `alias ApiServer.Vx` (line 4)
- `alias ApiServer.Vx.VXUserFunction` (line 5)
- `action_fallback ApiServerWeb.FallbackController` (line 7)

**Functions defined (live):** None

**Functions commented out:**

| Commented function | Lines |
|---|---|
| `index/2` | 9–12 |
| `create/2` | 14–21 |
| `show/2` | 23–26 |
| `update/2` | 28–34 |
| `delete/2` | 36–41 |

**Types/Constants/Errors defined:** None

**Notes:**
- All five standard REST actions are commented out. The module body is entirely inert — the module exists only as a stub with dead commented code.
- Both aliases (`ApiServer.Vx` and `ApiServer.Vx.VXUserFunction`) and `action_fallback` are unreferenced because the module has no live code.

---

## Findings

---

**B020-1** — HIGH: All five controller actions commented out; module is entirely inert
File: `lib/api_server_web/controllers/vx_user_function_controller.ex:9-41`
Description: Every standard REST action (`index`, `create`, `show`, `update`, `delete`) is commented out across lines 9–41, leaving the module with no live functions. The module still imports `ApiServerWeb`, aliases `ApiServer.Vx` and `ApiServer.Vx.VXUserFunction`, and declares `action_fallback` — all of which are unused because there is no live code to reference them. This will produce compiler warnings for unused aliases. The module serves no runtime purpose and represents either abandoned code that should be deleted, or a planned feature that should be tracked via a proper stub or issue rather than commented code. As confirmed in the pass instructions, this was expected to be found and is reported at HIGH severity.

---

**B020-2** — MEDIUM: `IO.inspect` debug call left in production login path
File: `lib/api_server_web/controllers/vx_user_controller.ex:19`
Description: `IO.inspect get_req_header(conn, "origin")` is called unconditionally inside `lookup_customer_from_conn/1`, which is itself called on every invocation of the `login/2` action. This writes the raw `Origin` request header to stdout on every login attempt. In production this pollutes logs, leaks request metadata, and was clearly left over from development. It should be removed.

---

**B020-3** — MEDIUM: Malformed JSON in multiple `send_resp` error responses
File: `lib/api_server_web/controllers/vx_user_controller.ex:73, 117, 119, 147`
Description: Four `send_resp` calls produce invalid JSON. Each affected string closes the JSON object correctly (`}`) and then appends `\" }` — a literal escaped double-quote followed by a space and a closing brace — outside the JSON structure. For example, line 117:
```
"{\"error\": \"Error updating user\", \"reason\": \"...\"}\" }"
```
The trailing `\" }` is not valid JSON. Any client attempting to parse these responses will receive a parse error. Affected lines: 73 (`change_password`), 117 and 119 (`update_user`), 147 (`create_user`).

---

**B020-4** — MEDIUM: `get_user_with_email/2` will crash on empty result set
File: `lib/api_server_web/controllers/vx_user_controller.ex:90`
Description: `Vx.get_rhm_user/2` (2-arity) returns a list via `Repo.all`. Line 90 unconditionally destructures the result as `[user | _]`. If no user is found the list is `[]`, which does not match the pattern and raises a `MatchError` (an unhandled exception) rather than returning the intended 500 error response. The nil check on line 92 (`if user != nil`) will never handle this case because execution does not reach it when the list is empty. This path also leaks the existence check through the wrong status code (500 instead of 404) and uses a login error message for a non-login endpoint.

---

**B020-5** — MEDIUM: Unused alias `ApiServer.Vx.VXThing` in omega controller
File: `lib/api_server_web/controllers/vx_thing_omega_controller.ex:6`
Description: `alias ApiServer.Vx.VXThing` is declared at line 6 but `VXThing` is never referenced anywhere in the module body. All context operations go through the `Vx` alias. Elixir will emit a compiler warning for this unused alias. Dead aliases obscure the module's actual dependencies.

---

**B020-6** — MEDIUM: Unused aliases and `action_fallback` in `[REDACTED-AWS-SMTP-PASSWORD]`
File: `lib/api_server_web/controllers/vx_user_function_controller.ex:4-7`
Description: Because all actions are commented out, `alias ApiServer.Vx` (line 4), `alias ApiServer.Vx.VXUserFunction` (line 5), and `action_fallback ApiServerWeb.FallbackController` (line 7) all refer to names that are never used in any live code. Elixir will emit "unused alias" compiler warnings for lines 4 and 5. This is a direct consequence of B020-1 but is a distinct compiler-warning pattern worth tracking separately.

---

**B020-7** — LOW: Deprecated bare path helper used in `create/2` actions
File: `lib/api_server_web/controllers/vx_thing_summary_controller.ex:18`
File: `lib/api_server_web/controllers/vx_user_controller.ex:13`
Description: Both `create/2` actions use the Phoenix 1.3-era bare path helper syntax (`vx_thing_summary_path/3` and `vx_user_path/3`) rather than the `Routes.*_path` helper form introduced in Phoenix 1.4 and the verified-routes form introduced in Phoenix 1.7. The project is on Phoenix 1.5.9 (`mix.exs:36`), where these helpers still function but were already deprecated in favour of `Routes.*_path`. This is a build warning pattern; newer Phoenix versions would refuse to compile these.

---

**B020-8** — LOW: `user = user` no-op self-assignment in `login/2`
File: `lib/api_server_web/controllers/vx_user_controller.ex:47`
Description: Inside the `{:ok, token, _claims}` branch of `login/2`, line 47 reads `user = user` before calling `Map.put_new(:jwt, token)`. The self-assignment is a no-op: it rebinds `user` to its own current value. This produces no semantic difference but indicates the code was incorrectly written (the intent was presumably to pipe `user` through `Map.put_new/3` inline rather than via a multi-line pipe). The Elixir compiler may emit a warning about a variable being assigned and immediately used without transformation.

---

**B020-9** — LOW: Redundant `case` with catch-all in `change_password/2`
File: `lib/api_server_web/controllers/vx_user_controller.ex:71-74`
Description: The `{:error, changeset}` branch of `change_password/2` contains:
```elixir
case changeset.errors do
  _ ->
    send_resp(...)
end
```
A `case` expression with only a catch-all clause (`_`) is semantically identical to evaluating the expression and ignoring its value, then executing the body unconditionally. The `case` adds no branching logic. This pattern suggests that error-specific handling (similar to `update_user/2`) was intended but never implemented. As written it is dead structure.

---

**B020-10** — LOW: Pervasive copy-paste of JWT claims extraction across all omega controller actions
File: `lib/api_server_web/controllers/vx_thing_omega_controller.ex:11-13, 23-25, 34-36, 45-47, 54-56, 64-66`
Description: All six functions in `[REDACTED-AWS-SMTP-PASSWORD]` repeat the identical three-line block:
```elixir
customer = ApiServer.Guardian.Plug.current_claims(conn)["customer"]
user_id = ApiServer.Guardian.Plug.current_claims(conn)["sub"]
user_timezone = ApiServer.Vx.get_vx_user_offset(user_id, customer)
```
`ApiServer.Guardian.Plug.current_claims(conn)` is called twice per function (12 total calls across the module) when a single call and local destructuring would suffice. This duplication is a style inconsistency relative to the rest of the codebase and a maintenance hazard: any change to claims key names must be made in six places. A private helper or a Plug-level assign would eliminate the repetition.

---

**B020-11** — LOW: `do_fix_summary/2` is a non-action public function placed inside a Phoenix controller
File: `lib/api_server_web/controllers/vx_thing_summary_controller.ex:45-47`
Description: `do_fix_summary/2` does not follow the Phoenix controller action signature `(conn, params)`. It accepts `(hardwareid, customer)` and is called cross-module from `vx_thing_controller.ex:852`. Placing a utility/helper function inside a controller module creates a leaky abstraction: the controller's public surface now includes a non-HTTP function that couples `VXThingController` to `[REDACTED-AWS-SMTP-PASSWORD]` at the module level. This logic belongs in the `ApiServer.Vx` context layer, not in a web controller. The function also has no `@doc`.

---

**B020-12** — LOW: `update_key_if_value/3` is a public utility function with no callers in any controller
File: `lib/api_server_web/controllers/vx_user_controller.ex:99-102`
Description: `update_key_if_value/3` is a public function (two clauses) that wraps `Map.put_new/3` with a nil-guard. A search of the controller layer finds no callers. If this function is only called from within the same file it should be declared `defp`; if it is unused entirely it is dead code. Its presence as a public function makes it part of the module's public API surface, which is misleading in a Phoenix controller context.

---

**B020-13** — LOW: Argument order inversion for `to_date`/`from_date` in omega report calls
File: `lib/api_server_web/controllers/vx_thing_omega_controller.ex:58, 68`
Description: `get_operation_summary_report/2` (line 58) and `get_engine_utilization_report/2` (line 68) both call their respective context functions with `to_date` as the second argument and `from_date` as the third, matching the context function signatures at `vx.ex:749` and `vx.ex:726`. However, all other report functions in this controller (`get_container_lift_report/2`, `get_lift_summary_report/2`, `get_lift_list_report/2`) pass `from_date` before `to_date`. This inconsistency in argument order across the context API — some functions take `(from, to)`, others take `(to, from)` — is surfaced visibly in the controller and is a style and safety concern: a developer adding a new report function must know which ordering each context function expects.

---

**B020-14** — LOW: `login/2` uses request `customer` param for JWT but `Origin`-derived value only for session
File: `lib/api_server_web/controllers/vx_user_controller.ex:41-57`
Description: `login/2` derives `cust_from_origin` by mapping the `Origin` header to a customer slug (line 42), but then signs the JWT with the `customer` value from the **request body** (line 45). The Origin-derived value is only stored in the session (line 52). These two customer values can differ with no error or reconciliation. If a client sends `customer: "vx_admin"` in the POST body with any `Origin` header, the JWT will be signed for `vx_admin` regardless of the origin check. The origin-mapping logic in `lookup_customer_from_conn/1` only affects the session, not the authoritative JWT claim. This is a security-relevant inconsistency in the authentication flow.

---

## Summary Table

| ID | Severity | File | Short Title |
|---|---|---|---|
| B020-1 | HIGH | vx_user_function_controller.ex:9-41 | All 5 REST actions commented out; module entirely inert |
| B020-2 | MEDIUM | vx_user_controller.ex:19 | `IO.inspect` debug call in production login path |
| B020-3 | MEDIUM | vx_user_controller.ex:73,117,119,147 | Malformed JSON in 4 `send_resp` error responses |
| B020-4 | MEDIUM | vx_user_controller.ex:90 | `get_user_with_email/2` crashes on empty query result |
| B020-5 | MEDIUM | vx_thing_omega_controller.ex:6 | Unused alias `VXThing` — will emit compiler warning |
| B020-6 | MEDIUM | vx_user_function_controller.ex:4-5 | Unused aliases produce compiler warnings (consequence of B020-1) |
| B020-7 | LOW | vx_thing_summary_controller.ex:18, vx_user_controller.ex:13 | Deprecated bare path helpers |
| B020-8 | LOW | vx_user_controller.ex:47 | `user = user` no-op self-assignment |
| B020-9 | LOW | vx_user_controller.ex:71-74 | Redundant `case` with only catch-all clause |
| B020-10 | LOW | vx_thing_omega_controller.ex (6 sites) | Copy-paste JWT claims extraction across all 6 actions |
| B020-11 | LOW | vx_thing_summary_controller.ex:45 | Non-action public function `do_fix_summary/2` in controller |
| B020-12 | LOW | vx_user_controller.ex:99 | `update_key_if_value/3` public with no visible callers |
| B020-13 | LOW | vx_thing_omega_controller.ex:58,68 | Inconsistent `from_date`/`to_date` argument order in context API |
| B020-14 | LOW | vx_user_controller.ex:41-57 | JWT signed from request body `customer`; origin check only affects session |
# Pass 4 – B021

**Date:** 2026-02-27
**Audit run:** 2026-02-27-01
**Agent:** B021
**Pass:** 4 (Code Quality)

**Files reviewed:**
- `lib/api_server_web/resolvers/puls.ex`
- `lib/api_server_web/resolvers/things.ex`

---

## Reading Evidence

### File 1: `lib/api_server_web/resolvers/puls.ex`

**Module:** `ApiServerWeb.Resolvers.Puls`

**Functions:**

| Function | Line |
|---|---|
| `puls_record/3` | 3 |

**Types defined:** none
**Constants defined:** none (inline literal token at line 4)
**Errors defined:** none
**Aliases/imports:** none

---

### File 2: `lib/api_server_web/resolvers/things.ex`

**Module:** `ApiServerWeb.Resolvers.Things`

**Functions:**

| Function | Line |
|---|---|
| `find_thing/3` | 3 |
| `get_all_things/3` | 13 |

**Types defined:** none
**Constants defined:** none
**Errors defined:** none
**Aliases/imports:** none

---

## Findings

---

**B021-1** — [CRITICAL] Hardcoded Base64-encoded credential in source code

File: `lib/api_server_web/resolvers/puls.ex:4`

Description: A Base64-encoded Basic Auth token (`"VHJhY2tpbmdTb2x1dGlvbnM6U2tQREk4ZXo="`) is hardcoded directly in the function body. Decoding this value yields a plaintext `username:password` pair for the CalAmp PULS service. Embedding credentials in source code exposes them to anyone with repository access, in version-control history, and in compiled BEAM files. The token cannot be rotated without a code change and redeployment. This credential must be moved to runtime configuration (e.g., `Application.fetch_env!/2` backed by a secret manager or environment variable).

---

**B021-2** — [HIGH] `receive/after` used to implement a blocking retry sleep inside a GraphQL resolver

File: `lib/api_server_web/resolvers/puls.ex:12-17`

Description: When the HTTP call returns `:error`, the resolver enters a `receive` block with a 60-second `after` timeout, then tail-calls itself recursively. This has several severe consequences:

1. The calling process (the Absinthe/Cowboy request handler) is blocked for at least 60 seconds per retry, consuming a scheduler thread and holding the HTTP connection open until the client times out.
2. There is no retry limit. If the CalAmp endpoint is persistently unavailable, the process will loop indefinitely until the client disconnects or the VM is restarted.
3. `receive` with only an `after` clause is an anti-pattern for sleeping; `Process.sleep/1` is the correct primitive if sleeping is genuinely required, but neither belongs in a synchronous resolver.
4. The unbounded recursion can exhaust the call stack under a sufficiently long outage.

The correct remediation is to return `{:error, reason}` immediately on HTTP failure and let the caller (client) decide on retry strategy, or use a background process / circuit breaker.

---

**B021-3** — [HIGH] `IO.puts` debug output left in production resolver code

File: `lib/api_server_web/resolvers/puls.ex:11`

Description: `IO.puts "Will attempt Re-send"` writes to standard output on every HTTP error. In a production Phoenix/OTP deployment, `IO.puts` bypasses the Logger subsystem entirely: output goes directly to the group leader and is not captured by log aggregators, log levels, or metadata. This is a build-warning-level issue under many static analysis tools and a runtime concern in production because it cannot be suppressed without a code change. All diagnostic output must use `Logger` with an appropriate level (`Logger.warn/2` or `Logger.error/2`).

---

**B021-4** — [MEDIUM] Variable `record` is rebound inside a `case` branch, shadowing the outer `case` result binding

File: `lib/api_server_web/resolvers/puls.ex:9-25`

Description: The outer assignment is `record = case status do ...`. Inside the `:ok` branch (line 20), a second `record = %{...}` binding is created. In Elixir, the inner binding shadows the outer one within that branch and the outer `record` variable ultimately receives the value of the last expression in the matching branch. While this is syntactically legal and produces the intended result, it is confusing: a reader must reason that the inner `record` is simultaneously the return value of the branch and the variable assigned at the outer level. The standard Elixir idiom is to omit the inner binding name entirely and just write the map literal as the branch expression. This pattern can cause maintainers to introduce bugs if the inner and outer bindings are ever modified independently.

---

**B021-5** — [MEDIUM] `get_vx_thing_with_hardware_id!/2` does not raise — bang-name is misleading and `nil` return is matched in `case`

File: `lib/api_server_web/resolvers/things.ex:4`

Description: The function `ApiServer.Vx.get_vx_thing_with_hardware_id!/2` (defined in `lib/api_server/vx/vx.ex:1347`) calls `Repo.one/2`, which returns `nil` when no record is found rather than raising. The bang (`!`) suffix in Elixir conventionally signals that the function raises on failure. The resolver at line 5 explicitly matches `nil ->` as a normal return value from this function, which confirms the function never raises. This is a leaky abstraction: the name promises a raising contract that does not exist, and every call site must add a `nil` guard that would be unnecessary if the name were correct (i.e., `get_vx_thing_with_hardware_id/2`). Any future caller who trusts the bang name and omits the nil check will get a runtime error downstream when the nil propagates.

---

**B021-6** — [MEDIUM] `get_all_things/3` matches `nil` as the error case for `list_vxthings/1`, but `list_vxthings` returns an empty list `[]` on no results, not `nil`

File: `lib/api_server_web/resolvers/things.ex:14-20`

Description: `ApiServer.Vx.list_vxthings/1` (defined in `lib/api_server/vx/vx.ex:470`) calls `Repo.all/2`, which always returns a list — either populated or `[]` — and never returns `nil`. The `nil ->` branch in the `case` on line 15 is therefore unreachable dead code. The genuine error condition (e.g., a database exception) would propagate as an uncaught exception rather than being converted to an `{:error, ...}` tuple. Callers observing a database outage will receive a 500-level crash instead of a structured GraphQL error response. The `nil` clause should be replaced with a `rescue` block or the query should be wrapped in a `try`/`rescue`.

---

**B021-7** — [LOW] Inconsistent indentation style between the two resolver files

File: `lib/api_server_web/resolvers/puls.ex` (4-space indent) vs `lib/api_server_web/resolvers/things.ex` (2-space indent for function bodies, mixed 4-space inside case)

Description: `puls.ex` uses 4-space indentation consistently. `things.ex` uses 2-space indentation for function bodies (lines 4, 14) but the closing `end` alignment is inconsistent (lines 19-21 show mixed 2/4-space nesting). The Elixir community standard (enforced by `mix format`) is 2-space indentation. Neither file appears to have been run through `mix format`. While this does not affect runtime behavior, it increases cognitive load when reading across files and indicates the formatter has not been applied to this module directory.

---

**B021-8** — [LOW] Double space in string literal produces incorrect error message

File: `lib/api_server_web/resolvers/things.ex:6`

Description: The error string `"Thing with  HardwareId #{hardwareid} not found"` contains two consecutive spaces between "with" and "HardwareId". This is a typographical error in a user-visible error message that will appear in GraphQL error responses returned to API clients.

---

**B021-9** — [LOW] No module-level `use` / `alias` declarations; full module paths repeated inline

File: `lib/api_server_web/resolvers/things.ex:4,14`

Description: Both calls use the fully-qualified name `ApiServer.Vx.*` rather than an `alias ApiServer.Vx` at the top of the module. The sibling `puls.ex` makes HTTP calls without an alias as well. While this is not a compile or runtime issue, it is inconsistent with the style used in the project's controllers (which uniformly use `alias`), makes the module harder to read, and requires changes in multiple places if the context module is renamed. This is a style inconsistency relative to other files in the same web layer.

---

## Summary Table

| ID | Severity | Title | File(s) |
|---|---|---|---|
| B021-1 | CRITICAL | Hardcoded Base64-encoded credential in source code | `resolvers/puls.ex:4` |
| B021-2 | HIGH | `receive/after` blocking retry loop inside GraphQL resolver | `resolvers/puls.ex:12-17` |
| B021-3 | HIGH | `IO.puts` debug output in production resolver | `resolvers/puls.ex:11` |
| B021-4 | MEDIUM | Inner `record` variable shadows outer `case` result binding | `resolvers/puls.ex:9-25` |
| B021-5 | MEDIUM | Bang-named function does not raise; nil-return matched in resolver | `resolvers/things.ex:4` |
| B021-6 | MEDIUM | Unreachable `nil` branch — `list_vxthings` never returns nil | `resolvers/things.ex:14-20` |
| B021-7 | LOW | Inconsistent indentation style between resolver files | `resolvers/puls.ex`, `resolvers/things.ex` |
| B021-8 | LOW | Double space in user-visible error message string | `resolvers/things.ex:6` |
| B021-9 | LOW | No aliases; full module paths repeated inline, inconsistent with project style | `resolvers/things.ex:4,14` |

**Total findings: 9**
- CRITICAL: 1
- HIGH: 2
- MEDIUM: 3
- LOW: 3
# Pass 4 – B022

**Date:** 2026-02-27
**Audit run:** 2026-02-27-01
**Agent:** B022

**Files reviewed:**
- `lib/api_server_web/router.ex`
- `lib/api_server_web/schema.ex`
- `lib/api_server_web/schema/thing_types.ex`

---

## Reading Evidence

### lib/api_server_web/router.ex

**Module:** `ApiServerWeb.Router`

No named functions are defined directly. The file uses Phoenix router macros only.

**Pipelines defined:**
| Name | Line |
|---|---|
| `:browser` | 4 |
| `:api` | 12 |
| `:api_xml` | 18 |
| `:authenticated` | 24 |

**Scopes defined:**
| Scope path | Line | Pipelines |
|---|---|---|
| `/api/v1` (first) | 28 | none at scope open; `pipe_through([:api, :authenticated])` at line 33 |
| `/api/v1` (second) | 156 | `:api` |
| `/` | 179 | `:api_xml` |

**Routes (in order of appearance):**

| Line | Verb | Path | Controller | Action |
|---|---|---|---|---|
| 30 | GET | `/api/v1/rhm/engine_usage` | VXThingController | `:combined_engine_usage` |
| 31 | GET | `/api/v1/rhm/monday_hour_meters` | VXThingController | `:monday_hour_meters` |
| 36 | GET | `/api/v1/rhm/pape_export` | VXThingController | `:pape_export` |
| 37 | GET | `/api/v1/rhm/sielift_export` | VXThingController | `:sielift_export` |
| 40 | GET | `/api/v1/rhm/reports/geofence_events` | GeofenceController | `:process_things_geofences` |
| 41 | (commented out) | `/api/v1/rhm/work_in_progress` | VXThingController | `:work_in_progress` |
| 42 | GET | `/api/v1/rhm/work_in_progress` | VXThingController | `:sielift_export` |
| 45 | GET | `/api/v1/rhm/things_with_usage` | VXThingController | `:rhm_get_things_with_usage` |
| 46 | GET | `/api/v1/rhm/thing_records` | VXThingController | `:rhm_get_thing_records` |
| 47 | GET | `/api/v1/rhm/:customer/things/names` | VXThingController | `:rhm_get_things_names` |
| 48 | GET | `/api/v1/rhm/:customer/things` | VXThingController | `:rhm_get_things` |
| 50 | GET | `/api/v1/rhm/thing/:hardwareid/events` | VXThingController | `:rhm_get_thing_events` |
| 51 | GET | `/api/v1/rhm/thing/:hardwareid/usage` | VXThingController | `:rhm_get_thing_usage` |
| 52 | GET | `/api/v1/rhm/:customer/thing/:hardwareid` | VXThingController | `:rhm_get_thing` |
| 53 | GET | `/api/v1/rhm/thing/:hardwareid/active_rental` | VXRentalController | `:rhm_active_rental` |
| 54 | POST | `/api/v1/rhm/thing/` | VXThingController | `:update_thing` |
| 55 | PUT | `/api/v1/rhm/thing/` | VXThingController | `:create_thing` |
| 56 | GET | `/api/v1/rhm/thing/:hardwareid/omega_data` | VXThingEventController | `:get_current_omega_status` |
| 57 | GET | `/api/v1/vx/:customer/thing/:hardwareid/movements/:day` | VXThingController | `:get_movements` |
| 60–64 | GET | `/api/v1/rhm/omega_thing/:hardwareid/container_lift_report` | VXThingOmegaController | `:get_container_lift_report` |
| 66–70 | GET | `/api/v1/rhm/omega_thing/:hardwareid/lift_summary_report` | VXThingOmegaController | `:get_lift_summary_report` |
| 72–76 | GET | `/api/v1/rhm/omega_thing/:hardwareid/lift_list_report` | VXThingOmegaController | `:get_lift_list_report` |
| 78–82 | GET | `/api/v1/rhm/omega_fleet/:fleetid/lift_summary_report` | VXThingOmegaController | `:get_lift_summary_report` |
| 84–88 | GET | `/api/v1/rhm/omega_thing/:hardwareid/engine_utilization_report` | VXThingOmegaController | `:get_engine_utilization_report` |
| 90–94 | GET | `/api/v1/rhm/omega_fleet/:fleetid/operation_summary_report` | VXThingOmegaController | `:get_operation_summary_report` |
| 96–100 | GET | `/api/v1/rhm/omega_fleet/:fleetid/operation_summary_report` | VXThingOmegaController | `:get_operation_summary_report` |
| 103 | GET | `/api/v1/rhm/fleets` | VXFleetController | `:get_fleets` |
| 104 | GET | `/api/v1/rhm/fleets_with_equipment` | VXFleetController | `:get_fleets_with_equipment` |
| 105 | PUT | `/api/v1/rhm/:customer/fleet/` | VXFleetController | `:create_fleet` |
| 106 | DELETE | `/api/v1/rhm/:customer/fleet/:id` | VXFleetController | `:delete_fleet` |
| 107 | POST | `/api/v1/rhm/:customer/fleet/` | VXFleetController | `:update_fleet` |
| 108 | GET | `/api/v1/rhm/:customer/fleet/:id/equipment` | VXFleetController | `:get_equipment_in_fleet` |
| 109 | POST | `/api/v1/rhm/:customer/fleet/:id/manage` | VXFleetController | `:manage_fleet` |
| 112 | GET | `[REDACTED-AWS-SMTP-PASSWORD]` | VXAblRecordController | `:rhm_service_records` |
| 115 | GET | `/api/v1/rhm/:customer/rentals` | VXRentalController | `:get_rentals` |
| 116 | POST | `/api/v1/rhm/:customer/rentals/` | VXRentalController | `:update_rental` |
| 117 | PUT | `/api/v1/rhm/:customer/rentals/` | VXRentalController | `:create_rental` |
| 118 | DELETE | `/api/v1/rhm/:customer/rentals/:id` | VXRentalController | `:delete_rental` |
| 120–124 | GET | `/api/v1/rhm/thing/:hardwareid/rental_anniversaries` | VXRentalController | `:get_rental_anniversaries` |
| 126 | GET | `/api/v1/rhm/rentals/midpac_style_report` | VXRentalController | `:get_midpac_style_rental_report` |
| 129 | POST | `/api/v1/rhm/user/change_password` | VXUserController | `:change_password` |
| 130 | GET | `/api/v1/rhm/user/:user_id/fleets` | VXUserController | `:get_user_fleets` |
| 131 | POST | `/api/v1/rhm/user/:user_id/fleets` | VXUserController | `:manage_user_fleets` |
| 132 | GET | `/api/v1/rhm/:customer/users` | VXUserController | `:get_users` |
| 133 | GET | `/api/v1/rhm/:customer/user/:email` | VXUserController | `:get_user_with_email` |
| 134 | POST | `/api/v1/rhm/:customer/user/` | VXUserController | `:update_user` |
| 135 | PUT | `/api/v1/rhm/:customer/user/` | VXUserController | `:create_user` |
| 136 | DELETE | `/api/v1/rhm/:customer/user/:id` | VXUserController | `:delete_user` |
| 139 | GET | `[REDACTED-AWS-SMTP-PASSWORD]` | VXCustomerController | `:index` |
| 140 | GET | `/api/v1/rhm/customer/:id` | VXCustomerController | `:show` |
| 141 | POST | `[REDACTED-AWS-SMTP-PASSWORD]` | VXCustomerController | `:update` |
| 142 | PUT | `[REDACTED-AWS-SMTP-PASSWORD]` | VXCustomerController | `:create` |
| 143 | DELETE | `/api/v1/rhm/customer/:id` | VXCustomerController | `:delete` |
| 146 | GET | `[REDACTED-AWS-SMTP-PASSWORD]` | VXThingController | `:get_fleet_map` |
| 147 | GET | `/api/v1/rhm/fleetmap/:fleetid` | VXThingController | `:get_fleet_map` |
| 150 | GET | `[REDACTED-AWS-SMTP-PASSWORD]` | GeofenceController | `:list_all_geofences` |
| 151 | PUT | `[REDACTED-AWS-SMTP-PASSWORD]` | GeofenceController | `:create_geofence` |
| 152 | POST | `[REDACTED-AWS-SMTP-PASSWORD]` | GeofenceController | `:update_geofence` |
| 153 | DELETE | `/api/v1/rhm/geofence/:id` | GeofenceController | `:delete_geofence` |
| 159 | GET | `/api/v1/hc` | UtilityController | `:do_health_check` |
| 160 | POST | `/api/v1/rhm/:customer/login/` | VXUserController | `:login` |
| 162 | resources | `[REDACTED-AWS-SMTP-PASSWORD]` | VXThingSummaryController | (except :new, :edit) |
| 164 | (commented out) | `/api/v1/files` | FileController | `:index` |
| 165 | GET | `/api/v1/files/getsize/:esn` | FileController | `:get_size` |
| 166 | GET | `/api/v1/files/getfile/:esn` | FileController | `:send_file_download` |
| 169 | GET | `/api/v1/vx/:customer/thing/with_checklists` | VXThingController | `:get_hardware_with_checklists` |
| 170 | GET | `/api/v1/vx/:customer/thing/:hardwareid/checklists` | VXThingController | `:get_checklists` |
| 171 | GET | `/api/v1/vx/:customer/pmServicesAjax/:hardwareid` | VXThingController | `:get_pm_data` |
| 172 | GET | `/api/v1/vx/:customer/pmServicesAjax` | VXThingController | `:get_all_pm_data` |
| 173 | GET | `/api/v1/vx/:customer/rentalStats` | VXThingController | `:get_all_rental_stats` |
| 175 | GET | `[REDACTED-AWS-SMTP-PASSWORD]` | VXThingController | `:get_timezones` |
| 176 | GET | `/api/v1/rhm/:customer/fix_info` | VXThingInfoController | `:fix_infos` |
| 182 | GET | `/` | UtilityController | `:do_health_check` |
| 183 | GET | `/geocode` | UtilityController | `:do_geocode_lookup` |
| 184 | GET | `/error/:status_code` | UtilityController | `:do_error` |
| 185 | POST | `/test-omega-data` | UtilityController | `:process_incoming_omegawatch_data` |
| 186 | POST | `/prodisplay/event` | UtilityController | `:process_prodisplay_event` |
| 188 | POST | `/` | DigitalMatterController | `:get_g62_data` |
| 190 | POST | `/erp-import` | UtilityController | `:erp_import` |
| 191 | POST | `/driverid-converter` | UtilityController | `:driverid_converter` |
| 192 | GET | `/dis-sync` | UtilityController | `:sync_to_DISCorp` |

**Commented-out blocks:**
- Lines 13 (inside `:api` pipeline): `# plug CORSPlug, origin: "*"`
- Lines 19 (inside `:api_xml` pipeline): `# plug CORSPlug, origin: "*"`
- Line 41: `# get "/rhm/work_in_progress", VXThingController, :work_in_progress`
- Line 164: `# get "/files", FileController, :index`
- Lines 195–202: entire GraphQL `forward` block for `/graphql` and `/graphiql`

---

### lib/api_server_web/schema.ex

**Module:** `ApiServerWeb.Schema`

No named functions are defined. The file uses Absinthe schema macros only.

**Imports / aliases:**
| Item | Line |
|---|---|
| `use Absinthe.Schema` | 3 |
| `import_types Absinthe.Type.Custom` | 4 |
| `import_types ApiServerWeb.Schema.ThingTypes` | 5 |
| `alias ApiServerWeb.Resolvers` | 6 |

**GraphQL fields defined in `query` block:**
| Field name | Line | Return type | Arguments |
|---|---|---|---|
| `:get_thing` | 11 | `:thing` | `aadhardwareid` (non-null string), `customer` (non-null string) |
| `:get_puls_record` | 18 | `:puls_record` | `hardwareid` (non-null string) |
| `:get_all_things` | 23 | `list_of(:thing)` | `customer` (non-null string) |

**Resolvers referenced:**
- `Resolvers.Things.find_thing/3` (line 14)
- `Resolvers.Puls.puls_record/3` (line 20)
- `Resolvers.Things.get_all_things/3` (line 26)

**Commented-out code:** None within this file itself — the GraphQL forwarding is commented out in router.ex, not here.

---

### lib/api_server_web/schema/thing_types.ex

**Module:** `ApiServerWeb.Schema.ThingTypes`

No named functions. Uses Absinthe schema notation macros.

**Types defined:**

`:thing` object (line 5–37):
| Field | Type |
|---|---|
| `aadcustcode` | `:string` |
| `aaddesc` | `:string` |
| `aadintext` | `:string` |
| `aadaddr` | `:string` |
| `aadcustomerid` | `:integer` |
| `aadcat` | `:integer` |
| `aadhardwareid` | `:string` |
| `aadhw_type` | `:integer` |
| `aadmake` | `:string` |
| `aadmodel` | `:string` |
| `aadserialno` | `:string` |
| `aadmobile` | `:string` |
| `aadimei` | `:string` |
| `aadhourmeter` | `:float` |
| `aadhourmeter1` | `:float` |
| `aadhourmeter2` | `:float` |
| `aadhourmeter3` | `:float` |
| `aadhourmeter4` | `:float` |
| `aadodometer` | `:integer` |
| `aadhourmeteromega` | `:float` |
| `aadhourmeterothcan` | `:float` |
| `aaddateintoservice` | `:date` |
| `aadlastservice` | `:date` |
| `aadvalid` | `:string` |
| `aadserviceoffset` | `:float` |
| `aadsvchrs` | `:integer` |
| `aadrange_lat` | `:float` |
| `aadrange_long` | `:float` |
| `aadrange_dist` | `:integer` |
| `aadrange_unit` | `:string` |
| `service_calculation_input` | `:string` |

`:puls_record` object (line 41–45):
| Field | Type |
|---|---|
| `esn` | `:string` |
| `iccid` | `:string` |
| `group` | `:string` |

**Constants / errors defined:** None.

---

## Findings

---

**B022-1** — [HIGH] Route/handler mismatch: `:work_in_progress` route silently calls `:sielift_export`

File: `lib/api_server_web/router.ex:41-42`

The commented-out line at line 41 shows the original intent: `get "/rhm/work_in_progress", VXThingController, :work_in_progress`. The live route directly below it at line 42 uses the same URL path but dispatches to `:sielift_export` instead. This is not a temporary workaround that was cleaned up; the original route declaration was left as a comment alongside the substitute, creating a permanent lie in the routing table. Any caller or developer reading the URL `/rhm/work_in_progress` has no indication they are actually invoking sielift export logic. If `:sielift_export` is ever changed or removed independently, this silent aliasing makes the breakage harder to diagnose. The commented line also constitutes commented-out code (see B022-2).

---

**B022-2** — [LOW] Commented-out route: `:work_in_progress` original declaration left in place

File: `lib/api_server_web/router.ex:41`

The line `# get "/rhm/work_in_progress", VXThingController, :work_in_progress` is dead commented-out code left directly above its live replacement. It should be removed once the intent of the substitution is documented. Its presence alongside the live route (B022-1) is actively misleading.

---

**B022-3** — [MEDIUM] Commented-out code: entire GraphQL forwarding block never removed

File: `lib/api_server_web/router.ex:195-202`

Eight lines of commented-out `forward` declarations for `/graphql` and `/graphiql` remain in the router. The full `ApiServerWeb.Schema` module and its types are fully defined and compiled, yet the only entry points into the GraphQL layer are commented out. This means the schema module (`schema.ex`, `thing_types.ex`) and all three resolvers it references compile and are linked into the application but are completely unreachable at runtime. The comment block provides no explanation of whether this feature was abandoned, is planned, or is gated behind a flag. This is not merely style debt: the entire GraphQL stack is dead weight that increases binary size, complicates dependency management, and misleads developers about available API surfaces.

---

**B022-4** — [MEDIUM] Dead code: GraphQL schema and types are compiled but entirely unreachable

File: `lib/api_server_web/schema.ex:1-29`, `lib/api_server_web/schema/thing_types.ex:1-47`

As a direct consequence of B022-3, `ApiServerWeb.Schema` and `ApiServerWeb.Schema.ThingTypes` are compiled modules with no live callers. The three resolver functions (`Resolvers.Things.find_thing/3`, `Resolvers.Puls.puls_record/3`, `Resolvers.Things.get_all_things/3`) are also compiled and linked, but never invoked. The `alias ApiServerWeb.Resolvers` in `schema.ex` line 6 is a build-time alias used only through the commented-out forwarding path; it resolves but is operationally unused at runtime. If the GraphQL feature is not planned for re-enablement, these modules should be deleted. If it is planned, the forwarding should be restored and the commented-out block in the router removed.

---

**B022-5** — [LOW] Commented-out code: CORSPlug disabled in both API pipelines with no explanation

File: `lib/api_server_web/router.ex:13`, `lib/api_server_web/router.ex:19`

`# plug CORSPlug, origin: "*"` is commented out in both the `:api` pipeline (line 13) and the `:api_xml` pipeline (line 19). The `:browser` pipeline has no such comment. There is no explanation for why CORS handling is disabled, nor any indication of whether this is intentional policy or an oversight. Disabling CORS handling silently means cross-origin requests to all `/api/v1` and root XML endpoints are governed only by browser defaults, which may or may not be acceptable depending on client deployment. The commented-out code should either be deleted with a changelog note or restored with a clear reason in a comment.

---

**B022-6** — [LOW] Commented-out route: `/files` index route left in place

File: `lib/api_server_web/router.ex:164`

`# get "/files", FileController, :index` is commented out with no explanation. Two other `FileController` routes immediately follow (`get_size` at line 165, `send_file_download` at line 166). It is unclear whether the index action was intentionally disabled, never implemented, or removed as dead code. The dead comment adds noise and should be removed or restored.

---

**B022-7** — [HIGH] Duplicate route: `/rhm/omega_fleet/:fleetid/operation_summary_report` registered twice

File: `lib/api_server_web/router.ex:90-100`

The route `GET /api/v1/rhm/omega_fleet/:fleetid/operation_summary_report` dispatching to `VXThingOmegaController.:get_operation_summary_report` is declared identically at lines 90–94 and again at lines 96–100. Phoenix will compile both and the first match wins, making the second route permanently unreachable. This is a build warning in recent Phoenix/Plug versions (`warning: this clause cannot match because a previous clause at line N always matches`). The duplicate should be deleted.

---

**B022-8** — [MEDIUM] Authentication bypass: two routes outside `pipe_through` in an authenticated scope

File: `lib/api_server_web/router.ex:29-33`

Within the first `/api/v1` scope (line 28), `pipe_through([:api, :authenticated])` is invoked at line 33 — *after* two routes have already been declared at lines 30–31:

```elixir
get("/rhm/engine_usage", VXThingController, :combined_engine_usage)
get("/rhm/monday_hour_meters", VXThingController, :monday_hour_meters)
...
pipe_through([:api, :authenticated])
```

In Phoenix, `pipe_through` inside a scope applies to all routes in that scope regardless of declaration order — the plug pipeline is not conditional on position. However, this layout is dangerously misleading: it strongly implies to any reader that the two routes above the `pipe_through` call are intentionally unauthenticated, when in fact (per Phoenix semantics) they will also pass through `:authenticated`. The comment at line 29 (`# Avoid authentication, locking to a specific database`) reinforces the developer's belief that these routes skip authentication. If the developer's intent was truly to make these routes unauthenticated, the implementation is wrong and both routes are silently authenticated. If the intent was always to authenticate them, the comment is false and misleading. Either way, the code does not accurately express its intent, which constitutes a latent security defect.

---

**B022-9** — [LOW] Style inconsistency: mixed REST verb conventions for create/update operations

File: `lib/api_server_web/router.ex:54-55`, `105-107`, `116-117`, `129-136`, `141-143`

Throughout the router, create operations consistently use `PUT` and update operations use `POST`. This is the inverse of conventional REST semantics (POST for create, PUT for idempotent update/replace). The pattern is applied consistently within the codebase, but it directly contradicts RFC 7231 and the Rails/Phoenix default resource conventions. Any new developer or external integrator will be confused. The `resources/3` macro at line 162 for `[REDACTED-AWS-SMTP-PASSWORD]` uses the conventional mapping (Phoenix default: POST for create, PUT/PATCH for update), creating an internal inconsistency between RESTful resource routes and manually declared routes. This makes the API surface inconsistent and error-prone for clients.

---

**B022-10** — [INFO] Indentation inconsistency in schema.ex

File: `lib/api_server_web/schema.ex:1-29`

The top-level module body uses 4-space indentation (lines 3–6 are indented with 4 spaces relative to the `defmodule`), while Elixir community convention (and the style used in `thing_types.ex`) is 2-space indentation. This does not affect compilation or runtime behavior but is a style inconsistency that will produce diff noise and may trigger credo style warnings.

---

## Summary Table

| ID | Severity | File(s) | Short Title |
|---|---|---|---|
| B022-1 | HIGH | router.ex:41-42 | Route/handler mismatch: work_in_progress calls sielift_export |
| B022-2 | LOW | router.ex:41 | Commented-out original work_in_progress route left in place |
| B022-3 | MEDIUM | router.ex:195-202 | Entire GraphQL forwarding block commented out with no explanation |
| B022-4 | MEDIUM | schema.ex, thing_types.ex | GraphQL schema modules compiled but entirely unreachable at runtime |
| B022-5 | LOW | router.ex:13,19 | CORSPlug disabled in both API pipelines with no explanation |
| B022-6 | LOW | router.ex:164 | Commented-out /files index route left in place |
| B022-7 | HIGH | router.ex:90-100 | Duplicate route: operation_summary_report registered twice |
| B022-8 | MEDIUM | router.ex:29-33 | Authentication bypass ambiguity: pipe_through after route declarations |
| B022-9 | LOW | router.ex (multiple) | Mixed REST verb conventions (PUT=create, POST=update) inconsistent with Phoenix resources macro |
| B022-10 | INFO | schema.ex | 4-space indentation inconsistent with 2-space Elixir convention |

**Total findings: 10** (2 HIGH, 3 MEDIUM, 4 LOW, 1 INFO)
# Pass 4 – B023

**Date:** 2026-02-27
**Audit run:** 2026-02-27-01
**Agent:** B023
**Pass:** 4 – Code Quality

**Files reviewed:**
- `lib/api_server_web/views/changeset_view.ex`
- `lib/api_server_web/views/error_helpers.ex`
- `lib/api_server_web/views/error_view.ex`
- `lib/api_server_web/views/file_view.ex`

---

## Reading Evidence

### `lib/api_server_web/views/changeset_view.ex`

**Module:** `ApiServerWeb.ChangesetView`

**Functions:**

| Name | Line |
|---|---|
| `translate_errors/1` | 10 |
| `render/2` (clause `"error.json"`) | 14 |

**Types / constants defined:** none

**Notes:** `translate_errors/1` delegates to `Ecto.Changeset.traverse_errors/2` and `translate_error/1` (imported from `ApiServerWeb.ErrorHelpers` via `use ApiServerWeb, :view`). Only one render clause defined; the function is public but only called from within the same module.

---

### `lib/api_server_web/views/error_helpers.ex`

**Module:** `ApiServerWeb.ErrorHelpers`

**Functions:**

| Name | Line |
|---|---|
| `error_tag/2` | 11 |
| `translate_error/1` | 20 |

**Types / constants defined:** none

**Notes:** Uses `Phoenix.HTML` (for `content_tag/3`). `translate_error/1` is consumed by `ApiServerWeb.ChangesetView` and is imported into every view module via `use ApiServerWeb, :view`. `error_tag/2` generates HTML `<span>` elements with CSS class `"help-block"`.

---

### `lib/api_server_web/views/error_view.ex`

**Module:** `ApiServerWeb.ErrorView`

**Functions:**

| Name | Line |
|---|---|
| `template_not_found/2` | 13 |

**Types / constants defined:** none

**Notes:** Contains a commented-out render clause for `"500.html"` (lines 6–8). The active `template_not_found/2` is a Phoenix fallback callback; it returns a map with an `:error` key rather than a plain string, which means JSON clients receive a structured response regardless of the requested template name/format.

---

### `lib/api_server_web/views/file_view.ex`

**Module:** `ApiServerWeb.FileView`

**Functions:**

| Name | Line |
|---|---|
| `render/2` (clause `"index.json"`) | 5 |
| `render/2` (clause `"show.json"`) | 9 |
| `render/2` (clause `"filesize.json"`) | 13 |
| `render/2` (clause `"file.json"`) | 20 |

**Types / constants defined:** none

**Aliases:** `alias ApiServerWeb.FileView` (line 3) — self-alias used to pass the current module as the view argument to `render_many/3` and `render_one/3`.

**Notes:** The controller (`FileController`) only ever calls `render(conn, "filesize.json", ...)`. The `"index.json"` and `"show.json"` clauses (and their shared `"file.json"` helper) have no corresponding controller action calling them. The `"filesize.json"` clause omits the `fobs` key that `"file.json"` includes; the two shapes are intentionally different.

---

## Findings

---

**B023-1** — [LOW] Commented-out render clause left in production source

File: `lib/api_server_web/views/error_view.ex:6-8`

Description: Lines 6–8 contain a commented-out function clause:

```elixir
# def render("500.html", _assigns) do
#   "Internal Server Error"
# end
```

The accompanying comment on lines 4–5 frames this as an intentional example ("If you want to customize…"), which is boilerplate left over from the Phoenix generator. Commented-out code in a generated file that has since been put into production use should be removed; it creates noise when reading the module and could mislead a maintainer into thinking the clause was recently disabled for a reason.

---

**B023-2** — [MEDIUM] `error_tag/2` is dead code — the application has no HTML forms

File: `lib/api_server_web/views/error_helpers.ex:11`

Description: `error_tag/2` generates HTML `<span class="help-block">` error tags for Phoenix form helpers. A search across all `.ex`, `.eex`, `.heex`, and `.leex` files in the repository finds zero call-sites for `error_tag/2`. The application is a JSON API server; the only template files present (`app.html.eex`, `page/index.html.eex`) are Phoenix-generator placeholders. The function is imported into every view module via `use ApiServerWeb, :view`, so it never triggers an "unused import" warning, but it is never exercised at runtime.

Keeping it raises two concerns:
1. It silently imports `Phoenix.HTML` (`use Phoenix.HTML` at line 6) purely to support `content_tag/3`, pulling in a dependency that is otherwise unused in this module.
2. It misleads maintainers into believing the codebase has, or intends to have, server-rendered HTML forms.

---

**B023-3** — [LOW] `use Phoenix.HTML` imported solely to support a dead function

File: `lib/api_server_web/views/error_helpers.ex:6`

Description: The only consumer of the `Phoenix.HTML` import in this module is `content_tag/3`, called exclusively from `error_tag/2` (finding B023-2). If `error_tag/2` is removed, the `use Phoenix.HTML` line becomes entirely unnecessary. Even if `error_tag/2` is retained, this is a build-warning-class issue: the Elixir compiler will emit warnings about unused imports if `Phoenix.HTML` macros are never called in compiled code paths. The import exists solely to prop up dead code.

---

**B023-4** — [MEDIUM] `render("index.json")` and `render("show.json")` clauses in `FileView` are dead code

File: `lib/api_server_web/views/file_view.ex:5-11`

Description: `ApiServerWeb.FileController` — the only controller that uses `ApiServerWeb.FileView` — defines only two actions: `get_size/2` (renders `"filesize.json"`) and `send_file_download/2` (streams a binary download, no view render). No controller anywhere in the project calls `render(conn, "index.json", files: ...)` or `render(conn, "show.json", file: ...)` targeting `FileView`.

Consequently:
- `render("index.json", %{files: files})` at line 5 is never invoked.
- `render("show.json", %{file: file})` at line 9 is never invoked.
- `render("file.json", %{file: file})` at line 20 is dead by transitivity (called only by the two dead clauses above via `render_many`/`render_one`).

Three of the four render clauses in this view module are unreachable. This indicates either planned functionality that was never implemented or leftovers from generator scaffolding that was not cleaned up.

---

**B023-5** — [LOW] Self-alias pattern is unnecessary boilerplate in `FileView`

File: `lib/api_server_web/views/file_view.ex:3`

Description:

```elixir
alias ApiServerWeb.FileView
```

This alias is used at lines 6 and 10 to pass the current module to `render_many/3` and `render_one/3`. The idiomatic Elixir/Phoenix pattern is to use `__MODULE__` for this purpose, which is unambiguous and does not require an alias declaration. Using an explicit self-alias adds a line of noise and creates a minor trap: if the module is renamed, the alias must be updated in two places (the module name and the alias line) instead of one. This is a style-consistency issue relative to the other views in the codebase (e.g., `GeofenceView`, `VxThingView`) which use the aliased module name but obtain it from the generator — the inconsistency here is that this pattern is unnecessary overhead for a self-reference.

---

**B023-6** — [INFO] `translate_errors/1` is public but only called internally

File: `lib/api_server_web/views/changeset_view.ex:10`

Description: `translate_errors/1` is defined as a public function (`def`) but is only called from within `ApiServerWeb.ChangesetView` itself, at line 11 inside `render("error.json", ...)`. No other module calls it. It could be made private (`defp`) to enforce encapsulation and allow the compiler to warn if it ever becomes unused. This is a minor encapsulation issue, not a correctness problem.

---

**B023-7** — [LOW] Style inconsistency: map formatting differs between render clauses in `FileView`

File: `lib/api_server_web/views/file_view.ex:13-26`

Description: The `"filesize.json"` and `"file.json"` render clauses format their return maps inconsistently:

`"filesize.json"` (lines 14–17):
```elixir
%{hardwareid: file.hardwareid,
  size: file.size,
  num_fobs: file.num_fobs }
```
— closing `}` is on the same line as the last key-value pair, with a space before it.

`"file.json"` (lines 21–25):
```elixir
%{hardwareid: file.hardwareid,
  size: file.size,
  num_fobs: file.num_fobs,
  fobs: file.fobs
}
```
— closing `}` is on its own line, no trailing space.

Within the same file, two structurally similar map literals use different closing-brace placement. This inconsistency is a style finding. The `"filesize.json"` style also has a trailing space before the closing brace, which is non-standard.

Additionally, there is a double blank line between the `"show.json"` and `"filesize.json"` clauses (line 18–19) while other clause boundaries use a single blank line — a minor but consistent formatting deviation.

---

## Summary Table

| ID | Severity | Title | File | Line(s) |
|---|---|---|---|---|
| B023-1 | LOW | Commented-out render clause left in production source | `error_view.ex` | 6–8 |
| B023-2 | MEDIUM | `error_tag/2` is dead code — no HTML forms in API server | `error_helpers.ex` | 11–15 |
| B023-3 | LOW | `use Phoenix.HTML` imported solely to support dead function | `error_helpers.ex` | 6 |
| B023-4 | MEDIUM | `render("index.json")`, `render("show.json")`, `render("file.json")` are dead code | `file_view.ex` | 5–11, 20–26 |
| B023-5 | LOW | Unnecessary self-alias; `__MODULE__` is the idiomatic alternative | `file_view.ex` | 3 |
| B023-6 | INFO | `translate_errors/1` should be private (`defp`) | `changeset_view.ex` | 10 |
| B023-7 | LOW | Inconsistent map literal formatting within `FileView` | `file_view.ex` | 14–17, 21–25 |
# Pass 4 – B024

**Date:** 2026-02-27
**Audit run:** 2026-02-27-01
**Pass:** 4 (Code Quality)

## Files Reviewed

- `lib/api_server_web/views/geofence_view.ex`
- `lib/api_server_web/views/layout_view.ex`
- `lib/api_server_web/views/page_view.ex`
- `lib/api_server_web/views/vx_abl_record_view.ex`

---

## Reading Evidence

### `lib/api_server_web/views/geofence_view.ex`

**Module:** `ApiServerWeb.GeofenceView`

**Aliases declared:**
- `ApiServerWeb.GeofenceView` (line 4)
- `ApiServerWeb.VXThingView` (line 5)
- `ApiServer.Vx` (line 6)
- `ApiServer.Vx.Geofence` (line 7)

**Functions:**

| Line | Name/Arity | Notes |
|------|-----------|-------|
| 9    | `render/2` — `"index.json"` | Delegates to `render_many` with `GeofenceView` |
| 13   | `render/2` — `"geofence.json"` | Returns id, name, geoJSON |
| 22   | `render/2` — `"geofence_events.json"` | Maps events, calls `render_one` with `VXThingView` / `"rhm_thing.json"` |

**Types / constants / errors defined:** None.

---

### `lib/api_server_web/views/layout_view.ex`

**Module:** `ApiServerWeb.LayoutView`

**Aliases declared:** None.

**Functions:** None (module body contains only `use ApiServerWeb, :view`).

**Types / constants / errors defined:** None.

---

### `lib/api_server_web/views/page_view.ex`

**Module:** `ApiServerWeb.PageView`

**Aliases declared:** None.

**Functions:** None (module body contains only `use ApiServerWeb, :view`).

**Types / constants / errors defined:** None.

---

### `lib/api_server_web/views/vx_abl_record_view.ex`

**Module:** `ApiServerWeb.VXAblRecordView`

**Aliases declared:**
- `ApiServerWeb.VXAblRecordView` (line 4)
- `ApiServer.Vx` (line 5)

**Functions:**

| Line | Name/Arity | Notes |
|------|-----------|-------|
| 8    | `render/2` — `"index.json"` | Wraps `render_many` in `%{data: ...}` |
| 12   | `render/2` — `"show.json"` | Wraps `render_one` in `%{data: ...}` |
| 16   | `render/2` — `"vx_abl_record.json"` | Returns id and ablcustcode only |
| 22   | `render/2` — `"services.json"` | Maps records, delegates to `"service.json"` via `render_one` with tuple arg |
| 28   | `clean_xml_value/1` | Public; maps `%{}` -> `nil`, otherwise identity |
| 37   | `clean_xml_number_value/1` | Public; maps `%{}` -> `0`, otherwise identity |
| 46   | `render/2` — `"service.json"` | Main audit-log render; calls `Vx.get_vx_thing_with_hardware_id!`; builds full map |

**Types / constants / errors defined:** None.

---

## Findings

### B024-1 — [HIGH] Dead code: `clean_xml_value/1` and `clean_xml_number_value/1` duplicated in view, never called

**File:** `lib/api_server_web/views/vx_abl_record_view.ex:28` and `:37`

**Description:**
`clean_xml_value/1` (line 28) and `clean_xml_number_value/1` (line 37) are defined as public functions in `ApiServerWeb.VXAblRecordView`. An exhaustive search across all `.ex` files under `lib/` shows that neither function is called anywhere — not within the view itself, not from any controller, and not from any other module. The identical functions exist (and are actively used) in `ApiServer.VxAblRecord` (`lib/api_server/vx/vx_abl_record.ex:54` and `:63`).

These functions appear to be stale copies that were pasted into the view module during an earlier refactor and then never wired up. Because they are `def` (public), not `defp`, they are part of the module's exported interface despite being unreachable from any call site. This is dead code that silently widens the public API and will never be exercised.

Severity is HIGH rather than MEDIUM because `clean_xml_number_value/1` is not only dead in the view but also dead in its context module (`vx_abl_record.ex` defines it but never calls it), meaning the numeric-zero sentinel path has no production consumer at all, indicating a logic gap that may have been intentional at one point and silently dropped.

---

### B024-2 — [MEDIUM] Logic executed inside a view: database call in `render/2`

**File:** `lib/api_server_web/views/vx_abl_record_view.ex:49`

**Description:**
The `render("service.json", ...)` clause (line 46) makes a direct call to `Vx.get_vx_thing_with_hardware_id!(record.hardwareid, customer)` on line 49. This is a database query issued inside a view render function. Phoenix views are intended to be pure presentation/serialization layers; all data fetching is expected to happen in controllers or context modules before the render call. Placing a database call here:

1. Bypasses the controller's ability to handle query errors gracefully — the bang function will raise on miss, producing an unhandled exception rather than a controlled error response.
2. Makes the render clause non-pure: the same input data can produce different output (or raise) depending on database state at render time.
3. Hides N+1 query risk — this call is inside `render("service.json", ...)` which is invoked per-record by `Enum.map` in `render("services.json", ...)`.

This is a leaky abstraction: the data-access layer is being breached inside the presentation layer.

---

### B024-3 — [MEDIUM] Inconsistent response envelope across render clauses

**File:** `lib/api_server_web/views/vx_abl_record_view.ex:8–25`

**Description:**
The `"index.json"` and `"show.json"` clauses wrap their payloads in a `%{data: ...}` envelope (lines 9 and 13), matching the conventional JSON API style used elsewhere in the project. However, `"services.json"` (line 22) returns a bare list with no envelope, and `"geofence_events.json"` in `GeofenceView` (line 24) similarly returns a bare list. Within `VXAblRecordView` specifically, the inconsistency means two render paths from the same module use different top-level shapes, which breaks client-side predictability and contradicts the convention established by `index.json` and `show.json` in the same module.

---

### B024-4 — [LOW] Unused alias: `ApiServer.Vx` in `GeofenceView`

**File:** `lib/api_server_web/views/geofence_view.ex:6`

**Description:**
`alias ApiServer.Vx` is declared on line 6 of `GeofenceView`. The module's three render functions only reference `GeofenceView`, `VXThingView`, and `Geofence` (the last alias on line 7). No call to `Vx.*` appears anywhere within this module. The `Vx` alias is therefore unused and will generate an Elixir compiler warning (`warning: unused alias Vx`). Unused aliases indicate incomplete refactoring and add noise to the module's dependency surface.

---

### B024-5 — [LOW] `nil` guard using `if thing != nil` instead of pattern matching

**File:** `lib/api_server_web/views/vx_abl_record_view.ex:50`

**Description:**
Inside `render("service.json", ...)`, line 50 uses `if thing != nil do` to guard the branch that accesses `thing.fleet_thing_joins`. This is an anti-pattern in Elixir: the idiomatic approach is to guard with a `nil`-matching function clause or use `case`. Using `if thing != nil` is fragile because it still executes `Vx.get_vx_thing_with_hardware_id!/2` (which has a bang and will raise on not-found) before reaching the guard; if the function raises, the `nil` check is never reached. The guard provides false safety. Pattern matching at the function clause level or using `with` would make the control flow explicit and safe.

---

### B024-6 — [LOW] `cond` used where `if/else` or pattern matching is idiomatic

**File:** `lib/api_server_web/views/vx_abl_record_view.ex:29–44` and `60–65`

**Description:**
`clean_xml_value/1` (lines 29–34), `clean_xml_number_value/1` (lines 38–44), and the `user_name` derivation (lines 60–65) all use `cond do` with exactly two clauses where the second is `true ->`. In Elixir, two-clause `cond` with a `true` catch-all is stylistically equivalent to `if/else` and the idiomatic form is to use two function clauses with pattern matching (for `clean_xml_*`) or `if/else` (for the inline expression). This pattern appears three times within the same module and once in the sibling `vx_abl_record.ex` context module, representing a consistent but non-idiomatic coding style that would produce Dialyzer/Credo style warnings in a strict project configuration.

---

### B024-7 — [INFO] `LayoutView` and `PageView` are empty scaffolding modules

**File:** `lib/api_server_web/views/layout_view.ex:1–3` and `lib/api_server_web/views/page_view.ex:1–3`

**Description:**
Both `ApiServerWeb.LayoutView` and `ApiServerWeb.PageView` contain only `use ApiServerWeb, :view` and no functions. These are Phoenix-generated scaffold modules. For a JSON-only API server (which this appears to be), `PageView` in particular is never referenced and represents generated boilerplate that was never removed. This is INFO only — Phoenix convention generates these and their presence is not harmful — but in a pure-API application with no HTML templates, `PageView` is dead code at the module level.

---

## Summary Table

| ID      | Severity | File                             | Title |
|---------|----------|----------------------------------|-------|
| B024-1  | HIGH     | `vx_abl_record_view.ex:28,37`   | Dead code: `clean_xml_value/1` and `clean_xml_number_value/1` defined but never called in view |
| B024-2  | MEDIUM   | `vx_abl_record_view.ex:49`      | Leaky abstraction: database query inside view render clause (N+1 risk, unhandled raise) |
| B024-3  | MEDIUM   | `vx_abl_record_view.ex:8–25`    | Inconsistent response envelope: `index`/`show` use `%{data:}`, `services` returns bare list |
| B024-4  | LOW      | `geofence_view.ex:6`            | Unused alias `ApiServer.Vx` — will produce compiler warning |
| B024-5  | LOW      | `vx_abl_record_view.ex:50`      | `nil` guard via `if thing != nil` after bang function — false safety |
| B024-6  | LOW      | `vx_abl_record_view.ex:29–65`   | Two-clause `cond` used where `if/else` or pattern matching is idiomatic |
| B024-7  | INFO     | `layout_view.ex`, `page_view.ex` | Empty scaffold modules; `PageView` likely dead in a pure-API application |
# Pass 4 – B025

**Date:** 2026-02-27
**Audit run:** 2026-02-27-01
**Agent:** B025

**Files reviewed:**
- `lib/api_server_web/views/vx_access_fob_view.ex`
- `lib/api_server_web/views/vx_customer_view.ex`
- `lib/api_server_web/views/vx_fleet_association_view.ex`
- `lib/api_server_web/views/vx_fleet_view.ex`

---

## Reading Evidence

### File 1: `lib/api_server_web/views/vx_access_fob_view.ex`

**Module:** `ApiServerWeb.VXAccessFobView`

**Aliases:**
- `ApiServerWeb.VXAccessFobView` (line 3) — self-alias for use in `render_many`/`render_one` calls

**Functions:**

| Function | Line |
|---|---|
| `render("index.json", %{vxaccessfobs: vxaccessfobs})` | 5 |
| `render("show.json", %{vx_access_fob: vx_access_fob})` | 9 |
| `render("vx_access_fob.json", %{vx_access_fob: vx_access_fob})` | 13 |

**Types / Constants / Errors defined:** None

**Notes:** All three `render` clauses are standard scaffold output. `index.json` wraps in `%{data: ...}`. `show.json` wraps in `%{data: ...}`. The partial `"vx_access_fob.json"` returns only `id` and `fob_code`.

---

### File 2: `lib/api_server_web/views/vx_customer_view.ex`

**Module:** `ApiServerWeb.VXCustomerView`

**Aliases:**
- `ApiServerWeb.VXCustomerView` (line 3) — self-alias

**Functions:**

| Function | Line |
|---|---|
| `render("index.json", %{vx_customers: vx_customers})` | 5 |
| `render("show.json", %{vx_customer: vx_customer})` | 9 |
| `render("vx_customer.json", %{vx_customer: nil})` | 13 |
| `render("vx_customer.json", %{vx_customer: vx_customer})` | 14 |

**Types / Constants / Errors defined:** None

**Notes:**
- `index.json` returns a bare list (no `%{data: ...}` wrapper) — contrast with the other three view files which all wrap.
- `show.json` also returns a bare value (no `%{data: ...}` wrapper).
- Two-clause guard on the partial: `nil` short-circuits to `%{}`, then `Ecto.assoc_loaded?/1` is checked inside the second clause.
- Lines 30–31 contain commented-out fields (`aaaudfcustcode`, `aaacolour`).
- The second `render("vx_customer.json", ...)` clause uses an imperative `if !Ecto.assoc_loaded?` rather than a separate function-head guard.

---

### File 3: `lib/api_server_web/views/vx_fleet_association_view.ex`

**Module:** `ApiServerWeb.VXFleetAssociationView`

**Aliases:**
- `ApiServerWeb.VXFleetAssociationView` (line 3) — self-alias

**Functions:**

| Function | Line |
|---|---|
| `render("index.json", %{vxfleetassociationss: vxfleetassociationss})` | 5 |
| `render("show.json", %{vx_fleet_association: vx_fleet_association})` | 9 |
| `render("vx_fleet_association.json", %{vx_fleet_association: vx_fleet_association})` | 13 |

**Types / Constants / Errors defined:** None

**Notes:**
- The `index.json` assign key is `[REDACTED-AWS-SMTP-PASSWORD]` (double trailing `s`).
- The corresponding controller (`[REDACTED-AWS-SMTP-PASSWORD]`, line 11) assigns the key as `vxfleetassociations` (single `s`).
- This mismatch causes a `FunctionClauseError` at runtime whenever `index` is called.
- The partial exposes `aafcustcode` as a raw database column name in the JSON response key.

---

### File 4: `lib/api_server_web/views/vx_fleet_view.ex`

**Module:** `ApiServerWeb.VXFleetView`

**Aliases:**
- `ApiServerWeb.VXFleetView` (line 3) — self-alias

**Functions:**

| Function | Line |
|---|---|
| `render("index.json", %{vxfleets: vxfleets})` | 5 |
| `render("show.json", %{vx_fleet: vx_fleet})` | 9 |
| `render("vx_fleet.json", %{vx_fleet: vx_fleet})` | 13 |
| `render("rhm_fleets.json", %{vx_fleets: vx_fleets})` | 22 |
| `render("rhm_fleet.json", %{vx_fleet: vx_fleet})` | 25 |
| `render("rhm_fleets_with_equip.json", %{vx_fleets: vx_fleets})` | 34 |
| `render("rhm_fleet_with_equip.json", %{vx_fleet: vx_fleet})` | 37 |
| `render("rhm_fleet_equipment.json", %{results: results})` | 47 |
| `render("assoc.json", %{vx_fleet: {fleet_id, equipment_id, equipment_name}})` | 51 |

**Types / Constants / Errors defined:** None

**Notes:**
- `render("index.json", ...)` is never called by any controller (confirmed by searching all controllers). The fleet controller uses only `show.json`, `rhm_fleets.json`, `rhm_fleets_with_equip.json`, `rhm_fleet.json`, `rhm_fleet_equipment.json`.
- `render("vx_fleet.json", ...)` exposes raw database column names (`aaetype`, `aaeshowfilter`, `aaecolour`) as JSON keys. The `rhm_fleet.json` partial for the same data uses human-readable aliases (`type`, `show_in_filters`, `color`). These two render the same underlying struct fields but with different key naming conventions.
- Blank line inconsistency: a double blank line appears at line 45–46 between `render("rhm_fleet_with_equip.json", ...)` and `render("rhm_fleet_equipment.json", ...)`, and a trailing blank line inside the body of `render("rhm_fleet_equipment.json", ...)` at line 49.
- `render("rhm_fleet_with_equip.json", ...)` omits `color` / `aaecolour` compared to `rhm_fleet.json`, even though both render the same struct.

---

## Findings

---

**B025-1** — HIGH — Runtime FunctionClauseError: `index.json` assign key mismatch in VXFleetAssociationView
File: `lib/api_server_web/views/vx_fleet_association_view.ex:5`
Description: The view's `render("index.json", ...)` clause pattern-matches on the key `[REDACTED-AWS-SMTP-PASSWORD]` (double `s`), but `VXFleetAssociationController.index/2` assigns the key as `vxfleetassociations` (single `s`) — confirmed at `lib/api_server_web/controllers/vx_fleet_association_controller.ex:11`. Because Phoenix dispatches `render/2` via pattern matching, a request to the `index` action will always raise `Phoenix.View.RenderError` (wrapping a `FunctionClauseError`) at runtime. The mismatch is invisible at compile time. Any client calling the list endpoint receives a 500 error.

---

**B025-2** — LOW — Commented-out code left in production view
File: `lib/api_server_web/views/vx_customer_view.ex:30-31`
Description: Two fields are commented out inside the `render("vx_customer.json", ...)` response map:
```elixir
# aaaudfcustcode: vx_customer.aaaudfcustcode,
# aaacolour: vx_customer.aaacolour
```
Commented-out code in a view is either dead code that should be deleted, or intentionally suppressed output that should be tracked via a feature flag or a separate branch. As written it creates ambiguity about the intended public API shape and will confuse maintainers.

---

**B025-3** — MEDIUM — `index.json` and `show.json` lack `%{data: ...}` envelope in VXCustomerView; inconsistent with all peer views
File: `lib/api_server_web/views/vx_customer_view.ex:5-10`
Description: `render("index.json", ...)` returns a bare list and `render("show.json", ...)` returns a bare value. Every other view in the same directory (`VXAccessFobView`, `[REDACTED-AWS-SMTP-PASSWORD]`, `VXFleetView`, `VXThingView`, `VXThingSummaryView`, `VXThingEventView`, `VXUserFunctionView`, `VXRestrictionView`, `VXAblRecordView`) wraps the result in `%{data: ...}`. This breaks API envelope consistency for customers and makes the customer endpoint a special case for all API consumers and tests.

---

**B025-4** — MEDIUM — `render("vx_fleet.json", ...)` exposes raw database column names as JSON keys; conflicts with `rhm_fleet.json` naming for the same struct
File: `lib/api_server_web/views/vx_fleet_view.ex:13-19`
Description: The `vx_fleet.json` partial emits `aaetype`, `aaeshowfilter`, and `aaecolour` as JSON response keys. The `rhm_fleet.json` partial (line 25) renders the identical struct fields under the human-readable aliases `type`, `show_in_filters`, and `color`. Two templates exist in the same module for the same underlying data with incompatible key naming: one leaks storage-layer column names into the public API, the other uses a clean presentation layer. Any client of the `show.json` / `create` response route receives raw column names while clients of all RHM routes receive semantic names. This is a leaky abstraction and a consistency violation.

---

**B025-5** — LOW — Dead render clause: `render("index.json", ...)` in VXFleetView is unreachable from any controller
File: `lib/api_server_web/views/vx_fleet_view.ex:5-7`
Description: No controller in the application calls `render(conn, "index.json", ...)` through `VXFleetView`. The fleet controller (`vx_fleet_controller.ex`) uses `rhm_fleets.json`, `rhm_fleets_with_equip.json`, `rhm_fleet.json`, `rhm_fleet_equipment.json`, and `show.json` — never `index.json`. The clause `render("index.json", %{vxfleets: vxfleets})` is therefore dead code. Dead render clauses in Phoenix views are not flagged by the compiler and silently accumulate maintenance debt.

---

**B025-6** — LOW — `render("vx_fleet_association.json", ...)` exposes raw database column name `aafcustcode` as a JSON key
File: `lib/api_server_web/views/vx_fleet_association_view.ex:14-15`
Description: The response map for a fleet association record emits `aafcustcode` — a raw database storage column name — as a public API key. This is a leaky abstraction: the internal persistence naming convention (three-character prefix `aaf`) is directly visible to API consumers. If the underlying column is ever renamed or the schema is migrated, all clients break. A semantic key such as `customer_code` would decouple the API surface from the storage layer.

---

**B025-7** — LOW — `render("rhm_fleet_with_equip.json", ...)` omits the `color` field present in `render("rhm_fleet.json", ...)`
File: `lib/api_server_web/views/vx_fleet_view.ex:37-43`
Description: `render("rhm_fleet.json", ...)` (line 25) includes `color: vx_fleet.aaecolour`. `render("rhm_fleet_with_equip.json", ...)` (line 37) renders the same struct but omits `color`. Both templates are used by the fleet controller for fleet listings. Clients receiving the with-equipment response get less data than clients receiving the plain fleet response, with no documented reason for the omission. This is a silent field-level inconsistency that can cause client-side rendering bugs.

---

**B025-8** — LOW — `if !Ecto.assoc_loaded?` imperative guard inside `render("vx_customer.json", ...)` body; should be a separate function head
File: `lib/api_server_web/views/vx_customer_view.ex:14-34`
Description: The second `render("vx_customer.json", ...)` clause uses an `if !Ecto.assoc_loaded?(vx_customer)` branch inside the function body to return `%{}` for unloaded associations. The preceding clause (line 13) already handles `nil` via a dedicated function head. The unloaded-association guard should follow the same pattern — a separate function head with a `when not Ecto.assoc_loaded?(vx_customer)` guard — making all short-circuit cases structurally uniform and avoiding a nested `if` with an implicit `else` branch. As written, the `else` branch (the full field map) is only reached after evaluating `Ecto.assoc_loaded?` at runtime, and the code path is harder to trace than a series of pattern-matched heads.

---

**B025-9** — INFO — Style: blank line inside `render("rhm_fleet_equipment.json", ...)` body and double blank line before it
File: `lib/api_server_web/views/vx_fleet_view.ex:45-50`
Description: A double blank line separates `render("rhm_fleet_with_equip.json", ...)` from `render("rhm_fleet_equipment.json", ...)` (lines 45-46). Additionally, the body of `render("rhm_fleet_equipment.json", ...)` contains a trailing blank line before the `end` keyword (line 49). The rest of the module uses single blank lines between function clauses and no trailing blank lines inside function bodies. This is a minor style inconsistency but inconsistent whitespace in Elixir view files is typically cleaned up by `mix format`.

---

## Summary Table

| ID | Severity | File | Short Title |
|---|---|---|---|
| B025-1 | HIGH | `vx_fleet_association_view.ex:5` | Runtime `FunctionClauseError`: `index.json` assign key typo `[REDACTED-AWS-SMTP-PASSWORD]` does not match controller assign `vxfleetassociations` |
| B025-2 | LOW | `vx_customer_view.ex:30-31` | Commented-out code: `aaaudfcustcode` and `aaacolour` fields silently suppressed |
| B025-3 | MEDIUM | `vx_customer_view.ex:5-10` | `index.json` / `show.json` lack `%{data: ...}` envelope; inconsistent with all peer views |
| B025-4 | MEDIUM | `vx_fleet_view.ex:13-19` | `vx_fleet.json` leaks raw DB column names (`aaetype`, `aaeshowfilter`, `aaecolour`) while `rhm_fleet.json` uses semantic names for the same struct |
| B025-5 | LOW | `vx_fleet_view.ex:5-7` | Dead clause: `render("index.json", ...)` unreachable from any controller |
| B025-6 | LOW | `vx_fleet_association_view.ex:14-15` | `aafcustcode` raw DB column name exposed as public API key |
| B025-7 | LOW | `vx_fleet_view.ex:37-43` | `rhm_fleet_with_equip.json` silently omits `color` field present in `rhm_fleet.json` |
| B025-8 | LOW | `vx_customer_view.ex:14-34` | `if !Ecto.assoc_loaded?` guard inside function body; should be a separate function head |
| B025-9 | INFO | `vx_fleet_view.ex:45-50` | Inconsistent whitespace: double blank line and trailing blank line inside function body |
# Pass 4 – B026

**Date:** 2026-02-27
**Audit run:** 2026-02-27-01
**Agent:** B026

**Files reviewed:**
- `lib/api_server_web/views/vx_rental_view.ex`
- `lib/api_server_web/views/vx_restriction_view.ex`
- `lib/api_server_web/views/vx_thing_event_view.ex`
- `lib/api_server_web/views/vx_thing_omega_view.ex`

---

## Reading Evidence

### File 1: `lib/api_server_web/views/vx_rental_view.ex`

**Module name:** `ApiServerWeb.VXRentalView`

**Aliases declared:**
- `ApiServer.Vx` (line 3)
- `ApiServerWeb.VXRentalView` (line 4)
- `ApiServerWeb.VXThingView` (line 5)
- `ApiServerWeb.VXCustomerView` (line 6)

**Functions:**

| Name | Line | Visibility |
|------|------|------------|
| `render/2` — `"rhm_rentals.json"` | 8 | public |
| `render/2` — `"rhm_rental.json"` | 13 | public |
| `render/2` — `"midpac_report.json"` | 64 | public |
| `render/2` — `"rental_anniversaries.json"` | 68 | public |
| `convert_json_to_changeset/1` | 73 | public |

**Types/constants/errors defined:** none

**Notable observations during reading:**
- Line 55: JSON output key is `hours_to_serivce` (transposed letters in "service").
- Lines 17–21: `render/2` calls `Vx.fetch_actual_usage/5`, `Vx.get_usage_since_service/2`, and `Vx.get_avg_weekly_hours/2` — live database queries executed from inside a view function.
- Lines 17–18: `/1` division used as a type-coercion idiom to guarantee float (no comment explaining intent).
- Lines 28–34: `Map.has_key?/2` used on a struct — this works but is fragile; accessing struct fields is the conventional pattern.
- Line 80: `changeset` variable is bound but the function body ends with the pipe chain implicitly returning the value; the named binding `changeset =` on line 80 is unused as an explicit return — it is the last expression so it does return, but the name `changeset` is misleading (it is a plain atom-keyed map, not an Ecto changeset).
- `convert_json_to_changeset/1` lives in a View module but contains data-mapping logic more appropriate for a context or schema module; this is a separation-of-concerns violation.

---

### File 2: `lib/api_server_web/views/vx_restriction_view.ex`

**Module name:** `ApiServerWeb.VXRestrictionView`

**Aliases declared:**
- `ApiServerWeb.VXRestrictionView` (line 3)

**Functions:**

| Name | Line | Visibility |
|------|------|------------|
| `render/2` — `"index.json"` | 5 | public |
| `render/2` — `"show.json"` | 9 | public |
| `render/2` — `"vx_restriction.json"` | 13 | public |

**Types/constants/errors defined:** none

**Notable observations during reading:**
- Smallest and most conventional of the four files; follows standard Phoenix view scaffolding pattern.
- Field names in the output map (`aauid`, `aauuser_id`, `aaucustcode`, `aaufun`, `aaucharval`, `aaunumval`) are raw database column names exposed verbatim in the API surface — leaky abstraction.

---

### File 3: `lib/api_server_web/views/vx_thing_event_view.ex`

**Module name:** `ApiServerWeb.VXThingEventView`

**Aliases declared:**
- `ApiServerWeb.VXThingEventView` (line 3)

**Functions:**

| Name | Line | Visibility |
|------|------|------------|
| `render/2` — `"index.json"` | 5 | public |
| `render/2` — `"show.json"` | 9 | public |
| `render/2` — `"vx_thing_event.json"` | 13 | public |
| `omega_to_map/1` | 18 | private |
| `thingevent_to_map/1` | 83 | private |

**Types/constants/errors defined:** none

**Notable observations during reading:**
- Line 14: `vx_thing_event.thingeventomega` is accessed directly; if `thingeventomega` is not preloaded, this raises `%Ecto.Association.NotLoaded{}` at runtime with no guard.
- Line 43: field name `[REDACTED-AWS-SMTP-PASSWORD]` is a typo (should be `[REDACTED-AWS-SMTP-PASSWORD]`); the misspelling originates in the schema definition and is propagated verbatim here.
- Line 28: key `parkbreakreleased` (misspelling — should be `parkbrakereleased`); confirmed the schema field is also misspelled so this is consistent with the schema, but the misspelling is exposed in the API contract.
- Line 130: trailing comma after `prntcalctotalseconds: thingevent.prntcalctotalseconds,` is legal Elixir (trailing comma in map literal) but inconsistent with all other map literals in these four files.
- `show.json` render (line 10) does NOT wrap result in `%{data: ...}` unlike `index.json` (line 6) and unlike the pattern used in `vx_restriction_view.ex`.

---

### File 4: `lib/api_server_web/views/vx_thing_omega_view.ex`

**Module name:** `ApiServerWeb.VXThingOmegaView`

**Aliases declared:**
- `ApiServerWeb.VXThingOmegaView` (line 3)

**Functions:**

| Name | Line | Visibility |
|------|------|------------|
| `render/2` — `"container_lift_report.json"` | 6 | public |
| `render/2` — `"lift_summary_report_fleet.json"` | 17 | public |
| `render/2` — `"lift_summary_report.json"` | 39 | public |
| `render/2` — `"lift_list_report.json"` | 63 | public |
| `render/2` — `"engine_utilization_report.json"` | 77 | public |
| `render/2` — `"operation_summary_report.json"` | 92 | public |
| `translate_lift_type_to_string/1` | 139 | private |

**Types/constants/errors defined:** none

**Notable observations during reading:**
- Lines 103–122: three consecutive `cond do` blocks where only one arm does meaningful work and the other arm returns `0`. The `operating_hours == 0` guard is applied differently for `average_fuel_per_lift` (uses `Decimal.to_integer(lift_count) == 0`) vs. `average_lifts_per_hour` and `average_fuel_per_hour` (use `operating_hours == 0`). This is asymmetric: `average_fuel_per_lift` divides by `lift_count`, not `operating_hours`, so the distinct guard is correct in intent — but using `Decimal.to_integer` as a zero-check is inconsistent with the direct `== 0` used for `operating_hours`.
- Lines 17–61: `lift_summary_report_fleet.json` and `lift_summary_report.json` share identical structure for six of their seven output keys; `lift_summary_report.json` adds `thing_name`. This duplication is an opportunity for a shared helper.
- Line 78: `engine_utilization_report.json` destructures tuples using a `[list]` pattern (square brackets), while all other render clauses use `{tuple}` patterns (curly braces). This is a structural inconsistency — the data shape from the context is actually different (a list vs. a tuple), which is itself inconsistent API design.
- `translate_lift_type_to_string/1` maps integer codes `0,1,2,4,8` — note value `3` is skipped and there is no value between `2` and `4`, implying sparse codes. All unmapped codes silently return `"unknown"`.

---

## Findings

---

**B026-1** — [HIGH] Live database queries executed inside a view render function

File: `lib/api_server_web/views/vx_rental_view.ex:17-21`

Description: `render("rhm_rental.json", ...)` calls `Vx.fetch_actual_usage/5` (twice), `Vx.get_usage_since_service/2`, and `Vx.get_avg_weekly_hours/2` — all database-hitting context functions — directly inside the view layer. Views are responsible for serialising already-computed data; performing queries in a view violates the MVC separation of concerns, prevents caching or pre-computation at the controller level, makes the view untestable in isolation, and hides N+1 query risks when `render("rhm_rentals.json", ...)` maps over a list of rentals (each element triggers four queries). This is the primary architectural defect in this file.

---

**B026-2** — [HIGH] `vx_thing_event_view.ex` crashes on unpreloaded association with no guard

File: `lib/api_server_web/views/vx_thing_event_view.ex:14`

Description: `render("vx_thing_event.json", ...)` accesses `vx_thing_event.thingeventomega` unconditionally. If the caller did not preload the `thingeventomega` association, Ecto returns an `%Ecto.Association.NotLoaded{}` struct, and `omega_to_map/1` immediately crashes attempting to access fields on it (e.g., `thing_event_omega.accelerometerx`). There is no `nil` guard, no `%Ecto.Association.NotLoaded{}` guard, and no documentation that preloading is required. Per prior pass notes, this is a confirmed leaky abstraction: the view silently mandates an internal preload contract that is invisible to callers. The crash manifests as a runtime 500 error rather than a compile-time or early validation failure.

---

**B026-3** — [MEDIUM] Typo in public JSON API key: `hours_to_serivce`

File: `lib/api_server_web/views/vx_rental_view.ex:55`

Description: The JSON output key is spelled `hours_to_serivce` (letters `i` and `c` transposed). The corresponding internal variable on line 15 is correctly spelled `hours_to_service`. This means every API consumer receives a misspelled key. Correcting it would be a breaking change for any client already parsing this field, so the defect compounds over time. The correct spelling `hours_to_service` is used consistently in every other view and controller in the codebase that outputs this concept (e.g., `vx_abl_record_view.ex:80`, `vx_thing_view.ex:425`).

---

**B026-4** — [MEDIUM] `show.json` response envelope inconsistency in `vx_thing_event_view.ex`

File: `lib/api_server_web/views/vx_thing_event_view.ex:9-11`

Description: `render("show.json", ...)` returns the raw merged map from `render("vx_thing_event.json", ...)` without wrapping it in `%{data: ...}`. By contrast, `render("index.json", ...)` wraps its result in `%{data: ...}`. This makes single-record and multi-record responses structurally different — clients must apply different parsing logic depending on whether they requested a list or a single item. The same module-wide `%{data: ...}` envelope pattern is used consistently in `vx_restriction_view.ex` (both `index.json` and `show.json` wrap in `%{data: ...}`). The inconsistency is not justified by any comment or convention.

---

**B026-5** — [MEDIUM] `convert_json_to_changeset/1` placed in a View module — wrong layer

File: `lib/api_server_web/views/vx_rental_view.ex:73-89`

Description: `convert_json_to_changeset/1` translates a user-facing JSON parameter map (string keys) into an internal atom-keyed map for persistence. This is business/context logic, not presentation logic. Its presence in a View module violates the Phoenix layering contract (views serialise; contexts validate and persist). The controller (`vx_rental_controller.ex:159,178`) calls `ApiServerWeb.VXRentalView.convert_json_to_changeset/1` directly, creating a cross-layer dependency from controller to view that is atypical and will surprise maintainers. The function should live in the `ApiServer.Vx` context or the `VXRental` schema module.

---

**B026-6** — [MEDIUM] `engine_utilization_report.json` destructures rows as lists; all other render clauses use tuples

File: `lib/api_server_web/views/vx_thing_omega_view.ex:78`

Description: The `engine_utilization_report.json` render clause destructures each row as `[{date_year, date_month, date_day}, day_name, engine_hours, idle_hours, total_fuel, idle_fuel]` — a list containing a date tuple followed by scalar values. Every other render clause in this module (lines 7, 18, 40, 64, 94) destructures rows as flat tuples with `{...}` syntax. This inconsistency indicates the underlying query for this report returns a structurally different result type, which is an inconsistent context API surface. The view accurately reflects the inconsistency but does not hide it; a consumer comparing these render clauses will be confused about the contract.

---

**B026-7** — [MEDIUM] `Map.has_key?/2` used to test struct fields instead of pattern matching

File: `lib/api_server_web/views/vx_rental_view.ex:29`

Description: `Map.has_key?(vx_rental, :overage)` checks for the presence of an `:overage` field on what is expected to be a struct. For Ecto structs all defined fields are always present (with `nil` values when unset), so this check will always return `true` for a genuine `VXRental` struct, and `false` only if `vx_rental` is a plain map without the key. If the intent is to handle both plain maps (from a decorated result set) and structs, this should be documented; if the intent is a nil-check, `vx_rental.overage != nil` is clearer. The current code will mislead any reader who assumes struct semantics.

---

**B026-8** — [LOW] Trailing comma in map literal in `thingevent_to_map/1`

File: `lib/api_server_web/views/vx_thing_event_view.ex:130`

Description: The last entry of the map literal in `thingevent_to_map/1` has a trailing comma: `prntcalctotalseconds: thingevent.prntcalctotalseconds,`. This is syntactically valid Elixir but is inconsistent with all other map literals across all four files under review, none of which use trailing commas. It appears to be an artifact of a field having been inserted or removed without cleanup, and will cause unnecessary diff noise on future edits.

---

**B026-9** — [LOW] `lift_summary_report.json` and `lift_summary_report_fleet.json` are near-duplicate render clauses with no shared helper

File: `lib/api_server_web/views/vx_thing_omega_view.ex:17-61`

Description: `render("lift_summary_report_fleet.json", ...)` (lines 17–37) and `render("lift_summary_report.json", ...)` (lines 39–61) produce output maps with six identical keys (`date`, `day_name`, `count_20`, `count_30`, `count_40`, `count_chain`, `count_bottom`, `total_lifts`). The only difference is that `lift_summary_report.json` also includes `thing_name`. The six shared keys are duplicated verbatim across both clauses. Any future schema change to the shared fields must be applied in two places.

---

**B026-10** — [LOW] Database column names exposed verbatim in public API output in `vx_restriction_view.ex`

File: `lib/api_server_web/views/vx_restriction_view.ex:14-21`

Description: The `vx_restriction.json` template serialises raw database column names (`aauid`, `aauuser_id`, `aaucustcode`, `aaufun`, `aaucharval`, `aaunumval`) directly as JSON keys. These names are internal database artefacts and provide no semantic clarity to API consumers. If the underlying table schema changes, the API contract changes simultaneously. This is a leaky abstraction — the view does not translate internal field names to a stable, domain-meaningful API vocabulary. By contrast, `vx_rental_view.ex` translates column names to readable aliases (`abhid` → `id`, `abhcustcode` → `cust_code`, etc.).

---

**B026-11** — [LOW] Inconsistent zero-guard style for division safety in `operation_summary_report.json`

File: `lib/api_server_web/views/vx_thing_omega_view.ex:103-122`

Description: Three consecutive division-safety guards use two different patterns. `average_lifts_per_hour` (line 104) and `average_fuel_per_hour` (line 111) check `operating_hours == 0` using direct equality. `average_fuel_per_lift` (line 118) checks `Decimal.to_integer(lift_count) == 0` — using `Decimal.to_integer` to convert before comparing. If `operating_hours` is also a `Decimal`, the direct `== 0` comparison may silently succeed (Decimal implements `==` with integers via the `Decimal` protocol) or it may not, depending on the version. The asymmetric treatment of what appear to be the same type creates a risk of one guard behaving unexpectedly at runtime, and it is inconsistent style regardless.

---

**B026-12** — [LOW] `convert_json_to_changeset/1` binds result to variable `changeset` but the name is misleading

File: `lib/api_server_web/views/vx_rental_view.ex:80`

Description: The function body assigns the pipe result to a local variable named `changeset` on line 80. The value is a plain Elixir map (`%{}`), not an `Ecto.Changeset` struct. In Phoenix/Ecto conventions, `changeset` refers to `%Ecto.Changeset{}`. A maintainer reading the call site (`ApiServerWeb.VXRentalView.convert_json_to_changeset/1`) or the body will expect Ecto changeset semantics (cast, validate, errors) that do not exist. The misnaming contributes to the broader placement problem (finding B026-5) and makes the code harder to reason about.

---

**B026-13** — [LOW] Misspelled field name `[REDACTED-AWS-SMTP-PASSWORD]` propagated into public API output

File: `lib/api_server_web/views/vx_thing_event_view.ex:43`

Description: The JSON key `[REDACTED-AWS-SMTP-PASSWORD]` (transposed letters: `filger` instead of `filter`) originates in the schema (`vx_thing_event_omega.ex:30`) and is faithfully propagated through the view into the API response. The misspelling is therefore consistent from schema to wire format, but it is part of the public API contract. Any client already consuming this key will break if the spelling is corrected, so the cost of fixing it grows over time. This finding documents it for visibility; correction should be coordinated with a versioned API change.

---

**B026-14** — [INFO] `/1` division used as float-coercion idiom without explanation

File: `lib/api_server_web/views/vx_rental_view.ex:17-18`

Description: `Vx.fetch_actual_usage(...)/1` divides the result by the integer `1`. This is a pattern used elsewhere in the codebase to force an integer result to a float type (Elixir's `/` always returns a float when at least one operand is a float, but here both are integers so the result is an integer — division by `1` does not produce a float in Elixir). If the intent is type coercion, this pattern does not achieve it for integer inputs; `last_week` and `for_month` will remain integers if `fetch_actual_usage` returns an integer. If the intent is something else, it is undocumented. This is an INFO observation because no crash results, but it may indicate a latent type assumption bug.

---

## Summary Table

| ID | Severity | File | Short Title |
|----|----------|------|-------------|
| B026-1 | HIGH | vx_rental_view.ex:17-21 | Live DB queries inside view render function |
| B026-2 | HIGH | vx_thing_event_view.ex:14 | Crash on unpreloaded `thingeventomega` association — no guard |
| B026-3 | MEDIUM | vx_rental_view.ex:55 | Typo in public API key: `hours_to_serivce` |
| B026-4 | MEDIUM | vx_thing_event_view.ex:9-11 | `show.json` missing `%{data: ...}` envelope, inconsistent with `index.json` |
| B026-5 | MEDIUM | vx_rental_view.ex:73-89 | `convert_json_to_changeset/1` belongs in context layer, not a view |
| B026-6 | MEDIUM | vx_thing_omega_view.ex:78 | `engine_utilization_report.json` uses list destructuring; all others use tuples |
| B026-7 | MEDIUM | vx_rental_view.ex:29 | `Map.has_key?/2` on struct field — misleading and fragile |
| B026-8 | LOW | vx_thing_event_view.ex:130 | Trailing comma in map literal — style inconsistency |
| B026-9 | LOW | vx_thing_omega_view.ex:17-61 | Near-duplicate render clauses with no shared helper |
| B026-10 | LOW | vx_restriction_view.ex:14-21 | Raw database column names exposed verbatim in API output |
| B026-11 | LOW | vx_thing_omega_view.ex:103-122 | Inconsistent zero-guard style for `Decimal` division safety |
| B026-12 | LOW | vx_rental_view.ex:80 | `changeset` variable name is misleading — value is a plain map |
| B026-13 | LOW | vx_thing_event_view.ex:43 | Misspelled field `[REDACTED-AWS-SMTP-PASSWORD]` locked into public API |
| B026-14 | INFO | vx_rental_view.ex:17-18 | `/1` division does not produce float — float-coercion idiom is ineffective |
# Pass 4 – B027

**Date:** 2026-02-27
**Audit run:** 2026-02-27-01
**Agent:** B027
**Pass:** 4 – Code Quality

## Files Reviewed

1. `lib/api_server_web/views/vx_thing_summary_view.ex`
2. `lib/api_server_web/views/vx_thing_view.ex`
3. `lib/api_server_web/views/vx_user_function_view.ex`
4. `lib/api_server_web/views/vx_user_view.ex`

---

## Reading Evidence

### File 1: `lib/api_server_web/views/vx_thing_summary_view.ex`

**Module:** `ApiServerWeb.VXThingSummaryView`

**Aliases:**
- `ApiServerWeb.VXThingSummaryView` (line 3)

**Functions:**

| Name | Line |
|------|------|
| `render/2` — `"index.json"` | 5 |
| `render/2` — `"show.json"` | 9 |
| `render/2` — `"vx_thing_summary.json"` | 13 |
| `render/2` — `"rhm_thing_summary.json"` | 57 |

**Types/constants/errors defined:** None.

**Notes:**
- Line 75 contains a commented-out expression: `# location: name <> ", " <> state`
- `"rhm_thing_summary.json"` (line 57) emits the raw `[REDACTED-AWS-SMTP-PASSWORD]` and `[REDACTED-AWS-SMTP-PASSWORD]` keys directly in the response map (lines 119–120) without renaming them to snake_case-free names, unlike all other keys in that same render clause which use clean names (`as_of`, `ignition_status`, etc.).

---

### File 2: `lib/api_server_web/views/vx_thing_view.ex`

**Module:** `ApiServerWeb.VXThingView`

**Uses:**
- `ApiServerWeb, :view` (line 2)
- `Timex` (line 3)

**Aliases:**
- `ApiServerWeb.VXThingView` (line 4)
- `ApiServerWeb.VXThingSummaryView` (line 5)

**Functions:**

| Name | Line |
|------|------|
| `render/2` — `"index.json"` | 8 |
| `render/2` — `"show.json"` | 12 |
| `render/2` — `"fleet_map.json"` (collection) | 16 |
| `render/2` — `"fleet_map.json"` (single) | 20 |
| `render/2` — `"hardware_with_checklists.json"` | 105 |
| `render/2` — `"pm_data.json"` (collection) | 109 |
| `render/2` — `"pm_data.json"` (single) | 113 |
| `render/2` — `"movements.json"` | 147 |
| `render/2` — `"movement.json"` | 150 |
| `render/2` — `"checklists.json"` | 164 |
| `render/2` — `"vx_checklist.json"` | 168 |
| `render/2` — `"vx_thing.json"` | 176 |
| `render/2` — `"rhm_thing_usage.json"` | 220 |
| `render/2` — `"rhm_thing_usage_manual.json"` | 224 |
| `render/2` — `"usage_report.json"` | 228 |
| `render/2` — `"usage_report_many.json"` | 265 |
| `render/2` — `"rhm_things_usage.json"` | 292 |
| `render/2` — `"rhm_thing_events.json"` | 315 |
| `render/2` — `"event_report.json"` | 318 |
| `render/2` — `"rhm_thing.json"` (collection) | 351 |
| `render/2` — `"rhm_thing.json"` (single) | 354 |
| `render/2` — `"basic_thing.json"` (nil guard) | 359 |
| `render/2` — `"basic_thing.json"` | 360 |
| `render/2` — `"sielift_wip_export.json"` | 396 |
| `render/2` — `"pape_exports.json"` | 434 |
| `render/2` — `"pape_export.json"` | 437 |
| `render/2` — `"rhm_things_names.json"` | 449 |
| `render/2` — `"things_only.json"` | 453 |
| `info_to_map/1` | 487 |
| `thing_to_map/2` | 499 |

**Types/constants/errors defined:** None.

**Notes:**
- Large block of commented-out code (lines 507–532): experimental `predicted_service_date` logic with `IO.puts` debug output.
- Line 573: additional single commented-out key in a map: `# predicted_service_date: predicted_service_date`.
- Lines 138–142 in `pm_data.json` single render: hardcoded sentinel floats `0.1`, `0.2`, `0.2`, `0.3`, `0.4` for `previousweek`, `thisweek`, `avgperweek`, `mtdraw`, `weekstoservice`.
- `use Timex` (line 3) is declared but Timex functions are called only through module references (`Timezone.name_of`, `Timezone.get`, `Timezone.convert`, `Timex.now`, `Timex.shift`, `Timex.format`) — the active code only uses `Timezone.*` module calls without the `use Timex` macro being needed for them; the `Timex.*` calls exist only inside the commented-out block.
- Line 541 checks `if vx_thing == nil` inside `thing_to_map/2` after already accessing `vx_thing.aadsvchrs` and other fields on line 571 — the nil check is logically unreachable in the non-nil path and is dead code given the struct access would have already crashed.
- `"hardware_with_checklists.json"` (line 105) delegates to `"vx_thing.json"` rather than a dedicated checklist template — misleading name.
- `render/2` for `"fleet_map.json"` single (line 20) returns an empty string `""` for the no-summary branch (line 101); this is inconsistent with other nil-guard render clauses that return `%{}` (e.g., line 359).

---

### File 3: `lib/api_server_web/views/vx_user_function_view.ex`

**Module:** `ApiServerWeb.VXUserFunctionView`

**Aliases:**
- `ApiServerWeb.VXUserFunctionView` (line 3)

**Functions:**

| Name | Line |
|------|------|
| `render/2` — `"index.json"` | 5 |
| `render/2` — `"show.json"` | 9 |
| `render/2` — `"vx_user_function.json"` | 13 |

**Types/constants/errors defined:** None.

**Notes:** No anomalies detected in isolation. Very small, straightforward module.

---

### File 4: `lib/api_server_web/views/vx_user_view.ex`

**Module:** `ApiServerWeb.VXUserView`

**Aliases:**
- `ApiServerWeb.VXUserView` (line 3)

**Functions:**

| Name | Line |
|------|------|
| `render/2` — `"index.json"` | 5 |
| `render/2` — `"show.json"` | 9 |
| `render/2` — `"rhm_users.json"` | 13 |
| `render/2` — `"rhm_user.json"` | 17 |
| `render/2` — `"fleet_list.json"` | 58 |

**Types/constants/errors defined:** None.

**Notes:**
- `render/2` for `"index.json"` (line 5) delegates to `"rhm_user.json"` but the template name on the wire is `"rhm_user.json"`, not `"vx_user.json"`. This is a naming inconsistency — other view modules use a `"vx_<entity>.json"` template for the canonical single-item rendering, but this one uses `"rhm_user.json"` for both the collection render and the `show` render.
- `user_level` falls back to the hard-coded integer `2` (line 36) when no function is attached. This magic number has no named constant or comment explaining its meaning (2 = some privilege level?).
- The variable `user` is rebound (shadowed) inside `render/2` at line 39 using the same name as the incoming pattern-match variable. While legal in Elixir, this is a code smell that can confuse readers.

---

## Findings

---

**B027-1** — [HIGH] Hardcoded stub sentinel values in `pm_data.json` render — never replaced with real implementation

File: `lib/api_server_web/views/vx_thing_view.ex:138`

Description: The single-item render clause for `"pm_data.json"` (lines 113–145) returns five fields with hardcoded floating-point sentinel values: `previousweek: 0.1`, `thisweek: 0.2`, `avgperweek: 0.2`, `mtdraw: 0.3`, `weekstoservice: 0.4`. These are clearly placeholder/stub values that were never replaced with actual computed data. API consumers silently receive fabricated numbers. The fields `previousweek`, `thisweek`, `avgperweek`, and `mtdraw` have no corresponding computation anywhere in the function — unlike `lastmeterreading` and `hourstoservice` which are properly derived. This endpoint is misleading and incorrect in production.

---

**B027-2** — [MEDIUM] Large block of commented-out code with `IO.puts` debug lines in `thing_to_map/2`

File: `lib/api_server_web/views/vx_thing_view.ex:507`

Description: Lines 507–532 contain a large multi-line comment block that includes experimental `predicted_service_date` logic along with seven `IO.puts` debug statements. The comment block is prefaced with a narrative explanation of why the logic was disabled (lines 507–511), indicating the code was never finished, not merely temporarily disabled. Dead commented-out code of this size obscures the module, and the embedded `IO.puts` calls would produce stdout noise in production if re-enabled carelessly. This should be removed from the codebase.

---

**B027-3** — [LOW] Single commented-out map key referencing a variable from the dead block

File: `lib/api_server_web/views/vx_thing_view.ex:573`

Description: Line 573 contains `# predicted_service_date: predicted_service_date` inside the return map of `thing_to_map/2`. This is a remnant of the commented-out logic in finding B027-2. It is unnecessary noise left in the map structure comment and should be removed along with the larger block.

---

**B027-4** — [LOW] Commented-out map key in `"rhm_thing_summary.json"` render

File: `lib/api_server_web/views/vx_thing_summary_view.ex:75`

Description: Line 75 contains `# location: name <> ", " <> state` inside the `gps` sub-map of the `"rhm_thing_summary.json"` render clause. The variables `name` and `state` are not bound anywhere in the function — meaning this code would not compile if uncommented as-is. This indicates incomplete feature work that was never implemented. The comment should be removed or completed with actual implementation.

---

**B027-5** — [MEDIUM] `use Timex` declared but only needed by commented-out dead code

File: `lib/api_server_web/views/vx_thing_view.ex:3`

Description: `use Timex` is declared on line 3. The active (non-commented) code in this module uses `Timezone.name_of/1`, `Timezone.get/1`, and `Timezone.convert/2` directly by module name — these do not require `use Timex`. The only calls that require `Timex.*` namespace (`Timex.now/0`, `Timex.shift/2`, `Timex.format/3`) are exclusively inside the commented-out `predicted_service_date` block (lines 524–529). Keeping `use Timex` causes an unnecessary macro expansion and may produce a compiler warning depending on Elixir/Timex version. If the commented-out block is removed (as recommended in B027-2), `use Timex` becomes entirely dead.

---

**B027-6** — [MEDIUM] `"fleet_map.json"` single-item render returns `""` (empty string) instead of `%{}` for the no-summary case

File: `lib/api_server_web/views/vx_thing_view.ex:101`

Description: The single-item `"fleet_map.json"` render clause (line 20) returns the empty string `""` when `vx_thing.summary` is `nil` (line 101). All other nil-guard or fallback render clauses in this file and in the view layer return `%{}` (an empty map) — for example, `render("basic_thing.json", %{vx_thing: nil})` on line 359, `info_to_map/1` on line 489, and `thing_to_map/2` on line 542. Returning `""` (a string) where a map is expected breaks the type contract of the collection renderer: `render_many` on line 17 will insert a bare string element into the list rather than a map, potentially causing JSON encoding errors or malformed API responses downstream.

---

**B027-7** — [LOW] Style inconsistency — two raw `abm*` keys leak through the otherwise clean `"rhm_thing_summary.json"` response shape

File: `lib/api_server_web/views/vx_thing_summary_view.ex:119`

Description: The `"rhm_thing_summary.json"` render clause (lines 57–122) was clearly designed to expose a clean, human-readable API surface using keys like `as_of`, `ignition_status`, `event_type`, `hour_meters`, etc. However, lines 119–120 emit `[REDACTED-AWS-SMTP-PASSWORD]` and `[REDACTED-AWS-SMTP-PASSWORD]` using their raw database field names instead of clean equivalents such as `prestart_last_gmt` and `prestart_checklist`. This is a leaky abstraction — internal database naming conventions are exposed through the public API.

---

**B027-8** — [LOW] Magic number `2` used as default `user_level` with no explanation

File: `lib/api_server_web/views/vx_user_view.ex:36`

Description: In `render/2` for `"rhm_user.json"`, the `user_level` falls back to the literal integer `2` when no function record is associated with the user (line 36). There is no named constant, module attribute, or comment explaining what privilege level `2` represents. This makes it impossible to audit correct behavior or safely change the default without understanding the entire privilege level scheme.

---

**B027-9** — [LOW] Variable shadowing — `user` rebound over the pattern-match parameter of the same name

File: `lib/api_server_web/views/vx_user_view.ex:39`

Description: In `render("rhm_user.json", %{vx_user: user})` (line 17), the parameter `user` is used in expressions on lines 18–37 and then rebound at line 39 with `user = %{...}`. The rebinding replaces the original struct with a plain map of the same name. While syntactically valid Elixir, this pattern is a code smell: a reader expecting `user` to refer to the original struct after line 39 will be confused. The inner variable should use a distinct name such as `user_json` or `response`.

---

**B027-10** — [LOW] Style inconsistency — `"index.json"` in `VXUserView` delegates to `"rhm_user.json"` instead of a `"vx_user.json"` template, inconsistent with peer view modules

File: `lib/api_server_web/views/vx_user_view.ex:6`

Description: All other view modules in this group (`VXThingView`, `VXThingSummaryView`, `VXUserFunctionView`) use a `"vx_<entity>.json"` template as the canonical single-item serializer, which `"index.json"` and `"show.json"` delegate to. `VXUserView` instead uses `"rhm_user.json"` for this role (lines 6 and 10), mixing the `rhm_` naming convention into what is otherwise a `vx_` naming scheme. This inconsistency makes it harder to reason about which template is authoritative.

---

**B027-11** — [LOW] Unreachable nil guard inside `thing_to_map/2`

File: `lib/api_server_web/views/vx_thing_view.ex:541`

Description: `thing_to_map/2` accesses `vx_thing.aadsvchrs` on line 502 and multiple other struct fields on lines 544–576, then checks `if vx_thing == nil` on line 541 before the struct-access block. If `vx_thing` were actually `nil`, the function would already have raised a `KeyError` or `[REDACTED-AWS-SMTP-PASSWORD]` at line 502 (inside the `weeks_to_service` computation). The `if vx_thing == nil` guard on line 541 is therefore unreachable dead code — it provides no actual protection and gives a false sense of safety.

---

## Summary Table

| ID | Severity | Title | File | Line |
|----|----------|-------|------|------|
| B027-1 | HIGH | Hardcoded stub sentinel values in `pm_data.json` — never replaced | `vx_thing_view.ex` | 138 |
| B027-2 | MEDIUM | Large commented-out block with `IO.puts` debug statements | `vx_thing_view.ex` | 507 |
| B027-3 | LOW | Commented-out map key referencing variable from dead block | `vx_thing_view.ex` | 573 |
| B027-4 | LOW | Commented-out map key with unbound variables in `rhm_thing_summary.json` | `vx_thing_summary_view.ex` | 75 |
| B027-5 | MEDIUM | `use Timex` only needed by commented-out dead code | `vx_thing_view.ex` | 3 |
| B027-6 | MEDIUM | `fleet_map.json` returns `""` instead of `%{}` for no-summary case | `vx_thing_view.ex` | 101 |
| B027-7 | LOW | Raw `abm*` field names leak through otherwise clean `rhm_thing_summary.json` | `vx_thing_summary_view.ex` | 119 |
| B027-8 | LOW | Magic number `2` used as default `user_level` with no explanation | `vx_user_view.ex` | 36 |
| B027-9 | LOW | Variable `user` shadowed by rebinding in same function | `vx_user_view.ex` | 39 |
| B027-10 | LOW | `"index.json"` delegates to `"rhm_user.json"` — inconsistent with `vx_*` naming convention | `vx_user_view.ex` | 6 |
| B027-11 | LOW | Unreachable nil guard in `thing_to_map/2` after prior struct access | `vx_thing_view.ex` | 541 |

**Total findings: 11** (1 HIGH, 3 MEDIUM, 7 LOW)
