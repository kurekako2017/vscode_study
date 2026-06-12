"""
文件功能概述：`code/C3/visual_bge/visual_bge/eva_clip/factory.py` 主要是 factory，这个文件里有 0 个类、16 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 函数 `_natural_key`：先接收输入参数 string_，再调用 s.isdigit、int、re.split 等内部步骤完成主要工作，最后返回结果。
2. 函数 `_rescan_model_configs`：先进入当前步骤，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 dict、sorted、config_path.is_file 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
3. 函数 `list_models`：先进入当前步骤，再调用 list、_MODEL_CONFIGS.keys 等内部步骤完成主要工作，最后返回结果。
4. 函数 `add_model_config`：先接收输入参数 path，接着根据条件分支选择不同处理路径，再调用 _MODEL_CONFIG_PATHS.append、_rescan_model_configs、isinstance 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
5. 函数 `get_model_config`：先接收输入参数 model_name，接着根据条件分支选择不同处理路径，再调用 deepcopy 等内部步骤完成主要工作，最后返回结果。
6. 函数 `get_tokenizer`：先接收输入参数 model_name，再调用 get_model_config、HFTokenizer 等内部步骤完成主要工作，最后返回结果。
7. 函数 `load_state_dict`：先接收输入参数 checkpoint_path, map_location, model_key, is_openai, skip_list，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 eval、model.state_dict、torch.load 等内部步骤完成主要工作，最后返回结果。
8. 函数 `load_checkpoint`：先接收输入参数 model, checkpoint_path, model_key, strict，接着根据条件分支选择不同处理路径，再调用 load_state_dict、model.load_state_dict、logging.info 等内部步骤完成主要工作，最后返回结果。
9. 函数 `load_clip_visual_state_dict`：先接收输入参数 checkpoint_path, map_location, is_openai, skip_list，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 load_state_dict、list、state_dict.keys 等内部步骤完成主要工作，最后返回结果。
10. 函数 `load_clip_text_state_dict`：先接收输入参数 checkpoint_path, map_location, is_openai, skip_list，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 load_state_dict、list、state_dict.keys 等内部步骤完成主要工作，最后返回结果。
11. 函数 `get_pretrained_tag`：先接收输入参数 pretrained_model，接着根据条件分支选择不同处理路径，再调用 pretrained_model.lower 等内部步骤完成主要工作，最后返回结果。
12. 函数 `load_pretrained_checkpoint`：先接收输入参数 model, visual_checkpoint_path, text_checkpoint_path, strict, visual_model, text_model, model_key, skip_list，接着根据条件分支选择不同处理路径，再调用 get_pretrained_tag、logging.info、model.visual.load_state_dict 等内部步骤完成主要工作，最后返回结果。
13. 函数 `create_model`：先接收输入参数 model_name, pretrained, precision, device, jit, force_quick_gelu, force_custom_clip, force_patch_dropout, pretrained_image, pretrained_text, pretrained_hf, pretrained_visual_model, pretrained_text_model, cache_dir, skip_list, is_only_visual, is_only_text，接着根据条件分支选择不同处理路径，再调用 model_name.replace、isinstance、torch.device 等内部步骤完成主要工作，最后返回结果。
14. 函数 `create_model_and_transforms`：先接收输入参数 model_name, pretrained, precision, device, jit, force_quick_gelu, force_custom_clip, force_patch_dropout, pretrained_image, pretrained_text, pretrained_hf, pretrained_visual_model, pretrained_text_model, image_mean, image_std, cache_dir, skip_list，再调用 create_model、image_transform、getattr 等内部步骤完成主要工作，最后返回结果。
15. 函数 `create_eva_vision_and_transforms`：先接收输入参数 model_name, pretrained, precision, device, jit, force_quick_gelu, force_custom_clip, force_patch_dropout, pretrained_image, pretrained_text, pretrained_hf, pretrained_visual_model, pretrained_text_model, image_mean, image_std, cache_dir, skip_list，再调用 create_model、image_transform、getattr 等内部步骤完成主要工作，最后返回结果。
16. 函数 `create_model_from_pretrained`：先接收输入参数 model_name, pretrained, precision, device, jit, force_quick_gelu, force_custom_clip, force_patch_dropout, return_transform, image_mean, image_std, cache_dir, is_frozen，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 create_model、image_transform、RuntimeError 等内部步骤完成主要工作，最后返回结果。
"""

