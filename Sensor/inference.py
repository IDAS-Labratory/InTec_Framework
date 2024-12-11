import numpy as np
import tflite_runtime.interpreter as tflite
import os
import time
import pandas as pd 
import json
from datetime import datetime
import paho.mqtt.client as mqtt
import joblib

sensor_name = os.environ["Name"] #1st param device name
subject = os.environ["Subject"] #2nd param sampling subject in dataset
mqtt_broker = os.environ["Broker"] #3th param broker address
mqtt_topic = os.environ["Topic"] #4th param publish topic
window_size = int(os.environ["WindowSize"]) #5th param part sliding window size
sampling_rate = int(os.environ["Rate"]) #6th param sampling rate (Hz)
work_time = int(os.environ["Time"]) * 60 #7th param work duration in minutes 

data_path = "data/" + subject #data path
scaler_file = "model/Scaler.joblib"

list_of_sensor_data_file = os.listdir(data_path) # load data

#start measuring sensor execution time
print("IoT device is activated.", 
      "\n Device Name:" , sensor_name,
      "\n Sampling Data:", subject, 
      "\n MQTT Broker:", mqtt_broker,
      "\n Topic:", mqtt_topic,
      "\n Inference Window size:", window_size,
      "\n Sampling Rate:", sampling_rate,
      "\n Sensor Execution Long Time:", work_time/60 , "mins",  
      )
start_work = time.time()

def load_to_json(data,class_label_array,n_fields,latency, sliding_window = 25):
    """[summary]
    Args:
        data ([type]): [description]
        class_label_array ([type]): [description]

    Returns:
        [type]: [description]
    """
    ## Reshaping data array to normal DataFrame format
    x_json = pd.DataFrame(data.reshape(n_fields,sliding_window)).to_json(force_ascii=False)
    
    ## Convert to standard json : one sliding windows
    x_json = json.loads(x_json)
    modified_x_json={}
    modified_x_json["device"] = sensor_name
    modified_x_json["date"] = str(datetime.now())
    modified_x_json["windowSize"] = sliding_window
    modified_x_json["data"] = x_json
    modified_x_json["label"] =  class_label_array.reshape(-1).tolist().index(class_label_array.max()) + 1
    modified_x_json["latency"] = latency
    ## Find the label number of correspoding data from one-hot
    ## array
    
    return modified_x_json
    
def run_model_on_simulated_data(dir_path = data_path, sliding_window = 25):
    """[summary]
    Args:
        dir_path (str, optional): [description]. Defaults to "data_path".
        sliding_window (int, optional): [description]. Defaults to 25.
    """

    client = mqtt.Client(sensor_name) #create new instance
    client.connect(mqtt_broker) #connect to broker
    
    ## Loading scaler model
    scaler_model = joblib.load(scaler_file)

    interpreter = tflite.Interpreter(model_path="model/model.tflite")
    interpreter.allocate_tensors()
    
    # Get input and output tensors.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    list_of_data = []

    while True:
        for i,path in enumerate(list_of_sensor_data_file):
            
            # Watchdog
            if (time.time() - start_work > work_time ):
                print("<<" + sensor_name  + "is done. Runtime was " + str(work_time) + "minutes. >>")
                return 
                
            if len(list_of_data) == sliding_window:
                ### Convert .npz to standard format for model
                input_data = np.array(list_of_data).reshape(1,sliding_window,23)
                
                ### Start measuring inference latenc
                start_Latency = time.time()

                ### Feed data to model
                interpreter.set_tensor(input_details[0]['index'], input_data.astype('float32'))
                ### Print the result
                interpreter.invoke()
                
                # The function `get_tensor()` returns a copy of the tensor data.
                # Use `tensor()` in order to get a pointer to the tensor.
                output_data = interpreter.get_tensor(output_details[0]['index'])
                
                ## Stop measuring inference latency
                stop_Latency = time.time()
                ## Calculate inference latency to millisecond
                inference_Latency = (stop_Latency - start_Latency) * 1000
            
                ## create json message for publishing 
                msg = load_to_json(input_data, output_data, 23, inference_Latency, sliding_window)
                print(">> Device " + sensor_name + " has published message on Topic " + mqtt_topic + "-> Window Size: " + json.dumps(msg["windowSize"])  + ", Date: " + json.dumps(msg["date"]), ", Label: " + json.dumps(msg["label"]), ", Inference Latency:" + str(inference_Latency))
                
                ## Publish MQTT message on given topic
                client.publish(mqtt_topic, json.dumps(msg))
                
                ## empty the list_of_data
                list_of_data = []

                ## sleep time is eaqual to sliding window_size/sampling_rate (duration of sampling data as many as sliding window)
                time.sleep(sliding_window/sampling_rate)

            else:
                ## read data one by one
                data_stream = np.load(file=dir_path+"/"+path)
                ## Scaling data stream
                data_stream = scaler_model.transform(data_stream)
                ## concate them into a list
                list_of_data.append(data_stream)
                

run_model_on_simulated_data(data_path, window_size)
