from sublime_plugin import TextCommand


class _docblockr_test_replace_cursor_position(TextCommand):
    def run(self, edit):
        cursor_placeholder = self.view.find('\\|', 0)

        if not cursor_placeholder or cursor_placeholder.empty():
            return

        self.view.sel().clear()
        self.view.sel().add(cursor_placeholder.begin())
        self.view.replace(edit, cursor_placeholder, '')
