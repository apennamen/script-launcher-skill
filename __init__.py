import subprocess
from mycroft import MycroftSkill, intent_handler
from mycroft.util.log import getLogger

LOGGER =  getLogger(__name__)

class ScriptLauncher(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_handler('launcher.script.intent')
    def handle_launcher_script(self, message):
        process = subprocess.Popen("/home/pi/picroft-scripts/connect-speaker.sh", 
                                   shell=True, stdout=subprocess.PIPE)
        process.wait()
        LOGGER.debug(process.returncode)
        self.speak_dialog('launcher.script')


def create_skill():
    return ScriptLauncher()

