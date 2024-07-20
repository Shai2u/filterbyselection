# Filter by Selection - Your QGIS Fitler buddy!

Quick and intutitive way to filter a lyer or reset a fitler based on a selection from a reference layer

![Image](media/example.png)

[![](https://markdown-videos-api.jorgenkh.no/youtube/QbB1vsQhOrs)](https://youtu.be/QbB1vsQhOrs)

## Description:

Filtering in QGIS can be challenging, with some aspects of the interface needing improvement. Here are a couple of the main issues users encounter:

1. Modal Windows: When you open a modal window in QGIS, you cannot interact with any other part of the application until you click “Cancel” or “OK.” This limitation hinders your ability to integrate the filter with the rest of the QGIS interface.
2. Value Selection: Loading and selecting values from the value window is cumbersome and time-consuming.
3. Lack of reaction to selection of the user.

To address these issues, I have developed a plugin that enhances the QGIS filtering experience.

Filter by Selection is a QGIS plugin designed to enhance spatial analysis by allowing users to quickly filter one layer based on the selected feature and attribute from another layer, or a spreadsheet table. This tool provides a seamless way to apply attribute-based filtering, thereby enabling more precise and targeted data visualization and analysis within QGIS. The tool adds intuitive layer filtering, enabling users to quickly apply filters by a reference feature or attribute, significantly speeding up the process compared to manual filtering. This can cut the time to 1-2 seconds per filter, avoiding the need to open the filter window.

### Example Workflow:

1. Select Source Layer:
   Choose the source layer that contains the features and attributes you want to use for filtering.
2. Select Target Layer:
   Choose the target layer that you wish to filter based on the selected features andattributes from the source layer.
3. Select Features and Attributes:
   Use the tool to select one or more features from the source layer.
   Choose the attribute of interest that will be used to filter the target layer.
4. Apply Filter Quickly:
   Once clicking on "filter" The plugin applies the filter to the target layer.
5. Clear Filter Easily:
   Quickly clear the applied filter with a single action to reset the target layer to itsoriginal state.

### Usage Scenarios In Transporation:

1. Select All City Tracts Based on Selected Few Tracts:
   - Quickly filter city tracts based on the selected few tracts to analyze specific areas of interest.
2. Select Lines by Self Selection:
   - Easily select and filter transportation lines (e.g., bus routes or train tracks) based on user selection for detailed analysis.
3. Filter Routes from Selection:
   - Filter transportation routes based on selected criteria, enabling focused analysis on specific routes.
4. Filter Stops Affiliated to a Certain Route:
   - Identify and filter stops that are associated with a specific route, facilitating targeted route management and planning.
5. Show Where You Can Go from a Specific Stop:
   - Determine and visualize all possible destinations from a selected stop, enhancing route planning and decision-making.
6. Attribute-Based Selection from a CSV File Dictating the GIS File:
   - Perform attribute-based selections using criteria from a CSV file to filter target gis layer effecitvly.
