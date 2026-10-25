# 🍣 Sushida Auto Typer

**Python + Selenium + Tesseract OCRで動作する、寿司打の自動タイピングプログラム。**

An automatic typing bot for the Japanese typing game *Sushi-da*, powered by Python, Selenium, and Tesseract OCR.

## 🏆 Performance / 実行結果

**お手軽3,000円コース（普通）での実測結果**

| Metric | Result |
|---|---:|
| Sushi value / 獲得金額 | ¥21,120 |
| Profit / お得金額 | ¥18,120 |
| Correct keystrokes / 正しく打ったキー | 1,116 |
| Average typing speed / 平均タイプ速度 | 9.9 keys/sec |
| Misses / ミスタイプ | 14 |

*These results were obtained during one test run. Performance may vary.*

## ✨ Features / 主な機能

- 🍣 Automatic typing in Sushi-da / 寿司打の自動入力
- 🔍 OCR-based text recognition / 画面のローマ字をOCRで認識
- 📚 Dictionary-based error correction / 辞書による誤認識補正
- ⌨️ Automated keyboard input using Selenium / Seleniumによるキー入力
- ⚙️ Configurable typing speed / 入力速度の調整
- 📝 Debug screenshots for correction candidates / 補正候補の画像保存

## 🛠 Requirements / 動作環境

- Windows
- Python 3
- Google Chrome
- Tesseract OCR
- Internet connection for the game and initial dictionary download

### Install Python packages

```bash
py -m pip install selenium pytesseract pillow requests beautifulsoup4
```

### Install Tesseract OCR

Install Tesseract OCR separately.

The default Windows installation path expected by the script is:

```text
C:\Program Files\Tesseract-OCR\tesseract.exe
```

If Tesseract is installed elsewhere, update the path in `auto_v7.py`.

## 🚀 Usage / 使い方

**1. Download the project / プロジェクトをダウンロード**

Download the repository as a ZIP file and extract it.

**2. Open PowerShell in the extracted folder / フォルダ内でPowerShellを開く**

**3. Run the script / 実行**

```powershell
py auto_v7.py
```

Chrome will open automatically and the script will attempt to start the 3,000-yen course.

Chromeが自動で起動し、3,000円コースのプレイを開始します。

**4. Stop the script / 停止**

Press `Ctrl + C` in PowerShell.

V7 does not automatically detect the results screen and may continue running after the game finishes.

V7は結果画面を自動判定しないため、ゲーム終了後は手動で停止してください。

## ⚙️ Configuration / 設定

The following values can be changed in `auto_v7.py`:

```python
KEY_DELAY = 0.035
AFTER_WORD_DELAY = 0.08
USE_CORRECTION = True
```

| Setting | Description |
|---|---|
| `KEY_DELAY` | Delay between individual keystrokes |
| `AFTER_WORD_DELAY` | Delay after typing a word |
| `USE_CORRECTION` | Enable or disable dictionary correction |

The script uses a fixed OCR crop region. Recognition may fail if the browser layout or game display changes.

OCRの認識範囲は固定されているため、画面サイズや表示位置によっては正常に動作しない場合があります。

## 🧠 How It Works / 仕組み

1. Selenium opens the Sushi-da game.
2. The program captures screenshots of the game canvas.
3. Tesseract OCR recognizes the displayed Roman letters.
4. The dictionary attempts to correct certain OCR errors.
5. Selenium sends the recognized characters as keyboard input.
6. The process repeats until manually stopped.

## ⚠️ Disclaimer / 注意事項

This project is for programming experiments and educational purposes.

- Not affiliated with the creators of Sushi-da.
- Automated scores should not be submitted to public rankings.
- Use only where permitted by the game's terms and rules.
- Dictionary content from third-party sources remains subject to its original licensing and redistribution conditions.

本プロジェクトはプログラミング学習・実験を目的としています。寿司打の公式プロジェクトではありません。自動入力による記録をランキングに投稿しないでください。

## 📄 License

No license has been selected yet. Redistribution and modification permissions are not granted automatically.

## 👨‍💻 Author

Created by [mohmedhaathim-create](https://github.com/mohmedhaathim-create).

---

⭐ If you find this project interesting, consider starring the repository!
