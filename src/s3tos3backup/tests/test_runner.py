from __future__ import unicode_literals, absolute_import
import os

from mock import patch
from moto import mock_s3

from s3tos3backup.tests.compat import unittest
from s3tos3backup.runner import main
from s3tos3backup.backup import run_backup


class TestRunner(unittest.TestCase):

    def tearDown(self):
        config_file = os.path.join(os.getenv("HOME"), ".s3tos3backup")
        if os.path.exists(config_file):
            os.remove(config_file)

    def test_configure(self):
        with self.assertRaises(SystemExit) as cm:
            main(['--configure'])
        self.assertEqual(cm.exception.code, 0)

    def test_version(self):
        with self.assertRaises(SystemExit) as cm:
            main(['--version'])
        self.assertEqual(cm.exception.code, 0)

    def test_wrong_config(self):
        with self.assertRaises(SystemExit) as cm:
            main(['--config='])
        self.assertEqual(cm.exception.code, 1)

    @patch('s3tos3backup.runner.run_backup')
    def test_no_bucket(self, MockClass):
        with self.assertRaises(SystemExit) as cm:
            main([])
        self.assertEqual(cm.exception.code, 1)
        assert not MockClass.called

    @patch('s3tos3backup.runner.run_backup')
    def test_run(self, MockClass):
        main(['-b src'])
        assert MockClass.called

    @patch('s3tos3backup.backup.copy_bucket')
    @patch('s3tos3backup.backup.remove_old_buckets')
    @mock_s3
    def test_backup_all(self, MockClass1, MockClass2):
        run_backup('src', True, True)
        assert MockClass1.called
        assert MockClass2.called
