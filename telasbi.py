import time
import subprocess
from screeninfo import get_monitors
import pygetwindow as gw
import pyautogui as pa

# --- CONFIGURAÇÕES ---
CHROME_EXE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PROFILE_DIR = r"C:\Users\calyme.santos\AppData\Local\Google\Chrome\User Data"
PROFILE_NAME = "Default"

# Dashboards a abrir
urls = [
    "https://app.powerbi.com/groups/5c03b87e-c5cf-4df7-b6cb-7de67718eb23/reports/b14eca2e-bf90-4424-9eb4-35b4c0ad5512/d1b77882d3ec4d4bab8d?chromeless=1",
    "https://app.powerbi.com/groups/d702a34a-014d-4648-907f-c7db7e866666/reports/d351ccee-9056-4c85-9fae-d3ebc72fc927/56d9bc526243eb2b7e90?chromeless=1"
]

# --- Detecta monitores ---
monitores = get_monitors()
n_monitores = len(monitores)
print(f"Monitores detectados: {n_monitores}")
for i, m in enumerate(monitores):
    print(f"Monitor {i+1}: x={m.x}, y={m.y}, width={m.width}, height={m.height}")

# --- Funções auxiliares ---
def chrome_janelas_existentes():
    """Retorna lista de janelas do Chrome abertas"""
    return gw.getWindowsWithTitle("Chrome")

def abrir_chrome_nova_janela(url):
    """Abre uma nova janela do Chrome com perfil logado"""
    args = [
        CHROME_EXE,
        "--new-window",
        "--disable-gpu",
        "--disable-software-rasterizer",
        "--start-maximized",
        f"--user-data-dir={PROFILE_DIR}",
        f"--profile-directory={PROFILE_NAME}",
        url
    ]
    subprocess.Popen(args)

def esperar_janela_nova(janelas_antes, timeout=20):
    """Espera até que uma nova janela do Chrome apareça"""
    for _ in range(int(timeout / 0.5)):
        janelas_depois = chrome_janelas_existentes()
        novas = [j for j in janelas_depois if j not in janelas_antes]
        if novas:
            return novas[0]
        time.sleep(0.5)
    return None

def mover_para_monitor(janela, monitor):
    """Move a janela para o monitor especificado"""
    try:
        janela.activate()
        time.sleep(0.5)
        janela.moveTo(monitor.x, monitor.y)
        janela.resizeTo(monitor.width, monitor.height)
        time.sleep(1)
        janela.activate()
        pa.press("f11")  # Tela cheia
        print(f"✅ Janela posicionada em monitor {monitor.x}, {monitor.y}")
    except Exception as e:
        print("⚠️ Erro ao mover:", e)

# --- Loop principal ---
for i, url in enumerate(urls):
    if i >= n_monitores:
        print("⚠️ Mais dashboards do que monitores disponíveis.")
        break

    monitor = monitores[i]
    print(f"🌐 Abrindo dashboard {i+1} no monitor {i+1}")

    janelas_antes = chrome_janelas_existentes()
    abrir_chrome_nova_janela(url)
    time.sleep(2)

    janela_encontrada = esperar_janela_nova(janelas_antes)
    if janela_encontrada:
        mover_para_monitor(janela_encontrada, monitor)
    else:
        print(f"⚠️ Janela {i+1} não detectada.")
    time.sleep(3)

print("🎯 Todas as janelas abertas, distribuídas e em tela cheia!")
