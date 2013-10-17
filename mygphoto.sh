#!/bin/bash
#
dev=`gphoto2 --auto-detect | grep usb | cut -b 36-42 | sed 's/,/\//'`
if [ -z ${dev} ]
then
   echo "Error: Camera not found"
   exit
fi
./usbreset/usbreset /dev/bus/usb/${dev}
gphoto2 $@
./usbreset/usbreset /dev/bus/usb/${dev}
