


class MenuItem:
    def __init__(self, label: str, func_call, callback=None) -> None:
        self._label = label
        self._func_call = func_call
        self._callback = callback


    @property
    def label(self):
        return self._label


    def __call__(self) -> None:
        if self._callback is None:
            self._func_call()
        else:
            self._callback(self._func_call())


class Menu:
    def __init__(self, items: list[MenuItem], preamble: str | None = None, prompt='> ', back=False, quittable=True) -> None:
        self._items = items
        self._preamble = preamble
        self._prompt = prompt
        self.back = back
        self.quittable = quittable

    @property
    def items(self) -> list[MenuItem]:
        return self._items


    @property
    def preamble(self) -> str | None:
        return self._preamble


    @property
    def prompt(self) -> str:
        return self._prompt


    def __str__(self) -> str:
        output = ''

        if self.preamble is not None:
            output += self.preamble + '\n'

        for idx, item in enumerate(self.items, 1):
            output += f'{idx} - {item.label}\n'

        if self.back:
            output += 'b - Return to the previous menu\n'

        if self.quittable:
            output += 'q - Quit the application\n'

        return output


    def __call__(self):
        print(self, end='')
        selection = input(self.prompt)

        if selection in ('b', 'B') and self.back:
            return

        if selection in ('q', 'Q') and self.quittable:
            exit(0)

        menu_idx = 0
        try:
            menu_idx = int(selection) - 1
            menu_item = self.items[menu_idx]
        except (ValueError, IndexError):
            print('ERROR! Invalid option. Please enter the number or letter of your selection.', end='\n\n')
            input('Press any key to continue...\n')
            self()
            return

        if isinstance(menu_item, SubmenuItem):
            print()
            menu_item()
            print()
            self()
        else:
            print()
            menu_item()


class SubmenuItem(MenuItem):
    def __init__(self, label: str, submenu: Menu) -> None:
        submenu.back = True
        super().__init__(label, submenu)


if __name__ == '__main__':
    submenu = Menu(
        [
            MenuItem('First submenu option', lambda: print('You selected the first submenu option')),
            MenuItem('Second submenu option', lambda: print('You selected the second submenu option'))
        ]
    )

    menu = Menu(
        [
            MenuItem('Menu item', lambda: print('This is the first menu item')),
            MenuItem('Menu item w/ callback', lambda: input('Enter value to send to callback: '), lambda ret_val: print(f'Callback received value: {ret_val}')),
            SubmenuItem('Submenu', submenu)
        ],
        'MAIN MENU - Select your option:',
        'MENU> '
    )

    menu()
