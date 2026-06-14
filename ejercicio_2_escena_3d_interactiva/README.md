# Línea de Producción Automática en 3D

## ¿Qué problema o propósito aborda el ejercicio?

El objetivo de este ejercicio es implementar una simulación interactiva de una línea de producción automática en 3D para consolidar conceptos fundamentales de gráficos por computadora.

La aplicación desarrollada permite visualizar un entorno industrial donde un brazo robótico interactúa con objetos en movimiento sobre una cinta transportadora, integrando jerarquías y cinemática.

El propósito principal es comprender cómo se coordinan múltiples sistemas en tiempo real, aplicando transformaciones geométricas, físicas simuladas y respuesta a eventos del usuario.

---

## ¿Qué herramientas, librerías o motores se utilizaron?

El proyecto fue desarrollado utilizando JavaScript y las siguientes tecnologías:

### Three.js

Librería principal utilizada para el renderizado 3D en el navegador:

* Creación de geometrías y materiales PBR.
* Configuración de iluminación dinámica y sombras.
* Manejo de jerarquías y animaciones matemáticas.
* Implementación de Raycasting para selección de objetos.

### Vite

Herramienta de construcción utilizada para inicializar el entorno de desarrollo y empaquetar los módulos de forma moderna y rápida.

### OrbitControls

Módulo de Three.js implementado para dotar a la cámara de interactividad, permitiendo al usuario rotar, desplazar y hacer zoom en la escena con el ratón.

### JavaScript Vanilla, HTML y CSS

Lenguajes base utilizados para estructurar la aplicación, implementar la lógica de estados de la fábrica y estilizar el contenedor del canvas para que ocupe toda la pantalla.

---

## ¿Cómo se ejecuta la solución?

### Instalación de dependencias

```bash
npm install
npm install three
```

### Ejecución

Desde la carpeta raíz del proyecto:
```bash
npm run dev
```

### Uso de la aplicación

1. Abrir la aplicación en el navegador web local.
2. Observar la simulación automática de la cinta transportadora y el robot en estado de espera.
3. Presionar la tecla Espacio para pausar o reanudar completamente el flujo de la producción.
4. Hacer clic (usando el mouse) sobre las cajas en movimiento para marcarlas como defectuosas (cambiarán a color rojo).
5. Observar cómo el brazo robótico detecta la caja roja, coordina sus ejes para recogerla y la arroja fuera de la línea.
6. Navegar por la escena arrastrando el mouse para rotar la cámara y usando la rueda de desplazamiento para acercar o alejar.

## ¿Qué resultados se obtuvieron?

La aplicación genera la siguiente simulación interactiva:

### Entorno industrial 3D

Permite visualizar una escena completa con iluminación coherente, sombras proyectadas reales y materiales que reaccionan a la luz simulando metal, cartón y caucho.

### Cinta transportadora infinita

Desplaza las cajas de forma continua y resetea su posición al llegar al final del recorrido, creando la ilusión de un flujo ininterrumpido de producción optimizando los recursos.

### Interacción de usuario

Implementa un sistema preciso que traduce las coordenadas 2D del clic del usuario en intersecciones 3D con los elementos en movimiento dentro del espacio tridimensional.

### Cinemática de brazo robótico

Ejecuta animaciones dinámicas basadas en jerarquías, permitiendo que la rotación del hombro y el codo trabajen en conjunto de forma fluida para simular movimientos mecánicos complejos.

### Simulación de físicas

Calcula vectores de velocidad e implementa una gravedad simulada cuando el robot suelta una pieza defectuosa, generando un tiro parabólico convincente hasta que el objeto desaparece de la vista.

## ¿Qué dificultades aparecieron y cómo se resolvieron?

Se tuvo dificultades principalmente en las animaciones ya que estas tomaron mucho tiempo de lograr hacer funcionar correctamente.

## ¿Qué partes fueron verificadas manualmente por el estudiante?

Se realizaron pruebas manuales para validar el funcionamiento correcto de cada componente de la simulación.

### Detección de Raycasting

Se verificó que los clics del usuario cambiaran el estado y color exclusivo de las cajas objetivo, sin seleccionar por error el suelo, la estructura de la cinta o el propio brazo robótico.

### Animación jerárquica

Se comprobó visualmente que la interpolación de los ángulos de rotación en los ejes X e Y del robot permitiera a la garra bajar exactamente al nivel de la cinta sin atravesar la geometría de las cajas.

### Lógica de estados

Se validó que el flujo interno de los objetos pasara sin conflictos de un estado normal a defectuoso, luego a ser agarrado (anclando su posición al robot) y finalmente al estado de caída.

### Físicas de descarte

Se calibraron los valores de gravedad y fuerza de impulso para asegurar que la trayectoria de la caja arrojada se viera natural y saliera del plano de visión correctamente.

### Pausa global

Se comprobó que el evento del teclado detuviera por completo y de forma sincronizada tanto el desplazamiento lineal de la cinta como las rutinas trigonométricas del brazo en estado de espera.