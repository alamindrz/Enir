from django import forms
from .models import ShortVideo



class ShortVideoForm(forms.ModelForm):
    class Meta:
        model = ShortVideo
        fields = ['title', 'description', 'video']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control w-full md:w-2/3 p-2 border border-gray-300 rounded',
                'placeholder': 'Enter video title',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control w-full md:w-2/3 p-2 border border-gray-300 rounded',
                'rows': 4,  # Reduces the height of the text area
                'placeholder': 'Enter video description',
            }),
            'video': forms.ClearableFileInput(attrs={
                'class': 'form-control-file w-full md:w-2/3 p-2 border border-gray-300 rounded',
            }),
        }

    def clean_video(self):
        video = self.cleaned_data.get('video')

        # Validate video size and format (optional)
        if video.size > 50 * 1024 * 1024:  # 50MB limit
            raise forms.ValidationError("Video file is too large. Maximum size allowed is 50MB.")

        if not video.name.endswith(('.mp4', '.mov', '.avi', '.mkv')):
            raise forms.ValidationError("Unsupported video format. Allowed formats: mp4, mov, avi, mkv.")

        return video