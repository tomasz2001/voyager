from PIL import Image, ImageDraw, ImageFont
import os
import platform
import subprocess

# ================== KONFIGURACJA ==================
INPUT_IMAGE   = "v_medium.png"
OUTPUT_IMAGE  = "v_medium_out.png"
FONT_PATH     = "font.ttf"
FONT_SIZE     = 27
LINE_SPACING  = 12
COLOR         = (0, 0, 0)

TEXT1_POS     = (190, 900)
TEXT1_WIDTH   = 1000
TEXT2_POS     = (1370, 300)
TEXT2_WIDTH   = 1000
# ==================================================

def _preprocess(text: str) -> str:
    """
    Normalizacja odstępów i akapitów.
    HARD-COMPRESS: usuwa wielokrotne spacje i traktuje [endend] jako większy odstęp.
    """
    text = text.replace("\r", " ").replace("\n", " ")
    text = " ".join(text.split())
    text = text.replace("[endend]", "\n\n\n")
    return text


def _wrap(text: str, font, max_width: int, draw) -> list[str]:
    """
    HARD-COMPRESS WRAPPER:
    - maksymalne ściskanie tekstu
    - agresywne łamanie słów
    - brak pustych przestrzeni
    - minimalna liczba linii
    """

    lines = []
    paragraphs = text.split("\n")

    for paragraph in paragraphs:
        paragraph = " ".join(paragraph.split())
        if not paragraph:
            lines.append("")
            continue

        words = paragraph.split()
        current = ""

        for word in words:
            while word:
                candidate = (current + " " if current else "") + word

                if draw.textlength(candidate, font=font) <= max_width:
                    current = candidate
                    word = ""
                    continue

                # Nie mieści się → dzielimy słowo
                if current == "":
                    split_pos = 1
                    for i in range(1, len(word) + 1):
                        if draw.textlength(word[:i] + "-", font=font) > max_width:
                            break
                        split_pos = i

                    lines.append(word[:split_pos] + "-")
                    word = word[split_pos:]
                    continue

                # Zatwierdź linię
                lines.append(current)
                current = ""

        if current:
            lines.append(current)

    return lines


def paint_text(tekst_lewy: str, tekst_prawy: str):
    img = Image.open(INPUT_IMAGE).convert("RGB")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    ascent, descent = font.getmetrics()
    line_height = ascent + descent + LINE_SPACING

    # lewy tekst
    lines1 = _wrap(_preprocess(tekst_lewy), font, TEXT1_WIDTH, draw)
    x, y = TEXT1_POS
    for line in lines1:
        draw.text((x, y), line, font=font, fill=COLOR)
        y += line_height

    # prawy tekst
    lines2 = _wrap(_preprocess(tekst_prawy), font, TEXT2_WIDTH, draw)
    x, y = TEXT2_POS
    for line in lines2:
        draw.text((x, y), line, font=font, fill=COLOR)
        y += line_height

    img.save(OUTPUT_IMAGE, "PNG")
    print(f"Gotowe! Zapisano: {OUTPUT_IMAGE}")


def np_print():
    """
    Drukowanie pliku OUTPUT_IMAGE:
    - Windows → os.startfile
    - Linux/macOS → lp
      automatycznie szuka domyślnej drukarki lub pierwszej fizycznej drukarki
    """
    if not os.path.exists(OUTPUT_IMAGE):
        print(f"Błąd: nie ma pliku {OUTPUT_IMAGE}")
        return

    system = platform.system()
    try:
        if system == "Windows":
            os.startfile(OUTPUT_IMAGE, "print")
        elif system in ("Darwin", "Linux"):
            # Sprawdź domyślną drukarkę
            result = subprocess.run(["lpstat", "-d"], capture_output=True, text=True)
            default_printer = None
            if "system default destination:" in result.stdout:
                default_printer = result.stdout.strip().split(":")[-1].strip()

            # Jeśli brak domyślnej drukarki, weź pierwszą fizyczną
            if not default_printer:
                result = subprocess.run(["lpstat", "-p"], capture_output=True, text=True)
                printers = [line.split()[1] for line in result.stdout.splitlines() if line.startswith("printer")]
                if printers:
                    default_printer = printers[0]

            if not default_printer:
                print("⚠️ Brak dostępnej drukarki")
                return

            subprocess.run(["lp", "-d", default_printer, "-o", "fit-to-page", OUTPUT_IMAGE], check=True)

        print(f"Wysłano {OUTPUT_IMAGE} do drukarki")
    except Exception as e:
        print(f"Nie udało się wydrukować: {e}")


def paper_test(text_add: str, text1: str, text2: str):
    """
    Sprawdza, czy nowy tekst zmieści się w kolumnie lewej lub prawej
    """
    MAX_LINES1 = 60
    MAX_LINES2 = 60

    img = Image.open(INPUT_IMAGE).convert("RGB")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    combined1 = text1 + ("[endend]" if text1 else "") + text_add
    combined2 = text2 + ("[endend]" if text2 else "") + text_add

    lines1 = _wrap(_preprocess(combined1), font, TEXT1_WIDTH, draw)
    lines2 = _wrap(_preprocess(combined2), font, TEXT2_WIDTH, draw)

    if len(lines1) <= MAX_LINES1:
        return "1_ok"
    elif len(lines2) <= MAX_LINES2:
        return "2_ok"
    else:
        return "no_ok"


if __name__ == "__main__":
    text1 = input("Lewy tekst: ")
    text2 = input("Prawy tekst: ")
    paint_text(text1, text2)
    np_print()
