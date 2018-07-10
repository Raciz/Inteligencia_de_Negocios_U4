
# coding: utf-8

# In[1]:


#importacion de las bibliotecas nesesarias para el script
get_ipython().magic(u'matplotlib inline')
import os,sys
import pandas as pd
import matplotlib.pyplot as plot
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import linkage, fcluster
from mpl_toolkits.mplot3d import Axes3D


# In[2]:


random_state = 170

#obtencion de los nombres de los datasets
files = os.listdir("./datasets")

#ordenamos los nombres de los archivos
files.sort()

#titulos de las graficas y los scatters
name = ["Ubicacion de las fuerzas policiacas","Total de crimenes y area de la fuerza policiaca","Ubicacion y area de las fuerzas policiacas","Total de reportes para cada tipo de crimen","Total de reportes anuales","Total de reportes mensuales"];

#nombre de los ejes de los scatters
axis2D = [["Latitud","Longitud"],["Total Crimenes","Area de la Fuerza Policiaca"]]
axis3D = ["Latitud","Longitud","Area de la Fuerza Policiaca"]

#for para eliminar la extencion del nombre de los archivos
for i in range(len(files)):
    files[i] = files[i][:-4]

#lista para guardar la mejor K de cada archivo para cada algoritmo
best_K = []
for i in range(len(files)):
    best_K.append([0]*4)


# In[3]:


count = 0
for i in files:
    #lectura del dataset con pandas
    dataset = pd.read_csv("./datasets/"+i+".csv", header=None)
    
    #obtenemos la dimencionalidad del dataset
    D = len(dataset.columns)-1
    
    #eliminamos el nombre de las fuerzas del dataset
    del dataset[0]
    
    #normalizacion de los datos del dataset
    dataset = StandardScaler().fit_transform(dataset)
    
    #lista para guardar el resultado de la metrica silhouette_score
    result_silhouette_score = []
    for i in range(0,4):
        result_silhouette_score.append([0.0]*40)
    
    j = 0
    for K in range(2,42):
        #ejecusion de KMeans
        labels_kmeans = KMeans(n_clusters=K, random_state=random_state).fit_predict(dataset)

        #ejecucion de HAC averange linkage
        labels_HAC_averange = AgglomerativeClustering(n_clusters=K, linkage="average").fit_predict(dataset)
    
        #ejecucion de HAC single linkage
        links = linkage(dataset,"single")
        labels_HAC_single = fcluster(links,K,criterion="maxclust")
    
        #ejecucion de HAC complete linkage
        labels_HAC_complete = AgglomerativeClustering(n_clusters=K, linkage="complete").fit_predict(dataset)
    
        #calculo de la metrica ARI para los algoritmos de clustering
        result_silhouette_score[0][j] = silhouette_score(dataset,labels_kmeans)
        result_silhouette_score[1][j] = silhouette_score(dataset,labels_HAC_averange)
        result_silhouette_score[2][j] = silhouette_score(dataset,labels_HAC_single)
        result_silhouette_score[3][j] = silhouette_score(dataset,labels_HAC_complete)
        j += 1
        
    #obtencion del mejor K de los algoritmos
    best_K[count][0] = result_silhouette_score[0].index(max(result_silhouette_score[0]))+2#kmeans
    best_K[count][1] = result_silhouette_score[1].index(max(result_silhouette_score[1]))+2#HAC_averange
    best_K[count][2] = result_silhouette_score[2].index(max(result_silhouette_score[2]))+2#HAC_single
    best_K[count][3] = result_silhouette_score[3].index(max(result_silhouette_score[3]))+2#HAC_complete
        
    #creamos la figura para la grafica de lineas
    fig = plot.figure(figsize=(18,6))
    ax = fig.add_subplot(111)

    #asignamos los titulos de los ejes x y y
    plot.xlabel("Numero de Clusters (K)",fontsize=14,fontweight="bold")
    plot.ylabel("Mean Silhouette Coefficient",fontsize=14,fontweight="bold")

    #activamos la cuadricula de la grafica
    plot.grid(True,color="black",linewidth=1)

    #asignamos los ticks de los ejes x y y
    plot.xticks(range(40),range(2,42),fontsize=14,fontweight="bold")
    plot.yticks(fontsize=14,fontweight="bold")

    #graficamos las curvas en la grafica
    colors = ["red","blue","brown","black"]
    for line in range(4):
        plot.plot(range(40), result_silhouette_score[line], '-',color=colors[line],linewidth=3)

    #ponemos la leyenda de la grafica
    plot.legend(["Kmeans","HAC average linkage","HAC single linkage","HAC complete linkage"],prop = {"size":14,"weight":"bold"}, loc = 1)

    #asignacion del titulo a la figura
    plot.suptitle(name[count],fontsize=14,fontweight="bold")
        
    #guardamos la figura en una imagen
    plot.savefig("GRAFICA: "+name[count])
        
    #cerramos el plot
    plot.close()

    count += 1


