#!/usr/bin/python
from collections import deque

def assign_frames_to_clients(clients, frames, name_head, padding, name_tail):
    #Generate a dict with key:frame and value:filename with the correct
    #sequence number
    file_seq = {frame: name_head + str(padding % frame) + name_tail
                for frame in frames}
    #Make a queue from the frames and loop through every client and assign
    #one frame at a time until there are no frames left    
    frames_per_client = {client:[] for client in clients}
    frames_queue = deque(frames)
    for i, frame in enumerate(frames):
        client_id = clients[i % len(clients)]
        frames_per_client[client_id].append(frames_queue.popleft())
    return frames_per_client


def start_process():
    pass


if __name__ == "__main__":
    selected_client_ids = [1,3,4,5]
    frame_seq = range(1, 20)
    name_head = "pig_v001."
    padding = "%04d"
    name_tail = ".ifd"
    print assign_frames_to_clients(selected_client_ids, frame_seq,
                                   name_head, padding, name_tail)