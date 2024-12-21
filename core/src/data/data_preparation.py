import sqlite3
import numpy as np
from sklearn.model_selection import train_test_split
from src.feature_extraction import PacketFeatureExtractor

class DataPreparation:
    def __init__(self, db_path):
        self.db_path = db_path
        self.feature_extractor = PacketFeatureExtractor()

    def load_data(self):
        """Load packet data from the SQLite database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM packets")
        rows = cursor.fetchall()
        
        conn.close()
        
        print(f"Rows fetched from database: {len(rows)}")  # Debugging line
        return rows

    def prepare_data(self):
        """Prepare the dataset for training."""
        data = self.load_data()
        
        features = []
        labels = []
        
        for row in data:
            packet_info = {
                'timestamp': row[0],
                'src_ip': row[1],
                'dst_ip': row[2],
                'protocol': row[3],
                'length': row[4],
                'src_port': row[5],
                'dst_port': row[6],
                'payload': row[7],
                'flags': row[8]
            }
            
            # Extract features
            feature_vector = self.feature_extractor.extract_features(packet_info)
            features.append(feature_vector)
            
            # Assuming the last column in the database indicates if the packet is malicious (1) or benign (0)
            label = self.get_label_from_packet_info(packet_info)  # Implement this method based on your labeling logic
            labels.append(label)

        print(f"Features collected: {len(features)}, Labels collected: {len(labels)}")  # Debugging line
        
        # Convert to numpy arrays
        X = np.array(features)
        y = np.array(labels)

        # Split the data into training and testing sets
        return train_test_split(X, y, test_size=0.2, random_state=42)

    def get_label_from_packet_info(self, packet_info):
        """Determine the label for the packet (malicious or benign)."""
        # Implement your logic to determine if the packet is malicious or benign
        return 0  # Replace with actual logic

# Example usage
if __name__ == "__main__":
    data_preparation = DataPreparation(db_path="packets.db")
    X_train, X_test, y_train, y_test = data_preparation.prepare_data()
    print(f"Training set size: {X_train.shape}, Testing set size: {X_test.shape}") 