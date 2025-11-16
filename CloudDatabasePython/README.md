# Overview

The software that I wrote for this project is a simple javascript frontend, python backend, and all connected to a cloud database using firestore. I wanted to create a way to track a little competition that I have been having with some family members and that it was a perfect chance to learn more abotu web databases.

[Software Demo Video](https://youtu.be/wf6DJ44iLoE)

# Cloud Database

I am using firebase/firestore for my web database.

Instead of tables firestore uses collections of documents. So for this project I have the users collection with multiple user documents. Each user document have a variety of fields associated to them for storing information as well as a sub collection that stores the dates I use for various calculations.

# Development Environment

- Flask
- Firebase/Firestore
- Python

I used basic javascript for the frontend and Python was used for all the backend code.

# Useful Websites

- [Web Database Overview](https://www.mongodb.com/resources/basics/databases/cloud-databases)
- [Flask](https://flask.palletsprojects.com/en/stable/)
- [Firebase/Firestore](https://firebase.google.com/docs/firestore)
- [Google Authentication](https://docs.cloud.google.com/docs/authentication/client-libraries)

# Future Work

- Deploy application so that it isn't just hosted locally
- Implement authentication
- Expand the data structure
