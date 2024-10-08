import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from torch.utils.data import Dataset, DataLoader
import json
import random
import argparse
import os

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Constants
PAD_token = 0
SOS_token = 1
EOS_token = 2
MAX_LENGTH = 20  # Maximum sequence length to consider

# Text preprocessing functions
def tokenize(text):
    tokens = word_tokenize(text.lower())
    tokens = [token for token in tokens if token.isalpha()]  # Remove punctuation and numbers
    return tokens

def lemmatize(tokens):
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(token) for token in tokens]

def remove_stopwords(tokens):
    stop_words = set(stopwords.words('english'))
    return [token for token in tokens if token not in stop_words]

# Define dataset class for conversation pairs
class ConversationDataset(Dataset):
    def __init__(self, data_path):
        self.data_path = data_path
        self.conversations = self.load_data(data_path)
        self.tokenizer = tokenize
        self.lemmatizer = lemmatize
        self.stopwords_remover = remove_stopwords
        self.vocab = self.build_vocab()

    def __len__(self):
        return len(self.conversations)

    def __getitem__(self, idx):
        return self.conversations[idx]

    def load_data(self, data_path):
        with open(data_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    def build_vocab(self):
        vocab = set()
        for conv in self.conversations:
            for utterance in conv['dialog']:
                tokens = self.tokenizer(utterance)
                tokens = self.lemmatizer(tokens)
                tokens = self.stopwords_remover(tokens)
                vocab.update(tokens)
        return {word: idx + 3 for idx, word in enumerate(vocab)}

    def tensorize_batch(self, batch_data):
        input_seqs = []
        target_seqs = []
        for pair in batch_data:
            input_seqs.append([self.vocab[token] for token in self.tokenizer(pair['question'])])
            target_seqs.append([self.vocab[token] for token in self.tokenizer(pair['answer'])])
        input_seqs = self.zero_pad(input_seqs)
        target_seqs = self.zero_pad(target_seqs)
        input_seqs_tensor = torch.LongTensor(input_seqs)
        target_seqs_tensor = torch.LongTensor(target_seqs)
        return input_seqs_tensor, target_seqs_tensor

    def zero_pad(self, seqs):
        padded_seqs = []
        for seq in seqs:
            if len(seq) < MAX_LENGTH:
                seq += [PAD_token] * (MAX_LENGTH - len(seq))
            else:
                seq = seq[:MAX_LENGTH]
            padded_seqs.append(seq)
        return padded_seqs

# Encoder
class EncoderRNN(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(EncoderRNN, self).__init__()
        self.hidden_size = hidden_size
        self.embedding = nn.Embedding(input_size, hidden_size)
        self.gru = nn.GRU(hidden_size, hidden_size)

    def forward(self, input, hidden):
        embedded = self.embedding(input).view(1, 1, -1)
        output = embedded
        output, hidden = self.gru(output, hidden)
        return output, hidden

    def init_hidden(self):
        return torch.zeros(1, 1, self.hidden_size)

# Decoder with attention
class AttnDecoderRNN(nn.Module):
    def __init__(self, hidden_size, output_size, dropout_p=0.1, max_length=MAX_LENGTH):
        super(AttnDecoderRNN, self).__init__()
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.dropout_p = dropout_p
        self.max_length = max_length

        self.embedding = nn.Embedding(self.output_size, self.hidden_size)
        self.attn = nn.Linear(self.hidden_size * 2, self.max_length)
        self.attn_combine = nn.Linear(self.hidden_size * 2, self.hidden_size)
        self.dropout = nn.Dropout(self.dropout_p)
        self.gru = nn.GRU(self.hidden_size, self.hidden_size)
        self.out = nn.Linear(self.hidden_size, self.output_size)

    def forward(self, input, hidden, encoder_outputs):
        embedded = self.embedding(input).view(1, 1, -1)
        embedded = self.dropout(embedded)

        attn_weights = torch.softmax(
            self.attn(torch.cat((embedded[0], hidden[0]), 1)), dim=1)
        attn_applied = torch.bmm(attn_weights.unsqueeze(0),
                                 encoder_outputs.unsqueeze(0))

        output = torch.cat((embedded[0], attn_applied[0]), 1)
        output = self.attn_combine(output).unsqueeze(0)

        output = torch.relu(output)
        output, hidden = self.gru(output, hidden)

        output = torch.log_softmax(self.out(output[0]), dim=1)
        return output, hidden, attn_weights

# Training function
def train(input_tensor, target_tensor, encoder, decoder, encoder_optimizer, decoder_optimizer, criterion, max_length=MAX_LENGTH):
    encoder_hidden = encoder.init_hidden()

    encoder_optimizer.zero_grad()
    decoder_optimizer.zero_grad()

    input_length = input_tensor.size(0)
    target_length = target_tensor.size(0)

    encoder_outputs = torch.zeros(max_length, encoder.hidden_size)

    loss = 0

    for ei in range(input_length):
        encoder_output, encoder_hidden = encoder(
            input_tensor[ei], encoder_hidden)
        encoder_outputs[ei] = encoder_output[0, 0]

    decoder_input = torch.tensor([[SOS_token]])

    decoder_hidden = encoder_hidden

    for di in range(target_length):
        decoder_output, decoder_hidden, decoder_attention = decoder(
            decoder_input, decoder_hidden, encoder_outputs)
        loss += criterion(decoder_output, target_tensor[di])
        decoder_input = target_tensor[di]

    loss.backward()

    encoder_optimizer.step()
    decoder_optimizer.step()

    return loss.item() / target_length

# Greedy decoding function
def greedy_decode(encoder, decoder, vocab, sentence, max_length=MAX_LENGTH):
    with torch.no_grad():
        input_tensor = torch.tensor([vocab[token] for token in tokenize(sentence)])
        input_length = input_tensor.size()[0]
        encoder_hidden = encoder.init_hidden()

        encoder_outputs = torch.zeros(max_length, encoder.hidden_size)

        for ei in range(input_length):
            encoder_output, encoder_hidden = encoder(input_tensor[ei], encoder_hidden)
            encoder_outputs[ei] += encoder_output[0, 0]

        decoder_input = torch.tensor([[SOS_token]])
        decoder_hidden = encoder_hidden

        decoded_words = []

        for di in range(max_length):
            decoder_output, decoder_hidden, _ = decoder(
                decoder_input, decoder_hidden, encoder_outputs)
            _, topi = decoder_output.data.topk(1)
            if topi.item() == EOS_token:
                decoded_words.append('<EOS>')
                break
            else:
                decoded_words.append(vocab[topi.item()])

            decoder_input = topi.squeeze().detach()

        return ' '.join(decoded_words)

# Command-line interface
def parse_arguments():
    parser = argparse.ArgumentParser(description="PyTorch Chatbot Engine")
    parser.add_argument('--data', type=str, required=True, help='Path to JSON file containing conversation data')
    parser.add_argument('--num_epochs', type=int, default=10, help='Number of training epochs')
    parser.add_argument('--hidden_size', type=int, default=256, help='Size of hidden layers for RNN')
    parser.add_argument('--learning_rate', type=float, default=0.01, help='Learning rate for optimizer')
    return parser.parse_args()

def main(args):
    # Load and preprocess data
    dataset = ConversationDataset(args.data)
    vocab_size = len(dataset.vocab) + 3

    # Initialize models
    encoder = EncoderRNN(vocab_size, args.hidden_size)
    decoder = AttnDecoderRNN(args.hidden_size, vocab_size)
    criterion = nn.NLLLoss()
    encoder_optimizer = optim.SGD(encoder.parameters(), lr=args.learning_rate)
    decoder_optimizer = optim.SGD(decoder.parameters(), lr=args.learning_rate)

    # Training loop
    for epoch in range(args.num_epochs):
        total_loss = 0
        for i in range(len(dataset)):
            pair = dataset[i]
            input_tensor, target_tensor = dataset.tensorize_batch([pair])
            loss = train(input_tensor.squeeze(0), target_tensor.squeeze(0), encoder, decoder,
                         encoder_optimizer, decoder_optimizer, criterion)
            total_loss += loss

            print(f'Epoch [{epoch+1}/{args.num_epochs}], Loss: {total_loss / len(dataset):.4f}')

    # Save the trained models
    model_dir = 'models'
    os.makedirs(model_dir, exist_ok=True)
    encoder_path = os.path.join(model_dir, 'encoder.pth')
    decoder_path = os.path.join(model_dir, 'decoder.pth')
    torch.save(encoder.state_dict(), encoder_path)
    torch.save(decoder.state_dict(), decoder_path)
    print(f'Models saved to {encoder_path} and {decoder_path}')

    # Test the chatbot
    encoder.eval()
    decoder.eval()
    while True:
        input_sentence = input("You: ")
        if input_sentence.lower() == 'exit':
            break
        output_sentence = greedy_decode(encoder, decoder, dataset.vocab, input_sentence)
        print(f'Bot: {output_sentence}')

if __name__ == "__main__":
    args = parse_arguments()
    main(args)

