import argparse
import torch
import torchvision
import os
import numpy as np
from skimage import io
from skimage.transforms import resize
import argparse
import uncertainty 

parser = argparse.ArgumentParser()
parser.add_argument('--img_path', type=str, required=True)
parser.add_argument('--model_dir', type=str, required=True)

def main():
    # parse args
    args = parser.parse_args()
    
    # load and prep image
    image = io.imread(args.img_path).astype(np.float32)
    image = resize(image, (225,300)).transpose(2,0,1) / 255.0
    image = torch.tensor(image) 
    
    # prep model
    model = torchvision.models.resnet18(pretrained=True)
    model.fc.out_features=7
    n_model_paths = os.listdir(args.model_dir)
    
    # load models and perform inference
    preds = []
    for model_pth in n_model_paths:
        full_model_path = os.path.join(args.model_dir, model_pth)
        model.load_state_dict(torch.load(full_model_path, map_location=lambda storage, loc: storage))
        output = model(image)
        preds.append(output)
        
    preds = np.array(preds)
    MI, entropy, variance, mean = uncertainty.uncertainty_metrics_classification(preds)
     
    
    
if __name__ == "__main__":
    main()