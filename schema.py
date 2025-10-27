import graphene
from crm.schema import Query as CrmQuery

class Query(CrmQuery, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)

