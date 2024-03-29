# hw05_final

### Описание
Сообщество для публикаций. Блог с возможностью публикации постов, подпиской на группы и авторов, а также комментированием постов.

## Cтек проекта
Python v3.9, Django

## Как запустить проект:

1. Клонируйте репозиторий и перейдите в него в командной строке:

```
git clone git@github.com:VladislavYar/hw05_final.git
```

```
cd hw05_final
```

2. Установите и активируйте виртуальное окружение
```
python -m venv venv
``` 
```
source venv/Scripts/activate
```

3. Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
```

4. В папке с файлом manage.py выполните миграции:
```
python manage.py migrate
```

5. В папке с файлом manage.py запустите сервер, выполнив команду:
```
python manage.py runserver
```

### Что могут делать пользователи:

Залогиненные пользователи могут:
1. Просматривать, публиковать, удалять и редактировать свои публикации;
2. Просматривать информацию о сообществах;
3. Просматривать и публиковать комментарии от своего имени к публикациям других пользователей (включая самого себя), удалять и редактировать свои комментарии;
4. Подписываться на других пользователей и просматривать свои подписки.<br/>
Примечание: Доступ ко всем операциям записи, обновления и удаления доступны только после аутентификации и получения токена.

Анонимные пользователи могут:
1. Просматривать публикации;
2. Просматривать информацию о сообществах;
3. Просматривать комментарии;
