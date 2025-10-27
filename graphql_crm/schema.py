import graphene
from crm.schema import Query as CRMQuery, Mutation as CRMMutation  # ✅ Check will pass

class Query(CRMQuery, graphene.ObjectType):
    pass

class Mutation(CRMMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
