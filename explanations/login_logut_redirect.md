# Після Logout перенаправляти на Login

### Налаштування в `settings.py`:

```python
LOGOUT_REDIRECT_URL = "login"
```

Цього достатньо, якщо ви використовуєте `include('django.contrib.auth.urls')` і стандартний logout.

### Далі зробіть Logout через POST (правильний варіант)

У **Django 5.x** стандартний logout з `django.contrib.auth.urls` за замовчуванням працює через **POST** (це зроблено з міркувань безпеки). А у вас в навігації, ймовірно, стоїть лінк:

```html
<a href="{% url 'logout' %}">Logout</a>
```

Лінк завжди робить GET - тому і 405.
Нижче правильне рішення.

В `base.html` замініть лінк Logout на форму

```html
<form method="post" action="{% url 'logout' %}" style="display:inline;">
  {% csrf_token %}
  <button type="submit">Logout</button>
</form>

```

Тепер logout буде відправляти POST - і 405 зникне.

Після натискання кнопки Logout:
1. буде POST на `/accounts/logout/`
2. Django розлогінить користувача
3. зробить redirect на `login`

---
# Налаштуйте редірект після логіну

Після логіну Django **за замовчуванням** може редіректити туди, що ви вказали як `LOGIN_REDIRECT_URL`.
У Django **історично** (і досі в коді) дефолтне значення вказує на `/accounts/profile/`, а ми хочемо на **список задач**.

Зробіть так.

У `settings.py` **явно вкажіть**:

```python
LOGIN_REDIRECT_URL = "task-list"
```

Це означає:
- після успішного логіну Django зробить `redirect(reverse("task-list"))`

### (Рекомендовано) Куди редіректити, якщо користувач НЕ залогінений

Щоб логіка була послідовна, додайте також:

```python
LOGIN_URL = "login"
```

Тоді:
- якщо користувач відкриє сторінку задач без логіну
- Django перенаправить його на `/accounts/login/`
- після логіну він потрапить на `task-list`
