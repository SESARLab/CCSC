import colander


class Certification(colander.MappingSchema):
    property=colander.SchemaNode(colander.String())
    rank=colander.SchemaNode(colander.Int())

class Certifications(colander.SequenceSchema):
    cert=Certification()

class Composition(colander.MappingSchema):
    feauture=colander.SchemaNode(colander.String())
    certs=Certifications()

class Compositions(colander.SequenceSchema):
    composition=Composition()

class Request(colander.MappingSchema):
    id=colander.SchemaNode(colander.Int())
    compostitions=Compositions()

class Requests(colander.SequenceSchema):
    request = Request()