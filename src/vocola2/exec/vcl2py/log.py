def set_log(target):
    global LOG
    LOG = target


def print_log(message, no_newline=False):
    ## TODO removed for the moment, QH, March 2022
    try:
        global LOG
        if no_newline:
            print(message, file=LOG)
        else:
            print(message, file=LOG)
    except NameError:
        print(message)

def close_log():
    global LOG
    LOG.close()
