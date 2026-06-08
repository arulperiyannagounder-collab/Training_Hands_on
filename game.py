# main.py
import cv2
import numpy as np
import math
import random
from collections import deque
from audio import AudioManager
from visuals import VisualFX

# Initialize external modules
audio = AudioManager()
fx = VisualFX(500, 500)

# Game State
ball_pos = [250.0, 50.0]
ball_vel = [0.0, 0.0]
ball_radius = 10
score = 0
lives = 3
trail = deque(maxlen=7)

mouse_pos = (250, 250)
anomaly_radius = 90  

target_pos = [250, 300]
target_radius = 15

# Screen Shake variable
shake_frames = 0

def mouse_callback(event, x, y, flags, param):
    global mouse_pos
    if event == cv2.EVENT_MOUSEMOVE:
        mouse_pos = (x, y)

cv2.namedWindow("Temporal Tether")
cv2.setMouseCallback("Temporal Tether", mouse_callback)

while True:
    # 1. Blank Canvas & Background
    game_window = np.zeros((500, 500, 3), dtype=np.uint8)
    fx.draw_cyber_grid(game_window)

    # 2. Physics & Controls
    dx = mouse_pos[0] - ball_pos[0]
    dy = mouse_pos[1] - ball_pos[1]
    distance = math.hypot(dx, dy)

    if distance < anomaly_radius:
        ball_vel[1] -= 1.0  # Anti-gravity
        ball_vel[0] += (dx / max(distance, 1)) * 0.6
        cv2.circle(game_window, mouse_pos, anomaly_radius, (60, 20, 60), -1)
        ball_color = (0, 255, 255)
    else:
        ball_vel[1] += 0.5  # Normal gravity
        ball_vel[0] *= 0.98
        cv2.circle(game_window, mouse_pos, anomaly_radius, (50, 50, 50), 1)
        ball_color = (0, 0, 255)

    # Speed limits
    ball_vel[1] = max(-10, min(ball_vel[1], 10))
    ball_vel[0] = max(-8, min(ball_vel[0], 8))

    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    trail.append((ball_pos[0], ball_pos[1]))

    # 3. Collisions
    # Wall Bounce
    if ball_pos[0] <= ball_radius or ball_pos[0] >= 500 - ball_radius:
        ball_vel[0] *= -0.8
        ball_pos[0] = max(ball_radius, min(ball_pos[0], 500 - ball_radius))
        audio.play_bounce()

    # Ceiling Bounce
    if ball_pos[1] <= ball_radius:
        ball_vel[1] *= -0.5
        ball_pos[1] = ball_radius
        audio.play_bounce()

    # Floor / Damage
    if ball_pos[1] >= 500 - ball_radius:
        audio.play_hit()
        fx.spawn_particles(ball_pos[0], ball_pos[1], (0, 0, 255))
        shake_frames = 10
        lives -= 1
        score = max(0, score - 1)
        ball_pos = [250.0, 50.0]
        ball_vel = [0.0, 0.0]
        trail.clear()
        if lives <= 0:
            print("Game Over! Final Score:", score)
            break

    # Target Collision (Scoring)
    t_dist = math.hypot(target_pos[0] - ball_pos[0], target_pos[1] - ball_pos[1])
    if t_dist < (ball_radius + target_radius):
        audio.play_score()
        fx.spawn_particles(target_pos[0], target_pos[1], (0, 255, 0))
        score += 1
        target_pos = [random.randint(50, 450), random.randint(100, 400)]

    # 4. Drawing Target, Particles, and Ball
    cv2.circle(game_window, (int(target_pos[0]), int(target_pos[1])), target_radius, (0, 255, 0), 2)
    fx.update_and_draw_particles(game_window)

    for i, pos in enumerate(trail):
        t_radius = int(ball_radius * ((i + 1) / len(trail)))
        cv2.circle(game_window, (int(pos[0]), int(pos[1])), t_radius, (150, 150, 150), -1)

    cv2.circle(game_window, (int(ball_pos[0]), int(ball_pos[1])), ball_radius, ball_color, -1)

    # 5. Screen Shake Effect
    if shake_frames > 0:
        shake_x = random.randint(-5, 5)
        shake_y = random.randint(-5, 5)
        M = np.float32([[1, 0, shake_x], [0, 1, shake_y]])
        game_window = cv2.warpAffine(game_window, M, (500, 500))
        shake_frames -= 1

    # UI
    cv2.putText(game_window, f"Score: {score}", (15, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(game_window, f"Lives: {lives}", (380, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (50, 50, 255), 2)

    cv2.imshow("Temporal Tether", game_window)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

