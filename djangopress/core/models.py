from django.db import models

# Create your models here.

class Property(models.Model):
    name = models.CharField(max_length=50)
    value = models.TextField()
    value_type = models.CharField(max_length=1, choices=(('s','string'),('i','integer'),('b','boolean'), ('f', 'float')))

    def actual_value(self):
        types = {
            's': str, 
            'i': int,
            'f': float,
            'b': (lambda v: v.lower().startswith('t') or v.startswith('1'))
        }
        return types[self.value_type](self.value)