class Printer(object):

    LEVELS = {"DEBUG", "NOMINAL", "LOGGING", "NONE"}
    EXTRA = {"HIGH", "MED", "LOW", "ALL"}
    ON = True

    def __init__(self, prefix):
        print
        self.prefix = "[ " + str(prefix) + " ]"

    def __call__(self, *args, **kwargs):
        if Printer.level == "DEBUG":
            self.write(args, kwargs)
        

    def user(self, *args, **kwargs):
        if Printer.level == "NOMINAL":
            self.write(args, kwargs)

    def format(self, args, kwargs):
        return str(self.prefix+" "+" ".join(map(str, args)))


    def write(self, args, kwargs):
        if Printer.ON:
            print self.format(args, kwargs)


    @property 
    @classmethod
    def level(cls):
        try:
            return cls._level

        except AttributeError:
            cls._level = "NOMINAL"
            return cls._level

    @level.setter
    @classmethod
    def level(cls, value):
        #if value in regesterd types
        cls._level = value
        #else Raise Type Error