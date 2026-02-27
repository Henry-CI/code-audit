# Pass 3 -- Documentation Audit: bean package (E-P)

**Auditor:** A02
**Date:** 2026-02-25
**Branch:** release/UAT_RELEASE_FLEETFOCUS_Production
**Base path:** `WEB-INF/src/com/torrent/surat/fms6/bean/`

---

## 1. EntityBean.java

### Reading Evidence

- **Class:** `EntityBean implements Serializable` (line 5)
- **Javadoc class comment:** ABSENT
- **serialVersionUID comment:** Empty block comment (lines 7-9) -- not a class-level Javadoc
- **TODO/FIXME/HACK/XXX:** None found
- **Misleading inline comments:** None found

| # | Method Signature | Line | Javadoc |
|---|-----------------|------|---------|
| 1 | `public String getId()` | 19 | ABSENT |
| 2 | `public void setId(String id)` | 22 | ABSENT |
| 3 | `public String getName()` | 25 | ABSENT |
| 4 | `public void setName(String name)` | 28 | ABSENT |
| 5 | `public double getTotalno()` | 31 | ABSENT |
| 6 | `public void setTotalno(double totalno)` | 34 | ABSENT |
| 7 | `public String getAttribute()` | 37 | ABSENT |
| 8 | `public void setAttribute(String attribute)` | 40 | ABSENT |
| 9 | `public String getLocs()` | 43 | ABSENT |
| 10 | `public void setLocs(String locs)` | 46 | ABSENT |
| 11 | `public String getDepts()` | 49 | ABSENT |
| 12 | `public void setDepts(String depts)` | 52 | ABSENT |

---

## 2. FleetCheckBean.java

### Reading Evidence

- **Class:** `FleetCheckBean` (line 5) -- does NOT implement Serializable
- **Javadoc class comment:** ABSENT
- **TODO/FIXME/HACK/XXX:** None found
- **Misleading inline comments:** None found

| # | Method Signature | Line | Javadoc |
|---|-----------------|------|---------|
| 1 | `public String getAvg_completion_time()` | 11 | ABSENT |
| 2 | `public void setAvg_completion_time(String avg_completion_time)` | 14 | ABSENT |
| 3 | `public ArrayList<String> getFrequent_failed_question()` | 18 | ABSENT |
| 4 | `public void setFrequent_failed_question(ArrayList<String> frequent_failed_question)` | 21 | ABSENT |
| 5 | `public String getUnitName()` | 25 | ABSENT |
| 6 | `public void setUnitName(String unitName)` | 28 | ABSENT |

---

## 3. ImpactBean.java

### Reading Evidence

- **Class:** `ImpactBean implements Serializable` (line 6)
- **Javadoc class comment:** ABSENT
- **serialVersionUID comment:** Empty block comment (lines 7-9) -- not a class-level Javadoc
- **TODO/FIXME/HACK/XXX:** None found
- **Inline comments:** `//monthly national report` (line 25), `//new monthly report` (line 40), `//end` (line 43) -- not misleading but terse

