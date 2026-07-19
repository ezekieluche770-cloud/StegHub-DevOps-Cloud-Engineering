# DevOps Tooling Website Solution

## Introduction

This project involves implementation of a solution that consists of the following components:

- **Infrastructure:** AWS
- **Web Server Linux:** Red Hat Enterprise Linux 9
- **Database Server:** Ubuntu Linux + MySQL
- **Storage Server:** Red Hat Enterprise Linux 9 + NFS Server
- **Programming Language:** PHP
- **Code Repository:** GitHub

The diagram below shows the architecture of the solution.

![Architecture](./img/image1.png)

## Step 1 - Prepare NFS Server

1. Spin up an EC2 instance with RHEL Operating System

![RHEL EC2 Instance](./img/image2.png)

2. Configure Logical volume management on the server

Format the lvm as xfs

Create 3 Logical volumes: lv-opt, lv-apps, lv-logs.

Create mount points on /mnt directory for the logical volumes as follows:

- Mount lv-apps on /mnt/apps - To be used by web servers
- Mount lv-logs on /mnt/logs - To be used by web server logs
- Mount lv-opt on /mnt/opt - To be used by Jenkins server in next project.

Create 3 volumes in the same AZ as the NFS Server EC2 each of 10GB and attach all 3 volumes one by one to the NFS Server.

![Attach Volumes](./img/image3.png)

Open up the Linux terminal to begin configuration.

```
ssh -i "my-ec2-key.pem" ec2-user@ec2-34-229-222-243
```

![SSH into NFS Server](./img/image4.png)

Use `lsblk` to inspect what block devices are attached to the server. All devices in Linux reside in /dev/ directory. Inspect with `ls /dev/` and ensure all 3 newly created devices are there. Their name will likely be `xvdf`, `xvdg` and `xvdh`.

```
lsblk
```

![lsblk output](./img/image5.png)

Use `gdisk` utility to create a single partition on each of the 3 disks

```
sudo gdisk /dev/nvme1n1
```

![gdisk nvme1n1](./img/image6.png)

```
sudo gdisk /dev/nvme2n1
```

![gdisk nvme2n1](./img/image7.png)

```
sudo gdisk /dev/nvme3n1
```

![gdisk nvme3n1](./img/image8.png)

Use `lsblk` utility to view the newly configured partitions on each of the 3 disks

```
lsblk
```

![lsblk partitions](./img/image9.png)

Install `lvm` package

```
sudo yum install lvm2 -y
```

![Install LVM2](./img/image10.png)

Use `pvcreate` utility to mark each of the 3 disks as physical volumes (PVs) to be used by LVM. Verify that each of the volumes have been created successfully

```
sudo pvcreate /dev/nvme1n1p1 /dev/nvme2n1p1 /dev/nvme3n1p1
sudo pvs
```

![PV Create](./img/image11.png)

Use `vgcreate` utility to add all 3 PVs to a volume group (VG). Name the VG `webdata-vg`. Verify that the VG has been created successfully

```
sudo vgcreate webdata-vg /dev/nvme1n1p1 /dev/nvme2n1p1 /dev/nvme3n1p1
sudo vgs
```

![VG Create](./img/image12.png)

Use `lvcreate` utility to create 3 logical volumes, `lv-apps`, `lv-logs` and `lv-opt`. Verify that the logical volumes have been created successfully

```
sudo lvcreate -n lv-apps -L 9G webdata-vg
sudo lvcreate -n lv-logs -L 9G webdata-vg
sudo lvcreate -n lv-opt -L 9G webdata-vg

sudo lvs
```

![LV Create](./img/image13.png)

Verify the entire setup

```
sudo vgdisplay -v   #view complete setup, VG, PV and LV
```

![VG Display](./img/image14.png)

```
lsblk
```

![lsblk final](./img/image15.png)

Use `mkfs -t xfs` to format the logical volumes instead of ext4 filesystem

```
sudo mkfs -t xfs /dev/webdata-vg/lv-apps
sudo mkfs -t xfs /dev/webdata-vg/lv-logs
sudo mkfs -t xfs /dev/webdata-vg/lv-opt
```

![mkfs xfs](./img/image16.png)

Create mount points on `/mnt` directory

```
sudo mkdir /mnt/apps
sudo mkdir /mnt/logs
sudo mkdir /mnt/opt
sudo mount /dev/webdata-vg/lv-apps /mnt/apps
sudo mount /dev/webdata-vg/lv-logs /mnt/logs
sudo mount /dev/webdata-vg/lv-opt /mnt/opt
```

![Mount points](./img/image17.png)

