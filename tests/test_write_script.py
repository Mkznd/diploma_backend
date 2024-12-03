import unittest
from unittest.mock import patch, mock_open
import tempfile
import os

from video_generation.write_script import write_script


class TestWriteScript(unittest.TestCase):
    @patch("video_generation.write_script.generate_script")
    @patch("builtins.open", new_callable=mock_open)
    def test_write_script(self, mock_open_func, mock_generate_script):
        # Mock generate_script
        mock_generate_script.return_value = "Generated script [note]"

        # Use a temporary directory
        with tempfile.TemporaryDirectory() as tempdir:
            dir_name = tempdir
            name = "test_script"
            topic = "test_topic"
            length = 100

            # Call the function under test
            result = write_script(topic, length, name, dir_name)

            # Assertions
            self.assertEqual(result, "Generated script ")
            mock_generate_script.assert_called_once_with(topic, length)

            # Check file writing
            mock_open_func.assert_called_once_with(f"{dir_name}/{name}.txt", "w")
            mock_open_func().write.assert_called_once_with("Generated script ")


if __name__ == "__main__":
    unittest.main()
