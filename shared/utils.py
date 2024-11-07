def garbage_cleaner(str: str):
    clend_string = ''
    for i in str:
        if i.isdigit():
            clend_string += i
    return clend_string if len(clend_string) else 0

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args