| # | Method Signature | Line | Javadoc |
|---|-----------------|------|---------|
| 1 | `public void addImactMap(int month, int impact_no)` | 47 | ABSENT |
| 2 | `public String getModel_name()` | 52 | ABSENT |
| 3 | `public void setModel_name(String model_name)` | 55 | ABSENT |
| 4 | `public String getModel_cd()` | 58 | ABSENT |
| 5 | `public void setModel_cd(String model_cd)` | 60 | ABSENT |
| 6 | `public String getDept_name()` | 64 | ABSENT |
| 7 | `public void setDept_name(String dept_name)` | 67 | ABSENT |
| 8 | `public String getDept_cd()` | 70 | ABSENT |
| 9 | `public void setDept_cd(String dept_cd)` | 72 | ABSENT |
| 10 | `public String getDriver_name()` | 76 | ABSENT |
| 11 | `public void setDriver_name(String driver_name)` | 79 | ABSENT |
| 12 | `public String getDriver_cd()` | 82 | ABSENT |
| 13 | `public void setDriver_cd(String driver_cd)` | 85 | ABSENT |
| 14 | `public int getYear()` | 88 | ABSENT |
| 15 | `public void setYear(int year)` | 91 | ABSENT |
| 16 | `public String getCust_cd()` | 94 | ABSENT |
| 17 | `public void setCust_cd(String cust_cd)` | 97 | ABSENT |
| 18 | `public String getLoc_cd()` | 100 | ABSENT |
| 19 | `public void setLoc_cd(String loc_cd)` | 103 | ABSENT |
| 20 | `public HashMap<Integer, Integer> getImpactMap()` | 106 | ABSENT |
| 21 | `public void setImpactMap(HashMap<Integer, Integer> impactMap)` | 109 | ABSENT |
| 22 | `public int getMonth()` | 112 | ABSENT |
| 23 | `public void setMonth(int month)` | 116 | ABSENT |
| 24 | `public int getImpact_no()` | 120 | ABSENT |
| 25 | `public void setImpact_no(int impact_no)` | 124 | ABSENT |
| 26 | `public int[] getBlueshock()` | 128 | ABSENT |
| 27 | `public void setBlueshock(int[] blueshock)` | 132 | ABSENT |
| 28 | `public int[] getAmbershock()` | 136 | ABSENT |
| 29 | `public void setAmbershock(int[] ambershock)` | 140 | ABSENT |
| 30 | `public int[] getRedshock()` | 144 | ABSENT |
| 31 | `public void setRedshock(int[] redshock)` | 148 | ABSENT |
| 32 | `public String getUnit_cd()` | 152 | ABSENT |
| 33 | `public void setUnit_cd(String unit_cd)` | 156 | ABSENT |
| 34 | `public String getUnit_name()` | 160 | ABSENT |
| 35 | `public void setUnit_name(String unit_name)` | 164 | ABSENT |
| 36 | `public int getBlueimpact()` | 168 | ABSENT |
| 37 | `public void setBlueimpact(int blueimpact)` | 172 | ABSENT |
| 38 | `public int getAmberimpact()` | 176 | ABSENT |
| 39 | `public void setAmberimpact(int amberimpact)` | 180 | ABSENT |
| 40 | `public int getRedimpact()` | 184 | ABSENT |
| 41 | `public void setRedimpact(int redimpact)` | 188 | ABSENT |
| 42 | `public int getIotime()` | 192 | ABSENT |
| 43 | `public void setIotime(int iotime)` | 196 | ABSENT |
| 44 | `public String getUsagePercentage()` | 200 | ABSENT |
| 45 | `public void setUsagePercentage(String usagePercentage)` | 204 | ABSENT |
| 46 | `public int[] getImpacts()` | 208 | ABSENT |
| 47 | `public void setImpacts(int[] impacts)` | 212 | ABSENT |
| 48 | `public int getTotal()` | 216 | ABSENT |
| 49 | `public void setTotal(int total)` | 220 | ABSENT |
| 50 | `public String getUnit_type()` | 224 | ABSENT |
| 51 | `public void setUnit_type(String unit_type)` | 228 | ABSENT |
| 52 | `public int[][] getBlueshockShift()` | 232 | ABSENT |
| 53 | `public int[][] getAmbershockShift()` | 236 | ABSENT |
| 54 | `public int[][] getRedshockShift()` | 240 | ABSENT |
| 55 | `public void setBlueshockShift(int[][] blueshockShift)` | 244 | ABSENT |
| 56 | `public void setAmbershockShift(int[][] ambershockShift)` | 248 | ABSENT |
| 57 | `public void setRedshockShift(int[][] redshockShift)` | 252 | ABSENT |

---

## 4. ImpactDeptBean.java

### Reading Evidence

- **Class:** `ImpactDeptBean implements Serializable` (line 6)
- **Javadoc class comment:** ABSENT
- **serialVersionUID comment:** Empty block comment (lines 7-9) -- not a class-level Javadoc
- **TODO/FIXME/HACK/XXX:** None found
- **Misleading inline comments:** None found

| # | Method Signature | Line | Javadoc |
|---|-----------------|------|---------|
| 1 | `public String getDept_cd()` | 18 | ABSENT |
| 2 | `public void setDept_cd(String dept_cd)` | 21 | ABSENT |
| 3 | `public String getDept_name()` | 24 | ABSENT |
| 4 | `public void setDept_name(String dept_name)` | 27 | ABSENT |
| 5 | `public ArrayList<ImpactSummaryBean> getArrImpactSummryBean()` | 30 | ABSENT |
| 6 | `public void setArrImpactSummryBean(ArrayList<ImpactSummaryBean> arrImpactSummryBean)` | 33 | ABSENT |
| 7 | `public int getTotal()` | 37 | ABSENT |
| 8 | `public void setTotal(int total)` | 40 | ABSENT |

---

## 5. ImpactLocBean.java

### Reading Evidence

- **Class:** `ImpactLocBean implements Serializable` (line 6)
- **Javadoc class comment:** ABSENT
- **serialVersionUID comment:** Empty block comment (lines 8-10) -- not a class-level Javadoc
- **TODO/FIXME/HACK/XXX:** None found
- **Misleading inline comments:** None found

