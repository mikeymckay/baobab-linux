Midori for the Iopener and IA-1
(see http://m4i.homeip.net/)

M4I is a variant of Transmeta's Midori Embedded Linux that was customized 
for the Iopener Network appliance and the very similar Compaq IA-1 (also 
known as "MSN Companion"). It is a fully-functional linux distribution that 
fits into 16MB of flash memory.

This folder contains everything needed to build an image file that
you can install onto your web appliance. It includes all the stuff that
will be part of the image- all contained in the 'root' directory, except
for the kernel, which is contained in the 'kernel' directory. 

The build script ('build') will (hopefully!) put everything together and 
generate your image. So, you can add or remove stuff from root and then run 
'build' to create a customized image. Note that if you run build with a
single 'w' as an argument (eg. './build w') then the winchip kernel will
be used (this is necessary for some early version Iopeners). Otherwise,
the kernel optimized for K6-2/3, Winchip 2 and Rise 266 CPUs will be used.

Once you've built a customized image, you'll probably want to install it 
onto your web appliance. This is easy if you are already running Linux (eg.
M4I or Jailbait)- copy the 'm4i-xxxx.img' image file to /tmp on your appliance 
and do 'dd if=/tmp/m4i-xxxx.img of=/dev/hdb'. I strongly urge you to also 
check the md5sum (run 'md5sum -c /tmp/m4i-xxxx.md5') to make sure that your 
image didn't get corrupted in transit. Note that if you haven't upgraded 
your memory to more than 32M, you will want to do this from the root console 
and you will want ot kill the X server and icewm to free up space for the 
16M image that you need to copy to the ram disk.

I hope that you find this stuff useful. 
Bob Dougherty

