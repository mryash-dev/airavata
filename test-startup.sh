#!/bin/bash

set -e

echo "Starting Apache Airavata Monolithic Server..."
echo "All services included: API Server, Agent Service, Research Service, File Server"

# Wait for dependencies if environment variables are set
if [ ! -z "${DB_HOST}" ]; then
    echo "Waiting for database at ${DB_HOST}:${DB_PORT:-13306}..."
    while ! nc -z ${DB_HOST} ${DB_PORT:-13306}; do
        sleep 2
    done
    echo "Database is ready"
fi

if [ ! -z "${RABBITMQ_HOST}" ]; then
    echo "Waiting for RabbitMQ at ${RABBITMQ_HOST}:${RABBITMQ_PORT:-5672}..."
    while ! nc -z ${RABBITMQ_HOST} ${RABBITMQ_PORT:-5672}; do
        sleep 2
    done
    echo "RabbitMQ is ready"
fi

if [ ! -z "${ZOOKEEPER_HOST}" ]; then
    echo "Waiting for ZooKeeper at ${ZOOKEEPER_HOST}:${ZOOKEEPER_PORT:-2181}..."
    while ! nc -z ${ZOOKEEPER_HOST} ${ZOOKEEPER_PORT:-2181}; do
        sleep 2
    done
    echo "ZooKeeper is ready"
fi

# Function to log with timestamp
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1"
    sleep 1
}

# ================================
# Start the API Server Components
# ================================
log "Starting the API Services..."

cd ${AIRAVATA_HOME}

log "Starting orchestrator..."
./bin/orchestrator.sh -d start api-orch
log "Orchestrator started."

log "Starting controller..."
./bin/controller.sh -d start
log "Controller started."

log "Starting participant..."
./bin/participant.sh -d start
log "Participant started."

log "Starting email monitor..."
./bin/email-monitor.sh -d start
log "Email Monitor started."

log "Starting realtime monitor..."
./bin/realtime-monitor.sh -d start
log "Realtime Monitor started."

log "Starting pre-workflow manager..."
./bin/pre-wm.sh -d start
log "Pre-Workflow Manager started."

log "Starting post-workflow manager..."
./bin/post-wm.sh -d start
log "Post-Workflow Manager started."

# ================================
# Start the Agent Service
# ================================
log "Starting the Agent Service..."
cd ${AIRAVATA_AGENT_HOME}
./bin/agent-service.sh -d start
log "Agent Service started."

# ================================
# Start the Research Service
# ================================
log "Starting the Research Service..."
cd ${AIRAVATA_RESEARCH_HOME}
./bin/research-service.sh -d start
log "Research Service started."

# ================================
# Start the File Service
# ================================
log "Starting the File Service..."
cd ${AIRAVATA_FILE_HOME}
./bin/file-service.sh -d start
log "File Service started."

# ================================
# Start the REST proxy (commented out as restproxy distribution is not available)
# ================================
# log "Starting the REST proxy..."
# cd ${AIRAVATA_REST_HOME}
# ./bin/restproxy.sh -d start
# log "REST proxy started."

# ================================
# Monitor all logs with multitail or fallback
# ================================
log "All Airavata services started successfully!"
log "Starting log monitoring..."

# Create a multitail configuration to monitor all service logs
cd ${AIRAVATA_HOME}

# Wait a moment for logs to be created
sleep 5

# Try to use multitail, but fallback to simple tail if terminal issues occur
if command -v multitail >/dev/null 2>&1; then
    log "Using multitail for log monitoring..."
    # Set TERM to avoid terminal issues
    export TERM=xterm
    multitail \
        -e "API Server" ${AIRAVATA_HOME}/logs/orchestrator.log \
        -e "Controller" ${AIRAVATA_HOME}/logs/controller.log \
        -e "Participant" ${AIRAVATA_HOME}/logs/participant.log \
        -e "Email Monitor" ${AIRAVATA_HOME}/logs/email-monitor.log \
        -e "Realtime Monitor" ${AIRAVATA_HOME}/logs/realtime-monitor.log \
        -e "Pre-WM" ${AIRAVATA_HOME}/logs/pre-wm.log \
        -e "Post-WM" ${AIRAVATA_HOME}/logs/post-wm.log \
        -e "Agent Service" ${AIRAVATA_AGENT_HOME}/logs/agent-service.log \
        -e "Research Service" ${AIRAVATA_RESEARCH_HOME}/logs/research-service.log \
        -e "File Service" ${AIRAVATA_FILE_HOME}/logs/file-service.log 2>/dev/null || {
        log "Multitail failed, using simple tail fallback..."
        tail -f ${AIRAVATA_HOME}/logs/orchestrator.log
    }
else
    log "Multitail not available, using simple tail..."
    tail -f ${AIRAVATA_HOME}/logs/orchestrator.log
fi 