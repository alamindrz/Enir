from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ShortVideo
from .forms import ShortVideoForm
from django.contrib import messages

@login_required
def upload_video(request):
    if request.method == 'POST':
        form = ShortVideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user
            video.save()
            messages.success(request, "Video uploaded successfully!")
            return redirect('posts:video_list')  
        else:
            messages.error(request, "There was an error with your submission.")
    else:
        form = ShortVideoForm()

    return render(request, 'videos/upload_video.html', {'form': form})


@login_required
def delete_video(request, pk):
    short_video = get_object_or_404(ShortVideo, pk=pk)

    if request.method == 'POST':
        short_video.delete()
        messages.success(request, 'Short video deleted successfully.')
        return redirect('posts:video_list')  # Redirect to the video list page

    return render(request, 'videos/delete_confirm.html', {'short_video': short_video})

@login_required
def video_list(request):
    videos = ShortVideo.objects.all().order_by('-created_at')
    return render(request, 'videos/video_list.html', {'videos': videos})