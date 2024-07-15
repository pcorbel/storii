import os

import pygame

# Initialize Pygame and Mixer
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FONT_SIZE = 30
CHEVRON_SIZE = (64, 64)
COVER_SIZE = (256, 256)
ICON_SIZE = (256, 256)
PADDING = 20
PROGRESS_BAR_HEIGHT = 10
PROGRESS_BAR_PADDING = 40
PROGRESS_BAR_Y = SCREEN_HEIGHT - 50
APP_BAR_HEIGHT = 24

# Colors
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)

# Paths
SCRIPT_PATH = os.path.abspath(__file__)
SCRIPT_DIR = os.path.dirname(SCRIPT_PATH)
FONT_PATH = os.path.join(SCRIPT_DIR, "res", "roboto-bold.ttf")
CHEVRON_LEFT_PATH = os.path.join(SCRIPT_DIR, "res", "chevron-left.png")
CHEVRON_RIGHT_PATH = os.path.join(SCRIPT_DIR, "res", "chevron-right.png")
DEFAULT_IMG_PATH = os.path.join(SCRIPT_DIR, "res", "image.png")
PLAY_ICON_PATH = os.path.join(SCRIPT_DIR, "res", "play.png")
PAUSE_ICON_PATH = os.path.join(SCRIPT_DIR, "res", "pause.png")
BATTERY_ICON_PATH = os.path.join(SCRIPT_DIR, "res", "battery.png")
STORIIES_PATH = os.environ["STORIIES_PATH"]
PWM_PATH = "/sys/devices/soc0/soc/1f003400.pwm/pwm/pwmchip0/pwm0/duty_cycle"
BATTERY_PERC_PATH = "/tmp/percBat"
STARTUP_PATH = "/mnt/SDCARD/.tmp_update/startup/launch-storii-startup.sh"

# Konami Code
KONAMI_CODE = [
    pygame.K_UP,
    pygame.K_UP,
    pygame.K_DOWN,
    pygame.K_DOWN,
    pygame.K_LEFT,
    pygame.K_RIGHT,
    pygame.K_LEFT,
    pygame.K_RIGHT,
    pygame.K_LCTRL,
    pygame.K_SPACE,
]
