# Trabajo Práctico 2: Clasificación Estadística de Patrones

Este documento resume los resultados y las lecciones clave extraídas de la implementación de clasificadores estadísticos en Python. Se abordó el problema de clasificación desde escenarios analíticos ideales hasta la estimación paramétrica sobre corpus de datos empíricos.


## 1. Clasificadores Lineales y Regiones de Decisión

En la primera sección del ejercicio se analizó un clasificador geométrico con tres funciones discriminantes lineales genéricas (g1, g2, g3). Al carecer de términos cuadráticos, las fronteras donde dos clases "empatan" en puntaje (ejemplo, g1(x) = g2(x)) resultaron invariablemente en ecuaciones de rectas (hiperplanos en el espacio bidimensional).

La regla de decisión establece que un patrón pertenece a la región Ri si gi(x) maximiza el puntaje. Las tres fronteras calculadas se intersectaron en un único punto (0.5, 0), dividiendo el plano cartesiano en tres cuñas infinitas. La evaluación puntual de nuevas coordenadas demostró que la clasificación se reduce a un simple problema de álgebra vectorial.

!!! note El Clasificador Gaussiano Isotrópico (Caso 1)

    Se demostró que si dos clases (A y B) tienen la misma probabilidad a priori y matrices de covarianza idénticas a la matriz identidad (Σ = I), el clasificador de Bayes se degrada elegantemente a un clasificador de mínima distancia euclídea. Geométricamente, las nubes de datos son esféricas y del mismo tamaño, por lo que la frontera de decisión óptima resultó ser la mediatriz exacta entre ambas medias (la recta x1 = x2).


## 2. Estimación de Parámetros por Máxima Verosimilitud (ML)

Al procesar el mini-corpus de datos reales con múltiples clases, abandonamos el mundo de los parámetros ideales (asumidos) para entrar en el aprendizaje basado en datos. Dado que desconocíamos la distribución poblacional original, utilizamos la técnica de Máxima Verosimilitud para extraer la "firma" estadística de cada clase directamente de las muestras de entrenamiento.
Tópicos Selectos de Aprendizaje Maquinal Página 1

El proceso implicó calcular el vector de medias (μ) y la matriz de covarianza empírica (Σ) filtrando el dataset por cada etiqueta de clase. Asimismo, se calculó la probabilidad a priori P(ωi) como la frecuencia relativa de aparición de cada clase en el corpus original. Con estos parámetros, instanciamos el Caso 3 del Clasificador Gaussiano (covarianzas arbitrarias y distintas), lo que habilitó al modelo a trazar fronteras hipercuádricas, ajustándose a la rotación y dispersión particular de cada grupo.

| Estructura de la Matriz (Σ) | Forma de la Nube de Datos |	Frontera de Decisión Resultante |
| :--- | :--- | :--- |
| Σ = σ2 I (Caso 1) | Esférica (Isotrópica). Todas las variables tienen misma varianza y 0 correlación. | Lineal (Hiperplano). Equivale a clasificar por mínima distancia euclídea. |
| Σi = Σ (Caso 2) | Hiperelíptica, pero idéntica para todas las clases en tamaño y rotación. | Lineal (Hiperplano). Equivale a la distancia de Mahalanobis. |
| Σi Arbitraria (Caso 3) | Hiperelíptica. Cada clase tiene su propio volumen, dispersión y ángulo de rotación. | Cuadrática (Hipercuádricas: parábolas, elipses, hipérbolas). |


## 3. Validación y Generalización

Una conclusión vital del ejercicio radicó en la capacidad de generalización del clasificador paramétrico. Al generar un volumen grande de datos de prueba sintéticos utilizando las distribuciones normales ajustadas en el entrenamiento (μ y Σ empíricas), observamos que la tasa de aciertos (Accuracy) se mantuvo sumamente estable e incluso similar a la obtenida sobre los datos de entrenamiento.

Esto demuestra la potencia del modelado generativo subyacente al Teorema de Bayes: al capturar correctamente la FDP real que gobierna la emisión de los datos, el clasificador se vuelve robusto ante muestras inéditas, siempre y cuando estas respeten el supuesto de normalidad que sustenta la arquitectura del modelo.
