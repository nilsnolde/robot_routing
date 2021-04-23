## Status

I fully implemented everything. However, I could only verify the 1st example as correct. For some reason the other examples were either producing sub-optimal paths or were iterating forever and had to be stopped.

Unfortunately I didn't have the time for the necessary investigation yet (writing this at 3 am).

## Build, install and verify

I didn't try on any other Python version than my local one, so first install Python 3.9 to the container:

```shell script
# from inside the repo directory
docker run -dt --name ubuntu-16.04 --entrypoint=/bin/bash -v $(pwd):/robot_routing ubuntu:16.04
docker exec -it ubuntu-16.04 bash

# in container
apt-get update && apt-get install -y software-properties-common
add-apt-repository ppa:deadsnakes/ppa && apt-get update
apt-get install -y python3.9

# test the solution
cd /robot_routing
./robot_router.py exercise_description/problem1/problem.txt exercise_description/problem1/solution.txt
```
