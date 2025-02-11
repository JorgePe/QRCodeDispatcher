from flask import Flask, render_template, request , redirect
import paho.mqtt.publish as mqttpub

app = Flask(__name__)

mqtt_broker = 'test.mosquitto.org'
mqtt_topic = '/plug/teste'

@app.route('/publish')
def publish():
    # extracts a msg from the called URL
    msg = request.args.get('msg')
    # and forwards it to a MQTT broker
    mqttpub.single(mqtt_topic, msg, hostname=mqtt_broker)
    # then redirects visitor to a page that informs what was done
    return render_template('message.html', msg = 'Comando enviado para ' + msg)

@app.route('/')
@app.route('/home')
def index():
    # renders a short web page
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=False)
