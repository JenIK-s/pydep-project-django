# Установка и настройка Editor.js

## ✅ Текущий статус: Editor.js уже настроен и готов к использованию!

Editor.js подключен через CDN в шаблоне `lesson_edit.html` и полностью функционален.

## Вариант 1: Использование CDN (Текущий вариант - уже настроен) ✅

Editor.js уже подключен через CDN в шаблоне `lesson_edit.html`. Это самый простой способ, который работает "из коробки".

### Преимущества:
- ✅ Не требует установки
- ✅ Всегда актуальные версии
- ✅ Быстрая настройка
- ✅ Работает сразу

### Недостатки:
- ⚠️ Требует интернет-соединение
- ⚠️ Зависит от внешнего CDN

### Что уже настроено:
1. ✅ Editor.js подключен через CDN
2. ✅ Все необходимые плагины подключены:
   - Header (заголовки)
   - List (списки)
   - Image (изображения) - с endpoint для загрузки
   - Code (код)
   - Quote (цитаты)
   - Delimiter (разделитель)
   - Table (таблицы)
   - Checklist (чеклисты)
3. ✅ Endpoint для загрузки изображений (`/lesson/upload-image/`)
4. ✅ Сохранение блоков в JSON формате
5. ✅ Отображение блоков в шаблоне урока

## Вариант 2: Локальная установка через npm (Рекомендуется для продакшена)

### Шаг 1: Установка зависимостей

```bash
cd /Users/jeniks/Dev/pydep-project-django
npm init -y  # если package.json еще нет
npm install @editorjs/editorjs
npm install @editorjs/header
npm install @editorjs/list
npm install @editorjs/image
npm install @editorjs/code
npm install @editorjs/quote
npm install @editorjs/delimiter
npm install @editorjs/table
npm install @editorjs/checklist
```

### Шаг 2: Копирование файлов в static

```bash
# Создаем директорию для Editor.js
mkdir -p pydep/static/editorjs

# Копируем файлы из node_modules
cp node_modules/@editorjs/editorjs/dist/bundle.js pydep/static/editorjs/
cp node_modules/@editorjs/editorjs/dist/bundle.css pydep/static/editorjs/

# Копируем плагины
cp node_modules/@editorjs/header/dist/bundle.js pydep/static/editorjs/header.js
cp node_modules/@editorjs/list/dist/bundle.js pydep/static/editorjs/list.js
cp node_modules/@editorjs/image/dist/bundle.js pydep/static/editorjs/image.js
cp node_modules/@editorjs/code/dist/bundle.js pydep/static/editorjs/code.js
cp node_modules/@editorjs/quote/dist/bundle.js pydep/static/editorjs/quote.js
cp node_modules/@editorjs/delimiter/dist/bundle.js pydep/static/editorjs/delimiter.js
cp node_modules/@editorjs/table/dist/bundle.js pydep/static/editorjs/table.js
cp node_modules/@editorjs/checklist/dist/bundle.js pydep/static/editorjs/checklist.js
```

### Шаг 3: Обновление шаблона

После копирования файлов нужно обновить `lesson_edit.html` для использования локальных файлов вместо CDN.

## Вариант 3: Использование webpack/rollup для сборки (Продвинутый)

Можно собрать все в один bundle.js файл для оптимизации.

## Текущая конфигурация

Сейчас используется **Вариант 1 (CDN)**, который уже настроен и работает.

## Дополнительные плагины Editor.js

Если нужно добавить больше возможностей:

```bash
npm install @editorjs/link          # Ссылки
npm install @editorjs/embed         # Встраивание видео
npm install @editorjs/warning       # Предупреждения
npm install @editorjs/marker        # Выделение текста
npm install @editorjs/inline-code   # Инлайн код
npm install @editorjs/underline      # Подчеркивание
```

## Настройка загрузки изображений

Для работы плагина Image нужно создать endpoint для загрузки файлов. См. инструкции в коде.

