import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from ej3_1 import PCA

# Carga de los 150 ejemplos del dataset Iris
iris = load_iris()
X = iris.data
y = iris.target
nombres_clases = iris.target_names

# Aplicación de la reducción dimensional
pca = PCA(n_components=2)
pca.fit(X)
X_proyectado = pca.transform(X)

# Visualización de la dispersión
plt.figure(figsize=(9, 6))
colores = ['#d62728', '#2ca02c', '#1f77b4']  # Rojo, Verde, Azul

for clase_idx, color, nombre in zip(range(3), colores, nombres_clases):
    plt.scatter(X_proyectado[y == clase_idx, 0], 
                X_proyectado[y == clase_idx, 1], 
                color=color, label=nombre, alpha=0.8, edgecolor='k', s=60)

plt.title('Proyección PCA del Dataset Iris (Reducción de 4D a 2D)')
plt.xlabel('Componente Principal 1')
plt.ylabel('Componente Principal 2')
plt.legend(title='Especies')
plt.grid(True, alpha=0.3)
plt.show()