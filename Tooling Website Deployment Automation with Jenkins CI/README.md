## Tooling Website Deployment Automation with Jenkins CI

This project implements a Continuous Integration (CI) pipeline using Jenkins to automate the deployment of the Tooling Website on AWS. It covers provisioning a dedicated Jenkins server on Ubuntu 26.04 LTS, connecting it to a GitHub repository via webhooks, and automatically deploying application updates to a shared NFS server that serves multiple web servers.

Key steps include:
- **Jenkins Server** — launching an Ubuntu EC2 instance, installing JDK 17 and Jenkins, and performing the initial setup via the web interface
- **GitHub Integration** — configuring GitHub webhooks to trigger Jenkins jobs automatically on every code push to the repository
- **Freestyle Job** — creating a Jenkins Freestyle project that pulls the latest source code from GitHub and archives the build artifacts
- **NFS Deployment** — installing the Publish Over SSH plugin and configuring Jenkins to copy build artifacts to the NFS server's `/mnt/apps` directory
- **Permissions** — setting appropriate ownership and permissions on the NFS target directory to allow Jenkins to write files

The result is an automated CI pipeline where any code push to GitHub triggers Jenkins to build and deploy the updated application to the shared NFS storage, making the latest version immediately available to all connected web servers without manual intervention.

For a complete walkthrough with commands and screenshots, see the [full documentation](Docs.md).
