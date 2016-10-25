import grass.script as grass
from grass.script import raster as grassR
import os
import string
import glob
import re
import fnmatch
lista_arquivos=[]
LISTA=[]
LISTA2=[]  
list_patter=[]

def import_fd(folder_files):
    for file in os.listdir(folder_files):
        if fnmatch.fnmatch(file, '*.tif'):
            lista_arquivos.append(file)
      
    for file in os.listdir(folder_files):
        if fnmatch.fnmatch(file, '*.img'):
            lista_arquivos.append(file)    
                 
    os.chdir(folder_files)
    for i in lista_arquivos:
        
        out=i.replace('.tif','')
        list_patter.append(out)
        #print out
        #grass.run_command('r.in.gdal',input=i,out=out,overwrite=True,flags="o")
    return list_patter
    

 
    

