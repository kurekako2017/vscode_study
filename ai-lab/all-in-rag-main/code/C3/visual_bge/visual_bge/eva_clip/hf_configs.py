# HF architecture dict:
"""
文件功能概述：`code/C3/visual_bge/visual_bge/eva_clip/hf_configs.py` 主要是 hfconfigs，这个文件里有 0 个类、0 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 这个文件没有独立类或函数，主要靠模块级代码直接执行。
"""

arch_dict = {
  # https://huggingface.co/docs/transformers/model_doc/roberta#roberta
  "roberta": {
      "config_names": {
          "context_length": "max_position_embeddings",
          "vocab_size": "vocab_size",
          "width": "hidden_size",
          "heads": "num_attention_heads",
          "layers": "num_hidden_layers",
          "layer_attr": "layer",
          "token_embeddings_attr": "embeddings"
      },
      "pooler": "mean_pooler",
  },
  # https://huggingface.co/docs/transformers/model_doc/xlm-roberta#transformers.XLMRobertaConfig
  "xlm-roberta": {
      "config_names": {
          "context_length": "max_position_embeddings",
          "vocab_size": "vocab_size",
          "width": "hidden_size",
          "heads": "num_attention_heads",
          "layers": "num_hidden_layers",
          "layer_attr": "layer",
          "token_embeddings_attr": "embeddings"
      },
      "pooler": "mean_pooler",
  },
  # https://huggingface.co/docs/transformers/model_doc/mt5#mt5
  "mt5": {
      "config_names": {
          # unlimited seqlen
          # https://github.com/google-research/text-to-text-transfer-transformer/issues/273
          # https://github.com/huggingface/transformers/blob/v4.24.0/src/transformers/models/t5/modeling_t5.py#L374
          "context_length": "",
          "vocab_size": "vocab_size",
          "width": "d_model",
          "heads": "num_heads",
          "layers": "num_layers",
          "layer_attr": "block",
          "token_embeddings_attr": "embed_tokens"
      },
      "pooler": "mean_pooler",
  },
  "bert": {
    "config_names": {
      "context_length": "max_position_embeddings",
      "vocab_size": "vocab_size",
      "width": "hidden_size",
      "heads": "num_attention_heads",
      "layers": "num_hidden_layers",
      "layer_attr": "layer",
      "token_embeddings_attr": "embeddings"
    },
    "pooler": "mean_pooler",
  }
}