import json
import logging
import os
import pathlib
import re
from copy import deepcopy
from pathlib import Path
from typing import Optional, Tuple, Union, Dict, Any
import torch

from .constants import OPENAI_DATASET_MEAN, OPENAI_DATASET_STD
from .model import CLIP, CustomCLIP, convert_weights_to_lp, convert_to_custom_text_state_dict,\
    get_cast_dtype
from .openai import load_openai_model
from .pretrained import is_pretrained_cfg, get_pretrained_cfg, download_pretrained, list_pretrained_tags_by_model
from .transform import image_transform
from .tokenizer import HFTokenizer, tokenize
from .utils import resize_clip_pos_embed, resize_evaclip_pos_embed, resize_visual_pos_embed, resize_eva_pos_embed


_MODEL_CONFIG_PATHS = [Path(__file__).parent / f"model_configs/"]
_MODEL_CONFIGS = {}  # directory (model_name: config) of model architecture configs


def _natural_key(string_):  # 中文名称：naturalkey
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_.lower())]


def _rescan_model_configs():  # 中文名称：rescanmodelconfigs
    global _MODEL_CONFIGS

    config_ext = ('.json',)
    config_files = []
    for config_path in _MODEL_CONFIG_PATHS:
        if config_path.is_file() and config_path.suffix in config_ext:
            config_files.append(config_path)
        elif config_path.is_dir():
            for ext in config_ext:
                config_files.extend(config_path.glob(f'*{ext}'))

    for cf in config_files:
        with open(cf, "r", encoding="utf8") as f:
            model_cfg = json.load(f)
            if all(a in model_cfg for a in ('embed_dim', 'vision_cfg', 'text_cfg')):
                _MODEL_CONFIGS[cf.stem] = model_cfg

    _MODEL_CONFIGS = dict(sorted(_MODEL_CONFIGS.items(), key=lambda x: _natural_key(x[0])))


_rescan_model_configs()  # initial populate of model config registry


def list_models():  # 中文名称：listmodels
    """ enumerate available model architectures based on config files """
    return list(_MODEL_CONFIGS.keys())


def add_model_config(path):  # 中文名称：addmodel配置
    """ add model config path or file and update registry """
    if not isinstance(path, Path):
        path = Path(path)
    _MODEL_CONFIG_PATHS.append(path)
    _rescan_model_configs()


def get_model_config(model_name):  # 中文名称：获取model配置
    if model_name in _MODEL_CONFIGS:
        return deepcopy(_MODEL_CONFIGS[model_name])
    else:
        return None


def get_tokenizer(model_name):  # 中文名称：获取tokenizer
    config = get_model_config(model_name)
    tokenizer = HFTokenizer(config['text_cfg']['hf_tokenizer_name']) if 'hf_tokenizer_name' in config['text_cfg'] else tokenize
    return tokenizer


# loading openai CLIP weights when is_openai=True for training
def load_state_dict(checkpoint_path: str, map_location: str='cpu', model_key: str='model|module|state_dict', is_openai: bool=False, skip_list: list=[]):  # 中文名称：加载statedict
    if is_openai:
        model = torch.jit.load(checkpoint_path, map_location="cpu").eval()
        state_dict = model.state_dict()
        for key in ["input_resolution", "context_length", "vocab_size"]:
            state_dict.pop(key, None)
    else:
        checkpoint = torch.load(checkpoint_path, map_location=map_location)
        for mk in model_key.split('|'):
            if isinstance(checkpoint, dict) and mk in checkpoint:
                state_dict = checkpoint[mk]
                break
            else:
                state_dict = checkpoint
        if next(iter(state_dict.items()))[0].startswith('module'):
            state_dict = {k[7:]: v for k, v in state_dict.items()}
    
    for k in skip_list:
        if k in list(state_dict.keys()):
            logging.info(f"Removing key {k} from pretrained checkpoint")
            del state_dict[k]

    if os.getenv('RoPE') == '1':
        for k in list(state_dict.keys()):
            if 'freqs_cos' in k or 'freqs_sin' in k:
                del state_dict[k]
    return state_dict



