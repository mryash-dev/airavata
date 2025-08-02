# 🚀 Apache Airavata - User Guide

## Quick Start

### 1. Copy the example properties file
```bash
cp vault/airavata-server.properties airavata-server.properties
```

### 2. Edit the properties file (optional)
```bash
# Modify your configuration
nano airavata-server.properties
# or
vim airavata-server.properties
```

### 3. Start the services
```bash
docker-compose up -d
```

### 4. View all logs
```bash
docker logs airavata-monolithic
```

## Properties File Mounting

The container expects your properties file at:
- **Host path:** `./airavata-server.properties` (in the same directory as `docker-compose.yml`)
- **Container path:** `/opt/airavata/vault/airavata-server.properties`

### Example docker-compose.yml volume mount:
```yaml
volumes:
  - ./airavata-server.properties:/opt/airavata/vault/airavata-server.properties:ro
```

## Viewing Logs

### All Services Logs
```bash
# View all logs from all services
docker logs airavata-monolithic

# Follow logs in real-time
docker logs -f airavata-monolithic

# View last 100 lines
docker logs --tail 100 airavata-monolithic
```

### What You'll See
The logs include all services with prefixes:
- `[API-Orchestrator]` - Main API server
- `[API-Controller]` - Workflow controller
- `[API-Participant]` - Workflow participant
- `[API-PreWM]` - Pre-workflow manager
- `[API-PostWM]` - Post-workflow manager
- `[API-EmailMonitor]` - Email monitoring
- `[API-RealtimeMonitor]` - Real-time monitoring
- `[Agent]` - Agent service
- `[Research]` - Research service
- `[File]` - File service

## Configuration Changes

### After modifying properties file:
```bash
# Restart only the Airavata container (keeps database data)
docker-compose restart airavata-monolithic

# Or restart all services
docker-compose restart
```

### Check if changes took effect:
```bash
# View logs to see startup messages
docker logs airavata-monolithic
```

## Common Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View running containers
docker ps

# View logs
docker logs airavata-monolithic

# Access RabbitMQ Management
# Open: http://localhost:15672
# Username: airavata
# Password: airavata
```

## Troubleshooting

### Properties file not found:
```bash
# Check if file exists
ls -la airavata-server.properties

# Check file permissions
chmod 644 airavata-server.properties
```

### Services not starting:
```bash
# Check container logs
docker logs airavata-monolithic

# Check if all containers are running
docker ps

# Restart services
docker-compose restart
```

### Database connection issues:
```bash
# Check database logs
docker logs mariadb

# Check if database is accessible
docker exec mariadb mysql -u airavata -pairavata_password -e "SELECT 1"
```

## Service Endpoints

| Service | Port | Protocol | Description |
|---------|------|----------|-------------|
| Airavata API | 8930 | Thrift RPC | Main API server |
| Agent Service | 18800 | Thrift RPC | Agent service |
| Research Service | 18889 | Thrift RPC | Research service |
| File Service | 8050 | Thrift RPC | File service |
| RabbitMQ Management | 15672 | HTTP | Web UI |

## Next Steps

1. **Connect with clients:**
   - Python: `pip install airavata-python-sdk`
   - Java: Use examples in `examples/airavata-api-java-client-samples/`

2. **Configure compute resources:**
   - Add SSH connections in properties file
   - Set up job schedulers (SLURM, PBS, etc.)

3. **Create experiments:**
   - Use the API to create and manage experiments
   - Monitor job status and results 