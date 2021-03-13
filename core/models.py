from django.db import models


class Bling(models.Model):
    """
    Different accounts of Bling ERP.
    Fields:
        name (str): Name given to Bling Account
        api_key (str): API key provided by Bling
     """
    name = models.CharField(max_length=20)
    api_key = models.CharField(max_length=100)

    def __str__(self):
        return self.name
