# rpmbuild方法
インストール直後の最小インストール構成のRockyLinux8/Almalinux8/CentOS8から以下のコマンドでrpmパッケージを作成できます。  
```
dnf groupinstall -y "Development Tools"
dnf --enablerepo powertools install -y gcc git cmake openssl-devel libX11-devel libXext-devel libXinerama-devel libXcursor-devel \
 libXdamage-devel libXv-devel libxkbfile-devel alsa-lib-devel cups-devel libjpeg-turbo-devel libXrandr-devel turbojpeg-devel pcsc-lite-devel \
 sudo wget which SDL2 hardlink imlib2-devel libXfont2-devel

dnf install -y epel-release

useradd -m builduser
usermod -aG wheel builduser
echo "builduser:P@ssw0rd" | chpasswd
echo "builduser ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/builduser 
su - builduser
cd ~


#  wget https://github.com/TOMATO-ONE/xrdp-proxy/raw/devel/centos/el8/SRPMS/neutrinordp-gitf7832d6-1.el8.src.rpm
rpm -ivh neutrinordp-gitf7832d6-1.el8.src.rpm

rpmbuild -ba --clean ~/rpmbuild/SPECS/neutrinordp.spec


sudo dnf install --enablerepo powertools -y openssl pam-devel pkgconfig\(fuse\) pkgconfig\(pixman-1\) nasm checkpolicy selinux-policy-devel \
 ~/rpmbuild/RPMS/x86_64/neutrinordp-libs-gitf7832d6-1.el8.x86_64.rpm \
 ~/rpmbuild/RPMS/x86_64/neutrinordp-devel-gitf7832d6-1.el8.x86_64.rpm

#  wget https://github.com/TOMATO-ONE/xrdp-proxy/raw/devel/centos/el8/SRPMS/xrdp-0.9.19-1.el8.src.rpm

rpm -ivh xrdp-0.9.19-1.el8.src.rpm

rpmbuild -ba --clean ~/rpmbuild/SPECS/xrdp.spec

```
※2022.06.19 RockyLinux 8.6 の docker image での build を確認しています。
