import ROOT

fInput1 = ROOT.TFile("ws_signal.root")
fInput1.cd()

workspace1 = fInput1.Get("myworkspace")

mass = workspace1.var("Memu")
sigPDF = workspace1.pdf("sigPDF")

#data = workspace.data("dataset")
fInput2 = ROOT.TFile("ws_bkg.root")
fInput2.cd()

workspace2 = fInput2.Get("myworkspace")

mass = workspace2.var("Memu")
bkgPDF = workspace2.pdf("bkgPDF")

frac = ROOT.RooRealVar("frac","Fraction of signal",0.1,0.,1.)


br_rat = ROOT.RooRealVar("br_rat","branching ratio",1.,0.00001,5.)
lumi = ROOT.RooRealVar("lumi","The luminosity",59.74)
cross_sig = ROOT.RooRealVar("cross_sig","cross section", 2075./0.0336)
Nsig_form = ROOT.RooFormulaVar("Nsig_form","@0*@1*@2",ROOT.RooArgList(br_rat,cross_sig,lumi))

#fileInput = ROOT.TFile("MC_Data.root")
#fileInput.cd()
#tree = fileInput.Get("Cumulative_Events")

#dataset = ROOT.RooDataSet("dataset","dataset",ROOT.RooArgSet(mass),ROOT.RooFit.Import(tree))

finalPDF = ROOT.RooAddPdf("finalPDF","The total PDF",ROOT.RooArgList(sigPDF,bkgPDF),ROOT.RooArgList(Nsig_form))

dataset = finalPDF.generate(ROOT.RooArgSet(mass),50491)

finalPDF.fitTo(dataset)

massplot = mass.frame(50)
#data.plotOn(massplot)
dataset.plotOn(massplot)
finalPDF.plotOn(massplot)
#sigPDF.plotOn(massplot)
#bkgPDF.plotOn(massplot)



#canvas = ROOT.TCanvas()
#canvas.cd()
#massplot.Draw()
#canvas.SaveAs("exercise_3.png")


c1 = ROOT.TCanvas()
c1.cd()
massplot.Draw()
c1.SaveAs("totalfit.pdf")

#Create Workspace
workspace = ROOT.RooWorkspace("myworkspace")
getattr(workspace,'import')(finalPDF)

fOut = ROOT.TFile("ws_final.root","RECREATE")
fOut.cd()
workspace.Write()
fOut.Close()
