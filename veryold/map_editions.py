import numpy as np
import pandas
from pylab import *
from matplotlib import pyplot
import scipy.ndimage
import io
import subprocess
import commands

def capiselect2df( capiselect ):
    cmd    = 'lscapi -csv ' + capiselect
    stdout = commands.getoutput(cmd)
    csv    = io.StringIO(unicode(stdout,'utf-8'))
    # pandas dataframe
    df = pandas.read_csv(csv, sep=',', skiprows=0, na_values = ['nan','NaN'] ) 
    return df



def df2map(df, attrX, attrY, attrValues):
    attrX      = attrX.upper()
    attrY      = attrY.upper()
    attrValues = attrValues.upper()
    #
    X = np.ma.masked_invalid(df.pivot(attrX, attrY, attrValues))
    return X


def df2mapv2(df, attrX, attrY, attrValues):
    attrX      = attrX.upper()
    attrY      = attrY.upper()
    attrValues = attrValues.upper()
    #
    x = df[attrX].values
    y = df[attrY].values
    v = df[attrValues].values
    #
    x1 = np.sort(np.unique(x))
    y1 = np.sort(np.unique(y))
    x2 = np.arange( x1.min(), x1.max() + 1 )
    y2 = np.arange( y1.min(), y1.max() + 1 )
    #
    xdiff = np.asarray( list(set(x2).difference(set(x1))) ).astype(int)
    #
    x3 = np.repeat(xdiff, len(y2))
    y3 = np.tile(y2, len(xdiff) )
    v3 = np.tile(np.nan, len(x3) )
    #
    d = { attrX: x3, attrY: y3, attrValues: v3 }
    df0 = pandas.DataFrame(d)
    #
    df1 = pandas.concat([df, df0])
    #
    X = np.ma.masked_invalid(df1.pivot(attrX, attrY, attrValues))
    return X



def view(X, attrX=None, attrY=None, extent=None, cmap=None, clim=None, figsize=None, aspect='auto', colorbar=True, savefigas=None, showplot=True):
    #
    if cmap is None :
        cmap = pyplot.cm.RdYlBu_r        
    #
    fig = pyplot.figure(figsize=figsize)
    pyplot.imshow(X.T, aspect=aspect, origin=0, cmap=cmap, clim=clim, extent=extent)
    if attrX:
        pyplot.xlabel(attrX, size=18)
    if attrY:
        pyplot.ylabel(attrY, size=18)
    if colorbar:
        pyplot.colorbar(orientation='vertical')
    pyplot.draw()
    if savefigas:
        pyplot.savefig(savefigas)
    if showplot is not False:
        pyplot.show()


def distr(x1, y1):
  idx = np.where(y1>0)[0]
  x1 = x1[idx]
  y1 = log(y1[idx])
  xbins = linspace(0, 100, 100)
  ybins = linspace(4, 16, 100)
  Hxy, xe, ye = np.histogram2d(x1, y1, [xbins, ybins])
  Hxy_log = np.ma.masked_invalid(log(Hxy))
  figure()
  imshow(Hxy_log.T, aspect='auto', extent=[xe.min(), xe.max(), ye.min(), ye.max()], origin=0)
  colorbar(orientation='horizontal')
  xlabel('Dominant Frequency', size=20)
  ylabel(r'$\log$ Amplitude', size=20)
  title(r'$\log$ Distribution', size=25)

 
def mask(X, condition):
  Mx = np.ones_like(X)
  Mx[condition] = 0.
  # trying to ignore isolated spikes
  Mx = scipy.ndimage.morphology.grey_opening(Mx, [2,2])
  Mx = scipy.ndimage.morphology.grey_closing(Mx, [3,3])
  #
  Mx1 = scipy.ndimage.morphology.grey_erosion(Mx, [50,50])
  #Mx1 = scipy.ndimage.morphology.grey_opening(Mx1, [15,15])
  return Mx1


