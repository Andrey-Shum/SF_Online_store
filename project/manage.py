#!/usr/bin/env python
"""Утилита командной строки Django для административных задач."""
import os
import sys
print(sys.path)


def main():
    """Выполнять административные задачи."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
    print(f"Использование модуля настроек: {os.environ['DJANGO_SETTINGS_MODULE']}")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Не удалось импортировать Django. Вы уверены, что оно установлено "
            "и доступно в вашей переменной среды PYTHONPATH? "
            "Вы забыли активировать виртуальную среду?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
