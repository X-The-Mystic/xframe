import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
import argparse
import os

# Define a simple LSTM-based Language Model
class LSTMModel(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, num_layers):
        super(LSTMModel, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, vocab_size)

    def forward(self, x, hidden):
        embedded = self.embedding(x)
        out, hidden = self.lstm(embedded, hidden)
        out = self.fc(out)
        return out, hidden

    def init_hidden(self, batch_size):
        weight = next(self.parameters()).data
        hidden = (weight.new_zeros(num_layers, batch_size, hidden_dim).to(device),
                  weight.new_zeros(num_layers, batch_size, hidden_dim).to(device))
        return hidden

# Custom Dataset class for Language Modeling
class TextDataset(Dataset):
    def __init__(self, data, sequence_length):
        self.data = data
        self.sequence_length = sequence_length

    def __len__(self):
        return len(self.data) - self.sequence_length

    def __getitem__(self, idx):
        chunk = self.data[idx:idx + self.sequence_length]
        return torch.tensor(chunk), torch.tensor(self.data[idx + self.sequence_length])

# Command-line interface
def parse_arguments():
    parser = argparse.ArgumentParser(description="PyTorch Language Modeling Engine")
    parser.add_argument('--data', type=str, required=True, help='Path to text file for training')
    parser.add_argument('--sequence_length', type=int, default=20, help='Sequence length for training')
    parser.add_argument('--batch_size', type=int, default=32, help='Batch size for training')
    parser.add_argument('--embedding_dim', type=int, default=300, help='Dimensionality of word embeddings')
    parser.add_argument('--hidden_dim', type=int, default=512, help='Dimensionality of hidden layers')
    parser.add_argument('--num_layers', type=int, default=2, help='Number of LSTM layers')
    parser.add_argument('--num_epochs', type=int, default=10, help='Number of training epochs')
    parser.add_argument('--learning_rate', type=float, default=0.001, help='Learning rate for optimizer')
    return parser.parse_args()

def main(args):
    # Check device availability
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'Using device: {device}')

    # Load and preprocess data
    with open(args.data, 'r', encoding='utf-8') as f:
        text = f.read()
    vocab = sorted(set(text))
    char_to_index = {char: index for index, char in enumerate(vocab)}
    index_to_char = {index: char for index, char in enumerate(vocab)}
    data = [char_to_index[char] for char in text]

    # Initialize model, loss function, and optimizer
    model = LSTMModel(len(vocab), args.embedding_dim, args.hidden_dim, args.num_layers).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=args.learning_rate)

    # Create DataLoader for training
    dataset = TextDataset(data, args.sequence_length)
    dataloader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True)

    # Training loop
    for epoch in range(args.num_epochs):
        model.train()
        total_loss = 0.0
        for batch_inputs, batch_targets in dataloader:
            batch_inputs, batch_targets = batch_inputs.to(device), batch_targets.to(device)
            optimizer.zero_grad()
            hidden = model.init_hidden(batch_size=args.batch_size)
            outputs, _ = model(batch_inputs, hidden)
            loss = criterion(outputs.view(-1, len(vocab)), batch_targets.view(-1))
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        print(f'Epoch [{epoch+1}/{args.num_epochs}], Loss: {total_loss:.4f}')

    # Save the model
    model_dir = 'models'
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, 'lm_model.pth')
    torch.save(model.state_dict(), model_path)
    print(f'Model saved to {model_path}')

if __name__ == "__main__":
    args = parse_arguments()
    main(args)
