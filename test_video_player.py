# Tests for the Cinefy video player. VLC is replaced by a stand-in (see conftest.py);
# Tk needs a display, so on a server run them with: xvfb-run python -m pytest
import pytest
from unittest.mock import MagicMock
from Functions import VideoPlayer
import tkinter as tk
from unittest.mock import Mock, patch


@pytest.fixture
def mock_video_player():
    master = tk.Tk()
    player = VideoPlayer(master)
    player.player = MagicMock()
    player.vlc_instance = MagicMock()
    player.media = MagicMock()
    yield player
    master.destroy()


def test_load(mock_video_player):
    with patch('tkinter.filedialog.askopenfilename', return_value='test.mp4'), \
            patch('vlc.Instance.media_new') as mock_media_new:
        mock_video_player.vlc_instance.media_new = mock_media_new
        mock_video_player.load()
        mock_media_new.assert_called_once_with('test.mp4')


def test_set_volume(mock_video_player):
    volume = 50
    mock_video_player.set_volume(volume)
    mock_video_player.player.audio_set_volume.assert_called_once_with(int(volume))


def test_set_speed(mock_video_player):
    speed = 1.5
    mock_video_player.set_speed(speed)
    mock_video_player.player.set_rate.assert_called_once_with(float(speed))


def test_play(mock_video_player):
    mock_video_player.play()
    mock_video_player.player.play.assert_called_once()


def test_load_does_nothing_when_the_dialog_is_cancelled(mock_video_player):
    with patch('tkinter.filedialog.askopenfilename', return_value=''):
        mock_video_player.load()
    mock_video_player.vlc_instance.media_new.assert_not_called()


def test_pause(mock_video_player):
    mock_video_player.pause()
    mock_video_player.player.pause.assert_called_once()


def test_stop(mock_video_player):
    mock_video_player.stop()
    mock_video_player.player.stop.assert_called_once()


def test_seek_video(mock_video_player):
    value = 50
    mock_video_player.player.get_length.return_value = 5000
    mock_video_player.seek_video(value)
    mock_video_player.player.set_time.assert_called_once_with(2500)


def test_load_subtitles(mock_video_player):
    with patch('tkinter.filedialog.askopenfilename', return_value='test.srt'):
        mock_video_player.load_subtitles()
        mock_video_player.player.video_set_subtitle_file.assert_called_once_with('test.srt')


def test_add_to_playlist(mock_video_player):
    with patch('tkinter.filedialog.askopenfilename', return_value='test.mp4'):
        mock_video_player.add_to_playlist()
        assert mock_video_player.playlist[-1] == 'test.mp4'


def test_remove_from_playlist(mock_video_player):
    mock_video_player.playlist = ['test1.mp4', 'test2.mp4', 'test3.mp4']
    assert mock_video_player.remove_from_playlist(1) == 'test2.mp4'
    assert mock_video_player.playlist == ['test1.mp4', 'test3.mp4']
    assert mock_video_player.remove_from_playlist(5) is None


def test_removing_an_earlier_video_keeps_the_current_one_selected(mock_video_player):
    mock_video_player.playlist = ['a.mp4', 'b.mp4', 'c.mp4']
    mock_video_player.current_index = 2
    mock_video_player.remove_from_playlist(0)
    assert mock_video_player.playlist[mock_video_player.current_index] == 'c.mp4'


def test_shuffle_playlist(mock_video_player):
    mock_video_player.playlist = ['test1.mp4', 'test2.mp4', 'test3.mp4']
    with patch('random.shuffle'):
        mock_video_player.shuffle_playlist()
        assert mock_video_player.is_shuffled


def test_toggle_repeat(mock_video_player):
    mock_video_player.toggle_repeat()
    assert mock_video_player.is_repeating


def test_play_current_video(mock_video_player):
    mock_video_player.playlist = ['test1.mp4', 'test2.mp4', 'test3.mp4']
    with patch('vlc.Instance.media_new') as mock_media_new:
        mock_video_player.vlc_instance.media_new = mock_media_new
        mock_video_player.play_current_video()
        mock_media_new.assert_called_once_with('test1.mp4')


def test_set_aspect_ratio(mock_video_player):
    mock_video_player.aspect_ratio_var = Mock()
    mock_video_player.aspect_ratio_var.get.return_value = '16:9'
    mock_video_player.set_aspect_ratio()
    mock_video_player.player.video_set_aspect_ratio.assert_called_once_with('16:9')

def test_update_seek_slider(mock_video_player):
    mock_video_player.player.get_length.return_value = 5000
    mock_video_player.player.get_time.return_value = 2500
    mock_video_player.seek_var = MagicMock()
    mock_video_player.master = MagicMock()
    mock_video_player.update_seek_slider()
    mock_video_player.seek_var.set.assert_called_once_with(50)
    mock_video_player.master.after.assert_called_once_with(1000, mock_video_player.update_seek_slider)


def test_seek_slider_stays_at_zero_before_a_video_is_loaded(mock_video_player):
    mock_video_player.player.get_length.return_value = -1
    mock_video_player.player.get_time.return_value = -1
    assert mock_video_player.seek_percentage() == 0


def test_seek_video_accepts_the_slider_text_value(mock_video_player):
    mock_video_player.player.get_length.return_value = 8000
    mock_video_player.seek_video('25')
    mock_video_player.player.set_time.assert_called_once_with(2000)


def test_convert_to_seconds():
    assert VideoPlayer.convert_to_seconds(2500) == 2.5


if __name__ == "__main__":
    pytest.main()
