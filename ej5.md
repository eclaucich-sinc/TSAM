# Ejercicio 5: Aprendizaje por refuerzo pasivo

**Tópicos Selectos en Aprendizaje Maquinal — TP N°1: Algoritmos para Reconocimiento de Patrones**

Este ejercicio es de "lápiz y papel": se estudia un problema de juguete (el mundo de grilla de $4\times3$) para entender cómo se define y se evalúa una **política** en un problema de decisión secuencial con incertidumbre.

| Inciso | Consigna | Qué se hace |
|:--|:--|:--|
| **5.1** | Encontrar la política óptima para un agente pasivo en el mundo de $4\times3$ (recompensa $-0.04$ en los estados no terminales) | Determinar qué acción conviene en cada estado |
| **5.2** | Calcular las utilidades de los estados dada la política óptima | Resolver un sistema de 9 ecuaciones lineales |

---

## 0. Resumen: qué hay que hacer en lápiz y papel

> **Orden recomendado.** Para *verificar* que la política del 5.1 es óptima hacen falta las utilidades del 5.2, así que conviene: (1) proponer la política razonando, (2) calcular las utilidades (5.2) y (3) volver a verificar la política (5.1).

**Ejercicio 5.1 — política óptima**

- [ ] **Dibujar la grilla** de $4\times3$ con las coordenadas (columna, fila), la pared en $(2,2)$, los terminales $+1$ en $(4,3)$ y $-1$ en $(4,2)$ y el inicio en $(1,1)$ (sección 1).
- [ ] **Razonar la política** estado por estado (sección 3.1) y dibujarla con **flechas** en cada casilla.
- [ ] **Verificar la optimalidad** en los estados donde la decisión no es obvia, $(4,1)$, $(3,1)$, $(1,1)$ y $(3,2)$, comparando el valor de las acciones con la ecuación de Bellman (sección 3.3). Es la parte más "de cuentas" del 5.1.

**Ejercicio 5.2 — utilidades**

- [ ] **Escribir las 9 ecuaciones** de Bellman para la política fija, una por cada estado no terminal (sección 4.2).
- [ ] **Resolver por sustitución** (el sistema se simplifica mucho; sección 4.3).
- [ ] **Dibujar la grilla con las utilidades** en cada casilla.

**Qué gráficas incluir:** (a) la grilla con la política (flechas) y (b) la grilla con las utilidades. Más abajo hay un lugar marcado para cada una.

---

## 1. El problema

El agente vive en una grilla de $4\times3$. Se usa la notación $(x,y)$: $x$ es la **columna** (1 a 4, de izquierda a derecha) e $y$ es la **fila** (1 a 3, de abajo hacia arriba), de modo que el inicio es $(1,1)$ y el estado $+1$ es $(4,3)$.

| fila \ columna | **1** | **2** | **3** | **4** |
|:--:|:--:|:--:|:--:|:--:|
| **3** | $(1,3)$ | $(2,3)$ | $(3,3)$ | **+1** (terminal) |
| **2** | $(1,2)$ | *pared* | $(3,2)$ | **−1** (terminal) |
| **1** | **START** $(1,1)$ | $(2,1)$ | $(3,1)$ | $(4,1)$ |

- Hay $11$ casillas transitables (12 menos la pared) y 2 de ellas son terminales; por lo tanto hay **9 estados no terminales**.
- Al llegar a un estado terminal, el episodio termina y se cobra su recompensa ($+1$ o $-1$).
- En cada estado **no terminal** el agente cobra una recompensa de $R(s)=-0.04$ por paso (un "costo de vivir" que lo empuja a terminar rápido).

### Supuestos del modelo

El enunciado no los escribe, pero son los del problema clásico de Russell y Norvig (*Inteligencia Artificial: Un enfoque moderno*, cap. 17 y 21), y con ellos se reproducen los resultados de la guía:

- **Acciones:** arriba ($\uparrow$), abajo ($\downarrow$), izquierda ($\leftarrow$) y derecha ($\rightarrow$).
- **Modelo de transición estocástico:** el movimiento sale como se pidió con probabilidad $0.8$; con probabilidad $0.1$ el agente se desvía hacia cada uno de los dos lados perpendiculares. Por ejemplo, con $\uparrow$: sube con $0.8$, va a la izquierda con $0.1$ y a la derecha con $0.1$.
- **Choques:** si el movimiento llevaría al agente contra la pared o fuera de la grilla, **se queda donde está**.
- **Factor de descuento** $\gamma=1$ (sin descuento). Es razonable porque el episodio siempre termina.
- **Utilidad de un estado** = suma esperada de las recompensas que se acumulan hasta el final.

