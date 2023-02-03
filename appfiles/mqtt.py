from cherrystrap import logger, formatter
import appfiles
import paho.mqtt.client as mqtt
import time
import json

def connect_mqtt(**kwargs):

	def on_connect(client, userdata, flags, rc):
		if rc == 0:
			client.connected_flag=True
			logger.info("Connected to MQTT Broker!")
		else:
			client.connected_flag=False
			logger.warn("Failed to connect, return code %d\n", rc)

	client = mqtt.Client(kwargs['mqtt_client_id'])
	client.username_pw_set(kwargs['mqtt_username'], kwargs['mqtt_password'])
	client.on_connect = on_connect
	client.connect(kwargs['mqtt_broker_addr'], kwargs['mqtt_broker_port'])

	return client

def publish(*args, **kwargs):
	client = connect_mqtt(mqtt_client_id=kwargs['mqtt_client_id'], mqtt_username=kwargs['mqtt_username'], 
		mqtt_password=kwargs['mqtt_password'], mqtt_broker_addr=kwargs['mqtt_broker_addr'], mqtt_broker_port=kwargs['mqtt_broker_port']
		)
	client.loop_start()
	msg_count = 0
	while msg_count < 1:
		time.sleep(1)
		result = client.publish(args[0], args[1])
		status = result[0]
		if status == 0:
			logger.info(f"Send `{args[1]}` to topic `{args[0]}`")
		else:
			logger.warn(f"Failed to send message to topic {args[0]}")
		msg_count +=1
	disconnect_mqtt(client)

def establish_sensor(*args, **kwargs):
	sensor_id = args[0].lower().replace(' ','_')
	topic = kwargs['mqtt_prefix']+'/sensor/'+sensor_id+'/config'
	sensorConfig = {
		'name': args[0],
		'state_topic': kwargs['mqtt_prefix']+'/sensor/'+sensor_id+'/state'
	}
	if 'attributes' in kwargs and kwargs['attributes']:
		sensorConfig['json_attributes_topic']=kwargs['mqtt_prefix']+'/sensor/'+sensor_id+'/attributes'
	if 'units' in kwargs and kwargs['units']:
		sensorConfig['unit_of_measurement']=kwargs['units']
	if 'icon' in kwargs and kwargs['icon']:
		sensorConfig['icon']=kwargs['icon']

	sensorJson = json.dumps(sensorConfig)
	publish(topic, sensorJson, **kwargs)

def update_values(*args, **kwargs):
	sensor_id = args[0].lower().replace(' ','_')
	topic = kwargs['mqtt_prefix']+'/sensor/'+sensor_id+'/state'
	publish(topic, args[1], **kwargs)

def update_attributes(*args, **kwargs):
	sensor_id = args[0].lower().replace(' ','_')
	topic = kwargs['mqtt_prefix']+'/sensor/'+sensor_id+'/attributes'
	attrArr = kwargs['attrArray']
	attrJson = json.dumps(attrArr)
	publish(topic, attrJson, **kwargs)

def disconnect_mqtt(client):
	client.disconnect()
	client.connected_flag=False
	logger.info("Disconnected from MQTT Broker!")

if __name__ == '__main__':

	pass