def load_checkpoint(model, checkpoint_path, model_key="model|module|state_dict", strict=True):  # 中文名称：加载checkpoint
    state_dict = load_state_dict(checkpoint_path, model_key=model_key, is_openai=False)
    # detect old format and make compatible with new format
    if 'positional_embedding' in state_dict and not hasattr(model, 'positional_embedding'):
        state_dict = convert_to_custom_text_state_dict(state_dict)
    if 'text.logit_scale' in state_dict and hasattr(model, 'logit_scale'):
        state_dict['logit_scale'] = state_dict['text.logit_scale']
        del state_dict['text.logit_scale']

    # resize_clip_pos_embed for CLIP and open CLIP
    if 'visual.positional_embedding' in state_dict:
        resize_clip_pos_embed(state_dict, model)
    # specified to eva_vit_model
    elif 'visual.pos_embed' in state_dict:
        resize_evaclip_pos_embed(state_dict, model)

    # resize_clip_pos_embed(state_dict, model)
    incompatible_keys = model.load_state_dict(state_dict, strict=strict)
    logging.info(f"incompatible_keys.missing_keys: {incompatible_keys.missing_keys}")
    return incompatible_keys

def load_clip_visual_state_dict(checkpoint_path: str, map_location: str='cpu', is_openai: bool=False, skip_list:list=[]):  # 中文名称：加载clipvisualstatedict
    state_dict = load_state_dict(checkpoint_path, map_location=map_location, is_openai=is_openai, skip_list=skip_list)

    for k in list(state_dict.keys()):
        if not k.startswith('visual.'):
            del state_dict[k]
    for k in list(state_dict.keys()):
        if k.startswith('visual.'):
            new_k = k[7:]
            state_dict[new_k] = state_dict[k]
            del state_dict[k]
    return state_dict

def load_clip_text_state_dict(checkpoint_path: str, map_location: str='cpu', is_openai: bool=False, skip_list:list=[]):  # 中文名称：加载clip文本statedict
    state_dict = load_state_dict(checkpoint_path, map_location=map_location, is_openai=is_openai, skip_list=skip_list)

    for k in list(state_dict.keys()):
        if k.startswith('visual.'):
            del state_dict[k]
    return state_dict

def get_pretrained_tag(pretrained_model):  # 中文名称：获取pretrainedtag
    pretrained_model = pretrained_model.lower()
    if "laion" in pretrained_model or "open_clip" in pretrained_model:
        return "open_clip"
    elif "openai" in pretrained_model:
        return "clip"
    elif "eva" in pretrained_model and "clip" in pretrained_model:
        return "eva_clip"
    else:
        return "other"

def load_pretrained_checkpoint(
        model,
        visual_checkpoint_path,
        text_checkpoint_path,
        strict=True,
        visual_model=None,
        text_model=None,
        model_key="model|module|state_dict",
        skip_list=[]):  # 中文名称：加载pretrainedcheckpoint
    visual_tag = get_pretrained_tag(visual_model)
    text_tag = get_pretrained_tag(text_model)

    logging.info(f"num of model state_dict keys: {len(model.state_dict().keys())}")
    visual_incompatible_keys, text_incompatible_keys = None, None
    if visual_checkpoint_path:
        if visual_tag == "eva_clip" or visual_tag == "open_clip":
            visual_state_dict = load_clip_visual_state_dict(visual_checkpoint_path, is_openai=False, skip_list=skip_list)
        elif visual_tag == "clip":
            visual_state_dict = load_clip_visual_state_dict(visual_checkpoint_path, is_openai=True, skip_list=skip_list)
        else:
            visual_state_dict = load_state_dict(visual_checkpoint_path, model_key=model_key, is_openai=False, skip_list=skip_list)
    
        # resize_clip_pos_embed for CLIP and open CLIP
        if 'positional_embedding' in visual_state_dict:
            resize_visual_pos_embed(visual_state_dict, model)
        # specified to EVA model
        elif 'pos_embed' in visual_state_dict:
            resize_eva_pos_embed(visual_state_dict, model)

        visual_incompatible_keys = model.visual.load_state_dict(visual_state_dict, strict=strict)
        logging.info(f"num of loaded visual_state_dict keys: {len(visual_state_dict.keys())}")
        logging.info(f"visual_incompatible_keys.missing_keys: {visual_incompatible_keys.missing_keys}")

    if text_checkpoint_path:
        if text_tag == "eva_clip" or text_tag == "open_clip":
            text_state_dict = load_clip_text_state_dict(text_checkpoint_path, is_openai=False, skip_list=skip_list)
        elif text_tag == "clip":
            text_state_dict = load_clip_text_state_dict(text_checkpoint_path, is_openai=True, skip_list=skip_list)
        else:
            text_state_dict = load_state_dict(visual_checkpoint_path, model_key=model_key, is_openai=False, skip_list=skip_list)

        text_incompatible_keys = model.text.load_state_dict(text_state_dict, strict=strict)
        
        logging.info(f"num of loaded text_state_dict keys: {len(text_state_dict.keys())}")
        logging.info(f"text_incompatible_keys.missing_keys: {text_incompatible_keys.missing_keys}")

    return visual_incompatible_keys, text_incompatible_keys