3. Install NFS Server, configure it to start on reboot and ensure it is up and running.

```
sudo yum update -y
sudo yum install nfs-utils -y
```

![Install NFS Utils](./img/image18.png)

```
sudo systemctl start nfs-server.service
sudo systemctl enable nfs-server.service
sudo systemctl status nfs-server.service
```

![NFS Server Status](./img/image19.png)

4. Export the mounts for Webservers' subnet cidr (IPv4 cidr) to connect as clients. For simplicity, all 3 Web Servers are installed in the same subnet but in production setup, each tier should be separated inside its own subnet for higher level of security.

Set up permission that will allow the Web Servers to read, write and execute files on NFS.

```
sudo chown -R nobody: /mnt/apps
sudo chown -R nobody: /mnt/logs
sudo chown -R nobody: /mnt/opt

sudo chmod -R 777 /mnt/apps
sudo chmod -R 777 /mnt/logs
sudo chmod -R 777 /mnt/opt

sudo systemctl restart nfs-server.service
```

![NFS Permissions](./img/image20.png)

Configure access to NFS for clients within the same subnet (example Subnet Cidr - 172.31.16.0/20)

```
sudo vi /etc/exports

/mnt/apps 172.31.16.0/20(rw,sync,no_all_squash,no_root_squash)
/mnt/logs 172.31.16.0/20(rw,sync,no_all_squash,no_root_squash)
/mnt/opt 172.31.16.0/20(rw,sync,no_all_squash,no_root_squash)

sudo exportfs -arv
```

![ExportFS](./img/image21.png)

![ExportFS verify](./img/image22.png)

5. Check which port is used by NFS and open it using the security group (add new inbound rule)

```
rpcinfo -p | grep nfs
```

![NFS Ports](./img/image23.png)

**Note:** For NFS Server to be accessible from the client, the following ports must be opened: TCP 111, UDP 111, UDP 2049, NFS 2049. Set the Web Server subnet cidr as the source.

![Security Group Ports](./img/image24.png)

## Step 2 - Configure the Database Server

Launch an Ubuntu EC2 instance that will have a role - DB Server

![Ubuntu DB Instance](./img/image25.png)

Access the instance to begin configuration.

```
ssh -i "my-ec2-key.pem" ubuntu@ec2-54-91-132-50
```

![SSH DB Server](./img/image26.png)

Update and upgrade Ubuntu

```
sudo apt update && sudo apt upgrade -y
```

![Update Ubuntu](./img/image27.png)

1. Install MySQL Server

```
sudo apt install mysql-server
```

![Install MySQL](./img/image28.png)

Run mysql secure script

```
sudo mysql_secure_installation
```

![MySQL Secure Installation](./img/image29.png)

2. Create a database and name it `tooling`
3. Create a database user and name it `webaccess`
4. Grant permission to `webaccess` user on `tooling` database to do anything only from the webservers' subnet cidr

```
sudo mysql

CREATE DATABASE tooling;
CREATE USER 'webaccess'@'172.31.16.0/20' IDENTIFIED BY 'PassWord.1';
GRANT ALL PRIVILEGES ON tooling.* TO 'webaccess'@'172.31.16.0/20' WITH GRANT OPTION;
FLUSH PRIVILEGES;
show databases;

use tooling;
select host, user from mysql.user;
exit
```

![MySQL Setup](./img/image30.png)

Set Bind Address and restart MySQL

```
sudo vi /etc/mysql/mysql.conf.d/mysqld.cnf

sudo systemctl restart mysql
sudo systemctl status mysql
```

![MySQL Bind Address](./img/image31.png)

![MySQL Status](./img/image32.png)

Open MySQL port 3306 on the DB Server EC2.

Access to the DB Server is allowed only from the `Subnet Cidr` configured as source.

![MySQL Security Group](./img/image33.png)

## Step 3 - Prepare the Web Servers

There is need to ensure that the Web Servers can serve the same content from a shared storage solution, in this case - NFS and MySQL database. One DB can be accessed for `read` and `write` by multiple clients. For storing shared files that the Web Servers will use, NFS is utilized and previously created Logical Volume `lv-apps` is mounted to the folder where Apache stores files to be served to the users (`/var/www`).

This approach makes the Web server `stateless` which means they can be replaced when needed and data (in the database and on NFS) integrity is preserved.

In further steps, the following was done:

- Configured NFS (This step was done on all 3 servers)
- Deployed a tooling application to the Web Servers into a shared NFS folder
- Configured the Web Server to work with a single MySQL database

### Web Server 1

1. Launch a new EC2 instance with RHEL Operating System

![Web Server 1 RHEL](./img/image34.png)

