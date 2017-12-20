#!/bin/bash
# Description: parse json string
# Author: Charles/Carl
#
# Usage: JsonParser "$jsonstr" "fieldname"
#		 JsonParser "$jsonstr" "fieldname__subfield__subfield"
#		 JsonParser "$jsonstr" "fieldname[index]__subfield"
# 		
#	     # read from stdin	
# 		 echo $jsonstr | JsonParser "fieldname"
#


# debug
debug=false


# remove feature of json string.
filter() {
	local _json=$1
	if grep -q '^\[' <<< $_json;then
		filter_str=`echo $_json | \
					sed -r 's/\[(.*)\]/\1/' | \
					awk -F, '{
						for(i=1; i<=NF; i++){
							printf "%s ",$i
						}
					}' `
	elif grep -q '\"' <<< $_json;then
#		filter_str=`echo $_json | \
#					sed -r 's/\{(.*)\}/\1/' | \
#					sed -r "s/([^:,\"\'\{\}\[])\s/\1--/g" | sed -r 's/(\])--/\1 /g' | \
#					sed -r "s/[[:space:]]//g" | \
#					sed -r "s/([^0-9\"\}]),/\1~~/g" | sed -r 's/(\])~~/\1,/g' | \
#					sed -r 's/([0-9]),([^0-9\"\{\}])/\1~~\2/g' | \
#					sed -r "s/[\'\"]//g" | uniq | \
#					awk -F, '{ 
#						for(i=1; i<=NF; i++) { 
#							printf "%s ",$i
#						} 
#					}' `
		filter_str=`echo $_json | \
					awk '{
						counter = 0
						newstr = ""
						for(i=1; i<=NF; i++) {
							if ($i ~ /"/) {
								counter += gsub(/"/, "", $i)
						    }
							if (counter % 2 > 0) {
								$i = $i"--"
								if ($i ~ /:/) {
									split($i, A, ":")
									gsub(/,/, "~~", A[length(A)])
									for(a=1; a<=length(A); a++){
										tmp = a!=1 ? tmp":"A[a] : A[a]
									}
									newstr=newstr""tmp
								} else {
									gsub(",", "~~", $i)
									newstr=newstr""$i
								}
							} else {
								newstr=newstr""$i
							} 
						}	
					    print newstr
					}' | \
					sed -r 's/\{(.*)\}/\1/' | \
					awk -F, '{
						for(i=1; i<=NF; i++) {
							printf "%s ",$i
						}
					}'`
	else
		filter_str=`echo $_json | \
					sed -r 's/\{(.*)\}/\1/' | \
					awk -F, '{
						for(i=1; i<=NF; i++) {
							printf "%s ",$i
						}
					}' `
	fi
	echo $filter_str
}


# recovery some feature of json string.
reverse_filter() {
	local _str=$1
	if grep -Eq '[\{\[]' <<< $_str;then
		result=`echo $_str |awk -F: '{
					newstr=""
					for(i=1; i<=NF; i++) {
						gsub(/[^\{\}\[\]\\:,[:space:]]+/, "\"&\"", $i)
						newstr = i!=1 ? newstr":"$i : $i
					}
					print newstr
				 }' | \
				 sed -r 's/"([0-9]+)"/\1/g'| \
				 sed -r 's/[:,]/& /g' | \
				 sed -r 's/--/ /g' | \
				 sed -r 's/~~/, /g' `
	else
		result=`echo $_str | \
				sed -r 's/--/ /g' | \
				sed -r 's/~~/, /g'`
	fi
	echo "$result"
}


