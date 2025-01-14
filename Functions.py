from tkinter import filedialog
from gui import VideoPlayer
import Playlist


class VideoPlayer(VideoPlayer, Playlist.Playlist):
    def __init__(self, root):
        super().__init__(root)

    def load(self):
        filepath = filedialog.askopenfilename(filetypes=[("Video files", ".mp4;.avi;*.mkv")])
        self.media = self.vlc_instance.media_new(filepath)
        self.player.set_media(self.media)

    def play(self):
        self.player.play()
        self.update_seeker()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def set_volume(self, volume):
        self.player.audio_set_volume(int(volume))

    def set_speed(self, speed):
        self.player.set_rate(float(speed))

    MILLISECONDS_TO_SECONDS = 1000

    def convert_to_seconds(milliseconds, MILLISECONDS_TO_SECONDS=None):
        return milliseconds / MILLISECONDS_TO_SECONDS

    def update_seek_slider(self, MILLISECONDS_TO_SECONDS=None):
        video_length_seconds = self.convert_to_seconds(self.player.get_length())
        video_time_seconds = self.convert_to_seconds(self.player.get_time())
        seek_position_percentage = (video_time_seconds / video_length_seconds) * 100
        self.seek_var.set(seek_position_percentage)
        self.master.after(MILLISECONDS_TO_SECONDS, self.update_seek_slider)

    def calculate_seek_time(self, percentage):

        video_length_ms = self.player.get_length()  # Video length in milliseconds
        seek_time_ms = int((percentage / 100) * video_length_ms)
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
