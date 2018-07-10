
# coding: utf-8

# In[ ]:




#importacion de los modulos nesesarios para el script
import sys, os
import pandas as pd


# In[ ]:


#lista con el nombre de las fuerza policiacas
forces = os.listdir("./CrimesUK_2011_2017/2011-01")

#borramos lo necesario para quedarnos solo con el nombre de la fuerza
for i in range(len(forces)):
    forces[i] = forces[i][8:-11]

#lista con el nombre de todos los crimenes
crimes =['Burglary','Public order','Shoplifting','Drugs','Public disorder and weapons','Other crime','Anti-social behaviour','Other theft','Bicycle theft','Violent crime','Robbery','Vehicle crime','Violence and sexual offences','Criminal damage and arson','Theft from the person','Possession of weapons']

#lista para sumar los crimenes reportados de cada fuerza policiaca por cada tipo de crimen 
forcesTypeCrimes = [0] * len(forces)
for i in range(len(forces)):
    forcesTypeCrimes[i] = [0] * len(crimes) 


# In[ ]:


#ciclo para abrir recorrer los archivos por año
for i in ["2011-","2012-","2013-","2014-","2015-","2016-","2017-"]:
    #ciclo para abrir los archivos mes por mes
    for j in ["01","02","03","04","05","06","07","08","09","10","11","12"]:
        #ciclo para abrir los archivos fuerza por fuerza 
        for k in range(len(forces)):
            
            #abrimos el archivo mediantes pandas para obtener un dataframe
            dataset = pd.read_csv("./CrimesUK_2011_2017/"+i+j+"/"+i+j+"-"+forces[k]+"-street.csv", header=0)
    
            #for para contar para un archivo el numero de crimen registrado para cada uno de los crimenes
            for l in range(len(crimes)):
                #contamos el numero de filas del dataFrame y lo sumamos en su posicion correspodiente a la fuerza 
                #y el tipo de crimen
                forcesTypeCrimes[k][l] += len(dataset[dataset["Crime type"] == crimes[l]])


# In[ ]:


#convertimo la matriz Q7 en un dataframe
Q7dataFrame = pd.DataFrame(forcesTypeCrimes,index=forces)

#y exportamos su informacion a un csv
Q7dataFrame.to_csv("./dataset-4.csv",header=False)

