import paho.mqtt.client as mqtt
import time
import json

status = "off"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

#Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/iot/coffeemaker")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	global status	
	payload = json.loads(str(msg.payload))
	status = payload["status"]
	print status

#def on_publish(client, userdata, msg):
#	print{"alive":"true"}

       
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker_ip_address", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.

alive = True
t = 0
time.sleep(5)

while alive:
	client.loop()
	now = time.time()
	print now
	print t
	if status == "on" and t == 0:
		print "problem"
                alive = False

	if status == "off" and 10 < now-t < 60 and t != 0:
		print "problem"
		alive = False

	if status == "off" and t == 0:
		client.publish("/iot/coffeemaker/messages", '{"command":"on"}')
		t = now

 	if status == "on" and now-t > 60: 
		client.publish("/iot/coffeemaker/messages", '{"command":"off"}')
		alive = False
