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

## 

This project implements a MERN stack (MongoDB, Express.js, React, Node.js) on an AWS EC2 instance. It covers provisioning a Ubuntu 26.04 LTS server on t3.micro, configuring security groups for SSH and HTTP access, and building a full-stack To-Do application.

KMERN Stack Implementationey steps include:
- **Backend Setup** — installing Node.js and npm, initializing the project, and installing Express.js along with dotenv
- **MongoDB** — creating a cloud database via MongoDB Atlas, configuring database access, and connecting the application using Mongoose
- **RESTful API** — defining routes and models for creating, reading, and deleting To-Do items using Express routers and HTTP methods (GET, POST, DELETE)
- **Frontend Setup** — scaffolding a React app with create-react-app, installing Axios and concurrently, and configuring a proxy for seamless API communication
- **React Components** — building reusable Input, ListTodo, and Todo components to manage the user interface and state
- **Integration Testing** — validating the full stack with Postman and verifying end-to-end functionality in the browser

The result is a fully functional MERN To-Do application deployed on AWS, demonstrating a complete JavaScript-based full-stack development workflow from database to user interface.

For a complete walkthrough with commands and screenshots, see the [full documentation](MERN-Stack/Docs.md).