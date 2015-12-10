import sublime, sublime_plugin, json, subprocess
from subprocess import Popen, PIPE, STDOUT
try:
  from urllib.request import urlopen, Request, build_opener
except ImportError:
  from urllib2 import urlopen, Request, build_opener

class PasteryCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    settings = sublime.load_settings('Pastery.sublime-settings')
    api_key = settings.get("api_key")
    content = u''
    for region in self.view.sel():
      if not region.empty():
          content += self.view.substr(region)

    url = "https://www.pastery.net/api/paste/?&api_key=" + api_key

    # determine POST
    try:
      print("Trying to post with Python lib")
      req = Request(url,
            data=bytes(content),
            headers={'User-Agent': 'Mozilla/5.0 (Sublime Text) Pastery plugin'})
      response = urlopen(req)

      if response.code != 200:
        print("Error while pasting.")
        sublime.status_message("Error while pasting to Pastery.")
      else:
        rurl = json.loads(response.decode("utf8"))["url"]
        print("Python lib it is:" + rurl)
        sublime.set_clipboard(str(rurl))
        sublime.status_message("Paste: " + str(rurl))
    except Exception:
      print("Trying to post with CURL")
      curl = "curl -X POST "+url
      response = subprocess.Popen(["curl", "-X", "POST", url, "--data", content], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      stdout, stderr = response.communicate()
      rurl = json.loads(stdout.decode("utf8"))["url"]
      print("CURL it is: " + rurl)

      if rurl:
        sublime.set_clipboard(str(rurl))
        sublime.status_message("Paste: " + str(rurl))
      else:
        print("Error while pasting.")
        sublime.status_message("Error while pasting to Pastery.")
