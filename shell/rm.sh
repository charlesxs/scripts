#!/bin/bash
# description: rm command for bash
# 

export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin
ORIGINRM=/bin/rm
MOVE="/bin/mv -f --backup=numbered"


# return dirname and file path
_walk() {
	local _path=$1
	echo $_path |sed -nr 's#^(\.{1,2}|/{1,})/?(.*)#\1 \2#p'
}

# count abspath
abspath() {
	local _dir=$1
	local _referdir=$2
	local referdirInfo dirInfo
	[[ $_referdir ]] || _referdir=`pwd`
	referdirInfo=(`_walk $_referdir`)
	if [[ ${referdirInfo[0]} != '/' ]];then
		if [[ $_referdir != '/' ]];then
			echo "Refer Directory must be Absolute Path."
			return 1
		fi
	fi
	dirInfo=(`_walk $_dir`)
	if [[ -n $dirInfo ]];then
		if [[ ${dirInfo[0]} == ".." ]];then
			abspath ${dirInfo[1]} "`dirname $_referdir`"
		elif [[ ${dirInfo[0]} == "." ]];then
			abspath ${dirInfo[1]} $_referdir
		elif [[ ${dirInfo[0]} == "/" ]];then
			echo $_dir
			return 0
		fi
	else
		[[ "$_referdir" != "/" ]] && echo "${_referdir}/${_dir}" || echo "${_referdir}${_dir}"
		return 0
	fi
}

fetch_all_mount_points() {
	if [ -f /proc/mounts ];then
		/bin/awk 'function checkIn(source, pat, __ARGVEND__, i) {
					split(source, A, " ")
					for(i in A) {
						if (A[i] == pat) {
							return 1
						}
					}
					return 0
				}
				!/(tmpfs|devpts|cgroup)/ && /\/dev/ {
				if ($2 != "/") {
					mps[$2] = length($2)
				}} END {
				   newstr=""
				   slen = asort(mps, mpsA)
				   for (i=1; i<=slen; i++) {
					for (mp in mps) {
					  if (mps[mp] == mpsA[i] && ! checkIn(newstr, mp)) {
						  newstr = mp" "newstr
						  break
						}
					 }
				 }   
					 print newstr
				 }'  /proc/mounts
	else
		/bin/mount -l | \
		/bin/awk 'function checkIn(source, pat, __ARGVEND__, i) {
					split(source, A, " ")
					for(i in A) {
						if (A[i] == pat) {
							return 1
						}
					}
					return 0
				}
				!/(tmpfs|devpts|cgroup)/ && /\/dev/{ 
				if ($2 != "/") {
					mps[$2] = length($2)
				}} END {
				   newstr=""
				   slen = asort(mps, mpsA)
				   for (i=1; i<=slen; i++) {
					for (mp in mps) {
					  if (mps[mp] == mpsA[i] && ! checkIn(newstr, mp)) {
						  newstr = mp" "newstr
						  break
						}
					 }
				 }   
					 print newstr
				 }' 
	fi
}


_split_path() {
	echo $1 | awk -F"/" '{
			for(i=1; i<=NF; i++) {
				print $i
			}
		}'	
}

choice_trash() {
	local _mps=$1
	local _path=$2
	local smp spath valid_mp= trash_dir=
	local apath spath smp_len=0 valid=

	# mount points: /opt/a/v/c/d  /opt/a/c/d
	# file path: /opt/a/v/dd
	apath=`abspath $_path`
	spath=(`_split_path "$apath"`)
	for mp in $mps;do
		valid=true
		smp=(`_split_path "$mp"`)
		smp_len=${#smp[*]}
		for ((i=0; i<smp_len; i++)) {
			if [ "${smp[$i]}" != "${spath[$i]}" ];then
				valid=false
				break 
			fi
		}
		$valid && valid_mp=$mp && break
	done

	[[ $valid_mp ]] && trash_dir="$valid_mp/.Trash" || trash_dir="/.Trash"
	echo $trash_dir
}


# main
if (($# > 0));then
	mps=`fetch_all_mount_points`
	for arg; do
		if [ "$arg" == "--help" ];then
			$ORIGINRM --help
			exit 1
		else
			[ ! -e $arg ] && continue
			trash_dir=`choice_trash "$mps" "$arg"`
			[ ! -d $trash_dir ] && (umask 0000; /bin/mkdir -p $trash_dir)
			$MOVE $arg $trash_dir
		fi
	done
else
	$ORIGINRM --help
fi
