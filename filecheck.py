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
        self.compression = self.get_compression(self.basename)
        self.extension = self.get_extension(self.basename)        
        self.filename = self.get_filename(self.basename)
        self.seq_number = ""
        self.filename_no_seq = ""
        self.padding = ""

    def get_directory(self, file_path):
        '''Return the path of a files directory'''
        return os.path.dirname(os.path.realpath(file_path))

    def get_basename(self, file_path):
        '''Return the basename of a file path. basename = name + extension'''
        return os.path.basename(file_path)

    def get_compression(self, basename):
        '''Return the compression of the basename'''
        compression = basename.rpartition(".")[-1]
        if compression not in self.settings.compression:
            return None
        else:
            return compression

    def get_extension(self, basename):
        '''Return the extension of a basename'''
        if self.compression == None:
            extension = basename.rpartition(".")[-1]
        else:
            extension = basename.split(".")[-2]
        return extension

    def get_filename(self, basename):
        '''Return the file name of a basename.
           Only the name without the extension
        '''
        filename = basename.rpartition(".")[0]
        if self.compression == None:
            return filename
        else:
            return filename.rpartition(".")[0]


if __name__ == "__main__":
    test_path = ("/LOSTBOYS/FX/STUDENTS/FXTD_00X/Name/projects/project_name/"
                 + "renders/render_file_v001.0001.ifd.sc")
    ifd = RenderFile(test_path)
    print "Directory:", ifd.directory
    print "Basename:", ifd.basename
    print "Compression:", ifd.compression
    print "Extension:", ifd.extension
    print "Filename:", ifd.filename

