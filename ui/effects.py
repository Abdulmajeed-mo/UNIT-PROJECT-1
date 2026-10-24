# ألوان الغابة والمؤثرات النصية

import time

from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.text import Text
from rich.theme import Theme
from game.localization import Localization

# Fantasy Forest color palette
FOREST_GREEN = "#2F5249"
ANTIQUE_GOLD = "#C5A46D"
SOFT_GREEN = "#A3B18A"
WOOD_BROWN = "#987554"
MIST_GRAY = "#9AA5A0"
DANGER_RED = "#C76D6D"


FOREST_THEME = Theme({
    "forest": f"bold {FOREST_GREEN}",
    "gold": f"bold {ANTIQUE_GOLD}",
    "wood": WOOD_BROWN,
    "mystery": f"italic {SOFT_GREEN}",
    "danger": DANGER_RED,
    "success": SOFT_GREEN,
    "muted": MIST_GRAY,
})

console = Console(theme=FOREST_THEME)


def show_panel(title, description="", style="forest"):
    """Display a Fantasy Forest panel."""

    content = description if description else title

    console.print(
        Panel(
            Text(str(content)),
            title=str(title),
            border_style=style,
            padding=(1, 2),
            expand=False,
        )
    )


def show_success(message):
    """Display a success message."""

    console.print(
        Text(f"✨ {message}", style="success")
    )


def show_error(message):
    """Display an error message."""

    console.print(
        Text(f"✖ {message}", style="danger")
    )


def show_separator():
    """Display a forest-themed separator."""

    console.print(
        Rule(style=WOOD_BROWN)
    )




def show_forest_entry(language="ar"):
    """Play an atmospheric animation when entering the forest."""

    message = (
        "🌲 تستيقظ الغابة القديمة..."
        if language == "ar"
        else "🌲 The ancient forest is awakening..."
    )

    with console.status(
        Text(message, style=SOFT_GREEN),
        spinner="dots",
        spinner_style=ANTIQUE_GOLD,
    ):
        time.sleep(1.5)

    console.print(
        Rule("✦ ELDERGROVE ✦", style=FOREST_GREEN)
    )




def show_magic_loading(language="ar"):
    """Display a magical spinner before a puzzle."""

    message = (
        "🔮 تتوهج الرموز السحرية..."
        if language == "ar"
        else "🔮 Ancient runes are glowing..."
    )

    with console.status(
        Text(message, style=ANTIQUE_GOLD),
        spinner="moon",
        spinner_style=SOFT_GREEN,
    ):
        time.sleep(1.2)




def show_secret_discovery(language="ar", points=50):
    """Celebrate finding a hidden secret with Arabic support."""

    loc = Localization(language)

    message = (
        "لقد اكتشفت أحد أسرار الغابة!"
        if language == "ar"
        else "You discovered a forest secret!"
    )

    points_message = (
        f"+{points} نقطة للأسرار"
        if language == "ar"
        else f"+{points} Secret Points"
    )

    formatted_message = loc.format_arabic(message)
    formatted_points = loc.format_arabic(points_message)

    content = Text(justify="center")
    content.append("✨ ")
    content.append(formatted_message)
    content.append("\n\n")
    content.append("✦ ")
    content.append(formatted_points)
    content.append(" ✦")

    console.print()

    console.print(
        Panel(
            content,
            title="🌿 ✦ SECRET DISCOVERED ✦ 🌿",
            border_style=ANTIQUE_GOLD,
            padding=(1, 2),
            expand=False,
        )
    )




def type_narration(
    text,
    delay=0.06,
    style=SOFT_GREEN,
    formatter=None,
):
    """
    Reveal narration word by word.

    formatter can be loc.format_arabic when
    displaying Arabic narration.
    """

    words = str(text).split()

    if not words:
        console.print()
        return

    for index in range(1, len(words) + 1):
        partial_text = " ".join(words[:index])

        if formatter is not None:
            partial_text = formatter(partial_text)

        console.print(
            Text(partial_text, style=style),
            end="\r",
        )

        time.sleep(delay)

    console.print(
        Text(
            formatter(str(text))
            if formatter is not None
            else str(text),
            style=style,
        )
    )


#

def show_final_fate(language="ar"):
    """Play an atmospheric effect before the final ending."""

    message = (
        "🪄 الغابة تحدد مصيرك..."
        if language == "ar"
        else "🪄 The forest is deciding your fate..."
    )

    with console.status(
        Text(message, style=ANTIQUE_GOLD),
        spinner="earth",
        spinner_style=SOFT_GREEN,
    ):
        time.sleep(2)

    console.print()
    console.print(
        Rule(
            "✦ THE FOREST REMEMBERS ✦",
            style=ANTIQUE_GOLD,
        )
    )