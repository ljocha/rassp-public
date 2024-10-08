#!/usr/bin/env python3

import yaml
import sys
import json
import pandas as pd
import numpy as np
from rdkit import Chem
from rassp.msutil.masscompute import FragmentFormulaPeakEnumerator

#valid_atoms = {1, 5, 6, 7, 8, 9, 14, 15, 16, 17, 35, 53}
valid_atoms = {1, 6, 7, 8, 9, 15, 16, 17}
num_peaks_per_formula = 12
#max_formulae = 100000
max_formulae = 4096
max_atoms = 48

ffe = FragmentFormulaPeakEnumerator(sorted(valid_atoms), use_highres=True, max_peak_num=num_peaks_per_formula)

if len(sys.argv) != 3:
	raise ValueError(f"usage: {sys.argv[0]} input.jsonl output.pq\n")

def goodmol(mol):
        if len(mol.GetAtoms()) > max_atoms:
            return False
        
        atoms = { a.GetAtomicNum() for a in mol.GetAtoms() }
        if not atoms < valid_atoms:
            return False
            
        f,m = ffe.get_frag_formulae(mol)
        if len(f) > max_formulae:
            return False

        return True

smi = []
mol = []
spec = []

with open(sys.argv[1]) as inp:
	for l in inp:
		j = json.loads(l)
		smi1 = j['smiles']
		spec1 = np.array( [ np.array([ mz, i ]) for mz,i in zip(j['mz'],j['intensity']) ] + [ np.array([0]) ],dtype=object )[:-1]
		mol1 = Chem.AddHs(Chem.MolFromSmiles(smi1))

		if goodmol(mol1):
			smi.append(smi1)
			mol.append(mol1.ToBinary())
			spec.append(spec1)


#print(spec[0])
df = pd.DataFrame({ 'rdmol' : mol, 'spect' : spec, 'smiles' : smi })
df.to_parquet(sys.argv[2])
	



