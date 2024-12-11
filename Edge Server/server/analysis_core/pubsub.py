import sys
sys.path.append('/home/pc/edge_service/v1/config/')
import settings
import outlier
import dbmodel
import reduction
import inference

import paho.mqtt.client as mqtt
import time
import json
import threading
import logging
import datetime

logging.basicConfig(level = logging.INFO)


# Default Configurations
edge_client_id = settings.client_id
interval = settings.cloud_sync_period # synchronyzation period time

cloud_broker_addr = settings.cloud_mqtt_broker
cloud_broker_port = settings.cloud_mqtt_port
cloud_mqtt_topic = settings.cloud_mqtt_topic

edge_broker_addr = settings.mqtt_broker 
edge_broker_port = settings.mqtt_port
edge_mqtt_topic = settings.mqtt_topic

clients=[
{"broker": cloud_broker_addr, "port": cloud_broker_port, "name": edge_client_id + "_cloud", "sub_topic": cloud_mqtt_topic, "pub_topic":cloud_mqtt_topic},
{"broker": edge_broker_addr, "port": edge_broker_port, "name": edge_client_id + "_edge", "sub_topic": edge_mqtt_topic, "pub_topic": edge_mqtt_topic}
]

nclients=len(clients)
message="test message"
threads=[]

def Connect(client,broker,port,keepalive,run_forever=False):
    """Attempts connection set delay to >1 to keep trying
    but at longer intervals. If runforever flag is true then
    it will keep trying to connect or reconnect indefinetly otherwise
    gives up after 3 failed attempts"""
    connflag = False
    delay = 5
    #print("connecting ",client)
    badcount = 0 # counter for bad connection attempts
    while not connflag:
        logging.info("connecting to broker " + str(broker))
        #print("connecting to broker "+str(broker)+":"+str(port))
        print("Attempts ", str(badcount))
        time.sleep(delay)
        try:
            client.connect(broker,port,keepalive)
            connflag=True

        except:
            client.badconnection_flag=True
            logging.info("connection failed "+str(badcount))
            badcount +=1
            if badcount>=3 and not run_forever: 
                return -1
                raise SystemExit #give up


                
    return 0
    #####end connecting


def wait_for(client, msgType, period=1, wait_time=10, running_loop=False):
    """Will wait for a particular event gives up after period*wait_time, Default=10 seconds.Returns True if succesful False if fails"""
    #running loop is true when using loop_start or loop_forever
    client.running_loop=running_loop #
    wcount=0  
    while True:
        logging.info("Waiting for: " + msgType)
        if msgType=="CONNACK":
            if client.on_connect:
                if client.connected_flag:
                    return True
                if client.bad_connection_flag: #
                    return False
                
        if msgType=="SUBACK":
            if client.on_subscribe:
                if client.suback_flag:
                    return True
        if msgType=="MESSAGE":
            if client.on_message:
                if client.message_received_flag:
                    return True
        if msgType=="PUBACK":
            if client.on_publish:        
                if client.puback_flag:
                    return True
     
        if not client.running_loop:
            client.loop(.01)  #check for messages manually
        time.sleep(period)
        wcount+=1
        if wcount>wait_time:
            print("--> Return from wait loop taken too long")
            return False
    return True


def client_loop(client, broker, port, keepalive=60, loop_function=None, loop_delay=1, run_forever=False):
    """runs a loop that will auto reconnect and subscribe to topics
    pass topics as a list of tuples. You can pass a function to be
    called at set intervals determined by the loop_delay
    """
    client.run_flag = True
    client.broker = broker
    print("--> Running loop for client: " + broker)
    client.reconnect_delay_set(min_delay = 1, max_delay = 12)
      
    while client.run_flag: #loop forever

        if client.bad_connection_flag:
            break         
        if not client.connected_flag:
            print("--> Connecting to ", broker, "...")
            if Connect(client, broker, port, keepalive, run_forever) != -1:
                if not wait_for(client, "CONNACK"):
                   client.run_flag = False #break no connack
            else: #connect fails
                client.run_flag = False #break
                print("--> Quitting loop for  broker ", broker)

        client.loop(0.01)

        if client.connected_flag and loop_function: #function to call
            loop_function(client, loop_delay) #call function
    
    time.sleep(1)
    print("disconnecting from", broker)
    if client.connected_flag:
        client.disconnect()
        client.connected_flag = False


