from django import template

register = template.Library()


@register.filter()
def censor(censored_string):
    list_bad_words = ['Редиска', 'дурак', 'нехороший человек']
    for bad_word in list_bad_words:
        censored_string = censored_string.replace(bad_word, f"{bad_word[0]}{'*' * (len(bad_word) - 1)}")
    return f'{censored_string}'
