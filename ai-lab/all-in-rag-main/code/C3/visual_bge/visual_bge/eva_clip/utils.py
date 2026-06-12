"""
文件功能概述：`code/C3/visual_bge/visual_bge/eva_clip/utils.py` 主要是 工具，这个文件里有 1 个类、8 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 函数 `resize_clip_pos_embed`：先接收输入参数 state_dict, model, interpolation, seq_dim，接着根据条件分支选择不同处理路径，再调用 state_dict.get、to_2tuple、logging.info 等内部步骤完成主要工作，最后返回结果。
2. 函数 `resize_visual_pos_embed`：先接收输入参数 state_dict, model, interpolation, seq_dim，接着根据条件分支选择不同处理路径，再调用 state_dict.get、to_2tuple、logging.info 等内部步骤完成主要工作，最后返回结果。
3. 函数 `resize_evaclip_pos_embed`：先接收输入参数 state_dict, model, interpolation, seq_dim，接着根据条件分支选择不同处理路径，再调用 list、state_dict.keys、int 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
4. 函数 `resize_eva_pos_embed`：先接收输入参数 state_dict, model, interpolation, seq_dim，接着根据条件分支选择不同处理路径，再调用 list、state_dict.keys、int 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
5. 函数 `resize_rel_pos_embed`：先接收输入参数 state_dict, model, interpolation, seq_dim，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 list、state_dict.keys、int 等内部步骤完成主要工作，最后返回结果。
6. 函数 `freeze_batch_norm_2d`：先接收输入参数 module, module_match, name，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 isinstance、FrozenBatchNorm2d、module.named_children 等内部步骤完成主要工作，最后返回结果。
7. 函数 `_ntuple`：先接收输入参数 n，接着根据条件分支选择不同处理路径，再调用 isinstance、tuple、repeat 等内部步骤完成主要工作，最后返回结果。
8. 函数 `is_logging`：先接收输入参数 args，再调用 is_local_master、is_global_master 等内部步骤完成主要工作，最后返回结果。
9. 类 `AllGather`：功能概述：这个类是 `AllGather`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `forward`：先接收输入参数 ctx, tensor, rank, world_size，再调用 torch.distributed.all_gather、torch.cat、torch.empty_like 等内部步骤完成主要工作，最后返回结果。 2. `backward`：先接收输入参数 ctx, grad_output，最后返回结果。
"""

from itertools import repeat
import collections.abc
import logging
import math
import numpy as np

import torch
from torch import nn as nn
from torchvision.ops.misc import FrozenBatchNorm2d
import torch.nn.functional as F

# open CLIP
def resize_clip_pos_embed(state_dict, model, interpolation: str = 'bicubic', seq_dim=1):
    # Rescale the grid of position embeddings when loading from state_dict  # 中文名称：resizeclipposembed
    old_pos_embed = state_dict.get('visual.positional_embedding', None)
    if old_pos_embed is None or not hasattr(model.visual, 'grid_size'):
        return
    grid_size = to_2tuple(model.visual.grid_size)
    extra_tokens = 1  # FIXME detect different token configs (ie no class token, or more)
    new_seq_len = grid_size[0] * grid_size[1] + extra_tokens
    if new_seq_len == old_pos_embed.shape[0]:
        return

    if extra_tokens:
        pos_emb_tok, pos_emb_img = old_pos_embed[:extra_tokens], old_pos_embed[extra_tokens:]
    else:
        pos_emb_tok, pos_emb_img = None, old_pos_embed
    old_grid_size = to_2tuple(int(math.sqrt(len(pos_emb_img))))

    logging.info('Resizing position embedding grid-size from %s to %s', old_grid_size, grid_size)
    pos_emb_img = pos_emb_img.reshape(1, old_grid_size[0], old_grid_size[1], -1).permute(0, 3, 1, 2)
    pos_emb_img = F.interpolate(
        pos_emb_img,
        size=grid_size,
        mode=interpolation,
        align_corners=True,
    )
    pos_emb_img = pos_emb_img.permute(0, 2, 3, 1).reshape(1, grid_size[0] * grid_size[1], -1)[0]
    if pos_emb_tok is not None:
        new_pos_embed = torch.cat([pos_emb_tok, pos_emb_img], dim=0)
    else:
        new_pos_embed = pos_emb_img
    state_dict['visual.positional_embedding'] = new_pos_embed


