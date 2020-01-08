import torch
import torch.nn as nn
import torch.nn.functional as F

torch.set_printoptions(linewidth=120)
torch.set_grad_enabled(True)


class Network(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=128, kernel_size=5)
        self.bn1 = nn.BatchNorm2d(num_features=128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)

        self.conv2 = nn.Conv2d(in_channels=128, out_channels=192, kernel_size=3)
        self.bn2 = nn.BatchNorm2d(num_features=192, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)

        self.conv3 = nn.Conv2d(in_channels=192, out_channels=256, kernel_size=3)
        self.bn3 = nn.BatchNorm2d(num_features=256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)

        self.conv4 = nn.Conv2d(in_channels=256, out_channels=128, kernel_size=3)
        self.bn4 = nn.BatchNorm2d(num_features=128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)

        self.fc1 = nn.Linear(in_features=128 * 4 * 4, out_features=1024)
        self.drop_out = nn.Dropout(p=0.3)

        self.fc2 = nn.Linear(in_features=1024, out_features=512)
        self.drop_out_2 = nn.Dropout(p=0.3)
        self.out = nn.Linear(in_features=512, out_features=9)

    def forward(self, t):
        # 1st conv layer
        t = t.float()
        t = self.conv1(t)
        t = self.bn1(t)
        t = F.relu(t)
        t = F.max_pool2d(t, kernel_size=2, stride=2)

        # 2nd conv layer
        t = self.conv2(t)
        t = self.bn2(t)
        t = F.relu(t)
        t = F.max_pool2d(t, kernel_size=2, stride=2)

        # 3rd conv layer
        t = self.conv3(t)
        t = self.bn3(t)
        t = F.relu(t)
        t = F.max_pool2d(t, kernel_size=2, stride=2)

        # 4th conv layer
        t = self.conv4(t)
        t = self.bn4(t)
        t = F.relu(t)

        # 5th layer
        t = self.fc1(t.reshape(-1, 128 * 4 * 4))
        t = self.drop_out(t)
        t = F.relu(t)

        t = self.fc2(t)
        t = self.drop_out_2(t)
        t = F.relu(t)

        # output layer
        t = self.out(t)
        return t
