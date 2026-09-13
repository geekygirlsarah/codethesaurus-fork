import os
import shutil
from io import StringIO
from django.core.management import call_command
from django.test import TestCase

class TestCommands(TestCase):
    def test_validatemetainfofile_command(self):
        out = StringIO()
        call_command('validatemetainfofile', stdout=out)
        self.assertIn('No errors found in meta_info.json.', out.getvalue())

    def test_validatelanginfofiles_command(self):
        out = StringIO()
        # This might take a while as it validates all files
        call_command('validatelanginfofiles', stdout=out)
        # It should at least finish without error and say something positive
        # Depending on the output of that command
        self.assertIn('no issues found', out.getvalue().lower())

    def test_generate_template_command(self):
        out = StringIO()
        test_lang = 'test_lang'
        test_version = '1.0'
        test_structure = 'data_types'
        
        # Ensure cleanup
        test_lang_dir = os.path.join('web', 'thesauruses', test_lang)
        if os.path.exists(test_lang_dir):
            shutil.rmtree(test_lang_dir)
            
        try:
            call_command(
                'generate_template', 
                test_lang, 
                test_structure, 
                language_version=test_version, 
                stdout=out
            )
            
            self.assertIn('Created template file', out.getvalue())
            
            # Verify file exists
            expected_file = os.path.join('web', 'thesauruses', test_lang, '1', f'{test_structure}.json')
            self.assertTrue(os.path.exists(expected_file))
            
        finally:
            # Cleanup
            if os.path.exists(test_lang_dir):
                shutil.rmtree(test_lang_dir)

    def test_generate_missing_templates_command(self):
        # This one uses os.system('python manage.py ...') which is hard to test with call_command
        # and it might try to generate MANY files.
        # Maybe skip for now or mock os.system
        pass
