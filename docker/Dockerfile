# Workshop sandbox image: Python + MiniGrid + pytest + Codex (the coding agent) in an isolated Linux container.
# Used by VS Code Dev Containers by BOTH packages: environment/.devcontainer/devcontainer.json (pre-workshop test)
# and project/.devcontainer/devcontainer.json (workshop day). Build and publish with environment/docker/build_and_push.sh.

# Stage 1: get Node + Codex CLI (students use the CLI in the VS Code terminal: they type `codex`).
FROM node:22-slim AS codex
ARG CODEX_VERSION=0.172.0
RUN npm install -g --prefix /opt/codex @openai/codex@${CODEX_VERSION}

# Stage 2: the workshop image.
FROM python:3.12-slim
# Model the agent uses (an OpenRouter model id). Change here + rebuild, or edit ~/.codex/config.toml in a test.
ARG CODEX_MODEL=deepseek/deepseek-v4.1-flash

# PYTHONDONTWRITEBYTECODE and the pytest options below let tests run inside Codex's READ-ONLY sandbox
# (nothing may be written there without the student's approval).
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTEST_ADDOPTS="-s -p no:cacheprovider" \
    PIP_NO_CACHE_DIR=1 \
    SDL_VIDEODRIVER=dummy \
    PYGAME_HIDE_SUPPORT_PROMPT=1

# git, certificates (needed for HTTPS), curl/procps (needed by the VS Code server)
RUN apt-get update \
 && apt-get install -y --no-install-recommends git ca-certificates curl procps \
 && rm -rf /var/lib/apt/lists/*

COPY --from=codex /usr/local/bin/node /usr/local/bin/node
COPY --from=codex /opt/codex /opt/codex
RUN ln -s /opt/codex/bin/codex /usr/local/bin/codex

# Pin versions after the spike confirms they work (see SPIKE.md).
RUN pip install "minigrid>=3,<4" pillow pytest

# Non-root user. Only the project folder (mounted from the student's laptop) is meant to be written.
RUN useradd -m -u 1000 -s /bin/bash student
USER student
ENV HOME=/home/student
RUN git config --global user.name "Student" \
 && git config --global user.email "student@workshop.local" \
 && git config --global --add safe.directory '*' \
 && git config --global init.defaultBranch main \
 && mkdir -p /home/student/.codex
# Codex's own READ-ONLY sandbox + approval_policy "on-request": the agent can read and run commands that do not write,
# but must ask the student (an approval request) before changing any file. This needs user namespaces inside the
# container, which Docker's default seccomp profile blocks; devcontainer.json relaxes it (seccomp=unconfined).
# (With "danger-full-access" Codex never asks: tested.)
RUN printf '%s\n' \
  "model = \"${CODEX_MODEL}\"" \
  'model_provider = "openrouter"' \
  'sandbox_mode = "read-only"' \
  'approval_policy = "on-request"' \
  '' \
  '[model_providers.openrouter]' \
  'name = "OpenRouter"' \
  'base_url = "https://openrouter.ai/api/v1"' \
  'env_key = "OPENROUTER_API_KEY"' \
  'wire_api = "responses"' \
  > /home/student/.codex/config.toml
CMD ["bash"]
