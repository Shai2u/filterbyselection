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
from qgis.core import QgsProject
from qgis.PyQt.QtCore import pyqtSignal


sys.modules["qgsfieldcombobox"] = qgis.gui
sys.modules["qgsmaplayercombobox"] = qgis.gui

try:
    from qgis.core import QgsMapLayerRegistry
except ImportError:
    pass

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'forms/ui_filter.ui'))


class FilterByFeatureDialog(QtWidgets.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, iface, parent=None):
        QtWidgets.QDockWidget.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)

        self.setupUi(self)
        self.iface = iface

        # self.rdo_single.toggled.connect(self.single_or_multi)
        # self.rdo_multi.toggled.connect(self.single_or_multi)

        self.from_layer_cb.layerChanged.connect(self.add_fields_to_from_box)
        self.filter_layer_cb.layerChanged.connect(self.add_fields_to_filter_box)
        self.from_field_cb.fieldChanged.connect(self.changed_from_field)
        self.filter_field.fieldChanged.connect(self.changed_filter_field)

        # self.list_values.itemSelectionChanged.connect(self.selected_value)
        # self.chb_zoom.toggled.connect(self.do_zooming)

        # self.but_deselect_all.clicked.connect(self.deselect_all)
        # self.but_select_all.clicked.connect(self.select_all)

        # Extra attributes
        self.from_layer = None
        self.from_field = None

        self.filter_layer = None
        self.filter_field = None
        self.add_fields_to_from_box()
        self.add_fields_to_filter_box()


    # def check_layer(self):
    #     if self.layer is None:
    #         self.list_values.clear()
    #         return False
    #     if self.layer not in QgsProject.instance().mapLayers().values():
    #         self.list_values.clear()
    #         return False
    #     if not isinstance(self.layer, qgis.core.QgsVectorLayer):
    #         return False
    #     return True

    # def single_or_multi(self):
    #     if self.rdo_single.isChecked():
    #         self.deselect_all()
    #         self.list_values.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
    #     else:
    #         self.list_values.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)

    def add_fields_to_from_box(self):
        # self.reset_filter()
        self.from_layer = self.from_layer_cb.currentLayer()
        self.from_layer.selectionChanged.connect(self.change_seleciton)
        self.from_field = None
        # if self.check_layer():
        self.from_field_cb.setLayer(self.from_layer)
        self.changed_from_field()

        # else:
        # if not isinstance(self.layer, qgis.core.QgsVectorLayer):
        #     self.layer = None
    
    def add_fields_to_filter_box(self):
        # self.reset_filter()
        self.filter_layer = self.filter_layer_cb.currentLayer()
        self.filter_field = None
        self.filter_field_cb.setLayer(self.filter_layer)
        self.filter_field_cb.setField(self.from_field)
        self.changed_filter_field()

    def changed_from_field(self):
        # self.reset_filter()
        self.from_field = self.from_field_cb.currentField()
        self.changed_filter_field()

    def changed_filter_field(self):
        # self.reset_filter()
        self.from_field = self.from_field_cb.currentField()

    def change_seleciton(self):
        selected_features_count = self.filter_layer.selectedFeatureCount()
        # Do something with the number of selected features
        if selected_features_count == 0:

            self.features_selected_label.setText("No selected features")
        elif selected_features_count == 1:
            selected_features = self.filter_layer.selectedFeatures()
            for feature in selected_features:
                # Get the value of the specified field for each selected feature
                field_value = feature.attribute(self.from_field)
                self.features_selected_label.setText(f"{self.from_field} : {field_value}")

        else:
            self.features_selected_label.setText("Number of Selected Features: {}".format(selected_features_count))

    # def reset_filter(self):
    #     if self.check_layer():
    #         self.layer.setSubsetString("")

    # def do_filtering(self):
    #     if not self.check_layer():
    #         return
    #     table = self.list_values
    #     table.clear()

    #     idx = self.layer.dataProvider().fieldNameIndex(self.field)
    #     values = sorted(str(value) for value in self.layer.uniqueValues(idx))
    #     table.addItems(values)
    #     self.select_all()
        # for v in set(values):
        #     it = QtWidgets.QListWidgetItem(str(v))
        #     table.addItem(it)
        #     it.setSelected(True)

    # def do_zooming(self):
    #     if self.chb_zoom.isChecked():
    #         self.iface.setActiveLayer(self.layer)
    #         self.iface.zoomToActiveLayer()

    # def selected_value(self):
    #     if self.chb_go.isChecked():
    #         l = [i.text() for i in self.list_values.selectedItems()]
    #         if l:
    #             self.apply_filter(l)

    def apply_filter(self, list_of_values):
        if not self.check_layer():
            return

        filter_expression = '"{}" = \'{}\''.format(self.field, list_of_values[0])
        if len(list_of_values) > 1:
            for i in list_of_values[1:]:
                filter_expression = filter_expression + ' OR "{}" = \'{}\''.format(self.field, i)
        self.layer.setSubsetString(filter_expression)

        # self.do_zooming()

    # def deselect_all(self):
    #     self.list_values.clearSelection()

    # def select_all(self):
    #     self.list_values.selectAll()

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()