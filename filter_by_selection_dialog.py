"""
****************************************************************
 Filter by Selection
                              -------------------
        begin                : 2024-05-31
        copyright            : Shai Sussman
        email                : shai.sussman@gmail.com
****************************************************************
"""
import os
import sys
from typing import Optional, TYPE_CHECKING

import qgis
from qgis.PyQt import QtWidgets, uic, QtGui, QtCore
from qgis.core import QgsProject, QgsVectorLayer, Qgis, QgsFeatureRequest
from qgis.PyQt.QtCore import pyqtSignal, QVariant

if TYPE_CHECKING:
    from qgis.gui import QgisInterface

sys.modules["qgsfieldcombobox"] = qgis.gui
sys.modules["qgsmaplayercombobox"] = qgis.gui

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui_filter.ui'))

# Field types that should be embedded unquoted in the filter expression.
NUMERIC_FIELD_TYPES = (
    QVariant.Bool,
    QVariant.Int,
    QVariant.UInt,
    QVariant.LongLong,
    QVariant.ULongLong,
    QVariant.Double,
)


class FilterBySelectionDialog(QtWidgets.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, iface: "QgisInterface", parent: Optional[QtWidgets.QWidget] = None) -> None:
        """Wire up the UI signal connections and initialize selection state.

        Args:
            iface: The QGIS interface instance.
            parent: Unused; the dock widget is always created without a
                Qt parent so it can float on top of the QGIS main window.
        """
        QtWidgets.QDockWidget.__init__(self, None, QtCore.Qt.WindowType.WindowStaysOnTopHint)

        self.setupUi(self)
        self.iface = iface


        self.from_layer_cb.layerChanged.connect(self.add_fields_to_from_box)
        self.filter_layer_cb.layerChanged.connect(self.add_fields_to_filter_box)
        self.from_field_cb.fieldChanged.connect(self.changed_from_field)
        self.filter_field_cb.fieldChanged.connect(self.changed_filter_field)
        self.filter_button.clicked.connect(self.set_filter)
        self.select_button.clicked.connect(self.set_selection)
        self.clear_button.clicked.connect(self.clear_filter)


        # Extra attributes
        self.from_layer: Optional[QgsVectorLayer] = None
        self.from_field: Optional[str] = None

        self.filter_layer: Optional[QgsVectorLayer] = None
        self.filter_field: Optional[str] = None
        self.add_fields_to_from_box()
        self.add_fields_to_filter_box()


    def add_fields_to_from_box(self) -> None:
        """Refresh the from-field combo box for the currently selected from-layer."""
        self.from_layer = self.from_layer_cb.currentLayer()
        if  (self.from_layer != None) and isinstance(self.from_layer, QgsVectorLayer):
            self.from_layer.selectionChanged.connect(self.change_seleciton)
            self.from_field = None
            self.from_field_cb.setLayer(self.from_layer)
            self.changed_from_field()


    def add_fields_to_filter_box(self) -> None:
        """Refresh the filter-field combo box for the currently selected filter layer."""
        self.filter_layer = self.filter_layer_cb.currentLayer()
        if (self.filter_layer != None) and isinstance(self.filter_layer, QgsVectorLayer):
            self.filter_field = None
            self.filter_field_cb.setLayer(self.filter_layer)
            self.filter_field_cb.setField(self.from_field)
            self.changed_filter_field()

    def changed_from_field(self) -> None:
        """Update from_field to match the from-field combo box selection."""
        # self.reset_filter()
        self.from_field = self.from_field_cb.currentField()
        self.changed_filter_field()

    def changed_filter_field(self) -> None:
        """Update filter_field to match the filter-field combo box selection."""
        self.filter_field = self.filter_field_cb.currentField()

    def change_seleciton(self) -> None:
        """Update the selected-features label to reflect the from-layer's current selection."""
        selected_features_count = self.from_layer.selectedFeatureCount()
        # Do something with the number of selected features
        if selected_features_count == 0:

            self.features_selected_label.setText("No selected features")
        elif selected_features_count == 1:
            feature =  self.from_layer.selectedFeatures()[0]
            # Get the value of the specified field for each selected feature
            field_value = feature.attribute(self.from_field)
            self.features_selected_label.setText(f"{self.from_field} : {field_value}")

        else:
            self.features_selected_label.setText("Number of Selected Features: {}".format(selected_features_count))
    
    def prepare_selection_query(self) -> str:
        """
        Prepare the selection query based on the selected features and fields.
        Returns:
            str: The selection query string.
        Raises:
            None
        """
        selected_features = self.from_layer.selectedFeatures()
        if len(selected_features)> 0:
            # get only the unique set
            fields = self.from_layer.fields()
            fieldType = fields.field(self.from_field).type()
            numberType = fieldType in NUMERIC_FIELD_TYPES

            # make sure the set of values is unique
            get_values_from_seleceted_items = list(set([selected_feature[self.from_field] for selected_feature in selected_features]))
            selected_items = '('
            for selected_item in get_values_from_seleceted_items:
                if numberType:
                    selected_items += (f"{selected_item} ,")
                else:
                    selected_items += (f"'{selected_item}' ,")

            selected_items = selected_items[0:-1] +')'
            
            self.filter_layer.setSubsetString('')

            # Set the filter expression
        
            query = f"\"{self.filter_field}\" in {selected_items}"
            return query
        else: 
            return '-1'
        
    def set_filter(self) -> None:
        """
        Set the filter for the layer based on the selected features.

        Returns:
            None

        Raises:
            None
        """
        query = self.prepare_selection_query()
        if query != '-1':
            self.filter_layer.setSubsetString(query)
        else:
            self.iface.messageBar().pushMessage("Ooops", "Select at least one feature", level=Qgis.Warning, duration=3)

    def set_selection(self) -> None:
        """Select filter-layer features matching the from-layer's selection.

        The filter layer's subset filter is cleared while the match query is
        built (see prepare_selection_query), then restored before the
        matching features are selected.
        """
        # Remeber the original filter
        original_filter = self.filter_layer.subsetString()

        # Perform Query
        query = self.prepare_selection_query()

        # Return to original filter
        if len(original_filter)>0:
            self.filter_layer.setSubsetString(original_filter)
        if query != '-1':
            # Use QgsFeatureRequest to perform the query
            request = QgsFeatureRequest().setFilterExpression(query)
            # Iterate over the features that match the query and select them
            for feature in self.filter_layer.getFeatures(request):
                self.filter_layer.select(feature.id())
        else:
            self.iface.messageBar().pushMessage("Ooops", "Select at least one feature", level=Qgis.Warning, duration=3)


    def clear_filter(self) -> None:
        """Reset the filter layer's subset filter."""
        self.filter_layer.setSubsetString('')



    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """Emit closingPlugin and accept the widget close event."""
        self.closingPlugin.emit()
        event.accept()