2. Install NFS Client

```
sudo yum install nfs-utils nfs4-acl-tools -y
```

![Install NFS Client WS1](./img/image35.png)

3. Mount `/var/www/` and target the NFS server's export for `apps`. NFS Server private IP address = 172.31.25.85

```
sudo mkdir /var/www
sudo mount -t nfs -o rw,nosuid 172.31.25.85:/mnt/apps /var/www
```

4. Verify that NFS was mounted successfully by running `df -h`. Ensure that the changes will persist after reboot.

![df -h WS1](./img/image36.png)

```
sudo vi /etc/fstab
```

Add the following line

```
172.31.25.85:/mnt/apps /var/www nfs defaults 0 0
```

![fstab WS1](./img/image37.png)

5. Install Remi's repository, Apache and PHP

```
sudo yum install httpd -y
```

![Install httpd WS1](./img/image38.png)

```
sudo dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm
```

![Install EPEL WS1](./img/image39.png)

```
sudo dnf install dnf-utils http://rpms.remirepo.net/enterprise/remi-release-9.rpm
```

![Install Remi WS1](./img/image40.png)

```
sudo dnf module reset php
```

![PHP Reset WS1](./img/image41.png)

```
sudo dnf module enable php:remi-8.2
```

![PHP Enable WS1](./img/image42.png)

```
sudo dnf install php php-opcache php-gd php-curl php-mysqlnd
```

![Install PHP WS1](./img/image43.png)

```
sudo systemctl start php-fpm
sudo systemctl enable php-fpm
sudo systemctl status php-fpm

sudo setsebool -P httpd_execmem 1
sudo setsebool -P httpd_can_network_connect=1
sudo setsebool -P httpd_can_network_connect_db=1
```

![PHP-FPM and SELinux WS1](./img/image44.png)

### Web Server 2

![Web Server 2 RHEL](./img/image45.png)

2. Install NFS Client

```
sudo yum install nfs-utils nfs4-acl-tools -y
```

![Install NFS Client WS2](./img/image46.png)

3. Mount `/var/www/` and target the NFS server's export for `apps`. NFS Server private IP address = 172.31.25.85

```
sudo mkdir /var/www
sudo mount -t nfs -o rw,nosuid 172.31.25.85:/mnt/apps /var/www
```

4. Verify that NFS was mounted successfully by running `df -h`. Ensure that the changes will persist after reboot.

```
sudo vi /etc/fstab
```

Add the following line

```
172.31.25.85:/mnt/apps /var/www nfs defaults 0 0
```

![fstab WS2](./img/image47.png)

5. Install Remi's repository, Apache and PHP

```
sudo yum install httpd -y
```

![Install httpd WS2](./img/image48.png)

```
sudo dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm
```

![Install EPEL WS2](./img/image49.png)

```
sudo dnf install dnf-utils http://rpms.remirepo.net/enterprise/remi-release-9.rpm
```

![Install Remi WS2](./img/image50.png)

```
sudo dnf module reset php
```

![PHP Reset WS2](./img/image51.png)

```
sudo dnf module enable php:remi-8.2
```

![PHP Enable WS2](./img/image52.png)

```
sudo dnf install php php-opcache php-gd php-curl php-mysqlnd
```

![Install PHP WS2](./img/image53.png)

```
sudo systemctl start php-fpm
sudo systemctl enable php-fpm
sudo systemctl status php-fpm
sudo setsebool -P httpd_execmem 1
```

![PHP-FPM WS2](./img/image54.png)

### Web Server 3

![Web Server 3 RHEL](./img/image55.png)

2. Install NFS Client

```
sudo yum install nfs-utils nfs4-acl-tools -y
```

![Install NFS Client WS3](./img/image56.png)

3. Mount `/var/www/` and target the NFS server's export for `apps`. NFS Server private IP address = 172.31.25.85

```
sudo mkdir /var/www
sudo mount -t nfs -o rw,nosuid 172.31.25.85:/mnt/apps /var/www
```

4. Verify that NFS was mounted successfully by running `df -h`. Ensure that the changes will persist after reboot.

![df -h WS3](./img/image57.png)

```
sudo vi /etc/fstab
```

Add the following line

```
172.31.25.85:/mnt/apps /var/www nfs defaults 0 0
```

![fstab WS3](./img/image58.png)

5. Install Remi's repository, Apache and PHP

```
sudo yum install httpd -y
```

![Install httpd WS3](./img/image59.png)

```
sudo dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm
```

![Install EPEL WS3](./img/image60.png)

```
sudo dnf install dnf-utils http://rpms.remirepo.net/enterprise/remi-release-9.rpm
```

