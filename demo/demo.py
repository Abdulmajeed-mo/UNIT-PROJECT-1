import time

import questionary
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

from game.localization import Localization
from ui.audio import play_intro, play_forest, play_sound, stop_all_audio
from ui.effects import (
    console,
    show_forest_entry,
    show_magic_loading,
    show_secret_discovery,
    show_final_fate,
)


GREEN = "#2F5249"
GOLD = "#C5A46D"
SOFT_GREEN = "#A3B18A"

WORD_DELAY = 0.30
SCENE_DELAY = 1

loc = Localization("ar")

menu_style = questionary.Style([
    ("question", "fg:#C5A46D bold"),
    ("pointer", "fg:#C5A46D bold"),
    ("highlighted", "fg:#A3B18A bold"),
    ("selected", "fg:#2F5249"),
])


def ar(text):
    return loc.format_arabic(str(text))


def slow_text(text, color=SOFT_GREEN):
    words = str(text).split()

    if not words:
        return

    console.print()

    with Live(
        Text("", style=color),
        console=console,
        refresh_per_second=20,
        transient=False,
    ) as live:
        for index in range(1, len(words) + 1):
            current_text = " ".join(words[:index])

            live.update(
                Text(ar(current_text), style=color),
                refresh=True,
            )

            time.sleep(WORD_DELAY)

    console.print()
    time.sleep(SCENE_DELAY)


def pause(message="اضغط Enter للمتابعة..."):
    input(f"\n{ar(message)}")


def show_scene(title, description):
    console.print()

    console.print(
        Panel(
            Text(ar(title), style=GOLD, justify="center"),
            title="🌲 ✦ ELDERGROVE ✦ 🌲",
            border_style=GREEN,
            expand=False,
        )
    )

    time.sleep(0.6)
    slow_text(description)


def choose(question, options):
    choices = [
        questionary.Choice(
            title=ar(label),
            value=value,
        )
        for label, value in options
    ]

    return questionary.select(
        ar(question),
        choices=choices,
        pointer="❯",
        style=menu_style,
        use_shortcuts=False,
    ).ask()


def show_journal(evidence, solved_puzzles):
    play_sound("journal")

    console.print(
        Panel(
            Text(
                "📜 EXPLORER JOURNAL",
                justify="center",
                style=GOLD,
            ),
            border_style=GREEN,
            expand=False,
        )
    )

    slow_text("هذه الأدلة التي جمعتها خلال رحلتك.")

    for index, item in enumerate(evidence, start=1):
        console.print(
            Text(f"{index}. {ar(item)}", style=SOFT_GREEN)
        )
        time.sleep(0.5)

    for puzzle in solved_puzzles:
        console.print(
            Text(f"🔮 {ar(puzzle)}", style=GOLD)
        )
        time.sleep(0.5)


def show_demo_score(score, start_time):
    play_sound("success")

    elapsed = int(time.monotonic() - start_time)
    minutes, seconds = divmod(elapsed, 60)

    content = Text(justify="center")
    content.append(f"⭐ SCORE: {score}\n", style=GOLD)
    content.append(
        f"⏳ TIME: {minutes:02d}:{seconds:02d}",
        style=SOFT_GREEN,
    )

    console.print(
        Panel(
            content,
            title="🏆 DEMO PROGRESS",
            border_style=GOLD,
            padding=(1, 2),
            expand=False,
        )
    )


def solve_demo_puzzle():
    play_sound("mystery")
    show_magic_loading("ar")

    show_scene(
        "اللغز الأول",
        "تظهر رموز سحرية على لوح حجري قديم.",
    )

    slow_text(
        "لدي مفاتيح كثيرة، لكنني لا أفتح أي قفل. فمن أنا؟",
        GOLD,
    )

    while True:
        answer = choose(
            "اختر الإجابة الصحيحة:",
            [
                ("الباب", 1),
                ("لوحة المفاتيح", 2),
                ("الصندوق", 3),
                ("المفتاح الذهبي", 4),
            ],
        )

        if answer is None:
            return False

        if answer == 2:
            play_sound("success")
            slow_text(
                "إجابة صحيحة! تتوهج الرموز السحرية، "
                "وينفتح الممر أمامك.",
                GOLD,
            )
            return True

        slow_text(
            "إجابة خاطئة! تلميح: أستخدم للكتابة.",
            GOLD,
        )


