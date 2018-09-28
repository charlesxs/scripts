#!/bin/bash
#

exec 5<>a
while read -u5 host; do
    echo "\033[32mfix $host ~*~: \033[0m"
    ssh -n xs.xiao@$host '
    systemctl cat icinga2.service |grep "Restart"
    '

done
    #grep "icinga" /home/q/nrpe/etc/nrpe.cfg || { sudo sed -i "\$a\command[check_procs_icinga]=/home/q/nrpe/libexec/check_procs -c 1: -C icinga2" /home/q/nrpe/etc/nrpe.cfg; sudo /etc/init.d/q-nrpe restart; }
    #grep "Restart" /usr/lib/systemd/system/icinga2.service || { sudo sed -i "/#LimitNPROC/a\Restart=on-failure\nRestartSec=42s" /usr/lib/systemd/system/icinga2.service; sudo systemctl daemon-reload; }
    #grep "Restart" /usr/lib/systemd/system/icinga2.service || { sudo sed -i "/^TimeoutStartSec/a\Restart=on-failure\nRestartSec=42s" /usr/lib/systemd/system/icinga2.service; sudo systemctl daemon-reload; }
