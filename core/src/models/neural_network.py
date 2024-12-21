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

def custom_loss(y_true, y_pred):
    """
    Custom loss function that includes a decay term.
    """
    cross_entropy_loss = tf.keras.losses.binary_crossentropy(y_true, y_pred)
    decay_term = 0.01 * tf.reduce_sum(tf.square(y_pred))
    return cross_entropy_loss + decay_term

def build_advanced_model(input_shape):
    """
    Build and compile an advanced neural network model.
    """
    try:
        model = Sequential()
        model.add(Conv2D(64, (3, 3), activation='relu', input_shape=input_shape))
        model.add(BatchNormalization())
        model.add(Dropout(0.3))
        model.add(Conv2D(128, (3, 3), activation='relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.4))
        model.add(Flatten())
        model.add(Dense(256, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)))
        model.add(Dropout(0.5))
        model.add(Dense(1, activation='sigmoid'))  # Output layer for binary classification
        model.compile(optimizer=RMSprop(learning_rate=0.001), loss=custom_loss, metrics=['accuracy'])
        logging.info("Advanced model with custom loss built successfully.")
    except Exception as e:
        logging.error(f"Error building model: {e}")
        raise
    return model

def train_advanced_model(model, X_train, y_train, X_test, y_test):
    """
    Train the advanced model with the provided training and testing data.
    """
    try:
        def lr_schedule(epoch, lr):
            if epoch > 10:
                return lr * 0.5
            return lr

        model_checkpoint = ModelCheckpoint('best_advanced_model.keras', save_best_only=True, monitor='val_loss')
        early_stopping = EarlyStopping(monitor='val_loss', patience=10)
        lr_scheduler = LearningRateScheduler(lr_schedule)

        history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=100, batch_size=64, 
                            callbacks=[model_checkpoint, early_stopping, lr_scheduler], verbose=2)
        logging.info("Advanced model training completed successfully.")
    except Exception as e:
        logging.error(f"Error during advanced model training: {e}")
        raise
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
    from bin.data_preparation import DataPreparation

    data_preparation = DataPreparation(db_path="packets.db")
    X_train, X_test, y_train, y_test = data_preparation.prepare_data()

    # Scale features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Build and train the model
    input_dim = X_train.shape[1]
    model = build_advanced_model(input_dim)
    history = train_advanced_model(model, X_train, y_train, X_test, y_test)

    # Evaluate the model
    evaluate_model(model, X_test, y_test)

    # Plot training history
    plot_training_history(history)

    # Save the final model
    save_model(model) 