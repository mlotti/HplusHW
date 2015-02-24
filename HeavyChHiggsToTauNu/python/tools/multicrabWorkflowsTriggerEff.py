## \package multicrabDatasetsTriggerEff
# Functions for trigger efficiency workflow definitions

from multicrabWorkflowsTools import Dataset, Workflow, Data, Source, updatePublishName, TaskDef, updateTaskDefinitions
from multicrabWorkflowsPattuple import constructProcessingWorkflow_53X

import multicrabDatasetsCommon as common

def addTauLegSkim_53X(version, datasets, updateDefinitions, skim=None):
    mcTriggerTauLeg = "HLT_IsoMu15_eta2p1_L1ETM20_v5"
    mcTriggers = [mcTriggerTauLeg]

    def TaskDefMC(**kwargs):
        return TaskDef(triggerOR=mcTriggers, **kwargs)

    defaultDefinitions = {
	"TauPlusX_190456-193621_2012A_Jan22": TaskDef(njobsIn= 200, njobsOut=  70,triggerOR=["HLT_IsoMu15_eta2p1_L1ETM20_v3","HLT_IsoMu15_eta2p1_L1ETM20_v4"], triggerThrow=False),
        "TauPlusX_193834-196531_2012B_Jan22": TaskDef(njobsIn=2000, njobsOut= 400, triggerOR=["HLT_IsoMu15_eta2p1_L1ETM20_v5"]),
        "TauPlusX_198022-203742_2012C_Jan22": TaskDef(njobsIn=2000, njobsOut= 400, triggerOR=["HLT_IsoMu15_eta2p1_L1ETM20_v6","HLT_IsoMu15_eta2p1_L1ETM20_v7"], triggerThrow=False),
        "TauPlusX_203777-208686_2012D_Jan22": TaskDef(njobsIn=3600, njobsOut= 500, triggerOR=["HLT_IsoMu15_eta2p1_L1ETM20_v7"]),

        "DYToTauTau_M_20_CT10_TuneZ2star_powheg_tauola_Summer12":    TaskDefMC(njobsIn= 40, njobsOut= 10),                                                   
        "DYToTauTau_M_20_CT10_TuneZ2star_v2_powheg_tauola_Summer12": TaskDefMC(njobsIn= 2000, njobsOut= 200),                                                
        "DYToTauTau_M_100to200_TuneZ2Star_pythia6_tauola_Summer12":  TaskDefMC(njobsIn= 5, njobsOut= 1),                                             
        "DYToTauTau_M_200to400_TuneZ2Star_pythia6_tauola_Summer12":  TaskDefMC(njobsIn= 5, njobsOut= 1),                                             
        "DYToTauTau_M_400to800_TuneZ2Star_pythia6_tauola_Summer12":  TaskDefMC(njobsIn= 5, njobsOut= 1),                                             
        "DYToTauTau_M_800_TuneZ2Star_pythia6_tauola_Summer12":       TaskDefMC(njobsIn= 5, njobsOut= 1),

        "QCD_Pt30to50_TuneZ2star_Summer12":       TaskDefMC(njobsIn= 20, njobsOut=1),                                                                                                                                         
        "QCD_Pt50to80_TuneZ2star_Summer12":       TaskDefMC(njobsIn= 20, njobsOut=1),                                                                                                                                         
        "QCD_Pt80to120_TuneZ2star_Summer12":      TaskDefMC(njobsIn= 20, njobsOut=4),                                                                                                                                         
        "QCD_Pt120to170_TuneZ2star_Summer12":     TaskDefMC(njobsIn= 40, njobsOut=4),                                                                                                                                         
        "QCD_Pt170to300_TuneZ2star_Summer12":     TaskDefMC(njobsIn= 80, njobsOut=2),                                                                                                                                         
        "QCD_Pt170to300_TuneZ2star_v2_Summer12":  TaskDefMC(njobsIn=300, njobsOut=6),                                                                                                                                         
        "QCD_Pt300to470_TuneZ2star_Summer12":     TaskDefMC(njobsIn=250, njobsOut=4),                                                                                                                                         
        "QCD_Pt300to470_TuneZ2star_v2_Summer12":  TaskDefMC(njobsIn=150, njobsOut=3),                                                                                                                                         
        "QCD_Pt300to470_TuneZ2star_v3_Summer12":  TaskDefMC(njobsIn=850, njobsOut=14),                                                                                                                                        
                                                                                                                                                                                                                              
        "WW_TuneZ2star_Summer12":                 TaskDefMC(njobsIn=150, njobsOut= 8),                                                                                                                                        
        "WZ_TuneZ2star_Summer12":                 TaskDefMC(njobsIn=150, njobsOut= 8),                                                                                                                                        
        "ZZ_TuneZ2star_Summer12":                 TaskDefMC(njobsIn=150, njobsOut= 8),                                                                                                                                        
        "TTJets_TuneZ2star_Summer12":             TaskDefMC(njobsIn=700, njobsOut=30),                                                                                                                                        
        "WJets_TuneZ2star_v1_Summer12":           TaskDefMC(njobsIn=100, njobsOut= 4, args={"wjetsWeighting": 1}),
        "WJets_TuneZ2star_v2_Summer12":           TaskDefMC(njobsIn=250, njobsOut=16, args={"wjetsWeighting": 1}),
        "W1Jets_TuneZ2star_Summer12":             TaskDefMC(njobsIn=150, njobsOut= 8, args={"wjetsWeighting": 1}),
        "W2Jets_TuneZ2star_Summer12":             TaskDefMC(njobsIn=800, njobsOut=40, args={"wjetsWeighting": 1}),
        "W3Jets_TuneZ2star_Summer12":             TaskDefMC(njobsIn=490, njobsOut=50, args={"wjetsWeighting": 1}),
        "W4Jets_TuneZ2star_Summer12":             TaskDefMC(njobsIn=550, njobsOut=30, args={"wjetsWeighting": 1}),
        "DYJetsToLL_M50_TuneZ2star_Summer12":     TaskDefMC(njobsIn=350, njobsOut=60),                                                                                                                                        
        "DYJetsToLL_M10to50_TuneZ2star_Summer12": TaskDefMC(njobsIn= 40, njobsOut= 1),                                                                                                                                        
        "T_t-channel_TuneZ2star_Summer12":        TaskDefMC(njobsIn=100, njobsOut= 5),                                                                                                                                        
        "Tbar_t-channel_TuneZ2star_Summer12":     TaskDefMC(njobsIn= 50, njobsOut= 5),                                                                                                                                        
        "T_tW-channel_TuneZ2star_Summer12":       TaskDefMC(njobsIn= 20, njobsOut= 2),                                                                                                                                        
        "Tbar_tW-channel_TuneZ2star_Summer12":    TaskDefMC(njobsIn= 20, njobsOut= 2),                                                                                                                                        
        "T_s-channel_TuneZ2star_Summer12":        TaskDefMC(njobsIn= 10, njobsOut= 1),                                                                                                                                        
        "Tbar_s-channel_TuneZ2star_Summer12":     TaskDefMC(njobsIn= 10, njobsOut= 1),
    }

    workflowName = "triggerTauLeg_skim_"+version

    # Update the default definitions from the argument
    updateTaskDefinitions(defaultDefinitions, updateDefinitions)

    # Add pattuple Workflow for each dataset
    for datasetName, taskDef in defaultDefinitions.iteritems():
        dataset = datasets.getDataset(datasetName)

        # Construct processing workflow
        wf = constructProcessingWorkflow_53X(dataset, taskDef, sourceWorkflow="AOD", workflowName=workflowName, skimConfig=skim)

        # Set tau-leg specific customizations on job configuration
        wf.addArg("customizeConfig", "TauLegZMuTauFilter")

        # Setup the publish name
