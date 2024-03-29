def has_relation(model, serializers, value, many=False):
    if many:
        if value is not None:
            for instance_id in value:
                if not model.objects.filter(pk=instance_id).exists():
                    raise serializers.ValidationError(f'{model.__name__} with ID {instance_id} does not exist.')
        return value

    if value is not None:
        if not model.objects.filter(pk=value).exists():
            raise serializers.ValidationError(f'{model.__name__} with ID {value} does not exist.')
    return value
