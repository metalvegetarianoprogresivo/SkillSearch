# Skills Searcher

Skills Searcher is an app that enables finding people with a certain profile among Intersys organization. Besides from finding people, the app allowes you to create and groom rosters of candidates to fit certain project requirements. 

## Getting Started

Create virtual environment and activate using:
    
    ./rtualenv_dir/Scripts> activate.bat
Clone repository. 
    using command line:

    git clone https://github.com/IntersysConsulting/SkillSearch
Python3.6+, Java 8+ is required.

    https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html
    https://www.python.org/downloads/
Install PIP for python3:

    sudo apt-get update
    sudo apt install python3-pip
MongoDB Server 4.0 or greater is required using [djongo](https://nesdis.github.io/djongo/get-started/)

Install dependencies required

    pip3 install -r requirements.txt

Install NGINX

    sudo apt-get install nginx

## Deployment

Issue the following command to start the Mongo server before running the Django app:

    mongod

Then issue the following command to create the database and collections for the first time:

    ./manage.py makemigrations
    ./manage.py migrate

Start the server by using:
    
    python3 manage.py runserver

create redirects on nginx url = /etc/nginx/...default4. pip freezerun in 0.0.0.0:port https://github.com/IntersysConsulting/simple-ms-login

## The Project

Our project has 3 main modules:

1. bios. Here is where all the information needed is loaded into the database.
2. search. This is our search engine, extracts information from the database and structures it.
3. roster. Here is where selected elements from the search are stored.

## Additional Notes

### [How to install Java on Ubuntu 18.04 | DigitalOcean](https://linuxize.com/post/install-java-on-ubuntu-18-04/)

In this tutorial, we will walk through installing and managing Java on Ubuntu 18.04. Java is one of the most popular programming languages in the world, used for building different types of cross platform applications.

![Java Linux](https://linuxize.com/post/install-java-on-ubuntu-18-04/featured.jpg)

### [How To Install Nginx on Ubuntu 18.04 [Quickstart] | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-18-04-quickstart)
Nginx is one of the most popular web servers in the world and is responsible for hosting some of the largest and highest-traffic sites on the internet. In this guide, we'll explain how to install Nginx on your Ubuntu 18.04 server.
![Nginx](https://www.digitalocean.com/assets/community/default_community_sharing-65c1cc547375d6e37cc45195b3686769.png)

### [Simple MS Login](https://github.com/IntersysConsulting/simple-ms-login)

Contribute to `IntersysConsulting/simple-ms-login` development by creating an account on GitHub and following the contriution notes.
