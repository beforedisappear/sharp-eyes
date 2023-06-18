from django_hosts import patterns, host
from sharpeyes.settings import base

host_patterns = patterns(
   '',
   host(r'', base.ROOT_URLCONF, name=' '),
   host(r'abc', 'sharpeyes.admurls', name='admin')
)