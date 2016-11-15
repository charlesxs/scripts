#!/bin/bash
#


ADMINS="xxxx"
LOGDIR="/opt/mail-sender/logs"
DATE=`date +'%F'`
LOGFILE="$LOGDIR/mail-sender-api-error.${DATE}.log"
PFILE="`cd $(dirname $0) && pwd`/.pline"


# source profile
. /etc/profile


get_start_linenumber() {
	local _num

	[ ! -r "$PFILE" ] && { echo 0; return 0; }
	_num=`cat $PFILE`
	[[ $_num ]] && echo $_num || echo 0
}


inspect_file() {
	local snum

	[ ! -r "$LOGFILE" ] && return 1
	snum=`get_start_linenumber`
	awk -v snum=$snum 'NR>snum {
		if ($0 ~ "IMAPError") {
			Eary["IMAPError"]++
		}

		if ($0 ~ "MailSendError") {
			Eary["MailSendError"]++
		}
	} END{
		print NR
		for(e in Eary) {
			print e":"Eary[e]
		}
	}' $LOGFILE
}


alarm() {
	# urlencode
	local _msg=`echo $1 | sed 's/ /%20/g;
							  s/!/%21/g;
							  s/"/%22/g;
							  s/#/%23/g;
							  s/\&/%26/g;
							  s/'\''/%28/g;
							  s/(/%28/g;
							  s/)/%29/g;
							  s/:/%3A/g;
							  s/\//%2F/g'`

	for admin in $ADMINS; do
		curl http://ismsm.xxxx.com/weixin.php?user=$admin\&info="$_msg"\&channel=mail-sender
	done
}


main() {
	local result current_linenum
	local msg rlen

	result=(`inspect_file`)
	current_linenum=${result[0]}

	# write current line number in pfile
	echo $current_linenum > $PFILE

	# alarm
	rlen=${#result[*]}
	if ((rlen > 1)); then
		msg="Some erros in 15 minutes: "

		for ((i=1; i<=$((rlen-1)); i++)); do
			msg="$msg ${result[$i]}"
		done

		alarm "$msg"
	fi

}


# main
main
