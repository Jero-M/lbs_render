#!/usr/bin/python
import os
import getpass
import sys

import config


class RenderFile(object):
    '''Create a render file object and check all of its properties'''

    def __init__(self, file_path):
        '''Initialize the file object'''
        self.settings = config.Settings()
        self.render_file = file_path
        self.directory = self.get_directory(self.render_file)
        self.basename = self.get_basename(self.render_file)
        self.compression = ""
        self.filename = ""
        self.extension = ""
        self.seq_partition = ""
        self.filename_no_seq = ""
        self.padding = ""
        self.seq_number = ""

    def get_directory(self, file_path):
        '''Return the path of a files directory'''
        return os.path.dirname(os.path.realpath(file_path))

    def get_basename(self, file_path):
        '''Return the basename of a file path. basename = name + extension'''
        return os.path.basename(file_path)

    def get_compression(self, basename):
        '''Return the compression of the basename'''
        compression = basename.rpartition(".")[-1]
        if compression == 

    def get_filename(self, basename):
        #Return the file name of a basename. Only the name without the extension
        return basename.rpartition(".")[0]

    def get_extension(self, basename):
        #Return the extension of a basename
        return basename.rpartition(".")[-1]


if __name__ == "__main__":
    test_path = ("/lbs/staff/hip/FXTD_00X/Name/projects/project_name/renders/"
                + "render_file_v001.0001.ifd.sc")
    ifd = RenderFile(test_path)
    directory = ifd.directory
    basename = ifd.basename
    filename = ifd.filename
    print directory
    #test