def on_log(client, userdata, level, buf):
   print(buf)


def on_message(client, userdata, message):
    jsonMsg=json.loads(str(message.payload.decode("utf-8")))
    #print("-> "+ str(jsonMsg['device']) +" Your Activity: " + str(jsonMsg['label']))
    if settings.inference_enable:
        inference.feed(jsonMsg)
    else:
        #send data to oulier detection module
        outlier.feed(jsonMsg)


def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        for c in clients:
          if client==c["client"]:
              if c["sub_topic"]!="":
                  client.subscribe(c["sub_topic"])
          
        #print("connected OK")
    else:
        print("Bad connection Returned code=",rc)
        client.loop_stop()


def on_disconnect(client, userdata, rc):
   client.connected_flag=False #set flag
   #print("client disconnected ok")


def on_publish(client, userdata, mid):
   print("-> Publish mid = "  ,mid)


def pub(client, loop_delay):
    
    msg_dict = {
            'edge_id': edge_client_id,
            'reduction_model': settings.reduction_model,
            'window_size': settings.sliding_window_size,
            'date': str(datetime.datetime.utcnow()),
            'data': []
        }
    data_batch = dbmodel.fetch_data_batch(loop_delay)
    if not settings.inference_enable:
        for data in data_batch:
            reduced_data = reduction.reduce_data(data["data"])
            red_json_data = json.loads(reduced_data)
            red_json_data["label"] = int(data["label"])
            msg_dict["data"].append(red_json_data)
    else:
        for data in data_batch:
            json_data = data["data"]
            json_data["label"] = int(data["label"])
            msg_dict["data"].append(json_data)
    
    msg = json.dumps(msg_dict)
    result = client.publish(cloud_mqtt_topic, msg)
    status = result[0]
    if status == 0:
        print('-> Publish: ' + str(msg_dict["edge_id"]) + ' Send message to topic ' + cloud_mqtt_topic)
    else:
        print(f'--> Failed to send message to topic {cloud_mqtt_topic}: {result}')
        time.sleep(1)

    time.sleep(loop_delay)
    

def Create_connections():
    for i in range(nclients):
        cname = edge_client_id + str(i)
        ti = int(time.time())
        client_id = cname + "_" + str(ti) # create unique client_id
        client = mqtt.Client(client_id)             #create new instance
        
        clients[i]["client"] = client 
        clients[i]["client_id"] = client_id
        clients[i]["cname"] = cname
        
        broker = clients[i]["broker"]
        port = clients[i]["port"]
        
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        
        if clients[i]["broker"] == cloud_broker_addr:
            client.on_publish = on_publish
            t = threading.Thread(target = client_loop,args = (client,broker,port,60, pub, interval*60))

        elif clients[i]["broker"] == edge_broker_addr:
            client.on_message = on_message
            t = threading.Thread(target = client_loop,args = (client,broker,port,60))

        threads.append(t)
        t.start()  


def run():
    mqtt.Client.connected_flag = False #create flag in class
    mqtt.Client.bad_connection_flag = False #create flag in class

    
    print("--> Creating Connections ")
    no_threads=threading.active_count()
    print("Current threads =",no_threads)
    print("Publishing ")
    Create_connections()

    print("--> All clients connected ")
    no_threads=threading.active_count()
    print("Current threads =",no_threads)
    print("--> Starting main loop")
    try:
        while True:
            time.sleep(10)
            no_threads = threading.active_count()
            print("Current threads =",no_threads)
            for c in clients:
                if not c["client"].connected_flag:
                    print("--> Broker ",c["broker"]," is disconnected")
        

    except KeyboardInterrupt:
        print("ending")
        for c in clients:
            c["client"].run_flag=False
    time.sleep(10)
   





