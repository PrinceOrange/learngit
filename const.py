# -*- coding: utf-8 -*-
# _author_='HAN'

import sys


class _Const:
    class ConstError(TypeError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't rebind const instance attribute %s", name)

        self.__dict__[name] = value


sys.modules[__name__] = _Const()

