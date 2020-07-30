import ROOT
import argparse
import os
import math

import copy
import sys

import numpy as np

todaywd = "20200630" #temporary replacement for -ln command


# Scale correction - loading 2D histos

el_ID_scale_name_2018  = "scale_factors/2018_ElectronMVA80.root"
el_ID_scale_file_2018  = ROOT.TFile(el_ID_scale_name_2018)
el_ID_scale_histo_2018 = ROOT.TH2F()
el_ID_scale_histo_2018 = el_ID_scale_file_2018.Get("EGamma_SF2D")

el_reco_scale_name_2018  = "scale_factors/egammaEffi.txt_EGM2D_updatedAll_2018.root"
el_reco_scale_file_2018  = ROOT.TFile(el_reco_scale_name_2018)
el_reco_scale_histo_2018 = ROOT.TH2F()
el_reco_scale_histo_2018 = el_reco_scale_file_2018.Get("EGamma_SF2D")

mu_ID_scale_name_2018  = "scale_factors/RunABCD_SF_ID_muon_2018.root"
mu_ID_scale_file_2018  = ROOT.TFile(mu_ID_scale_name_2018)
mu_ID_scale_histo_2018 = ROOT.TH2F()
mu_ID_scale_histo_2018 = mu_ID_scale_file_2018.Get("NUM_TightID_DEN_TrackerMuons_pt_abseta")

mu_Iso_scale_name_2018  = "scale_factors/RunABCD_SF_ISO_muon_2018.root"
mu_Iso_scale_file_2018  = ROOT.TFile(mu_Iso_scale_name_2018)
mu_Iso_scale_histo_2018 = ROOT.TH2F()
mu_Iso_scale_histo_2018 = mu_Iso_scale_file_2018.Get("NUM_TightRelIso_DEN_TightIDandIPCut_pt_abseta")

mu_Trigger_scale_name_BeforeHLTUpdate_2018       = "scale_factors/EfficienciesAndSF_2018Data_BeforeMuonHLTUpdate.root"
mu_Trigger_scale_file_BeforeHLTUpdate_2018       = ROOT.TFile(mu_Trigger_scale_name_BeforeHLTUpdate_2018)
mu_Trigger_scale_histo_BeforeHLTUpdate_2018_Mu24 = ROOT.TH2F()
mu_Trigger_scale_histo_BeforeHLTUpdate_2018_Mu24 = mu_Trigger_scale_file_BeforeHLTUpdate_2018.Get("IsoMu24_PtEtaBins/abseta_pt_ratio")
mu_Trigger_scale_histo_BeforeHLTUpdate_2018_Mu50 = ROOT.TH2F()
mu_Trigger_scale_histo_BeforeHLTUpdate_2018_Mu50 = mu_Trigger_scale_file_BeforeHLTUpdate_2018.Get("Mu50_OR_OldMu100_OR_TkMu100_PtEtaBins/abseta_pt_ratio")

mu_Trigger_scale_name_AfterHLTUpdate_2018       = "scale_factors/EfficienciesAndSF_2018Data_AfterMuonHLTUpdate.root"
mu_Trigger_scale_file_AfterHLTUpdate_2018       = ROOT.TFile(mu_Trigger_scale_name_AfterHLTUpdate_2018)
mu_Trigger_scale_histo_AfterHLTUpdate_2018_Mu24 = ROOT.TH2F()
mu_Trigger_scale_histo_AfterHLTUpdate_2018_Mu24 = mu_Trigger_scale_file_AfterHLTUpdate_2018.Get("IsoMu24_PtEtaBins/abseta_pt_ratio")
mu_Trigger_scale_histo_AfterHLTUpdate_2018_Mu50 = ROOT.TH2F()
mu_Trigger_scale_histo_AfterHLTUpdate_2018_Mu50 = mu_Trigger_scale_file_AfterHLTUpdate_2018.Get("Mu50_OR_OldMu100_OR_TkMu100_PtEtaBins/abseta_pt_ratio")
 
#___________________________________________________________________________________________________________

p = argparse.ArgumentParser(description='Select rootfile to plot')
p.add_argument('rootfile_name', help='Type rootfile name')
args = p.parse_args()

fInput = ROOT.TFile(args.rootfile_name)

