import ROOT
import copy
import sys

ROOT.gROOT.SetBatch(True)   

list_inputfiles = []

#check inputfiles before loading, debug

i=0
for filename in sys.argv[1:]:
    list_inputfiles.append(filename)
    print "inputfiles =", list_inputfiles[i]
    i=i+1

hstack  = dict()
hsignal = dict()
hdata   = dict()
canvas  = dict()
histo_container = [] #just for memory management

list_histos = ["h_Memu","h_Mueta", "h_Mupt", "h_Muphi", "h_Eeta", "h_Ept", "h_Ephi", "h_PuppiMETphi", "h_PuppiMETpt", "h_Jetpt", "h_IsoMu"]

for hname in list_histos:
    hstack[hname] = ROOT.THStack("hstack_" + hname,"")

colors_mask = dict()
colors_mask["ttbarlnu"]            = ROOT.kAzure+7
colors_mask["DY50"]                = ROOT.kViolet-6
colors_mask["WW"]                  = ROOT.kPink+1
colors_mask["SingleAntiTop"]       = ROOT.kYellow-8 #
colors_mask["SingleTop"]           = ROOT.kMagenta+1
colors_mask["ttbarHadronic"]       = ROOT.kBlue-7
colors_mask["ttbarSemileptonic"]   = ROOT.kOrange-3

leg1 = ROOT.TLegend(0.6868687,0.6120093,0.9511784,0.9491917) #right positioning
leg1.SetHeader(" ")
leg1.SetFillColor(0)
leg1.SetBorderSize(1)
leg1.SetLineColor(1)
leg1.SetLineStyle(1)
leg1.SetLineWidth(1)
leg1.SetFillStyle(1001)



for filename in list_inputfiles:
    fileIn = ROOT.TFile(filename)

    sample_name = filename.split("_")[0]
    for histo_name in list_histos:
        histo = fileIn.Get(histo_name)


        histo_container.append(copy.copy(histo))
        #print sample_name    print samplename to check for cycle, debug

        if "Signal" in sample_name:               #drawing parameters
            histo_container[-1].SetLineStyle(2)   #dashed
            histo_container[-1].SetLineColor(2)   #red
            histo_container[-1].SetLineWidth(4)   #kind of thick
            hsignal[histo_name] = histo_container[-1]

        elif "Data" in sample_name:
            histo_container[-1].SetMarkerStyle(20)   #point
            hdata[histo_name] = histo_container[-1]
            
        else:
            histo_container[-1].SetFillColor(colors_mask[sample_name])
            hstack[histo_name].Add(histo_container[-1])


        if histo_name == "h_Memu": #Add the legend only once

            
                if not sample_name == "Data" and not sample_name == "Signal":
                    leg1.AddEntry(histo_container[-1],sample_name,"f")
                elif sample_name == "Data":
                    leg1.AddEntry(histo_container[-1],sample_name,"lep")
                elif sample_name == "Signal":
                    leg1.AddEntry(histo_container[-1],sample_name + " x ")


    fileIn.Close()


for histo_name in list_histos:

    canvas[histo_name] = ROOT.TCanvas("Cavas_" + histo_name,"",200,106,600,600)
    canvas[histo_name].cd()

    pad1 = ROOT.TPad("pad_" + histo_name,"",0,0.28,1,1)
    pad2 = ROOT.TPad("pad_" + histo_name,'',0,0,1,0.25)
    pad1.Draw()
    pad2.Draw()

    hstack[histo_name].SetTitle("")
    hstack[histo_name].Draw("histo")

    if histo_name == "h_Memu" :
        hstack[histo_name].GetXaxis().SetTitle("m_{#mu e} (GeV)")
        hstack[histo_name].SetMaximum(600)
    
    if histo_name == "h_Mueta" :
        hstack[histo_name].GetXaxis().SetTitle("#eta ")
        hstack[histo_name].SetMaximum(350)

    if histo_name == "h_Mupt" :
        hstack[histo_name].GetXaxis().SetTitle("#mu_{pt} (GeV)")
        hstack[histo_name].SetMaximum(1800)

    if histo_name == "h_Muphi" :
        hstack[histo_name].GetXaxis().SetTitle("#phi ")
        hstack[histo_name].SetMaximum(300)

    if histo_name == "h_Eeta" :
        hstack[histo_name].GetXaxis().SetTitle("#eta ")
        hstack[histo_name].SetMaximum(400)

    if histo_name == "h_Ept" :
       hstack[histo_name].GetXaxis().SetTitle("#e_{pt} (GeV)")
       hstack[histo_name].SetMaximum(2000)

    if histo_name == "h_Ephi" :
       hstack[histo_name].GetXaxis().SetTitle("#phi ")
       hstack[histo_name].SetMaximum(300)

    if histo_name == "h_PuppiMETphi" :
       hstack[histo_name].GetXaxis().SetTitle("#phi ")
       hstack[histo_name].SetMaximum(350)

    if histo_name == "h_PuppiMETpt" :
        hstack[histo_name].GetXaxis().SetTitle("#E_{pt} (GeV)")
        hstack[histo_name].SetMaximum(350)

    if histo_name == "h_Jetpt" :
        hstack[histo_name].GetXaxis().SetTitle("#jet_{pt} (GeV)")

    if histo_name == "h_IsoMu" :
        hstack[histo_name].GetXaxis().SetTitle("IsoMu")



    
    hstack[histo_name].Draw("histo")
    hsignal[histo_name].Draw("SAME,hist")
    hdata[histo_name].Draw("SAME,E1")


    leg1.Draw()

    

    ROOT.gStyle.SetOptStat(0)





    canvas[histo_name].SaveAs( histo_name + ".pdf")