# generate array string.
make_array() {
	local _json=$1
	local strings=`filter "$_json"`
	$debug && echo "\"Filter_strings:\" $strings"
	local counter=0
	for s in $strings; do
		if grep -Eq '(\{|\[)' <<< $s && ! grep -Eq '(\}|\])' <<< $s;then
			left_brackets=`echo $s |grep -oE '(\[|\{)' |wc -l`
			((counter+=left_brackets))
			newstr="${newstr}${s},"
		elif grep -Eq '(\]|\})' <<< $s && ! grep -Eq '(\{|\[)' <<< $s;then
			right_brackets=`echo $s |grep -oE '(\]|\})' |wc -l`
			((counter-=right_brackets))
			if ((counter <=0 ));then
				newstr="${newstr}${s} "
			else
				newstr="${newstr}${s},"
			fi
		elif grep -Eq '(\]|\})' <<< $s && grep -Eq '(\{|\[)' <<< $s; then
			left_brackets=`echo $s |grep -oE '(\[|\{)' |wc -l`
			right_brackets=`echo $s |grep -oE '(\]|\})' |wc -l`
			temp=$((right_brackets - left_brackets))
			((counter-=temp))	
			if ((counter <= 0));then
				newstr="${newstr}${s} "
			else
				newstr="${newstr}${s},"
			fi
		elif ((counter > 0)) ;then
			newstr="${newstr}${s},"
		else
			newstr="${newstr}${s} "
		fi
		$debug && echo $counter
	done
	echo $newstr
}


# fetch all keys in current layer of json.
get_keys() {
	local _ary=$1
	for i in $_ary;do
		echo $i |awk -F: '{print $1}'
	done
}


# fetch values of the key in current layer of json.
get_value() {
	local _ary=($1)
	local _keys=($2)
	local _field=$3
	local index=0
	for key in ${_keys[*]}; do
		if [ "$key" == "$_field" ];then
			echo ${_ary[$index]} | awk -F: '{
				newstr=""
				if(NF>2) {
					for(i=2; i<=NF; i++) {
						newstr = i!=NF ? newstr""$i":" : newstr""$i
					}
				} else {
					newstr=newstr""$2
				};
				print newstr
			}'
		fi
		((index++))
	done
}


# main function.
JsonParser() {
	case $# in
	1)
		local _field=$1
		read _json
	;;
	2)
		local _json=$1
		local _field=$2
	;;
	*)
		echo "Argument error."
		return 1
	;;
	esac

	local ary=(`make_array "$_json"`)
	local keys=(`get_keys "${ary[*]}"`)
	$debug && echo "\"make_array:\" ${ary[*]}"
	$debug && echo "\"keys:\" ${keys[*]}"

	if grep -q "__" <<< $_field ;then 
		keyname="${_field%%__*}"
		if grep -Pq "(?<=\w)\[[0-9]+\]" <<< "$keyname";then
			key=`echo $keyname | grep -oP "\w+(?=\[[0-9]+\])"`
			value=`get_value "${ary[*]}" "${keys[*]}" "${key}"`
			valueAry=(`make_array "$value"`)
			idx=`grep -oP '(?<=\[)[0-9]+(?=\])' <<< "$_field"`
			JsonParser "${valueAry[$idx]}" "${_field#*__}"
		else
			value=`get_value "${ary[*]}" "${keys[*]}" "$keyname"`
			JsonParser "$value" "${_field#*__}"
		fi
	elif grep -Pq "(?<=\w)\[[0-9]+\]"  <<< "$_field";then
		keyname=`echo $_field | grep -oP "\w+(?=\[[0-9]+\])"`
		value=`get_value "${ary[*]}" "${keys[*]}" "${keyname}"`
		valueAry=(`make_array "$value"`)
		idx=`grep -oP '(?<=\[)[0-9]+(?=\])' <<< "$_field"`
		reverse_filter "${valueAry[$idx]}"
	else
		value=`get_value "${ary[*]}" "${keys[*]}" "${_field}"`
		reverse_filter "$value"
	fi
}


# test strings
#jsonstr='{
#			"name": "Charles", 
#			"age": 25, 
#			"gender": "male", 
#			"aa": {
#				   "bb": "bbb",
#			       "cc": "ccc",
#				   "ff": {
#					   	   "gg": "ggg", 
#				   		   "ee": {
#							   	   "qq": "qqq", 
#						           "ww": {
#									     "tt": [1, 2, "aa, 100" ]
#										 }
#								 }
#						 }, 
#				   "dd": "ddd"
#				  },
#			"grade": [99, 89, {"yy": "yyy, 200"}],
#			"address": {"ww": "www"}
#		}'
#
#JsonParser "$jsonstr" "name"
#JsonParser "$jsonstr" "grade[1]"
#JsonParser "$jsonstr" "grade[2]__yy"
#JsonParser "$jsonstr" "aa__ff__ee__ww__tt[0]"
#JsonParser "$jsonstr" "aa"
