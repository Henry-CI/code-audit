# Pass 3 Documentation Audit — A78
**Audit run:** 2026-02-26-01
**Agent:** A78
**Files:**
- `src/main/java/com/dao/ManufactureDAO.java`
- `src/main/java/com/dao/MenuDAO.java`

---

## 1. Reading Evidence

### ManufactureDAO.java

**Class:** `ManufactureDAO` — line 17

**Fields:**

| Name | Type | Line |
|------|------|------|
| `log` | `static Logger` | 19 |
| `QUERY_MANUFACTURE_SQL` | `static final String` | 21–22 |
| `QUERY_VEHICLE_BY_MANUFACTURE_SQL` | `static final String` | 24–25 |
| `theInstance` | `static ManufactureDAO` | 27 |

**Methods:**

| Method | Modifier(s) | Return Type | Line |
|--------|-------------|-------------|------|
| `getInstance()` | `public synchronized static` | `ManufactureDAO` | 29 |
| `ManufactureDAO()` (constructor) | `private` | — | 37 |
| `getAllManufactures(String companyId)` | `public static` | `List<ManufactureBean>` | 40 |
| `getManufactureById(String id)` | `public` | `ArrayList<ManufactureBean>` | 60 |
| `delManufacturById(String id)` | `public static` | `Boolean` | 99 |
| `checkManuByNm(String name, String id)` | `public` | `boolean` | 137 |
| `saveManufacturer(ManufactureBean manufactureBean)` | `public static` | `boolean` | 174 |
| `updateManufacturer(ManufactureBean manufactureBean)` | `public static` | `boolean` | 210 |
| `getManu_type_fuel_rel(String manuId)` | `public` | `ArrayList<ManuTypeFuleRelBean>` | 247 |
| `checkManu_type_fuel_rel(ManuTypeFuleRelBean manuTypeFuleRelBean)` | `public` | `boolean` | 291 |
| `saveManu_type_fuel_rel(ManuTypeFuleRelBean manuTypeFuleRelBean)` | `public` | `boolean` | 335 |
| `delManu_type_fuel_rel(String relId)` | `public` | `boolean` | 373 |
| `isVehicleAssignedToManufacturer(String manufacturerId)` | `public static` | `boolean` | 404 |

---

### MenuDAO.java

**Class:** `MenuDAO` — line 17

**Fields:**

| Name | Type | Line |
|------|------|------|
| `log` | `static Logger` | 19 |

**Methods:**

| Method | Modifier(s) | Return Type | Line |
|--------|-------------|-------------|------|
| `getAllMenu(String lanCode)` | `public` | `ArrayList<MenuBean>` | 21 |
| `getRoleMenu(ArrayList<String> arrRole, String lanCode)` | `public` | `ArrayList<MenuBean>` | 66 |
| `saveRoleMenu(String roleId, String menuId)` | `public` | `void` | 112 |
| `delRoleMenu(String roleId)` | `public` | `Boolean` | 139 |

---

## 2. Javadoc Coverage Analysis

### ManufactureDAO.java

A search of the file reveals zero Javadoc comment blocks (`/** ... */`). No method or class in this file has any Javadoc documentation.

### MenuDAO.java

A search of the file reveals zero Javadoc comment blocks (`/** ... */`). No method or class in this file has any Javadoc documentation.

---

## 3. Findings

### A78-1 — No class-level Javadoc: ManufactureDAO
- **Severity:** LOW
- **File:** `ManufactureDAO.java`, line 17
- **Detail:** The class `ManufactureDAO` has no class-level Javadoc comment. There is no description of the class purpose, the singleton pattern employed, or the domain it covers (manufacturer/fuel-type relationship management).

---

### A78-2 — No class-level Javadoc: MenuDAO
- **Severity:** LOW
- **File:** `MenuDAO.java`, line 17
- **Detail:** The class `MenuDAO` has no class-level Javadoc comment. There is no description of the class purpose or the domain (role-based menu retrieval).

---

### A78-3 — Undocumented non-trivial public method: `getInstance()`
- **Severity:** MEDIUM
- **File:** `ManufactureDAO.java`, line 29
- **Detail:** `getInstance()` implements the singleton pattern with `synchronized` double-checked construction. No Javadoc is present. Callers have no documentation of the thread-safety guarantee or the singleton lifecycle.