def mask_apply(seqnb):
  seqnb = str(seqnb).zfill(3)
  capiselect = "'select to_int32(shotno), to_int32(channel_first), qc_freqdom, qc_amax from a:::416j603:/qc/sb2/q110_amp3dqc/q110_map_freq_ampmax_seq" + seqnb + "'"
  # loading into a dataframe
  print 'loading Seq' + seqnb + ' into a dataframe'
  df = capiselect2df(capiselect)
  X = df2map(df, df.columns.tolist()[0], df.columns.tolist()[1], 'qc_freqdom' )
  Y = df2map(df, df.columns.tolist()[0], df.columns.tolist()[1], 'qc_amax' )
  Y_old = Y.copy()
  #
  # eliminating weak shots before applying method (will be removed later)
  idx = np.where( np.mean(Y, axis=1) <= 40000 )[0]
  if len(idx)>0:
    shotno_min = int(df[df.columns.tolist()[0]].min())
    f = open('weakshots_seq' + seqnb + '.txt', 'w')
    for ii in idx:
      f.write( seqnb + ' ' + str(shotno_min + ii) +  '\n')
    f.close()
    #
    X[idx,:] = np.nan
    Y[idx,:] = np.nan
    X = np.ma.masked_invalid(X)
    Y = np.ma.masked_invalid(Y)
  # eliminating weak channels before applying method (will be removed later)
  idx = np.where( np.mean(Y, axis=0) <= 40000 )[0]
  if len(idx)>0:
    channel_min = int(df[df.columns.tolist()[1]].min())
    f = open('weakchannels_seq' + seqnb + '.txt', 'w')
    for jj in idx:
      f.write( seqnb + ' ' + str(channel_min + jj) +  '\n')
    f.close()
    #
    X[:,idx] = np.nan
    Y[:,idx] = np.nan
    X = np.ma.masked_invalid(X)
    Y = np.ma.masked_invalid(Y)
  #
  #
  print 'creating the mask'
  M = mask(Y, np.logical_and(Y<30000, X<25))

  #
  Y1 = Y.copy()
  Y1[M==0] = 0.0
  Y1 = np.ma.masked_equal(Y1, 0.0)
  #
  print 'saving editions'
  ix,iy = np.where(M==0.0)
  shotno_min  = int(df[df.columns.tolist()[0]].min())
  channel_min = int(df[df.columns.tolist()[1]].min())
  f = open('pol_seq' + seqnb + '.txt', 'w')
  for ii, jj in zip(ix, iy):
    f.write( seqnb + ' ' + str(shotno_min + ii) + ' ' + str(channel_min + jj) + '\n')
  f.close()
  #
  print 'preparing plot...'
  # fig properties
  extent = [df[df.columns.tolist()[0]].min(), df[df.columns.tolist()[0]].max(), df[df.columns.tolist()[1]].min(), df[df.columns.tolist()[1]].max() ]
  #figsize = [15, 12]
  figsize = None
  basename = 'fig_qc_seq' + seqnb
  #
  pyplot.close('all')
  view(Y_old,  clim=[0, 300000], figsize=figsize, attrX='Shotno', attrY='Channel', extent=extent, savefigas=basename+'_amp_b4.png', showplot=False)
  view(Y1,     clim=[0, 300000], figsize=figsize, attrX='Shotno', attrY='Channel', extent=extent, savefigas=basename+'_amp_af.png', showplot=False)
  pyplot.close('all')
  return Y, Y1

  seqnb = str(seqnb).zfill(3)
  capiselect = "'select to_int32(shotno), to_int32(channel_first), qc_freqdom, qc_amax from a:::416j603:/qc/sb2/q107_amp3dqc/q107_map_freq_ampmax_seq" + seqnb + "'"
  # loading into a dataframe
  print 'loading Seq' + seqnb + ' into a dataframe'









