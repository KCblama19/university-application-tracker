from django import forms

from .models import University


class UniversityForm(forms.ModelForm):
    """
    Form used to create and edit universities.
    """

    class Meta:
        model = University
        fields = (
            "name",
            "country",
            "city",
            "website",
            "ranking",
            "description",
            "notes",
        )

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Dalian University of Technology",
                }
            ),
            "country": forms.TextInput(
                attrs={
                    "placeholder": "e.g. China",
                }
            ),
            "city": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Dalian",
                }
            ),
            "website": forms.URLInput(
                attrs={
                    "placeholder": "https://example.com",
                }
            ),
            "ranking": forms.NumberInput(
                attrs={
                    "min": 1,
                    "placeholder": "Optional",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Brief description of the university...",
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Your personal notes...",
                }
            ),
        }

    def clean_name(self):
        """
        Normalize the university name and prevent duplicates
        that differ only by capitalization or whitespace.
        """

        name = " ".join(
            self.cleaned_data["name"].strip().split()
        )

        queryset = University.objects.filter(
            name__iexact=name
        )

        if self.instance.pk:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():
            raise forms.ValidationError(
                "A university with this name already exists."
            )

        return name

    def clean_ranking(self):
        """
        Ensure rankings are positive when provided.
        """

        ranking = self.cleaned_data.get("ranking")

        if ranking is not None and ranking < 1:
            raise forms.ValidationError(
                "Ranking must be greater than zero."
            )

        return ranking
    
from django import forms

from .models import Program, University


class UniversityForm(forms.ModelForm):
    """
    Form used to create and edit universities.
    """

    class Meta:
        model = University
        fields = (
            "name",
            "country",
            "city",
            "website",
            "ranking",
            "description",
            "notes",
        )

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Dalian University of Technology",
                }
            ),
            "country": forms.TextInput(
                attrs={
                    "placeholder": "e.g. China",
                }
            ),
            "city": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Dalian",
                }
            ),
            "website": forms.URLInput(
                attrs={
                    "placeholder": "https://example.com",
                }
            ),
            "ranking": forms.NumberInput(
                attrs={
                    "min": 1,
                    "placeholder": "Optional",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Brief description of the university...",
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Your personal notes...",
                }
            ),
        }

    def clean_name(self):
        """
        Normalize the university name and prevent duplicates
        that differ only by capitalization or whitespace.
        """

        name = " ".join(
            self.cleaned_data["name"].strip().split()
        )

        queryset = University.objects.filter(
            name__iexact=name
        )

        if self.instance.pk:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():
            raise forms.ValidationError(
                "A university with this name already exists."
            )

        return name

    def clean_ranking(self):
        """
        Ensure rankings are positive when provided.
        """

        ranking = self.cleaned_data.get("ranking")

        if ranking is not None and ranking < 1:
            raise forms.ValidationError(
                "Ranking must be greater than zero."
            )

        return ranking


class ProgramForm(forms.ModelForm):
    """
    Form used to create and edit an academic program.
    """

    class Meta:
        model = Program
        fields = (
            "name",
            "degree_type",
            "study_language",
            "duration",
            "tuition_fee",
            "description",
            "requirements",
        )

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Software Engineering",
                }
            ),
            "duration": forms.NumberInput(
                attrs={
                    "min": 0,
                    "step": "0.1",
                    "placeholder": "e.g. 2.5",
                }
            ),
            "tuition_fee": forms.NumberInput(
                attrs={
                    "min": 0,
                    "step": "0.01",
                    "placeholder": "Annual tuition fee",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Program description...",
                }
            ),
            "requirements": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Admission requirements...",
                }
            ),
        }

    def __init__(self, *args, university=None, **kwargs):
        """
        Accept the university explicitly so that the form can
        associate a new program with the correct university.
        """

        super().__init__(*args, **kwargs)

        self.university = university

    def save(self, commit=True):
        """
        Automatically associate a new program with the
        university provided to the form.
        """

        program = super().save(commit=False)

        if self.university is not None:
            program.university = self.university

        if commit:
            program.save()

        return program