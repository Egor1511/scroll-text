import os
import uuid

import cv2
import numpy as np
import transliterate
from django.conf import settings


class ScrollingTextVideoGenerator:
    def __init__(self, text: str, duration: int, size: tuple[int, int],
                 fps: int, text_color: tuple[int, int, int],
                 background_color: tuple[int, int, int]):
        """
        Initialize the ScrollingTextVideoGenerator.

        :param text: The text to be scrolled in the video.
        :param duration: The duration of the video in seconds.
        :param size: A tuple representing the size of the video (width, height).
        :param fps: Frames per second for the video.
        :param text_color: A tuple representing the color of the text (B, G, R).
        :param background_color: A tuple representing the background color (B, G, R).
        """
        self.text = text
        self.duration = duration
        self.width, self.height = size
        self.fps = fps
        self.text_color = text_color
        self.background_color = background_color
        self.mp4_name = self._generate_filename()

    def _generate_filename(self):
        """
        Generate a unique filename for the video file based on the text and a unique identifier.

        :return: A string representing the generated filename.
        """
        slugged_text = transliterate.slugify(
            self.text[:10] if len(self.text) > 10 else self.text, 'ru')
        unique_id = uuid.uuid4().hex[:6]
        return f'{slugged_text}-{unique_id}.mp4'

    def _calculate_parameters(self):
        """
        Calculate the parameters required for video generation, such as number of frames, font scale, text size, etc.
        """
        self.num_frames = self.duration * self.fps
        self.font_scale = 1
        self.font_thickness = 2
        self.text_size = \
        cv2.getTextSize(self.text, cv2.FONT_HERSHEY_COMPLEX, self.font_scale,
                        self.font_thickness)[0]
        self.text_x = self.width
        self.text_y = self.height // 2 + self.text_size[1] // 2
        self.total_distance = self.width + self.text_size[0]
        self.speed = self.total_distance / self.num_frames

    def _create_video_writer(self, filepath):
        """
        Create a video writer object to write the video frames.

        :param filepath: The path where the video file will be saved.
        :return: A cv2.VideoWriter object.
        """
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        return cv2.VideoWriter(filepath, fourcc, self.fps,
                               (self.width, self.height))

    def _generate_frame(self, text_x):
        """
        Generate a single frame for the video with the scrolling text.

        :param text_x: The x-coordinate position of the text in the frame.
        :return: A numpy array representing the frame image.
        """
        frame_img = np.full((self.height, self.width, 3),
                            self.background_color, dtype=np.uint8)
        cv2.putText(frame_img, self.text, (int(text_x), self.text_y),
                    cv2.FONT_HERSHEY_COMPLEX, self.font_scale, self.text_color,
                    self.font_thickness, cv2.LINE_AA)
        return frame_img

    def create_video(self):
        """
        Create the video with scrolling text and save it to the specified path.

        :return: The path to the saved video file.
        """
        self._calculate_parameters()
        video_directory = os.path.join(settings.MEDIA_ROOT, 'video', 'videos')
        os.makedirs(video_directory, exist_ok=True)
        video_path = os.path.join(video_directory, self.mp4_name)

        video = self._create_video_writer(video_path)
        text_x = self.text_x

        for frame in range(self.num_frames):
            frame_img = self._generate_frame(text_x)
            text_x -= self.speed
            video.write(frame_img)

        video.release()
        return video_path