#SPLIT: I can split a string of chars before and after a split code (that could be a string or a symbol)
#then I can take the string stands before or after with [0] or [1], respectively. 
#[:-n] is not an emoji, it deletes last n symbols from the string

samplename = (args.rootfile_name.split("ZEMuAnalysis_")[1])[:-5] 
print "samplename =", samplename

yearlum = samplename.split("_")[1]
print "yearlum =", yearlum

def givescalefactor( str0 , str1 ):
#simple method wich return the correct scale factor cut event_sim
    switcher = {

      "Signal_2018": (1.e-6*0.5*1910./0.0336) / 32172. ,
      "ttbarlnu_2018": 88.29/64120000.,  #88.29/                      (./(0.1739*0.1782))/ 1.
      "WW_2018": 12.178/7758900., #BR? #12.178/       (1.*1910./(0.1071*0.1063))/
      "DY50_2018": (2075.14*3.) / (193215674. *(1-2*0.163)),  #Drell-Y 2075.14*3 / 193215674 neratio 0.163
      "SingleAntiTop_2018": 34.97 / (7623000. *(1-2*0.0034)),
      "SingleTop_2018": 34.91 / (9598000. *(1-2*0.0038)),
      "ttbarHadronic_2018": 377.96 / 199524000. ,
      "ttbarSemileptonic_2018": 365.34 / 199637998.

    }

    year = {

      "2018": 59.74*1000.,
      "2017": 41.48*1000.,
      "2016": 35.92*1000.

    }
    
    if str0 == "Data_2018":
       return 1.
    else:
       return (switcher.get(str0, 1)) * year.get(str1, 1);


def get_ele_scale(lep_pt, lep_eta):
    
    local_lep_pt = lep_pt

    if local_lep_pt > 499.: # This is because corrections are up to 499 GeV
       local_lep_pt = 499.

    local_lep_eta = lep_eta

    if local_lep_eta >= 2.5:
       local_lep_eta = 2.49
    if local_lep_eta < -2.5: # Corrections reach down to eta = -2.5, but only up to eta = 2.49
       local_lep_eta = -2.5
            
    scale_factor_ID   = el_ID_scale_histo_2018.GetBinContent( el_ID_scale_histo_2018.GetXaxis().FindBin(local_lep_eta), el_ID_scale_histo_2018.GetYaxis().FindBin(local_lep_pt) )
    scale_factor_reco   = el_reco_scale_histo_2018.GetBinContent( el_reco_scale_histo_2018.GetXaxis().FindBin(local_lep_eta), el_reco_scale_histo_2018.GetYaxis().FindBin(local_lep_pt) )
    #scale_factor_trigger   = el_trigger_scale_histo_2018.GetBinContent( el_trigger_scale_histo_2018.GetXaxis().FindBin(local_lep_eta), el_trigger_scale_histo_2018.GetYaxis().FindBin(local_lep_pt) )
            
    return 1. #scale_factor_ID #* scale_factor_reco


