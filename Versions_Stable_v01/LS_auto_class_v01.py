#!/c/Python25 python
import sys, os, numpy #sys, os, PIL, numpy, Image, ImageEnhance
import grass.script as grass
from PIL import Image
import wx
import random
import re
import time
import math
#from rpy2 import robjects
from datetime import tzinfo, timedelta, datetime
import win32gui
from win32com.shell import shell, shellcon
import string
import glob

import fnmatch
from subprocess import Popen
ID_ABOUT=101
ID_IBMCFG=102
ID_EXIT=110



def selecdirectori():
  mydocs_pidl = shell.SHGetFolderLocation (0, shellcon.CSIDL_DESKTOP, 0, 0)
  pidl, display_name, image_list = shell.SHBrowseForFolder (
    win32gui.GetDesktopWindow (),
    mydocs_pidl,
    "Select a file or folder",
    shellcon.BIF_BROWSEINCLUDEFILES,
    None,
    None
  )
  
  if (pidl, display_name, image_list) == (None, None, None):
    print "Nothing selected"
  else:
    path = shell.SHGetPathFromIDList (pidl)
    #print "Opening", #path
    a=(path)
  
  return a




def selecDirectory_folder(): 
    desktop_pidl = shell.SHGetFolderLocation (0, shellcon.CSIDL_DESKTOP, 0, 0)
    pidl, display_name, image_list = shell.SHBrowseForFolder (
      win32gui.GetDesktopWindow (),
      desktop_pidl,
      "Choose a folder",
      0,
      None,
      None
      
    )
    return shell.SHGetPathFromIDList (pidl)








