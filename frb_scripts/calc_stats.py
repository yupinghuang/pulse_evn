import numpy as np
from functools import partial
import glob
from astropy.io import fits
from astropy import units
import multiprocessing
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
from scipy import stats

def calc_sum_shift_peak(fn):
    print 'summing ',fn
    f = fits.open(fn)
    dat = f[0].data.flatten()
    xshift = deg_to_mas(f[0].header['xshift'])
    yshift = deg_to_mas(f[0].header['yshift'])
    dat.sort()
    length = dat.size
    mid80dat = dat[int(round(length*0.1)):int(round(length*0.9))+1]
    count = mid80dat.size
    sums = np.sum(mid80dat)
    peak = np.max(dat)
    return sums, count, xshift, yshift,peak

def calc_mean(sums, count):
    return sums/count

def calc_difsqr(fn,mean):
    print 'squaring ',fn
    f = fits.open(fn)
    dat = f[0].data.flatten()
    dat.sort()
    length = dat.size
    mid80dat = dat[int(round(length*0.1)):int(round(length*0.9))+1]
    count = mid80dat.size
    difsqr = np.sum(np.square(mid80dat-mean))
    return difsqr, count

def deg_to_mas(deg):
    deg = deg * units.deg
    return deg.to(units.mas).value

"""
imsize in pixels
pixelsize in mas
"""
def get_imsize_pixelsize(fn):
    imsize = [0,0]
    pixelsize =[0.,0.]
    with fits.open(fn) as f:
        imsize[0] = abs(f[0].header['NAXIS1'])
        imsize[1] = abs(f[0].header['NAXIS2'])
        pixelsize[0] = abs(deg_to_mas(f[0].header['CDELT1']))
        pixelsize[1] = abs(deg_to_mas(f[0].header['CDELT2']))
        imsize = np.multiply(imsize, pixelsize)
    return imsize, pixelsize

    
def plot_diagnostics(xshift, yshift, indicator, imsizemas, pixelsize):
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal')
    ax.set_axis_bgcolor('gray')
    ax.set_xlim([np.min(xshift)-imsizemas[0],np.max(xshift)+imsizemas[0]])
    ax.set_ylim([np.min(yshift)-imsizemas[1], np.max(yshift)+imsizemas[1]])
    # cmap = plt.cm.YlOrRd_r
    patches =[]
    for x,y,s in zip(xshift,yshift,indicator):
        patches.append(Rectangle(xy=(x-0.5*imsizemas[0],y-0.5*imsizemas[1]),
             width = imsizemas[0], height=imsizemas[1]))
    # cbar = fig.colorbar(ax ,orientation='horizontal')
    p = PatchCollection(patches, cmap=plt.cm.hot)
    p.set_array(indicator)
    # plt.colorbar()
    ax.add_collection(p)
    plt.colorbar(p)
    plt.show()

def max_snr(files):
    pool = multiprocessing.Pool(processes=9)
    results = np.array(pool.map(calc_sum_shift_peak,files))
    sums_and_count = np.sum(results[:,:2],axis=0)
    sums = sums_and_count[0]
    count = sums_and_count[1]
    xshift = results[:,2]
    yshift = results[:,3]
    peak = results[:,4]

    mean = calc_mean(sums,count)
    print 'sums ',sums,' count ', count
    # second pass: get the (unbiased) rms
    count = 0
    partial_calc_difsqr = partial(calc_difsqr,mean=mean)
    results = np.array(pool.map(partial_calc_difsqr,files))
    difsqr_and_count  = np.sum(results,axis=0)
    difsqr = difsqr_and_count[0]
    count = difsqr_and_count[1]
    rms  = np.sqrt(difsqr/(count-1))
    snr = np.divide((peak-mean),rms)
    print 'rms ',rms
    return snr, xshift, yshift

""" shapiro-wilks test for gaussianity
"""
def shapiro_wilks(fn):
    print 'calculcating shapiro-wilks test for ',fn
    f = fits.open(fn)
    dat = f[0].data.flatten()
    xshift = deg_to_mas(f[0].header['xshift'])
    yshift = deg_to_mas(f[0].header['yshift'])
    w, pval = stats.shapiro(dat)
    return w ,xshift, yshift

def gaussianity_test(files):
    pool = multiprocessing.Pool(processes=5)
    results = np.array(pool.map(shapiro_wilks, files))
    wstats = results[:,0]
    xshift = results[:,1]
    yshift = results [:,2]
    return wstats, xshift, yshift


def main():
    files = glob.glob('/home/huang/data/images/p0beam/*fits')
    # get the ra and dec shift of each plot in one pass and prep for simple stats
    imsizemas, pixelsize = get_imsize_pixelsize(files[0])
    # now imsize is in mas
    indicator, xshift, yshift = max_snr(files)
    plot_diagnostics(xshift, yshift, indicator, imsizemas, pixelsize)
    """
    plt.scatter(xshift,yshift,c=snr,cmap=plt.cm.YlOrRd_r)
    plt.xlabel('RA shift (mas)')
    plt.ylabel('DEC shift(mas)')
    plt.colorbar()
    """
if __name__=="__main__":
    main()
