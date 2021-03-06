import ROOT

fInputPDF = ROOT.TFile("ws_final.root")
ws = fInputPDF.Get("myworkspace")
ws.Print()

br_rat = ws.var("br_rat")
poi_list = ROOT.RooArgSet(br_rat)
mass = ws.var("Memu")
obs_list = ROOT.RooArgSet(ws.var("Memu"))
data = ws.data("dataset")

ws.Print()

nuisance_params = ROOT.RooArgSet()
nuisance_params.add(ws.var("a_bkg"))
nuisance_params.add(ws.var("b_bkg"))
nuisance_params.add(ws.var("c_bkg"))
nuisance_params.add(ws.var("Nbkg"))
nuisance_params.add(ws.var("efficiency"))

glb_list = ROOT.RooArgSet()
glb_list.add(ws.var("globaleff"))


#Set the RooModelConfig and let it know what the content of the workspace is about
model = ROOT.RooStats.ModelConfig()
model.SetWorkspace(ws)
model.SetPdf("finalPDF")
model.SetParametersOfInterest(poi_list)
model.SetObservables(obs_list)
model.SetNuisanceParameters(nuisance_params)
model.SetGlobalObservables(glb_list)
model.SetName("S+B Model")
model.SetProtoData(data)



print "model set!"

bModel = model.Clone()
bModel.SetName("B model")
oldval = poi_list.find("br_rat").getVal()
poi_list.find("br_rat").setVal(0) #BEWARE that the range of the POI has to contain zero! -> signal is suppressed
bModel.SetSnapshot(poi_list)
poi_list.find("br_rat").setVal(oldval)

fc = ROOT.RooStats.AsymptoticCalculator(data, bModel, model)
fc.SetOneSided(1)

#Create hypotest inverter passing desired calculator
calc = ROOT.RooStats.HypoTestInverter(fc)
calc.SetConfidenceLevel(0.95)

#Use CLs
calc.UseCLs(1)
calc.SetVerbose(0)
#Configure ToyMC sampler
toymc = fc.GetTestStatSampler()
#Set profile likelihood test statistics
profl = ROOT.RooStats.ProfileLikelihoodTestStat(model.GetPdf())
#For CLs (bounded intervals) use one-sided profile likelihood
profl.SetOneSided(1)
#Set the test statistic to use
toymc.SetTestStatistic(profl)

npoints = 100 #Number of points to scan
# min and max for the scan (better to choose smaller intervals)
poimin = poi_list.find("br_rat").getMin()
poimax = poi_list.find("br_rat").getMax()

min_scan = 10**(-12) #sistemare
max_scan = 10**(-5)
print "Doing a fixed scan  in interval : ",min_scan, " , ", max_scan
calc.SetFixedScan(npoints,min_scan,max_scan)
#calc.SetAutoScan()

# In order to use PROOF, one should install the test statistic on the workers
# pc = ROOT.RooStats.ProofConfig(workspace, 0, "workers=6",0)
# toymc.SetProofConfig(pc)

result = calc.GetInterval() #This is a HypoTestInveter class object

upperLimit = result.UpperLimit()

print "################"
print "The observed CLs upper limit is: ", upperLimit

##################################################################

#Compute expected limit
print "Expected upper limits, using the B (alternate) model : "
print " expected limit (median) ", result.GetExpectedUpperLimit(0)
print " expected limit (-1 sig) ", result.GetExpectedUpperLimit(-1)
print " expected limit (+1 sig) ", result.GetExpectedUpperLimit(1)
print "################"



del fc
