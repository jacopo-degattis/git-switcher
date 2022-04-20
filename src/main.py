import yaml
import rumps
import subprocess
import pprint
from yaml.loader import FullLoader
from pprint import pprint

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

    def _write_to_file(self, email):
        documents = None
        with open("./config.yaml", "w") as config:
            documents = yaml.dump([{"accounts": [*self.config["accounts"], email]}], config)
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

        accounts = self.config["accounts"] or []
        
        for index, account in enumerate(accounts):
            btn = rumps.MenuItem(
                title=account,
                callback=self._btn_callback,
                key=str(index+1)
            )

            btn.add(
                rumps.MenuItem(
                    title="Delete",
                    callback=lambda sender: self._remove_from_list(sender, account)
                )
            )

            self.buttons.append(btn)

        self.app.menu = [
            *self.buttons,
            rumps.MenuItem(
                title="+ Add",
                callback=lambda _: self._handle_window()
            )
        ]

    def _remove_from_list(self, sender, email):
        del self.app.menu[email]
        # TODO: remove email also from local yaml / json storage file

    def _toggle_btns_from_value(self, value):
        for entry in self.buttons:
            entry.state = 1 if entry.title == value else 0

    def _handle_window(self):
        win = rumps.Window(
            message='Insert emails separated by a comma',
            default_text='test@example.com',
            title='Add new email',
            ok=None,
            cancel=True,
            dimensions=(200, 25)
        )

        response = win.run()
        
        if not response.clicked:
            return
        
        if not response.text:
            return

        self._write_to_file(str(response.text))
        
        new_entry = rumps.MenuItem(
            title=str(response.text),
            callback=self._btn_callback,
            key=str(len(self.app.menu) - 1)
        )
        new_entry.add(           
            rumps.MenuItem(
                title="Delete",
                callback=lambda sender: self._remove_from_list(sender, str(response.text)),
            )
        )
        self.buttons = [*self.buttons, new_entry]
        
        self.app.menu.insert_before(
            "+ Add",
            new_entry
        )

    def _btn_callback(self, sender):
        subprocess.call([*UPDATE_COMMAND, sender.title])
        rumps.notification(title="Git mail changed", subtitle="Git email has been succesfully changed !", message='')
        self._toggle_btns_from_value(sender.title)

    def run(self):
        self.app.run()

if __name__ == "__main__":
    a = GitSwitchApp()
    a.run()

