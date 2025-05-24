
Query-A
SELECT Node.NodeMasterID as NodeMasterId, TestplanVersion.MasterTPRID as TestplanMasterId, TestcaseVersion.TCMasterRID as TestcaseMasterId, 
				RUNDetail.ProjectId,RUNDetail.ProjectName, RUNDetail.ProjectRoot, RUNDetail.ManualSession, RUNDetail.RequestGroupMasterID, 
                RUNDetail.FarmName, RUNDetail.ReportingProduct, RUNDetail.ReportingMetaBuild, RUNDetail.TesterID, RUNDetail.UserDomain, 
                RUNDetail.TestPlanName, NODEDataRID.StartTime, NODEDataRID.TestStartTime, NODEDataRID.TestStopTime, 
                NODEDataRID.LastModifiedBy, ResultOption.Result,  QlasrRequestGrp.RequestedBy 
            FROM 
                [QCA_RPT].[dbo].[tblRunTitleDetails] AS RUNDetail 
			INNER JOIN   [QCA_RPT].[tms].[tblTestPlanByVersion] AS TestplanVersion on TestplanVersion.TPByVerRID = RUNDetail.TestPlanID
            INNER JOIN [QCA_RPT].[dbo].[tblNODEData] AS NODEDataRID on NODEDataRID.SessionDataRID = RUNDetail.SessionDataRID
			INNER JOIN   [QCA_RPT].[tms].[tblTestCaseByVersion] AS TestcaseVersion on TestcaseVersion.TCByVerRID = NODEDataRID.TCByVerRID
            INNER JOIN [QCA_RPT].[prj].[tblNODE] AS Node  on RUNDetail.ProjectID = Node.NodeID
            INNER JOIN [QCA_RPT].[dbo].[tblResultOptions] AS ResultOption on ResultOption.ResultOptionsRID = NODEDataRID.ResultOptionsRID
            LEFT JOIN  [QCA_RPT].[lap].[tblRequestGroup] AS QlasrRequestGrp on QlasrRequestGrp.RequestGroupID = RUNDetail.RequestGroupMasterID
            WHERE 
                NODEDataRID.TCByVerRID IS NOT NULL AND NODEDataRID.StartTime between getdate()-7 and getdate() 
				AND (RUNDetail.ReportingProduct LIKE 'IPQ%' OR RUNDetail.ReportingProduct LIKE 'QCA9531%') AND QlasrRequestGrp.PoolID IS NULL AND 
                (RUNDetail.TestPlanName NOT LIKE '%Devpool%' AND RUNDetail.TestPlanName NOT LIKE '%SU_Sanity%') AND 
                (ResultOption.Result != 'Skipped' AND ResultOption.Result != 'Exception')

Query-B

SELECT Node.NodeMasterID as NodeMasterId, TestplanVersion.MasterTPRID as TestplanMasterId, TestcaseVersion.TCMasterRID as TestcaseMasterId, ResultOption.Result
            FROM 
            [QCA_RPT].[dbo].[tblRunTitleDetails] AS RUNDetail 
			INNER JOIN   [QCA_RPT].[tms].[tblTestPlanByVersion] AS TestplanVersion on TestplanVersion.TPByVerRID = RUNDetail.TestPlanID
            INNER JOIN [QCA_RPT].[dbo].[tblNODEData] AS NODEDataRID on NODEDataRID.SessionDataRID = RUNDetail.SessionDataRID
			INNER JOIN   [QCA_RPT].[tms].[tblTestCaseByVersion] AS TestcaseVersion on TestcaseVersion.TCByVerRID = NODEDataRID.TCByVerRID
            INNER JOIN [QCA_RPT].[prj].[tblNODE] AS Node  on RUNDetail.ProjectID = Node.NodeID
            INNER JOIN [QCA_RPT].[dbo].[tblResultOptions] AS ResultOption on ResultOption.ResultOptionsRID = NODEDataRID.ResultOptionsRID
            LEFT JOIN  [QCA_RPT].[lap].[tblRequestGroup] AS QlasrRequestGrp on QlasrRequestGrp.RequestGroupID = RUNDetail.RequestGroupMasterID
            WHERE NodeDataRID.NodeDataRID in (
				SELECT MAX(NodeDataRID)
				FROM 
				[QCA_RPT].[dbo].[tblRunTitleDetails] AS RUNDetail 
				INNER JOIN   [QCA_RPT].[tms].[tblTestPlanByVersion] AS TestplanVersion on TestplanVersion.TPByVerRID = RUNDetail.TestPlanID
				INNER JOIN [QCA_RPT].[dbo].[tblNODEData] AS NODEDataRID on NODEDataRID.SessionDataRID = RUNDetail.SessionDataRID
				INNER JOIN   [QCA_RPT].[tms].[tblTestCaseByVersion] AS TestcaseVersion on TestcaseVersion.TCByVerRID = NODEDataRID.TCByVerRID
				INNER JOIN [QCA_RPT].[prj].[tblNODE] AS Node  on RUNDetail.ProjectID = Node.NodeID
				INNER JOIN [QCA_RPT].[dbo].[tblResultOptions] AS ResultOption on ResultOption.ResultOptionsRID = NODEDataRID.ResultOptionsRID
				LEFT JOIN  [QCA_RPT].[lap].[tblRequestGroup] AS QlasrRequestGrp on QlasrRequestGrp.RequestGroupID = RUNDetail.RequestGroupMasterID
				WHERE Node.NodeMasterID in (762701, 762702)
				 AND NODEDataRID.StartTime < getdate()-7
				 AND (RUNDetail.ReportingProduct LIKE 'IPQ%' OR RUNDetail.ReportingProduct LIKE 'QCA9531%') AND QlasrRequestGrp.PoolID IS NULL AND 
                (RUNDetail.TestPlanName NOT LIKE '%Devpool%' AND RUNDetail.TestPlanName NOT LIKE '%SU_Sanity%') AND (ResultOption.Result != 'Skipped' AND ResultOption.Result != 'Exception')
				group by Node.NodeMasterID, TestplanVersion.MasterTPRID, TestcaseVersion.TCMasterRID 
			)
