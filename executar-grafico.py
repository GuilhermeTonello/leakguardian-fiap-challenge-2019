import time
import multiprocessing as mp
from mq import *
import time
import paho.mqtt.client as mqtt
import RPi.GPIO as gpio
import matplotlib.pyplot as grafico

gpio.setwarnings(False)
buzz = 20
gpio.setmode(gpio.BCM)
gpio.setup(buzz, gpio.OUT)

conectado = False
graf = True

user = 'SEU USUÁRIO AQUI'
password = 'SUA SENHA AQUI'
server = 'mqtt.mydevices.com'
port = 1883
client_id = 'SEU ID DE CLIENTE AQUI'
publish_0 = 'v1/'+user+'/things/'+client_id+'/data/0'
client = mqtt.Client(client_id)

def gas():
    global graf
    mq = MQ();
    x = 0
    
    while True:
        perc = mq.MQPercentage()
        y = perc["GAS_LPG"]
    
        if (y > 50):
            print("ALERTA! GAS LPG DETECTADO:", y)
            for dc in range(0, 5, 1):
                gpio.output(buzz, gpio.HIGH)
                time.sleep(0.15)
                gpio.output(buzz, gpio.LOW)
                time.sleep(0.15)
                    
            if conectado:
                client.publish(publish_0, y)
            
        if graf:
            xdata = []
            ydata = []
            grafico.figure(num='Grafico Gas x Tempo')
            axes = grafico.gca()
            axes.set_xlim(0, 100)
            axes.set_ylim(-2000, +2000)
            line, = axes.plot(xdata, ydata, 'b-')

            grafico.title('Gas x Tempo')
            grafico.xlabel('Tempo')
            grafico.ylabel('Gas')
            grafico.grid()
            graf = False

        x += 1
        xdata.append(x)
        ydata.append(y)
        line.set_xdata(xdata)
        line.set_ydata(ydata)
        grafico.draw()
        grafico.pause(1e-17)
            
            
        time.sleep(0.33)

if __name__ == "__main__":
    
    try:
        client.username_pw_set(user, password)
        client.connect(server,port)
        conectado = True
    except:
        print("Falha ao conectar")

    p1 = mp.Process(target=gas)
    p1.start()
    
    comando = input("Pressione ENTER quando desejar fechar o programa...\n")
    
    client.disconnect()
    gpio.cleanup()
    p1.terminate()
