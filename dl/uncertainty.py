import numpy as np


def uncertainty_metrics_classification(prd):
    """
    Arguments:
      - prd: post-softmax                                 (mcs, batch_size, num_classes)
    Returns:
      - Entropy: entropy of MC samples across classes                 (batch_size)
      - MI: Mutual Information (bald) of MC samples across classes    (batch_size)
      - variance: Variance of MC samples across classes               (batch_size)
      - mean: Mean of MC samples. DO argmax of this                   (batch_size, num_classes)       
    Refer: https://arxiv.org/pdf/1703.02910.pdf and https://arxiv.org/pdf/1808.01200.pdf for more info about Entropy and MI
    """    
    _EPS = 1e-10
    entropy = -np.sum(np.mean(prd, 0) * np.log2(np.mean(prd, 0) + _EPS), -1)
    expected_entropy = -np.mean(np.sum(prd * np.log2(prd + _EPS), -1), 0)
    MI = entropy - expected_entropy
    variance = np.mean(np.var(prd,0),-1)
    mean = np.mean(prd, 0)
    return MI, entropy, variance, mean 