from tkinter import filedialog

from gui import VideoPlayer
import Playlist


class VideoPlayer(VideoPlayer, Playlist.Playlist):
    def __init__(self, root):
        super().__init__(root)

    def load(self):
        filepath = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mkv")])
        if not filepath:  # the dialog was cancelled
            return
        self.media = self.vlc_instance.media_new(filepath)
        self.player.set_media(self.media)

    def play(self):
        # The seek slider is already refreshed every second (see update_seek_slider).
        self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def set_volume(self, volume):
        self.player.audio_set_volume(int(volume))

    def set_speed(self, speed):
        self.player.set_rate(float(speed))

    MILLISECONDS_PER_SECOND = 1000
    SLIDER_REFRESH_MS = 1000

    @staticmethod
    def convert_to_seconds(milliseconds):
        return milliseconds / VideoPlayer.MILLISECONDS_PER_SECOND

    def seek_percentage(self):
        """How far through the video we are, from 0 to 100. 0 when nothing is loaded."""
        length = self.player.get_length()  # -1 or 0 when no media is loaded
        position = self.player.get_time()
        if not length or length <= 0 or position is None or position < 0:
            return 0
        return min(100, (position / length) * 100)

    def update_seek_slider(self):
        self.seek_var.set(self.seek_percentage())
        self.master.after(self.SLIDER_REFRESH_MS, self.update_seek_slider)

    def calculate_seek_time(self, percentage):
        video_length_ms = self.player.get_length()  # Video length in milliseconds
        if not video_length_ms or video_length_ms <= 0:
            return 0
        seek_time_ms = int((float(percentage) / 100) * video_length_ms)
        return seek_time_ms

    def seek_video(self, percentage):

        seek_time_ms = self.calculate_seek_time(percentage)
        self.player.set_time(seek_time_ms)

    def get_aspect_ratio_value(self, aspect_ratio):
        aspect_ratios = {
            "16:9": "16:9",
            "4:3": "4:3",
            "1:1": "1:1"
        }
        return aspect_ratios.get(aspect_ratio)

    def set_aspect_ratio(self):
        selected_aspect_ratio = self.aspect_ratio_var.get()
        aspect_ratio_value = self.get_aspect_ratio_value(selected_aspect_ratio)
        self.player.video_set_aspect_ratio(aspect_ratio_value or None)

    def set_media_and_play(self, media):
        self.player.set_media(media)
        self.player.play()
