import utils

class Log:
    product_mode="release"

    def __init__(self):
        self.log_type = utils.enum(INFO="INFO", DEBUG="DEBUG", WARNING="WARN", ERROR="ERROR")

    def do_log(self,type, str):
        print "***" + type + ": " + str

    def log(self, str, type=None):
        if (type == self.log_type.WARNING or type == self.log_type.ERROR)\
        or (type == self.log_type.DEBUG and product_mode == "debug")\
        or (type == self.log_type.INFO):
            self.do_log(type,str)

    def log_info(self, str):
        self.log(str, self.log_type.INFO)