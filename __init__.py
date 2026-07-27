"""
***************************************************************************
 Filter by Selection
 A QGIS plugin by Shai Sussman

        First developed     2024/05/31
        copyright           Shai Sussman
        contact             shai.sussman@gmail.com
        contributors        Shai Sussman
 ***************************************************************************

"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from qgis.gui import QgisInterface

    from .filterbyselection import filterBySelection


# noinspection PyDocstring,PyPep8Naming
def classFactory(iface: "QgisInterface") -> "filterBySelection":
    """Entry point called by QGIS to instantiate the plugin.

    Args:
        iface: The QGIS interface instance.

    Returns:
        The plugin instance.
    """
    from .filterbyselection import filterBySelection
    return filterBySelection(iface)
