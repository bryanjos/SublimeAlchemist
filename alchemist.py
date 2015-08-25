import sublime, sublime_plugin
from subprocess import Popen, PIPE, STDOUT, check_output
import os
import shlex
from .server import AlchemistServer

alchemist_servers = {}

def get_current_server_instance(window):
  return alchemist_servers.setdefault(window.id(), AlchemistServer(window))

class AlchemistStartCommand(sublime_plugin.WindowCommand):
  def run(self):
    current_server = get_current_server_instance(self.window)
    current_server.start()

class AlchemistStopCommand(sublime_plugin.WindowCommand):
  def run(self):
    current_server = get_current_server_instance(self.window)
    current_server.stop()

class AlchemistMixCommand(sublime_plugin.WindowCommand):
  def run(self):
    current_server = get_current_server_instance(self.window)
    self.tasks = current_server.get_mix_tasks()

    return self.window.show_quick_panel(self.tasks, self.on_done, 0)

  def on_done(self, input):
    if input >= 0:
      current_server = get_current_server_instance(self.window)
      current_server.run_mix_command(self.tasks[input])

class AlchemistMixTestCommand(sublime_plugin.WindowCommand):
  def run(self):
    current_server = get_current_server_instance(self.window)
    current_server.run_mix_command("test")

class AlchemistMixCompileCommand(sublime_plugin.WindowCommand):
  def run(self):
    current_server = get_current_server_instance(self.window)
    current_server.run_mix_command("compile")

class AlchemistEventListener(sublime_plugin.EventListener):
  def on_activated_async(self, view):
      self.on_load_async(view)

  def on_load_async(self, view):
    filename = view.file_name()
    if filename and filename.endswith(('.ex', '.exs')):
      get_current_server_instance(view.window())


