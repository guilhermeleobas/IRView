import sublime
import sublime_plugin
import os
from subprocess import Popen, PIPE

settings_file = 'IRView.sublime-settings';

def get_opt():
  return os.path.expanduser(
    os.path.expandvars(sublime.load_settings(settings_file).get('opt')))

def cp_to_tmp(filename):
  cmd = ['cp', filename, '/tmp']
  p = Popen(cmd, stdout=PIPE, stderr=PIPE)

  output, err = p.communicate()
  if err:
    print('Error while moving {} to /tmp'.format(filename))

  return '/tmp/' + os.path.basename(filename)

def create_dots(opt, filename, pass_name):
  cmd = [opt, filename, pass_name, '-disable-output']
  p = Popen(cmd, stdout=PIPE, stderr=PIPE)

  output, err = p.communicate()

  files = err.decode("utf-8")\
    .replace("Writing ", "").replace("'", "")\
    .strip('...\n').split('...\n')\

  return list(map(lambda x: '/tmp/' + x, files))

def create_pdfs(dotfiles):
  for f in dotfiles:
    basename = os.path.basename(f)
    cmd = ['dot', '-Tpdf', f, '-o', '/tmp/' + basename + '.pdf']
    Popen(cmd, stdout=None, stderr=None).communicate()

  return ['/tmp/' + os.path.basename(f) + '.pdf' for f in dotfiles]

def open_pdfs(pdfs):
  for pdf in pdfs:
    cmd = ['open', pdf]
    Popen(cmd, stdout=None, stderr=None).communicate()

def view(filename, pass_name):
  opt = get_opt()
  filename = cp_to_tmp(filename)
  os.chdir('/tmp')
  dots = create_dots(opt, filename, pass_name)
  pdfs = create_pdfs(dots)
  open_pdfs(pdfs)

###
class IrViewCallGraphCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    filename = self.view.file_name()
    view(filename, '-dot-callgraph')

###
class IrViewCfgCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    filename = self.view.file_name()
    view(filename, '-dot-cfg')

class IrViewCfgOnlyCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    filename = self.view.file_name()
    view(filename, '-dot-cfg-only')

###
class IrViewDomCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    filename = self.view.file_name()
    view(filename, '-dot-dom')

class IrViewDomOnlyCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    filename = self.view.file_name()
    view(filename, '-dot-dom-only')

###
class IrViewPostdomCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    filename = self.view.file_name()
    view(filename, '-dot-postdom')

class IrViewPostdomOnlyCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    filename = self.view.file_name()
    view(filename, '-dot-postdom-only')

###
class IrViewRegionsCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    filename = self.view.file_name()
    view(filename, '-dot-regions')

class IrViewRegionsOnlyCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    filename = self.view.file_name()
    view(filename, '-dot-regions-only')

###


class IrViewSetPathCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    w = sublime.active_window()
    w.show_input_panel("Path to opt: ", "", set_path, None, None)

  def set_path(value):
    settings = sublime.load_settings(settings_file)
    binary = os.path.expanduser(os.path.expandvars(value))
    print("opt path: {}".format(binary))
    settings.set('opt', path)
    sublime.save_settings(settings_file)