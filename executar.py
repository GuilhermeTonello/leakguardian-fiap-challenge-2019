import time
import multiprocessing as mp
from mq import *
import time
import paho.mqtt.client as mqtt
import RPi.GPIO as gpio

gpio.setwarnings(False)
buzz = 20
gpio.setmode(gpio.BCM)
gpio.setup(buzz, gpio.OUT)
p = gpio.PWM(buzz, 1500)
p.start(0)

conectado = False

user = 'SEU USUÁRIO AQUI'
password = 'SUA SENHA AQUI'
server = 'mqtt.mydevices.com'
port = 1883
client_id = 'SEU ID DE CLIENTE AQUI'
publish_0 = 'v1/'+user+'/things/'+client_id+'/data/0'
client = mqtt.Client(client_id)

def gas():
    
    mq = MQ();
    
    while True:
        perc = mq.MQPercentage()
        y = perc["GAS_LPG"]
    
        if (y > 50):
            print("ALERTA! GAS LPG DETECTADO:", y)
            for dc in range(0, 5, 1):
                p.ChangeDutyCycle(100)
                time.sleep(0.2)
                p.ChangeDutyCycle(0)
                time.sleep(0.2)
            
        if conectado:
            client.publish(publish_0, y)
        p.ChangeDutyCycle(0)
        time.sleep(0.33)

if __name__ == "__main__":
    
    try:
        client.username_pw_set(user, password)
        client.connect(server,port)
        conectado = True
    except:
        print("Falha ao conectar")
        
    gas()  
    
    client.disconnect()
    
    p.stop()
    gpio.cleanup()