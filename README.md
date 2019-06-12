#### Pythonic implementation of a Distributed Log Tracer especially for microservices

This repo is a _quick implementation_ of log tracer for OpenTracing like logs, more like a Jaegar client

This was created as an excercise during one of my interviews

It uses **Direct Acyclic Graph(DAG)** data structure to trace span and trace ids and has a O(N) complexity for getting traces and O(M*N) for printing them

#### Requirements - Mac OS X

```bash
 # Install python if not already present
 brew install python
 
 # Create a virtual environment 
 python -m venv venv
 
 # Activate it
 source ./venv/bin/activate
 
 # install requirements
 pip install -r requirements.txt
``` 

#### Run by

```bash    
    python tracer.py
```

#### Output

The output will be something like:

```bash
- 2018-10-25T04:13:18+11:00 svc-app1 auth.user.Login()starting login for bc0a0f86-b311-464e-b960-090ae667d5a1


     - 2018-10-25T21:36:32+11:00 svc-app-2 auth.user.AuthCheck()checking auth creds for bc0a0f86-b311-464e-b960-090ae667d5a1


     - 2018-10-26T06:13:44+11:00 svc-app-2 auth.user.AuthCheck()extracted subject from JWT token


     - 2018-10-27T07:13:18+11:00 svc-app-2 auth.user.AuthCheck()verified subject in JWT token


- 2018-10-27T15:46:19+11:00 svc-app1 auth.user.Login()auth check succeeded

```