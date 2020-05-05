from datetime import datetime
from django.db import models
from django.db.models import QuerySet

from custom.exception import CustomException


class CustomQuerySet(QuerySet):

    def delete(self):
        self.update(delete_at=datetime.now())


class BaseManager(models.Manager):
    """
    仅返回未被删除的实例
    """
    _queryset_class = CustomQuerySet

    def get_queryset(self):
        """
        在这里处理一下QuerySet, 然后返回没删除的
        """
        kwargs = {'model': self.model, 'using': self._db}
        if hasattr(self, '_hints'):
            kwargs['hints'] = self._hints

        return self._queryset_class(**kwargs).filter(delete_at=None)

    def get_or_404(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except Exception as e:
            raise CustomException(code=4004, message='没有找到该资源')


class BaseModel(models.Model):

    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    delete_at = models.DateTimeField(null=True, blank=True, verbose_name='删除时间')

    objects = BaseManager()

    def delete(self, using=None, soft=True, *args, **kwargs):
        """
        Soft delete object (set its ``is_deleted`` field to True).
        Actually delete object if setting ``soft`` to False.
        """
        if soft:
            self.delete_at = datetime.now()
            self.save(using=using)
        else:
            return super().delete(using=using, *args, **kwargs)

    class Meta:
        abstract = True
