from django.template import Library
import time

def formatDate(value):
    t = time.localtime(value)
    return "%d/%d/%d %d:%d"%(t.tm_mday,t.tm_mon,t.tm_year, t.tm_hour,t.tm_min)

register = Library()
register.filter('formatDate', formatDate)