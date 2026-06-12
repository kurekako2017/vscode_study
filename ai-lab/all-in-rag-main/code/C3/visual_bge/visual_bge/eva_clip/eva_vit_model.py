# --------------------------------------------------------
# Adapted from  https://github.com/microsoft/unilm/tree/master/beit
# --------------------------------------------------------
"""
文件功能概述：`code/C3/visual_bge/visual_bge/eva_clip/eva_vit_model.py` 主要是 evavitmodel，这个文件里有 8 个类、0 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 类 `DropPath`：功能概述：这个类是 `DropPath`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 drop_prob，再调用 __init__、super 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 2. `forward`：先接收输入参数 x，再调用 drop_path 等内部步骤完成主要工作，最后返回结果。 3. `extra_repr`：先进入当前步骤，再调用 format 等内部步骤完成主要工作，最后返回结果。
2. 类 `Mlp`：功能概述：这个类是 `Mlp`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 in_features, hidden_features, out_features, act_layer, norm_layer, drop, subln，再调用 __init__、nn.Linear、act_layer 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 2. `forward`：先接收输入参数 x，再调用 self.fc1、self.act、self.ffn_ln 等内部步骤完成主要工作，最后返回结果。
3. 类 `SwiGLU`：功能概述：这个类是 `SwiGLU`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 in_features, hidden_features, out_features, act_layer, drop, norm_layer, subln，再调用 __init__、nn.Linear、act_layer 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 2. `forward`：先接收输入参数 x，再调用 self.w1、self.w2、self.ffn_ln 等内部步骤完成主要工作，最后返回结果。
4. 类 `Attention`：功能概述：这个类是 `Attention`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 dim, num_heads, qkv_bias, qk_scale, attn_drop, proj_drop, window_size, attn_head_dim, xattn, rope, subln, norm_layer，接着根据条件分支选择不同处理路径，再调用 __init__、nn.Dropout、nn.Linear 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 2. `forward`：先接收输入参数 x, rel_pos_bias, attn_mask，接着根据条件分支选择不同处理路径，再调用 F.linear、permute、self.rope 等内部步骤完成主要工作，最后返回结果。
5. 类 `Block`：功能概述：这个类是 `Block`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 dim, num_heads, mlp_ratio, qkv_bias, qk_scale, drop, attn_drop, drop_path, init_values, act_layer, norm_layer, window_size, attn_head_dim, xattn, rope, postnorm, subln, naiveswiglu，接着根据条件分支选择不同处理路径，再调用 __init__、norm_layer、Attention 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 2. `forward`：先接收输入参数 x, rel_pos_bias, attn_mask，接着根据条件分支选择不同处理路径，再调用 self.drop_path、self.norm1、self.norm2 等内部步骤完成主要工作，最后返回结果。
6. 类 `PatchEmbed`：功能概述：这个类是 `PatchEmbed`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 img_size, patch_size, in_chans, embed_dim，再调用 __init__、to_2tuple、nn.Conv2d 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 2. `forward`：先接收输入参数 x, **kwargs，再调用 transpose、flatten、self.proj 等内部步骤完成主要工作，最后返回结果。
7. 类 `RelativePositionBias`：功能概述：这个类是 `RelativePositionBias`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 window_size, num_heads，再调用 __init__、nn.Parameter、torch.arange 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 2. `forward`：先进入当前步骤，再调用 view、contiguous、relative_position_bias.permute 等内部步骤完成主要工作，最后返回结果。
8. 类 `EVAVisionTransformer`：功能概述：这个类是 `EVAVisionTransformer`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 img_size, patch_size, in_chans, num_classes, embed_dim, depth, num_heads, mlp_ratio, qkv_bias, qk_scale, drop_rate, attn_drop_rate, drop_path_rate, norm_layer, init_values, patch_dropout, use_abs_pos_emb, use_rel_pos_bias, use_shared_rel_pos_bias, rope, use_mean_pooling, init_scale, grad_checkpointing, xattn, postnorm, pt_hw_seq_len, intp_freq, naiveswiglu, subln，接着根据条件分支选择不同处理路径，再调用 __init__、PatchEmbed、nn.Parameter 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 2. `fix_init_weight`：先进入当前步骤，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 enumerate、param.div_、rescale 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 3. `get_cast_dtype`：先进入当前步骤，最后返回结果。 4. `_init_weights`：先接收输入参数 m，接着根据条件分支选择不同处理路径，再调用 isinstance、trunc_normal_、nn.init.constant_ 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 5. `get_num_layers`：先进入当前步骤，再调用 len 等内部步骤完成主要工作，最后返回结果。 6. `lock`：先接收输入参数 unlocked_groups, freeze_bn_stats，然后循环处理每一条数据，再调用 self.parameters 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 7. `set_grad_checkpointing`：先接收输入参数 enable，最后把结果交给下一步或直接结束。 8. `no_weight_decay`：先进入当前步骤，最后返回结果。 9. `get_classifier`：先进入当前步骤，最后返回结果。 10. `reset_classifier`：先接收输入参数 num_classes, global_pool，再调用 nn.Linear、nn.Identity 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 11. `forward_features`：先接收输入参数 x, return_all_features，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 self.patch_embed、x.size、self.cls_token.expand 等内部步骤完成主要工作，最后返回结果。 12. `forward`：先接收输入参数 x, return_all_features，接着根据条件分支选择不同处理路径，再调用 self.forward_features、self.head 等内部步骤完成主要工作，最后返回结果。
"""

