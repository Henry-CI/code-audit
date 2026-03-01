#!/bin/bash
# Dispatch all 94 security audit agents

REPO="C:/Projects/cig-audit/repos/fleetiq"
OUT="C:/Projects/cig-audit/repos/fleetiq/audit/2026-03-01-01/pass1"
BRANCH="multi-customer-sync-to-master"

dispatch_agent() {
  local ID="$1"
  local FILES="$2"
  local PROMPT="Security audit agent ${ID}. Repository: C:/Projects/cig-audit/repos/fleetiq. Branch: multi-customer-sync-to-master.
1. Verify branch: run git -C \"C:/Projects/cig-audit/repos/fleetiq\" branch --show-current — must be multi-customer-sync-to-master. STOP if wrong.
2. Read: C:/Projects/cig-audit/repos/fleetiq/audit/2026-03-01-01/pass1/AGENT-INSTRUCTIONS.md
3. Read: C:/Projects/cig-audit/audit-skills/PASS1-CHECKLIST-ff-new.md
4. Read EACH file IN FULL (paths relative to C:/Projects/cig-audit/repos/fleetiq/):
${FILES}
5. Produce reading evidence for every file FIRST, then review against all applicable checklist sections.
6. Write output to: C:/Projects/cig-audit/repos/fleetiq/audit/2026-03-01-01/pass1/${ID}.md
Report only — do NOT fix anything."

  echo "Dispatching ${ID}..."
  echo "$PROMPT" | claude --model claude-sonnet-4-5 --no-interactive -p - > "${OUT}/${ID}.log" 2>&1 &
  echo "PID $! for ${ID}"
}

# J01
dispatch_agent "J01" "WEB-INF/src/com/ci/entity/Dealer.java
WEB-INF/src/com/ci/entity/DealerConfigBean.java
WEB-INF/src/com/torrent/surat/fms6/bean/BatteryBean.java"

# J02
dispatch_agent "J02" "WEB-INF/src/com/torrent/surat/fms6/bean/BroadcastmsgBean.java
WEB-INF/src/com/torrent/surat/fms6/bean/CanruleBean.java
WEB-INF/src/com/torrent/surat/fms6/bean/DailyUsageDeptDataBean.java"

# J03
dispatch_agent "J03" "WEB-INF/src/com/torrent/surat/fms6/bean/DailyUsageHourBean.java
WEB-INF/src/com/torrent/surat/fms6/bean/DashboarSubscriptionBean.java
WEB-INF/src/com/torrent/surat/fms6/bean/DayhoursBean.java"

# J04
dispatch_agent "J04" "WEB-INF/src/com/torrent/surat/fms6/bean/DriverBean.java
WEB-INF/src/com/torrent/surat/fms6/bean/DriverImportBean.java
WEB-INF/src/com/torrent/surat/fms6/bean/DriverInfoBean.java"

# J05
dispatch_agent "J05" "WEB-INF/src/com/torrent/surat/fms6/bean/DriverLeagueBean.java
WEB-INF/src/com/torrent/surat/fms6/bean/EntityBean.java
WEB-INF/src/com/torrent/surat/fms6/bean/EquipmentBypassAlert.java"

# J06
dispatch_agent "J06" "WEB-INF/src/com/torrent/surat/fms6/bean/FleetCheckBean.java
WEB-INF/src/com/torrent/surat/fms6/bean/ImpactBean.java
WEB-INF/src/com/torrent/surat/fms6/bean/ImpactDeptBean.java"

# J07
dispatch_agent "J07" "WEB-INF/src/com/torrent/surat/fms6/bean/ImpactLevel.java
WEB-INF/src/com/torrent/surat/fms6/bean/ImpactLocBean.java
WEB-INF/src/com/torrent/surat/fms6/bean/ImpactSummaryBean.java"

# J08
dispatch_agent "J08" "WEB-INF/src/com/torrent/surat/fms6/bean/LicenseBlackListBean.java
WEB-INF/src/com/torrent/surat/fms6/bean/LockOutBean.java
WEB-INF/src/com/torrent/surat/fms6/bean/MaxHourUsageBean.java"

# J09
dispatch_agent "J09" "WEB-INF/src/com/torrent/surat/fms6/bean/MenuBean.java
WEB-INF/src/com/torrent/surat/fms6/bean/MymessagesUsersBean.java
WEB-INF/src/com/torrent/surat/fms6/bean/NetworkSettingBean.java"

