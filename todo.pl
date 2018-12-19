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
    printf("\n./todo.pl --setup  <dir>                                     Download and unpack the lates madgraph version to <dir> ");
    printf("\n  ========================================================================================\n");
    exit(0);  
}



for($l=0;$l<$numArgs; $l++){
    
    if($ARGV[$l] eq "--setup"){
	$setdir=$ARGV[l+1];
	system(sprintf("mkdir  $setdir \n"));
	system(sprintf("cd $setdir; wget https://launchpad.net/mg5amcnlo/2.0/2.6.x/+download/MG5_aMC_v2.6.4.tar.gz;"));
	system(sprintf("cd $setdir; tar -xzf MG5_aMC_v2.6.4.tar.gz;"));
    }
}
