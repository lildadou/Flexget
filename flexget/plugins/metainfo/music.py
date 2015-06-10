from __future__ import unicode_literals, division, absolute_import
import logging
from flexget.plugins.parsers.music.parser_guessit_music import ParserGuessitMusic

from flexget.plugins.parsers.parser_common import normalize_name, remove_dirt
from flexget import plugin
from flexget.event import event
from flexget.plugin import get_plugin_by_name


log = logging.getLogger('metainfo_music')


class MetainfoMusic(object):
    schema = {'type': 'boolean'}

    @plugin.priority(120)
    def on_task_metainfo(self, task, config):
        if config is False:
            return
        for entry in task.entries:
            # If series plugin already parsed this, don't touch it.
            if entry.get('music_title'):
                continue
            self.guess_entry(entry)


    def guess_entry(self, entry, config=None):
        """
        Populates music_* fields for entries that are successfully parsed.

        :param dict config: A series config to be used. This will also cause 'path' and 'set' fields to be populated.
        """
        if entry.get('music_parser') and entry['music_parser'].valid:
            # Return true if we already parsed this, false if series plugin parsed it
            return entry.get('music_guessed')

        parsed = get_plugin_by_name('parsing').instance.parse_music(data=entry['title'])
        if parsed and parsed.valid:
            parsed.name = normalize_name(remove_dirt(parsed.name))
            entry.update_using_map(ParserGuessitMusic.get_entry_map(), parsed)
            entry['music_guessed'] = True
            log.debug("'%s' successfully parsed" % entry['title'])
            return True
        else:
            log.info("Unable to parse '%s'" % entry['title'])
            return False


@event('plugin.register')
def register_plugin():
    plugin.register(MetainfoMusic, 'music', api_ver=2)
