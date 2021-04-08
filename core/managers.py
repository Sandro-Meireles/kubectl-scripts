import os

import questionary


class Pod(object):

    def __init__(self, name: str, namespace):
        self._name = name
        self._namespace = namespace

    def get_name(self) -> str:
        return self._name

    def __str__(self):
        return self._name

    def _copy(self, path: str, to: str):
        command = f'cp {path} {to}'
        self.get_namespace().execute(command)

    def copy_to_pod(self, path: str, to: str):
        """
            Copies a file from your machine into this pod
        """

        pod_path = f'{self.get_name()}:/{to}'
        self._copy(path, pod_path)

    def copy_by_pod(self, path: str, to: str):
        """
            Copies a file from this pod into your machine
        """

        pod_path = f'{self.get_name()}:/{path}'
        self._copy(pod_path, to)

    def execute(self, command: str):
        """
            Run a command
        """

        body = f'exec {self.get_name()} -- {command}'
        namespace = self.get_namespace()

        return namespace.execute(body)

    def get_namespace(self):
        return self._namespace

    def make_port_forward(self, internal_port: int, external_port):
        body = 'port-forward'
        args = [self.get_name(), f'{internal_port}:{external_port}']

        namespace = self.get_namespace()
        namespace.execute(body, *args)


class Namespace(object):

    def __init__(self, script):
        self._script = script
        self.name = self.get_namespace_input()
        self.pods = self.get_pods()

    def get_namespace_input(self) -> str:
        return input('In which namespace the application is located? \n: ')

    def execute(self, command: str, *args: list) -> str:
        args = self.assemble_arguments(args)

        body = f'kubectl -n {self.name} {command}'
        if args:
            body += f' {args}'

        self.show_command(body)

        # TODO: Add immediate exit when doing KeyboardInterrupt

        try:
            return os.popen(body).read()
        except KeyboardInterrupt as err:
            raise err

    def assemble_arguments(self, args: list) -> str:

        return ' '.join(args)

    def show_command(self, command: str):
        os.system('clear')

        print('Running command:')
        print(f'  └─ $ {command}\n')

    def validate_pods_str(self, pods_str: str) -> bool:
        return bool(pods_str or 'Forbidden' in pods_str)

    def get_pods(self) -> list:
        print(f'Getting {self.name} pods')

        command = 'get pods'
        args = ['--no-headers',
                '-o',
                'custom-columns=":metadata.name"']

        while True:
            only_str_pods = self.execute(command, *args)

            if self.validate_pods_str(only_str_pods):
                break

            self.name = self.get_namespace_input()

        pods = [Pod(pod_name, self) for pod_name in only_str_pods.split()]

        return pods

    def get_pod_selected(self, response: str, pod_names: list) -> Pod:
        index = pod_names.index(response)
        return self.pods[index]

    def get_pod(self, message: str = 'Select your pod') -> Pod:
        pods_names = list(map(lambda pod: pod.get_name(), self.pods))

        response = questionary.select(
            message,
            pods_names).ask()

        pod = self.get_pod_selected(response, pods_names)

        return pod
