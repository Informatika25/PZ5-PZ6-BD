from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    AcademicGroupForm,
    CourseForm,
    DepartmentForm,
)

from .models import (
    AcademicGroup,
    Course,
    Department,
    StudentProfile
)

from django.shortcuts import render
from django.db.models import Count



def is_methodist(user):
    return user.groups.filter(
        name='Методист'
    ).exists()


@login_required
def profile(request):
    return render(
        request,
        'profile.html',
        {
            'is_methodist': is_methodist(
                request.user
            )
        }
    )


@login_required
def course_list(request):
    courses = Course.objects.select_related(
        'department'
    ).all()

    return render(
        request,
        'course_list.html',
        {
            'courses': courses,
            'is_methodist': is_methodist(
                request.user
            ),
        }
    )


@login_required
def department_list(request):
    departments = Department.objects.all()

    return render(
        request,
        'department_list.html',
        {
            'departments': departments,
            'is_methodist': is_methodist(
                request.user
            ),
        }
    )


@login_required
@user_passes_test(is_methodist)
def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(
            request.POST
        )

        if form.is_valid():
            form.save()

            return redirect(
                'department_list'
            )
    else:
        form = DepartmentForm()

    return render(
        request,
        'object_form.html',
        {
            'form': form,
            'title': 'Добавление факультета',
        }
    )


@login_required
@user_passes_test(is_methodist)
def department_update(
    request,
    pk
):
    department = get_object_or_404(
        Department,
        pk=pk
    )

    if request.method == 'POST':
        form = DepartmentForm(
            request.POST,
            instance=department
        )

        if form.is_valid():
            form.save()

            return redirect(
                'department_list'
            )
    else:
        form = DepartmentForm(
            instance=department
        )

    return render(
        request,
        'object_form.html',
        {
            'form': form,
            'title': 'Изменение факультета',
        }
    )


@login_required
@user_passes_test(is_methodist)
def department_delete(
    request,
    pk
):
    department = get_object_or_404(
        Department,
        pk=pk
    )

    if request.method == 'POST':
        department.delete()

        return redirect(
            'department_list'
        )

    return render(
        request,
        'object_confirm_delete.html',
        {
            'object': department,
            'title': 'Удаление факультета',
        }
    )


@login_required
def academic_group_list(request):
    groups = AcademicGroup.objects.select_related(
        'department'
    ).all()

    return render(
        request,
        'academic_group_list.html',
        {
            'groups': groups,
            'is_methodist': is_methodist(
                request.user
            ),
        }
    )


@login_required
@user_passes_test(is_methodist)
def academic_group_create(request):
    if request.method == 'POST':
        form = AcademicGroupForm(
            request.POST
        )

        if form.is_valid():
            form.save()

            return redirect(
                'academic_group_list'
            )
    else:
        form = AcademicGroupForm()

    return render(
        request,
        'object_form.html',
        {
            'form': form,
            'title': 'Добавление учебной группы',
        }
    )


@login_required
@user_passes_test(is_methodist)
def academic_group_update(
    request,
    pk
):
    group = get_object_or_404(
        AcademicGroup,
        pk=pk
    )

    if request.method == 'POST':
        form = AcademicGroupForm(
            request.POST,
            instance=group
        )

        if form.is_valid():
            form.save()

            return redirect(
                'academic_group_list'
            )
    else:
        form = AcademicGroupForm(
            instance=group
        )

    return render(
        request,
        'object_form.html',
        {
            'form': form,
            'title': 'Изменение учебной группы',
        }
    )


@login_required
@user_passes_test(is_methodist)
def academic_group_delete(
    request,
    pk
):
    group = get_object_or_404(
        AcademicGroup,
        pk=pk
    )

    if request.method == 'POST':
        group.delete()

        return redirect(
            'academic_group_list'
        )

    return render(
        request,
        'object_confirm_delete.html',
        {
            'object': group,
            'title': 'Удаление учебной группы',
        }
    )


@login_required
@user_passes_test(is_methodist)
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(
            request.POST
        )

        if form.is_valid():
            form.save()

            return redirect(
                'course_list'
            )
    else:
        form = CourseForm()

    return render(
        request,
        'object_form.html',
        {
            'form': form,
            'title': 'Добавление курса',
        }
    )


@login_required
@user_passes_test(is_methodist)
def course_update(
    request,
    pk
):
    course = get_object_or_404(
        Course,
        pk=pk
    )

    if request.method == 'POST':
        form = CourseForm(
            request.POST,
            instance=course
        )

        if form.is_valid():
            form.save()

            return redirect(
                'course_list'
            )
    else:
        form = CourseForm(
            instance=course
        )

    return render(
        request,
        'object_form.html',
        {
            'form': form,
            'title': 'Изменение курса',
        }
    )


@login_required
@user_passes_test(is_methodist)
def course_delete(
    request,
    pk
):
    course = get_object_or_404(
        Course,
        pk=pk
    )

    if request.method == 'POST':
        course.delete()

        return redirect(
            'course_list'
        )

    return render(
        request,
        'object_confirm_delete.html',
        {
            'object': course,
            'title': 'Удаление курса',
        }
    )
#Добавляем дашборды

# Дашборды аналитики
@login_required
def dashboard_view(request):
    # Общие показатели из базы данных
    total_departments = Department.objects.count()
    total_courses = Course.objects.count()
    total_groups = AcademicGroup.objects.count()
    total_students = StudentProfile.objects.count()

    # Считаем данные отдельно для каждого факультета
    departments_stats = Department.objects.annotate(
        courses_count=Count('courses', distinct=True),
        groups_count=Count('groups', distinct=True),
        students_count=Count('students', distinct=True),
    ).order_by('name')

    # Подготавливаем данные для графиков
    dept_names = []
    courses_counts = []
    groups_counts = []
    students_counts = []

    for department in departments_stats:
        dept_names.append(department.name)
        courses_counts.append(department.courses_count)
        groups_counts.append(department.groups_count)
        students_counts.append(department.students_count)

    # Студенты с назначенной учебной группой и без неё
    students_with_group = StudentProfile.objects.filter(
        academic_group__isnull=False
    ).count()

    students_without_group = StudentProfile.objects.filter(
        academic_group__isnull=True
    ).count()

    # Количество записей студентов на курсы (это именно связи студент-курс, а не число уникальных курсов)
    total_enrollments = sum(
        student.courses.count()
        for student in StudentProfile.objects.prefetch_related('courses')
    )

    # Количество студентов в каждой учебной группе
    groups_stats = AcademicGroup.objects.annotate(
        students_count=Count('students', distinct=True)
    ).order_by('name')

    group_names = [group.name for group in groups_stats]
    group_students_counts = [
        group.students_count for group in groups_stats
    ]

    context = {
        'total_departments': total_departments,
        'total_courses': total_courses,
        'total_groups': total_groups,
        'total_students': total_students,
        'total_enrollments': total_enrollments,

        'dept_names': dept_names,
        'courses_counts': courses_counts,
        'groups_counts': groups_counts,
        'students_counts': students_counts,

        'students_with_group': students_with_group,
        'students_without_group': students_without_group,

        'group_names': group_names,
        'group_students_counts': group_students_counts,
    }

    return render(request, 'dashboard.html', context)