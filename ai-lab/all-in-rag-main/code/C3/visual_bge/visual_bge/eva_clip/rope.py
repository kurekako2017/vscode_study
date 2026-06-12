"""
文件功能概述：`code/C3/visual_bge/visual_bge/eva_clip/rope.py` 主要是 rope，这个文件里有 2 个类、2 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 函数 `broadcat`：先接收输入参数 tensors, dim，再调用 len、set、list 等内部步骤完成主要工作，最后返回结果。
2. 函数 `rotate_half`：先接收输入参数 x，再调用 rearrange、x.unbind、torch.stack 等内部步骤完成主要工作，最后返回结果。
3. 类 `VisionRotaryEmbedding`：功能概述：这个类是 `VisionRotaryEmbedding`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 dim, pt_seq_len, ft_seq_len, custom_freqs, freqs_for, theta, max_freq, num_freqs，接着根据条件分支选择不同处理路径，再调用 __init__、torch.einsum、repeat 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 2. `forward`：先接收输入参数 t, start_index，再调用 torch.cat、rotate_half 等内部步骤完成主要工作，最后返回结果。
4. 类 `VisionRotaryEmbeddingFast`：功能概述：这个类是 `VisionRotaryEmbeddingFast`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 dim, pt_seq_len, ft_seq_len, custom_freqs, freqs_for, theta, max_freq, num_freqs, patch_dropout，接着根据条件分支选择不同处理路径，再调用 __init__、torch.einsum、repeat 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 2. `forward`：先接收输入参数 t, patch_indices_keep，接着根据条件分支选择不同处理路径，再调用 torch.arange、repeat、rearrange 等内部步骤完成主要工作，最后返回结果。
"""

from math import pi
import torch
from torch import nn
from einops import rearrange, repeat
import logging

def broadcat(tensors, dim = -1):  # 中文名称：broadcat
    num_tensors = len(tensors)
    shape_lens = set(list(map(lambda t: len(t.shape), tensors)))
    assert len(shape_lens) == 1, 'tensors must all have the same number of dimensions'
    shape_len = list(shape_lens)[0]
    dim = (dim + shape_len) if dim < 0 else dim
    dims = list(zip(*map(lambda t: list(t.shape), tensors)))
    expandable_dims = [(i, val) for i, val in enumerate(dims) if i != dim]
    assert all([*map(lambda t: len(set(t[1])) <= 2, expandable_dims)]), 'invalid dimensions for broadcastable concatentation'
    max_dims = list(map(lambda t: (t[0], max(t[1])), expandable_dims))
    expanded_dims = list(map(lambda t: (t[0], (t[1],) * num_tensors), max_dims))
    expanded_dims.insert(dim, (dim, dims[dim]))
    expandable_shapes = list(zip(*map(lambda t: t[1], expanded_dims)))
    tensors = list(map(lambda t: t[0].expand(*t[1]), zip(tensors, expandable_shapes)))
    return torch.cat(tensors, dim = dim)

def rotate_half(x):  # 中文名称：rotatehalf
    x = rearrange(x, '... (d r) -> ... d r', r = 2)
    x1, x2 = x.unbind(dim = -1)
    x = torch.stack((-x2, x1), dim = -1)
    return rearrange(x, '... d r -> ... (d r)')