---

### A78-4 — Undocumented non-trivial public method: `getAllManufactures(String companyId)`
- **Severity:** MEDIUM
- **File:** `ManufactureDAO.java`, line 40
- **Detail:** No Javadoc. This method queries manufactures visible to a company — it returns both globally shared records (`company_id IS NULL`) and company-specific records via the same query. This filtering behaviour is non-obvious and warrants documentation. No `@param`, `@return`, or `@throws` tags.

---

### A78-5 — Undocumented non-trivial public method: `getManufactureById(String id)`
- **Severity:** MEDIUM
- **File:** `ManufactureDAO.java`, line 60
- **Detail:** No Javadoc. Returns a list (potentially empty) rather than a single bean or `null`. No `@param`, `@return`, or `@throws` tags.

---

### A78-6 — Undocumented non-trivial public method: `delManufacturById(String id)`
- **Severity:** MEDIUM
- **File:** `ManufactureDAO.java`, line 99
- **Detail:** No Javadoc. This method performs a two-step transactional delete: it first removes dependent rows from `manu_type_fuel_rel` before removing the manufacture record, then commits. The transactional behaviour and the cascade semantics are not documented. No `@param`, `@return`, or `@throws` tags.

---

### A78-7 — Undocumented non-trivial public method: `checkManuByNm(String name, String id)`
- **Severity:** MEDIUM
- **File:** `ManufactureDAO.java`, line 137
- **Detail:** No Javadoc. The semantics of the `id` parameter are non-obvious: when non-empty it is used to exclude the record with that `id` from the duplicate check (edit-vs-create duality). No `@param`, `@return`, or `@throws` tags.

---

### A78-8 — Undocumented non-trivial public method: `saveManufacturer(ManufactureBean manufactureBean)`
- **Severity:** MEDIUM
- **File:** `ManufactureDAO.java`, line 174
- **Detail:** No Javadoc. Returns `false` both when `executeUpdate()` does not affect exactly one row and when the bean argument is `null`. No `@param`, `@return`, or `@throws` tags.

---

### A78-9 — Undocumented non-trivial public method: `updateManufacturer(ManufactureBean manufactureBean)`
- **Severity:** MEDIUM
- **File:** `ManufactureDAO.java`, line 210
- **Detail:** No Javadoc. Same dual-false-return semantics as `saveManufacturer`. No `@param`, `@return`, or `@throws` tags.

---

### A78-10 — Undocumented non-trivial public method: `getManu_type_fuel_rel(String manuId)`
- **Severity:** MEDIUM
- **File:** `ManufactureDAO.java`, line 247
- **Detail:** No Javadoc. Executes a four-table LEFT OUTER JOIN query to retrieve manufacturer/type/fuel-type relationship data. No `@param`, `@return`, or `@throws` tags.

---

### A78-11 — Undocumented non-trivial public method: `checkManu_type_fuel_rel(ManuTypeFuleRelBean manuTypeFuleRelBean)`
- **Severity:** MEDIUM
- **File:** `ManufactureDAO.java`, line 291
- **Detail:** No Javadoc. The method returns `true` both when a matching relationship already exists (primary intent) AND when the input bean is `null` (defensive fallback at line 320). The `null`-returns-`true` semantic is counter-intuitive and entirely undocumented. No `@param`, `@return`, or `@throws` tags.

---

### A78-12 — Undocumented non-trivial public method: `saveManu_type_fuel_rel(ManuTypeFuleRelBean manuTypeFuleRelBean)`
- **Severity:** MEDIUM
- **File:** `ManufactureDAO.java`, line 335
- **Detail:** No Javadoc. No `@param`, `@return`, or `@throws` tags.

---

### A78-13 — Undocumented non-trivial public method: `delManu_type_fuel_rel(String relId)`
- **Severity:** MEDIUM
- **File:** `ManufactureDAO.java`, line 373
- **Detail:** No Javadoc. No `@param`, `@return`, or `@throws` tags.

---

