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
    parser.add_argument("-p", "--pdf-type",help="PDFID; 1 - CT14nlo, 2 - MMHT2014nlo68clas118, 3 - NNPDF30_nlo_nf_5_pdfas, 4 - MMHT2014nnlo68cl, 5 - PDF4LHC15_nnlo_100_pdfas ", type = str,action="store", default = '0 - nominal')
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
    
    
    h = ROOT.TH1F('invmass','Invariant Mass of Final State',150,0,175)
    h.SetFillColor(38)
    pos = ROOT.TH1F('pos','Invariant Mass of Final pos State',150,0,175)
    neg = ROOT.TH1F('neg','Invariant Mass of Final neg State',150,0,175)
    
    

    def invariant_mass(p1,p2):
        return math.sqrt(sum((1 if mu=='e' else -1)*(getattr(p1,mu)+getattr(p2,mu))**2 for mu in ['e','px','py','pz']))

    num=0
    for e in pylhe.readLHE(args.input_file):
        num=num+1
        if num%1000==0:
            print "Processing event number: ",num
        w=1;
        if "0" in args.pdf_type: 
            w =1
        if "1" in args.pdf_type:
            w=float(e.pdfwe[319])/float(e.pdfwe[1])
        if "2" in args.pdf_type:
            w=float(e.pdfwe[379])/float(e.pdfwe[1])
        if "3" in args.pdf_type:
            w=float(e.pdfwe[1009])/float(e.pdfwe[1])
        if "4" in args.pdf_type:
            w=float(e.pdfwe[430])/float(e.pdfwe[1])
        if "5" in args.pdf_type:
            w=float(e.pdfwe[615])/float(e.pdfwe[1])
        if abs(getattr(e.particles[-1],'id'))==15 and abs(getattr(e.particles[-2],'id'))==15:
            h.Fill(invariant_mass(e.particles[-1],e.particles[-2]),e.eventinfo.weight)
            zmass[0]=invariant_mass(e.particles[-1],e.particles[-2]);
#        print "id of interracting particles:  ", getattr(e.particles[-1],'id')
        if getattr(e.particles[-1],'id')==15: #c'est tau
                if getattr(e.particles[-1],'spin')==-1:
                    neg.Fill(invariant_mass(e.particles[-1],e.particles[-2]),w)
                if getattr(e.particles[-1],'spin')== 1:
                    pos.Fill(invariant_mass(e.particles[-1],e.particles[-2]),w)

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
