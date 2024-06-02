#!/usr/bin/env python
import numpy as np
import scipy as scipy
import os 
import matplotlib.pyplot as plt

nframes=523
natoms=248

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
    energyout = open("/scratch/tn51/ttd110/nequip-data/training/dataLiBr-lb3/energy.raw", "w")
    coordout = open("/scratch/tn51/ttd110/nequip-data/training/dataLiBr-lb3/coord.raw", "w")
    boxout = open("/scratch/tn51/ttd110/nequip-data/training/dataLiBr-lb3/box.raw", "w")
    forceout = open("/scratch/tn51/ttd110/nequip-data/training/dataLiBr-lb3/force.raw", "w")
    cellout =  open("/scratch/tn51/ttd110/nequip-data/training/dataLiBr-lb3/cell.raw", "w")
    pbcout = open("/scratch/tn51/ttd110/nequip-data/training/dataLiBr-lb3/pbc.raw", "w")

    coord= readinput("/scratch/tn51/ttd110/CP2K/LiBr-2p4M-R2SCAN/LiBr-2p4M-DCR2SCAN-reftraj/LiBr-DCR2SCAN-reftraj-pos-1-full.xyz")
    forceCP2K = readinputfrc("/scratch/tn51/ttd110/CP2K/LiBr-2p4M-R2SCAN/LiBr-2p4M-DCR2SCAN-reftraj/LiBr-DCSR2CAN-reftrajforces-full.xyz")
    energyCP2K=readinputlist("/scratch/tn51/ttd110/CP2K/LiBr-2p4M-R2SCAN/LiBr-2p4M-DCR2SCAN-reftraj/energy-full.dat")
    COforceLAMMPS = readinputlmps("/scratch/tn51/ttd110/LAMMPS/LiBr-2p4M-DCR2SCAN-COrerun/full/lowD/LiBr-R2SCAN-COalt-frc.lammpstrj")
    COenergylammps=readinputlist("/scratch/tn51/ttd110/LAMMPS/LiBr-2p4M-DCR2SCAN-COrerun/full/lowD/energy.dat")
    autoev=27.211386245988
    kcaltoev=0.0433641078686
    bohrrad= 0.5291772108

    for i in range(0,nframes):
        print("---"+str(i))
        boxout.write("13.7 0.0 0.0 0.0 13.7  0.0 0.0 0.0 13.7 \n")
        print(str(energyCP2K[i])+"\n")
        energyout.write(str(energyCP2K[i]*autoev-COenergylammps[i])+"\n")
        for j in range(natoms):
            coordout.write(str(coord[i][j][0])+" "+str(coord[i][j][1])+" "+str(coord[i][j][2])+" ")
            force=forceCP2K[i][j]*autoev/bohrrad-COforceLAMMPS[i][j]
            forceout.write(str(force[0])+" "+str(force[1])+" "+str(force[2])+" ")
        coordout.write("\n")
        forceout.write("\n")

    cellout.write("13.7 0.0 0.0 \n 0 13.7 0 \n 0 0 13.7 \n")
    pbcout.write("1 1 1")
    
 
main()
                
