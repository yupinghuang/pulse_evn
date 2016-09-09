from AIPS import AIPS
from AIPSTask import AIPSTask, AIPSList
from AIPSData import AIPSUVData, AIPSImage
import glob
AIPS.userno=668
merge = False
tasavpath = '/jop87_2/scratch/huang/ep100/recal/ep100.tasav.2.FITS'
def clear(aipsDataObject):
    if aipsDataObject.exists():
        aipsDataObject.clrstat()
        aipsDataObject.zap()


# load the tasav file
tasav = AIPSUVData('ep100','TASAV ',1,1)
clear(tasav)
fitld = AIPSTask('FITLD')
fitld.datain = tasavpath
fitld.outdata = tasav
fitld.go()

# process each file
filenames = glob.glob('/jop87_2/scratch/huang/ep100/recal/ppl_single_pulse2/ep100_scan*.idi')

uvdat = AIPSUVData('PULSE','UVDATA',1,2)
count = 0
for f in filenames:
    # load
    clear(uvdat)
    fitld = AIPSTask('FITLD')
    fitld.datain = f
    fitld.outdata = uvdat
    fitld.digicor = -1
    fitld.go()

    #tacop BP and CL from TASAV to data
    tacop = AIPSTask('TACOP')
    tacop.indata = tasav
    tacop.outdata = uvdat
    tacop.ncount = 1
    tacop.inext = 'CL'
    tacop.invers = 0
    tacop.go()
    tacop.inext = 'BP'
    tacop.invers = 0
    tacop.go()
    tacop.inext = 'FG'
    tacop.invers = 0
    tacop.go()

    # SPLIT to apply the calibs
    if count==0:
        tempDiskNo = 1
        tempSeqNo = 4
    else:
        tempDiskNo = 1
        tempSeqNo = 3 
    splitdat = AIPSUVData('J1819-1458','SPLIT ',tempDiskNo,tempSeqNo)
    clear(splitdat)
    split = AIPSTask('SPLIT')
    split.indata = uvdat
    split.aparm=AIPSList([2,1,0])
    split.outdisk = tempDiskNo
    split.outseq = tempSeqNo
    split.docalib = 1
    split.gainuse = 2
    split.doband = 1
    split.bpver = 1
    split.go()

    if merge:
        # merge data files
        if count>0:
            condat = AIPSUVData('J1819-1458','DBCON ',1,count+4)
            clear(condat)
            if count==1:
                prev_condat = AIPSUVData('J1819-1458','SPLIT ',1,count+3)
            else:
                prev_condat = AIPSUVData('J1819-1458','DBCON ',1,count+3)

            dbcon = AIPSTask('DBCON')
            dbcon.doarray = 1
            dbcon.indata = splitdat
            dbcon.in2data = prev_condat
            dbcon.outdata = condat
            dbcon.go()
        count+=1

    # output the uvfits file
    fittp = AIPSTask('FITTP')
    fittp.dataout = f+'.uvfits'
    fittp.indata = splitdat
    fittp.go()

"""
    infile = 'difmap_command' 
    with open(infile,'w') as cf:
        commands = ['observe ' +f+'.uvfits'+'\n',
                'select\n',
                'mapsize 8192, 0.5\n',
                'device /NULL\n',
                'uvw 0,0\n',
                'mapl\n',
                'print peak(x),peak(y)\n'
                'exit\n']
        cf.write(u''.join(commands))
    output = subprocess.check_output('difmap<'+infile,shell=True)
    pos = output.split('\n')[-3]
    posx,posy,junk = pos.split(' ')
    posx = float(posx)
    posy = float(posy)
    print posx,posy
    """


