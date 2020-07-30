#if name for scripting reason... 
import ROOT
import argparse
import os
import math
import copy
import sys
import numpy as np

from ROOT import TCanvas, TGraph

ROOT.gROOT.SetBatch(True)   

list_inputfiles = []

#check inputfiles before loading, debug

i=0
for filename in sys.argv[1:]:
    list_inputfiles.append(filename)
    print "inputfiles in Cut.py =", list_inputfiles[i]
    i=i+1

#-----Some selection bools------#
is_Mupt            = False
is_Ept             = False
is_PuppiMetpt      = False
is_Jetpt           = True

#----pi pT and gamma ET cuts----- 
if is_Mupt:
    steps_cut1 = 40
    cut1_init = 25.
    cut1_stepsize = 1.
    name = "Mupt"

#----The next one is for lepton pT-----
if is_Ept:
    steps_cut1 = 40
    cut1_init = 20.
    cut1_stepsize = 1.
    name = "Ept"

if is_PuppiMetpt:
    steps_cut1 = 40
    cut1_init = 10.
    cut1_stepsize = 1.
    name = "PuppiMetpt"

#----The next one is for deltaphi------
if is_Jetpt:
    steps_cut1 = 40
    cut1_init = 40.
    cut1_stepsize = 1.
    name = "Jetpt"

cut_Nbkg = [0 for x in range(steps_cut1)]
cut_Nsig = [0 for x in range(steps_cut1)] 

for filename in list_inputfiles:
    root_file = ROOT.TFile(filename)
    mytree = root_file.Get("Cumulative_Events")
    nentries = mytree.GetEntriesFast()
    
    for jentry in xrange(nentries):

        ientry = mytree.LoadTree( jentry )
        if ientry < 0:
           break
        nb = mytree.GetEntry( jentry )
        if nb <= 0:
           continue

        temp_Memu = mytree.Memu
        temp_Mupt = mytree.Mupt
        temp_Ept = mytree.Ept
        temp_PuppiMetpt = mytree.PuppiMetpt
        temp_Jetpt = mytree.Jetpt
        weight = mytree.eventweight

        for icut1 in xrange(steps_cut1):
            cut1_value = cut1_init + cut1_stepsize*icut1
            #x[icut1] = cut1_value 

            if is_Mupt:
                if temp_Mupt < cut1_value:
                    continue
            
            if is_Ept:
                 if temp_Ept < cut1_value:
                    continue

            if is_PuppiMetpt:
                 if temp_PuppiMetpt > cut1_value:
                    continue
            
            if is_Jetpt:
                 if temp_Jetpt > cut1_value:
                    continue
            
            if filename == "background.root" :

                cut_Nbkg[icut1] =+ weight

            else:

                cut_Nsig[icut1] =+ weight
            
   
print "Done looping over the events"

Sig = [0 for x in range(steps_cut1)]

x = [0 for x in range(steps_cut1)] 

for icut1 in xrange(steps_cut1):
    cut1_value = cut1_init + cut1_stepsize*icut1
    x[icut1] = cut1_value 

#print x



#print cut_Nsig
#print cut_Nbkg

for icut1 in xrange(steps_cut1):
   
    if cut_Nbkg[icut1] > 0:
       Sig[icut1] = cut_Nsig[icut1] / math.sqrt(cut_Nbkg[icut1])
    else:
       Sig[icut1] = 0.



#Sig = cut_Nsig / np.sqrt(cut_Nbkg)
#end = cut1_init + steps_cut1*cut1_stepsize

#x = np.linspace( cut1_init, end, num = steps_cut1, dtype = float )

#print cut_Nsig
#print cut_Nbkg

#print Sig
#print x

aSig = np.array(Sig)
ax = np.array(x)

gr = ROOT.TGraph( steps_cut1, ax, aSig)

s1 = ROOT.TCanvas('s1', 'Significance', 200, 10, 700, 500)
s1.cd()

gr.SetLineColor( 2 )
gr.SetLineWidth( 4 )
gr.SetMarkerColor( 4 )
gr.SetMarkerStyle( 21 )
gr.SetTitle( 'Significance vs Cut' + name )
gr.GetXaxis().SetTitle( 'Cut' )
gr.GetYaxis().SetTitle( 'Significance' )
gr.Draw( 'ACP' )
   

s1.SaveAs("Cut_opt/Cut" + name + ".pdf")


   

