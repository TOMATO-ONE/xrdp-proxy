#BUILD方法

```
yum update -y
yum groupinstall -y "Development Tools"

yum install -y gcc git cmake openssl-devel libX11-devel libXext-devel libXinerama-devel libXcursor-devel \
libXdamage-devel libXv-devel libxkbfile-devel alsa-lib-devel cups-devel ffmpeg-devel libjpeg-turbo-devel libXrandr-devel turbojpeg-devel pcsc-lite-devel \
sudo wget which


useradd -m builduser
usermod -aG wheel builduser
echo "builduser:P@ssw0rd" | chpasswd
echo "ALL ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/builduser 
su - builduser
cd ~
# wget 
rpm -ivh NeutrinoRDP-devel-2.el7.src.rpm

QA_RPATHS=0x0001 rpmbuild -ba --clean rpmbuild/SPECS/neutrinordp.spec


 sudo yum install -y ~/rpmbuild/RPMS/x86_64/NeutrinoRDP-devel-devel-2.el7.x86_64.rpm ~/rpmbuild/RPMS/x86_64/NeutrinoRDP-libs-devel-2.el7.x86_64.rpm \
 		openssl pam-devel pkgconfig\(fuse\) pkgconfig\(pixman-1\) nasm checkpolicy selinux-policy-devel

rpm -ivh xrdp-0.9.15-3a.el7.src.rpm

rpmbuild -ba --clean rpmbuild/SPECS/xrdp.spec

```
