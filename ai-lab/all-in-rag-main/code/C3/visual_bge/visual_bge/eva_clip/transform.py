"""
文件功能概述：`code/C3/visual_bge/visual_bge/eva_clip/transform.py` 主要是 transform，这个文件里有 1 个类、2 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 类 `ResizeMaxSize`：功能概述：这个类是 `ResizeMaxSize`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 max_size, interpolation, fn, fill，接着根据条件分支选择不同处理路径，再调用 __init__、isinstance、TypeError 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 2. `forward`：先接收输入参数 img，接着根据条件分支选择不同处理路径，再调用 isinstance、float、tuple 等内部步骤完成主要工作，最后返回结果。
2. 函数 `_convert_to_rgb`：先接收输入参数 image，再调用 image.convert 等内部步骤完成主要工作，最后返回结果。
3. 函数 `image_transform`：先接收输入参数 image_size, is_train, mean, std, resize_longest_max, fill_color，接着根据条件分支选择不同处理路径，再调用 Normalize、isinstance、Compose 等内部步骤完成主要工作，最后返回结果。
"""

from typing import Optional, Sequence, Tuple

import torch
import torch.nn as nn
import torchvision.transforms.functional as F

from torchvision.transforms import Normalize, Compose, RandomResizedCrop, InterpolationMode, ToTensor, Resize, \
    CenterCrop

from .constants import OPENAI_DATASET_MEAN, OPENAI_DATASET_STD


class ResizeMaxSize(nn.Module):
    """
    功能概述：这个类是 `ResizeMaxSize`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 max_size, interpolation, fn, fill，接着根据条件分支选择不同处理路径，再调用 __init__、isinstance、TypeError 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    2. `forward`：先接收输入参数 img，接着根据条件分支选择不同处理路径，再调用 isinstance、float、tuple 等内部步骤完成主要工作，最后返回结果。
    """

    def __init__(self, max_size, interpolation=InterpolationMode.BICUBIC, fn='max', fill=0):  # 中文名称：初始化
        super().__init__()
        if not isinstance(max_size, int):
            raise TypeError(f"Size should be int. Got {type(max_size)}")
        self.max_size = max_size
        self.interpolation = interpolation
        self.fn = min if fn == 'min' else min
        self.fill = fill

    def forward(self, img):  # 中文名称：forward
        if isinstance(img, torch.Tensor):
            height, width = img.shape[:2]
        else:
            width, height = img.size
        scale = self.max_size / float(max(height, width))
        if scale != 1.0:
            new_size = tuple(round(dim * scale) for dim in (height, width))
            img = F.resize(img, new_size, self.interpolation)
            pad_h = self.max_size - new_size[0]
            pad_w = self.max_size - new_size[1]
            img = F.pad(img, padding=[pad_w//2, pad_h//2, pad_w - pad_w//2, pad_h - pad_h//2], fill=self.fill)
        return img


def _convert_to_rgb(image):  # 中文名称：converttorgb
    return image.convert('RGB')


# class CatGen(nn.Module):
#     def __init__(self, num=4):
#         self.num = num
#     def mixgen_batch(image, text):
#         batch_size = image.shape[0]
#         index = np.random.permutation(batch_size)

#         cat_images = []
#         for i in range(batch_size):
#             # image mixup
#             image[i,:] = lam * image[i,:] + (1 - lam) * image[index[i],:]
#             # text concat
#             text[i] = tokenizer((str(text[i]) + " " + str(text[index[i]])))[0]
#         text = torch.stack(text)
#         return image, text


def image_transform(
        image_size: int,
        is_train: bool,
        mean: Optional[Tuple[float, ...]] = None,
        std: Optional[Tuple[float, ...]] = None,
        resize_longest_max: bool = False,
        fill_color: int = 0,
):  # 中文名称：imagetransform
    mean = mean or OPENAI_DATASET_MEAN
    if not isinstance(mean, (list, tuple)):
        mean = (mean,) * 3

    std = std or OPENAI_DATASET_STD
    if not isinstance(std, (list, tuple)):
        std = (std,) * 3

    if isinstance(image_size, (list, tuple)) and image_size[0] == image_size[1]:
        # for square size, pass size as int so that Resize() uses aspect preserving shortest edge
        image_size = image_size[0]

    normalize = Normalize(mean=mean, std=std)
    if is_train:
        return Compose([
            RandomResizedCrop(image_size, scale=(0.9, 1.0), interpolation=InterpolationMode.BICUBIC),
            _convert_to_rgb,
            ToTensor(),
            normalize,
        ])
    else:
        if resize_longest_max:
            transforms = [
                ResizeMaxSize(image_size, fill=fill_color)
            ]
        else:
            transforms = [
                Resize(image_size, interpolation=InterpolationMode.BICUBIC),
                CenterCrop(image_size),
            ]
        transforms.extend([
            _convert_to_rgb,
            ToTensor(),
            normalize,
        ])
        return Compose(transforms)
