import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import laplace, norm, uniform

# Configuraciones iniciales
T = 100000
np.random.seed(42)

# 1. Definición de las distribuciones
dist_laplace = laplace(loc=0.0, scale=1.0)
dist_norm = norm(loc=0.0, scale=1.0)
dist_unif = uniform(loc=-2.0, scale=4.0)

# Valores teóricos de entropía diferencial
H_teo_laplace = dist_laplace.entropy()
H_teo_norm = dist_norm.entropy()
H_teo_unif = dist_unif.entropy()

# 2. Generación de muestras aleatorias
muestras_laplace = dist_laplace.rvs(size=T)
muestras_norm = dist_norm.rvs(size=T)
muestras_unif = dist_unif.rvs(size=T)

# Función para calcular la convergencia acumulada de la entropía
def entropia_acumulada(muestras, distribucion):
    pdf_values = distribucion.pdf(muestras)
    pdf_values = np.where(pdf_values == 0, 1e-10, pdf_values) # Evitar log(0)
    
    # Calculamos el promedio acumulado: suma acumulada / índice actual
    promedio_acumulado = -np.cumsum(np.log(pdf_values)) / np.arange(1, T + 1)
    return promedio_acumulado

# Cálculo de las trayectorias
conv_laplace = entropia_acumulada(muestras_laplace, dist_laplace)
conv_norm = entropia_acumulada(muestras_norm, dist_norm)
conv_unif = entropia_acumulada(muestras_unif, dist_unif)

# 3. Creación de los gráficos
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# --- Gráfico 1: Funciones de Densidad de Probabilidad (fdp) ---
x_axis = np.linspace(-5, 5, 1000)
ax1.plot(x_axis, dist_laplace.pdf(x_axis), label='Laplaciana', color='blue', lw=2)
ax1.plot(x_axis, dist_norm.pdf(x_axis), label='Gaussiana', color='red', lw=2)
ax1.plot(x_axis, dist_unif.pdf(x_axis), label='Uniforme', color='green', lw=2)

ax1.set_title('Funciones de Densidad de Probabilidad')
ax1.set_xlabel('x')
ax1.set_ylabel('p(x)')
ax1.legend()
ax1.grid(True, alpha=0.3)

# --- Gráfico 2: Convergencia de la Estimación de Entropía ---
x_muestras = np.arange(1, T + 1)

# Trayectorias empíricas
ax2.plot(x_muestras, conv_laplace, color='blue', alpha=0.6)
ax2.plot(x_muestras, conv_norm, color='red', alpha=0.6)
ax2.plot(x_muestras, conv_unif, color='green', alpha=0.6)

# Líneas horizontales de referencia (Valores teóricos)
ax2.axhline(H_teo_laplace, color='blue', linestyle='--', label=f'Teórico Laplaciana: {H_teo_laplace:.3f}')
ax2.axhline(H_teo_norm, color='red', linestyle='--', label=f'Teórico Gaussiana: {H_teo_norm:.3f}')
ax2.axhline(H_teo_unif, color='green', linestyle='--', label=f'Teórico Uniforme: {H_teo_unif:.3f}')

# Configuración del eje X en escala logarítmica
ax2.set_xscale('log')
ax2.set_title('Convergencia de la Estimación Numérica')
ax2.set_xlabel('Cantidad de Muestras (Escala Logarítmica)')
ax2.set_ylabel('Entropía Diferencial (nats)')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()