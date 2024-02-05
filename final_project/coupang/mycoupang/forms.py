# forms.py
from django import forms
from .models import ReviewsTable

class ArticleForm(forms.ModelForm):
    제품 = forms.ChoiceField(choices=[], initial='', widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = ReviewsTable
        fields = ('제품', 'review_contents')
        widgets = {
            'review_contents': forms.Textarea(attrs={'class': 'form-control', 'id': 'id_review_contents'}),
        }
        labels = {
            'review_contents': '리뷰내용',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Dynamically set choices for category1, category2, and 제품
        
        self.fields['제품'].choices = ReviewsTable.objects.values_list('product_name', 'product_name').distinct()
        
class PredictForm(forms.ModelForm):

    class Meta:
        model = ReviewsTable
        fields = ('review_contents', )
        widgets = {
            'review_contents': forms.Textarea(attrs={'class': 'form-control', 'id': 'id_review_contents'}),
        }
        labels = {
            'review_contents': '리뷰내용',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Dynamically set choices for category1, category2, and 제품
        