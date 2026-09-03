from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import UniversityForm, ProgramForm
from .models import University, Program


@login_required
def university_list(request):
    """
    Display all universities in the tracker.
    """

    universities = University.objects.prefetch_related(
        "programs"
    )

    return render(
        request,
        "universities/university_list.html",
        {
            "universities": universities,
        },
    )


@login_required
def university_detail(request, pk):
    """
    Display a university and its available programs.
    """

    university = get_object_or_404(
        University.objects.prefetch_related("programs"),
        pk=pk,
    )

    return render(
        request,
        "universities/university_detail.html",
        {
            "university": university,
        },
    )


@login_required
def university_create(request):
    """
    Create a new university.
    """

    form = UniversityForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        university = form.save()

        return redirect(
            "universities:detail",
            pk=university.pk,
        )

    return render(
        request,
        "universities/university_form.html",
        {
            "form": form,
            "page_title": "Add University",
            "submit_label": "Add University",
        },
    )
    
@login_required
def university_update(request, pk):
    """
    Update an existing university.
    """

    university = get_object_or_404(
        University,
        pk=pk,
    )

    form = UniversityForm(
        request.POST or None,
        instance=university,
    )

    if request.method == "POST" and form.is_valid():
        university = form.save()

        return redirect(
            "universities:detail",
            pk=university.pk,
        )

    return render(
        request,
        "universities/university_form.html",
        {
            "form": form,
            "page_title": "Edit University",
            "submit_label": "Save Changes",
            "university": university,
        },
    )


@login_required
def university_delete(request, pk):
    """
    Delete a university after explicit confirmation.
    """

    university = get_object_or_404(
        University,
        pk=pk,
    )

    if request.method == "POST":
        university.delete()

        return redirect(
            "universities:list"
        )

    return render(
        request,
        "universities/university_confirm_delete.html",
        {
            "university": university,
        },
    )
    

@login_required
def program_create(request, university_pk):
    """
    Create a program for a specific university.
    """

    university = get_object_or_404(
        University,
        pk=university_pk,
    )

    form = ProgramForm(
        request.POST or None,
        university=university,
    )

    if request.method == "POST" and form.is_valid():
        form.save()

        return redirect(
            "universities:detail",
            pk=university.pk,
        )

    return render(
        request,
        "universities/program_form.html",
        {
            "form": form,
            "university": university,
            "page_title": "Add Program",
            "submit_label": "Add Program",
        },
    )


@login_required
def program_update(request, pk):
    """
    Update an existing program.
    """

    program = get_object_or_404(
        Program,
        pk=pk,
    )

    form = ProgramForm(
        request.POST or None,
        instance=program,
        university=program.university,
    )

    if request.method == "POST" and form.is_valid():
        form.save()

        return redirect(
            "universities:detail",
            pk=program.university.pk,
        )

    return render(
        request,
        "universities/program_form.html",
        {
            "form": form,
            "university": program.university,
            "program": program,
            "page_title": "Edit Program",
            "submit_label": "Save Changes",
        },
    )


@login_required
def program_delete(request, pk):
    """
    Delete an existing program after confirmation.
    """

    program = get_object_or_404(
        Program,
        pk=pk,
    )

    university = program.university

    if request.method == "POST":
        program.delete()

        return redirect(
            "universities:detail",
            pk=university.pk,
        )

    return render(
        request,
        "universities/program_confirm_delete.html",
        {
            "program": program,
            "university": university,
        },
    )