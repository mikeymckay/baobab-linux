echo "Mounting"
mount /dev/sda1 /tmp/tmp
echo "Flashing"
dd if=/tmp/tmp/m4i-23~1.img of=/dev/hdb
echo "Rebooting"
reboot
