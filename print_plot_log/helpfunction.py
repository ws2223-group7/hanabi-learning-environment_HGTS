import os 
import numpy as np

def read_epoch_number(modelpath):
        """Return Epoch number based on last modelname"""
        if not os.path.exists(modelpath):
           return 0
        
        networks = os.listdir(modelpath)
        networks_as_int = [int(i) for i in networks]
        epoch_number = int(np.max(networks_as_int))

        return epoch_number

def main():
    print(read_epoch_number("models_with_reward_shaping"))

if __name__ == "__main__":
    main()