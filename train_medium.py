#!/usr/bin/env python3

import os
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:512"
os.environ["OMP_NUM_THREADS"] = "12"

import torch


import time
import yaml
import pandas as pd
from rdkit import Chem

valid_atoms = {1, 5, 6, 7, 8, 9, 14, 15, 16, 17, 35, 53}
#valid_atoms = {1, 6, 7, 8, 9, 15, 16, 17}
num_peaks_per_formula = 12
#max_formulae = 100000
#max_formulae = 4096
max_formulae = 16384

with open('rassp/expconfig/demo.yaml') as cf:
    exp_config = yaml.load(cf,Loader=yaml.FullLoader)

exp_config['max_epochs'] = 3000
exp_config['epoch_size'] = 4096
exp_config['seed'] = int(time.time())
exp_config['batch_size'] = 2
exp_config['checkpoint_every_n_epochs'] = 1
exp_config['attempt_load_recent_checkpoint'] = True
exp_config['validate_every'] = 10
exp_config['cluster_config']['data_dir'] = '.'
exp_config['DATALOADER_NUM_WORKERS'] = 2

exp_config['featurize_config']['explicit_formulae_config']['max_formulae'] = max_formulae
exp_config['featurize_config']['element_oh']=list(valid_atoms)
exp_config['featurize_config']['explicit_formulae_config']['formula_possible_atomicno'] = list(valid_atoms)
exp_config['net_params']['spect_out_config']['formula_oh_sizes'] = [50, 46, 30, 30, 30, 30, 30, 30, 20, 20, 16, 8] # XXX: guess



exp_config['exp_data']['data'][0]['db_filename'] = 'mediumtrain.pq'
exp_config['exp_data']['data'][1]['db_filename'] = 'mediumtest.pq'

with open('exp.yml','w') as y:
    yaml.dump(exp_config,y)


import sys
sys.path.append('./rassp')
from forward_train import train as rassp_train

rassp_train('medium',exp_config,exp_config_filename='exp.yml',USE_CUDA=True)
