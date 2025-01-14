from tkinter import filedialog
import tkinter as tk
import os
import random
import vlc


class Playlist:

    def __init__(self):
        self.player = None
        self.vlc_instance = None
        self.playlist = []  # Initialize an empty playlist
        self.current_index = 0
        self.is_shuffled = False
        self.is_repeating = False

    def load_subtitles(self):
        subtitle_path = filedialog.askopenfilename(filetypes=[("Subtitle files", "*.srt")])
        if subtitle_path:
            self.player.video_set_subtitle_file(subtitle_path)

    def show_playlist(self):
        playlist_window = tk.Toplevel()
        playlist_window.title("Playlist")

        playlist_listbox = tk.Listbox(playlist_window, selectmode=tk.SINGLE)
        playlist_listbox.pack()

        for i, video in enumerate(self.playlist):
            filename, extension = os.path.splitext(os.path.basename(video))
            playlist_listbox.insert(tk.END, f"{i + 1}. {filename} ({extension})")

        def remove_selected():
            selected_index = playlist_listbox.curselection()
            if selected_index:
                removed_video = self.playlist.pop(selected_index[0])
                playlist_listbox.delete(selected_index)

        remove_button = tk.Button(playlist_window, text="Remove Selected Video", command=remove_selected)
        remove_button.pack()

        def load_selected_video():
            selected_index = playlist_listbox.curselection()
            if selected_index:
                self.current_index = selected_index[0]
                self.play_current_video()
                playlist_window.destroy()

        load_button = tk.Button(playlist_window, text="Load Selected Video", command=load_selected_video)
        load_button.pack()

    def add_to_playlist(self):

        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mkv")])
        if file_path:
            self.playlist.append(file_path)

    def shuffle_playlist(self):
        if self.playlist:
            random.shuffle(self.playlist)
            self.is_shuffled = True
            self.current_index = 0
            self.play_current_video()

    def toggle_repeat(self):
        self.is_repeating = not self.is_repeating

    def play_current_video(self):
        if self.playlist:
            media = self.vlc_instance.media_new(self.playlist[self.current_index])
            self.set_aspect_ratio()
            self.set_media_and_play(media)
            if self.is_repeating:
                self.player.event_manager().event_attach(vlc.EventType.MediaPlayerEndReached, self.repeat_video)

    def repeat_video(self, event):
        if self.is_repeating:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            self.play_current_video()