def create_model(
        model_name: str,
        pretrained: Optional[str] = None,
        precision: str = 'fp32',
        device: Union[str, torch.device] = 'cpu',
        jit: bool = False,
        force_quick_gelu: bool = False,
        force_custom_clip: bool = False,
        force_patch_dropout: Optional[float] = None,
        pretrained_image: str = '',
        pretrained_text: str = '',
        pretrained_hf: bool = True,
        pretrained_visual_model: str = None,
        pretrained_text_model: str = None,
        cache_dir: Optional[str] = None,
        skip_list: list  = [],
        is_only_visual: bool = False,
        is_only_text: bool = False,
):  # 中文名称：创建model
    model_name = model_name.replace('/', '-')  # for callers using old naming with / in ViT names
    if isinstance(device, str):
        device = torch.device(device)

    if pretrained and pretrained.lower() == 'openai':
        logging.info(f'Loading pretrained {model_name} from OpenAI.')
        model = load_openai_model(
            model_name,
            precision=precision,
            device=device,
            jit=jit,
            cache_dir=cache_dir,
        )
    else:
        model_cfg = get_model_config(model_name)
        if model_cfg is not None:
            logging.info(f'Loaded {model_name} model config.')
        else:
            logging.error(f'Model config for {model_name} not found; available models {list_models()}.')
            raise RuntimeError(f'Model config for {model_name} not found.')

        if 'rope' in model_cfg.get('vision_cfg', {}):
            if model_cfg['vision_cfg']['rope']:
                os.environ['RoPE'] = "1"
        else:
            os.environ['RoPE'] = "0"

        if force_quick_gelu:
            # override for use of QuickGELU on non-OpenAI transformer models
            model_cfg["quick_gelu"] = True
        
        if force_patch_dropout is not None:
            # override the default patch dropout value
            model_cfg['vision_cfg']["patch_dropout"] = force_patch_dropout

        cast_dtype = get_cast_dtype(precision)
        custom_clip = model_cfg.pop('custom_text', False) or force_custom_clip or ('hf_model_name' in model_cfg['text_cfg'])


        if custom_clip:
            if 'hf_model_name' in model_cfg.get('text_cfg', {}):
                model_cfg['text_cfg']['hf_model_pretrained'] = pretrained_hf
            model = CustomCLIP(**model_cfg, cast_dtype=cast_dtype, is_only_visual=is_only_visual, is_only_text=is_only_text)
        else:
            model = CLIP(**model_cfg, cast_dtype=cast_dtype)
            print("Not CustomCLIP: If you have set building only visual or text tower, you may still get a complete CLIP model.")

        pretrained_cfg = {}
        if pretrained:
            checkpoint_path = ''
            pretrained_cfg = get_pretrained_cfg(model_name, pretrained)
            if pretrained_cfg:
                checkpoint_path = download_pretrained(pretrained_cfg, cache_dir=cache_dir)
            elif os.path.exists(pretrained):
                checkpoint_path = pretrained

            if checkpoint_path:
                logging.info(f'Loading pretrained {model_name} weights ({pretrained}).')
                load_checkpoint(model,
                               checkpoint_path,
                               model_key="model|module|state_dict",
                               strict=False
                               ) 
            else:
                error_str = (
                    f'Pretrained weights ({pretrained}) not found for model {model_name}.'
                    f'Available pretrained tags ({list_pretrained_tags_by_model(model_name)}.')
                logging.warning(error_str)
                raise RuntimeError(error_str)
        else:
            visual_checkpoint_path = ''
            text_checkpoint_path = ''
            
            if pretrained_image:
                pretrained_visual_model = pretrained_visual_model.replace('/', '-')  # for callers using old naming with / in ViT names
                pretrained_image_cfg = get_pretrained_cfg(pretrained_visual_model, pretrained_image)
                if 'timm_model_name' in model_cfg.get('vision_cfg', {}):
                    # pretrained weight loading for timm models set via vision_cfg
                    model_cfg['vision_cfg']['timm_model_pretrained'] = True
                elif pretrained_image_cfg:
                    visual_checkpoint_path = download_pretrained(pretrained_image_cfg, cache_dir=cache_dir)
                elif os.path.exists(pretrained_image):
                    visual_checkpoint_path = pretrained_image
                else:
                    logging.warning(f'Pretrained weights ({visual_checkpoint_path}) not found for model {model_name}.visual.')
                    raise RuntimeError(f'Pretrained weights ({visual_checkpoint_path}) not found for model {model_name}.visual.')

            if pretrained_text:
                pretrained_text_model = pretrained_text_model.replace('/', '-')  # for callers using old naming with / in ViT names
                pretrained_text_cfg = get_pretrained_cfg(pretrained_text_model, pretrained_text)
                if pretrained_image_cfg:
                    text_checkpoint_path = download_pretrained(pretrained_text_cfg, cache_dir=cache_dir)
                elif os.path.exists(pretrained_text):
                    text_checkpoint_path = pretrained_text
                else:
                    logging.warning(f'Pretrained weights ({text_checkpoint_path}) not found for model {model_name}.text.')
                    raise RuntimeError(f'Pretrained weights ({text_checkpoint_path}) not found for model {model_name}.text.')
            
            if visual_checkpoint_path:
                logging.info(f'Loading pretrained {model_name}.visual weights ({visual_checkpoint_path}).')
            if text_checkpoint_path:
                logging.info(f'Loading pretrained {model_name}.text weights ({text_checkpoint_path}).')

            if visual_checkpoint_path or text_checkpoint_path:
                load_pretrained_checkpoint(
                    model,
                    visual_checkpoint_path,
                    text_checkpoint_path,
                    strict=False,
                    visual_model=pretrained_visual_model,
                    text_model=pretrained_text_model,
                    model_key="model|module|state_dict",
                    skip_list=skip_list
                )
        
        if "fp16" in precision or "bf16" in precision:
            logging.info(f'convert precision to {precision}')
            model = model.to(torch.bfloat16) if 'bf16' in precision else model.to(torch.float16)

        model.to(device=device)

        # set image / mean metadata from pretrained_cfg if available, or use default
        if not is_only_text:
            model.visual.image_mean = pretrained_cfg.get('mean', None) or OPENAI_DATASET_MEAN
            model.visual.image_std = pretrained_cfg.get('std', None) or OPENAI_DATASET_STD

        if jit:
            model = torch.jit.script(model)

    return model


