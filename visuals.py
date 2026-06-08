# visuals.py
import cv2
import numpy as np
import random

class VisualFX:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.particles = []
        self.grid_offset = 0.0

    def draw_cyber_grid(self, frame):
        # Background color (Dark blue/purple)
        frame[:] = (20, 10, 15)
        
        # Move grid downward to create illusion of forward movement
        self.grid_offset += 2.0
        if self.grid_offset >= 40:
            self.grid_offset = 0

        # Draw vertical lines
        for x in range(0, self.width, 40):
            cv2.line(frame, (x, 0), (x, self.height), (40, 20, 40), 1)

        # Draw horizontal moving lines
        for y in range(int(self.grid_offset), self.height, 40):
            # Fade lines out towards the top for depth
            brightness = int(255 * (y / self.height))
            color = (brightness, int(brightness/2), brightness)
            cv2.line(frame, (0, y), (self.width, y), color, 1)

    def spawn_particles(self, x, y, color):
        # Spawn 15 particles moving in random directions
        for _ in range(15):
            vx = random.uniform(-5, 5)
            vy = random.uniform(-5, 5)
            life = random.randint(15, 30)
            self.particles.append({'x': x, 'y': y, 'vx': vx, 'vy': vy, 'life': life, 'max_life': life, 'color': color})

    def update_and_draw_particles(self, frame):
        for p in self.particles[:]:
            # Move particle
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['life'] -= 1
            
            if p['life'] <= 0:
                self.particles.remove(p)
            else:
                # Shrink radius based on remaining life
                radius = max(1, int(4 * (p['life'] / p['max_life'])))
                cv2.circle(frame, (int(p['x']), int(p['y'])), radius, p['color'], -1)