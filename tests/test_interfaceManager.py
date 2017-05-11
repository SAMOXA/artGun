from unittest import TestCase
from interfaceManager import InterfaceManager
from interfaceManager import Interface
from interfaceManager import InterfaceNotExist
from interfaceManager import InterfaceAlreadyExist
from appMediator import AppMediator


class TestInterface(TestCase):
    def test_interface_base(self):
        test_method1 = lambda: "test_method1"
        test_method_args = (lambda x, y: x + y)

        methods = {"test_method1": test_method1, "test_method_args": test_method_args}
        interface = Interface("test_method1", methods)

        have_func = interface.have_method("test_method1")
        self.assertTrue(have_func)

        have_func = interface.have_method("there_is_no_method")
        self.assertFalse(have_func)

    def test_get_name(self):
        methods = {}
        interface = Interface("test_interface", methods)

        name = interface.get_interface_name()
        self.assertEqual(name, "test_interface")

    def test_get_methods_list(self):
        test_method1 = lambda: "test_method1"
        test_method_args = (lambda x, y: x + y)
        methods = {"test_interface": test_method1, "test_method_args": test_method_args}
        interface = Interface("test_interface", methods)

        list = interface.get_methods_list()
        self.assertEqual(list, methods)

    def test_interface_without_methods(self):
        methods = {}
        interface = Interface("test_interface", methods)

        list = interface.get_methods_list()
        self.assertEqual(list, methods)


class TestInterfaceManager(TestCase):
    def test_interface_manager_base(self):
        test_method1 = lambda: "test_method1"
        test_method_args = (lambda x, y: x + y)

        methods = {"test_method1": test_method1, "test_method_args": test_method_args}
        interface = Interface("test_interface", methods)

        mediator = AppMediator()

        i = InterfaceManager(mediator)
        i.add_interface(interface)

        have_interface = i.have_interface("test_interface")
        self.assertTrue(have_interface)

        have_interface = i.have_interface("interface_to_not_found")
        self.assertFalse(have_interface)

        have_method = i.interface_have_method("test_interface", "test_method1")
        self.assertTrue(have_method)

        have_method = i.interface_have_method("test_interface", "test_method_not")
        self.assertFalse(have_method)

        returned_interface = i.get_interface("test_interface")
        self.assertEqual(returned_interface, interface)

    def test_error_input(self):
        test_method1 = lambda: "test_method1"
        test_method_args = (lambda x, y: x + y)

        methods = {"test_method1": test_method1, "test_method_args": test_method_args}
        interface = Interface("test_interface", methods)

        mediator = AppMediator()

        i = InterfaceManager(mediator)
        i.add_interface(interface)

        try:
            i.get_interface("test_interface_that_not_exist")
            self.assertRaises(Exception)
        except InterfaceNotExist as detail:
            self.assertEqual(detail.interface_name, "test_interface_that_not_exist")

    def test_interface_with_same_name(self):
        test_method1 = lambda: "test_method1"
        methods = {"test_interface": test_method1}

        interface = Interface("test_interface", methods)
        interface1 = Interface("test_interface", methods)

        mediator = AppMediator()

        i = InterfaceManager(mediator)
        i.add_interface(interface)
        try:
            i.add_interface(interface1)
            self.assertRaises(Exception)
        except InterfaceAlreadyExist as detail:
            self.assertEqual(detail.interface_name, "test_interface")