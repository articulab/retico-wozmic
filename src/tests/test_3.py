import pygame
import threading
import time
import keyboard

# THREAD_ACTIVE = False

# def on_key_event(e):
#     if e.name == 'm':
#         print("M was pressed!")
#         time.sleep(1)

# def run_process():
#     while THREAD_ACTIVE:
#         keyboard.on_press(on_key_event)

#         # # Keep the program running
#         # keyboard.wait('esc')  # Press ESC to stop


# if __name__ == "__main__":
    
#     THREAD_ACTIVE = True
#     threading.Thread(target=run_process).start()
    
#     # running system
#     try:
#         print("Dialog system running until ENTER key is pressed")
#         input()
#         THREAD_ACTIVE = False
#     except Exception as e:
#         print("exception in main", e)
        
        

# import os
# os.environ["SDL_VIDEODRIVER"] = "dummy"  # No window

# import pygame

# pygame.init()
# screen = pygame.display.set_mode((1, 1))  # Required even if dummy
# pygame.display.set_caption("Headless Input")

# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_m:
#                 print("M was pressed")
#             elif event.key == pygame.K_ESCAPE:
#                 running = False

# pygame.quit()


import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Press M Example")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                print("M was pressed!")

pygame.quit()