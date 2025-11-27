import pygame

pygame.mixer.init()

class AudioManager:
    def __init__(self):
        self.menu_music = "Codigos\Banda_Sonora\TombJ.mpeg"
        self.game_music = "Codigos\Banda_Sonora\Tomb.mpeg"

    def play_menu_music(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.menu_music)
        pygame.mixer.music.play(-1)   
        pygame.mixer.music.set_volume(0.7)

    def play_game_music(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.game_music)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.7)

    def stop_music(self):
        pygame.mixer.music.stop()