def get_muon_scale(lep_pt, lep_eta):

        local_lep_pt = lep_pt
        if local_lep_pt >= 120.:  # This is because corrections go up to 120 GeV (excluded)
            local_lep_pt = 119.
        if local_lep_pt < 20.:
            local_lep_pt = 20.

        local_lep_eta = lep_eta
        if local_lep_eta >= 2.4:
            local_lep_eta = 2.39
        if local_lep_eta <= -2.4:
            local_lep_eta = -2.39


        luminosity_norm = 59.74
        luminosity_BeforeHLTUpdate = 8.98
        luminosity_AfterHLTUpdate = 50.71

        # Use a random number to select which muon scale factor to use for trigger, depending on the respective lumi fraction (only for 2018)
        Nrandom_for_SF = ROOT.TRandom3(92562).Rndm()
            
        scale_factor_ID       = mu_ID_scale_histo_2018.GetBinContent( mu_ID_scale_histo_2018.GetXaxis().FindBin(local_lep_pt), mu_ID_scale_histo_2018.GetYaxis().FindBin(math.fabs(local_lep_eta)) )
        scale_factor_Iso      = mu_Iso_scale_histo_2018.GetBinContent( mu_Iso_scale_histo_2018.GetXaxis().FindBin(local_lep_pt), mu_Iso_scale_histo_2018.GetYaxis().FindBin(math.fabs(local_lep_eta)) )

        if Nrandom_for_SF <= (luminosity_BeforeHLTUpdate/luminosity_norm): # Access muon Trigger SF: Before HLT Update

           local_lep_pt_forTrigger = lep_pt # Corrections related to this trigger start from 52 GeV

           if local_lep_pt_forTrigger < 52.:
              local_lep_pt_forTrigger = 52.
                
           scale_factor_Trigger = mu_Trigger_scale_histo_BeforeHLTUpdate_2018_Mu50.GetBinContent( mu_Trigger_scale_histo_BeforeHLTUpdate_2018_Mu50.GetXaxis().FindBin(math.fabs(local_lep_eta)), mu_Trigger_scale_histo_BeforeHLTUpdate_2018_Mu50.GetYaxis().FindBin(local_lep_pt_forTrigger) )

        else: # Access muon Trigger SF: After HLT Update

           local_lep_pt_forTrigger = lep_pt # Corrections related to this trigger start from 52 GeV

           if local_lep_pt_forTrigger < 52.:
              local_lep_pt_forTrigger = 52.
                
           scale_factor_Trigger = mu_Trigger_scale_histo_AfterHLTUpdate_2018_Mu50.GetBinContent( mu_Trigger_scale_histo_AfterHLTUpdate_2018_Mu50.GetXaxis().FindBin(math.fabs(local_lep_eta)), mu_Trigger_scale_histo_AfterHLTUpdate_2018_Mu50.GetYaxis().FindBin(local_lep_pt_forTrigger) )

        scale_factor = scale_factor_ID * scale_factor_Iso #* scale_factor_Trigger

        return scale_factor




#___________________________________________________________________________________________________________

fOutput = ROOT.TFile( samplename + ".root","RECREATE")
fOutput.cd()

#histogram
h_Memu = ROOT.TH1F("h_Memu", "M_{#mu e}", 50, 75., 110.)
h_Mueta = ROOT.TH1F("h_Mueta", "Mu_{eta}", 100, -3., 3.)
h_Mupt = ROOT.TH1F("h_Mupt", "Mu_{pt}", 50, 25., 140.)
h_Muphi = ROOT.TH1F("h_Muphi", "Mu_{phi}", 100, -3.5, 3.5)
h_Eeta = ROOT.TH1F("h_Eeta", "e_{eta}", 100, -3., 3.)
h_Ept = ROOT.TH1F("h_Ept", "e_{pt}", 50, 30., 140.)
h_Ephi = ROOT.TH1F("h_Ephi", "e_{phi}", 100, -3.5, 3.5)
h_PuppiMETphi = ROOT.TH1F("h_PuppiMETphi", "MET_{phi}", 100, -3.5, 3.5)
h_PuppiMETpt = ROOT.TH1F("h_PuppiMETpt", "MET_{pt}", 100, 0., 51.)
h_Jetpt = ROOT.TH1F("h_Jetpt", "Jet_{pt}", 100, 30., 200.)
h_IsoMu = ROOT.TH1F("h_IsoMu", "IsoMu",100, 0., 4.)

#tree variables
Memu = np.zeros(1, dtype=float)
Mupt = np.zeros(1, dtype=float)
Ept = np.zeros(1, dtype=float)
PuppiMetpt = np.zeros(1, dtype=float)
Jetpt = np.zeros(1, dtype=float)
IsoMu = np.zeros(1, dtype=float)
eventweight = np.zeros(1, dtype=float)

#tree initialization
tree_output = ROOT.TTree('Cumulative_Events','Cumulative_Events')
tree_output.Branch('Memu',Memu,'Memu/D')
tree_output.Branch('Mupt',Mupt,'Mupt/D')
tree_output.Branch('Ept',Ept,'Ept/D')
tree_output.Branch('PuppiMetpt',PuppiMetpt,'PuppiMetpt/D')
tree_output.Branch('Jetpt',Jetpt,'Jetpt/D')
tree_output.Branch('IsoMu',IsoMu, 'IsoMu/D')
tree_output.Branch('eventweight',eventweight,'eventweight/D')

root_file = ROOT.TFile("ZEMuAnalysis_" + samplename + ".root") #must be changed
mytree = root_file.Get("Events")

Nevts_per_sample   = 0. # Count the number of events in input per each sample processed

