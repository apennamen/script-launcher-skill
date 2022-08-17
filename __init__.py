import subprocess
import json
from mycroft import MycroftSkill, intent_handler


class ScriptLauncher(MycroftSkill):
    def __init__(self):
        self.scripts_registry = dict()
        MycroftSkill.__init__(self)

    def initialize(self):
        self.register_entity_file('script_alias.entity')
        
        self.settings_change_callback = self.on_settings_changed
        self.on_settings_changed()
    
    def on_settings_changed(self):
        self.init_script_registry()

    def init_script_registry(self):
        scripts_setting = self.settings.get('scripts_dict')
        if scripts_setting is None:
            return self.speak('settings.configuration.needed')
        self.parse_script_registry_from_settings(scripts_setting)
        
    def parse_script_registry_from_settings(self, scripts_setting):
        try:
            self.scripts_registry = json.loads(scripts_setting)
            self.log.debug("Configuration loaded")
        except Exception:
            self.log.error("Error parsing configuration from server")
            self.speak_dialog('settings.configuration.failed')

    @intent_handler('launcher.script.intent')
    def handle_launcher_script(self, message):
        # Extract script alias from intent
        script_alias = message.data.get('script_alias')
        self.log.debug("Script alias received: %s" % script_alias)
        if script_alias is None:
            return self.speak_dialog('no.script.found')

        # Find script to execute
        script_to_exec = self.scripts_registry.get(script_alias)
        self.log.debug("Script to execute: %s" % script_alias)
        if script_to_exec is None:
            return self.speak_dialog('no.script.found')

        # Execute process
        process = subprocess.Popen(script_to_exec,
                                   shell=True, stdout=subprocess.PIPE)
        process.wait()

        # Handle script return code
        self.log.debug("Script return code: %s" % process.returncode)
        if process.returncode != 0:
            return self.speak_dialog('script.error')

        self.speak_dialog('launcher.script')


def create_skill():
    return ScriptLauncher()
