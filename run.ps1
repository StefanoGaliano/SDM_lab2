#Requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$CONTAINER_NAME = "graphdb"
$IMAGE          = "ontotext/graphdb:10.7.6"
$PORT           = 7200

# ── Prerequisites check ───────────────────────────────────────────────────────
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Error "Docker is not installed. Install it from https://docs.docker.com/get-docker/"
    exit 1
}

docker info 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Error "Docker daemon is not running. Please start Docker Desktop and retry."
    exit 1
}

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python is not installed or not in PATH."
    exit 1
}

# ── Start GraphDB in Docker if not already running ────────────────────────────
$running = docker ps --format '{{.Names}}' | Where-Object { $_ -eq $CONTAINER_NAME }
$stopped = docker ps -a --format '{{.Names}}' | Where-Object { $_ -eq $CONTAINER_NAME }

if ($running) {
    Write-Host "GraphDB container already running."
} elseif ($stopped) {
    Write-Host "Restarting stopped GraphDB container..."
    docker start $CONTAINER_NAME
} else {
    Write-Host "Pulling and starting GraphDB container (first run may take a few minutes)..."
    docker run -d `
        --name $CONTAINER_NAME `
        -p "${PORT}:${PORT}" `
        -e "GDB_JAVA_OPTS=-Xmx2000m -Xms1000m -Dgraphdb.workbench.maxUploadSize=40000000000" `
        $IMAGE
}

# ── Build graph and upload ────────────────────────────────────────────────────
Write-Host "Installing Python dependencies..."
pip install -q rdflib requests

Set-Location $PSScriptRoot
python build_kg.py
