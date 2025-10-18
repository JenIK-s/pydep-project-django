
# Справочник HTML-тегов

| Тег | Назначение | Пример |
|-----|------------|--------|
| `<!DOCTYPE html>` | Указывает, что используется HTML5 | `<!DOCTYPE html>` |
| `<html>` | Корневой тег страницы | `<html> ... </html>` |
| `<head>` | Служебная информация (метаданные) | `<head><title>Сайт</title></head>` |
| `<title>` | Название вкладки браузера | `<title>Моя страница</title>` |
| `<meta>` | Метаданные (кодировка, описание, ключи) | `<meta charset="UTF-8">` |
| `<body>` | Всё содержимое страницы | `<body>Текст</body>` |
| `<h1>`–`<h6>` | Заголовки от крупного до мелкого | `<h1>Главный заголовок</h1>` |
| `<p>` | Абзац текста | `<p>Это абзац.</p>` |
| `<br>` | Перенос строки | `Привет<br>мир` |
| `<hr>` | Горизонтальная линия | `<hr>` |
| `<b>` | Жирный текст | `<b>Важное</b>` |
| `<strong>` | Важный текст (семантика) | `<strong>Очень важно!</strong>` |
| `<i>` | Курсив | `<i>Текст</i>` |
| `<em>` | Выделение (акцент) | `<em>Акцент</em>` |
| `<u>` | Подчёркивание | `<u>Подчёркнутый</u>` |
| `<s>` | Зачёркнутый | `<s>Старое</s>` |
| `<sup>` | Верхний индекс | `x<sup>2</sup>` |
| `<sub>` | Нижний индекс | `H<sub>2</sub>O` |
| `<mark>` | Подсветка текста | `<mark>Важное слово</mark>` |
| `<small>` | Мелкий текст | `<small>Примечание</small>` |
| `<abbr>` | Аббревиатура с подсказкой | `<abbr title="HyperText Markup Language">HTML</abbr>` |
| `<blockquote>` | Цитата (блок) | `<blockquote>Цитата</blockquote>` |
| `<q>` | Короткая цитата | `<q>Фраза</q>` |
| `<code>` | Код | `<code>print("Hello")</code>` |
| `<pre>` | Предварительное форматирование | `<pre>    текст</pre>` |
| `<ul>` | Маркированный список | `<ul><li>Элемент</li></ul>` |
| `<ol>` | Нумерованный список | `<ol><li>Первый</li></ol>` |
| `<li>` | Элемент списка | `<li>Пункт</li>` |
| `<dl>` | Список определений | `<dl><dt>HTML</dt><dd>Язык разметки</dd></dl>` |
| `<dt>` | Термин | `<dt>CSS</dt>` |
| `<dd>` | Определение | `<dd>Таблицы стилей</dd>` |
| `<a>` | Ссылка | `<a href="https://google.com">Google</a>` |
| `<img>` | Изображение | `<img src="pic.jpg" alt="Картинка">` |
| `<map>` + `<area>` | Карта изображения | `<map><area shape="rect" coords="34,44,270,350" href="link.html"></map>` |
| `<audio>` | Вставка аудио | `<audio controls src="music.mp3"></audio>` |
| `<video>` | Вставка видео | `<video controls src="movie.mp4"></video>` |
| `<source>` | Источник для аудио/видео | `<source src="file.ogg" type="audio/ogg">` |
| `<table>` | Таблица | `<table border="1">...</table>` |
| `<tr>` | Строка таблицы | `<tr><td>Ячейка</td></tr>` |
| `<td>` | Ячейка | `<td>Текст</td>` |
| `<th>` | Заголовок ячейки | `<th>Имя</th>` |
| `<caption>` | Заголовок таблицы | `<caption>Оценки</caption>` |
| `<thead>` | Заголовок таблицы | `<thead>...</thead>` |
| `<tbody>` | Основная часть таблицы | `<tbody>...</tbody>` |
| `<tfoot>` | Нижняя часть таблицы | `<tfoot>...</tfoot>` |
| `colspan` | Объединение ячеек по горизонтали | `<td colspan="2">Объединено</td>` |
| `rowspan` | Объединение ячеек по вертикали | `<td rowspan="2">Объединено</td>` |
| `<form>` | Форма | `<form action="send.php" method="post">...</form>` |
| `<input>` | Поле ввода | `<input type="text" name="user">` |
| `<label>` | Подпись к полю | `<label for="login">Логин:</label>` |
| `<textarea>` | Многострочное поле ввода | `<textarea rows="4"></textarea>` |
| `<select>` | Выпадающий список | `<select><option>1</option></select>` |
| `<option>` | Элемент списка | `<option value="1">Первый</option>` |
| `<button>` | Кнопка | `<button>Нажми</button>` |
| `<fieldset>` | Группировка полей | `<fieldset><legend>Регистрация</legend>...</fieldset>` |
| `<legend>` | Заголовок группы | `<legend>Авторизация</legend>` |
| `<div>` | Блочный контейнер | `<div>Блок</div>` |
| `<span>` | Строчный контейнер | `<span style="color:red">красный</span>` |
| `<header>` | Шапка страницы | `<header>...</header>` |
| `<nav>` | Меню навигации | `<nav><a href="#">Ссылка</a></nav>` |
| `<main>` | Основное содержимое | `<main>...</main>` |
| `<section>` | Раздел страницы | `<section><h2>Новости</h2></section>` |
| `<article>` | Независимая статья | `<article>...</article>` |
| `<aside>` | Боковая панель | `<aside>Реклама</aside>` |
| `<footer>` | Подвал | `<footer>© 2025</footer>` |
| `<script>` | Вставка JavaScript | `<script>alert("Hi")</script>` |
| `<style>` | Встроенные стили CSS | `<style>p{color:red;}</style>` |
| `<link>` | Подключение стилей | `<link rel="stylesheet" href="style.css">` |
| `<base>` | Базовый URL | `<base href="https://site.com/">` |
| `<noscript>` | Контент, если JS отключён | `<noscript>Включите JavaScript</noscript>` |
