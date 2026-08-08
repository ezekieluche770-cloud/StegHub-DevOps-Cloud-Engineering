# Ansible Configuration Management – Automate Project 7 to 10

## Introduction

This project focuses on using Ansible Configuration Management to automate the configuration and management of multiple Linux servers in an AWS environment. In previous projects, server setup, software installation, and application configuration involved several manual operations. This project introduces Ansible to automate these repetitive tasks using YAML-based playbooks, making server management more consistent, efficient, and scalable.

As part of the project, an Ansible client is configured as a Jump Server (Bastion Host) through which the target servers can be managed. The setup involves configuring SSH connectivity, creating an Ansible inventory to define the managed servers, and developing playbooks that automate software installation and server configuration.

The project also provides practical experience with Ansible inventories, playbooks, SSH authentication, privilege escalation, package management, and automated server configuration, while demonstrating how Infrastructure/Configuration as Code can simplify the management of multiple servers.

## Task

- Install and configure Ansible client to act as a Jump Server/Bastion Host
- Create a simple Ansible playbook to automate servers configuration

On the diagram below the Virtual Private Network (VPC) is divided into two subnets - Public subnet has public IP addresses and Private subnet is only reachable by private IP addresses.

![Architecture](img/image1.png)

## Step 1 - Install and Configure ANSIBLE ON EC2 Instance

1. Update `Name` tag on Jenkins EC2 Instance to `Jenkins-Ansible`. The server will be used to run playbooks.

![Rename EC2 Instance](img/image2.png)

2. In GitHub account create a new repository and name it `ansible-config-mgt`

![Create repository](img/image3.png)

3. Install Ansible (See: install ansible with pip)

```
sudo apt update
```

![apt update](img/image4.png)

```
sudo apt install ansible
```

![apt install ansible](img/image5.png)

Check your ansible version

```
ansible --version
```

![ansible version](img/image6.png)

4. Configure Jenkins build job to save repository content every time you change it – this will solidify your Jenkins configuration skills acquired in Project 9

Configure a Webhook in GitHub and set the webhook to trigger `ansible` build. On `ansible-config-mgt` repository, select Settings > Webhooks > Add webhook

![Webhook](img/image7.png)

Create a new Freestyle project `ansible` in Jenkins

![Freestyle project](img/image8.png)

Point it to the `ansible-config-mgt` repository. Copy the repository URL

![Repository URL](img/image9.png)

In configuration of the `ansible` freestyle project choose `Git`, provide there the link to `ansible-config-mgt` GitHub repository and credentials (user/password) so Jenkins could access files in the repository.

![Git configuration](img/image10.png)

![Git configuration 2](img/image11.png)

Configure a Post-build job to save all (**) files, like in Project 9.

![Post-build archive](img/image12.png)

5. Test the setup by making some change in README.MD file in `master` branch and make sure that builds starts automatically and Jenkins saves the files (build artifacts) in following folder

![Test setup](img/image13.png)

Check `ansible` project on jenkins for the build

![Jenkins build](img/image14.png)

Console output

![Console output](img/image15.png)

```
ls /var/lib/jenkins/jobs/ansible/builds/<build_number>/archive/
```

![Archive](img/image16.png)

Note: Trigger Jenkins project execution only for /main (master) branch.

Now your setup will look like this:

![Setup](img/image17.png)

Tip: Allocate an Elastic IP to Jenkins-Ansible server to avoid reconfigure of GitHub webhook to a new IP address anytime you stop/start the Jenkins-Ansible server.

Allocate elastic IP

![Allocate elastic IP](img/image18.png)

Associate the elastic IP

![Associate elastic IP](img/image19.png)

![Associate elastic IP 2](img/image20.png)

Update the webhook

![Update webhook](img/image21.png)

Note: Elastic IP is free only when it is being allocated to an EC2 Instance, so do not forget to release Elastic IP once the EC2 Instance is terminated.

## Step 2 – Prepare your development environment using Visual Studio Code

1. First part of `DevOps` is `Dev`, which means you will require to write some codes and you shall have proper tools that will make your coding and debugging comfortable – you need an Integrated development environment (IDE) or Source-code Editor.

There is a plethora of different IDEs and Source-code Editors for different languages with their own advantages and drawbacks, you can choose whichever you are comfortable with, but we recommend one free and universal editor that will fully satisfy your needs – `Visual Studio Code (VSC)`.

