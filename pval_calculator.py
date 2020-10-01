import ROOT
#ROOT.gROOT.ProcessLineSync(".L dCB/RooDoubleCBFast.cc+")

#Get model and data
fInputPDF = ROOT.TFile("ws_final.root")
workspace = fInputPDF.Get("myworkspace")
workspace.Print()

#Define parameter of interest
br_rat = workspace.var("br_rat")
poi = ROOT.RooArgSet(br_rat)

#Define observables
mass = workspace.var("Memu")

observables = ROOT.RooArgSet()
observables.add(mass)

model = ROOT.RooStats.ModelConfig(workspace)
model.SetObservables(observables)
model.SetPdf("finalPDF")

#Null Hypo
nullParams = poi.snapshot()
nullParams.setRealValue("br_rat",0.)

#Build profile likelihood calculator: performs scan of the likelihood ratio
plc = ROOT.RooStats.ProfileLikelihoodCalculator()

#dataset = ROOT.RooDataSet("dataset","dataset",ROOT.RooArgSet(mass),ROOT.RooFit.Import(mytree)) #sistema input data
dataset = workspace.data("dataset")

plc.SetData(dataset)
plc.SetModel(model)
plc.SetParameters(poi)
plc.SetNullParameters(nullParams)

#The the Hypotest result
htr = plc.GetHypoTest()

print "-------------------------------------------------"
print "The p-value for the null is ", htr.NullPValue()
print "Corresponding to a signifcance of ", htr.Significance()
print "-------------------------------------------------"

#PyROOT sometimes fails cleaning memory, this helps
del plc
