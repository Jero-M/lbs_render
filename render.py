#!/usr/bin/python
from collections import deque
import subprocess
import sys
import shlex

def map_frames_to_files(frames, name_head, padding, name_tail):
    #Generate a dict with key:frame and value:filename with the correct
    #sequence number
    file_seq = {frame: name_head + str(padding % frame) + name_tail
                for frame in frames}
    return file_seq

def assign_frames_to_clients(clients, frames):
    #Make a queue from the frames and loop through every client and assign
    #one frame at a time until there are no frames left    
    frames_per_client = {client:[] for client in clients}
    frames_queue = deque(frames)
    for i, frame in enumerate(frames):
        client_id = clients[i % len(clients)]
        frames_per_client[client_id].append(frames_queue.popleft())
    return frames_per_client


def start_process(parent_pid, host, client, client_id, render_engine_script,
                  render_engine_path, log_file, render_args,
                  render_files_path, render_files):
    ''' 
    Terminal command:
        gnome-terminal -e 'bash -c "python /LOSTBOYS/FX/STUDENTS/FXTD_008/
        Jeronimo/scripts/ifd_3.0_dev/ifd/mantra.py; exec bash"'

    os.system returns exit code. It does not provide pid of the child process.
    Use subprocess instead.
    shlex.split splits the terminal command into the format required by Popen.
    '''
    cmd_args = [str(parent_pid),
                   host,
                   client,
                   str(client_id),
                   render_engine_path,
                   log_file,
                   render_args,
                   render_files_path,
                   " ".join(render_files)
                  ]
    cmd_args = " ".join(cmd_args)

    terminal_cmd = ("gnome-terminal -e 'bash -c"
                  + " \"{0} {1}; exec bash\"'".format(
                                                        render_engine_script,
                                                        cmd_args))
    p = subprocess.Popen(shlex.split(terminal_cmd), stdout=subprocess.PIPE)
    return p.pid


if __name__ == "__main__":
    selected_client_ids = [1,3,4,5]
    frame_seq = range(1, 20)
    name_head = "pig_v001."
    padding = "%04d"
    name_tail = ".ifd"
    print map_frames_to_files(frame_seq, name_head, padding, name_tail)
    print assign_frames_to_clients(selected_client_ids, frame_seq)