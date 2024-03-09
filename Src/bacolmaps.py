import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib
import cpt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap


#Create custom colormap
def cmap(name) :
  '''
  Arguments:
  ---------
    name: ='crust' or None
  '''

  path="/home/barn/Dropbox/Src/Python/Utils/Cmaps/"
  if name == 'crust' :
    clist =    get_hex_list(hex_list=1)
    bacmap =  get_continuous_cmap(clist)
    plt.colormaps.register(cmap=bacmap, name='crust')
    bacmap.set_under('white')
  elif name == 'globe' :
    rgb = cpt.getcpt(path+'GMT_globe'+'.cpt')
    bacmap = ListedColormap(rgb)
    plt.colormaps.register(cmap=bacmap, name='globe')
  elif name == 'ocean' :
    rgb = cpt.getcpt(path+'GMT_ocean'+'.cpt')
    bacmap = ListedColormap(rgb)
    plt.colormaps.register(cmap=bacmap, name='ocean')
   
   

def hex_to_rgb(value):
    '''
    Converts hex to rgb colours
    value: string of 6 characters representing a hex colour.
    Returns: list length 3 of RGB values
    '''

    value = value.strip("#") # removes hash symbol if present
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def rgb_to_dec(value):
    '''
    Converts rgb to decimal colours (i.e. divides each value by 256)
    value: list (length 3) of RGB values
    Returns: list (length 3) of decimal values
    '''

    return [v/256 for v in value]

def get_continuous_cmap(hex_list, float_list=None):
    ''' 
    Creates and returns a color map that can be used in heat map figures.
    If float_list is not provided, colour map graduates linearly between each color in hex_list.
    If float_list is provided, each color in hex_list is mapped to the respective location in float_list.

    Parameters
    ----------
      hex_list: list of hex code strings
      float_list: list of floats between 0 and 1, same length as hex_list. Must start with 0 and end with 1.

    Returns
    ----------
      colour map
   ''' 

    rgb_list = [rgb_to_dec(hex_to_rgb(i)) for i in hex_list]
    if float_list:
        pass
    else:
        float_list = list(np.linspace(0,1,len(rgb_list)))

    cdict = dict()
    for num, col in enumerate(['red', 'green', 'blue']):
        col_list = [[float_list[i], rgb_list[i][num], rgb_list[i][num]] for i in range(len(float_list))]
        cdict[col] = col_list
    cmp = colors.LinearSegmentedColormap('my_cmp', segmentdata=cdict, N=256)
    return cmp

def get_hex_list(hex_list=1):
  '''
  Arguments:
  ----------
    hex_list: 0,1  Correspondng  to the two lists below 
    
  Returns:
  --------
    A list of Hex values corresponding to a list of colors.
  '''

  if hex_list==0:
    # red, red 70%, orange, gold, khaki, gray 209, 202, 201, aquamarine, blue, indigo
    ls = ['#FF0000','#ff6666','#FFA500','#FFD700','#F0E68C','#D1CAC9','7FFFD4','#00FFFF','#0000FF','4B0082']
  if hex_list==1:
    # blue, aqumarine, green, yellow, red
    ls = ['#2702a1','#1551e8','#18b1f2','#00eaff','#1ed433','#ffff00','#ff7700','#ff4000']
  return ls