#        name = updatePublishName(dataset, wf.source.getDataForDataset(dataset).getDatasetPath(), "analysis_tauleg_"+version)
	name = updatePublishName(dataset, wf.source.getDataForDataset(dataset).getDatasetPath(), workflowName)
        wf.addCrabLine("USER.publish_data_name = "+name)

        # For MC, split by events, for data, split by lumi
        if dataset.isMC():
            wf.addCrabLine("CMSSW.total_number_of_events = -1")
        else:
            wf.addCrabLine("CMSSW.total_number_of_lumis = -1")

        # Add the pattuple Workflow to Dataset
        dataset.addWorkflow(wf)
        # If DBS-dataset of the pattuple has been specified, add also analysis Workflow to Dataset
        if wf.output != None:
            commonArgs = {
                "source": Source(workflowName),
                "args": wf.args,
                "skimConfig": skim
                }
            commonArgs["args"]["trgAnalysis"] = "TauLeg"

            if dataset.isData():
                # For data, construct one analysis workflow per trigger type
                pd = datasetName.split("_")[0]
                if pd == "Tau" or pd == "TauPlusX":
                    dataset.addWorkflow(Workflow("triggerTauLeg_analysis_"+version, triggerOR=wf.triggerOR, **commonArgs))
                elif pd == "MultiJet":
                    if datasetName in quadJetTriggers:
                        dataset.addWorkflow(Workflow("analysis_quadjet_"+version, triggerOR=quadJetTriggers[datasetName], **commonArgs))
                    if datasetName in quadJetBTagTriggers:
                        dataset.addWorkflow(Workflow("analysis_quadjetbtag_"+version, triggerOR=quadJetBTagTriggers[datasetName], **commonArgs))
                    if datasetName in quadPFJetBTagTriggers:
                        dataset.addWorkflow(Workflow("analysis_quadpfjetbtag_"+version, triggerOR=quadPFJetBTagTriggers[datasetName], **commonArgs))
                else:
                    raise Exception("Unsupported PD name %s" % pd)
            else:
                # For MC, also construct one analysis workflow per trigger type
                dataset.addWorkflow(Workflow("triggerTauLeg_analysis_"+version, triggerOR=[mcTriggerTauLeg], **commonArgs))


def addTauLegSkim_53X_v3(datasets):
    definitions = {
        "TauPlusX_190456-193621_2012A_Jan22": TaskDef(""),
        "TauPlusX_193834-196531_2012B_Jan22": TaskDef(""),
        "TauPlusX_198022-203742_2012C_Jan22": TaskDef(""),
        "TauPlusX_203777-208686_2012D_Jan22": TaskDef(""),
        
        "DYToTauTau_M_20_CT10_TuneZ2star_powheg_tauola_Summer12":    TaskDef(""),
        "DYToTauTau_M_20_CT10_TuneZ2star_v2_powheg_tauola_Summer12": TaskDef(""),
        "DYToTauTau_M_100to200_TuneZ2Star_pythia6_tauola_Summer12":  TaskDef(""),
        "DYToTauTau_M_200to400_TuneZ2Star_pythia6_tauola_Summer12":  TaskDef(""),
        "DYToTauTau_M_400to800_TuneZ2Star_pythia6_tauola_Summer12":  TaskDef(""),
        "DYToTauTau_M_800_TuneZ2Star_pythia6_tauola_Summer12":       TaskDef(""),

        "QCD_Pt30to50_TuneZ2star_Summer12":       TaskDef(""),                                                                                                                                                                
        "QCD_Pt50to80_TuneZ2star_Summer12":       TaskDef(""),                                                                                                                                                                
        "QCD_Pt80to120_TuneZ2star_Summer12":      TaskDef(""),                                                                                                                                                                
        "QCD_Pt120to170_TuneZ2star_Summer12":     TaskDef(""),                                                                                                                                                                
        "QCD_Pt170to300_TuneZ2star_Summer12":     TaskDef(""),                                                                                                                                                                
        "QCD_Pt170to300_TuneZ2star_v2_Summer12":  TaskDef(""),                                                                                                                                                                
        "QCD_Pt300to470_TuneZ2star_Summer12":     TaskDef(""),                                                                                                                                                                
        "QCD_Pt300to470_TuneZ2star_v2_Summer12":  TaskDef(""),                                                                                                                                                                
        "QCD_Pt300to470_TuneZ2star_v3_Summer12":  TaskDef(""),                                                                                                                                                                
                                                                                                                                                                                                                              
        "WW_TuneZ2star_Summer12":                 TaskDef(""),                                                                                                                                                                
        "WZ_TuneZ2star_Summer12":                 TaskDef(""),                                                                                                                                                                
        "ZZ_TuneZ2star_Summer12":                 TaskDef(""),                                                                                                                                                                
        "TTJets_TuneZ2star_Summer12":             TaskDef(""),                                                                                                                                                                
        "WJets_TuneZ2star_v1_Summer12":           TaskDef(""),                                                                                                                                                                
        "WJets_TuneZ2star_v2_Summer12":           TaskDef(""),                                                                                                                                                                
        "W1Jets_TuneZ2star_Summer12":             TaskDef(""),                                                                                                                                                                
        "W2Jets_TuneZ2star_Summer12":             TaskDef(""),                                                                                                                                                                
        "W3Jets_TuneZ2star_Summer12":             TaskDef(""),                                                                                                                                                                
        "W4Jets_TuneZ2star_Summer12":             TaskDef(""),                                                                                                                                                                
        "DYJetsToLL_M50_TuneZ2star_Summer12":     TaskDef(""),                                                                                                                                                                
        "DYJetsToLL_M10to50_TuneZ2star_Summer12": TaskDef(""),                                                                                                                                                                
        "T_t-channel_TuneZ2star_Summer12":        TaskDef(""),                                                                                                                                                                
        "Tbar_t-channel_TuneZ2star_Summer12":     TaskDef(""),                                                                                                                                                                
        "T_tW-channel_TuneZ2star_Summer12":       TaskDef(""),                                                                                                                                                                
        "Tbar_tW-channel_TuneZ2star_Summer12":    TaskDef(""),                                                                                                                                                                
        "T_s-channel_TuneZ2star_Summer12":        TaskDef(""),                                                                                                                                                                
        "Tbar_s-channel_TuneZ2star_Summer12":     TaskDef(""),
        }
        
    addTauLegSkim_53X("v53_v3", datasets, definitions)



