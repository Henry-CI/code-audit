import os

OUT = 'C:/Projects/cig-audit/repos/fleetiq/audit/2026-03-01-01/pass1/prompts'
os.makedirs(OUT, exist_ok=True)

agents = {
    'J01': 'WEB-INF/src/com/ci/entity/Dealer.java\nWEB-INF/src/com/ci/entity/DealerConfigBean.java\nWEB-INF/src/com/torrent/surat/fms6/bean/BatteryBean.java',
    'J02': 'WEB-INF/src/com/torrent/surat/fms6/bean/BroadcastmsgBean.java\nWEB-INF/src/com/torrent/surat/fms6/bean/CanruleBean.java\nWEB-INF/src/com/torrent/surat/fms6/bean/DailyUsageDeptDataBean.java',
    'J03': 'WEB-INF/src/com/torrent/surat/fms6/bean/DailyUsageHourBean.java\nWEB-INF/src/com/torrent/surat/fms6/bean/DashboarSubscriptionBean.java\nWEB-INF/src/com/torrent/surat/fms6/bean/DayhoursBean.java',
    'J04': 'WEB-INF/src/com/torrent/surat/fms6/bean/DriverBean.java\nWEB-INF/src/com/torrent/surat/fms6/bean/DriverImportBean.java\nWEB-INF/src/com/torrent/surat/fms6/bean/DriverInfoBean.java',
    'J05': 'WEB-INF/src/com/torrent/surat/fms6/bean/DriverLeagueBean.java\nWEB-INF/src/com/torrent/surat/fms6/bean/EntityBean.java\nWEB-INF/src/com/torrent/surat/fms6/bean/EquipmentBypassAlert.java',
    'J06': 'WEB-INF/src/com/torrent/surat/fms6/bean/FleetCheckBean.java\nWEB-INF/src/com/torrent/surat/fms6/bean/ImpactBean.java\nWEB-INF/src/com/torrent/surat/fms6/bean/ImpactDeptBean.java',
    'J07': 'WEB-INF/src/com/torrent/surat/fms6/bean/ImpactLevel.java\nWEB-INF/src/com/torrent/surat/fms6/bean/ImpactLocBean.java\nWEB-INF/src/com/torrent/surat/fms6/bean/ImpactSummaryBean.java',
    'J08': 'WEB-INF/src/com/torrent/surat/fms6/bean/LicenseBlackListBean.java\nWEB-INF/src/com/torrent/surat/fms6/bean/LockOutBean.java\nWEB-INF/src/com/torrent/surat/fms6/bean/MaxHourUsageBean.java',
    'J09': 'WEB-INF/src/com/torrent/surat/fms6/bean/MenuBean.java\nWEB-INF/src/com/torrent/surat/fms6/bean/MymessagesUsersBean.java\nWEB-INF/src/com/torrent/surat/fms6/bean/NetworkSettingBean.java',
    'J10': 'WEB-INF/src/com/torrent/surat/fms6/bean/NotificationSettingsBean.java\nWEB-INF/src/com/torrent/surat/fms6/bean/PreCheckBean.java\nWEB-INF/src/com/torrent/surat/fms6/bean/PreCheckDriverBean.java',
    'J11': 'WEB-INF/src/com/torrent/surat/fms6/bean/PreCheckSummaryBean.java\nWEB-INF/src/com/torrent/surat/fms6/bean/QuestionBean.java\nWEB-INF/src/com/torrent/surat/fms6/bean/RestrictedAccessUsageBean.java',
    'J12': 'WEB-INF/src/com/torrent/surat/fms6/bean/SalespersonBean.java\nWEB-INF/src/com/torrent/surat/fms6/bean/ServiceDueFlagBean.java\nWEB-INF/src/com/torrent/surat/fms6/bean/SessionEntity.java',
    'J13': 'WEB-INF/src/com/torrent/surat/fms6/bean/SiteConfigurationBean.java\nWEB-INF/src/com/torrent/surat/fms6/bean/SpecialAccessBean.java\nWEB-INF/src/com/torrent/surat/fms6/bean/StateTimezone.java',
    'J14': 'WEB-INF/src/com/torrent/surat/fms6/bean/SubscriptionBean.java\nWEB-INF/src/com/torrent/surat/fms6/bean/SuperMasterAuthBean.java\nWEB-INF/src/com/torrent/surat/fms6/bean/UnitBean.java',
    'J15': 'WEB-INF/src/com/torrent/surat/fms6/bean/UnitUtilSummaryBean.java\nWEB-INF/src/com/torrent/surat/fms6/bean/UnitVersionInfoBean.java\nWEB-INF/src/com/torrent/surat/fms6/bean/UnitutilBean.java',
    'J16': 'WEB-INF/src/com/torrent/surat/fms6/bean/UnusedUnitBean.java\nWEB-INF/src/com/torrent/surat/fms6/bean/UserBean.java\nWEB-INF/src/com/torrent/surat/fms6/bean/UserDriverBean.java',
    'J17': 'WEB-INF/src/com/torrent/surat/fms6/bean/UserFormBean.java\nWEB-INF/src/com/torrent/surat/fms6/bean/VehDiagnostic.java\nWEB-INF/src/com/torrent/surat/fms6/bean/VehNetworkSettingsBean.java',
    'J18': 'WEB-INF/src/com/torrent/surat/fms6/bean/VehicleImportBean.java\nWEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsight.java\nWEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightBean.java',
    'J19': 'WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightExcel.java\nWEB-INF/src/com/torrent/surat/fms6/businessinsight/CustomReports.java\nWEB-INF/src/com/torrent/surat/fms6/chart/BarChartCategory.java',
    'J20': 'WEB-INF/src/com/torrent/surat/fms6/chart/BarChartImpactCategory.java\nWEB-INF/src/com/torrent/surat/fms6/chart/BarChartNational.java\nWEB-INF/src/com/torrent/surat/fms6/chart/BarChartR.java',
    'J21': 'WEB-INF/src/com/torrent/surat/fms6/chart/BarChartUtil.java\nWEB-INF/src/com/torrent/surat/fms6/chart/BarChartUtil_bak.java\nWEB-INF/src/com/torrent/surat/fms6/chart/Chart.java',
    'J22': 'WEB-INF/src/com/torrent/surat/fms6/chart/JfreeGroupStackChart.java\nWEB-INF/src/com/torrent/surat/fms6/chart/LineChartR.java\nWEB-INF/src/com/torrent/surat/fms6/chart/LineChartR_au.java',
    'J23': 'WEB-INF/src/com/torrent/surat/fms6/chart/PieChartR.java\nWEB-INF/src/com/torrent/surat/fms6/chart/StackedBarChart.java\nWEB-INF/src/com/torrent/surat/fms6/chart/excel/BatteryChargeBean.java',
    'J24': 'WEB-INF/src/com/torrent/surat/fms6/chart/excel/BatteryChargeChart.java\nWEB-INF/src/com/torrent/surat/fms6/chart/excel/ChartDashboard.java\nWEB-INF/src/com/torrent/surat/fms6/chart/excel/ChartDashboardUtil.java',
    'J25': 'WEB-INF/src/com/torrent/surat/fms6/chart/excel/ChartMailListBean.java\nWEB-INF/src/com/torrent/surat/fms6/chart/excel/ChartsExcelDao.java\nWEB-INF/src/com/torrent/surat/fms6/chart/excel/CustLocBean.java',
    'J26': 'WEB-INF/src/com/torrent/surat/fms6/chart/excel/DriverAccessAbuseBean.java\nWEB-INF/src/com/torrent/surat/fms6/chart/excel/DriverAccessAbuseChart.java\nWEB-INF/src/com/torrent/surat/fms6/chart/excel/DriverActivityBean.java',
    'J27': 'WEB-INF/src/com/torrent/surat/fms6/chart/excel/DriverActivityChart.java\nWEB-INF/src/com/torrent/surat/fms6/chart/excel/ExpiryBean.java\nWEB-INF/src/com/torrent/surat/fms6/chart/excel/ExpiryChart.java',
    'J28': 'WEB-INF/src/com/torrent/surat/fms6/chart/excel/ImpactChart.java\nWEB-INF/src/com/torrent/surat/fms6/chart/excel/MachineUnlockChart.java\nWEB-INF/src/com/torrent/surat/fms6/chart/excel/PreopFailBean.java',
    'J29': 'WEB-INF/src/com/torrent/surat/fms6/chart/excel/PreopFailChart.java\nWEB-INF/src/com/torrent/surat/fms6/chart/excel/UnitUtilBean.java\nWEB-INF/src/com/torrent/surat/fms6/chart/excel/UnlockBean.java',
    'J30': 'WEB-INF/src/com/torrent/surat/fms6/chart/excel/UserLoginBean.java\nWEB-INF/src/com/torrent/surat/fms6/chart/excel/UserLoginChart.java\nWEB-INF/src/com/torrent/surat/fms6/dao/UnitDAO.java',
    'J31': 'WEB-INF/src/com/torrent/surat/fms6/dashboard/BatteryCharge.java\nWEB-INF/src/com/torrent/surat/fms6/dashboard/Config.java\nWEB-INF/src/com/torrent/surat/fms6/dashboard/CriticalBattery.java',
    'J32': 'WEB-INF/src/com/torrent/surat/fms6/dashboard/Impacts.java\nWEB-INF/src/com/torrent/surat/fms6/dashboard/Licence.java\nWEB-INF/src/com/torrent/surat/fms6/dashboard/Pct_utilisation.java',
    'J33': 'WEB-INF/src/com/torrent/surat/fms6/dashboard/Preop.java\nWEB-INF/src/com/torrent/surat/fms6/dashboard/SessionCleanupListener.java\nWEB-INF/src/com/torrent/surat/fms6/dashboard/Summary.java',
    'J34': 'WEB-INF/src/com/torrent/surat/fms6/dashboard/TableServlet.java\nWEB-INF/src/com/torrent/surat/fms6/dashboard/Utilisation.java\nWEB-INF/src/com/torrent/surat/fms6/excel/Frm_MaxHourUsage.java',
    'J35': 'WEB-INF/src/com/torrent/surat/fms6/excel/Frm_excel.java\nWEB-INF/src/com/torrent/surat/fms6/excel/Frm_inaUnit_rpt.java\nWEB-INF/src/com/torrent/surat/fms6/excel/Frm_month_rpt.java',
    'J36': 'WEB-INF/src/com/torrent/surat/fms6/excel/Frm_national_rpt.java\nWEB-INF/src/com/torrent/surat/fms6/excel/Frm_quater_rpt.java\nWEB-INF/src/com/torrent/surat/fms6/excel/Frm_unitSummary_rpt.java',
    'J37': 'WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailBatteryReport.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailBroadcastMsgReport.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailCimplicityShockReport.java',
    'J38': 'WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailCimplicityUtilReport.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailCurrDrivReport.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailCurrUnitReport.java',
    'J39': 'WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDailyVehSummaryReport.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDriverAccessAbuseReport.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDriverImpactReport.java',
    'J40': 'WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDriverLicenceExpiry.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDynDriverReport.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDynUnitReport.java',
    'J41': 'WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailImpactMeterReport.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailImpactReport.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailKeyHourUtilReport.java',
    'J42': 'WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailPreOpChkFailReport.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailPreOpChkReport.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailRestictedAccessUsageReport.java',
    'J43': 'WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailSeatHourUtilReport.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailServMaintenanceReport.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailServMaintenanceReportNew.java',
    'J44': 'WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailSuperMasterAuthReport.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailUnitUnlockReport.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailUtilWowReport.java',
    'J45': 'WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailUtilisationReport.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelBatteryReport.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelBroadcastMsgReport.java',
    'J46': 'WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelCimplicityShockReport.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelCimplicityUtilReport.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelCurrDrivReport.java',
    'J47': 'WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelCurrUnitReport.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelDailyVehSummaryReport.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelDetailUnitReportBmw.java',
    'J48': 'WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelDriverAccessAbuseReport.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelDriverImpactReport.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelDriverLicenceExpiry.java',
    'J49': 'WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelDynDriverReport.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelDynUnitReport.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelImpactMeterReport.java',
    'J50': 'WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelImpactReport.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelImpactReportBmw.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelKeyHourUtilReport.java',
    'J51': 'WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelPreOpCheckDetailedReport.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelPreOpCheckFailReport.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelPreOpCheckReport.java',
    'J52': 'WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelRestrictedUsageReport.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelSeatHourUtilReport.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelServMaintenanceReport.java',
    'J53': 'WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelSuperMasterAuthReport.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelUnitUnlockReport.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelUtilWOWReport.java',
    'J54': 'WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelUtilWOWReportEmail.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelUtilisationReport.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/MailBase.java',
    'J55': 'WEB-INF/src/com/torrent/surat/fms6/excel/reports/MailExcelReports.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/BatteryReportBean.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/CimplicityShockReportBean.java',
    'J56': 'WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/CimplicityUtilReportBean.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/CurrDrivReportBean.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/CurrUnitReportBean.java',
    'J57': 'WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/DailyVehSummaryReportBean.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/DetailUnitReportBmwBean.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/DetailUnitReportBmwItemBean.java',
    'J58': 'WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/DriverAccessAbuseBean.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/DriverImpactReportBean.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/DriverLicenceExpiryBean.java',
    'J59': 'WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/DynDriverReportBean.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/DynUnitReportBean.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/ImpactReportBean.java',
    'J60': 'WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/ImpactReportBmwBean.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/ImpactReportBmwItemBean.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/KeyHourUtilBean.java',
    'J61': 'WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/PreOpCheckFailReportBean.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/PreOpCheckReportBean.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/SeatHourUtilBean.java',
    'J62': 'WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/ServMaintenanceReportBean.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/SuperMasterAuthReportBean.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/UnitUnlockReportBean.java',
    'J63': 'WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/UtilWowReportBean.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/UtilisationReportBean.java\nWEB-INF/src/com/torrent/surat/fms6/excel/reports/dao/CustomerDAO.java',
    'J64': 'WEB-INF/src/com/torrent/surat/fms6/excel/reports/dao/DriverAccessAbuseDAO.java\nWEB-INF/src/com/torrent/surat/fms6/master/Databean_customer.java\nWEB-INF/src/com/torrent/surat/fms6/master/Databean_getter.java',
    'J65': 'WEB-INF/src/com/torrent/surat/fms6/master/Databean_getuser.java\nWEB-INF/src/com/torrent/surat/fms6/master/Databean_user.java\nWEB-INF/src/com/torrent/surat/fms6/master/FirmwareverBean.java',
    'J66': 'WEB-INF/src/com/torrent/surat/fms6/master/Frm_saveuser.java\nWEB-INF/src/com/torrent/surat/fms6/master/Frm_upload.java\nWEB-INF/src/com/torrent/surat/fms6/pdf/MonthlyPDFRpt.java',
    'J67': 'WEB-INF/src/com/torrent/surat/fms6/pdf/ReportPDF.java\nWEB-INF/src/com/torrent/surat/fms6/reports/Databean_cdisp.java\nWEB-INF/src/com/torrent/surat/fms6/reports/Databean_dyn_reports.java',
    'J68': 'WEB-INF/src/com/torrent/surat/fms6/reports/Databean_report.java\nWEB-INF/src/com/torrent/surat/fms6/reports/Databean_report1.java\nWEB-INF/src/com/torrent/surat/fms6/reports/Databean_report_new.java',
    'J69': 'WEB-INF/src/com/torrent/surat/fms6/reports/Databean_reports.java\nWEB-INF/src/com/torrent/surat/fms6/reports/UtilBean.java\nWEB-INF/src/com/torrent/surat/fms6/reports/UtilModelBean.java',
    'J70': 'WEB-INF/src/com/torrent/surat/fms6/security/Databean_security.java\nWEB-INF/src/com/torrent/surat/fms6/security/Frm_customer.java\nWEB-INF/src/com/torrent/surat/fms6/security/Frm_login.java',
    'J71': 'WEB-INF/src/com/torrent/surat/fms6/security/Frm_security.java\nWEB-INF/src/com/torrent/surat/fms6/security/Frm_vehicle.java\nWEB-INF/src/com/torrent/surat/fms6/security/GetGenericData.java',
    'J72': 'WEB-INF/src/com/torrent/surat/fms6/security/GetMessages.java\nWEB-INF/src/com/torrent/surat/fms6/util/BeanComparator.java\nWEB-INF/src/com/torrent/surat/fms6/util/CftsAlert.java',
    'J73': 'WEB-INF/src/com/torrent/surat/fms6/util/CustomComparator.java\nWEB-INF/src/com/torrent/surat/fms6/util/CustomUpload.java\nWEB-INF/src/com/torrent/surat/fms6/util/DBUtil.java',
    'J74': 'WEB-INF/src/com/torrent/surat/fms6/util/DataUtil.java\nWEB-INF/src/com/torrent/surat/fms6/util/DateUtil.java\nWEB-INF/src/com/torrent/surat/fms6/util/DriverExpiryAlert.java',
    'J75': 'WEB-INF/src/com/torrent/surat/fms6/util/DriverListUtil.java\nWEB-INF/src/com/torrent/surat/fms6/util/DriverMedicalAlert.java\nWEB-INF/src/com/torrent/surat/fms6/util/DriverUtil.java',
    'J76': 'WEB-INF/src/com/torrent/surat/fms6/util/Dt_Checker.java\nWEB-INF/src/com/torrent/surat/fms6/util/EncryptTest.java\nWEB-INF/src/com/torrent/surat/fms6/util/ExcelUtil.java',
    'J77': 'WEB-INF/src/com/torrent/surat/fms6/util/FleetCheckFTP.java\nWEB-INF/src/com/torrent/surat/fms6/util/GForceCalibration.java\nWEB-INF/src/com/torrent/surat/fms6/util/GetFile.java',
    'J78': 'WEB-INF/src/com/torrent/surat/fms6/util/GetHtml.java\nWEB-INF/src/com/torrent/surat/fms6/util/ImpactUtil.java\nWEB-INF/src/com/torrent/surat/fms6/util/ImportFiles.java',
    'J79': 'WEB-INF/src/com/torrent/surat/fms6/util/InfoLogger.java\nWEB-INF/src/com/torrent/surat/fms6/util/LindeConfig.java\nWEB-INF/src/com/torrent/surat/fms6/util/LoadBundle.java',
    'J80': 'WEB-INF/src/com/torrent/surat/fms6/util/LogicBean_filter.java\nWEB-INF/src/com/torrent/surat/fms6/util/LogicBean_filter1.java\nWEB-INF/src/com/torrent/surat/fms6/util/Menu_Bean.java',
    'J81': 'WEB-INF/src/com/torrent/surat/fms6/util/Menu_Bean1.java\nWEB-INF/src/com/torrent/surat/fms6/util/PurgeData.java\nWEB-INF/src/com/torrent/surat/fms6/util/RuntimeConf.java',
    'J82': 'WEB-INF/src/com/torrent/surat/fms6/util/SendMessage.java\nWEB-INF/src/com/torrent/surat/fms6/util/SessionVar.java\nWEB-INF/src/com/torrent/surat/fms6/util/SkyhookService.java',
    'J83': 'WEB-INF/src/com/torrent/surat/fms6/util/TeslaBadgeUtil.java\nWEB-INF/src/com/torrent/surat/fms6/util/UtilBean.java\nWEB-INF/src/com/torrent/surat/fms6/util/call_mail.java',
    'J84': 'WEB-INF/src/com/torrent/surat/fms6/util/escapeSingleQuotes.java\nWEB-INF/src/com/torrent/surat/fms6/util/fix_department.java\nWEB-INF/src/com/torrent/surat/fms6/util/mail.java',
    'J85': 'WEB-INF/src/com/torrent/surat/fms6/util/password_life.java\nWEB-INF/src/com/torrent/surat/fms6/util/password_policy.java\nWEB-INF/src/com/torrent/surat/fms6/util/send_timezone.java',
    'J86': 'WEB-INF/src/com/torrent/surat/fms6/util/send_updatepreop.java\nWEB-INF/src/com/torrent/surat/frms6/dao/BatteryDAO.java\nWEB-INF/src/com/torrent/surat/frms6/dao/DriverDAO.java',
    'J87': 'WEB-INF/src/com/torrent/surat/frms6/dao/DriverImportDAO.java\nWEB-INF/src/com/torrent/surat/frms6/dao/ImpactDAO.java\nWEB-INF/src/com/torrent/surat/frms6/dao/ImportDAO.java',
    'J88': 'WEB-INF/src/com/torrent/surat/frms6/dao/LockOutDAO.java\nWEB-INF/src/com/torrent/surat/frms6/dao/MessageDao.java\nWEB-INF/src/com/torrent/surat/frms6/dao/PreCheckDAO.java',
    'J89': 'WEB-INF/src/com/torrent/surat/frms6/dao/RegisterDAO.java\nWEB-INF/src/com/torrent/surat/frms6/dao/UnitDAO.java',
    'C01': 'Jenkinsfile\nWEB-INF/src/log4j.properties\nWEB-INF/src/log4j2.properties\nWEB-INF/urlrewrite.xml\nWEB-INF/web - Copy.xml\nWEB-INF/web.xml',
    'C02': 'WEB-INF/src/main/resource/Messages.properties\nWEB-INF/src/main/resource/Messages_en.properties\nWEB-INF/src/main/resource/Messages_en_US.properties\nWEB-INF/src/main/resource/Messages_es.properties\nWEB-INF/src/main/resource/Messages_zh.properties\nWEB-INF/src/main/resource/Messages_zh_CN.properties\nWEB-INF/taglibs-mailer.tld\nWEB-INF/taglibs-request.tld\npages/bundle/Messages.properties\npages/bundle/Messages_en.properties\npages/bundle/Messages_en_US.properties\npages/bundle/Messages_es.properties\npages/bundle/Messages_zh.properties\npages/bundle/Messages_zh_CN.properties',
    'S01': 'sql/FLEETIQ_AUG_2022.sql\nsql/FLEETIQ_JAN_2022.sql\nsql/FLEETIQ_JAN_2023.sql\nsql/FLEETIQ_JUN_2022.sql\nsql/FLEETIQ_MAR_2022.sql\nsql/FLEETIQ_MAY_2022.sql\nsql/FLEETIQ_NOV_2022.sql\nsql/FLEETIQ_SEPT_2022.sql',
    'S02': 'sql/check_firmware_idauth_driver_name.sql\nsql/disable_unit_preop_perday_perdriver.sql\nsql/equipment_bypass.sql\nsql/equipment_bypass_report.sql\nsql/pedestrian_detection.sql\nsql/sp_driver_shock_message.sql\nsql/sp_eos_message.sql',
    'S03': 'sql/sp_equipment_bypass_alert.sql\nsql/sp_get_driver_name.sql\nsql/sp_opchks_response.sql\nsql/sp_pstat_message.sql\nsql/sp_store_mk3dbg.sql\nsql/time_zone_impl.sql\nsql/time_zone_impl_varchar_int.sql',
}

