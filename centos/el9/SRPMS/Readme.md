# rpmbuild方法
インストール直後の最小インストール構成のRockyLinux9から以下のコマンドでrpmパッケージを作成できます。  
```
dnf groupinstall -y "Development Tools"
dnf --enablerepo crb install -y gcc git cmake openssl-devel libX11-devel libXext-devel libXinerama-devel libXcursor-devel \
 libXdamage-devel libXv-devel libxkbfile-devel alsa-lib-devel cups-devel libjpeg-turbo-devel libXrandr-devel turbojpeg-devel pcsc-lite-devel \
 sudo wget which SDL2 hardlink imlib2-devel libXfont2-devel bash-completion

dnf install -y epel-release

useradd -m builduser
usermod -aG wheel builduser
echo "builduser:P@ssw0rd" | chpasswd
echo "builduser ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/builduser 
su - builduser
cd ~


#  wget https://github.com/TOMATO-ONE/xrdp-proxy/raw/devel/centos/el9/SRPMS/neutrinordp-git836b738-1.el9.src.rpm
rpm -ivh neutrinordp-git836b738-1.el9.src.rpm

rpmbuild -ba --clean ~/rpmbuild/SPECS/neutrinordp.spec


sudo dnf install --enablerepo crb -y openssl pam-devel pkgconfig\(fuse\) pkgconfig\(pixman-1\) nasm checkpolicy selinux-policy-devel \
 ~/rpmbuild/RPMS/x86_64/neutrinordp-libs-git836b738-1.el9.x86_64.rpm \
 ~/rpmbuild/RPMS/x86_64/neutrinordp-devel-git836b738-1.el9.x86_64.rpm

#  wget https://github.com/TOMATO-ONE/xrdp-proxy/raw/devel/centos/el9/SRPMS/xrdp-0.9.20-1.el9.src.rpm

rpm -ivh xrdp-0.9.20-1.el9.src.rpm

rpmbuild -ba --clean ~/rpmbuild/SPECS/xrdp.spec

```
※2022.09.19 RockyLinux 9.0 の docker image での build を確認しています。
