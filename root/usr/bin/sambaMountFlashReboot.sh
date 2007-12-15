echo "Mounting via network"
smbmnt //192.168.1.169/ /tmp/tmp
echo "Flashing"
dd if=/tmp/tmp/m4i-23~1.img of=/dev/hdb
echo "Rebooting"
reboot
