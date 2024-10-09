#!/usr/bin/env python3

#RASSP='/storage/brno12-cerit/home/ljocha/work/Recetox/rassp-public'
RASSP='.'

import sys
sys.path.insert(0,RASSP+'/rassp')

import os
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:512"
# os.environ["OMP_NUM_THREADS"] = "12"

import torch

import yaml
import time

from forward_train import train as rassp_train

with open(RASSP+'/rassp/expconfig/demo.yaml') as cf:
    exp_config = yaml.load(cf,Loader=yaml.FullLoader)

exp_config['max_epochs'] = 3000
exp_config['epoch_size'] = 4096
exp_config['seed'] = int(time.time())
exp_config['batch_size'] = 8
exp_config['checkpoint_every_n_epochs'] = 1
exp_config['attempt_load_recent_checkpoint'] = True
exp_config['validate_every'] = 10
exp_config['cluster_config']['data_dir'] = '.'
exp_config['DATALOADER_NUM_WORKERS'] = 8
exp_config['exp_data']['data'][0]['db_filename'] = 'train-rassp-small.pq'
exp_config['exp_data']['data'][1]['db_filename'] = 'valid-rassp-small.pq'

#abiff

os.environ["OMP_NUM_THREADS"] = "6"
exp_config['batch_size'] = 8


with open('exp.yml','w') as y:
    yaml.dump(exp_config,y)

rassp_train('small',exp_config,exp_config_filename='exp.yml',USE_CUDA=True)
