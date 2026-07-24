# Tooling Website Deployment Automation with Jenkins CI

## Introduction

In the previous project, I implemented a highly available Tooling Website infrastructure using two web servers behind an Apache Load Balancer. This architecture improved scalability by distributing incoming traffic across multiple servers, ensuring better performance and availability.

While this setup works well, manually deploying application updates to every web server quickly becomes inefficient as the infrastructure grows. In production environments where applications may run on dozens or even hundreds of servers, manually copying files and updating each server is time-consuming, error-prone, and difficult to maintain.

To address this challenge, this project introduces Jenkins, an open-source automation server widely used to implement Continuous Integration (CI). Jenkins automates repetitive deployment tasks, enabling developers to deliver software changes faster, more consistently, and with fewer manual steps.

Continuous Integration is a software development practice where developers frequently commit code changes to a shared repository. Each change automatically triggers a build and deployment pipeline, allowing updates to be validated and delivered quickly while reducing the risk of integration issues.

In this project, I extended the existing Tooling Website architecture by deploying a dedicated Jenkins server and configuring it to automatically retrieve the latest source code from GitHub whenever changes are made. Jenkins then deploys the updated application to the shared NFS storage, making the latest version immediately available to all connected web servers without requiring manual intervention.

This automation forms the foundation of a modern CI/CD pipeline, improving deployment speed, consistency, and reliability.

## Project Objectives

The objectives of this project are to:

- Enhance the existing Tooling Website architecture by introducing a Jenkins server.
- Install and configure Jenkins as a Continuous Integration (CI) server.
- Connect Jenkins to a GitHub repository containing the Tooling Website source code.
- Configure a Jenkins Freestyle Job to automatically pull the latest code from GitHub.
- Deploy updated application files to the shared NFS server used by all web servers.
- Eliminate manual deployment steps and ensure that code changes are automatically reflected across the web environment.
- Demonstrate the role of Continuous Integration in automating software delivery workflows.

Below is the updated architectural diagram:

![Architectural diagram](img/image1.png)

## Step 1 - Install Jenkins server

1. Create an aws EC2 instance based on Ubuntu Server 26.04 LTS and name it Jenkins

![EC2 instance](img/image2.png)

2. Install JDK since Jenkins is a Java-based application

Access the instance

```
ssh -i "my-ec2-key.pem" ubuntu@ec2-98-83-25-153
```

![SSH access](img/image3.png)

Update the Instance

```
sudo apt-get update
```

![apt-get update](img/image4.png)

Download the Jenkins key

```
sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc \
https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key
```

![Download Jenkins key](img/image5.png)

Add the Jenkins Repository

```
echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" | \
sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
```

![Add Jenkins repo](img/image6.png)

Install Java

Jenkins requires Java to run, yet not all Linux distributions include Java by default. Additionally, not all Java versions are compatible with Jenkins. Install OpenJDK 17

```
sudo apt install fontconfig openjdk-17-jre
```

![Install Java](img/image7.png)

3. Install Jenkins

Update ubuntu

```
sudo apt-get update
```

![apt-get update](img/image8.png)

Install Jenkins

```
sudo apt-get install jenkins -y
```

![Install Jenkins](img/image9.png)

Ensure jenkins is up and running

```
sudo systemctl enable jenkins
sudo systemctl start jenkins
sudo systemctl status Jenkins
```

![Jenkins status](img/image10.png)

4. By default Jenkins server uses TCP port 8080 - open it by creating a new Inbound rule in the EC2 Security Group

![Security group](img/image11.png)

5. Perform initial Jenkins setup

From a browser access `http://<Jenkins-Server-Public-IP-Address>:8080` You will be prompted to provide a default admin password. Retrieve it from the server.

