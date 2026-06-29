# Client-Server Architecture side side self study

## 1. Ping and Traceroute Network Diagnostic Utilities

**What is Ping?**

**Ping is a network utility used to test whether a destination device (computer, server, or website) is reachable over a network. It measures the round-trip time (RTT) between your computer and the destination using ICMP (Internet Control Message Protocol) Echo Request and Echo Reply messages.**

**Syntax**

**Windows**

```
ping google.com
```

**Linux/macOS**

```
ping google.com
```

**Sample Output**

```
Pinging google.com [142.250.190.78] with 32 bytes of data:
Reply from 142.250.190.78: bytes=32 time=15ms TTL=117
Reply from 142.250.190.78: bytes=32 time=14ms TTL=117
Reply from 142.250.190.78: bytes=32 time=16ms TTL=117
Reply from 142.250.190.78: bytes=32 time=15ms TTL=117

Ping statistics:
Packets: Sent = 4, Received = 4, Lost = 0 (0% loss)
```

**Understanding the Results**

**Common Uses**

- Test internet connectivity.
- Verify whether a server is online.
- Measure network latency.
- Detect packet loss.

**What is Traceroute?**

**Traceroute (called tracert on Windows) shows the path packets take from your computer to a destination. It lists every router (hop) along the way and the time taken to reach each one. It works by manipulating the packet's TTL (Time To Live) value.**

**Syntax**

**Windows**

```
tracert google.com
```

**Linux/macOS**

```
traceroute google.com
```

**Sample Output**

```
Tracing route to google.com

1   1 ms    1 ms    1 ms   192.168.1.1
2   9 ms   10 ms    8 ms   ISP Router
3  14 ms   13 ms   15 ms   Regional Router
4  19 ms   18 ms   20 ms   Google Server

Trace complete.
```

**Understanding the Results**

**Common Uses**

- Find where network delays occur.
- Troubleshoot routing problems.
- Detect network bottlenecks.
- Identify failed network hops.

**Ping vs Traceroute**

## 2. Basic SQL Commands

SQL (Structured Query Language) is used to create, modify, and query relational databases.

**SHOW**

Displays database information.

Examples (MySQL):

```
SHOW DATABASES;
SHOW TABLES;
SHOW COLUMNS FROM students;
```

Output:

```
students
courses
teachers
```

**CREATE**

Creates a database or table.

**Create a Database**

```
CREATE DATABASE SchoolDB;
```

**Create a Table**

```
CREATE TABLE students (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    age INT
);
```

**INSERT**

Adds new records into a table.

```
INSERT INTO students (id, name, age)
VALUES (1, 'John', 20);
```

Insert multiple rows:

```
INSERT INTO students
VALUES
    (2, 'Mary', 19),
    (3, 'David', 21);
```

**SELECT**

Retrieves data from a table.

**View all records**

```
SELECT * FROM students;
```

Output

**Select specific columns**

```
SELECT name, age
FROM students;
```

**Filter records**

```
SELECT *
FROM students
WHERE age > 19;
```

Output

**DROP**

Deletes a database or table permanently.

Delete a table:

```
DROP TABLE students;
```

Delete a database:

```
DROP DATABASE SchoolDB;
```

**Warning: DROP permanently removes the object and its data.**

## Practice Exercise

Create a database:

```
CREATE DATABASE SchoolDB;
```

Use it:

```
USE SchoolDB;
```

Create a table:

```
CREATE TABLE students (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    age INT
);
```

Insert records:

```
INSERT INTO students
VALUES
    (1,'John',20),
    (2,'Mary',19),
    (3,'David',21);
```

Display all records:

```
SELECT * FROM students;
```

Display only names:

```
SELECT name FROM students;
```

Display students older than 19:

```
SELECT * FROM students
WHERE age > 19;
```

View the table (MySQL):

```
SHOW TABLES;
```

Delete the table:

```
DROP TABLE students;
```

## Quick Revision

### Networking

- Ping → Checks if a host is reachable and measures latency.
- Traceroute/Tracert → Shows the path packets take and identifies where delays or failures occur.

### SQL

- SHOW → Display databases, tables, or columns.
- CREATE → Create databases or tables.
- INSERT → Add records.
- SELECT → Retrieve records.
- DROP → Delete databases or tables permanently.