from src.TextRenderer3D import TextRenderer3D

class TextController3D:
    def __init__(self):
        self.textRenderer3D = []

    def update(self, data):
        num_instances = len(self.textRenderer3D)
        num_data = len(data)

        # Remove excess instances
        if num_data < num_instances:
            self.textRenderer3D = self.textRenderer3D[:num_data]

        # Füge fehlende Instanzen hinzu
        if num_data > num_instances:
            self.textRenderer3D.extend([TextRenderer3D() for _ in range(num_instances, num_data)])

        # Aktualisiere vorhandene Instanzen
        for i in range(min(num_instances, num_data)):
            self.textRenderer3D[i].update(*data[i])


    def render(self):
        for textRenderer in self.textRenderer3D:
            textRenderer.render()


