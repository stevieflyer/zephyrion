class JsGenerator:
    """
    A Basic Javascript code generator.
    """
    # query related
    @staticmethod
    def get_element(selector: str) -> str:
        return f'document.querySelector("{selector}")'

    @staticmethod
    def get_elements(selector: str) -> str:
        return f'document.querySelectorAll("{selector}")'

    # attr related
    @staticmethod
    def get_attr(selector: str, attr: str) -> str:
        return f'{JsGenerator.get_element(selector)}.getAttribute("{attr}")'

    @staticmethod
    def set_attr(selector: str, attr: str, value: str) -> str:
        return f'{JsGenerator.get_element(selector)}.setAttribute("{attr}", "{value}")'

    # class list related
    @staticmethod
    def get_class_list(selector: str) -> str:
        return f'{JsGenerator.get_element(selector)}.classList'

    @staticmethod
    def add_class(selector: str, class_name: str) -> str:
        return f'{JsGenerator.get_class_list(selector)}.add("{class_name}")'

    @staticmethod
    def remove_class(selector: str, class_name: str) -> str:
        return f'{JsGenerator.get_class_list(selector)}.remove("{class_name}")'

    @staticmethod
    def toggle_class(selector: str, class_name: str) -> str:
        return f'{JsGenerator.get_class_list(selector)}.toggle("{class_name}")'

    # action related
    @staticmethod
    def click(selector: str) -> str:
        return f'{JsGenerator.get_element(selector)}.click()'

    @staticmethod
    def submit(selector: str) -> str:
        return f'{JsGenerator.get_element(selector)}.submit()'

    @staticmethod
    def focus(selector: str) -> str:
        return f'{JsGenerator.get_element(selector)}.focus()'

    @staticmethod
    def blur(selector: str) -> str:
        return f'{JsGenerator.get_element(selector)}.blur()'

    @staticmethod
    def select(selector: str) -> str:
        return f'{JsGenerator.get_element(selector)}.select()'

    # scroll related
    @staticmethod
    def get_scroll_height() -> str:
        return "document.body.scrollHeight"

    @staticmethod
    def get_scroll_width() -> str:
        return "document.body.scrollWidth"

    @staticmethod
    def get_scroll_top() -> str:
        return "document.body.scrollTop"

    @staticmethod
    def scroll_to(x: int, y: int):
        return f"window.scrollTo({x}, {y});"

    @staticmethod
    def scroll_by(x_disp: int, y_disp: int):
        return f"window.scrollBy({x_disp}, {y_disp});"

    @staticmethod
    def scroll_to_bottom():
        return f"window.scrollTo(0, {JsGenerator.get_scroll_height()});"

    @staticmethod
    def scroll_to_top():
        return "window.scrollTo(0,0);"



__all__ = ['JsGenerator']