### A78-14 — Undocumented non-trivial public method: `isVehicleAssignedToManufacturer(String manufacturerId)`
- **Severity:** MEDIUM
- **File:** `ManufactureDAO.java`, line 404
- **Detail:** No Javadoc. No `@param`, `@return`, or `@throws` tags.

---

### A78-15 — Undocumented non-trivial public method: `getAllMenu(String lanCode)`
- **Severity:** MEDIUM
- **File:** `MenuDAO.java`, line 21
- **Detail:** No Javadoc. Retrieves ALL menus from the database for a given language code (not filtered by role). The distinction between this method and `getRoleMenu` is not documented. No `@param`, `@return`, or `@throws` tags.

---

### A78-16 — Undocumented non-trivial public method: `getRoleMenu(ArrayList<String> arrRole, String lanCode)`
- **Severity:** MEDIUM
- **File:** `MenuDAO.java`, line 66
- **Detail:** No Javadoc. The method accepts a list of role IDs and returns only the menus accessible to any of those roles for the given language. The role-filtering and language-filtering semantics are not documented. No `@param`, `@return`, or `@throws` tags.

---

### A78-17 — Undocumented non-trivial public method: `saveRoleMenu(String roleId, String menuId)`
- **Severity:** MEDIUM
- **File:** `MenuDAO.java`, line 112
- **Detail:** No Javadoc. Inserts a row into `role_menu_rel` without any duplicate-check guard. No `@param` or `@throws` tags.

---

### A78-18 — Undocumented non-trivial public method: `delRoleMenu(String roleId)`
- **Severity:** MEDIUM
- **File:** `MenuDAO.java`, line 139
- **Detail:** No Javadoc. Deletes ALL menu assignments for a given role. The bulk-delete behaviour (not a single record) is non-obvious from the name alone and is undocumented. No `@param`, `@return`, or `@throws` tags.

---

### A78-19 — Inaccurate log message in `delManufacturById`
- **Severity:** MEDIUM
- **File:** `ManufactureDAO.java`, line 102
- **Detail:** The log statement reads `"Inside LoginDAO Method : delManufacturById"`. The class is `ManufactureDAO`, not `LoginDAO`. This copy-paste error causes misleading log output that would hamper troubleshooting in production.

---

### A78-20 — Inaccurate log message in `checkManuByNm`
- **Severity:** MEDIUM
- **File:** `ManufactureDAO.java`, line 141
- **Detail:** The log statement reads `"Inside LoginDAO Method : checkManuByNm"`. The class is `ManufactureDAO`, not `LoginDAO`.

---

### A78-21 — Inaccurate log message in `saveManufacturer`
- **Severity:** MEDIUM
- **File:** `ManufactureDAO.java`, line 178
- **Detail:** The log statement reads `"Inside LoginDAO Method : saveManufacturer"`. The class is `ManufactureDAO`, not `LoginDAO`.

---

### A78-22 — Inaccurate log message in `updateManufacturer`
- **Severity:** MEDIUM
- **File:** `ManufactureDAO.java`, line 214
- **Detail:** The log statement reads `"Inside LoginDAO Method : updateManufacturer"`. The class is `ManufactureDAO`, not `LoginDAO`.

---

### A78-23 — Inaccurate log message in `getManu_type_fuel_rel`
- **Severity:** MEDIUM
- **File:** `ManufactureDAO.java`, line 252
- **Detail:** The log statement reads `"Inside LoginDAO Method : getManu_type_fuel_rel"`. The class is `ManufactureDAO`, not `LoginDAO`.

---

### A78-24 — Inaccurate log message in `checkManu_type_fuel_rel`
- **Severity:** MEDIUM
- **File:** `ManufactureDAO.java`, line 296
- **Detail:** The log statement reads `"Inside LoginDAO Method : updateManufacturer"`. The class is `ManufactureDAO` and the method is `checkManu_type_fuel_rel`, not `updateManufacturer`. The method name is also wrong.

---

### A78-25 — Inaccurate log message in `saveManu_type_fuel_rel`
- **Severity:** MEDIUM
- **File:** `ManufactureDAO.java`, line 339
- **Detail:** The log statement reads `"Inside LoginDAO Method : updateManufacturer"`. The class is `ManufactureDAO` and the method is `saveManu_type_fuel_rel`, not `updateManufacturer`. Both the class name and the method name in the log message are wrong.

