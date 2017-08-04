#!/bin/bash
#Description: The Requestion for qq.
##################################################################################################
#Requestion:
#文件格式：
#qq_number:phone
#
#cat qq.txt
#1234567:13700000000
#92990826:13911111111
#1234567:18399999999
#170838394:18833333333
#
#Expect output(期望输出):
#[1234567]   2  13700000000 18399999999
#[92990826]  1  13911111111
#[170838394] 1  18833333333
###################################################################################################
#The Method with me.
file=qq.txt
#取出所有qq号列表，放入变量。
feild=`awk -F":" '{print $1}' $file | sort -n |uniq`
for i in $feild
do
grep -w "^$i" $file | awk -F: '{B[$1]++;A[$2]=$2} END{printf "%-12s %s ","["$1"]",B[$1];for(i in A) {printf "%s ",i}}'
echo
done

#The Method with 永夜.    				---关联数组
awk -F: '{++key[$1]; value[$1]=" "$2"\n"value[$1]} END {for(i in value) printf("[%d] %s\n%s", i,key[i],value[i]) }'  $file