def addMetLegSkim_53X(version, datasets, updateDefinitions, skim=None):
    mcTriggerMETLeg = "HLT_LooseIsoPFTau35_Trk20_Prong1_v6"
    mcTriggers = [
        mcTriggerMETLeg,
        ]
    def TaskDefMC(**kwargs):
        return TaskDef(triggerOR=mcTriggers, **kwargs)

    defaultDefinitions = {                                                                                                                                             
        # njobsOut is just a guess                  
        "Tau_190456-193621_2012A_Jan22":       TaskDef(njobsIn= 300, njobsOut= 6, triggerOR=["HLT_LooseIsoPFTau35_Trk20_Prong1_v2","HLT_LooseIsoPFTau35_Trk20_Prong1_v3","HLT_LooseIsoPFTau35_Trk20_Prong1_v4"], triggerThrow=False),
        "TauParked_193834-196531_2012B_Jan22": TaskDef(njobsIn=2500, njobsOut=25, triggerOR=["HLT_LooseIsoPFTau35_Trk20_Prong1_v6"], triggerThrow=False),
        "TauParked_198022-202504_2012C_Jan22": TaskDef(njobsIn=3000, njobsOut=40, triggerOR=["HLT_LooseIsoPFTau35_Trk20_Prong1_v7","HLT_LooseIsoPFTau35_Trk20_Prong1_v9"], triggerThrow=False),
        "TauParked_202972-203742_2012C_Jan22": TaskDef(njobsIn= 150, njobsOut= 1, triggerOR=["HLT_LooseIsoPFTau35_Trk20_Prong1_v10"], triggerThrow=False),
        "TauParked_203777-208686_2012D_Jan22": TaskDef(njobsIn=7000, njobsOut=500, triggerOR=["HLT_LooseIsoPFTau35_Trk20_Prong1_v10"], triggerThrow=False),
                                                                                       
        "QCD_Pt30to50_TuneZ2star_Summer12":       TaskDefMC(njobsIn= 20, njobsOut=1),
        "QCD_Pt50to80_TuneZ2star_Summer12":       TaskDefMC(njobsIn= 20, njobsOut=2),
        "QCD_Pt80to120_TuneZ2star_Summer12":      TaskDefMC(njobsIn= 20, njobsOut=4),  
        "QCD_Pt120to170_TuneZ2star_Summer12":     TaskDefMC(njobsIn= 40, njobsOut=4),  
        "QCD_Pt170to300_TuneZ2star_Summer12":     TaskDefMC(njobsIn= 80, njobsOut=2),  
        "QCD_Pt170to300_TuneZ2star_v2_Summer12":  TaskDefMC(njobsIn=300, njobsOut=6),  
        "QCD_Pt300to470_TuneZ2star_Summer12":     TaskDefMC(njobsIn=250, njobsOut=4),  
        "QCD_Pt300to470_TuneZ2star_v2_Summer12":  TaskDefMC(njobsIn=150, njobsOut=3),  
        "QCD_Pt300to470_TuneZ2star_v3_Summer12":  TaskDefMC(njobsIn=850, njobsOut=14), 
                                                                                       
        "WW_TuneZ2star_Summer12":                 TaskDefMC(njobsIn=150, njobsOut= 15),
        "WZ_TuneZ2star_Summer12":                 TaskDefMC(njobsIn=150, njobsOut= 15),
        "ZZ_TuneZ2star_Summer12":                 TaskDefMC(njobsIn=150, njobsOut= 15),
        "TTJets_TuneZ2star_Summer12":             TaskDefMC(njobsIn=700, njobsOut=30), 
        "WJets_TuneZ2star_v1_Summer12":           TaskDefMC(njobsIn=100, njobsOut= 10, args={"wjetsWeighting": 1}),
        "WJets_TuneZ2star_v2_Summer12":           TaskDefMC(njobsIn=250, njobsOut= 25, args={"wjetsWeighting": 1}),
        "W1Jets_TuneZ2star_Summer12":             TaskDefMC(njobsIn=150, njobsOut= 15, args={"wjetsWeighting": 1}),
        "W2Jets_TuneZ2star_Summer12":             TaskDefMC(njobsIn=800, njobsOut= 80, args={"wjetsWeighting": 1}),
        "W3Jets_TuneZ2star_Summer12":             TaskDefMC(njobsIn=490, njobsOut= 50, args={"wjetsWeighting": 1}),
        "W4Jets_TuneZ2star_Summer12":             TaskDefMC(njobsIn=550, njobsOut= 55, args={"wjetsWeighting": 1}),
        "DYJetsToLL_M50_TuneZ2star_Summer12":     TaskDefMC(njobsIn=350, njobsOut= 60),                                           
        "DYJetsToLL_M10to50_TuneZ2star_Summer12": TaskDefMC(njobsIn= 40, njobsOut= 1),                                            
        "T_t-channel_TuneZ2star_Summer12":        TaskDefMC(njobsIn=100, njobsOut= 5),
        "Tbar_t-channel_TuneZ2star_Summer12":     TaskDefMC(njobsIn= 50, njobsOut= 5),
        "T_tW-channel_TuneZ2star_Summer12":       TaskDefMC(njobsIn= 20, njobsOut= 2),                                            
        "Tbar_tW-channel_TuneZ2star_Summer12":    TaskDefMC(njobsIn= 20, njobsOut= 2),                                            
        "T_s-channel_TuneZ2star_Summer12":        TaskDefMC(njobsIn= 10, njobsOut= 1),                                            
        "Tbar_s-channel_TuneZ2star_Summer12":     TaskDefMC(njobsIn= 10, njobsOut= 1),                                            
        }

    workflowName = "triggerMetLeg_skim_"+version

    # Update the default definitions from the argument             
    updateTaskDefinitions(defaultDefinitions, updateDefinitions)   
                                                                   
    # Add pattuple Workflow for each dataset                       
    for datasetName, taskDef in defaultDefinitions.iteritems():    
        dataset = datasets.getDataset(datasetName)                 
                                                                   
        # Construct processing workflow                                       
        wf = constructProcessingWorkflow_53X(dataset, taskDef, sourceWorkflow="AOD", workflowName=workflowName, skimConfig=skim)

        # Setup the publish name                                                 
        name = updatePublishName(dataset, wf.source.getDataForDataset(dataset).getDatasetPath(), workflowName)
        wf.addCrabLine("USER.publish_data_name = "+name)                         
                                                                                 
        # For MC, split by events, for data, split by lumi                       
        if dataset.isMC():                                                       
            wf.addCrabLine("CMSSW.total_number_of_events = -1") 
        else:                                                   
            wf.addCrabLine("CMSSW.total_number_of_lumis = -1")  
                                                                
        # Add the pattuple Workflow to Dataset                  
        dataset.addWorkflow(wf)                                 
        # If DBS-dataset of the pattuple has been specified, add also analysis Workflow to Dataset
        if wf.output != None:                                                                     
            commonArgs = {                                                                        
                "source": Source(workflowName),                                                   
                "args": wf.args,                                                                  
                "skimConfig": skim                                                                
                }
            commonArgs["args"]["trgAnalysis"] = "MetLeg"

            if dataset.isData():                                                                  
                # For data, construct one analysis workflow per trigger type                      
                pd = datasetName.split("_")[0]                                                    
                if pd == "Tau" or pd == "TauParked":
                    dataset.addWorkflow(Workflow("triggerMetLeg_analysis_"+version, triggerOR=wf.triggerOR, **commonArgs))
                elif pd == "MultiJet":                                                                                    
                    if datasetName in quadJetTriggers:                                                                    
                        dataset.addWorkflow(Workflow("analysis_quadjet_"+version, triggerOR=quadJetTriggers[datasetName], **commonArgs))                               
                    if datasetName in quadJetBTagTriggers:                                                                
                        dataset.addWorkflow(Workflow("analysis_quadjetbtag_"+version, triggerOR=quadJetBTagTriggers[datasetName], **commonArgs))                       
                    if datasetName in quadPFJetBTagTriggers:                                                              
                        dataset.addWorkflow(Workflow("analysis_quadpfjetbtag_"+version, triggerOR=quadPFJetBTagTriggers[datasetName], **commonArgs))                   
                else:                                                                                                     
                    raise Exception("Unsupported PD name %s" % pd)                                                        
            else:                                                                                                         
                # For MC, also construct one analysis workflow per trigger type                                           
                dataset.addWorkflow(Workflow("triggerMetLeg_analysis_"+version, triggerOR=[mcTriggerMETLeg], **commonArgs))

