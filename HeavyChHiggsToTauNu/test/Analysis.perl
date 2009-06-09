#!/usr/local/bin/perl

        $BatchQueue     = "1nw";
        $Jobfile        = "Analysis.job";
        $rootfilelist   = "test.URLs";

######################################################################

        open( FILE, "< $rootfilelist" ) or die "Can't open $filename : $!";

        while( <FILE> ) {

            s/#.*//;            # ignore comments by erasing them
            next if /^(\s)*$/;  # skip blank lines

            chomp;              # remove trailing newline characters

            $lastSlashPos = rindex($_,"/") + 1;
            $filename = substr($_,$lastSlashPos,length($_)-$lastSlashPos);
            $path     = substr($_,0,$lastSlashPos);
#           print "$_\n";
            system("bsub -q $BatchQueue $Jobfile $path $filename");
        }

        close FILE;
