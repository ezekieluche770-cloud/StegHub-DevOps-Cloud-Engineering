# Load Balancer Solution With Nginx and SSL/TLS

## Introduction

Modern web applications must be designed to provide high availability, scalability, and secure communication between users and backend services. As application traffic grows, relying on a single web server creates a single point of failure and limits the application's ability to handle increasing user requests. Implementing a load balancer distributes incoming traffic across multiple web servers, improving performance, ensuring fault tolerance, and increasing service availability.

Equally important is protecting data transmitted between clients and web servers. Information exchanged over unencrypted HTTP connections is vulnerable to interception through attacks such as Man-in-the-Middle (MITM), potentially exposing sensitive user data including login credentials, financial information, and personal details. To mitigate these risks, websites use the HTTPS protocol, which encrypts communication using SSL/TLS certificates issued by trusted Certificate Authorities (CAs).

In this project, I deployed Nginx as a reverse proxy and load balancer to distribute client requests across multiple backend web servers. I also registered a domain name, configured DNS records, and secured the application with a trusted Let's Encrypt SSL/TLS certificate using Certbot, enabling encrypted HTTPS communication. This implementation demonstrates how modern cloud infrastructure combines load balancing and transport-layer encryption to deliver highly available, secure, and production-ready web applications.

## Task

This project consist of two parts:

- Configure Nginx as a Load Balancer
- Register a new domain name and configure secure connection

The diagram below shows the architecture of the solution

![Architecture](img/image1.png)

## Part 1 - Configure Nginx As A Load Balancer

### 1. Create an EC2 VM based on Ubuntu Server 26.04 LTS and name it nginx LB

![EC2 VM](img/image2.png)

Open TCP port 80 for HTTP connections and TCP port 443 for secured HTTPS connections

![Security Groups](img/image3.png)

### 2. Update `/etc/hosts` file for local DNS with Web Servers' names (e.g `web1` and `web2`) and their local IP addresses

Access the instance

```
ssh -i "my-ec2-key.pem" ubuntu@ec2.3.91.151.166
```

![SSH Access](img/image4.png)

Update the hosts file

```
sudo vi /etc/hosts
```

![Hosts File](img/image5.png)

![Hosts File Updated](img/image6.png)

### 3. Install and configure Nginx as a load balancer to point traffic to the resolvable DNS names of the webservers

Update the instance

```
sudo apt update && sudo apt upgrade -y
```

![Update Instance](img/image7.png)

Install Nginx

```
sudo apt install nginx
```

![Install Nginx](img/image8.png)

### 4. Configure Nginx LB using the Web Servers' name defined in /etc/hosts

Open the default Nginx configuration file

```
sudo vi /etc/nginx/nginx.conf
```

Insert the following configuration in http section

```
upstream myproject {
    server web1 weight=5;
    server web2 weight=5;
}

server {
    listen 80;
    server_name www.domain.com;
    location / {
        proxy_pass http://myproject;
    }
}

# comment out this line
# include /etc/nginx/sites-enabled/
```

![Nginx Config](img/image9.png)

Test the server configuration

```
sudo nginx -t
```

![Nginx Test](img/image10.png)

Restart Nginx and ensure the service is up and running

```
sudo systemctl restart nginx
sudo systemctl status nginx
```

![Nginx Status](img/image11.png)

## Part 2 - Register a new domain name and configure secured connection using SSL/TLS certificates

In order to get a valid SSL certificate we need to register a new domain name, we can do it using any Domain name registrar - a company that manages reservation of domain names. The most popular ones are: GoDaddy.com, Domain.com, Bluehost.com.

### 1. Assign an Elastic IP to our Nginx LB server

This is necessary in order to have a static IP address that does not change after reboot.

![Elastic IP](img/image12.png)

Associate the elastic IP with Nginx LB

![Associate Elastic IP](img/image13.png)

![Associate Elastic IP 2](img/image14.png)

### 2. Register a new domain name with any registrar of your choice in any domain zone (e.g .com, .net, .org, .edu, info, .xyz or any other) and associate the domain name with the Elastic IP

`my.noip.com` is the domain name registrar used for this project.

![Domain Registration](img/image15.png)

![Domain Registration 2](img/image16.png)

![Domain Registration 3](img/image17.png)

Then verify that it resolves to your Elastic IP.

On your computer, run:

```
nslookup toolingwebsolution.ddns.net
```

![NSLookup](img/image18.png)

### 3. Configure Nginx to recognize your new domain name

Update your `nginx.conf` with `server_name www.<your-domain-name.com>` instead of `server_name www.domain.com`

In our case, the server_name is `toolingwebsolution.ddns.net`

```
sudo vi /etc/nginx/nginx.conf
```

![Nginx Config Domain](img/image19.png)

Restart Nginx

```
sudo systemctl restart nginx
```

![Restart Nginx](img/image20.png)

### 4. Check that the Web Server can be reach from a browser with the new domain name using HTTP protocol

```
http://<your-domain-name.com>
```

![HTTP Browser Access](img/image21.png)

### 5. Install certbot and request for an SSL/TLS certificate

Ensure `snapd` service is active and running

```
sudo systemctl status snapd
```

![Snapd Status](img/image22.png)

Install certbot

```
sudo snap install --classic certbot
```

![Install Certbot](img/image23.png)

Request SSL/TLS Certificate

Create a Symlink in `/usr/bin` for Certbot: Place a symbolic link in this PATH to make it easier to run certbot from the command line without needing to specify its full path.

```
sudo ln -s /snap/bin/certbot /usr/bin/certbot
```

Follow the certbot instructions you will need to choose which domain you want your certificate to be issued for, domain name will be looked up from `nginx.conf` file so ensure you have updated it on step 4.

```
sudo certbot --nginx  # Obtain certificate
```

![Certbot Request](img/image24.png)

Test secured access to your Web Solution by trying to reach `https://<your-domain-name.com>`.

You shall be able to access your website using HTTPS protocol (Uses TCP port 443) and see a padlock image in your browsers' search string.

![HTTPS Access](img/image25.png)

Click on the padlock icon and you can see the detail of the certificate issued for the website.

![Padlock Icon](img/image26.png)

![Certificate Details](img/image27.png)

### 6. Set up periodical renewal of your SSL/TLS certificate

By default, Let's Encrypt certificate is valid for 90 days, so it is recommended to renew it at least every 60 days or more frequently.

Test the renewal command in dry-run mode

```
sudo certbot renew --dry-run
```

![Certbot Renew Dry Run](img/image28.png)

Best practice is to have a scheduled job that runs `renew` command periodically. Configure a cronjob to run the command twice a day

Edit the crontab file

```
crontab -e
```

![Crontab](img/image29.png)

Add the following line to schedule a job that runs renew command twice daily

```
* */12 * * *   root /usr/bin/certbot renew > /dev/null 2>&1
```

![Cron Job Added](img/image30.png)

You can always change the interval of the cronjob if twice a day is too often by adjusting the schedule expression.