def addMetLegSkim_53X_v3(datasets):
    definitions = {
        "Tau_190456-193621_2012A_Jan22":          TaskDef(""),
        "TauParked_193834-196531_2012B_Jan22":    TaskDef(""),
        "TauParked_198022-202504_2012C_Jan22":    TaskDef(""),
        "TauParked_202972-203742_2012C_Jan22":    TaskDef(""),
        "TauParked_203777-208686_2012D_Jan22":    TaskDef(""),

        "QCD_Pt30to50_TuneZ2star_Summer12":       TaskDef(""),                               
        "QCD_Pt50to80_TuneZ2star_Summer12":       TaskDef(""),                               
        "QCD_Pt80to120_TuneZ2star_Summer12":      TaskDef(""),                               
        "QCD_Pt120to170_TuneZ2star_Summer12":     TaskDef(""),                               
        "QCD_Pt170to300_TuneZ2star_Summer12":     TaskDef(""),                               
        "QCD_Pt170to300_TuneZ2star_v2_Summer12":  TaskDef(""),                               
        "QCD_Pt300to470_TuneZ2star_Summer12":     TaskDef(""),                               
        "QCD_Pt300to470_TuneZ2star_v2_Summer12":  TaskDef(""),                               
        "QCD_Pt300to470_TuneZ2star_v3_Summer12":  TaskDef(""),                               
                                                                                             
        "WW_TuneZ2star_Summer12":                 TaskDef(""),                               
        "WZ_TuneZ2star_Summer12":                 TaskDef(""),                               
        "ZZ_TuneZ2star_Summer12":                 TaskDef(""),                               
        "TTJets_TuneZ2star_Summer12":             TaskDef(""),                               
        "WJets_TuneZ2star_v1_Summer12":           TaskDef(""),                               
        "WJets_TuneZ2star_v2_Summer12":           TaskDef(""),                               
        "W1Jets_TuneZ2star_Summer12":             TaskDef(""),                               
        "W2Jets_TuneZ2star_Summer12":             TaskDef(""),                               
        "W3Jets_TuneZ2star_Summer12":             TaskDef(""),                               
        "W4Jets_TuneZ2star_Summer12":             TaskDef(""),                               
        "DYJetsToLL_M50_TuneZ2star_Summer12":     TaskDef(""),                               
        "DYJetsToLL_M10to50_TuneZ2star_Summer12": TaskDef(""),                               
        "T_t-channel_TuneZ2star_Summer12":        TaskDef(""),                               
        "Tbar_t-channel_TuneZ2star_Summer12":     TaskDef(""),                               
        "T_tW-channel_TuneZ2star_Summer12":       TaskDef(""),                               
        "Tbar_tW-channel_TuneZ2star_Summer12":    TaskDef(""),                               
        "T_s-channel_TuneZ2star_Summer12":        TaskDef(""),                               
        "Tbar_s-channel_TuneZ2star_Summer12":     TaskDef(""),                               
        }
                                                                                             
    addMetLegSkim_53X("v53_v3", datasets, definitions)                                        

def addMetLegSkim_44X(version, datasets, updateDefinitions, skim=None):
    mcTriggerMETLeg = "HLT_MediumIsoPFTau35_Trk20_v1"
    def TaskDefMC(**kwargs):
        return TaskDef(triggerOR=[mcTriggerMETLeg], **kwargs)

    # The numbers of jobs are from multicrabDatasetsPattuple, they may have to be adjusted
    defaultDefinitions = {
        "Tau_165970-167913_2011A_Nov08": TaskDef(njobsIn=300, njobsOut=30, triggerOR=[
                                                    "HLT_IsoPFTau35_Trk20_v2", # 165970-166164, 166374-167043
                                                    "HLT_IsoPFTau35_Trk20_v3", # 166346-166346
                                                    "HLT_IsoPFTau35_Trk20_v4", # 167078-167913
                                                ], triggerThrow=False),
        "Tau_170722-173198_2011A_Nov08": TaskDef(njobsIn=70, njobsOut=30, triggerOR=["HLT_IsoPFTau35_Trk20_v6"]),
        "Tau_173236-173692_2011A_Nov08": TaskDef(njobsIn=30, njobsOut=30, triggerOR=["HLT_MediumIsoPFTau35_Trk20_v1"]),
        "Tau_175832-180252_2011B_Nov19": TaskDef(njobsIn=300, njobsOut=30, triggerOR=[
                                                    "HLT_MediumIsoPFTau35_Trk20_v1", #175832-178380
                                                    "HLT_MediumIsoPFTau35_Trk20_v5", #178420-179889
                                                    "HLT_MediumIsoPFTau35_Trk20_v6", #179959-180252
                                              ], triggerThrow=False),

        # MC, triggered with mcTrigger
        "QCD_Pt30to50_TuneZ2_Fall11":       TaskDefMC(njobsIn=10, njobsOut=1),
        "QCD_Pt50to80_TuneZ2_Fall11":       TaskDefMC(njobsIn=10, njobsOut=1),
        "QCD_Pt80to120_TuneZ2_Fall11":      TaskDefMC(njobsIn=10, njobsOut=10),
        "QCD_Pt120to170_TuneZ2_Fall11":     TaskDefMC(njobsIn=20, njobsOut=20),
        "QCD_Pt170to300_TuneZ2_Fall11":     TaskDefMC(njobsIn=40, njobsOut=4),
        "QCD_Pt300to470_TuneZ2_Fall11":     TaskDefMC(njobsIn=40, njobsOut=10),
                                            
        "WW_TuneZ2_Fall11":                 TaskDefMC(njobsIn=50, njobsOut=3),
        "WZ_TuneZ2_Fall11":                 TaskDefMC(njobsIn=50, njobsOut=3),
        "ZZ_TuneZ2_Fall11":                 TaskDefMC(njobsIn=50, njobsOut=3),
        "TTJets_TuneZ2_Fall11":             TaskDefMC(njobsIn=490, njobsOut=250),
        "WJets_TuneZ2_Fall11":              TaskDefMC(njobsIn=490, njobsOut=10),
        "W2Jets_TuneZ2_Fall11":             TaskDefMC(njobsIn=300, njobsOut=20),
        "W3Jets_TuneZ2_Fall11":             TaskDefMC(njobsIn=120, njobsOut=10),
        "W4Jets_TuneZ2_Fall11":             TaskDefMC(njobsIn=200, njobsOut=40),
        "DYJetsToLL_M50_TuneZ2_Fall11":     TaskDefMC(njobsIn=350, njobsOut=35),
        "DYJetsToLL_M10to50_TuneZ2_Fall11": TaskDefMC(njobsIn=300, njobsOut=10),
        "T_t-channel_TuneZ2_Fall11":        TaskDefMC(njobsIn=50, njobsOut=5),
        "Tbar_t-channel_TuneZ2_Fall11":     TaskDefMC(njobsIn=50, njobsOut=5),
        "T_tW-channel_TuneZ2_Fall11":       TaskDefMC(njobsIn=20, njobsOut=5),
        "Tbar_tW-channel_TuneZ2_Fall11":    TaskDefMC(njobsIn=20, njobsOut=5),
        "T_s-channel_TuneZ2_Fall11":        TaskDefMC(njobsIn=10, njobsOut=2),
        "Tbar_s-channel_TuneZ2_Fall11":     TaskDefMC(njobsIn=10, njobsOut=2),

        # Here is an example how to specity number of events/job
        # instead of number of jobs, and how to give dataset-specific
        # arbitrary crab configuration lines
        #"Tbar_s-channel_TuneZ2_Fall11":     TaskDefMC(neventsPerJobIn=10000, neventsPerJobOut=1000000, crabLines=["USER.user_remote_dir=/foo"]),
        }

    # Update the default definitions from the argument
    updateTaskDefinitions(defaultDefinitions, updateDefinitions, workflowName)

    # Add Workflow for each dataset
    for datasetName, taskDef in defaultDefinitions.iteritems():
        dataset = datasets.getDataset(datasetName)

        # Construct processing workflow
        wf = constructProcessingWorkflow_44X(dataset, taskDef, sourceWorkflow="AOD", workflowName=workflowName, inputLumiMaskData="Nov08ReReco", outputLumiMaskData=None)

        # Example of how to set user_remote_dir for this workflow only (but for all datasets)
        #wf.addCrabLine("USER.user_remote_dir = /whatever")

        dataset.addWorkflow(wf)


        # If have skim output, define the workflows which depend on it
#        if wf.output != None:
#	    wf.output.dbs_url = common.tteff_dbs
#            dataset.addWorkflow(Workflow("triggerMetLeg_analysis_"+version, source=Source(workflowName),
#                                         triggerOR=taskDef.triggerOR, args=wf.args, output_file="tteffAnalysis-metleg.root"))


