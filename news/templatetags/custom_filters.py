from django import template

register = template.Library()

censure_list = ['пока', 'тут']


@register.filter()
def censure(string):
    for el in string.split():
        word = el.strip(',.:!@#№;$%^:&?*()-=+_/\\[]{}"<>')
        if word.lower() in censure_list:
            string = string.replace(word, f"{el[0]}{'*' * (len(word) - 1)}")
    return string