def resize_visual_pos_embed(state_dict, model, interpolation: str = 'bicubic', seq_dim=1):
    # Rescale the grid of position embeddings when loading from state_dict  # 中文名称：resizevisualposembed
    old_pos_embed = state_dict.get('positional_embedding', None)
    if old_pos_embed is None or not hasattr(model.visual, 'grid_size'):
        return
    grid_size = to_2tuple(model.visual.grid_size)
    extra_tokens = 1  # FIXME detect different token configs (ie no class token, or more)
    new_seq_len = grid_size[0] * grid_size[1] + extra_tokens
    if new_seq_len == old_pos_embed.shape[0]:
        return

    if extra_tokens:
        pos_emb_tok, pos_emb_img = old_pos_embed[:extra_tokens], old_pos_embed[extra_tokens:]
    else:
        pos_emb_tok, pos_emb_img = None, old_pos_embed
    old_grid_size = to_2tuple(int(math.sqrt(len(pos_emb_img))))

    logging.info('Resizing position embedding grid-size from %s to %s', old_grid_size, grid_size)
    pos_emb_img = pos_emb_img.reshape(1, old_grid_size[0], old_grid_size[1], -1).permute(0, 3, 1, 2)
    pos_emb_img = F.interpolate(
        pos_emb_img,
        size=grid_size,
        mode=interpolation,
        align_corners=True,
    )
    pos_emb_img = pos_emb_img.permute(0, 2, 3, 1).reshape(1, grid_size[0] * grid_size[1], -1)[0]
    if pos_emb_tok is not None:
        new_pos_embed = torch.cat([pos_emb_tok, pos_emb_img], dim=0)
    else:
        new_pos_embed = pos_emb_img
    state_dict['positional_embedding'] = new_pos_embed

def resize_evaclip_pos_embed(state_dict, model, interpolation: str = 'bicubic', seq_dim=1):  # 中文名称：resizeevaclipposembed
    all_keys = list(state_dict.keys())
    # interpolate position embedding
    if 'visual.pos_embed' in state_dict:
        pos_embed_checkpoint = state_dict['visual.pos_embed']
        embedding_size = pos_embed_checkpoint.shape[-1]
        num_patches = model.visual.patch_embed.num_patches
        num_extra_tokens = model.visual.pos_embed.shape[-2] - num_patches
        # height (== width) for the checkpoint position embedding
        orig_size = int((pos_embed_checkpoint.shape[-2] - num_extra_tokens) ** 0.5)
        # height (== width) for the new position embedding
        new_size = int(num_patches ** 0.5)
        # class_token and dist_token are kept unchanged
        if orig_size != new_size:
            print("Position interpolate from %dx%d to %dx%d" % (orig_size, orig_size, new_size, new_size))
            extra_tokens = pos_embed_checkpoint[:, :num_extra_tokens]
            # only the position tokens are interpolated
            pos_tokens = pos_embed_checkpoint[:, num_extra_tokens:]
            pos_tokens = pos_tokens.reshape(-1, orig_size, orig_size, embedding_size).permute(0, 3, 1, 2)
            pos_tokens = torch.nn.functional.interpolate(
                pos_tokens, size=(new_size, new_size), mode='bicubic', align_corners=False)
            pos_tokens = pos_tokens.permute(0, 2, 3, 1).flatten(1, 2)
            new_pos_embed = torch.cat((extra_tokens, pos_tokens), dim=1)
            state_dict['visual.pos_embed'] = new_pos_embed

            patch_embed_proj = state_dict['visual.patch_embed.proj.weight']
            patch_size = model.visual.patch_embed.patch_size
            state_dict['visual.patch_embed.proj.weight'] = torch.nn.functional.interpolate(
                patch_embed_proj.float(), size=patch_size, mode='bicubic', align_corners=False)


def resize_eva_pos_embed(state_dict, model, interpolation: str = 'bicubic', seq_dim=1):  # 中文名称：resizeevaposembed
    all_keys = list(state_dict.keys())
    # interpolate position embedding
    if 'pos_embed' in state_dict:
        pos_embed_checkpoint = state_dict['pos_embed']
        embedding_size = pos_embed_checkpoint.shape[-1]
        num_patches = model.visual.patch_embed.num_patches
        num_extra_tokens = model.visual.pos_embed.shape[-2] - num_patches
        # height (== width) for the checkpoint position embedding
        orig_size = int((pos_embed_checkpoint.shape[-2] - num_extra_tokens) ** 0.5)
        # height (== width) for the new position embedding
        new_size = int(num_patches ** 0.5)
        # class_token and dist_token are kept unchanged
        if orig_size != new_size:
            print("Position interpolate from %dx%d to %dx%d" % (orig_size, orig_size, new_size, new_size))
            extra_tokens = pos_embed_checkpoint[:, :num_extra_tokens]
            # only the position tokens are interpolated
            pos_tokens = pos_embed_checkpoint[:, num_extra_tokens:]
            pos_tokens = pos_tokens.reshape(-1, orig_size, orig_size, embedding_size).permute(0, 3, 1, 2)
            pos_tokens = torch.nn.functional.interpolate(
                pos_tokens, size=(new_size, new_size), mode='bicubic', align_corners=False)
            pos_tokens = pos_tokens.permute(0, 2, 3, 1).flatten(1, 2)
            new_pos_embed = torch.cat((extra_tokens, pos_tokens), dim=1)
            state_dict['pos_embed'] = new_pos_embed

            patch_embed_proj = state_dict['patch_embed.proj.weight']
            patch_size = model.visual.patch_embed.patch_size
            state_dict['patch_embed.proj.weight'] = torch.nn.functional.interpolate(
                patch_embed_proj.float(), size=patch_size, mode='bicubic', align_corners=False)
                

