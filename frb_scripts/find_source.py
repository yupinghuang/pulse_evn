import numpy as np
# read a fits file

# parallel compute statistics and record peak stuff

def compute_stats(data_chunk):
    chunkcount = data_chunk.size
    chunksum = np.sum(data_chunk)
    chunksqrsum = np.sum(np.sqr(data_chunk))

