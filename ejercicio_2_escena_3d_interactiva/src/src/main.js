import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';

// ==========================================
// 1. CONFIGURACIÓN BÁSICA
// ==========================================
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x20252f);
scene.fog = new THREE.Fog(0x20252f, 10, 50);

const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0, 8, 15);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
document.body.appendChild(renderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.target.set(0, 0, 0);

// ==========================================
// 2. ILUMINACIÓN
// ==========================================
const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
scene.add(ambientLight);

const dirLight = new THREE.DirectionalLight(0xffffff, 1.5);
dirLight.position.set(5, 10, 5);
dirLight.castShadow = true;
dirLight.shadow.mapSize.width = 2048;
dirLight.shadow.mapSize.height = 2048;
scene.add(dirLight);

// ==========================================
// 3. MATERIALES
// ==========================================
const metalMaterial = new THREE.MeshStandardMaterial({ color: 0x888888, roughness: 0.4, metalness: 0.8 });
const beltMaterial = new THREE.MeshStandardMaterial({ color: 0x111111, roughness: 0.9, metalness: 0.1 });
const boxMaterial = new THREE.MeshStandardMaterial({ color: 0xe0a060, roughness: 0.7, metalness: 0.0 });

// ==========================================
// 4. ESCENA BASE Y CAJAS
// ==========================================
// Suelo
const floor = new THREE.Mesh(new THREE.PlaneGeometry(50, 50), new THREE.MeshStandardMaterial({ color: 0x333333 }));
floor.rotation.x = -Math.PI / 2;
floor.receiveShadow = true;
scene.add(floor);

// Cinta Transportadora
const belt = new THREE.Mesh(new THREE.BoxGeometry(30, 0.5, 3), beltMaterial);
belt.position.y = 1;
belt.receiveShadow = true;
scene.add(belt);

// Soportes
const supportGeo = new THREE.CylinderGeometry(0.2, 0.2, 1);
for(let i = -7; i <= 7; i+=7) {
    const support = new THREE.Mesh(supportGeo, metalMaterial);
    support.position.set(i, 0.5, 0);
    scene.add(support);
}

// Cajas (Añadimos userData para controlar sus estados físicos y lógicos)
const boxes = [];
const boxGeo = new THREE.BoxGeometry(1, 1, 1);
for (let i = 0; i < 8; i++) {
    const box = new THREE.Mesh(boxGeo, boxMaterial.clone());
    box.position.set(-15 + (i * 8), 1.75, 0);
    box.castShadow = true;
    
    // ESTADOS: 'normal', 'defective' (roja), 'grabbed' (agarrada), 'falling' (arrojada)
    box.userData = { 
        status: 'normal', 
        velocity: new THREE.Vector3() 
    };
    
    scene.add(box);
    boxes.push(box);
}

// ==========================================
// 5. BRAZO ROBÓTICO (Con "Mano")
// ==========================================
const robotBase = new THREE.Group();
robotBase.position.set(0, 0, -2.5); // Lo acercamos un poco para que alcance la cinta
scene.add(robotBase);

const pilar = new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.6, 2), metalMaterial);
pilar.position.y = 1;
robotBase.add(pilar);

const shoulder = new THREE.Group();
shoulder.position.y = 2;
robotBase.add(shoulder);

const arm1 = new THREE.Mesh(new THREE.BoxGeometry(0.6, 3, 0.6), metalMaterial);
arm1.position.y = 1.5;
shoulder.add(arm1);

const elbow = new THREE.Group();
elbow.position.y = 3;
shoulder.add(elbow);

const arm2 = new THREE.Mesh(new THREE.BoxGeometry(0.4, 2.5, 0.4), metalMaterial);
arm2.position.y = 1.25;
elbow.add(arm2);

// Agregamos una "mano" o garra al final del brazo para tener un punto de anclaje
const hand = new THREE.Mesh(new THREE.BoxGeometry(0.6, 0.2, 0.6), beltMaterial);
hand.position.y = 1.25; // Punta del arm2
arm2.add(hand);

// ==========================================
// 6. INTERACCIONES DEL USUARIO
// ==========================================
let isRunning = true;

// Teclado
window.addEventListener('keydown', (event) => {
    if (event.code === 'Space') isRunning = !isRunning;
});

// Mouse (Clic para marcar como defectuosa)
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

window.addEventListener('click', (event) => {
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
    raycaster.setFromCamera(mouse, camera);

    const intersects = raycaster.intersectObjects(boxes);
    if (intersects.length > 0) {
        const box = intersects[0].object;
        // Solo cambiamos a rojo si la caja está normal en la cinta
        if (box.userData.status === 'normal') {
            box.material.color.setHex(0xff0000); // Color Rojo
            box.userData.status = 'defective';
        }
    }
});

