# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connect_me.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
from utils.core import Core

"""
    Main class. Responsible for running the application.
"""
class main:
    @staticmethod
    def run():
        try:
            # defaul path at login page
            #app = Core.openController("login")
            app = Core()
            app.main()
        except Exception as e:
            print(str(e))

if __name__ == "__main__":
    # run core
    main.run()