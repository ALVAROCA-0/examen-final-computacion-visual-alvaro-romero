# Procesamiento de Imágenes con OpenCV y CustomTkinter

## ¿Qué problema o propósito aborda el ejercicio?

El objetivo de este ejercicio es implementar un pipeline básico de procesamiento digital de imágenes que permita visualizar y comparar distintas etapas utilizadas en visión por computador.

La aplicación desarrollada permite cargar una imagen y aplicar diferentes técnicas de preprocesamiento, detección de características y segmentación, mostrando los resultados de forma interactiva mediante una interfaz gráfica.

El propósito principal es comprender cómo las transformaciones realizadas sobre una imagen afectan la información visual disponible para tareas posteriores de análisis y reconocimiento.

---

## ¿Qué herramientas, librerías o motores se utilizaron?

El proyecto fue desarrollado utilizando Python y las siguientes librerías:

### OpenCV

Biblioteca principal utilizada para el procesamiento de imágenes:

* Conversión entre espacios de color.
* Aplicación de filtros.
* Detección de bordes.
* Segmentación.
* Lectura y almacenamiento de imágenes.

### NumPy

Utilizada para la manipulación eficiente de matrices y arreglos numéricos empleados por OpenCV.

### Pillow (PIL)

Utilizada para convertir imágenes entre formatos compatibles con OpenCV y la interfaz gráfica.

### CustomTkinter

Framework utilizado para construir la interfaz gráfica moderna de la aplicación.

### TkinterDnD2

Permite la funcionalidad de arrastrar y soltar archivos dentro de la aplicación.

---

## ¿Cómo se ejecuta la solución?

### Instalación de dependencias

```bash
pip install opencv-python numpy pillow customtkinter tkinterdnd2
```

### Ejecución

Desde la carpeta raíz del proyecto:

```bash
python main.py
```

### Uso de la aplicación

1. Abrir la aplicación.
2. Cargar una imagen mediante arrastrar y soltar o utilizando el selector de archivos.
3. Visualizar la imagen original.
4. Seleccionar el espacio de color deseado (HSV o LAB).
5. Seleccionar el método de suavizado (Gaussiano o Mediana).
6. Seleccionar el detector de bordes (Canny o Sobel).
7. Seleccionar el método de segmentación (Otsu o Umbralización Adaptativa).
8. Observar los resultados en cada pestaña.
9. Revisar las imágenes generadas en la carpeta `results`.

---

## ¿Qué resultados se obtuvieron?

La aplicación genera las siguientes salidas:

### Imagen original

Permite visualizar la entrada sin modificaciones.

### Escala de grises

Reduce la información de color a una representación de intensidad, facilitando el procesamiento posterior.

### Espacios de color HSV y LAB

Permiten observar distintas representaciones cromáticas de una misma imagen y comparar cómo se distribuye la información de color.

### Suavizado

Los filtros Gaussiano y de Mediana reducen el ruido presente en la imagen antes de aplicar algoritmos de detección de características.

### Detección de bordes

* El método Canny produce contornos definidos y continuos.
* El método Sobel resalta regiones con cambios bruscos de intensidad mediante gradientes.

### Segmentación

* El método de Otsu separa automáticamente regiones de interés utilizando un umbral global.
* La umbralización adaptativa mejora los resultados en imágenes con iluminación no uniforme.

### Almacenamiento de resultados

Todas las imágenes procesadas son guardadas automáticamente para facilitar la comparación entre técnicas.

---

## ¿Qué dificultades aparecieron y cómo se resolvieron?

### Uso de Tkinter y diseño

Se dificulto principalmente la creación de la applicación con tkinter. Ya que para que esta tuviera un buen diseño se requirio de manipular varias veces cada uno de los objetos usados. Para facilitar este se le pidio a una IA que generara este diseño y colores para permitir el flujo de imagenes entre cada punto del proceso.

### Enlazado del Pipline

Inicialmente se planteo la idea de que con los cambios en el dropdown cambiaran solo las imagenes que se querían pero esto habría requerido de muchos más metodos y callbacks en los dropdown de tkinter, entonces se decidio unir todo el pipeline en un solo método `process_image`, esto se unió a `update_labels` por medio de `on_parameter_change` para que todo se vuelva a ejecutar en el cambio de un dropdown. Esto tiene la desventaja de realentizar toda la aplicación solo con cambiar una imagen.

---

## ¿Qué prompts de IA se usaron, si aplica?

### Creación del ambiente Tkinter

Inicié creando las clases de `Image`, `FileDrop` y un inicio de la applicación principal `App`, despues le pedí a la IA que a partir de estas clases (Y las tabs dentro de `App`) organizara los elementos para poder resolver cada uno de los puntos, y que agrupara algunos como escala de grises y HSV/LAB.

---

## ¿Qué partes fueron verificadas manualmente por el estudiante?

Se realizaron pruebas manuales para validar el funcionamiento correcto de cada componente de la aplicación.

### Carga de imágenes

Se verificó la carga correcta de archivos PNG, JPG y JPEG mediante selección manual y arrastrar y soltar.

### Conversión de espacios de color

Se comprobó visualmente que las representaciones HSV y LAB fueran generadas correctamente al cambiar la opción seleccionada.

### Filtros de suavizado

Se verificó que los filtros Gaussiano y de Mediana modificaran la imagen de acuerdo con el comportamiento esperado, reduciendo ruido y suavizando detalles.

### Detección de bordes

Se compararon los resultados de Canny y Sobel para confirmar que ambos métodos respondieran a los cambios de intensidad presentes en la imagen.

### Segmentación

Se validó que los métodos de Otsu y Umbralización Adaptativa generaran máscaras binarias coherentes con el contenido de la imagen.

### Guardado de resultados

Se comprobó la creación automática de la carpeta `results` y el almacenamiento correcto de cada imagen procesada.

### Interfaz gráfica

Se verificó que los cambios realizados en los menús desplegables actualizaran correctamente los resultados mostrados en pantalla sin necesidad de volver a cargar la imagen.
