"""
文件功能概述：`code/C3/visual_bge/visual_bge/eva_clip/modified_resnet.py` 主要是 modifiedresnet，这个文件里有 3 个类、0 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 类 `Bottleneck`：功能概述：这个类是 `Bottleneck`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 inplanes, planes, stride，接着根据条件分支选择不同处理路径，再调用 __init__、nn.Conv2d、nn.BatchNorm2d 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 2. `forward`：先接收输入参数 x，接着根据条件分支选择不同处理路径，再调用 self.act1、self.act2、self.avgpool 等内部步骤完成主要工作，最后返回结果。
2. 类 `AttentionPool2d`：功能概述：这个类是 `AttentionPool2d`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 spacial_dim, embed_dim, num_heads, output_dim，再调用 __init__、nn.Parameter、nn.Linear 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 2. `forward`：先接收输入参数 x，再调用 permute、torch.cat、F.multi_head_attention_forward 等内部步骤完成主要工作，最后返回结果。
3. 类 `ModifiedResNet`：功能概述：这个类是 `ModifiedResNet`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 layers, output_dim, heads, image_size, width，再调用 __init__、nn.Conv2d、nn.BatchNorm2d 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 2. `_make_layer`：先接收输入参数 planes, blocks, stride，然后循环处理每一条数据，再调用 range、nn.Sequential、Bottleneck 等内部步骤完成主要工作，最后返回结果。 3. `init_parameters`：先进入当前步骤，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 nn.init.normal_、resnet_block.named_parameters、name.endswith 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 4. `lock`：先接收输入参数 unlocked_groups, freeze_bn_stats，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 self.parameters、freeze_batch_norm_2d 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 5. `set_grad_checkpointing`：先接收输入参数 enable，最后把结果交给下一步或直接结束。 6. `stem`：先接收输入参数 x，再调用 self.act1、self.act2、self.act3 等内部步骤完成主要工作，最后返回结果。 7. `forward`：先接收输入参数 x，再调用 self.stem、self.layer1、self.layer2 等内部步骤完成主要工作，最后返回结果。
"""

from collections import OrderedDict

import torch
from torch import nn
from torch.nn import functional as F

from .utils import freeze_batch_norm_2d


class Bottleneck(nn.Module):
    """
    功能概述：这个类是 `Bottleneck`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 inplanes, planes, stride，接着根据条件分支选择不同处理路径，再调用 __init__、nn.Conv2d、nn.BatchNorm2d 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    2. `forward`：先接收输入参数 x，接着根据条件分支选择不同处理路径，再调用 self.act1、self.act2、self.avgpool 等内部步骤完成主要工作，最后返回结果。
    """
    expansion = 4

    def __init__(self, inplanes, planes, stride=1):  # 中文名称：初始化
        super().__init__()

        # all conv layers have stride 1. an avgpool is performed after the second convolution when stride > 1
        self.conv1 = nn.Conv2d(inplanes, planes, 1, bias=False)
        self.bn1 = nn.BatchNorm2d(planes)
        self.act1 = nn.ReLU(inplace=True)

        self.conv2 = nn.Conv2d(planes, planes, 3, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)
        self.act2 = nn.ReLU(inplace=True)

        self.avgpool = nn.AvgPool2d(stride) if stride > 1 else nn.Identity()

        self.conv3 = nn.Conv2d(planes, planes * self.expansion, 1, bias=False)
        self.bn3 = nn.BatchNorm2d(planes * self.expansion)
        self.act3 = nn.ReLU(inplace=True)

        self.downsample = None
        self.stride = stride

        if stride > 1 or inplanes != planes * Bottleneck.expansion:
            # downsampling layer is prepended with an avgpool, and the subsequent convolution has stride 1
            self.downsample = nn.Sequential(OrderedDict([
                ("-1", nn.AvgPool2d(stride)),
                ("0", nn.Conv2d(inplanes, planes * self.expansion, 1, stride=1, bias=False)),
                ("1", nn.BatchNorm2d(planes * self.expansion))
            ]))

    def forward(self, x: torch.Tensor):  # 中文名称：forward
        identity = x

        out = self.act1(self.bn1(self.conv1(x)))
        out = self.act2(self.bn2(self.conv2(out)))
        out = self.avgpool(out)
        out = self.bn3(self.conv3(out))

        if self.downsample is not None:
            identity = self.downsample(x)

        out += identity
        out = self.act3(out)
        return out


