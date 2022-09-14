#!/bin/bash
backup_file="/home/deathclick/Desktop/etc_backup.txt"
log_file="/var/log/checketc.log"
edited_files=()
created_files=()
deleted_files=()

#Check running with root
if [ "$EUID" -ne 0 ]; then
	echo "Please run as root!"
	exit
fi

#Kiem tra $backup_file da duoc tao chua
if [ ! -e "$backup_file" ]; then
	echo "$(find /etc -type f)" > "$backup_file"
	echo -e "First run, file $backup_file created.\nExit the program.."
	exit
fi

echo "Running.."

#Tim cac file chinh sua lan cuoi tu 30 phut truoc va gan vao $cur_modified
readarray -t cur_modified <<< "$(find /etc -type f -mmin -30)"
#List cac file trong /etc va gan vao $new_etc
readarray -t new_etc <<< "$(find /etc -type f)"
#List cac file trong /etc truoc day, gan vao $old_etc
readarray -t old_etc <<< "$(cat $backup_file)"

for file in "${cur_modified[@]}"
do
	if [[ ! -z "$file" ]]; then
		if [[ ! "${old_etc[@]}" =~ "$file" ]]; then
			created_files+=("$file")
		else
			edited_files+=("$file")
		fi
	fi
done

for file in "${old_etc[@]}"
do
	if [[ ! -e "$file" ]]; then
		deleted_files+=("$file")
	fi
done

#Show thong tin
date=$(date "+%H:%M:%S %d/%m/%Y")
echo "[Log checketc - $date]\n" > "$log_file"
echo -e "=====Danh sach file duoc tao moi=====\n" >> "$log_file"
for file in "${created_files[@]}"
do
	echo -e "$file \n" >> "$log_file"
	head -10 "$file" >> "$log_file"	
	echo -e "\n" >> "$log_file"
done

echo -e "=====Danh sach file bi chinh sua=====\n" >> "$log_file"
for file in "${edited_files[@]}"
do
	echo -e "$file \n" >> "$log_file"
done

echo -e "=====Danh sach cac file bi xoa=====\n" >> "$log_file"
for file in "${deleted_files[@]}"
do
	echo -e "$file \n" >> "$log_file"
done

echo "Updated $log_file."

#Update $backup_file
echo "$(find /etc -type f)" > "$backup_file"
echo "Updated $backup_file."
