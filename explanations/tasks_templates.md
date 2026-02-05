
### Чому в шаблоні `task_confirm_delete.html` є `object`

#### Звідки взявся `object`

Це стандартна поведінка **DeleteView**.

```python
class TaskDeleteView(DeleteView):
```

DeleteView автоматично:
- отримує обʼєкт по `pk`
- кладе його в context під іменем:
    - `object`

Тобто Django робить:
```python
context = {
    'object': task
}
```


**Тому в шаблоні можна писати**
`{{ object.title }}`

**Аналогія:**
У ListView є `object_list`,
у DetailView - `object`,
у DeleteView - теж `object`.

#### Де описана логіка кнопки "Yes, delete"

**Кнопка**

```html
<form method="post">
    {% csrf_token %}
    <button type="submit">Yes, delete</button>
</form>
```

Тут:
- форма без `action`
- відправляється POST **на той самий URL**

**Що відбувається далі**

1. Користувач натискає кнопку
2. Відправляється POST-запит
3. Django потрапляє в `TaskDeleteView`
4. DeleteView викликає метод:
    - `post()`
5. Усередині `post()`:
    - викликається `delete()`
    - обʼєкт видаляється з БД
6. Після цього:
    - redirect на `success_url`

**Чому ми не пишемо це вручну**

Тому що `DeleteView` вже реалізує:
- отримання обʼєкта
- перевірку прав
- видалення
- редірект

**Ми керуємо тільки:**
- моделлю
- шаблоном
- success_url
- правами доступу
