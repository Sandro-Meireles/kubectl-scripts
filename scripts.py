"""
Here are some sample scripts, feel free to change or delete them.
"""

from core.script import Script


class PortForward(Script):

    def body(self):
        namespace = self.namespace

        internal_port = int(input('Internal PORT: '))
        external_port = int(input('Extenal PORT: '))

        pod = namespace.get_pod()

        pod.make_port_forward(internal_port, external_port)

        print('Port forward completed!')

    class Meta:
        description = 'Forward a local port to a port on the Pod'


class GetEnvironmentVariables(Script):

    def body(self):
        namespace = self.namespace
        pod = namespace.get_pod()

        result = pod.execute('printenv')

        print(result)

    class Meta:
        description = 'Forward a local port to a port on the Pod'
