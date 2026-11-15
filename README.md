<p align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f172a,100:38bdf8&height=180&section=header&text=Subtitle+Shift&fontSize=46&fontColor=ffffff&animation=fadeIn&fontAlignY=35" width="100%" alt="Subtitle Shift banner"/>
<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=20&pause=900&color=38bdf8&center=true&vCenter=true&width=760&lines=Fix+SRT+timing+offsets+and+validate+cue+order" alt="Typing title"/>
</p>
<p align="center">
<img src="https://img.shields.io/github/license/CyberLoop-dev/subtitle-shift?style=for-the-badge" alt="License"/>
<img src="https://img.shields.io/github/languages/top/CyberLoop-dev/subtitle-shift?style=for-the-badge" alt="Language"/>
<img src="https://img.shields.io/github/stars/CyberLoop-dev/subtitle-shift?style=for-the-badge" alt="Stars"/>
<img src="https://img.shields.io/github/last-commit/CyberLoop-dev/subtitle-shift?style=for-the-badge" alt="Last commit"/>
</p>
<p align="center"><img src="assets/overview.svg" width="640" alt="Subtitle Shift illustration"/></p>

## 🧭 Overview
Subtitle Shift is a dependency-free Python CLI for correcting subtitle timing drift. It validates cue ranges, applies positive or negative millisecond offsets, preserves subtitle text, and writes a separate output file.

## ✨ Features
- ⏱️ Shift every cue by a precise millisecond offset
- 🧪 Check timestamp syntax and cue ordering before editing
- 🧱 Preserve cue numbers and subtitle text
- 🛡️ Refuse to overwrite an existing output file
- 📄 Work with standard SubRip .srt files

## 🎬 Demo
~~~bash
python main.py check movie.srt
python main.py shift movie.srt --offset-ms 1250 --output movie-fixed.srt
~~~
Positive offsets move subtitles later; negative offsets move them earlier.

## 🚀 Quick Start
Requires Python 3.10+. No third-party packages are required.
~~~bash
python main.py check subtitles.srt
python main.py shift subtitles.srt --offset-ms -750 --output subtitles-fixed.srt
python -m unittest discover -s tests
~~~

## 🧰 Tech Stack
- 🐍 Python standard library
- 🕒 Regular expressions and datetime-style arithmetic
- 🧪 unittest

## 🗂️ Folder Structure
~~~text
subtitle-shift/
├── assets/overview.svg
├── tests/test_main.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
~~~

## 🗺️ Roadmap
- [ ] 🧩 Support WebVTT files
- [ ] 📊 Add a cue-duration summary
- [ ] 🧪 Add optional batch-folder processing

## 🤝 Contributing
Bug reports and focused pull requests are welcome. Include a reproducible example or a test when changing behavior.

## 📄 License
MIT — see [LICENSE](LICENSE).

<p align="center"><img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f172a,100:38bdf8&height=110&section=footer" width="100%" alt="Animated wave footer"/></p>