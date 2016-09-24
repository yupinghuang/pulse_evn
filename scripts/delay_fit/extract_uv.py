import glob
import numpy as np

def extract_uv(filename):
    print filename
    stations = {'Ef':[],'Jb':[], 'Mc':[], 'Wb':[]}
    curr = ''
    with open(filename,'r') as f:
        for line in f:
            s = line.split()
            if s[0]=='Station':
                if s[1] in stations:
                    # set current station to the one read
                    curr = s[1]
                else:
                    # not the station I want
                    curr = ''
            elif (s[0]=='u' and curr!=''):
                # read data from a station
                u = float(s[2].rstrip(','))
                v = float(s[5].rstrip(','))
                stations[curr].append([u,v])

        for s in stations:
            print np.mean(stations[s],axis=0)
        result = [np.mean(stations[sta],axis=0) for sta in ['Ef','Jb','Mc','Wb']] 
        return result

                

if __name__=='__main__':
    filelist = glob.glob('/jop87_2/scratch/huang/ep100/recal/single_pulse2/delay_fit/uvw/*')
    filelist.sort()
    print filelist
    ant_no = [1,3,4,7]
    with open('uv.txt','w') as out:
        out.write('# pulse.no station u(m) v(m)\n')
        out.write('# then edit out pulses we have no data and copy the cols over\n')
        n_pulse = 0
        for ind in range(len(filelist)):
            n_pulse += 1
            result = extract_uv(filelist[ind])
            for i in range(len(result)):
                out.write(str(n_pulse)+' ')
                out.write(str(ant_no[i])+' ')
                out.write(str(result[i][0])+' '+str(result[i][1])+'\n')
             
