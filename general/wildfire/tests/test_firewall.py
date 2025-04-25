import unittest
from src.network.feature_extraction import PacketFeatureExtractor

class TestPacketFeatureExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = PacketFeatureExtractor()

    def test_extract_features(self):
        packet_info = {
            'src_ip': '192.168.1.1',
            'dst_ip': '192.168.1.2',
            'protocol': 'TCP',
            'length': 100,
            'src_port': 80,
            'dst_port': 8080,
            'payload': b'hello',
            'flags': 'S'
        }
        features = self.extractor.extract_features(packet_info)
        self.assertEqual(len(features), 20)  # Adjust based on the number of features

if __name__ == '__main__':
    unittest.main() 