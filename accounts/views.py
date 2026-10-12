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


# Дашборды аналитики
@login_required
def dashboard_view(request):
    departments = Department.objects.all().order_by('name')

    selected_department_id = request.GET.get('department')

# Создаём запрос для получения статистики по факультетам
    departments_stats = Department.objects.annotate(
        courses_count=Count('courses', distinct=True),
        groups_count=Count('groups', distinct=True),
        students_count=Count('students', distinct=True),
    ).order_by('name')

    # Получаем название вкладки, которую нужно открыть
    selected_tab = request.GET.get('tab', '')

    # Если пользователь выбрал конкретный факультет,
    # оставляем в статистике только его
    if selected_department_id:
        departments_stats = departments_stats.filter(
            id=selected_department_id
        )

    dept_names = []
    courses_counts = []
    groups_counts = []
    students_counts = []

    # Здесь статистика для таблицы
    departments_table = []

    for department in departments_stats:
        dept_names.append(department.name)
        courses_counts.append(department.courses_count)
        groups_counts.append(department.groups_count)
        students_counts.append(department.students_count)

        # Добавляем показатели факультета в таблицу
        departments_table.append({
            'name': department.name,
            'courses_count': department.courses_count,
            'groups_count': department.groups_count,
            'students_count': department.students_count,
        })

    # Находим факультет с наибольшим количеством студентов и курсов
    if departments_stats.exists():
        department_by_students = departments_stats.order_by(
            '-students_count', 'name'
        ).first()

        department_by_courses = departments_stats.order_by(
            '-courses_count', 'name'
        ).first()

        top_students_department = department_by_students.name
        top_students_count = department_by_students.students_count

        top_courses_department = department_by_courses.name
        top_courses_count = department_by_courses.courses_count
    else:
        top_students_department = 'Нет данных'
        top_students_count = 0

        top_courses_department = 'Нет данных'
        top_courses_count = 0


    # Если выбран конкретный факультет,
    # карточки показывают данные только по нему
    if selected_department_id:
        selected_department = departments_stats.first()

        if selected_department:
            total_departments = 1
            total_courses = selected_department.courses_count
            total_groups = selected_department.groups_count
            total_students = selected_department.students_count
        else:
            total_departments = 0
            total_courses = 0
            total_groups = 0
            total_students = 0
    else:
        # Если факультет не выбран, показываем общую статистику
        total_departments = Department.objects.count()
        total_courses = Course.objects.count()
        total_groups = AcademicGroup.objects.count()
        total_students = StudentProfile.objects.count()


    # Получаем всех студентов
    students = StudentProfile.objects.all()

    # Считаем студентов с группой и без группы
    if selected_department_id:
        students_with_group = students.filter(
            academic_group__department_id=selected_department_id
        ).count()

        students_without_group = 0
    else:
        students_with_group = students.filter(
            academic_group__isnull=False
        ).count()

        students_without_group = students.filter(
            academic_group__isnull=True
        ).count()

    # Считаем количество записей студентов на курсы
    students_for_enrollments = StudentProfile.objects.prefetch_related(
        'courses'
    )

    if selected_department_id:
        students_for_enrollments = students_for_enrollments.filter(
            academic_group__department_id=selected_department_id
        )

    total_enrollments = sum(
        student.courses.count()
        for student in students_for_enrollments
    )

    # Получаем количество студентов в каждой учебной группе
    groups = AcademicGroup.objects.all()

    if selected_department_id:
        groups = groups.filter(
            department_id=selected_department_id
        )

    groups_stats = groups.annotate(
        students_count=Count('students', distinct=True)
    ).order_by('name')

    group_names = []
    group_students_counts = []

    for group in groups_stats:
        group_names.append(group.name)
        group_students_counts.append(group.students_count)


    print('Всего студентов:', StudentProfile.objects.count())
    print(
        'Студентов без группы:',
        StudentProfile.objects.filter(
            academic_group__isnull=True
        ).count()
    )

    # Передаём все данные
    context = {
        'departments': departments,
        'selected_department_id': selected_department_id,
        'selected_tab': selected_tab,

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

        'departments_table': departments_table,

        'top_students_department': top_students_department,
        'top_students_count': top_students_count,
        'top_courses_department': top_courses_department,
        'top_courses_count': top_courses_count,
    }

    return render(request,'dashboard.html', context)