class VisionRotaryEmbedding(nn.Module):
    """
    功能概述：这个类是 `VisionRotaryEmbedding`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 dim, pt_seq_len, ft_seq_len, custom_freqs, freqs_for, theta, max_freq, num_freqs，接着根据条件分支选择不同处理路径，再调用 __init__、torch.einsum、repeat 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    2. `forward`：先接收输入参数 t, start_index，再调用 torch.cat、rotate_half 等内部步骤完成主要工作，最后返回结果。
    """
    def __init__(
        self,
        dim,
        pt_seq_len,
        ft_seq_len=None,
        custom_freqs = None,
        freqs_for = 'lang',
        theta = 10000,
        max_freq = 10,
        num_freqs = 1,
    ):  # 中文名称：初始化
        super().__init__()
        if custom_freqs:
            freqs = custom_freqs
        elif freqs_for == 'lang':
            freqs = 1. / (theta ** (torch.arange(0, dim, 2)[:(dim // 2)].float() / dim))
        elif freqs_for == 'pixel':
            freqs = torch.linspace(1., max_freq / 2, dim // 2) * pi
        elif freqs_for == 'constant':
            freqs = torch.ones(num_freqs).float()
        else:
            raise ValueError(f'unknown modality {freqs_for}')

        if ft_seq_len is None: ft_seq_len = pt_seq_len
        t = torch.arange(ft_seq_len) / ft_seq_len * pt_seq_len

        freqs_h = torch.einsum('..., f -> ... f', t, freqs)
        freqs_h = repeat(freqs_h, '... n -> ... (n r)', r = 2)

        freqs_w = torch.einsum('..., f -> ... f', t, freqs)
        freqs_w = repeat(freqs_w, '... n -> ... (n r)', r = 2)

        freqs = broadcat((freqs_h[:, None, :], freqs_w[None, :, :]), dim = -1) 

        self.register_buffer("freqs_cos", freqs.cos())
        self.register_buffer("freqs_sin", freqs.sin())

        logging.info(f'Shape of rope freq: {self.freqs_cos.shape}')

    def forward(self, t, start_index = 0):  # 中文名称：forward
        rot_dim = self.freqs_cos.shape[-1]
        end_index = start_index + rot_dim
        assert rot_dim <= t.shape[-1], f'feature dimension {t.shape[-1]} is not of sufficient size to rotate in all the positions {rot_dim}'
        t_left, t, t_right = t[..., :start_index], t[..., start_index:end_index], t[..., end_index:]
        t = (t * self.freqs_cos) + (rotate_half(t) * self.freqs_sin)

        return torch.cat((t_left, t, t_right), dim = -1)

class VisionRotaryEmbeddingFast(nn.Module):
    """
    功能概述：这个类是 `VisionRotaryEmbeddingFast`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 dim, pt_seq_len, ft_seq_len, custom_freqs, freqs_for, theta, max_freq, num_freqs, patch_dropout，接着根据条件分支选择不同处理路径，再调用 __init__、torch.einsum、repeat 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    2. `forward`：先接收输入参数 t, patch_indices_keep，接着根据条件分支选择不同处理路径，再调用 torch.arange、repeat、rearrange 等内部步骤完成主要工作，最后返回结果。
    """
    def __init__(
        self,
        dim,
        pt_seq_len,
        ft_seq_len=None,
        custom_freqs = None,
        freqs_for = 'lang',
        theta = 10000,
        max_freq = 10,
        num_freqs = 1,
        patch_dropout = 0.
    ):  # 中文名称：初始化
        super().__init__()
        if custom_freqs:
            freqs = custom_freqs
        elif freqs_for == 'lang':
            freqs = 1. / (theta ** (torch.arange(0, dim, 2)[:(dim // 2)].float() / dim))
        elif freqs_for == 'pixel':
            freqs = torch.linspace(1., max_freq / 2, dim // 2) * pi
        elif freqs_for == 'constant':
            freqs = torch.ones(num_freqs).float()
        else:
            raise ValueError(f'unknown modality {freqs_for}')

        if ft_seq_len is None: ft_seq_len = pt_seq_len
        t = torch.arange(ft_seq_len) / ft_seq_len * pt_seq_len

        freqs = torch.einsum('..., f -> ... f', t, freqs)
        freqs = repeat(freqs, '... n -> ... (n r)', r = 2)
        freqs = broadcat((freqs[:, None, :], freqs[None, :, :]), dim = -1)

        freqs_cos = freqs.cos().view(-1, freqs.shape[-1])
        freqs_sin = freqs.sin().view(-1, freqs.shape[-1])

        self.patch_dropout = patch_dropout

        self.register_buffer("freqs_cos", freqs_cos)
        self.register_buffer("freqs_sin", freqs_sin)

        logging.info(f'Shape of rope freq: {self.freqs_cos.shape}')

    def forward(self, t, patch_indices_keep=None):  # 中文名称：forward
        if patch_indices_keep is not None:
            batch = t.size()[0]
            batch_indices = torch.arange(batch)
            batch_indices = batch_indices[..., None]

            freqs_cos = repeat(self.freqs_cos, 'i j -> n i m j', n=t.shape[0], m=t.shape[1])
            freqs_sin = repeat(self.freqs_sin, 'i j -> n i m j', n=t.shape[0], m=t.shape[1])

            freqs_cos = freqs_cos[batch_indices, patch_indices_keep]
            freqs_cos = rearrange(freqs_cos, 'n i m j -> n m i j')
            freqs_sin = freqs_sin[batch_indices, patch_indices_keep]
            freqs_sin = rearrange(freqs_sin, 'n i m j -> n m i j')

            return  t * freqs_cos + rotate_half(t) * freqs_sin

        return  t * self.freqs_cos + rotate_half(t) * self.freqs_sin