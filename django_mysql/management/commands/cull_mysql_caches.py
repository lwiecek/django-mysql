# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.core.cache import InvalidCacheBackendError, caches
from django.core.management import BaseCommand, CommandError

from django_mysql.cache import MySQLCache
from django_mysql.utils import collapse_spaces


class Command(BaseCommand):
    args = "<optional cache aliases>"

    help = collapse_spaces("""
        Runs cache.cull() on all your MySQLCache caches, or only those
        specified aliases.
    """)

    def handle(self, *aliases, **options):
        verbosity = options.get('verbosity')

        if aliases:
            names = set(aliases)
        else:
            names = settings.CACHES

        for alias in names:
            try:
                cache = caches[alias]
            except InvalidCacheBackendError:
                raise CommandError("Cache '{}' does not exist".format(alias))

            if not isinstance(cache, MySQLCache):  # pragma: no cover
                continue

            if verbosity >= 1:
                self.stdout.write(
                    "Deleting from cache '{}'... ".format(alias),
                    ending=''
                )
            num_deleted = cache.cull()
            if verbosity >= 1:
                self.stdout.write("{} entries deleted.".format(num_deleted))
