"""[OVERVIEW] Sublime Text plugin, which sends the selected text or entire file content to the Pastery pastebin service.

[INFO] Pastery online service:
https://www.pastery.net/

[API]
https://www.pastery.net/api/
"""

import os
import json
import subprocess

from urllib.parse import quote
from urllib.request import urlopen, Request

import sublime
import sublime_plugin


class PasteryCommand(sublime_plugin.TextCommand):
    """Sublime Text “pastery” command.

    Attributes
    ----------
        api_key (str): The API key required for authentication with Pastery.
        default_title (str): The default title for the snippet.
        duration (str): The duration in minutes for which the snippet will be available on Pastery.
    """

    def __init__(self, view):
        """Initialize API parameters.

        [REQUIRED] To resolve Pylint “W0201” warning:
        https://pylint.readthedocs.io/en/latest/user_guide/messages/warning/attribute-defined-outside-init.html
        """
        super().__init__(view)
        self.api_key = None
        self.default_title = "Untitled"
        self.duration = "1440"

    def run(self, edit):
        """Jumping-off point for the code. Sublime Text calls this method when the command is invoked.

        [INFO] From the book “Writing Sublime plugins” by Josh Earl, page 20:
        “The second parameter, "edit", is an instance of the "Edit" class.
        This class allows you to bundle multiple text changes together
        so they can be rolled back as a group if necessary.”

        Parameters
        ----------
            edit (sublime.Edit): An edit object used for making changes to the view.
        """
        settings = sublime.load_settings("Pastery.sublime-settings")
        self.api_key = settings.get("api_key")
        self.duration = settings.get("duration")

        # [INFO] “Returns the full name of the file associated with the sheet, or “None” if it doesn’t exist on disk”:
        # https://www.sublimetext.com/docs/api_reference.html#sublime.View.file_name
        active_view = self.view.file_name()

        # [INFO] Set default title:
        #
        # 1. If the user selected text in a file that is saved in his file system,
        # “default_title” is the filename without path and with extension.
        # 2. Else the user has selected text in an unsaved file, in the so-called “unsaved buffer”,
        # the value of “default_title” is “Untitled” string.
        self.default_title = os.path.basename(active_view) if active_view else "Untitled"

        # [INFO] Sublime Text input panel:
        # https://www.sublimetext.com/docs/api_reference.html#sublime.Window.show_input_panel
        self.view.window().show_input_panel(
            "Name your snippet: ",
            self.default_title,
            self.on_done,
            # [REQUIRED] Wrapping “sublime.status_message()” to function here
            lambda *args: sublime.status_message("You are editing the default snippet name"),
            lambda *args: sublime.status_message(
                "The snippet wasn’t sent to Pastery. To send, press “Enter” when your caret inside the input panel."
            )
        )

    def on_done(self, user_input):
        """Handle the user input for the snippet’s title and sends the content to Pastery.

        Parameters
        ----------
            user_input (str): The title entered by the user in the input panel.
        """
        # [INFO] Removes any leading and trailing whitespaces in user input
        stripped_user_input = user_input.strip()

        # [INFO] Set the title:
        #
        # 1. If any text in the input panel before pressing “Enter”, this text will be the name of the snippet.
        # 2. Else the user removes all text from input panel and press “Enter”, plugin sent to Pastery “default_title”.
        title = stripped_user_input if user_input else self.default_title

        # [REQUIRED] Encode the title.
        #
        # The plugin may not correctly send the snippet if the title contains spaces and/or non-ASCII characters,
        # such as Cyrillic.
        #
        # [INFO] The Pastery site shows decoded titles to its visitors.
        encoded_title = quote(title.encode("utf8"))

        # Extract content from selection or entire file
        content = ""
        for region in self.view.sel():
            if not region.empty():
                content += self.view.substr(region)

        # Nothing was selected, try selecting everything.
        if not content:
            content = self.view.substr(sublime.Region(0, self.view.size()))

        # There was still nothing selected, which means the file is empty.
        if not content:
            sublime.status_message("There was nothing to paste, aborted.")
            return

        # [INFO] The final URL to send to Pastery via API
        url = (
            f"https://www.pastery.net/api/paste/?api_key={self.api_key}&duration={self.duration}&title={encoded_title}"
        )
        print(url)

        # determine POST
        try:
            print("Trying to post with Python lib")
            req = Request(
                url,
                data=bytes(content.encode("utf8")),
                headers={"User-Agent": "Mozilla/5.0 (Sublime Text) Pastery plugin"},
            )
            response = urlopen(req)

            if response.code != 200:
                print("Error while pasting.")
                sublime.status_message("Error while pasting to Pastery.")
            else:
                rurl = json.loads(response.read().decode("utf8"))["url"]
                print("Python lib it is:" + rurl)
                sublime.set_clipboard(str(rurl))
                sublime.status_message("Paste: " + str(rurl))
        except Exception:
            print("Trying to post with CURL")
            response = subprocess.Popen(
                ["curl", "-X", "POST", url, "--data", content], stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            stdout, stderr = response.communicate()
            rurl = json.loads(stdout.decode("utf8"))["url"]
            print("CURL it is: " + rurl)

            if rurl:
                sublime.set_clipboard(str(rurl))
                sublime.status_message("Paste: " + str(rurl))
            else:
                print("Error while pasting.")
                sublime.status_message("Error while pasting to Pastery.")
