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
from dateutil.relativedelta import relativedelta, SU
from jinja2 import Environment, FileSystemLoader


# Custom import
from Common import DatabaseSource as DB
from Common import CustomLogging as LOG
from Common import CustomEmail as MAIL
from Common import Config as CFG
import pandas as pd
from collections import defaultdict
from datetime import datetime



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
        # print(qlasrpastresult)
        self.qlasrObj.Close()
        
      
        
        previous_result_dict={}
        for row in qlasrpastresult:
                key=f"{row.NodeMasterId}_{row.TestplanMasterId}_{row.TestcaseMasterId}"  
                previous_result_dict[key]=True
        for k,v in previous_result_dict.items():
            print(f"key:{k},Value:{v}")
    
        # Iterating the qlasr execution details and identifying the total per engineer
html use key words this coding:
        project_dict=defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:{"NewRun":{'pass':0,'Fail':0},'Revalidation':{'pass':0,'Fail':0}})))
        for row in qlasrResult:
            project_name=row.ProjectName
            tester=row.LastModifiedBy 
            date=row.TestStartTime.date().isoformat() if row.TestStartTime else "unknownDate"
            run_type="NewRun" if "NR" in row.TestPlanName else "Revalidation"
            result=getattr(row,"result","").strip().lower()
            result=result if result in ['pass','Fail'] else 'Fail'
            project_dict[project_name][tester][date][run_type][result] += 1
        print(json.dumps(project_dict,indent=4))


new code:26/05/25
start 
        all_dates = set()
        for date_data in project_dict.values():
                all_dates.update(date_data.keys())
        sorted_dates = sorted(date for date in all_dates if date is not None)        

        html="""
        <html>
        <head>
        <title>Test Execution Summary</title>
        <style>
        table{
            border-collapse:collapse; with:100%;
            th,td {border:1px solid #999; padding:8px; text-align:center;}
            th{background-color:#f2f2f2;}
        </style> 
        </head>
        <h2>Test Execution Summary</h2>
        <table>
        <tr>
        <th>Employee </th>
        <th>Total</th>
        }"""
        
        for date in sorted_dates:
            html += f"<th colspan='4'>{date}</th>"
        html +="<tr>\n<tr><td></td><td></td>"
        for  _ in sorted_dates:
            html +="<td>NewRun Pass</td><td>NewRun Fail</td><td>Revalidation Pass</td><td>Revalidation Fail</td>"
        html += "</tr>\n"
        for project_name,date_data in project_dict.items():
            total_exec=0
            row_html=f"<tr><td>{project_name}</td>"
            row_data=[]
            for date in sorted_dates:
                run_type=date_data.get(date,{"NewRun":{"Pass":0,"Fail":0},"Revalidation":{"Pass":0,"fail":0}})
                np=run_type["NewRun"].get["Pass",0]
                nf=run_type["NewRun"].get["Fail",0]
                rp=run_type["Revalidation"].get["Pass",0]
                rf=run_type["Revalidation"].get["Fail",0]
                total_exec +=(np+nf+rp+rf)
                row_data.extend([np,nf,rp,rf])
            row_html +=f"<td>{total_exec}</td>"
            for val in row_data:
                row_html +=f"<td>{val}</td>"
            row_html +="</tr>\n" 
            html += row_html
            html += """ 
            </table>
            </body>
            </html>"""
            with open("templates\\generated.html","w")as file:
                file.write(html)  
            print(project_dict)    

end 
        # for project_name,tester in project_dict.items():
        #     for tester,date in tester.items():
        #         total=0
        #         row_html=f"<tr><td>{tester}</td>"
        #         date_values=[]
        #         for date in sorted_dates:
        #             for run_type,result in run_type.items():
        #                 run_type=date.get(date,{"NewRun":{"Pass":0,"Fail":0},"Revalidation":{"Pass":0,"fail":0}})
        #                 np=run_type["NewRun"]["Pass"],
        #                 nf=run_type["NewRun"]["Fail"]
        #                 rp=run_type["Revalidation"]["Pass"],
        #                 rf=run_type["Revalidation"]["Fail"]
        #                 total +=(np + nf + rp + rf)
        #                 date_values.extend([np,nf,rp,rf])
        #         row_html += f"<td>{total}</td>" 
        #         row_html += "".join([f"<td>{v}</td>" for v in date_values])  
        #         row_html +="</tr>"
        #         html += row_html
        # html += "</table></body></html>"
        # with open("templates\\generated.html","w")as file:
        #     file.write(html)  
        # print(project_dict)          
        # html_ouput=""    
        # for project_name, tester in project_dict.items():
        #         for tester,date in tester.items():
        #             for date,run_type in date.items():
        #                 for run_type,result in run_type.items():
        #                     pass_count=result.get("pass",0)
        #                     fail_count=result.get("fail",0)
        #                     html_ouput += f"""
        #             <tr> 
        #                 <td>{project_name}</td>
        #                 <td>{tester}</td>
        #                 <td>{date}</td>
        #                 <td>{run_type}</td>
        #                 <td>{pass_count}</td>
        #                 <td>{fail_count}</td>
        #             </tr>   
        #                 """
        # html_ouput +="</table></body></html>" 
        # with open("templates\\generated.html","w")as f:
        #     f.write(html_ouput)
        


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
