import unittest
from src.models.neural_network import build_complex_model

class TestNeuralNetwork(unittest.TestCase):
    def test_build_complex_model(self):
        model = build_complex_model((32, 32, 3))
        self.assertEqual(len(model.layers), 6)  # Example check for number of layers

if __name__ == '__main__':
    unittest.main() 