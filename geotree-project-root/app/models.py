from app import geotree

class Tree(geotree.Model):
    id = geotree.Column(geotree.Integer, primary_key=True)  # Corrección aquí
    photo_url = geotree.Column(geotree.String, nullable=False)
    latitude = geotree.Column(geotree.Float, nullable=False)
    longitude = geotree.Column(geotree.Float, nullable=False)
    description = geotree.Column(geotree.String, nullable=True)
    timestamp = geotree.Column(geotree.DateTime, nullable=False)
    user = geotree.Column(geotree.String, nullable=False)

    def __repr__(self):
        return f'<Tree {self.id}>'

