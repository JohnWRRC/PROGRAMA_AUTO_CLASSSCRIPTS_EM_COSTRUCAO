#!/c/Python25 python
# -*- coding: utf-8 -*-
import sys, os, numpy #sys, os, PIL, numpy, Image, ImageEnhance

import os
from subprocess import Popen
import zipfile
import win32com.client as win32




def prep_kmean(namemap,dirout,nclass):
    dirout=dirout.replace("\\",'/').replace("\n",'/n').replace('\a','/a')   
    os.chdir(dirout)
    kameans2=open('Kmeans_final.txt','w')
    
    #
    
    foreign="require(foreign)"
    stwd="setwd("+'\''+dirout+'\''")"
    dados="dados<-read.dbf("+"\""+namemap+'.dbf'+"\""+")"
    teste="test=logical(ncol(dados))"
    loop="for(i in 1:ncol(dados)) {"
    teste2="test[i]=all(dados[,i]==0)==F}"

    which="which.col=which(test)"
    
    dados_use="dados.use=dados[,which(test)]   " 
    
    
    
    deletar1="deletar1<-grep('_n', colnames(dados.use))"
    deleta_dados="dados2<-dados.use [,-deletar1]"
    deletar2="deletar2<-grep('_sum', colnames(dados2))"
    deleta_dados2="dados2<-dados2[,-deletar2]"
    dados2="dados2<-dados2[,-c(1,2,3)]"
    
    dados3_scale="dados3.scale<-scale(dados2)"
    fit="fit <- kmeans(dados3.scale,"+nclass+") "
    
    dados3_scale2="dados3.scale <- data.frame(dados3.scale, fit$cluster)"
    dados3_scale3="dados3.scale<-subset(dados3.scale, select=c(fit.cluster))"
    
    write_dbf="write.dbf(dados3.scale,"+"\""+namemap+"\""+")"
    
    
    kameans2.write(stwd+'\n')
    kameans2.write(foreign+'\n')
    kameans2.write(dados+'\n')
    kameans2.write(teste+'\n')
    kameans2.write(loop+'\n')
    kameans2.write(teste2+'\n')
    kameans2.write(which+'\n')
    kameans2.write(dados_use+'\n')
    
    
    kameans2.write(deletar1+'\n')
    kameans2.write(deleta_dados+'\n')
    kameans2.write(deletar2+'\n')
    kameans2.write(deleta_dados2+'\n')
    kameans2.write(dados2+'\n')
    
    kameans2.write(dados3_scale+'\n')
    kameans2.write(fit+'\n')
    
    kameans2.write(dados3_scale2+'\n')
    kameans2.write(dados3_scale3+'\n')
    kameans2.write(write_dbf)
    kameans2.close()




