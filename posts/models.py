from django.db import models
from django.conf import settings
# from moviepy.video.io.VideoFileClip import VideoFileClip
import os

class ShortVideo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    video = models.FileField(upload_to='videos/')
    created_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        # Delete the file from storage
        if self.video:
            if os.path.isfile(self.video.path):
                os.remove(self.video.path)
        # Call the parent class's delete method
        super().delete(*args, **kwargs)



    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    #     # Validate and trim video
    #     video_path = self.video.path
    #     with VideoFileClip(video_path) as clip:
    #         if clip.duration > 300:  # 5 minutes = 300 seconds
    #             # Trim the video to the first 5 minutes
    #             trimmed_clip = clip.subclip(0, 300)
    #             trimmed_clip.write_videofile(video_path, codec="libx264")
    #             trimmed_clip.close()