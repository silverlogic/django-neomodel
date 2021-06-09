from django.db import models as dj_models
from django.utils.functional import cached_property

from neomodel.core import NodeMeta, StructuredNode
from neomodel.properties import Property

from .fields import UniqueIdProperty
from .manager import NodeModelManager


class BaseManagerBase:
    @cached_property
    def base_manager(self):
        import pdb; pdb.set_trace()
        # almost all of this function is copied from Django itself
        base_manager_name = self.base_manager_name
        if not base_manager_name:
            # Get the first parent's base_manager_name if there's one.
            for parent in self.model.mro()[1:]:
                if hasattr(parent, '_meta'):
                    if parent._base_manager.name != '_base_manager':
                        base_manager_name = parent._base_manager.name
                    break

        if base_manager_name:
            try:
                return self.managers_map[base_manager_name]
            except KeyError:
                raise ValueError(
                    "%s has no manager named %r" % (
                        self.object_name,
                        base_manager_name,
                    )
                )

        manager = NodeModelManager()
        manager.name = '_base_manager'
        manager.model = self.model
        manager.auto_created = True
        return manager


class NeoModelBase(BaseManagerBase, type(dj_models.Model), NodeMeta):
    def __new__(cls, name, bases, attrs,*args, **kwargs):
        super_new = super().__new__
        new_cls = super_new(cls, name, bases, attrs, *args, **kwargs)
        #  import pdb; pdb.set_trace()
        #  setattr(new_cls, "_default_manager", NodeModelManager(new_cls))
        if not new_cls._meta.abstract:
            new_cls._meta.pk = new_cls.id

        return new_cls


class DjangoNeoModel(dj_models.Model, StructuredNode, metaclass=NeoModelBase):
    __abstract_node__ = True

    class Meta:
        abstract = True
        #  default_manager = NodeModelManager


class NeoModel(DjangoNeoModel):
    objects = NodeModelManager()
    #  _default_manager = NodeModelManager()
    id = UniqueIdProperty(db_property="id")
    #  pk = UniqueIdProperty(db_property="id")

    __abstract_node__ = True

    class Meta:
        abstract = True

    @classmethod
    def defined_properties(cls, **kwargs):
        props = super().defined_properties(**kwargs)        
        #  import pdb; pdb.set_trace()
        return props
