#!/usr/bin/env bash
set -e

# ── Prerequisites check ───────────────────────────────────────────────────────
if ! command -v docker &>/dev/null; then
    echo "Error: Docker is not installed. Install it from https://docs.docker.com/get-docker/"
    exit 1
fi
if ! docker info &>/dev/null; then
    echo "Error: Docker daemon is not running. Please start Docker and retry."
    exit 1
fi
if ! command -v python3 &>/dev/null; then
    echo "Error: python3 is not installed."
    exit 1
fi

CONTAINER_NAME="graphdb"
IMAGE="ontotext/graphdb:10.7.6"
PORT=7200

# ── Start GraphDB in Docker if not already running ───────────────────────────
if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "GraphDB container already running."
elif docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "Restarting stopped GraphDB container..."
    docker start "$CONTAINER_NAME"
else
    echo "Pulling and starting GraphDB container (first run may take a few minutes)..."
    docker run -d \
        --name "$CONTAINER_NAME" \
        -p ${PORT}:${PORT} \
        -e GDB_JAVA_OPTS="-Xmx2000m -Xms1000m -Dgraphdb.workbench.maxUploadSize=40000000000" \
        "$IMAGE"
fi

# ── Build graph and upload ────────────────────────────────────────────────────
pip install -q rdflib requests
cd "$(dirname "$0")"
python3 build_kg.py