import math
import os
from functools import partial
import torch
import torch.nn as nn
import torch.nn.functional as F
try:
    from timm.models.layers import drop_path, to_2tuple, trunc_normal_
except:
    from timm.layers import drop_path, to_2tuple, trunc_normal_
    
from .transformer import PatchDropout
from .rope import VisionRotaryEmbedding, VisionRotaryEmbeddingFast

if os.getenv('ENV_TYPE') == 'deepspeed':
    try:
        from deepspeed.runtime.activation_checkpointing.checkpointing import checkpoint
    except:
        from torch.utils.checkpoint import checkpoint
else:
    from torch.utils.checkpoint import checkpoint

try:
    import xformers.ops as xops
except ImportError:
    xops = None
    # print("Please 'pip install xformers'")


class DropPath(nn.Module):
    """
    功能概述：这个类是 `DropPath`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 drop_prob，再调用 __init__、super 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    2. `forward`：先接收输入参数 x，再调用 drop_path 等内部步骤完成主要工作，最后返回结果。
    3. `extra_repr`：先进入当前步骤，再调用 format 等内部步骤完成主要工作，最后返回结果。
    """
    def __init__(self, drop_prob=None):  # 中文名称：初始化
        super(DropPath, self).__init__()
        self.drop_prob = drop_prob

    def forward(self, x):  # 中文名称：forward
        return drop_path(x, self.drop_prob, self.training)
    
    def extra_repr(self) -> str:  # 中文名称：extrarepr
        return 'p={}'.format(self.drop_prob)


class Mlp(nn.Module):
    """
    功能概述：这个类是 `Mlp`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 in_features, hidden_features, out_features, act_layer, norm_layer, drop, subln，再调用 __init__、nn.Linear、act_layer 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    2. `forward`：先接收输入参数 x，再调用 self.fc1、self.act、self.ffn_ln 等内部步骤完成主要工作，最后返回结果。
    """
    def __init__(
        self, 
        in_features, 
        hidden_features=None, 
        out_features=None, 
        act_layer=nn.GELU, 
        norm_layer=nn.LayerNorm, 
        drop=0.,
        subln=False,

        ):  # 中文名称：初始化
        super().__init__()
        out_features = out_features or in_features
        hidden_features = hidden_features or in_features
        self.fc1 = nn.Linear(in_features, hidden_features)
        self.act = act_layer()

        self.ffn_ln = norm_layer(hidden_features) if subln else nn.Identity()

        self.fc2 = nn.Linear(hidden_features, out_features)
        self.drop = nn.Dropout(drop)

    def forward(self, x):  # 中文名称：forward
        x = self.fc1(x)
        x = self.act(x)
        # x = self.drop(x)
        # commit this for the orignal BERT implement 
        x = self.ffn_ln(x)

        x = self.fc2(x)
        x = self.drop(x)
        return x