# J10
dispatch_agent "J10" "WEB-INF/src/com/torrent/surat/fms6/bean/NotificationSettingsBean.java
WEB-INF/src/com/torrent/surat/fms6/bean/PreCheckBean.java
WEB-INF/src/com/torrent/surat/fms6/bean/PreCheckDriverBean.java"

# J11
dispatch_agent "J11" "WEB-INF/src/com/torrent/surat/fms6/bean/PreCheckSummaryBean.java
WEB-INF/src/com/torrent/surat/fms6/bean/QuestionBean.java
WEB-INF/src/com/torrent/surat/fms6/bean/RestrictedAccessUsageBean.java"

# J12
dispatch_agent "J12" "WEB-INF/src/com/torrent/surat/fms6/bean/SalespersonBean.java
WEB-INF/src/com/torrent/surat/fms6/bean/ServiceDueFlagBean.java
WEB-INF/src/com/torrent/surat/fms6/bean/SessionEntity.java"

# J13
dispatch_agent "J13" "WEB-INF/src/com/torrent/surat/fms6/bean/SiteConfigurationBean.java
WEB-INF/src/com/torrent/surat/fms6/bean/SpecialAccessBean.java
WEB-INF/src/com/torrent/surat/fms6/bean/StateTimezone.java"

# J14
dispatch_agent "J14" "WEB-INF/src/com/torrent/surat/fms6/bean/SubscriptionBean.java
WEB-INF/src/com/torrent/surat/fms6/bean/SuperMasterAuthBean.java
WEB-INF/src/com/torrent/surat/fms6/bean/UnitBean.java"

# J15
dispatch_agent "J15" "WEB-INF/src/com/torrent/surat/fms6/bean/UnitUtilSummaryBean.java
WEB-INF/src/com/torrent/surat/fms6/bean/UnitVersionInfoBean.java
WEB-INF/src/com/torrent/surat/fms6/bean/UnitutilBean.java"

# J16
dispatch_agent "J16" "WEB-INF/src/com/torrent/surat/fms6/bean/UnusedUnitBean.java
WEB-INF/src/com/torrent/surat/fms6/bean/UserBean.java
WEB-INF/src/com/torrent/surat/fms6/bean/UserDriverBean.java"

# J17
dispatch_agent "J17" "WEB-INF/src/com/torrent/surat/fms6/bean/UserFormBean.java
WEB-INF/src/com/torrent/surat/fms6/bean/VehDiagnostic.java
WEB-INF/src/com/torrent/surat/fms6/bean/VehNetworkSettingsBean.java"

# J18
dispatch_agent "J18" "WEB-INF/src/com/torrent/surat/fms6/bean/VehicleImportBean.java
WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsight.java
WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightBean.java"

# J19
dispatch_agent "J19" "WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightExcel.java
WEB-INF/src/com/torrent/surat/fms6/businessinsight/CustomReports.java
WEB-INF/src/com/torrent/surat/fms6/chart/BarChartCategory.java"

# J20
dispatch_agent "J20" "WEB-INF/src/com/torrent/surat/fms6/chart/BarChartImpactCategory.java
WEB-INF/src/com/torrent/surat/fms6/chart/BarChartNational.java
WEB-INF/src/com/torrent/surat/fms6/chart/BarChartR.java"

# J21
dispatch_agent "J21" "WEB-INF/src/com/torrent/surat/fms6/chart/BarChartUtil.java
WEB-INF/src/com/torrent/surat/fms6/chart/BarChartUtil_bak.java
WEB-INF/src/com/torrent/surat/fms6/chart/Chart.java"

# J22
dispatch_agent "J22" "WEB-INF/src/com/torrent/surat/fms6/chart/JfreeGroupStackChart.java
WEB-INF/src/com/torrent/surat/fms6/chart/LineChartR.java
WEB-INF/src/com/torrent/surat/fms6/chart/LineChartR_au.java"

# J23
dispatch_agent "J23" "WEB-INF/src/com/torrent/surat/fms6/chart/PieChartR.java
WEB-INF/src/com/torrent/surat/fms6/chart/StackedBarChart.java
WEB-INF/src/com/torrent/surat/fms6/chart/excel/BatteryChargeBean.java"

# J24
dispatch_agent "J24" "WEB-INF/src/com/torrent/surat/fms6/chart/excel/BatteryChargeChart.java
WEB-INF/src/com/torrent/surat/fms6/chart/excel/ChartDashboard.java
WEB-INF/src/com/torrent/surat/fms6/chart/excel/ChartDashboardUtil.java"

