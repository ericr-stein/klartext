# Monitoring Setup for Simplify Language Application

This document describes how to use the monitoring setup for the Simplify Language application.

## Overview

The monitoring stack consists of:

1. **Streamlit App with Embedded Metrics**: The application directly exposes Prometheus metrics on port 8000
2. **Prometheus**: Collects and stores metrics from the application
3. **Grafana**: Provides visualization dashboards for the collected metrics

## Metrics Collected

The monitoring system captures:

- **Request Counts**: Total number of simplification requests by simplification level, mode, and model
- **Processing Times**: How long each request takes to process (with percentile distributions)
- **Success Rate**: Percentage of successful requests 
- **Text Statistics**: Word counts for input and output texts
- **Compression Ratio**: Ratio of output to input word count

## Architecture Changes

The monitoring architecture has been simplified:
- Instead of using a separate log exporter, metrics are now embedded directly in the Streamlit app
- The app exposes a Prometheus metrics endpoint (port 8000)
- Prometheus scrapes this endpoint to collect metrics
- Grafana visualizes the metrics from Prometheus

This follows the KISS and SOLID principles by:
- Reducing the number of components (KISS)
- Making each component have a single responsibility (SOLID)
- Eliminating complex file parsing and intermediary containers

## Running Locally

To run the monitoring stack locally:

```bash
docker-compose -f docker-compose.local.yml down
docker-compose -f docker-compose.local.yml up -d
```

Access the services at:
- **Application**: http://localhost:8501
- **Metrics Endpoint**: http://localhost:8000
- **Grafana**: http://localhost:3000
- **Prometheus**: http://localhost:9090

## Production Deployment

The production setup is configured to work with Traefik reverse proxy:

```bash
docker-compose down
docker-compose up -d
```

Access the services at:
- **Application**: https://sp000201-t3.kt.ktzh.ch
- **Metrics Endpoint**: https://sp000201-t3.kt.ktzh.ch/metrics
- **Grafana**: https://sp000201-t3.kt.ktzh.ch/grafana
- **Prometheus**: https://sp000201-t3.kt.ktzh.ch/prometheus

## How It Works

1. The application directly exposes Prometheus metrics on port 8000
2. When users process texts, the metrics are updated in real-time
3. Prometheus scrapes metrics from the application every 15 seconds
4. Grafana displays these metrics in pre-configured dashboards

## Customizing Dashboards

The default dashboard "Simplify Language Metrics" provides an overview of the application performance. You can customize it or create new dashboards in Grafana.

## Troubleshooting

- **No data in Grafana**: Check that Prometheus can connect to the application metrics endpoint. Verify the connection settings in grafana/provisioning/datasources/prometheus.yaml.
- **Prometheus issues**: Check docker logs with `docker logs simplify-prometheus-local` or `docker logs simplify-prometheus`.
- **Application metrics**: Check that the app is exposing metrics correctly with `curl http://localhost:8000` (local) or `curl https://sp000201-t3.kt.ktzh.ch/metrics` (production).
