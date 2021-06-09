from neomodel import properties


class Property(properties.Property):
    is_relation = False
    many_to_many = False
    primary_key = False
    one_to_one = False
    unique = False
    null = False
    remote_field = False
    concrete = True

    # These track each time a Property instance is created. Used to retain order.
    # The auto_creation_counter is used for fields that Django implicitly
    # creates, creation_counter is used for all user-specified fields.
    creation_counter = 0
    auto_creation_counter = -1

    def __init__(self, *args, auto_created=False, **kwargs):
        super().__init__(*args, auto_created=auto_created, **kwargs)
        # Adjust the appropriate creation counter, and save our local copy.
        if auto_created:
            self.creation_counter = Property.auto_creation_counter
            Property.auto_creation_counter -= 1
        else:
            self.creation_counter = Property.creation_counter
            Property.creation_counter += 1

    def __eq__(self, other):
        # Needed for @total_ordering
        if isinstance(other, Property):
            return (
                self.creation_counter == other.creation_counter and
                getattr(self, 'model', None) == getattr(other, 'model', None)
            )
        return NotImplemented

    def __lt__(self, other):
        # This is needed because bisect does not take a comparison function.
        # Order by creation_counter first for backward compatibility.
        if isinstance(other, Property):
            if (
                self.creation_counter != other.creation_counter or
                not hasattr(self, 'model') and not hasattr(other, 'model')
            ):
                return self.creation_counter < other.creation_counter
            elif hasattr(self, 'model') != hasattr(other, 'model'):
                return not hasattr(self, 'model')  # Order no-model fields first
            else:
                # creation_counter's are equal, compare only models.
                return (
                    (self.model._meta.app_label, self.model._meta.model_name) <
                    (other.model._meta.app_label, other.model._meta.model_name)
                )
        return NotImplemented

    def contribute_to_class(self, cls, name, private_only=False):
        self.name = name
        self.attname = name
        self.column = name
        self.model = cls
        print(name, cls)
        cls._meta.add_field(self, private=private_only)
        if self.column:
            # Don't override classmethods with the descriptor. This means that
            # if you have a classmethod and a field with the same name, then
            # such fields can't be deferred (we don't have a check for this).
            if not getattr(cls, self.attname, None):
                setattr(cls, self.attname, self)
        #  import pdb; pdb.set_trace()

    def get_attname_column(self):
        return None, self.db_property

    def check(self, **kwargs):
        print("check")
        print(kwargs)
        return []
    
    def get_default(self):
        return None


class UniqueIdProperty(properties.UniqueIdProperty, Property):
    primary_key = True
    auto_created = False
    attname = "id"
    name = "id"
    unique = True
    null = False

    # start a neomodel branch to fix this stuff
    
    def to_python(self, object_id):
        return str(object_id)


class StringProperty(properties.StringProperty, Property):
    pass
