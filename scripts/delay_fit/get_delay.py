from AIPS import AIPS
from AIPSData import AIPSUVData
from Wizardry.AIPSData import AIPSUVData as WAIPSUVData

AIPS.userno = 100

if __name__=='__main__':
    data = WAIPSUVData('MULTI', 'MSORT ',1,1)
    sntable = data.table('SN',1)
    n=0
    with open('delay.txt','w') as f:
        f.write('# pulse antenna delay(s) weight\n')
        for item in sntable:
            if item['antenna_no']==1:
                # next pulse
                n+=1
            if item['antenna_no'] in [1,3,4,7]:
                delay = item['delay_1'][0]
                weight = item['weight_1'][0]
                if not(delay>1 or delay==0.):
                    f.write(str(n)+' '+' '+str(item['antenna_no'])+' '+str(delay)+' '+str(weight)+'\n')

