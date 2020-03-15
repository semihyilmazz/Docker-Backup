import docker
import os

def create_needed_dirs():

    if not (os.path.exists("/dockerbackup/")):
        os.makedirs('/dockerbackup/')
create_needed_dirs()

#creates directory  if it doesnt exist with a name 'dockerbackup'

def backup_containers():

    client = docker.from_env()
    containers = client.containers.list()
    #connecting Docker

    for container in containers:
        container_name = container.name.lower()
        container_id = container.id
        #looping through in all runnig container objects

        try:
            os.stat('/dockerbackup/{container_name}'.format(container_name=container_name))
            #Checking if dockerbackup/container_name exist if not go to except block
        except:
            os.chdir('C:/dockerbackup/')
            os.system('mkdir {container_name}'.format(container_name=container_name))
            #go in dockerbackup directory and create new directory with a container name

        os.system('docker commit -p {container_id} {name}backup01'.format(container_id=container_id, name=container_name))
        #Saving running Container current state as an image
        print('commiting')
        os.chdir('C:/dockerbackup/{containerName}'.format(containerName=container_name))
        os.system('docker save -o {backUpName}.tar {name}backup01'.format(backUpName=container_name+'Backup',name=container_name))
        #Saving images to a tar archive
        print('saving')


def restore_single():

    containersDict={}
    client = docker.from_env()
    containers = client.containers.list()
    index=1
    for container in containers:
        #going through in all container objects to store them in a dictioanry
        container_name = container.name.lower()
        container_id = container.id
        containersDict[str(index)] ={'containerName': container_name,'containerId':container_id}
        index += 1
        #creating a dictionary to store containerss
        #example dictionary  { 1 : { 'containerName' : name , 'containerId': b547962f85ec } }

    index =1
    for containers in containersDict:
        print(str(index)+'.' + containersDict[containers]['containerName'])
        index +=1
        #priting container names and asking to user  which one he wants to restore

    while True:
        choice = input('which one do you wanna restore ? \n')
        if int(choice) <= index and int(choice) > 0:
            break
        else:
            continue
    #getting user input for storing spesific container

    container_id = containersDict[choice]['containerId']
    client = docker.from_env()
    container = client.containers.get(container_id)
    container_name = container.name
    #collecting container details with docker client

    os.chdir('C:/dockerbackup/{name}'.format(name=container_name))
    os.system('docker load -i {backupName}.tar'.format(backupName=container_name + 'Backup'))
    os.system('docker stop {container_id}'.format(container_id=container_id))
    os.system('docker rm {container_id}'.format(container_id=container_id))
    newContainerName = input('New container Name ?\n' )
    os.system('docker run --name {newContainerName} -it {name}backup01'.format(newContainerName=newContainerName,name=container_name))
    os.system('docker start {newContainerName}'.format(newContainerName=newContainerName))

    #creating directory with container name , loading backup image , stoping running container  and removing it with given id
    #asking for new container name and creating in and starting it

def restore_all():
    client = docker.from_env()
    containers = client.containers.list()
    for container in containers:
        # going through in all container objects
        container_name = container.name
        container_id = container.id

        os.chdir('C:/dockerbackup/{name}'.format(name=container_name))
        os.system('docker load -i {backupName}.tar'.format(backupName=container_name + 'Backup'))
        os.system('docker stop {container_id}'.format(container_id=container_id))
        os.system('docker rm {container_id}'.format(container_id=container_id))
        newContainerName = str(container_name) + 'backup'
        os.system('docker run --name {newContainerName} -it {name}backup01'.format(newContainerName=newContainerName,
                                                                                   name=container_name))
        os.system('docker start {newContainerName}'.format(newContainerName=newContainerName))

        #restoring all containers with backup images,

def restore_multiple():
    containersDict = {}
    client = docker.from_env()
    containers = client.containers.list()

    index = 1
    for container in containers:
        container_name = container.name.lower()
        container_id = container.id
        containersDict[str(index)] = {'containerName': container_name, 'containerId': container_id}
        index += 1

    index = 1
    for containers in containersDict:
        print(str(index) + '.' + containersDict[containers]['containerName'])
        index += 1
    choice = input('which ones do you wanna restore example = 1,3,4? \n')
    choice_list = choice.split(',')

    for container_id in choice_list:

        container_id = containersDict[container_id]['containerId']
        client = docker.from_env()

        container = client.containers.get(container_id)
        container_name = container.name

        os.chdir('C:/dockerbackup/{name}'.format(name=container_name))
        os.system('docker load -i {backupName}.tar'.format(backupName=container_name + 'Backup'))
        os.system('docker stop {container_id}'.format(container_id=container_id))
        os.system('docker rm {container_id}'.format(container_id=container_id))
        newContainerName = input('New container Name ?\n')
        os.system('docker run --name {newContainerName} -it {name}backup01'.format(newContainerName=newContainerName,name=container_name))
        os.system('docker start {newContainerName}'.format(newContainerName=newContainerName))

        # creating directory with container name , loading backup image , stoping running container  and removing it with given id
        # asking for new container name and creating in and starting it


def how_to_restore():

    while True:
        howMany_restore = input('Do you want to restore single container, multiple, all or exit ? 1/2/3/4 \n')
        if howMany_restore == "1":
            restore_single()
            break
        elif howMany_restore == '2':
            restore_multiple()
            break
        elif howMany_restore == '3':
            restore_all()
            break

        elif howMany_restore == '4':
            break

    #asking user what operations he wants to do

if __name__ == '__main__':
    backup_containers()
    how_to_restore()

#docker commit -p [container-id] backup01
# docker save -o backup01.tar backup01