| # | Method Signature | Line | Javadoc |
|---|-----------------|------|---------|
| 1 | `public String getLoc_cd()` | 19 | ABSENT |
| 2 | `public void setLoc_cd(String loc_cd)` | 22 | ABSENT |
| 3 | `public String getLoc_name()` | 25 | ABSENT |
| 4 | `public void setLoc_name(String loc_name)` | 28 | ABSENT |
| 5 | `public ArrayList<ImpactDeptBean> getArrImpactDeptBean()` | 31 | ABSENT |
| 6 | `public void setArrImpactDeptBean(ArrayList<ImpactDeptBean> arrImpactDeptBean)` | 34 | ABSENT |
| 7 | `public int getIndex()` | 37 | ABSENT |
| 8 | `public void setIndex(int index)` | 40 | ABSENT |
| 9 | `public int getTotal()` | 43 | ABSENT |
| 10 | `public void setTotal(int total)` | 46 | ABSENT |
| 11 | `public void addArrImpactDeptBean(ImpactDeptBean impactDeptBean)` | 50 | ABSENT |

---

## 6. ImpactSummaryBean.java

### Reading Evidence

- **Class:** `ImpactSummaryBean implements Serializable` (line 6)
- **Javadoc class comment:** ABSENT
- **serialVersionUID:** NOT declared (missing)
- **TODO/FIXME/HACK/XXX:** None found
- **Misleading inline comments:** None found

| # | Method Signature | Line | Javadoc |
|---|-----------------|------|---------|
| 1 | `public String getLoc_cd()` | 16 | ABSENT |
| 2 | `public void setLoc_cd(String loc_cd)` | 19 | ABSENT |
| 3 | `public String getLoc_name()` | 22 | ABSENT |
| 4 | `public void setLoc_name(String loc_name)` | 25 | ABSENT |
| 5 | `public ArrayList<ImpactBean> getArrImpact()` | 28 | ABSENT |
| 6 | `public void setArrImpact(ArrayList<ImpactBean> arrImpact)` | 31 | ABSENT |
| 7 | `public int getIndex()` | 34 | ABSENT |
| 8 | `public void setIndex(int index)` | 37 | ABSENT |
| 9 | `public void addArrImpact(ImpactBean impactBean)` | 40 | ABSENT |
| 10 | `public int getTotal()` | 43 | ABSENT |
| 11 | `public void setTotal(int total)` | 46 | ABSENT |
| 12 | `public String getDriver_cd()` | 49 | ABSENT |
| 13 | `public void setDriver_cd(String driver_cd)` | 52 | ABSENT |
| 14 | `public String getDriver_name()` | 55 | ABSENT |
| 15 | `public void setDriver_name(String driver_name)` | 58 | ABSENT |

---

## 7. LicenseBlackListBean.java

### Reading Evidence

- **Class:** `LicenseBlackListBean` (line 5) -- does NOT implement Serializable
- **Javadoc class comment:** ABSENT
- **TODO/FIXME/HACK/XXX:** None found
- **Misleading inline comments:** None found

| # | Method Signature | Line | Javadoc |
|---|-----------------|------|---------|
| 1 | `public String getVehicleType()` | 19 | ABSENT |
| 2 | `public void setVehicleType(String vehicleType)` | 22 | ABSENT |
| 3 | `public String getCustCd()` | 25 | ABSENT |
| 4 | `public void setCustCd(String custCd)` | 28 | ABSENT |
| 5 | `public String getLocCd()` | 31 | ABSENT |
| 6 | `public void setLocCd(String locCd)` | 34 | ABSENT |
| 7 | `public String getDeptCd()` | 37 | ABSENT |
| 8 | `public void setDeptCd(String deptCd)` | 40 | ABSENT |
| 9 | `public String getExpiryDate()` | 43 | ABSENT |
| 10 | `public void setExpiryDate(String expiryDate)` | 46 | ABSENT |
| 11 | `public String getDriverCd()` | 49 | ABSENT |
| 12 | `public void setDriverCd(String driverCd)` | 52 | ABSENT |
| 13 | `public String getAccess_level()` | 55 | ABSENT |
| 14 | `public void setAccess_level(String access_level)` | 58 | ABSENT |
| 15 | `public String getAccess_cust()` | 61 | ABSENT |
| 16 | `public void setAccess_cust(String access_cust)` | 64 | ABSENT |
| 17 | `public String getAccess_site()` | 67 | ABSENT |
| 18 | `public void setAccess_site(String access_site)` | 70 | ABSENT |
| 19 | `public String getAccess_dept()` | 73 | ABSENT |
| 20 | `public void setAccess_dept(String access_dept)` | 76 | ABSENT |
| 21 | `public ArrayList<String> getVehicleCds()` | 79 | ABSENT |
| 22 | `public void setVehicleCds(ArrayList<String> vehicleCds)` | 82 | ABSENT |

