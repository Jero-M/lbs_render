#!/usr/bin/python
import unittest
import sys
import os

test_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, test_path)

from filecheck import RenderFile
import config

class TestRenderFileCheck(unittest.TestCase):
    '''Tests for the filecheck.RenderFile class'''

    def setUp(self):
        '''Create a RenderFile object from the test file'''
        self.test_file = str("/lbs/staff/hip/FXTD_00X/Name/projects/"
                        + "project_name/renders/render_file_v001.0001.ifd.sc")
        self.ifd = RenderFile(self.test_file)

    def test_directory(self):
        '''Test the directory attribute matches the test file dir'''
        compare_dir = str("/lbs/staff/hip/FXTD_00X/Name/projects/project_name"
                        + "/renders")
        self.assertEqual(compare_dir, self.ifd.directory)

    def test_get_directory(self):
        '''Test get directory method matches the test file dir'''
        compare_dir = str("/lbs/staff/hip/FXTD_00X/Name/projects/project_name"
                        + "/renders")
        self.assertEqual(compare_dir, self.ifd.get_directory(self.test_file))

    def test_basename(self):
        '''Test the basename attribute matches the test file basename'''
        compare_basename = "render_file_v001.0001.ifd.sc"
        self.assertEqual(compare_basename, self.ifd.basename)

    def test_get_basename(self):
        '''Test get basename method matches the test path dir'''
        compare_basename = "render_file_v001.0001.ifd.sc"
        self.assertEqual(compare_basename, self.ifd.get_basename(
                                                              self.test_file))

    


unittest.main()