```
http://98.83.25.153:8080
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

![Initial password](img/image12.png)

Then you will be asked which plugins to install - choose suggested plugins

![Suggested plugins](img/image13.png)

![Plugin installation](img/image14.png)

Once plugins installation is done, create an admin user and you will get the jenkins server address.

![Admin user](img/image15.png)

The installation is complete

![Jenkins ready](img/image16.png)

## Step 2 - Configure Jenkins to retrieve source codes from GitHub using Webhooks

In this part, we will be configuring a simple Jenkins job/project. This job will be triggered by GitHub webhooks and will execute a build task to retrieve codes from GitHub and store it locally on Jenkins server.

1. Enable webhooks in your GitHub repository settings.

On your GitHub repository,

Select Settings > Webhooks > Add webhook

![GitHub webhook](img/image17.png)

2. Go to Jenkins web console, click New Item and create a Freestyle project

![Freestyle project](img/image18.png)

To connect our GitHub repository, we will need to provide its URL, we can copy from the repository itself

```
https://github.com/ezekieluche770-cloud/tooling.git
```

![GitHub URL](img/image19.png)

In configuration of our Jenkins freestyle project choose Git repository, provide there the link to our Tooling GitHub repository and credentials (user/password) so Jenkins could access files in the repository.

![Git credentials](img/image20.png)

Save the configuration and try to run the build. For now we can only do it manually. Click Build Now button. After all was configured correctly, the build was successfull and was seen under #1 You can open the build and check in Console Output if it has run successfully.

![Build success](img/image21.png)

But this build does not produce anything and it runs only when we trigger it manually. Let us fix it.

3. Click Configure our job/project and add these two configurations

Configure triggering the job from GitHub webhook and also Configure Post-build Actions to archive all the files - files resulted from a build are called artifacts:

![Trigger config](img/image22.png)

![Post-build actions](img/image23.png)

Now, go ahead and make some change in any file in our GitHub repository (e.g. README.MD file) and push the changes to the main branch.

![Change README](img/image24.png)

we will see that a new build has been launched automatically by webhook and its results - artifacts, saved on Jenkins server.

![Build triggered](img/image25.png)

Now we configured an automated Jenkins job that receives files from GitHub by webhook trigger this method is considered as push because the changes are being pushed and files transfer is initiated by GitHub. There are also other methods: trigger one job (downstreadm) from another (upstream), poll GitHub periodically and others.

By default, the artifacts are stored on Jenkins server locally

```
ls /var/lib/jenkins/jobs/tooling_github/builds/<build_number>/archive/
```

![Artifacts stored](img/image26.png)

## Step 3 - Configure Jenkins to copy files to NFS server via SSH

Now we have our artifacts saved locally on Jenkins server, the next step is to copy them to our NFS server to /mnt/apps directory.

Jenkins is a highly extendable application and there are more than 1400 plugins available. now we will need a plugin that is called Publish Over SSH

1. Install Publish Over SSH plugin.

On main dashboard, Select Manage Jenkins > Manage Plugins > Available > Search for Publish over SSH and Install without restart.

![Publish over SSH plugin](img/image27.png)

![Plugin install](img/image28.png)

2. Configure the job/project to copy artifacts over to NFS server

On main dashboard select Manage Jenkins > Configure System menu item.

Scroll down to Publish over SSH plugin configuration section and configure it to be able to connect to your NFS server:

- Provide a private key (content of .pem file that we use to connect to NFS server via SSH/Putty)
- Arbitrary name
- Hostname - can be private IP address of our NFS server
- Username - ec2-user (since NFS server is based on EC2 with RHEL 9)
- Remote directory - /mnt/apps since our Web Servers use it as a mointing point to retrieve files from the NFS server

![SSH config](img/image29.png)

Test the configuration and make sure the connection returns Success. N.B that TCP port 22 on NFS server must be open to receive SSH connections

![Test connection](img/image30.png)

Save the configuration, open your Jenkins job/project configuration page and add another one Post-build Action (Send build artifact over ssh).

Also, Configure it to send all files produced by the build into our previouslys define remote directory In our case we want to copy all files and directories, so we use ** If you want to apply some particular pattern to define which files to send - use this syntax

![Send build artifacts](img/image31.png)

Save this configuration and go ahead, change something in README.MD file in our GitHub Tooling repository

![Change README again](img/image32.png)

The line created previously in the README.md file have been removed

Webhook will trigger a new job

![New build triggered](img/image33.png)

The error in the build #3 above indicates that we need to set permissions for user ec2-user on the NFS server : Ensure the target directory (/mnt) and it's contents on the NFS server has the correct permissions. We might need to change ownership or modify the permissions to allow the Jenkins user to write to it.

```
sudo chown -R ec2-user:ec2-user /mnt/apps
sudo chmod -R 777 /mnt/apps
```

![Permission error](img/image34.png)

Run the build again from jenkins GUI

Webhook triggers a new job and in the Console Output of the job we get something like this:

```
SSH: Transferred 24 file(s)
Finished: SUCCESS
```

![SSH success](img/image35.png)

To make sure that the files in /mnt/apps have been updated - connect via SSH to our NFS Server and verify README.MD file

```
ls /mnt/apps
```

or

```
ls -l /mnt/apps
```

![ls /mnt/apps](img/image36.png)

```
cat /mnt/apps/README.md
```

![cat README](img/image37.png)

If you see the changes you had previously made in your GitHub - the job works as expected.
