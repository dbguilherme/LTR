#!/usr/bin/perl

# my $infile = $ARGV[0];
my $train_file = $ARGV[0];
# my $featnum = $ARGV[2];
my $outfile = $ARGV[1];
#my $outfile2 = $ARGV[2];
my $vez=$ARGV[2];
my $linecount = 1;

open (F1, $train_file) || die ("Could not open $train_file!");
open (F2, ">$outfile") || die ("Could not open $outfile!");
#open (F3, ">$outfile2") || die ("Could not open $outfile2!");

print "\n removendo linhas";
while ($line = <F1>) {
    
    @vals = split(/ /, $line,2);
    if($vals[0] > 1000*$vez){
      $j=$vals[0]-1000*$vez;
     
      
      if($vals[0]>3000){
         print "$vez ---$j $vals[0]\n";
         print F2 "$j $vals[1]";
      }
     
      
    }
    #print @vals;
   # else{
   #   print  "$line";
   # }

}