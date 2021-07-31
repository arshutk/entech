from django import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.core.files.uploadedfile import UploadedFile
from django.db.models.fields.files import ImageFieldFile
from django.conf import settings

from .models import (Post, Comment, Vote)

class PostForm(forms.ModelForm):
    
    def clean_cover_img(self):
        content = self.cleaned_data['cover_img']

        if content and isinstance(content, UploadedFile):
            content_type = content.content_type.split('/')[0]
            if content_type in settings.CONTENT_TYPES:
                if content.size > settings.MAX_UPLOAD_SIZE:
                    raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(content.size)))
            else:
                raise forms.ValidationError(_('File type is not supported'))
        
        elif content and isinstance(content, ImageFieldFile):
            pass

        return content
        

    class Meta:
        model = Post
        exclude = ('written_by', 'slug', 'status')


class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        exclude = ('voter', 'post')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('post', 'comment', 'written_by')