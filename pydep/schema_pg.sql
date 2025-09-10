-- Таблица пользователей (CustomUser)
CREATE TABLE customuser (
    id INTEGER PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP,
    is_superuser BOOLEAN NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    image VARCHAR(255),
    description TEXT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    birthday DATE,
    is_staff BOOLEAN NOT NULL,
    is_active BOOLEAN NOT NULL,
    date_joined TIMESTAMP NOT NULL,
    is_teacher BOOLEAN DEFAULT FALSE,
    is_student BOOLEAN DEFAULT TRUE,
    is_tutor_student BOOLEAN DEFAULT FALSE,
    is_tutor_admin BOOLEAN DEFAULT FALSE,
    payment INTEGER
);

-- Таблица категорий
CREATE TABLE category (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    slug VARCHAR(50) UNIQUE
);

-- Таблица уроков
CREATE TABLE lesson (
    id INTEGER PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT
);

-- Таблица модулей
CREATE TABLE module (
    id INTEGER PRIMARY KEY,
    title VARCHAR(255) UNIQUE NOT NULL,
    description TEXT NOT NULL,
    image VARCHAR(255) NOT NULL
);

-- Таблица курсов
CREATE TABLE course (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    slug VARCHAR(50),
    description TEXT NOT NULL,
    price INTEGER DEFAULT 1000,
    image VARCHAR(255) NOT NULL,
    duration INTEGER DEFAULT 3,
    level VARCHAR(50) DEFAULT 'С нуля',
    category_id INTEGER,
    programming_language VARCHAR(255) NOT NULL,
    FOREIGN KEY (category_id) REFERENCES category(id) ON DELETE CASCADE
);

-- Промежуточная таблица ModulesInCourse
CREATE TABLE modulesincourse (
    id INTEGER PRIMARY KEY,
    module_id INTEGER,
    course_id INTEGER,
    sequence_number INTEGER NOT NULL,
    FOREIGN KEY (module_id) REFERENCES module(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES course(id) ON DELETE CASCADE
);

-- Промежуточная таблица LessonsInModule
CREATE TABLE lessonsinmodule (
    id INTEGER PRIMARY KEY,
    module_id INTEGER,
    lesson_id INTEGER,
    FOREIGN KEY (module_id) REFERENCES module(id) ON DELETE CASCADE,
    FOREIGN KEY (lesson_id) REFERENCES lesson(id) ON DELETE CASCADE
);

-- ManyToMany для courses_learn (CustomUser ↔ Course)
CREATE TABLE customuser_courses_learn (
    id INTEGER PRIMARY KEY,
    customuser_id INTEGER,
    course_id INTEGER,
    FOREIGN KEY (customuser_id) REFERENCES customuser(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES course(id) ON DELETE CASCADE
);

-- ManyToMany для courses_teach (CustomUser ↔ Course)
CREATE TABLE customuser_courses_teach (
    id INTEGER PRIMARY KEY,
    customuser_id INTEGER,
    course_id INTEGER,
    FOREIGN KEY (customuser_id) REFERENCES customuser(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES course(id) ON DELETE CASCADE
);

-- Прогресс пользователя по урокам
CREATE TABLE userlessonprogress (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    course_id INTEGER,
    module_id INTEGER,
    lesson_id INTEGER,
    completed BOOLEAN DEFAULT FALSE,
    current BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES customuser(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES course(id) ON DELETE CASCADE,
    FOREIGN KEY (module_id) REFERENCES module(id) ON DELETE CASCADE,
    FOREIGN KEY (lesson_id) REFERENCES lesson(id) ON DELETE CASCADE
);

-- Документы проекта
CREATE TABLE projectdocument (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    file VARCHAR(255) NOT NULL
);

-- Запись на курс
CREATE TABLE registercourse (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    course_id INTEGER,
    status VARCHAR(9) DEFAULT 'wait',
    UNIQUE(user_id, course_id),
    FOREIGN KEY (user_id) REFERENCES customuser(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES course(id) ON DELETE CASCADE
);

-- Отмена занятия
CREATE TABLE cancelledlesson (
    id INTEGER PRIMARY KEY,
    student_id INTEGER,
    date_cancelled DATE NOT NULL,
    FOREIGN KEY (student_id) REFERENCES customuser(id) ON DELETE CASCADE
);

-- Расписание занятий
CREATE TABLE schedule (
    id INTEGER PRIMARY KEY,
    student_id INTEGER,
    weekday VARCHAR(19) NOT NULL,
    time_start TIME NOT NULL,
    hour_amount INTEGER DEFAULT 1,
    FOREIGN KEY (student_id) REFERENCES customuser(id) ON DELETE CASCADE
);

-- Таблица связи ManyToMany для отменённых занятий (Schedule ↔ CancelledLesson)
CREATE TABLE schedule_cancelledlesson (
    id INTEGER PRIMARY KEY,
    schedule_id INTEGER,
    cancelledlesson_id INTEGER,
    FOREIGN KEY (schedule_id) REFERENCES schedule(id) ON DELETE CASCADE,
    FOREIGN KEY (cancelledlesson_id) REFERENCES cancelledlesson(id) ON DELETE CASCADE
);
