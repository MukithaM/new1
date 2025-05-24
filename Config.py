Config.py

# BEGIN Credentials
import os

cstAutoDb = {
    'dsn' : 'WIN_CST_AUTO_ServerDatasource',
    'username': 'AP\\wincstauto',
    'password': 'Cdccoredev123#',
    'database': 'WIN_CST_AUTO',
}

odsDb = {
    'dsn': 'ODSServerDatasource',
    'username': 'AP\\wincstauto',
    'password': 'Cdccoredev123#',
    'database': 'ODS',
}

qlasrDb = {
    'dsn': 'QLASRServerDatasource',
    'username': 'AP\\qiplcst',
    'password': 'cQualcomm$123456c',
    'database': 'QCA_RPT',
    'hostname': 'QCASQLPRD2',
    'driver': 'pymssql'
}

orbitPostAPI = {
    'domain': 'orbit',
    'appsource': 'bugspot',
    'username': 'swat',
    'password': 'b(OI@g1g4wV119aI',
    # 'password': 'w&?nV91~g?Im6e-V',
    'realm': 'AP.QUALCOMM.COM',
}

hostWinCst = {
    'userId': 'wincstauto',
    'hostname' : 'WINCSTDDEV',
    'QSPRhostname' : 'WINCSTDDEV',
}

# END Credentials

# BEGIN Daemon config
qlasrSync = {
    'logDir': 'C:\\CSTDLogs\\QlasrSyncLogs',
    'logDirCrSync': 'C:\\CSTDLogs\\QlasrCrSyncLogs',
    'logName': 'QlasrSync',
    # 'syncThreshold': 30,  # in minutes
    # 'crSyncThreshold': 45,  # in minutes
}

projectSync = {
    'logDir': 'C:\\CSTDLogs\\ProjectSyncLogs',
    'logName': 'ProjectSync',
}

testplanTestcase = {
    'logDir': 'C:\\CSTDLogs\\TestplanTestcaseLogs',
    'logName': 'TestplanTestcase',
    'patterns': [
        "(.*tcp.*)|(.*udp.*)|(.*cpu.*)|(.*throughput.*)|(.*uplink.*)|(.*downlink.*)|(.*notes.*)|(.*jitter.*)|(.*latency.*)",
        "(.*Tput.*)|(.*memory.*)|(.*ram.*)|(.*througput.*)|(.*validation.*)|(.*ping.*)|(.*stream.*)|(.*count.*)|(.*rate.*)",
        "(.*cac.*)|(.*rssi.*)|(.*percent.*)|(.*associate.*)|(.*attenuation.*)|(.*flow.*)|(.*mcs.*)|(.*pkts.*)"
    ],
}

testplanTestcaseHistory = {
    'logDir': 'C:\\CSTDLogs\\TestplanTestcaseHistoryLogs',
    'logName': 'TestplanTestcaseHistory',
}

resultManager = {
    'logDir': 'C:\\CSTDLogs\\ResultDaemonLogs',
    'logName': 'ResultManager',
}

processing = {
    'logDir': 'C:\\CSTDLogs\\ResultDaemonLogs',
    'logName': 'Processing',
    'MinFailEmailTime': 30,  # in minutes
}

scheduling = {
    'logDir': 'C:\\CSTDLogs\\ResultDaemonLogs',
    'logName': 'Scheduling',
    'MinFailEmailTime': 30,  # in minutes
}

modifyResults = {
    'logDir': 'C:\\CSTDLogs\\ResultDaemonLogs',
    'logName': 'ModifyResults',
    'MinFailEmailTime': 30,  # in minutes
    'RequestHoldTime': 5,  # in minutes
    'replaceCharacters': ["–", "-"],
}

checkResultUpdate = {
    'logDir': 'C:\\CSTDLogs\\ResultDaemonLogs',
    'logName': 'CheckResults',
    'ExecutionInterval': 360,  # in minutes
    'MaxRequestAge': 720,  # in minutes
}

triggerManager = {
    'logDir': 'C:\\CSTDLogs\\TriggerManagerDaemonLogs',
    'logName': 'TriggerManager',
    'AutoSchedulerExecutionInterval': 15,    # in minutes
    'MonitorExecutionInterval': 5,    # in minutes
}

scheduler = {
    'logDir': 'C:\\CSTDLogs\\SchedulerDaemonLogs',
    'logName': 'Scheduler',
    'AutoSchedulerExecutionInterval': 10,    # in minutes
    'MonitorExecutionInterval': 5,    # in minutes
    'TestbedInfoUpdaterInterval': 720,    # in minutes
}

