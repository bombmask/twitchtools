
import json
import os
from glob import iglob
#
# Use this bated VV
class Profile(object):

    def __init__(self, username = None, search=False, oauth = None):
        if oauth:
            self.name = username
            self.password = oauth
            
        elif username:
            if search:
                search = (search if isinstance(search, str) else "./")
                self.lookforuser(username, search)

            else:
                self.extract(username)


    @property
    def name(self):
        """'name' property"""
        return self.username
        
    @name.setter
    def name(self, value):
        self.username = value

    @property
    def password(self):
        """'password' property"""
        return self.key

    @password.setter
    def password(self, value):
        self.key = value


    def export(self, name = None):
        filename = (name if name else self.username)+'.json'
        with open(filename, 'w') as fout:
            fout.write(json.dumps({"profile":self.__dict__}))

    def extract(self, name):
        filename = (name if name else self.username)+'.json'
        with open(filename) as fin:
            self.__dict__ = json.load(fin)["profile"]

    def lookforuser(self, username, path = './'):
        returnpath = os.getcwd()
        os.chdir(path)

        for filename in iglob("*.json"):
            print filename
            print "="*80

            with open(filename) as fin:
                jsondata = json.load(fin)
                if jsondata["profile"]["username"] == username:
                    self.__dict__ = jsondata["profile"]
                    os.chdir(returnpath)
                    return

        os.chdir(returnpath)
        raise NameError("User profile '{}' not found in '{}'".format(username, os.path.abspath(path)))


if __name__ == '__main__':
    t = Profile()
    t.name = "Test_user"
    t.password = "Weak ass pass"
    t.export()
    print t.__dict__

    del t

    m = Profile("Test_user")
    print m.name, m.password, m.__dict__