class Classification(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        
        #variavels_______________________________________
        self.mapa_entrada=''
        
        
        
        self.background_filename=[]
        
        self.size = 450
        self.hsize = 450
        
        self.formcalculate='Multiple'
        self.species_profile_group=''
        self.speciesList=[]
        self.species_profile=''
        
        
        
        self.label_prefix=''
        self.RedularExp=''
        self.listMapsPng=[]
        self.listMapsPngAux=[]
        
        
         
        
        
        
       
        
        
        #
        self.dir_in=''
        self.dir_out='E:\data_2015\___john\Desenvolvimentos\aplications\Aplicacoes_grass\automatic classification'
        self.Chech_single=0
        self.Chech_mult=0
        self.import_map=''
        self.out_map=''
        self.group_img=''
        self.thrs=0.25
        self.Misize=200
        self.out_name_vect=''
        self.nclass='10'
        self.list_pattern=''
        self.dir_out_vect=''
        self.classify=0
        
        
        
        
        #________________________________________________

        #self.speciesList = ['Random walk','Core dependent','Frag. dependent', 'Habitat dependent', 'Moderately generalist', 'Highly generalist']
        #self.speciesList=grass.mlist_grouped ('rast', pattern='(*)') ['PERMANENT']
        
        #____________________________________________________________________________
        
        
        self.start_popsize=5
        self.numberruns=100
        self.timesteps=200


        #self.dirout=selecdirectori()

        
        self.output_prefix2='Nome do arquivo + ext '


        # titulo
        self.quote = wx.StaticText(self, id=-1, label="Auto Class",pos=wx.Point(20, 20))
        
        font = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.quote.SetForegroundColour("blue")
        self.quote.SetFont(font)
         #____________________________________________________________________________
        
        #
        self.quote = wx.StaticText(self, id=-1, label="Read files or folder :",pos=wx.Point(180, 62))
               
        font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.quote.SetForegroundColour("green")
        self.quote.SetFont(font)        

        #____________________________________________________________________________
        
        self.quote = wx.StaticText(self, id=-1, label="Threshold (Variability 0 to 1)",pos=wx.Point(20, 100))
                       
        font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.quote.SetForegroundColour("green")
        self.quote.SetFont(font)                
        #____________________________________________________________________________
        
        self.quote = wx.StaticText(self, id=-1, label="Classify",pos=wx.Point(300, 100))
                               
        font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.quote.SetForegroundColour("green")
        self.quote.SetFont(font)         
        
        
        
        #____________________________________________________________________________
                
        self.quote = wx.StaticText(self, id=-1, label="Minimum patch size (pixel)",pos=wx.Point(20, 170))
                               
        font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.quote.SetForegroundColour("green")
        self.quote.SetFont(font)                
        #____________________________________________________________________________        
        
        
        # A multiline TextCtrl - This is here to show how the events work in this program, don't pay too much attention to it
        #caixa de mensagem
        self.logger = wx.TextCtrl(self,5, '',wx.Point(20,240), wx.Size(340,120),wx.TE_MULTILINE | wx.TE_READONLY)
        
        #self.editname = wx.TextCtrl(self, 190, 'reg', wx.Point(180, 82), wx.Size(100,-1)) #Regular expression
        
        
        #caixa de texto do treshold
        
        self.editname = wx.TextCtrl(self, 192, '0.25', wx.Point(90,125), wx.Size(40,-1)) #borda
      
        self.editname = wx.TextCtrl(self, 194, '10', wx.Point(327,125), wx.Size(40,-1)) #borda
        self.editname = wx.TextCtrl(self, 193, '200', wx.Point(75,190), wx.Size(50,-1)) #escala
        
        
        wx.EVT_TEXT(self, 192, self.EvtText)
        wx.EVT_TEXT(self, 193, self.EvtText)
        wx.EVT_TEXT(self, 194, self.EvtText)
        #____________________________________________________________________________
        # A button
        self.button =wx.Button(self, 11, "READ FILES", wx.Point(310, 58))
        wx.EVT_BUTTON(self, 11, self.OnClick)   
        
        self.button =wx.Button(self, 10, "START SIMULATION", wx.Point(20, 380))
        wx.EVT_BUTTON(self, 10, self.OnClick)
        
        self.button =wx.Button(self, 8, "EXIT", wx.Point(270, 380))
        wx.EVT_BUTTON(self, 8, self.OnExit)        
       
      
        
       
        
        
        self.SelecMetrcis = wx.StaticText(self,-1,"Threshold:",wx.Point(22, 130))
        
        self.SelecMetrcis = wx.StaticText(self,-1,"N classes:",wx.Point(270, 130))
        self.SelecMetrcis = wx.StaticText(self,-1,"Min size :",wx.Point(22,195))
        
        #self.SelecMetrcis = wx.StaticText(self,-1,"List Ed. Unit(m):",wx.Point(180,228))
        wx.EVT_TEXT(self, 185, self.EvtText)
        
      
        
        #______________________________________________________________________________________________________________
        # Checkbox

        self.insure = wx.CheckBox(self, 96, "Single file.",wx.Point(20, 62))
        wx.EVT_CHECKBOX(self, 96,   self.EvtCheckBox)     
        
        self.insure = wx.CheckBox(self, 95, "Mult file.",wx.Point(100,62))
        wx.EVT_CHECKBOX(self, 95,   self.EvtCheckBox)   
        
        self.insure = wx.CheckBox(self, 97, "",wx.Point(280,100))
        wx.EVT_CHECKBOX(self, 97,   self.EvtCheckBox)        
        
        
      
       
 
    def EvtRadioBox(self, event):
      if event.GetId()==92:
        self.formcalculate=event.GetString()
        print self.formcalculate
        if self.formcalculate=="Single":
          self.file_sigle=''
          self.file_sigle=selecdirectori()
          print self.file_sigle
          #______________________________________________________________________________________________________
        else:
          self.Refresh()
       
            
        
        
       # self.logger.AppendText('Dispersive behaviour: %s\n' % )
     
     
     
     
    #______________________________________________________________________________________________________    
    def EvtComboBox(self, event):
        if event.GetId()==93:   #93==Species Profile Combo box
            self.mapa_entrada=event.GetString()
            self.logger.AppendText('Map : %s' % event.GetString())
        else:
            self.logger.AppendText('EvtComboBox: NEED TO BE SPECIFYED' )
            
            


        
    #______________________________________________________________________________________________________   
    def OnClick(self,event):
        #self.logger.AppendText(" Click on object with Id %d\n" %event.GetId())
        
        #______________________________________________________________________________________________________________ 
        if event.GetId()==10:   #10==START
          d= wx.MessageDialog( self, " Please select the folder where the files will be saved \n"
                                      " ","", wx.OK)
          # Create a message dialog box
          d.ShowModal() # Shows it
          d.Destroy() # finally destroy it when finished.
               
          self.dir_out=selecDirectory_folder()
          self.logger.AppendText('Directory output :'+self.dir_out+' \n ')
          self.logger.AppendText('runing... :'+self.import_map+' \n ')
          if self.Chech_single==1:
            import Cria_grupo
            import v_what
            import prepara_kmeans
            self.out_map=self.import_map.split('\\');self.out_map=self.out_map[-1].replace('.','_')            
            grass.run_command('r.in.gdal',input=self.import_map,out=self.out_map,overwrite=True,flags="o")
            self.group_img=grass.list_grouped('rast', pattern='*'+self.out_map+'*') ['PERMANENT']
            Cria_grupo.CriaGrupo(self.group_img,self.group_img[0])
            grass.run_command('g.region', rast=self.group_img[0],verbose=False)
            grass.run_command('i.segment', group='Grupo',output=self.group_img[0]+'_segment_thre'+`self.thrs`+'_'+`self.Misize`,threshold=self.thrs, minsize=self.Misize,overwrite=True)
            self.out_name_vect=self.group_img[0]+'_segment_thre'+`self.thrs`+'_'+`self.Misize`
            self.out_name_vect=self.out_name_vect.replace('.','_')
            self.out_name_vect=self.out_name_vect.replace('-','_')
            self.out_name_vect='A'+self.out_name_vect
            grass.run_command('r.to.vect',input=self.group_img[0]+'_segment_thre'+`self.thrs`+'_'+`self.Misize`,output=self.out_name_vect,type='area',overwrite=True)
            if self.classify==1:
              v_what.v_what(self.group_img,self.out_name_vect)
            os.chdir(self.dir_out)
            self.dir_out_vect=self.dir_out.replace("\\",'/').replace("\n",'/n').replace('\a','/a')
            
            grass.run_command('v.out.ogr', input=self.out_name_vect, output=self.dir_out_vect+'/'+self.out_name_vect+'.shp',type='area',flags='c',quiet=True )
            if self.classify==1:
              os.chdir(self.dir_out)
              prepara_kmeans.prep_kmean(self.out_name_vect, self.dir_out, self.nclass) 
              p = Popen([r"C:\Program Files\R\R-2.15.3\bin\x64\Rscript.exe",self.dir_out_vect+'/'+"Kmeans_final.txt"])

            grass.run_command('g.remove',flags='f',type="group",pattern='*Grupo*')

        
          if self.Chech_mult==1:
            import import_folder_imagens
            import Cria_grupo
            import v_what
            import prepara_kmeans            
            self.list_pattern=import_folder_imagens.import_fd(folder_files=self.dir_in)

            for i in self.list_pattern:
              os.chdir(self.dir_in)
              grass.run_command('r.in.gdal',input=i+".tif",out=i,overwrite=True,flags="o")
              #grass.run_command('g.remove',flags='f',type="group",pattern='*Grupo*')
              self.group_img=grass.list_grouped('rast', pattern='*'+i+'*') ['PERMANENT']
              grass.run_command('g.remove',flags='f',type="group",pattern='*Grupo*')
              Cria_grupo.CriaGrupo(self.group_img,self.group_img[0])
              grass.run_command('g.region', rast=self.group_img[0],verbose=False)
              grass.run_command('i.segment', group='Grupo',output=i+'_segment_thre'+`self.thrs`+'_'+`self.Misize`,threshold=self.thrs, minsize=self.Misize,overwrite=True )
              self.out_name_vect=i+'_segment_thre'+`self.thrs`+'_'+`self.Misize`
              self.out_name_vect=self.out_name_vect.replace('.','_')
              self.out_name_vect=self.out_name_vect.replace('-','_')
              self.out_name_vect='JWR_'+self.out_name_vect
              
              
              
              grass.run_command('r.to.vect',input=i+'_segment_thre'+`self.thrs`+'_'+`self.Misize`,output=self.out_name_vect,type='area',overwrite=True )
              if self.classify==1:
                v_what.v_what(self.group_img,self.out_name_vect)
              
              self.dir_out_vect=self.dir_out.replace("\\",'/').replace("\n",'/n').replace('\a','/a')
              grass.run_command('v.out.ogr', input=self.out_name_vect, output=self.dir_out+'/'+self.out_name_vect+'.shp',type='area',overwrite=True,flags='c',quiet=True)
              if self.classify==1:
                prepara_kmeans.prep_kmean(self.out_name_vect, self.dir_out, self.nclass) 
                p = Popen([r"C:\Program Files\R\R-2.15.3\bin\x64\Rscript.exe",self.dir_out_vect+'/'+"Kmeans_final.txt"])  
              
              for i in self.group_img:
                grass.run_command('g.remove',flags='f',type="raster",pattern='*'+i+'*')
          
          d= wx.MessageDialog( self, " Finish \n"
                               " ","", wx.OK)
          # Create a message dialog box
          d.ShowModal() # Shows it
          d.Destroy() # finally destroy it when finished.
                   
            
        #______________________________________________________________________________________________________________ 
       
        
        if event.GetId()==11:
          if self.Chech_mult==1:
            self.dir_in=selecDirectory_folder()
            self.logger.AppendText('Directory input :'+self.dir_in+' \n ')
            
                            
          if self.Chech_single==1:
            self.import_map=selecdirectori()
            self.logger.AppendText('File input :'+self.import_map+' \n ')
            
                        
            
            
            
          
          
              
    
    #______________________________________________________________________________________________________________                
    def EvtText(self, event):
        #self.logger.AppendText('EvtText: %s\n' % event.GetString())
      #______________________________________________________________________________________________________________ 
        if event.GetId()==192: #20=output_prefix
          self.thrs=event.GetString()
          self.logger.AppendText('Treshold :'+self.thrs+' \n ')
          self.thrs=float(self.thrs)
          
            
        if event.GetId()==193: #20=output_prefix
          self.Misize=event.GetString()
          self.logger.AppendText('Min size :'+self.Misize+' \n ')
          self.Misize=float(self.Misize)
          
        if event.GetId()==194: #20=output_prefix
          self.nclass=event.GetString() 
          self.logger.AppendText('N class :'+self.nclass+' \n ')
                   
            
            
        
        
          
             

    #______________________________________________________________________________________________________
    def EvtCheckBox(self, event):
        if event.GetId()==95:
          if self.Chech_mult==1:
            self.Chech_mult=0
          else: 
            self.Chech_mult=1
            
          if self.Chech_mult==1:
            
            self.logger.AppendText('Option Mult file selected : TRUE\n')
          else:
            
            self.logger.AppendText('Option Multfile selected : FALSE\n')
            
            
            
        if event.GetId()==96:
          if self.Chech_single==1:
            self.Chech_single=0
          else:
            self.Chech_single=1
          
          if self.Chech_single==1:
            self.logger.AppendText('Option Single selected :TRUE\n')
          else:
            self.logger.AppendText('Option Single selected :FALSE\n')
        
        
        
        if event.GetId()==97:
          if self.classify==1: 
            self.classify=0
          else:
            self.classify=1
             
          if self.classify==1:  
            self.logger.AppendText('Option classify selected: TRUE\n')        
          else:
            self.logger.AppendText('Option classify selected: FALSE\n')  
              
                           
        
           
        
            
         
            
    #______________________________________________________________________________________________________
    def OnExit(self, event):
        d= wx.MessageDialog( self, " Thanks for simulating \n"
                            " ","Good bye", wx.OK)
                            # Create a message dialog box
        d.ShowModal() # Shows it
        d.Destroy() # finally destroy it when finished.
        frame.Close(True)  # Close the frame. 

#----------------------------------------------------------------------
#......................................................................
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = wx.Frame(None, -1, "JWR & MHV", size=(410,450))
    Classification(frame,-1)
    frame.Show(1)
    
    app.MainLoop()
