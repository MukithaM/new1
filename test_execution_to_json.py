
import sys
import os
import re
import logging
import argparse
import json
import pandas as pd
from datetime import datetime
from collections import defaultdict
from Common import DatabaseSource as DB
from Common import CustomLogging as LOG
from Common import Config as CFG

parser = argparse.ArgumentParser()
parser.add_argument("--qgroup", "-qgroup", help="Qgroup for which report is to be prepared", default=None)
parser.add_argument("--saveJson", "-saveJson", help="File path to save output JSON", default="testcase_output.json")
args = parser.parse_args()

class TestExecutionJSONExtractor:
    def __init__(self):
        logName = CFG.testcaseExecutionReport['logName']
        LOG.TestcaseExecutionReportConfig(logName)
        self.log = logging.getLogger("TestcaseExecutionReport")
        self.qlasrObj = DB.Qlasr(self.log)

    def execute_and_process(self):
        today = datetime.now()
        from_date = (today - pd.Timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
        to_date = today.strftime("%Y-%m-%d %H:%M:%S")

        # Query A (last 7 days)
        query_a_results = self.qlasrObj.A(from_date, to_date)
        nodemasterid_set = set(row.NodeMasterId for row in query_a_results)

        # Query B (older than 7 days)
        nodemasterid_csv = ",".join(str(i) for i in nodemasterid_set)
        query_b_results = self.qlasrObj.B(nodemasterid_csv, from_date)
        self.qlasrObj.Close()

        # Process both results into JSON
        json_result = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: {"TR": [], "RV": []})))

        for row in query_a_results:
            try:
                project = row.ProjectName
                testplan = row.TestPlanName
                date = row.StartTime.strftime("%Y-%m-%d")
                testcase_id = row.TestcaseMasterId
                if row.Result in ("Passed", "Failed"):
                    json_result[project][testplan][date]["TR"].append({"p": testcase_id})
            except Exception as e:
                self.log.error(f"Error processing Query A row: {e}")

        for row in query_b_results:
            try:
                project = "Historical_Results"
                testplan = "Historical"
                date = "OlderThan7Days"
                testcase_id = row.TestcaseMasterId
                if row.Result in ("Passed", "Failed"):
                    json_result[project][testplan][date]["RV"].append({"p": testcase_id})
            except Exception as e:
                self.log.error(f"Error processing Query B row: {e}")

        # Convert to regular dict and save
        output_dict = json.loads(json.dumps(json_result, indent=2))
        with open(args.saveJson, "w") as f:
            json.dump(output_dict, f, indent=2)
        print(f"JSON output saved to {args.saveJson}")

if __name__ == "__main__":
    extractor = TestExecutionJSONExtractor()
    extractor.execute_and_process()
