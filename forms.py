from django.forms import ModelForm
from django import forms
from models import RVGL, Campana2, Caida, Verificaciones, Evaluaciontc, Evaluacionpld, Seguimiento1, FlujOperativo, HipotecaSSFF, HipotecaConce, Moras
from adaptor.model import CsvDbModel

class UploadRVGL(forms.Form):
    rvgl = forms.FileField()

class RVGLCsv(CsvDbModel):
    class Meta:
        dbModel = RVGL
        delimiter = ","

#class UploadCampana(forms.Form):
    #campana = forms.FileField()

#class CampanaCsv(CsvDbModel):
    #class Meta:
        #dbModel = Campana
        #delimiter = ","

class UploadCampana2(forms.Form):
    campana2 = forms.FileField()

class Campana2Csv(CsvDbModel):
    class Meta:
        dbModel = Campana2
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

class UploadEvaluaciontc(forms.Form):
    evaluaciontc = forms.FileField()

class EvaluaciontcCsv(CsvDbModel):
    class Meta:
        dbModel = Evaluaciontc
        delimiter = ","

class UploadEvaluacionpld(forms.Form):
    evaluacionpld = forms.FileField()

class EvaluacionpldCsv(CsvDbModel):
    class Meta:
        dbModel = Evaluacionpld
        delimiter = ","

class UploadSeguimiento1(forms.Form):
    seguimiento1 = forms.FileField()

class Seguimiento1Csv(CsvDbModel):
    class Meta:
        dbModel = Seguimiento1
        delimiter = ","

class UploadFlujOperativo(forms.Form):
    flujoperativo = forms.FileField()

class FlujOperativoCsv(CsvDbModel):
    class Meta:
        dbModel = FlujOperativo
        delimiter = ","

class UploadHipotecaSSFF(forms.Form):
    hipotecassff = forms.FileField()

class HipotecaSSFFCsv(CsvDbModel):
    class Meta:
        dbModel = HipotecaSSFF
        delimiter = ","

class UploadHipotecaConce(forms.Form):
    hipotecaconce = forms.FileField()

class HipotecaConceCsv(CsvDbModel):
    class Meta:
        dbModel = HipotecaConce
        delimiter = ","

class UploadMoras(forms.Form):
    moras = forms.FileField()

class MorasCsv(CsvDbModel):
    class Meta:
        dbModel = Moras
        delimiter = ","

