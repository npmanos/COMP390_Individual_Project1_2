"""
This module contains a customizable terminal interactive menu framework.
"""


from meteorite_filter.tui.utils import *


class MenuItem:
    def __init__(self, label: str, func_call, callback=None) -> None:
        """
        Represents a menu item with a label, function call, and optional callback.

        Args:
            label (str): The label of the menu item.
            func_call: The function to be called when the menu item is selected.
            callback (optional): An optional callback function to be called after the function call.

        Returns:
            None
        """
        self._label = label
        self._func_call = func_call
        self._callback = callback


    @property
    def label(self):
        """
        Get the label of the menu item.

        Returns:
            str: The label of the menu item.
        """
        return self._label


    def __call__(self) -> None:
        """
        Call the function associated with the menu item.

        If a callback function is provided, it will be called after the function call.

        Returns:
            None
        """
        if self._callback is None:
            self._func_call()
        else:
            self._callback(self._func_call())


class Menu:
    def __init__(self, items: list[MenuItem] | dict[str, MenuItem], preamble: str | None = None, prompt='> ', default: int | None = None, back=False, quittable=True, back_label='b', quit_label='q') -> None:
        """
        Represents a menu with selectable items.

        Args:
            items (list[MenuItem] | dict[str, MenuItem]): The menu items. Can be a list of MenuItem objects or a dictionary with string keys and MenuItem values.
            preamble (str | None, optional): The preamble text displayed before the menu items. Defaults to None.
            prompt (str, optional): The prompt text displayed to the user. Defaults to '> '.
            default (int | None, optional): The index of the default menu item. Defaults to None.
            back (bool, optional): Whether the menu has a "Return to the previous menu" option. Defaults to False.
            quittable (bool, optional): Whether the menu has a "Quit the application" option. Defaults to True.
            back_label (str, optional): The label for the "Return to the previous menu" option. Defaults to 'b'.
            quit_label (str, optional): The label for the "Quit the application" option. Defaults to 'q'.
        """
        self._items = self._normalize_menu_items(items)
        self._preamble = preamble
        self._default = default
        self._prompt = prompt
        self.back = back
        self._back_label = back_label
        self.quittable = quittable
        self._quit_label = quit_label

    @property
    def items(self) -> dict[str, MenuItem]:
        """
        Get the menu items.

        Returns:
            dict[str, MenuItem]: The menu items.
        """
        return self._items


    @property
    def preamble(self) -> str | None:
        """
        Get the preamble text.

        Returns:
            str | None: The preamble text.
        """
        return self._preamble


    @property
    def prompt(self) -> str:
        """
        Get the prompt text.

        Returns:
            str: The prompt text.
        """
        return self._prompt


    @property
    def default(self) -> int | None:
        """
        Get the index of the default menu item.

        Returns:
            int | None: The index of the default menu item.
        """
        return self._default
    

    def _normalize_menu_items(self, items: list[MenuItem] | dict[str, MenuItem]) -> dict[str, MenuItem]:
        """
        Normalize the menu items to a dictionary with string keys.

        Args:
            items (list[MenuItem] | dict[str, MenuItem]): The menu items.

        Returns:
            dict[str, MenuItem]: The normalized menu items.
        """
        if isinstance(items, dict):
            return items
        
        return {str(idx): value for idx, value in enumerate(items, 1)}


    def __str__(self) -> str:
        """
        Get the string representation of the menu.

        Returns:
            str: The string representation of the menu.
        """
        output = ''

        if self.preamble is not None:
            output += term_format(self.preamble, TERM_FG_CYAN) + '\n'

        for idx, (key, item) in enumerate(self.items.items(), 1):
            output += f'{key} - {item.label}{" (default)" if (idx - 1) == self._default else ""}\n'

        output += f'{self._back_label} - Return to the previous menu\n' if self.back else ''
        output += f'{self._quit_label} - Quit the application\n' if self.quittable else ''

        output += term_format(f'Type a letter or number to select your choice{" or press enter for the default" if self.default is not None else ""}\n', TERM_FG_CYAN)

        return output


    def __call__(self):
        """
        Display the menu and handle user input.
        """
        print(self, end='')
        selection = self._get_user_selection()
        if selection is None: return

        try:
            menu_key = list(self.items.keys())[self._default] if selection == '' and self._default is not None else selection
            if menu_key not in self.items.keys(): raise ValueError
            self._run_selection(self.items[menu_key])
        except (ValueError, IndexError):
            throw_error('Invalid option. Please enter the number or letter of your selection.')
            self()

    def _get_user_selection(self) -> str | None:
        """
        Get the user's menu selection.

        Returns:
            str | None: The user's menu selection.
        """
        selection = finput(self.prompt, TERM_FG_GREEN).lower()

        if selection in ('b', 'B', '?b', '?B', '>b', '>B', self._back_label) and selection not in self._items.keys() and self.back:
            return None

        if selection in ('q', 'Q', '?q', '?Q', '>q', '>Q', self._quit_label) and selection not in self._items.keys() and self.quittable:
            quit_app()
        
        return selection

    def _run_selection(self, menu_item: MenuItem):
        """
        Run the selected menu item.

        Args:
            menu_item (MenuItem): The selected menu item.
        """
        if isinstance(menu_item, ReturnableMenuItem) and menu_item.go_back:
            print()
            menu_item()
            print()
            self()
        else:
            print()
            menu_item()


class ReturnableMenuItem(MenuItem):
    """
    A menu item that can be returned to the previous menu.

    Args:
        label (str): The label of the menu item.
        func_call: The function to be called when the menu item is selected.
        callback: An optional callback function to be called after the menu item is selected.
        go_back (bool): Whether to go back to the previous menu after the menu item is selected.
    """

    def __init__(self, label: str, func_call, callback=None, go_back=True) -> None:
        self.go_back = go_back
        super().__init__(label, func_call, callback)


class SubmenuItem(ReturnableMenuItem):
    """
    Represents a menu item that opens a submenu when selected.

    Args:
        label (str): The label or name of the menu item.
        submenu (Menu): The submenu to be opened when the menu item is selected.
    """
    def __init__(self, label: str, submenu: Menu) -> None:
        submenu.back = True
        super().__init__(label, submenu, go_back=True)