---

## 8. LockOutBean.java

### Reading Evidence

- **Class:** `LockOutBean implements Serializable` (line 5)
- **Javadoc class comment:** ABSENT
- **serialVersionUID comment:** Empty block comment (lines 7-9) -- not a class-level Javadoc
- **TODO/FIXME/HACK/XXX:** None found
- **Misleading inline comments:** None found

| # | Method Signature | Line | Javadoc |
|---|-----------------|------|---------|
| 1 | `public String getId()` | 19 | ABSENT |
| 2 | `public void setId(String id)` | 22 | ABSENT |
| 3 | `public String getFleetno()` | 25 | ABSENT |
| 4 | `public void setFleetno(String fleetno)` | 28 | ABSENT |
| 5 | `public String getLockouttime()` | 31 | ABSENT |
| 6 | `public void setLockouttime(String lockouttime)` | 34 | ABSENT |
| 7 | `public String getDriver()` | 37 | ABSENT |
| 8 | `public void setDriver(String driver)` | 40 | ABSENT |
| 9 | `public String getUnlocktime()` | 43 | ABSENT |
| 10 | `public void setUnlocktime(String unlocktime)` | 46 | ABSENT |
| 11 | `public String getMaster_code()` | 49 | ABSENT |
| 12 | `public void setMaster_code(String master_code)` | 52 | ABSENT |
| 13 | `public String getType()` | 55 | ABSENT |
| 14 | `public void setType(String type)` | 58 | ABSENT |

---

## 9. MaxHourUsageBean.java

### Reading Evidence

- **Class:** `MaxHourUsageBean implements Serializable` (line 6)
- **Javadoc class comment:** ABSENT
- **serialVersionUID comment:** Empty block comment (lines 8-10) -- not a class-level Javadoc
- **TODO/FIXME/HACK/XXX:** None found
- **Misleading inline comments:** None found

| # | Method Signature | Line | Javadoc |
|---|-----------------|------|---------|
| 1 | `public String getModel_name()` | 17 | ABSENT |
| 2 | `public void setModel_name(String model_name)` | 20 | ABSENT |
| 3 | `public String getModel_img()` | 23 | ABSENT |
| 4 | `public void setModel_img(String model_img)` | 26 | ABSENT |
| 5 | `public ArrayList<UnitutilBean> getArrUnitUtil()` | 29 | ABSENT |
| 6 | `public void setArrUnitUtil(ArrayList<UnitutilBean> arrUnitUtil)` | 32 | ABSENT |
| 7 | `public void addArrUnitUtil(UnitutilBean unitutilBean)` | 36 | ABSENT |

---

## 10. MenuBean.java

### Reading Evidence

- **Class:** `MenuBean` (line 5) -- does NOT implement Serializable
- **Javadoc class comment:** ABSENT
- **TODO/FIXME/HACK/XXX:** None found
- **Misleading inline comments:** None found

| # | Method Signature | Line | Javadoc |
|---|-----------------|------|---------|
| 1 | `public String getMenus_Cd()` | 13 | ABSENT |
| 2 | `public String getMenus_Name()` | 16 | ABSENT |
| 3 | `public String getForm_Cd()` | 19 | ABSENT |
| 4 | `public String getForm_Name()` | 22 | ABSENT |
| 5 | `public String getForm_Path()` | 25 | ABSENT |
| 6 | `public String getReskinPath()` | 28 | ABSENT |
| 7 | `public void setMenus_Cd(String menus_Cd)` | 31 | ABSENT |
| 8 | `public void setMenus_Name(String menus_Name)` | 34 | ABSENT |
| 9 | `public void setForm_Cd(String form_Cd)` | 37 | ABSENT |
| 10 | `public void setForm_Name(String form_Name)` | 40 | ABSENT |
| 11 | `public void setForm_Path(String form_Path)` | 43 | ABSENT |
| 12 | `public void setReskinPath(String reskinPath)` | 46 | ABSENT |

---

## 11. MymessagesUsersBean.java

### Reading Evidence

- **Class:** `MymessagesUsersBean implements Serializable` (line 5)
- **Javadoc class comment:** ABSENT
- **serialVersionUID comment:** Empty block comment (lines 7-9) -- not a class-level Javadoc
- **TODO/FIXME/HACK/XXX:** None found
- **Misleading inline comments:** None found

