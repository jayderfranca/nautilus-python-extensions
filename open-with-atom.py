import os
from gi.repository import Nautilus, GObject


def which(program):
    def _is_exe(fd):
        return os.path.isfile(fd) and os.access(fd, os.X_OK)

    fpath, fname = os.path.split(program)

    if fpath:
        if _is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe = os.path.join(path, program)
            if _is_exe(exe):
                return exe
    return None


class OpenWithAtomExtension(GObject.GObject, Nautilus.MenuProvider):

    def __init__(self, *args, **kwargs):
        super(OpenWithAtomExtension, self).__init__(*args, **kwargs)
        self._location = which('atom')

    def _is_installed(self):
        return self._location is not None

    def _open_atom(self, item):
        os.system('%s %s' % (self._location, item.get_location().get_path()))

    def menu_activate_cb(self, _, item):
        self._open_atom(item)

    def menu_background_activate_cb(self, _, current_folder):
        self._open_atom(current_folder)

    def get_file_items(self, _, files):

        if not self._is_installed():
            return

        if len(files) != 1:
            return

        selected = files[0]
        item = Nautilus.MenuItem(name='Nautilus::open_with_atom_file',
                                 label='Open With Atom')
        item.connect('activate', self.menu_activate_cb, selected)
        return item,

    def get_background_items(self, _, current_folder):
        item = Nautilus.MenuItem(name='Nautilus::open_with_atom_background',
                                 label='Open With Atom')
        item.connect('activate', self.menu_background_activate_cb, current_folder)
        return item,
