from django import forms


from .models import CustomUser, Profile, Contact


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput, required=True)
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"required": "required"}))
    date_of_birth = forms.DateField(label='Date of Birth', widget=forms.DateInput(attrs={"required": "required", "type": "date"}))

    class Meta:
        model = CustomUser
        fields = ("username", "email", "date_of_birth")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(max_length=200,widget=forms.FileInput())

    class Meta:
        model = Profile
        fields = ['avatar']


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'address', 'phone_number', 'email', 'birthday']
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'})
        }