def addMetLegSkim_cmssw44X_v1(datasets):
    definitions = {

        "Tau_165970-167913_2011A_Nov08":    TaskDef(""),
        "Tau_170722-173198_2011A_Nov08":    TaskDef(""),
        "Tau_173236-173692_2011A_Nov08":    TaskDef(""),
        "Tau_175832-180252_2011B_Nov19":    TaskDef(""),

        "QCD_Pt30to50_TuneZ2_Fall11":       TaskDef(""),
        "QCD_Pt50to80_TuneZ2_Fall11":       TaskDef(""),
        "QCD_Pt80to120_TuneZ2_Fall11":      TaskDef(""),
        "QCD_Pt120to170_TuneZ2_Fall11":     TaskDef(""),
        "QCD_Pt170to300_TuneZ2_Fall11":     TaskDef(""),
        "QCD_Pt300to470_TuneZ2_Fall11":     TaskDef(""),

        "WW_TuneZ2_Fall11":                 TaskDef(""),
        "WZ_TuneZ2_Fall11":                 TaskDef(""),
        "ZZ_TuneZ2_Fall11":                 TaskDef(""),
        "TTJets_TuneZ2_Fall11":             TaskDef(""),
        "WJets_TuneZ2_Fall11":              TaskDef(""),
        "W2Jets_TuneZ2_Fall11":             TaskDef(""),
        "W3Jets_TuneZ2_Fall11":             TaskDef(""),
        "W4Jets_TuneZ2_Fall11":             TaskDef(""),
        "DYJetsToLL_M50_TuneZ2_Fall11":     TaskDef(""),
        "DYJetsToLL_M10to50_TuneZ2_Fall11": TaskDef(""),
        "T_t-channel_TuneZ2_Fall11":        TaskDef(""),
        "Tbar_t-channel_TuneZ2_Fall11":     TaskDef(""),
        "T_tW-channel_TuneZ2_Fall11":       TaskDef(""),
        "Tbar_tW-channel_TuneZ2_Fall11":    TaskDef(""),
        "T_s-channel_TuneZ2_Fall11":        TaskDef(""),
        "Tbar_s-channel_TuneZ2_Fall11":     TaskDef(""),
        }

    addMetLegSkim_44X("cmssw44X_v1", datasets, definitions)



