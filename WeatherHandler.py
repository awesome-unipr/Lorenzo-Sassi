import python_weather
import json
import asyncio
import os
import paho.mqtt.client as mqtt
from aiohttp import web

class MqttClient:
    def __init__(self, host, port):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.host = host
        self.port = port

        self.mqtt_connection()

    def mqtt_connection(self):
        self.client.connect(self.host, self.port, 60)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
    
    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))

    def subscribe(self, topic):
        self.client.subscribe(topic)
        print("Subscribed to " + topic)
    
    def publish(self,topic, message):
        self.client.publish(topic, message)

    def start(self):
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()

class HttpServer:
    def __init__(self, WeatherHandler):
        self.app = web.Application()
        self.routes = web.RouteTableDef()

        self.WeatherHandler = WeatherHandler

        @self.routes.post('/weathercurrent')
        async def post_handler(request):
            print("POST (current weather) ricevuto")
            data_curr = await request.post()
            #a = json.load(data)
            b = int(data_curr['current_temperature'])
            print(b)
            print(data_curr['current_description'])
            print(data_curr['current_kind'])
            
            return web.Response(text = "ok")

        @self.routes.post('/weatherforecast')
        async def post_handler1(request):
            print("POST (forecast) ricevuto")
            print("----")
            data_forec = await request.json()
            
            data = json.loads(data_forec)

            print(data)
            print("------")
            print(data['0']['kind'])
            print("------")
            
            return web.Response(text = "ok")

        self.app.add_routes(self.routes)


    def start(self):
        web.run_app(self.app)
    
    def stop(self):
        web.run_app(self.app)

class WeatherHandler:
    def __init__(self, mqtt_client):
        self._mqtt_client = mqtt_client

    def current_w(self):
        
        self._mqtt_client.publish("vc2324/weather-current")
        
mqtt_client = MqttClient('127.0.0.1', 1883)

WeatherHandler = WeatherHandler(mqtt_client)
        
http_server = HttpServer(WeatherHandler)

mqtt_client.subscribe("vc2324/weather-current")
mqtt_client.start()
http_server.start()

mqtt_client.stop()

print("Program terminated!")