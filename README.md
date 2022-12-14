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
1. Add email to ```config.ini``` (obligatory by NCBI)
2. Change the value of the```csrf_key``` variable  in ```sensitive.py``` to a custom, random, unguessable value. CAGECAT will raise an error if you did forgot to change this value.


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
4. **(!)** Manually append (**not in commands below**) the contents of ```/repo/config_files/cron_commands.txt``` to the root crontab file by running ```crontab -e```.   
5. Restart the container

#### a. Linux/macOS

```
container_name=<container_name>
tag=<tag>

docker run --name $container_name -d -p 5364:88 matthiasvdbelt/cagecat_instance:$tag

docker cp CAGECAT_instance/dummies/config.py $container_name:/repo/config_files/config.py
docker cp CAGECAT_instance/dummies/sensitive.py $container_name:/repo/config_files/sensitive.py
docker cp CAGECAT_instance/dummies/config.ini $container_name:/root/.config/cblaster/config.ini

docker restart $container_name
```


#### b. Windows
```
set container_name=<container_name>
set tag=<tag>

docker run --name %container_name% -d -p 5364:88 matthiasvdbelt/cagecat_instance:%tag%

docker cp CAGECAT_instance\dummies\config.py %container_name%:/repo/config_files/config.py
docker cp CAGECAT_instance\dummies\sensitive.py %container_name%:/repo/config_files/sensitive.py
docker cp CAGECAT_instance\dummies\config.ini %container_name%:/root/.config/cblaster/config.ini

docker restart %container_name%
```


### 4. Using CAGECAT
For local CAGECAT instances, no HMM databases are present by default. You are able to create HMM databases by running the script located at
```/repo/hmm_database_creation/create_hmm_databases.py```.
As a result of this script, reference/representative RefSeq genome files of fungi and bacteria are downloaded from NCBI. These genome files are used by the ```cblaster makedb``` module to create HMM databases that can be searched using given HMM profiles.

The script creates a HMM database for every genus that meets the minimum number of genome files. This number of genome files can be adapted within the ```/repo/hmm_database_creation/create_hmm_databases.py``` file (variable: ```min_genomes_number```) 

Currently, HMM databases can only be created for fungi and bacteria (and as a whole). In future releases, we aim to have pre-baked HMM databases and scripts to create HMM databases for specific genera. 

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

### 5. Updating CAGECAT
1. Currently, **no backup** is created from your local database and executed jobs.
Make sure you **copy the contents** of 
```/repo/cagecat/database.db``` and the ```/repo/cagecat/jobs``` 
folder to the host by executing the following commands on the host machine. 
Skipping this step will result in loss of all data of your container. 
In a future release, Docker volumes will be used to preserve your data when updating your CAGECAT instance.

```
docker cp <container_name>:/repo/cagecat/database.db database.db
docker cp <container_name>:/repo/cagecat/jobs jobs

docker cp <container_name>:/repo/config_files/config.py config.py
docker cp <container_name>:/repo/config_files/sensitive.py sensitive.py
docker cp <container_name>:/repo/config_files/config.ini config.ini
```

2. To update CAGECAT to its latest codebase, the latest Docker image should be pulled from Docker hub.
However, when creating a new container, Docker will automatically fetch the specified (specification by tag) image from Docker Hub.
First, execute the following commands to remove the old container.
```
docker stop <container_name>
docker remove <container_name>
```

3. Next, create a new container as described in chapter 3, but rewrite the ```docker cp``` commands as you are not copying 
these files from a ```CAGECAT_instance``` folder, but from your current work directory. Set the tag to the CAGECAT version you are updating to.


4. Last, the ```database.db``` file and ```jobs``` folder back to your new CAGECAT instance and restart the container.
```
docker cp database.db <container_name>:/repo/cagecat/database.db
docker cp jobs <container_name>:/repo/cagecat/jobs

docker restart <container_name>
```
