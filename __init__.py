import subprocess
from mycroft import MycroftSkill, intent_handler
from mycroft.util.log import getLogger

LOGGER = getLogger(__name__)


class ScriptLauncher(MycroftSkill):
    def __init__(self):
        self.scripts_registry = dict()
        MycroftSkill.__init__(self)

    def initialize(self):
        self.scripts_registry.update({
            "connexion enceinte": "/home/pi/picroft-scripts/connect-speaker.sh",
            "déconnexion enceinte": "/home/pi/picroft-scripts/disconnect-speaker.sh",
        })

    @intent_handler('launcher.script.intent')
    def handle_launcher_script(self, message):
        # Extract script alias from intent
        script_alias = message.data.get('script_alias')
        LOGGER.debug("Script alias received: %s" % script_alias)
        if script_alias is None:
            return self.speak_dialog('no.script.found')

        # Find script to execute
        script_to_exec = self.scripts_registry.get(script_alias)
        LOGGER.debug("Script to execute: %s" % script_alias)
        if script_to_exec is None:
            return self.speak_dialog('no.script.found')

        # Execute process
        process = subprocess.Popen(script_to_exec,
                                   shell=True, stdout=subprocess.PIPE)
        process.wait()

        # Handle script return code
        LOGGER.debug("Script return code: %s" % process.returncode)
        if process.returncode != 0:
            return self.speak_dialog('script.error')

        self.speak_dialog('launcher.script')


def create_skill():
    return ScriptLauncher()
