## Pre-Installation Steps

### 1. Verify System Date  

Ensure the Orin device has the correct date by running:
```bash
date
```

### 2. System Update & Cleanup  

Update and clean up your system by running:

```bash
sudo apt-get update 
sudo dpkg --configure -a
sudo apt-get upgrade -y
sudo apt-get autoremove
```

### 3. Install Required Tools (Check if Already Installed)

- **Firefox**:
  - **Check if installed**:
    ```bash
    firefox --version
    ```
  - **Install if not**:
    ```bash
    sudo snap install firefox
    ```

    or use Software Install Center of Ubuntu with graphical interface.

- **Git**:
  - **Check if installed**:
    ```bash
    git --version
    ```
  - **Install if not**:
    ```bash
    sudo apt-get install git
    ```

- **Python**:
  - **Check if installed**:
    ```bash
    python3 --version
    ```
  - **Install if not**:
    ```bash
    sudo apt-get install python3
    ```

- **Pip**:
  - **Check if installed**:
    ```bash
    pip3 --version
    ```
  - **Install if not**:
    ```bash
    sudo apt-get install python3-pip -y
    ```

- **Visual Studio Code**:
  - **Check if installed**:
    ```bash
    code --version
    ```
  - **Install if not**:
    ```bash
    wget -N -O vscode-linux-deb.arm64.deb https://update.code.visualstudio.com/latest/linux-deb-arm64/stable
    sudo apt install ./vscode-linux-deb.arm64.deb
    sudo rm ./vscode-linux-deb.arm64.deb
    ```

- **Jtop** (for Jetson system monitoring):
  - **Check if installed**:
    ```bash
    jtop --version
    ```
  - **Install if not**:
    ```bash
    sudo -H pip3 install -U jetson-stats
    sudo reboot
    ```

- **Docker**:
  - **Check if installed**:
    ```bash
    docker --version
    ```
  - **If installed, ensure user permissions**:
    ```bash
    sudo groupadd docker
    sudo usermod -aG docker $USER
    sudo chmod 666 /var/run/docker.sock
    ```

  - **If not installed:**
    Follow the instructions in [this guide](https://www.jetson-ai-lab.com/tips_ssd-docker.html).

### 4. Install Rye (Python Toolchain Manager)
To install Rye and set it up:
```bash
curl -sSf https://rye.astral.sh/get | bash
source "$HOME/.rye/env"
```

Ensure Python 3.12 is managed by Rye. Use `UV` as the dependency manager.

### 5. Clone Project Repository  
Create a development folder and clone your chatbot project:
```bash
mkdir -p /home/johbaum8/DEV
cd /home/johbaum8/DEV
git clone <repo-url>
```

### 6. Set Up VSCode for Development

- **Recommended Extensions**:
  Add these extensions for a smoother development experience. You can copy the below JSON into your `.vscode/extensions.json`:
  ```json
  {
      "recommendations": [
          "ms-python.python",
          "ms-python.vscode-pylance",
          "esbenp.prettier-vscode",
          "foxundermoon.shell-format",
          "ms-azuretools.vscode-docker",
          "rangav.vscode-thunder-client",
          "mhutchie.git-graph",
          "ms-vscode-remote.remote-containers",
          "ms-python.isort",
          "ms-toolsai.jupyter"
      ]
  }
  ```

- **Install Extensions**:
  Install the recommended VSCode extensions with:
  ```bash
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
  ```

### 7. Set Up Project Environment & Dependencies
Navigate to your project directory and synchronize dependencies:
```bash
cd /home/johbaum8/DEV/build-your-own-chatbot
rye sync
```

### Trouble shooting

Fehlermeldung: bad interpreter `/bin/bash^M`:
```bash
sed -i -e 's/\r$//' install_prerequisites_jetson_nano.sh
```
