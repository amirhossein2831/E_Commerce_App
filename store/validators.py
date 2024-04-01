from django.core.exceptions import ValidationError


def validate_file_size(file):
    max_size_kb = 100

    if file.size > max_size_kb * 1024:
        raise ValidationError(f'the file size should be less than {max_size_kb} KB')
