import torch.nn as nn

class BiLSTMTagger(nn.Module):
    def __init__(self, num_characters, num_tags, embedding_dim, hidden_dim):
        super(BiLSTMTagger, self).__init__()
        self.embedding = nn.Embedding(num_characters, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True, bidirectional=True)
        self.fc = nn.Linear(hidden_dim * 2, num_tags)

    def forward(self, x):
        x = self.embedding(x)
        x, _ = self.lstm(x)
        x = self.fc(x)
        return x