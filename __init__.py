"""
***************************************************************************
 Filter by feature
 A QGIS plugin by Shai Sussman

        First developed     2024/05/31
        copyright           Shai Sussman
        contact             shai.sussman@gmail.com
        contributors        Shai Sussman
 ***************************************************************************

"""


# noinspection PyDocstring,PyPep8Naming
def classFactory(iface):
    from .filterbyselection import filterBySelection
    return filterBySelection(iface)
