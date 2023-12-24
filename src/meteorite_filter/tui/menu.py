from meteorite_filter.tui.utils import *


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
    def __init__(
            self,
            items: list[MenuItem] | dict[str, MenuItem],
            preamble: str | None = None, prompt='> ',
            default: int | None = None,
            back=False,
            quittable=True
        ) -> None:
        self._items = self._normalize_menu_items(items)
        self._preamble = preamble
        self._default = default
        self._prompt = prompt
        self.back = back
        self.quittable = quittable

    @property
    def items(self) -> dict[str, MenuItem]:
        return self._items


    @property
    def preamble(self) -> str | None:
        return self._preamble


    @property
    def prompt(self) -> str:
        return self._prompt


    @property
    def default(self) -> int | None:
        return self._default
    

    def _normalize_menu_items(self, items: list[MenuItem] | dict[str, MenuItem]) -> dict[str, MenuItem]:
        if isinstance(items, dict):
            return items
        
        return {str(idx): value for idx, value in enumerate(items, 1)}


    def __str__(self) -> str:
        output = ''

        if self.preamble is not None:
            output += term_format(self.preamble, TERM_FG_CYAN) + '\n'

        for idx, (key, item) in enumerate(self.items.items(), 1):
            output += f'{key} - {item.label}{" (default)" if (idx - 1) == self._default else ""}\n'

        if self.back:
            output += 'b - Return to the previous menu\n'

        if self.quittable:
            output += 'q - Quit the application\n'

        output += term_format(f'Type a letter or number to select your choice{" or press enter for the default" if self.default is not None else ""}\n', TERM_FG_CYAN)

        return output


    def __call__(self):
        print(self, end='')
        selection = finput(self.prompt, TERM_FG_GREEN).lower()

        if selection in ('b', 'B', '?b', '?B', '>b', '>B') and self.back:
            return

        if selection in ('q', 'Q', '?q', '?Q', '>q', '>Q') and self.quittable:
            quit_app()

        try:
            if selection == '' and self._default is not None:
                menu_key = menu_key = list(self.items.keys())[self._default]
            else:
                menu_key = selection
            
            if menu_key not in self.items.keys():
                raise ValueError

            menu_item = self.items[menu_key]
        except (ValueError, IndexError):
            throw_error('Invalid option. Please enter the number or letter of your selection.')
            self()
            return

        if isinstance(menu_item, ReturnableMenuItem) and menu_item.go_back:
            print()
            menu_item()
            print()
            self()
        else:
            print()
            menu_item()


class ReturnableMenuItem(MenuItem):
    def __init__(self, label: str, func_call, callback=None, go_back=True) -> None:
        self.go_back = go_back
        super().__init__(label, func_call, callback)


class SubmenuItem(ReturnableMenuItem):
    def __init__(self, label: str, submenu: Menu) -> None:
        submenu.back = True
        super().__init__(label, submenu, go_back=True)