---

### A78-26 — Inaccurate log message in `getAllMenu`
- **Severity:** MEDIUM
- **File:** `MenuDAO.java`, line 26
- **Detail:** The log statement reads `"Inside TimezoneDAO Method : getAllMenu"`. The class is `MenuDAO`, not `TimezoneDAO`.

---

### A78-27 — Inaccurate log message in `getRoleMenu`
- **Severity:** MEDIUM
- **File:** `MenuDAO.java`, line 71
- **Detail:** The log statement reads `"Inside TimezoneDAO Method : getRoleMenu"`. The class is `MenuDAO`, not `TimezoneDAO`.

---

## 4. Summary Table

| ID | Severity | File | Line | Description |
|----|----------|------|------|-------------|
| A78-1 | LOW | ManufactureDAO.java | 17 | No class-level Javadoc |
| A78-2 | LOW | MenuDAO.java | 17 | No class-level Javadoc |
| A78-3 | MEDIUM | ManufactureDAO.java | 29 | `getInstance()` undocumented |
| A78-4 | MEDIUM | ManufactureDAO.java | 40 | `getAllManufactures()` undocumented |
| A78-5 | MEDIUM | ManufactureDAO.java | 60 | `getManufactureById()` undocumented |
| A78-6 | MEDIUM | ManufactureDAO.java | 99 | `delManufacturById()` undocumented |
| A78-7 | MEDIUM | ManufactureDAO.java | 137 | `checkManuByNm()` undocumented |
| A78-8 | MEDIUM | ManufactureDAO.java | 174 | `saveManufacturer()` undocumented |
| A78-9 | MEDIUM | ManufactureDAO.java | 210 | `updateManufacturer()` undocumented |
| A78-10 | MEDIUM | ManufactureDAO.java | 247 | `getManu_type_fuel_rel()` undocumented |
| A78-11 | MEDIUM | ManufactureDAO.java | 291 | `checkManu_type_fuel_rel()` undocumented |
| A78-12 | MEDIUM | ManufactureDAO.java | 335 | `saveManu_type_fuel_rel()` undocumented |
| A78-13 | MEDIUM | ManufactureDAO.java | 373 | `delManu_type_fuel_rel()` undocumented |
| A78-14 | MEDIUM | ManufactureDAO.java | 404 | `isVehicleAssignedToManufacturer()` undocumented |
| A78-15 | MEDIUM | MenuDAO.java | 21 | `getAllMenu()` undocumented |
| A78-16 | MEDIUM | MenuDAO.java | 66 | `getRoleMenu()` undocumented |
| A78-17 | MEDIUM | MenuDAO.java | 112 | `saveRoleMenu()` undocumented |
| A78-18 | MEDIUM | MenuDAO.java | 139 | `delRoleMenu()` undocumented |
| A78-19 | MEDIUM | ManufactureDAO.java | 102 | Log says "LoginDAO" in `delManufacturById` |
| A78-20 | MEDIUM | ManufactureDAO.java | 141 | Log says "LoginDAO" in `checkManuByNm` |
| A78-21 | MEDIUM | ManufactureDAO.java | 178 | Log says "LoginDAO" in `saveManufacturer` |
| A78-22 | MEDIUM | ManufactureDAO.java | 214 | Log says "LoginDAO" in `updateManufacturer` |
| A78-23 | MEDIUM | ManufactureDAO.java | 252 | Log says "LoginDAO" in `getManu_type_fuel_rel` |
| A78-24 | MEDIUM | ManufactureDAO.java | 296 | Log says "LoginDAO / updateManufacturer" in `checkManu_type_fuel_rel` |
| A78-25 | MEDIUM | ManufactureDAO.java | 339 | Log says "LoginDAO / updateManufacturer" in `saveManu_type_fuel_rel` |
| A78-26 | MEDIUM | MenuDAO.java | 26 | Log says "TimezoneDAO" in `getAllMenu` |
| A78-27 | MEDIUM | MenuDAO.java | 71 | Log says "TimezoneDAO" in `getRoleMenu` |

**Total findings: 27** (2 LOW, 25 MEDIUM)
