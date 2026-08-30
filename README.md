# Azure VM and Container Monitoring Platform

A cloud-hosted monitoring and observability project built to monitor the health and performance of a containerized Flask application and its underlying infrastructure.

The project uses Prometheus, Grafana, Node Exporter and cAdvisor for metrics collection and visualization, while Docker Compose runs the application and monitoring stack.

Infrastructure is provisioned in Microsoft Azure using Terraform, while a GitHub Actions CI/CD pipeline automatically tests, builds, scans and deploys the Flask application.

## Architecture

![System Status Dashboard architecture](./docs/screenshots/architecture/system-status-architecture.png)

The application runs on an Azure Linux VM using Docker Compose.

Terraform provisions the Azure infrastructure, while GitHub Actions handles application CI/CD. Prometheus collects application, host and container metrics, while Grafana provides visualization and alerting.

## Dashboard Preview

### Flask Dashboard

![Flask dashboard](./docs/screenshots/healthy/flask-dashboard.png)

### Health Check

![Health endpoint](./docs/screenshots/healthy/flask-health-check.png)

### Grafana Dashboard

| Application Health                                                                         | Application Traffic and Performance                                                                      |
| ------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| ![Application health](./docs/screenshots/healthy/grafana-dashboard/application-health.png) | ![Application traffic](./docs/screenshots/healthy/grafana-dashboard/application-traffic-performance.png) |
| **Server Metrics**                                                                         | **Container Metrics**                                                                                    |
| ![Server metrics](./docs/screenshots/healthy/grafana-dashboard/server-metrics.png)         | ![Container metrics](./docs/screenshots/healthy/grafana-dashboard/container-metrics.png)                 |

## Features

- Real-time monitoring of application and server health
- CPU, memory, disk and uptime metrics
- Container monitoring with cAdvisor
- Host monitoring with Node Exporter
- Application metrics exposed through the Flask `/metrics` endpoint
- Grafana dashboards for historical visualization
- Grafana alerts for service and resource issues
- Automated CI/CD deployment with GitHub Actions
- Container vulnerability scanning with Trivy
- Docker image storage in GitHub Container Registry
- Azure infrastructure provisioned with Terraform

## Tech Stack

| Technology                | Purpose                                      |
| ------------------------- | -------------------------------------------- |
| Flask                     | Provides the dashboard and API endpoints     |
| Docker Compose            | Runs and manages the containerized services  |
| Prometheus                | Collects and stores monitoring metrics       |
| Grafana                   | Displays dashboards and evaluates alerts     |
| Node Exporter             | Provides Linux host metrics                  |
| cAdvisor                  | Provides Docker container metrics            |
| Terraform                 | Provisions the Azure infrastructure          |
| Azure Linux VM            | Hosts the application and monitoring stack   |
| GitHub Actions            | Runs tests, scanning and deployment          |
| GitHub Container Registry | Stores the Flask Docker image                |
| Trivy                     | Scans the image for security vulnerabilities |
| pytest                    | Tests the Flask application                  |

## How It Works

1. The developer pushes code to GitHub.
2. GitHub Actions runs pytest, builds the Flask Docker image and scans it with Trivy.
3. The approved image is pushed to GitHub Container Registry.
4. GitHub Actions authenticates to Azure using OIDC.
5. Azure VM Run Command starts the deployment on the VM.
6. The VM pulls the latest Flask image and recreates the Flask service with Docker Compose.
7. Prometheus collects application, host and container metrics.
8. Grafana queries Prometheus and displays dashboards and alerts.
9. Users access the Flask dashboard and Grafana through the Azure VM public IP, subject to the Network Security Group rules.

## Monitoring & Observability

Prometheus collects metrics from the Flask application, Node Exporter and cAdvisor.

- Flask exposes application metrics through `/metrics`
- Node Exporter provides host CPU, memory, disk and uptime metrics
- cAdvisor provides container CPU and memory metrics
- Grafana queries Prometheus and visualizes the metrics in dashboards
- Grafana alerts detect application and resource issues

The project focuses on metrics-based observability. Container logs are available through Docker, while distributed tracing is not included because the application runs as a single Flask service.

## CI/CD Pipeline

The project uses GitHub Actions to automate testing, security scanning, image publishing and deployment.

Pipeline flow:

1. Code is pushed to the `main` branch.
2. `pytest` runs the Flask application tests.
3. A Docker image is built.
4. Trivy scans the image for High and Critical vulnerabilities.
5. The image is pushed to GitHub Container Registry.
6. GitHub Actions authenticates to Azure using OIDC.
7. Azure VM Run Command starts the deployment.
8. The VM pulls the latest image and recreates the Flask service with Docker Compose.

Pull requests run the testing, build and security scan stages. Image publishing and Azure deployment only run for pushes to `main`.

## Azure Infrastructure

