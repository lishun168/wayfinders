from django.db import models

class SearchObject(models.Model):
    reference_type = models.IntegerField()
    url = models.IntegerField()
    description = models.CharField(max_length=255)

class SearchTags(models.Model):
    tag = models.CharField(max_length=255)
    search_object = models.ForeignKey(SearchObject, on_delete=models.CASCADE)


