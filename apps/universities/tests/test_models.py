from decimal import Decimal

from django.test import TestCase

from apps.universities.models import Program, University


class UniversityModelTests(TestCase):
    """Tests for the University model."""

    def test_university_can_be_created(self):
        """A university can be created with valid information."""
        university = University.objects.create(
            name="Dalian University of Technology",
            country="China",
            city="Dalian",
            website="https://www.dlut.edu.cn/",
            ranking=25,
            description="A university in Dalian.",
            notes="Consider for master's application.",
        )

        self.assertEqual(
            university.name,
            "Dalian University of Technology",
        )
        self.assertEqual(university.country, "China")
        self.assertEqual(university.city, "Dalian")
        self.assertEqual(university.ranking, 25)

    def test_country_defaults_to_china(self):
        """A university defaults to China when no country is provided."""
        university = University.objects.create(
            name="Test University",
        )

        self.assertEqual(university.country, "China")

    def test_optional_fields_can_be_empty(self):
        """Optional university fields can be left blank."""
        university = University.objects.create(
            name="Test University",
        )

        self.assertEqual(university.city, "")
        self.assertEqual(university.website, "")
        self.assertIsNone(university.ranking)
        self.assertEqual(university.description, "")
        self.assertEqual(university.notes, "")

    def test_university_string_representation(self):
        """The university string representation is its name."""
        university = University.objects.create(
            name="Tsinghua University",
        )

        self.assertEqual(
            str(university),
            "Tsinghua University",
        )


class ProgramModelTests(TestCase):
    """Tests for the Program model."""

    def setUp(self):
        self.university = University.objects.create(
            name="Dalian University of Technology",
        )

    def test_program_can_be_created(self):
        """A program can be created for a university."""
        program = Program.objects.create(
            university=self.university,
            name="Software Engineering",
            degree_type=Program.DegreeType.MASTER,
            study_language=Program.StudyLanguage.ENGLISH,
            duration=Decimal("2.5"),
            tuition_fee=Decimal("30000.00"),
        )

        self.assertEqual(
            program.name,
            "Software Engineering",
        )
        self.assertEqual(
            program.degree_type,
            Program.DegreeType.MASTER,
        )
        self.assertEqual(
            program.study_language,
            Program.StudyLanguage.ENGLISH,
        )
        self.assertEqual(
            program.duration,
            Decimal("2.5"),
        )
        self.assertEqual(
            program.tuition_fee,
            Decimal("30000.00"),
        )

    def test_program_belongs_to_university(self):
        """A program is associated with its university."""
        program = Program.objects.create(
            university=self.university,
            name="Software Engineering",
            degree_type=Program.DegreeType.MASTER,
        )

        self.assertEqual(
            program.university,
            self.university,
        )

    def test_university_can_access_its_programs(self):
        """A university can access its programs through the related name."""
        Program.objects.create(
            university=self.university,
            name="Software Engineering",
            degree_type=Program.DegreeType.MASTER,
        )

        Program.objects.create(
            university=self.university,
            name="Computer Science",
            degree_type=Program.DegreeType.MASTER,
        )

        self.assertEqual(
            self.university.programs.count(),
            2,
        )

    def test_program_string_representation(self):
        """The program string representation includes its university."""
        program = Program.objects.create(
            university=self.university,
            name="Software Engineering",
            degree_type=Program.DegreeType.MASTER,
        )

        self.assertEqual(
            str(program),
            "Software Engineering — Dalian University of Technology",
        )

    def test_program_defaults_to_english(self):
        """Programs default to English as their study language."""
        program = Program.objects.create(
            university=self.university,
            name="Software Engineering",
            degree_type=Program.DegreeType.MASTER,
        )

        self.assertEqual(
            program.study_language,
            Program.StudyLanguage.ENGLISH,
        )

    def test_duplicate_program_for_same_university_and_degree_is_rejected(self):
        """The same program cannot be duplicated for the same degree."""
        Program.objects.create(
            university=self.university,
            name="Software Engineering",
            degree_type=Program.DegreeType.MASTER,
        )

        duplicate = Program(
            university=self.university,
            name="Software Engineering",
            degree_type=Program.DegreeType.MASTER,
        )

        with self.assertRaises(Exception):
            duplicate.save()

    def test_same_program_name_can_exist_for_different_degree(self):
        """The same program name can exist for different degree types."""
        Program.objects.create(
            university=self.university,
            name="Computer Science",
            degree_type=Program.DegreeType.BACHELOR,
        )

        program = Program.objects.create(
            university=self.university,
            name="Computer Science",
            degree_type=Program.DegreeType.MASTER,
        )

        self.assertIsNotNone(program.pk)

    def test_deleting_university_deletes_programs(self):
        """Deleting a university also deletes its programs."""
        Program.objects.create(
            university=self.university,
            name="Software Engineering",
            degree_type=Program.DegreeType.MASTER,
        )

        self.university.delete()

        self.assertEqual(
            Program.objects.count(),
            0,
        )