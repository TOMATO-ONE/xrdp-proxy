# rpmbuild方法
インストール直後の最小インストール構成のCentOS7から以下のコマンドでrpmパッケージを作成できます。

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
#  wget https://github.com/TOMATO-ONE/xrdp-proxy/raw/devel/centos/el7/SRPMS/neutrinordp-git836b738-1.el7.src.rpm
rpm -ivh neutrinordp-git836b738-1.el7.src.rpm

QA_RPATHS=0x0001 rpmbuild -ba --clean rpmbuild/SPECS/neutrinordp.spec


 sudo yum install -y ~/rpmbuild/RPMS/x86_64/neutrinordp-libs-git836b738-1.el7.x86_64.rpm \
   ~/rpmbuild/RPMS/x86_64/neutrinordp-devel-git836b738-1.el7.x86_64.rpm \
 		openssl pam-devel pkgconfig\(fuse\) pkgconfig\(pixman-1\) nasm checkpolicy selinux-policy-devel

# wget https://github.com/TOMATO-ONE/xrdp-proxy/raw/devel/centos/el7/SRPMS/xrdp-0.9.20-1.el7.src.rpm
rpm -ivh xrdp-0.9.20-1.el7.src.rpm

rpmbuild -ba --clean rpmbuild/SPECS/xrdp.spec

```
