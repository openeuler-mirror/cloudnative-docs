# HTTP APIs

## Overview

The open APIs of Rubik are all HTTP APIs, including the API for setting or updating the pod priority, API for detecting the Rubik availability, and API for querying the Rubik version.

## APIs

### API for Setting or Updating the Pod Priority

Rubik provides the function of setting or updating the pod priority. External systems can call this API to send pod information. Rubik sets the priority based on the received pod information to isolate resources. The API call format is as follows:

```bash
HTTP POST /run/rubik/rubik.sock
{
    "Pods": {
        "podaaa": {
            "CgroupPath": "kubepods/burstable/podaaa",
            "QosLevel": 0
        },
        "podbbb": {
            "CgroupPath": "kubepods/burstable/podbbb",
            "QosLevel": -1
        }
    }
}
```

In the **Pods** settings, specify information about the pods whose priorities need to be set or updated. At least one pod must be specified for each HTTP request, and **CgroupPath** and **QosLevel** must be specified for each pod. The meanings of **CgroupPath** and **QosLevel** are as follows:

| Item    | Value Type| Value Range| Description                                               |
| ---------- | ---------- | ------------ | ------------------------------------------------------- |
| QosLevel   | Integer        | 0, -1       | pod priority. The value **0** indicates that the service is an online service, and the value **-1** indicates that the service is an offline service.       |
| CgroupPath | String     | Relative path    | cgroup subpath of the pod (relative path in the cgroup subsystem)|

The following is an example of calling the API:

```sh
curl -v -H "Accept: application/json" -H "Content-type: application/json" -X POST --data '{"Pods": {"podaaa": {"CgroupPath": "kubepods/burstable/podaaa","QosLevel": 0},"podbbb": {"CgroupPath": "kubepods/burstable/podbbb","QosLevel": -1}}}' --unix-socket /run/rubik/rubik.sock http://localhost/
```

### API for Detecting Availability

As an HTTP service, Rubik provides an API for detecting whether it is running.

API format: HTTP/GET /ping

The following is an example of calling the API:

```sh
curl -XGET --unix-socket /run/rubik/rubik.sock http://localhost/ping
```

If **ok** is returned, the Rubik service is running.

### API for Querying Version Information

Rubik allows you to query the Rubik version number through an HTTP request.

API format: HTTP/GET /version

The following is an example of calling the API:

```sh
curl -XGET --unix-socket /run/rubik/rubik.sock http://localhost/version
{"Version":"0.0.1","Release":"1","Commit":"29910e6","BuildTime":"2021-05-12"}
```
