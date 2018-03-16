#!/bin/bash
# backup mysql data.
# user xtrabackup to do that.
# every week backup a full version.
# every day backup a update version.
export PATH=/bin:/sbin:/usr/bin:/usr/sbin

full_option="--host=127.0.0.1 --port=3306 --user=xxx --password=xxx --use-memory=1G --defaults-file=/opt/mysql/my.cnf"
rsync_host="x.x.x.x"
rsync_module="dbbackup/"
target_dir="/opt/dbbackup/"
log_dir="/opt/shells/logs"
admin_email="admin@xxx.com"

date=$(date +%Y%m%d)
innobackupex="/usr/bin/innobackupex"
incre_option="$full_option --incremental"
today_dir="$target_dir/$date"
full_dir="$today_dir/full"
incre_dir="$today_dir/incre"

makeDir() {
    if [ ! -d $1 ];then
        mkdir -p $1
    fi
}


fullBack() {
    makeDir $full_dir
    $innobackupex $full_option $full_dir >> $log_dir/dbbackup.log 2>&1
    if [ $? == "0" ];then
        echo "$date Full backup sucessufully!" >> $log_dir/dbbackup.res
        echo "$full_dir/$(ls -t $full_dir | head -n 1)" > $log_dir/befull_dir.txt
    else
        echo "$date Backup Error" >> $log_dir/dbbackup.res
        return 10
    fi
}


increBack() {
    makeDir $incre_dir
    basedir=$(cat $log_dir/befull_dir.txt)
    $innobackupex $incre_option --incremental-basedir=$basedir $incre_dir  >> $log_dir/dbbackup.log 2>&1
    if [ $? == "0" ];then
        echo "$date Increment backup succuessfully!" >> $log_dir/dbbackup.res
    else
        echo "$date Backup Error!" >> $log_dir/dbbackup.res
        return 11
    fi
}

rsyncFile() {
    dir=$1
    types=$2
    filename="$dir.$types.tar.bz2"
    cd $(dirname $dir)
    dir=$(basename $dir)
    tar cjf $filename $dir
    rsync -avz $filename $rsync_host::$rsync_module >> $log_dir/dbbackup.log 2>&1
    rm -f $filename
}

clearOldFile() {
    cd $target_dir
    days=$(ls -l | wc -l)
    if [ $days -gt 8 ];then
        ls -rl | awk 'NR!=1 && NR>8 { print $9 }' | xargs rm -rf
    fi   
}


send_wechat() {
	local _message=$1; shift
	local _users=$*

	# urlencode
	local _msg=`echo $_message | sed 's/ /%20/g;
							  s/!/%21/g;
							  s/"/%22/g;
							  s/#/%23/g;
							  s/\&/%26/g;
							  s/'\''/%28/g;
							  s/(/%28/g;
							  s/)/%29/g;
							  s/:/%3A/g;
							  s/\//%2F/g;
                              s/\[/%5B/g;
                              s/\]/%5D/g'`

	for user in $_users; do
		curl http://isms.xxx.com/weixin.php?user=$user\&info="$_msg"\&channel=backup
	done
}

makeDir $log_dir
makeDir $target_dir
clearOldFile
case "$1" in
    incre)
        increBack && \
		rsyncFile $today_dir incre && \
		clearOldFile && \
		send_wechat "DB incremental backup succuessfully." "username" 
		
		[ $? -ne 0 ] && send_wechat "DB incremental backup failed." "username"
        ;;
    full)
        fullBack && \
		rsyncFile $today_dir full && \
		clearOldFile && \
		send_wechat "DB full backup sucessfully." "username"
		
		[ $? -ne 0 ] && send_wechat "DB full backup failed." "username"
        ;;
    *)
        echo "Usage: script incre|full"
        ;;
esac
