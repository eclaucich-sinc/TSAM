import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, multivariate_normal

# Configuración general
N = 10000  # Cantidad de muestras aleatorias
np.random.seed(42)  # Semilla para reproducibilidad

# ==========================================
# Caso i) FDP Gaussiana Unidimensional
# ==========================================
mu_1d = 0.0
sigma_1d = 1.0

# a) Generar números aleatorios
x_1d = np.random.normal(mu_1d, sigma_1d, N)

# b y c) Histograma experimental vs FDP teórica
plt.figure(figsize=(8, 5))
# Histograma normalizado (density=True)
plt.hist(x_1d, bins=50, density=True, alpha=0.6, color='skyblue', edgecolor='black', label='FDP Experimental (Histograma)')

# Curva teórica
x_axis = np.linspace(mu_1d - 4*sigma_1d, mu_1d + 4*sigma_1d, 1000)
pdf_teorica_1d = norm.pdf(x_axis, mu_1d, sigma_1d)
plt.plot(x_axis, pdf_teorica_1d, 'r-', lw=2, label='FDP Teórica')

plt.title('i) Gaussiana Unidimensional')
plt.xlabel('x')
plt.ylabel('Densidad de Probabilidad')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()


# ==========================================
# Casos ii) y iii) FDP Gaussiana Bidimensional
# ==========================================
mu_2d = np.array([0.0, 0.0])

# Matriz de covarianza ii) No correlacionada (Diagonal)
cov_no_corr = np.array([[1.0, 0.0], 
                        [0.0, 1.0]])

# Matriz de covarianza iii) Correlacionada (Valores fuera de la diagonal)
cov_corr = np.array([[1.0, 0.8], 
                     [0.8, 1.0]])

# a) Generar muestras para ambos casos
data_no_corr = np.random.multivariate_normal(mu_2d, cov_no_corr, N)
data_corr = np.random.multivariate_normal(mu_2d, cov_corr, N)

# Grilla para evaluar la FDP teórica bidimensional
x_grid, y_grid = np.mgrid[-3.5:3.5:.05, -3.5:3.5:.05]
pos = np.dstack((x_grid, y_grid))

# Función auxiliar para graficar 2D
def graficar_2d(data, cov_matrix, titulo):
    plt.figure(figsize=(7, 6))
    
    # b) Histograma experimental 2D (Mapa de densidad)
    plt.hist2d(data[:, 0], data[:, 1], bins=40, density=True, cmap='Blues')
    plt.colorbar(label='Densidad empírica')
    
    # c) FDP teórica (Curvas de nivel / Contornos)
    rv = multivariate_normal(mu_2d, cov_matrix)
    contornos = plt.contour(x_grid, y_grid, rv.pdf(pos), colors='red', linewidths=1.5, alpha=0.8)
    plt.clabel(contornos, inline=True, fontsize=8, fmt='%.2f')
    
    plt.title(titulo)
    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.axis('equal')
    plt.show()

# Graficar Caso ii
graficar_2d(data_no_corr, cov_no_corr, 'ii) Gaussiana 2D No Correlacionada\n(Elipses alineadas)')

# Graficar Caso iii
graficar_2d(data_corr, cov_corr, 'iii) Gaussiana 2D Correlacionada\n(Elipses rotadas)')