# -*- coding: utf-8 -*-
"""
Created on Tue May  1 10:57:41 2018

@author: hsevilla
"""
import pandas as pd
import numpy as np
import copy
import math

#Import all Sales Extracts
se_1803 = pd.read_excel("se_selection\\*** 05.03.18.xlsx", 'Retail')
se_1712 = pd.read_excel("se_selection\\*** 11.12.17.xlsx", 'Retail')
se_1709 = pd.read_excel("se_selection\\*** 04.09.17.xlsx", 'Retail')
se_1706 = pd.read_excel("se_selection\\*** 06.06.17.xlsx", 'Retail')
se_1703 = pd.read_excel("se_selection\\*** 06.03.17.xlsx", 'Retail') 
se_1612 = pd.read_excel("se_selection\\*** 05.12.16.xlsx", 'RetailOurModels')
se_1609 = pd.read_excel("se_selection\\*** 21.09.2016.xlsx", 'Retail2')
se_1606 = pd.read_excel("se_selection\\*** 01.05.2016 - 07.07.2016.xlsx", 'Retail') 
se_1603 = pd.read_excel("se_selection\\*** 01.05.2015 - 24.05.2016.xlsx", 'Retail') 

##Keep relevant columns
se_1803 = se_1803.loc[:,['DealerName','AFRLingDealer','Zone','RegistrationDate','CustomerOrderDate','Fullname','FleetCategory','FleetCustomer','VIN','FamilyLCDV']]
se_1712 = se_1712.loc[:,['DealerName','AFRLingDealer','Zone','RegistrationDate','CustomerOrderDate','Fullname','FleetCategory','FleetCustomer','VIN','FamilyLCDV']]
se_1709 = se_1709.loc[:,['DealerName','AFRLingDealer','Zone','RegistrationDate','CustomerOrderDate','Fullname','FleetCategory','FleetCustomer','VIN','FamilyLCDV']]
se_1706 = se_1706.loc[:,['DealerName','AFRLingDealer','Zone','RegistrationDate','CustomerOrderDate','Fullname','FleetCategory','FleetCustomer','VIN','FamilyLCDV']]
se_1703 = se_1703.loc[:,['DealerName','AFRLingDealer','Zone','RegistrationDate','CustomerOrderDate','Fullname','FleetCategory','FleetCustomer','VIN','FamilyLCDV']]
se_1612 = se_1612.loc[:,['DealerName','AFRLingDealer','Zone','RegistrationDate','CustomerOrderDate','Fullname','FleetCategory','FleetCustomer','VIN','FamilyLCDV']]
se_1609 = se_1609.loc[:,['DealerName','AFRLingDealer','Zone','RegistrationDate','CustomerOrderDate','Fullname','FleetCategory','FleetCustomer','VIN','FamilyLCDV']]
se_1606 = se_1606.loc[:,['DealerName','AFRLingDealer','Zone','RegistrationDate','CustomerOrderDate','Fullname','FleetCategory','FleetCustomer','VIN','FamilyLCDV']]
se_1603 = se_1603.loc[:,['DealerName','AFRLingDealer','Zone','RegistrationDate','CustomerOrderDate','Fullname','FleetCategory','FleetCustomer','VIN','FamilyLCDV']]

#Concatenate, delete duplicates
frames = [se_1803,se_1712,se_1709,se_1706,se_1703,se_1612,se_1609,se_1606,se_1603]
solid = pd.concat(frames,ignore_index=True)
solid = solid.drop_duplicates(subset='VIN',keep='first')
solid['RegistrationDate'] = solid['RegistrationDate'].map(lambda x: 100*x.year + x.month)
solid['CustomerOrderDate'] = solid['CustomerOrderDate'].map(lambda x: 100*x.year + x.month)
solid = solid.sort_values(by = ['DealerName','CustomerOrderDate'])
solid.index = range(0,solid.shape[0])

#solid = solid.iloc[0:2000,:]

SalesPerMonth = pd.DataFrame(columns = solid.columns)
SalesPerModel = pd.DataFrame()


tretail = 0
tpack = 0
ppack = 0
selfreg = 0
pselfreg = 0



for i in solid.index:
#for i in range(0,10):
    tretail+=1
  
    #Is a majority of words from 'DealerName' in 'Fullname'?
    p1 = 0
    for j in range(0,len(solid.loc[i,'DealerName'].split())):    
        try :
            p1 = p1 + (solid.loc[i,'DealerName'].split()[j] in solid.loc[i,'Fullname'])
        except :
            pass
    p1=p1/len(solid.loc[i,'DealerName'].split())
    
    #Is a majority of words from 'Fullname' in 'DealerName'?
    p2 = 0
    if not pd.isnull(solid.loc[i,'Fullname']):
        for j in range(0,len(solid.loc[i,'Fullname'].split())):    
            try :
                p2 = p2 + (solid.loc[i,'Fullname'].split()[j] in solid.loc[i,'DealerName'])
            except :
                pass
        p2=p2/len(solid.loc[i,'Fullname'].split())

    #if self-registration is identified:                    
    if p1>0.5 or p2>0.5 :
        selfreg+=1
        solid.loc[i,'SelfRegistrationSales'] = selfreg    


    #pack identification
    if 'pack' in solid.loc[i,'FleetCategory'] and 'package' not in solid.loc[i,'FleetCategory']:
        tpack +=1
        solid.loc[i,'PackSales'] = tpack


    #identify going to next retailer/date    
    try :
        nextretailer = solid.loc[i,'DealerName'] != solid.loc[i+1,'DealerName']\
        or solid.loc[i,'CustomerOrderDate'] != solid.loc[i+1,'CustomerOrderDate']
    except :
        nextretailer = True
        

    SalesPerModel.loc[i,solid.loc[i,'FamilyLCDV']] = 1

    #save informations in solid and SalesPerMonth          
    if nextretailer :
        solid.loc[i,'TotalRetailSales'] = tretail
        solid.loc[i,'PackSales'] = tpack
        solid.loc[i,'PackPercentage'] = tpack/tretail
        solid.loc[i,'SelfRegistrationSales'] = selfreg
        solid.loc[i,'SelfRgistrationPercentage'] = selfreg/tretail

        SalesPerMonth.loc[i,:]=solid.loc[i,:]
        SalesPerMonth.loc[i,'TotalRetailSales'] = tretail
        SalesPerMonth.loc[i,'PackSales'] = tpack
        SalesPerMonth.loc[i,'PackPercentage'] = tpack/tretail
        SalesPerMonth.loc[i,'SelfRegistrationSales'] = selfreg
        SalesPerMonth.loc[i,'SelfRgistrationPercentage'] = selfreg/tretail
        
        
        for m in SalesPerModel.columns:    
            SalesPerMonth.loc[i,m]=SalesPerModel.sum(0).loc[m]
        SalesPerModel = pd.DataFrame()
            
        tretail = 0
        tpack = 0
        ppack = 0
        selfreg = 0
        pselfreg = 0

SalesPerMonth.index = range(0,SalesPerMonth.shape[0])
