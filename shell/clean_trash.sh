#!/bin/bash
# clean Trash
#

#stop on fail
set -e

ORIGINRM=/bin/rm

fetch_all_mount_points() {
	if [ -f /proc/mounts ];then
		/bin/awk '!/(tmpfs|devpts|cgroup)/ && /\/dev/ {if ($2 != "/") print $2}' /proc/mounts
	else
		/bin/mount -l | \
		/bin/awk '!/(tmpfs|devpts|cgroup)/ && /\/dev/{if ($3 != "/") print $3}'
	fi
}

# clean
mps=`fetch_all_mount_points`
for mp in $mps;do
	trash_dir="$mp/.Trash"
	[ -d $trash_dir ] && cd $trash_dir && $ORIGINRM -rf *
done

# clean root trash
[ -d /.Trash ] && cd /Trash && $ORIGINRM -rf *
