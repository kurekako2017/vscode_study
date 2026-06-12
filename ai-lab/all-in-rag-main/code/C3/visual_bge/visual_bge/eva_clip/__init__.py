"""
文件功能概述：`code/C3/visual_bge/visual_bge/eva_clip/__init__.py` 主要是 初始化，这个文件里有 0 个类、0 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 这个文件没有独立类或函数，主要靠模块级代码直接执行。
"""

from .constants import OPENAI_DATASET_MEAN, OPENAI_DATASET_STD
from .factory import create_model, create_model_and_transforms, create_model_from_pretrained, get_tokenizer, create_eva_vision_and_transforms
from .factory import list_models, add_model_config, get_model_config, load_checkpoint
from .loss import ClipLoss
from .model import CLIP, CustomCLIP, CLIPTextCfg, CLIPVisionCfg,\
    convert_weights_to_lp, convert_weights_to_fp16, trace_model, get_cast_dtype
from .openai import load_openai_model, list_openai_models
from .pretrained import list_pretrained, list_pretrained_models_by_tag, list_pretrained_tags_by_model,\
    get_pretrained_url, download_pretrained_from_url, is_pretrained_cfg, get_pretrained_cfg, download_pretrained
from .tokenizer import SimpleTokenizer, tokenize
from .transform import image_transform