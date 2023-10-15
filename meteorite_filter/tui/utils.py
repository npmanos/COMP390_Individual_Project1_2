def throw_error(msg: str):
    print(f'\nERROR! {msg}\n')
    pause()

def pause():
    input('Press any key to continue...\n')

def clear():
    print('\u001b[2J')

def quit_app():
    print('\nQuitting applicaiton... Goodbye!')
    exit(0)
