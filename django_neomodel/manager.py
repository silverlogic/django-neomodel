from django.db import models
from django.db.models.query import EmptyQuerySet

#  from neo4django.decorators import not_implemented
#  from query import NodeQuerySet
from neomodel.match import NodeSet


class FakeQuery:
    select_related = False
    order_by = ['id']


class NeoNodeSet(NodeSet):
    query = FakeQuery()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = self.source

    #  def order_by(self, *fields):
    #      return self

    def count(self):
        return 1

    def _clone(self):
        return self


class NodeModelManager(models.Manager):
    def __init__(self, *args, **kwargs):
        print("NodeModelManager")
        print(args)
        print(kwargs)
        super(NodeModelManager, self).__init__()
        #  print(self.source)
        self._using = None
        self.model = None
        self._inherited = False

    #  @not_implemented
    def _insert(self, values, **kwargs):
        pass

    #  @not_implemented
    def _update(self, values, **kwargs):
        pass

    def get_empty_query_set(self):
        return EmptyQuerySet()

    #  @not_implemented
    def exclude(self, *args, **kwargs):
        pass

    def get_queryset(self):
        print("get_queryset")
        print(self.model)
        return NeoNodeSet(self.model)
        #  return NodeQuerySet(self.model)

    #  def all(self):
    #      return self.get_query_set()

    #  def get(self, *args, **kwargs):
    #      return self.get_query_set().get(*args, **kwargs)

    #  def dates(self, *args, **kwargs):
    #      return self.get_query_set().dates(*args, **kwargs)

    #  def create(self, **kwargs):
    #      return self.get_query_set().create(**kwargs)

    #  def filter(self, *args, **kwargs):
    #      return self.get_query_set().filter(*args, **kwargs)

