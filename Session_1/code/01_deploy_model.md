# Deploying a Large Language Model (LLM) on Jetson Orin Nano with Ollama

> ``📝`` If your are not using a Nvidia Jetson, just follow the Instructions [here](https://ollama.com/blog/ollama-is-now-available-as-an-official-docker-image) 
> 
> **For CPUs** just run the following command:
> ```bash
> docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
> ```
>
> **For GPUs** install the Nvidia Container Toolkit ([Instructions](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)) and run the following command:
> ```bash
> docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
> ```

## Overview

This guide provides a streamlined approach to deploying and running a Large Language Model (LLM) on the Jetson Orin Nano using Ollama, a powerful framework for running LLMs locally. You will learn how to set up the environment, deploy a pre-built Docker container, and interact with the model inside the container.

For more detailed documentation, visit the official guide here: [Jetson AI Lab Ollama Tutorial](https://www.jetson-ai-lab.com/tutorial_ollama.html).

---

## Deployment Using a Pre-Built Container

You can pull a pre-built Ollama container from Docker Hub: [makoit13/ollama](https://hub.docker.com/r/makoit13/ollama).

Pre-built images are available for different Jetpack versions:

- **Jetpack 6 with Cuda 12.6**: `makoit13/ollama:r36.4.0`

### Steps

1. **Pull the Docker image**:

   ```bash
   docker pull makoit13/ollama:r36.4.0
   ```

2. **Run the container**:

   Execute following command in the shell path: `~/build-your-own-chatbot`:

   ```bash
   docker run -d \
      --runtime nvidia \
      -it \
      -v "$(pwd)/container_cache/ollama/models:/data/models/ollama/models" \
      -p 11434:11434 \
      --name ollama makoit13/ollama:r36.4.0
   ```

3. **Download model and run in container**:

   To manually download and run a model like Llama 3.2 inside the Ollama container, use the following command outside the container:

   ```bash
   docker exec -it ollama ollama run llama3.2:1b
   ```

   After executing this command you have attached the container shell which means you are inside of the container.

### Optional: Start container and run model

   ```bash
   docker run -d \
      --runtime nvidia \
      -it \
      -v "$(pwd)/container_cache/ollama/models:/data/models/ollama/models" \
      -p 11434:11434 \
      --name ollama makoit13/ollama:r36.4.0 \
      bash -c "ollama serve & sleep 5; ollama run llama3.2:1b"
   ```

---

### Access the Container Shell

To troubleshoot or manage the container manually, access its shell using:

```bash
docker exec -it ollama sh
```

This opens an interactive shell within the running Ollama container.

---

### Interact with Ollama in the Container Shell

Once inside the container, you can interact with Ollama via its CLI. Here are some basic commands:

#### General Command Format

```bash
ollama [command] [flags]
```

#### Available Commands

- **serve**: Start Ollama's service.
- **create**: Create a model from a Modelfile.
- **show**: Display model information.
- **run**: Execute a model.
- **pull**: Download a model from a registry.
- **push**: Upload a model to a registry.
- **list**: List all available models.
- **ps**: List currently running models.
- **cp**: Copy a model.
- **rm**: Remove a model.
- **help**: Get help for any command.

#### Example Commands

1. **Run a Model**:

   ```bash
   ollama run llama3.2:1b
   ```

2. **List Available Models**:

   ```bash
   ollama list
   ```

3. **Pull a Model from a Registry**:

   ```bash
   ollama pull llama3.2:1b
   ```

---

## Final Check

Execute the following command in a bash while the ollama container is running.

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2:1b",
  "prompt": "Why is the sky blue?"
}'
```
