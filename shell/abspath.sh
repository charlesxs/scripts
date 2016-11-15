#!/bin/bash
#Descirption: 根据当前目录(或参考目录)计算出文件(或脚本)的绝对路径.
#Author: Carl
#

_walk() {
	local _path=$1
	echo $_path |sed -nr 's#^(\.{1,2}|/{1,})/?(.*)#\1 \2#p'
}

abspath() {
	local _dir=$1
	local _referdir=$2
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

main() {
#	curpath=`pwd`
#	abspath "$curpath" "$0"
	abspath "../../../a" "/root/a"
	abspath "/a"
	abspath "./a"
}

main
