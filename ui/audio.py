# تشغيل الأصوات والتحكم بها
# Eldergrove - Fantasy Audio System
# Background ambience, sound effects, and audio controls.

from pathlib import Path

import pygame


# --------------------------------------------------
# Audio paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
SOUND_DIR = BASE_DIR / "assets" / "sounds"

SOUND_FILES = {
    "forest": "forest",
    "gate": "gate",
    "success": "success",
    "mystery": "mystery",
    "journal": "journal",
}

SUPPORTED_FORMATS = (".mp3", ".wav", ".ogg")


# --------------------------------------------------
# Audio settings
# --------------------------------------------------

SOUND_ENABLED = True

MUSIC_VOLUME = 0.25
EFFECT_VOLUME = 0.65

_audio_ready = False
_music_playing = False

_sound_cache = {}


# --------------------------------------------------
# Initialize audio
# --------------------------------------------------

def initialize_audio():
    """Initialize the audio mixer once."""

    global _audio_ready

    if _audio_ready:
        return True

    try:
        pygame.mixer.init(
            frequency=44100,
            size=-16,
            channels=2,
            buffer=1024,
        )

        pygame.mixer.set_num_channels(8)

        _audio_ready = True
        return True

    except pygame.error as error:
        print(f"Audio unavailable: {error}")
        return False


# --------------------------------------------------
# Find sound files
# --------------------------------------------------

def get_sound_path(sound_name):
    """Find a sound file using its name and extension."""

    filename = SOUND_FILES.get(sound_name)

    if filename is None:
        return None

    for extension in SUPPORTED_FORMATS:
        path = SOUND_DIR / f"{filename}{extension}"

        if path.is_file():
            return path

    return None


# --------------------------------------------------
# Background forest ambience
# --------------------------------------------------

def play_forest():
    """
    Play forest ambience continuously.

    Background music loops independently
    from the sound effects.
    """

    global _music_playing

    if not SOUND_ENABLED:
        return

    if not initialize_audio():
        return

    if _music_playing and pygame.mixer.music.get_busy():
        return

    path = get_sound_path("forest")

    if path is None:
        print("Forest audio file not found.")
        return

    try:
        pygame.mixer.music.load(str(path))

        pygame.mixer.music.set_volume(MUSIC_VOLUME)

        # -1 means infinite looping.
        pygame.mixer.music.play(loops=-1, fade_ms=1000)

        _music_playing = True

    except pygame.error as error:
        _music_playing = False
        print(f"Cannot play forest ambience: {error}")


# --------------------------------------------------
# Stop background ambience
# --------------------------------------------------

def stop_forest():
    """Stop the forest ambience."""

    global _music_playing

    if not _audio_ready:
        return

    pygame.mixer.music.stop()

    _music_playing = False


# --------------------------------------------------
# Sound effects
# --------------------------------------------------

def play_sound(sound_name):
    """
    Play a sound effect without interrupting
    the forest ambience.
    """

    if not SOUND_ENABLED:
        return

    if not initialize_audio():
        return

    # Forest ambience has its own music channel.
    if sound_name == "forest":
        play_forest()
        return

    path = get_sound_path(sound_name)

    if path is None:
        print(f"Sound file not found: {sound_name}")
        return

    try:
        if sound_name not in _sound_cache:
            _sound_cache[sound_name] = pygame.mixer.Sound(
                str(path)
            )

        sound = _sound_cache[sound_name]

        sound.set_volume(EFFECT_VOLUME)

        sound.play()

    except pygame.error as error:
        print(f"Cannot play sound '{sound_name}': {error}")


# --------------------------------------------------
# Sound enable / disable
# --------------------------------------------------

def toggle_sound():
    """Enable or mute all audio."""

    global SOUND_ENABLED

    SOUND_ENABLED = not SOUND_ENABLED

    if not initialize_audio():
        return SOUND_ENABLED

    if SOUND_ENABLED:
        # Resume ambience only if it was playing.
        if _music_playing:
            pygame.mixer.music.unpause()

    else:
        pygame.mixer.music.pause()
        pygame.mixer.stop()

    return SOUND_ENABLED


# --------------------------------------------------
# Audio status
# --------------------------------------------------

def is_sound_enabled():
    """Return whether sound is enabled."""

    return SOUND_ENABLED


# --------------------------------------------------
# Stop everything
# --------------------------------------------------

def stop_all_audio():
    """Stop background ambience and all effects."""

    stop_forest()

    if _audio_ready:
        pygame.mixer.stop()


# --------------------------------------------------
# Adjust volume
# --------------------------------------------------

def set_music_volume(volume):
    """Set background volume between 0.0 and 1.0."""

    global MUSIC_VOLUME

    MUSIC_VOLUME = max(0.0, min(1.0, float(volume)))

    if _audio_ready:
        pygame.mixer.music.set_volume(MUSIC_VOLUME)


def set_effect_volume(volume):
    """Set effects volume between 0.0 and 1.0."""

    global EFFECT_VOLUME

    EFFECT_VOLUME = max(0.0, min(1.0, float(volume)))

    for sound in _sound_cache.values():
        sound.set_volume(EFFECT_VOLUME)