| # | Method Signature | Line | Javadoc |
|---|-----------------|------|---------|
| 1 | `public String getCust_cd()` | 22 | ABSENT |
| 2 | `public void setCust_cd(String cust_cd)` | 25 | ABSENT |
| 3 | `public String getLoc_cd()` | 28 | ABSENT |
| 4 | `public void setLoc_cd(String loc_cd)` | 31 | ABSENT |
| 5 | `public String getDept_cd()` | 34 | ABSENT |
| 6 | `public void setDept_cd(String dept_cd)` | 37 | ABSENT |
| 7 | `public String getThreshold()` | 40 | ABSENT |
| 8 | `public void setThreshold(String threshold)` | 43 | ABSENT |
| 9 | `public String getUser_id()` | 46 | ABSENT |
| 10 | `public void setUser_id(String user_id)` | 49 | ABSENT |
| 11 | `public String getUser_email()` | 52 | ABSENT |
| 12 | `public void setUser_email(String user_email)` | 55 | ABSENT |
| 13 | `public String getDescrption()` | 58 | ABSENT |
| 14 | `public void setDescrption(String descrption)` | 61 | ABSENT |
| 15 | `public String getId()` | 64 | ABSENT |
| 16 | `public void setId(String id)` | 67 | ABSENT |

---

## 12. NetworkSettingBean.java

### Reading Evidence

- **Class:** `NetworkSettingBean implements Serializable` (line 5)
- **Javadoc class comment:** ABSENT
- **serialVersionUID:** NOT declared (missing)
- **TODO/FIXME/HACK/XXX:** None found
- **Misleading inline comments:** None found

| # | Method Signature | Line | Javadoc |
|---|-----------------|------|---------|
| 1 | `public int getIndex()` | 12 | ABSENT |
| 2 | `public void setIndex(int index)` | 15 | ABSENT |
| 3 | `public String getCountry()` | 18 | ABSENT |
| 4 | `public void setCountry(String country)` | 21 | ABSENT |
| 5 | `public String getSsid()` | 24 | ABSENT |
| 6 | `public void setSsid(String ssid)` | 27 | ABSENT |
| 7 | `public String getPassword()` | 30 | ABSENT |
| 8 | `public void setPassword(String password)` | 33 | ABSENT |

---

## 13. NotificationSettingsBean.java

### Reading Evidence

- **Class:** `NotificationSettingsBean` (line 3) -- does NOT implement Serializable
- **Javadoc class comment:** ABSENT
- **TODO/FIXME/HACK/XXX:** None found
- **Misleading inline comments:** None found

| # | Method Signature | Line | Javadoc |
|---|-----------------|------|---------|
| 1 | `public String getNotification_id()` | 12 | ABSENT |
| 2 | `public void setNotification_id(String notification_id)` | 15 | ABSENT |
| 3 | `public String getHeader()` | 18 | ABSENT |
| 4 | `public void setHeader(String header)` | 21 | ABSENT |
| 5 | `public String getTitle()` | 24 | ABSENT |
| 6 | `public void setTitle(String title)` | 27 | ABSENT |
| 7 | `public String getContent()` | 30 | ABSENT |
| 8 | `public void setContent(String content)` | 33 | ABSENT |
| 9 | `public String getSignature()` | 36 | ABSENT |
| 10 | `public void setSignature(String signature)` | 39 | ABSENT |
| 11 | `public boolean isEnabled()` | 42 | ABSENT |
| 12 | `public void setEnabled(boolean enabled)` | 45 | ABSENT |

---

## 14. PreCheckBean.java

### Reading Evidence

- **Class:** `PreCheckBean implements Serializable` (line 8)
- **Javadoc class comment:** ABSENT
- **serialVersionUID comment:** Empty block comment (lines 10-12) -- not a class-level Javadoc
- **TODO/FIXME/HACK/XXX:** None found
- **Inline comments:** `//new Monthly Report` (line 22) -- not misleading but terse

| # | Method Signature | Line | Javadoc |
|---|-----------------|------|---------|
| 1 | `public void addCheckMap(String drivername, int total)` | 29 | ABSENT |
| 2 | `public HashMap<String, Integer> getCheckMap()` | 33 | ABSENT |
| 3 | `public void setCheckMap(HashMap<String, Integer> checkMap)` | 36 | ABSENT |
| 4 | `public String getName()` | 40 | ABSENT |
| 5 | `public void setName(String name)` | 43 | ABSENT |
| 6 | `public String getId()` | 46 | ABSENT |
| 7 | `public void setId(String id)` | 49 | ABSENT |
| 8 | `public int getComplete()` | 52 | ABSENT |
| 9 | `public void setComplete(int complete)` | 55 | ABSENT |
| 10 | `public int getIncomplete()` | 58 | ABSENT |
| 11 | `public void setIncomplete(int incomplete)` | 61 | ABSENT |
| 12 | `public int getTotal()` | 64 | ABSENT |
| 13 | `public void setTotal(int total)` | 67 | ABSENT |
| 14 | `public String getDept_id()` | 70 | ABSENT |
| 15 | `public void setDept_id(String dept_id)` | 73 | ABSENT |
| 16 | `public String getDept_name()` | 76 | ABSENT |
| 17 | `public void setDept_name(String dept_name)` | 79 | ABSENT |
| 18 | `public int[] getChecks()` | 82 | ABSENT |
| 19 | `public void setChecks(int[] checks)` | 85 | ABSENT |
| 20 | `public ArrayList<PreCheckDriverBean> getArrPreCheckDriverBean()` | 88 | ABSENT |
| 21 | `public void setArrPreCheckDriverBean(ArrayList<PreCheckDriverBean> arrPreCheckDriverBean)` | 91 | ABSENT |

