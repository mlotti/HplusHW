#!/bin/csh

set passed = 0
set failed = 0
set total = 0
set alljobs = ""

foreach samplename (*/)
  if ( -e $samplename/res ) then
    if ( `ls $samplename/res/ | grep -c stdout` > 0 ) then
      set jobs=""
      foreach i ($samplename/res/*stdout)
        @ total++
        if ( `grep -c "JOB_EXIT_STATUS = 0" $i` < 1) then
          echo "\nfailed:" $i
          echo .. `grep -e "CMSException" $i`
          echo .. `grep -e JOB_EXIT_STATUS $i`, `grep -e WNHostName $i`
          echo .. `grep -e "attempt failed" $i`
          @ failed++
          # obtain job id
          set mystart = `echo $i | awk '{print index($0,"CMSSW")}'`
          set myend = `echo $i | awk '{print index($0,"stdout")}'`
          set myid = `echo $i | awk '{print substr($0,'$mystart+6','$myend-$mystart-7')}'`
          # obtain job title
          set myend = `echo $i | awk '{print index($0,"//")}'`
          set mytitle = `echo $i | awk '{print substr($0,0,'$myend-1')}'`
          if (`echo $jobs | awk '{print length($0)}'` > 0) then
            set jobs = "$jobs,$myid"
          else
            set jobs = "crab -c "$mytitle" -resubmit "$myid
          endif
        else
          @ passed++
        endif
      end
      if (`echo $jobs | awk '{print length($0)}'` > 0) then
        #echo $jobs
        set alljobs = "$alljobs\n$jobs"
      endif
    endif
  endif
end
echo $jobs
echo Failed jobs: $failed / $total
echo Successful jobs: $passed / $total
echo .
echo List of jobs to resubmit
echo $alljobs
