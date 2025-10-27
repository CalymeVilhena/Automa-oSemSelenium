from screeninfo import get_monitors

for i, monitor in enumerate(get_monitors()):
    print(f"Monitor {i + 1}:")
    print(f"  Resolução: {monitor.width}x{monitor.height}")
    print(f"  Posição: x={monitor.x}, y={monitor.y}")
    print("-" * 30)