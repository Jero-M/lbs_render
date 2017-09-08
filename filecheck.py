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
        self.ifd_user = self.get_ifd_user(self.directory)
        self.basename = self.get_basename(self.render_file)
        self.compression = self.get_compression(self.basename)
        self.extension = self.get_extension(self.basename)        
        self.filename = self.get_filename(self.basename)
        self.seq_obj = self.get_seq_object(self.directory, self.basename)
        self.seq_files = [obj.name for obj in self.seq_obj]
        self.is_seq = self.determine_if_seq(self.seq_obj)
        self.filename_head = self.get_filename_head(self.is_seq, self.seq_obj)
        self.seq_length = self.seq_obj.length()
        self.seq_frames = self.get_seq_frames(self.is_seq, self.seq_obj)
        self.start_frame = self.get_start_frame(self.is_seq, self.seq_obj)
        self.end_frame = self.get_end_frame(self.is_seq, self.seq_obj)
        self.seq_padding = self.get_padding(self.is_seq, self.seq_obj)
        
    def get_directory(self, file_path):
        '''Return the path of a files directory'''
        return os.path.dirname(os.path.realpath(file_path))

    def get_ifd_user(self, dir):
        '''Based on the directory of the file, get the name of the user'''
        return dir.split("/")[5]

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

    def get_filename_head(self, is_seq, seq):
        '''Return the string ahead of the sequence number'''
        if is_seq:
            return seq.head()
        else:
            return seq.name.rpartition(".")[0]

    def get_seq_frames(self, is_seq, seq):
        '''Return a list of the frame numbers in the seq'''
        if is_seq:
            return seq.frames()
        else:
            return [1]

    def get_start_frame(self, is_seq, seq):
        '''Return the first frame of the sequence'''
        if is_seq:
            return seq.start()
        else:
            return 1

    def get_end_frame(self, is_seq, seq):
        '''Return the last frame of the sequence'''
        if is_seq:
            return seq.end()
        else:
            return 1

    def get_padding(self, is_seq, seq):
        '''Return the padding of the sequence'''
        if is_seq:
            return seq.format("%p")
        else:
            return 0


if __name__ == "__main__":
    project_path = os.path.dirname(os.path.realpath(__file__))
    test_path = (project_path + "/tests/img_seqs/pig_v002_fxtd.0006.ifd.sc")
    ifd = RenderFile(test_path)
    print "Directory:", ifd.directory
    print "IFD User:", ifd.ifd_user
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