def mask_apply_q107(seqnb):
  seqnb = str(seqnb).zfill(3)
  capiselect = "'select to_int32(shotno), to_int32(channel), qc_freqdom, qc_amax from a:::416j603:/qc/sb2/q107_amp3dqc/q107_map_freq_ampmax_seq" + seqnb + "_i'"
  # loading into a dataframe
  print 'loading Seq' + seqnb + ' into a dataframe'
  df = capiselect2df(capiselect)
  X = df2map(df, df.columns.tolist()[0], df.columns.tolist()[1], 'qc_freqdom' )
  Y = df2map(df, df.columns.tolist()[0], df.columns.tolist()[1], 'qc_amax' )
  Y_old = Y.copy()
  #
  # eliminating weak shots before applying method (will be removed later)
  idx = np.where( np.mean(Y, axis=1) <= 40000 )[0]
  if len(idx)>0:
    shotno_min = int(df[df.columns.tolist()[0]].min())
    f = open('weakshots_seq' + seqnb + '.txt', 'w')
    for ii in idx:
      f.write( seqnb + ' ' + str(shotno_min + ii) +  '\n')
    f.close()
    #
    X[idx,:] = np.nan
    Y[idx,:] = np.nan
    X = np.ma.masked_invalid(X)
    Y = np.ma.masked_invalid(Y)
  # eliminating weak channels before applying method (will be removed later)
  idx = np.where( np.mean(Y, axis=0) <= 40000 )[0]
  if len(idx)>0:
    channel_min = int(df[df.columns.tolist()[1]].min())
    f = open('weakchannels_seq' + seqnb + '.txt', 'w')
    for jj in idx:
      f.write( seqnb + ' ' + str(channel_min + jj) +  '\n')
    f.close()
    #
    X[:,idx] = np.nan
    Y[:,idx] = np.nan
    X = np.ma.masked_invalid(X)
    Y = np.ma.masked_invalid(Y)
  #
  #
  print 'creating the mask'
  # processing each cable individually
  M = np.ones_like(X)
  for k in [1, 2, 3, 4, 5, 6]:
    idx = slice( (k-1)*480, k*480)
    M_c = mask(Y[:,idx], np.logical_and(Y[:,idx]<35000, X[:,idx]<20))
    M[:,idx] = M_c.copy()
  #
  Y1 = Y.copy()
  Y1[M==0] = 0.0
  Y1 = np.ma.masked_equal(Y1, 0.0)
  #
  print 'saving editions'
  ix,iy = np.where(M==0.0)
  shotno_min  = int(df[df.columns.tolist()[0]].min())
  channel_min = int(df[df.columns.tolist()[1]].min())
  f = open('pol_seq' + seqnb + '.txt', 'w')
  for ii, jj in zip(ix, iy):
    f.write( seqnb + ' ' + str(shotno_min + ii) + ' ' + str(channel_min + jj) + '\n')
  f.close()
  #
  print 'preparing plot...'
  # fig properties
  extent = [df[df.columns.tolist()[0]].min(), df[df.columns.tolist()[0]].max(), df[df.columns.tolist()[1]].min(), df[df.columns.tolist()[1]].max() ]
  #figsize = [15, 12]
  figsize = None
  basename = 'fig_qc_seq' + seqnb
  #
  pyplot.close('all')
  view(Y_old,  clim=[0, 300000], figsize=figsize, attrX='Shotno', attrY='Channel', extent=extent, savefigas=basename+'_amp_b4.png', showplot=False)
  view(Y1,     clim=[0, 300000], figsize=figsize, attrX='Shotno', attrY='Channel', extent=extent, savefigas=basename+'_amp_af.png', showplot=False)
  pyplot.close('all')
  return Y, Y1






list_seqs = np.loadtxt('seq_patches_sb2_sorted.txt')[:,0].astype(int)

for seqnb in list_seqs[125:]:
  Y, Y1 = mask_apply_q107(seqnb)
  #Y, Y1 = mask_apply(seqnb)


