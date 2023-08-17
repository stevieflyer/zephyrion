import abc


class JsExecutor(abc.ABC):
    """
    Javascript executor interface.
    """
    @abc.abstractmethod
    async def exec_js(self, js: str):
        """
        Execute javascript code.

        This interface does not define the return value specifications.

        :param js: (str) Javascript code to execute
        :return:
        """
        raise NotImplementedError()


class JsHandler:
    def __init__(self, js_executor: JsExecutor):
        if not isinstance(js_executor, JsExecutor):
            raise ValueError(f"js_executor must be an instance of JsExecutor, got {type(js_executor)}")
        self._js_executor = js_executor

    @property
    def js_executor(self):
        return self._js_executor


__all__ = ['JsExecutor', 'JsHandler']
