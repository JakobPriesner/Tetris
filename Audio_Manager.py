import pygame


class Audio_Manager:
    def __init__(self, volume, loops, channel, fading_time=0, audio_file=None, play=False):
        self.volume = volume
        print(audio_file)
        if audio_file is not None:

            self.audio_file = pygame.mixer.Sound(audio_file)
        else:
            self.audio_file = None
        self.channel = channel
        self.loop = loops
        self.fading_time = fading_time
        self.set_volume(self.volume)

        if play:
            self.play()

    def play(self, audio_file=None):
        if audio_file is None:
            if self.audio_file is not None:
                pygame.mixer.Channel(self.channel).play(self.audio_file, self.loop, self.fading_time)
        else:
            temp_audio_file = pygame.mixer.Sound(audio_file)
            pygame.mixer.Channel(self.channel).play(temp_audio_file, self.loop, self.fading_time)

    def pause(self):
        pygame.mixer.Channel(self.channel).pause()

    def stop(self):
        pygame.mixer.Channel(self.channel).stop()

    def resume(self):
        pygame.mixer.Channel(self.channel).unpause()

    def get_busy(self):
        return pygame.mixer.Channel(self.channel).get_busy()

    def set_volume(self, volume):
        self.volume = volume
        pygame.mixer.Channel(self.channel).set_volume(volume/100)