# components/embedder.py

class Embedder:
    def __init__(self):
        # Initialize any configuration here
        self.model_config = self.load_model_config()

    def load_model_config(self):
        # Load the model configuration
        return {"key": "value"}  # Example configuration

    def embed_query(self, query):
        # Embed query using the loaded model configuration
        pass
