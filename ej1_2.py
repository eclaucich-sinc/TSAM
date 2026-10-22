import numpy as np
import matplotlib.pyplot as plt

# Configuración
N_muestras = 10000  # Cantidad de sumas a generar
K_valores = [1, 2, 5, 10, 20, 40, 80, 100, 200]  # Cantidad de variables uniformes a sumar en cada prueba
np.random.seed(42)

plt.figure(figsize=(12, 8))

for i, K in enumerate(K_valores, 1):
    # Generar una matriz de K x N_muestras con distribución uniforme entre 0 y 1
    # Cada fila es una variable aleatoria uniforme independiente
    muestras_uniformes = np.random.uniform(0, 1, (K, N_muestras))
    
    # Sumar las K variables (sumar a lo largo de las columnas)
    suma_muestras = np.sum(muestras_uniformes, axis=0)
    
    # Graficar el histograma de la suma
    plt.subplot(3, 3, i)
    plt.hist(suma_muestras, bins=50, density=True, color='mediumseagreen', edgecolor='black', alpha=0.7)
    
    plt.title(f'Suma de K={K} variables uniformes')
    plt.xlabel('Valor de la suma')
    plt.ylabel('Densidad')
    plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()