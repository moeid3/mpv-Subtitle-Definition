# mpv-Subtitle-Definition

An offline [mpv](https://github.com/mpv-player/mpv) extension for language learners.

While watching a video with English subtitles, press `TAB` or `ENTER` to instantly look up unfamiliar words from the currently displayed subtitle.

The extension uses **NLTK + WordNet locally**, so there is:

- No OpenAI API
- No API key
- No subscription
- No network request during normal use

After the initial installation and WordNet download, the extension works completely offline.

## Features

- **Fully offline after installation**
- **Free to use**
- **No API key required**
- **Instant subtitle vocabulary lookup**
- **Automatic word normalization and lemmatization**
  - `evacuated` → `evacuate`
  - `running` → `run`
- **Preserves useful surface forms**
  - `premises` can be looked up as `premises` instead of blindly reducing it to `premise`
- **Part-of-speech-aware WordNet lookup**
- **Fallback dictionary lookup when POS detection fails**
- **Known-word filtering**
- **English dictionary definitions**
- **Example sentences when WordNet provides them**
- **Definitions displayed directly through mpv's OSD**
- **Customizable known-word lists**
- **No browser or external dictionary window required**

## How it works

Suppose the current subtitle is:

~~~text
We need to evacuate the premises immediately.
~~~

Press `TAB` or `ENTER`.

The extension then:

1. Reads the subtitle currently displayed by mpv.
2. Splits the subtitle into individual words.
3. Normalizes and lemmatizes the words for known-word detection.
4. Compares them against the files inside `word-lists/`.
5. Removes words that are already considered known.
6. Detects the likely part of speech of each remaining word.
7. Tries to find the most appropriate WordNet entry using the original word form.
8. Falls back to the lemmatized form when necessary.
9. If POS-restricted lookup fails, performs a broader WordNet lookup.
10. Displays the resulting definitions directly on mpv's OSD.

For example:

~~~text
evacuate
  move out of an unsafe location into safety
  Example: After the earthquake, residents were evacuated

premises
  land and the buildings on it
  Example: bread is baked on the premises
~~~

Playback is automatically paused while the definitions are displayed.

Press `SPACE` to clear the definition from the OSD and toggle playback.

If every word in the subtitle is already present in your known-word lists, mpv displays:

~~~text
You know all these words!
~~~

and playback automatically resumes.

## Requirements

You need:

- [mpv](https://github.com/mpv-player/mpv)
- Python 3
- Python `venv` support
- Git
- An English subtitle track

The current installation layout is designed for **macOS and Linux**.

Windows support is not currently included because the Lua integration expects a Unix-style Python virtual environment path.

## Installation

### 1. Make sure mpv's scripts directory exists

~~~bash
mkdir -p ~/.config/mpv/scripts
cd ~/.config/mpv/scripts
~~~

### 2. Clone the repository

~~~bash
git clone https://github.com/moeid3/mpv-Subtitle-Definition.git
cd mpv-Subtitle-Definition
~~~

Your repository will be located at:

~~~text
~/.config/mpv/scripts/mpv-Subtitle-Definition/
~~~

### 3. Create a Python virtual environment

From inside the repository:

~~~bash
python3 -m venv .venv
~~~

Activate it:

~~~bash
source .venv/bin/activate
~~~

### 4. Install the Python dependencies

~~~bash
pip install -r requirements.txt
~~~

The Python dependency is currently:

~~~text
nltk
~~~

### 5. Download the required NLTK data

Run:

~~~bash
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('averaged_perceptron_tagger_eng'); nltk.download('wordnet'); nltk.download('omw-1.4')"
~~~

These resources are downloaded only during installation.

Normal dictionary lookups are local afterward.

### 6. Make the Lua script available to mpv

mpv loads scripts directly from:

~~~text
~/.config/mpv/scripts/
~~~

Create a symbolic link from the repository's Lua script into that directory:

~~~bash
ln -sf "$HOME/.config/mpv/scripts/mpv-Subtitle-Definition/mpv-Subtitle-Definition.lua" \
"$HOME/.config/mpv/scripts/mpv-Subtitle-Definition.lua"
~~~

The resulting layout should look approximately like this:

~~~text
~/.config/mpv/scripts/
├── mpv-Subtitle-Definition.lua
└── mpv-Subtitle-Definition/
    ├── mpv-Subtitle-Definition.lua
    ├── script.py
    ├── requirements.txt
    ├── word-lists/
    └── .venv/
~~~

Using a symbolic link means future Git updates to the Lua script are automatically reflected in mpv.

### 7. Test the Python backend

While still inside:

~~~text
~/.config/mpv/scripts/mpv-Subtitle-Definition/
~~~

run:

~~~bash
.venv/bin/python3 script.py "We need to evacuate the premises immediately."
~~~

You should receive dictionary output similar to:

~~~text
evacuate
  move out of an unsafe location into safety

premises
  land and the buildings on it
  Example: bread is baked on the premises
~~~

The exact WordNet example text may vary depending on the selected dictionary entry.

### 8. Start mpv

You do **not** need to activate the Python virtual environment every time you use the extension.

The Lua script calls:

~~~text
mpv-Subtitle-Definition/.venv/bin/python3
~~~

directly.

Start mpv normally:

~~~bash
mpv video.mkv
~~~

Select an English subtitle track and use the extension.

## Usage

### Look up the current subtitle

Press:

~~~text
TAB
~~~

or:

~~~text
ENTER
~~~

The video pauses, the subtitle is processed, and definitions for unfamiliar words appear on the OSD.

### Close the definitions

Press:

~~~text
SPACE
~~~

This clears the definition OSD and toggles playback.

### No subtitle currently displayed

If you trigger the extension while no subtitle is visible, mpv displays:

~~~text
No subtitle currently displayed.
~~~

## Known-word filtering

The extension does not need to define every word you already understand.

Known words are stored in text files inside:

~~~text
word-lists/
~~~

The extension reads every `.txt` file in this directory.

Each known word should appear on its own line.

Example:

~~~text
the
a
this
that
have
need
immediately
~~~

If a word is present in one of these files, it will normally be excluded from the definition results.

This allows you to progressively customize the extension around your own vocabulary level.

The repository includes several lists for different categories of words.

You can also create your own `.txt` file inside `word-lists/`.

For example:

~~~text
word-lists/my-known-words.txt
~~~

with:

~~~text
evacuate
building
resident
earthquake
~~~

No code changes are required.

## Limitations

This project intentionally uses an offline dictionary rather than an LLM.

That makes it private, fast, free, and deterministic, but there are tradeoffs.

### Slang and modern expressions

WordNet is primarily a traditional lexical database.

Some:

- modern slang
- internet language
- proper nouns
- names
- fictional terminology
- highly specialized vocabulary
- multi-word expressions

may not be available.


## Customizing key bindings

The default bindings are:

| Key | Action |
| --- | --- |
| `TAB` | Look up current subtitle |
| `ENTER` | Look up current subtitle |
| `SPACE` | Clear definitions and toggle playback |

They are defined inside:

~~~text
mpv-Subtitle-Definition.lua
~~~

For example:

~~~lua
mp.add_key_binding("TAB", "fetch_subtitle2", function()
    mp.set_property_bool("pause", true)
    mp.osd_message("Processing...", 999)
    send_current_subtitle()
end)
~~~

You can change `"TAB"` to another mpv-compatible key if desired.


## Uninstalling

Remove the mpv Lua link:

~~~bash
rm ~/.config/mpv/scripts/mpv-Subtitle-Definition.lua
~~~

Then remove the repository:

~~~bash
rm -rf ~/.config/mpv/scripts/mpv-Subtitle-Definition
~~~

The NLTK data downloaded into your user account is separate and can be kept if other Python projects use NLTK.

## Troubleshooting

### mpv shows `Processing...` forever or no definition appears

First test the backend directly:

~~~bash
cd ~/.config/mpv/scripts/mpv-Subtitle-Definition
.venv/bin/python3 script.py "We need to evacuate the premises immediately."
~~~

If this fails, the problem is with the Python environment or NLTK installation rather than mpv.

### `Resource ... not found`

If NLTK reports a missing resource, reactivate the virtual environment:

~~~bash
cd ~/.config/mpv/scripts/mpv-Subtitle-Definition
source .venv/bin/activate
~~~

Then download the required resources again:

~~~bash
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('averaged_perceptron_tagger_eng'); nltk.download('wordnet'); nltk.download('omw-1.4')"
~~~

### `No subtitle currently displayed`

The extension only processes the subtitle currently visible on screen.

Wait until a subtitle appears and press `TAB` or `ENTER` again.

### All words are skipped

Check the files inside:

~~~text
word-lists/
~~~

A word found in those files is treated as already known.

### mpv does not react to `TAB` or `ENTER`

Verify that the Lua script exists at:

~~~text
~/.config/mpv/scripts/mpv-Subtitle-Definition.lua
~~~

You can check with:

~~~bash
ls -l ~/.config/mpv/scripts/mpv-Subtitle-Definition.lua
~~~

Also make sure the repository exists at:

~~~text
~/.config/mpv/scripts/mpv-Subtitle-Definition/
~~~


## Credits

This project is a fork of the original [`tripasect/mpv-Subtitle-Definition`](https://github.com/tripasect/mpv-Subtitle-Definition).

The original project used the OpenAI API to generate vocabulary definitions.

This fork replaces that dependency with a fully local **NLTK + WordNet** implementation so the core vocabulary lookup can run for free and offline.

Dictionary data is provided by [WordNet](https://wordnet.princeton.edu/) and accessed through [NLTK](https://www.nltk.org/).

## Contributing

Issues, bug reports, suggestions, and pull requests are welcome.

Repository:

https://github.com/moeid3/mpv-Subtitle-Definition