def create_model_and_transforms(
        model_name: str,
        pretrained: Optional[str] = None,
        precision: str = 'fp32',
        device: Union[str, torch.device] = 'cpu',
        jit: bool = False,
        force_quick_gelu: bool = False,
        force_custom_clip: bool = False,
        force_patch_dropout: Optional[float] = None,
        pretrained_image: str = '',
        pretrained_text: str = '',
        pretrained_hf: bool = True,
        pretrained_visual_model: str = None,
        pretrained_text_model: str = None,
        image_mean: Optional[Tuple[float, ...]] = None,
        image_std: Optional[Tuple[float, ...]] = None,
        cache_dir: Optional[str] = None,
        skip_list: list = [],
):  # 中文名称：创建modelandtransforms
    model = create_model(
        model_name,
        pretrained,
        precision=precision,
        device=device,
        jit=jit,
        force_quick_gelu=force_quick_gelu,
        force_custom_clip=force_custom_clip,
        force_patch_dropout=force_patch_dropout,
        pretrained_image=pretrained_image,
        pretrained_text=pretrained_text,
        pretrained_hf=pretrained_hf,
        pretrained_visual_model=pretrained_visual_model,
        pretrained_text_model=pretrained_text_model,
        cache_dir=cache_dir,
        skip_list=skip_list,
    )

    image_mean = image_mean or getattr(model.visual, 'image_mean', None)
    image_std = image_std or getattr(model.visual, 'image_std', None)
    preprocess_train = image_transform(
        model.visual.image_size,
        is_train=True,
        mean=image_mean,
        std=image_std
    )
    preprocess_val = image_transform(
        model.visual.image_size,
        is_train=False,
        mean=image_mean,
        std=image_std
    )

    return model, preprocess_train, preprocess_val

