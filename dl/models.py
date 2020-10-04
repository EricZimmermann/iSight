import torch
from torch import nn

class BasicCNN(nn.Module):
    def __init__(self, channel_sizes, layers, batch_norm, dropout, num_classes):
        super(BasicCNN, self).__init__()
        
        modules = []
        
        for block_idx in range(0, len(channel_sizes) -1):
            modules.append(nn.Conv2d(channel_sizes[block_idx], channel_sizes[block_idx+1], 3, padding=1))
            modules.append(nn.ReLU(True))
            if batch_norm:
                modules.append(nn.BatchNorm2d(channel_sizes[block_idx+1]))
            if dropout is not None:
                modules.append(nn.Dropout2d(dropout, inplace=False))
                
            if layers > 1:
                for layer in range(layers - 1):
                    modules.append(nn.Conv2d(channel_sizes[block_idx+1], channel_sizes[block_idx+1], 3, padding=1))
                    modules.append(nn.ReLU(True))
                    if batch_norm:
                        modules.append(nn.BatchNorm2d(channel_sizes[block_idx+1]))
                    if dropout is not None:
                        modules.append(nn.Dropout2d(dropout, inplace=False))
            
            if block_idx + 1  != len(channel_sizes) - 1:
                modules.append(nn.MaxPool2d(2,2))
        
        self.cnn_core = nn.Sequential(*modules)
        self.gap = nn.AdaptiveAvgPool2d(1)
        self.linear = nn.Linear(channel_sizes[-1], num_classes)
            
    def forward(self, x):
        x = self.cnn_core(x)
        x = self.gap(x)
        x = x.view(x.size(0), -1)
        x = self.linear(x)
        return x