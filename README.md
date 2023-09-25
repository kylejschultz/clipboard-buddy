# Clipboard Buddy

### _A simple MacOS clipboard history app_

This simple Python based app provides a history for your clipboard, locally storing the last 15 clipboard entries in an easy-access Menu Bar app. 

Most clipboard managers offered things like cloud-sync and cross-platform compatability, which was more than I was looking for. What I needed was a simple list of the last handful of things I copied but I forgot to paste.

## Features
### Current Features
- Saves up to 15 previous clipboard entries for re-copying and reusing later.
- Option to clear the history
- Stored locally using Python `shelve`
- Entries shortened to 25 characters for view.
### Future Features
- [ ] Settings dialogue
    - [ ] Adjustable history count
    - [ ] Word wrap in menu vs truncation
    - [ ] Check for duplicates in history and ignore if already there (optional in settings)
- [ ] Configure automatic build in GitHub Actions on PR/Merge
- [ ] Add app to brew for easier installation.

## Installation
To install, go to the release page to download the latest `.app` version of Clipboard Buddy.

## Build
To build the app yourself, you will need to use [PyInstaller]{https://pyinstaller.org/en/stable/index.html}. 

Simply use `pyinstaller cb.spec` to build a copy of the application with the proper files mounted. `Clipboard Buddy.app` will be available in the `dist` folder.