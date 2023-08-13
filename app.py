import sys

from handler.browser_handler import BrowserHandler
from handler.preferences_handler import PreferencesHandler, ChannelErrorState
from ui.ui_handler_main import UIHandlerMain, UICleaner
from ui.ui_handler_run import UIHandlerRun
from ui.ui_handler_user_input import UIHandlerUserInput


class App:
    def __init__(self):
        self.preference_handler = PreferencesHandler()

    def _run_on_start(self):
        UIHandlerMain.show_logo()
        # do countdown
        if UIHandlerMain.run_on_start_countdown():
            UIHandlerRun(self.preference_handler.channels, self.preference_handler.options["browser_path"]).run()

    def run(self):
        are_preferences_loaded = self.preference_handler.load_from_file() is None

        options = self.preference_handler.options
        channels = self.preference_handler.channels

        if options.get("app_run_on_start"):
            self._run_on_start()

        ui_handler = UIHandlerMain(are_preferences_loaded, options, channels)

        while True:
            option = ui_handler.run()
            ui_handler.print_ui = True
            ui_handler.clear_console = True
            match option:
                case 1:
                    # run sniffer
                    if self.preference_handler.options["browser_path"] is None:
                        ui_handler.run_no_browser_path_error()
                        continue
                    if not BrowserHandler.browser_is_path_correct(self.preference_handler.options["browser_path"]):
                        ui_handler.run_bad_browser_path_error()
                        continue
                    if not self.preference_handler.channels:
                        ui_handler.run_no_channel_error()
                        continue
                    UIHandlerRun(self.preference_handler.channels,
                                 self.preference_handler.options["browser_path"]).run()
                    ui_handler.print_ui = True
                    ui_handler.clear_console = True
                case 2:
                    # set/edit browser path

                    UIHandlerUserInput.clear_and_show_logo()
                    while True:
                        browser_path = UIHandlerUserInput.browser_path_input_menu(
                            self.preference_handler.options["browser_path"])
                        if browser_path is None:
                            break
                        is_path_correct = BrowserHandler.browser_is_path_correct(browser_path)
                        if is_path_correct:
                            self.preference_handler.options["browser_path"] = browser_path
                        UIHandlerUserInput.browser_path_input_result(is_path_correct)
                case 3:
                    # add new channel
                    prompt = " - Add new channel menu"
                    UIHandlerUserInput.clear_and_show_logo()
                    while True:
                        channel = UIHandlerUserInput.channel_input_menu(channels, prompt, True)
                        if channel is None:
                            break
                        UIHandlerUserInput.channel_add_result(self.preference_handler.channel_add(channel))
                    # update the main menu ui with changes on return
                    ui_handler.update(options, channels)
                case 4:
                    # remove channel
                    prompt = " - Remove channel menu"
                    UIHandlerUserInput.clear_and_show_logo()
                    while True:
                        channel = UIHandlerUserInput.channel_input_menu(channels, prompt, True)
                        if channel is None:
                            break
                        UIHandlerUserInput.channel_remove_result(self.preference_handler.channel_remove(channel))
                    # update the main menu ui with changes
                    ui_handler.update(options, channels)
                case 5:
                    # move channel up
                    prompt = " - Move channel up menu"
                    UIHandlerUserInput.clear_and_show_logo()
                    while True:
                        channel = UIHandlerUserInput.channel_input_menu(channels, prompt, True)
                        if channel is None:
                            break
                        move_result = self.preference_handler.channel_move_up(channel)
                        if move_result is None:
                            UIHandlerUserInput.channel_move_success(True, channels)
                        if move_result == ChannelErrorState.CHANNEL_ALREADY_ON_TOP:
                            UIHandlerUserInput.channel_move_already_on(True)
                        if move_result == ChannelErrorState.CHANNEL_DOES_NOT_EXIST:
                            UIHandlerUserInput.channel_move_not_exist()
                    # update the main menu ui with changes on return
                    ui_handler.update(options, channels)
                case 6:
                    # move channel down
                    prompt = " - Move channel down menu"
                    UIHandlerUserInput.clear_and_show_logo()
                    while True:
                        channel = UIHandlerUserInput.channel_input_menu(channels, prompt, True)
                        if channel is None:
                            break
                        move_result = self.preference_handler.channel_move_down(channel)
                        if move_result is None:
                            UIHandlerUserInput.channel_move_success(False, channels)
                        if move_result == ChannelErrorState.CHANNEL_ALREADY_ON_BOTTOM:
                            UIHandlerUserInput.channel_move_already_on(False)
                        if move_result == ChannelErrorState.CHANNEL_DOES_NOT_EXIST:
                            UIHandlerUserInput.channel_move_not_exist()
                    # update the main menu ui with changes on return
                    ui_handler.update(options, channels)
                case 7:
                    # toggle run on start
                    UICleaner.clear_console()
                    self.preference_handler.option_set("app_run_on_start",
                                                       not self.preference_handler.options.get("app_run_on_start"))
                case 8:
                    # toggle save on exit
                    UICleaner.clear_console()
                    self.preference_handler.option_set("app_save_on_exit",
                                                       not self.preference_handler.options.get("app_save_on_exit"))
                case 9:
                    # save preferences and cookies to file
                    UIHandlerUserInput.save_preferences_result(self.preference_handler.save_to_file())
                    ui_handler.print_ui = False
                    ui_handler.clear_console = False
                case 0:
                    # exit
                    UICleaner.clear_console()
                    UIHandlerMain.show_logo()
                    if self.preference_handler.options.get("app_save_on_exit"):
                        UIHandlerUserInput.save_preferences_result(self.preference_handler.save_to_file())
                    print(" Exiting\n")
                    sys.exit(0)
                case _:
                    print(" Invalid option. Try again.")