def addQuadJetSkim_53X(version, datasets, updateDefinitions, skim=None):
    mcTriggerSingleMu = []
    mcTriggerSingleMu.append("HLT_Mu5_v18")
    mcTriggerSingleMu.append("HLT_Mu8_v16")   
    mcTriggerSingleMu.append("HLT_Mu12_v16")
    mcTriggerSingleMu.append("HLT_Mu17_v3")
    mcTriggerSingleMu.append("HLT_Mu12_eta2p1_L1Mu10erJetC12WdEtaPhi1DiJetsC_v3")
    mcTriggerSingleMu.append("HLT_Mu15_eta2p1_v3")
    mcTriggerSingleMu.append("HLT_Mu24_v14")
    mcTriggerSingleMu.append("HLT_Mu24_eta2p1_v3")
    mcTriggerSingleMu.append("HLT_Mu30_v14")
    mcTriggerSingleMu.append("HLT_Mu30_eta2p1_v3")
    mcTriggerSingleMu.append("HLT_Mu40_v12")
    mcTriggerSingleMu.append("HLT_Mu40_eta2p1_v9")
    mcTriggerSingleMu.append("HLT_Mu50_eta2p1_v6")  
    mcTriggerSingleMu.append("HLT_RelIso1p0Mu5_v4")
    mcTriggerSingleMu.append("HLT_RelIso1p0Mu20_v1")
    mcTriggerSingleMu.append("HLT_IsoMu15_eta2p1_L1ETM20_v5")
    mcTriggerSingleMu.append("HLT_IsoMu20_eta2p1_v5")
    mcTriggerSingleMu.append("HLT_IsoMu24_v15")
    mcTriggerSingleMu.append("HLT_IsoMu24_eta2p1_v13")
    mcTriggerSingleMu.append("HLT_IsoMu30_v9")
    mcTriggerSingleMu.append("HLT_IsoMu30_eta2p1_v13")
    mcTriggerSingleMu.append("HLT_IsoMu34_eta2p1_v11")
    mcTriggerSingleMu.append("HLT_IsoMu40_eta2p1_v8")
    mcTriggerSingleMu.append("HLT_Mu40_eta2p1_Track50_dEdx3p6_v3")
    mcTriggerSingleMu.append("HLT_Mu40_eta2p1_Track60_dEdx3p7_v3")

    mcTriggers = mcTriggerSingleMu

    def TaskDefMC(**kwargs):
        return TaskDef(triggerOR=mcTriggers, **kwargs)
    
    defaultDefinitions = {
        
        # njobsOut is just a guess
        "SingleMu_190456-190738_2012A_Jul13": TaskDef(njobsIn= 490, njobsOut= 4, triggerOR=["HLT_Mu5_v18","HLT_Mu8_v16","HLT_Mu12_v16","HLT_Mu17_v3","HLT_Mu12_eta2p1_L1Mu10erJetC12WdEtaPhi1DiJetsC_v3", "HLT_Mu15_eta2p1_v3",                                                                                                                                                                                          
                                               "HLT_Mu24_eta2p1_v3", "HLT_Mu30_eta2p1_v3", "HLT_Mu40_eta2p1_v9",                                                                                                                                                                                                                                                                                                         
                                               "HLT_Mu50_eta2p1_v6", "HLT_RelIso1p0Mu5_v2", "HLT_RelIso1p0Mu17_v2", "HLT_IsoMu15_eta2p1_L1ETM20_v3", "HLT_IsoMu20_eta2p1_v3",                                                                                                                                                                                                                                            
                                               "HLT_IsoMu24_eta2p1_v11", "HLT_IsoMu30_eta2p1_v11", "HLT_IsoMu34_eta2p1_v9",                                                                                                                                                                                                                                                                                              
                                               "HLT_IsoMu40_eta2p1_v6", "HLT_Mu40_eta2p1_Track50_dEdx3p6_v3", "HLT_Mu40_eta2p1_Track60_dEdx3p7_v3" ]),                                                                                                                                                                                                                                                                   
        "SingleMu_190782-190949_2012A_Aug06": TaskDef(njobsIn= 490, njobsOut= 4, triggerOR=[ "HLT_Mu5_v18","HLT_Mu8_v16","HLT_Mu12_v16","HLT_Mu17_v3","HLT_Mu12_eta2p1_L1Mu10erJetC12WdEtaPhi1DiJetsC_v3", "HLT_Mu15_eta2p1_v3",                                                                                                                                                                                         
                                               "HLT_Mu24_eta2p1_v3", "HLT_Mu30_eta2p1_v3", "HLT_Mu40_eta2p1_v9",                                                                                                                                                                                                                                                                                                         
                                               "HLT_Mu50_eta2p1_v6", "HLT_RelIso1p0Mu5_v3", "HLT_RelIso1p0Mu17_v3", "HLT_IsoMu15_eta2p1_L1ETM20_v4", "HLT_IsoMu20_eta2p1_v4",                                                                                                                                                                                                                                            
                                               "HLT_IsoMu24_eta2p1_v12", "HLT_IsoMu30_eta2p1_v12", "HLT_IsoMu34_eta2p1_v10",                                                                                                                                                                                                                                                                                             
                                               "HLT_IsoMu40_eta2p1_v7", "HLT_Mu40_eta2p1_Track50_dEdx3p6_v3", "HLT_Mu40_eta2p1_Track60_dEdx3p7_v3"]),                                                                                                                                                                                                                                                                    
        "SingleMu_191043-193621_2012A_Jul13": TaskDef(njobsIn= 490, njobsOut= 4, triggerOR=["HLT_Mu5_v18","HLT_Mu8_v16","HLT_Mu12_v16","HLT_Mu17_v3","HLT_Mu12_eta2p1_L1Mu10erJetC12WdEtaPhi1DiJetsC_v3", "HLT_Mu15_eta2p1_v3",                                                                                                                                                                                          
                                               "HLT_Mu24_eta2p1_v3", "HLT_Mu30_eta2p1_v3", "HLT_Mu40_eta2p1_v9",                                                                                                                                                                                                                                                                                                         
                                               "HLT_Mu50_eta2p1_v6", "HLT_RelIso1p0Mu5_v3", "HLT_RelIso1p0Mu17_v3", "HLT_IsoMu15_eta2p1_L1ETM20_v4", "HLT_IsoMu20_eta2p1_v4",                                                                                                                                                                                                                                            
                                               "HLT_IsoMu24_eta2p1_v12", "HLT_IsoMu30_eta2p1_v12", "HLT_IsoMu34_eta2p1_v10",                                                                                                                                                                                                                                                                                             
                                               "HLT_IsoMu40_eta2p1_v7", "HLT_Mu40_eta2p1_Track50_dEdx3p6_v3", "HLT_Mu40_eta2p1_Track60_dEdx3p7_v3" ]),                                                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                                                                                                                                                                         
        "SingleMu_193834-196531_2012B_Jul13": TaskDef(njobsIn= 1000, njobsOut= 100, triggerOR=["HLT_Mu5_v18","HLT_Mu8_v16","HLT_Mu12_v16","HLT_Mu17_v3","HLT_Mu12_eta2p1_L1Mu10erJetC12WdEtaPhi1DiJetsC_v3","HLT_Mu15_eta2p1_v3","HLT_Mu24_v14","HLT_Mu24_eta2p1_v3",                                                                                                                                                    
                                               "HLT_Mu30_v14","HLT_Mu30_eta2p1_v3","HLT_Mu40_v12","HLT_Mu40_eta2p1_v9","HLT_Mu50_eta2p1_v6","HLT_RelIso1p0Mu5_v4","HLT_RelIso1p0Mu20_v1","HLT_IsoMu15_eta2p1_L1ETM20_v5",                                                                                                                                                                                                
                                               "HLT_IsoMu20_eta2p1_v5","HLT_IsoMu24_v15","HLT_IsoMu24_eta2p1_v13","HLT_IsoMu30_v9","HLT_IsoMu30_eta2p1_v13","HLT_IsoMu34_eta2p1_v11","HLT_IsoMu40_eta2p1_v8",                                                                                                                                                                                                            
                                               "HLT_Mu40_eta2p1_Track50_dEdx3p6_v3","HLT_Mu40_eta2p1_Track60_dEdx3p7_v3"]),                                                                                                                                                                                                                                                                                              
        "SingleMu_198022-198523_2012C_Aug24": TaskDef(njobsIn= 490, njobsOut= 4, triggerOR=["HLT_Mu5_v19","HLT_Mu8_v17","HLT_Mu12_v17","HLT_Mu17_v4","HLT_Mu12_eta2p1_L1Mu10erJetC12WdEtaPhi1DiJetsC_v5", "HLT_Mu15_eta2p1_v4",                                                                                                                                                                                          
                                               "HLT_Mu24_v15", "HLT_Mu24_eta2p1_v4","HLT_Mu30_v15", "HLT_Mu30_eta2p1_v4", "HLT_Mu40_v13","HLT_Mu40_eta2p1_v10",                                                                                                                                                                                                                                                          
                                               "HLT_Mu50_eta2p1_v7", "HLT_RelIso1p0Mu5_v5", "HLT_RelIso1p0Mu20_v2", "HLT_IsoMu15_eta2p1_L1ETM20_v6", "HLT_IsoMu20_eta2p1_v6",                                                                                                                                                                                                                                            
                                               "HLT_IsoMu24_v16", "HLT_IsoMu24_eta2p1_v14", "HLT_IsoMu30_v10", "HLT_IsoMu30_eta2p1_v14", "HLT_IsoMu34_eta2p1_v12",                                                                                                                                                                                                                                                       
                                               "HLT_IsoMu40_eta2p1_v9", "HLT_Mu40_eta2p1_Track50_dEdx3p6_v4", "HLT_Mu40_eta2p1_Track60_dEdx3p7_v4" ]),                                                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                                                                                                                                                                         
        "SingleMu_198941-199608_2012C_Prompt": TaskDef(njobsIn= 490, njobsOut= 4, triggerOR=[ "HLT_Mu5_v19","HLT_Mu8_v17","HLT_Mu12_v17","HLT_Mu17_v4","HLT_Mu12_eta2p1_L1Mu10erJetC12WdEtaPhi1DiJetsC_v5",                                                                                                                                                                                                              
                                                "HLT_Mu15_eta2p1_L1Mu10erJetC12WdEtaPhi1DiJetsC_v1","HLT_Mu15_eta2p1_v4","HLT_Mu24_v15","HLT_Mu24_eta2p1_v4","HLT_Mu30_v15","HLT_Mu30_eta2p1_v4",                                                                                                                                                                                                                        
                                                "HLT_Mu40_v13","HLT_Mu40_eta2p1_v10","HLT_Mu50_eta2p1_v7","HLT_RelIso1p0Mu5_v5","HLT_RelIso1p0Mu20_v2","HLT_IsoMu15_eta2p1_L1ETM20_v6",                                                                                                                                                                                                                                  
                                                "HLT_IsoMu20_eta2p1_v6","HLT_IsoMu24_v16","HLT_IsoMu24_eta2p1_v14","HLT_IsoMu30_v10","HLT_IsoMu30_eta2p1_v14","HLT_IsoMu34_eta2p1_v12",                                                                                                                                                                                                                                  
                                                "HLT_IsoMu40_eta2p1_v9","HLT_Mu40_eta2p1_Track50_dEdx3p6_v4","HLT_Mu40_eta2p1_Track60_dEdx3p7_v4",                                                                                                                                                                                                                                                                       
]),                                                                                                                                                                                                                                                                                                                                                                                                                      
        "SingleMu_199698-202504_2012C_Prompt": TaskDef(njobsIn= 1000, njobsOut= 100, triggerOR=[ "HLT_Mu5_v20","HLT_Mu8_v18","HLT_Mu12_v18","HLT_Mu17_v5","HLT_Mu12_eta2p1_L1Mu10erJetC12WdEtaPhi1DiJetsC_v6",                                                                                                                                                                                                           
                                                "HLT_Mu15_eta2p1_L1Mu10erJetC12WdEtaPhi1DiJetsC_v2","HLT_Mu15_eta2p1_v5","HLT_Mu24_v16","HLT_Mu24_eta2p1_v5","HLT_Mu30_v16","HLT_Mu30_eta2p1_v5",                                                                                                                                                                                                                        
                                                "HLT_Mu40_v14","HLT_Mu40_eta2p1_v11","HLT_Mu50_eta2p1_v8","HLT_RelIso1p0Mu5_v6","HLT_RelIso1p0Mu20_v3","HLT_IsoMu15_eta2p1_L1ETM20_v7",                                                                                                                                                                                                                                  
                                                "HLT_IsoMu20_eta2p1_v7","HLT_IsoMu24_v17","HLT_IsoMu24_eta2p1_v15","HLT_IsoMu30_v11","HLT_IsoMu30_eta2p1_v15","HLT_IsoMu34_eta2p1_v13",                                                                                                                                                                                                                                  
                                                "HLT_IsoMu40_eta2p1_v10","HLT_Mu40_eta2p1_Track50_dEdx3p6_v5","HLT_Mu40_eta2p1_Track60_dEdx3p7_v5"]),                                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                                                                                                                                                                         
        "SingleMu_202970-203742_2012C_Prompt": TaskDef(njobsIn= 490, njobsOut= 4, triggerOR=[ "HLT_Mu5_v20","HLT_Mu8_v18","HLT_Mu12_v18","HLT_Mu17_v5","HLT_Mu12_eta2p1_L1Mu10erJetC12WdEtaPhi1DiJetsC_v7", "HLT_Mu15_eta2p1_v5",                                                                                                                                                                                        
                                               "HLT_Mu24_v16", "HLT_Mu24_eta2p1_v5","HLT_Mu30_v16", "HLT_Mu30_eta2p1_v5", "HLT_Mu40_v14","HLT_Mu40_eta2p1_v11",                                                                                                                                                                                                                                                          
                                               "HLT_Mu50_eta2p1_v8", "HLT_RelIso1p0Mu5_v6", "HLT_RelIso1p0Mu20_v3", "HLT_IsoMu15_eta2p1_L1ETM20_v7", "HLT_IsoMu20_eta2p1_v7",                                                                                                                                                                                                                                            
                                               "HLT_IsoMu24_v17", "HLT_IsoMu24_eta2p1_v15", "HLT_IsoMu30_v11", "HLT_IsoMu30_eta2p1_v15", "HLT_IsoMu34_eta2p1_v13",                                                                                                                                                                                                                                                       
                                               "HLT_IsoMu40_eta2p1_v10", "HLT_Mu40_eta2p1_Track50_dEdx3p6_v5", "HLT_Mu40_eta2p1_Track60_dEdx3p7_v5"]),                                                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                                                                                                                                                                         
                                                                                                                                                                                                                                                                                                                                                                                                                         
        "SingleMu_203777-208686_2012D_Prompt": TaskDef(njobsIn= 2000, njobsOut= 200, triggerOR=[ "HLT_Mu5_v20","HLT_Mu8_v18","HLT_Mu12_v18","HLT_Mu17_v5","HLT_Mu12_eta2p1_L1Mu10erJetC12WdEtaPhi1DiJetsC_v7", "HLT_Mu15_eta2p1_v5",                                                                                                                                                                                     
                                               "HLT_Mu24_v16", "HLT_Mu24_eta2p1_v5","HLT_Mu30_v16", "HLT_Mu30_eta2p1_v5", "HLT_Mu40_v14","HLT_Mu40_eta2p1_v11",                                                                                                                                                                                                                                                          
                                               "HLT_Mu50_eta2p1_v8", "HLT_RelIso1p0Mu5_v6", "HLT_RelIso1p0Mu20_v3", "HLT_IsoMu15_eta2p1_L1ETM20_v7", "HLT_IsoMu20_eta2p1_v7",                                                                                                                                                                                                                                            
                                               "HLT_IsoMu24_v17", "HLT_IsoMu24_eta2p1_v15", "HLT_IsoMu30_v11", "HLT_IsoMu30_eta2p1_v15", "HLT_IsoMu34_eta2p1_v13",                                                                                                                                                                                                                                                       
                                               "HLT_IsoMu40_eta2p1_v10", "HLT_Mu40_eta2p1_Track50_dEdx3p6_v5", "HLT_Mu40_eta2p1_Track60_dEdx3p7_v5" ]),
                                                                                                                                     
#        "MultiJet_190456-190738_2012A_Jul13":  TaskDef(njobsIn=  35, njobsOut=  1, triggerOR=["HLT_QuadJet80_v1"]),
#        "MultiJet_190782-190949_2012A_Aug06":  TaskDef(njobsIn=  10, njobsOut=  1, triggerOR=["HLT_QuadJet80_v2"]),
#        "MultiJet_191043-193621_2012A_Jul13":  TaskDef(njobsIn= 150, njobsOut=  3, triggerOR=["HLT_QuadJet80_v2"]),
#        "MultiJet_193834-194225_2012B_Jul13":  TaskDef(njobsIn=2000, njobsOut= 20, triggerOR=["HLT_QuadJet80_v2"]),        
#        "MultiJet_194270-196531_2012B_Jul13":  TaskDef(njobsIn= 200, njobsOut=  2, triggerOR=["HLT_QuadJet80_v2","HLT_QuadJet80_v3"]),
#        "MultiJet_198022-198523_2012C_Aug24": TaskDef(njobsIn=1500, njobsOut= 10, triggerOR=["HLT_QuadJet80_v4","HLT_QuadJet80_v6"]),
#        "MultiJet_198941-200601_2012C_Prompt": TaskDef(njobsIn=1500, njobsOut= 12, triggerOR=["HLT_QuadJet80_v4","HLT_QuadJet80_v6"]),
#        "MultiJet_200961-202504_2012C_Prompt": TaskDef(njobsIn= 150, njobsOut=  1, triggerOR=["HLT_QuadJet80_v6"]),
#        "MultiJet_202792-203742_2012C_Prompt": TaskDef(njobsIn= 150, njobsOut=  1, triggerOR=["HLT_QuadJet80_v6"]),


        "QCD_Pt30to50_TuneZ2star_Summer12":       TaskDefMC(njobsIn= 20, njobsOut=1),
        "QCD_Pt50to80_TuneZ2star_Summer12":       TaskDefMC(njobsIn= 20, njobsOut=1),
        "QCD_Pt80to120_TuneZ2star_Summer12":      TaskDefMC(njobsIn= 20, njobsOut=1),
        "QCD_Pt120to170_TuneZ2star_Summer12":     TaskDefMC(njobsIn= 40, njobsOut=1),
        "QCD_Pt170to300_TuneZ2star_Summer12":     TaskDefMC(njobsIn= 80, njobsOut=2),
        "QCD_Pt170to300_TuneZ2star_v2_Summer12":  TaskDefMC(njobsIn=300, njobsOut=6),
        "QCD_Pt300to470_TuneZ2star_Summer12":     TaskDefMC(njobsIn=250, njobsOut=4),
        "QCD_Pt300to470_TuneZ2star_v2_Summer12":  TaskDefMC(njobsIn=150, njobsOut=3),
        "QCD_Pt300to470_TuneZ2star_v3_Summer12":  TaskDefMC(njobsIn=850, njobsOut=14),
        
        "WW_TuneZ2star_Summer12":                 TaskDefMC(njobsIn=150, njobsOut= 8),
        "WZ_TuneZ2star_Summer12":                 TaskDefMC(njobsIn=150, njobsOut= 8),
        "ZZ_TuneZ2star_Summer12":                 TaskDefMC(njobsIn=150, njobsOut= 8),
        "TTJets_TuneZ2star_Summer12":             TaskDefMC(njobsIn=700, njobsOut=30),
        "WJets_TuneZ2star_v1_Summer12":           TaskDefMC(njobsIn=100, njobsOut= 4, args={"wjetsWeighting": 1}),
        "WJets_TuneZ2star_v2_Summer12":           TaskDefMC(njobsIn=250, njobsOut= 8, args={"wjetsWeighting": 1}),
        "W1Jets_TuneZ2star_Summer12":             TaskDefMC(njobsIn=150, njobsOut= 8, args={"wjetsWeighting": 1}),
        "W2Jets_TuneZ2star_Summer12":             TaskDefMC(njobsIn=400, njobsOut=20, args={"wjetsWeighting": 1}),
        "W3Jets_TuneZ2star_Summer12":             TaskDefMC(njobsIn=490, njobsOut=20, args={"wjetsWeighting": 1}),
        "W4Jets_TuneZ2star_Summer12":             TaskDefMC(njobsIn=550, njobsOut=30, args={"wjetsWeighting": 1}),
        "DYJetsToLL_M50_TuneZ2star_Summer12":     TaskDefMC(njobsIn=350, njobsOut= 6),
        "DYJetsToLL_M10to50_TuneZ2star_Summer12": TaskDefMC(njobsIn= 40, njobsOut= 1),
        "T_t-channel_TuneZ2star_Summer12":        TaskDefMC(njobsIn= 50, njobsOut= 2),
        "Tbar_t-channel_TuneZ2star_Summer12":     TaskDefMC(njobsIn= 50, njobsOut= 1),
        "T_tW-channel_TuneZ2star_Summer12":       TaskDefMC(njobsIn= 20, njobsOut= 2),
        "Tbar_tW-channel_TuneZ2star_Summer12":    TaskDefMC(njobsIn= 20, njobsOut= 2),
        "T_s-channel_TuneZ2star_Summer12":        TaskDefMC(njobsIn= 10, njobsOut= 1),
        "Tbar_s-channel_TuneZ2star_Summer12":     TaskDefMC(njobsIn= 10, njobsOut= 1),
 
        }

    workflowName = "triggerQuadJet_skim_"+version
    
    # Update the default definitions from the argument                                                                                                                 
    updateTaskDefinitions(defaultDefinitions, updateDefinitions)                                                                                                       
    
    # Add pattuple Workflow for each dataset                                                                                                                           
    for datasetName, taskDef in defaultDefinitions.iteritems():                                                                                                        
        dataset = datasets.getDataset(datasetName)                                                                                                                     
        
        # Construct processing workflow                                                                                                                                
        wf = constructProcessingWorkflow_53X(dataset, taskDef, sourceWorkflow="AOD", workflowName=workflowName, skimConfig=skim)                                
        
        # Setup the publish name                                                                                                                                       
        name = updatePublishName(dataset, wf.source.getDataForDataset(dataset).getDatasetPath(), workflowName)                                                  
        wf.addCrabLine("USER.publish_data_name = "+name)                                                                                                               
        
        # For MC, split by events, for data, split by lumi                                                                                                             
        if dataset.isMC():                                                                                                                                             
            wf.addCrabLine("CMSSW.total_number_of_events = -1")                                                                                                        
        else:                                                                                                                                                          
            wf.addCrabLine("CMSSW.total_number_of_lumis = -1")                                                                                                         
            
            # Add the pattuple Workflow to Dataset                                                                                                                         
        dataset.addWorkflow(wf)                                                                                                                                        
            # If DBS-dataset of the pattuple has been specified, add also analysis Workflow to Dataset                                                                     
        if wf.output != None:                                                                                                                                          
            commonArgs = {                                                                                                                                             
                "source": Source(workflowName),
                "args": wf.args,
                "skimConfig": skim
                }
            commonArgs["args"]["trgAnalysis"] = "QuadJet"
            
            if dataset.isData():                                                                                                                                       
                # For data, construct one analysis workflow per trigger type                                                                                           
                pd = datasetName.split("_")[0]                                                                                                                         
                if pd == "SingleMu":
                    dataset.addWorkflow(Workflow("triggerQuadJet_analysis_"+version, triggerOR=wf.triggerOR, **commonArgs))                                                    
