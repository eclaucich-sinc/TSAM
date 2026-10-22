import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal

# ==========================================
# Ejercicio 2.1: Clasificador Geométrico Lineal
# ==========================================
def plot_ejercicio_1():
    x1, x2 = np.mgrid[-2:4:0.02, -2:3:0.02]
    
    # Evaluar discriminantes en toda la grilla
    g1 = -x1
    g2 = x1 + x2 - 1
    g3 = x1 - x2 - 1
    
    # Encontrar la clase ganadora por cada punto
    G = np.dstack((g1, g2, g3))
    clases = np.argmax(G, axis=2) + 1  # Clases 1, 2, 3
    
    plt.figure(figsize=(7, 5))
    plt.contourf(x1, x2, clases, alpha=0.3, cmap='Set2')
    
    # Graficar rectas (Fronteras)
    x1_line = np.linspace(-2, 4, 100)
    plt.plot(x1_line, -2*x1_line + 1, 'k--', label='Frontera 1-2')
    plt.plot(x1_line, 2*x1_line - 1, 'k-.', label='Frontera 1-3')
    plt.axhline(0, color='k', linestyle=':', label='Frontera 2-3')

    # Graficar los puntos a clasificar
    puntos = np.array([[2, 1], [2, -1], [-1, 1], [-1, -1]])
    etiquetas = ['(2,1)', '(2,-1)', '(-1,1)', '(-1,-1)']
    plt.scatter(puntos[:,0], puntos[:,1], c='red', zorder=5, s=60)
    for p, eq in zip(puntos, etiquetas):
        plt.text(p[0]+0.1, p[1]+0.1, eq, fontweight='bold')
    
    plt.xlim(-2, 4)
    plt.ylim(-2, 3)
    plt.title('2.1 Regiones de Decisión y Clasificación de Puntos')
    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.legend()
    plt.show()

# ==========================================
# Ejercicio 2.2: Clasificador Gaussiano (Caso 1)
# ==========================================
def plot_ejercicio_2():
    mu_a, mu_b = np.array([3, 0]), np.array([0, 3])
    cov = np.eye(2) # Identidad
    
    x1, x2 = np.mgrid[-2:6:0.05, -2:6:0.05]
    pos = np.dstack((x1, x2))
    
    pdf_a = multivariate_normal(mu_a, cov).pdf(pos)
    pdf_b = multivariate_normal(mu_b, cov).pdf(pos)
    
    plt.figure(figsize=(6, 6))
    plt.contour(x1, x2, pdf_a, colors='blue', alpha=0.5)
    plt.contour(x1, x2, pdf_b, colors='red', alpha=0.5)
    
    # Graficar frontera x1 = x2
    plt.plot([-2, 6], [-2, 6], 'g-', lw=2, label='Frontera de decisión ($x_1=x_2$)')
    
    plt.scatter(*mu_a, c='blue', marker='X', s=100, label='Media Clase A')
    plt.scatter(*mu_b, c='red', marker='X', s=100, label='Media Clase B')
    
    plt.title('2.2 Clasificador Gaussiano y Frontera Lineal')
    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

# ==========================================
# Ejercicio 2.3: Clasificador ML (Generando mini-corpus)
# ==========================================
def plot_ejercicio_3(ruta_archivo='gaussDATA.txt'):
    # 1. Cargar datos (Asegurate de que el txt esté en la misma carpeta)
    try:
        datos = np.loadtxt(ruta_archivo)
    except FileNotFoundError:
        print(f"No se encontró {ruta_archivo}. Por favor, verificá la ruta.")
        return

    X_train = datos[:, :2]
    y_train = datos[:, 2].astype(int)
    clases = np.unique(y_train)
    N_total = len(y_train)
    
    # Diccionarios para guardar los parámetros estimados por clase
    params_ml = {}
    
    # 2. Estimación por Máxima Verosimilitud (ML)
    for c in clases:
        X_c = X_train[y_train == c]
        N_c = len(X_c)
        
        # Estimadores ML: Prior, Media y Covarianza
        prior = N_c / N_total
        mu = np.mean(X_c, axis=0)
        cov = np.cov(X_c, rowvar=False)
        
        params_ml[c] = {'prior': prior, 'mu': mu, 'cov': cov}
        print(f"Clase {c}: Prior={prior:.2f}, Media={mu.round(2)}")

    # Función Discriminante Cuadrática (Caso 3)
    def predecir_bayes(X, parametros):
        puntajes = np.zeros((X.shape[0], len(parametros)))
        
        for idx, c in enumerate(parametros.keys()):
            mu = parametros[c]['mu']
            cov = parametros[c]['cov']
            prior = parametros[c]['prior']
            
            inv_cov = np.linalg.inv(cov)
            det_cov = np.linalg.det(cov)
            diff = X - mu
            
            # g_i(x) = -0.5*(x-mu)^T * Cov^-1 * (x-mu) - 0.5*log(|Cov|) + log(P(w_i))
            term1 = -0.5 * np.sum(diff.dot(inv_cov) * diff, axis=1)
            term2 = -0.5 * np.log(det_cov)
            term3 = np.log(prior)
            
            puntajes[:, idx] = term1 + term2 + term3
            
        # Retorna la clase con el máximo discriminante
        return np.array(list(parametros.keys()))[np.argmax(puntajes, axis=1)]    

        
    # 3. Clasificar datos de entrenamiento y calcular tasa de aciertos
    y_pred_train = predecir_bayes(X_train, params_ml)
    acc_train = np.mean(y_pred_train == y_train) * 100
    
    # 4. Generar datos de prueba sintéticos desde los parámetros modelados
    X_test_list, y_test_list = [], []
    for c in clases:
        # Generamos 200 muestras sintéticas por clase
        X_sintetico = np.random.multivariate_normal(params_ml[c]['mu'], params_ml[c]['cov'], 200)
        X_test_list.append(X_sintetico)
        y_test_list.append(np.full(200, c))
        
    X_test = np.vstack(X_test_list)
    y_test = np.concatenate(y_test_list)
    
    y_pred_test = predecir_bayes(X_test, params_ml)
    acc_test = np.mean(y_pred_test == y_test) * 100
    
    # 5. Representación gráfica
    plt.figure(figsize=(9, 7))
    
    # Crear grilla para pintar regiones de decisión
    x_min, x_max = X_train[:, 0].min() - 2, X_train[:, 0].max() + 2
    y_min, y_max = X_train[:, 1].min() - 2, X_train[:, 1].max() + 2
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.05),
                         np.arange(y_min, y_max, 0.05))
    
    grilla_puntos = np.c_[xx.ravel(), yy.ravel()]
    predicciones_grilla = predecir_bayes(grilla_puntos, params_ml)
    Z = np.array(predicciones_grilla).reshape(xx.shape)
    
    # Dibujar regiones
    plt.contourf(xx, yy, Z, alpha=0.3, cmap='tab10')
    
    # Superponer datos originales
    scatter = plt.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap='tab10', 
                          edgecolor='k', s=50, label='Entrenamiento')
    
    plt.title(f'Clasificador Gaussiano Multiclase\nAcc Train: {acc_train:.1f}% | Acc Test Sintético: {acc_test:.1f}%')
    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.legend(*scatter.legend_elements(), title="Clases")
    plt.grid(True, alpha=0.3)
    plt.show()

# Ejecutar las funciones
plot_ejercicio_1()
plot_ejercicio_2()
plot_ejercicio_3()