window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

// ==========================================
// 7. ANIMACIÓN Y LÓGICA DE ESTADOS
// ==========================================
const clock = new THREE.Clock();

// Variables para el control del robot
let activeBox = null; 
let throwPhase = 0; // 0: Agarrando, 1: Arrojando

function animate() {
    requestAnimationFrame(animate);
    const time = clock.getElapsedTime();

    if (isRunning) {
        // --- LÓGICA DEL ROBOT ---
        if (!activeBox) {
            // Si el robot está libre, busca una caja roja que esté en su zona de alcance
            activeBox = boxes.find(b => b.userData.status === 'defective' && b.position.x > -0.5 && b.position.x < 1.5);
            if (activeBox) {
                activeBox.userData.status = 'grabbed';
                throwPhase = 0;
            }
        }

        if (activeBox) {
            // Obtener la posición global de la "mano" del robot
            const handPos = new THREE.Vector3();
            hand.getWorldPosition(handPos);

            if (throwPhase === 0) {
                // FASE 0: Acercarse e imantar la caja
                // shoulder.rotation.y = THREE.MathUtils.lerp(shoulder.rotation.y, 0, 0.1);
                // Inclinarse hacia la cinta
                shoulder.rotation.x = THREE.MathUtils.lerp(shoulder.rotation.x, 0.6, 0.1);
                elbow.rotation.x = THREE.MathUtils.lerp(elbow.rotation.x, 1.2, 0.1);

                // La caja "levita" hacia la mano (efecto de succión/imán)
                activeBox.position.lerp(handPos, 0.15);

                // Cuando la caja está lo suficientemente cerca de la mano, pasar a lanzar
                if (activeBox.position.distanceTo(handPos) < 0.5) {
                    throwPhase = 1;
                }
            } else if (throwPhase === 1) {
                // FASE 1: Girar bruscamente para arrojar
                // shoulder.rotation.y = THREE.MathUtils.lerp(shoulder.rotation.y, Math.PI / 1.5, 0.15); // Girar a la derecha
                // Levantar el brazo
                shoulder.rotation.x = THREE.MathUtils.lerp(shoulder.rotation.x, 0, 0.15);
                elbow.rotation.x = THREE.MathUtils.lerp(elbow.rotation.x, -0.5, 0.15); 

                // La caja sigue anclada a la mano
                activeBox.position.copy(handPos);

                // Cuando alcanza cierto ángulo de rotación, la soltamos
                if (shoulder.rotation.x < 0.1) {
                    activeBox.userData.status = 'falling';
                    // Le damos velocidad inicial en X, Y (arriba) y Z (hacia la pantalla)
                    activeBox.userData.velocity.set(0.1, 0.25, 0.3); 
                    activeBox = null; // El robot queda libre
                }
            }
        } else {
            // FASE IDLE: Si no hay cajas rojas, el robot hace su trabajo normal
            // shoulder.rotation.y = THREE.MathUtils.lerp(shoulder.rotation.y, Math.sin(time * 2) * 1.5, 0.05);
            elbow.rotation.x = THREE.MathUtils.lerp(elbow.rotation.x, Math.abs(Math.sin(time * 4)) * 0.5 - 0.2, 0.05);
        }

        // --- LÓGICA DE LAS CAJAS ---
        const has_defective = !boxes.every(box => box.userData.status === 'normal' || box.userData.status === 'falling')
        boxes.forEach((box) => {
            if (box.userData.status === 'normal' || box.userData.status === 'defective') {
                // Movimiento normal en la cinta
                box.position.x += has_defective?0.02:0.05;
                if (box.position.x > 15) {
                    // Loop de la cinta
                    box.position.set(-15, 1.75, 0);
                    box.material.color.setHex(0xe0a060);
                    box.userData.status = 'normal';
                }
            } else if (box.userData.status === 'falling') {
                // Físicas de caída cuando es arrojada
                box.position.add(box.userData.velocity);
                box.userData.velocity.y -= 0.015; // Gravedad simulada
                
                // Rotación caótica mientras cae
                box.rotation.x += 0.1;
                box.rotation.y += 0.1;

                // Resetearla cuando caiga al fondo
                if (box.position.y < -5) {
                    box.position.set(-8, 1.75, 0);
                    box.rotation.set(0, 0, 0);
                    box.material.color.setHex(0xe0a060);
                    box.userData.status = 'normal';
                }
            }
        });
    }

    controls.update();
    renderer.render(scene, camera);
}

animate();