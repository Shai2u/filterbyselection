"""
****************************************************************
 Filter by feature
                              -------------------
        begin                : 2024-05-31
        copyright            : Shai Sussman
        email                : shai.sussman@gmail.com
****************************************************************
"""
import os
import sys

import qgis
from qgis.PyQt import QtWidgets, uic, QtGui, QtCore, QtWidgets
from qgis.PyQt.QtWidgets import *
from qgis.core import QgsProject, QgsVectorLayer, Qgis
from qgis.PyQt.QtCore import pyqtSignal


sys.modules["qgsfieldcombobox"] = qgis.gui
sys.modules["qgsmaplayercombobox"] = qgis.gui

try:
    from qgis.core import QgsMapLayerRegistry
except ImportError:
    pass

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'forms/ui_filter.ui'))


class FilterBySelectionDialog(QtWidgets.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, iface, parent=None):
        QtWidgets.QDockWidget.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)

        self.setupUi(self)
        self.iface = iface


        self.from_layer_cb.layerChanged.connect(self.add_fields_to_from_box)
        self.filter_layer_cb.layerChanged.connect(self.add_fields_to_filter_box)
        self.from_field_cb.fieldChanged.connect(self.changed_from_field)
        self.filter_field_cb.fieldChanged.connect(self.changed_filter_field)
        self.filter_button.clicked.connect(self.set_filter)
        self.clear_button.clicked.connect(self.clear_filter)

     
        # Extra attributes
        self.from_layer = None
        self.from_field = None

        self.filter_layer = None
        self.filter_field = None
        self.add_fields_to_from_box()
        self.add_fields_to_filter_box()


    def add_fields_to_from_box(self):
        self.from_layer = self.from_layer_cb.currentLayer()
        if  (self.from_layer != None) and isinstance(self.from_layer, QgsVectorLayer):
            self.from_layer.selectionChanged.connect(self.change_seleciton)
            self.from_field = None
            self.from_field_cb.setLayer(self.from_layer)
            self.changed_from_field()

    
    def add_fields_to_filter_box(self):
        self.filter_layer = self.filter_layer_cb.currentLayer()
        if (self.filter_layer != None) and isinstance(self.filter_layer, QgsVectorLayer):
            self.filter_field = None
            self.filter_field_cb.setLayer(self.filter_layer)
            self.filter_field_cb.setField(self.from_field)
            self.changed_filter_field()

    def changed_from_field(self):
        # self.reset_filter()
        self.from_field = self.from_field_cb.currentField()
        self.changed_filter_field()

    def changed_filter_field(self):
        self.filter_field = self.filter_field_cb.currentField()

    def change_seleciton(self):
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

    def set_filter(self):
        selected_features = self.from_layer.selectedFeatures()
        if len(selected_features)> 0:
            # get only the unique set
            fields = self.from_layer.fields()
            fieldType = fields.field(self.from_field).type()
            # If field type is Bool, Int, Uint, LongLong, ULongLong, Double
            numberType = fieldType in [1, 2, 3, 4, 5, 6]

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
            self.filter_layer.setSubsetString(query)
        else:
            self.iface.messageBar().pushMessage("Ooops", "Select at least one feature", level=Qgis.Warning, duration=3)



    def clear_filter(self):
        self.filter_layer.setSubsetString('')



    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()