2. After you have successfully installed `VSC`, configure it to connect to your newly created GitHub repository.

![VSC connect](img/image22.png)

```
https://github.com/ezekieluche770-cloud/ansible-config-mgt.git
```

3. Clone down the ansible-config-mgt repo to the Jenkins-Ansible instance

```
git clone <ansible-config-mgt repo link>
```

![Clone repo](img/image23.png)

## Step 3 - Begin Ansible Development

1. In the ansible-config-mgt GitHub repository, create a new branch that will be used for development of a new feature

Tip: Give the branches descriptive and comprehensive names, for example, if you use Jira or Trello as a project management tool - include ticket number (e.g. PRJ-num) in the name of the branch and add a topic and a brief description what this branch is about - a bugfix, hotfix, feature, release (e.g. feature/prj-145-lvm)

```
git checkout -b feature/prj-11-ansible-config
```

![Create branch](img/image24.png)

2. Checkout the newly created feature branch to the local machine and start building the code and directory structure

```
git fetch
git checkout feature/prj-11-ansible-config
```

3. Create a directory and name it `playbooks` - it will be used to store all the playbook files.

```
mkdir playbooks
```

4. Create a directory and name it `inventory` - it will be used to keep the hosts organised

```
mkdir inventory
```

![Directories](img/image25.png)

5. Within the playbooks folder, create your first playbook, and name it `common.yml`

```
touch playbooks/common.yml
```

6. Within the inventory folder, create an inventory file (.yml) for each environment (Development, Staging, Testing and Production) dev, staging, uat, and prod respectively.

```
touch inventory/dev.yml inventory/staging.yml inventory/uat.yml inventory/prod.yml
```

These inventory files use .ini languages style to configure Ansible hosts.

![Playbook file](img/image26.png)

![Inventory files](img/image27.png)

## Step 4 - Set up an Ansible Inventory

An Ansible inventory file defines the hosts and groups of hosts upon which commands, modules, and tasks in a playbook operate. Since our intention is to execute Linux commands on remote hosts, and ensure that it is the intended configuration on a particular server that occurs. It is important to have a way to organize our hosts in such an Inventory

Save the below inventory structure in the `inventory/dev` file to start configuring your development servers. Ensure to replace the IP addresses according to your own setup.

Note: Ansible uses TCP port 22 by default, which means it needs to ssh into target servers from Jenkins-Ansible host - for this you can implement the concept of `ssh-agent`. Now you need to import your key into `ssh-agent`:

To learn how to setup SSH agent and connect VS Code to your Jenkins-Ansible instance, please see this video:

- For Windows users - `ssh-agent on windows`
- For Linux users - `ssh-agent on linux`

Start the SSH Agent:

This starts the `SSH agent` in your current terminal session and sets the necessary environment variables.

```
eval `ssh-agent -s`
```

Add Your SSH Key:

Add your `SSH private key` to the agent. replace the path with the correct path to the private key.

```
ssh-add <path-to-private-key>
```

![ssh-add](img/image28.png)

Verify the Key is Loaded:

Check that your key has been successfully added to the SSH agent. you should see the name of your key

```
ssh-add -l
```

![ssh-add -l](img/image29.png)

Now, ssh into your Jenkins-Ansible server using ssh-agent

```
ssh -A ubuntu@public-ip
```

![ssh -A](img/image30.png)

![ssh -A 2](img/image31.png)

To learn how to setup SSH agent and connect VS Code to your Jenkins-Ansible instance, See this video: `Windows` `Linux`

Also notice, that your Load Balancer user is `ubuntu` and user for RHEL-based servers is `ec2-user`

Update your `inventory/dev.yml` file with this snippet of code:

```yaml
all:
  children:
    nfs:
      hosts:
        <NFS-Server-Private-IP-Address>:
          ansible_ssh_user: ec2-user
    webservers:
      hosts:
        <Web-Server1-Private-IP-Address>:
          ansible_ssh_user: ec2-user
        <Web-Server2-Private-IP-Address>:
          ansible_ssh_user: ec2-user
    db:
      hosts:
        <Database-Private-IP-Address>:
          ansible_ssh_user: ubuntu
    lb:
      hosts:
        <Load-Balancer-Private-IP-Address>:
          ansible_ssh_user: ubuntu
```

![Inventory dev](img/image32.png)

## Step 5 - Create a Common Playbook

It is time to start giving Ansible the instructions on what you need to be performed on all servers listed in `inventory/dev`

