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