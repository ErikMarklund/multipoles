#!/bin/zsh

N=10000
minat=2
maxat=8
l_max=5

log=testac_natoms.log

echo "# Rnning test_accuracy.py with and without imaginary parts." | tee $log
echo "# N=${N}  minat=maxat=${minat}--${maxat}  l_max=${l_max}" | tee -a $log

current=$(git branch | grep "^*" | awk '{print $2}')

echo "======== complex ========" | tee -a $log
if [[ $current != "complex" ]]; then
    git checkout complex -q
fi

for i in $(seq $minat $maxat); do
    echo "--- $i atoms ---" | tee -a $log
    ./test_accuracy.py $N $i $i $l_max | tee -a $log
done


echo "======== real ========" | tee -a $log
git checkout master -q

for i in $(seq $minat $maxat); do
    echo "--- $i atoms ---" | tee -a $log
    ./test_accuracy.py $N $i $i $l_max | tee -a $log
done

git checkout $current -q
