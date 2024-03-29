def has_relation(model, serializers, value, many=False):
    if value is not None and not value:
        return None
    if value is None:
        return value

    if many:
        for instance_id in value:
            if not model.objects.filter(pk=instance_id).exists():
                raise serializers.ValidationError(f'{model.__name__} with ID {instance_id} does not exist.')
    else:
        if not model.objects.filter(pk=value).exists():
            raise serializers.ValidationError(f'{model.__name__} with ID {value} does not exist.')
