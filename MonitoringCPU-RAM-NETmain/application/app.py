from flask import Flask, jsonify, render_template, Response
import psutil
import time
from collections import Counter
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST

# Define the gauge metric
bytes_sent_gauge = Gauge('network_bytes_sent_total', 'Total number of bytes sent over the network', ["interface"])
# Define the gauge for bytes received
bytes_recv_gauge = Gauge('network_bytes_received_total', 'Total number of bytes received over the network', ["interface"])

packets_sent_gauge = Gauge('network_packets_sent_total', 'Total number of packets sent over the network', ["interface"])

packets_recv_gauge = Gauge('network_packets_received_total', 'Total number of packets received over the network', ["interface"])

# Define Gauges
cpu_usage_percent = Gauge("cpu_usage_percent", "CPU usage percentage")
memory_usage_percent = Gauge("memory_usage_percent", "Memory usage percentage")
memory_used_bytes = Gauge("memory_used_bytes", "Used memory in bytes")
memory_available_bytes = Gauge("memory_available_bytes", "Available memory in bytes")

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"This is a page to show the application is on and running fine STATUS": "OK"})



#threathold configure with time
last_alert_time = 0
alert_interval = 100  # seconds

@app.route('/stats')
def stats():
    global last_alert_time
    cpu_percent = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    ram_percent = ram.percent

    

    return jsonify(cpu=cpu_percent, ram=ram_percent)



#network monitoring coding

@app.route('/network')
def network():
    stats = psutil.net_io_counters(pernic=True)
    usage = {
        iface: {
            'bytes_sent': data.bytes_sent,
            'bytes_recv': data.bytes_recv,
            'packets_sent': data.packets_sent,
            'packets_recv': data.packets_recv
        }
        for iface, data in stats.items()
    }
    return jsonify(usage)


#send the metrics to prometheus
@app.route('/metrics')
def metrics():

    # Update CPU metrics
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_usage_percent.set(cpu_percent)

    # Update memory metrics
    mem = psutil.virtual_memory()
    memory_usage_percent.set(mem.percent)
    memory_used_bytes.set(mem.used)
    memory_available_bytes.set(mem.available)
    stats = psutil.net_io_counters(pernic=True)

    for iface, data in stats.items():
        bytes_sent_gauge.labels(interface=iface).set(data.bytes_sent)
        bytes_recv_gauge.labels(interface=iface).set(data.bytes_recv)
        packets_sent_gauge.labels(interface=iface).set(data.packets_sent)
        packets_recv_gauge.labels(interface=iface).set(data.packets_recv)

    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == '__main__':
    app.run(debug=True)