---

## 15. PreCheckDriverBean.java

### Reading Evidence

- **Class:** `PreCheckDriverBean implements Serializable` (line 5)
- **Javadoc class comment:** ABSENT
- **serialVersionUID comment:** Empty block comment (lines 7-9) -- not a class-level Javadoc
- **TODO/FIXME/HACK/XXX:** None found
- **Misleading inline comments:** None found

| # | Method Signature | Line | Javadoc |
|---|-----------------|------|---------|
| 1 | `public int getTotal()` | 17 | ABSENT |
| 2 | `public void setTotal(int total)` | 20 | ABSENT |
| 3 | `public String getDriver_cd()` | 23 | ABSENT |
| 4 | `public void setDriver_cd(String driver_cd)` | 26 | ABSENT |
| 5 | `public String getDriver_name()` | 29 | ABSENT |
| 6 | `public void setDriver_name(String driver_name)` | 32 | ABSENT |
| 7 | `public int[] getChecks()` | 35 | ABSENT |
| 8 | `public void setChecks(int[] checks)` | 38 | ABSENT |

---

## 16. PreCheckSummaryBean.java

### Reading Evidence

- **Class:** `PreCheckSummaryBean implements Serializable` (line 6)
- **Javadoc class comment:** ABSENT
- **serialVersionUID:** NOT declared (missing)
- **TODO/FIXME/HACK/XXX:** None found
- **Misleading inline comments:** None found

| # | Method Signature | Line | Javadoc |
|---|-----------------|------|---------|
| 1 | `public String getLoc_cd()` | 15 | ABSENT |
| 2 | `public void setLoc_cd(String loc_cd)` | 18 | ABSENT |
| 3 | `public String getLoc_name()` | 21 | ABSENT |
| 4 | `public void setLoc_name(String loc_name)` | 24 | ABSENT |
| 5 | `public ArrayList<PreCheckBean> getArrPrecheck()` | 27 | ABSENT |
| 6 | `public void setArrPrecheck(ArrayList<PreCheckBean> arrPrecheck)` | 30 | ABSENT |
| 7 | `public void addArrPrecheck(PreCheckBean preCheckBean)` | 34 | ABSENT |
| 8 | `public int getIndex()` | 37 | ABSENT |
| 9 | `public void setIndex(int index)` | 40 | ABSENT |
| 10 | `public int getTotal()` | 43 | ABSENT |
| 11 | `public void setTotal(int total)` | 46 | ABSENT |

---

## Findings

### A02-1 -- Missing class-level Javadoc on all 16 bean classes

