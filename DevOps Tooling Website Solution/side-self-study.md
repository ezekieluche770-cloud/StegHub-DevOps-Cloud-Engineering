# Side Self Study: Storage Technologies in Cloud Computing

## Network-Attached Storage (NAS)

Network-Attached Storage (NAS) is a file storage device that is connected to a network and allows multiple users or computers to access and share files from a central location. Instead of storing files on individual computers, all files are kept on the NAS device and can be accessed over the network. NAS uses file-level storage, meaning users interact with files and folders just as they would on their personal computers.

NAS is commonly used in homes, schools, and businesses for file sharing, backups, and collaborative work because it is easy to manage and cost-effective.

## Storage Area Network (SAN)

A Storage Area Network (SAN) is a high-speed network that connects servers to storage devices. Unlike NAS, which provides access to files, SAN provides block-level storage, making the storage appear as if it were a local hard drive attached directly to the server. The operating system is responsible for formatting the storage and creating a file system.

SAN is commonly used in enterprise environments where applications such as databases, virtualization platforms, and large business systems require high performance, low latency, and reliable storage.

## Difference Between NAS and SAN

The main difference is that NAS provides file-level storage, while SAN provides block-level storage. NAS is designed for sharing files among multiple users, whereas SAN is designed for high-performance applications that require storage to behave like a local disk. NAS is generally less expensive and easier to deploy, while SAN offers better performance but is more complex and costly.

## Storage Protocols

### Network File System (NFS)

Network File System (NFS) is a file-sharing protocol mainly used in Linux and Unix operating systems. It allows multiple computers to access and share files stored on a remote server as though they were stored locally. In AWS, Amazon Elastic File System (EFS) uses the NFS protocol.

### Server Message Block (SMB)

Server Message Block (SMB) is a file-sharing protocol developed by Microsoft and is commonly used on Windows operating systems. It allows users to share files, folders, and printers across a network while supporting authentication and access permissions.

### FTP and SFTP

File Transfer Protocol (FTP) is used to transfer files between computers over a network. However, FTP does not encrypt data, making it less secure for sensitive information.

Secure File Transfer Protocol (SFTP) is a secure version that runs over the Secure Shell (SSH) protocol. It encrypts both the data and authentication process, making it the preferred option for securely transferring files between systems.

### Internet Small Computer Systems Interface (iSCSI)

Internet Small Computer Systems Interface (iSCSI) is a protocol used to access block storage over an IP network. It enables remote storage devices to appear as locally attached disks to a server. iSCSI is commonly used in SAN environments because it delivers high-performance block storage over standard Ethernet networks.

## Block-Level Storage

Block-level storage stores data in fixed-size blocks. Each block has its own unique address, allowing the operating system to organize the blocks into a file system such as NTFS or ext4. Because applications communicate directly with these storage blocks, block storage offers high performance and low latency.

Cloud service providers use block storage to provide virtual disks for virtual machines. For example, when an Amazon EC2 instance is launched, an Amazon Elastic Block Store (EBS) volume can be attached to it. The EBS volume behaves like a physical hard drive where the operating system, databases, and applications are installed.

## Difference Between Block Storage and Object Storage

Block storage and object storage are designed for different purposes.

Block storage divides data into blocks and presents it as a disk drive to the operating system. It requires a file system before data can be stored and is ideal for operating systems, databases, and applications that require fast performance.

Object storage stores data as individual objects. Each object contains the actual data, metadata, and a unique identifier. Unlike block storage, object storage does not require a traditional file system and is accessed using APIs over the internet. It is highly scalable and is best suited for storing images, videos, documents, backups, and log files.

In summary, block storage focuses on performance and low latency, while object storage focuses on scalability, durability, and cost-effective storage of large amounts of unstructured data.

## Difference Between Block Storage, Object Storage, and Network File System in AWS

Amazon Web Services (AWS) provides examples of these three storage models through different services.

**Amazon Elastic Block Store (EBS)** is AWS's block storage service. It provides persistent storage volumes that can be attached to EC2 instances and are commonly used for operating systems, databases, and enterprise applications that require high performance.

**Amazon Simple Storage Service (S3)** is AWS's object storage service. It stores data as objects and is ideal for backups, media files, archives, static website hosting, and data lakes. S3 is highly durable, scalable, and accessed using web APIs rather than being mounted as a disk.

**Amazon Elastic File System (EFS)** is AWS's network file storage service. It uses the NFS protocol to provide a shared file system that multiple EC2 instances can access simultaneously. EFS automatically scales as storage needs grow and is suitable for shared application data, web servers, and containerized workloads.

## Conclusion

In conclusion, NAS and SAN are two different approaches to network storage. NAS provides file-level storage for sharing files across a network, while SAN provides high-performance block-level storage for enterprise applications. Protocols such as NFS, SMB, FTP, SFTP, and iSCSI enable different methods of accessing and transferring data depending on the operating system and storage requirements. In AWS, Amazon EBS represents block storage, Amazon S3 represents object storage, and Amazon EFS represents network file storage. Choosing the appropriate storage solution depends on the application's performance, scalability, and data-sharing requirements.
