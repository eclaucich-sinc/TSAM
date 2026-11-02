import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import glob
from ej3_1 import PCA

# ==========================================
# 2. Preprocesamiento de Imágenes (Inciso a)
# ==========================================
def cargar_y_procesar_imagenes(directorio, tamano=(32, 32)):
    rutas_imagenes = glob.glob(os.path.join(directorio, '*.jpg'))
    if len(rutas_imagenes) != 112:
        print(f"Advertencia: Se esperaban 112 imágenes, pero se encontraron {len(rutas_imagenes)}.")
    
    matriz_datos = []
    
    for ruta in rutas_imagenes:
        # Abrir imagen, convertir a escala de grises ('L') y redimensionar
        img = Image.open(ruta).convert('L').resize(tamano)
        # Convertir a array numpy y aplanar a un vector de 1024 elementos
        img_vector = np.array(img).flatten()
        matriz_datos.append(img_vector)
        
    # Retorna matriz de 112 x 1024
    return np.array(matriz_datos)

# ==========================================
# 3. Ejecución y Visualización (Incisos c y d)
# ==========================================
directorio_tinifaces = 'tinyface_20'

try:
    # a) Obtener matriz de 112x1024
    X_caras = cargar_y_procesar_imagenes(directorio_tinifaces)
    
    # b y c) Aplicar PCA para extraer las 12 primeras Eigenfaces
    pca = PCA(n_components=12)
    pca.fit(X_caras)
    
    # d) Graficar las 12 Eigenfaces en un arreglo de 4x3
    fig, axes = plt.subplots(3, 4, figsize=(10, 8))
    fig.suptitle('Las primeras 12 Eigenfaces extraídas de Tinyfaces', fontsize=16)
    
    for i, ax in enumerate(axes.flat):
        # Deshacer vectorización: transformar autovector 1024x1 a matriz 32x32
        eigenface_matriz = pca.componentes[:, i].reshape(32, 32)
        
        # Mostrar imagen con mapa de colores en grises
        ax.imshow(eigenface_matriz, cmap='gray')
        ax.set_title(f'Eigenface {i+1}')
        ax.axis('off')
        
    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f"Ocurrió un error al procesar las imágenes: {e}")
    print("Asegurate de que la carpeta 'tinifaces_20' existe y contiene los archivos .jpg.")