def resize_rel_pos_embed(state_dict, model, interpolation: str = 'bicubic', seq_dim=1):  # 中文名称：resizerelposembed
    all_keys = list(state_dict.keys())
    for key in all_keys:
        if "relative_position_index" in key:
            state_dict.pop(key)

        if "relative_position_bias_table" in key:
            rel_pos_bias = state_dict[key]
            src_num_pos, num_attn_heads = rel_pos_bias.size()
            dst_num_pos, _ = model.visual.state_dict()[key].size()
            dst_patch_shape = model.visual.patch_embed.patch_shape
            if dst_patch_shape[0] != dst_patch_shape[1]:
                raise NotImplementedError()
            num_extra_tokens = dst_num_pos - (dst_patch_shape[0] * 2 - 1) * (dst_patch_shape[1] * 2 - 1)
            src_size = int((src_num_pos - num_extra_tokens) ** 0.5)
            dst_size = int((dst_num_pos - num_extra_tokens) ** 0.5)
            if src_size != dst_size:
                print("Position interpolate for %s from %dx%d to %dx%d" % (
                    key, src_size, src_size, dst_size, dst_size))
                extra_tokens = rel_pos_bias[-num_extra_tokens:, :]
                rel_pos_bias = rel_pos_bias[:-num_extra_tokens, :]

                def geometric_progression(a, r, n):  # 中文名称：geometricprogression
                    return a * (1.0 - r ** n) / (1.0 - r)

                left, right = 1.01, 1.5
                while right - left > 1e-6:
                    q = (left + right) / 2.0
                    gp = geometric_progression(1, q, src_size // 2)
                    if gp > dst_size // 2:
                        right = q
                    else:
                        left = q

                # if q > 1.090307:
                #     q = 1.090307

                dis = []
                cur = 1
                for i in range(src_size // 2):
                    dis.append(cur)
                    cur += q ** (i + 1)

                r_ids = [-_ for _ in reversed(dis)]

                x = r_ids + [0] + dis
                y = r_ids + [0] + dis

                t = dst_size // 2.0
                dx = np.arange(-t, t + 0.1, 1.0)
                dy = np.arange(-t, t + 0.1, 1.0)

                print("Original positions = %s" % str(x))
                print("Target positions = %s" % str(dx))

                all_rel_pos_bias = []

                for i in range(num_attn_heads):
                    z = rel_pos_bias[:, i].view(src_size, src_size).float().numpy()
                    f = F.interpolate.interp2d(x, y, z, kind='cubic')
                    all_rel_pos_bias.append(
                        torch.Tensor(f(dx, dy)).contiguous().view(-1, 1).to(rel_pos_bias.device))

                rel_pos_bias = torch.cat(all_rel_pos_bias, dim=-1)

                new_rel_pos_bias = torch.cat((rel_pos_bias, extra_tokens), dim=0)
                state_dict[key] = new_rel_pos_bias

    # interpolate position embedding
    if 'pos_embed' in state_dict:
        pos_embed_checkpoint = state_dict['pos_embed']
        embedding_size = pos_embed_checkpoint.shape[-1]
        num_patches = model.visual.patch_embed.num_patches
        num_extra_tokens = model.visual.pos_embed.shape[-2] - num_patches
        # height (== width) for the checkpoint position embedding
        orig_size = int((pos_embed_checkpoint.shape[-2] - num_extra_tokens) ** 0.5)
        # height (== width) for the new position embedding
        new_size = int(num_patches ** 0.5)
        # class_token and dist_token are kept unchanged
        if orig_size != new_size:
            print("Position interpolate from %dx%d to %dx%d" % (orig_size, orig_size, new_size, new_size))
            extra_tokens = pos_embed_checkpoint[:, :num_extra_tokens]
            # only the position tokens are interpolated
            pos_tokens = pos_embed_checkpoint[:, num_extra_tokens:]
            pos_tokens = pos_tokens.reshape(-1, orig_size, orig_size, embedding_size).permute(0, 3, 1, 2)
            pos_tokens = torch.nn.functional.interpolate(
                pos_tokens, size=(new_size, new_size), mode='bicubic', align_corners=False)
            pos_tokens = pos_tokens.permute(0, 2, 3, 1).flatten(1, 2)
            new_pos_embed = torch.cat((extra_tokens, pos_tokens), dim=1)
            state_dict['pos_embed'] = new_pos_embed

            patch_embed_proj = state_dict['patch_embed.proj.weight']
            patch_size = model.visual.patch_embed.patch_size
            state_dict['patch_embed.proj.weight'] = torch.nn.functional.interpolate(
                patch_embed_proj.float(), size=patch_size, mode='bicubic', align_corners=False)


def freeze_batch_norm_2d(module, module_match={}, name=''):  # 中文名称：freezebatchnorm2d
    """
    Converts all `BatchNorm2d` and `SyncBatchNorm` layers of provided module into `FrozenBatchNorm2d`. If `module` is
    itself an instance of either `BatchNorm2d` or `SyncBatchNorm`, it is converted into `FrozenBatchNorm2d` and
    returned. Otherwise, the module is walked recursively and submodules are converted in place.

    Args:
        module (torch.nn.Module): Any PyTorch module.
        module_match (dict): Dictionary of full module names to freeze (all if empty)
        name (str): Full module name (prefix)

    Returns:
        torch.nn.Module: Resulting module

    Inspired by https://github.com/pytorch/pytorch/blob/a5895f85be0f10212791145bfedc0261d364f103/torch/nn/modules/batchnorm.py#L762
    """
    res = module
    is_match = True
    if module_match:
        is_match = name in module_match
    if is_match and isinstance(module, (nn.modules.batchnorm.BatchNorm2d, nn.modules.batchnorm.SyncBatchNorm)):
        res = FrozenBatchNorm2d(module.num_features)
        res.num_features = module.num_features
        res.affine = module.affine
        if module.affine:
            res.weight.data = module.weight.data.clone().detach()
            res.bias.data = module.bias.data.clone().detach()
        res.running_mean.data = module.running_mean.data
        res.running_var.data = module.running_var.data
        res.eps = module.eps
    else:
        for child_name, child in module.named_children():
            full_child_name = '.'.join([name, child_name]) if name else child_name
            new_child = freeze_batch_norm_2d(child, module_match, full_child_name)
            if new_child is not child:
                res.add_module(child_name, new_child)
    return res


# From PyTorch internals
def _ntuple(n):  # 中文名称：ntuple
    def parse(x):  # 中文名称：解析
        if isinstance(x, collections.abc.Iterable):
            return x
        return tuple(repeat(x, n))
    return parse


to_1tuple = _ntuple(1)
to_2tuple = _ntuple(2)
to_3tuple = _ntuple(3)
to_4tuple = _ntuple(4)
to_ntuple = lambda n, x: _ntuple(n)(x)


def is_logging(args):  # 中文名称：是否logging
    def is_global_master(args):  # 中文名称：是否globalmaster
        return args.rank == 0

    def is_local_master(args):  # 中文名称：是否localmaster
        return args.local_rank == 0

    def is_master(args, local=False):  # 中文名称：是否master
        return is_local_master(args) if local else is_global_master(args)
    return is_master


class AllGather(torch.autograd.Function):
    """
    功能概述：这个类是 `AllGather`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `forward`：先接收输入参数 ctx, tensor, rank, world_size，再调用 torch.distributed.all_gather、torch.cat、torch.empty_like 等内部步骤完成主要工作，最后返回结果。
    2. `backward`：先接收输入参数 ctx, grad_output，最后返回结果。
    """

    @staticmethod
    def forward(ctx, tensor, rank, world_size):  # 中文名称：forward
        tensors_gather = [torch.empty_like(tensor) for _ in range(world_size)]
        torch.distributed.all_gather(tensors_gather, tensor)
        ctx.rank = rank
        ctx.batch_size = tensor.shape[0]
        return torch.cat(tensors_gather, 0)

    @staticmethod
    def backward(ctx, grad_output):  # 中文名称：backward
        return (
            grad_output[ctx.batch_size * ctx.rank: ctx.batch_size * (ctx.rank + 1)],
            None,
            None
        )

allgather = AllGather.apply