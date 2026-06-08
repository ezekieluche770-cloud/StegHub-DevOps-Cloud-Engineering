# StegHub-DevOps-Cloud-Engineering

## LAMP Stack Implementation

This project implements a LAMP stack (Linux, Apache, MySQL, PHP) on an AWS EC2 instance. It covers provisioning a Ubuntu 26.04 LTS server on t3.micro, configuring security groups for SSH and HTTP access, and installing each component of the stack.

Key steps include:
- **Apache** — installing and configuring the web server, updating firewall rules, and verifying HTTP access via public IP
- **MySQL** — installing the database server, setting a root password, and running the secure installation script
- **PHP** — installing PHP along with the MySQL module and Apache integration
- **Virtual Hosts** — creating a custom Apache virtual host configuration for projectlamp
- **PHP Enablement** — modifying Apache's DirectoryIndex to prioritize PHP over HTML, and verifying with a phpinfo script

The result is a fully functional web server environment on AWS, ready to host dynamic PHP-based web applications.

For a complete walkthrough with commands and screenshots, see the [full documentation](LAMP-Stack/Docs.md).