Terraform provisions the Azure infrastructure used to host the application and monitoring stack.

The deployed resources include:

- Resource Group
- Virtual Network
- Subnet
- Network Security Group
- Static Public IP address
- Network Interface
- Azure Linux Virtual Machine

The Azure VM runs Ubuntu Linux and hosts the Docker Compose stack containing the Flask application, Prometheus, Grafana, Node Exporter and cAdvisor.

## Security

- GitHub Actions authenticates to Azure using OpenID Connect (OIDC).
- No Azure password or client secret is stored in GitHub.
- SSH access on port `22` is restricted to the administrator IP address.
- Grafana access on port `3000` is restricted to the administrator IP address.
- Password authentication is disabled on the Azure VM, and access requires an SSH key.
- Trivy scans the Docker image and fails the pipeline when High or Critical vulnerabilities are detected.
- Prometheus, Node Exporter and cAdvisor are only available through the internal Docker network.
- Only the Flask dashboard on port `5000` is publicly exposed for demonstration.
- Terraform state, variable files and local plans are excluded from Git using `.gitignore`.
- The SSH private key is stored outside the repository.

## Failure Detection and Recovery

The monitoring setup was tested by intentionally stopping the Flask container and observing how the system responded.

Test flow:

1. The Flask container was stopped.
2. Prometheus detected that the application target was unavailable.
3. Grafana displayed the application as `DOWN`.
4. The Grafana alert changed to the `Firing` state.
5. Docker Compose confirmed that the Flask container was stopped.
6. The Flask container was started again.
7. Prometheus detected the recovered service.
8. Grafana returned the application status to `UP`.

This test demonstrates that the monitoring stack can detect an application failure and confirm recovery after the service is restored.

### Application Failure Detected

![Flask application down](./docs/screenshots/unhealthy/grafana-dashboards/flask-down.png)

### Alert Firing

![Grafana alert firing](./docs/screenshots/unhealthy/grafana-dashboards/flask-alert-firing.png)

## Local Setup

### Prerequisites

- Docker with Docker Compose
- Git

Clone the repository.

```bash
git clone https://github.com/aden-farah/system-status-dashboard.git
cd system-status-dashboard
```

Start the monitoring stack.

```bash
docker compose up -d
```

Confirm that the containers are running.

```bash
docker compose ps
```

Verify the Flask health endpoint.

```bash
curl http://localhost:5000/health
```

Open the Flask dashboard.

```text
http://localhost:5000
```

Open Grafana.

```text
http://localhost:3000
```

Stop the monitoring stack.

```bash
docker compose down
```

## Project Structure

```text
system-status-dashboard/
├── .github/
│   └── workflows/
│       └── pipeline.yml
├── app/
│   ├── static/
│   │   ├── script.js
│   │   └── style.css
│   ├── templates/
│   │   └── index.html
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── test_app.py
├── docs/
│   └── screenshots/
│       ├── architecture/
│       ├── healthy/
│       │   └── grafana-dashboard/
│       └── unhealthy/
│           └── grafana-dashboards/
├── grafana/
│   ├── dashboards/
│   │   └── system-status-dashboard.json
│   └── provisioning/
│       ├── alerting/
│       ├── dashboards/
│       └── datasources/
├── prometheus/
│   └── prometheus.yml
├── terraform/
│   ├── main.tf
│   ├── network.tf
│   ├── outputs.tf
│   ├── provider.tf
│   ├── variables.tf
│   └── vm.tf
├── docker-compose.yml
├── .gitignore
└── README.md
```

## Challenges and Lessons Learned

- Azure VM sizes are not always available in every region because of capacity restrictions. I learned how to check regional availability and adjust the deployment when required.
- Terraform state must remain synchronized with the actual Azure infrastructure. I learned to review Terraform plans and inspect the state before applying changes.
- Node Exporter required access to the host filesystem to provide accurate Azure VM metrics while running inside a container.
- Grafana dashboards and alert rules must be provisioned as code so the monitoring environment can be recreated consistently.
- Azure OIDC requires the federated identity configuration to match the GitHub Actions identity correctly.
- Testing application failure and recovery helped me understand how Prometheus target health and Grafana alerts react when a service goes down and recovers.
- Docker service names allow Prometheus, Grafana and the exporters to communicate through the internal Docker network without exposing every service publicly.
- Building the project end-to-end helped me understand how containers, monitoring, CI/CD, infrastructure as code and Azure networking work together as one system.

## Future Improvements

- Replace the Flask development server with a production WSGI server such as Gunicorn
- Add HTTPS with a custom domain and reverse proxy
- Configure email or messaging notifications for Grafana alerts
- Store Terraform state remotely in Azure Storage
- Pin Docker image versions instead of relying on `latest`
- Automate deployment of Docker Compose and Grafana configuration changes
