import torch.nn as nn
import torch.backends.cudnn as cudnn
import torch
import torch.nn.functional as F
import torchvision
import os
import numpy as np
from skimage import io
from skimage.transform import resize
rejected_models = [1,3]
var_tresholding = [0.0113876,  0.015099, 0.01973732, 0.00275105, 0.02780673, 0.02693587, 0.00160483]
inverse_mapping = {0:"Bowen's Disease", 
                   1:"Basal Cell Carcinoma", 
                   2:'Benign Keratosis-like Lesions', 
                   3:'Dermatofibroma', 
                   4:'Melanoma', 
                   5:'Melanocytic Nevi', 
                   6:'Vascular Lesions'} 

def infer(img_path, ensemble_path):
    
    img = io.imread(img_path).astype(np.float32)
    img = resize(img, (225,300,3)).transpose(2,0,1) / 255.0
    img = torch.tensor(img).unsqueeze(0).to('cpu')
        
    # prep model
    model = torchvision.models.resnet18(pretrained=False).to('cpu')
    in_ftr  = model.fc.in_features
    model.fc = nn.Linear(in_ftr, 7, bias=True)
    n_model_paths = [path for idx, path in enumerate(sorted(os.listdir(ensemble_path))) if idx not in rejected_models]
    
    # load models and perform inference
    preds = []
    for model_pth in n_model_paths:
        full_model_path = os.path.join(ensemble_path, model_pth)
        model.load_state_dict(torch.load(full_model_path, map_location='cpu'))
        model.eval()
        output = F.softmax(model(img), dim=1)
        preds.append(output.detach().numpy())

    mean_preds = np.mean(preds, axis=0)[0]
    variance = np.var(preds, axis=0)[0]
    
    arg = np.argmax(mean_preds)
    results = {'disease' : inverse_mapping[arg],
               'prob' : mean_preds[arg],
               'conf' : None}
               
    
    if variance[arg] > var_tresholding[arg]*0.85:
        results['conf'] = False
    else:
        results['conf'] = True

    return results