In `common.yml` playbook you will write configuration for repeatable, re-usable, and multi-machine tasks that is common to systems within the infrastructure.

Update your `playbooks/common.yml` file with following code

```yaml
---
- name: Update web and NFS servers
  hosts: webservers, nfs
  remote_user: ec2-user
  become: true
  become_user: root
  tasks:
    - name: Ensure wireshark is at the latest version
      yum:
        name: wireshark
        state: latest
- name: Update LB and DB servers
  hosts: lb, db
  remote_user: ubuntu
  become: true
  become_user: root
  tasks:
    - name: Update apt repo
      apt:
        update_cache: yes
    - name: Ensure wireshark is at the latest version
      apt:
        name: wireshark
        state: latest
```

![Common playbook](img/image33.png)

Examine the code above and try to make sense out of it. This playbook is divided into two parts, each of them is intended to perform the same task:

install `wireshark` utility (or make sure it is updated to the latest version) on your RHEL 9 and Ubuntu servers. It uses root user to perform this task and respective package manager: `yum` for RHEL 9 and `apt` for Ubuntu.

Feel free to update this playbook with following tasks:

- Create a directory and a file inside it
- Change timezone on all servers
- Run some shell script

## Step 6 - Update GIT with the latest code

Now all of your directories and files live on your machine and you need to push changes made locally to GitHub.

In the real world, you will be working within a team of other DevOps engineers and developers. It is important to learn how to collaborate with help of GIT. In many organisations there is a development rule that do not allow to deploy any code before it has been reviewed by an extra pair of eyes - it is also called Four eyes principle. Now you have a separate branch, you will need to know how to raise a `Pull Request (PR)`, get your branch peer reviewed and merged to the `main` branch.

Commit your code into GitHub:

Use git commands to add, commit and push your branch to GitHub.

```
git status
git add <selected files>
git commit -m "commit message"
git push origin <the feature branch>
```

![Git push](img/image34.png)

Create a Pull Request (PR)

![Pull Request](img/image35.png)

Wear the hat of another developer for a second, and act as a reviewer.

![Reviewer](img/image36.png)

If the reviewer is happy with the new feature development, merge the code to the main branch.

![Merge PR](img/image37.png)

![Merge PR 2](img/image38.png)

Head back on your terminal, checkout from the feature branch into the master, and pull down the latest changes

![Checkout master](img/image39.png)

Once your code changes appear in main branch - Jenkins will do its job and save all the files (build artifacts) to

![Build artifacts](img/image40.png)

Console Output

![Console output](img/image41.png)

Check the artifact directory

```
/var/lib/jenkins/jobs/ansible/builds/<build_number>/archive/
```

![Artifact directory](img/image42.png)

## Step 7 - Run first Ansible test

Now, it is time to execute ansible-playbook command and verify if your playbook actually works: first setup our vs code to connect our instance for remote development, follow these steps:

Install Remote Development and Remote - SSH Extension

Configure the SSH Host

![Configure SSH Host](img/image43.png)

Another VSCODE opens showing the access mode and the name of the remote server (SSH: jenkins-ansible) at the top and at the bottom left conner. This indicates that we are now in the remote server

![Remote server](img/image44.png)

Run ansible-playbook command:

```
ansible-playbook -i inventory/dev.yml playbooks/common.yml
```

![Run playbook](img/image45.png)

You can go to each of the servers and check if wireshark has been installed by running

```
which wireshark
```

or

```
wireshark --version
```

Web Servers

![Web Servers](img/image46.png)

Check NFS Server

![NFS Server](img/image47.png)

Check Database Server

![Database Server](img/image48.png)

Check Load Balancer Server

![Load Balancer Server](img/image49.png)

The updated architecture with Ansible now looks like this:

![Updated architecture](img/image50.png)

## Conclusion

The Ansible Configuration Management project successfully automated the configuration and management of the web, NFS, database, and load balancer servers from a centralized Ansible client. The project implemented inventory files to organize the servers and Ansible playbooks to perform tasks such as updating system repositories and ensuring required packages were installed and maintained across the target servers. SSH was configured to provide secure communication between the Ansible client and the managed nodes, while the Jump Server approach provided a centralized point for managing access to the infrastructure. The successful execution of the playbooks demonstrated that the server configurations could be applied consistently without manually connecting to and configuring each server individually. Overall, the project achieved its objective of replacing repetitive manual server administration with a structured and repeatable configuration management process.
