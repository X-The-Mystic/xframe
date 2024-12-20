import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# 1. Packet Representation and Feature Engineering
def extract_features(packet):
    """
    Extract features from a packet including header, payload entropy, and metadata.
    """
    # Header features: normalize IP and protocol fields
    header_features = np.array([
        hash_ip(packet['src_ip']),
        hash_ip(packet['dst_ip']),
        packet['protocol'] / 255.0
    ])
    
    # Payload entropy: quantify randomness in the payload
    payload_entropy = calculate_entropy(packet['payload'])

    # Metadata features: include contextual properties like timestamps and packet size
    metadata_features = np.array([
        normalize_timestamp(packet['timestamp']),
        packet['frequency'],
        len(packet['payload']) / 1500.0  # Normalize by max MTU
    ])

    # Aggregate all features into a single vector
    return np.concatenate([header_features, [payload_entropy], metadata_features])

def hash_ip(ip):
    """
    Convert IP address to a normalized numeric hash value.
    """
    return sum(int(octet) for octet in ip.split('.')) / 1020.0

def normalize_timestamp(timestamp):
    """
    Normalize timestamps to a 24-hour period (seconds in a day).
    """
    return (timestamp % 86400) / 86400.0

def calculate_entropy(payload):
    """
    Compute Shannon entropy of a packet payload.
    """
    byte_counts = np.bincount(np.frombuffer(payload, dtype=np.uint8), minlength=256)
    probabilities = byte_counts / len(payload) if len(payload) > 0 else np.zeros(256)
    entropy = -np.sum(probabilities * np.log2(probabilities + 1e-9))  # Add epsilon to avoid log(0)
    return entropy

# 2. Neural Network Model
def build_model(input_dim):
    """
    Build and compile a multi-layer perceptron model for threat detection.
    """
    model = Sequential([
        Dense(256, activation='relu', input_shape=(input_dim,)),
        BatchNormalization(),
        Dropout(0.4),
        Dense(128, activation='relu'),
        BatchNormalization(),
        Dropout(0.3),
        Dense(64, activation='relu'),
        BatchNormalization(),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer=Adam(learning_rate=0.0001), loss='binary_crossentropy', metrics=['accuracy'])
    return model

# 3. Dataset Preparation and Augmentation
def prepare_data(packet_list):
    """
    Prepare features and labels from the raw packet dataset.
    """
    features = np.array([extract_features(packet) for packet in packet_list])
    labels = np.array([packet['label'] for packet in packet_list])  # 1 for malicious, 0 for benign
    return features, labels

# Example packets for demonstration purposes (replace with real data)
packets = [
    {'src_ip': '192.168.1.1', 'dst_ip': '192.168.1.2', 'protocol': 6, 'payload': b'hello', 'timestamp': 1618044000, 'frequency': 0.01, 'label': 0},
    {'src_ip': '10.0.0.1', 'dst_ip': '172.16.0.1', 'protocol': 17, 'payload': b'\x00\x01\x02\x03\x04', 'timestamp': 1618044010, 'frequency': 0.05, 'label': 1},
    {'src_ip': '203.0.113.1', 'dst_ip': '198.51.100.2', 'protocol': 1, 'payload': b'test packet payload', 'timestamp': 1618044050, 'frequency': 0.02, 'label': 0}
]

features, labels = prepare_data(packets)
scaler = StandardScaler()
features = scaler.fit_transform(features)
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# 4. Train the Model
input_dim = X_train.shape[1]
model = build_model(input_dim)
history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=50, batch_size=16, verbose=2)

# 5. Threat Confidence Scoring
def compute_threat_score(packet, model):
    """
    Compute the confidence score for a given packet.
    """
    features = scaler.transform([extract_features(packet)])
    threat_probability = model.predict(features)[0][0]
    anomaly_score = calculate_entropy(packet['payload']) / 8.0  # Normalize entropy
    confidence_score = 0.7 * threat_probability + 0.3 * anomaly_score
    return confidence_score

# Example usage for scoring
new_packet = {'src_ip': '8.8.8.8', 'dst_ip': '192.0.2.1', 'protocol': 6, 'payload': b'randomdata', 'timestamp': 1618044070, 'frequency': 0.04}
threat_score = compute_threat_score(new_packet, model)
print("Threat Confidence Score:", threat_score)

# 6. Dynamic Defense Rules
def apply_defense(packet, score, threshold=0.5):
    """
    Apply dynamic defense rules based on the computed threat score.
    """
    if score > threshold:
        print("[ALERT] Packet blocked:", packet)
        # Additional actions: log to file or notify admin
    else:
        print("[INFO] Packet allowed:", packet)

apply_defense(new_packet, threat_score)

# 7. Advanced Analysis and Logging
def log_packet_decision(packet, score, action):
    """
    Log the decision made for a packet.
    """
    log_entry = {
        'timestamp': packet['timestamp'],
        'src_ip': packet['src_ip'],
        'dst_ip': packet['dst_ip'],
        'protocol': packet['protocol'],
        'payload_entropy': calculate_entropy(packet['payload']),
        'threat_score': score,
        'action': action
    }
    print("[LOG]:", log_entry)

# Log decision
log_packet_decision(new_packet, threat_score, "blocked" if threat_score > 0.5 else "allowed")

# 8. Evaluation Metrics
def evaluate_model(model, X_test, y_test):
    """
    Evaluate the model on test data and print performance metrics.
    """
    from sklearn.metrics import classification_report, roc_auc_score

    y_pred = (model.predict(X_test) > 0.5).astype(int)
    print("Classification Report:\n", classification_report(y_test, y_pred))
    print("ROC-AUC Score:", roc_auc_score(y_test, y_pred))

# Evaluate the model
evaluate_model(model, X_test, y_test)
