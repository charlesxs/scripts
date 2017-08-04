#!/bin/bash
#Description: Deny login if IP illegal.
#Author: Carl
#

black_ip_list=$(grep "`date | awk '{print $2,$3}'`.*Failed" /var/log/secure | grep -o "[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}" | sort |uniq -cd | awk '{if($1>5) print $2}')

for ip in $black_ip_list;do
	if ! grep $ip /etc/hosts.deny &> /dev/null;then
		echo "sshd:$ip:deny" >> /etc/hosts.deny
	fi
done
