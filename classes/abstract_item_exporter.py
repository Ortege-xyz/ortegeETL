class AbstractItemExporter:
    """Abstract class to a item exporter"""
    def open(self):
        pass

    def export_items(self, items):
        pass
    def export_item(self, item):
        pass

    def close(self):
        pass