class SwiGLU(nn.Module):
    """
    功能概述：这个类是 `SwiGLU`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 in_features, hidden_features, out_features, act_layer, drop, norm_layer, subln，再调用 __init__、nn.Linear、act_layer 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    2. `forward`：先接收输入参数 x，再调用 self.w1、self.w2、self.ffn_ln 等内部步骤完成主要工作，最后返回结果。
    """
    def __init__(self, in_features, hidden_features=None, out_features=None, act_layer=nn.SiLU, drop=0., 
                norm_layer=nn.LayerNorm, subln=False):  # 中文名称：初始化
        super().__init__()
        out_features = out_features or in_features
        hidden_features = hidden_features or in_features

        self.w1 = nn.Linear(in_features, hidden_features)
        self.w2 = nn.Linear(in_features, hidden_features)

        self.act = act_layer()
        self.ffn_ln = norm_layer(hidden_features) if subln else nn.Identity()
        self.w3 = nn.Linear(hidden_features, out_features)
        
        self.drop = nn.Dropout(drop)

    def forward(self, x):  # 中文名称：forward
        x1 = self.w1(x)
        x2 = self.w2(x)
        hidden = self.act(x1) * x2
        x = self.ffn_ln(hidden)
        x = self.w3(x)
        x = self.drop(x)
        return x

