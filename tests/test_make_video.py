import unittest
from unittest.mock import patch, MagicMock
import tempfile
import os

from video_generation.video_maker import make_video


class TestMakeVideo(unittest.TestCase):
    @patch("video_generation.video_maker.VideoFileClip")
    @patch("video_generation.video_maker.concatenate_videoclips")
    @patch("video_generation.video_maker.AudioFileClip")
    @patch("video_generation.video_maker.ImageClip")
    def test_make_video(
        self,
        mock_image_clip,
        mock_audio_file_clip,
        mock_concatenate,
        mock_video_file_clip,
    ):
        # Mock ImageClip
        mock_clip_instance = MagicMock()
        mock_clip_instance.set_duration.return_value.fadein.return_value = (
            mock_clip_instance
        )
        mock_image_clip.return_value = mock_clip_instance

        # Mock AudioFileClip
        mock_audio_file_clip_instance = MagicMock()
        mock_audio_file_clip_instance.duration = 10.0
        mock_audio_file_clip.return_value = mock_audio_file_clip_instance

        # Mock concatenate_videoclips
        mock_video_clip_instance = MagicMock()
        mock_concatenate.return_value = mock_video_clip_instance

        # Mock VideoFileClip
        mock_video_file_clip.return_value = MagicMock()

        # Use a temporary directory
        with tempfile.TemporaryDirectory() as tempdir:
            dir_name = tempdir
            name = "test_video"
            n = 3
            voice_length = 10.0

            # Call the function under test
            result = make_video(n, dir_name, voice_length, name)

            # Assertions
            self.assertEqual(result, f"{dir_name}/{name}.mp4")

            # Verify ImageClip is created for each image
            mock_image_clip.assert_any_call(f"{dir_name}/images/0.png")
            mock_image_clip.assert_any_call(f"{dir_name}/images/1.png")
            mock_image_clip.assert_any_call(f"{dir_name}/images/2.png")
            self.assertEqual(mock_image_clip.call_count, 3)

            # Verify AudioFileClip is created
            mock_audio_file_clip.assert_called_once_with(f"{dir_name}/{name}.mp3")

            # Verify clips are concatenated
            mock_concatenate.assert_called_once()

            # Verify video is written
            mock_video_clip_instance.write_videofile.assert_called_once_with(
                f"{dir_name}/{name}.mp4",
                codec="libx264",
                audio=f"{dir_name}/{name}.mp3",
                fps=24,
                audio_codec="libmp3lame",
                audio_bitrate="160k",
            )


if __name__ == "__main__":
    unittest.main()
