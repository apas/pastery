import sublime, sublime_plugin, json, subprocess
from subprocess import Popen, PIPE, STDOUT

class PasteryCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    content = u''
    for region in self.view.sel():
      if not region.empty():
          content += self.view.substr(region)

    url = "https://www.pastery.net/api/paste/?"
    curl = "curl -X POST "+url
    response = subprocess.Popen(["curl", "-X", "POST", url, "--data", content], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = response.communicate()
    rurl = json.loads(stdout)["url"]
    print(rurl)

    if rurl:
      sublime.set_clipboard(str(rurl))
      sublime.status_message("Paste: " + str(rurl))
    else:
      print("Error while pasting.")
