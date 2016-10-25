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
import re
import fnmatch
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




  







class Form1(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        
        #variavels_______________________________________
        Form1.mapa_entrada=''
        
        
        
        Form1.background_filename=[]
        
        Form1.size = 450
        Form1.hsize = 450
        
        Form1.formcalculate='Multiple'
        Form1.species_profile_group=''
        Form1.speciesList=[]
        Form1.species_profile=''
        
        
        
        Form1.label_prefix=''
        Form1.RedularExp=''
        Form1.listMapsPng=[]
        Form1.listMapsPngAux=[]
        
        
         
        
        
        
       
        
        
        #
        Form1.dir_in=''
        Form1.Chech_single=0
        Form1.Chech_mult=0
        Form1.import_map=''
        Form1.out_map=''
        Form1.group_img=''
        Form1.thrs=0.25
        Form1.Misize=200
        
        
        
        
        #________________________________________________

        #self.speciesList = ['Random walk','Core dependent','Frag. dependent', 'Habitat dependent', 'Moderately generalist', 'Highly generalist']
        #Form1.speciesList=grass.mlist_grouped ('rast', pattern='(*)') ['PERMANENT']
        
        #____________________________________________________________________________
        
        
        Form1.start_popsize=5
        Form1.numberruns=100
        Form1.timesteps=200


        #Form1.dirout=selecdirectori()

        
        Form1.output_prefix2='Nome do arquivo + ext '


        # titulo
        self.quote = wx.StaticText(self, id=-1, label="Map Auto Classe (MAC)",pos=wx.Point(20, 20))
        
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
        
        self.quote = wx.StaticText(self, id=-1, label="Treshold (Variabilidade  de 0 a 1) ",pos=wx.Point(20, 100))
                       
        font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.quote.SetForegroundColour("green")
        self.quote.SetFont(font)                
        #____________________________________________________________________________
        
        
        #____________________________________________________________________________
                
        self.quote = wx.StaticText(self, id=-1, label="Minimum size patc(Hectares)",pos=wx.Point(20, 170))
                               
        font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.quote.SetForegroundColour("green")
        self.quote.SetFont(font)                
        #____________________________________________________________________________        
        
        
        # A multiline TextCtrl - This is here to show how the events work in this program, don't pay too much attention to it
        #caixa de mensagem
        self.logger = wx.TextCtrl(self,5, '',wx.Point(20,330), wx.Size(340,120),wx.TE_MULTILINE | wx.TE_READONLY)
        
        #self.editname = wx.TextCtrl(self, 190, 'reg', wx.Point(180, 82), wx.Size(100,-1)) #Regular expression
        
        
        #caixa de texto do treshold
        
        self.editname = wx.TextCtrl(self, 192, '0.25', wx.Point(90,125), wx.Size(40,-1)) #borda
        self.editname = wx.TextCtrl(self, 193, '200', wx.Point(90,190), wx.Size(50,-1)) #escala
        
        wx.EVT_TEXT(self, 190, self.EvtText)
        wx.EVT_TEXT(self, 191, self.EvtText)
        wx.EVT_TEXT(self, 192, self.EvtText)
        #____________________________________________________________________________
        # A button
        self.button =wx.Button(self, 11, "READ FILES", wx.Point(310, 58))
        wx.EVT_BUTTON(self, 11, self.OnClick)   
        
        self.button =wx.Button(self, 10, "START SIMULATION", wx.Point(20, 480))
        wx.EVT_BUTTON(self, 10, self.OnClick)
        self.button =wx.Button(self, 8, "EXIT", wx.Point(270, 480))
        wx.EVT_BUTTON(self, 8, self.OnExit)        
       
        #____________________________________________________________________________
        ##------------ LElab_logo
        #imageFile = 'logo_lab.png'
        #im1 = Image.open(imageFile)
        #jpg1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        #wx.StaticBitmap(self, -1, jpg1, (20,190), (jpg1.GetWidth(), jpg1.GetHeight()), style=wx.SUNKEN_BORDER)


       #______________________________________________________________________________________________________________
       #static text
        
        #self.SelecMetrcis = wx.StaticText(self,-1,"Chose Metric:",wx.Point(20,150))
        
        
       
        
        
        self.SelecMetrcis = wx.StaticText(self,-1,"Threshold:",wx.Point(22, 130))
        self.SelecMetrcis = wx.StaticText(self,-1,"Min size (Ha):",wx.Point(22,195))
        #self.SelecMetrcis = wx.StaticText(self,-1,"List Ed. Unit(m):",wx.Point(180,228))
        wx.EVT_TEXT(self, 185, self.EvtText)
        
        
        #______________________________________________________________________________________________________________
        # the combobox Control
        #Form1.editspeciesList=wx.ComboBox(self, 93, Form1.species_profile, wx.Point(80, 115), wx.Size(280, -1),
        #Form1.speciesList, wx.CB_DROPDOWN)
        #wx.EVT_COMBOBOX(self, 93, self.EvtComboBox)
        #wx.EVT_TEXT(self, 93, self.EvtText)
        
        #______________________________________________________________________________________________________________
        # Checkbox

        self.insure = wx.CheckBox(self, 96, "Single file.",wx.Point(20, 62))
        wx.EVT_CHECKBOX(self, 96,   self.EvtCheckBox)     
        
        self.insure = wx.CheckBox(self, 95, "Mult file.",wx.Point(100,62))
        wx.EVT_CHECKBOX(self, 95,   self.EvtCheckBox)   
        
        
        
        #______________________________________________________________________________________________________________
        
        #Radio Boxes
        #self.dispersiveList = ['Multiple', 'Single','',          ]
        #rb = wx.RadioBox(self, 92, "Chose form calculate", wx.Point(20, 62), wx.DefaultSize,
                        #self.dispersiveList, 3, wx.RA_SPECIFY_COLS)
        
        #wx.EVT_RADIOBOX(self, 92, self.EvtRadioBox)
        
       
        #rb.ShowItem(2, show=False)
        
        #______________________________________________________________________________________________________________ 

       
 
    def EvtRadioBox(self, event):
      if event.GetId()==92:
        Form1.formcalculate=event.GetString()
        print Form1.formcalculate
        if Form1.formcalculate=="Single":
          Form1.file_sigle=''
          Form1.file_sigle=selecdirectori()
          print Form1.file_sigle
          #______________________________________________________________________________________________________
        else:
          self.Refresh()
       
            
        
        
       # self.logger.AppendText('Dispersive behaviour: %s\n' % )
     
     
     
     
    #______________________________________________________________________________________________________    
    def EvtComboBox(self, event):
        if event.GetId()==93:   #93==Species Profile Combo box
            Form1.mapa_entrada=event.GetString()
            self.logger.AppendText('Map : %s' % event.GetString())
        else:
            self.logger.AppendText('EvtComboBox: NEED TO BE SPECIFYED' )
            
            


        
    #______________________________________________________________________________________________________   
    def OnClick(self,event):
        #self.logger.AppendText(" Click on object with Id %d\n" %event.GetId())
        
        #______________________________________________________________________________________________________________ 
        if event.GetId()==10:   #10==START
          if Form1.Chech_single==1:
            import Cria_grupo
            Form1.out_map=Form1.import_map.split('\\');Form1.out_map=Form1.out_map[-1].replace('.','_')            
            grass.run_command('r.in.gdal',input=Form1.import_map,out=Form1.out_map,overwrite=True)
            Form1.group_img=grass.list_grouped('rast', pattern='*'+Form1.out_map+'*') ['PERMANENT']
            Cria_grupo.CriaGrupo(Form1.group_img)
            grass.run_command('g.region', rast=Form1.group_img[0],verbose=False)
            grass.run_command('i.segment', group='Grupo',output=Form1.group_img[0]+'_segment_thre'+`Form1.thrs`+'_'+`Form1.Misize`,threshold=Form1.thrs, minsize=Form1.Misize)
            #grass.run_command('r.to.vect',input=Form1.group_img[0]+'_segment_thre'+`Form1.thrs`+'_'+`Form1.Misize`,output=Form1.group_img[0]+'_segment_thre'+`Form1.thrs`+'_'+`Form1.Misize`,type='area' )
          
          
         
          if event.GetId()==11:
            if Form1.Chech_mult==1:
              import import_folder_imagens
              import_folder_imagens.import_fd(folder_files=Form1.dir_in)          
        
        
        
        #______________________________________________________________________________________________________________ 
        if event.GetId()==9:   #9==CHANGE BACKGROUND
          if Form1.plotmovements==1:
            self.Refresh()
            Form1.background_filename=Form1.listMapsPng
            Form1.background_filename_start=Form1.background_filename[Form1.contBG]   
            img =Image.open(Form1.background_filename[Form1.contBG])
          
            # redimensionamos sem perder a qualidade
            img = img.resize((Form1.size,Form1.hsize),Image.ANTIALIAS)
            img.save(Form1.background_filename[Form1.contBG])        
          
          
            imageFile=Form1.background_filename[Form1.contBG]
            im1 = Image.open(imageFile)
            jpg1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            wx.StaticBitmap(self, -1, jpg1, (380,40), (jpg1.GetWidth(),  jpg1.GetHeight()), style=wx.SIMPLE_BORDER)
                              
            Form1.background_filename=Form1.background_filename_start
            Form1.contBG=Form1.contBG+1
            self.Refresh() 
            if len(Form1.listMapsPng)==Form1.contBG:
              Form1.contBG=0      
              self.Refresh() 
              #______________________________________________________________________________________________________________ 
        if event.GetId()==11:
          if Form1.Chech_mult==1:
            Form1.dir_in=selecdirectori()
          if Form1.Chech_single==1:
            Form1.import_map=selecdirectori()
            
            
            
          
          
              
    
    #______________________________________________________________________________________________________________                
    def EvtText(self, event):
        #self.logger.AppendText('EvtText: %s\n' % event.GetString())
      #______________________________________________________________________________________________________________ 
        if event.GetId()==192: #20=output_prefix
            Form1.thrs=event.GetString()
            Form1.thrs=float(Form1.thrs)
            
        if event.GetId()==193: #20=output_prefix
          Form1.Misize=event.GetString()
          Form1.Misize=float(Form1.Misize)        
            
            
            
        
        
           
             

    #______________________________________________________________________________________________________
    def EvtCheckBox(self, event):
        #self.logger.AppendText('EvtCheckBox: %d\n' % event.Checked())
      #multiplos
        if event.GetId()==95:
            Form1.Chech_mult=1
        if event.GetId()==96:
          Form1.Chech_single=1        
              
              
                           
        
           
        
            
         
            
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
    frame = wx.Frame(None, -1, " ", size=(410,550))
    Form1(frame,-1)
    frame.Show(1)
    
    app.MainLoop()
