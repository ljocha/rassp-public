#!/bin/bash

chunk=$1
dir=/storage/brno3-cerit/home/ljocha/work/Recetox/rassp-public
smiles=$dir/$chunk
model=$dir/small.80261075.00001800.model
meta=$dir/small.80261075.meta

cp $smiles $model $meta $dir/predict.py $dir/predict-singularity.sh $SCRATCHDIR

cd $SCRATCHDIR || exit 1

mv $chunk ${chunk}_

split -n -l 1000 ${chunk}_
rm ${chunk}_

for c in ${chunk}_*; do
	./predict-singularity -m $(basename $model} -e $(basename $meta) -s $c -o $c.msp
	cp $c.msp $dir
done




