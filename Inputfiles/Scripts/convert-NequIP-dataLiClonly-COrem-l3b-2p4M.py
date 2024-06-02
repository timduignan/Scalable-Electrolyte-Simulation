
#!/usr/bin/env python
import numpy as np
import scipy as scipy
import os 
import matplotlib.pyplot as plt

nframes=24000
natoms=48

def readinput(inputlocation): #funtion to read an input file at given location and spit back out an arry of all of the coordinates/forces. assumes two header lines and atomtype specification before xyz coords.
    with open(inputlocation,'r') as waterstrucfile:
        data = np.zeros([nframes, natoms, 3], dtype="float64")
        for i in range(0,nframes):
            waterstrucfile.readline()
            waterstrucfile.readline()
            for j in range(0,natoms):
                line = waterstrucfile.readline().split()
                data[i][j]=np.array(line[1:4])
    return data

def readinputfrc(inputlocation): #funtion to read an input file at given location and spit back out an arry of all of the coordinates/forces. assumes two header lines and atomtype specification before xyz coords.
    with open(inputlocation,'r') as waterstrucfile:
        data = np.zeros([nframes, natoms, 3], dtype="float64")
        for i in range(0,nframes):
            waterstrucfile.readline()
            waterstrucfile.readline()
            waterstrucfile.readline()
            waterstrucfile.readline()
            for j in range(0,natoms):
                line = waterstrucfile.readline().split()
                data[i][j]=np.array(line[3:6])
            waterstrucfile.readline()
    return data


def readinputlmps(inputlocation): #funtion to read an input file at given location and spit back out an arry of all of the coordinates/forces. assumes two header lines and atomtype specification before xyz coords.
    with open(inputlocation,'r') as waterstrucfile:
        data = np.zeros([nframes, natoms, 3], dtype="float64")
        for i in range(0,nframes):
            for j in range(0,9):
                waterstrucfile.readline()
            for j in range(0,natoms):
                line = waterstrucfile.readline().split()
                data[i][j]=np.array(line[2:5])
    return data

def readinputlist(inputlocation): #funtion to read an input file at given location and spit back out an arry of all of the coordinates/forces. assumes two header lines and atomtype specification before xyz coords.
    with open(inputlocation,'r') as waterstrucfile:
        data = np.zeros([nframes], dtype="float64")
        for i in range(0,nframes):
                data[i]=float(waterstrucfile.readline())
    return data

def main():
    energyout = open("/scratch/tn51/ttd110/nequip-data/training/dataLiClonly-COrem-l3b-2p4M/energy.raw", "w")
    coordout = open("/scratch/tn51/ttd110/nequip-data/training/dataLiClonly-COrem-l3b-2p4M/coord.raw", "w")
    boxout = open("/scratch/tn51/ttd110/nequip-data/training/dataLiClonly-COrem-l3b-2p4M/box.raw", "w")
    forceout = open("/scratch/tn51/ttd110/nequip-data/training/dataLiClonly-COrem-l3b-2p4M/force.raw", "w")

    coord= readinputlmps("/scratch/tn51/ttd110/nequip-data/lammps_run/l3b-bigbox-2p4M-reftraj-LiClonly/LiClonly-l3b.lammpstrj")
    forceLAMMPS = readinputlmps("/scratch/tn51/ttd110/nequip-data/lammps_run/l3b-bigbox-2p4M-reftraj-LiClonly/LiClonly-l3b-frc.lammpstrj")
    energyLAMMPS=readinputlist("/scratch/tn51/ttd110/nequip-data/lammps_run/l3b-bigbox-2p4M-reftraj-LiClonly/energy.dat")
    
    autoev=27.211386245988
    kcaltoev=0.0433641078686
    bohrrad= 0.5291772108

    for i in range(0,nframes):
        print("---"+str(i))
        energyout.write(str(energyLAMMPS[i])+"\n")
        boxout.write("25.26 0.0 0.0 0.0 25.26  0.0 0.0 0.0 25.26 \n")
        for j in range(natoms):
            coordout.write(str(coord[i][j][0])+" "+str(coord[i][j][1])+" "+str(coord[i][j][2])+" ")
            force=forceLAMMPS[i][j]
            forceout.write(str(force[0])+" "+str(force[1])+" "+str(force[2])+" ")
        coordout.write("\n")
        forceout.write("\n")
 
main()
                
