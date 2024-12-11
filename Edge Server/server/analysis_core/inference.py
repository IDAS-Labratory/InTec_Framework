import sys
sys.path.append('/home/pc/edge_service/v1/config/')
import settings

import dbmodel as db
import outlier
import reduction

import json
import tensorflow as tf
import logging
import joblib
import pandas as pd
import numpy as np
from numpy import array

inference_enable = settings.inference_enable

def recall_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

def precision_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))



scaler_file = "./server/analysis/models/Scaler.joblib"
scaler_model = joblib.load(scaler_file)

inference_model_file = "./server/analysis/models/CNN_LSTM.h5"
inference_model = tf.keras.models.load_model(inference_model_file, custom_objects={'f1_m': f1_m, 'precision_m':precision_m, 'recall_m':recall_m })


def run():
    if inference_enable:
        print("--> Inference model is set.")
    else:
        print("--> Inference model is not set.")

def scalering_data(data):
    #Convert data window to panda dataframe
    converted_data = pd.DataFrame(data["data"]).T
    return scaler_model.transform(converted_data)

def split_sequences(sequences, n_steps):
	X = list()
	for i in range(len(sequences)):
		# find the end of this pattern
		end_ix = i + n_steps
		# check if we are beyond the dataset
		if end_ix > len(sequences):
			break
		# gather input and output parts of the pattern
		seq_x = sequences[i:end_ix]
		X.append(seq_x)

	return array(X)


def feed(data):
    if inference_enable:
        scaler_data = scalering_data(data)
        #converted_data = pd.DataFrame(data["data"]).T
        #print(converted_data.shape)
        outlier_scaler_data = outlier.inference_feed(scaler_data)
        if outlier_scaler_data['value']:
            reduced_outlier_scaler_data = reduction.infernce_reduce_data(outlier_scaler_data['data'])
            reduced_outlier_scaler_data_np = np.expand_dims(reduced_outlier_scaler_data, axis=0)
            prediction = inference_model.predict(np.array(reduced_outlier_scaler_data_np[:]), batch_size=1)
            data["label"] = int(np.argmax(prediction))
            #data["data"] = json.loads(reduced_outlier_scaler_data.to_json(orient ='index'))
            if settings.store_enable:
                db.insert(data)