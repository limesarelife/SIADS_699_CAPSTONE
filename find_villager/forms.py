from django import forms

class VillagerForm(forms.Form):
    yourname = forms.CharField(max_length=100, required=True)
    species = forms.CharField(max_length=100, required=True)
    personality = forms.CharField(max_length=100, required=True)
    hobby = forms.CharField(max_length=100, required=True)
    astrological = forms.CharField(max_length=100, required=True)
    music = forms.CharField(max_length=100, required=True)
    style1 = forms.CharField(max_length=100, required=True)
    style2 = forms.CharField(max_length=100, required=True)
    color1 = forms.CharField(max_length=100, required=True)
    color2 = forms.CharField(max_length=100, required=True)

class VillagerResponse(forms.Form):
    villager_option = forms.CharField(max_length=100, required=True)
    villager_why = forms.CharField(max_length=800, required=True)
    

