import numpy as np
import pygame

class AudioManager:
    def __init__(self):
        # FIX 1: Initialize pygame mixer explicitly in STEREO (channels=2)
        pygame.mixer.init(frequency=44100, size=-16, channels=2)
        
        # Synthesize our game sounds automatically!
        self.snd_score = self._generate_sound(freq=880, duration=0.2, wave_type='sine')
        self.snd_hit = self._generate_sound(freq=150, duration=0.3, wave_type='noise')
        self.snd_bounce = self._generate_sound(freq=440, duration=0.1, wave_type='sine')

    def _generate_sound(self, freq, duration, wave_type='sine'):
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        
        if wave_type == 'sine':
            # A clean beep
            wave = np.sin(freq * t * 2 * np.pi)
        elif wave_type == 'noise':
            # A crunch/static sound for taking damage
            wave = np.random.uniform(-1, 1, len(t))
            wave *= np.sin(freq * t * 2 * np.pi) # Ring modulate it
            
        # Apply a fade-out envelope so it doesn't click at the end
        envelope = np.linspace(1, 0, len(wave))
        audio_data = np.int16(wave * envelope * 32767)
        
        # FIX 2: Pygame wants a 2D array for stereo sound (Left and Right channels)
        # We duplicate our mono audio data into two columns to create a stereo array.
        stereo_audio = np.column_stack((audio_data, audio_data))
        
        # Convert numpy array to pygame sound
        return pygame.sndarray.make_sound(stereo_audio)

    def play_score(self):
        self.snd_score.play()

    def play_hit(self):
        self.snd_hit.play()
        
    def play_bounce(self):
        self.snd_bounce.play()