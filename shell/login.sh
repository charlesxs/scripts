#!/bin/bash
#

ssh_exec() {
    local _uhost="$1"
    local _pass="$2"
    local _cmd="${@:3}"
    expect -c "set timeout -1;
    spawn -noecho ssh -p 2001 -o StrictHostKeyChecking=no $_uhost $_cmd;
    expect {
		*password: {
			send ${_pass}\r;
		}
	}
    interact;";
}


ssh_exec "user@10.16.2.122" "xxx" "/sbin/ifconfig eth0"

