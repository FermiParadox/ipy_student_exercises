class_var = 2


class A(object):
    class_var = 'Hi'

    def __init__(self, var=class_var):
        self.var = var
        print(var)

A()
