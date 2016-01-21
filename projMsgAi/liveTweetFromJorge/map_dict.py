# make figures better:
#font = {'weight':'normal','size':20}
#matplotlib.rc('font', **font)
#matplotlib.rc('figure', figsize=(9.0, 6.0))
#matplotlib.rc('xtick.major', pad=10) # xticks too close to border!
import sys
import warnings
warnings.filterwarnings('ignore')

import random, math
import numpy as np
import scipy, scipy.stats

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
nicered = "#E6072A"
niceblu = "#424FA4"
nicegrn = "#6DC048"

from matplotlib.collections import LineCollection
from matplotlib.colors import rgb2hex
from mpl_toolkits.basemap import Basemap

def map_dict(export_fn,states_happiness):
    # Lambert Conformal map of lower 48 states.
    m = Basemap(llcrnrlon=-119,llcrnrlat=22,
                    urcrnrlon=-64, urcrnrlat=49,
                                projection='lcc', lat_1=33,lat_2=45,lon_0=-95)
    
    # laod state boundaries.
    # data from U.S Census Bureau
    # http://www.census.gov/geo/www/cob/st1990.html
    shp_info = m.readshapefile('gz_2010_us_040_00_500k/gz_2010_us_040_00_500k','states',drawbounds=False)
    # This loads three files:
    #   gz_2010_us_040_00_500k.dbf
    #   gz_2010_us_040_00_500k.shp
    #   gz_2010_us_040_00_500k.shx
    
    max_score = -sys.maxint - 1
    min_score = sys.maxint+1
    happiest_state = ''
    saddest_state = ''
    for state in states_happiness:
          score = states_happiness[state]
          if (score > max_score):
                happiest_state = state
                max_score = score
          if (score < min_score):
                saddest_state = state
                min_score = score
    
    for state in states_happiness:
        states_happiness[state] -= min_score
    
    min_score = 0
    max_score = max_score-min_score
    
    # choose a color for each state based on happiness score.
    colors={}
    statenames=[]
    cmap = plt.cm.Blues_r # use 'hot' colormap
    vmin = min_score; vmax = max_score # set range.
    sm = plt.cm.ScalarMappable(cmap=cmap, 
                                   norm=plt.normalize(vmin=vmin, vmax=vmax))
    
    for shapedict in m.states_info:
        statename = shapedict['NAME']
        #print statesNames[statename], ' ', statename
        try:
            #score = states_happiness[statesNames[statename]]
            score = states_happiness[statename]
        except KeyError:
            score = 0.0
            
        # calling colormap with value between 0 and 1 returns
        # rgba value. Invert color range (hot colors are
        # high
        # population), take sqrt root to spread out
        # colors more.
        if vmax-vmin != 0:
            colors[statename] = cmap((score-vmin)/(vmax-vmin))[:3]
        else:
            colors[statename] = cmap(0)[:3]
        statenames.append(statename)
        
    # cycle through state names,
    # color each one.
    for nshape,seg in enumerate(m.states):
        xx,yy = zip(*seg)
        if statenames[nshape] != 'District of Columbia' and \
        statenames[nshape] != "Puerto Rico":
            color = rgb2hex(colors[statenames[nshape]]) 
            plt.fill(xx,yy,color,edgecolor='black')
    
    # draw
    # meridians
    # and
    # parallels.
    m.drawparallels(np.arange(25,65,20),   labels=[0,0,0,0],
                        zorder=-1,color="w")
    m.drawmeridians(np.arange(-120,-40,20),labels=[0,0,0,0],
                        zorder=-1,color="w")
     
    # set  up colorbar:
    mm = plt.cm.ScalarMappable(cmap=cmap)
    mm.set_array([0,1])
    #plt.colorbar(mm, label="Happiness",
    #                              orientation="horizontal", fraction=0.05)
    plt.colorbar(mm,orientation="horizontal", fraction=0.05)
     
    #plt.title('Filling State Polygons by Population Density')
    plt.gca().axis("off")
    plt.savefig(export_fn)
    plt.close('all')
    #plt.show()