# J25
dispatch_agent "J25" "WEB-INF/src/com/torrent/surat/fms6/chart/excel/ChartMailListBean.java
WEB-INF/src/com/torrent/surat/fms6/chart/excel/ChartsExcelDao.java
WEB-INF/src/com/torrent/surat/fms6/chart/excel/CustLocBean.java"

# J26
dispatch_agent "J26" "WEB-INF/src/com/torrent/surat/fms6/chart/excel/DriverAccessAbuseBean.java
WEB-INF/src/com/torrent/surat/fms6/chart/excel/DriverAccessAbuseChart.java
WEB-INF/src/com/torrent/surat/fms6/chart/excel/DriverActivityBean.java"

# J27
dispatch_agent "J27" "WEB-INF/src/com/torrent/surat/fms6/chart/excel/DriverActivityChart.java
WEB-INF/src/com/torrent/surat/fms6/chart/excel/ExpiryBean.java
WEB-INF/src/com/torrent/surat/fms6/chart/excel/ExpiryChart.java"

# J28
dispatch_agent "J28" "WEB-INF/src/com/torrent/surat/fms6/chart/excel/ImpactChart.java
WEB-INF/src/com/torrent/surat/fms6/chart/excel/MachineUnlockChart.java
WEB-INF/src/com/torrent/surat/fms6/chart/excel/PreopFailBean.java"

# J29
dispatch_agent "J29" "WEB-INF/src/com/torrent/surat/fms6/chart/excel/PreopFailChart.java
WEB-INF/src/com/torrent/surat/fms6/chart/excel/UnitUtilBean.java
WEB-INF/src/com/torrent/surat/fms6/chart/excel/UnlockBean.java"

# J30
dispatch_agent "J30" "WEB-INF/src/com/torrent/surat/fms6/chart/excel/UserLoginBean.java
WEB-INF/src/com/torrent/surat/fms6/chart/excel/UserLoginChart.java
WEB-INF/src/com/torrent/surat/fms6/dao/UnitDAO.java"

# J31
dispatch_agent "J31" "WEB-INF/src/com/torrent/surat/fms6/dashboard/BatteryCharge.java
WEB-INF/src/com/torrent/surat/fms6/dashboard/Config.java
WEB-INF/src/com/torrent/surat/fms6/dashboard/CriticalBattery.java"

# J32
dispatch_agent "J32" "WEB-INF/src/com/torrent/surat/fms6/dashboard/Impacts.java
WEB-INF/src/com/torrent/surat/fms6/dashboard/Licence.java
WEB-INF/src/com/torrent/surat/fms6/dashboard/Pct_utilisation.java"

# J33
dispatch_agent "J33" "WEB-INF/src/com/torrent/surat/fms6/dashboard/Preop.java
WEB-INF/src/com/torrent/surat/fms6/dashboard/SessionCleanupListener.java
WEB-INF/src/com/torrent/surat/fms6/dashboard/Summary.java"

# J34
dispatch_agent "J34" "WEB-INF/src/com/torrent/surat/fms6/dashboard/TableServlet.java
WEB-INF/src/com/torrent/surat/fms6/dashboard/Utilisation.java
WEB-INF/src/com/torrent/surat/fms6/excel/Frm_MaxHourUsage.java"

# J35
dispatch_agent "J35" "WEB-INF/src/com/torrent/surat/fms6/excel/Frm_excel.java
WEB-INF/src/com/torrent/surat/fms6/excel/Frm_inaUnit_rpt.java
WEB-INF/src/com/torrent/surat/fms6/excel/Frm_month_rpt.java"

# J36
dispatch_agent "J36" "WEB-INF/src/com/torrent/surat/fms6/excel/Frm_national_rpt.java
WEB-INF/src/com/torrent/surat/fms6/excel/Frm_quater_rpt.java
WEB-INF/src/com/torrent/surat/fms6/excel/Frm_unitSummary_rpt.java"

# J37
dispatch_agent "J37" "WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailBatteryReport.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailBroadcastMsgReport.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailCimplicityShockReport.java"

# J38
dispatch_agent "J38" "WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailCimplicityUtilReport.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailCurrDrivReport.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailCurrUnitReport.java"

# J39
dispatch_agent "J39" "WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDailyVehSummaryReport.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDriverAccessAbuseReport.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDriverImpactReport.java"

# J40
dispatch_agent "J40" "WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDriverLicenceExpiry.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDynDriverReport.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDynUnitReport.java"

