from flask import Flask, render_template,jsonify
import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("LAPI/case/live")
    client.subscribe("LAPI/lamp/live")
    client.subscribe("lapiClock/#")

def on_message(client, userdata, msg):
     #print("on message "+ msg.topic+" "+str(msg.payload))
     global case_status
     if msg.topic == "LAPI/case/live":
         case_status = str(msg.payload)
     global lamp_status
     if msg.topic == "LAPI/lamp/live":
         lamp_status = str(msg.payload)


mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("localhost", 1883, 60)
mqttc.loop_start()

app = Flask(__name__)

clock_status = ''
case_status = ''
lamp_status = ''
cup_status = ''
clean_status = ''
@app.route('/')
def hello():
    return render_template('index.html')
@app.route('/status')
def api():
    data = {
        "clock_status": clock_status,
        "case_status": case_status,
        "lamp_status": lamp_status,
        "cup_status": cup_status,
        "clean_status": clean_status
    }
    return jsonify(data)

@app.route("/case/open")
def case_open():
    print('case open')
    mqttc.publish("LAPI/case/speed1",155)
    mqttc.publish("LAPI/case/speed2",155)
    
    mqttc.publish("LAPI/case/motor1",512)
    mqttc.publish("LAPI/case/motor2",512)
    return ''

@app.route("/case/close")
def case_close():
    print('case close')
    mqttc.publish("LAPI/case/speed1",155)
    mqttc.publish("LAPI/case/speed2",155)
    
    mqttc.publish("LAPI/case/motor1",815)
    mqttc.publish("LAPI/case/motor2",195)
    return ''
    
@app.route("/case/init")
def clock_init():
    print('clock init')
    mqttc.publish("LAPI/case/speed1",155)
    mqttc.publish("LAPI/case/speed2",155)
    
    mqttc.publish("LAPI/case/motor1",512)
    mqttc.publish("LAPI/case/motor2",512)
    
    time.sleep(2)

    mqttc.publish("LAPI/case/motor1",815)
    mqttc.publish("LAPI/case/motor2",195)
    
    time.sleep(2)

    return ''

@app.route("/lamp/init")
def lamp_init():
    print('clock init')
    mqttc.publish("LAPI/lamp/speed1",155)
    mqttc.publish("LAPI/lamp/speed2",155)
    mqttc.publish("LAPI/lamp/speed3",155)
    mqttc.publish("LAPI/lamp/speed4",155)
    mqttc.publish("LAPI/lamp/speed5",155)
    mqttc.publish("LAPI/lamp/speed6",155)
    mqttc.publish("LAPI/lamp/speed7",155)
    
    mqttc.publish("LAPI/lamp/motor2",300)
    time.sleep(1)
    mqttc.publish("LAPI/lamp/motor1",1023)
    time.sleep(1)
    mqttc.publish("LAPI/lamp/motor3",330)
    time.sleep(1)
    mqttc.publish("LAPI/lamp/motor6",700)
    #time.sleep(1)
    #mqttc.publish("LAPI/lamp/motor4",450)
    time.sleep(1)
    mqttc.publish("LAPI/lamp/motor5",900)
    #time.sleep(1)
    #mqttc.publish("LAPI/lamp/motor7",450)
    
    time.sleep(2)
    
    mqttc.publish("LAPI/lamp/motor2",195)
    time.sleep(1)
    mqttc.publish("LAPI/lamp/motor1",512)
    time.sleep(1)
    mqttc.publish("LAPI/lamp/motor3",0)
    time.sleep(1)
    mqttc.publish("LAPI/lamp/motor6",1023)
    #time.sleep(1)
    #mqttc.publish("LAPI/lamp/motor4",450)
    time.sleep(1)
    mqttc.publish("LAPI/lamp/motor5",767)
    #time.sleep(1)
    #mqttc.publish("LAPI/lamp/motor7",450)
    
    return ''

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
