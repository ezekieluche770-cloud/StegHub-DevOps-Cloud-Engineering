# StegHub-DevOps-Cloud-Engineering

## Client-Server Architecture with MySQL

This project implements a client-server architecture using MySQL on two AWS EC2 instances. It covers provisioning two Ubuntu 26.04 LTS servers (`mysql-server` and `mysql-client`) on t3.micro, configuring security groups for SSH access, and setting up the MySQL DBMS to communicate over a private network.

Key steps include:
- **MySQL Server** — installing and configuring MySQL Server, enabling the service, and binding it to the private IP for remote connections
- **MySQL Client** — installing MySQL Client on a separate instance and connecting to the remote MySQL Server over the network
- **Security Configuration** — configuring the MySQL user for remote access and updating the bind-address and firewall rules
- **Connectivity Testing** — verifying the client-server connection by executing SQL queries from the client instance

The result is a functional client-server database architecture on AWS, demonstrating how a MySQL client can connect to a remote MySQL server and execute queries over the network.

For a complete walkthrough with commands and screenshots, see the [full documentation](Client-Server-Architecture%20with%20Mysql/Docs.md).

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

## LEMP Stack Implementation

This project implements a LEMP stack (Linux, Nginx, MySQL, PHP) on an AWS EC2 instance. It covers provisioning a Ubuntu 26.04 LTS server on t3.micro, configuring security groups for SSH and HTTP access, and installing each component of the stack.

Key steps include:
- **Nginx** — installing and configuring the web server, updating firewall rules, and verifying HTTP access via public IP
- **MySQL** — installing the database server, setting a root password, and running the secure installation script
- **PHP** — installing PHP-FPM along with the MySQL module and configuring Nginx to pass PHP requests
- **Nginx Configuration** — creating a custom Nginx server block configuration for projectLEMP
- **PHP Enablement** — troubleshooting and updating PHP-FPM socket version to resolve a 502 Bad Gateway error, and verifying with a phpinfo script
- **Database Integration** — creating a MySQL database and user, then retrieving data via a PHP script

The result is a fully functional web server environment on AWS, ready to host dynamic PHP-based web applications using Nginx.

For a complete walkthrough with commands and screenshots, see the [full documentation](LEMP-Stack/Docs.md).

## MEAN Stack Implementation

This project implements a MEAN stack (MongoDB, Express.js, Angular, Node.js) on an AWS EC2 instance. It covers provisioning a Ubuntu 26.04 LTS server on t3.micro, configuring security groups for SSH and HTTP access, and building a full-stack Book Register application.

Key steps include:
- **Node.js** — installing Node.js and npm to set up the Express routes and AngularJS controllers
- **MongoDB** — installing and configuring the database, adding the repository, and starting the MongoDB service
- **Express.js & Mongoose** — installing Express and Mongoose, defining routes for CRUD operations, and creating a Book schema with fields for name, ISBN, author, and pages
- **AngularJS** — connecting the frontend to the backend with AngularJS controllers that handle GET, POST, PUT, and DELETE requests
- **Integration Testing** — launching the server, verifying endpoints with curl, and accessing the Book Register application via the browser

The result is a fully functional Book Register application deployed on AWS, demonstrating a complete JavaScript-based full-stack development workflow from database to user interface.

For a complete walkthrough with commands and screenshots, see the [full documentation](MEAN-Stack/Docs.md).

## MERN Stack Implementation

This project implements a MERN stack (MongoDB, Express.js, React, Node.js) on an AWS EC2 instance. It covers provisioning a Ubuntu 26.04 LTS server on t3.micro, configuring security groups for SSH and HTTP access, and building a full-stack To-Do application.

Key steps include:
- **Backend Setup** — installing Node.js and npm, initializing the project, and installing Express.js along with dotenv
- **MongoDB** — creating a cloud database via MongoDB Atlas, configuring database access, and connecting the application using Mongoose
- **RESTful API** — defining routes and models for creating, reading, and deleting To-Do items using Express routers and HTTP methods (GET, POST, DELETE)
- **Frontend Setup** — scaffolding a React app with create-react-app, installing Axios and concurrently, and configuring a proxy for seamless API communication
- **React Components** — building reusable Input, ListTodo, and Todo components to manage the user interface and state
- **Integration Testing** — validating the full stack with Postman and verifying end-to-end functionality in the browser

The result is a fully functional MERN To-Do application deployed on AWS, demonstrating a complete JavaScript-based full-stack development workflow from database to user interface.

For a complete walkthrough with commands and screenshots, see the [full documentation](MERN-Stack/Docs.md).

## Web Solution with WordPress

This project implements a two-tier WordPress deployment on two AWS EC2 instances (RedHat), separating the web layer from the database layer for independent scaling, patching, and security. It covers provisioning instances, configuring LVM storage across multiple EBS volumes, and installing each component of the stack.

Key steps include:
- **LVM Configuration** — creating logical volumes for application files (`apps-lv`) and system logs (`logs-lv`) on the Web Server, and a dedicated database volume (`db-lv`) on the DB Server using LVM across EBS volumes
- **Web Stack** — installing Apache and PHP 8.2 with necessary modules and PHP-FPM on the Web Server
- **Database** — installing MySQL on a separate DB Server with the database stored on LVM-backed storage
- **WordPress** — downloading and deploying WordPress to the web server's document root
- **Security** — configuring SELinux policies for Apache, binding MySQL to the private IP, and locking the DB Server's security group to the Web Server's private IP only
- **Connectivity** — connecting WordPress to the remote MySQL database over the private network

