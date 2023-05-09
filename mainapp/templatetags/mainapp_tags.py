from django import template

#хранение логики работы тегов

#экземпляр класс Library, через который происходит
#создание собственных шаблонных тегов
register = template.Library()

@register.simple_tag(name='get_day')
def get_articles(userqueryset, date):
   return userqueryset.filter(current_date=date)
   # if result == None: return ...
