from ui.ui_handler_main import UICleaner, UIHandlerMain


class UIHandlerUserInput:
    def __init__(self):
        pass

    @staticmethod
    def clear_and_show_logo():
        UICleaner.clear_console()
        UIHandlerMain.show_logo()

    @staticmethod
    def browser_path_input_menu(path: str) -> str:
        is_path_set = path is not None and path != ""
        set_edit = "Edit" if is_path_set else "Set"
        path_str = ""
        if is_path_set:
            path_str = "\n" + f"    Current path: {path}"
        prompt = f" - {set_edit} browser path menu {path_str}"
        print(prompt)
        while True:
            browser_path = UIHandlerUserInput._input_browser_path()
            if browser_path is None:
                break
            print("")
            return browser_path

    @staticmethod
    def browser_path_input_result(success) -> None:
        print(" Browser path set successfully.\n" if success else " Browser path does not exit, please try again.\n")

    @staticmethod
    def channel_input_menu(channels: list, prompt: str, print_channel_bar: bool = False) -> str:
        print(prompt)
        if print_channel_bar:
            UIHandlerMain.print_channel_bar(channels)
        while True:
            channel = UIHandlerUserInput._input_channel()
            if channel is None:
                break
            print("")
            return channel

    @staticmethod
    def channel_add_wrong_input():
        print(" Invalid channel name.\n")

    @staticmethod
    def channel_add_result(success) -> None:
        print(" Channel added successfully.\n" if success is None else " Channel already exists.\n")

    @staticmethod
    def channel_remove_result(success) -> None:
        print(" Channel removed successfully.\n" if success is None else " Channel does not exist.\n")

    @staticmethod
    def channel_move_not_exist() -> None:
        print(" Channel does not exist.\n")

    @staticmethod
    def channel_move_already_on(top: bool) -> None:
        direction = "top" if top else "bottom"
        print(f" Channel already on {direction}.\n")

    @staticmethod
    def channel_move_success(up: bool, channels: list = None) -> None:
        if channels:
            UIHandlerMain.print_channel_bar(channels)
        direction = "up" if up else "down"
        print(f" \nChannel successfully moved {direction}.\n")

    @staticmethod
    def save_preferences_result(success, end: str = "") -> None:
        print(("\n Preferences saved successfully.\n" if success is None else "\n Could not save preferences.\n") + end)

    @staticmethod
    def _input_channel() -> str:
        print("")
        print(" Enter '_' to return.")
        while True:
            try:
                channel = input(" Enter channel name: ")
                if channel == '_':
                    break
                if channel == "":
                    print(" Channel name cannot be empty.")
                    continue
                return channel
            except ValueError:
                print(" Invalid channel. Try again.")

    @staticmethod
    def _input_browser_path() -> str:
        print("")
        print(" Enter '_' to return.")
        while True:
            try:
                browser_path = input(" Enter browser path: ")
                if browser_path == '_':
                    break
                if browser_path == "":
                    print(" Browser path cannot be empty.")
                    continue
                return browser_path
            except ValueError:
                print(" Invalid browser path. Try again.")
