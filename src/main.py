import yaml
import rumps
import subprocess
from yaml.loader import FullLoader

UPDATE_COMMAND = ["/usr/local/bin/git", "config", "--global", "user.email"]

class GitSwitchApp(object):

    def __init__(self):
        self.buttons = list()
        self.app = rumps.App("GitSwitch", icon="./git-logo.png")
        self.config = self._load_config_file()
        self._create_entries_from_config()
        self._toggle_btns_from_value(subprocess.check_output(UPDATE_COMMAND).decode().strip())

    def _load_config_file(self, config_file="./config.yaml"):
        data = None
        with open(config_file) as config:
            data = yaml.load(config, Loader=FullLoader)
        return data

    def _create_entries_from_config(self):
        
        if not self.config:
            raise Exception("No config file found. Please create a valid config.yaml file")

        if not "accounts" in self.config.keys():
            raise Exception("Invalid config file")

        accounts = self.config["accounts"]

        for index, account in enumerate(accounts):
            self.buttons.append(rumps.MenuItem(title=account, callback=self._btn_callback, key=str(index+1)))

        self.app.menu = self.buttons

    def _toggle_btns_from_value(self, value):
        for entry in self.buttons:
            entry.state = 1 if entry.title == value else 0

    def _btn_callback(self, sender):
        subprocess.call([*UPDATE_COMMAND, sender.title])
        rumps.notification(title="Git mail changed", subtitle="Git email has been succesfully changed !", message='')
        self._toggle_btns_from_value(sender.title)

    def run(self):
        self.app.run()

if __name__ == "__main__":
    a = GitSwitchApp()
    a.run()

