import pygame

from config import *
from utils import *


def draw_story_menu(
    screen, font, story_list, current_story_index, chevron_left_img, chevron_right_img, battery_level, battery_img,
):
    screen.fill(BLACK)
    story = story_list[current_story_index]
    story_cover_img = load_image(story["cover"], COVER_SIZE)
    cover_y = (SCREEN_HEIGHT - APP_BAR_HEIGHT - COVER_SIZE[1]) // 2 + APP_BAR_HEIGHT
    render_text(
        screen, story["title"], font, WHITE, (cover_y - FONT_SIZE - PADDING) // 2 + APP_BAR_HEIGHT,
    )
    if story_cover_img:
        screen.blit(
            story_cover_img, ((SCREEN_WIDTH - story_cover_img.get_width()) // 2, cover_y),
        )
    screen.blit(
        chevron_left_img, (PADDING, (SCREEN_HEIGHT - chevron_left_img.get_height()) // 2 + APP_BAR_HEIGHT,),
    )
    screen.blit(
        chevron_right_img, (SCREEN_WIDTH - chevron_right_img.get_width() - PADDING, (SCREEN_HEIGHT - chevron_right_img.get_height()) // 2 + APP_BAR_HEIGHT,),
    )
    draw_app_bar(screen, battery_level, battery_img)
    pygame.display.flip()


def draw_chapter_menu(
    screen, font, story_list, current_story_index, current_chapter_index, chevron_left_img, chevron_right_img, battery_level, battery_img,
):
    screen.fill(BLACK)
    story = story_list[current_story_index]
    load_chapters_for_story(story)
    chapters = story["chapters"]

    if not chapters:
        render_text(screen, "No chapters found", font, WHITE, SCREEN_HEIGHT // 2 - FONT_SIZE // 2 + APP_BAR_HEIGHT)
        pygame.display.flip()
        return

    if current_chapter_index < 0 or current_chapter_index >= len(chapters):
        current_chapter_index = 0

    chapter = chapters[current_chapter_index]
    chapter_cover_img = extract_cover_image_if_needed(chapter)
    chapter_cover_img = pygame.transform.scale(chapter_cover_img, COVER_SIZE)
    cover_y = (SCREEN_HEIGHT - APP_BAR_HEIGHT - COVER_SIZE[1]) // 2 + APP_BAR_HEIGHT
    render_text(
        screen, chapter["title"], font, WHITE, (cover_y - FONT_SIZE - PADDING) // 2 + APP_BAR_HEIGHT,
    )
    if chapter_cover_img:
        screen.blit(
            chapter_cover_img, ((SCREEN_WIDTH - chapter_cover_img.get_width()) // 2, cover_y),
        )
    chapter_info = "{} / {}".format(current_chapter_index + 1, len(chapters))
    render_text(screen, chapter_info, font, WHITE, cover_y + COVER_SIZE[1] + PADDING)
    screen.blit(
        chevron_left_img, (PADDING, (SCREEN_HEIGHT - chevron_left_img.get_height()) // 2 + APP_BAR_HEIGHT,),
    )
    screen.blit(
        chevron_right_img, (SCREEN_WIDTH - chevron_right_img.get_width() - PADDING, (SCREEN_HEIGHT - chevron_right_img.get_height()) // 2 + APP_BAR_HEIGHT,),
    )
    draw_app_bar(screen, battery_level, battery_img)
    pygame.display.flip()


def draw_player_menu(
    screen, font, audio_playing, current_audio_position, audio_total_length, play_icon_img, pause_icon_img, battery_level, battery_img,
):
    screen.fill(BLACK)
    icon_img = pause_icon_img if audio_playing else play_icon_img
    screen.blit(
        icon_img, ((SCREEN_WIDTH - ICON_SIZE[0]) // 2, (SCREEN_HEIGHT - ICON_SIZE[1]) // 2),
    )
    current_time_text = format_time(current_audio_position)
    total_time_text = format_time(audio_total_length)
    progress_ratio = current_audio_position / audio_total_length if audio_total_length > 0 else 0
    progress_bar_width = int((SCREEN_WIDTH - 2 * PROGRESS_BAR_PADDING) * progress_ratio)
    pygame.draw.rect(
        screen, WHITE, (PROGRESS_BAR_PADDING, PROGRESS_BAR_Y + APP_BAR_HEIGHT, SCREEN_WIDTH - 2 * PROGRESS_BAR_PADDING, PROGRESS_BAR_HEIGHT,), 2,
    )
    pygame.draw.rect(
        screen, WHITE, (PROGRESS_BAR_PADDING, PROGRESS_BAR_Y + APP_BAR_HEIGHT, progress_bar_width, PROGRESS_BAR_HEIGHT,),
    )
    render_text(
        screen, current_time_text, font, WHITE, PROGRESS_BAR_Y - FONT_SIZE - PADDING + APP_BAR_HEIGHT, PADDING,
    )
    render_text(
        screen, total_time_text, font, WHITE, PROGRESS_BAR_Y - FONT_SIZE - PADDING + APP_BAR_HEIGHT, SCREEN_WIDTH - PADDING - font.size(total_time_text)[0],
    )
    draw_app_bar(screen, battery_level, battery_img)
    pygame.display.flip()


def draw_konami_menu(
    screen, font, konami_menu_options, selected_index, timer_minutes, launch_at_startup, battery_level, battery_img,
):
    screen.fill(BLACK)
    menu_height = len(konami_menu_options) * 50
    start_y = (SCREEN_HEIGHT - menu_height) // 2
    for i, option in enumerate(konami_menu_options):
        color = WHITE if i == selected_index else pygame.Color("gray")
        if option == "Set Timer":
            text = "{} ({} min)".format(option, timer_minutes)
        elif option == "Launch at Startup":
            text = "{} [{}]".format(option, "X" if launch_at_startup else " ")
        elif option == "Quit":
            text = "Quit Storii"
        render_text(screen, text, font, color, y=start_y + i * 50)
    draw_app_bar(screen, battery_level, battery_img)
    pygame.display.flip()


def draw_error_menu(screen, font):
    screen.fill(BLACK)
    render_text(
        screen, "No stories found", font, WHITE, SCREEN_HEIGHT // 2 - FONT_SIZE // 2 + APP_BAR_HEIGHT,
    )
    pygame.display.flip()


def draw_app_bar(screen, battery_level, battery_img):
    font = pygame.font.Font(FONT_PATH, APP_BAR_HEIGHT)
    app_bar_rect = pygame.Rect(0, 0, SCREEN_WIDTH, APP_BAR_HEIGHT)
    pygame.draw.rect(screen, BLACK, app_bar_rect)
    battery_text = "{}%".format(battery_level)
    battery_text_width = font.size(battery_text)[0]
    render_text(
        screen, battery_text, font, WHITE, (APP_BAR_HEIGHT - FONT_SIZE) // 2, SCREEN_WIDTH - battery_text_width - APP_BAR_HEIGHT - 15,
    )
    screen.blit(
        battery_img, (SCREEN_WIDTH - APP_BAR_HEIGHT - 10, (APP_BAR_HEIGHT - APP_BAR_HEIGHT) // 2),
    )