class Attention(nn.Module):
    """
    功能概述：这个类是 `Attention`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 dim, num_heads, qkv_bias, qk_scale, attn_drop, proj_drop, window_size, attn_head_dim, xattn, rope, subln, norm_layer，接着根据条件分支选择不同处理路径，再调用 __init__、nn.Dropout、nn.Linear 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    2. `forward`：先接收输入参数 x, rel_pos_bias, attn_mask，接着根据条件分支选择不同处理路径，再调用 F.linear、permute、self.rope 等内部步骤完成主要工作，最后返回结果。
    """
    def __init__(
            self, dim, num_heads=8, qkv_bias=False, qk_scale=None, attn_drop=0.,
            proj_drop=0., window_size=None, attn_head_dim=None, xattn=False, rope=None, subln=False, norm_layer=nn.LayerNorm):  # 中文名称：初始化
        super().__init__()
        self.num_heads = num_heads
        head_dim = dim // num_heads
        if attn_head_dim is not None:
            head_dim = attn_head_dim
        all_head_dim = head_dim * self.num_heads
        self.scale = qk_scale or head_dim ** -0.5

        self.subln = subln
        if self.subln:
            self.q_proj = nn.Linear(dim, all_head_dim, bias=False)
            self.k_proj = nn.Linear(dim, all_head_dim, bias=False)
            self.v_proj = nn.Linear(dim, all_head_dim, bias=False)
        else:
            self.qkv = nn.Linear(dim, all_head_dim * 3, bias=False)

        if qkv_bias:
            self.q_bias = nn.Parameter(torch.zeros(all_head_dim))
            self.v_bias = nn.Parameter(torch.zeros(all_head_dim))
        else:
            self.q_bias = None
            self.v_bias = None

        if window_size:
            self.window_size = window_size
            self.num_relative_distance = (2 * window_size[0] - 1) * (2 * window_size[1] - 1) + 3
            self.relative_position_bias_table = nn.Parameter(
                torch.zeros(self.num_relative_distance, num_heads))  # 2*Wh-1 * 2*Ww-1, nH
            # cls to token & token 2 cls & cls to cls

            # get pair-wise relative position index for each token inside the window
            coords_h = torch.arange(window_size[0])
            coords_w = torch.arange(window_size[1])
            coords = torch.stack(torch.meshgrid([coords_h, coords_w]))  # 2, Wh, Ww
            coords_flatten = torch.flatten(coords, 1)  # 2, Wh*Ww
            relative_coords = coords_flatten[:, :, None] - coords_flatten[:, None, :]  # 2, Wh*Ww, Wh*Ww
            relative_coords = relative_coords.permute(1, 2, 0).contiguous()  # Wh*Ww, Wh*Ww, 2
            relative_coords[:, :, 0] += window_size[0] - 1  # shift to start from 0
            relative_coords[:, :, 1] += window_size[1] - 1
            relative_coords[:, :, 0] *= 2 * window_size[1] - 1
            relative_position_index = \
                torch.zeros(size=(window_size[0] * window_size[1] + 1, ) * 2, dtype=relative_coords.dtype)
            relative_position_index[1:, 1:] = relative_coords.sum(-1)  # Wh*Ww, Wh*Ww
            relative_position_index[0, 0:] = self.num_relative_distance - 3
            relative_position_index[0:, 0] = self.num_relative_distance - 2
            relative_position_index[0, 0] = self.num_relative_distance - 1

            self.register_buffer("relative_position_index", relative_position_index)
        else:
            self.window_size = None
            self.relative_position_bias_table = None
            self.relative_position_index = None

        self.attn_drop = nn.Dropout(attn_drop)
        self.inner_attn_ln = norm_layer(all_head_dim) if subln else nn.Identity()
        # self.proj = nn.Linear(all_head_dim, all_head_dim)
        self.proj = nn.Linear(all_head_dim, dim)
        self.proj_drop = nn.Dropout(proj_drop)
        self.xattn = xattn
        self.xattn_drop = attn_drop

        self.rope = rope

    def forward(self, x, rel_pos_bias=None, attn_mask=None):  # 中文名称：forward
        B, N, C = x.shape
        if self.subln: 
            q = F.linear(input=x, weight=self.q_proj.weight, bias=self.q_bias)
            k = F.linear(input=x, weight=self.k_proj.weight, bias=None)
            v = F.linear(input=x, weight=self.v_proj.weight, bias=self.v_bias)

            q = q.reshape(B, N, self.num_heads, -1).permute(0, 2, 1, 3)     # B, num_heads, N, C
            k = k.reshape(B, N, self.num_heads, -1).permute(0, 2, 1, 3)  
            v = v.reshape(B, N, self.num_heads, -1).permute(0, 2, 1, 3) 
        else: 

            qkv_bias = None
            if self.q_bias is not None:
                qkv_bias = torch.cat((self.q_bias, torch.zeros_like(self.v_bias, requires_grad=False), self.v_bias))
            
            qkv = F.linear(input=x, weight=self.qkv.weight, bias=qkv_bias)
            qkv = qkv.reshape(B, N, 3, self.num_heads, -1).permute(2, 0, 3, 1, 4)   # 3, B, num_heads, N, C
            q, k, v = qkv[0], qkv[1], qkv[2]

        if self.rope:
            # slightly fast impl
            q_t = q[:, :, 1:, :]
            ro_q_t = self.rope(q_t)
            q = torch.cat((q[:, :, :1, :], ro_q_t), -2).type_as(v)

            k_t = k[:, :, 1:, :]
            ro_k_t = self.rope(k_t)
            k = torch.cat((k[:, :, :1, :], ro_k_t), -2).type_as(v)

        if xops is not None:
            q = q.permute(0, 2, 1, 3)   # B, num_heads, N, C -> B, N, num_heads, C
            k = k.permute(0, 2, 1, 3)
            v = v.permute(0, 2, 1, 3)

            x = xops.memory_efficient_attention(
                q, k, v,
                p=self.xattn_drop,
                scale=self.scale,
                )
            x = x.reshape(B, N, -1)
            x = self.inner_attn_ln(x)
            x = self.proj(x)
            x = self.proj_drop(x)
        else:
            q = q * self.scale
            attn = (q @ k.transpose(-2, -1))

            if self.relative_position_bias_table is not None:
                relative_position_bias = \
                    self.relative_position_bias_table[self.relative_position_index.view(-1)].view(
                        self.window_size[0] * self.window_size[1] + 1,
                        self.window_size[0] * self.window_size[1] + 1, -1)  # Wh*Ww,Wh*Ww,nH
                relative_position_bias = relative_position_bias.permute(2, 0, 1).contiguous()  # nH, Wh*Ww, Wh*Ww
                attn = attn + relative_position_bias.unsqueeze(0).type_as(attn)

            if rel_pos_bias is not None:
                attn = attn + rel_pos_bias.type_as(attn)

            if attn_mask is not None:
                attn_mask = attn_mask.bool()
                attn = attn.masked_fill(~attn_mask[:, None, None, :], float("-inf"))
            
            attn = attn.softmax(dim=-1)
            attn = self.attn_drop(attn)

            x = (attn @ v).transpose(1, 2).reshape(B, N, -1)
            x = self.inner_attn_ln(x)
            x = self.proj(x)
            x = self.proj_drop(x)
        return x


