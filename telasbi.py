import time
import subprocess
from screeninfo import get_monitors
import pygetwindow as gw
import pyautogui as pa

# --- CONFIGURAÇÕES ---
CHROME_EXE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PROFILE_DIR = r"C:\Users\calyme.santos\AppData\Local\Google\Chrome\User Data"
PROFILE_NAME = "Default"

urls = [
    "https://app.powerbi.com/groups/d702a34a-014d-4648-907f-c7db7e866666/reports/96202848-3ed9-49f1-8eef-4db4788ef112/f3e2df5a5423ea6a8949?experience=power-bi&chromeless=1",
    "https://app.powerbi.com/groups/d702a34a-014d-4648-907f-c7db7e866666/reports/e16448ab-e673-4e98-b2e9-53c1dd294dc1/8326f342dc397d3d73a5?experience=power-bi&chromeless=1"
]

# --- Detecta monitores disponíveis ---
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
    """Move a janela para o monitor especificado usando coordenadas diretas"""
    try:
        janela.activate()
        time.sleep(0.5)
        janela.moveTo(monitor.x, monitor.y)
        janela.resizeTo(monitor.width, monitor.height)
        time.sleep(1)
        janela.activate()
        pa.press("f11")  # tela cheia
        time.sleep(1)
        print(f"✅ Janela posicionada em monitor com x={monitor.x}, y={monitor.y}")
    except Exception as e:
        print("⚠️ Erro ao mover ou colocar em tela cheia:", e)

# --- Loop principal ---
for i, url in enumerate(urls):
    monitor = monitores[i % n_monitores]
    janelas_antes = chrome_janelas_existentes()

    abrir_chrome_nova_janela(url)
    print(f"Abrindo URL: {url}")

    janela_encontrada = esperar_janela_nova(janelas_antes, timeout=20)
    if not janela_encontrada:
        print("⚠️ Não foi possível identificar a janela recém-aberta. Pulando para próxima URL.")
        continue

    mover_para_monitor(janela_encontrada, monitor)
    time.sleep(1)  # espera antes de abrir a próxima janela

print("🎯 Todas as janelas abertas, distribuídas e em tela cheia (F11).")
