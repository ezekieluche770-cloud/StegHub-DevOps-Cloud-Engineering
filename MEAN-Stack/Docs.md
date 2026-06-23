# MEAN Web Stack Implementation on AWS

## Introduction

The MEAN stack is a full-stack JavaScript technology stack used to develop modern, dynamic, and scalable web applications. The acronym MEAN represents MongoDB, Express.js, Angular, and Node.js, with each component serving a specific role in the application architecture. Since JavaScript is used throughout the entire stack, developers can build both the frontend and backend using a single programming language.

### MongoDB

MongoDB is a NoSQL database that stores data in flexible, JSON-like documents known as BSON (Binary JSON). Unlike traditional relational databases, it does not require a fixed schema, allowing developers to easily adapt data structures as application requirements evolve. Its scalability, high performance, and ability to handle large volumes of data make it a popular choice for modern web applications.

### Express.js

Express.js is a lightweight and flexible web application framework built on Node.js. It simplifies backend development by providing features such as routing, middleware integration, request handling, and API creation. Express enables developers to build robust server-side applications efficiently while maintaining a clean and organized code structure.

### Angular

Angular is a frontend framework developed and maintained by Google for creating dynamic, single-page web applications. It extends HTML with reusable components, powerful directives, and two-way data binding, making it easier to build interactive and responsive user interfaces. Angular follows a component-based architecture that promotes code reusability, maintainability, and scalability.

### Node.js

Node.js is an open-source JavaScript runtime environment built on Google's V8 JavaScript engine. It allows developers to execute JavaScript code outside the browser, making it possible to build fast and scalable server-side applications. Its event-driven, non-blocking I/O architecture enables efficient handling of multiple simultaneous requests, making it an excellent choice for real-time and high-performance web applications.

## Step 0: Prerequisites

1. EC2 Instance of t3.micro type and Ubuntu 26.04 LTS (HVM) was lunched in the us-east-1 region using the AWS console.

![EC2 Instance](images/image1.png)

2. Attached SSH key named `my-ec2-key` to access the instance on port 22

![SSH Key](images/image2.png)

3. The security group was configured with the following inbound rules:
   - Allow traffic on port 80 (HTTP) with source from anywhere on the internet.
   - Allow traffic on port 443 (HTTPS) with source from anywhere on the internet.
   - Allow traffic on port 22 (SSH) with source from any IP address. This is opened by default.

![Security Group](images/image3.png)

4. The private ssh key permission was changed for the private key file and then used to connect to the instance by running

```
chmod 400 my-ec2-key.pem
ssh -i "my-ec2-key.pem" ubuntu@ec2-34-207-82-254
```

Where `username=ubuntu` and `public ip address=34-207-82-254`

![SSH Connection](images/image4.png)

## Step 1 - Install Nodejs

Node.js is a JavaScript runtime built on Chrome's V8 JavaScript engine. Node.js is used in this tutorial to set up the Express routes and AngularJS controllers.

1. **Update and Upgrade ubuntu**

```
sudo apt update && sudo apt upgrade -y
```

![Update and Upgrade](images/image5.png)

2. **Add certificates**

```
sudo apt -y install curl dirmngr apt-transport-https lsb-release ca-certificates
```

![Add Certificates](images/image6.png)

```
curl -sL https://deb.nodesource.com/setup_22.x | sudo -E bash -
```

![NodeSource Setup](images/image7.png)

3. **Install NodeJS**

```
sudo apt install -y nodejs
```

![Install NodeJS](images/image8.png)

## Step 2 - Install MongoDB

For this application, Book records were added to MongoDB that contain book name, isbn number, author, and number of pages.

1. **Download the MongoDB public GPG key**

```
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor
```

2. **Add the MongoDB repository**

```
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] \
https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | \
sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
```

![MongoDB Repository](images/image9.png)

3. **Update the package database and install MongoDB**

```
sudo apt-get update
```

![apt-get update](images/image10.png)

```
sudo apt-get install -y mongodb-org
```

![Install MongoDB](images/image11.png)

4. **Start and enable MongoDB**

```
sudo systemctl start mongod
sudo systemctl enable mongod
sudo systemctl status mongod
```

![MongoDB Status](images/image12.png)

5. **Install body-parser package**

`body-parser` package is needed to help process JSON files passed in requests to the server.

```
sudo npm install body-parser
```