| ID | Severity | File | Description |
|----|----------|------|-------------|
| A02-1 | MEDIUM | EntityBean.java:5 | No class-level Javadoc. Purpose of this data-transfer object (entity with id, name, totalno, attribute, locs, depts) is unclear without documentation. |
| A02-2 | MEDIUM | FleetCheckBean.java:5 | No class-level Javadoc. Bean carries fleet check data (unit name, avg completion time, frequent failed questions) but purpose and usage context are undocumented. |
| A02-3 | MEDIUM | ImpactBean.java:6 | No class-level Javadoc. Large bean (57 public methods, ~30 fields) representing impact/shock data. Multiple field groups (blue/amber/red shock, shift variants, monthly report arrays) have no explanation of their domain meaning. |
| A02-4 | MEDIUM | ImpactDeptBean.java:6 | No class-level Javadoc. Aggregation bean grouping ImpactSummaryBeans by department; relationship hierarchy is undocumented. |
| A02-5 | MEDIUM | ImpactLocBean.java:6 | No class-level Javadoc. Aggregation bean grouping ImpactDeptBeans by location; relationship hierarchy is undocumented. |
| A02-6 | MEDIUM | ImpactSummaryBean.java:6 | No class-level Javadoc. Summary bean aggregating ImpactBeans with location and driver info; relationship to ImpactLocBean/ImpactDeptBean hierarchy is undocumented. |
| A02-7 | MEDIUM | LicenseBlackListBean.java:5 | No class-level Javadoc. Bean carries license blacklist filter criteria including access-level fields; business rules for blacklisting are undocumented. |
| A02-8 | MEDIUM | LockOutBean.java:5 | No class-level Javadoc. Bean represents a fleet lockout event with lockout/unlock times and master code; domain context is undocumented. |
| A02-9 | MEDIUM | MaxHourUsageBean.java:6 | No class-level Javadoc. Bean groups UnitutilBeans by model for max-hour usage reporting; purpose undocumented. |
| A02-10 | MEDIUM | MenuBean.java:5 | No class-level Javadoc. Bean represents a menu item with form paths and reskin paths; navigation model is undocumented. |
| A02-11 | MEDIUM | MymessagesUsersBean.java:5 | No class-level Javadoc. Bean carries user messaging subscription data (threshold, email, description); domain purpose is undocumented. |
| A02-12 | MEDIUM | NetworkSettingBean.java:5 | No class-level Javadoc. Bean stores WiFi network settings (country, SSID, password); deployment context is undocumented. |
| A02-13 | MEDIUM | NotificationSettingsBean.java:3 | No class-level Javadoc. Bean represents notification template settings (header, title, content, signature, enabled flag); purpose undocumented. |
| A02-14 | MEDIUM | PreCheckBean.java:8 | No class-level Javadoc. Bean tracks pre-check completion counts by driver, with monthly report arrays; relationship to PreCheckDriverBean is undocumented. |
| A02-15 | MEDIUM | PreCheckDriverBean.java:5 | No class-level Javadoc. Bean holds per-driver pre-check data with monthly check arrays; purpose undocumented. |
| A02-16 | MEDIUM | PreCheckSummaryBean.java:6 | No class-level Javadoc. Summary bean grouping PreCheckBeans by location; hierarchy undocumented. |

### A02-17 -- Missing Javadoc on non-trivial public methods

| ID | Severity | File | Line | Method | Description |
|----|----------|------|------|--------|-------------|
| A02-17 | MEDIUM | ImpactBean.java | 47 | `addImactMap(int, int)` | Business logic method (adds month-to-impact mapping) with no Javadoc. Method name also contains a typo ("Imact" instead of "Impact"). Lacks @param documentation for `month` and `impact_no`. |
| A02-18 | MEDIUM | ImpactLocBean.java | 50 | `addArrImpactDeptBean(ImpactDeptBean)` | Mutator that appends to internal list -- not a simple setter. No Javadoc. |
| A02-19 | MEDIUM | ImpactSummaryBean.java | 40 | `addArrImpact(ImpactBean)` | Mutator that appends to internal list -- not a simple setter. No Javadoc. |
| A02-20 | MEDIUM | MaxHourUsageBean.java | 36 | `addArrUnitUtil(UnitutilBean)` | Mutator that appends to internal list -- not a simple setter. No Javadoc. |
| A02-21 | MEDIUM | PreCheckBean.java | 29 | `addCheckMap(String, int)` | Business logic method (adds driver-name-to-total mapping) with no Javadoc. Lacks @param documentation. |
| A02-22 | MEDIUM | PreCheckSummaryBean.java | 34 | `addArrPrecheck(PreCheckBean)` | Mutator that appends to internal list -- not a simple setter. No Javadoc. |

### A02-23 -- Missing Javadoc on all getter/setter methods (bulk)

| ID | Severity | File | Count | Description |
|----|----------|------|-------|-------------|
| A02-23 | LOW | EntityBean.java | 12 | All 12 getter/setter methods lack Javadoc. |
| A02-24 | LOW | FleetCheckBean.java | 6 | All 6 getter/setter methods lack Javadoc. |
| A02-25 | LOW | ImpactBean.java | 56 | All 56 getter/setter methods lack Javadoc. Fields like `blueshock[8]`, `ambershock[8]`, `redshock[8]`, `blueshockShift[8][3]` and `iotime` have non-obvious semantics. |
| A02-26 | LOW | ImpactDeptBean.java | 8 | All 8 getter/setter methods lack Javadoc. |
| A02-27 | LOW | ImpactLocBean.java | 10 | All 10 getter/setter methods lack Javadoc. |
| A02-28 | LOW | ImpactSummaryBean.java | 14 | All 14 getter/setter methods lack Javadoc. |
| A02-29 | LOW | LicenseBlackListBean.java | 22 | All 22 getter/setter methods lack Javadoc. |
| A02-30 | LOW | LockOutBean.java | 14 | All 14 getter/setter methods lack Javadoc. |
| A02-31 | LOW | MaxHourUsageBean.java | 6 | All 6 getter/setter methods lack Javadoc. |
| A02-32 | LOW | MenuBean.java | 12 | All 12 getter/setter methods lack Javadoc. |
| A02-33 | LOW | MymessagesUsersBean.java | 16 | All 16 getter/setter methods lack Javadoc. |
| A02-34 | LOW | NetworkSettingBean.java | 8 | All 8 getter/setter methods lack Javadoc. |
| A02-35 | LOW | NotificationSettingsBean.java | 12 | All 12 getter/setter methods lack Javadoc. |
| A02-36 | LOW | PreCheckBean.java | 20 | All 20 getter/setter methods lack Javadoc. |
| A02-37 | LOW | PreCheckDriverBean.java | 8 | All 8 getter/setter methods lack Javadoc. |
| A02-38 | LOW | PreCheckSummaryBean.java | 10 | All 10 getter/setter methods lack Javadoc. |

