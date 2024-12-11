import sys
sys.path.append('/home/pc/edge_service/v1/config/')
import settings
import dbmodel
import reduction

import logging
import joblib
import pandas as pd

logging.basicConfig(level = logging.INFO)


sliding_window_size = settings.sliding_window_size
outlier_drop_rate = settings.outlier_drop_rate

outlier_enable = settings.outlier_enable
outlier_model_name = settings.outlier_model_name

#Load outlier model
outlier_file = "./server/analysis/models/" + outlier_model_name + ".joblib"
outlier_model = joblib.load(outlier_file)

#global outlier_model

def run():
  if outlier_enable:
    print("--> Outlier detection model " + outlier_model_name + " is set.")
  else:
    print("--> Outlier Detection model is not set.")

def feed(data):
  if outlier_enable:
    #Convert data window to panda dataframe
    converted_data = pd.DataFrame(data['data']).T
    #Detect outliers and count valid data
    data_validation_value = pd.DataFrame(outlier_model.predict(converted_data)).T
    data_valid_count = data_validation_value.values.tolist()[0].count(1)
    #Check data validation and drop invalid data.  
    if (data_valid_count/sliding_window_size)*100 >= outlier_drop_rate:
      #store only valid data in database
      data["validation"] = "checked"
      data["outlier_model"] = outlier_model_name
      if settings.store_enable:
        dbmodel.insert(data)
      
  else:
    #store all data in database without outlier detection
    data["validation"] = "unchecked"
    data["outlier_model"] = None
    if settings.store_enable:
        dbmodel.insert(data)



def inference_feed(data):
  #Detect outliers and count valid data
  data_validation_value = pd.DataFrame(outlier_model.predict(data)).T
  data_valid_count = data_validation_value.values.tolist()[0].count(1)
  #Check data validation and drop invalid data.  
  if (data_valid_count/sliding_window_size)*100 >= outlier_drop_rate:
    return {"value": True,"data":data}
  else:
    return {"value": False,"data":None}
