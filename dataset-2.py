import os
import re
import math
from matplotlib import pyplot as plt
import numpy as np
import scipy.stats as st

EARTH_RADIUS_KM = 6371.0

#Función para eliminar las etiquetas de un string
def eliminarEtiquetas(texto):
	regExp = re.compile("<.*?>") #Expresión regular que identifica las etiquetas
	nvoTexto = re.sub(regExp, " ", texto) #El texto se "limpia" y se pasa a un nuevo string
	return nvoTexto #Se retorna el string limpio

#Converts degrees to radians
def degrees_to_radians(degrees):
	return ( degrees * math.pi / 180.0 )


#Haversine formula
def distance_km(lat1, lon1, lat2, lon2):
	#Conversion to radians
	lat1 = degrees_to_radians( lat1 )
	lon1 = degrees_to_radians( lon1 )
	lat2 = degrees_to_radians( lat2 )
	lon2 = degrees_to_radians( lon2 )

	#Computing terms based on the differences in longitude and latitud
	sin_delta_lat = math.sin( (lat2 - lat1) / 2.0 )
	sin_delta_lat *= sin_delta_lat;
	
	sin_delta_lon = math.sin( (lon2 - lon1) / 2.0 )
	sin_delta_lon *= sin_delta_lon

	#Apply formula and convert to KM
	hav = ( sin_delta_lat + math.cos( lat1 ) * math.cos( lat2 ) * sin_delta_lon )

	return 2.0 * EARTH_RADIUS_KM * math.asin( math.sqrt( hav ) )



fuerzasPoliciacas = {} #Para guardar el área de cada fuerza policiaca

ruta = "./PoliceForce_KML/" #Ruta en la que se encuentran los archivos KML
archivos = os.listdir(ruta) #Lista de archivos KML
archivos.sort() #Se ordenan los archivos

ruta2 = "./CrimesUK_2011_2017/" #Ruta de los archivos principales
directorios = os.listdir(ruta2) #lista los directorios que se encuentran dentro de la carpeta principal

#Ciclo para recorrer los archivos. Para cada fuerza policiaca...
for f in archivos:
	nombreFuerza = os.path.splitext(f)[0] #Se obtiene el nombre de la fuerza policiaca
	totalReportes = 0 #Contador de crímenes reportados por la fuerza
	archivo = open(ruta + f) #Se abre el archivo "f" del directorio

	latitudes = [] #Lista para guardar las latitudes
	longitudes = [] #Lista para guardar las longitudes

	i = 0 #Contador de líneas
	#Ciclo para recorrer el archivo
	for line in archivo:
		#Si se ha llegado a la línea 13 (la que contiene las coordenadas)
		if i == 13:
			coordenadasTotales = eliminarEtiquetas(line).split() #Se eliminan las etiquetas de esa línea y las coordenadas se guardan en una lista

			#Se recorre la lista de coordenadas
			for coordenadas in coordenadasTotales:
				coordenadas2 = coordenadas.split(",") #El string de las coordenadas se separa para guardar por separado la latitud y la longitud 
				longitudes.append(float(coordenadas2[0])) #Se guarda la longitud actual en valor decimal
				latitudes.append(float(coordenadas2[1])) #Se guarda la latitud actual en valor decimal

			longitudes.sort() #Se ordenan las longitudes
			latitudes.sort() #Se ordenan las latitudes
		
			x1, x2 = latitudes[0], latitudes[-1] #Se sacan los puntos de menor y mayor latitud
			y1, y2 = longitudes[0], longitudes[-1] #Se sacan los puntos de menor y mayor longitud
			
			base = distance_km(x1, y1, x2, y1) #Se saca la base del área total
			altura = distance_km(x1, y1, x1, y2) #Se saca la altura del área total
			area = round(base * altura, 2) #Se calcula el área (redondeada a 2 dígitos después del punto)

			fuerzasPoliciacas.update({nombreFuerza : {"area": area}}) #Se agrega al diccionario el nombre de la fuerza y su área

			#Ciclo para recorrer los archivos de reportes principales
			for f2 in directorios:
				rutaSecundaria = ruta2+f2+"/" #se prepara la ruta donde se buscarán los archivos

				#se recorren todos los archivos encontrados en ese directorio
				for e in os.listdir(rutaSecundaria):
					#Se comprueba que el archivo sea el de los reportes de la fuerza policiaca actual
					if e.find(nombreFuerza) != -1:
						archivo = open(rutaSecundaria+e) #se abre el archivo
						
						cLine = 0 #variable para que no cuente la primera línea, que es la del encabezado de cada archivo

						#Se recorre el archivo
						for line in archivo:
							if(cLine!=0):
								totalReportes += 1 #Se aumenta el número de crímenes reportados
							cLine+=1
				
						break #Se rompe el ciclo, ya no es necesario verificar los demás archivos

			break #Se rompe el ciclo, ya no es necesario verificar los demás archivos

		i += 1 #Se aumenta el contador

	fuerzasPoliciacas[nombreFuerza].update({"totalReportes" : totalReportes}) #Se agrega al diccionario en la fuerza actual el total de reportes

resultados = open("dataset-2.csv", "a") #Se abre el archiv


#Se asignan los resultados
for fuerza in fuerzasPoliciacas:
	fila = fuerza + "," + str(fuerzasPoliciacas[fuerza]["totalReportes"]) + "," + str(fuerzasPoliciacas[fuerza]["area"]) + "\n"
	resultados.write(fila)
	print(fila)

resultados.close() #Se cierra el archivo



