from AIPS import AIPS
from AIPSTask import AIPSTask, AIPSList
from AIPSData import AIPSUVData, AIPSImage
import multiprocessing
import tempofile,os

AIPS.userno = 43

def get_boxfile():
    pass

def call_imagr(boxfile):
    imagr = AIPSTask('IMAGR')
    ####################
    imagr.boxfile = MEEEP
    imagr.outdisk =1
    imagr.nfield = 1
    imagr.antennas = AIPSList([1,2,3,4,5,6])
    imagr.bchan = 1
    imagr.echan = 32
    imagr.nchav = 32
    imagr.bif = 1
    imagr.eif = 8
    imagr.cellsize = AIPSList([0.0005,0.0005])
    imagr.imsize = AIPSList([4096,4096])
    ########################
    imagr.stokes = 'I'
    imagr.do3dimag = 1
    imagr.niter = 0
    imagr.robust = 0
    imagr.cmethod = 'DFT'
    imagr.dotv = -1
    imagr.outdata = outdat
    imagr.go()

def  

def main():
   """ test cases
   1) one-by-one double harddrives
   2) ten by ten double harddrives
   but really how do I know if a task has finished or not?
   """
"""
parseltongue parallel seems to be a bad choice...subprocess with different disk number?
 ***Assumes that we already have single-pulse calibrated multi-channel uvdata
 """
 
