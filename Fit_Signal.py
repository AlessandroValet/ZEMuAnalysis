import ROOT

mass = ROOT.RooRealVar("Memu","memu",91.,75.,120.,"GeV/c^2")

mean = ROOT.RooRealVar("mean","mean",91.,75.,110.)
sigma = ROOT.RooRealVar("sigma","sigma",3.,0.1,6.)
alpha = ROOT.RooRealVar("alpha","alpha",1.,0.1,10.)
enne = ROOT.RooRealVar("enne","enne",2.,0.1,20.)


signalPDF = ROOT.RooCBShape("signalPDF","signalPDF",mass,mean,sigma,alpha,enne)


meangauss = ROOT.RooRealVar("meangauss","The mean of the gaussian",85.,75.,110.)
widthgauss = ROOT.RooRealVar("widthgauss","The width of the gaussian",7.,0.1,10.)

gaussPDF = ROOT.RooGaussian("gaussPDF","The gaussian function",mass,meangauss,widthgauss)


frac_sign = ROOT.RooRealVar("frac_sign","Fraction of signal",0.6,0.,1.)

sigPDF = ROOT.RooAddPdf("sigPDF","The total PDF",ROOT.RooArgList(signalPDF,gaussPDF),ROOT.RooArgList(frac_sign))




fileInput = ROOT.TFile("Signal_2018.root")
fileInput.cd()
tree = fileInput.Get("Cumulative_Events")

dataset = ROOT.RooDataSet("dataset","dataset",ROOT.RooArgSet(mass),ROOT.RooFit.Import(tree))


sigPDF.fitTo(dataset)

alpha.setConstant(ROOT.kTRUE)
enne.setConstant(ROOT.kTRUE)
sigma.setConstant(ROOT.kTRUE)
mean.setConstant(ROOT.kTRUE)
frac_sign.setConstant(ROOT.kTRUE)
meangauss.setConstant(ROOT.kTRUE)
widthgauss.setConstant(ROOT.kTRUE)


xframe = mass.frame(45)
dataset.plotOn(xframe)
sigPDF.plotOn(xframe)
xframe.SetTitle("")
xframe.GetXaxis().SetTitle("m_{K^{+}K^{-}#gamma} [GeV]")
xframe.GetXaxis().SetRangeUser(0.,170.)

print xframe.chiSquare()

c1 = ROOT.TCanvas()
c1.cd()
c1.SetTitle("")
xframe.Draw()
c1.SaveAs("fitsignal.pdf")

#create Workspace
workspace = ROOT.RooWorkspace("myworkspace")
getattr(workspace,'import')(sigPDF)

fOut = ROOT.TFile("ws_signal.root","RECREATE")
fOut.cd()
workspace.Write()
fOut.Close()

del workspace 
