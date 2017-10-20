#!/bin/bash
#
# tomcat startup script for the Tomcat server
#
# chkconfig: 345 80 20
# description: start the tomcat deamon
#
# Source function library
. /etc/rc.d/init.d/functions
export  PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:/usr/local/mysql/bin:/usr/java/default/bin:$PATH
export JAVA_HOME=/usr/java/default

ACTION=$1; shift
TOMCAT_HOMES="$*"


usage() {
	echo "Usage: `basename $0` <start|stop|stop-all|restart|status> tomcat_home [tomcat_home2 ...]"
}


all_live_containers() {
	ps -e -o pid,cmd | awk '/.*java.*tomcat/ && !/awk/ {
							for (i=2; i<=NF; i++) {
								if ($i ~ /catalina.home/) {
									split($i, home, "=")
									print $1, home[2]
								}
							}
						}'
}


killer() {
	local _pid=$1
	local _thome=${2%/}
	local _timeout=${3:-60}
	local _cpid
	kill $_pid
	_thome=${_thome//\//\\/}
	for ((i=1; i<=$_timeout; i++)); do
		_cpid=`ps -e -o pid,cmd | awk '/catalina.home='"$_thome"' / && /java/ && !/awk/{print $1}'`
		[ -z "$_cpid" ] && return 0 || { echo -n '.'; sleep 1; }
	done
	return 1
}


_alive_exec() {
	local _action=$1
	local _pid=$2
	local _thome=$3
	case "$_action" in
	'start')
		echo -e "\"${_thome}\" is running, pid \033[32m$_pid\033[0m ..." ;;
	'stop')
		echo -n "Stopping tomcat ${_thome} ..."
		killer $_pid "$_thome"
		[ "$?" -eq 0 ] && success || failure
		echo
		;;
	esac
}


_defunct_exec() {
	local _action=$1
	local _thome=$2
	case "$_action" in
	'start')
		echo -n "Starting tomcat ${_thome} ..."
		daemon --user tomcat "${_thome}/bin/catalina.sh start > /dev/null";echo ;;
	'stop')
		echo -e "\"${_thome}\" is \033[31mnot run\033[0m ...";;
	esac
}


_check_chain() {
	local _thome=$1
	for ((i=1; i<=${#ALL_CONTAINERS[*]}; i+=2)); do
		if [[ "${ALL_CONTAINERS[$i]}" == "${_thome%/}" ]];then
			echo ${ALL_CONTAINERS[$((i-1))]}
			return 0
		fi
	done
	echo 0
}


exector() {
	local _action=$1
	local _thome _pid

	if [ -z "$TOMCAT_HOMES" ];then
		echo "Not special the tomcat home"
		exit 1
	fi

	for _thome in $TOMCAT_HOMES; do
		[ ! -d $_thome ] && echo -e "\033[31mNot found tomcat home ${_thome}\033[0m" && continue

		if ((${#ALL_CONTAINERS[*]} == 0));then
			_defunct_exec "$_action" "$_thome"
		else
			_pid=`_check_chain ${_thome}`
			if (($_pid > 0)); then
				_alive_exec "$_action" "$_pid" "$_thome"
			else
				_defunct_exec "$_action" "$_thome"
			fi
		fi
	done
}


ALL_CONTAINERS=(`all_live_containers`)

case "$ACTION" in
start)
	exector "start"
;;

stop)
	exector "stop"
;;

restart)
	exector "stop"
	unset ALL_CONTAINERS
	sleep 1
	ALL_CONTAINERS=(`all_live_containers`)
	exector "start"
;;

stop-all)
	echo "stopping all the tomcats ..."
	for ((i=1; i<=${#ALL_CONTAINERS[*]}; i+=2)); do
			kill ${ALL_CONTAINERS[$((i-1))]}
	done
;;

status)
	[[ -z "${ALL_CONTAINERS}" ]] && echo "No tomcat has ran ..." && exit 2
	for ((i=1; i<=${#ALL_CONTAINERS[*]}; i+=2)); do
			echo -e "\"${ALL_CONTAINERS[$i]}\" is running, pid \033[32m${ALL_CONTAINERS[$((i-1))]}\033[0m ..."
	done
;;

*)
	usage;;
esac
exit 0
