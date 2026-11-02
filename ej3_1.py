import numpy as np

class PCA:
    def __init__(self, n_components):
        self.n_components = n_components
        self.componentes = None
        self.media = None

    def fit(self, X):
        # 1. Centrado de los datos
        self.media = np.mean(X, axis=0)
        X_c = X - self.media
        
        # 2. Matriz de covarianza
        # rowvar=False asegura que las columnas representan las características
        covarianza = np.cov(X_c, rowvar=False)
        
        # 3. Descomposición espectral
        autovalores, autovectores = np.linalg.eigh(covarianza)
        
        # 4. Ordenamiento de mayor a menor varianza
        idx = np.argsort(autovalores)[::-1]
        autovectores = autovectores[:, idx]
        
        # 5. Construcción de la matriz de proyección W
        self.componentes = autovectores[:, :self.n_components]

    def transform(self, X):
        # Proyección ortogonal sobre el nuevo subespacio latente
        X_c = X - self.media
        return np.dot(X_c, self.componentes)