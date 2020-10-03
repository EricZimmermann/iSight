from skimage import io
from skimage.transform import rescale
import numpy as np
import torch
import torchvision
from torch.utils.data import Dataset

def generateExperiment(data_file, n_cls):
    
    '''
        default 80/10/10 splitting
    '''
    
    # prep experiment with class balance in mind
    experiment = {cls : {'train' : {}, 'validation' : {}} for cls in range(n_cls)}
    experiment['test'] = {}
    
    # split by cls
    bin_cls = [[] for cls in range(n_cls)]
    for ID in data_file.keys():
        label = data_file[ID]['label']
        bin_cls[label].append(ID)
    
    
    # split
    for cls in range(n_cls):
        np.random.shuffle(bin_cls[cls])
        split_point = len(bin_cls[cls]) // 10
        experiment[cls]['train'] = {ID: data_file[ID] for ID in bin_cls[cls][: 8*split_point]}
        experiment[cls]['validation'] = {ID: data_file[ID] for ID in bin_cls[cls][8*split_point:9*split_point]}
        for ID in bin_cls[cls][9*split_point:]:
            experiment['test'][ID] = data_file[ID] 
        
    return experiment

class Transformer():
    def __init__(self):
        self.transformation = []
    
    def add(self, txf):
        self.transformation.append(txf)
        
    def transforms(self):
        return torchvision.transforms.Compose(self.transformations)
    
class Oversampler(Dataset):
    def __init__(self, datasets):
        self.datasets = datasets
        self.max_len = len(max(datasets, key=len))
        self.length = len(datasets) * self.max_len

    def __len__(self):
        return self.length

    def __getitem__(self, idx):
        select, index = divmod(idx, self.max_len)
        if len(self.datasets[select]) <= index: 
            index = int(np.random.random()*len(self.datasets[select])) % len(self.datasets[select])
        return self.datasets[select][index]
    
    
class SkinSet(Dataset):
    def __init__(self, data, transforms=None):
        self.data = data
        self.IDs = list(data.keys())
        self.length = len(self.IDs)
        self.transforms = transforms
        
    def __len__(self):
        return self.length
    
    def __getitem__(self, idx):
        patient = self.data[self.IDs[idx]]
        image = np.load(patient['image'])
        label = patient['label']
        
        if self.transforms is not None:
            image = self.transforms(image)
            
        return image, label
        