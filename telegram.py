
import requests as rq
import json
import time
from SECRET import HTTP_API
from mod_scheme.scheme import Data_content, URL_Converter
from mod_shell.shell_command import shell_exec
from mod_active.acitve_id import user_validation
from mod_shell.cmd_ctrl import detencion_programa, signal_handler


from os.path import dirname, realpath, join
import sys

Dir_prog = dirname(realpath(__file__))
for j in ['mod_active/', 'mod_scheme/', 'mod_shell/']:
    Dir_files = (join(Dir_prog, j))
    sys.path.append(Dir_files)

class Model():
    full_name = "JOintSHellUserAuthority"
    short_name = "JOSHUA"
    version = "0.0.1a"
    os = f"{sys.platform} {sys.version}".upper()

class Bot_Implementation(Model, URL_Converter):
    https_url = f"https://api.telegram.org/bot{HTTP_API}"
    message_rec = None
    message_update_id = 0
    message_id_last = 0
    message_update_offset = 0
    new_message_flag = False
    new_message_queue_flag = False
    new_command_queue_flag = False
    active_chats = []
    active_users = []
    last_message = None
    command_queue = []
    message_queue = []
    active_commands = []
    delete_list = []
    log_file= None

    def open_log(self):
        self.log_file = open(f"{Dir_prog}/log_files/log_telegram.log", "a")

    def print_log(self, text, error):
        time_lookback = time.strftime('%d-%m-%Y %H:%M:%S')
        if error:
            self.log_file.write(f"{time_lookback}\t***Error: {text}\n")
        elif error is None:
            self.log_file.write(f"{time_lookback}\t***INVALID USER: {text}\n")
        else:
            self.log_file.write(f"{time_lookback}\t{text}\n")

    def get_Updates(self, allowed_updates = []):
        try:
            message_rec_raw = rq.get(f"{self.https_url}/getUpdates?offset={self.message_update_offset}&allowed_updates={allowed_updates}")
            message_rec_raw_status_code = message_rec_raw.status_code
            update_code = self.__status_code_handler(message_rec_raw_status_code)
            if update_code == 0:
                message_content = message_rec_raw.content
                try:
                    message_content_json = json.loads(message_content)
                    self.message_rec = message_content_json
                    self.__get_update_id()
                    self.__message_Handling()
                except json.JSONDecodeError as JSON_ERROR:
                    print(JSON_ERROR)
                    self.print_log(JSON_ERROR, True)
                except KeyError:
                    pass
        except rq.ConnectTimeout as C_error:
            print(C_error)
            self.print_log(C_error, True)
        except rq.ConnectionError as R_error:
            print(R_error)
            self.print_log(R_error, True)
        except rq.exceptions as P_error:
            print(P_error)
            self.print_log(P_error, True)

    def print_Updates(self):
        if self.new_message_queue_flag:
            print(self.message_queue)
            self.new_message_queue_flag = False
        if self.new_command_queue_flag:
            print(self.command_queue)
            self.new_command_queue_flag = False

    def send_Message(self, chat_id, text):
        text_url_form = self.Data_text_convert_to_url(text)
        resp = f"?chat_id={chat_id}&text={text_url_form}"
        send_message = rq.post(f"{self.https_url}/sendMessage{resp}")
        send_message.status = send_message.status_code

    def __message_Handling(self):
        if self.new_message_flag:
            for chat in self.active_chats:
                message = Data_content(chat)
                id_ = message["chat_id"]
                try:
                    text_message = message["text"]
                    command = message["entity"]
                    command_dict = {"chat_id": id_, "content": [command, text_message]}
                    self.command_queue.append(command_dict)
                    self.new_command_queue_flag = True
                except KeyError as K_err:
                    print(f"Error: {K_err}", message)
                    self.print_log(K_err, True)

            self.new_message_flag = False

    def __get_update_id(self):
        chat_list = self.message_rec["result"]
        try:
            self.active_chats = chat_list
            self.message_update_id = chat_list[-1]["update_id"]
            self.message_update_offset = self.message_update_id + 1
            self.new_message_flag = True
        except IndexError:
            self.new_message_flag = False


    def __status_code_handler(self, code_input):
        code_output = None
        if code_input>= 200 and code_input<300:
            code_output = 0
        elif code_input>=300 and code_input<400:
            code_output = 1
        elif code_input>=400 and code_input<500:
            code_output = -1
        elif code_input>=500 and code_input<600:
            code_input = -2
        return code_output

    def time_lookback(self):
        return time.strftime('System Date & Local Time:  %d-%m-%Y  @  %H:%M:%S')

    def execute(self):
        commands = {"/start" : f"{self.short_name}, ver: {self.version}, os: {self.os}.\nHelp on: /help",
                    "/end" : "Aou revoir",
                    "/version" : f"{self.version}",
                    "/os" : f"{self.os}",
                    "/time" : self.time_lookback(),
                    "/help" : "Comandos diposnibles: \n/time\n/version\n/os",
                    "/helplogon" : """\nCall for /shell -> System control;\npid return for killing and output when it's done\n/current : commands on wait"""
                     }
        try:
            ind = 0
            for index,command in enumerate(self.command_queue):
                inn = index
                print(command)
                self.print_log(command, False)
                chat_id = command["chat_id"]
                if command["content"][1][:6].lower()=="/shell":
                    #call_command = command["content"][1].replace("/shell","")
                    call_command = command["content"][1][7:]
                    true_value = user_validation(chat_id)
                    command_execution, pid_exec = shell_exec(call_command, true_value)
                    self.send_Message(chat_id, f"PID: {pid_exec}")
                    if pid_exec is not None:
                        self.active_commands.append([chat_id, command_execution, pid_exec])
                elif command["content"][1][:9].lower()=="/current":

                    if self.active_commands != []:
                        exec_list_value = []
                        for commands_in_exec in self.active_commands:
                            if commands_in_exec[0] == chat_id:
                                exec_list_value.append(commands_in_exec[1:])
                        if exec_list_value == []:
                            self.send_Message(chat_id, "No current commands on wait")
                        else:
                            self.send_Message(chat_id, f"Commands on queue: {exec_list_value}")
                elif command["content"][1][:9]=="/validate":
                    content_of_validation = command["content"][1][10:]
                    with open(f"{Dir_prog}/mod_active/validation_log.request" ,"a") as valid_file:
                        valid_file.write(f"{chat_id}\t{content_of_validation}\n")

                else:
                    text = commands[command["content"][1]]
                    self.send_Message(chat_id, text)

            self.command_queue = []
        except KeyError as kerror:
            error_output = f"Command {command['content'][1]} not found"
            self.send_Message(chat_id, error_output)
            self.command_queue.pop(ind)

        except IndexError as ierror:
            error_output = f"Command {command['content'][1]} not found"
            self.send_Message(chat_id, error_output)
            self.command_queue.pop(ind)

        except TypeError as T_error:
            if true_value:
                self.send_Message(chat_id, f"Verify syntax, {command['content'][1]}")
            else:
                self.send_Message(chat_id, f"Use /validate <name>  <e-mail>")
                self.print_log(f"{chat_id}{command}", None)
            self.command_queue.pop(ind)

        except PermissionError as P_error:
            self.send_Message(chat_id, P_error)
            self.send_Message(chat_id, "Use /validate '<name> <email>' for vaildation.")
            self.command_queue.pop(ind)
        #for commands_due in self.command_queue:
    def active_exec(self):
        if len(self.active_commands)!= 0:
            for index, execute in enumerate(self.active_commands):
                if execute[1].poll() is not None:
                    try:
                        output, error = execute[1].communicate()
                        self.send_Message(execute[0], output)
                        self.send_Message(execute[0], error)
                        self.delete_list.append(execute)
                    except ValueError:
                        self.send_Message(execute[0], f"Verify command {execute[1]}")
                        self.print_log(execute, True)
            if self.delete_list != []:
                for item in self.delete_list:
                    self.active_commands.remove(item)
                    self.delete_list.remove(item)
            if self.active_commands is None:
                self.active_commands = []
                self.delete_list = []
    def close_log(self):
        self.log_file.close()

    def purge(self):
        self.message_rec = None
        self.message_update_id = 0
        self.message_id_last = 0
        self.message_update_offset = 0
        self.new_message_flag = False
        self.new_message_queue_flag = False
        self.new_command_queue_flag = False
        self.active_chats = []
        self.active_users = []
        self.last_message = None
        self.command_queue = []
        self.message_queue = []
        self.active_commands = []
        self.delete_list = []

def main():
    Bot_Implementation_JOSHUA = Bot_Implementation()
    Bot_Implementation_JOSHUA.get_Updates()
    Bot_Implementation_JOSHUA.get_Updates()
    Bot_Implementation_JOSHUA.purge()
    while True:
        Bot_Implementation_JOSHUA.open_log()
        Bot_Implementation_JOSHUA.get_Updates()
        Bot_Implementation_JOSHUA.execute()
        Bot_Implementation_JOSHUA.active_exec()
        Bot_Implementation_JOSHUA.close_log()
        detencion_programa()
        time.sleep(0.5)

if __name__ == '__main__':
    main()