template = (
    'Security audit agent {ID}. Repository: C:/Projects/cig-audit/repos/fleetiq. Branch: multi-customer-sync-to-master.\n'
    '1. Verify branch: run git -C "C:/Projects/cig-audit/repos/fleetiq" branch --show-current - must be multi-customer-sync-to-master. STOP if wrong.\n'
    '2. Read: C:/Projects/cig-audit/repos/fleetiq/audit/2026-03-01-01/pass1/AGENT-INSTRUCTIONS.md\n'
    '3. Read: C:/Projects/cig-audit/audit-skills/PASS1-CHECKLIST-ff-new.md\n'
    '4. Read EACH file IN FULL (paths relative to C:/Projects/cig-audit/repos/fleetiq/):\n'
    '{FILES}\n'
    '5. Produce reading evidence for every file FIRST, then review against all applicable checklist sections.\n'
    '6. Write output to: C:/Projects/cig-audit/repos/fleetiq/audit/2026-03-01-01/pass1/{ID}.md\n'
    'Report only - do NOT fix anything.'
)

for agent_id, files in agents.items():
    prompt = template.replace('{ID}', agent_id).replace('{FILES}', files)
    with open(os.path.join(OUT, agent_id + '.txt'), 'w') as f:
        f.write(prompt)

print(f'Created {len(agents)} prompt files in {OUT}')
