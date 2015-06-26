"""
Tab Switcher plugin for Sublime Text 3.
"""
import os

import sublime
import sublime_plugin


class TabSwitcherCommand(sublime_plugin.WindowCommand):
    """
    Tab Switcher command object.
    """
    def run(self):
        """
        Run command.
        """
        self.window = sublime.active_window()
        self.views = self.window.views()

        folders = self.window.folders()
        active_view = self.window.active_view()
        active_view_id = -1
        files_list = []

        for view in self.views:
            file_name = view.file_name()
            file_path = ''

            if file_name:
                for folder in folders:
                    if os.path.commonprefix([folder, file_name]) == folder:
                        file_path = os.path.relpath(file_name, folder)
                        break
                file_name = os.path.basename(file_name)
            elif view.name():
                file_name = view.name()
            else:
                file_name = 'untitled'

            if view.id() == active_view.id():
                active_view_id = len(files_list)

            files_list.append([file_name, file_path])

        self.window.show_quick_panel(files_list, self.tab_selected, False,
                                     active_view_id)

    def tab_selected(self, selected):
        """
        Activate selected tab.
        """
        if selected > -1:
            self.window.focus_view(self.views[selected])
        return selected
