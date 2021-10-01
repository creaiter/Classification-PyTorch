import torch

import torchvision
import torchvision.transforms as transforms
from torchvision.datasets import CIFAR10


class Cifar10(object):  
    def __init__(self, cfg):
        self.datapath = cfg.datapath

        self.image_size = 32
        self.num_classes = 10
        self.batch_size = cfg.batch_size

        self.num_workers = cfg.workers
        self.cuda = True if cfg.device == 'gpu' else False

        self.normalize = transforms.Normalize(
            mean=[0.4914, 0.4822, 0.4465],
            std=[0.2023, 0.1994, 0.2010])

    def train_loader(self):
        transform_train = transforms.Compose([
            transforms.RandomCrop(32, padding=4),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            self.normalize,
        ])

        trainset = CIFAR10(
            root=self.datapath, train=True, download=True,
            transform=transform_train)

        train_loader = torch.utils.data.DataLoader(
            trainset,
            batch_size=self.batch_size, shuffle=True,
            num_workers=self.num_workers,
            pin_memory=True if self.cuda else False)
        return train_loader
    
    def val_loader(self):
        transform_val = transforms.Compose([
            transforms.ToTensor(),
            self.normalize,
        ])

        valset = CIFAR10(
            root=self.datapath, train=False, download=True,
            transform=transform_val)

        val_loader = torch.utils.data.DataLoader(
            valset,
            batch_size=self.batch_size, shuffle=False,
            num_workers=self.num_workers,
            pin_memory=True if self.cuda else False)
        return val_loader
    
    def test_loader(self):
        return None


def set_dataset(cfg, image_size, train=True, val=True, test=False):
    assert image_size == 32, "The image size for CIFAR dataset should be 32."
    assert not test, "There is no test data for CIFAR dataset."

    dataset = Cifar10(cfg)

    loaders = {}
    loaders['train'] = dataset.train_loader() if train else None
    loaders['val'] = dataset.val_loader() if val else None
    loaders['test'] = dataset.test_loader() if test else None
    return loaders