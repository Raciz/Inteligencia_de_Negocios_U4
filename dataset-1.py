import os
import re

#Función para eliminar las etiquetas de un string
def eliminarEtiquetas(texto):
	regExp = re.compile("<.*?>") #Expresión regular que identifica las etiquetas
	nvoTexto = re.sub(regExp, " ", texto) #El texto se "limpia" y se pasa a un nuevo string
	return nvoTexto #Se retorna el string limpio


ruta = "./PoliceForce_KML/" #Ruta en la que se encuentran los archivos KML
archivos = os.listdir(ruta) #Lista de archivos KML
archivos.sort() #Se ordenan los archivos

fuerzasPoliciacas = {} #Diccionario para guardar las fuerzas policiacas y sus centroides


#Ciclo para recorrer los archivos. Para cada fuerza policiaca...
for f in archivos:
	nombreFuerza = os.path.splitext(f)[0] #Se obtiene el nombre de la fuerza policiaca
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

			promedioLatitud = sum(latitudes) / len(latitudes) #Se saca el promedio de las latitudes
			promedioLongitud = sum(longitudes) / len(longitudes) #Se saca el promedio de las longitudes

			#Se agrega al diccionario el nombre promedio de la latitud y de la longitud
			fuerzasPoliciacas.update({nombreFuerza : {"latitud": promedioLatitud, "longitud": promedioLongitud}})

			break #Se rompe el ciclo, ya no es necesario verificar el resto del archivo

		i += 1 #Se aumenta el contador de líneas

resultados = open("dataset-1.csv", "a") #Se abre el archivo

#Se imprimen los resultados
for fuerza in fuerzasPoliciacas:
	fila = fuerza + "," + str(fuerzasPoliciacas[fuerza]["latitud"]) + "," + str(fuerzasPoliciacas[fuerza]["longitud"]) + "\n"
	resultados.write(fila)
	print(fila)

resultados.close() #Se cierra el archivo