---

## 2. Conceptos

### 2.1 Proceso de decisión de Markov (MDP)

El problema es un **MDP**, definido por: un conjunto de estados $S$, un conjunto de acciones $A$, un modelo de transición $P(s'\mid s,a)$ (probabilidad de llegar a $s'$ al ejecutar $a$ en $s$), una función de recompensa $R(s)$ y un factor de descuento $\gamma$. La propiedad de Markov dice que la transición depende solo del estado y la acción actuales, no de la historia.

### 2.2 Política

Una **política** $\pi$ es una regla que dice qué acción ejecutar en cada estado, $\pi:S\to A$. Como el entorno es estocástico, aplicar $\pi$ no produce una única secuencia de estados sino una **distribución** de secuencias posibles. Por eso una política no se evalúa por un solo recorrido, sino por su resultado **esperado**.

Para acciones fijas por estado (política *determinista*), la política se puede dibujar como una flecha en cada casilla.

### 2.3 Utilidad de un estado

La **utilidad** de un estado bajo la política $\pi$ es la recompensa total esperada al seguir $\pi$ desde $s$:

$$
U^{\pi}(s)=E\left[\sum_{t=0}^{\infty}\gamma^{t}R(s_t)\;\Big|\;s_0=s,\ \pi\right].
$$

Esta definición lleva a la **ecuación de Bellman para una política fija**: la utilidad de un estado es la recompensa inmediata más la utilidad esperada del estado siguiente,

