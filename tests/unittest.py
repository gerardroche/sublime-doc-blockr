import unittest

import sublime


class ViewTestCase(unittest.TestCase):

    def setUp(self):
        self.window = sublime.active_window()
        self.view = self.window.new_file()
        self.view.set_scratch(True)

        # TODO there's probably a better way to initialise the testcase default settings
        settings = self.view.settings()
        settings.set('auto_indent', False)
        settings.set('docblockr.lower_case_primitives', False)
        settings.set('docblockr.param_description', True)
        settings.set('docblockr.per_section_indent', False)
        settings.set('docblockr.return_description', True)
        settings.set('docblockr.short_primitives', False)
        settings.set('docblockr.spacer_between_sections', False)
        settings.set('docblockr.function_description', True)

        if int(sublime.version()) < 3000:
            self.edit = self.view.begin_edit()

    def tearDown(self):
        if int(sublime.version()) < 3000:
            self.view.sel().clear()
            self.view.end_edit(self.edit)
            self.window.run_command('close')
        else:
            self.view.close()

    def set_view_content(self, content):
        if isinstance(content, list):
            content = '\n'.join(content)
        self.view.run_command('insert', {'characters': content})
        self.view.run_command('_docblockr_test_replace_cursor_position')
        self.view.set_syntax_file(self.get_syntax_file())

    def get_syntax_file(self):
        raise NotImplementedError('Must be implemented')

    def get_view_content(self):
        return self.view.substr(sublime.Region(0, self.view.size()))

    def run_doc_blockr(self):
        self.view.run_command('jsdocs')

    def assertDocBlockrResult(self, expected):
        if isinstance(expected, list):
            expected = '\n'.join(expected)

        # TODO test selections; for now just removing the placeholders
        expected = expected.replace('|CURSOR|', '')
        expected = expected.replace('|SELECTION_BEGIN|', '')
        expected = expected.replace('|SELECTION_END|', '')

        self.assertEquals(expected, self.get_view_content())
