#!/bin/bash
# reconf static address
#

export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin

# debug
DEBUG=false

# restart network
RESTART_NET=false


nic_info() {
    local action=$1 
    case $action in
    'route')
		ip route | awk '/default/ {print $3}';;
    *)
		ifconfig | \
		sed -rn '/eth[0-9]/,+1{N;s/(eth[0-9]).*addr:([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+).*Mask:([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)/\1:\2:\3/p}'
    esac
}


check_config() {
	local _conf=$1
	local _addr=$2
	if [ -f "$_conf" ];then
		bootproto=`awk -F= '/BOOTPROTO/{gsub(/\"/, "", $2); print $2}' $_conf`
		ip=`awk -F= '/IPADDR/{gsub(/\"/, "", $2); print $2}' $_conf`
		if [[ "$bootproto" == "dhcp" ]];then
			return 1
		else
			{ [ -n "$ip" ] && [[ "$ip" == "$_addr" ]]; } && return 0 || return 1
		fi
	else
		return 1
	fi
}


edit_config() {
	local _info=$1
	local _addr=$2
	local _conf=$3
	[ -f $_conf ] && mv  $_conf ${_conf}.bak
	cat > $_conf << EOF
DEVICE="`echo $_info|awk -F: '{print $1}'`"
BOOTPROTO="static"
NM_CONTROLLED="yes"
ONBOOT="yes"
TYPE="Ethernet"
IPADDR="$_addr"
NETMASK="`echo $_info|awk -F: '{print $3}'`"
GATEWAY="`nic_info "route"`"
EOF
	RESTART_NET=true
}

probe_addrs() {
	local _addr=$1
	prefix=${_addr%.*}
	rm $used $free
	for i in {1..254};do
		{
		addr=${prefix}.${i}
		if ping -c 1 -w 3 ${addr} &> /dev/null;then
			echo $addr >> $used
		else
			echo $addr >> $free
		fi 
		}&
	done
	echo $prefix
}

vote_addr() {
	local _addr=$1
	prefix=`probe_addrs "$_addr"`
	sleep 2
	[ ! -f $free ] && echo "not found \"$free\"." && exit
	biggers=`grep -Ew '[0-9]{3}$' $used | wc -l`
	smallers=`grep -Ew '[0-9]{1,2}$' $used | wc -l`
	if (( $biggers > $smallers ));then
		suffix=`awk -F. '{print $4}' $free | \
				sort -n | \
				sed -n '6p'`
	else
		suffix=`awk -F. '{print $4}' $free | \
				sort -rn | \
				sed -n '6p'`
	fi
	echo ${prefix}.${suffix}
}


main() {
	addrinfo=`nic_info`
	if [ -z $addrinfo ]; then
		echo "not found any valid address, exiting ..."
	else
		for info in $addrinfo; do
			$DEBUG && echo "info:  \"$info\""
			addr=`echo $info |awk -F: '{print $2}'`
			nic=`echo $info |awk -F: '{print $1}'`
			conf="/etc/sysconfig/network-scripts/ifcfg-${nic}"

#			if ! check_config "$conf" "$addr";then
				# vote a valid ip
				valid_addr=`vote_addr "$addr"`
				$DEBUG && echo "fetch valid address: $valid_addr"

				# edit configurate file
#				edit_config "$info" "$valid_addr" "$conf"
#			fi
		done
	fi
}


# main
used='/tmp/usedIP.txt'
free='/tmp/freeIP.txt'
main

# restart network
$RESTART_NET && /etc/init.d/network restart
