#!/usr/bin/env python3

use_gpu=True
batch_size=8
workers=12

import argparse
import rassp
from rassp import netutil
from rdkit import Chem
import numpy as np
import matchms
matchms.set_matchms_logger_level("ERROR")

from rassp import msutil,model
import sys
sys.modules['msutil'] = msutil
sys.modules['model'] = model


p = argparse.ArgumentParser()
p.add_argument('-m','--model')
p.add_argument('-e','--meta')
p.add_argument('-s','--smiles')
p.add_argument('-o','--output')

a = p.parse_args()

predictor = netutil.PredModel(
    a.meta,
    a.model,
    USE_CUDA=use_gpu,
    data_parallel=False,
)

with open(a.smiles) as sf:
	smiles = sf.read().splitlines()

mols = [ Chem.AddHs(Chem.MolFromSmiles(s)) for s in smiles]
assert len(mols) == len(smiles)

pred = predictor.pred(
    mols,
    progress_bar=False,
    normalize_pred=True,
    output_hist_bins=True,
    batch_size=batch_size, # XXX
    dataloader_config={
        'pin_memory': False,
        'num_workers': workers, # XXX
        'persistent_workers': False,
    },
    benchmark_dataloader=False,
)['pred_binned']

assert len(pred) == len(smiles)

def to_matchms_spec(s,m):
    return matchms.Spectrum(mz=s[:,0].astype(float),intensities=s[:,1].astype(float),metadata={'id':m,'Compound Name':m,'SMILES':m})

matchms.exporting.save_as_msp([to_matchms_spec(s,smiles[i]) for i,s in enumerate(pred)],a.output)
