import pygame
import time

time.sleep(30)  #30 sec time sleep
pygame.mixer.init()
pygame.mixer.music.load("myFileName.wav")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue