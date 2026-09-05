from decimal import Decimal

from django.test import TestCase

from apps.universities.forms import ProgramForm, UniversityForm
from apps.universities.models import Program, University


class UniversityFormTests(TestCase):
    """Tests for the UniversityForm."""

    def test_valid_university_form(self):
        """Valid university data produces a valid form."""
        form = UniversityForm(
            data={
                "name": "Dalian University of Technology",
                "country": "China",
                "city": "Dalian",
                "website": "https://www.dlut.edu.cn/",
                "ranking": 25,
                "description": "A university in Dalian.",
                "notes": "Consider for application.",
            }
        )

        self.assertTrue(form.is_valid())

    def test_university_name_is_normalized(self):
        """Extra whitespace is removed from the university name."""
        form = UniversityForm(
            data={
                "name": "  Dalian   University of Technology  ",
                "country": "China",
                "city": "Dalian",
                "website": "",
                "ranking": "",
                "description": "",
                "notes": "",
            }
        )

        self.assertTrue(form.is_valid())

        self.assertEqual(
            form.cleaned_data["name"],
            "Dalian University of Technology",
        )

    def test_duplicate_university_name_is_rejected_case_insensitively(self):
        """A university cannot be duplicated using different capitalization."""
        University.objects.create(
            name="Dalian University of Technology",
        )

        form = UniversityForm(
            data={
                "name": "DALIAN UNIVERSITY OF TECHNOLOGY",
                "country": "China",
                "city": "Dalian",
                "website": "",
                "ranking": "",
                "description": "",
                "notes": "",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_duplicate_university_name_with_extra_spaces_is_rejected(self):
        """Whitespace differences do not bypass duplicate validation."""
        University.objects.create(
            name="Dalian University of Technology",
        )

        form = UniversityForm(
            data={
                "name": "  Dalian   University   of   Technology ",
                "country": "China",
                "city": "Dalian",
                "website": "",
                "ranking": "",
                "description": "",
                "notes": "",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_ranking_must_be_positive(self):
        """A ranking below one is rejected."""
        form = UniversityForm(
            data={
                "name": "Test University",
                "country": "China",
                "city": "",
                "website": "",
                "ranking": 0,
                "description": "",
                "notes": "",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("ranking", form.errors)

    def test_empty_ranking_is_allowed(self):
        """Ranking can be omitted because it is optional."""
        form = UniversityForm(
            data={
                "name": "Test University",
                "country": "China",
                "city": "",
                "website": "",
                "ranking": "",
                "description": "",
                "notes": "",
            }
        )

        self.assertTrue(form.is_valid())

    def test_updating_same_university_does_not_trigger_duplicate_error(self):
        """A university can be edited without conflicting with itself."""
        university = University.objects.create(
            name="Dalian University of Technology",
        )

        form = UniversityForm(
            data={
                "name": "Dalian University of Technology",
                "country": "China",
                "city": "Dalian",
                "website": "",
                "ranking": "",
                "description": "",
                "notes": "",
            },
            instance=university,
        )

        self.assertTrue(form.is_valid())


class ProgramFormTests(TestCase):
    """Tests for the ProgramForm."""

    def setUp(self):
        self.university = University.objects.create(
            name="Dalian University of Technology",
        )

    def test_valid_program_form(self):
        """Valid program data produces a valid form."""
        form = ProgramForm(
            data={
                "name": "Software Engineering",
                "degree_type": Program.DegreeType.MASTER,
                "study_language": Program.StudyLanguage.ENGLISH,
                "duration": "2.5",
                "tuition_fee": "30000.00",
                "description": "Master's program.",
                "requirements": "Bachelor's degree required.",
            },
            university=self.university,
        )

        self.assertTrue(form.is_valid())

    def test_program_is_assigned_to_university_on_save(self):
        """Saving a program form associates it with the supplied university."""
        form = ProgramForm(
            data={
                "name": "Software Engineering",
                "degree_type": Program.DegreeType.MASTER,
                "study_language": Program.StudyLanguage.ENGLISH,
                "duration": "2.5",
                "tuition_fee": "30000.00",
                "description": "",
                "requirements": "",
            },
            university=self.university,
        )

        self.assertTrue(form.is_valid())

        program = form.save()

        self.assertEqual(
            program.university,
            self.university,
        )

    def test_program_can_be_saved_without_immediate_database_write(self):
        """commit=False returns an unsaved program with its university assigned."""
        form = ProgramForm(
            data={
                "name": "Software Engineering",
                "degree_type": Program.DegreeType.MASTER,
                "study_language": Program.StudyLanguage.ENGLISH,
                "duration": "2.5",
                "tuition_fee": "30000.00",
                "description": "",
                "requirements": "",
            },
            university=self.university,
        )

        self.assertTrue(form.is_valid())

        program = form.save(commit=False)

        self.assertIsNone(program.pk)
        self.assertEqual(
            program.university,
            self.university,
        )

    def test_program_form_without_university_does_not_assign_one(self):
        """The form does not invent a university when none is supplied."""
        form = ProgramForm(
            data={
                "name": "Software Engineering",
                "degree_type": Program.DegreeType.MASTER,
                "study_language": Program.StudyLanguage.ENGLISH,
                "duration": "2.5",
                "tuition_fee": "30000.00",
                "description": "",
                "requirements": "",
            }
        )

        self.assertTrue(form.is_valid())

        program = form.save(commit=False)

        self.assertIsNone(program.university_id)

    def test_optional_program_fields_can_be_empty(self):
        """Duration, tuition, description, and requirements can be omitted."""
        form = ProgramForm(
            data={
                "name": "Software Engineering",
                "degree_type": Program.DegreeType.MASTER,
                "study_language": Program.StudyLanguage.ENGLISH,
                "duration": "",
                "tuition_fee": "",
                "description": "",
                "requirements": "",
            },
            university=self.university,
        )

        self.assertTrue(form.is_valid())