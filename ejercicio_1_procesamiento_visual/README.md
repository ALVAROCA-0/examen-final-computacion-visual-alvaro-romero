# Ejercicio 1 - Parcial Computación Visual

Autor: Álvaro Andrés Romero Castro

## Descripción General

Este proyecto implementa una aplicación gráfica para el procesamiento digital de imágenes utilizando Python, OpenCV y CustomTkinter. La aplicación permite cargar una imagen y visualizar distintas etapas de un pipeline de visión por computador, incluyendo conversión de espacios de color, filtrado, detección de bordes y segmentación.

El objetivo es demostrar de manera interactiva conceptos fundamentales de procesamiento de imágenes mediante una interfaz gráfica organizada por pestañas.

---

## Funcionalidades Implementadas

La aplicación permite:

* Cargar imágenes en formato PNG, JPG o JPEG.
* Visualizar la imagen original.
* Convertir la imagen a escala de grises.
* Convertir la imagen a espacios de color HSV o LAB.
* Aplicar filtros de suavizado:

  * Gaussiano.
  * Mediana.
* Aplicar detección de bordes:

  * Canny.
  * Sobel.
* Realizar segmentación mediante:

  * Umbralización de Otsu.
  * Umbralización Adaptativa.
* Guardar automáticamente los resultados generados.
* Comparar visualmente cada etapa del procesamiento.

---

# Dependencias

El proyecto fue desarrollado utilizando Python 3.14.

Bibliotecas requeridas:

```bash
customtkinter
tkinterdnd2
opencv-python
numpy
pillow
```

---

# Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/ALVAROCA-0/examen-final-computacion-visual-alvaro-romero.git
```

2. Ingresar al directorio:

```bash
cd ejercicio_1_procesamiento_visual
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

# Ejecución

Ejecutar el archivo principal:

```bash
python main.py
```

Al iniciar la aplicación aparecerá una interfaz gráfica con cinco pestañas:

1. Cargar Imagen.
2. Pre-Procesado.
3. Detección de Bordes.
4. Segmentación.
5. Resultados.

---

# Estructura del Repositorio

```text
proyecto-procesamiento-imagenes/
│
├── src/
|   ├── main.py
|   ├── README.md
|   ├── requirements.txt
│
├── resultados/
│   ├── gray.png
│   ├── hsv.png
│   ├── blur.png
│   ├── edges.png
│   └── segmented.png
│
└── data/
    └── ejemplo.jpg
```

---

# Evidencias

## Pre-Procesado

La aplicación genera:

* Conversión a escala de grises.
* Conversión a HSV o LAB.

![Imagen a gray](./resultados/gray.png)
![Imagen a HSV](./resultados/hsv.png)

---

## Suavisazado y Detección de Bordes

Se aplican técnicas de suavizado y posteriormente algoritmos de detección de bordes.

Opciones disponibles:

* Filtro Gaussiano.
* Filtro Mediana.
* Detector Canny.
* Detector Sobel.

![Suavizado](./resultados/blur.png)
![Bordes](./resultados/edges.png)

---

## Segmentación

La aplicación permite comparar dos métodos clásicos de segmentación:

* Umbralización de Otsu.
* Umbralización Adaptativa.

![Segmentación](./resultados/segmented.png)

---

## Resultados Guardados

Las imágenes generadas se almacenan automáticamente en la carpeta `results`.

---

# Análisis Técnico

## Conversión a Escala de Grises

La imagen original se transforma a una representación monocanal mediante:

```python
cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
```

Esta etapa reduce la complejidad de la información visual y facilita operaciones posteriores como filtrado, detección de bordes y segmentación.

---

## Conversión a Espacios de Color

### HSV

El espacio HSV separa la información de color de la intensidad luminosa, facilitando tareas de análisis y segmentación basadas en color.

### LAB

El espacio LAB representa los colores de forma más cercana a la percepción humana, separando luminosidad y cromaticidad.

La posibilidad de alternar entre ambos espacios permite observar distintas representaciones de una misma escena.

---

## Suavizado

Se implementaron dos filtros:

### Filtro Gaussiano

```python
cv2.GaussianBlur(gray, (5,5), 0)
```

Reduce ruido de alta frecuencia mediante una convolución con una distribución gaussiana.

### Filtro Mediana

```python
cv2.medianBlur(gray, 5)
```

Sustituye cada píxel por la mediana de sus vecinos, siendo especialmente efectivo contra ruido impulsivo.

Se seleccionó un kernel de tamaño 5×5 por ofrecer un equilibrio adecuado entre suavizado y preservación de detalles.

---

## Detección de Bordes

### Detector Canny

```python
cv2.Canny(blur, 100, 200)
```

Se utilizaron umbrales de 100 y 200 para identificar cambios significativos de intensidad manteniendo una buena relación entre sensibilidad y robustez al ruido.

### Detector Sobel

```python
cv2.Sobel(...)
```

Calcula gradientes horizontales y verticales de intensidad para identificar regiones con cambios abruptos.

---

## Segmentación

### Método de Otsu

```python
cv2.threshold(..., cv2.THRESH_OTSU)
```

Calcula automáticamente el umbral óptimo a partir del histograma de la imagen.

### Umbralización Adaptativa

```python
cv2.adaptiveThreshold(...)
```

Utiliza ventanas locales de 11×11 píxeles y una constante de ajuste de 2 para adaptarse a cambios de iluminación.

---

## Justificación de los Parámetros Utilizados

Los parámetros seleccionados corresponden a configuraciones ampliamente utilizadas en aplicaciones académicas y de prototipado:

* Kernel de 5×5 para suavizado.
* Umbrales 100–200 para Canny.
* Kernel de tamaño 3 para Sobel.
* Ventana local 11×11 para umbralización adaptativa.

Estos valores permiten obtener resultados estables en una amplia variedad de imágenes sin necesidad de ajustes específicos para cada caso, facilitando la comparación entre técnicas de procesamiento.

## Uso de IA

Debido al uso extensivo de tkinter se uso a la IA para generar este espació de una forma organizada. También se le pregunto sobre los parámetros a usar para el procesamiento de imagenes.