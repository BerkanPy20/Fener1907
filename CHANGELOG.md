# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.0] - 2026-03-31

### Changed

- Session 5: Updated the chroma dependency from `0.x.x` to `1.5.5`. Fixed the container health check and the container data path
- Session 5: Dockerfile is now at toplevel to foster a proper uv build the docker compose files use the Dockerfile accordingly
- Session 5 docker compose files now mount the content for the data to `/data`

### Add

- Session 5: Added some instructions to launch the streamlit app without debugging locally.
- Session 5: Update the task. Add a `01_TASK.md` with 3 steps.

## [2.1.0] - 2026-03-20

### Fixed

- Session 4: update `langchain.chains` and `langchain.memory` imports to `langchain_classic` in both task and solution notebooks
- Session 5: replace removed `langchain.schema.ChatMessage` with a plain Python dataclass in `main.py` (task & solution)
- Session 5: remove internal `langchain_core.load.serializable.Serializable` import; use public `Runnable` type annotation in `chatbot.py` (task & solution)
- Session 5: fix `os.environ(...)` call (TypeError at startup) to `os.environ.get(...)` in `chatbot_solution/src/chatbot.py`
- Session 5: replace deprecated `loader.load_and_split()` with `splitter.split_documents(loader.load())` in both `chatbot.py` files
- Session 5: fix structural gaps in chatbot task stub — add missing `COLLECTION_NAME` env var, add missing `logger.info` calls in `_index_data_to_vector_db`, fix broken `astream` stub (wrong indentation, undefined `chunk` variable)

### Changed

- Session 2: sync task notebook with updated LangChain agent API — replace `AgentExecutor` + `create_tool_calling_agent` with `create_agent`, update invoke format, remove deprecated optional memory task
- Session 5: update both READMEs — replace Claude Code launch instructions with VS Code `Run and Debug` panel using the existing `app/.vscode/launch.json` profiles (`LocalPython:Streamlit`, `DockerPython:Streamlit`)
- Consolidate VS Code `launch.json` to repository root (`.vscode/launch.json`)

### Added

- Updated Streamlit to latest compatible version (`pyproject.toml`)
- Tighten all minimum version constraints in `pyproject.toml` to match tested/installed versions — notably `langchain-openai` (0.1.14→1.1.11), `langchain-ollama` (0.1.2→1.0.1), `openai` (1.35.10→2.29.0), `pypdf` (4.3.1→6.9.1), `paramiko` (3.5.1→4.0.0); also normalize `langchain_community` to `langchain-community`
- Pin all dependencies to their current major version (e.g. `>=1.2.12,<2`) to prevent unexpected breaking upgrades

## [2.0.0] - 2025-02-18

### Fixed

- all containers now have specific versions
- ollama container is a custom build due to a open bug in the nvidia container release pipeline

### Change

- change frontend to streamlit
- change embedding models
- architecture change: remove of websockets

### Added

- setup tools


## [1.1.1] - 2024-10-31

- Fix Session 4: fix wrong paramter in huggingface call
- Fix devcontainer: fix no connection to host network
- Update add curl example as bash check in session 1 instructions

## [1.1.0] - 2024-10-20

- Update prerequisites for jetson installation
- Update workshop tasks
- Change LLM to llama3.2
- Update chatbot app
    - embedding model integrated into docker image
    - refine docker compose config


## [1.0.0] - 2024-09-16

- Initial version of workshop content