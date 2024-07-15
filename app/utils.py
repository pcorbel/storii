import io
import math
import os
import re
import shutil
import sys

import pygame
from mutagen.id3 import APIC, ID3
from mutagen.mp3 import MP3

from config import *


def decode(text):
    try:
        return text.decode("utf-8")
    except Exception:
        return text


def format_time(seconds):
    mins = int(seconds) // 60
    secs = int(seconds) % 60
    return "{:02}:{:02}".format(mins, secs)


def load_image(path, size=None):
    try:
        img = pygame.image.load(path)
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except (pygame.error, IOError):
        img = pygame.image.load(DEFAULT_IMG_PATH)
        if size:
            img = pygame.transform.scale(img, size)
        return img


def render_text(surface, text, font, color, y, x=None):
    text_surface = font.render(decode(text), True, color)
    if x is None:
        x = (SCREEN_WIDTH - text_surface.get_width()) // 2
    surface.blit(text_surface, (x, y))


def extract_story_info(folder_name):
    artist_match = re.search(r"\[(.*?)\]", folder_name)
    artist = artist_match.group(1) if artist_match else ""
    title = folder_name.replace("[{}]".format(artist), "").strip() if artist else folder_name.strip()
    return artist, title


def format_chapter_title(title):
    title = re.sub(r"^(E\d{2} - |S\d{2}E\d{2} - )", "", title)
    return title.strip()


def get_chapter_info_from_id3(mp3_file):
    try:
        audio = MP3(mp3_file, ID3=ID3)
        title = audio.get("TIT2", None)
        track_number = audio.get("TRCK", None)
        album = audio.get("TALB", None)
        disc_number = audio.get("TPOS", None)
        if title:
            title = title.text[0]
        if track_number:
            track_number = track_number.text[0].split("/")[0]
            track_number = int(track_number)
        if album:
            album = album.text[0]
        if disc_number:
            disc_number = disc_number.text[0].split("/")[0]
            disc_number = int(disc_number)
        return format_chapter_title(title) if title else None, track_number, album, disc_number
    except Exception as e:
        return None, None, None, None


def get_chapter_cover_from_id3(mp3_file):
    try:
        audio = MP3(mp3_file, ID3=ID3)
        for tag in audio.tags.values():
            if isinstance(tag, APIC):
                cover_image = tag.data
                return pygame.image.load(io.BytesIO(cover_image))
        return None
    except Exception as e:
        return None


def get_audio_sampling_rate(path):
    try:
        audio = MP3(path)
        return audio.info.sample_rate
    except (pygame.error, IOError):
        return 44100


def process_story(folder_path):
    folder_name = os.path.basename(folder_path)
    artist, story_title = extract_story_info(folder_name)
    story_cover = os.path.join(folder_path, "cover.png")
    return {
        "title": story_title,
        "artist": artist,
        "cover": story_cover,
        "folder_path": folder_path,
        "chapters": None,
    }


def get_stories():
    if not os.path.exists(STORIIES_PATH):
        return []
    stories = [process_story(os.path.join(STORIIES_PATH, folder_name)) for folder_name in os.listdir(STORIIES_PATH) if os.path.isdir(os.path.join(STORIIES_PATH, folder_name))]
    return sorted(stories, key=lambda x: x["title"].lower())


def get_audio_length(path):
    try:
        audio = MP3(path)
        return audio.info.length
    except (pygame.error, IOError) as e:
        return 0


def get_battery_level():
    try:
        with open(BATTERY_PERC_PATH, "r") as f:
            return f.read().strip()
    except IOError:
        return "N/A"


def set_brightness(brightness):
    system_value = int(round(3.0 * math.exp(0.350656 * brightness)))
    try:
        with open(PWM_PATH, "w") as fp:
            fp.write("{}\n".format(system_value))
    except IOError:
        pass


def extract_cover_image_if_needed(chapter):
    cover_image = get_chapter_cover_from_id3(chapter["audio"])
    if cover_image:
        chapter["cover"] = cover_image
    else:
        chapter["cover"] = load_image(DEFAULT_IMG_PATH, COVER_SIZE)
    return chapter["cover"]


def load_chapters_for_story(story):
    if story["chapters"] is not None:
        return
    folder_path = story["folder_path"]
    chapters = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".mp3"):
            audio_file = os.path.join(folder_path, file_name)
            chapter_title, track_number, album, disc_number = get_chapter_info_from_id3(audio_file)
            if not chapter_title:
                chapter_title = file_name.replace(".mp3", "")
            chapters.append({"title": chapter_title, "audio": audio_file, "cover": None, "track_number": track_number, "album": album, "disc_number": disc_number})
    chapters.sort(key=lambda x: (x["disc_number"] if x["disc_number"] is not None else float("inf"), x["track_number"] if x["track_number"] is not None else float("inf"), x["title"]))
    story["chapters"] = chapters


def timer_end(story_player):
    if story_player.audio_playing:
        story_player.exit_after_audio = True
    else:
        pygame.quit()
        sys.exit(128)


def check_timer_end(story_player, current_time):
    if story_player.timer_start_time and story_player.current_menu != "konami":
        elapsed_time = (current_time - story_player.timer_start_time) / 1000
        if elapsed_time >= story_player.timer_duration:
            story_player.timer_start_time = None
            timer_end(story_player)


def set_launch_at_startup(value):
    source_path = os.path.join(SCRIPT_DIR, "launch-storii-startup.sh")
    if value:
        try:
            shutil.copyfile(source_path, STARTUP_PATH)
        except OSError:
            pass
    else:
        try:
            os.remove(STARTUP_PATH)
        except OSError:
            pass
