#!/bin/bash
#shell 函数自调用
#

trace_ppid() {
	pid=$1
	pidppid=(`ps -el |awk '{if($4=="'$pid'")print $4,$5}'`)
	spid=${pidppid[0]}
	ppid=${pidppid[1]}
	if [ $ppid == 1 ];then
		echo "$spid"
		return 0
	else
		trace_ppid $ppid
	fi
}

trace_ppid 24804 
