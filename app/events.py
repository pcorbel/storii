import pygame

from config import *
from ui import *


def handle_keydown_event(e, story_player):
    story_player.konami_code.append(e.key)
    if len(story_player.konami_code) > len(KONAMI_CODE):
        story_player.konami_code.pop(0)
    if story_player.konami_code == KONAMI_CODE:
        story_player.reset_to_initial_state()
        story_player.current_menu = "konami"

    story_player.last_activity_time = pygame.time.get_ticks()

    if story_player.current_menu == "story":
        handle_story_menu_keydown(e, story_player)
    elif story_player.current_menu == "chapter":
        handle_chapter_menu_keydown(e, story_player)
    elif story_player.current_menu == "player":
        handle_player_menu_keydown(e, story_player)
    elif story_player.current_menu == "konami":
        handle_konami_menu_keydown(e, story_player)


def handle_story_menu_keydown(e, story_player):
    if e.key == pygame.K_LEFT:
        story_player.key_left_pressed = True
    elif e.key == pygame.K_RIGHT:
        story_player.key_right_pressed = True
    elif e.key == pygame.K_SPACE:
        story_player.current_menu = "chapter"


def handle_chapter_menu_keydown(e, story_player):
    if e.key == pygame.K_LEFT:
        story_player.key_left_pressed = True
    elif e.key == pygame.K_RIGHT:
        story_player.key_right_pressed = True
    elif e.key == pygame.K_SPACE:
        story_player.current_menu = "player"
        story_player.start_audio()
    elif e.key == pygame.K_LCTRL:
        story_player.reset_audio()
        story_player.current_menu = "story"


def handle_player_menu_keydown(e, story_player):
    if e.key == pygame.K_SPACE:
        story_player.handle_player_controls()
    elif e.key == pygame.K_LEFT:
        story_player.key_left_pressed = True
    elif e.key == pygame.K_RIGHT:
        story_player.key_right_pressed = True
    elif e.key == pygame.K_LCTRL:
        story_player.reset_audio()
        story_player.current_menu = "chapter"


def handle_konami_menu_keydown(e, story_player):
    if e.key == pygame.K_UP:
        story_player.konami_menu_selected_index = (story_player.konami_menu_selected_index - 1) % len(story_player.konami_menu_options)
    elif e.key == pygame.K_DOWN:
        story_player.konami_menu_selected_index = (story_player.konami_menu_selected_index + 1) % len(story_player.konami_menu_options)
    elif e.key == pygame.K_LEFT:
        story_player.key_left_pressed = True
    elif e.key == pygame.K_RIGHT:
        story_player.key_right_pressed = True
    elif e.key == pygame.K_SPACE:
        if story_player.konami_menu_selected_index == 1:
            story_player.launch_at_startup = not story_player.launch_at_startup
            set_launch_at_startup(story_player.launch_at_startup)
        elif story_player.konami_menu_selected_index == 2:
            story_player.is_running = False
    elif e.key == pygame.K_LCTRL:
        story_player.timer_start_time = pygame.time.get_ticks()
        story_player.timer_duration = story_player.timer_minutes * 60
        story_player.current_menu = "story"


def handle_keyup_event(e, story_player):
    if e.key == pygame.K_LEFT:
        story_player.key_left_pressed = False
    elif e.key == pygame.K_RIGHT:
        story_player.key_right_pressed = False
