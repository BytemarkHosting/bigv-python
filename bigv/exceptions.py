class BigVGroupMissing(Exception):
    def __init__(self,grp,msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)

class BigVProblem(Exception):
    def __init__(self,msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)

class BigVCollision(Exception):
    def __init__(self,msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


