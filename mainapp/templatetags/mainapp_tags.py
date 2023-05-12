from django import template

#хранение логики работы тегов

#экземпляр класс Library, через который происходит
#создание собственных шаблонных тегов
register = template.Library()
