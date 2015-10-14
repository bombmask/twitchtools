class Operator(object):
    init_on_attach = False

    def __init__(self):
        #super(self).__init__(self)
        pass

    @classmethod
    def poll(cls, *args):
        return True

    def execute(self, *args):
        return {"FINISHED"}
