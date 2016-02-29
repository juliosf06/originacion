from django.forms import ModelForm
from django import forms
from models import RVGL
from adaptor.model import CsvDbModel

class UploadRVGL(forms.Form):
    rvgl = forms.FileField()

class RVGLCsv(CsvDbModel):
    class Meta:
        dbModel = RVGL
        delimiter = ","
