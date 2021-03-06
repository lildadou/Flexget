from __future__ import unicode_literals, division, absolute_import
import os

from tests import FlexGetBase, build_parser_function, use_vcr
from tests.util import maketemp


class BaseExistsMovie(FlexGetBase):

    __yaml__ = """
        tasks:
          test_dirs:
            mock:
              - {title: 'Existence.2012'}
              - {title: 'The.Missing.2014'}
            accept_all: yes
            exists_movie:
              path: autogenerated in setup()

          test_files:
            mock:
              - {title: 'Duplicity.2009'}
              - {title: 'Downloaded.2013'}
              - {title: 'Gone.Missing.2013'}
            accept_all: yes
            exists_movie:
              path: autogenerated in setup()
              type: files

          test_lookup_imdb:
            mock:
              - {title: 'Existence.2012'}
              - {title: 'The.Matrix.1999'}
            accept_all: yes
            exists_movie:
              path: autogenerated in setup()
              lookup: imdb

          test_diff_qualities_allowed:
            mock:
              - {title: 'Quality.of.Life.480p'}
            accept_all: yes
            exists_movie:
              path:  path autogenerated in setup()
              allow_different_qualities: yes

          test_diff_qualities_not_allowed:
            mock:
              - {title: 'Quality.of.Life.1080p'}
            accept_all: yes
            exists_movie: path autogenerated in setup()

          test_diff_qualities_downgrade:
            mock:
              - {title: 'Quality.of.Life.480p'}
            accept_all: yes
            exists_movie:
              path:  path autogenerated in setup()
              allow_different_qualities: better

          test_diff_qualities_upgrade:
            mock:
              - {title: 'Quality.of.Life.1080p'}
            accept_all: yes
            exists_movie:
              path:  path autogenerated in setup()
              allow_different_qualities: better

          test_propers:
            mock:
              - {title: 'Mock.S01E01.Proper'}
              - {title: 'Test.S01E01'}
            accept_all: yes
            exists_movie: path autogenerated in setup()

          test_invalid:
            mock:
              - {title: 'Invalid.S01E01'}
            accept_all: yes
            exists_movie: path autogenerated in setup()
    """

    test_files = [ 'Downloaded.2013.mkv', 'Invalid.jpg' ]
    test_dirs = [ 'Existence.2012', 'Quality.of.Life.720p', 'Subs']

    def __init__(self):
        self.test_home = None
        FlexGetBase.__init__(self)

    def setup(self):
        FlexGetBase.setup(self)
        # generate config
        self.test_home = maketemp()
        for task_name in self.manager.config['tasks'].iterkeys():
            if isinstance(self.manager.config['tasks'][task_name]['exists_movie'], dict):
                self.manager.config['tasks'][task_name]['exists_movie']['path'] = self.test_home
            else:
                self.manager.config['tasks'][task_name]['exists_movie'] = self.test_home
        # create test dirs
        for test_dir in self.test_dirs:
            os.makedirs(os.path.join(self.test_home, test_dir))
        # create test files
        for test_file in self.test_files:
            open(os.path.join(self.test_home, test_file), 'a').close()

    def teardown(self):
        curdir = os.getcwd()
        os.chdir(self.test_home)
        for test_dir in self.test_dirs:
            os.removedirs(test_dir)
        for test_file in self.test_files:
            os.remove(test_file)
        os.chdir(curdir)
        os.rmdir(self.test_home)
        FlexGetBase.teardown(self)

    def test_existing_dirs(self):
        """exists_movie plugin: existing"""
        self.execute_task('test_dirs')
        assert not self.task.find_entry('accepted', title='Existence.2012'), \
            'Existence.2012 should not have been accepted (exists)'
        assert self.task.find_entry('accepted', title='The.Missing.2014'), \
            'The.Missing.2014 should have been accepted'

    def test_existing_files(self):
        """exists_movie plugin: existing"""
        self.execute_task('test_files')
        assert not self.task.find_entry('accepted', title='Downloaded.2013'), \
            'Downloaded.2013 should not have been accepted (exists)'
        assert self.task.find_entry('accepted', title='Gone.Missing.2013'), \
            'Gone.Missing.2013 should have been accepted'

    @use_vcr
    def test_lookup_imdb(self):
        """exists_movie plugin: existing"""
        self.execute_task('test_lookup_imdb')
        assert self.task.find_entry('accepted', title='The.Matrix.1999')['imdb_id'], \
            'The.Matrix.1999 should have an `imdb_id`'
        assert not self.task.find_entry('accepted', title='Existence.2012'), \
            'Existence.2012 should not have been accepted (exists)'

    def test_diff_qualities_allowed(self):
        """exists_movie plugin: existsting but w. diff quality"""
        self.execute_task('test_diff_qualities_allowed')
        assert self.task.find_entry('accepted', title='Quality.of.Life.480p'), \
            'Quality.of.Life.480p should have been accepted'

    def test_diff_qualities_not_allowed(self):
        """exists_movie plugin: existsting but w. diff quality"""
        self.execute_task('test_diff_qualities_not_allowed')
        assert self.task.find_entry('rejected', title='Quality.of.Life.1080p'), \
            'Quality.of.Life.1080p should have been rejected'

    def test_diff_qualities_downgrade(self):
        """Test worse qualities than exist are rejected."""
        self.execute_task('test_diff_qualities_downgrade')
        assert self.task.find_entry('rejected', title='Quality.of.Life.480p'), \
            'Quality.of.Life.480p should have been rejected'

    def test_diff_qualities_upgrade(self):
        """Test better qualities than exist are accepted."""
        self.execute_task('test_diff_qualities_upgrade')
        assert self.task.find_entry('accepted', title='Quality.of.Life.1080p'), \
            'Quality.of.Life.1080p should have been accepted'

'''
    def test_propers(self):
        """exists_movie plugin: new proper & proper already exists"""
        self.execute_task('test_propers')
        assert self.task.find_entry('accepted', title='Mock.S01E01.Proper'), \
            'new proper not accepted'
        assert self.task.find_entry('rejected', title='Test.S01E01'), \
            'pre-existin proper should have caused reject'

    def test_invalid(self):
        """exists_movie plugin: no episode numbering on the disk"""
        # shouldn't raise anything
        self.execute_task('test_invalid')

    def test_with_metainfo_series(self):
        """Tests that exists_movie works with series data from metainfo_series"""
        self.execute_task('test_with_metainfo_series')
        assert self.task.find_entry('rejected', title='Foo.Bar.S01E02.XViD'), \
            'Foo.Bar.S01E02.XViD should have been rejected(exists)'
        assert not self.task.find_entry('rejected', title='Foo.Bar.S01E03.XViD'), \
            'Foo.Bar.S01E03.XViD should not have been rejected'
'''

class TestGuessitExistsMovie(BaseExistsMovie):
    def __init__(self):
        super(TestGuessitExistsMovie, self).__init__()
        self.add_tasks_function(build_parser_function('guessit'))


class TestInternalExistsMovie(BaseExistsMovie):
    def __init__(self):
        super(TestInternalExistsMovie, self).__init__()
        self.add_tasks_function(build_parser_function('internal'))