syncMilestoneTAReportInfo = {
    'logDir': 'C:\\CSTDLogs\\SyncMilestoneTAReportInfoLogs',
    'logName': 'SyncMilestoneTAReportInfo'
}


# Auto Triage Log configs 

autoTriage = {
    'apiHost': 'wincstddev',
    'logDir': 'C:\\CSTDLogs\\AutoTriageLogs',
    'logName': 'AutoTriage',
    'templates': 'templates',
    'fromEmail': "cst_reports@qualcomm.com",
    'globalEmailList': ["cdc.cst.devpool.sanity@qti.qualcomm.com", "win_cst_dashboard_admin@qti.qualcomm.com"],
    # 'globalEmailList': ["rubaeshk@qti.qualcomm.com"],
    'subLogs' : {
        'getInitialRun' : {
            'logDir': 'C:\\CSTDLogs\\AutoTriageLogs',
            'logName': 'GetInitialRun',
        },
        'requeueInitialRun' : {
            'logDir': 'C:\\CSTDLogs\\AutoTriageLogs',
            'logName': 'RequeueInitialRun',
        },
        'compareInitialRun' : {
            'logDir': 'C:\\CSTDLogs\\AutoTriageLogs',
            'logName': 'CompareInitialRun',
        },
        'compareRetry' : {
            'logDir': 'C:\\CSTDLogs\\AutoTriageLogs',
            'logName': 'CompareRetry',
        },                        
        'compareRetryOnReference' : {
            'logDir': 'C:\\CSTDLogs\\AutoTriageLogs',
            'logName': 'CompareRetryOnReference',
        },        
        'reportMail' : {
            'logDir': 'C:\\CSTDLogs\\AutoTriageLogs',
            'logName': 'ReportMail',
        },
        'progressMail' : {
            'logDir': 'C:\\CSTDLogs\\AutoTriageLogs',
            'logName': 'ProgressMail',
        }
    }     
}

# END Auto Triage Log configs 

autoScheduler = {
    'logDir': 'C:\\CSTDLogs\\SchedulerDaemonLogs',
    'logName': 'AutoScheduler',
    'MinFailEmailTime': 30,  # in minutes
}

qlasrTrigger = {
    'logDir': 'C:\\CSTDLogs\\SchedulerDaemonLogs',
    'logName': 'QlasrTrigger',
    'MinFailEmailTime': 30,  # in minutes
}

testTrigger = {
    'logDir': 'C:\\CSTDLogs\\SchedulerDaemonLogs',
    'logName': 'TestTrigger',
    'MinFailEmailTime': 30,  # in minutes
}

trigger = {
    'logDir': 'C:\\CSTDLogs\\SchedulerDaemonLogs',
    'logName': 'Trigger',
    'MinFailEmailTime': 30,  # in minutes
}

monitor = {
    'logDir': 'C:\\CSTDLogs\\SchedulerDaemonLogs',
    'logName': 'Monitor',
    'MinFailEmailTime': 30,  # in minutes
}

testbedInfoUpdater = {
    'logDir': 'C:\\CSTDLogs\\SchedulerDaemonLogs',
    'logName': 'TestbedInfoUpdater',
    'MinFailEmailTime': 30,  # in minutes
}

emailReport = {
    'logDir': 'C:\\CSTDLogs\\EmailReportLogs',
    'logName': 'EmailReport',
    'templates': 'templates',
    'tempDir': 'temp',
    'networkShare': r'\\winter\swat\QSPR\CSTReports\ResultsExcel',
    'cstDashboardBaseUrl': 'http://wincstd/project/',
    'fromEmail': "cst_reports@qualcomm.com",
    'globalEmailList': ["CNSS.CST.CDC.ALL@qti.qualcomm.com"]
}