# In[4]:


count = 0
for i in files:
    #lectura del dataset con pandas
    dataset = pd.read_csv("./datasets/"+i+".csv", header=None)
    
    #obtenemos la dimencionalidad del dataset
    D = len(dataset.columns)-1
     
    #eliminamos el nombre de las fuerzas del dataset
    del dataset[0]
    
    #normalizacion de los datos del dataset
    dataset = StandardScaler().fit_transform(dataset)
        
    if(D == 2):

        #ejecusion de KMeans
        labels_kmeans = KMeans(n_clusters=best_K[count][0], random_state=random_state).fit_predict(dataset)
        
        #ejecucion de HAC averange linkage
        labels_HAC_averange = AgglomerativeClustering(n_clusters=best_K[count][1], linkage="average").fit_predict(dataset)
    
        #ejecucion de HAC single linkage
        links = linkage(dataset,"single")
        labels_HAC_single = fcluster(links,best_K[count][2],criterion="maxclust")
    
        #ejecucion de HAC complete linkage
        labels_HAC_complete = AgglomerativeClustering(n_clusters=best_K[count][3], linkage="complete").fit_predict(dataset)
        
        #creamos la figura para los scatterplots
        figure = plot.figure(figsize=(10, 10))
         
        #creamos el scatter plot del Kmeans
        plot.subplot(221)
        plot.scatter(dataset[:, 0], dataset[:, 1], c=labels_kmeans, linewidth=1)
        plot.title("KMeans",fontsize=18,fontweight="bold")
        plot.xlabel(axis2D[count][0],fontsize=14,fontweight="bold")
        plot.ylabel(axis2D[count][1],fontsize=14,fontweight="bold")
        plot.xticks([])
        plot.yticks([])
        
        #creamos el scatter plot del HAC Average
        plot.subplot(222)
        plot.scatter(dataset[:, 0], dataset[:, 1], c=labels_HAC_averange, linewidth=1)
        plot.title("HAC Average linkage",fontsize=18,fontweight="bold")
        plot.xlabel(axis2D[count][0],fontsize=14,fontweight="bold")
        plot.ylabel(axis2D[count][1],fontsize=14,fontweight="bold")
        plot.xticks([])
        plot.yticks([])
        
        #creamos el scatter plot del HAC single
        plot.subplot(223)
        plot.scatter(dataset[:, 0], dataset[:, 1], c=labels_HAC_single, linewidth=1)
        plot.title("HAC Single linkage",fontsize=18,fontweight="bold")
        plot.xlabel(axis2D[count][0],fontsize=14,fontweight="bold")
        plot.ylabel(axis2D[count][1],fontsize=14,fontweight="bold")
        plot.xticks([])
        plot.yticks([])
        
        #creamos el scatter plot del HAC complete
        plot.subplot(224)
        plot.scatter(dataset[:, 0], dataset[:, 1], c=labels_HAC_complete, linewidth=1)
        plot.title("HAC Complete linkage",fontsize=18,fontweight="bold")
        plot.xlabel(axis2D[count][0],fontsize=14,fontweight="bold")
        plot.ylabel(axis2D[count][1],fontsize=14,fontweight="bold")
        plot.xticks([])
        plot.yticks([])
        
        #asignacion del titulo a la figura
        plot.suptitle(name[count],fontsize=18,fontweight="bold")
        
        #guardamos la figura en una imagen
        plot.savefig("SCATTER: "+name[count])
        
        #cerramos el plot
        plot.close()    
    
    if(D == 3):
        
        #ejecusion de KMeans
        labels_kmeans = KMeans(n_clusters=best_K[count][0], random_state=random_state).fit_predict(dataset)
        
        #ejecucion de HAC averange linkage
        labels_HAC_averange = AgglomerativeClustering(n_clusters=best_K[count][1], linkage="average").fit_predict(dataset)
    
        #ejecucion de HAC single linkage
        links = linkage(dataset,"single")
        labels_HAC_single = fcluster(links,best_K[count][2],criterion="maxclust")
    
        #ejecucion de HAC complete linkage
        labels_HAC_complete = AgglomerativeClustering(n_clusters=best_K[count][3], linkage="complete").fit_predict(dataset)
        
        #creamos la figura para los scatterplots
        figure = plot.figure(figsize=(10, 10))
        
        #creamos el scatter plot del Kmeans
        ax = figure.add_subplot(221, projection="3d")
        ax.scatter(dataset[:, 0], dataset[:, 1], dataset[:, 2], c=labels_kmeans, linewidth=1)
        ax.text2D(0.05, 0.95, "KMeans",fontsize=18,fontweight="bold", transform=ax.transAxes)
        ax.set_xlabel(axis3D[0],fontsize=14,fontweight="bold")
        ax.set_ylabel(axis3D[1],fontsize=14,fontweight="bold")
        ax.set_zlabel(axis3D[2],fontsize=14,fontweight="bold")
        
        #creamos el scatter plot del HAC Average
        ax = figure.add_subplot(222, projection="3d")
        ax.scatter(dataset[:, 0], dataset[:, 1], dataset[:, 2], c=labels_HAC_averange, linewidth=1)
        ax.text2D(0.05, 0.95, "HAC Average linkage",fontsize=18,fontweight="bold", transform=ax.transAxes)            
        ax.set_xlabel(axis3D[0],fontsize=14,fontweight="bold")
        ax.set_ylabel(axis3D[1],fontsize=14,fontweight="bold")
        ax.set_zlabel(axis3D[2],fontsize=14,fontweight="bold")
        
        #creamos el scatter plot del HAC single
        ax = figure.add_subplot(223, projection="3d")
        ax.scatter(dataset[:, 0], dataset[:, 1], dataset[:, 2], c=labels_HAC_single, linewidth=1)
        ax.text2D(0.05, 0.95, "HAC Single linkage",fontsize=18,fontweight="bold", transform=ax.transAxes)            
        ax.set_xlabel(axis3D[0],fontsize=14,fontweight="bold")
        ax.set_ylabel(axis3D[1],fontsize=14,fontweight="bold")
        ax.set_zlabel(axis3D[2],fontsize=14,fontweight="bold")
        
        #creamos el scatter plot del HAC complete
        ax = figure.add_subplot(224, projection="3d")
        ax.scatter(dataset[:, 0], dataset[:, 1], dataset[:, 2], c=labels_HAC_complete, linewidth=1)
        ax.text2D(0.05, 0.95, "HAC Complete linkage", fontsize=18, fontweight="bold", transform=ax.transAxes)            
        ax.set_xlabel(axis3D[0],fontsize=14,fontweight="bold")
        ax.set_ylabel(axis3D[1],fontsize=14,fontweight="bold")
        ax.set_zlabel(axis3D[2],fontsize=14,fontweight="bold")

        #asignacion del titulo a la figura
        plot.suptitle(name[count],fontsize=18,fontweight="bold")
        
        #guardamos la figura en una imagen
        plot.savefig("SCATTER: "+name[count])
        
        #cerramos el plot
        plot.close()
    count += 1

