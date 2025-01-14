import tkinter as tk
import vlc


class VideoPlayer:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        self.vlc_instance = vlc.Instance()
        self.player = self.vlc_instance.media_player_new()
        self.media = None

        # widgets

        self.canvas = tk.Canvas(self.frame, width=640, height=480)
        self.load_button = tk.Button(self.frame, text="Load", command=self.load)
        self.play_button = tk.Button(self.frame, text="Play", command=self.play)
        self.pause_button = tk.Button(self.frame, text="Pause", command=self.pause)
        self.stop_button = tk.Button(self.frame, text="Stop", command=self.stop)
        self.volume_slider = tk.Scale(self.frame, from_=0, to=100, orient='horizontal', command=self.set_volume)
        self.speed_slider = tk.Scale(self.frame, from_=0.5, to=2, resolution=0.1, orient='horizontal',
                                     command=self.set_speed)
        self.subtitle_button = tk.Button(self.master, text="Load Subtitles", command=self.load_subtitles)
        self.show_playlist_button = tk.Button(text="Show Playlist", command=self.show_playlist)
        self.add_to_playlist_button = tk.Button(text="Add to Playlist", command=self.add_to_playlist)
        #self.delete_from_playlist_button = tk.Button(text="Delete from Playlist",
        #                                             command=self.delete_from_playlist)
        self.playlist = []
        self.current_index = 0
        self.is_shuffled = False
        self.is_repeating = False
        self.shuffle_button = tk.Button(text="Shuffle", command=self.shuffle_playlist)
        self.repeat_button = tk.Button(text="Repeat", command=self.toggle_repeat)
        self.aspect_ratio_label = tk.Label(self.frame, text="Aspect Ratio:")
        self.aspect_ratio_var = tk.StringVar()
        self.aspect_ratio_options = ["Original", "16:9", "4:3", "1:1"]
        self.aspect_ratio_menu = tk.OptionMenu(self.frame, self.aspect_ratio_var, *self.aspect_ratio_options)
        self.aspect_ratio_var.set("Original")

        # widget_packs

        self.canvas.pack()
        self.load_button.pack(side="bottom", padx=5, pady=5)
        self.play_button.pack(side='left', padx=5, pady=5)
        self.pause_button.pack(side='left', padx=5, pady=5)
        self.stop_button.pack(side='left', padx=5, pady=5)
        self.volume_slider.pack(side='right')
        self.speed_slider.pack(side='bottom')
        self.subtitle_button.pack(side='left', padx=5, pady=5)
        self.shuffle_button.pack()
        self.repeat_button.pack()
        self.show_playlist_button.pack()
        self.add_to_playlist_button.pack()
        #self.delete_from_playlist_button.pack()
        self.aspect_ratio_label.pack(side='left', padx=5, pady=5)
        self.aspect_ratio_menu.pack(side='left', padx=5, pady=5)
        self.seek_var = tk.DoubleVar()
        self.seek_slider = tk.Scale(self.master, variable=self.seek_var, command=self.seek_video)
        self.seek_slider.pack(side='bottom')
        self.master.after(1000, self.update_seek_slider)
        self.player.set_hwnd(self.canvas.winfo_id())
