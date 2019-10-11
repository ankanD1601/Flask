# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 23:13:04 2019

@author: datta
"""

from flask_frozen import Freezer
from myapp import app

freezer = Freezer(app)

if __name__ == '__main__':
    freezer.freeze()