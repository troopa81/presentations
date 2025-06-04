"""
Model exported as python.
Name : Modèle
Group : 
With QGIS : 34300
"""

from typing import Any, Optional

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingContext
from qgis.core import QgsProcessingFeedback, QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterMultipleLayers
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterFeatureSink
from qgis import processing


class Modle(QgsProcessingAlgorithm):

    def initAlgorithm(self, config: Optional[dict[str, Any]] = None):
        self.addParameter(QgsProcessingParameterVectorLayer('communes', 'Communes', defaultValue=None))
        self.addParameter(QgsProcessingParameterMultipleLayers('raster_sentinelsB4', 'Raster Sentinels B4', layerType=QgsProcessing.TypeRaster, defaultValue=None))
        self.addParameter(QgsProcessingParameterMultipleLayers('raster_sentinelsB8', 'Raster Sentinels', layerType=QgsProcessing.TypeRaster, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Zonesvertes', 'ZonesVertes', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters: dict[str, Any], context: QgsProcessingContext, model_feedback: QgsProcessingFeedback) -> dict[str, Any]:
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        results = {}
        outputs = {}

        rastersB4 = self.parameterAsLayerList(parameters, "raster_sentinelsB4", context)
        rastersB8 = self.parameterAsLayerList(parameters, "raster_sentinelsB8", context)
        
        communes = parameters['communes']

        for i, (B4, B8) in enumerate(zip(rastersB4, rastersB8)):

            # last model call should output in our defined out, the other one in temporary output
            alg_output = QgsProcessing.TEMPORARY_OUTPUT if i<len(rastersB4)-1 else parameters['Zonesvertes']

            # Analyse des zones vertes
            alg_params = {
                'communes': communes,
                'raster_sentinel_bande_4': B4,
                'raster_sentinel_bande_8': B8,
                'analyse_des_zones_vertes': alg_output,
                'nom_du_champs' : f"green_area_{i}"
            }

            # kind of a bug here, we need to clear model result, if not QGIS could consider the model
            # algorithms already run
            context.clearModelResult()
            
            new_layer = processing.run('model:Analyse des zones vertes',
                                       alg_params, context=context, feedback=feedback,
                                       is_child_algorithm=True)

            communes = new_layer['analyse_des_zones_vertes']

        results["Zonesvertes"] = communes
                
        return results


    def name(self) -> str:
        return 'ExampleFOR'

    def displayName(self) -> str:
        return 'ExampleFOR'

    def group(self) -> str:
        return ''

    def groupId(self) -> str:
        return ''

    def createInstance(self):
        return self.__class__()
