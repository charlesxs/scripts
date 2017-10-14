#!/bin/bash
#

ssh_run() {
    local _uhost="$1"
    local _pass="$2"
    local _cmd="${@:3}"
    expect -c "set timeout -1;
    spawn -noecho ssh -p 22 -o StrictHostKeyChecking=no $_uhost $_cmd;
    expect {
        yes/no* {
            send yes\r;
            exp_continue;
        };
		*password: {
			send ${_pass}\r;
		}
	}
    interact;";
}


ssh_run "user@172.16.2.122" "password" "/sbin/ifconfig eth0"

