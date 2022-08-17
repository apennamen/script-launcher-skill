from mycroft import MycroftSkill, intent_file_handler


class ScriptLauncher(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('launcher.script.intent')
    def handle_launcher_script(self, message):
        self.speak_dialog('launcher.script')


def create_skill():
    return ScriptLauncher()