testcaseExecutionReport = {
    'logDir': 'C:\\CSTDLogs\\EmailReportLogs',
    'logName': 'TestcaseExecuted',
    'templates': 'templates',
    'tempDir': 'temp',
    'weekCount': 4,
    'dayCount': 7,
    'networkShare': r'\\winter\swat\QSPR\CSTReports\TestExecutionExcel',
    'fromEmail': "cst_reports@qualcomm.com",
    'globalEmailList': ["CDC.CST.Staff@qti.qualcomm.com", "arunach@qti.qualcomm.com"]
}
devPoolReport = {
    'logDir': 'C:\\CSTDLogs\\DevPoolReportLogs',
    'logName': 'DevPoolReport',
    'templates': 'templates',
    'tempDir': 'temp',
    'networkShare': r'\\winter\CBU-SPE\CSTDashboard\Reports',
    'fromEmail': "cst_reports@qualcomm.com",
    'globalEmailList': ["cdc_devpool_poc@qti.qualcomm.com"]
}
TestplanAutomationUpdateReport = {
    'logDir': 'C:\\CSTDLogs\\TestplanAutomationUpdateReportLogs',
    'logName': 'TestplanAutomationUpdateReport',
    'templates': 'templates',
    'tempDir': 'temp',
    'networkShare': r'\\winter\swat\QSPR\CSTReports\UpdateReports',
    'fromEmail': "cst_reports@qualcomm.com",
    'globalEmailList': ["cst.cdc.systemtest.leads@qti.qualcomm.com"]
}


MissingCRReport = {
    'logDir': 'C:\\CSTDLogs\\MissingCRReportLogs',
    'logName': 'MissingCRReport',
    'templates': 'templates',
    'fromEmail': "cst_reports@qualcomm.com",
    'CcEmails' : ["CDC.CST.Staff@qti.qualcomm.com"]
}

ResultManagerDeletion = {
    'logDir': 'C:\\CSTDLogs\\ResultManagerDeletion',
    'logName': 'ResultManagerDeletion',
    'templates': 'templates',
    'fromEmail': "cst_reports@qualcomm.com",
    'CcEmails' : ["CDC.CST.Staff@qti.qualcomm.com"]
}

CstExecutionMetrics = {
    'logDir': 'C:\\CSTDLogs\\CstExecutionMetrics',
    'logName': 'CstExecutionMetrics',
    'templates': 'templates',
    'fromEmail': "cst_reports@qualcomm.com",
    'CcEmails' : ["CDC.CST.Staff@qti.qualcomm.com"]
}

DaemonMonitorReport = {
    'logDir': 'C:\\CSTDLogs\\DaemonMonitorReport',
    'logName': 'DaemonMonitorReport',
    'templates': 'templates',
    'fromEmail': "cst_reports@qualcomm.com",
    'globalEmailList': ["win_cst_dashboard_admin@qti.qualcomm.com"],
}

NewReleaseAutomationSummary = {
    'logDir': 'C:\\CSTDLogs\\NewReleaseAutomationSummaryLogs',
    'logName': 'NewReleaseAutomationSummary',
    'templates': 'templates',
    'tempDir': 'temp',
    'networkShare': r'\\winter\swat\QSPR\CSTReports\NewReleaseAutomationSummary',
    'fromEmail': "cst_reports@qualcomm.com",
    'globalEmailList': ["CDC.CST.Staff@qti.qualcomm.com","WIN.SJ.CST.Automation@qti.qualcomm.com"]
}

fwMainlineReport = {
    'logDir': 'C:\\CSTDLogs\\FwMainlineReportLogs',
    'logName': 'FwMainlineReport',
    'templates': 'templates',
    'tempDir': 'temp',
    'fromEmail': "cst_reports@qualcomm.com",
    'globalEmailList': ["rubaeshk@qti.qualcomm.com", "lpalanic@qti.qualcomm.com", "jyoganat@qti.qualcomm.com"]    
}

