#!/bin/bash

#Kiem tra quyen root
if [ "$EUID" -ne 0 ]; then
	echo "Please run as root!"
	exit
fi

echo "Running.."

date_exec=$(date --date="5 minutes ago" "+%F %H:%M:%S")

#Lay cac phien dang nhap ssh tu 5 phut truoc
cur_ssh_str="$(journalctl -u ssh --since="$date_exec" | grep "Accepted password")"

log_file="/var/log/sshmonitor.log"
messages=()
mail_content=""
readarray -t cur_ssh_arr <<< "$cur_ssh_str"

echo -e "[Log sshmonitor - $date_exec]\n" > "$log_file"

#Setup thong tin cac phien dang nhap moi
for conn in "${cur_ssh_arr[@]}"
do
	if [[ "$conn" != "" ]]; then
		date_conn="$(echo "$conn" | awk '{printf "%s %s %s",$1,$2,$3}')"
		date_to_show=$(date --date="$date_conn" "+%H:%M:%S %d/%m/%Y")
		message=$(echo "User" "$(echo "$conn" | awk '{printf $9}')" "dang nhap thanh cong vao thoi gian" "$date_to_show.")
		messages+=("$message")
		mail_content="$mail_content$message\n"
	fi
done
if [ "${#messages[@]}" == 0 ]; then
	messages+=("Khong co ket noi nao moi.")
fi

#Ghi thong tin ra file log va gui email
for message in "${messages[@]}"
do
	echo -e "$message\n" >> "$log_file"
done
echo "Updated /var/log/sshmonitor.log."

if [ -z "$(dpkg -l | grep mailutils)" ]; then
	echo "mailutils package not found!"
	exit
fi

if [ "$mail_content" != "" ]; then
	echo -e "$mail_content" | mail -s "[Log sshmonitor - $date_exec]" root@localhost
	echo "Email is sent to root@localhost"
fi
