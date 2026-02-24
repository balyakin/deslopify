# Руководство по разработке плагинов (Instruction for LLMs)

## Введение
Этот документ содержит инструкции для языковых моделей (LLM) по созданию новых плагинов для статического анализатора `deslopify`. 
Ваша задача — писать чекеры, которые анализируют AST (Abstract Syntax Tree) и находят стилистические ошибки или "мусорный" код.

## СТРОГИЕ ПРАВИЛА ПРОЕКТА (CRITICAL)
При написании кода плагина ВЫ ОБЯЗАНЫ соблюдать следующие правила:
1. **Python 3.5:** Код должен быть строго совместим с Python 3.5.
2. **НЕТ f-строкам:** Использовать только метод `.format()`. Строго запрещено `f"..."`.
3. **Без комментариев в коде:** Запрещено писать комментарии (начинающиеся с `#`) внутри функций и методов. Вся логика должна быть понятна из имен переменных.
4. **Докстринги (Google Style):** Обязательны для классов и публичных методов. **В конце последнего предложения описания докстринга ТОЧКА НЕ СТАВИТСЯ**.
5. **Именование:** Переменные — существительные, функции — глаголы. Не использовать встроенное слово `id`. Имена должны быть длиннее 3 символов (кроме x, y и т.п.).
6. **Чистый код:** Никакой глубокой вложенности. Выносите проверки в переменные с понятными названиями.

## Структура плагина
Каждый плагин должен находиться в своей директории внутри `plugins/`:
```text
plugins/
└── <plugin_name>/
    ├── __init__.py
    ├── checker.py       # Код чекера
    ├── README.md        # Описание того, что делает плагин
    ├── example_pass.py  # Валидный код (чекер не должен находить ошибок)
    └── example_fail.py  # Плохой код (чекер ОБЯЗАН найти ошибку)
```

**ВАЖНО:** Каждый плагин обязан сопровождаться двумя тестовыми файлами `example_pass.py` и `example_fail.py`. Они используются скриптом `run_tests.py` для автоматической верификации (snapshot testing) того, что плагин работает корректно и не выдает ложных срабатываний.

## Интерфейс `BaseChecker`
Чекер должен наследоваться от `core.base_checker.BaseChecker` (который, в свою очередь, наследуется от `ast.NodeVisitor`). 

Базовый класс предоставляет методы:
- `self.add_error(file_path, line_number, message)`: Метод для регистрации найденной ошибки.
- `self.current_file`: Строка, содержащая путь к текущему обрабатываемому файлу (обновляется автоматически на Phase 1).

### Двухфазная архитектура анализа

Анализатор работает в два прохода, чтобы поддерживать как локальные, так и глобальные проверки.

#### Phase 1: Обход файлов (Локальный анализ)
Метод `process_file(filename, tree)` вызывается для каждого файла в проекте. Во время этой фазы чекер использует стандартные методы `ast.NodeVisitor` (например, `visit_FunctionDef`, `visit_ExceptHandler`).
- **Если проверка локальная** (ошибка видна в пределах одного AST-узла, например, `try/except pass`), вызывайте `self.add_error` прямо в методе `visit_...`.
- **Если проверка глобальная** (зависит от других файлов), используйте `visit_...` только для **сбора данных** в атрибуты класса (например, `self.declared_methods`, `self.accessed_attributes`). Обязательно сохраняйте `self.current_file` и `node.lineno` в эти структуры данных, чтобы потом указать точное место ошибки.
- **ОБЯЗАТЕЛЬНО:** Вызывайте `self.generic_visit(node)` в конце переопределенных методов `visit_...`, чтобы продолжить обход дочерних узлов.

#### Phase 2: Анализ проекта (Глобальный анализ)
Метод `finalize()` вызывается один раз после того, как все файлы проекта были обработаны.
- Здесь чекер должен проанализировать собранные словари/множества.
- Если обнаружена глобальная ошибка (например, "переменная объявлена, но ни разу не вызывалась"), вызывается `self.add_error(saved_file_path, saved_line, "Описание ошибки")`.

## Пример локального плагина (`plugins/try_except_pass/checker.py`)

```python
import ast
from core.base_checker import BaseChecker

class TryExceptPassChecker(BaseChecker):
    """Проверяет наличие блоков except, в которых используется только pass"""

    def visit_ExceptHandler(self, node):
        """Анализирует обработчики исключений

        Args:
            node: Узел AST

        Returns:
            None
        """
        has_one_statement = len(node.body) == 1
        is_pass_statement = isinstance(node.body[0], ast.Pass) if has_one_statement else False
        
        if has_one_statement and is_pass_statement:
            self.add_error(
                self.current_file,
                node.lineno,
                "Found try/except block with only 'pass'"
            )
            
        self.generic_visit(node)
```

## Пример глобального плагина (Псевдокод концепта)

```python
import ast
from core.base_checker import BaseChecker

class PrivateFieldChecker(BaseChecker):
    """Проверяет публичные поля, которые должны быть приватными"""

    def __init__(self):
        """Инициализирует структуры для сбора статистики по проекту"""
        super().__init__()
        self.declared_fields = {}
        self.accessed_fields = set()

    def visit_Attribute(self, node):
        """Собирает информацию об объявленных и используемых полях

        Args:
            node: Узел AST

        Returns:
            None
        """
        is_self_attribute = isinstance(node.value, ast.Name) and node.value.id == 'self'
        
        if is_self_attribute:
            self.declared_fields[node.attr] = (self.current_file, node.lineno)
        else:
            self.accessed_fields.add(node.attr)
            
        self.generic_visit(node)

    def finalize(self):
        """Анализирует собранные поля после обхода всех файлов

        Returns:
            None
        """
        for field_name, location_data in self.declared_fields.items():
            file_path, line_number = location_data
            is_public = not field_name.startswith('_')
            is_unused_externally = field_name not in self.accessed_fields
            
            if is_public and is_unused_externally:
                self.add_error(
                    file_path,
                    line_number,
                    "Public field '{0}' is never accessed externally, should be private".format(field_name)
                )
```
