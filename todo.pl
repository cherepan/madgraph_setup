#! /usr/bin/perl
use Cwd;
use POSIX;
use POSIX qw(strftime);

#############################################
$numArgs = $#ARGV +1;
$ARGV[$argnum];


if($ARGV[0] eq "--help" || $ARGV[0] eq ""){
    printf("\n\n\n ========================================================================================");
    printf("\n./todo.pl --help                                             Prints this message");
    printf("\n./todo.pl --setupmadgraph  <dir>                             Download and unpack the lates madgraph version to <dir> ");
    printf("\n./todo.pl --gridpack  <dir>                                  Run DYTarball gridpack, valid only for local.uscms.org ");
    printf("\n  ========================================================================================\n");
    exit(0);  
}

$CMSSWRel="9_4_4";
$ARCH="slc6_amd64_gcc530";

for($l=0;$l<$numArgs; $l++){
    
    if($ARGV[$l] eq "--setupmadgraph"){
	$setdir=$ARGV[l+1];
	system(sprintf("mkdir  $setdir \n"));
	system(sprintf("cd $setdir; wget https://launchpad.net/mg5amcnlo/2.0/2.6.x/+download/MG5_aMC_v2.6.4.tar.gz;"));
	system(sprintf("cd $setdir; tar -xzf MG5_aMC_v2.6.4.tar.gz;"));
    }

    if($ARGV[$l] eq "--gridpack"){

	$currentdir=getcwd;
	if($ARGV[1] ne ""){
	    $basedir=$ARGV[1];
	}
	$CMSPATH="/CMSSW_$CMSSWRel";
	$CMSSW_BASE="$basedir$CMSPATH";
	system(sprintf("rm  Setup_gridpack"));
	system(sprintf("echo \"mkdir $basedir\" >>  Setup_gridpack")); 
	system(sprintf("echo \"cd $basedir\" >>  Setup_gridpack")); 
	system(sprintf("echo \"cmsrel CMSSW_$CMSSWRel\" >>  Setup_gridpack")); 
	system(sprintf("echo \"cd CMSSW_$CMSSWRel/src\" >> Setup_gridpack")); 
	system(sprintf("echo \"cmsenv\" >> Setup_gridpack")); 
	system(sprintf("echo \"cd $currentdir/$CMSSW_BASE/src\" >> Setup_gridpack")); 
	system(sprintf("echo \"scram b -j 4\" >> Setup_gridpack")); 

	system(sprintf("echo \"cp /local-scratch/vladimircherepanov/storage/DYJets_HT-incl_tarball.tar.xz .\" >> Setup_gridpack")); 
	system(sprintf("echo \"tar -xvf DYJets_HT-incl_tarball.tar.xz \" >> Setup_gridpack")); 


    }


}
