import numpy as np
import matplotlib.pylab as plt
from AIPS import AIPS
from AIPSTask import AIPSTask, AIPSList
from Wizardry.AIPSData import AIPSImage as WAIPSImage
from AIPSData import AIPSImage
from scipy import stats

""" take the facted images and compute statistics
"""
AIPS.userno = 669

"""given an image no, compute its mean and std of mid-80%
plot histogram and overplot corresponding gaussian curve
"""
def plot_gauss(no):
    seq = 1
    if no==1:
        n = str(no)
        n = n.zfill(3)
        imtype ='IIM'+n
    elif no<1000:
        n = str(no)
        n = n.zfill(3)
        imtype = 'IIM'+n
    else:
        imtype = 'II'+str(no)

    print 'doing '+imtype
    testImg = WAIPSImage('J0528+2200', imtype, 1, seq,43)
    dat = testImg.pixels.flatten()
    end_1, end_2 = np.array([dat.size*0.1,dat.size*0.9],dtype=int)
    mu=np.mean(dat[end_1:end_2])
    sigma=stats.tstd(dat[end_1:end_2])
    peak = np.max(dat)
    print 'peak:', np.max(dat), 'rms: ', sigma, 'snr: ', peak/sigma
    plt.figure()
    n,bins,patches = plt.hist(dat,100,normed=1,histtype='stepfilled')
    plt.setp(patches,'facecolor','g','alpha',0.75)
    y = plt.normpdf(bins,mu,sigma)
    plt.plot(bins,y,'k--',linewidth=1.5)
    plt.show()
""" 
"""
def has_source(image):
    pass

def get_fits(no):
    seq = 1
    if no<1000:
        n = str(no)
        n = n.zfill(3)
        imtype = 'IIM'+n
    else:
        imtype = 'II'+str(no)
    dat = AIPSImage('J0528+2200',imtype,1,seq)
    if not dat.exists():
        print imtype+' failed!!!!'
    fittp = AIPSTask('FITTP')
    fittp.indata = dat
    fittp.dataout = '/jop87_2/scratch/huang/rp024c/grid_trial/p0beam/beam'+str(no)+'.fits'
    fittp.go()

def show_hist():
    samples = np.random.randint(9,4097,6)
    plot_gauss(1)
    for s in samples:
        plot_gauss(s)

if __name__=='__main__':
    for i in range(4096):
        j = i+1
        get_fits(j)
