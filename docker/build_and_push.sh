#!/bin/sh
# Instructor only. Builds the workshop image for both Windows/Intel (amd64) and Apple silicon (arm64) and publishes it.
# Usage:  ./build_and_push.sh ghcr.io/ORG/jc-workshop:1.0 [openrouter-model-id]
# Before: docker login <registry>; make the image PUBLIC on the registry so students can pull it without an account.
# After:  put the image name in environment/.devcontainer/devcontainer.json AND project/.devcontainer/devcontainer.json
#         (both the "image" line and the initializeCommand), and in environment/README.md.
set -e
IMAGE="${1:?Usage: $0 <registry/name:tag> [model]}"
MODEL="${2:-deepseek/deepseek-v4.1-flash}"
cd "$(dirname "$0")"
docker buildx build --platform linux/amd64,linux/arm64 --build-arg CODEX_MODEL="$MODEL" -t "$IMAGE" --push .
echo "Pushed $IMAGE (model $MODEL)"
