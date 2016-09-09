import glob
import numpy as np
import subprocess
import tempfile
import os
import multiprocessing, Queue

def work(infile):
    print 'start '+infile
    with open(infile,'r') as uvfitsfile:
        commands = ['observe ' + infile+'\n',
                'select\n',
                'mapsize 8192, 0.5\n',
                'device /NULL\n',
                'mapl\n',
                'print "peak1::", peak(flux,max)\n',
                'print "rms1::", imstat(rms)\n',
                'clean 50,0.05\n',
                'mapl\n',
                'print "rms3::", imstat(rms)\n',
                'mapl clean\n',
                'print "peak2::", peak(flux,max)\n',
                'print "rms2::",imstat(rms)\n',
                'print "pos::",peak(x),peak(y)\n',
                'exit\n']

        with tempfile.NamedTemporaryFile(mode='w',delete=True) as tmp:
            tmp.write(u''.join(commands))
            tmp.flush()
            os.fsync(tmp.fileno())
            output = subprocess.check_output('difmap<'+tmp.name,shell=True)
        split_output = output.split('\n')
        # create output row: peakx,peaky,peakflux(Jy),rms(Jy), snr
        result_row=np.empty(5)
        # cheap hack to check if the run is succefully
        if split_output[-1]=='' and ('closed' in split_output[-2]):
            # glean information from the text output
            result_row[0] = float(split_output[-3].split(' ')[1])
            result_row[1] = float(split_output[-3].split(' ')[2])
            # result_row[3] = float(split_output[-4].split(' ')[1])
            result_row[3] = float(split_output[-9].split(' ')[1])
            result_row[2] = float(split_output[-5].split(' ')[1])
            result_row[4] = result_row[2]/result_row[3]
        else:
            print infile
            print output
            result_row[4] = 1e-2
    filename = infile.split('/')[-1]
    return (result_row, filename)

def main():
    file_list = glob.glob('J0528+2200.PULSE.ALL*UVFITS')
    pool = multiprocessing.Pool()
    result = pool.map(work,file_list)
    with open('J0528+2200pos.dat','w') as outfile:
        outfile.write('# Peakx(mas), peaky(mas), peakflux, rms, snr\n')
        for row in result:
            string_rep=np.array_str(row[0],precision=5)
            filename = row[1]
            outfile.write(string_rep[2:-2]+' '+filename+'\n')

def test():
    file_list = glob.glob('J0528+2200.PULSE.ALL*UVFITS')
    result = []
    for fn in file_list:
        result.append(work(fn))
    with open('J0528+2200pos.dat','w') as outfile:
        outfile.write('# Peakx(mas), peaky(mas), peakflux, rms, snr\n')
        for row in result:
            string_rep=np.array_str(row[0],precision=5)
            filename = row[1]
            outfile.write(string_rep[2:-2]+' '+filename+'\n')
if __name__=='__main__':
    main()
    #test()
