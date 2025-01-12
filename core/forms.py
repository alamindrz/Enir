from django import forms
from django.contrib.auth.models import User
from .models import Profile


class SignupForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        required=True
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput,
        required=True
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        help_text="",  # Remove the default help text
    )
    first_name = forms.CharField(
        max_length=150,
        required=True,
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        """Ensure email is unique."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean(self):
        """Ensure password1 and password2 match."""
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields must match.")

        return cleaned_data

    def save(self, commit=True):
        """Save user with hashed password."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user



class ProfileEditForm(forms.ModelForm):
    # Adding first name and last name fields to edit
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = Profile
        fields = ['bio',
        'profile_picture',
        'street_address', 
        'city',
        'state',
        'postal_code',
        'country',
        'latitude',
        'longitude',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add first_name and last_name to the form's fields dynamically
        if self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, commit=True):
        # Save the user fields as well as the profile fields
        profile = super().save(commit=False)
        if self.cleaned_data['first_name']:
            profile.user.first_name = self.cleaned_data['first_name']
        if self.cleaned_data['last_name']:
            profile.user.last_name = self.cleaned_data['last_name']
        
        if commit:
            profile.user.save()  # Save the user instance
            profile.save()  # Save the profile instance
        return profile