def create_eva_vision_and_transforms(
        model_name: str,
        pretrained: Optional[str] = None,
        precision: str = 'fp32',
        device: Union[str, torch.device] = 'cpu',
        jit: bool = False,
        force_quick_gelu: bool = False,
        force_custom_clip: bool = False,
        force_patch_dropout: Optional[float] = None,
        pretrained_image: str = '',
        pretrained_text: str = '',
        pretrained_hf: bool = True,
        pretrained_visual_model: str = None,
        pretrained_text_model: str = None,
        image_mean: Optional[Tuple[float, ...]] = None,
        image_std: Optional[Tuple[float, ...]] = None,
        cache_dir: Optional[str] = None,
        skip_list: list = [],
):  # 中文名称：创建evavisionandtransforms
    model = create_model(
        model_name,
        pretrained,
        precision=precision,
        device=device,
        jit=jit,
        force_quick_gelu=force_quick_gelu,
        force_custom_clip=force_custom_clip,
        force_patch_dropout=force_patch_dropout,
        pretrained_image=pretrained_image,
        pretrained_text=pretrained_text,
        pretrained_hf=pretrained_hf,
        pretrained_visual_model=pretrained_visual_model,
        pretrained_text_model=pretrained_text_model,
        cache_dir=cache_dir,
        skip_list=skip_list,
        is_only_visual=True, # only use visual tower
    )

    image_mean = image_mean or getattr(model.visual, 'image_mean', None)
    image_std = image_std or getattr(model.visual, 'image_std', None)
    preprocess_train = image_transform(
        model.visual.image_size,
        is_train=True,
        mean=image_mean,
        std=image_std
    )
    preprocess_val = image_transform(
        model.visual.image_size,
        is_train=False,
        mean=image_mean,
        std=image_std
    )

    return model, preprocess_train, preprocess_val

def create_model_from_pretrained(
        model_name: str,
        pretrained: str,
        precision: str = 'fp32',
        device: Union[str, torch.device] = 'cpu',
        jit: bool = False,
        force_quick_gelu: bool = False,
        force_custom_clip: bool = False,
        force_patch_dropout: Optional[float] = None,
        return_transform: bool = True,
        image_mean: Optional[Tuple[float, ...]] = None,
        image_std: Optional[Tuple[float, ...]] = None,
        cache_dir: Optional[str] = None,
        is_frozen: bool = False,
):  # 中文名称：创建modelfrompretrained
    if not is_pretrained_cfg(model_name, pretrained) and not os.path.exists(pretrained):
        raise RuntimeError(
            f'{pretrained} is not a valid pretrained cfg or checkpoint for {model_name}.'
            f' Use open_clip.list_pretrained() to find one.')

    model = create_model(
        model_name,
        pretrained,
        precision=precision,
        device=device,
        jit=jit,
        force_quick_gelu=force_quick_gelu,
        force_custom_clip=force_custom_clip,
        force_patch_dropout=force_patch_dropout,
        cache_dir=cache_dir,
    )

    if is_frozen:
        for param in model.parameters():
            param.requires_grad = False

    if not return_transform:
        return model

    image_mean = image_mean or getattr(model.visual, 'image_mean', None)
    image_std = image_std or getattr(model.visual, 'image_std', None)
    preprocess = image_transform(
        model.visual.image_size,
        is_train=False,
        mean=image_mean,
        std=image_std
    )

    return model, preprocess
