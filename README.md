# Running your own local CAGECAT instance

Requirements:
- Sufficient rights to use Docker
- More than 16GB of free space
- 2GB of RAM memory

### Installing prerequisites
```
sudo apt-get
sudo apt install docker git nano
```

### Clone this repository
```
git clone https://github.com/MatthiasvdBelt/CAGECAT_instance.git
```

### Customize the ```config.py``` file
The cloned ```config.py``` file is a dummy file, and can not be directly used. All missing parameters should be filled manually.


### Running the instance
1. Clone the CAGECAT repository
2. Move the Dockerfile to the current directory
3. Edit the ```config.py``` file
4. Build the Docker image with your custom tag
   1. This process is able to build on the background (i.e. appending ```&``` to the command)
5. Create a Docker container using the preivously built image and run it in detached mode
```
git clone -b main https://github.com/MatthiasvdBelt/CAGECAT.git
mv CAGECAT/config_files/Dockerfile ./Dockerfile
nano CAGECAT/config.py
docker build -t <cagecat_custom_tag> .
docker run --name <custom_container_name> -d <cagecat_custom_tag>
```

### Connecting to the container
Get the IP address of the Docker container with

```
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' container_name_or_id
```

#### When on same computer as Docker container
In your browser, navigate to
```
<container_ip_address>:88
```
Now, you are be able to use CAGECAT and all it's functionalities.

#### When on a different computer
An SSH tunnel needs to be created between the computer running the Docker container, and the computer you wish to use for using CAGECAT. All interactions with the Docker container will use this SSH tunneling.

Create the SSH tunnel by executing
```
ssh <ip_address_of_computer_running_docker_container> -L 9999:<container_ip_address>:88
```
Next, you are be able to use CAGECAT and all it's functionalities when navigating to <a href="127.0.0.1:9999">127.0.0.1:9999</a> in your browser.

missing the sensitive.py file
