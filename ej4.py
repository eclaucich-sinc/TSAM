import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. Implementación de FastICA Deflacionario
# ==========================================
def centrar(X):
    return X - np.mean(X, axis=1, keepdims=True)

def blanquear(X):
    # Descomposición de la matriz de covarianza
    cov = np.cov(X)
    autovalores, autovectores = np.linalg.eigh(cov)
    # Matriz D^(-1/2)
    D_inv_sqrt = np.diag(1.0 / np.sqrt(autovalores + 1e-10))
    # Matriz de blanqueo: E * D^(-1/2) * E^T
    matriz_blanqueo = autovectores.dot(D_inv_sqrt).dot(autovectores.T)
    X_blanqueada = matriz_blanqueo.dot(X)
    return X_blanqueada, matriz_blanqueo

def fastica_deflacionario(X_w, n_componentes, max_iter=1000, tol=1e-5):
    n_caracteristicas, n_muestras = X_w.shape
    W = np.zeros((n_componentes, n_caracteristicas))
    
    # Función de contraste g(u) = tanh(u) y su derivada
    def g(u): return np.tanh(u)
    def g_prime(u): return 1 - np.tanh(u)**2
    
    for i in range(n_componentes):
        # Inicializar vector w aleatorio
        w = np.random.rand(n_caracteristicas)
        w = w / np.linalg.norm(w)
        
        for iteracion in range(max_iter):
            # Proyección w^T X
            u = np.dot(w.T, X_w)
            
            # Actualización de pesos
            w_nuevo = np.mean(X_w * g(u), axis=1) - np.mean(g_prime(u)) * w
            
            # Ortogonalización de Gram-Schmidt (Aprendizaje deflacionario)
            if i > 0:
                w_nuevo -= np.dot(np.dot(W[:i], w_nuevo), W[:i])
                
            w_nuevo = w_nuevo / np.linalg.norm(w_nuevo)
            
            # Condición de convergencia (w y w_nuevo apuntan en la misma dirección)
            if np.abs(np.abs(np.dot(w.T, w_nuevo)) - 1) < tol:
                break
            w = w_nuevo
            
        W[i, :] = w
    return W

# ==========================================
# 2. Generación de Datos y Resolución (Inciso a)
# ==========================================
np.random.seed(42)
n_muestras = 2000

# Fuentes laplacianas (Componentes Independientes)
s1 = np.random.laplace(size=n_muestras)
s2 = np.random.laplace(size=n_muestras)
S = np.vstack((s1, s2))

# Matriz de mezcla A aleatoria
A = np.array([[1.5, 0.8], 
              [0.6, 1.2]])

# Mezclas observables X
X = np.dot(A, S)

# Preprocesamiento ICA
X_c = centrar(X)
X_w, matriz_blanqueo = blanquear(X_c)

# Ejecución de FastICA
W_ica = fastica_deflacionario(X_w, n_componentes=2)
# Matriz de separación global W = W_ica * matriz_blanqueo
W_global = np.dot(W_ica, matriz_blanqueo)

# Señales separadas Y
Y = np.dot(W_global, X_c)

# Graficar las 4 etapas
fig, axes = plt.subplots(1, 4, figsize=(16, 4))
etapas = [(S, 'Fuentes Originales (S)'), (X, 'Mezclas Observables (X)'), 
          (X_w, 'Señales Blanqueadas (X_w)'), (Y, 'Señales Separadas (Y)')]

for ax, (datos, titulo) in zip(axes, etapas):
    ax.scatter(datos[0, :], datos[1, :], alpha=0.3, color='teal', s=10)
    ax.set_title(titulo)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Imprimir matrices para los incisos b y c
print("Matriz Mezcla (A):\n", A)
print("\nMatriz Inversa de A (A^-1):\n", np.linalg.inv(A))
print("\nMatriz de Separación Global (W):\n", W_global)
print("\nProducto W * A (Matriz G):\n", np.dot(W_global, A).round(2))