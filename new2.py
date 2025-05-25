import sys
sys.path.append('..')

# System imports
import os
import re
import logging
from datetime import datetime
from datetime import timedelta
import argparse
import json
from dateutil.relativedelta import relativedelta
from jinja2 import Environment, FileSystemLoader

# Custom import
from Common import DatabaseSource as DB
from Common import CustomLogging as LOG
from Common import CustomEmail as MAIL
from Common import Config as CFG
import pandas as pd
from collections import defaultdict

# Optional CLI (no required args)
parser = argparse.ArgumentParser()
parser.add_argument("--qgroup", "-qgroup", help="Qgroup for which report is to be prepared", default=None)
parser.add_argument("--emailList", "-emailList", help="Emails to send the report to", default=None)
args = parser.parse_args()

class TestExecutionSummaryReport(object):
    def __init__(self):
        logName = CFG.testcaseExecutionReport['logName']
        LOG.TestcaseExecutionReportConfig(logName)
        self.log = logging.getLogger("TestcaseExecutionReport")
        self.mailObj = MAIL.SendEmail(self.log)
        self.employeeExecutionDict = dict()
        self.executionSummary = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: {"TR": [], "RV": []})))

        self.qgroup = args.qgroup or CFG.testcaseExecutionReport.get("defaultQgroup", "DefaultQgroup")
        self.toEmails = CFG.testcaseExecutionReport['globalEmailList']
        if args.emailList:
            self.toEmails = list(filter(None, args.emailList.split(',')))

    def GetFromToDates(self):
        self.weeksRange = CFG.testcaseExecutionReport['dayCount']
        weeks = []
        today = datetime.now()
        for i in range(self.weeksRange):
            day = today - relativedelta(days=i)
            weeks.append({
                'from': day.strftime("%Y-%m-%d") + ' 00:00:00:000',
                'to': day.strftime("%Y-%m-%d") + ' 23:59:59:999',
                'str': day.strftime("%m/%d")
            })
        self.weeks = weeks
        return weeks

    def GenerateWeeklyExecutionSummary(self, fromDate, toDate):
        # Query A (last 7 days)
        self.qlasrObj = DB.Qlasr(self.log)
        qlasrResult = self.qlasrObj.A(fromDate, toDate)
        self.qlasrObj.Close()

        nodemasterid_set = set(row.NodeMasterId for row in qlasrResult)
        nodemasterid_csv = ",".join(str(i) for i in nodemasterid_set)

        # Query B (older)
        self.qlasrObj = DB.Qlasr(self.log)
        qlasrpastresult = self.qlasrObj.B(nodemasterid_csv, fromDate)
        self.qlasrObj.Close()

        # Process Query B (RV)
        for row in qlasrpastresult:
            try:
                self.executionSummary["Historical_Results"]["Historical"]["OlderThan7Days"]["RV"].append(
                    {"p": row.TestcaseMasterId}
                )
            except Exception as e:
                self.log.error(f"Error processing Query B row: {e}")

        # Process Query A (TR)
        for row in qlasrResult:
            try:
                project = row.ProjectName or "Unknown"
                testplan = row.TestPlanName or "Unknown"
                date = pd.to_datetime(row.StartTime).strftime('%Y-%m-%d')
                if row.Result in ("Passed", "Failed"):
                    self.executionSummary[project][testplan][date]["TR"].append({"p": row.TestcaseMasterId})
            except Exception as e:
                self.log.error(f"Error processing Query A row: {e}")

        # Output summary for debug
        print(json.dumps(self.executionSummary, indent=2))

    def GenerateManagerwiseEmployeeInfo(self):
        overallEmployeeDict = { 'All GEOs':{'details':{}}}
        self.odsObj = DB.Ods(self.log)

        overallEmployeeDict['All GEOs']['details'][self.qgroup] = {}
        managerInfo = overallEmployeeDict['All GEOs']['details'][self.qgroup]

        empRes = self.odsObj.GetEmpInfoByQgroup(self.qgroup)
        for res in empRes:
            if res.Uid not in managerInfo:
                managerInfo[res.EmployeeName] = {'Uid': res.Uid}

        self.odsObj.Close()
        return overallEmployeeDict

    def GenerateOverallExectionSummary(self, overallEmployeeDict):
        return overallEmployeeDict  # Stubbed logic

    def SendReport(self, overallDict, fromDate, toDate):
        templateDir = CFG.emailReport['templates']
        env = Environment(loader=FileSystemLoader(templateDir))
        template = env.get_template("dayWiseReportTemplateWithQgroup.html")

        reportTitle = f'Testcase Execution Report - {self.qgroup}'
        emailSubject = f"{reportTitle} - Date ({fromDate.split()[0]})"

        template_vars = {
            "title": reportTitle,
            "overallData": overallDict,
            "weeksRange": self.weeksRange,
            "hideManagerColumn": True,
            "weeks": self.weeks[::-1]
        }

        with open("templates/generated.html", "w", encoding="utf-8") as f:
            f.write(template.render(template_vars))

        print(f"✅ Report rendered and saved as HTML.")
        print(json.dumps(template_vars, indent=2))

if __name__ == "__main__":
    Report = TestExecutionSummaryReport()
    weeks = Report.GetFromToDates()
    Report.GenerateWeeklyExecutionSummary(weeks[-1]['from'], weeks[0]['to'])
    overallEmployeeDict = Report.GenerateManagerwiseEmployeeInfo()
    overallResult = Report.GenerateOverallExectionSummary(overallEmployeeDict)
    Report.SendReport(overallResult, weeks[0]['from'], weeks[0]['to'])
