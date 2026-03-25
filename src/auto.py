import os
import pandas as pd
from netmiko import ConnectHandler
from datetime import datetime
import subprocess
from dotenv import load_dotenv 

# Cargar las variables del archivo .env
load_dotenv() 

device = {
    'device_type': 'cisco_ios',
    'host': os.getenv('ROUTER_HOST'),      
    'username': os.getenv('ROUTER_USER'),  
    'password': os.getenv('ROUTER_PASS'),  
    'secret': os.getenv('ROUTER_SECRET'),  
    'conn_timeout': 20,
}

def run_windows_command(command):
    try:
        # Capturamos la salida del ping
        resultado = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return resultado.decode('cp1252')
    except Exception as e:
        return f"Error al ejecutar ping: {e}"

def run_audit():
    print(f"--- [{datetime.now().strftime('%H:%M:%S')}] Iniciando Captura de datos ---")
    
    try:
        #  Prueba de Ping 
        print(f"Probando conectividad (Ping) a {device['host']}...")
        ping_raw = run_windows_command(f"ping -n 4 {device['host']}")

        # Conexión al Router y Comandos
        print(f"Conectando a {device['host']}...")
        connection = ConnectHandler(**device)
        connection.enable()
        connection.send_command("terminal length 0")
        
        # Mandar el comando show interfaces y show running-config
        print("Capturando configuracion e interfaces...")
        run_config = connection.send_command("show running-config")
        interfaces_full = connection.send_command("show interfaces")
        connection.disconnect()

        # Preparación de datos para Excel
        print("Organizando excel...")
        df_ping = pd.DataFrame(ping_raw.split('\n'), columns=['Prueba de Ping'])
        df_config = pd.DataFrame(run_config.split('\n'), columns=['Configuración del Sistema'])
        df_interfaces = pd.DataFrame(interfaces_full.split('\n'), columns=['Detalle de Interfaces'])

        nombre = f"reporte_{datetime.now().strftime('%H%M')}.xlsx"

        with pd.ExcelWriter(nombre, engine='xlsxwriter') as writer:
            # Guardamos 3 pestañas de Excell
            df_ping.to_excel(writer, sheet_name='Conectividad', index=False)
            df_config.to_excel(writer, sheet_name='Configuracion', index=False)
            df_interfaces.to_excel(writer, sheet_name='Interfaces', index=False)
            
            workbook  = writer.book
            
            # --- ESTILOS ---
            header_format = workbook.add_format({
                'bold': True, 'fg_color': '#003366', 'font_color': 'white', 'border': 1
            })
            body_format = workbook.add_format({
                'font_name': 'Courier New', 'font_size': 10, 'fg_color': '#F8F8F8'
            })

            # Aplicar formato a todas las hojas
            for sheet_name in writer.sheets:
                worksheet = writer.sheets[sheet_name]
                worksheet.set_column('A:A', 120, body_format)
                
                # Títulos personalizados por pestaña
                if sheet_name == 'Conectividad':
                    worksheet.write('A1', f'PRUEBA DE PING {device["host"]}', header_format)
                elif sheet_name == 'Configuracion': # Corregido para que coincida con sheet_name arriba
                    worksheet.write('A1', 'CONFIGURACIÓN DE ROUTER', header_format)
                else:
                    worksheet.write('A1', 'ESTADO DE INTERFACES', header_format)
                
                worksheet.autofilter('A1:A1000')

        print(f"\n Excell generado: {nombre}")

    except Exception as e:
        print(f"\n Error: {e}")

if __name__ == "__main__":
    run_audit()