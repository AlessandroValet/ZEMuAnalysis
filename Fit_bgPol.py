import ROOT


mass = ROOT.RooRealVar("Memu","Memu",75.,120.,"GeV/c^2")

mass.setRange("LowSideband",75.,85.)
mass.setRange("HighSideband",95.,120.)

a_bkg = ROOT.RooRealVar("a_bkg","a_bkg",-0.8,-3.,3.)
b_bkg = ROOT.RooRealVar("b_bkg","b_bkg",0.3,-3.,3.)
c_bkg = ROOT.RooRealVar("c_bkg","c_bkg",-0.2,-3.,3.)
d_bkg = ROOT.RooRealVar("d_bkg","d_bkg",-0.02,-3.,3.)
e_bkg = ROOT.RooRealVar("e_bkg","e_bkg",0.,-10.,10.)
f_bkg = ROOT.RooRealVar("f_bkg","f_bkg",0.,-10.,10.)
g_bkg = ROOT.RooRealVar("g_bkg","g_bkg",0.,-10.,10.)

bkgPDF = ROOT.RooChebychev("bkgPDF","bkgPDF",mass,ROOT.RooArgList(a_bkg,b_bkg,c_bkg))

fileInput = ROOT.TFile("Data_2018.root")
fileInput.cd()
tree = fileInput.Get("Cumulative_Events")

dataset = ROOT.RooDataSet("dataset","dataset",ROOT.RooArgSet(mass),ROOT.RooFit.Import(tree))

bkgPDF.fitTo(dataset,ROOT.RooFit.Range("LowSideband,HighSideband"))



data_blinded = dataset.reduce("Memu < 84.9 || Memu > 95.7") #sistem
xframe = mass.frame(50)
data_blinded.plotOn(xframe)
#dataset.plotOn(xframe)
bkgPDF.plotOn(xframe,ROOT.RooFit.Range("LowSideband,HighSideband"))

#xframe.chiSquare("bkgPDF")

c1 = ROOT.TCanvas()
c1.cd()
xframe.Draw()
c1.SaveAs("fitdataPol.pdf")

print xframe.chiSquare()

#create Workspace
workspace = ROOT.RooWorkspace("myworkspace")
getattr(workspace,'import')(bkgPDF)

fOut = ROOT.TFile("ws_bkg.root","RECREATE")
fOut.cd()
workspace.Write()
fOut.Close()



del workspace 
