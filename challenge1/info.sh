echo -e "[Thong tin he thong]\n"
echo "Ten may:" $(hostnamectl | grep "Static hostname" | cut -d: -f2 | xargs)
echo "Ten ban phan phoi:" $(hostnamectl | grep "Operating System" | cut -d: -f2 | xargs)
echo "Ten he dieu hanh:" $(hostnamectl | grep "Kernel" | cut -d: -f2 | xargs)

echo -e "\n[Thong tin CPU]\n"
echo -e "Ten CPU:" $(lscpu | grep "Model name" | cut -d: -f2 | xargs)
echo -e "Kien truc:" $(lscpu | grep "Architecture" | cut -d: -f2 | xargs)
echo -e "Toc do:" $(lscpu | grep "CPU MHz" | cut -d: -f2 | xargs)

echo -e "\n[Thong tin o cung]\n"
df -h --output=source,size,used,avail

echo -e "\n[Danh sach dia chi IP]\n"

echo -e "\n[Danh sach cac user]\n"
awk -F: '{print $1}' /etc/passwd

echo -e "\n[Danh sach cac process dang chay voi quyen root]\n"
ps -U root | sort

echo -e "\n[Danh sach cac port dang mo]\n"
cat /etc/services | grep -E "[0-9]/[a-z]"

echo -e "\n[Cac folder co the duoc ghi boi other]\n"
find / -type d -perm -o=w 2> /dev/null

echo -e "\n[Cac package da cai dat]\n"
dpkg-query -W -f='${binary:Package} ${Version}\n'
