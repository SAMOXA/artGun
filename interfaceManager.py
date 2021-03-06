class InterfaceError(Exception):
    pass


class InterfaceMethodNotExist(InterfaceError):
    method_name = ""
    interface_name = ""
    existing_methods = {}

    def __init__(self, interface_name, method_name, exist_methods):
        self.interface_name = interface_name
        self.method_name = method_name
        self.exist_methods = exist_methods


class InterfaceNotExist(InterfaceError):
    interface_name = ""
    existing_interfaces = {}

    def __init__(self, interface_name, existing_interfaces):
        self.interface_name = interface_name
        self.existing_interfaces = existing_interfaces


class InterfaceAlreadyExist(InterfaceError):
    interface_name = ""
    existing_interfaces = {}

    def __init__(self, interface_name, existing_interfaces):
        self.interface_name = interface_name
        self.existing_interfaces = existing_interfaces


class InterfaceMediatorNotSet(InterfaceError):
    interface_name = ""

    def __init__(self, interface_name):
        self.interface_name = interface_name


class BaseInterface:

    def __init__(self, name, methods):
        self.methods = methods.copy()
        self.name = name
        self.mediator = None
        self.msg_prototypes = dict()

    def have_method(self, method_name):
        return method_name in self.methods

    def call_method(self, method_name, msg):
        if self.have_method(method_name) is False:
            raise InterfaceMethodNotExist(self.name, method_name, self.methods)
        if self.mediator is None:
            raise InterfaceMediatorNotSet(self.name)

        event_engine = self.mediator.get_event_engine()
        return event_engine.call_method(self.name, method_name, msg)

    def get_interface_name(self):
        return self.name

    def set_mediator(self, mediator):
        self.mediator = mediator

    def get_methods_list(self):
        methods_names = []
        for method in self.methods:
            methods_names.append(method)

        return self.methods


class InterfaceManager:
    interfaces = {}

    def __init__(self, mediator):
        self.mediator = mediator
        self.interfaces = {}

    def add_interface(self, interface):
        if interface.get_interface_name() in self.interfaces:
            raise InterfaceAlreadyExist(interface.get_interface_name(), self.interfaces)
        self.interfaces[interface.get_interface_name()] = interface
        event_engine = self.mediator.get_event_engine()
        event_engine.add_interface(interface)
        interface.set_mediator(self.mediator)

    def have_interface(self, interface_name):
        return interface_name in self.interfaces

    def interface_have_method(self, interface_name, method_name):
        return self.interfaces[interface_name].have_method(method_name)

    def get_interface(self, interface_name):
        if self.have_interface(interface_name) is False:
            raise InterfaceNotExist(interface_name, self.interfaces)

        return self.interfaces[interface_name]

    def get_interface_list(self):
        list = []
        for interface in self.interfaces:
            list.append(interface)

        return list
