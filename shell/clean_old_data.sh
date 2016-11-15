#!/bin/bash
#
# clean the old data of expires N days.
#

# Separated by spaces if you have several directories.
DIRS="/data1/dbbackup "
EXCLUDE_DIRS="/data1/dbbackup/git-2.23/git
			  /data1/dbbackup/jlsoft_bug_2.18/webcode
			  /data1/dbbackup/newgit_2.12/gitlab
			  /data1/dbbackup/newgit_2.12/gitlab_data
			  /data1/dbbackup/svnbackup_0.196
			  "
TRASH="/data1/Trash"

# expires N days.
EXPIRES=10

# remove empty directoires. 
REMOVE_EMPTY_DIR=true

# debug
DEBUG=false

# move
MOVE="/bin/mv -f --backup=numbered"




find_dir() {
	local _dir=$1
	find $_dir -mindepth 1 -maxdepth 1 -type d
}

check_exclude() {
	local _dir=$1
	for edir in $EXCLUDE_DIRS; do
		[[ "${_dir%/}" == ${edir%/} ]] && return 1
	done

	return 0
}

clean_data() {
	local _dir=$1
	
	if check_exclude "$_dir";then
		if $DEBUG; then
			# file
			find $_dir -mindepth 1 -maxdepth 1 -type f -mtime +$EXPIRES -printf "\033[33mmtime:[%AF %AT] %p\n\033[0m"
			# empty directires
			[[ $REMOVE_EMPTY_DIR ]] && find $_dir -mindepth 1 -maxdepth 1 -type d -mtime +$EXPIRES -empty -printf "\033[33mmtime:[%AF %AT] %p\n\033[0m"
		else
			# file
			find $_dir -mindepth 1 -maxdepth 1 -type f -mtime +$EXPIRES -print -exec $MOVE {} $TRASH \;
			# empty directires
			[[ $REMOVE_EMPTY_DIR ]] && find $_dir -mindepth 1 -maxdepth 1 -type d -mtime +$EXPIRES -empty -print -delete
		fi

		subdirs=`find_dir $_dir`
		if [[ "$subdirs" ]];then
			for sdir in $subdirs;do
				clean_data $sdir
			done
		fi
	fi
}

main() {
	# init trash dir
	[ ! -d "$TRASH" ] && mkdir -p $TRASH

	echo -e "[`date +'%F %T'`] start clear data.\n====================================="
	# clean data
	for dir in $DIRS; do
		clean_data $dir	
	done

	echo -e "=====================================\n[`date +'%F %T'`] end clear data. \n"
}


# main
main

