import graphene

import budgetmanager.schema

class Query(budgetmanager.schema.Query, graphene.ObjectType):
    pass

class Mutation(budgetmanager.schema.Mutation, graphene.ObjectType):

    pass


schema = graphene.Schema(query=Query, mutation=Mutation)