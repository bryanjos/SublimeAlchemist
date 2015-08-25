from subprocess import Popen, PIPE, STDOUT, check_output
import os
import shlex
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "pexpect"))
import pexpect

alchemist_plugin_path = os.path.dirname(os.path.realpath(__file__))
alchemist_server_path = "'" + alchemist_plugin_path + "/alchemist-server/run.exs" + "'"
alchemist_server_start_command = 'elixir ' + alchemist_server_path + ' dev'

class AlchemistServer:

  def __init__(self, window):
    self.server_instance = None
    self.root_dir = None
    self.window = window

    self.__get_root_dir()
    self.start()

  def __get_root_dir(self):
    if not self.root_dir:
      folders = self.window.folders()

      for folder in folders:
        for dirpath, dirnames, files in os.walk(folder):
          if files and 'mix.exs' in files:
            self.root_dir = folder
            break

    if not self.root_dir:
      raise Exception('mix.exs file not found')

  def start(self):
    if self.server_is_alive():
      self.stop()

    self.server_instance = pexpect.spawnu(alchemist_server_start_command,
                                         cwd=self.root_dir)

  def stop(self):
    if self.server_is_alive():
      self.server_instance.terminate()
      self.server_instance = None

  def server_is_alive(self):
    return self.server_instance != None and self.server_instance.isalive()

  def server_is_dead(self):
    return not self.server_is_alive()

  def run_server_command(self, type, args=""):
    if self.server_is_dead():
      self.start()

    command = type + " " + args
    self.server_instance.sendline(command)
    self.server_instance.expect('END-OF-' + type)
    return self.server_instance.before

  def run_mix_command(self, task_name, args=""):
    command = 'mix ' + task_name + ' ' + args
    command = shlex.split(command)

    with Popen(command, stdout=PIPE, cwd=self.root_dir) as proc:
      print(proc.stdout.read().decode("utf-8"))

  def get_mix_tasks(self):
    tasks = self.run_server_command("MIXTASKS")
    return [s.strip() for s in tasks.splitlines()][1:-1]