# J41
dispatch_agent "J41" "WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailImpactMeterReport.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailImpactReport.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailKeyHourUtilReport.java"

# J42
dispatch_agent "J42" "WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailPreOpChkFailReport.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailPreOpChkReport.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailRestictedAccessUsageReport.java"

# J43
dispatch_agent "J43" "WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailSeatHourUtilReport.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailServMaintenanceReport.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailServMaintenanceReportNew.java"

# J44
dispatch_agent "J44" "WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailSuperMasterAuthReport.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailUnitUnlockReport.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailUtilWowReport.java"

# J45
dispatch_agent "J45" "WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailUtilisationReport.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelBatteryReport.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelBroadcastMsgReport.java"

# J46
dispatch_agent "J46" "WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelCimplicityShockReport.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelCimplicityUtilReport.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelCurrDrivReport.java"

# J47
dispatch_agent "J47" "WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelCurrUnitReport.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelDailyVehSummaryReport.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelDetailUnitReportBmw.java"

# J48
dispatch_agent "J48" "WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelDriverAccessAbuseReport.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelDriverImpactReport.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelDriverLicenceExpiry.java"

# J49
dispatch_agent "J49" "WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelDynDriverReport.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelDynUnitReport.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelImpactMeterReport.java"

# J50
dispatch_agent "J50" "WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelImpactReport.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelImpactReportBmw.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelKeyHourUtilReport.java"

# J51
dispatch_agent "J51" "WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelPreOpCheckDetailedReport.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelPreOpCheckFailReport.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelPreOpCheckReport.java"

# J52
dispatch_agent "J52" "WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelRestrictedUsageReport.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelSeatHourUtilReport.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelServMaintenanceReport.java"

# J53
dispatch_agent "J53" "WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelSuperMasterAuthReport.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelUnitUnlockReport.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelUtilWOWReport.java"

# J54
dispatch_agent "J54" "WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelUtilWOWReportEmail.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelUtilisationReport.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/MailBase.java"

# J55
dispatch_agent "J55" "WEB-INF/src/com/torrent/surat/fms6/excel/reports/MailExcelReports.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/BatteryReportBean.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/CimplicityShockReportBean.java"

# J56
dispatch_agent "J56" "WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/CimplicityUtilReportBean.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/CurrDrivReportBean.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/CurrUnitReportBean.java"

# J57
dispatch_agent "J57" "WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/DailyVehSummaryReportBean.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/DetailUnitReportBmwBean.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/DetailUnitReportBmwItemBean.java"

# J58
dispatch_agent "J58" "WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/DriverAccessAbuseBean.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/DriverImpactReportBean.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/DriverLicenceExpiryBean.java"

# J59
dispatch_agent "J59" "WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/DynDriverReportBean.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/DynUnitReportBean.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/ImpactReportBean.java"

# J60
dispatch_agent "J60" "WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/ImpactReportBmwBean.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/ImpactReportBmwItemBean.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/KeyHourUtilBean.java"

# J61
dispatch_agent "J61" "WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/PreOpCheckFailReportBean.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/PreOpCheckReportBean.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/SeatHourUtilBean.java"

# J62
dispatch_agent "J62" "WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/ServMaintenanceReportBean.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/SuperMasterAuthReportBean.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/UnitUnlockReportBean.java"

# J63
dispatch_agent "J63" "WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/UtilWowReportBean.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/UtilisationReportBean.java
WEB-INF/src/com/torrent/surat/fms6/excel/reports/dao/CustomerDAO.java"

# J64
dispatch_agent "J64" "WEB-INF/src/com/torrent/surat/fms6/excel/reports/dao/DriverAccessAbuseDAO.java
WEB-INF/src/com/torrent/surat/fms6/master/Databean_customer.java
WEB-INF/src/com/torrent/surat/fms6/master/Databean_getter.java"

# J65
dispatch_agent "J65" "WEB-INF/src/com/torrent/surat/fms6/master/Databean_getuser.java
WEB-INF/src/com/torrent/surat/fms6/master/Databean_user.java
WEB-INF/src/com/torrent/surat/fms6/master/FirmwareverBean.java"

# J66
dispatch_agent "J66" "WEB-INF/src/com/torrent/surat/fms6/master/Frm_saveuser.java
WEB-INF/src/com/torrent/surat/fms6/master/Frm_upload.java
WEB-INF/src/com/torrent/surat/fms6/pdf/MonthlyPDFRpt.java"

