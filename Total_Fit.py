import ROOT

fInput1 = ROOT.TFile("ws_signal.root")
fInput1.cd()

workspace1 = fInput1.Get("myworkspace")

sigPDF = workspace1.pdf("sigPDF")


fInput2 = ROOT.TFile("ws_bkg.root")
fInput2.cd()

workspace2 = fInput2.Get("myworkspace")
mass = workspace2.var("Memu")

bkgPDF = workspace2.pdf("bkgPDF")

frac = ROOT.RooRealVar("frac","Fraction of signal",0.1,0.,1.)


br_rat = ROOT.RooRealVar("br_rat","branching ratio",0.000001,-0.0001,0.0000001) #-6  0.000001,-0.0001,0.0000001 / 0.0001,0.000001,0.001
lumi = ROOT.RooRealVar("lumi","The luminosity",59.74)
cross_sig = ROOT.RooRealVar("cross_sig","cross section", 2075./0.0336)
Nsig_form = ROOT.RooFormulaVar("Nsig_form","@0*@1*@2",ROOT.RooArgList(br_rat,cross_sig,lumi))

Nbkg = ROOT.RooRealVar("Nbkg","Number of background events",7890.,5000.,10000.)

finalPDF = ROOT.RooAddPdf("finalPDF","The total PDF",ROOT.RooArgList(sigPDF,bkgPDF),ROOT.RooArgList(Nsig_form,Nbkg))

dataset = finalPDF.generate(ROOT.RooArgSet(mass),7895)
dataset.SetName("dataset")


finalPDF.fitTo(dataset)

massplot = mass.frame(50)

dataset.plotOn(massplot)
finalPDF.plotOn(massplot)



c1 = ROOT.TCanvas()
c1.cd()
massplot.Draw()
c1.SaveAs("totalfit.pdf")

#Create Workspace
workspace = ROOT.RooWorkspace("myworkspace")
getattr(workspace,'import')(finalPDF)
getattr(workspace,'import')(dataset)

fOut = ROOT.TFile("ws_final.root","RECREATE")
fOut.cd()
workspace.Write()
fOut.Close()

del workspace 
