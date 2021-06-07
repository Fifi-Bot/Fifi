"""
MIT License

Copyright (c) 2021 Meme Studios

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from flask import Flask, redirect, render_template
from threading import Thread

#app = Flask('')

def urlparse(url) -> str:
  url = str(url)
  url.replace(" ", "+")
  url.replace("`", "%60")
  url.replace("@", "%40")
  url.replace("#", "%23")
  url.replace("$", "%24")
  url.replace("%", "%25")
  url.replace("^", "%5E")
  url.replace("&", "%26")
  url.replace("+", "%2B")
  url.replace("=", "%3D")
  url.replace("|", "%7C")
  url.replace("\\", "%5C")
  url.replace("[", "%5B")
  url.replace("]", "%5D")
  url.replace("{", "%7B")
  url.replace("}", "%7D")
  url.replace(":", "%3A")
  url.replace(";", "%3B")
  url.replace("'", "%27")
  url.replace(",", "%2C")
  url.replace("/", "%2F")
  url.replace("?", "%3F")
  return url

setFavicon = """
<link rel="Fifi Icon" type="image/png" href="https://cdn.discordapp.com/attachments/749875006238097478/833898070571614228/fifi_icon_transparent_background_revised_revised.png"/>
"""
setFont = """
<link href='https://fonts.googleapis.com/css?family=Comfortaa' rel='stylesheet'>

html {
      font-family: 'Comfortaa';
      margin: 0 auto;
    }
"""    

def commandSignature(command):
  clean_prefix = "f."
  if not command.signature and not command.parent:
    return f'"{clean_prefix}{command.name}"'
  if command.signature and not command.parent:
    return f'"{clean_prefix}{command.name} {command.signature}"'
  if not command.signature and command.parent:
    return f'"{clean_prefix}{command.parent} {command.name}"'
  else:
    return f'"{clean_prefix}{command.parent} {command.name} {command.signature}"'

msInvite = "https://discord.gg/3c5kc8M"

from replit import db

#gitbook = db['gitbook']

class FifiServer(Flask):
  def __init__(self, bot):
    super().__init__('Fifi')
    self.bot = bot
    #self.app = app
    self.route("/")(self.main)
    self.route("/status")(self.status)
    self.route("/redirect")(self._redirect)
    self.route("/stats")(self.status)
    self.route("/commands")(self.commands)
    self.route("/command")(self.commands)
    self.route("/guild")(self.guildInvite)
    self.route("/server")(self.guildInvite)
    self.route("/suport")(self.guildInvite)
    self.route("/invite")(self.botInvite)
    self.route("/invites")(self.botInvite)
    self.errorhandler(404)(self.unknownPage)
    self.route("/license")(self.license)
    self.route("/copyright")(self.license)

  def unknownPage(self, e):
    return render_template('unknown.html')

  def license(self):
    return """
MIT License
<br><br>
Copyright (c) 2021 Meme Studios
<br><br>
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish,distribute, sublicense, and/or sellcopies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
<br><br>
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
<br><br>
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
    """

  def _redirect(self, url):
    url = urlparse(url)
    return redirect(url)

  def botInvite(self):
    return render_template('botInvite.html')

  def guildInvite(self):
    return redirect(f"{msInvite}")

  #@app.route("/")
  def main(self):
    return render_template("main.html") #Get html and display it. yey

  #@app.route("/status")
  def status(self):
    return redirect("https://stats.uptimerobot.com/w7OgnCLQz7")

  def commands(self):
    s = f"{setFavicon}Note:<br>Arguments with <> means that the argument is required.<br>Arguments with [] means that the argument is optional.<br>DO NOT USE THESE WHEN TYPING COMMANDS<br><br>"
    for command in self.bot.commands:
      s += f"""
Command {command.name}: <br>- Syntax: {commandSignature(command)}<br>- Aliases: {' | '.join(command.aliases)[:-3]}<br>
      """
      if command.cog is None:
        s += "- Cog: No Category/None"
      else:
        s += f"- Cog: {command.cog.qualified_name}"
      s += "<br>"
      if command._buckets._cooldown is None:
        s += "- Cooldown: None"
      else:
        s += f"""
- Cooldown: <br>  - Rate (How long the cooldown lasts in seconds): {command._buckets._cooldown.rate} <br>  - Per (How many commands can be triggered before the cooldown hits): {command._buckets._cooldown.per} <br>  - Type: Each {str(command._buckets._cooldown.type).lower().replace('commands', '').replace('buckettype', '').replace('.', '').title()}
        """
      
      s += "<br><br>"
    return s

  

  def start(self):
    server = Thread(target=self.run)
    server.start()

  def run(self):
    super().run(host="0.0.0.0", port=8080)