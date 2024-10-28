import subprocess

def shell_parser(command_input, validate = True):
    output_status = ""
    if validate:
        output_status = subprocess.getoutput(command_input)

    return output_status

def pipe_stream(cmd_list : list, pipe : str ="|") -> list:

    quant_pipe = cmd_list.count(pipe)
    if quant_pipe>0:
        copy_list = cmd_list.copy()
        index_pipe_list = []
        for count in range(quant_pipe):
            index_base = copy_list.index(pipe)
            index_pipe_list.append(index_base)
            copy_list[index_base] = " "
    else:
        index_pipe_list = None

    return index_pipe_list

def space_trim(command_list):
    command_list = command_list+" "
    spread_list = []
    char = True
    base = 0
    for index,letter in enumerate(command_list):
        if letter == "'" or letter == '"':
            char = not char

        if letter == " " and char:
            spread_list.append(command_list[base:index])
            base = index+1

    command_list = spread_list
    quant_empty = command_list.count("")
    for quant in range(quant_empty):
        command_list.remove("")
    index_redirect = pipe_stream(command_list, "|")
    if index_redirect is not None:
        command_sep = []
        index_base = 0
        last_index = len(index_redirect)-1
        for index, value in enumerate(index_redirect):
            try:
                command_sep.append(command_list[index_base:value])
                index_base = value + 1
                if index == last_index:
                    command_sep.append(command_list[index_base:])
            except IndexError:
                print("Out of index")
        command_list = command_sep
    else:
        command_list = [command_list]
#    index_stdout = pipe_stream(command_list, ">")
#    index_stderr = pipe_stream(command_list, "2>")



    return command_list

def shell_exec(command_input : dict, validate : bool) -> tuple:
    if validate:
        command_spread = space_trim(command_input)
        try:
            pipe_tree = []
            stdin = None
            stdout = subprocess.PIPE
            stderr = subprocess.PIPE
            for index,cmd_steps in enumerate(command_spread):
#                print(cmd_steps)
                object_ = subprocess.Popen(cmd_steps,
                                           stdin=stdin,
                                           stdout=stdout,
                                           stderr=stderr,
                                           text=True,
                                           cwd=r"/home")
#                pid_number = object_.pid
                pipe_tree.append(object_)
                stdin = pipe_tree[index].stdout

            return pipe_tree[-1], pipe_tree[-1].pid
        except PermissionError as err:
            print("Error: ",err)
        except FileNotFoundError as F_n_err:
            print("Error", F_n_err)
        except FileExistsError as F_e_err:
            print("Error", F_e_err)
        return None, None


if __name__ == "__main__":
    import time
    val, pid = shell_exec("bash -e 'import this'", True)
    print(pid)
    while val.poll() is None:
        print("Exec")
        time.sleep(1)
    print(val.poll())
    output, error = val.communicate()
    print(output, error)
    subprocess.Popen().__dict__
