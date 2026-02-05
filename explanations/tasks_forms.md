# Пояснення коду

## Як працює `clean_deadline` і куди повертається `deadline`

Де викликається `clean_deadline`
Ти **не викликаєш його вручну**.
Django робить це сам, коли відпрацьовує:
```
form.is_valid()
```

Всередині `is_valid()` відбувається:
1. Отримання даних з POST
2. Перевірка типів
3. Виклик `clean_<fieldname>` для кожного поля
4. Формування `cleaned_data`

### Що саме робить `clean_deadline`

```python
def clean_deadline(self):
    deadline = self.cleaned_data['deadline']
```

На цьому етапі:
- `deadline` уже **перетворений у Python date**
- формат валідний

Далі:

```python
if deadline < today:
    raise forms.ValidationError(...)
```

Якщо помилка:
- форма стає невалідною
- помилка зʼявляється біля поля `deadline`
- `form_valid` **не викликається**

### Куди повертається `deadline`

Він повертається в:

```python
form.cleaned_data['deadline']
```

А потім Django:
- використовує `cleaned_data`
- створює або оновлює обʼєкт `Task`

**Коротко:**
> `clean_deadline` перевіряє значення і повертає очищене значення назад у форму