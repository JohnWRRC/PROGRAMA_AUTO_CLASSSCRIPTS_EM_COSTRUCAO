#!/c/Python25 python
import sys, os, numpy #sys, os, PIL, numpy, Image, ImageEnhance
import grass.script as grass
from PIL import Image
import wx
import random
import re
import time
import math

#grass.run_command('g.remove',group="Grupo")
def CriaGrupo(grupo,gregion):
    grass.run_command('g.remove',flags='f',type="group",pattern='*Grupo*')
    grass.run_command('g.region',rast=gregion)
    grass.run_command('i.group', group='Grupo' ,subgroup='Grupo', input=grupo, verbose=False)
    

