import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score
import matplotlib.pyplot as plt
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow logging

def build_model(input_dim):
    """
    Build and compile a multi-layer perceptron model for threat detection.
    """
    model = Sequential()
    model.add(Dense(128, activation='relu', input_dim=input_dim))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))  # Output layer for binary classification
    model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])
    logging.info("Model built successfully.")
    return model

def train_model(model, X_train, y_train, X_test, y_test):
    """
    Train the model with the provided training and testing data.
    """
    model_checkpoint = ModelCheckpoint('best_model.keras', save_best_only=True, monitor='val_loss')
    early_stopping = EarlyStopping(monitor='val_loss', patience=10)

    history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=50, batch_size=16, 
                        callbacks=[model_checkpoint, early_stopping], verbose=2)
    return history

def evaluate_model(model, X_test, y_test):
    """
    Evaluate the model on test data and print performance metrics.
    """
    y_pred = (model.predict(X_test) > 0.5).astype(int)
    print("Classification Report:\n", classification_report(y_test, y_pred))
    print("ROC-AUC Score:", roc_auc_score(y_test, y_pred))

def plot_training_history(history):
    """
    Plot training and validation accuracy and loss.
    """
    plt.figure(figsize=(12, 4))

    # Plot accuracy
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Train Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title('Model Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()

    # Plot loss
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Model Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()

    plt.tight_layout()
    plt.show()

def save_model(model, model_path='final_model.h5'):
    """
    Save the trained model to a file.
    """
    model.save(model_path)
    logging.info(f"Model saved to {model_path}")

def load_model(model_path='final_model.h5'):
    """
    Load a trained model from a file.
    """
    model = tf.keras.models.load_model(model_path)
    logging.info(f"Model loaded from {model_path}")
    return model

# Example usage
if __name__ == "__main__":
    from skel.data_preparation import DataPreparation

    data_preparation = DataPreparation(db_path="packets.db")
    X_train, X_test, y_train, y_test = data_preparation.prepare_data()

    # Scale features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Build and train the model
    input_dim = X_train.shape[1]
    model = build_model(input_dim)
    history = train_model(model, X_train, y_train, X_test, y_test)

    # Evaluate the model
    evaluate_model(model, X_test, y_test)

    # Plot training history
    plot_training_history(history)

    # Save the final model
    save_model(model) 