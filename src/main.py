import yaml
import rumps
import subprocess
from yaml.loader import FullLoader

UPDATE_COMMAND = ["/usr/local/bin/git", "config", "--global", "user.email"]

class GitSwitchApp(object):

    def __init__(self):
        self.buttons = list()
        self.win_text = None
        self.win_clicked = None
        self.app = rumps.App("GitSwitch", icon="./git-logo.png")
        self.config = self._load_config_file()[0]
        self._create_entries_from_config()
        self._toggle_btns_from_value(subprocess.check_output(UPDATE_COMMAND).decode().strip())

        self.window = rumps.Window(
            message='Insert emails separated by a comma',
            title='Add new email', default_text='test@example.com',
            ok=None,
            cancel=True,
            dimensions=(200, 25)
        )

    def _write_to_file(self, email):
        documents = None
        with open("./config.yaml", "w") as config:
            documents = yaml.dump([{"accounts": [*self.config["accounts"], str(email)]}], config)
            # del self.app.menu["jacopo.degattis@gmail.com"]
            self.app.menu.insert_after(self.config["accounts"][-1], rumps.MenuItem(title=str(email), callback=lambda x: print("CIAO")))
        return documents

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

        self.app.menu = [*self.buttons, rumps.MenuItem(title="Test", callback=lambda _: self._handle_window())]

    def _toggle_btns_from_value(self, value):
        for entry in self.buttons:
            entry.state = 1 if entry.title == value else 0

    def _handle_window(self):
        response = self.window.run()
        
        if not response.clicked:
            return
        
        if not response.text:
            return

        self._write_to_file(response.text)

    def _btn_callback(self, sender):
        subprocess.call([*UPDATE_COMMAND, sender.title])
        rumps.notification(title="Git mail changed", subtitle="Git email has been succesfully changed !", message='')
        self._toggle_btns_from_value(sender.title)

    def run(self):
        self.app.run()

if __name__ == "__main__":
    a = GitSwitchApp()
    a.run()