class Block(nn.Module):
    """
    功能概述：这个类是 `Block`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 dim, num_heads, mlp_ratio, qkv_bias, qk_scale, drop, attn_drop, drop_path, init_values, act_layer, norm_layer, window_size, attn_head_dim, xattn, rope, postnorm, subln, naiveswiglu，接着根据条件分支选择不同处理路径，再调用 __init__、norm_layer、Attention 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    2. `forward`：先接收输入参数 x, rel_pos_bias, attn_mask，接着根据条件分支选择不同处理路径，再调用 self.drop_path、self.norm1、self.norm2 等内部步骤完成主要工作，最后返回结果。
    """

    def __init__(self, dim, num_heads, mlp_ratio=4., qkv_bias=False, qk_scale=None, drop=0., attn_drop=0.,
                 drop_path=0., init_values=None, act_layer=nn.GELU, norm_layer=nn.LayerNorm,
                 window_size=None, attn_head_dim=None, xattn=False, rope=None, postnorm=False,
                 subln=False, naiveswiglu=False):  # 中文名称：初始化
        super().__init__()
        self.norm1 = norm_layer(dim)
        self.attn = Attention(
            dim, num_heads=num_heads, qkv_bias=qkv_bias, qk_scale=qk_scale,
            attn_drop=attn_drop, proj_drop=drop, window_size=window_size, attn_head_dim=attn_head_dim,
            xattn=xattn, rope=rope, subln=subln, norm_layer=norm_layer)
        # NOTE: drop path for stochastic depth, we shall see if this is better than dropout here
        self.drop_path = DropPath(drop_path) if drop_path > 0. else nn.Identity()
        self.norm2 = norm_layer(dim)
        mlp_hidden_dim = int(dim * mlp_ratio)

        if naiveswiglu:
            self.mlp = SwiGLU(
                in_features=dim, 
                hidden_features=mlp_hidden_dim, 
                subln=subln,
                norm_layer=norm_layer,
            )
        else:
            self.mlp = Mlp(
                in_features=dim, 
                hidden_features=mlp_hidden_dim, 
                act_layer=act_layer,
                subln=subln,
                drop=drop
            )

        if init_values is not None and init_values > 0:
            self.gamma_1 = nn.Parameter(init_values * torch.ones((dim)),requires_grad=True)
            self.gamma_2 = nn.Parameter(init_values * torch.ones((dim)),requires_grad=True)
        else:
            self.gamma_1, self.gamma_2 = None, None

        self.postnorm = postnorm

    def forward(self, x, rel_pos_bias=None, attn_mask=None):  # 中文名称：forward
        if self.gamma_1 is None:
            if self.postnorm:
                x = x + self.drop_path(self.norm1(self.attn(x, rel_pos_bias=rel_pos_bias, attn_mask=attn_mask)))
                x = x + self.drop_path(self.norm2(self.mlp(x)))
            else:
                x = x + self.drop_path(self.attn(self.norm1(x), rel_pos_bias=rel_pos_bias, attn_mask=attn_mask))
                x = x + self.drop_path(self.mlp(self.norm2(x)))
        else:
            if self.postnorm:
                x = x + self.drop_path(self.gamma_1 * self.norm1(self.attn(x, rel_pos_bias=rel_pos_bias, attn_mask=attn_mask)))
                x = x + self.drop_path(self.gamma_2 * self.norm2(self.mlp(x)))
            else:
                x = x + self.drop_path(self.gamma_1 * self.attn(self.norm1(x), rel_pos_bias=rel_pos_bias, attn_mask=attn_mask))
                x = x + self.drop_path(self.gamma_2 * self.mlp(self.norm2(x)))
        return x


