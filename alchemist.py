import sublime, sublime_plugin
from subprocess import Popen, PIPE, STDOUT, check_output
import os
import shlex

#TODO: Get path to mix.exs

alchemist_server = None
alchemist_plugin_path = os.path.dirname(os.path.realpath(__file__))
alchemist_server_path = "'" + alchemist_plugin_path + "/alchemist-server/run.exs" + "'"

def start_server():
  global alchemist_server
  command = 'elixir ' + alchemist_server_path + ' dev'
  command = shlex.split(command)
  alchemist_server = Popen(command, stdout=PIPE, stdin=PIPE, stderr=PIPE)

def stop_server():
  global alchemist_server

  if alchemist_server:
    alchemist_server.kill()
    alchemist_server = None

def execute_command(type, arguments=""):
  global alchemist_server

  if alchemist_server == None:
    start_server()

  command = bytes(type + " " + arguments, 'ascii')
  stdout_data = alchemist_server.communicate(input=command)[0]
  return stdout_data.decode("utf-8")

def do_mix_command(task_name, args=""):
  print(os.getcwd())
  command = 'mix ' + task_name + ' ' + args
  command = shlex.split(command)

  with Popen(command, stdout=PIPE) as proc:
    print(proc.stdout.read())

class AlchemistStartCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    start_server()

class AlchemistStopCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    stop_server()

class AlchemistMixCommand(sublime_plugin.WindowCommand):
  def run(self):
    self.tasks = execute_command("MIXTASKS")
    self.tasks = [s.strip() for s in self.tasks.splitlines()][:-1]

    return self.window.show_quick_panel(self.tasks, self.on_done, 0)

  def on_done(self, input):
    if input >= 0:
      do_mix_command(self.tasks[input])

class AlchemistMixTestCommand(sublime_plugin.WindowCommand):
  def run(self):
    do_mix_command("test")

class AlchemistMixCompileCommand(sublime_plugin.WindowCommand):
  def run(self):
    do_mix_command("compile")

class AlchemistCompletionCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    execute_command('COMPLETE')

class AlchemistDocumentationCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    execute_command('DOC')

class AlchemistEvaluationCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    execute_command('EVAL')

class AlchemistQuotedCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    execute_command('QUOTE')

class AlchemistDefinitionLookupCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    execute_command('SOURCE')

class AlchemistModulesCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    execute_command('MODULES')
