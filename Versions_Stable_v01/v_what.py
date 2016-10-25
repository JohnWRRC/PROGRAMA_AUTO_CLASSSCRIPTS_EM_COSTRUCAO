#!/c/Python25 python
import sys, os, numpy #sys, os, PIL, numpy, Image, ImageEnhance
import grass.script as grass
 
def v_what(gp,vect):
    grass.run_command('v.build',map=vect)
    cont_band=1
    for i in gp:
        format_bands='00'+`cont_band`
        format_bands=format_bands[-1:]
        
        grass.run_command('g.region', rast=gp[0])
        grass.run_command('v.rast.stats' ,map=vect, raster=i,colprefix='b'+format_bands)
        cont_band=cont_band+1
        