![Install body-parser](images/image13.png)

6. **Create the project root folder named `Books`**

```
mkdir Books && cd Books
```

Initialize the root folder

```
npm init
```

![npm init](images/image14.png)

Add file named server.js to Books folder

```
vim server.js
```

Copy and paste the web server code below into the server.js file.

```javascript
const express = require('express');
const bodyParser = require('body-parser');
const mongoose = require('mongoose'); // Make sure mongoose is installed and required
const path = require('path'); // To handle static file serving

const app = express();

// Connect to MongoDB
mongoose.connect('mongodb://localhost:27017/test', { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log('MongoDB connected'))
  .catch(err => console.error('MongoDB connection error:', err));

// Middleware
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'public')));

// Routes
require('./apps/routes')(app);

// Start the server
app.set('port', 3300);
app.listen(app.get('port'), () => {
  console.log('Server up: http://localhost:' + app.get('port'));
});
```

![server.js](images/image15.png)

## Step 3 - Install Express and set up routes to the server

Express was used to pass book information to and from our MongoDB database. Mongoose package provides a straightforward schema-based solution to model the application data. Mongoose was used to establish a schema for the database to store data of the book register.

1. **Install express and mongoose**

```
sudo npm install express mongoose
```

![Install express mongoose](images/image16.png)

2. **In Books folder, create a folder named `apps`**

```
mkdir apps && cd apps
```

In apps, create a file named routes.js

```
vim routes.js
```

Copy and paste the code below into routes.js

```javascript
const Book = require('./models/book');
const path = require('path');

module.exports = function(app) {
  // Get all books
  app.get('/book', async (req, res) => {
    try {
      const books = await Book.find({});
      res.json(books);
    } catch (err) {
      console.error(err);
      res.status(500).json({ error: 'Internal Server Error' });
    }
  });

  // Add a new book
  app.post('/book', async (req, res) => {
    try {
      const book = new Book({
        name: req.body.name,
        isbn: req.body.isbn,
        author: req.body.author,
        pages: req.body.pages
      });
      const result = await book.save();
      res.json({
        message: "Successfully added book",
        book: result
      });
    } catch (err) {
      console.error(err);
      res.status(500).json({ error: 'Internal Server Error' });
    }
  });

  // Update a book
  app.put('/book/:isbn', async (req, res) => {
    try {
      const updatedBook = await Book.findOneAndUpdate(
        { isbn: req.params.isbn },
        req.body,
        { new: true }
      );
      if (!updatedBook) {
        return res.status(404).json({ error: 'Book not found' });
      }
      res.json({
        message: "Successfully updated the book",
        book: updatedBook
      });
    } catch (err) {
      console.error(err);
      res.status(500).json({ error: 'Internal Server Error' });
    }
  });

  // Delete a book
  app.delete('/book/:isbn', async (req, res) => {
    try {
      const result = await Book.findOneAndRemove({ isbn: req.params.isbn });
      if (!result) {
        return res.status(404).json({ error: 'Book not found' });
      }
      res.json({
        message: "Successfully deleted the book",
        book: result
      });
    } catch (err) {
      console.error(err);
      res.status(500).json({ error: 'Internal Server Error' });
    }
  });

  // Serve static files
  app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, '../public', 'index.html'));
  });
};
```

![routes.js](images/image17.png)

3. **In the `apps` folder, create a folder named models**

```
mkdir models && cd models
```

In models, create a file named book.js

```
vim book.js
```

![book.js vim](images/image18.png)

Copy and paste the code below into book.js

```javascript
const mongoose = require('mongoose');

const bookSchema = new mongoose.Schema({
  name: { type: String, required: true },
  isbn: { type: String, required: true, unique: true },
  author: { type: String, required: true },
  pages: { type: Number, required: true }
});

module.exports = mongoose.model('Book', bookSchema);
```

![book.js](images/image19.png)

## Step 4 - Access the routes with AngularJS

In this project, AngularJS was used to connect the web page with Express and perform actions on the book register.

1. **Change the directory back to `Books` and create a folder named `public`**

```
cd ../..
```

```
mkdir public && cd public
```

Add a file named script.js into public folder

```
vim script.js
```

Copy and paste the code below (controller configuration defined) into the script.js file.