class AttentionPool2d(nn.Module):
    """
    功能概述：这个类是 `AttentionPool2d`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 spacial_dim, embed_dim, num_heads, output_dim，再调用 __init__、nn.Parameter、nn.Linear 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    2. `forward`：先接收输入参数 x，再调用 permute、torch.cat、F.multi_head_attention_forward 等内部步骤完成主要工作，最后返回结果。
    """
    def __init__(self, spacial_dim: int, embed_dim: int, num_heads: int, output_dim: int = None):  # 中文名称：初始化
        super().__init__()
        self.positional_embedding = nn.Parameter(torch.randn(spacial_dim ** 2 + 1, embed_dim) / embed_dim ** 0.5)
        self.k_proj = nn.Linear(embed_dim, embed_dim)
        self.q_proj = nn.Linear(embed_dim, embed_dim)
        self.v_proj = nn.Linear(embed_dim, embed_dim)
        self.c_proj = nn.Linear(embed_dim, output_dim or embed_dim)
        self.num_heads = num_heads

    def forward(self, x):  # 中文名称：forward
        x = x.reshape(x.shape[0], x.shape[1], x.shape[2] * x.shape[3]).permute(2, 0, 1)  # NCHW -> (HW)NC
        x = torch.cat([x.mean(dim=0, keepdim=True), x], dim=0)  # (HW+1)NC
        x = x + self.positional_embedding[:, None, :].to(x.dtype)  # (HW+1)NC
        x, _ = F.multi_head_attention_forward(
            query=x, key=x, value=x,
            embed_dim_to_check=x.shape[-1],
            num_heads=self.num_heads,
            q_proj_weight=self.q_proj.weight,
            k_proj_weight=self.k_proj.weight,
            v_proj_weight=self.v_proj.weight,
            in_proj_weight=None,
            in_proj_bias=torch.cat([self.q_proj.bias, self.k_proj.bias, self.v_proj.bias]),
            bias_k=None,
            bias_v=None,
            add_zero_attn=False,
            dropout_p=0.,
            out_proj_weight=self.c_proj.weight,
            out_proj_bias=self.c_proj.bias,
            use_separate_proj_weight=True,
            training=self.training,
            need_weights=False
        )

        return x[0]


class ModifiedResNet(nn.Module):
    """
    功能概述：这个类是 `ModifiedResNet`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 layers, output_dim, heads, image_size, width，再调用 __init__、nn.Conv2d、nn.BatchNorm2d 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    2. `_make_layer`：先接收输入参数 planes, blocks, stride，然后循环处理每一条数据，再调用 range、nn.Sequential、Bottleneck 等内部步骤完成主要工作，最后返回结果。
    3. `init_parameters`：先进入当前步骤，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 nn.init.normal_、resnet_block.named_parameters、name.endswith 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    4. `lock`：先接收输入参数 unlocked_groups, freeze_bn_stats，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 self.parameters、freeze_batch_norm_2d 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    5. `set_grad_checkpointing`：先接收输入参数 enable，最后把结果交给下一步或直接结束。
    6. `stem`：先接收输入参数 x，再调用 self.act1、self.act2、self.act3 等内部步骤完成主要工作，最后返回结果。
    7. `forward`：先接收输入参数 x，再调用 self.stem、self.layer1、self.layer2 等内部步骤完成主要工作，最后返回结果。
    """

    def __init__(self, layers, output_dim, heads, image_size=224, width=64):  # 中文名称：初始化
        super().__init__()
        self.output_dim = output_dim
        self.image_size = image_size

        # the 3-layer stem
        self.conv1 = nn.Conv2d(3, width // 2, kernel_size=3, stride=2, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(width // 2)
        self.act1 = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv2d(width // 2, width // 2, kernel_size=3, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(width // 2)
        self.act2 = nn.ReLU(inplace=True)
        self.conv3 = nn.Conv2d(width // 2, width, kernel_size=3, padding=1, bias=False)
        self.bn3 = nn.BatchNorm2d(width)
        self.act3 = nn.ReLU(inplace=True)
        self.avgpool = nn.AvgPool2d(2)

        # residual layers
        self._inplanes = width  # this is a *mutable* variable used during construction
        self.layer1 = self._make_layer(width, layers[0])
        self.layer2 = self._make_layer(width * 2, layers[1], stride=2)
        self.layer3 = self._make_layer(width * 4, layers[2], stride=2)
        self.layer4 = self._make_layer(width * 8, layers[3], stride=2)

        embed_dim = width * 32  # the ResNet feature dimension
        self.attnpool = AttentionPool2d(image_size // 32, embed_dim, heads, output_dim)

        self.init_parameters()

    def _make_layer(self, planes, blocks, stride=1):  # 中文名称：创建layer
        layers = [Bottleneck(self._inplanes, planes, stride)]

        self._inplanes = planes * Bottleneck.expansion
        for _ in range(1, blocks):
            layers.append(Bottleneck(self._inplanes, planes))

        return nn.Sequential(*layers)

    def init_parameters(self):  # 中文名称：初始化parameters
        if self.attnpool is not None:
            std = self.attnpool.c_proj.in_features ** -0.5
            nn.init.normal_(self.attnpool.q_proj.weight, std=std)
            nn.init.normal_(self.attnpool.k_proj.weight, std=std)
            nn.init.normal_(self.attnpool.v_proj.weight, std=std)
            nn.init.normal_(self.attnpool.c_proj.weight, std=std)

        for resnet_block in [self.layer1, self.layer2, self.layer3, self.layer4]:
            for name, param in resnet_block.named_parameters():
                if name.endswith("bn3.weight"):
                    nn.init.zeros_(param)

    def lock(self, unlocked_groups=0, freeze_bn_stats=False):  # 中文名称：lock
        assert unlocked_groups == 0, 'partial locking not currently supported for this model'
        for param in self.parameters():
            param.requires_grad = False
        if freeze_bn_stats:
            freeze_batch_norm_2d(self)

    @torch.jit.ignore
    def set_grad_checkpointing(self, enable=True):
        # FIXME support for non-transformer  # 中文名称：设置gradcheckpointing
        pass

    def stem(self, x):  # 中文名称：stem
        x = self.act1(self.bn1(self.conv1(x)))
        x = self.act2(self.bn2(self.conv2(x)))
        x = self.act3(self.bn3(self.conv3(x)))
        x = self.avgpool(x)
        return x

    def forward(self, x):  # 中文名称：forward
        x = self.stem(x)
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        x = self.attnpool(x)

        return x
