import keyboard

print("Pressione qualquer tecla (ESC para sair):")

while True:
    event = keyboard.read_event()
    if event.event_type == keyboard.KEY_DOWN:
        print(f"Tecla pressionada: {event.name}")
        if event.name == "esc":
            print("Encerrando...")
            break