weight = givescalefactor( samplename, yearlum ) 
print "weight =", weight

nentries = mytree.GetEntriesFast()

#Initializing variables
lep1_FourMom = ROOT.TLorentzVector()
lep2_FourMom = ROOT.TLorentzVector()

#Start looping over events
print "This sample has ", mytree.GetEntriesFast(), " events"


for jentry in xrange(nentries):

    ientry = mytree.LoadTree( jentry )
    if ientry < 0:
        break
    nb = mytree.GetEntry(jentry )
    if nb <= 0:
        continue

    Nevts_per_sample = Nevts_per_sample + 1

    if (Nevts_per_sample/100000.).is_integer() :
        print "Processed ", Nevts_per_sample, " events..."


    jetentries = mytree.nJet
       
    Maxjet = mytree.Jet_pt[0]

    for zentry in xrange(jetentries):
        if (mytree.Jet_pt[zentry] >= Maxjet and mytree.Jet_jetId[zentry] >= 4 and mytree.Jet_puId[zentry] >= 6) : #modified
            Maxjet = mytree.Jet_pt[zentry]


    lep1_pt = mytree.Muon_pt[0]
    lep1_eta = mytree.Muon_eta[0]
    lep1_phi = mytree.Muon_phi[0]
    lep1_mass = mytree.Muon_mass[0]

    lep2_pt = mytree.Electron_pt[0]
    lep2_eta = mytree.Electron_eta[0]
    lep2_phi = mytree.Electron_phi[0]
    lep2_mass = mytree.Electron_mass[0]

    met_phi = mytree.PuppiMET_phi
    met_pt = mytree.PuppiMET_pt

    Iso_Mu = mytree.Muon_pfRelIso03_all[0]

    # "Data" trees doesn't have genWeight and puWeight 
    if samplename == "Data_2018":
       Event_Weight = 1
     
    else:
       MC_Weight = mytree.genWeight
       PU_Weight = mytree.puWeight 
       Event_Weight = weight*MC_Weight*PU_Weight/math.fabs(MC_Weight) #* get_muon_scale(lep1_pt, lep1_eta) * get_ele_scale(lep2_pt, lep2_eta) 
       

    lep1_FourMom.SetPtEtaPhiM(lep1_pt,lep1_eta,lep1_phi,lep1_mass)
    lep2_FourMom.SetPtEtaPhiM(lep2_pt,lep2_eta,lep2_phi,lep2_mass)
    Zcand_FourMom = lep1_FourMom + lep2_FourMom



    if samplename == "Data_2018":
       if (Zcand_FourMom.M() <= 85.5 or Zcand_FourMom.M() >= 95.3) : 
           h_Memu.Fill(Zcand_FourMom.M(), Event_Weight)
           Memu[0] = Zcand_FourMom.M()
    else:
       #Fill histogram w/o blind analysis
       h_Memu.Fill(Zcand_FourMom.M(), Event_Weight)
       Memu[0] = Zcand_FourMom.M()

    #Fill histogram
    h_Mueta.Fill(lep1_eta, Event_Weight)
    h_Mupt.Fill(lep1_pt, Event_Weight)
    h_Muphi.Fill(lep1_phi, Event_Weight)
    h_Eeta.Fill(lep2_eta, Event_Weight)
    h_Ept.Fill(lep2_pt, Event_Weight)
    h_Ephi.Fill(lep2_phi, Event_Weight)
    h_PuppiMETphi.Fill(met_phi, Event_Weight)
    h_PuppiMETpt.Fill(met_pt, Event_Weight)
    h_Jetpt.Fill(Maxjet, Event_Weight)
    h_IsoMu.Fill(Iso_Mu, Event_Weight)


   
    Mupt[0] = lep1_pt
    Ept[0] = lep2_pt
    PuppiMetpt[0] = met_pt #*Event_Weight
    Jetpt[0] = Maxjet
    IsoMu[0] = Iso_Mu
    eventweight[0] = Event_Weight
    tree_output.Fill()


fOutput.Write()
fOutput.Close()


path = todaywd + "/" + samplename #"/"
try:
    os.makedirs( path )
except OSError:
    print ("Creation of the directory %s failed" % path)
else:
    print ("Successfully created the directory %s " % path)

print "Number of events processed = ", Nevts_per_sample


