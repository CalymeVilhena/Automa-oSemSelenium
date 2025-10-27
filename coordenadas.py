import pyautogui
import time

print("Posicione o mouse onde deseja obter as coordenadas e aguarde 5 segundos...")
time.sleep(5)

x, y = pyautogui.position()
print(f"As coordenadas do mouse são: X={x}, Y={y}")