![Install Remi WS3](./img/image61.png)

```
sudo dnf module reset php
```

![PHP Reset WS3](./img/image62.png)

```
sudo dnf module enable php:remi-8.2
```

![PHP Enable WS3](./img/image63.png)

```
sudo dnf install php php-opcache php-gd php-curl php-mysqlnd
```

![Install PHP WS3](./img/image64.png)

```
sudo systemctl start php-fpm
sudo systemctl enable php-fpm
sudo systemctl status php-fpm
sudo setsebool -P httpd_execmem 1
```

![PHP-FPM WS3](./img/image65.png)

6. Verify that Apache files and directories are available on the Web Servers in `/var/www` and also on the NFS Server in `/mnt/apps`. If the same files are present in both, it means NFS was mounted correctly. `test.txt` file was created from Web Server 1, and it was accessible from Web Server 2.

![Verify NFS mount 1](./img/image66.png)

![Verify NFS mount 2](./img/image67.png)

7. Locate the log folder for Apache on the Web Server and mount it to NFS server's export for logs. Repeat step 4 to ensure the mount point persists after reboot.

First create the mount point:

```
sudo mkdir -p /var/log/httpd
```

Mount the NFS log share:

```
sudo mount -t nfs4 172.31.25.85:/mnt/logs /var/log/httpd
```

Verify:

```
mount | grep httpd
```

![Mount logs WS1](./img/image68.png)

Repeat on Web Server 2

![Mount logs WS2](./img/image69.png)

Repeat on Web Server 3

![Mount logs WS3](./img/image70.png)

Make the mount persistent on each Web Server

Open /etc/fstab on each web server:

```
sudo vi /etc/fstab
```

Add a line like:

```
172.31.25.85:/mnt/logs   /var/log/httpd   nfs4   defaults,_netdev   0   0
```

![fstab logs WS1](./img/image71.png)

![fstab logs WS2](./img/image72.png)

![fstab logs WS3](./img/image73.png)

Confirm the names of the exported directories (whether they're /mnt/apps, /mnt/logs, and /mnt/opt)

![Exported directories](./img/image74.png)

8. Fork the tooling source code from StegHub GitHub Account

![GitHub Fork](./img/image75.png)

9. Deploy the tooling Website's code to the Web Server. Ensure that the `html` folder from the repository is deployed to `/var/www/html`

Install Git

![Install Git](./img/image76.png)

Initialize the directory and clone the tooling repository

Ensure to clone the forked repository

![Clone repository](./img/image77.png)

**Note:** Access the website on a browser

Ensure TCP port 80 is open on the Web Server.

If `403 Error` occurs, check permissions to the `/var/www/html` folder and also disable SELinux

```
sudo setenforce 0
```

To make the change permanent, open selinux file and set selinux to disable.

```
sudo vi /etc/sysconfig/selinux

SELINUX=disabled

sudo systemctl restart httpd
```

![Disable SELinux](./img/image78.png)

10. Update the website's configuration to connect to the database (in `/var/www/html/functions.php` file). Apply `tooling-db.sql` command

```
sudo mysql -h <db-private-IP> -u <db-username> -p <db-password < tooling-db.sql
```

```
sudo vi /var/www/html/functions.php
```

![functions.php](./img/image79.png)

```
cd tooling/
sudo mysql -h 172.31.30.214 -u webaccess -p tooling < tooling-db.sql
```

Access the database server from Web Server

```
sudo mysql -h 172.31.30.214 -u webaccess -p
```

![Access DB](./img/image80.png)

11. Create in MySQL a new admin user with username: `myuser` and password: `password`

```
INSERT INTO users(id, username, password, email, user_type, status) VALUES (2, 'myuser', '5f4dcc3b5aa765d61d8327deb882cf99', 'user@mail.com', 'admin', '1');
```

![Insert admin user](./img/image81.png)

12. Open a browser and access the website using the Web Server public IP address `http://<Web-Server-public-IP-address>/index.php`. Ensure login into the website with `myuser` user.

### From Web Server 1

![Web Server 1 login](./img/image82.png)

![Web Server 1 dashboard](./img/image83.png)

### From Web Server 2

Check Apache status

Run:

```
sudo systemctl status httpd
```

If it says inactive, start it:

```
sudo systemctl start httpd
sudo systemctl enable httpd
```

![Apache status WS2](./img/image84.png)

Disable SELinux

```
sudo setenforce 0

SELINUX=disabled
```

![Disable SELinux WS2](./img/image85.png)

Access the website

![Web Server 2 login](./img/image86.png)

![Web Server 2 dashboard](./img/image87.png)
