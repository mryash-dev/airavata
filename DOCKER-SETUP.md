# Apache Airavata Docker Setup

This repository contains a Dockerized setup for Apache Airavata with all services running in a single monolithic container.

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd airavata
   ```

2. **Copy and configure the properties file:**
   ```bash
   cp airavata-api/src/main/resources/airavata-server.properties.example airavata-server.properties
   # Edit airavata-server.properties with your configuration
   ```

3. **Start the services:**
   ```bash
   docker-compose up -d
   ```

4. **Test the services:**
   ```bash
   python3 test-airavata.py
   ```

## Docker Compose Services

- **airavata-monolithic**: Main Airavata server with all services
- **mariadb**: Database for Airavata catalogs
- **rabbitmq**: Message broker
- **zookeeper**: Distributed coordination service
- **kafka**: Distributed streaming platform

## Ports

- **8930**: Airavata API (Thrift RPC)
- **8050**: File Server (Thrift RPC)
- **18800**: Agent Service (Thrift RPC)
- **18889**: Research Service (Thrift RPC)
- **3306**: MariaDB
- **5672**: RabbitMQ
- **15672**: RabbitMQ Management UI
- **9092**: Kafka
- **2181**: ZooKeeper

## GitHub Actions

### Automated Docker Build and Push

The repository includes a GitHub Actions workflow that automatically builds and pushes the Docker image to Docker Hub.

#### Setup Required Secrets

To enable automatic Docker image publishing, add these secrets to your GitHub repository:

1. Go to your repository → Settings → Secrets and variables → Actions
2. Add the following secrets:

   - **`DOCKER_HUB_USERNAME`**: Your Docker Hub username
   - **`DOCKER_HUB_ACCESS_TOKEN`**: Your Docker Hub access token

#### How to Create Docker Hub Access Token

1. Log in to [Docker Hub](https://hub.docker.com)
2. Go to Account Settings → Security
3. Click "New Access Token"
4. Give it a name (e.g., "GitHub Actions")
5. Copy the token and save it as `DOCKER_HUB_ACCESS_TOKEN` in GitHub secrets

#### Workflow Triggers

The workflow runs on:
- Push to `main` or `master` branches
- Push of version tags (e.g., `v1.0.0`)
- Pull requests to `main` or `master` branches
- Manual trigger via workflow_dispatch

#### Image Tags

The workflow automatically creates tags:
- Branch name for branch pushes
- Version number for version tags
- SHA-based tags for commits

## Development

### Local Development

1. **Mount your properties file:**
   ```yaml
   volumes:
     - ./airavata-server.properties:/opt/airavata/vault/airavata-server.properties:ro
   ```

2. **View logs:**
   ```bash
   docker logs airavata-monolithic
   ```

3. **Access services:**
   - RabbitMQ Management: http://localhost:15672 (airavata/airavata)
   - All Thrift services are accessible on their respective ports

### Configuration

The main configuration file is `airavata-server.properties`. Key settings:

- Database connection (MariaDB)
- RabbitMQ configuration
- Kafka settings
- Service ports and hosts

## Troubleshooting

### Common Issues

1. **Services not starting:**
   ```bash
   docker-compose logs airavata-monolithic
   ```

2. **Database connection issues:**
   ```bash
   docker-compose restart mariadb
   ```

3. **Port conflicts:**
   Check if ports are already in use and modify `docker-compose.yml`

### Health Checks

The container includes health checks, but they may show as "unhealthy" due to Thrift RPC services not responding to HTTP health checks. This is normal - the services are working correctly.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with Docker Compose
5. Submit a pull request

## License

Apache License 2.0 