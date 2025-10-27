INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'graphene_django',
    'crm',
]

GRAPHENE = {
    "SCHEMA": "alx_backend_graphql_crm.schema.schema"
}

# Usual Django configurations below

