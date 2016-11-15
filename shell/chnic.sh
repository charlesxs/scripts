#!/bin/bash
#

export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin


check_platform() {
    dmidecode -t system |grep -iEq "(kvm|vmware|xen|virtual)" || { echo "run it in virtualization platform"; exit 1; }
}

nic_info() {
	local action=$1	
	case $action in
	'nic')
		ip addr show |sed -rn 's/^[0-9]:\s*(eth[0-9]):.*/\1/p';;
	'address')
		ip addr show |awk '/\<inet\>/{if ($2 !~ /127.0.0.1/){split($2,a,"/"); print a[1]}}' ;;
	*)
		ip addr show |awk '/\<inet\>/{if ($2 !~ /127.0.0.1/){split($2,a,"/"); print $NF":"a[1]}}';;
	esac
}

gen_conf() {
local file=$1
cat > $file << EOF
DEVICE="$nic"
BOOTPROTO="dhcp"
NM_CONTROLLED="yes"
ONBOOT="yes"
TYPE="Ethernet"
#IPADDR="172.16.8.254"
#NETMASK="255.255.252.0"
#GATEWAY="172.16.8.1"
EOF
}

edit_config() {
	local nics=`nic_info "nic"`
	local config_file="/etc/sysconfig/network-scripts/ifcfg"
	for nic in $nics; do
		conf=${config_file}-$nic
		if [ -f "$conf" ];then
			sed -ri '/(UUID|HWADDR)/d' $conf
			sed -i 's/ONBOOT="no"/ONBOOT="yes"/' $conf
		else
			gen_conf
		fi
	done
}

emit_driver() {
	local nic_drivers=`lsmod | awk '{if($1~/net/ && $3==0)print $1}'`
	rm -f /etc/udev/rules.d/70-persistent-net.rules
	for drive in $nic_drivers;do
		modprobe -r $drive
	done
		
	sleep 1
	for drive in $nic_drivers;do
		modprobe $drive
	done
}

main() {
	addrs=`nic_info "address"`
	if [ -z "$addrs" ];then
	 	# emit driver 
		emit_driver

		# fix config
		edit_config
		
	 	# restart network
	    /etc/init.d/network restart
	fi
}

# 
check_platform
main
