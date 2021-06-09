from datetime import datetime

from django.db import models
from django.db.models.base import ModelBase
from django_neomodel import DjangoNode
from django_neomodel.models import NeoModel
from django_neomodel.fields import StringProperty
from neomodel import DateTimeProperty, UniqueIdProperty
from neomodel.core import NodeMeta
from neomodel.match import NodeSet


class Library(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        app_label = 'someapp'


class NeoManager:
    def __init__(self, model):
        self.model = model

    #  def __new__(cls, *args, **kwargs):
    #      print(cls)
    #      print(args)
    #      print(kwargs)
    #      return super().__new__(cls)

    def get_queryset(self):
        return NeoNodeSet(self.model)


class FakeOpt:
    attname = 'faked'


class Metaclass(NodeMeta):
    pk = FakeOpt()

    def __new__(cls, *args, **kwargs):
        super_new = super().__new__
        print(cls)
        print(args)
        print(kwargs)
        new_cls = super_new(cls, *args, **kwargs)
        setattr(new_cls, "_default_manager", NeoManager(new_cls))
        return new_cls

    #  @property
    #  def _default_manager(cls):
    #      print("_default_manager", cls)
    #      return NeoManager(cls)


#  DjangoNodeWithAdmin = Metaclass('DjangoNodeWithAdmin', (DjangoNode,), {'__abstract_node__': True})


#  class Book(DjangoNodeWithAdmin):
#      uid = UniqueIdProperty()
#      pk = UniqueIdProperty(primary_key=True)
#      title = StringProperty(unique_index=True)
#      format = StringProperty(required=True)  # check required field can be omitted on update
#      status = StringProperty(choices=(
#              ('available', 'A'),
#              ('on_loan', 'L'),
#              ('damaged', 'D'),
#          ), default='available', coerce=str)
#      created = DateTimeProperty(default=datetime.utcnow)

#      class Meta:
#          verbose_name = "Book"
#          verbose_name_plural = "Books"

#      #  _default_manager = NeoManager()

#      def serializable_value(self, attr):
#          return str(getattr(self, attr))

#      class Meta:
#          app_label = 'someapp'


class Book(NeoModel):
    title = StringProperty(unique_index=True)
