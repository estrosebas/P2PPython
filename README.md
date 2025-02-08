Aquí tienes el `README.md` en formato Markdown completo:

````markdown
# P2P File Transfer 📤📥

Este es un programa de transferencia de archivos P2P con una interfaz gráfica desarrollada en Python usando `ttkbootstrap`. Permite enviar y recibir archivos fácilmente a través de una conexión de red.

## 🚀 Características

- Interfaz gráfica intuitiva con `ttkbootstrap`
- Modo de envío y recepción de archivos
- Configuración sencilla de IP y puerto
- Selección de archivos con explorador de archivos
- Iconos Unicode para una mejor experiencia visual
- Registro de eventos con `logging`

## 🛠️ Instalación

### 📌 Requisitos

Asegúrate de tener instalado Python 3 y las siguientes dependencias:

```bash
pip install ttkbootstrap
```
````

## 🎮 Uso

Ejecuta el script y sigue las instrucciones en la interfaz.

```bash
python p2p_transfer.py
```

### Modo Envío 📤

1. Selecciona el modo **Send**.
2. Introduce la dirección IP y el puerto del destinatario.
3. Selecciona el archivo a enviar.
4. Pulsa el botón **Send**.

### Modo Recepción 📥

1. Selecciona el modo **Receive**.
2. Introduce la dirección IP y el puerto donde escucharás conexiones.
3. Pulsa **Start Server** y espera la transferencia.

## 🔧 Configuración

Puedes modificar los valores predeterminados de IP y puerto editando las entradas en la interfaz o en el código:

```python
self.ip_entry.insert(0, "localhost")
self.port_entry.insert(0, "5000")
```

## ⚠️ Notas

- Asegúrate de que el firewall permite conexiones en el puerto configurado.
- Para transferencias en redes externas, el destinatario puede necesitar abrir puertos en su router.

## 📜 Licencia

Este proyecto está bajo la licencia MIT.

---

💡 Desarrollado con ❤️ en Python.

```

Puedes copiar y pegarlo directamente en tu archivo `README.md`. Si necesitas cambios, dime. 🚀
```
