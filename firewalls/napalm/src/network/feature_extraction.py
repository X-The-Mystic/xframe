import numpy as np
from scapy.all import *
from scapy.layers.inet import IP, TCP, UDP
from scipy.stats import entropy
import ipaddress
import struct

class PacketFeatureExtractor:
    def __init__(self):
        self.protocol_map = {
            'TCP': 6,
            'UDP': 17,
            'ICMP': 1
        }
        
    def extract_features(self, packet_info):
        """
        Extract comprehensive features from packet information
        Returns: numpy array of normalized features
        """
        features = {}
        
        # Basic header features
        features.update(self._extract_ip_features(packet_info))
        features.update(self._extract_port_features(packet_info))
        features.update(self._extract_protocol_features(packet_info))
        
        # Payload analysis
        features.update(self._analyze_payload(packet_info))
        
        # Metadata features
        features.update(self._extract_metadata(packet_info))
        
        # Convert to numpy array in consistent order
        return self._normalize_features(features)

    def _extract_ip_features(self, packet_info):
        """Extract and normalize IP-related features"""
        features = {}
        
        # Convert IPs to numerical representations
        src_ip = int(ipaddress.IPv4Address(packet_info['src_ip']))
        dst_ip = int(ipaddress.IPv4Address(packet_info['dst_ip']))
        
        features['src_ip_class'] = src_ip >> 24  # First octet
        features['dst_ip_class'] = dst_ip >> 24
        
        # Check if IPs are private
        features['src_is_private'] = int(ipaddress.ip_address(packet_info['src_ip']).is_private)
        features['dst_is_private'] = int(ipaddress.ip_address(packet_info['dst_ip']).is_private)
        
        return features

    def _extract_port_features(self, packet_info):
        """Extract and normalize port-related features"""
        features = {}
        
        src_port = packet_info['src_port'] or 0
        dst_port = packet_info['dst_port'] or 0
        
        features['src_port_normalized'] = src_port / 65535
        features['dst_port_normalized'] = dst_port / 65535
        
        # Common port categories
        features['src_port_well_known'] = int(src_port < 1024)
        features['dst_port_well_known'] = int(dst_port < 1024)
        
        return features

    def _extract_protocol_features(self, packet_info):
        """Extract protocol-related features"""
        features = {}
        
        # One-hot encoding for common protocols
        protocol = packet_info['protocol']
        features['is_tcp'] = int(protocol == 'TCP')
        features['is_udp'] = int(protocol == 'UDP')
        features['is_icmp'] = int(protocol == 'ICMP')
        
        # TCP flags if applicable
        if protocol == 'TCP' and packet_info['flags']:
            flags = packet_info['flags']
            features['tcp_syn'] = int('S' in flags)
            features['tcp_ack'] = int('A' in flags)
            features['tcp_fin'] = int('F' in flags)
            features['tcp_rst'] = int('R' in flags)
        else:
            features.update({
                'tcp_syn': 0,
                'tcp_ack': 0,
                'tcp_fin': 0,
                'tcp_rst': 0
            })
            
        return features

    def _analyze_payload(self, packet_info):
        """Analyze packet payload for various characteristics"""
        features = {}
        payload = packet_info['payload']
        
        if payload:
            # Calculate entropy
            byte_counts = np.srccount(np.frombuffer(payload, dtype=np.uint8), minlength=256)
            probabilities = byte_counts / len(payload)
            features['payload_entropy'] = entropy(probabilities)
            
            # Payload size characteristics
            features['payload_size'] = len(payload) / 1500  # Normalized by MTU
            
            # Analyze byte distribution
            features['null_byte_ratio'] = (payload.count(b'\x00') / len(payload)) if payload else 0
            features['printable_ratio'] = len([b for b in payload if 32 <= b <= 126]) / len(payload)
        else:
            features.update({
                'payload_entropy': 0,
                'payload_size': 0,
                'null_byte_ratio': 0,
                'printable_ratio': 0
            })
            
        return features

    def _extract_metadata(self, packet_info):
        """Extract packet metadata features"""
        features = {}
        
        # Packet length characteristics
        features['packet_size_normalized'] = packet_info['length'] / 1500
        
        return features

    def _normalize_features(self, features_dict):
        """Convert features dictionary to normalized numpy array"""
        # Define consistent feature order
        feature_order = [
            'src_ip_class', 'dst_ip_class', 'src_is_private', 'dst_is_private',
            'src_port_normalized', 'dst_port_normalized',
            'src_port_well_known', 'dst_port_well_known',
            'is_tcp', 'is_udp', 'is_icmp',
            'tcp_syn', 'tcp_ack', 'tcp_fin', 'tcp_rst',
            'payload_entropy', 'payload_size', 'null_byte_ratio', 'printable_ratio',
            'packet_size_normalized'
        ]
        
        # Create feature vector in consistent order
        feature_vector = np.array([features_dict[feature] for feature in feature_order])
        
        return feature_vector
