from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class TaggedItemManger(models.Manager):
    def get_tags_for(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)
        tagged_item = TaggedItem.objects.select_related('tag').filter(content_type=content_type, object_id=obj_id)
        return tagged_item


class Tag(models.Model):
    label = models.CharField(max_length=100)

    def __str__(self):
        return self.label


class TaggedItem(models.Model):
    objects = TaggedItemManger()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return self.tag

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