class PatchEmbed(nn.Module):
    """
    功能概述：这个类是 `PatchEmbed`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 img_size, patch_size, in_chans, embed_dim，再调用 __init__、to_2tuple、nn.Conv2d 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    2. `forward`：先接收输入参数 x, **kwargs，再调用 transpose、flatten、self.proj 等内部步骤完成主要工作，最后返回结果。
    """
    def __init__(self, img_size=224, patch_size=16, in_chans=3, embed_dim=768):  # 中文名称：初始化
        super().__init__()
        img_size = to_2tuple(img_size)
        patch_size = to_2tuple(patch_size)
        num_patches = (img_size[1] // patch_size[1]) * (img_size[0] // patch_size[0])
        self.patch_shape = (img_size[0] // patch_size[0], img_size[1] // patch_size[1])
        self.img_size = img_size
        self.patch_size = patch_size
        self.num_patches = num_patches

        self.proj = nn.Conv2d(in_chans, embed_dim, kernel_size=patch_size, stride=patch_size)

    def forward(self, x, **kwargs):  # 中文名称：forward
        B, C, H, W = x.shape
        # FIXME look at relaxing size constraints
        assert H == self.img_size[0] and W == self.img_size[1], \
            f"Input image size ({H}*{W}) doesn't match model ({self.img_size[0]}*{self.img_size[1]})."
        x = self.proj(x).flatten(2).transpose(1, 2) # [10, 3, 224, 224] -> [10, 196, 768]
        return x


class RelativePositionBias(nn.Module):
    """
    功能概述：这个类是 `RelativePositionBias`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 window_size, num_heads，再调用 __init__、nn.Parameter、torch.arange 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    2. `forward`：先进入当前步骤，再调用 view、contiguous、relative_position_bias.permute 等内部步骤完成主要工作，最后返回结果。
    """

    def __init__(self, window_size, num_heads):  # 中文名称：初始化
        super().__init__()
        self.window_size = window_size
        self.num_relative_distance = (2 * window_size[0] - 1) * (2 * window_size[1] - 1) + 3
        self.relative_position_bias_table = nn.Parameter(
            torch.zeros(self.num_relative_distance, num_heads))  # 2*Wh-1 * 2*Ww-1, nH
        # cls to token & token 2 cls & cls to cls

        # get pair-wise relative position index for each token inside the window
        coords_h = torch.arange(window_size[0])
        coords_w = torch.arange(window_size[1])
        coords = torch.stack(torch.meshgrid([coords_h, coords_w]))  # 2, Wh, Ww
        coords_flatten = torch.flatten(coords, 1)  # 2, Wh*Ww
        relative_coords = coords_flatten[:, :, None] - coords_flatten[:, None, :]  # 2, Wh*Ww, Wh*Ww
        relative_coords = relative_coords.permute(1, 2, 0).contiguous()  # Wh*Ww, Wh*Ww, 2
        relative_coords[:, :, 0] += window_size[0] - 1  # shift to start from 0
        relative_coords[:, :, 1] += window_size[1] - 1
        relative_coords[:, :, 0] *= 2 * window_size[1] - 1
        relative_position_index = \
            torch.zeros(size=(window_size[0] * window_size[1] + 1,) * 2, dtype=relative_coords.dtype)
        relative_position_index[1:, 1:] = relative_coords.sum(-1)  # Wh*Ww, Wh*Ww
        relative_position_index[0, 0:] = self.num_relative_distance - 3
        relative_position_index[0:, 0] = self.num_relative_distance - 2
        relative_position_index[0, 0] = self.num_relative_distance - 1

        self.register_buffer("relative_position_index", relative_position_index)

    def forward(self):  # 中文名称：forward
        relative_position_bias = \
            self.relative_position_bias_table[self.relative_position_index.view(-1)].view(
                self.window_size[0] * self.window_size[1] + 1,
                self.window_size[0] * self.window_size[1] + 1, -1)  # Wh*Ww,Wh*Ww,nH
        return relative_position_bias.permute(2, 0, 1).contiguous()  # nH, Wh*Ww, Wh*Ww


class EVAVisionTransformer(nn.Module):
    """
    功能概述：这个类是 `EVAVisionTransformer`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 img_size, patch_size, in_chans, num_classes, embed_dim, depth, num_heads, mlp_ratio, qkv_bias, qk_scale, drop_rate, attn_drop_rate, drop_path_rate, norm_layer, init_values, patch_dropout, use_abs_pos_emb, use_rel_pos_bias, use_shared_rel_pos_bias, rope, use_mean_pooling, init_scale, grad_checkpointing, xattn, postnorm, pt_hw_seq_len, intp_freq, naiveswiglu, subln，接着根据条件分支选择不同处理路径，再调用 __init__、PatchEmbed、nn.Parameter 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    2. `fix_init_weight`：先进入当前步骤，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 enumerate、param.div_、rescale 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    3. `get_cast_dtype`：先进入当前步骤，最后返回结果。
    4. `_init_weights`：先接收输入参数 m，接着根据条件分支选择不同处理路径，再调用 isinstance、trunc_normal_、nn.init.constant_ 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    5. `get_num_layers`：先进入当前步骤，再调用 len 等内部步骤完成主要工作，最后返回结果。
    6. `lock`：先接收输入参数 unlocked_groups, freeze_bn_stats，然后循环处理每一条数据，再调用 self.parameters 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    7. `set_grad_checkpointing`：先接收输入参数 enable，最后把结果交给下一步或直接结束。
    8. `no_weight_decay`：先进入当前步骤，最后返回结果。
    9. `get_classifier`：先进入当前步骤，最后返回结果。
    10. `reset_classifier`：先接收输入参数 num_classes, global_pool，再调用 nn.Linear、nn.Identity 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    11. `forward_features`：先接收输入参数 x, return_all_features，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 self.patch_embed、x.size、self.cls_token.expand 等内部步骤完成主要工作，最后返回结果。
    12. `forward`：先接收输入参数 x, return_all_features，接着根据条件分支选择不同处理路径，再调用 self.forward_features、self.head 等内部步骤完成主要工作，最后返回结果。
    """
    def __init__(self, img_size=224, patch_size=16, in_chans=3, num_classes=1000, embed_dim=768, depth=12,
                 num_heads=12, mlp_ratio=4., qkv_bias=False, qk_scale=None, drop_rate=0., attn_drop_rate=0.,
                 drop_path_rate=0., norm_layer=nn.LayerNorm, init_values=None, patch_dropout=0.,
                 use_abs_pos_emb=True, use_rel_pos_bias=False, use_shared_rel_pos_bias=False, rope=False,
                 use_mean_pooling=True, init_scale=0.001, grad_checkpointing=False, xattn=False, postnorm=False,
                 pt_hw_seq_len=16, intp_freq=False, naiveswiglu=False, subln=False):  # 中文名称：初始化
        super().__init__()
        self.image_size = img_size
        self.num_classes = num_classes
        self.num_features = self.embed_dim = embed_dim  # num_features for consistency with other models

        self.patch_embed = PatchEmbed(
            img_size=img_size, patch_size=patch_size, in_chans=in_chans, embed_dim=embed_dim)
        num_patches = self.patch_embed.num_patches

        self.cls_token = nn.Parameter(torch.zeros(1, 1, embed_dim))
        # self.mask_token = nn.Parameter(torch.zeros(1, 1, embed_dim))
        if use_abs_pos_emb:
            self.pos_embed = nn.Parameter(torch.zeros(1, num_patches + 1, embed_dim))
        else:
            self.pos_embed = None
        self.pos_drop = nn.Dropout(p=drop_rate)

        if use_shared_rel_pos_bias:
            self.rel_pos_bias = RelativePositionBias(window_size=self.patch_embed.patch_shape, num_heads=num_heads)
        else:
            self.rel_pos_bias = None

        if rope:
            half_head_dim = embed_dim // num_heads // 2
            hw_seq_len = img_size // patch_size
            self.rope = VisionRotaryEmbeddingFast(
                dim=half_head_dim,
                pt_seq_len=pt_hw_seq_len,
                ft_seq_len=hw_seq_len if intp_freq else None,
                # patch_dropout=patch_dropout
            )
        else: 
            self.rope = None

        self.naiveswiglu = naiveswiglu

        dpr = [x.item() for x in torch.linspace(0, drop_path_rate, depth)]  # stochastic depth decay rule
        self.use_rel_pos_bias = use_rel_pos_bias
        self.blocks = nn.ModuleList([
            Block(
                dim=embed_dim, num_heads=num_heads, mlp_ratio=mlp_ratio, qkv_bias=qkv_bias, qk_scale=qk_scale,
                drop=drop_rate, attn_drop=attn_drop_rate, drop_path=dpr[i], norm_layer=norm_layer,
                init_values=init_values, window_size=self.patch_embed.patch_shape if use_rel_pos_bias else None,
                xattn=xattn, rope=self.rope, postnorm=postnorm, subln=subln, naiveswiglu=naiveswiglu)
            for i in range(depth)])
        self.norm = nn.Identity() if use_mean_pooling else norm_layer(embed_dim)
        self.fc_norm = norm_layer(embed_dim) if use_mean_pooling else None
        self.head = nn.Linear(embed_dim, num_classes) if num_classes > 0 else nn.Identity()

        if self.pos_embed is not None:
            trunc_normal_(self.pos_embed, std=.02)

        trunc_normal_(self.cls_token, std=.02)
        # trunc_normal_(self.mask_token, std=.02)

        self.apply(self._init_weights)
        self.fix_init_weight()

        if isinstance(self.head, nn.Linear):
            trunc_normal_(self.head.weight, std=.02)
            self.head.weight.data.mul_(init_scale)
            self.head.bias.data.mul_(init_scale)

        # setting a patch_dropout of 0. would mean it is disabled and this function would be the identity fn
        self.patch_dropout = PatchDropout(patch_dropout) if patch_dropout > 0. else nn.Identity()

        self.grad_checkpointing = grad_checkpointing

    def fix_init_weight(self):  # 中文名称：fix初始化weight
        def rescale(param, layer_id):  # 中文名称：rescale
            param.div_(math.sqrt(2.0 * layer_id))

        for layer_id, layer in enumerate(self.blocks):
            rescale(layer.attn.proj.weight.data, layer_id + 1)
            if self.naiveswiglu:
                rescale(layer.mlp.w3.weight.data, layer_id + 1)
            else:
                rescale(layer.mlp.fc2.weight.data, layer_id + 1)

    def get_cast_dtype(self) -> torch.dtype:  # 中文名称：获取castdtype
        return self.blocks[0].mlp.fc2.weight.dtype

    def _init_weights(self, m):  # 中文名称：初始化weights
        if isinstance(m, nn.Linear):
            trunc_normal_(m.weight, std=.02)
            if m.bias is not None:
                nn.init.constant_(m.bias, 0)
        elif isinstance(m, nn.LayerNorm):
            nn.init.constant_(m.bias, 0)
            nn.init.constant_(m.weight, 1.0)

    def get_num_layers(self):  # 中文名称：获取numlayers
        return len(self.blocks)
    
    def lock(self, unlocked_groups=0, freeze_bn_stats=False):  # 中文名称：lock
        assert unlocked_groups == 0, 'partial locking not currently supported for this model'
        for param in self.parameters():
            param.requires_grad = False

    @torch.jit.ignore
    def set_grad_checkpointing(self, enable=True):  # 中文名称：设置gradcheckpointing
        self.grad_checkpointing = enable

    @torch.jit.ignore
    def no_weight_decay(self):  # 中文名称：noweightdecay
        return {'pos_embed', 'cls_token'}

    def get_classifier(self):  # 中文名称：获取classifier
        return self.head

    def reset_classifier(self, num_classes, global_pool=''):  # 中文名称：resetclassifier
        self.num_classes = num_classes
        self.head = nn.Linear(self.embed_dim, num_classes) if num_classes > 0 else nn.Identity()

    def forward_features(self, x, return_all_features=False):
          # 中文名称：forwardfeatures
        x = self.patch_embed(x)
        batch_size, seq_len, _ = x.size()

        cls_tokens = self.cls_token.expand(batch_size, -1, -1)  # stole cls_tokens impl from Phil Wang, thanks
        x = torch.cat((cls_tokens, x), dim=1)
        if self.pos_embed is not None:
            x = x + self.pos_embed
        x = self.pos_drop(x)

        # a patch_dropout of 0. would mean it is disabled and this function would do nothing but return what was passed in
        if os.getenv('RoPE') == '1':
            if self.training and not isinstance(self.patch_dropout, nn.Identity):
                x, patch_indices_keep = self.patch_dropout(x)
                self.rope.forward = partial(self.rope.forward, patch_indices_keep=patch_indices_keep)
            else:
                self.rope.forward = partial(self.rope.forward, patch_indices_keep=None)
                x = self.patch_dropout(x)
        else:
            x = self.patch_dropout(x)

        rel_pos_bias = self.rel_pos_bias() if self.rel_pos_bias is not None else None
        for blk in self.blocks:
            if self.grad_checkpointing:
                # x = checkpoint(blk, x, (rel_pos_bias,))
                x = checkpoint(blk, x, rel_pos_bias)
            else:
                x = blk(x, rel_pos_bias=rel_pos_bias)

        if not return_all_features:
            x = self.norm(x)
            if self.fc_norm is not None:
                return self.fc_norm(x.mean(1))
            else:
                return x[:, 0]
        return x

    def forward(self, x, return_all_features=True):  # 中文名称：forward
        if return_all_features:
            return self.forward_features(x, return_all_features)
        x = self.forward_features(x)
        x = self.head(x)
        return x
