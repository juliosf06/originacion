from __future__ import unicode_literals

from django.db import models

class Segment(models.Model):
    nombre = models.Charfield(max_length=100)

class Campana(models.Model)
    codigo_campana = models.Charfield(max_length=100)
    