# J67
dispatch_agent "J67" "WEB-INF/src/com/torrent/surat/fms6/pdf/ReportPDF.java
WEB-INF/src/com/torrent/surat/fms6/reports/Databean_cdisp.java
WEB-INF/src/com/torrent/surat/fms6/reports/Databean_dyn_reports.java"

# J68
dispatch_agent "J68" "WEB-INF/src/com/torrent/surat/fms6/reports/Databean_report.java
WEB-INF/src/com/torrent/surat/fms6/reports/Databean_report1.java
WEB-INF/src/com/torrent/surat/fms6/reports/Databean_report_new.java"

# J69
dispatch_agent "J69" "WEB-INF/src/com/torrent/surat/fms6/reports/Databean_reports.java
WEB-INF/src/com/torrent/surat/fms6/reports/UtilBean.java
WEB-INF/src/com/torrent/surat/fms6/reports/UtilModelBean.java"

# J70
dispatch_agent "J70" "WEB-INF/src/com/torrent/surat/fms6/security/Databean_security.java
WEB-INF/src/com/torrent/surat/fms6/security/Frm_customer.java
WEB-INF/src/com/torrent/surat/fms6/security/Frm_login.java"

# J71
dispatch_agent "J71" "WEB-INF/src/com/torrent/surat/fms6/security/Frm_security.java
WEB-INF/src/com/torrent/surat/fms6/security/Frm_vehicle.java
WEB-INF/src/com/torrent/surat/fms6/security/GetGenericData.java"

# J72
dispatch_agent "J72" "WEB-INF/src/com/torrent/surat/fms6/security/GetMessages.java
WEB-INF/src/com/torrent/surat/fms6/util/BeanComparator.java
WEB-INF/src/com/torrent/surat/fms6/util/CftsAlert.java"

# J73
dispatch_agent "J73" "WEB-INF/src/com/torrent/surat/fms6/util/CustomComparator.java
WEB-INF/src/com/torrent/surat/fms6/util/CustomUpload.java
WEB-INF/src/com/torrent/surat/fms6/util/DBUtil.java"

# J74
dispatch_agent "J74" "WEB-INF/src/com/torrent/surat/fms6/util/DataUtil.java
WEB-INF/src/com/torrent/surat/fms6/util/DateUtil.java
WEB-INF/src/com/torrent/surat/fms6/util/DriverExpiryAlert.java"

# J75
dispatch_agent "J75" "WEB-INF/src/com/torrent/surat/fms6/util/DriverListUtil.java
WEB-INF/src/com/torrent/surat/fms6/util/DriverMedicalAlert.java
WEB-INF/src/com/torrent/surat/fms6/util/DriverUtil.java"

# J76
dispatch_agent "J76" "WEB-INF/src/com/torrent/surat/fms6/util/Dt_Checker.java
WEB-INF/src/com/torrent/surat/fms6/util/EncryptTest.java
WEB-INF/src/com/torrent/surat/fms6/util/ExcelUtil.java"

# J77
dispatch_agent "J77" "WEB-INF/src/com/torrent/surat/fms6/util/FleetCheckFTP.java
WEB-INF/src/com/torrent/surat/fms6/util/GForceCalibration.java
WEB-INF/src/com/torrent/surat/fms6/util/GetFile.java"

# J78
dispatch_agent "J78" "WEB-INF/src/com/torrent/surat/fms6/util/GetHtml.java
WEB-INF/src/com/torrent/surat/fms6/util/ImpactUtil.java
WEB-INF/src/com/torrent/surat/fms6/util/ImportFiles.java"

# J79
dispatch_agent "J79" "WEB-INF/src/com/torrent/surat/fms6/util/InfoLogger.java
WEB-INF/src/com/torrent/surat/fms6/util/LindeConfig.java
WEB-INF/src/com/torrent/surat/fms6/util/LoadBundle.java"

# J80
dispatch_agent "J80" "WEB-INF/src/com/torrent/surat/fms6/util/LogicBean_filter.java
WEB-INF/src/com/torrent/surat/fms6/util/LogicBean_filter1.java
WEB-INF/src/com/torrent/surat/fms6/util/Menu_Bean.java"

# J81
dispatch_agent "J81" "WEB-INF/src/com/torrent/surat/fms6/util/Menu_Bean1.java
WEB-INF/src/com/torrent/surat/fms6/util/PurgeData.java
WEB-INF/src/com/torrent/surat/fms6/util/RuntimeConf.java"

