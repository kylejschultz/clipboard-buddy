import sys
import rumps
from AppKit import (NSPasteboard, NSPasteboardTypeString, NSAlert, NSModalResponseOK)
import shelve
import os
import webbrowser
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt

GITHUB_BASE_URL = "https://github.com/kylejschultz/clipboard-buddy/"

def format_clipboard_content(content, max_length=25):
    return content if len(content) <= max_length else content[:max_length] + "..."

class SettingsDialog(QDialog):
    def __init__(self, main_app, parent=None):
        super().__init__(parent)
        self.main_app = main_app  # Store reference to the main app
        self.setWindowTitle("Settings")
        self.setFixedSize(300, 225)  # Adjusted to half of original height

        layout = QVBoxLayout(self)

        # Clear history button
        self.clear_history_btn = QPushButton("Clear History", self)
        self.clear_history_btn.clicked.connect(self.clear_history)
        layout.addWidget(self.clear_history_btn)

        # Add some space between settings and the action buttons
        layout.addSpacing(20)

        # Using a horizontal layout for the Save and Close buttons
        button_layout = QHBoxLayout()

        # Save button
        self.save_btn = QPushButton("Save", self)
        self.save_btn.clicked.connect(self.save_settings)
        button_layout.addWidget(self.save_btn)

        # Close button (renamed from Exit)
        self.close_btn = QPushButton("Close", self)
        self.close_btn.clicked.connect(self.close)
        button_layout.addWidget(self.close_btn)

        layout.addLayout(button_layout)

    def clear_history(self):
        confirmation = NSAlert.alloc().init()
        confirmation.setMessageText_("Clear History Confirmation")
        confirmation.setInformativeText_("Are you sure you want to clear the clipboard history?")
        confirmation.addButtonWithTitle_("Clear")
        confirmation.addButtonWithTitle_("Cancel")

        CLEAR_RESPONSE = 1000  # This is the response when the "Clear" button is clicked
        response = confirmation.runModal()

        if response == CLEAR_RESPONSE:
            # Set flag to skip next clipboard check after clearing the history
            self.main_app.skip_next_clipboard_check = True

            print("Attempting to clear history...")
            self.main_app.clipboard_history = []  # Use main_app's clipboard_history
            print("History cleared in memory. Saving to DB...")
            with shelve.open(os.path.join(self.main_app.storage_path, "clipboard_history_db")) as db:
                db['history'] = self.main_app.clipboard_history
            self.main_app.update_menu()
            print("History saved to DB and menu updated.")

    def save_settings(self):
        # Logic to save settings goes here
        self.accept()

class ClipboardHistoryApp(rumps.App):
    def __init__(self, title, *args, **kwargs):
        super(ClipboardHistoryApp, self).__init__(title, *args, **kwargs)
        self.storage_path = os.path.expanduser('~/clipboard-buddy')
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)
        
        self.quit_button = None

        with shelve.open(os.path.join(self.storage_path, "clipboard_history_db")) as db:
            self.clipboard_history = db.get('history', [])        
            self.update_menu()  # Update the menu immediately after initializing
        
        self.skip_next_clipboard_check = False

    @rumps.clicked("About", "GitHub")
    def open_github(self, _):
        webbrowser.open(GITHUB_BASE_URL)

    @rumps.clicked("About", "Report Issue")
    def report_issue(self, _):
        webbrowser.open(GITHUB_BASE_URL + "issues")

    @rumps.clicked("Settings")
    def open_settings(self, _):
        app = QApplication(sys.argv)
        dialog = SettingsDialog(self)  # Pass a reference to the main app instance
        dialog.setWindowModality(Qt.WindowModality.ApplicationModal)  # Set the window to be modal
        dialog.show()
        app.setActiveWindow(dialog)  # Ensure dialog is the active window
        dialog.exec()

    @rumps.timer(1)
    def check_clipboard(self, _):
        if self.skip_next_clipboard_check:
            self.skip_next_clipboard_check = False
            return
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

    def get_version(self):
            if getattr(sys, 'frozen', False):
                application_path = sys._MEIPASS
            else:
                application_path = os.path.dirname(os.path.abspath(__file__))
            version_file = os.path.join(application_path, 'src', 'version.txt')
            with open(version_file, 'r') as f:
                return f.read().strip()
    
    def update_menu(self):
        # Clear the Menu
        self.menu.clear()
        
        # Add clipboard history items
        for item in reversed(self.clipboard_history):
            self.menu.add(rumps.MenuItem(item['display'], callback=self.copy_to_clipboard))
        self.menu.add(None)  # Separator line
        
        # Add Settings item
        self.menu.add(rumps.MenuItem("Settings", callback=self.open_settings))
        self.menu.add(None)  # Separator line

        # About submenu
        about_menu = rumps.MenuItem("About")
        about_menu.add(rumps.MenuItem("GitHub", callback=self.open_github))
        about_menu.add(rumps.MenuItem("Report Issue", callback=self.report_issue))
        about_menu.add(None)
        about_menu.add(rumps.MenuItem(f"App Version: {self.get_version()}"))        
        about_menu.add(rumps.MenuItem("Made by Kyle Schultz"))
        self.menu.add(about_menu)
        self.menu.add(None)  # Separator line

        # Ensure quit button always exists
        if not any(item.title == "Quit" for item in self.menu):
            self.menu.add(rumps.MenuItem("Quit", callback=self.quit_app))

    def quit_app(self, _):
        rumps.quit_application()

    def copy_to_clipboard(self, sender):
        pb = NSPasteboard.generalPasteboard()
        pb.declareTypes_owner_([NSPasteboardTypeString], None)
        content_to_copy = next((entry['full'] for entry in self.clipboard_history if entry['display'] == sender.title), None)
        if content_to_copy:
            pb.setString_forType_(content_to_copy, NSPasteboardTypeString)

if __name__ == "__main__":
    app = ClipboardHistoryApp("", icon='src/icon.icns')
    app.run()