The result is a secure, two-tier CMS platform on AWS where the web and database layers can be managed independently and the database is never exposed to the public internet.

For a complete walkthrough with commands and screenshots, see the [full documentation](Web-Solution-with-Wordpress/Docs.md).

## DevOps Tooling Website Solution

This project implements a scalable, stateless web application architecture on AWS using a shared NFS storage layer and a dedicated MySQL database server. It covers provisioning multiple RedHat Enterprise Linux 8 and Ubuntu EC2 instances, configuring LVM across EBS volumes, and deploying a PHP-based tooling application across three web servers that share code and logs via NFS.

Key steps include:
- **NFS Server** — configuring LVM across three 10 GB EBS volumes, creating logical volumes for apps, logs, and opt, then exporting them via NFS to the web servers
- **Database Server** — installing MySQL on Ubuntu, creating the `tooling` database and `webaccess` user, and binding MySQL to the private subnet
- **Web Servers** — launching three RHEL 8 instances, mounting `/var/www` to the NFS export and `/var/log/httpd` to the logs export, and installing Apache, PHP 8.2, and PHP-FPM
- **Shared Storage** — mounting the same NFS exports on all three web servers so they serve identical content, making the web tier stateless and replaceable
- **Application Deployment** — cloning the tooling repository from GitHub, configuring `functions.php` to connect to the remote MySQL database, and creating an admin user

The result is a stateless, multi-tier web architecture on AWS where any web server can be terminated and replaced without data loss, the database is isolated on a private subnet, and all application files are served from a central NFS share.

For a complete walkthrough with commands and screenshots, see the [full documentation](DevOps%20Tooling%20Website%20Solution/Docs.md).

## Load Balancer Solution With Apache

This project implements an Apache HTTP Server as a load balancer on an Ubuntu EC2 instance to distribute HTTP traffic between two RHEL9 web servers hosting the Tooling website. It covers provisioning a separate Ubuntu 26.04 LTS load balancer instance, configuring Apache's mod_proxy_balancer module, and verifying that requests are evenly distributed across backend servers.

Key steps include:
- **Apache Installation** — installing Apache2 and enabling proxy, proxy_balancer, proxy_http, headers, and lbmethod_bytraffic modules
- **Load Balancer Configuration** — defining a backend server pool with BalancerMember directives and selecting the bytraffic balancing method
- **Traffic Verification** — monitoring access logs on both web servers to confirm even request distribution
- **NFS Unmounting** — detaching shared log mounts to ensure each web server maintains independent logs
- **Local DNS Resolution** — configuring /etc/hosts for simplified backend server management using arbitrary hostnames

The result is a highly available web architecture on AWS where Apache acts as a reverse proxy and load balancer, distributing incoming client requests across multiple backend web servers to improve performance, fault tolerance, and scalability.

For a complete walkthrough with commands and screenshots, see the [full documentation](Load%20Balancer%20Solution%20With%20Apache/Docs.md).

## Load Balancer Solution With Nginx and SSL

This project implements an Nginx load balancer on an Ubuntu EC2 instance to distribute HTTP traffic across multiple backend web servers, and secures the application with an SSL/TLS certificate from Let's Encrypt. It covers provisioning an Nginx load balancer instance, configuring reverse proxy and upstream server blocks, registering a domain name, and enabling encrypted HTTPS communication via Certbot.

Key steps include:
- **Nginx Installation** — installing Nginx on Ubuntu and configuring it as a reverse proxy and load balancer
- **Load Balancer Configuration** — defining an upstream server pool with weighted distribution and proxying requests to the backend web servers
- **Domain Registration** — registering a domain name and associating it with an Elastic IP for a static public endpoint
- **SSL/TLS with Certbot** — installing Certbot via snap, requesting a Let's Encrypt certificate, and configuring automatic HTTPS redirects
- **Certificate Renewal** — setting up a cron job for automatic renewal of the 90-day Let's Encrypt certificate

The result is a highly available and secure web architecture on AWS where Nginx acts as an encrypted reverse proxy, distributing incoming HTTPS traffic across multiple backend servers while protecting data in transit.

For a complete walkthrough with commands and screenshots, see the [full documentation](Load%20Balancer%20Solution%20With%20Nginx%20and%20SSL/Docs.md).

## Tooling Website Deployment Automation with Jenkins CI

This project implements a Continuous Integration (CI) pipeline using Jenkins to automate the deployment of the Tooling Website on AWS. It covers provisioning a dedicated Jenkins server on Ubuntu 26.04 LTS, connecting it to a GitHub repository via webhooks, and automatically deploying application updates to a shared NFS server that serves multiple web servers.

Key steps include:
- **Jenkins Server** — launching an Ubuntu EC2 instance, installing JDK 17 and Jenkins, and performing the initial setup via the web interface
- **GitHub Integration** — configuring GitHub webhooks to trigger Jenkins jobs automatically on every code push to the repository
- **Freestyle Job** — creating a Jenkins Freestyle project that pulls the latest source code from GitHub and archives the build artifacts
- **NFS Deployment** — installing the Publish Over SSH plugin and configuring Jenkins to copy build artifacts to the NFS server's `/mnt/apps` directory
- **Permissions** — setting appropriate ownership and permissions on the NFS target directory to allow Jenkins to write files

The result is an automated CI pipeline where any code push to GitHub triggers Jenkins to build and deploy the updated application to the shared NFS storage, making the latest version immediately available to all connected web servers without manual intervention.

For a complete walkthrough with commands and screenshots, see the [full documentation](Tooling%20Website%20Deployment%20Automation%20with%20Jenkins%20CI/Docs.md).