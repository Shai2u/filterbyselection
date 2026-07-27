"""
****************************************************************
 Filter by Selection
                              -------------------
        begin                : 2024-05-31
        copyright            : Shai Sussman
        email                : shai.sussman@gmail.com
****************************************************************
"""

from __future__ import absolute_import
import os.path
from typing import List, Optional, TYPE_CHECKING

from qgis.PyQt.QtCore import Qt, QSettings, QTranslator, qVersion, QCoreApplication
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtGui import QIcon
from .filter_by_selection_dialog import FilterBySelectionDialog

if TYPE_CHECKING:
    from qgis.gui import QgisInterface


class filterBySelection:
    """QGIS Plugin Implementation."""

    def __init__(self, iface: "QgisInterface") -> None:
        """Store a reference to the QGIS interface and initialize plugin state.

        Args:
            iface: The QGIS interface instance.
        """
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.icon_path = os.path.join(self.plugin_dir, 'filter_icon.png')
        self.actions: List[QAction] = []
        self.menu = self.tr(u'&FilterBySelection')
        self.pluginIsActive = False
        self.dockwidget: Optional[FilterBySelectionDialog] = None

    def tr(self, message: str) -> str:
        """
        Get the translation for a string using Qt translation API.
        We implement this ourselves since we do not inherit QObject.
        """
        return QCoreApplication.translate('FilterBySelection', message)

    # noinspection PyPep8Naming
    def initGui(self) -> None:
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        """Add a toolbar icon to the toolbar."""
        icon = QIcon(self.icon_path)
        self.panelAction = QAction(icon, self.tr(u'FilterBySelection'), self.iface.mainWindow())
        self.panelAction.triggered.connect(self.run)
        self.panelAction.setCheckable(True)
        self.panelAction.setEnabled(True)

        self.iface.addToolBarIcon(self.panelAction)
        self.iface.addPluginToMenu(self.menu, self.panelAction)
        self.actions.append(self.panelAction)

    def unload(self) -> None:
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(self.tr(u'&FilterBySelection'), action)
            self.iface.removeToolBarIcon(action)

    def widgetVisibilityChanged(self, visible: bool) -> None:
        self.panelAction.setChecked(visible)

    def onClosePlugin(self) -> None:
        """Cleanup necessary items here when plugin dockwidget is closed"""

        # disconnects
        self.dockwidget.closingPlugin.disconnect(self.onClosePlugin)

        self.pluginIsActive = False

    def run(self, checked: bool) -> None:
        """Show the plugin dock widget, creating it on first use.

        Args:
            checked: Whether the triggering action is checked (i.e. whether
                the dock widget should be shown or hidden).
        """
        if not self.pluginIsActive:
            self.pluginIsActive = True
            if self.dockwidget is None:
                self.dockwidget = FilterBySelectionDialog(self.iface)
            self.dockwidget.visibilityChanged.connect(self.widgetVisibilityChanged)

            self.dockwidget.closingPlugin.connect(self.onClosePlugin)

            self.iface.addDockWidget(
                area=Qt.DockWidgetArea.LeftDockWidgetArea,
                dockwidget=self.dockwidget,
            )
            
        # The triggered signal includes a bool 
        # that indicates whether the button was checked or unchecked
        self.dockwidget.setVisible(checked)
