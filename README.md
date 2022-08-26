# Running your own local CAGECAT instance

Requirements:
- Sufficient rights to use Docker
- 15GB of free space


### 1. Clone this repository
```
git clone https://github.com/MatthiasvdBelt/CAGECAT_instance.git
```

### 2. Fill in parameters in the ```CAGECAT_instance/dummies``` folder
**Obligatory:**
1. Add email to config.ini (obligatory by NCBI)


**Optional**

If you wish to add the functionality to send your users email notifications, perform the following steps.

1. Add email configurations in ```sensitive.py```
2. Set ```send_email``` variable to ```True``` in ```config.py```


### 3. Preparing the container
Execute the following steps with the geven commands for your operating system.

1. Name a container and Docker image tag
   1. Use the desired Docker image tag. [Can be inspected here.](https://hub.docker.com/repository/docker/matthiasvdbelt/cagecat_instance/general)
2. Start a new container (if the image is not present locally, it will be fetched from Docker hub) 
3. Move configuration files to the running Docker container
4. Reload the container

#### a. Linux/macOS

```
container_name=<container_name>
tag=<tag>

docker run --name $container_name -d -p 5364:88 matthiasvdbelt/cagecat_instance:$tag

docker cp CAGECAT_instance/dummies/config.py $container_name:/repo/config_files/config.py
docker cp CAGECAT_instance/dummies/sensitive.py $container_name:/repo/config_files/sensitive.py
docker cp CAGECAT_instance/dummies/config.ini $container_name:/root/.config/cblaster/config.ini

docker exec $container_name uwsgi --reload /tmp/uwsgi-master.pid
```


#### b. Windows
```
set container_name=<container_name>
set tag=<tag>

docker run --name %container_name% -d -p 5364:88 matthiasvdbelt/cagecat_instance:%tag%

docker cp CAGECAT_instance\dummies\config.py %container_name%:/repo/config_files/config.py
docker cp CAGECAT_instance\dummies\sensitive.py %container_name%:/repo/config_files/sensitive.py
docker cp CAGECAT_instance\dummies\config.ini %container_name%:/root/.config/cblaster/config.ini

docker exec %container_name% uwsgi --reload /tmp/uwsgi-master.pid
```


### 4. Using CAGECAT

#### a. From your own computer
Navigate to [http://localhost:5364/](http://localhost:5364/) in your browser and use CAGECAT.

#### b. From a different computer
An SSH tunnel needs to be created between the computer running the Docker container, and the computer you wish to use for using CAGECAT. All interactions with the Docker container will use this SSH tunneling.

Get the IP of your running Docker container and create the SSH tunnel 


**Linux/macOS**
```
container_ip=docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $container_name
ssh <ip_address_of_computer_running_docker_container> -L 9999:$container_ip:88
```

**Windows**
```
set container_ip=docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' %container_name%
ssh <ip_address_of_computer_running_docker_container> -L 9999:%container_ip%:88
```

Next, you are able to use CAGECAT and all it's functionalities when navigating to [http://localhost:9999/](http://localhost:9999/) in your browser.
