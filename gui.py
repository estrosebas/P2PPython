import socket
import os
import threading
from tkinter import filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from pathlib import Path
import logging

class P2PFileTransfer:
    def __init__(self):
        self.window = ttk.Window(
            title="P2P File Transfer",
            themename="cosmo",
            size=(800, 600),
            resizable=(True, True)
        )
        self.window.place_window_center()
        
        # Iconos Unicode
        self.icons = {
            'swap': '🔄',
            'upload': '⬆️',
            'download': '⬇️',
            'pc': '💻',
            'network': '🌐',
            'folder': '📁',
            'file': '📄',
            'search': '🔍',
            'info': 'ℹ️',
            'send': '📤'
        }
        
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(
            self.window,
            padding=20
        )
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título con icono
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill="x", pady=(0, 20))
        
        title_icon = ttk.Label(
            title_frame,
            text=self.icons['swap'],
            font=("Segoe UI Emoji", 24)
        )
        title_icon.pack(side="left", padx=(0, 10))
        
        title = ttk.Label(
            title_frame,
            text="P2P File Transfer",
            font=("Helvetica", 24, "bold"),
            bootstyle="primary"
        )
        title.pack(side="left")
        
        # Selección de modo con iconos
        self.mode_var = ttk.StringVar(value="send")
        mode_frame = ttk.LabelFrame(
            main_frame,
            text="Transfer Mode",
            padding=10
        )
        mode_frame.pack(fill="x", pady=10)
        
        send_frame = ttk.Frame(mode_frame)
        send_frame.pack(side="left", padx=20)
        
        send_icon = ttk.Label(
            send_frame,
            text=self.icons['upload'],
            font=("Segoe UI Emoji", 14)
        )
        send_icon.pack(side="left", padx=5)
        
        send_radio = ttk.Radiobutton(
            send_frame,
            text="Send",
            variable=self.mode_var,
            value="send",
            command=self.update_ui,
            bootstyle="primary-toolbutton"
        )
        send_radio.pack(side="left")
        
        receive_frame = ttk.Frame(mode_frame)
        receive_frame.pack(side="left")
        
        receive_icon = ttk.Label(
            receive_frame,
            text=self.icons['download'],
            font=("Segoe UI Emoji", 14)
        )
        receive_icon.pack(side="left", padx=5)
        
        receive_radio = ttk.Radiobutton(
            receive_frame,
            text="Receive",
            variable=self.mode_var,
            value="receive",
            command=self.update_ui,
            bootstyle="primary-toolbutton"
        )
        receive_radio.pack(side="left")
        
        # Frame para campos de conexión
        connection_frame = ttk.LabelFrame(
            main_frame,
            text="Connection Details",
            padding=10
        )
        connection_frame.pack(fill="x", pady=10)
        
        # IP Address
        ip_frame = ttk.Frame(connection_frame)
        ip_frame.pack(fill="x", pady=5)
        
        ip_icon = ttk.Label(
            ip_frame,
            text=self.icons['pc'],
            font=("Segoe UI Emoji", 14)
        )
        ip_icon.pack(side="left", padx=5)
        
        ttk.Label(
            ip_frame,
            text="IP Address:",
            width=10
        ).pack(side="left")
        
        self.ip_entry = ttk.Entry(ip_frame)
        self.ip_entry.insert(0, "localhost")
        self.ip_entry.pack(side="left", fill="x", expand=True)
        
        # Port
        port_frame = ttk.Frame(connection_frame)
        port_frame.pack(fill="x", pady=5)
        
        port_icon = ttk.Label(
            port_frame,
            text=self.icons['network'],
            font=("Segoe UI Emoji", 14)
        )
        port_icon.pack(side="left", padx=5)
        
        ttk.Label(
            port_frame,
            text="Port:",
            width=10
        ).pack(side="left")
        
        self.port_entry = ttk.Entry(port_frame)
        self.port_entry.insert(0, "5000")
        self.port_entry.pack(side="left", fill="x", expand=True)
        
        # File selection frame
        file_frame = ttk.LabelFrame(
            main_frame,
            text="File Selection",
            padding=10
        )
        file_frame.pack(fill="x", pady=10)
        
        # Path selection
        path_frame = ttk.Frame(file_frame)
        path_frame.pack(fill="x", pady=5)
        
        self.path_icon = ttk.Label(
            path_frame,
            text=self.icons['folder'],
            font=("Segoe UI Emoji", 14)
        )
        self.path_icon.pack(side="left", padx=5)
        
        self.path_label = ttk.Label(
            path_frame,
            text="File Path:",
            width=10
        )
        self.path_label.pack(side="left")
        
        self.path_var = ttk.StringVar()
        self.path_entry = ttk.Entry(
            path_frame,
            textvariable=self.path_var
        )
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.browse_button = ttk.Button(
            path_frame,
            text=" Browse",
            compound="left",
            command=self.browse_path,
            bootstyle="primary-outline"
        )
        self.browse_button.configure(text=f"{self.icons['search']} Browse")
        self.browse_button.pack(side="right")
        
        # Progress frame
        progress_frame = ttk.LabelFrame(
            main_frame,
            text="Transfer Progress",
            padding=10
        )
        progress_frame.pack(fill="x", pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            progress_frame,
            length=400,
            mode="determinate",
            bootstyle="primary-striped"
        )
        self.progress.pack(fill="x", pady=10)
        
        # Status
        status_frame = ttk.Frame(progress_frame)
        status_frame.pack(fill="x")
        
        status_icon = ttk.Label(
            status_frame,
            text=self.icons['info'],
            font=("Segoe UI Emoji", 14)
        )
        status_icon.pack(side="left", padx=5)
        
        self.status_var = ttk.StringVar(value="Ready")
        self.status_label = ttk.Label(
            status_frame,
            textvariable=self.status_var
        )
        self.status_label.pack(side="left")
        
        # Transfer button
        self.transfer_button = ttk.Button(
            main_frame,
            compound="left",
            command=self.start_transfer,
            bootstyle="primary"
        )
        self.transfer_button.pack(pady=20)
        
        self.update_ui()
    
    def update_ui(self):
        is_send_mode = self.mode_var.get() == "send"
        self.path_label.config(
            text="File Path:" if is_send_mode else "Save Dir:"
        )
        self.path_icon.config(
            text=self.icons['file'] if is_send_mode else self.icons['folder']
        )
        self.transfer_button.configure(
            text=f"{self.icons['send']} {'Send File' if is_send_mode else 'Receive File'}"
        )
    
    def browse_path(self):
        if self.mode_var.get() == "send":
            path = filedialog.askopenfilename(title="Select File to Send")
        else:
            path = filedialog.askdirectory(title="Select Save Directory")
        
        if path:
            self.path_var.set(path)
    
    def update_progress(self, current, total):
        progress = (current / total) * 100
        self.progress["value"] = progress
        self.window.update_idletasks()
    
    def start_transfer(self):
        # Get values from UI
        mode = self.mode_var.get()
        host = self.ip_entry.get()
        
        try:
            port = int(self.port_entry.get())
        except ValueError:
            ttk.Messagebox.show_error(
                title="Error",
                message="Port must be a number",
                parent=self.window
            )
            return
        
        path = self.path_var.get()
        
        if not all([host, port, path]):
            ttk.Messagebox.show_warning(
                title="Missing Information",
                message="Please fill in all fields",
                parent=self.window
            )
            return
        
        # Start transfer in a separate thread
        self.transfer_button.config(state="disabled")
        self.status_var.set("Transfer in progress...")
        
        thread = threading.Thread(
            target=self.handle_transfer,
            args=(mode, host, port, path)
        )
        thread.start()
    
    def handle_transfer(self, mode, host, port, path):
        try:
            if mode == "send":
                self.send_file(host, port, path)
            else:
                self.receive_file(host, port, path)
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            ttk.Messagebox.show_error(
                title="Error",
                message=str(e),
                parent=self.window
            )
        finally:
            self.transfer_button.config(state="normal")
            self.progress["value"] = 0
    
    def send_file(self, host, port, file_path):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))
            
            # Send file info
            file_size = os.path.getsize(file_path)
            file_name = os.path.basename(file_path)
            header = f"{file_name}|{file_size}"
            client_socket.send(header.encode())
            
            # Wait for acknowledgment
            client_socket.recv(1024)
            
            # Send file data
            sent = 0
            with open(file_path, "rb") as file:
                while True:
                    data = file.read(8192)
                    if not data:
                        break
                    client_socket.sendall(data)
                    sent += len(data)
                    self.update_progress(sent, file_size)
            
            self.status_var.set("File sent successfully!")
    
    def receive_file(self, host, port, save_dir):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((host, port))
            server_socket.listen(1)
            self.status_var.set("Waiting for connection...")
            
            conn, addr = server_socket.accept()
            with conn:
                # Receive file info
                header = conn.recv(1024).decode()
                file_name, file_size = header.split("|")
                file_size = int(file_size)
                
                # Send acknowledgment
                conn.send(b"OK")
                
                # Receive file data
                save_path = os.path.join(save_dir, file_name)
                received = 0
                
                with open(save_path, "wb") as file:
                    while received < file_size:
                        data = conn.recv(8192)
                        if not data:
                            break
                        file.write(data)
                        received += len(data)
                        self.update_progress(received, file_size)
                
                self.status_var.set("File received successfully!")

if __name__ == "__main__":
    app = P2PFileTransfer()
    app.window.mainloop()