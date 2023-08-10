import os
import time


class UICleaner:

    @staticmethod
    def clear_console():
        os.system('cls' if os.name == 'nt' else 'clear')


class UIHandlerMain:
    def __init__(
            self,
            are_preferences_loaded: bool,
            options: dict,
            channels: list,
            print_ui: bool = True,
            clear_console: bool = True
    ):

        self.are_preferences_loaded = are_preferences_loaded
        self.options = options
        self.channels = channels
        self.print_ui = print_ui
        self.clear_console = clear_console

    @staticmethod
    def show_logo() -> None:
        print(" ------------------- TwitchSniffer ------------------- \n")

    def _show_info(self) -> None:
        print(" - Status:")
        print(f"    Preferences: {'successfully' if self.are_preferences_loaded else 'not '} loaded")

    def _show_channels(self) -> None:
        channel_list = self.channels
        print(""
              " - Channels:")

        if not channel_list:
            print("    No channels added.")
            return

        self.print_channel_bar(channel_list)

    def update(self, options: dict, channels: list) -> None:
        self.channels = channels
        self.options = options

    @staticmethod
    def print_channel_bar(channel_list: list, channels_per_line: int = 3, end: str = ""):
        if not channel_list:
            print("    No channels added.")
            return
        channel_string = "   "
        for i, channel in enumerate(channel_list, 0):
            if i != 0:
                channel_string += ","
            if i % channels_per_line == 0 and i != 0:
                channel_string += "\n   "
            channel_string += f" ({i + 1}){channel}"
        print(channel_string + end)

    def run_no_channel_error(self):
        print("\n - No channel was added")
        print("    Please add any channel and try again\n")
        self.print_ui = False
        self.clear_console = False

    def run_bad_browser_path_error(self):
        print("\n - Bad browser path")
        print("    Please edit browser path and try again\n")
        self.print_ui = False
        self.clear_console = False

    def run_no_browser_path_error(self):
        print("\n - No browser path was set")
        print("    Please set browser path and try again\n")
        self.print_ui = False
        self.clear_console = False

    def _show_options(self) -> None:
        set_edit = "Set" if self.options['browser_path'] is None else "Edit"
        options = [
            "",
            " 1)  Run",
            f" 2)  {set_edit} browser path",
            " 3)  Add new channel",
            " 4)  Remove channel",
            " 5)  Move channel up",
            " 6)  Move channel down",
            f" 7)  Run on startup: {self.options['app_run_on_start']}",
            f" 8)  Save on exit: {self.options['app_save_on_exit']}",
            " 9)  Save current settings",
            " 0)  Exit",
            ""
        ]

        options_string = "\n".join(options)
        print(options_string)

    @staticmethod
    def _get_option() -> int:
        while True:
            try:
                option = int(input(" Enter option: "))
                if option in range(10):
                    return option
                else:
                    print(" Invalid option. Try again.")
            except ValueError:
                print(" Invalid option. Try again.")

    @staticmethod
    def run_on_start_countdown(secs: int = 5) -> bool:
        print(f" - Starting in {secs} seconds")
        print("    Press Ctrl+C to cancel")
        print("")
        try:
            for i in range(secs, 0, -1):
                print(f"   {i}")
                time.sleep(1)
            print("")
            return True
        except KeyboardInterrupt:
            print("")
            print(" - Canceled")
            return False

    def run(self) -> int:
        if self.clear_console:
            UICleaner.clear_console()
        if self.print_ui:
            self.show_logo()
            self._show_info()
            self._show_channels()
            self._show_options()
        option = self._get_option()
        return option
