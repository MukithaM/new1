import sys
sys.path.append('..')

# System imports
import os
import re
import logging
from datetime import datetime
from datetime import timedelta
import argparse
from dateutil.relativedelta import relativedelta, SU
from jinja2 import Environment, FileSystemLoader

# Custom import
from Common import DatabaseSource as DB
from Common import CustomLogging as LOG
from Common import CustomEmail as MAIL
from Common import Config as CFG
import pandas as pd



parser = argparse.ArgumentParser()
parser.add_argument("--qgroup","-qgroup",
                    help='Qgroup for which report is to be prepared', default = None)

parser.add_argument("--emailList","-emailList",
                    help='Emails for which report is to be sent', default = None)

args = parser.parse_args()
print("Agrs:",parser.parse_args())
print("Qgroup:",args.qgroup)
print("emailList:",args.emailList)

class TestExecutionSummaryReport(object):
    def __init__(self):
        logName = CFG.testcaseExecutionReport['logName']
        LOG.TestcaseExecutionReportConfig(logName)
        self.log = logging.getLogger("TestcaseExecutionReport")
        self.mailObj = MAIL.SendEmail(self.log)
        self.employeeExecutionDict = dict()
        self.toEmails = CFG.testcaseExecutionReport['globalEmailList']

    def GetFromToDates(self):
        self.weeksRange = CFG.testcaseExecutionReport['dayCount']
        weeks = list()
        today = datetime.now()
        for i in range(0, self.weeksRange):
            dayDict = dict()
            day = today - relativedelta(days=i)
            dayDict['from'] = day.strftime("%Y-%m-%d") + ' 00:00:00:000'
            dayDict['to'] = day.strftime("%Y-%m-%d") + ' 23:59:59:999'
            dayDict['str'] = day.strftime("%m/%d")
            weeks.append(dayDict)
        self.weeks = weeks
        print(weeks)
        return weeks

    def GenerateManagerwiseEmployeeInfo(self):
        #get Perf team managers only
        managerList = {'All GEOs': {}}
        
        if args.emailList is None:
            self.toEmails = list(filter(None, args.qgroup.split(',')))
        else:
            self.toEmails = list(filter(None, args.emailList.split(',')))

        overallEmployeeDict = { 'All GEOs':{'details':{}}}

        self.odsObj = DB.Ods(self.log)

        for geo in managerList:
           
            overallEmployeeDict[geo]['details'][args.qgroup] = dict()

            managerInfo = overallEmployeeDict[geo]['details'][args.qgroup]                

            # Getting the list of employees under supervisor 
            empRes = self.odsObj.GetEmpInfoByQgroup(args.qgroup)
            if len(empRes) > 0:
                for res in empRes:
                    if res.Uid not in managerInfo:
                        managerInfo[res.EmployeeName] = dict()

                    empInfo = managerInfo[res.EmployeeName]

                    empInfo['Uid'] = res.Uid

        self.odsObj.Close()
        
        return overallEmployeeDict

    def GenerateWeeklyExecutionSummary(self, fromDate, toDate):

        self.qlasrObj = DB.Qlasr(self.log)
        qlasrResult = self.qlasrObj.A(fromDate,toDate)
        self.qlasrObj.Close()
        nodemasterid_set=set()  
        for row in qlasrResult:
            nodemasterid_set.add(row.NodeMasterId)

        nodemasterid_set=','.join(str(id) for id in nodemasterid_set)
        print(nodemasterid_set)
        self.qlasrObj = DB.Qlasr(self.log)
        qlasrpastresult = self.qlasrObj.B(nodemasterid_set,fromDate)
        self.qlasrObj.Close()
        
        # PreviousResults=self.qlasrObj.GetPreviousResults(nodemasterid_set)
        previous_result_dict={}
        for row in qlasrpastresult:
                key=f"{row.NodeMasterId}_{row.TestplanMasterId}_{row.TestcaseMasterId}"  
                previous_result_dict[key]=True
        for k,v in previous_result_dict.items():
            print(f"key:{k},Value:{v}")
                


        # Iterating the qlasr execution details and identifying the total per engineer
        for row in qlasrResult:
            if row.LastModifiedBy != None :
                testerName = row.LastModifiedBy
            elif row.RequestedBy != None :
                testerName = row.RequestedBy
            elif row.TesterID != None :
                testerName = re.sub(r'^(ap|na)\\', '', row.TesterID.lower())
            elif row.UserDomain != None :
                testerName = re.sub(r'^(ap|na)\\', '', row.UserDomain.lower())
            else:
                testerName = 'others'

            # Adding project execution information if its only required
            if True:
                if((row.ProjectRoot == None) or (row.ProjectRoot == "")):
                    project = 'Others'
                else:
                    project = row.ProjectRoot

                    if row.ProjectName:
                        milestone = row.ProjectName.split('->')[1]
                        project += f' - {milestone}'


    def GenerateOverallExectionSummary(self, overallEmployeeDict):

        # Generate the Employee Execution summary based on Geo & Supervisor list avaialble in Config file
        for empGeo in overallEmployeeDict:
            if 'projects' not in overallEmployeeDict[empGeo]:
                overallEmployeeDict[empGeo]['projects'] = dict()
            
            projectDict = overallEmployeeDict[empGeo]['projects']
            detailDict = overallEmployeeDict[empGeo]['details']
            for manager in detailDict:
                for empName in detailDict[manager]:
                    empUid = detailDict[manager][empName]['Uid']

                    empInfo = detailDict[manager][empName]
                    if empUid in self.employeeExecutionDict:
                        empInfo.update(self.employeeExecutionDict[empUid])

                        if 'projectInfo' not in empInfo:
                            empInfo['projectInfo'] = dict()

                        empProjectDict = empInfo['projectInfo']

                        #Iterate all week data and generate overall summary detail for CDC for first week
                        for week in range(1, self.weeksRange + 1):
                            if week in self.employeeExecutionDict[empUid] and len(self.employeeExecutionDict[empUid][week]['projectInfo']) > 0:
                                for projectData in self.employeeExecutionDict[empUid][week]['projectInfo']:
                                    if projectData not in projectDict:
                                        projectDict[projectData]= 0
                                    if projectData not in empProjectDict:
                                        empProjectDict[projectData] = 0

                                    projectDict[projectData] += self.employeeExecutionDict[empUid][week]['projectInfo'][projectData]
                                    empProjectDict[projectData] += self.employeeExecutionDict[empUid][week]['projectInfo'][projectData]

                        # Removing the employee execution information after updating it the overall dict 
                        del self.employeeExecutionDict[empUid]

        return overallEmployeeDict

    def SendReport(self, overallDict, fromDate, toDate):
        templateDir = CFG.emailReport['templates']
        env = Environment(loader=FileSystemLoader(templateDir))
        template = env.get_template("dayWiseReportTemplateWithQgroup.html")

        reportTitle = f'Testcase Execution Report - {args.qgroup}'
        emailSubject = '{0} - Date ({1})'.format(reportTitle, fromDate.split()[0])
        template_vars = {
            "title" : reportTitle,
            "overallData": overallDict,
            "weeksRange": self.weeksRange,
            "hideManagerColumn": True,
            "weeks": self.weeks[::-1]
        }
        htmlOut = template.render(template_vars)
        f = open("templates\\generated.html","w", encoding="utf-8")
        f.write(htmlOut)
        print(template_vars)
        sys.exit()
        

        # emailContent = {
        #     'Subject' :  emailSubject,
        #     'FromEmail' : CFG.testcaseExecutionReport['fromEmail'],
        #     'ToEmails' : self.toEmails,
        #     'ReportContent' : htmlOut
        # }

        # self.mailObj.sendEmail(emailContent)

if __name__ == "__main__":
    # Creating the object for generating the summary report
    Report = TestExecutionSummaryReport()
    
    # Construct Managerwise employee dict
    # overallEmployeeDict = Report.GenerateManagerwiseEmployeeInfo()

    # Getting the list of weeks with start date and end date
    weeks = Report.GetFromToDates()

    # for weekIndex, weekData in enumerate(weeks):
    #     isProjectReq =  True if(weekIndex == 0) else False
    #     # Getting the execution details per week from QLASR DB
    #     Report.GenerateWeeklyExecutionSummary(weekData['from'], weekData['to'], isProjectReq, weekIndex + 1)
    Report.GenerateWeeklyExecutionSummary(weeks[-1]['from'], weeks[0]['to'])

    # Constructing the overall dict to required for generating the EMAIL Report
    overallResult = Report.GenerateOverallExectionSummary(overallEmployeeDict)

    # sending overall report
    Report.SendReport(overallResult, weeks[0]['from'], weeks[0]['to'])
