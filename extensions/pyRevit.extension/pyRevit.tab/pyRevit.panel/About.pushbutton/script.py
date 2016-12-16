# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2016 Ehsan Iran-Nejad
Python scripts for Autodesk Revit

This file is part of pyRevit repository at https://github.com/eirannejad/pyRevit

pyRevit is a free set of scripts for Autodesk Revit: you can redistribute it and/or modify
it under the terms of the GNU General Public License version 3, as published by
the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

See this link for a copy of the GNU General Public License protecting this package.
https://github.com/eirannejad/pyRevit/blob/master/LICENSE
"""


import sys
import clr
import os
import webbrowser
from pyrevit.versionmgr import PYREVIT_VERSION

clr.AddReference('PresentationCore')
clr.AddReferenceByPartialName("PresentationFramework")
clr.AddReference('IronPython.Wpf')

# noinspection PyUnresolvedReferences
from System import Uri
# noinspection PyUnresolvedReferences
from System.Windows import Window
# noinspection PyUnresolvedReferences
from System.Windows.Media.Imaging import BitmapImage
# noinspection PyUnresolvedReferences
import wpf


folder = os.path.dirname(__file__)


__doc__ = 'About pyrevit. Opens the pyrevit blog website. You can find detailed information on how pyrevit works, ' \
          'updates about the new tools and changes, and a lot of other information there.'


class MyWindow(Window):
    def __init__(self):
        wpf.LoadComponent(self, os.path.join(folder, 'AboutWindow.xaml'))
        self.image_credits.Source = BitmapImage(Uri(os.path.join(folder, 'credits.png')))
        self.pyrevit_logo.Source = BitmapImage(Uri(os.path.join(folder, 'pyRevitlogo.png')))
        self.keybase_profile.Source = BitmapImage(Uri(os.path.join(folder, 'keybase.png')))
        self.version_info.Text = 'v {}'.format(PYREVIT_VERSION.get_formatted())
        self.pyrevit_subtitle.Text += '\nRunning on IronPython {}.{}.{}'.format(sys.version_info.major,
                                                                                sys.version_info.minor,
                                                                                sys.version_info.micro)

    # noinspection PyUnusedLocal
    # noinspection PyMethodMayBeStatic
    def opengithubrepopage(self, sender, args):
        webbrowser.open_new_tab('https://github.com/eirannejad/pyRevit')

    # noinspection PyUnusedLocal
    # noinspection PyMethodMayBeStatic
    def opengithubcommits(self, sender, args):
        webbrowser.open_new_tab('https://github.com/eirannejad/pyRevit/commits/master')

    # noinspection PyUnusedLocal
    # noinspection PyMethodMayBeStatic
    def openrevisionhistory(self, sender, args):
        webbrowser.open_new_tab('http://eirannejad.github.io/pyRevit/releasenotes/')

    # noinspection PyUnusedLocal
    # noinspection PyMethodMayBeStatic
    def opencredits(self, sender, args):
        webbrowser.open_new_tab('http://eirannejad.github.io/pyRevit/credits/')

    # noinspection PyUnusedLocal
    # noinspection PyMethodMayBeStatic
    def openkeybaseprofile(self, sender, args):
        webbrowser.open_new_tab('https://keybase.io/ein')

    # noinspection PyUnusedLocal
    # noinspection PyMethodMayBeStatic
    def handleclick(self, sender, args):
        self.Close()


if __name__ == '__main__':
    MyWindow().ShowDialog()