$$
\boxed{U^{\pi}(s)=R(s)+\gamma\sum_{s'}P\big(s'\mid s,\pi(s)\big)\,U^{\pi}(s')}
$$

con $U(s)=R(s)$ en los estados terminales. Si hay $n$ estados no terminales, estas son $n$ ecuaciones **lineales** con $n$ incógnitas: se pueden resolver exactamente (inciso 5.2).

### 2.4 Política óptima y ecuación de Bellman de optimalidad

La política **óptima** $\pi^*$ es la que maximiza la utilidad esperada en todos los estados. Su utilidad $U(s)=U^{\pi^*}(s)$ cumple la **ecuación de Bellman de optimalidad**:

$$
\boxed{U(s)=R(s)+\gamma\max_{a}\sum_{s'}P(s'\mid s,a)\,U(s')}
\qquad\Longrightarrow\qquad
\pi^*(s)=\arg\max_{a}\sum_{s'}P(s'\mid s,a)\,U(s').
$$

Es decir, **la política óptima es "codiciosa" respecto de las utilidades óptimas**: en cada estado elige la acción que lleva, en promedio, a los estados de mayor utilidad. Esta es la herramienta para verificar a mano si una política propuesta es óptima. Se calcula, para cada acción posible, el valor esperado $\sum_{s'}P(s'\mid s,a)\,U(s')$ y se comprueba que la acción de la política es la mayor.

Cuando el modelo se conoce, se puede obtener la política óptima numéricamente con **iteración de valor** (se aplica la ecuación de Bellman de optimalidad como actualización, empezando de $U=0$, hasta que converge) o con **iteración de política** (se alterna evaluar una política y mejorarla).

### 2.5 ¿Qué significa "pasivo" aquí?

En **aprendizaje por refuerzo pasivo** la política $\pi$ está **fija** y la tarea del agente es *aprender cuánto vale* $U^{\pi}(s)$; no decide qué hacer, solo ejecuta $\pi$ y observa. (Cuando además tiene que decidir qué política seguir, el aprendizaje es **activo**.) Cuando el modelo de transición es **desconocido**, se estima $U^\pi$ a partir de *experiencias* mediante:

- **estimación directa de la utilidad:** promediar los retornos observados desde cada estado;
- **programación dinámica adaptativa (ADP):** estimar el modelo $P(s'\mid s,a)$ de las observaciones y resolver Bellman;
- **diferencias temporales (TD):** actualizar $U^\pi(s)\leftarrow U^\pi(s)+\alpha\,[R(s)+\gamma U^\pi(s')-U^\pi(s)]$ tras cada transición observada.

En este ejercicio el modelo **sí se conoce**, así que ambos incisos se resuelven directamente con las ecuaciones de Bellman, sin necesidad de aprender de experiencia: el 5.1 es de *planificación* (hallar $\pi^*$) y el 5.2 es de *evaluación de política* (hallar $U^{\pi^*}$).

### 2.6 Las secuencias de la Figura 2

Las dos secuencias de la guía son **recorridos (episodios)** posibles en el mundo (cada estado va acompañado de su recompensa):

$$
\text{(a)}\;\; (1,1)_{-.04}\to(1,2)_{-.04}\to(1,3)_{-.04}\to(1,2)_{-.04}\to(1,3)_{-.04}\to(2,3)_{-.04}\to(3,3)_{-.04}\to(4,3)_{+1}
$$

$$
\text{(b)}\;\; (1,1)_{-.04}\to(2,1)_{-.04}\to(3,1)_{-.04}\to(3,2)_{-.04}\to(4,2)_{-1}
$$

Sirven para entender que el resultado de una política es **aleatorio**:

- **(a)** acumula $7\times(-0.04)+1=\mathbf{+0.72}$. Recorre la ruta larga y segura por la izquierda y arriba. Pasa dos veces por $(1,3)$ porque en algún paso el agente se "resbaló" hacia abajo ($0.1$ de probabilidad) y tuvo que volver a subir.
- **(b)** acumula $4\times(-0.04)-1=\mathbf{-1.16}$. Toma la ruta corta por abajo y termina en el estado $-1$.
- La secuencia (b) **no puede** provenir de la política óptima: desde $(2,1)$ la política óptima elige $\leftarrow$, y con esa acción es imposible moverse hacia la derecha. Corresponde a otra política (una que "va por abajo"). Ilustra por qué hay que *comparar* políticas por su utilidad esperada, y no por una sola corrida.

---

## 3. Ejercicio 5.1: política óptima

> *Encontrar la política óptima para un agente pasivo en el mundo de $4\times3$ de la Figura 1, con recompensa $-0.04$ en los estados no terminales.*

### 3.1 Razonamiento para proponer la política

La idea es combinar el *costo de vivir* con el *riesgo* de caer en el estado $-1$.

1. **El costo por paso es pequeño** ($-0.04$): no vale la pena arriesgarse para ahorrar unos pocos pasos. Conviene preferir el camino **seguro**, aunque sea más largo.
2. **Fila superior $(1,3),(2,3),(3,3)$: $\rightarrow$.** No hay nada peligroso arriba: se avanza hacia el $+1$. El borde superior protege de un desvío hacia arriba, y el peor desvío es bajar un casillero, que es poco grave.
3. **Estados $(1,1)$ y $(1,2)$: $\uparrow$.** Hay dos rutas hacia el $+1$: la **corta**, por la fila inferior y luego subiendo por la columna 4, que pasa pegada al estado $-1$; y la **larga y segura**, subiendo por la columna 1 y avanzando por la fila superior. La pared en $(2,2)$ obliga a elegir. Conviene la segura: en $(1,2)$ los desvíos hacia los costados solo hacen que el agente choque con el borde o la pared y se quede en su lugar, y en $(1,1)$ el desvío hacia la derecha lo lleva a $(2,1)$, de donde puede volver.
4. **Estado $(3,2)$: $\uparrow$.** Está al lado del $-1$ (a la derecha). Con $\uparrow$ solo cae en el $-1$ si se desvía a la derecha ($0.1$), mientras que si se desvía hacia la izquierda choca con la pared y no pasa nada grave.
5. **Estados $(3,1)$ y $(4,1)$: $\leftarrow$.** Aquí está lo menos intuitivo: en lugar de subir hacia el $+1$ por la columna 4 o por $(3,2)$, el agente **retrocede**. Subir desde $(4,1)$ lo lleva directo al $-1$ ($0.8$); y desde $(3,1)$ el desvío hacia la derecha lo dejaría en $(4,1)$, que es un estado muy malo. Es más rentable volver a $(2,1)$ y tomar la ruta larga.
6. **Estado $(2,1)$: $\leftarrow$.** Para volver a $(1,1)$ y subir por la columna 1. (No puede subir: arriba hay una pared.)

### 3.2 Resultado

Política óptima $\pi^*$:

| fila \ columna | **1** | **2** | **3** | **4** |
|:--:|:--:|:--:|:--:|:--:|
| **3** | $\rightarrow$ | $\rightarrow$ | $\rightarrow$ | **+1** |
| **2** | $\uparrow$ | *pared* | $\uparrow$ | **−1** |
| **1** | $\uparrow$ | $\leftarrow$ | $\leftarrow$ | $\leftarrow$ |

> 📌 **Acá va la gráfica de la política óptima** (la grilla con las flechas dibujadas en cada casilla, como en la Figura "Respuestas" de la guía).
>
> `![Política óptima](ej5_politica.png)`

### 3.3 Verificación con la ecuación de Bellman

Una política es óptima si en cada estado la acción elegida tiene el **mayor valor esperado** $Q(s,a)=\sum_{s'}P(s'\mid s,a)\,U(s')$ (ver 2.4). Usando las utilidades del inciso 5.2 (aquí redondeadas a 3 decimales), se comprueba en los cuatro estados más delicados. (Notación: "desvío" es el movimiento perpendicular, cada uno con probabilidad $0.1$.)

**Estado $(4,1)$** — comparar $\uparrow$ con $\leftarrow$:

- $\uparrow$: sube a $(4,2)$ con $0.8$ (valor $-1$); desvío a la izquierda $\to(3,1)$; desvío a la derecha choca con el borde y queda en $(4,1)$.
  $Q=0.8(-1)+0.1(0.611)+0.1(0.388)=\mathbf{-0.700}$
- $\leftarrow$: va a $(3,1)$ con $0.8$; desvío hacia arriba $\to(4,2)$; desvío hacia abajo choca y queda en $(4,1)$.
  $Q=0.8(0.611)+0.1(-1)+0.1(0.388)=\mathbf{+0.428}$ ← **mejor**

**Estado $(3,1)$** — comparar $\uparrow$ con $\leftarrow$:

- $\uparrow$: sube a $(3,2)$ con $0.8$; desvío izquierdo $\to(2,1)$; desvío derecho $\to(4,1)$.
  $Q=0.8(0.660)+0.1(0.655)+0.1(0.388)=\mathbf{0.632}$
- $\leftarrow$: va a $(2,1)$ con $0.8$; desvío hacia arriba $\to(3,2)$; desvío hacia abajo choca y queda en $(3,1)$.
  $Q=0.8(0.655)+0.1(0.660)+0.1(0.611)=\mathbf{0.651}$ ← **mejor**

(La ventaja de $\leftarrow$ es chica, $0.651$ vs. $0.632$, pero es la que decide la política.)

**Estado $(1,1)$** — comparar $\uparrow$ (ruta larga y segura) con $\rightarrow$ (ruta corta por abajo):

- $\uparrow$: sube a $(1,2)$ con $0.8$; desvío izquierdo choca con el borde y queda en $(1,1)$; desvío derecho $\to(2,1)$.
  $Q=0.8(0.762)+0.1(0.705)+0.1(0.655)=\mathbf{0.746}$ ← **mejor**
- $\rightarrow$: va a $(2,1)$ con $0.8$; desvío hacia arriba $\to(1,2)$; desvío hacia abajo choca y queda en $(1,1)$.
  $Q=0.8(0.655)+0.1(0.762)+0.1(0.705)=\mathbf{0.671}$

**Estado $(3,2)$** — comparar $\uparrow$ con $\leftarrow$ (la alternativa "prudente"):

- $\uparrow$: sube a $(3,3)$ con $0.8$; desvío izquierdo choca con la pared y queda en $(3,2)$; desvío derecho $\to(4,2)$.
  $Q=0.8(0.918)+0.1(0.660)+0.1(-1)=\mathbf{0.700}$ ← **mejor**
- $\leftarrow$: choca con la pared con $0.8$ y queda en $(3,2)$; desvío hacia arriba $\to(3,3)$; desvío hacia abajo $\to(3,1)$.
  $Q=0.8(0.660)+0.1(0.918)+0.1(0.611)=\mathbf{0.681}$

En todos los casos la acción de la política es la de mayor valor. (Estas comparaciones se verificaron también con iteración de valor hasta la convergencia, comprobando que la política resultante en los 9 estados es exactamente la de la guía.)

### 3.4 Alternativa sistemática: iteración de valor (por si se quiere hacer a mano)

Si en lugar de razonar se quiere **derivar** la política, se aplica la ecuación de Bellman de optimalidad partiendo de $U_0=0$ en los no terminales ($U_0(4,3)=+1$ y $U_0(4,2)=-1$ fijos). Con $\gamma=1$:

$$
U_{k+1}(s)=-0.04+\max_a\sum_{s'}P(s'\mid s,a)\,U_k(s').
$$

La **primera iteración** da $U_1(3,3)=-0.04+0.8(1)=0.76$ (acción $\rightarrow$), y $U_1=-0.04$ en todos los demás no terminales (en $(3,2)$ la acción $\uparrow$ daría $-0.14$ por el riesgo del $-1$, mientras que quedarse sin riesgo da $-0.04$). Las utilidades "se propagan" desde el $+1$ hacia atrás a medida que se itera, y la política codiciosa va tomando su forma final. A mano conviene hacer solo unas pocas iteraciones para ver el mecanismo. La convergencia completa requiere decenas de iteraciones.

---

## 4. Ejercicio 5.2: utilidades de los estados

> *Calcular las utilidades de los estados en el mundo de $4\times3$, dada la política óptima encontrada en el ejercicio anterior.*

### 4.1 Planteo

Con la política $\pi^*$ **fija**, la utilidad cumple la ecuación de Bellman lineal de 2.3. Hay 9 incógnitas (una por estado no terminal) y los terminales valen $U(4,3)=+1$ y $U(4,2)=-1$. Se escribe una ecuación por estado, mirando adónde puede ir el agente con la acción $\pi^*(s)$ (probabilidades $0.8,0.1,0.1$; en cada choque el agente "se queda").

### 4.2 Las 9 ecuaciones

Se abrevia $U_{xy}=U(x,y)$. Para cada estado se indica la acción y los tres resultados posibles:

| Estado | $\pi^*$ | Resultados (prob.) | Ecuación |
|:--:|:--:|:--|:--|
| $(1,3)$ | $\rightarrow$ | $(2,3)$ [0.8], se queda (borde sup.) [0.1], $(1,2)$ [0.1] | $U_{13}=-0.04+0.8\,U_{23}+0.1\,U_{13}+0.1\,U_{12}$ |
| $(2,3)$ | $\rightarrow$ | $(3,3)$ [0.8], se queda (borde sup.) [0.1], se queda (pared abajo) [0.1] | $U_{23}=-0.04+0.8\,U_{33}+0.2\,U_{23}$ |
| $(3,3)$ | $\rightarrow$ | $(4,3)=+1$ [0.8], se queda (borde sup.) [0.1], $(3,2)$ [0.1] | $U_{33}=-0.04+0.8(1)+0.1\,U_{33}+0.1\,U_{32}$ |
| $(1,2)$ | $\uparrow$ | $(1,3)$ [0.8], se queda (borde izq.) [0.1], se queda (pared der.) [0.1] | $U_{12}=-0.04+0.8\,U_{13}+0.2\,U_{12}$ |
| $(3,2)$ | $\uparrow$ | $(3,3)$ [0.8], se queda (pared izq.) [0.1], $(4,2)=-1$ [0.1] | $U_{32}=-0.04+0.8\,U_{33}+0.1\,U_{32}+0.1(-1)$ |
| $(1,1)$ | $\uparrow$ | $(1,2)$ [0.8], se queda (borde izq.) [0.1], $(2,1)$ [0.1] | $U_{11}=-0.04+0.8\,U_{12}+0.1\,U_{11}+0.1\,U_{21}$ |
| $(2,1)$ | $\leftarrow$ | $(1,1)$ [0.8], se queda (pared arriba) [0.1], se queda (borde inf.) [0.1] | $U_{21}=-0.04+0.8\,U_{11}+0.2\,U_{21}$ |
| $(3,1)$ | $\leftarrow$ | $(2,1)$ [0.8], $(3,2)$ [0.1], se queda (borde inf.) [0.1] | $U_{31}=-0.04+0.8\,U_{21}+0.1\,U_{32}+0.1\,U_{31}$ |
| $(4,1)$ | $\leftarrow$ | $(3,1)$ [0.8], $(4,2)=-1$ [0.1], se queda (borde inf.) [0.1] | $U_{41}=-0.04+0.8\,U_{31}+0.1(-1)+0.1\,U_{41}$ |

### 4.3 Resolución a mano por sustitución

El sistema parece de $9\times9$ pero tiene mucha estructura. Agrupando los términos que dependen de la propia incógnita:

**Paso 1 — Relaciones simples** (en las ecuaciones donde el agente "se queda" con probabilidad $0.2$):

$$
U_{23}=U_{33}-0.05,\qquad U_{12}=U_{13}-0.05,\qquad U_{21}=U_{11}-0.05.
$$

(Por ejemplo, $U_{23}=-0.04+0.8U_{33}+0.2U_{23}\Rightarrow0.8U_{23}=-0.04+0.8U_{33}$.)

**Paso 2 — $U_{13}$ en función de $U_{33}$.** Se sustituye lo anterior en la ecuación de $(1,3)$:
$0.9\,U_{13}=-0.04+0.8(U_{33}-0.05)+0.1(U_{13}-0.05)\ \Rightarrow\ 0.8\,U_{13}=-0.085+0.8\,U_{33}$, es decir

$$
U_{13}=U_{33}-0.10625.
$$

**Paso 3 — El par $(U_{33},U_{32})$.** Son las dos ecuaciones que mezclan el estado cercano al $+1$ y el cercano al $-1$:

$$
0.9\,U_{33}=0.76+0.1\,U_{32},\qquad 0.9\,U_{32}=-0.14+0.8\,U_{33}.
$$

De la primera, $U_{32}=9\,U_{33}-7.6$. Reemplazando en la segunda, $8.1\,U_{33}-6.84=-0.14+0.8\,U_{33}$, de donde $7.3\,U_{33}=6.70$:

$$
U_{33}=\frac{6.70}{7.3}\approx0.9178,\qquad U_{32}=9(0.9178)-7.6\approx0.6603.
$$

**Paso 4 — Resto de la fila superior y la columna 1.**

$$
U_{23}=0.9178-0.05=0.8678,\qquad U_{13}=0.9178-0.10625=0.8116,\qquad U_{12}=0.8116-0.05=0.7616.
$$

**Paso 5 — $U_{11}$.** De la ecuación de $(1,1)$ usando $U_{21}=U_{11}-0.05$: $0.8\,U_{11}=-0.045+0.8\,U_{12}$, luego $U_{11}=U_{12}-0.05625$:

$$
U_{11}=0.7616-0.05625=0.7053,\qquad U_{21}=0.7053-0.05=0.6553.
$$

**Paso 6 — Fila inferior.**

$$
0.9\,U_{31}=-0.04+0.8(0.6553)+0.1(0.6603)=0.5503\ \Rightarrow\ U_{31}\approx0.6114,
$$

$$
0.9\,U_{41}=-0.14+0.8(0.6114)=0.3491\ \Rightarrow\ U_{41}\approx0.3879.
$$

### 4.4 Resultado

Utilidades $U^{\pi^*}(s)$:

| fila \ columna | **1** | **2** | **3** | **4** |
|:--:|:--:|:--:|:--:|:--:|
| **3** | $0.812$ | $0.868$ | $0.918$ | **+1** |
| **2** | $0.762$ | *pared* | $0.660$ | **−1** |
| **1** | $0.705$ | $0.655$ | $0.611$ | $0.388$ |

> 📌 **Acá va la gráfica de las utilidades** (la grilla con el valor de cada estado, como en la figura de la guía).
>
> `![Utilidades](ej5_utilidades.png)`

> ⚠️ **Una discrepancia con la guía.** En la figura de respuestas de la guía el estado $(3,3)$ figura con $0.912$. El valor correcto con estas hipótesis es **$0.918$** (como en la fuente original del problema). Se puede ver comprobando la ecuación de Bellman en ese estado: con $0.918$ y $U_{32}=0.660$ da $-0.04+0.8+0.1(0.918)+0.1(0.660)=0.918$ (cierra), mientras que con $0.912$ da $0.917\neq0.912$ (no cierra). Los otros ocho valores coinciden con la guía. Probablemente es una errata en la figura.

### 4.5 Interpretación

- Las utilidades **decrecen a medida que el estado está más lejos del $+1$ en pasos** (de $0.918$ en $(3,3)$ a $0.705$ en el inicio), porque cada paso cuesta $0.04$ y además hay más oportunidades de desviarse.
- $(4,1)$ tiene la utilidad **más baja** ($0.388$) porque está pegada al $-1$ y desde allí no hay ninguna ruta sin riesgo (por eso la política se aleja hacia $(3,1)$).
- $(3,2)$ ($0.660$) también es baja pese a estar a un paso del $+1$ y de $(3,3)$: está **al lado del $-1$** y existe $0.1$ de probabilidad de caer en él en cada intento.
- Se cumple la consistencia entre ambos incisos: la política del 5.1 es codiciosa respecto de estas utilidades (sección 3.3).
- La utilidad del estado inicial, $U(1,1)\approx0.705$, es el **retorno esperado** de seguir la política óptima desde el inicio. Las dos trayectorias de la Figura 2 ($+0.72$ y $-1.16$) son realizaciones individuales de ese proceso aleatorio, mientras que $0.705$ es el valor esperado.

---

## 5. Extra: ¿cómo depende la política óptima de la recompensa $R(s)$?

El valor $-0.04$ tiene un papel decisivo. Se calculó la política óptima con iteración de valor para otros costos por paso (con el mismo modelo de transición):

| $R(s)$ | Política óptima (filas 3, 2 y 1) | Comportamiento |
|:--:|:--|:--|
| $-0.01$ | fila 3: $\rightarrow\rightarrow\rightarrow$ · fila 2: $\uparrow$, *pared*, $\leftarrow$ · fila 1: $\uparrow\ \leftarrow\ \leftarrow\ \downarrow$ | **Más prudente**: vivir casi no cuesta, así que prefiere evitar el $-1$ a toda costa (en $(3,2)$ choca contra la pared a propósito y en $(4,1)$ se apoya contra el borde inferior). |
| **$-0.04$** | fila 3: $\rightarrow\rightarrow\rightarrow$ · fila 2: $\uparrow$, *pared*, $\uparrow$ · fila 1: $\uparrow\ \leftarrow\ \leftarrow\ \leftarrow$ | **La política del ejercicio.** |
| $-0.5$ | fila 3: $\rightarrow\rightarrow\rightarrow$ · fila 2: $\uparrow$, *pared*, $\uparrow$ · fila 1: $\uparrow\ \rightarrow\ \uparrow\ \uparrow$ | **Apurado**: vivir es caro, entonces acepta el riesgo en la fila inferior: ya no retrocede desde $(3,1)$ y $(4,1)$ sino que avanza hacia arriba, aun a costa de una probabilidad alta de caer en el $-1$ desde $(4,1)$. |
| $-2$ | fila 3: $\rightarrow\rightarrow\rightarrow$ · fila 2: $\uparrow$, *pared*, $\rightarrow$ · fila 1: $\rightarrow\ \rightarrow\ \rightarrow\ \uparrow$ | **Desesperado**: es preferible terminar cuanto antes, aun cayendo en el $-1$, que seguir pagando. |

Moraleja: la recompensa por paso regula el equilibrio entre **riesgo** y **costo de seguir viviendo**, y por eso la política óptima no depende solo de la geometría de la grilla sino también del diseño de la función de recompensa.

---

## 6. Conclusiones

1. El problema es un **MDP**: la incertidumbre en el movimiento ($0.8/0.1/0.1$) hace que cada política produzca un resultado aleatorio, y que deba evaluarse por su **utilidad esperada**.
2. La **política óptima** es la codiciosa respecto de las utilidades óptimas (ecuación de Bellman de optimalidad). Para este mundo con $R=-0.04$ conviene la **ruta larga y segura** (columna 1 y fila superior) en lugar de la corta pegada al estado $-1$, y desde $(2,1)$, $(3,1)$ y $(4,1)$ conviene **retroceder** hacia la izquierda.
3. Las **utilidades** bajo esa política se obtienen resolviendo un sistema lineal de 9 ecuaciones (Bellman para política fija), que en este caso se resuelve a mano por sustitución. Van de $0.918$ en $(3,3)$ a $0.388$ en $(4,1)$, y el estado inicial vale $0.705$.
4. Verificar una política propuesta es fácil: basta comprobar, en cada estado, que la acción elegida tiene el mayor valor esperado dadas las utilidades.
5. El valor de la recompensa por paso condiciona fuertemente la política óptima: costos bajos dan políticas prudentes y costos altos, políticas arriesgadas.
