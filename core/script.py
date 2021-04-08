import inspect

from core.managers import Namespace


class Script(object):

    """
        Abstract class responsible for interpreting and executing scripts
    """

    def __init__(self):
        self.namespace = self.create_namespace()
        self.execute()

    def create_namespace(self) -> Namespace:
        namespace = Namespace(self)

        return namespace

    def execute(self):
        self.body()

    def body(self):
        ...

    @classmethod
    def get_script_by_name(cls, scripts: list, name: str):
        for script in scripts:
            if script.__name__ == name:
                return script

    @classmethod
    def get_scripts(cls) -> list:
        import scripts

        objs = []
        for name, obj in inspect.getmembers(scripts):
            objs.append(obj) if inspect.isclass(obj) \
                and not obj == cls \
                and issubclass(obj, cls) else None

        return objs

    def __str__(self):
        return str(self.__class__.__name__)

    class Meta:
        description = 'Abstract script class'
