# DoS-mediante-el-protocolo-CDP.

# Documentación Técnica: CDP Resource Exhaustion (DoS)
## 1. Objetivo del Script
El objetivo de este script es realizar un ataque de Denegación de Servicio (DoS) orientado al agotamiento de recursos del Plano de Control en dispositivos Cisco. Aprovechando que el protocolo CDP (Cisco Discovery Protocol) no requiere autenticación, el script inunda al switch con miles de anuncios de vecinos falsos ("Fake Neighbors"). Esto busca saturar la memoria RAM asignada al proceso CDP y elevar el uso de CPU, lo que en equipos reales o con recursos limitados puede provocar inestabilidad, lentitud en la gestión o el reinicio del dispositivo.

## 2. Topología y Escenario de Red
La topología se ha montado en un entorno virtualizado, conectando un nodo atacante directamente a un switch multicapa.

Detalles de la Topología
Atacante: Ubuntu Linux (Python 3 + Scapy).

Objetivo: Cisco Switch (IOSvL2).

Interfaz de conexión: eth0 (Atacante) conectada a Eth 0/1 (Switch).
NOTA: En el Switch no se uso vlans.

| Dispositivo | Interfaz | Rol       | Configuración Especial        |
|-------------|----------|-----------|--------------------------------|
| Ubuntu      | eth0     | Atacante  | Scapy instalado                |
| Switch      | Eth 0/1  | Víctima   | CDP habilitado (default)       |

<img width="947" height="408" alt="image" src="https://github.com/user-attachments/assets/1e9e9f88-afb2-4c71-83e9-d99ec6ad6ba3" />




## 3. Parámetros Usados
El script utiliza la librería Scapy para construir tramas de Capa 2 personalizadas:

* **Ethernet Destination (01:00:0c:cc:cc:cc):** Dirección Multicast propietaria de Cisco para anuncios CDP.
* **CDPv2_HDR:** Versión 2 del protocolo.
* **ttl=255:** Tiempo de vida máximo para que las entradas falsas permanezcan en la memoria del switch el mayor tiempo posible.
* **CDPMsgDeviceID:** Genera un nombre aleatorio (ej. Fake-Switch-XXXX) para cada paquete, forzando al switch a crear una nueva entrada en su tabla.
* **CDPMsgPlatform:** Carga útil simulando un modelo de switch de alto rendimiento para ocupar más espacio en memoria.


## 4. Requisitos para utilizar la herramienta
1. **Librerías de Python:** Tener instalada la última versión de Scapy (pip install scapy).
2. **Permisos:** El script debe ejecutarse con privilegios de root (sudo) para permitir la inyección de paquetes en la interfaz de red.
3. **Protocolo habilitado:** El switch objetivo debe tener activado CDP (comando cdp run en Cisco).

## Capturas de Pantalla (Evidencias)

<img width="587" height="345" alt="image" src="https://github.com/user-attachments/assets/434a0f92-1198-47c8-8116-8001b0ed4faf" />

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

<img width="997" height="716" alt="image" src="https://github.com/user-attachments/assets/8248fd4b-f07f-46d4-9fe7-faea49462847" />


## 6. Medidas de Mitigación
Para proteger la infraestructura contra este tipo de ataques, se deben implementar las siguientes mejores prácticas:

* **Desactivar CDP Globalmente:** Si el protocolo no es estrictamente necesario, usar no cdp run.
* **Desactivar CDP en Puertos de Usuario:** Deshabilitar el protocolo en todas las interfaces que conectan a dispositivos finales (PCs, laptops) con el comando no cdp enable en la interfaz.
* **Control Plane Policing (CoPP):** Configurar políticas que limiten la cantidad de paquetes CDP que el procesador del switch puede recibir por segundo.
* **Habilitar Port-Security:** Aunque CDP es capa 2, limitar el número de MACs por puerto puede ayudar a mitigar el impacto colateral de herramientas de ataque



