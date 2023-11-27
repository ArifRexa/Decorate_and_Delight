from django import forms
from accounts.models import CustomUser
from django.forms.widgets import ClearableFileInput

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
)


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    # Override the username field to customize help text
    username = forms.CharField(
        max_length=150,
        help_text='',  # Set an empty string to hide the help text
        # widget=forms.TextInput(attrs={'placeholder': 'Username'}),  # Optional: Add a placeholder to the input field
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'address', 'password',
                  'confirm_password', 'profile_image', 'gender']

    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #     if CustomUser.objects.filter(username=username).exists():
    #         raise forms.ValidationError('This username is already taken.')
    #     return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'address', 'profile_image', 'gender', 'phone_number']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': "block mb-6 px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-900 "
                                                          "bg-transparent rounded-lg border-1 border-gray-300 "
                                                          "appearance-none dark:text-black dark:border-gray-600 "
                                                          "dark:focus:border-blue-500 focus:outline-none focus:ring-0 "
                                                          "focus:border-blue-600 peer"}),

            'last_name': forms.TextInput(attrs={'class': "block px-2.5 mb-6 pb-2.5 pt-4 w-full text-sm text-gray-900 "
                                                         "bg-transparent rounded-lg border-1 border-gray-300 "
                                                         "appearance-none dark:text-black dark:border-gray-600 "
                                                         "dark:focus:border-blue-500 focus:outline-none focus:ring-0 "
                                                         "focus:border-blue-600 peer"}),

            'phone_number': forms.TextInput(
                attrs={'class': "block px-2.5 mb-6 pb-2.5 pt-4 w-full text-sm text-gray-900 "
                                "bg-transparent rounded-lg border-1 border-gray-300 "
                                "appearance-none dark:text-black dark:border-gray-600 "
                                "dark:focus:border-blue-500 focus:outline-none focus:ring-0"
                                "focus:border-blue-600 peer"}),

            'address': forms.TextInput(attrs={'class': "block px-2.5 mb-6 pb-2.5 pt-4 w-full text-sm text-gray-900 "
                                                       "bg-transparent rounded-lg border-1 border-gray-300 "
                                                       "appearance-none dark:text-black dark:border-gray-600 "
                                                       "dark:focus:border-blue-500 focus:outline-none focus:ring-0 "
                                                       "focus:border-blue-600 peer"}),

            'gender': forms.Select(attrs={'class': 'bg-gray-50 border my-5 border-gray-300 text-gray-900 text-sm '
                                                   'rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full '
                                                   'p-2.5 dark:bg-white dark:border-gray-600 '
                                                   'dark:placeholder-gray-400 dark:text-black '
                                                   'dark:focus:ring-blue-500 dark:focus:border-blue-500'}),

            'profile_image': ClearableFileInput(attrs={
                'class': 'block w-full text-lg text-gray-900 border border-gray-300 rounded-lg cursor-pointer '
                         'bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-white '
                         'dark:border-gray-600 dark:placeholder-gray-400',
                'accept': 'image/*',  # Allow only image files
            })
        }
