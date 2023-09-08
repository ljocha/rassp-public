#!/bin/bash

chunk=$1
dir=/storage/brno3-cerit/home/ljocha/work/Recetox/rassp-public
smiles=$dir/$chunk
model=$dir/small.80261075.00001800.model
meta=$dir/small.80261075.meta

echo cp $smiles $model $meta $dir/predict.py $dir/predict-singularity.sh $SCRATCHDIR
cp $smiles $model $meta $dir/VERSION $dir/predict.py $dir/predict-singularity.sh $SCRATCHDIR

cd $SCRATCHDIR || exit 1


split -d -l 1000 ${chunk} ${chunk}_
rm ${chunk}

for c in ${chunk}_900*; do
	mv $c $(echo $c | sed 's/900\(.\)/9\1/')
done


for c in ${chunk}_*; do
	./predict-singularity.sh -m $(basename $model) -e $(basename $meta) -s $c -o $c.msp
	cp $c.msp $dir
done




