#!/bin/bash
#Description: Requestion for Friends.

################################################################################################################################
#Requestion：一目录 /root/test/ 下有文件 1 2 3 9 8 和子目录 a e c ，其子目录下亦有 以1-9 单个整数为文件名的文件
#和名字是任意字母的子目录.
#
#Ask：计算出此目录下包括所有的子目录下，缺少的数字文件名(数字文件名的范围是 1-9)，如 /root/test 目录下有 1 2 3 9 8 几个文件，则其缺少
#的数字文件名是 4 5 6 7 ,那么显示出这个目录名和其缺少的数字文件名.
#
#Explain: 数字文件名---> 指的是以单个数字(范围是1-9)为名称的文件 
################################################################################################################################

# dir_root=/root/test/
# export Total=`ls -lR $dir_root`

# count() {
# 	prev=$1
# 	next=$2
# 	if [ -n "$prev" ] && [ "$next" -gt 0 ];then
# 		filename=`echo "$Total" | sed -n "$prev,$next p" | awk '/^-/ {print $NF}'`
# 		dir_name=`echo "$Total" | sed -n "$prev, $next p" |grep "^\/.*:$"`
# 		foundaction_str=`seq 1  9`
# 		for i in $filename; do
# 			foundaction_str=`echo "$foundaction_str"| sed -e "/$i/d"`
# 		done
# 		echo  "$dir_name The missing Digital_file ===> "$foundaction_str
# 	else
# 		filename=`echo "$Total" | sed -n "$prev,$ p" | awk '/^-/ {print $NF}'`
# 		dir_name=`echo "$Total" | sed -n "$prev,$ p" |grep "^\/.*:$"`
# 		foundaction_str=`seq 1  9`
# 		for i in $filename； do
# 			foundaction_str=`echo "$foundaction_str"| sed -e "/$i/d"`
# 		done
# 		echo  "$dir_name The missing Digital_file ===> "$foundaction_str
# 	fi
# }


# row_num=`echo "$Total" | grep -n "^\/.*:$" | awk -F: '{print $1}' `
# count_num=`echo "$row_num" |wc -l`
# count_array=(`echo $row_num`)

# for ((a=1;a<=$count_num;a++)); do
# 	Previous=$((a-1))
# 	count ${count_array[$Previous]}  $((${count_array[$a]}-1))
# done


ROOT_DIR='/root/test/'
FSTR=`seq 1 9`


_check_in() {
	local _fname=$1
	for i in {1..9}; do
		[[ "$fname" == "$i" ]] && return 0
	done
	return 1
}


counter() {
	local _dir=$1
	local missing files file name
	local dirs dir

	files=`find $_dir -type f`
	dirs=`find $_dir -type d`
	for file in files; do
		name=`basename file`
		if ! _check_in "$name"; then
			missing=(${missing[*]} $name)
		fi
	done

	if [[ "$dirs" ]];then
		for dir in $dirs; do
			counter "$dir"
		done
	fi

	echo "$_dir Missing Number files: ${missing[*]}"
}

