# SRE-Projects
This is a repository in which I will create the SRE academy project. looking to include all the concept an aspects I learned in the SRE academy, important concepts as an example: software engineering principles and system availability.






# Architecture
Flask App: periodically checks a list of URLs defined in urls.yaml, exposes /status and /metrics.

Prometheus: scrapes /metrics every 10 s via a ServiceMonitor.

Grafana: visualizes metrics and latency.

Alertmanager: alerts on failed URL checks; e.g. integration with Slack.

Kubernetes: orchestrates deployment via deployment.yaml, service.yaml, etc.







# Requirements
Podman or Docker
Prometheus + Grafana via Helm chart
Minikube (or any Kubernetes cluster) - Consider using the --driver=qemu for broad OS/CPU compatibility.
Helm
Python 3.9+
kubectl
