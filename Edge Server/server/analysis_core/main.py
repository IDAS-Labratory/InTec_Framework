import pubsub
import outlier
import reduction
import dbmodel
import inference

if __name__ == '__main__':
    #Run Database
    dbmodel.run()
    # Run Inference
    inference.run()
    #Run outlier detection    
    outlier.run()
    #Run Dimensionality Reduction
    reduction.run()
    #Run MQTT connections
    pubsub.run()
