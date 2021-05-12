from neomodel import properties

class UniqueIdProperty(properties.UniqueIdProperty):
    auto_created = False
    attname = "id"
