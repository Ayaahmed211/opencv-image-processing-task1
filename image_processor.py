from base_processor import BaseProcessor
from noise_processor import NoiseMixin
from filter_processor import FilterMixin
from edge_processor import EdgeMixin
from histogram_processor import HistogramMixin

class ImageProcessor(BaseProcessor, NoiseMixin, FilterMixin, EdgeMixin, HistogramMixin):
    """
    Main Image Processor class.
    
    It inherits state management from BaseProcessor, and all image 
    manipulation functions from the specific Domain Mixins.
    """
    pass