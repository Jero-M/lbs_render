#!/usr/bin/python
import os

import pyseq

import config


class RenderFile(object):
    '''Create a render file object and gather all of its properties'''

    def __init__(self, file_path):
        '''Initialize the file object'''
        self.settings = config.Settings()
        self.render_file = file_path
        self.directory = self.get_directory(self.render_file)
        self.basename = self.get_basename(self.render_file)
        self.compression = self.get_compression(self.basename)
        self.extension = self.get_extension(self.basename)        
        self.filename = self.get_filename(self.basename)
        self.seq_obj = self.get_seq_object(self.directory, self.basename)
        self.seq_files = [obj.name for obj in self.seq_obj]
        self.is_seq = self.determine_if_seq(self.seq_obj)
        self.filename_head = self.seq_obj.head()
        self.seq_length = self.seq_obj.length()
        self.seq_frames = self.seq_obj.frames()
        self.start_frame = self.seq_obj.start()
        self.end_frame = self.seq_obj.end()
        self.seq_padding = self.seq_obj.format("%p")

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

    def get_seq_object(self, path, basename):
        '''Check the directory for sequences and returns a sequence object'''
        dir_contents = pyseq.get_sequences(path)
        for content in dir_contents:
            if content.contains(basename):
                return content
        else:
            return pyseq.Sequence([basename])

    def determine_if_seq(self, seq):
        '''Check if the sequence object is a sequence or a single file'''
        if seq.length() > 1:
            return True
        else:
            return False


if __name__ == "__main__":
    project_path = os.path.dirname(os.path.realpath(__file__))
    test_path = (project_path + "/tests/img_seqs/pig_v001.0002.ifd")
    ifd = RenderFile(test_path)
    print "Directory:", ifd.directory
    print "Basename:", ifd.basename
    print "Compression:", ifd.compression
    print "Extension:", ifd.extension
    print "Filename:", ifd.filename
    print "Sequence Object:", ifd.seq_obj.format("%h%p%t%R")
    print "Is Sequence:", ifd.is_seq
    print "Render items:", ifd.seq_files
    print "Sequence Head:", ifd.filename_head
    print "Sequence Length:", ifd.seq_length
    print "Sequence Frames:", ifd.seq_frames
    print "Start Frame:", ifd.start_frame
    print "End Frame:", ifd.end_frame
    print "Sequence Padding:", ifd.seq_padding