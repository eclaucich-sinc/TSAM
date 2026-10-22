# Trabajo Práctico 1: Nociones de Probabilidad y Teoría de la Información

El presente informe sintetiza los hallazgos fundamentales obtenidos a partir de las simulaciones numéricas implementadas en el lenguaje de programación Python. El objetivo principal de estos ensayos fue validar empíricamente los conceptos teóricos abordados en clase sobre distribuciones de probabilidad, momentos estadísticos y teoría de la información.

---

## 1. Geometría y Generación de la Distribución Gaussiana

A través de la generación de datos pseudoaleatorios y su contraste con las Funciones de Densidad de Probabilidad (FDP) teóricas, se verificó el profundo impacto que tiene la matriz de covarianza Σ sobre la distribución de las variables en el espacio continuo multivariado.

En el espacio unidimensional, la aproximación a la campana de Gauss dependió críticamente de la cantidad de muestras (N). Al expandir el análisis al espacio bidimensional, la matriz de covarianza demostró ser el mecanismo algebraico exclusivo que define la morfología de la densidad de probabilidad. Se constató que:

!!! note Impacto de la Covarianza en Espacios 2D

    **Variables no correlacionadas**: Cuando los elementos fuera de la diagonal principal son nulos, las elipses de densidad se mantienen ortogonales y alineadas a los ejes coordenados (x1, x2).

    **Variables correlacionadas**: La inyección de valores no nulos fuera de la diagonal resulta en una evidente rotación topológica. El eje mayor de la elipse se alinea matemáticamente con la dirección de varianza máxima dominante.


Esta demostración es crucial para el aprendizaje automático paramétrico, dado que resalta que ignorar las covarianzas (como asume la versión ingenua o Naive de Bayes) fuerza al modelo a aproximar la distribución de los datos con elipses rectas, perdiendo la capacidad de capturar relaciones conjuntas (dependencias lineales) entre las características.
Tópicos Selectos de Aprendizaje Maquinal Página 1

## 2. Demostración Empírica del Teorema del Límite Central

El segundo ensayo consistió en sumar K variables aleatorias extraídas de distribuciones estrictamente uniformes (planas, sin ningún parecido a una campana). Los histogramas mostraron la metamorfosis de la densidad resultante:

* Para K = 1, la distribución se mantiene idéntica a la fuente (uniforme).
* Para K = 2, la densidad adquiere forma de triángulo perfecto, ya que hay más formas combinatorias de sumar valores medios que valores en los extremos.
* Para K ≥ 5, la FDP converge agresiva y rápidamente hacia una distribución Gaussiana canónica.

!!! note Implicancia Práctica

    Este experimento justifica por qué el ruido de medición en los sensores o los errores agregados en casi cualquier dataset asumen naturalmente una forma Gaussiana. Al ser producto de cientos de micro-efectos sumados, la FDP converge invariablemente hacia el modelo Normal.


## 3. Entropía Diferencial y Ley de los Grandes Números

Finalmente, se abordó la estimación numérica de la Entropía Diferencial H(x) basándose en el postulado teórico de que la entropía es la esperanza matemática de la función de sorpresa: $H(x) = E[-ln p(x)]$.

Mediante el principio estadístico de que la media empírica converge al valor esperado, se simuló la fórmula aproximada $H ≈ - (1/T)\sum{ln(p(x_t))}$. La trayectoria de la convergencia en el gráfico demostró que las estimaciones con un volumen de datos pequeño (< 1,000 muestras) sufren de altísima inestabilidad estocástica, evidenciando que los modelos probabilísticos requieren grandes masas de información ($T → \infin$) para asimilar una representación fiel de la distribución subyacente.

| Distribución | Característica de Información (Entropía Diferencial) |  
| :--- | :--- |
| Uniforme 	 | Máxima incertidumbre en un rango acotado. La FDP no tiene pico y todos los valores dentro del dominio proveen la misma "sorpresa". |
| Gaussiana 	| Maximiza sistemáticamente la entropía general entre todas las distribuciones con una misma varianza y media dadas. |
| Laplaciana 	| Exhibe un pico abrupto en la media, concentrando la probabilidad y, comparativamente, presentando colas más largas pero menor entropía en el núcleo. |
