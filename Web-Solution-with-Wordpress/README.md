# Web Solution With WordPress

## 1. The Business Problem

A growing team needed a self-managed CMS platform that could separate application and database concerns from day one — without locking into an all-in-one server that becomes a single point of failure. The goal was a two-tier WordPress deployment where the web layer and data layer could be scaled, patched, and secured independently, while keeping the database off the public internet entirely.

---

## 2. The Architecture

The deployment spans **two AWS EC2 instances** in the same subnet and availability zone:

- **Web Server** (RedHat) runs Apache + PHP 8.2 + WordPress. Its storage uses LVM across three 10 GB EBS volumes, split into separate logical volumes for application files (`apps-lv`) and system logs (`logs-lv`).
- **DB Server** (RedHat) runs MySQL. Its storage also uses LVM across three EBS volumes, with a single logical volume (`db-lv`) mounted at `/db`.
- The Web Server connects to MySQL over the **private IP** of the DB Server (port 3306). The DB Server's security group allows inbound traffic **only from the Web Server's private IP** (`/32`).
- SELinux is configured to let Apache execute PHP via PHP-FPM and make outbound connections to the database.

This separation means the database is never exposed to the internet, the web layer can be replaced or scaled without touching data, and LVM gives the flexibility to resize storage without rebuilding instances.

---

## 3. Key Decisions

**Why LVM instead of formatting EBS volumes directly**  
Raw EBS volumes are rigid — growing a filesystem means detaching, snapshotting, and recreating. LVM abstracts the physical disks into a volume group, so adding storage becomes a zero-downtime operation. It also made it practical to split 30 GB into two logical volumes (apps vs. logs) with a single pool of physical storage, avoiding the guesswork of pre-allocating disk sizes at launch.

**Why separate Web and DB servers instead of a single instance**  
An all-in-one WordPress server is simpler to set up but creates a single blast radius: a compromised web process gives an attacker direct access to the database. Placing MySQL on a separate instance with a security group locked to one source IP means the database has no public surface. It also lets each tier scale independently — the web server can be swapped for a larger type or replaced in an auto-scaling group without migrating data.

**Why binding MySQL to the private IP instead of `0.0.0.0`**  
Binding to all interfaces (`0.0.0.0`) works but widens the attack surface to every process on the same OS. Pinning MySQL to the private IP ensures the database only listens on the network interface that communicates with the Web Server. Combined with the `/32` security group rule, this creates a defense-in-depth posture: even if the security group were misconfigured, the database process itself would refuse connections from unexpected sources.

---

## 4. How to Deploy It

### Prerequisites

- An **AWS account** with permissions to create EC2 instances, EBS volumes, and security groups.
- A **key pair** (`.pem` file) for SSH access.
- A **RedHat Enterprise Linux 9** AMI (or equivalent).

### Variables to Set

| Variable | Example | Where Used |
|---|---|---|
| Web Server private IP | `172.31.32.64` | DB server's MySQL user GRANT and security group |
| DB Server private IP | `172.31.44.133` | `wp-config.php` `DB_HOST` and MySQL `bind-address` |
| DB password | `PassWord.1` | MySQL user creation and `wp-config.php` |

### Steps

**1. Launch the Web Server**  
Create a RedHat EC2 instance. Attach three 10 GB EBS volumes (all in the same AZ). SSH in and configure LVM:

```bash
# Create partitions and LVM
sudo gdisk /dev/nvme1n1   # Repeat for nvme2n1, nvme3n1
sudo pvcreate /dev/nvme1n1p1 /dev/nvme2n1p1 /dev/nvme3n1p1
sudo vgcreate webdata-vg /dev/nvme1n1p1 /dev/nvme2n1p1 /dev/nvme3n1p1
sudo lvcreate -n apps-lv -L 14G webdata-vg
sudo lvcreate -n logs-lv -L 14G webdata-vg
sudo mkfs.ext4 /dev/webdata-vg/apps-lv
sudo mkfs.ext4 /dev/webdata-vg/logs-lv
```

Mount the logical volumes and persist the mounts:

```bash
sudo mkdir -p /var/www/html /home/recovery/logs
sudo mount /dev/webdata-vg/apps-lv /var/www/html
sudo rsync -av /var/log /home/recovery/logs
sudo mount /dev/webdata-vg/logs-lv /var/log
sudo rsync -av /home/recovery/logs/log/ /var/log
# Update /etc/fstab with UUIDs from sudo blkid
```

**2. Install the Web Stack**  

```bash
sudo dnf install -y wget httpd php-json
sudo dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm
sudo dnf install -y dnf-utils http://rpms.remirepo.net/enterprise/remi-release-9.rpm
sudo dnf module reset php
sudo dnf module enable php:remi-8.2
sudo dnf install -y php php-opcache php-gd php-curl php-mysqlnd
sudo systemctl start php-fpm httpd
sudo systemctl enable php-fpm httpd
```

**3. Configure SELinux**  

```bash
sudo chown -R apache:apache /var/www/html
sudo chcon -t httpd_sys_rw_content_t /var/www/html -R
sudo setsebool -P httpd_execmem 1
sudo setsebool -P httpd_can_network_connect=1
sudo setsebool -P httpd_can_network_connect_db=1
sudo systemctl restart httpd
```

**4. Deploy WordPress**  

```bash
cd && mkdir wordpress && cd wordpress
sudo wget http://wordpress.org/latest.tar.gz
sudo tar xzvf latest.tar.gz
sudo cp -R wordpress/wp-config-sample.php wordpress/wp-config.php
sudo cp -R wordpress/. /var/www/html/
```

**5. Launch the DB Server**  
Create a second RedHat EC2 instance. Repeat the LVM setup, but create and mount `db-lv` to `/db`.

```bash
sudo lvcreate -n db-lv -L 20G database-vg
sudo mkfs.ext4 /dev/database-vg/db-lv
sudo mount /dev/database-vg/db-lv /db
```

**6. Install and Configure MySQL**  

```bash
sudo dnf install -y mysql-server
sudo systemctl start mysqld
sudo systemctl enable mysqld
sudo mysql_secure_installation
```

Create the database and user (use the Web Server's **private IP**):

```sql
CREATE DATABASE wordpress_db;
CREATE USER 'wordpress'@'<WEB-SERVER-PRIVATE-IP>' IDENTIFIED WITH mysql_native_password BY '<YOUR-PASSWORD>';
GRANT ALL PRIVILEGES ON wordpress_db.* TO 'wordpress'@'<WEB-SERVER-PRIVATE-IP>';
FLUSH PRIVILEGES;
```

Set `bind-address` to the DB Server's private IP in `/etc/my.cnf` and restart MySQL:

```ini
[mysqld]
bind-address = <DB-SERVER-PRIVATE-IP>
```

**7. Configure the DB Security Group**  
Add an inbound rule for MySQL/Aurora (port 3306) with source set to the Web Server's private IP (`/32`).

**8. Connect WordPress to the Database**  
On the Web Server, edit `/var/www/html/wp-config.php` and set:

```php
define('DB_NAME', 'wordpress_db');
define('DB_USER', 'wordpress');
define('DB_PASSWORD', '<YOUR-PASSWORD>');
define('DB_HOST', '<DB-SERVER-PRIVATE-IP>');
```

Restart Apache:

```bash
sudo systemctl restart httpd
```

**9. Complete the WordPress Install**  
Browse to the Web Server's public IP and follow the WordPress setup wizard.

---


For a detailed walkthrough with all commands, explanations, and screenshots, see the [main documentation](Docs.md).

