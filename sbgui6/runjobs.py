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
            seed = args.start_seed + i
            if not os.path.exists(outputdir):
                os.mkdir(outputdir)
            if not os.path.exists('log'):
                os.mkdir('log')
            filedata = filedata.replace('<dir>', cwd)
            filedata = filedata.replace('<exec>',
                                        cwd+"/short.sh  " + str(args.number_of_events) + " " + str(seed) + " 4 ")
            filename = "qsub_"+str(i)+".sh"
            print filename
            with open(filename, 'w') as file:
                file.write(filedata)

        qsubname= "submiter_"+str(i)
        with open("submit_template", "rwt") as submiter:
            filedata = submiter.read()
            filedata= filedata.replace("<exec>",filename)

            with open(qsubname, 'w') as file:
                file.write(filedata)
        print "-- Submitting Job N:  ", i
        os.system('chmod u+x '+qsubname)
        os.system('./' +qsubname  + ' ' + qsubname + ' --short')