def run_demo():
    start_time = time.monotonic()
    evidence = []
    solved_puzzles = []
    score = 0

    try:
        play_intro()

        console.print(
            Panel(
                Text(
                    "🌲 ELDERGROVE 🌲\n"
                    "THE FORGOTTEN FOREST\n\n"
                    "✦ PRESENTATION DEMO ✦",
                    justify="center",
                    style=GOLD,
                ),
                border_style=GREEN,
                padding=(1, 3),
                expand=False,
            )
        )

        while True:
            name = input(
                f"\n{ar('أدخل اسم المستكشف:')} "
            ).strip()

            if name:
                break

            slow_text("يرجى إدخال اسم المستكشف.")

        slow_text(
            f"مرحبًا بك يا {name} في غابة إلدرغروف."
        )

        pause("اضغط Enter لدخول الغابة...")

        play_forest()
        show_forest_entry("ar")

        show_scene(
            "البوابة الحجرية القديمة",
            "تقف أمام بوابة حجرية عتيقة، "
            "تغطي سطحها نقوش غامضة لم ترَ مثلها من قبل.",
        )

        play_sound("gate")

        slow_text("وفجأة، تسمع همسات خافتة من خلف البوابة...")

        slow_text(
                "الغابة تتذكر كل من يعبر بوابتها.",
                GOLD,
            )

        decision = choose(
                "كيف ستتصرف أمام البوابة؟",
                [
                    ("أنصت إلى الهمسات الغامضة", "listen"),
                    ("أتفحص النقوش الحجرية", "symbols"),
                    ("أدفع البوابة وأواصل طريقي", "push"),
                ],
            )

        if decision is None:
            return

        score += 40

        if decision == "listen":
            memory = "أنصت إلى همسات الغابة"

            slow_text(
                "تكشف لك الهمسات أن الغابة تختبر كل من يدخلها."
            )

            evidence.append(
                "الغابة تتذكر اختيارات المستكشف."
            )

        elif decision == "symbols":
            memory = "بحث عن الرموز القديمة"

            slow_text(
                "تكتشف رمزًا قديمًا يشير إلى ممر مخفي."
            )

            evidence.append(
                "الرموز القديمة تقود إلى أسرار الغابة."
            )

        else:
            memory = "دفع البوابة دون تردد"

            slow_text(
                "تنفتح البوابة بصوت مريب، "
                "وتشعر أن هناك من يراقبك."
            )

            evidence.append(
                "هناك قوة غامضة تراقب المستكشفين."
            )

        pause()

        show_scene(
            "الممر الغامض",
            "تتقدم داخل الغابة، لكن لوحًا حجريًا "
            "قديمًا يعترض طريقك.",
        )

        slow_text(
            "لن تتمكن من المتابعة حتى تحل اللغز المكتوب عليه."
        )

        pause("اضغط Enter لبدء اللغز...")

        if not solve_demo_puzzle():
            return

        score += 100

        solved_puzzles.append(
            "اللغز الأول: لوحة المفاتيح"
        )

        evidence.append(
            "حل الألغاز يكشف الطرق المخفية."
        )

        pause()

        show_scene(
            "السر المخفي",
            "بعد حل اللغز، تبدأ جذور شجرة قديمة "
            "بالتحرك ببطء، لتكشف مكانًا مخفيًا.",
        )

        score += 50

        show_secret_discovery(
            language="ar",
            points=50,
        )

        pause()

        slow_text(
            "خلال رحلتك، جمعت أدلة "
            "تساعدك على فهم أسرار الغابة."
        )

        action = choose(
            "ماذا تريد أن تفعل؟",
            [("فتح دفتر المستكشف", "journal")],
        )

        if action is None:
            return

        show_journal(evidence, solved_puzzles)

        pause("اضغط Enter لعرض نقاطك...")
        show_demo_score(score, start_time)

        pause()

        show_scene(
            "الممر الأخير",
            "تصل إلى قوس حجري قديم، "
            "وهناك تتوقف الرياح فجأة...",
        )

        slow_text(
            "الغابة الآن تتذكر رحلتك كاملة.",
            GOLD,
        )

        pause("اضغط Enter لاكتشاف مصيرك...")

        show_final_fate("ar")

        show_scene(
            "ذاكرة الغابة",
            f"تتذكر الغابة أنك {memory}. "
            "وتبدأ الأشجار بالهمس من جديد...",
        )

        slow_text(
            "لقد جمعت الأدلة، وحللت اللغز، "
            "واكتشفت أحد أسرار إلدرغروف."
        )

        show_scene(
            "النهاية: طريق النجاة",
            "تنفتح البوابة الأخيرة أمامك، "
            "وتسمح لك الغابة بالخروج. "
            "لكنها لن تنسى أثر رحلتك.",
        )

        console.print(
            Panel(
                Text(
                    f"EXPLORER: {ar(name)}\n"
                    f"DEMO SCORE: {score}\n\n"
                    "THE FOREST REMEMBERS.",
                    justify="center",
                    style=GOLD,
                ),
                title="🌲 ✦ THE END ✦ 🌲",
                border_style=GREEN,
                padding=(1, 2),
                expand=False,
            )
        )

    finally:
        stop_all_audio()
        play_intro()


if __name__ == "__main__":
    run_demo()

    input("\nPress Enter to exit...")
    stop_all_audio()