```javascript
var app = angular.module('myApp', []);

app.controller('myCtrl', function($scope, $http) {
  // Get all books
  function getAllBooks() {
    $http({
      method: 'GET',
      url: '/book'
    }).then(function successCallback(response) {
      $scope.books = response.data;
    }, function errorCallback(response) {
      console.log('Error: ' + response.data);
    });
  }

  // Initial load of books
  getAllBooks();

  // Add a new book
  $scope.add_book = function() {
    var body = {
      name: $scope.Name,
      isbn: $scope.Isbn,
      author: $scope.Author,
      pages: $scope.Pages
    };
    $http({
      method: 'POST',
      url: '/book',
      data: body
    }).then(function successCallback(response) {
      console.log(response.data);
      getAllBooks();  // Refresh the book list
      // Clear the input fields
      $scope.Name = '';
      $scope.Isbn = '';
      $scope.Author = '';
      $scope.Pages = '';
    }, function errorCallback(response) {
      console.log('Error: ' + response.data);
    });
  };

  // Update a book
  $scope.update_book = function(book) {
    var body = {
      name: book.name,
      isbn: book.isbn,
      author: book.author,
      pages: book.pages
    };
    $http({
      method: 'PUT',
      url: '/book/' + book.isbn,
      data: body
    }).then(function successCallback(response) {
      console.log(response.data);
      getAllBooks();  // Refresh the book list
    }, function errorCallback(response) {
      console.log('Error: ' + response.data);
    });
  };

  // Delete a book
  $scope.delete_book = function(isbn) {
    $http({
      method: 'DELETE',
      url: '/book/' + isbn
    }).then(function successCallback(response) {
      console.log(response.data);
      getAllBooks();  // Refresh the book list
    }, function errorCallback(response) {
      console.log('Error: ' + response.data);
    });
  };
});
```

![script.js](images/image20.png)

2. **In `public` folder, create a file named index.html**

```
vim index.html
```

Copy and paste the code below into index.html file

```html
<!DOCTYPE html>
<html ng-app="myApp" ng-controller="myCtrl">
<head>
  <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.6.4/angular.min.js"></script>
  <script src="script.js"></script>
  <style>
    /* Add your custom CSS styles here */
  </style>
</head>
<body>
  <div>
    <table>
      <tr>
        <td>Name:</td>
        <td><input type="text" ng-model="Name"></td>
      </tr>
      <tr>
        <td>Isbn:</td>
        <td><input type="text" ng-model="Isbn"></td>
      </tr>
      <tr>
        <td>Author:</td>
        <td><input type="text" ng-model="Author"></td>
      </tr>
      <tr>
        <td>Pages:</td>
        <td><input type="number" ng-model="Pages"></td>
      </tr>
    </table>
    <button ng-click="add_book()">Add</button>
    <div ng-if="successMessage">{{ successMessage }}</div>
    <div ng-if="errorMessage">{{ errorMessage }}</div>
  </div>
  <hr>
  <div>
    <table>
      <tr>
        <th>Name</th>
        <th>Isbn</th>
        <th>Author</th>
        <th>Page</th>
        <th>Action</th>
      </tr>
      <tr ng-repeat="book in books">
        <td>{{ book.name }}</td>
        <td>{{ book.isbn }}</td>
        <td>{{ book.author }}</td>
        <td>{{ book.pages }}</td>
        <td><button ng-click="del_book(book)">Delete</button></td>
      </tr>
    </table>
  </div>
</body>
</html>
```

![index.html](images/image21.png)

3. **Change the directory back up to `Books` and start the server**

```
cd ..
node server.js
```

![node server.js](images/image22.png)

The server is now up and running, Connection to it is via port 3300. A separate Putty or SSH console to test what curl command returns locally can be launched.

![curl test](images/image23.png)

The Book Register web application can now be accessed from the internet with a browser using the Public IP address or Public DNS name.

![Browser Access](images/image24.png)

## Conclusion

The MEAN stack, consisting of MongoDB, Express.js, Angular, and Node.js, offers a comprehensive and efficient framework for developing modern web applications. Each technology plays a distinct role, working together to deliver a seamless full-stack development experience.

By leveraging JavaScript across both the client and server sides, the MEAN stack simplifies the development process, improves code consistency, and enhances collaboration among development teams. Its scalability, flexibility, and extensive open-source ecosystem make it an excellent choice for building dynamic, high-performance, and maintainable web applications that can adapt to evolving business and user requirements.
