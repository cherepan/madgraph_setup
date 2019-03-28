#!/usr/bin/env python

import os
import ROOT
import pylhe
import sys
import math
import argparse
from array import array



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-file",help="Input file; [Default: %(default)s] ", type = str, action="store", default = '1')
    parser.add_argument("-o", "--output-file",help="Output file; [Default: %(default)s] ", type = str,action="store", default = '1000')
    args = parser.parse_args()
    cwd = os.getcwd()


    
    output_file = ROOT.TFile(args.output_file, "RECREATE")
    output_tree = ROOT.TTree()
    output_tree.SetName("lhetree")
    
    pdgid = array( 'f', [ 0 ] )
    px = array( 'f', [ 0 ] )
    py = array( 'f', [ 0 ] )
    pz = array( 'f', [ 0 ] )
    energy = array( 'f', [ 0 ] )
    mass = array( 'f', [ 0 ] )
    zmass = array( 'f', [ 0 ] )
    spin = array( 'f', [ 0 ] )
    
    
    output_tree.Branch("px",px , "px/F")
    output_tree.Branch("py",py , "py/F")
    output_tree.Branch("pz",pz , "pz/F")
    output_tree.Branch("energy",energy , "energy/F")
    output_tree.Branch("mass",mass , "mass/F")
    output_tree.Branch("zmass",zmass , "zmass/F")
    output_tree.Branch("spin",spin , "spin/F")
    output_tree.Branch("pdgid", pdgid, "pdgid/F")
    
    
    h = ROOT.TH1F('invmass','Invariant Mass of Final State',10,90,92)
    h.SetFillColor(38)
    pos = ROOT.TH1F('pos','Invariant Mass of Final pos State',10,90,92)
    neg = ROOT.TH1F('neg','Invariant Mass of Final neg State',10,90,92)
    
    

    def invariant_mass(p1,p2):
        return math.sqrt(sum((1 if mu=='e' else -1)*(getattr(p1,mu)+getattr(p2,mu))**2 for mu in ['e','px','py','pz']))

    num=0
    for e in pylhe.readLHE(args.input_file):
        num=num+1
        if num%1000==0:
            print "Processing event number: ",num
#        print e.pdfwe[0],e.pdfwe[1],e.pdfwe[2]
        if abs(getattr(e.particles[-1],'id'))==15 and abs(getattr(e.particles[-2],'id'))==15:
            h.Fill(invariant_mass(e.particles[-1],e.particles[-2]),e.eventinfo.weight)
            zmass[0]=invariant_mass(e.particles[-1],e.particles[-2]);
#        print "id of interracting particles:  ", getattr(e.particles[-1],'id')
        if getattr(e.particles[-1],'id')==15: #c'est tau
                if getattr(e.particles[-1],'spin')==-1:
                    neg.Fill(invariant_mass(e.particles[-1],e.particles[-2]),e.eventinfo.weight)
                if getattr(e.particles[-1],'spin')== 1:
                    pos.Fill(invariant_mass(e.particles[-1],e.particles[-2]),e.eventinfo.weight)

        for p in e.particles:
            pdgid[0] = getattr(p,'id')  
            px[0] = getattr(p,'px')
            py[0] = getattr(p,'py')
            pz[0] = getattr(p,'pz')
            energy[0] = getattr(p,'e')
            mass[0] = getattr(p,'m')
            spin[0] = getattr(p,'spin')
            output_tree.Fill()



    output_tree.Write()
    output_file.Write()
