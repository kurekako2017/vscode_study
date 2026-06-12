"""
文件功能概述：`code/C3/visual_bge/visual_bge/eva_clip/timm_model.py` 主要是 timmmodel，这个文件里有 1 个类、0 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 类 `TimmModel`：功能概述：这个类是 `TimmModel`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 model_name, embed_dim, image_size, pool, proj, proj_bias, drop, pretrained，接着根据条件分支选择不同处理路径，再调用 __init__、to_2tuple、timm.create_model 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 2. `lock`：先接收输入参数 unlocked_groups, freeze_bn_stats，再尝试执行核心处理，出错时进入异常兜底，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 self.trunk.parameters、self.trunk.group_matcher、group_parameters 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 3. `set_grad_checkpointing`：先接收输入参数 enable，再尝试执行核心处理，出错时进入异常兜底，再调用 self.trunk.set_grad_checkpointing、logging.warning 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 4. `forward`：先接收输入参数 x，再调用 self.trunk、self.head 等内部步骤完成主要工作，最后返回结果。
"""

import logging
from collections import OrderedDict

import torch
import torch.nn as nn

try:
    import timm
    from timm.models.layers import Mlp, to_2tuple
    try:
        # old timm imports < 0.8.1
        from timm.models.layers.attention_pool2d import RotAttentionPool2d
        from timm.models.layers.attention_pool2d import AttentionPool2d as AbsAttentionPool2d
    except ImportError:
        # new timm imports >= 0.8.1
        from timm.layers import RotAttentionPool2d
        from timm.layers import AttentionPool2d as AbsAttentionPool2d
except ImportError:
    timm = None

from .utils import freeze_batch_norm_2d


class TimmModel(nn.Module):
    """
    功能概述：这个类是 `TimmModel`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 model_name, embed_dim, image_size, pool, proj, proj_bias, drop, pretrained，接着根据条件分支选择不同处理路径，再调用 __init__、to_2tuple、timm.create_model 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    2. `lock`：先接收输入参数 unlocked_groups, freeze_bn_stats，再尝试执行核心处理，出错时进入异常兜底，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 self.trunk.parameters、self.trunk.group_matcher、group_parameters 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    3. `set_grad_checkpointing`：先接收输入参数 enable，再尝试执行核心处理，出错时进入异常兜底，再调用 self.trunk.set_grad_checkpointing、logging.warning 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    4. `forward`：先接收输入参数 x，再调用 self.trunk、self.head 等内部步骤完成主要工作，最后返回结果。
    """

    def __init__(
            self,
            model_name,
            embed_dim,
            image_size=224,
            pool='avg',
            proj='linear',
            proj_bias=False,
            drop=0.,
            pretrained=False):  # 中文名称：初始化
        super().__init__()
        if timm is None:
            raise RuntimeError("Please `pip install timm` to use timm models.")

        self.image_size = to_2tuple(image_size)
        self.trunk = timm.create_model(model_name, pretrained=pretrained)
        feat_size = self.trunk.default_cfg.get('pool_size', None)
        feature_ndim = 1 if not feat_size else 2
        if pool in ('abs_attn', 'rot_attn'):
            assert feature_ndim == 2
            # if attn pooling used, remove both classifier and default pool
            self.trunk.reset_classifier(0, global_pool='')
        else:
            # reset global pool if pool config set, otherwise leave as network default
            reset_kwargs = dict(global_pool=pool) if pool else {}
            self.trunk.reset_classifier(0, **reset_kwargs)
        prev_chs = self.trunk.num_features

        head_layers = OrderedDict()
        if pool == 'abs_attn':
            head_layers['pool'] = AbsAttentionPool2d(prev_chs, feat_size=feat_size, out_features=embed_dim)
            prev_chs = embed_dim
        elif pool == 'rot_attn':
            head_layers['pool'] = RotAttentionPool2d(prev_chs, out_features=embed_dim)
            prev_chs = embed_dim
        else:
            assert proj, 'projection layer needed if non-attention pooling is used.'

        # NOTE attention pool ends with a projection layer, so proj should usually be set to '' if such pooling is used
        if proj == 'linear':
            head_layers['drop'] = nn.Dropout(drop)
            head_layers['proj'] = nn.Linear(prev_chs, embed_dim, bias=proj_bias)
        elif proj == 'mlp':
            head_layers['mlp'] = Mlp(prev_chs, 2 * embed_dim, embed_dim, drop=drop, bias=(True, proj_bias))

        self.head = nn.Sequential(head_layers)

    def lock(self, unlocked_groups=0, freeze_bn_stats=False):  # 中文名称：lock
        """ lock modules
        Args:
            unlocked_groups (int): leave last n layer groups unlocked (default: 0)
        """
        if not unlocked_groups:
            # lock full model
            for param in self.trunk.parameters():
                param.requires_grad = False
            if freeze_bn_stats:
                freeze_batch_norm_2d(self.trunk)
        else:
            # NOTE: partial freeze requires latest timm (master) branch and is subject to change
            try:
                # FIXME import here until API stable and in an official release
                from timm.models.helpers import group_parameters, group_modules
            except ImportError:
                raise RuntimeError(
                    'Please install latest timm `pip install git+https://github.com/rwightman/pytorch-image-models`')
            matcher = self.trunk.group_matcher()
            gparams = group_parameters(self.trunk, matcher)
            max_layer_id = max(gparams.keys())
            max_layer_id = max_layer_id - unlocked_groups
            for group_idx in range(max_layer_id + 1):
                group = gparams[group_idx]
                for param in group:
                    self.trunk.get_parameter(param).requires_grad = False
            if freeze_bn_stats:
                gmodules = group_modules(self.trunk, matcher, reverse=True)
                gmodules = {k for k, v in gmodules.items() if v <= max_layer_id}
                freeze_batch_norm_2d(self.trunk, gmodules)

    @torch.jit.ignore
    def set_grad_checkpointing(self, enable=True):  # 中文名称：设置gradcheckpointing
        try:
            self.trunk.set_grad_checkpointing(enable)
        except Exception as e:
            logging.warning('grad checkpointing not supported for this timm image tower, continuing without...')

    def forward(self, x):  # 中文名称：forward
        x = self.trunk(x)
        x = self.head(x)
        return x