# J82
dispatch_agent "J82" "WEB-INF/src/com/torrent/surat/fms6/util/SendMessage.java
WEB-INF/src/com/torrent/surat/fms6/util/SessionVar.java
WEB-INF/src/com/torrent/surat/fms6/util/SkyhookService.java"

# J83
dispatch_agent "J83" "WEB-INF/src/com/torrent/surat/fms6/util/TeslaBadgeUtil.java
WEB-INF/src/com/torrent/surat/fms6/util/UtilBean.java
WEB-INF/src/com/torrent/surat/fms6/util/call_mail.java"

# J84
dispatch_agent "J84" "WEB-INF/src/com/torrent/surat/fms6/util/escapeSingleQuotes.java
WEB-INF/src/com/torrent/surat/fms6/util/fix_department.java
WEB-INF/src/com/torrent/surat/fms6/util/mail.java"

# J85
dispatch_agent "J85" "WEB-INF/src/com/torrent/surat/fms6/util/password_life.java
WEB-INF/src/com/torrent/surat/fms6/util/password_policy.java
WEB-INF/src/com/torrent/surat/fms6/util/send_timezone.java"

# J86
dispatch_agent "J86" "WEB-INF/src/com/torrent/surat/fms6/util/send_updatepreop.java
WEB-INF/src/com/torrent/surat/frms6/dao/BatteryDAO.java
WEB-INF/src/com/torrent/surat/frms6/dao/DriverDAO.java"

# J87
dispatch_agent "J87" "WEB-INF/src/com/torrent/surat/frms6/dao/DriverImportDAO.java
WEB-INF/src/com/torrent/surat/frms6/dao/ImpactDAO.java
WEB-INF/src/com/torrent/surat/frms6/dao/ImportDAO.java"

# J88
dispatch_agent "J88" "WEB-INF/src/com/torrent/surat/frms6/dao/LockOutDAO.java
WEB-INF/src/com/torrent/surat/frms6/dao/MessageDao.java
WEB-INF/src/com/torrent/surat/frms6/dao/PreCheckDAO.java"

# J89
dispatch_agent "J89" "WEB-INF/src/com/torrent/surat/frms6/dao/RegisterDAO.java
WEB-INF/src/com/torrent/surat/frms6/dao/UnitDAO.java"

# C01
dispatch_agent "C01" "Jenkinsfile
WEB-INF/src/log4j.properties
WEB-INF/src/log4j2.properties
WEB-INF/urlrewrite.xml
WEB-INF/web - Copy.xml
WEB-INF/web.xml"

# C02
dispatch_agent "C02" "WEB-INF/src/main/resource/Messages.properties
WEB-INF/src/main/resource/Messages_en.properties
WEB-INF/src/main/resource/Messages_en_US.properties
WEB-INF/src/main/resource/Messages_es.properties
WEB-INF/src/main/resource/Messages_zh.properties
WEB-INF/src/main/resource/Messages_zh_CN.properties
WEB-INF/taglibs-mailer.tld
WEB-INF/taglibs-request.tld
pages/bundle/Messages.properties
pages/bundle/Messages_en.properties
pages/bundle/Messages_en_US.properties
pages/bundle/Messages_es.properties
pages/bundle/Messages_zh.properties
pages/bundle/Messages_zh_CN.properties"

# S01
dispatch_agent "S01" "sql/FLEETIQ_AUG_2022.sql
sql/FLEETIQ_JAN_2022.sql
sql/FLEETIQ_JAN_2023.sql
sql/FLEETIQ_JUN_2022.sql
sql/FLEETIQ_MAR_2022.sql
sql/FLEETIQ_MAY_2022.sql
sql/FLEETIQ_NOV_2022.sql
sql/FLEETIQ_SEPT_2022.sql"

# S02
dispatch_agent "S02" "sql/check_firmware_idauth_driver_name.sql
sql/disable_unit_preop_perday_perdriver.sql
sql/equipment_bypass.sql
sql/equipment_bypass_report.sql
sql/pedestrian_detection.sql
sql/sp_driver_shock_message.sql
sql/sp_eos_message.sql"

# S03
dispatch_agent "S03" "sql/sp_equipment_bypass_alert.sql
sql/sp_get_driver_name.sql
sql/sp_opchks_response.sql
sql/sp_pstat_message.sql
sql/sp_store_mk3dbg.sql
sql/time_zone_impl.sql
sql/time_zone_impl_varchar_int.sql"

echo "All agents dispatched. Waiting for completion..."
wait
echo "All agents completed."
