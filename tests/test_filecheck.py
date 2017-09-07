#!/usr/bin/python
import unittest
import sys
import os

test_dir = (os.path.dirname(os.path.realpath(__file__)) + "/img_seqs")
project_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, project_path)

from filecheck import RenderFile
import config

test_files = ["/pig_v001.0001.ifd.gz",
              "/pig_v001.0002.ifd",
              "/pig_v001_0006.ifd",
              "/pig_v002_fxtd.0006.ifd.sc",
              "/pig_v002_fxtd.0006.ifd",
              "/pig_v003_0001.ifd",
             ]

class TestRenderFileCheck(unittest.TestCase):
    '''Tests for the filecheck.RenderFile class'''

    def setUp(self):
        '''Create a RenderFile object from the test file'''
        self.case1 = RenderFile(test_dir + test_files[0])
        self.case2 = RenderFile(test_dir + test_files[1])
        self.case3 = RenderFile(test_dir + test_files[2])
        self.case4 = RenderFile(test_dir + test_files[3])
        self.case5 = RenderFile(test_dir + test_files[4])
        self.case6 = RenderFile(test_dir + test_files[5])

    def test_directory(self):
        '''Test the directory attribute matches the test file dir'''
        self.assertEqual(test_dir, self.case1.directory)

    # def test_get_directory(self):
    #     '''Test get directory method matches the test file dir'''
    #     compare_dir = str("/lbs/staff/hip/FXTD_00X/Name/projects/project_name"
    #                     + "/renders")
    #     self.assertEqual(compare_dir, self.ifd.get_directory(self.test_file))

    # def test_basename(self):
    #     '''Test the basename attribute matches the test file basename'''
    #     compare_basename = "render_file_v001.0001.ifd.sc"
    #     self.assertEqual(compare_basename, self.ifd.basename)

    # def test_get_basename(self):
    #     '''Test get basename method matches the test path dir'''
    #     compare_basename = "render_file_v001.0001.ifd.sc"
    #     self.assertEqual(compare_basename, self.ifd.get_basename(
    #                                                           self.test_file))

    


unittest.main()