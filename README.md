# SRE-Projects
This is a repository in which I will create the SRE academy project. looking to include all the concept an aspects I learned in the SRE academy, important concepts as an example: software engineering principles and system availability. In this case an application that will monitor the CPU and RAM usage level and will trigger alerts in case the usage get critical levels






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



# Install Docker or Podman

For podman: https://podman.io/docs/installation

For docker: https://docs.docker.com/desktop/setup/install/mac-install/


# Install MInikube

https://minikube.sigs.k8s.io/docs/start/?arch=%2Fmacos%2Farm64%2Fstable%2Fbinary+download




# LOCAL (Minikube) DEPLOYMENT STEPS:

1. Start Minikube: (second command uses the podman driver)
   
             minikube start --driver=qemu # Recommended for broad OS/CPU compatibility


2. Point Docker environment to Minikube in order to build images directly into the Minikube VM.
   
             eval $(minikube -p minikube docker-env)

3. Build your application container image: After making changes to app/main.py or Dockerfile, rebuild the image. The kubectl rollout restart command in the next step will ensure the new image is used.

             docker build -t cpu_ram_monitor:latest -f MYdockerfile .

4. Install the monitoring tools, in this case(prometheus, grafana, alertmanager, Node Exporter):

            helm upgrade --install progralernod-stack prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace \
  --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesPods=false \
  --version 55.5.0




5. apply your application folder( which contains the .ymal deployment files):
   
        kubectl apply -f kub8s/


6. Portforwarding process to access the pods and the app's WEB GUI:

      Prometheus web gui:
   
        kubectl port-forward svc/prometheus-stack-grafana -n monitoring 3000:80

      grafana weg gui:
   
     kubectl port-forward svc/prometheus-stack-grafana -n monitoring 3000:80

    
