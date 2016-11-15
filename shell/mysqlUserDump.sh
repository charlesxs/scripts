#!/bin/bash
#Description:  Mysql user dump and restore tools.
#Author: Charles
#Version: 1.0
#

#Debug
#set -x

# Global Settings
Mysqlbin=/usr/bin/mysql
Muser=root
#Mpassword=xiao
Mhost=127.0.0.1
db=mysql

# Optional 
ignoreUser=root
encrypt_userfile=yes

# Vector
action=$1
userfile=${2:-`pwd`/userfile}

usage() {
	echo "Usage:`basename $0` <dump|load> [filename]"
}

encrypt_file() {
	local file=$1
	local eaction=${2:-'encrypt'}
	key="a7d54081c1140e91cfe8d2ca4896615bd"
	case $eaction in
	'encrypt')
		if [ -f $file ];then
			openssl enc -des3 -k ${key} -in $file -out ${file}.data
			[ $? -ne 0 ] && echo "Encrypt failed! Did you install openssl?" && rm ${file}.data && return 2
			mv ${file}.data $file
		else
			echo "No such file"
			return 3
		fi
	;;
	'decrypt')
		if [ -f $file ];then
			openssl enc -des3 -d -k ${key} -in $file -out ${file}.txt
			[ $? -ne 0 ] && echo "Decrypt failed! Did you install openssl?" && rm ${file}.txt && return 2
			mv ${file}.txt $file
		else
			echo "No such file"
			return 3
		fi
	;;
	esac
}

mysql_query() {
	local db=$1
	local sql=$2
	if [ $Mpassword ];then
		$Mysqlbin -u$Muser -p$Mpassword -h$Mhost $db -e "$sql;"
		[ "$?" -ne 0 ] && return 1 || return 0
	else
		$Mysqlbin -u$Muser -h$Mhost $db -e "$sql;"
		[ "$?" -ne 0 ] && return 1 || return 0
	fi
}

case $action in
'dump')
	#get user list
	if [ -z "$ignoreUser" ];then
		userlist=`mysql_query  mysql "select user from user group by user" |sed '1d'`
	else
		loop=1
		srcsql="select user from user where user <>"
		condsql="and user <>"
		groupby="group by user"
		for user in $ignoreUser;do
			if [ $loop -eq 1 ];then
				srcsql="${srcsql} \"${user}\""
			else
				srcsql="${srcsql} ${condsql} \"${user}\""
			fi  
			((loop++))
		done
		sql="${srcsql} ${groupby}"
		userlist=`mysql_query  mysql "$sql" | sed '1d'`
	fi
			
	#dump user to file
	[ -z "$userlist" ] && echo "No user for dump." && exit 7
	[ -f "$userfile" ] && rm $userfile
	for user in $userlist; do
		UserInfo=`mysql_query  mysql "select user,host from user where user='$user'"`
		User=`echo "$UserInfo"|awk 'NR==2{print $1}'`
		IPlist=`echo "$UserInfo"|awk '!/user/{print $2}'`
		for ip in $IPlist;do
			mysql_query "mysql" "show grants for \`$User\`@\`$ip\`"
			[ "$?" -ne 0 ] && exit 2 
			echo 
		done >> $userfile
	done
	
	#encrypt userfile.
	if [ "$encrypt_userfile" == "yes" ];then
		encrypt_file $userfile "encrypt"	
		[ "$?" -ne 0 ] && exit 6
	fi
	echo "dump OK! dump file is $userfile."
;;
'load')
	[ ! -f $userfile ] && echo "No Such file." && exit 1
	#decrypt userfile.
	if [ "$encrypt_userfile" == "yes" ];then
		encrypt_file $userfile "decrypt"
		[ "$?" -ne 0 ] && exit 5
	fi

	#format user file
	sed -i '/Grants for/d' $userfile
	sed -i 's/`/\\`/g' $userfile

	#load user from userfile.
	while read sql;do
		if [ "$sql" ];then
			mysql_query "mysql" "$sql"
			[ "$?" -ne 0 ] && exit 4
		fi
	done < $userfile
	echo "restore ok."
;;
*)
	usage ;;
esac
