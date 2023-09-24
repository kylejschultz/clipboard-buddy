import rumps
from AppKit import (NSPasteboard, NSPasteboardTypeString, NSAlert, NSModalResponseOK)
import shelve
import os
import webbrowser

GITHUB_BASE_URL = "https://github.com/kylejschultz/clipboard-buddy/"

def format_clipboard_content(content, max_length=25):
    return content if len(content) <= max_length else content[:max_length] + "..."

class ClipboardHistoryApp(rumps.App):
    def __init__(self, title, *args, **kwargs):
        super(ClipboardHistoryApp, self).__init__(title, *args, **kwargs)
        self.storage_path = os.path.expanduser('~/clipboard-buddy')
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)

        with shelve.open(os.path.join(self.storage_path, "clipboard_history_db")) as db:
            self.clipboard_history = db.get('history', [])        
            self.update_menu()  # Update the menu immediately after initializing

    @rumps.clicked("About", "GitHub")
    def open_github(self, _):
        webbrowser.open(GITHUB_BASE_URL)

    @rumps.clicked("About", "Report Issue")
    def report_issue(self, _):
        webbrowser.open(GITHUB_BASE_URL + "issues")

    @rumps.clicked("Clear History")
    def clear_history(self, _):
        confirmation = NSAlert.alloc().init()
        confirmation.setMessageText_("Clear History Confirmation")
        confirmation.setInformativeText_("Are you sure you want to clear the clipboard history?")
        confirmation.addButtonWithTitle_("Clear")
        confirmation.addButtonWithTitle_("Cancel")
        response = confirmation.runModal()
        if response == NSModalResponseOK:
            self.clipboard_history = []
            with shelve.open(os.path.join(self.storage_path, "clipboard_history_db")) as db:
                db['history'] = self.clipboard_history
            self.update_menu()

    @rumps.timer(1)
    def check_clipboard(self, _):
        pb = NSPasteboard.generalPasteboard()
        content = pb.stringForType_(NSPasteboardTypeString)
        if content:
            formatted_content = format_clipboard_content(content)
            if not self.clipboard_history or self.clipboard_history[-1]['full'] != content:
                entry = {'full': content, 'display': formatted_content}
                self.clipboard_history.append(entry)
                if len(self.clipboard_history) > 15:
                    self.clipboard_history.pop(0)
                self.update_menu()
                with shelve.open(os.path.join(self.storage_path, "clipboard_history_db")) as db:
                    db['history'] = self.clipboard_history

    def update_menu(self):
        self.menu.clear()
        for item in reversed(self.clipboard_history):
            self.menu.add(rumps.MenuItem(item['display'], callback=self.copy_to_clipboard))
        self.menu.add(None)
        self.menu.add(rumps.MenuItem("Clear History", callback=self.clear_history))
        about_menu = rumps.MenuItem("About")
        about_menu.add(rumps.MenuItem("GitHub", callback=self.open_github))
        about_menu.add(rumps.MenuItem("Report Issue", callback=self.report_issue))
        about_menu.add(None)
        about_menu.add(rumps.MenuItem("App Version 0.1"))
        about_menu.add(rumps.MenuItem("Made by Kyle Schultz"))
        self.menu.add(about_menu)

    def copy_to_clipboard(self, sender):
        pb = NSPasteboard.generalPasteboard()
        pb.declareTypes_owner_([NSPasteboardTypeString], None)
        content_to_copy = next((entry['full'] for entry in self.clipboard_history if entry['display'] == sender.title), None)
        if content_to_copy:
            pb.setString_forType_(content_to_copy, NSPasteboardTypeString)

if __name__ == "__main__":
    app = ClipboardHistoryApp("", icon='icon.png')
    app.run()
