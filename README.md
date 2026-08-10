# mpv-Subtitle-Definition

An offline [mpv-player](https://github.com/mpv-player/mpv) extension for language learners.

While watching a video with subtitles, press `TAB` or `ENTER` and the script:

1. Reads the subtitle currently shown by mpv.
2. Detects words that are not in your known-word lists.
3. Looks them up locally using **WordNet via NLTK**.
4. Displays short English definitions and example sentences directly on mpv's OSD.

No OpenAI API key is required. No internet connection is required after installation.

## Features

- **Fully offline**
- **Free to use**
- **No API key**
- **Instant subtitle vocabulary lookup**
- **Automatic lemmatization**
  - `evacuated` → `evacuate`
  - `premises` → `premise`
- **Known-word filtering**
- **English dictionary definitions**
- **Example sentences when available**
- **Works directly inside mpv**
- **Customizable key bindings and word lists**
