import tkinter as tk
from tkinter import ttk
import psutil
import platform
import datetime

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

class BenchmarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitor de Hardware em Tempo Real - Benchmark")
        self.root.geometry("600x700")
        
        # Estilo
        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 10))
        style.configure("Header.TLabel", font=("Arial", 12, "bold"))

        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.text_area = tk.Text(self.main_frame, wrap=tk.WORD, font=("Consolas", 10), bg="#1e1e1e", fg="#00ff00")
        self.text_area.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(self.text_area, command=self.text_area.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.config(yscrollcommand=scrollbar.set)

        self.update_data()

    def get_system_info(self):
        info = []
        info.append("=== INFORMAÇÕES DO SISTEMA E SO ===")
        info.append(f"Sistema: {platform.system()} {platform.release()}")
        info.append(f"Versão: {platform.version()}")
        info.append(f"Arquitetura: {platform.machine()}")
        info.append(f"Processador: {platform.processor()}\n")

        info.append("=== CPU (Tempo Real) ===")
        cpu_freq = psutil.cpu_freq()
        info.append(f"Núcleos Físicos: {psutil.cpu_count(logical=False)}")
        info.append(f"Total de Threads: {psutil.cpu_count(logical=True)}")
        if cpu_freq:
            info.append(f"Frequência Máxima: {cpu_freq.max:.2f}Mhz")
            info.append(f"Frequência Atual: {cpu_freq.current:.2f}Mhz")
        info.append(f"Uso Total da CPU: {psutil.cpu_percent()}%")
        
        core_usage = psutil.cpu_percent(percpu=True)
        for i, percentage in enumerate(core_usage):
            info.append(f"  Núcleo {i}: {percentage}%")
        info.append("")

        info.append("=== MEMÓRIA RAM (Tempo Real) ===")
        svmem = psutil.virtual_memory()
        info.append(f"Total: {get_size(svmem.total)}")
        info.append(f"Disponível: {get_size(svmem.available)}")
        info.append(f"Em Uso: {get_size(svmem.used)}")
        info.append(f"Porcentagem de Uso: {svmem.percent}%\n")

        info.append("=== ARMAZENAMENTO ===")
        partitions = psutil.disk_partitions()
        for partition in partitions:
            info.append(f"Dispositivo: {partition.device} ({partition.mountpoint})")
            info.append(f"  Tipo de Sistema de Arquivos: {partition.fstype}")
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
                info.append(f"  Tamanho Total: {get_size(partition_usage.total)}")
                info.append(f"  Usado: {get_size(partition_usage.used)} ({partition_usage.percent}%)")
                info.append(f"  Livre: {get_size(partition_usage.free)}")
            except PermissionError:
                info.append("  [Acesso Negado]")
        info.append("")

        info.append("=== REDE ===")
        if_addrs = psutil.net_if_addrs()
        for interface_name, interface_addresses in if_addrs.items():
            for address in interface_addresses:
                if str(address.family) == 'AddressFamily.AF_INET':
                    info.append(f"Interface: {interface_name}")
                    info.append(f"  Endereço IP: {address.address}")
                    info.append(f"  Máscara: {address.netmask}")
        
        net_io = psutil.net_io_counters()
        info.append(f"\nTotal de Dados Enviados: {get_size(net_io.bytes_sent)}")
        info.append(f"Total de Dados Recebidos: {get_size(net_io.bytes_recv)}")

        return "\n".join(info)

    def update_data(self):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, self.get_system_info())
        self.text_area.config(state=tk.DISABLED)
        
        self.root.after(1000, self.update_data)

if __name__ == "__main__":
    root = tk.Tk()
    app = BenchmarkApp(root)
    root.mainloop()