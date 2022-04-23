import json
import rumps
import subprocess
import pprint
from pprint import pprint

UPDATE_COMMAND = ["/usr/local/bin/git", "config", "--global", "user.email"]

class GitSwitchApp(object):

    def __init__(self):
        self.buttons = list()
        self.win_text = None
        self.win_clicked = None
        self.app = rumps.App("GitSwitch", icon="./git-logo.png")
        self.config = self._load_config_file()
        self._create_entries_from_config()
        self._toggle_btns_from_value(subprocess.check_output(UPDATE_COMMAND).decode().strip())

    def _write_to_file(self, emails):
        documents = None
        with open("./config.json", "w") as config:
            documents = json.dump({"accounts": emails}, config)
        return documents

    def _load_config_file(self, config_file="./config.json"):
        data = None
        with open(config_file) as config:
            data = json.load(config)
        return data

    def _create_entries_from_config(self):
        
        if not self.config:
            raise Exception("No config file found. Please create a valid config.json file")

        if not "accounts" in self.config.keys():
            raise Exception("Invalid config file")

        accounts = self.config["accounts"] or []
        
        for index, account in enumerate(accounts):
            btn = rumps.MenuItem(
                title=account,
                callback=self._btn_callback,
                key=str(index+1)
            )

            self.buttons.append(btn)

        self.app.menu = [
            *self.buttons,
            rumps.MenuItem(
                title="+ Add",
                callback=lambda _: self._handle_window()
            )
        ]

    def _toggle_btns_from_value(self, value):
        for entry in self.buttons:
            entry.state = 1 if entry.title == value else 0

    def _clean_empty_lines(self, lines):
        for x in lines:
            print("LINE => ", x)

    def _handle_window(self):
        win = rumps.Window(
            message='Insert emails separated by a comma',
            default_text=''.join(f"{x}\n" for x in self.config["accounts"]),
            title='Add new email',
            ok=None,
            cancel=True,
            dimensions=(200, 80)
        )

        response = win.run()
        
        if not response.clicked:
            return
        
        if not response.text:
            return

        lines = [x for x in response.text.split("\n") if x != ""]
        self._write_to_file(lines)
        
        for x in lines:
            if x not in self.config["accounts"]:
                new_entry = rumps.MenuItem(
                    title=x,
                    callback=self._btn_callback,
                    key=str(len(self.app.menu) - 1)
                )

                self.buttons = [*self.buttons, new_entry]
                self.config["accounts"].append(x)

                self.app.menu.insert_before(
                    "+ Add",
                    new_entry
                )

        new_config = self.config["accounts"]
        for y in new_config:
            if y not in lines:
                del self.app.menu[y]
                self.config["accounts"].remove(y)
                
                self.buttons = [x for x in self.buttons if x.title != y]
                
    def _btn_callback(self, sender):
        subprocess.call([*UPDATE_COMMAND, sender.title])
        rumps.notification(title="Git mail changed", subtitle="Git email has been succesfully changed !", message='')
        self._toggle_btns_from_value(sender.title)

    def run(self):
        self.app.run()

if __name__ == "__main__":
    a = GitSwitchApp()
    a.run()
