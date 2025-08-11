from flask import Flask, jsonify, render_template
import psutil

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stats')
def stats():
    cpu_percent = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    ram_percent = ram.percent
    return jsonify(cpu=cpu_percent, ram=ram_percent)



@app.route('/grafic')
def grafic():
    return render_template('grafic.html')


if __name__ == '__main__':
    app.run(debug=True)

#EMAIL set up, send alert to email

from flask_mail import Mail, Message


app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,  # Explicitly set this to False
    MAIL_USERNAME='albertocampos070@gmail.com',
    MAIL_PASSWORD='Alb3rtocampo$',
    MAIL_DEFAULT_SENDER='albertocampos070@gmail.com'
)






mail = Mail(app)




#SET THE THEATHOLD AT 50 TO SEND THE EMAIL
import psutil

last_alert_time = 0
alert_interval = 100  # seconds

@app.route('/stats')
def stats():
    global last_alert_time
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent

    now = time.time()
    if (cpu > 4 or ram > 50) and (now - last_alert_time > alert_interval):
        msg = Message("System Alert",
                      sender="albertocampos070@gmail.com",
                      recipients=["albertocampos070@gmail.com"])
        msg.body = f"High usage detected:\nCPU: {cpu}%\nRAM: {ram}%"
        mail.send(msg)
        last_alert_time = now

    return jsonify(cpu=cpu, ram=ram)


#send a test email
@app.route('/send')
def send_email():
    try:
        msg = Message("Hello from Flask",
                      recipients=["albertocampos070@gmail.com"])
        msg.body = "This is a test email sent from Flask-Mail."
        mail.send(msg)
        return "Email sent successfully!"
    except Exception as e:
        return f"Failed to send email: {e}"
