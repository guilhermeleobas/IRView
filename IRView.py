import sublime
import sublime_plugin

import os
import shutil
import tempfile

from subprocess import Popen, PIPE

settings_file = 'IRView.sublime-settings';
TEMP = tempfile.gettempdir()

def get_opt():
  return os.path.expanduser(
    os.path.expandvars(sublime.load_settings(settings_file).get('opt')))

def cp_to_tmp(filename):
  shutil.copy(filename, TEMP)
  return os.path.join(TEMP, os.path.basename(filename))

def create_dots(opt, filename, pass_name):
  cmd = [opt, filename, pass_name, '-disable-output']
  p = Popen(cmd, stdout=PIPE, stderr=PIPE)

  output, err = p.communicate()

  files = err.decode("utf-8")\
    .replace("Writing ", "").replace("'", "")\
    .strip('...\n').split('...\n')\

  return list(map(lambda x: os.path.join(TEMP, x), files))

def create_pdfs(dotfiles):
  for f in dotfiles:
    basename = os.path.basename(f)
    cmd = ['dot', '-Tpdf', f, '-o', os.path.join(TEMP, basename + '.pdf')]
    Popen(cmd, stdout=None, stderr=None).communicate()

  return [os.path.join(TEMP, os.path.basename(f) + '.pdf') for f in dotfiles]

def open_pdfs(pdfs):
  for pdf in pdfs:
    cmd = ['open', pdf]
    Popen(cmd, stdout=None, stderr=None).communicate()


def find_methods_name(view):
  names = ['all']
  for r in view.find_all(r'^define .*$'):
    b = view.substr(r).find('@')
    e = view.substr(r).find('(')
    names.append(view.substr(r)[b+1:e])
  return names

def run_cmd(view, filename, pass_name):

  def _run_cmd(filename, pass_name, method=None):
    opt = get_opt()
    filename = cp_to_tmp(filename)
    os.chdir(TEMP)
    dots = create_dots(opt, filename, pass_name)
    if method is None or method == 'all':
      pdfs = create_pdfs(dots)
    else:
      pdfs = create_pdfs(list(filter(lambda x: method + '.dot' in x, dots)))
    open_pdfs(pdfs)

  names = find_methods_name(view)
  sublime.active_window().show_quick_panel(names,
    lambda idx: None if idx == -1 else _run_cmd(filename, pass_name, names[idx]))

###
class IrViewCallGraphCommand(sublime_plugin.TextCommand, IRView):
  def run(self, edit):
    filename = self.view.file_name()
    run_cmd(self.view, filename, '-dot-callgraph')

###
class IrViewCfgCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    filename = self.view.file_name()
    run_cmd(self.view, filename, '-dot-cfg')
    # methods = ['all']


    # sublime.active_window().show_quick_panel(methods, 
    #   lambda idx: None if idx == -1 else run_cmd(self.view, filename, '-dot-cfg', methods[idx]))

class IrViewCfgOnlyCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    filename = self.view.file_name()
    run_cmd(self.view, filename, '-dot-cfg-only')

###
class IrViewDomCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    filename = self.view.file_name()
    run_cmd(self.view, filename, '-dot-dom')

class IrViewDomOnlyCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    filename = self.view.file_name()
    run_cmd(self.view, filename, '-dot-dom-only')

###
class IrViewPostdomCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    filename = self.view.file_name()
    run_cmd(self.view, filename, '-dot-postdom')

class IrViewPostdomOnlyCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    filename = self.view.file_name()
    run_cmd(self.view, filename, '-dot-postdom-only')

###
class IrViewRegionsCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    filename = self.view.file_name()
    run_cmd(self.view, filename, '-dot-regions')

class IrViewRegionsOnlyCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    filename = self.view.file_name()
    run_cmd(self.view, filename, '-dot-regions-only')

###
class IrViewSetPathCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    w = sublime.active_window()
    w.show_input_panel("Path to opt: ", "", set_path, None, None)

  def set_path(value):
    settings = sublime.load_settings(settings_file)
    binary = os.path.expanduser(os.path.expandvars(value))
    settings.set('opt', path)
    sublime.save_settings(settings_file)