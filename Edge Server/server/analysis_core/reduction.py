import sys
sys.path.append('/home/pc/edge_service/v1/config/')
import settings

import logging
import tensorflow as tf
import joblib
import pandas as pd

logging.basicConfig(level = logging.INFO)


reduction_enable = settings.reduction_enable
reduction_model_name = settings.reduction_model

#reduction_model = None



def model_selector(model_name):
  if model_name == 'PCA':
    pca_file = 'server/analysis/models/PCA.joblib'
    logging.info('--> PCA is set as reduction model.')
    return joblib.load(pca_file)
  elif model_name == 'AE':
    encoder_file = "server/analysis/models/encoder.h5"
    logging.info('--> Auto-Encoder is set as reduction model.')
    return tf.keras.models.load_model(encoder_file)
  else:
    logging.info('--> '+ model_name + ' is not supported as reducton model! Please set it as PCA or AE')
    #return None

def reduce_data(data):
  if reduction_enable:
    #if not data["reduction"]:  
      if reduction_model_name == 'PCA':
        print('-> Call PCA')
        converted_data = pd.DataFrame(data).T
        red_data = pd.DataFrame(reduction_model.transform(converted_data))
        return red_data.to_json(orient ='index')

      elif reduction_model_name == 'AE':
        print('-> Call AE')
        converted_data = pd.DataFrame(data).T
        red_data = pd.DataFrame(reduction_model.predict(converted_data))
        return red_data.to_json(orient ='index')

def infernce_reduce_data(data):
  if reduction_model_name == 'PCA':
    print('-> Call PCA')
    return pd.DataFrame(reduction_model.transform(data))

  elif reduction_model_name == 'AE':
    print('-> Call AE')
    return pd.DataFrame(reduction_model.predict(data))


reduction_model = model_selector(reduction_model_name)

def run():
  if reduction_enable:
    global reduction_model
    reduction_model = model_selector(reduction_model_name)
  else:
    logging.info('--> Dimensionality Reduction is disable')
    
