from __future__ import unicode_literals, absolute_import
from s3tos3backup.tests.compat import unittest
from s3tos3backup.copy import copy_bucket
from s3tos3backup.remove import remove_old_buckets
from moto import mock_s3
import boto


class TestOperations(unittest.TestCase):

    def _create_defaults(self, bucket_name='src'):
        self.connection = boto.connect_s3()
        self.connection.create_bucket(bucket_name)
        bucket = self.connection.get_bucket(bucket_name)
        for x in xrange(2):
            print 'key', 'foo-%d' % x
            key = bucket.new_key('foo-%d' % x)
            key.set_contents_from_string(x)
            key.set_acl('public-read')

    @mock_s3
    def test_copy(self):
        self._create_defaults()
        copy_bucket(self.connection, 'src', 'src-copy')

        # test 2nd copy errors
        copy_bucket(self.connection, 'src', 'src-copy')

        # test not implemented copy to path
        self.assertRaises(ValueError, copy_bucket, connection=self.connection, src='src', dst='src-copy/foo')

    @mock_s3
    def test_remove(self):
        self._create_defaults('src-backup-2012-01-01')
        remove_old_buckets(self.connection, 'src')
