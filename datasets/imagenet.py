import torch

import torchvision
import torchvision.transforms as transforms
from torchvision.datasets import ImageNet as IMAGENET

# for ignore ImageNet PIL EXIF UserWarning
import warnings
warnings.filterwarnings("ignore", "(Possibly )?corrupt EXIF data", UserWarning)


class ImageNet(object):  
    def __init__(self, cfg, image_size=224):
        self.datapath = cfg.datapath

        self.image_size = image_size
        self.num_classes = 1000
        self.batch_size = cfg.batch_size

        self.num_workers = cfg.workers
        self.cuda = True if cfg.device == 'gpu' else False

        self.normalize = transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225])

        self.transforms_train = [
            transforms.RandomResizedCrop(self.image_size),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
        ]

        self.transforms_val = [
            transforms.Resize(self.image_size + 32),
            transforms.CenterCrop(self.image_size),
            transforms.ToTensor(),
        ]

    def train_loader(self, image_size=224):
        transform_train = transforms.Compose(
            self.transforms_train + [self.normalize]
        )

        trainset = IMAGENET(
            root=self.datapath, split='train', transform=transform_train)

        train_loader = torch.utils.data.DataLoader(
            trainset,
            batch_size=self.batch_size, shuffle=True,
            num_workers=self.num_workers,
            pin_memory=True if self.cuda else False)
        return train_loader
    
    def val_loader(self, image_size=224):
        transform_val = transforms.Compose(
            self.transforms_val + [self.normalize]
        )

        valset = IMAGENET(
            root=self.datapath, split='val', transform=transform_val)

        val_loader = torch.utils.data.DataLoader(
            valset,
            batch_size=self.batch_size, shuffle=False,
            num_workers=self.num_workers,
            pin_memory=True if self.cuda else False)
        return val_loader
    
    def test_loader(self, image_size=224):
        return None


def set_dataset(cfg, image_size=224, train=True, val=True, test=False, hooks=[]):
    assert not test, "There is no test data for ImageNet dataset."

    dataset = ImageNet(cfg, image_size)

    # run hooks
    for func in hooks:
        func(cfg, dataset)

    # set loaders
    loaders = {}
    loaders['train'] = dataset.train_loader(image_size) if train else None
    loaders['val'] = dataset.val_loader(image_size) if val else None
    loaders['test'] = dataset.test_loader(image_size) if test else None
    return loaders