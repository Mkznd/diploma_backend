import unittest
from unittest.mock import patch, MagicMock
import tempfile
import os

from video_generation.images import generate_and_write_images_and_thumbnail


class TestImageGeneration(unittest.TestCase):
    @patch("video_generation.images.generate_images")
    @patch("requests.get")
    def test_generate_and_write_images_and_thumbnail(
        self, mock_requests_get, mock_generate_images
    ):
        # Mock dependencies
        mock_generate_images.return_value = ["url1", "url2", "url3"]
        mock_requests_get.return_value.content = b"fake_image_data"

        # Use a temporary directory
        with tempfile.TemporaryDirectory() as tempdir:
            dir_name = tempdir

            # Call the function under test
            result = generate_and_write_images_and_thumbnail("test_script", 1, dir_name)

            # Assert results
            self.assertEqual(result, 3)
            mock_generate_images.assert_called_once_with("test_script", 3)
            self.assertEqual(mock_requests_get.call_count, 3)

            # Verify directory structure
            images_dir = os.path.join(dir_name, "images")
            self.assertTrue(os.path.isdir(images_dir))

            # Check if the image files were "written"
            written_files = os.listdir(images_dir)
            self.assertEqual(len(written_files), 3)
            for i in range(3):
                with open(os.path.join(images_dir, f"{i}.png"), "rb") as f:
                    self.assertEqual(f.read(), b"fake_image_data")

            # Assert requests.get was called with the correct URLs
            expected_urls = ["url1", "url2", "url3"]
            actual_urls = [call.args[0] for call in mock_requests_get.call_args_list]
            self.assertEqual(actual_urls, expected_urls)

    @patch("video_generation.images.generate_images")
    @patch("requests.get")
    def test_empty_generate_images(self, mock_requests_get, mock_generate_images):
        # Mock dependencies
        mock_generate_images.return_value = []  # Simulate no images generated
        mock_requests_get.return_value.content = b"fake_image_data"

        with tempfile.TemporaryDirectory() as tempdir:
            dir_name = tempdir

            # Call the function under test
            result = generate_and_write_images_and_thumbnail("test_script", 1, dir_name)

            # Assert results
            self.assertEqual(result, 0)  # No images generated
            mock_generate_images.assert_called_once_with("test_script", 3)
            self.assertEqual(mock_requests_get.call_count, 0)  # No requests made

            # Verify images directory is created but empty
            images_dir = os.path.join(dir_name, "images")
            self.assertTrue(os.path.isdir(images_dir))
            self.assertEqual(len(os.listdir(images_dir)), 0)  # No files written
