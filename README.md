# SRE-Project: Flask application to monitor CPU, RAM and Network traffic and send alerts
This is a repository in which I will create the SRE academy project. looking to include all the concept an aspects I learned in the SRE academy, important concepts as an example: software engineering principles and system availability. In this case an application that will monitor the CPU, RAM and NETWORK traffic usage level and will trigger alerts in case the usage gets critical levels




# Architecture
Flask App: periodically checks with the use of (Python system and process utilities) the system CPU, RAM and Network traffic

Prometheus: scrapes /metrics every 10 seconds via a ServiceMonitor.

Grafana: visualizes metrics, cpu, ram usage and network traffic

Alertmanager: alerts on high cpu usage, high ram usage and high traffic volume in the interfaces

Kubernetes: orchestrates deployment via deployment.yaml, service.yaml, etc.




# Requirements
Podman or Docker

Prometheus + Grafana + alertmanager via Helm chart

Minikube (or any Kubernetes cluster) - Consider using the --driver=qemu for broad OS/CPU compatibility.

Helm --version 65.3.1

Python 3.9+

kubectl commands


# Project Tree

```text
.
├── ScreenShot evidence project running
│   ├── Getting-alerts-in-SLACK.png
│   ├── grafana-custom-dashboard.png
│   ├── Alerts in AlertManager.png
│   ├── more screenshot.png
├── Send-alerts-to-SLACK
│   └── alertmanager-slack-notification.yml
├── application
│   ├── app.py
│   ├── require.txt
├── kub8s
│   ├── 
│   ├── cpu-ram-in-servicemonitor.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   └── system-metrics-alerts.yml
├── monitoring-system-grafana-dashb
│   └── system-metrics-dashb.json
├── kubectl
├── CONTRIBUTING.md
├── MYdockerfile
├── LICENSE.md
├── .gitignore
└── README.md
```






# Install Docker

For docker: https://docs.docker.com/desktop/setup/install/mac-install/ **(recommended )**



# Install MInikube

https://minikube.sigs.k8s.io/docs/start/?arch=%2Fmacos%2Farm64%2Fstable%2Fbinary+download





# LOCAL (Minikube) DEPLOYMENT STEPS:

1. **Start Minikube:** 
   
             minikube start --driver=qemu          (in this case quemu used for better compatibility)



2. **Point Docker environment to Minikube in order to build images directly into the Minikube VM**. If you run command (docker images) and there is not any output, you need this command:
   
             eval $(minikube -p minikube docker-env)


3. **Build your application container image:** After making changes to application/app.py or MYdockerfile, rebuild the image.
   The command: kubectl rollout restart command in the next step will ensure the new image is used.

             docker build -t cpu_ram_monitor:latest -f MYdockerfile .
    #run the command: **docker images**
   
    You will see the image name: **<cpu_ram_monitor>** in the repository



4. **Install the monitoring tools, in this case(prometheus, grafana, alertmanager):**

```
helm upgrade --install promegralert-stack prometheus-community/kube-prometheus-stack \
--namespace monitoring --create-namespace \
--set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesPods=false \
--set defaultRules.create=false \
--values Send-alerts-to-SLACK/alertmanager-slack-notification.yml \
--version 65.3.1

```

  To review the prometheus stack, run the command:  ***kubectl get pods -n monitoring***

  **Important** Wait for all the pods to be in running state before continue



5. **apply your application folder( which contains the .ymal deployment files):**
   
        kubectl apply -f kub8s/



6. **Portforwarding process to access the pods and the app's WEB GUI:**

      The Flask monitoring application itself, to review status:

      #find the pod name(it changes everytime you deploy the application) commands:
   

       kubectl get pods -l app=cpu-ram-monitor -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}'
   

       kubectl port-forward $POD_NAME 8000:5000
   


      **#remember change $POD_NAME with the real pod name got in the previous command**

       

      **Prometheus web gui:**
           first review the current prometheus svc name with this command:
   
        kubectl get svc -n monitoring  
   
   
        kubectl port-forward svc/promegralert-stack-prometheus 9090 -n monitoring
   

        ***#remember change: promegralert-stack-prometheus (This name changes everytime you create the deployment)***

      **grafana weg gui:**
   
        kubectl port-forward svc/promegralert-stack-grafana -n monitoring 3000:80 
        

      **Alert Manager gui:**

        kubectl --namespace monitoring port-forward svc/promegralert-stack-kube-pr-alertmanager 9093:9093 & 



8. **Once the previous step is done(portforward), access the URL from you computer:**

      App Status (JSON): http://localhost:8000

      App Status (JSON)prometehus metrics:http://localhost:8000/metrics
   

      Prometheus UI: http://localhost:9090
   
      Grafana UI: http://localhost:3000
          (default credentials: username: admin   password: admin or prom-operator)
          in case login fail, run command: kubectl get secret prometheus-stack-grafana -n monitoring -o jsonpath='{.data.admin-password}' | base64 --decode
   
     Alertmanager UI: http://localhost:9093




   # Custom Dashboard in Grafata to visualize Metrics

     Import monitoring-system-grafana-dashb/system-metrics-dashb.json into Grafana.
   
    - Navigate to your Grafana UI (http://localhost:3000).
    - Go to Dashboards > New  > Import.
    - Click "Upload JSON file" and select monitoring-system-grafana-dashb/system-metrics-dashb.json from your project directory.
        (Ensure you select Prometheus as the data source when prompted.)
    

   # Alerts

   Defined in kub8s/system-metrics-alerts.yml
   
   This file structure uses the prometheus operator which comes with the Helm prometheus stack installed in step four.
   
   Verify the alert appears in Prometheus UI at http://localhost:9090  , then go to alerts tab

   Verify the alert appears in the Alertmanager UI at http://localhost:9093
      

   *****####Important statement####*****
    - wait sometime for the alearts to trigger and display in alertmanager
    - by default the alerts in the file(system-metrics-alerts.yml) are set to low threathold as a test mode in order to review the alert in the alertmanager page, please consider change the value based on your needs.


#  Optional step in case you want to send alert to SLACK (this step provides extra points in this project )
Steps:
    
1. Create a Slack Webhook space

    
 1.1 Go to your Slack workspace and visit Slack API: Incoming Webhooks.

       
 1.2 Create a new app or use an existing one.
       
 1.3 Enable Incoming Webhooks and create a webhook URL for the desired channel. (copy and save this URL, you will need it later)

2. In the file called: (alertmanager-slack-notification.yml) paste the URL you genetated in step 1.3
    
   2.1 in the file (alertmanager-slack-notification.yml) replace this line: api_url: 'https://hooks.slack.com/services/T00000000

3. in the file (alertmanager-slack-notification.yml) change the channel(channel: '#all-testalerts) for the one you created in your slack




   # Notes
   
 - In the folder **"ScreenShot evidence project running"** you will find screenshots, they show the project in running state
 - The **(ISSUES)** segment tab in this repository contains all the steps from 0 to the end with issues and steps during the process of this project creation, this can be used as a guide in case it is needed. Added   screenshot with the project running to take reference.
 - This repository was created to accomplish the final task project of a practical training series developed for the SRE Academy.
 - The main purpose is to create an application that can create alerts and also be monitored in prometheus and grafana
 - ***Sending the alerts to slack*** is an optinal step which in this proyect will have extra point in the final grade, but it is an optional step.

   
   

    
