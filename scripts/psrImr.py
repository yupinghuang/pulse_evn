from AIPS import AIPS
from AIPSTask import AIPSTask, AIPSList
from AIPSData import AIPSUVData, AIPSImage
from datetime import date,time,timedelta,datetime
import copy
# pulsar gating duty cycle in seconds
DUTYCYCLE=2.0
AIPS.userno=5
""" class storing start and end time of a given scan
"""
class Scan:
    def __init__(self,startHr,startMin,startSec,endHr,endMin,endSec):
        self.startTime=time(startHr,startMin,startSec)
        self.endTime=time(endHr,endMin,endSec)
        
class Pulsar:
    def __init__(self):
        self.scans=[]
        self.prefix=''
        self.dutyCycle=DUTYCYCLE
        self.allUVData=AIPSUVData('PSRALL','UVDATA',1,2)
        self.__clear(self.allUVData)

    """load the calibrated gated pusar uvdata
    """
    def load_calibrated_obs(self,filename):
        fitld=AIPSTask('FITLD')
        fitld.datain=filename
        fitld.outdata=self.allUVData
        fitld.go()
       #  sanity check
        if not self.allUVData.exists():
            raise ValueError
        #TODO get the start and end time using listr
        ####################################
        # If using this program for other projects need to modify scans here
        ######################################
        print "WARNING: I can't deal with cross-midnight observations"
        self.scans.append(Scan(23,17,33,23,25,29))
        self.scans.append(Scan(23,28,33,23,36,29))
        print "WARNING: startTime and endTime of each scan is HARDWIRED in the program"
        # find the prefix for naming output files
        self.prefix=filename.split('/')[-1]
        self.prefix=self.prefix[:self.prefix.rfind('.')]

    """split the loaded data into multiple files, each containing
    a pulse
    """
    def split_data(self):
        # adding today is just a trick to get time addition with the datetime package to work
        today=date.today()
        partNumber=0
        scanNumber = -1
        for scan in self.scans:
            scanNumber+=1
            endDatetime=datetime.combine(today,scan.endTime)
            sliceStartTime=datetime.combine(today,scan.startTime)
            dt=timedelta(seconds=DUTYCYCLE)
            sliceEndtTime=copy.copy(sliceStartTime)+dt
            while (endDatetime-sliceEndtTime>=timedelta(seconds=DUTYCYCLE)):
                self.__split_and_fittp(sliceStartTime.time(),sliceEndtTime.time(),partNumber,scanNumber)
                sliceStartTime=sliceStartTime+dt
                partNumber+=1
                sliceEndtTime=sliceEndtTime+dt

    """helper function to call SPLIT and FITTP to generate a single-pulse
    UVDATA file from the original datafile
    """
    def __split_and_fittp(self,startTime,endTime,partNumber,scanNumber):
         # temporary UVData to store the split, destroyed in the end
         tempDiskNo=1
         tempSeqNo=3
         tempUVData=AIPSUVData('PSRALL','SPLIT ',tempDiskNo,tempSeqNo)
         self.__clear(tempUVData)

         splitTask=AIPSTask('SPLIT')
         splitTask.indata=self.allUVData
         splitTask.timerang=AIPSList([0,startTime.hour,startTime.minute,startTime.second,
                 0,endTime.hour,endTime.minute,endTime.second])
         splitTask.outdisk=tempDiskNo
         splitTask.outseq=tempSeqNo
         try:
             splitTask.go()
         except RuntimeError:
             print ("!!!!Warning: SPLIT failed at "+startTime.isoformat()+
                     " - "+endTime.isoformat()+" possibly no data")
             
         # if SPLIT is successful, start FITTP
         if tempUVData.exists():
             fittpTask=AIPSTask('FITTP')
             fittpTask.dataout=('/jop87_2/scratch/huang/rp024c/grid_trial/pulses/'
                     +self.prefix+'.PART'+str(partNumber)+'.UVFITS')
             fittpTask.indata=tempUVData
             fittpTask.go()

    """ helper method to make sure that the disk and catalogue number
    is available for the AIPSData initialization
    """
    def __clear(self,aipsDataObject):
        if aipsDataObject.exists():
            aipsDataObject.clrstat()
            aipsDataObject.zap()

def main():
    pass

def test():
    psr=Pulsar()
    psr.load_calibrated_obs('/jop87_2/scratch/huang/rp024c/grid_trial/J0528+2200.PULSE.ALL.UVFITS')
    psr.split_data()

if __name__ == "__main__":
    #main()
    #test()
    print 'duh'


