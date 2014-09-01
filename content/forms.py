from django import forms
from content.models import Post
from ranking.models import Stock


class PostForm(forms.Form):
    MAX_SYMBOL_LENGTH = 10

    post_type = forms.ChoiceField(
        label=False,
        initial='link',
        choices=Post.POST_TYPES,
        required=True,
        widget=forms.RadioSelect(
            attrs={
                'class': 'sr-only'
            }
        )
    )

    symbol = forms.CharField(
        required=True,
        max_length=10,
        label='Stock Symbol',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Lookup',
                'class': 'form-control typeahead stock-symbol-box',
        }),
        error_messages={
            'required': 'NYSE and NASDAQ stock symbols only',
            'max_length': 'Please enter a valid stock symbol'
        }
    )

    trend = forms.ChoiceField(
        required=True,
        choices=Post.TREND_TYPES,
        label='Trend',
        initial='bull',
        widget=forms.RadioSelect(
            attrs={
                'class': 'sr-only'
            }
        )
    )

    title = forms.CharField(
        max_length=200,
        label='Title',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter title of your link or article',
                'class': 'form-control'
        }),
        error_messages={
            'required': 'Please enter a title of your link or article.',
            'max_length': 'Title must be less than 200 characters.'
        }
    )

    url = forms.URLField(
        required=False,
        max_length=1000,
        label='URL',
        widget=forms.URLInput(
            attrs={
                'placeholder': 'http://www.example.com',
                'class': 'form-control'
        }),
        error_messages={
            'max_length': 'URL must be less than 1000 characters.'
        }
    )
    summary = forms.CharField(
        label='Summary',
        required=False,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Add optional summary',
                'class': 'form-control',
                'rows': '3'
        })
    )

    text = forms.CharField(
        label='Text',
        required=False,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Write article text (optional)',
                'class': 'form-control',
                'rows': '10'
        })
    )

    def clean_symbol(self):
        symbol = self.cleaned_data['symbol'].upper()
        if len(symbol) > self.MAX_SYMBOL_LENGTH:
            raise forms.ValidationError(
                'Please enter a valid stock symbol.',
                'invalid'
            )
        try:
            stock = Stock.objects.get(symbol=symbol)
        except Stock.DoesNotExist:
            raise forms.ValidationError(
                'Not a NYSE or NASDAQ stock.',
                code='invalid'
            )
        return symbol

    def clean_url(self):
        post_type = self.cleaned_data['post_type']
        url = self.cleaned_data['url']

        if post_type == 'link' and not url:
            raise forms.ValidationError(
                'Please enter an URL.',
                code='required'
            )

        return url

    #TODO: Mark previous posts with same ticker inactive with alert