managers = {
    'cdc':{
        '32591': 'Abhiroop Mitra',
        '32747': 'Ajith Raj Kumar',
        '101459': 'Anand Lakshmanan',
        '32970': 'Antony Thomas',
        '101819': 'Aruna Sree Chereddy',
        '122325': 'Chintan Bhoot',
        '36220': 'Deepa Jayaraman',
        '104468': 'Jagatheesan Prabakaran',
        '111755': 'Janardhana Babu Parthasarathy',
        '118777': 'Johnu Jose',
        '109059': 'Karthikeyan Nagarajan',
        '32273': 'Kavitha Krishnamurthy',
        '32670': 'Kesavamurthy Palani',
        '32671': 'LakshmiNarayanan Palanichandran',
        '31617': 'Loganathan Arumugam',
        '121041': 'Manikandan (Manikandan M) Mohan',
        '32607': 'Nagarajan Murugesan',
        '32796': 'Nataraj Sadasivam',
        '31660': 'Pradeep Bojan',
        '105156': 'Pradheep Manokaran',
        '39191': 'Prakash Chennichetty',
        '32748': 'Sasikumar Rajagopal',
        '23849': 'Shilpa Pantula',
        '32719': 'Vadivel Pichaimani',
        '30013': 'Vani Pichikala',
        '32874': 'Vishnuvarthan Sivaramakrishnan',
        '122913': 'Yuvaraj Sudharsanan',
        '122638': 'Arun Thupati'

        # '32591': 'Abhiroop Mitra',
        # '32747': 'Ajith Raj Kumar',
        # '32970': 'Antony Thomas',
        # '101819': 'Aruna Sree Chereddy',
        # '36220': 'Deepa Jayaraman',
        # '124053': 'Dhivya Sakthivel',
        # '111755': 'Janardhana Babu Parthasarathy',
        # '32671': 'LakshmiNarayanan Palanichandran',
        # '31617': 'Loganathan Arumugam',
        # '32607': 'Nagarajan Murugesan',
        # '32796': 'Nataraj Sadasivam',
        # '31660': 'Pradeep Bojan',
        # '32748': 'Sasikumar Rajagopal',
        # '101603': 'Subramanian Anantharaman',
        # '21768': 'Suhaib Ahmed Malyalam Shakeel',
        # '32719': 'Vadivel Pichaimani'
    },
    'sjo':{
        '32668': 'Jeevan Padmaraju',
        '32596': 'Leonardo Monterola',
        '110952': 'Ruiqing Ye',
        '104314': 'Song Han'        
    }
}


managersTeamWise = {
    'performance': {
        'managers': {'32747', '111755', '32796'},
        'toEmails': ['CDC.CST.Performance@qti.qualcomm.com']
    },
    'functional': {
        'managers': {'36220', '122325', '32537', '32719'},
        'toEmails': ['tjeyacha@qti.qualcomm.com']
    }
}

daemonMonitor = {
    'logDir': 'C:\\CSTDLogs\\DaemonMonitorLogs',
    'logName': 'DaemonMonitor',
}

testbedUtilizationReport = {
    'logDir': 'C:\\CSTDLogs\\TestbedUtilizationReportLogs',
    'logName': 'TestbedUtilizationReport',
    'templates': 'templates',
    'tempDir': 'temp',
    'weekCount': 4,
    'fromEmail': "win_auto_tools@qti.qualcomm.com",
    'globalEmailList': ["win.sj.cst.all@qti.qualcomm.com"]
}

# END Daemon config

# BEGIN General config
url = {
    'qlasr': 'http://ctdsapi1:8100/',
    'qlasrTp': 'http://ctdsapi1:90/',
    'cstDashboard': 'http://WINCSTDDEV/',
    'webServerCstDashboard': 'http://WINCSTD/',
    'cstWebSd': 'http://cstwebsd/ticketingservice/',
    'qlasrQca': 'http://qcacst-qlasr2:1024/',
    'orbitPost': 'https://orbit-sd/',
}

sendEmail = {
    'senderEmail': 'wincstauto@qti.qualcomm.com',
    'serverEmail': 'smtphost.qualcomm.com',
    'adminEmail': 'win_cst_dashboard_admin@qti.qualcomm.com',
}

hostInfo = {
    'CHECSTP227040' : {
        'env' : 'Local'
    },
    'WINCSTDEV' : {
        'env' : 'Test'
    },
    'WINCSTDDEV' : {
        'env' : 'Prod - Daemon'
    },
    'WINCSTD' : {
        'env' : 'Prod - Web'
    }
}
# END General config

# BEGIN DaemonMonitor Config
appMonitor = [
    {
        'type': 'APP',
        'taskName': 'python.exe',
        'executable': os.path.join('C:\\Program Files\\Python37', 'python.exe'),
        'workingDir': 'C:\\CST_Dashboard\\Daemon\\ResultManagerDaemon',
        'args': 'C:\\CST_Dashboard\\Daemon\\ResultManagerDaemon\\resultDaemon.py',
    },
    {
        'type': 'APP',
        'taskName': 'QLASRClientExe.exe',
        'executable': os.path.join('C:\\CST_QSPR\\main\\bin', 'QLASRClientStartup.bat'),
        'workingDir': 'C:\\CST_QSPR\\main\\bin',
    },
    {
        'type': 'LOG',
        'logName': testplanTestcase["logName"],
        'logDir': testplanTestcase["logDir"],
        'logSyncTime': 360,  # in minutes
    },
    {
        'type': 'LOG',
        'logName': qlasrSync["logName"],
        'logDir': qlasrSync["logDir"],
        'logSyncTime': 180,  # in minutes
    },
]
# END DaemonMonitor Config

