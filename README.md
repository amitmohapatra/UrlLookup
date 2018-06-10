# UrlLookup

This project uses the following technologies:

  * [Flask](http://flask.pocoo.org/), Python based web framework
  * [uWSGI](http://uwsgi-docs.readthedocs.org/), web application deployment solution
  * [nginx](http://nginx.org/), reverse proxy server, Capable of proxying HTTP requests to uWSGI, can be used as load balancer
  * [HAProxy](http://www.haproxy.org/), load balancer
  * [Docker](https://www.docker.com/), applications in containers

Install Docker:
  * https://www.docker.com/community-edition#/download

Git Clone project:
  * git clone git@github.com:amitmohapatra/UrlLookup.git
  * or download the zip from https://github.com/amitmohapatra/UrlLookup and extract
  * then go inside UrlLookup directory

Build and run the application:

    [sudo] docker-compose build
    [sudo] docker-compose up

Get check:
  * In browser put "http://localhost:8080/urlinfo/1/127.0.0.1:8080/test?test=true"
  * you will get a response like : {"assessment":"very poor","category":"negetive","content":"malware","status":"found"}
  * status make sure this url is exist in db.
  * also we can consider some caching.

Thought to the following:

  The size of the URL list could grow infinitely:
     * hashing whould help. currently i am using. 
     * hash collision possible after 100 billion entry.
     * if we need security and more entry the we can go for SHA-256 or SHA-512
     * also both hash value of url and url string are unique so it make sure single entry at any given poit.

  The number of requests may exceed the capacity of this system:
     * load balancer has been used
     * HAPROXY and NGINX are both capable of load balansing in servers.
     * if we want datacenter basis load balance the we can use f5 or netscalar.
     * we can use newrelic to monitor the server.

  What are some strategies you might use to update the service with new URLs?

     * messaging queues.
     * make sure when queue producer enter the data into db both hash value and url both are unique. which currently i made in this project.
     * load balancer also help to distribute the load.

