from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.universities.models import Program, University


User = get_user_model()


class UniversityViewTestBase(TestCase):
    """Shared setup for university view tests."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="TestPassword123!",
        )

        self.university = University.objects.create(
            name="Dalian University of Technology",
            country="China",
            city="Dalian",
        )

        self.client.force_login(self.user)


class UniversityListViewTests(UniversityViewTestBase):
    """Tests for the university list view."""

    def test_list_page_loads(self):
        """Authenticated users can view the university list."""
        response = self.client.get(
            reverse("universities:list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "universities/university_list.html",
        )

    def test_list_contains_university(self):
        """The university list displays existing universities."""
        response = self.client.get(
            reverse("universities:list")
        )

        self.assertContains(
            response,
            "Dalian University of Technology",
        )

    def test_list_requires_authentication(self):
        """Unauthenticated users cannot access the university list."""
        self.client.logout()

        response = self.client.get(
            reverse("universities:list")
        )

        self.assertEqual(response.status_code, 302)


class UniversityDetailViewTests(UniversityViewTestBase):
    """Tests for the university detail view."""

    def test_detail_page_loads(self):
        """Authenticated users can view a university."""
        response = self.client.get(
            reverse(
                "universities:detail",
                kwargs={"pk": self.university.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "universities/university_detail.html",
        )

    def test_detail_displays_university(self):
        """The detail page contains the university information."""
        response = self.client.get(
            reverse(
                "universities:detail",
                kwargs={"pk": self.university.pk},
            )
        )

        self.assertContains(
            response,
            "Dalian University of Technology",
        )

    def test_detail_displays_programs(self):
        """The detail page displays programs belonging to the university."""
        Program.objects.create(
            university=self.university,
            name="Software Engineering",
            degree_type=Program.DegreeType.MASTER,
        )

        response = self.client.get(
            reverse(
                "universities:detail",
                kwargs={"pk": self.university.pk},
            )
        )

        self.assertContains(
            response,
            "Software Engineering",
        )

    def test_detail_returns_404_for_missing_university(self):
        """A missing university produces a 404 response."""
        response = self.client.get(
            reverse(
                "universities:detail",
                kwargs={"pk": 99999},
            )
        )

        self.assertEqual(response.status_code, 404)


class UniversityCreateViewTests(UniversityViewTestBase):
    """Tests for creating universities."""

    def test_create_page_loads(self):
        """Authenticated users can open the university creation form."""
        response = self.client.get(
            reverse("universities:create")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "universities/university_form.html",
        )

    def test_valid_post_creates_university(self):
        """Valid form data creates a university."""
        response = self.client.post(
            reverse("universities:create"),
            {
                "name": "Tsinghua University",
                "country": "China",
                "city": "Beijing",
                "website": "https://www.tsinghua.edu.cn/",
                "ranking": 1,
                "description": "A university in Beijing.",
                "notes": "Potential application.",
            },
        )

        self.assertEqual(
            University.objects.filter(
                name="Tsinghua University"
            ).count(),
            1,
        )

        university = University.objects.get(
            name="Tsinghua University"
        )

        self.assertRedirects(
            response,
            reverse(
                "universities:detail",
                kwargs={"pk": university.pk},
            ),
        )

    def test_invalid_post_does_not_create_university(self):
        """Invalid form data does not create a university."""
        response = self.client.post(
            reverse("universities:create"),
            {
                "name": "",
                "country": "China",
                "city": "Beijing",
                "website": "",
                "ranking": "",
                "description": "",
                "notes": "",
            },
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            University.objects.count(),
            1,
        )


class UniversityUpdateViewTests(UniversityViewTestBase):
    """Tests for updating universities."""

    def test_update_page_loads(self):
        """Authenticated users can open the edit form."""
        response = self.client.get(
            reverse(
                "universities:update",
                kwargs={"pk": self.university.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "universities/university_form.html",
        )

    def test_valid_post_updates_university(self):
        """Valid form data updates the university."""
        response = self.client.post(
            reverse(
                "universities:update",
                kwargs={"pk": self.university.pk},
            ),
            {
                "name": "Dalian University of Technology",
                "country": "China",
                "city": "Liaoning",
                "website": "",
                "ranking": 20,
                "description": "Updated description.",
                "notes": "Updated notes.",
            },
        )

        self.university.refresh_from_db()

        self.assertEqual(
            self.university.city,
            "Liaoning",
        )
        self.assertEqual(
            self.university.ranking,
            20,
        )

        self.assertRedirects(
            response,
            reverse(
                "universities:detail",
                kwargs={"pk": self.university.pk},
            ),
        )


class UniversityDeleteViewTests(UniversityViewTestBase):
    """Tests for deleting universities."""

    def test_delete_page_loads(self):
        """The deletion confirmation page is displayed."""
        response = self.client.get(
            reverse(
                "universities:delete",
                kwargs={"pk": self.university.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "universities/university_confirm_delete.html",
        )

    def test_get_does_not_delete_university(self):
        """Opening the delete page does not delete the university."""
        self.client.get(
            reverse(
                "universities:delete",
                kwargs={"pk": self.university.pk},
            )
        )

        self.assertTrue(
            University.objects.filter(
                pk=self.university.pk
            ).exists()
        )

    def test_post_deletes_university(self):
        """A confirmed POST deletes the university."""
        response = self.client.post(
            reverse(
                "universities:delete",
                kwargs={"pk": self.university.pk},
            )
        )

        self.assertFalse(
            University.objects.filter(
                pk=self.university.pk
            ).exists()
        )

        self.assertRedirects(
            response,
            reverse("universities:list"),
        )

    def test_deleting_university_also_deletes_programs(self):
        """Deleting a university cascades to its programs."""
        program = Program.objects.create(
            university=self.university,
            name="Software Engineering",
            degree_type=Program.DegreeType.MASTER,
        )

        self.client.post(
            reverse(
                "universities:delete",
                kwargs={"pk": self.university.pk},
            )
        )

        self.assertFalse(
            Program.objects.filter(
                pk=program.pk
            ).exists()
        )


class ProgramCreateViewTests(UniversityViewTestBase):
    """Tests for creating programs."""

    def test_create_page_loads(self):
        """The program creation page loads for a university."""
        response = self.client.get(
            reverse(
                "universities:program_create",
                kwargs={"university_pk": self.university.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "universities/program_form.html",
        )

    def test_valid_post_creates_program(self):
        """Valid data creates a program for the selected university."""
        response = self.client.post(
            reverse(
                "universities:program_create",
                kwargs={"university_pk": self.university.pk},
            ),
            {
                "name": "Software Engineering",
                "degree_type": Program.DegreeType.MASTER,
                "study_language": Program.StudyLanguage.ENGLISH,
                "duration": "2.5",
                "tuition_fee": "30000.00",
                "description": "Master's program.",
                "requirements": "Bachelor's degree.",
            },
        )

        program = Program.objects.get(
            name="Software Engineering"
        )

        self.assertEqual(
            program.university,
            self.university,
        )

        self.assertRedirects(
            response,
            reverse(
                "universities:detail",
                kwargs={"pk": self.university.pk},
            ),
        )


class ProgramUpdateViewTests(UniversityViewTestBase):
    """Tests for updating programs."""

    def setUp(self):
        super().setUp()

        self.program = Program.objects.create(
            university=self.university,
            name="Software Engineering",
            degree_type=Program.DegreeType.MASTER,
            study_language=Program.StudyLanguage.ENGLISH,
        )

    def test_valid_post_updates_program(self):
        """Valid data updates an existing program."""
        response = self.client.post(
            reverse(
                "universities:program_update",
                kwargs={"pk": self.program.pk},
            ),
            {
                "name": "Software Engineering",
                "degree_type": Program.DegreeType.MASTER,
                "study_language": Program.StudyLanguage.ENGLISH,
                "duration": "2.0",
                "tuition_fee": "35000.00",
                "description": "Updated program.",
                "requirements": "Updated requirements.",
            },
        )

        self.program.refresh_from_db()

        self.assertEqual(
            self.program.duration,
            2,
        )
        self.assertEqual(
            self.program.tuition_fee,
            35000,
        )

        self.assertRedirects(
            response,
            reverse(
                "universities:detail",
                kwargs={"pk": self.university.pk},
            ),
        )


class ProgramDeleteViewTests(UniversityViewTestBase):
    """Tests for deleting programs."""

    def setUp(self):
        super().setUp()

        self.program = Program.objects.create(
            university=self.university,
            name="Software Engineering",
            degree_type=Program.DegreeType.MASTER,
        )

    def test_delete_page_loads(self):
        """The program deletion confirmation page loads."""
        response = self.client.get(
            reverse(
                "universities:program-delete",
                kwargs={"pk": self.program.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "universities/program_confirm_delete.html",
        )

    def test_get_does_not_delete_program(self):
        """Opening the delete page does not delete the program."""
        self.client.get(
            reverse(
                "universities:program-delete",
                kwargs={"pk": self.program.pk},
            )
        )

        self.assertTrue(
            Program.objects.filter(
                pk=self.program.pk
            ).exists()
        )

    def test_post_deletes_program(self):
        """A confirmed POST deletes the program."""
        response = self.client.post(
            reverse(
                "universities:program-delete",
                kwargs={"pk": self.program.pk},
            )
        )

        self.assertFalse(
            Program.objects.filter(
                pk=self.program.pk
            ).exists()
        )

        self.assertRedirects(
            response,
            reverse(
                "universities:detail",
                kwargs={"pk": self.university.pk},
            ),
        )