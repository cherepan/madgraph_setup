#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-nj", "--number-of-jobs",help="Number of Jobs to be submitted; [Default: %(default)s] ", type = int, action="store", default = '1')
    parser.add_argument("-ne", "--number-of-events",help="Number of events per job; [Default: %(default)s] ", type = int,action="store", default = '1000')
    parser.add_argument("-ss", "--start-seed",help="Starting Madgraph Seed value; [Default: %(default)s] ", type = int,action="store", default = '10')
    args = parser.parse_args()
    cwd = os.getcwd()

    for i in range(1, args.number_of_jobs):
        with open('qsub_submit_template.sh', 'r') as file :
            filedata = file.read()
            outputdir = "output_"+str(i)
            if not os.path.exists(outputdir):
                os.mkdir(outputdir)
            if not os.path.exists('log'):
                os.mkdir('log')
            filedata = filedata.replace('<dir>', cwd)
            filedata = filedata.replace('<exec>',
                                        cwd+"/short.sh")
            filedata = filedata.replace('<output2>', 'gzip -d '+outputdir+'/cmsgrid_final_'+ str(i) +'.lhe.gz')
            filedata = filedata.replace('<output3>', 'cp -r  '+outputdir + '/*  ' + cwd + '/'+outputdir)
            filename = "runcms_condor_"+str(i)+".sh"
            print filename
            with open(filename, 'w') as file:
                file.write(filedata)
        condorname= "condor_submiter_"+str(i)
        with open("condor_submiter_template", "rwt") as submiter:
            filedata = submiter.read()
            seed = args.start_seed + i
            filedata= filedata.replace("Executable = runcms_condor.sh","Executable = "+filename)
            filedata= filedata.replace("Arguments = a b c","Arguments = "+str(args.number_of_events) + " " + str(seed) + " 4 ")

            with open(condorname, 'w') as file:
                file.write(filedata)
        print "-- Submitting Job N:  ", i
        os.system('condor_submit ' + condorname)
