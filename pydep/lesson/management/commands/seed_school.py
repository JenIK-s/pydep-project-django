from django.core.management.base import BaseCommand
from django.db import transaction

from lesson.models import Category, Course, Module, Lesson, ModulesInCourse, LessonsInModule
from users.models import CustomUser


class Command(BaseCommand):
    help = "Наполняет БД демонстрационными данными: пользователи, курсы, модули, уроки"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("Создание демонстрационных данных онлайн-школы"))

        # 1) Категория
        category, _ = Category.objects.get_or_create(name="Программирование")

        # 2) Пользователи (10+)
        users_spec = [
            ("alice", "Алиса", "Иванова", "alice@example.com", True),
            ("bob", "Борис", "Сергеев", "bob@example.com", True),
            ("carol", "Карина", "Петрова", "carol@example.com", False),
            ("dave", "Давид", "Кузнецов", "dave@example.com", False),
            ("erin", "Эрина", "Соколова", "erin@example.com", False),
            ("frank", "Фёдор", "Романов", "frank@example.com", False),
            ("grace", "Галина", "Лебедева", "grace@example.com", False),
            ("heidi", "Хеди", "Ковалева", "heidi@example.com", False),
            ("ivan", "Иван", "Смирнов", "ivan@example.com", False),
            ("judy", "Юлия", "Попова", "judy@example.com", False),
            ("karen", "Карина", "Морозова", "karen@example.com", False),
            ("leo", "Лев", "Волков", "leo@example.com", False),
        ]

        created_users = []
        for username, first_name, last_name, email, is_teacher in users_spec:
            user, created = CustomUser.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "first_name": first_name,
                    "last_name": last_name,
                    "description": (
                        "Увлечённый обучающийся в области ИТ. Люблю практические проекты, "
                        "чёткие объяснения и задачи с реальными примерами."
                    ),
                    "is_teacher": is_teacher,
                    "is_student": not is_teacher,
                },
            )
            if created:
                user.set_password("password123")
                user.save()
            created_users.append(user)

        teachers = [u for u in created_users if u.is_teacher]
        if not teachers:
            # Гарантируем хотя бы одного преподавателя
            created_users[0].is_teacher = True
            created_users[0].is_student = False
            created_users[0].save()
            teachers = [created_users[0]]

        # 3) Курсы (10+) со смыслами
        courses_spec = [
            ("Основы Python", "Первые шаги в Python: синтаксис, типы данных, условия и циклы.", "Python", 4900, "courses/cover-photo.png"),
            ("Продвинутый Python", "ООП, итераторы/генераторы, контекстные менеджеры, typing и best practices.", "Python", 6900, "courses/galaxy-cosmic-5376x3584-14974.jpg"),
            ("Веб‑разработка на Django", "Создание полноценных веб‑приложений на Django: модели, формы, ORM, админка.", "Python", 7900, "courses/maxresdefault.png"),
            ("JavaScript с нуля", "Базовый JS для фронтенда: основы языка, DOM, события, асинхронность.", "JavaScript", 5200, "courses/javascript-2048x1080.jpg"),
            ("Современный Frontend", "ES6+, модули, сборка, основы React и экосистема инструментария.", "JavaScript", 8400, "courses/image.png"),
            ("Git и командная работа", "Ветки, rebase, pull request‑ы, code review. Настоящий рабочий процесс.", "DevOps", 3500, "courses/scale_1200.png"),
            ("Алгоритмы и структуры данных", "Базовые алгоритмы, сложность, практические задачи для собеседований.", "CS", 6100, "courses/max-2614.jpg"),
            ("SQL и базы данных", "Проектирование схем, запросы, индексы, транзакции. SQLite и PostgreSQL.", "SQL", 5700, "courses/shutterstock_152245562_thumb-min.jpg"),
            ("Docker для разработчика", "Контейнеризация, Dockerfile, образы, docker‑compose. Деплой мини‑сервисов.", "DevOps", 4900, "courses/cover-photo.png"),
            ("Основы сетей для разработчика", "TCP/IP, HTTP, DNS, безопасность. Инструменты диагностики.", "Networks", 4500, "courses/photo_2023-09-10_13.38.07.jpeg"),
            ("Основы GitHub Actions", "CI/CD на GitHub Actions: сборка, тесты, деплой.", "DevOps", 4200, "courses/galaxy-cosmic-5376x3584-14974_XtpodOE.jpg"),
            ("ООП на примерах", "Объектно‑ориентированное проектирование на реальных мини‑проектах.", "CS", 5600, "courses/shutterstock_152245562_thumb-min_K6tTHwJ.jpg"),
        ]

        created_courses = []
        for idx, (name, description, language, price, image_path) in enumerate(courses_spec, start=1):
            course = Course(
                name=name,
                description=description,
                price=price,
                image=image_path,
                duration=3 + (idx % 4),
                level="С нуля" if idx % 2 else "С опытом",
                category=category,
                programming_language=language,
            )
            # Обход бага: в модели используется self.slug без поля — выставляем атрибут, чтобы save() не упал
            course.slug = name
            # Идемпотентность по уникальному name
            existing = Course.objects.filter(name=name).first()
            if existing:
                course = existing
            else:
                course.save()
            created_courses.append(course)

        # 4) Для каждого курса создаём 6–8 модулей и 6–8 уроков в модуле
        module_titles = [
            "Введение и установка окружения",
            "Основы синтаксиса и конструкции",
            "Коллекции и работа с данными",
            "Функции и модули",
            "Объектно‑ориентированное программирование",
            "Работа с файлами и сетью",
            "Тестирование и отладка",
            "Мини‑проект по итогам",
        ]

        lesson_titles = [
            "Понимание постановки задачи",
            "Разбор теории с примерами",
            "Практика: пишем код шаг за шагом",
            "Отладка и типичные ошибки",
            "Домашнее задание и критерии",
            "Разбор решения и улучшения",
            "Оптимизация и рефакторинг",
            "Итоги и чек‑лист",
        ]

        def rich_text(paragraph: str) -> str:
            return (
                f"<h3>{paragraph}</h3>"
                "<p>Материал подаётся через короткие объяснения, диаграммы и небольшие практики."
                " В конце — мини‑проект, который закрепляет навыки и создаёт портфолио‑результат.</p>"
                "<ul><li>Реальные кейсы из практики</li><li>Чек‑листы и памятки</li>"
                "<li>Пошаговые инструкции</li></ul>"
            )

        module_image = "courses/modules/cover-photo.png"

        for course in created_courses:
            # 6–8 модулей
            num_modules = 6
            created_module_objs = []
            for i in range(num_modules):
                title = f"{course.name}: {module_titles[i]}"
                module_obj, _ = Module.objects.get_or_create(
                    title=title,
                    defaults={
                        "description": (
                            f"Модуль посвящён теме: '{module_titles[i]}' в контексте курса '{course.name}'. "
                            "Вы разберёте теорию на примерах и выполните практические задания."
                        ),
                        "image": module_image,
                    },
                )
                # Привязка к курсу с порядком
                ModulesInCourse.objects.get_or_create(
                    course=course,
                    module=module_obj,
                    defaults={"sequence_number": i + 1},
                )
                created_module_objs.append(module_obj)

                # 6–8 уроков на модуль
                num_lessons = 6
                for j in range(num_lessons):
                    ltitle = f"{lesson_titles[j]}"
                    lesson_obj, _ = Lesson.objects.get_or_create(
                        title=f"{course.name}: {ltitle}",
                        defaults={
                            "description": rich_text(
                                f"{ltitle} в модуле '{module_titles[i]}' курса '{course.name}'"
                            )
                        },
                    )
                    LessonsInModule.objects.get_or_create(
                        module=module_obj,
                        lesson=lesson_obj,
                    )

            # Назначаем преподавателей курса (1–2)
            for teacher in teachers[:2]:
                teacher.courses_teach.add(course)

            # Несколько студентов «обучаются» на курсе
            for student in created_users:
                if not student.is_teacher and (hash(student.username + course.name) % 3 == 0):
                    student.courses_learn.add(course)

        self.stdout.write(self.style.SUCCESS("Готово: созданы пользователи, курсы, модули и уроки."))


