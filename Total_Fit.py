#0.00005,-0.0001,0.001 pval 2.99 significance
#4.21333479717 with 5k, 2.07884308591 with 2.5k, 2.691420335 with 3.5k, 2.71 with 4k, 3.4484983839 with 4.5k, 3.08356767271 with 4250

import ROOT
import math

#some testing numbers 

discovery_scale = 1. 
base_lum = 59.74
base_num = 7895

lum = discovery_scale * base_lum
numb_gen = discovery_scale * base_num

#pdf extraction from ws

fInput1 = ROOT.TFile("ws_signal.root")
fInput1.cd()
workspace1 = fInput1.Get("myworkspace")

sigPDF = workspace1.pdf("sigPDF")

fInput2 = ROOT.TFile("ws_bkg.root")
fInput2.cd()
workspace2 = fInput2.Get("myworkspace")

mass = workspace2.var("Memu")
bkgPDF = workspace2.pdf("bkgPDF")

#Br and event number for alternative method

Bree = ROOT.RooRealVar("Bree","Branching ratio Zee", 0.033632)
Brmumu = ROOT.RooRealVar("Brmumu","Branching ratio Zmumu", 0.033662)
Nmumu = ROOT.RooRealVar("Nmumu","Nmumu", 1.95572e+07)
Nee = ROOT.RooRealVar("Nee","Nee", 7.17908e+06)

#fraction of signal and Number of event components

#frac = ROOT.RooRealVar("frac","Fraction of signal",0.1,0.,1.)
br_rat = ROOT.RooRealVar("br_rat","branching ratio",0.00000001,-0.0001,0.0001) #-6  0.000001,-0.0001,0.0001 / 3.16851793943 sigma with 0.000051,0.000001,0.001 
lumi = ROOT.RooRealVar("lumi","The luminosity",59.74)
efficiency = ROOT.RooRealVar("efficiency","global efficiency", 0.12, 0., 1.)
efficiency_error = ROOT.RooRealVar("efficiency_error","global efficiency error", 0.06)
cross_sig = ROOT.RooRealVar("cross_sig","cross section", 1000.*2075./0.0336) 

#systematic uncertainty

globaleff = ROOT.RooRealVar("globaleff","dummy eff",0.12,0.,3.)
globaleff.setConstant(1)
#efficiency.setConstant(1)
#syst_eff = ROOT.RooRealVar("syst","The systematic uncertainty",0.05)  #5% uncertainty
#effsys_error = ROOT.RooFormulaVar("effsys_error","@0*@1",ROOT.RooArgList(efficiency_error,syst_eff))

Gausseff = ROOT.RooGaussian("Gausseff","efficiency smearing",globaleff,efficiency,efficiency_error)

#Nsig formula standard and alternative method

Nsig_form = ROOT.RooFormulaVar("Nsig_form","@0*@1*@2*@3",ROOT.RooArgList(br_rat,cross_sig,lumi,efficiency))
#Nsig_form = ROOT.RooFormulaVar("Nemu_Extracted","@0*sqrt((@1*@2)/(@3*@4))",ROOT.RooArgList(br_rat,Nee,Nmumu,Bree,Brmumu))

Nbkg = ROOT.RooRealVar("Nbkg","Number of background events",7890.,5000.,10000.)

#create finalPDF without systematics

finalPDFwosys = ROOT.RooAddPdf("finalPDFwosys","The total PDF",ROOT.RooArgList(sigPDF,bkgPDF),ROOT.RooArgList(Nsig_form,Nbkg))

#generate dataset
dataset = finalPDFwosys.generate(ROOT.RooArgSet(mass),numb_gen)
dataset.SetName("dataset")

#add systematics

finalPDF= ROOT.RooProdPdf("finalPDF","finalPDF", ROOT.RooArgList(finalPDFwosys,Gausseff))
finalPDF.fitTo(dataset,ROOT.RooFit.Extended(1), ROOT.RooFit.Constrain(ROOT.RooArgSet(efficiency))) #ROOT.RooFit.Extended(1),

#finalPDFwosys.fitTo(dataset, ROOT.RooFit.Extended(1))


#plotting&saving on workspace

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