### A02-39 -- Typo in method name constitutes misleading API surface

| ID | Severity | File | Line | Description |
|----|----------|------|------|-------------|
| A02-39 | HIGH | ImpactBean.java | 47 | Method `addImactMap` is misspelled -- should be `addImpactMap`. This constitutes a misleading public API identifier that could cause confusion or bugs in callers searching for "Impact" by name. |

### A02-40 -- Typo in field name / accessor

| ID | Severity | File | Line | Description |
|----|----------|------|------|-------------|
| A02-40 | INFO | MymessagesUsersBean.java | 17,58,61 | Field `descrption` and accessors `getDescrption()`/`setDescrption()` are misspelled (missing 'i' -- should be "description"). This is a minor API surface issue. |
| A02-41 | INFO | ImpactDeptBean.java | 14,30,33 | Field and accessor `arrImpactSummryBean` / `getArrImpactSummryBean()` / `setArrImpactSummryBean()` are misspelled (should be "Summary" not "Summry"). |

### A02-42 -- Empty serialVersionUID block comments

| ID | Severity | File | Lines | Description |
|----|----------|------|-------|-------------|
| A02-42 | INFO | EntityBean.java | 7-9 | Empty block comment above serialVersionUID (IDE-generated placeholder) provides no value. |
| A02-43 | INFO | ImpactBean.java | 7-9 | Same as A02-42. |
| A02-44 | INFO | ImpactDeptBean.java | 7-9 | Same as A02-42. |
| A02-45 | INFO | ImpactLocBean.java | 8-10 | Same as A02-42. |
| A02-46 | INFO | LockOutBean.java | 7-9 | Same as A02-42. |
| A02-47 | INFO | MaxHourUsageBean.java | 8-10 | Same as A02-42. |
| A02-48 | INFO | MymessagesUsersBean.java | 7-9 | Same as A02-42. |
| A02-49 | INFO | PreCheckBean.java | 10-12 | Same as A02-42. |
| A02-50 | INFO | PreCheckDriverBean.java | 7-9 | Same as A02-42. |

### A02-51 -- Terse / uninformative inline comments

| ID | Severity | File | Line | Comment | Description |
|----|----------|------|------|---------|-------------|
| A02-51 | INFO | ImpactBean.java | 25 | `//monthly national report` | Minimal context; does not explain what the following arrays represent or their index semantics. |
| A02-52 | INFO | ImpactBean.java | 40-43 | `//new monthly report` ... `//end` | Terse section markers with no explanation of what changed or why a new report format was added. |
| A02-53 | INFO | PreCheckBean.java | 22 | `//new Monthly Report` | Same pattern as A02-52; no explanation of the new fields that follow. |

---

## Summary

| Severity | Count |
|----------|-------|
| HIGH | 1 |
| MEDIUM | 22 |
| LOW | 16 |
| INFO | 13 |
| **Total** | **52** |

**Key observations:**

1. **Zero Javadoc across all 16 files.** Not a single class or method in any of the 16 bean files has a Javadoc comment. This is a systemic documentation gap across the entire bean package (E-P range).

2. **All 16 classes lack class-level Javadoc** explaining their purpose, domain context, or relationship to other beans in the impact/precheck/lockout hierarchies.

3. **Six non-trivial public methods** (add/mutator methods that are not simple getters/setters) lack documentation. These methods embed business logic (map population, list aggregation) that is not self-evident.

4. **One HIGH-severity finding:** The method `addImactMap` in ImpactBean.java is misspelled, creating a misleading API surface.

5. **224 total public methods** across all 16 files, all undocumented.

6. **Multiple identifier typos** (`descrption`, `Summry`, `Imact`) that, while not documentation per se, contribute to code comprehension difficulties and would be exacerbated by the complete absence of documentation.

---
*End of Pass 3 audit -- Agent A02*
