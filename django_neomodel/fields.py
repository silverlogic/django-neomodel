from neomodel import properties

class UniqueIdProperty(properties.UniqueIdProperty):
    auto_created = False
    attname = "pk"
    name = "pk"


    # start a neomodel branch to fix this stuff
    
    def to_python(self, object_id):
        return str(object_id)
