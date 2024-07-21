import os
import sys

import pygame

from config import *
from events import *
from ui import *
from utils import *


class StoryPlayer:
    def __init__(self):
        self.initialize_state()
        self.load_resources()
        self.setup_display()
        self.setup_timers()
        self.initialize_launch_at_startup()

    def initialize_state(self):
        self.is_running = True
        self.current_menu = "story"
        self.dim_mode = False
        self.konami_code = []
        self.konami_menu_options = ["Set Timer", "Launch at Startup", "Quit"]
        self.konami_menu_selected_index = 0
        self.timer_minutes = 0
        self.current_story_index = 0
        self.current_chapter_index = 0
        self.current_audio_position = 0
        self.audio_playing = False
        self.audio_total_length = 0
        self.key_press_delay = 200
        self.key_left_pressed = False
        self.key_right_pressed = False

    def load_resources(self):
        self.chevron_left_img = load_image(CHEVRON_LEFT_PATH, CHEVRON_SIZE)
        self.chevron_right_img = load_image(CHEVRON_RIGHT_PATH, CHEVRON_SIZE)
        self.play_icon_img = load_image(PLAY_ICON_PATH, ICON_SIZE)
        self.pause_icon_img = load_image(PAUSE_ICON_PATH, ICON_SIZE)
        self.battery_img = load_image(BATTERY_ICON_PATH, (APP_BAR_HEIGHT, APP_BAR_HEIGHT))
        self.story_list = get_stories()
        self.battery_level = get_battery_level()

    def setup_display(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF)
        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE)
        if not self.story_list:
            self.current_menu = "error"

    def setup_timers(self):
        self.last_key_press_time = 0
        self.last_status_update_time = 0
        self.last_activity_time = pygame.time.get_ticks()
        self.timer_start_time = None
        self.timer_duration = -1

    def initialize_launch_at_startup(self):
        self.launch_at_startup = os.path.exists("/mnt/SDCARD/.tmp_update/startup/launch-storii-startup.sh")

    def reset_to_initial_state(self):
        self.initialize_state()
        self.setup_timers()
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

    def reset_audio(self):
        self.audio_playing = False
        self.current_audio_position = 0
        self.audio_total_length = 0
        self.current_audio_file = None
        self.current_chapter_index = 0
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

    def start_audio(self):
        story = self.story_list[self.current_story_index]
        load_chapters_for_story(story)
        chapter = story["chapters"][self.current_chapter_index]
        self.current_audio_file = chapter["audio"]
        try:
            sampling_rate = get_audio_sampling_rate(self.current_audio_file)
            pygame.mixer.quit()
            pygame.mixer.init(frequency=sampling_rate)
            pygame.mixer.music.load(self.current_audio_file)
            pygame.mixer.music.set_volume(1.0)
            pygame.mixer.music.play()
            self.audio_playing = True
            self.audio_total_length = get_audio_length(self.current_audio_file)
        except Exception:
            self.audio_playing = False
            self.current_audio_file = None
            self.current_menu = "error"

    def handle_player_controls(self):
        if self.audio_playing:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
        self.audio_playing = not self.audio_playing
        self.draw_menu()

    def update_audio_position(self):
        if self.audio_playing:
            self.current_audio_position += 1 / 10.0
            if self.current_audio_position > self.audio_total_length:
                self.current_audio_position = self.audio_total_length

    def seek_audio(self, position):
        self.current_audio_position = max(0, min(position, self.audio_total_length))
        pygame.mixer.music.play(start=self.current_audio_position)
        if not self.audio_playing:
            pygame.mixer.music.pause()

    def fast_forward(self):
        self.seek_audio(self.current_audio_position + 10)

    def rewind(self):
        self.seek_audio(self.current_audio_position - 10)

    def check_audio_end(self):
        if not pygame.mixer.music.get_busy() and self.audio_playing:
            self.audio_playing = False
            self.current_audio_position = 0
            self.draw_menu()

    def draw_menu(self):
        if self.current_menu == "story":
            draw_story_menu(
                self.screen, self.font, self.story_list, self.current_story_index, self.chevron_left_img, self.chevron_right_img, self.battery_level, self.battery_img,
            )
        elif self.current_menu == "chapter":
            draw_chapter_menu(
                self.screen, self.font, self.story_list, self.current_story_index, self.current_chapter_index, self.chevron_left_img, self.chevron_right_img, self.battery_level, self.battery_img,
            )
        elif self.current_menu == "player":
            draw_player_menu(
                self.screen, self.font, self.audio_playing, self.current_audio_position, self.audio_total_length, self.play_icon_img, self.pause_icon_img, self.battery_level, self.battery_img,
            )
        elif self.current_menu == "konami":
            draw_konami_menu(
                self.screen, self.font, self.konami_menu_options, self.konami_menu_selected_index, self.timer_minutes, self.launch_at_startup, self.battery_level, self.battery_img,
            )
        elif self.current_menu == "error":
            draw_error_menu(self.screen, self.font)

    def run(self):
        clock = pygame.time.Clock()
        self.draw_menu()

        while self.is_running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.is_running = False
                elif e.type == pygame.KEYDOWN:
                    handle_keydown_event(e, self)
                elif e.type == pygame.KEYUP:
                    handle_keyup_event(e, self)

            current_time = pygame.time.get_ticks()

            if current_time - self.last_status_update_time >= 1000:
                self.battery_level = get_battery_level()
                self.last_status_update_time = current_time

            if current_time - self.last_activity_time >= 5000 and not self.dim_mode:
                set_brightness(0)
                self.dim_mode = True
            elif current_time - self.last_activity_time < 5000 and self.dim_mode:
                set_brightness(5)
                self.dim_mode = False

            if self.key_left_pressed and current_time - self.last_key_press_time >= self.key_press_delay:
                self.handle_key_press("left")
            if self.key_right_pressed and current_time - self.last_key_press_time >= self.key_press_delay:
                self.handle_key_press("right")

            self.update_audio_position()
            self.check_audio_end()
            check_timer_end(self, current_time)

            self.draw_menu()
            pygame.display.flip()
            clock.tick(10)

        pygame.quit()
        sys.exit(0)

    def handle_key_press(self, direction):
        self.last_key_press_time = pygame.time.get_ticks()
        if direction == "left":
            if self.current_menu == "story":
                self.current_story_index = (self.current_story_index - 1) % len(self.story_list)
            elif self.current_menu == "chapter":
                self.current_chapter_index = (self.current_chapter_index - 1) % len(self.story_list[self.current_story_index]["chapters"])
            elif self.current_menu == "player":
                self.rewind()
            elif self.current_menu == "konami" and self.konami_menu_selected_index == 0:
                self.timer_minutes = max(1, self.timer_minutes - 1)
        elif direction == "right":
            if self.current_menu == "story":
                self.current_story_index = (self.current_story_index + 1) % len(self.story_list)
            elif self.current_menu == "chapter":
                self.current_chapter_index = (self.current_chapter_index + 1) % len(self.story_list[self.current_story_index]["chapters"])
            elif self.current_menu == "player":
                self.fast_forward()
            elif self.current_menu == "konami" and self.konami_menu_selected_index == 0:
                self.timer_minutes += 1


if __name__ == "__main__":
    story_player = StoryPlayer()
    story_player.run()
