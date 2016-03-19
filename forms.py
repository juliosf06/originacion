from django.forms import ModelForm
from django import forms
from models import RVGL, Campana, Caida, Verificaciones
from adaptor.model import CsvDbModel

class UploadRVGL(forms.Form):
    rvgl = forms.FileField()

class RVGLCsv(CsvDbModel):
    class Meta:
        dbModel = RVGL
        delimiter = ","

class UploadCampana(forms.Form):
    campana = forms.FileField()

class CampanaCsv(CsvDbModel):
    class Meta:
        dbModel = Campana
        delimiter = ","

class UploadCaida(forms.Form):
    caidas = forms.FileField()

class CaidaCsv(CsvDbModel):
    class Meta:
        dbModel = Caida
        delimiter = ","

class UploadVerificaciones(forms.Form):
    verificaciones = forms.FileField()

class VerificacionesCsv(CsvDbModel):
    class Meta:
        dbModel = Verificaciones
        delimiter = ","
