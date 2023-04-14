import torch
import joblib
import torch.nn as nn
import torch.nn.functional as F
import __main__
from PIL import Image

class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv0 = nn.Conv2d(3, 1, 1)
        self.conv1 = nn.Conv2d(1, 3, 3)
        self.conv2 = nn.Conv2d(3, 9, 4)
        self.conv3 = nn.Conv2d(9, 27, 3)
        self.conv4 = nn.Conv2d(27, 81, 3)
        self.norm5 = nn.BatchNorm2d(81)
        self.pool = nn.MaxPool2d(2)
        self.fc1 = nn.Linear(81 * 12 * 12, 150)
        self.norm6 = nn.BatchNorm1d(150)
        self.fc2 = nn.Linear(150, 1)
        self.drop = nn.Dropout(p=0.8)

    def forward(self, x):
        x = self.conv0(x)
        x = F.relu(self.pool(self.conv1(x)))
        x = F.relu(self.pool(self.conv2(x)))
        x = F.relu(self.pool(self.conv3(x)))
        x = F.relu(self.pool(self.conv4(x)))
        x = self.norm5(x)
        x = x.view(-1, 81 * 12 * 12)
        x = F.relu(self.fc1(self.drop(x)))
        x = self.norm6(x)
        x = self.fc2(self.drop(x))
        x = x.squeeze(1) # Flatten to [batch_size]
        return x

    def evaluate(self, loader, criterion):
        err = 0
        losst = 0
        pictures = 0
        for i, data in enumerate(loader, 1):
            inputs, labels = data

            outputs = self(inputs)
            loss = criterion(outputs, labels)
            loss.backward()

            err += (torch.sigmoid(outputs).squeeze().round().int() != labels).sum()
            losst += loss.item()
            pictures += len(labels)
        return err/pictures, losst/i
    
setattr(__main__, "Net", Net)
classifier = joblib.load("./model.pkl")
