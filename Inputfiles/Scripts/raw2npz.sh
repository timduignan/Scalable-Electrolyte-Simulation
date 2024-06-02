#!/bin/bash

module load python3/3.9.2


#cp ../dataKCl-chargeonlyalt-R2SCAN-2p4M-lowdiel/pbc.raw ./
#cp ../dataKCl-chargeonlyalt-R2SCAN-2p4M-lowdiel/cell.raw ./
#cp ../dataKCl-chargeonlyalt-R2SCAN-2p4M-lowdiel/z.raw ./



nline_per_set=`cat coord.raw | wc -l`


if test $# -ge 1; then
    nline_per_set=$1
fi

echo nframe is `cat coord.raw | wc -l`
echo nline per set is $nline_per_set
export nline=$nline_per_set

split coord.raw	 -l $nline_per_set -d -a 3 coord.raw
test -f energy.raw && split energy.raw -l $nline_per_set -d -a 3 energy.raw
test -f force.raw  && split force.raw  -l $nline_per_set -d -a 3 force.raw
test -f virial.raw && split virial.raw -l $nline_per_set -d -a 3 virial.raw
test -f atom_ener.raw && split atom_ener.raw -l $nline_per_set -d -a 3 atom_ener.raw
test -f fparam.raw && split fparam.raw -l $nline_per_set -d -a 3 fparam.raw

nset=`ls | grep coord.raw[0-9] | wc -l`
nset_1=$(($nset-1))
echo will make $nset sets


for ii in `seq 0 $nset_1`
do
  echo making set $ii ...
  pi=`printf %03d $ii`
  mkdir set.$pi
  mv coord.raw$pi	set.$pi/coord.raw
  test -f energy.raw$pi && mv energy.raw$pi set.$pi/energy.raw
  test -f force.raw$pi  && mv force.raw$pi  set.$pi/force.raw
  test -f virial.raw$pi && mv virial.raw$pi set.$pi/virial.raw
  test -f atom_ener.raw$pi && mv atom_ener.raw$pi set.$pi/atom_ener.raw
  test -f fparam.raw$pi && mv fparam.raw$pi set.$pi/fparam.raw

  cd set.$pi
  if [ $ii -eq 0 ]
     then
  python3 -c 'import numpy as np; import os; data = np.loadtxt("coord.raw" , ndmin = 2); data = data.astype (np.float32); data = data.reshape(int(os.environ["nline"]),data.shape[1]//3,3); np.save ("R",  data)'
  python3 -c \
'import numpy as np; import os.path; 
if os.path.isfile("energy.raw"): 
   data = np.loadtxt("energy.raw"); 
   data = data.astype (np.float32); 
   data = data.reshape(int(os.environ["nline"]),1);
   np.save ("E", data)
'
  python3 -c \
'import numpy as np; import os; 
if os.path.isfile("force.raw" ): 
   data = np.loadtxt("force.raw", ndmin = 2); 
   data = data.astype (np.float32);
   data = data.reshape(int(os.environ["nline"]),data.shape[1]//3,3);
   np.save ("F",  data)
'
  python3 -c \
'import numpy as np; import os.path; 
if os.path.isfile("virial.raw"): 
   data = np.loadtxt("virial.raw", ndmin = 2); 
   data = data.astype (np.float32); 
   np.save ("virial", data)
'
  python3 -c \
'import numpy as np; import os.path; 
if os.path.isfile("atom_ener.raw"): 
   data = np.loadtxt("atom_ener.raw", ndmin = 2); 
   data = data.astype (np.float32); 
   np.save ("atom_ener", data)
'
  python3 -c \
'import numpy as np; import os.path; 
if os.path.isfile("fparam.raw"): 
   data = np.loadtxt("fparam.raw", ndmin = 2); 
   data = data.astype (np.float32); 
   np.save ("fparam", data)
'
  fi
  rm *.raw
  cd ../
done


python3 -c \
'import numpy as np; import os.path; 
data = np.loadtxt("z.raw"   , ndmin = 2); 
data = data.astype (np.int32); 
b = data.flatten();
np.save ("z",  b)'

python3 -c 'import numpy as np; data = np.loadtxt("cell.raw"   , ndmin = 2); data = data.astype (np.float32); np.save ("cell",    data)'
python3 -c 'import numpy as np; data = np.loadtxt("pbc.raw"   , ndmin = 2); data = data.astype (np.int32); b = data.flatten(); np.save ("pbc",    b)'

mv pbc.npy set.000
mv cell.npy set.000
mv z.npy set.000
cd set.000

python3 -c '\
import numpy as np; cell = np.load("cell.npy"); z = np.load("z.npy"); R = np.load("R.npy"); E = np.load("E.npy"); F = np.load("F.npy"); pbc = np.load("pbc.npy");
np.savez("dataLiBr.npz", cell=cell, z=z, R=R, E=E, F=F, pbc=pbc)'

mv dataLiBr.npz ..
cd ..

rm -fr set.*
