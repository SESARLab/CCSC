import colander

class Level(colander.MappingSchema):
    rank = colander.SchemaNode(colander.Int())
    p=colander.SchemaNode(colander.Float())

class Levels(colander.SequenceSchema):
    level = Level()

class Property(colander.MappingSchema):
    name = colander.SchemaNode(colander.String())
    levels = Levels()

class Properties(colander.SequenceSchema):
    property = Property()


class Functionality(colander.MappingSchema):
    function = colander.SchemaNode(colander.String())

class Functionalities(colander.SequenceSchema):
    function = Functionality()