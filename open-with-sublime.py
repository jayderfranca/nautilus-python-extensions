import os
from gi.repository import Nautilus, GObject


class OpenWithSublimeExtension(GObject.GObject, Nautilus.MenuProvider):

    def __init__(self, *args, **kwargs):
        super(OpenWithSublimeExtension, self).__init__(*args, **kwargs)
        self._location = "/opt/sublime_text/sublime_text"

    def _is_installed(self):
        return self._location is not None

    def _open_sublime(self, item):
        os.system('%s %s' % (self._location, item.get_location().get_path()))

    def _new_menu_nautilus(self, name, file, callback):

        if not self._is_installed():
            return

        if file.get_uri_scheme() != 'file':
            return

        item = Nautilus.MenuItem(name='OpenWithSublimeExtension::' + name,
                                 label='Open With Sublime')

        item.connect('activate', callback, file)
        return item,

    def menu_activate_cb(self, _, item):
        self._open_sublime(item)

    def menu_background_activate_cb(self, _, current_folder):
        self._open_sublime(current_folder)

    def get_file_items(self, _, files):
        if len(files) == 1:
            return self._new_menu_nautilus("File", files[0], self.menu_activate_cb)

    def get_background_items(self, _, current_folder):
        return self._new_menu_nautilus("Background", current_folder, self.menu_background_activate_cb)
