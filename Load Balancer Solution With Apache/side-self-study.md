# Side Self Study: Load Balancing Concepts and Apache mod_proxy_balancer

## Introduction

As web applications grow in popularity, a single server may no longer be able to handle all incoming requests efficiently. To improve performance, availability, and scalability, organizations use load balancing. A load balancer distributes incoming client requests across multiple servers, ensuring that no single server becomes overloaded. This improves application reliability and provides a better user experience.

## Load Balancing Concepts

Load balancing is the process of distributing network or application traffic across multiple servers, often called a server pool. The primary objective is to maximize resource utilization, reduce response time, and ensure high availability.

## Benefits of Load Balancing

- Prevents any one server from becoming overloaded.
- Improves application performance and response times.
- Provides high availability by redirecting traffic if a server fails.
- Allows applications to scale horizontally by adding more servers.
- Improves fault tolerance and reliability.

## Common Load Balancing Algorithms

### 1. Round Robin

The load balancer sends each incoming request to the next server in sequence. This is one of the simplest and most commonly used algorithms when all servers have similar capacity.

### 2. Weighted Round Robin

Each server is assigned a weight based on its processing power. Servers with higher weights receive more requests than those with lower weights.

### 3. Least Connections

Traffic is sent to the server with the fewest active connections. This method is useful when client sessions vary in length.

### 4. Least Response Time

Requests are forwarded to the server responding the fastest. This helps improve overall application performance.

### 5. IP Hash

The client's IP address is hashed to determine which server receives the request. This helps ensure that the same client is consistently directed to the same backend server.

## Difference Between Layer 4 (Network) and Layer 7 (Application) Load Balancing

Load balancers operate at different layers of the OSI model. The two most common are Layer 4 (Network) and Layer 7 (Application).

### Layer 4 (Network) Load Balancer

A Layer 4 load balancer operates at the Transport Layer of the OSI model. It makes routing decisions based on network information such as the source IP address, destination IP address, TCP ports, and UDP ports. It does not inspect the contents of the application data.

#### Characteristics

- Works with TCP and UDP traffic.
- Routes traffic based on IP addresses and port numbers.
- Very fast because it does not inspect HTTP requests.
- Suitable for applications requiring high throughput and low latency.

#### Use Cases

- Database servers
- Gaming servers
- VPN services
- General TCP/UDP applications

### Layer 7 (Application) Load Balancer

A Layer 7 load balancer operates at the Application Layer of the OSI model. It understands application protocols such as HTTP and HTTPS and can inspect request details before deciding where to send traffic.

It can route requests based on:

- URL path
- Hostname
- HTTP headers
- Cookies
- Request method (GET, POST, etc.)

#### Characteristics

- Understands application content.
- Supports content-based routing.
- Can perform SSL/TLS termination.
- Supports authentication and advanced routing policies.

#### Use Cases

- Web applications
- REST APIs
- Microservices
- Multi-domain websites

## Comparison Between L4 and L7 Load Balancers

| Feature | Layer 4 (L4) | Layer 7 (L7) |
|---------|--------------|--------------|
| OSI Layer | Transport Layer | Application Layer |
| Data Inspected | IP addresses, ports | HTTP headers, URLs, cookies |
| Speed | Faster | Slower (more processing) |
| Content-Based Routing | Not supported | Supported |
| SSL Termination | Not supported | Supported |
| Use Cases | TCP/UDP apps, databases | Web apps, APIs, microservices |

## Apache mod_proxy_balancer

### What is mod_proxy_balancer?

mod_proxy_balancer is an Apache HTTP Server module that provides load balancing by distributing requests across multiple backend servers. It works together with modules such as mod_proxy and mod_proxy_http to forward requests from clients to application servers.

This module improves scalability and ensures that applications remain available even if one backend server becomes unavailable.

## Configuration Aspects of Apache mod_proxy_balancer

Several directives are used when configuring Apache's load balancer.

### Balancer Definition

The Balancer section defines a group of backend servers that will receive incoming requests.

Example:

```
<Proxy "balancer://mycluster">
BalancerMember http://192.168.1.10:8080
BalancerMember http://192.168.1.11:8080
</Proxy>
```

This creates a cluster named mycluster with two backend servers.

### BalancerMember

The BalancerMember directive specifies each backend server that belongs to the load-balancing pool.

Additional options can be configured, such as:

- Load balancing weight
- Route identifier
- Maximum connections
- Status (enabled or disabled)

### ProxyPass

The ProxyPass directive tells Apache to forward incoming client requests to the load balancer.

Example:

```
ProxyPass "/" "balancer://mycluster/"
```

### ProxyPassReverse

This directive rewrites response headers so that redirects generated by backend servers point clients back through the Apache proxy instead of directly to the backend server.

Example:

```
ProxyPassReverse "/" "balancer://mycluster/"
```

## Load Balancing Methods

Apache supports several scheduling methods through lbmethod modules, including:

- **byrequests** – distributes requests evenly among servers (default).
- **bytraffic** – distributes traffic based on the amount of data transferred.
- **bybusyness** – sends requests to the least busy server.
- **heartbeat** – works with heartbeat information to route traffic to healthy servers.

Administrators select the method based on application requirements.

## Sticky Sessions

A sticky session, also called session persistence, ensures that all requests from the same user are consistently sent to the same backend server during an active session.

Normally, a load balancer distributes every request independently. If a web application stores session information locally on individual servers, sending subsequent requests to different servers may cause the user to lose their login session or shopping cart.

Sticky sessions solve this problem by keeping a user's requests on the same backend server.

### When Sticky Sessions Are Used

Sticky sessions are useful when:

- Applications store session data locally on each server.
- Users must remain logged in throughout a session.
- Shopping cart information must remain consistent.
- Legacy applications cannot use shared session storage.

For example, if a user logs into an online banking application and their session is stored only on Server A, all subsequent requests should continue to go to Server A until the session ends. Without sticky sessions, the next request might be routed to Server B, which has no record of the user's session, forcing the user to log in again.

Modern cloud-native applications often avoid relying on sticky sessions by storing session data in a shared database or distributed cache such as Redis, allowing any backend server to handle incoming requests.

## Conclusion

Load balancing is an essential technique for improving the performance, scalability, and availability of modern applications. Layer 4 load balancers provide fast routing based on network information, while Layer 7 load balancers make intelligent routing decisions based on application content. Apache's mod_proxy_balancer module enables administrators to build scalable web applications by distributing requests across multiple backend servers using configurable balancing methods. Sticky sessions provide session persistence for applications that store user session data locally, ensuring a consistent user experience.
