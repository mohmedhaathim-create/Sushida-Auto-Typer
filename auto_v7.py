
import re
import time
from io import BytesIO
from pathlib import Path

import requests
from bs4 import BeautifulSoup
import pytesseract
from PIL import Image, ImageOps, ImageEnhance

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


# ==========================================
# 寿司打 AUTO V7
# 15,320円版 + Python時間制限なし
# ==========================================

GAME_URL = "https://sushida.net/play.html"
WORDS_URL = "https://yamatnt.com/sushida-words/"

BASE = Path(__file__).resolve().parent
WORDS_FILE = BASE / "words.txt"
DEBUG_DIR = BASE / "debug_v7"
DEBUG_DIR.mkdir(exist_ok=True)

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

OCR_BOX = (185, 225, 315, 260)

KEY_DELAY = 0.035
AFTER_WORD_DELAY = 0.08

# 辞書補正ON
USE_CORRECTION = True

# Python側の90秒制限は廃止
# 停止するときは Ctrl+C


def normalize(text):
    text = text.lower().strip()

    for symbol in ("ー", "—", "–", "−"):
        text = text.replace(symbol, "-")

    return re.sub(r"[^a-z-]", "", text)


def download_words():
    print("単語辞書を取得中...")

    response = requests.get(
        WORDS_URL,
        timeout=20,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    words = set()
    in_easy_course = False

    for element in soup.find_all(["h2", "h3", "table"]):
        if element.name in ("h2", "h3"):
            heading = element.get_text(" ", strip=True)

            if "お手軽コースで出題されるワード一覧" in heading:
                in_easy_course = True

            elif (
                in_easy_course
                and "お勧めコースで出題されるワード一覧" in heading
            ):
                break

        elif element.name == "table" and in_easy_course:
            for row in element.find_all("tr"):
                cells = row.find_all("td")

                if len(cells) < 3:
                    continue

                word = normalize(
                    cells[2].get_text(" ", strip=True)
                )

                if len(word) >= 2:
                    words.add(word)

    if not words:
        raise RuntimeError(
            "単語一覧を抽出できませんでした"
        )

    WORDS_FILE.write_text(
        "\n".join(sorted(words)) + "\n",
        encoding="utf-8"
    )

    print(f"辞書保存完了：{len(words)}語")
    return words


def load_words():
    if WORDS_FILE.exists():
        words = {
            normalize(line)
            for line in WORDS_FILE.read_text(
                encoding="utf-8"
            ).splitlines()
        }

        words.discard("")

        if words:
            print(f"辞書読み込み：{len(words)}語")
            return words

    try:
        return download_words()
    except Exception as e:
        print("辞書取得エラー:", e)
        print("OCRのみで続行します")
        return set()


def capture(canvas):
    return Image.open(
        BytesIO(canvas.screenshot_as_png)
    ).convert("RGB")


def read_text(image):
    crop = image.crop(OCR_BOX).resize((780, 210))
    crop = ImageOps.grayscale(crop)
    crop = ImageEnhance.Contrast(crop).enhance(3)

    result = pytesseract.image_to_string(
        crop,
        config=(
            "--psm 7 "
            "-c tessedit_char_whitelist="
            "abcdefghijklmnopqrstuvwxyz-"
        )
    )

    return normalize(result)


def edit_distance_one(a, b):
    if abs(len(a) - len(b)) > 1 or a == b:
        return False

    i = 0
    j = 0
    edits = 0

    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            i += 1
            j += 1
        else:
            edits += 1

            if edits > 1:
                return False

            if len(a) > len(b):
                i += 1
            elif len(b) > len(a):
                j += 1
            else:
                i += 1
                j += 1

    edits += (len(a) - i) + (len(b) - j)
    return edits == 1


def correct_word(text, words):
    if not words or not text or text in words:
        return text, False

    if len(text) < 4:
        return text, False

    candidates = [
        word for word in words
        if edit_distance_one(text, word)
    ]

    if len(candidates) == 1:
        return candidates[0], True

    return text, False


words = load_words()

print("=" * 45)
print("寿司打 AUTO V7")
print("入力間隔:", KEY_DELAY)
print("単語後待機:", AFTER_WORD_DELAY)
print("辞書補正:", USE_CORRECTION)
print("辞書登録数:", len(words))
print("Python時間制限: なし")
print("=" * 45)

driver = webdriver.Chrome()

try:
    driver.set_window_size(1000, 900)
    driver.get(GAME_URL)

    canvas = WebDriverWait(driver, 30).until(
        lambda d: d.find_element(By.TAG_NAME, "canvas")
    )

    time.sleep(8)

    ActionChains(driver).move_to_element_with_offset(
        canvas, 0, 40
    ).click().perform()

    print("スタート画面を突破！")
    time.sleep(3)

    ActionChains(driver).move_to_element_with_offset(
        canvas, 0, -30
    ).click().perform()

    print("3,000円コース選択！")
    time.sleep(3)

    ActionChains(driver).send_keys(
        Keys.SPACE
    ).perform()

    print("ゲーム開始！")
    time.sleep(2)

    last_text = ""
    debug_number = 0

    # 時間制限なし
    while True:
        image = capture(canvas)
        raw_text = read_text(image)

        if not raw_text:
            time.sleep(0.1)
            continue

        if raw_text == last_text:
            time.sleep(0.1)
            continue

        corrected, changed = correct_word(
            raw_text, words
        )

        if changed:
            print(
                f"辞書補正: {raw_text} -> {corrected}"
            )

            debug_number += 1
            image.save(
                DEBUG_DIR /
                f"candidate_{debug_number:04d}.png"
            )

        target = (
            corrected
            if changed and USE_CORRECTION
            else raw_text
        )

        print("認識:", raw_text)
        print("入力:", target)

        for char in target:
            ActionChains(driver).send_keys(
                char
            ).perform()
            time.sleep(KEY_DELAY)

        last_text = raw_text
        time.sleep(AFTER_WORD_DELAY)

except KeyboardInterrupt:
    print("手動停止しました")

except Exception as e:
    print("エラー:", repr(e))

finally:
    print("辞書:", WORDS_FILE)
    print("確認画像:", DEBUG_DIR)
    input("Enterで終了")
    driver.quit()
