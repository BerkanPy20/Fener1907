#!/bin/bash

# Variables for options
REPO_URL=""

DEV_DIR="/home/johbaum8/DEV"



# Function to display help
display_help() {
  echo "Usage: script.sh [-h] [-g git-uri] [-d dev-dir]"
  echo "-h                Display help"
  echo "-g git-uri        Specify a git-uri"
  echo "-d dev-dir        Change default dev dir($DEV_DIR)"
}

# Using getopts to handle short options
while getopts "hg:d" opt; do
  case $opt in
    h)
      display_help
      exit 0
      ;;
    g)
      REPO_URL="$OPTARG"
      ;;
    d)
      DEV_DIR="$OPTARG"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      display_help
      exit 1
      ;;
  esac
done





# Update & cleanup the system
echo "Updating and cleaning up the system..."
sudo apt-get update 
sudo dpkg --configure -a
sudo apt-get upgrade -y
sudo apt-get autoremove -y

# Install required tools if not already installed
install_if_not_installed() {
    if ! command -v $1 &> /dev/null; then
        echo "Installing $2..."
        sudo apt-get install -y $2
    else
        echo "$2 is already installed."
    fi
}

#Checks the given docker demon config if the default runntime is
#nvidia. If this is not the case it updates the config
# usage update_docker_demon_config_if_needed "path/to/config.json"
update_docker_demon_config_if_needed(){

    local FILE="$1"
    
    # Check if the file exists
    if [[ -f "$FILE" ]]; then
        echo "Checking $FILE for default-runtime"
        # Check if the string is already present in the file
        if grep -q '"default-runtime": "nvidia"' "$FILE"; then
            echo "The string is already present in $FILE. No changes made."
        else
            # Read the entire file into the pattern space and replace the last occurrence of }
            sudo sed -i ':a;N;$!ba;
                s/}\s*$/,\
                "default-runtime": "nvidia"\
            }/' "$FILE"
            #sudo sed -i '$ s/}$/,"default-runtime": "nvidia"}/' $FILE

            echo "String appended to $FILE."
        fi
    else
        echo "File $FILE does not exist."
    fi
 }



# Firefox installation
install_if_not_installed firefox firefox

# Git installation
install_if_not_installed git git

# Python installation
install_if_not_installed python3 python3

# Pip installation
install_if_not_installed pip3 python3-pip

# Install VSCode if not installed
if ! command -v code &> /dev/null; then
    echo "Installing Visual Studio Code..."
    wget -N -O vscode-linux-deb.arm64.deb https://update.code.visualstudio.com/latest/linux-deb-arm64/stable
    sudo apt install ./vscode-linux-deb.arm64.deb
else
    echo "Visual Studio Code is already installed."
fi

# Install Jtop for Jetson system monitoring
if ! command -v jtop &> /dev/null; then
    echo "Installing Jtop..."
    sudo -H pip3 install -U jetson-stats
else
    echo "Jtop is already installed."
fi

# Ensure Docker is installed and set up permissions
if [ -x "$(command -v docker)" ]; then
    echo "Docker is already installed."
else
    echo "Download and configure docker ..."
    sudo apt install -y nvidia-container curl
    sudo apt-get install docker-ce docker-ce-cli containerd.io
    curl https://get.docker.com | sh && sudo systemctl --now enable docker
    sudo nvidia-ctk runtime configure --runtime=docker

    echo "Setting up Docker permissions for user..."
    sudo systemctl restart docker
    sudo usermod -aG docker $USER
    #newgrp docker terminates the script
    #sudo groupadd docker
    sudo chmod 666 /var/run/docker.sock

    echo "Backup runtime config to /etc/docker/daemon.json.bak  ..."
    sudo cp /etc/docker/daemon.json /etc/docker/daemon.json.bak
    
    echo "Set up default runtime ..."
    update_docker_demon_config_if_needed "/etc/docker/daemon.json"
    
    echo "Restart Docker ..."
    sudo systemctl daemon-reload && sudo systemctl restart docker
    echo "Docker install done. Final config is:"
    cat /etc/docker/daemon.json
    docker ps
fi

# Install Rye (Python Toolchain Manager)
if ! command -v rye &> /dev/null; then
    echo "Installing Rye..."
    curl -sSf https://rye.astral.sh/get | bash
    echo 'source "$HOME/.rye/env"' >> ~/.bashrc
    source ~/.bashrc
else
    echo "Rye is already installed."
fi

# VSCode recommended extensions setup
echo "Setting up VSCode recommended extensions..."
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension esbenp.prettier-vscode
code --install-extension foxundermoon.shell-format
code --install-extension ms-azuretools.vscode-docker
code --install-extension rangav.vscode-thunder-client
code --install-extension mhutchie.git-graph
code --install-extension ms-vscode-remote.remote-containers
code --install-extension ms-python.isort
code --install-extension ms-toolsai.jupyter

# Clone the project repository

if [ -n "$REPO_URL" ]; then
    echo "Repository specified: $REPO_URL"
    echo "Cloning into        : $DEV_DIR"

    if [ ! -d "$DEV_DIR" ]; then
        echo "Creating development directory..."
        mkdir -p $DEV_DIR
    fi

    cd $DEV_DIR

    #todo make the name nice
    if [ ! -d "$DEV_DIR/build-your-own-chatbot" ]; then
        echo "Cloning the project repository..."
        git clone $REPO_URL build-your-own-chatbot
    else
        echo "Repository already cloned."
    fi

    # Set up project environment and synchronize dependencies
    PROJECT_DIR="$DEV_DIR/build-your-own-chatbot"

    if [ -d "$PROJECT_DIR" ]; then
        echo "Navigating to the project directory..."
        cd $PROJECT_DIR
        echo "Synchronizing dependencies with Rye..."
        rye sync
    else
        echo "Project directory not found. Ensure the repository was cloned correctly."
    fi
else
  echo "No Repo cloned"
fi


# Final reboot
echo "Rebooting system to apply changes..."
sudo reboot