#                elif pd == "MultiJet":                                                                                                                                 
#                    if datasetName in quadJetTriggers:                                                                                                                 
#                        dataset.addWorkflow(Workflow("analysis_quadjetleg_"+version, triggerOR=quadJetTriggers[datasetName], **commonArgs))                               
#                    if datasetName in quadJetBTagTriggers:                                                                                                             
#                                dataset.addWorkflow(Workflow("analysis_quadjetbtag_"+version, triggerOR=quadJetBTagTriggers[datasetName], **commonArgs))                       
#                    if datasetName in quadPFJetBTagTriggers:                                                                                                     
#                                    dataset.addWorkflow(Workflow("analysis_quadpfjetbtag_"+version, triggerOR=quadPFJetBTagTriggers[datasetName], **commonArgs))               
                else:                                                                                                                                          
                    raise Exception("Unsupported PD name %s" % pd)                                                                                             
            else:                                                                                                                                          
                # For MC, also construct one analysis workflow per trigger type                                                                            
                dataset.addWorkflow(Workflow("triggerQuadJet_analysis_"+version, triggerOR=[mcTriggerSingleMu], **commonArgs))
                    
def addQuadJetSkim_53X_v3(datasets):
    dataDefinitions = {
#        "MultiJet_190456-190738_2012A_Jul13":     TaskDef(""),
#        "MultiJet_190456-190738_2012A_Jul13":     TaskDef(""),
#        "MultiJet_190782-190949_2012A_Aug06":     TaskDef(""),
#        "MultiJet_191043-193621_2012A_Jul13":     TaskDef(""),
#        "MultiJet_193834-194225_2012B_Jul13":     TaskDef(""),
#        "MultiJet_194270-196531_2012B_Jul13":     TaskDef(""),
#        "MultiJet_198022-198523_2012C_Aug24":     TaskDef(""),
#        "MultiJet_198941-200601_2012C_Prompt":    TaskDef(""),
#        "MultiJet_200961-202504_2012C_Prompt":    TaskDef(""),
#        "MultiJet_202792-203742_2012C_Prompt":    TaskDef(""),

	"SingleMu_190456-190738_2012A_Jul13":     TaskDef(""),
	"SingleMu_190782-190949_2012A_Aug06":     TaskDef(""),
	"SingleMu_191043-193621_2012A_Jul13":     TaskDef(""),
	"SingleMu_193834-196531_2012B_Jul13":     TaskDef(""),
	"SingleMu_198022-198523_2012C_Aug24":     TaskDef(""),
#	"SingleMu_198941-203742_2012C_Prompt":    TaskDef(""),
	"SingleMu_198941-199608_2012C_Prompt":    TaskDef(""),
	"SingleMu_199698-202504_2012C_Prompt":    TaskDef(""),
	"SingleMu_202970-203742_2012C_Prompt":    TaskDef(""),
	"SingleMu_203777-208686_2012D_Prompt":    TaskDef(""),
    }
    mcDefinitions = {
        "QCD_Pt30to50_TuneZ2star_Summer12":       TaskDef(""),                               
        "QCD_Pt50to80_TuneZ2star_Summer12":       TaskDef(""),                               
        "QCD_Pt80to120_TuneZ2star_Summer12":      TaskDef(""),                               
        "QCD_Pt120to170_TuneZ2star_Summer12":     TaskDef(""),                               
        "QCD_Pt170to300_TuneZ2star_Summer12":     TaskDef(""),                               
        "QCD_Pt170to300_TuneZ2star_v2_Summer12":  TaskDef(""),                               
        "QCD_Pt300to470_TuneZ2star_Summer12":     TaskDef(""),                               
        "QCD_Pt300to470_TuneZ2star_v2_Summer12":  TaskDef(""),                               
        "QCD_Pt300to470_TuneZ2star_v3_Summer12":  TaskDef(""),                               
        
        "WW_TuneZ2star_Summer12":                 TaskDef(""),                               
        "WZ_TuneZ2star_Summer12":                 TaskDef(""),                               
        "ZZ_TuneZ2star_Summer12":                 TaskDef(""),                               
        "TTJets_TuneZ2star_Summer12":             TaskDef(""),                               
        "WJets_TuneZ2star_v1_Summer12":           TaskDef(""),                               
        "WJets_TuneZ2star_v2_Summer12":           TaskDef(""),                               
        "W1Jets_TuneZ2star_Summer12":             TaskDef(""),                               
        "W2Jets_TuneZ2star_Summer12":             TaskDef(""),                               
        "W3Jets_TuneZ2star_Summer12":             TaskDef(""),                               
        "W4Jets_TuneZ2star_Summer12":             TaskDef(""),                               
        "DYJetsToLL_M50_TuneZ2star_Summer12":     TaskDef(""),                               
        "DYJetsToLL_M10to50_TuneZ2star_Summer12": TaskDef(""),                               
        "T_t-channel_TuneZ2star_Summer12":        TaskDef(""),                               
        "Tbar_t-channel_TuneZ2star_Summer12":     TaskDef(""),                               
        "T_tW-channel_TuneZ2star_Summer12":       TaskDef(""),                               
        "Tbar_tW-channel_TuneZ2star_Summer12":    TaskDef(""),                               
        "T_s-channel_TuneZ2star_Summer12":        TaskDef(""),                               
        "Tbar_s-channel_TuneZ2star_Summer12":     TaskDef(""),                               
        }

    # Switch GlobalTag for MC to match to prompt reco
    tmp = TaskDef(dataVersionAppend="prompt")
    for n, td in mcDefinitions.iteritems():
        td.update(tmp)
    dataDefinitions.update(mcDefinitions)
    
    addQuadJetSkim_53X("v53_v3", datasets, dataDefinitions) 
    
