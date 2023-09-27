# Clipboard Buddy
### _A simple MacOS clipboard history app_

This simple Python-based app provides a history for your clipboard, locally storing the last 15 clipboard entries in an easy-access Menu Bar app. 

Most clipboard managers offered things like cloud-sync and cross-platform compatability, which was more than I was looking for. What I needed was a simple list of the last handful of things I copied but I forgot to paste.

## Features
- Saves up to 15 previous clipboard entries for re-copying and reusing later.
- Option to clear the history
- Stored locally using Python `shelve`

Planned and requested features can be found on the [Issues tab with the Enhancement label](https://github.com/kylejschultz/clipboard-buddy/issues?q=is:open+is:issue+label:enhancement)

## Installation
To install the latest release build, go to the [release](https://github.com/kylejschultz/clipboard-buddy/releases) page and download the latest `dmg` file. You will likely receive a popup that the app cannot be installed as it is unsigned. You will need to go to __System Preferences__ > __Privacy & Security__ and allow the application to be installed.

Dev builds are automatically built by GitHub when changes are merged into `main` and are not recommended for use, as they are very much development builds and can be wildly unstable. 

## Build
To build the app yourself, you will need to use [PyInstaller](https://pyinstaller.org/en/stable/index.html). 

Simply use ```pyinstaller cb.spec``` to build a copy of the application with the proper files mounted. `Clipboard Buddy.app` will be available in the `dist` folder.