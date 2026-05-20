# 🌐 TransData Logistics — PoC Red Corporativa

Prueba de Concepto para el diseño e implementación de una red empresarial estandarizada para la empresa ficticia *TransData Logistics S.A. de C.V.*, simulada en Cisco Packet Tracer con automatización en Python.

---

## 📁 Estructura del Repositorio

```
📦 TransData-PoC
 ┣ 📂 PoC
 ┃ ┗ 📄 TransData.pkt         ← Topología completa en Cisco Packet Tracer
 ┣ 📂 src
 ┃ ┣ 📄 auto.py               ← Script principal de automatización
 ┃ ┗ 📄 .env.example          ← Plantilla de variables de entorno
 ┣ 📄 .gitignore
 ┗ 📄 README.md
```

> **`PoC/`** — Archivo `.pkt` con las 5 sedes, ISP central, switches capa 2/3, WLC y APs.  
> **`src/`** — Script Python que automatiza la conexión SSH y genera el reporte `.xlsx`.

---

## 🏗️ Topología de Red

Diseño jerárquico en tres capas (acceso, distribución y núcleo) replicado en cada sede.

**Sedes:**
- 🏢 Oficinas Centrales — CDMX — `10.1.X.X` — Router-ID `1.1.1.1`
- 🏭 Sucursal Norte — Monterrey — `10.2.X.X` — Router-ID `1.1.2.1`
- 🏬 Sucursal Bajío — Querétaro — `10.3.X.X` — Router-ID `1.1.3.1`
- 🏪 Sucursal Occidente — Guadalajara — `10.4.X.X` — Router-ID `1.1.4.1`
- 📦 Centro de Distribución — León — `10.5.X.X` — Router-ID `1.1.5.1`

### ✅ Tecnologías implementadas

- **Segmentación** — VLANs (Admin `10`, Ventas `20`, Logística `30`, Invitados `40`, Mgmt `99`)
- **Ruteo interno** — OSPF por sede (proceso privado)
- **Ruteo WAN** — OSPF proceso 1 compartido con ISP
- **Seguridad** — 10 túneles VPN IPsec site-to-site en malla completa
- **Traducción de direcciones** — NAT/PAT + NAT estático para servicios
- **Alta disponibilidad** — HSRP + EtherChannel LACP
- **Control de acceso** — ACLs extendidas por VLAN
- **Administración** — NTP, Syslog y SNMP centralizados

---

## 🤖 Automatización

El script `src/auto.py` realiza tres tareas:

```
1. Ping preventivo  →  Valida conectividad antes de conectar
2. Conexión SSH     →  Netmiko + enable mode
3. Reporte Excel    →  3 pestañas con formato profesional
```

El reporte generado contiene:
- **Conectividad** — resultado del `ping -n 4 [host]` desde Windows
- **Configuracion** — salida completa de `show running-config`
- **Interfaces** — salida completa de `show interfaces`

---

## 🚀 Cómo ejecutar

### 1. Instalar dependencias

```bash
pip install netmiko pandas xlsxwriter python-dotenv
```

### 2. Crear archivo `.env`

```env
ROUTER_HOST=192.168.X.X
ROUTER_USER=admin
ROUTER_PASS=cisco
ROUTER_SECRET=cisco
```

> ⚠️ El archivo `.env` está en `.gitignore` — nunca subas tus credenciales al repositorio.

### 3. Ejecutar

```bash
python src/auto.py
```

El reporte se genera en el directorio actual como `reporte_HHMM.xlsx`.

---

## 🛠️ Stack tecnológico

- **Cisco Packet Tracer** — Simulación de red
- **Python 3.x** — Lenguaje principal
- **`Netmiko`** — Conexión SSH a dispositivos Cisco
- **`Pandas`** + **`XlsxWriter`** — Procesamiento y generación de Excel
- **`python-dotenv`** — Manejo seguro de credenciales
- **`subprocess`** — Ejecución de comandos de sistema
