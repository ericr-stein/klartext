# Docker Setup for Language Simplification App

This guide explains how to run the Language Simplification App using Docker in conjunction with an existing Ollama setup.

## Prerequisites

1. Docker and Docker Compose installed
2. Access to an Ollama instance running in Docker
3. The following models available in your Ollama instance:
   - llama3-70b
   - sauerkraut-70b
   - gemma2-27b
   - phi-3
   - llama3.3-70b

## Network Setup

The application is designed to work with a Traefik reverse proxy and connect to an existing Ollama instance. Make sure you have:

1. A running Traefik instance
2. An Ollama instance accessible via Docker network
3. Access to the `traefik_network` Docker network

## Configuration

1. Update the domain in `docker-compose.yml`:
   ```yaml
   labels:
     - "traefik.http.routers.simplify.rule=Host(`your-domain.example.com`)"
   ```

2. The application will automatically connect to Ollama at `http://ollama:11434`. This is configured via the `OLLAMA_HOST` environment variable in the docker-compose.yml file.

## Running the Application

1. Build and start the application:
   ```bash
   docker-compose up -d
   ```

2. The application will be available at your configured domain through Traefik.

3. Monitor the logs:
   ```bash
   docker-compose logs -f
   ```

## Troubleshooting

1. Check Ollama connection:
   - The app will display a success message if it can connect to Ollama
   - Check the logs for any connection errors

2. Common issues:
   - Ensure the required models are loaded in Ollama
   - Verify network connectivity between containers
   - Check Traefik routing configuration

## Environment Variables

- `OLLAMA_HOST`: URL of the Ollama API (default: http://ollama:11434)

## Logs

- Application logs are stored in the `logs` directory
- The directory is mounted as a volume for persistence

## Security Notes

1. The application runs behind Traefik with TLS enabled
2. All communication with Ollama happens within the Docker network
3. No sensitive data is stored in the container

## Resource Considerations

The application itself is lightweight, but the Ollama models require significant resources:
- Memory: Varies by model (4GB-48GB)
- CPU: Multi-core recommended
- GPU: Required for optimal performance

## Maintenance

1. Updating the application:
   ```bash
   docker-compose pull
   docker-compose up -d
   ```

2. Checking container health:
   ```bash
   docker-compose ps
   ```

3. Restarting the application:
   ```bash
   docker-compose restart
