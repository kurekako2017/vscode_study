"""
文件功能概述：`code/C3/visual_bge/visual_bge/eva_clip/tokenizer.py` 主要是 tokenizer，这个文件里有 2 个类、6 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 函数 `default_bpe`：先进入当前步骤，再调用 lru_cache、os.path.join、os.path.dirname 等内部步骤完成主要工作，最后返回结果。
2. 函数 `bytes_to_unicode`：先进入当前步骤，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 lru_cache、range、dict 等内部步骤完成主要工作，最后返回结果。
3. 函数 `get_pairs`：先接收输入参数 word，然后循环处理每一条数据，再调用 set、pairs.add 等内部步骤完成主要工作，最后返回结果。
4. 函数 `basic_clean`：先接收输入参数 text，再调用 ftfy.fix_text、html.unescape、text.strip 等内部步骤完成主要工作，最后返回结果。
5. 函数 `whitespace_clean`：先接收输入参数 text，再调用 re.sub、text.strip 等内部步骤完成主要工作，最后返回结果。
6. 类 `SimpleTokenizer`：功能概述：这个类是 `SimpleTokenizer`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 bpe_path, special_tokens，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 default_bpe、bytes_to_unicode、split 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 2. `bpe`：先接收输入参数 token，再尝试执行核心处理，出错时进入异常兜底，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 get_pairs、join、tuple 等内部步骤完成主要工作，最后返回结果。 3. `encode`：先接收输入参数 text，然后循环处理每一条数据，再调用 lower、re.findall、join 等内部步骤完成主要工作，最后返回结果。 4. `decode`：先接收输入参数 tokens，再调用 join、replace、decode 等内部步骤完成主要工作，最后返回结果。
7. 函数 `tokenize`：先接收输入参数 texts, context_length，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 isinstance、torch.zeros、enumerate 等内部步骤完成主要工作，最后返回结果。
8. 类 `HFTokenizer`：功能概述：这个类是 `HFTokenizer`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 tokenizer_name，再调用 AutoTokenizer.from_pretrained 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 2. `__call__`：先接收输入参数 texts, context_length，接着根据条件分支选择不同处理路径，再调用 isinstance、whitespace_clean、self.tokenizer 等内部步骤完成主要工作，最后返回结果。
"""

import gzip
import html
import os
from functools import lru_cache
from typing import Union, List

import ftfy
import regex as re
import torch

# https://stackoverflow.com/q/62691279
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"


@lru_cache()
def default_bpe():  # 中文名称：defaultbpe
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "bpe_simple_vocab_16e6.txt.gz")


@lru_cache()
def bytes_to_unicode():  # 中文名称：bytestounicode
    """
    Returns list of utf-8 byte and a corresponding list of unicode strings.
    The reversible bpe codes work on unicode strings.
    This means you need a large # of unicode characters in your vocab if you want to avoid UNKs.
    When you're at something like a 10B token dataset you end up needing around 5K for decent coverage.
    This is a signficant percentage of your normal, say, 32K bpe vocab.
    To avoid that, we want lookup tables between utf-8 bytes and unicode strings.
    And avoids mapping to whitespace/control characters the bpe code barfs on.
    """
    bs = list(range(ord("!"), ord("~")+1))+list(range(ord("¡"), ord("¬")+1))+list(range(ord("®"), ord("ÿ")+1))
    cs = bs[:]
    n = 0
    for b in range(2**8):
        if b not in bs:
            bs.append(b)
            cs.append(2**8+n)
            n += 1
    cs = [chr(n) for n in cs]
    return dict(zip(bs, cs))


def get_pairs(word):  # 中文名称：获取pairs
    """Return set of symbol pairs in a word.
    Word is represented as tuple of symbols (symbols being variable-length strings).
    """
    pairs = set()
    prev_char = word[0]
    for char in word[1:]:
        pairs.add((prev_char, char))
        prev_char = char
    return pairs


def basic_clean(text):  # 中文名称：basic清理
    text = ftfy.fix_text(text)
    text = html.unescape(html.unescape(text))
    return text.strip()


def whitespace_clean(text):  # 中文名称：whitespace清理
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text


class SimpleTokenizer(object):
    """
    功能概述：这个类是 `SimpleTokenizer`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 bpe_path, special_tokens，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 default_bpe、bytes_to_unicode、split 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    2. `bpe`：先接收输入参数 token，再尝试执行核心处理，出错时进入异常兜底，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 get_pairs、join、tuple 等内部步骤完成主要工作，最后返回结果。
    3. `encode`：先接收输入参数 text，然后循环处理每一条数据，再调用 lower、re.findall、join 等内部步骤完成主要工作，最后返回结果。
    4. `decode`：先接收输入参数 tokens，再调用 join、replace、decode 等内部步骤完成主要工作，最后返回结果。
    """
    def __init__(self, bpe_path: str = default_bpe(), special_tokens=None):  # 中文名称：初始化
        self.byte_encoder = bytes_to_unicode()
        self.byte_decoder = {v: k for k, v in self.byte_encoder.items()}
        merges = gzip.open(bpe_path).read().decode("utf-8").split('\n')
        merges = merges[1:49152-256-2+1]
        merges = [tuple(merge.split()) for merge in merges]
        vocab = list(bytes_to_unicode().values())
        vocab = vocab + [v+'</w>' for v in vocab]
        for merge in merges:
            vocab.append(''.join(merge))
        if not special_tokens:
            special_tokens = ['<start_of_text>', '<end_of_text>']
        else:
            special_tokens = ['<start_of_text>', '<end_of_text>'] + special_tokens
        vocab.extend(special_tokens)
        self.encoder = dict(zip(vocab, range(len(vocab))))
        self.decoder = {v: k for k, v in self.encoder.items()}
        self.bpe_ranks = dict(zip(merges, range(len(merges))))
        self.cache = {t:t for t in special_tokens}
        special = "|".join(special_tokens)
        self.pat = re.compile(special + r"""|'s|'t|'re|'ve|'m|'ll|'d|[\p{L}]+|[\p{N}]|[^\s\p{L}\p{N}]+""", re.IGNORECASE)

        self.vocab_size = len(self.encoder)
        self.all_special_ids = [self.encoder[t] for t in special_tokens]

    def bpe(self, token):  # 中文名称：bpe
        if token in self.cache:
            return self.cache[token]
        word = tuple(token[:-1]) + ( token[-1] + '</w>',)
        pairs = get_pairs(word)

        if not pairs:
            return token+'</w>'

        while True:
            bigram = min(pairs, key = lambda pair: self.bpe_ranks.get(pair, float('inf')))
            if bigram not in self.bpe_ranks:
                break
            first, second = bigram
            new_word = []
            i = 0
            while i < len(word):
                try:
                    j = word.index(first, i)
                    new_word.extend(word[i:j])
                    i = j
                except:
                    new_word.extend(word[i:])
                    break

                if word[i] == first and i < len(word)-1 and word[i+1] == second:
                    new_word.append(first+second)
                    i += 2
                else:
                    new_word.append(word[i])
                    i += 1
            new_word = tuple(new_word)
            word = new_word
            if len(word) == 1:
                break
            else:
                pairs = get_pairs(word)
        word = ' '.join(word)
        self.cache[token] = word
        return word

    def encode(self, text):  # 中文名称：encode
        bpe_tokens = []
        text = whitespace_clean(basic_clean(text)).lower()
        for token in re.findall(self.pat, text):
            token = ''.join(self.byte_encoder[b] for b in token.encode('utf-8'))
            bpe_tokens.extend(self.encoder[bpe_token] for bpe_token in self.bpe(token).split(' '))
        return bpe_tokens

    def decode(self, tokens):  # 中文名称：decode
        text = ''.join([self.decoder[token] for token in tokens])
        text = bytearray([self.byte_decoder[c] for c in text]).decode('utf-8', errors="replace").replace('</w>', ' ')
        return text


_tokenizer = SimpleTokenizer()


def tokenize(texts: Union[str, List[str]], context_length: int = 77) -> torch.LongTensor:  # 中文名称：tokenize
    """
    Returns the tokenized representation of given input string(s)

    Parameters
    ----------
    texts : Union[str, List[str]]
        An input string or a list of input strings to tokenize
    context_length : int
        The context length to use; all CLIP models use 77 as the context length

    Returns
    -------
    A two-dimensional tensor containing the resulting tokens, shape = [number of input strings, context_length]
    """
    if isinstance(texts, str):
        texts = [texts]

    sot_token = _tokenizer.encoder["<start_of_text>"]
    eot_token = _tokenizer.encoder["<end_of_text>"]
    all_tokens = [[sot_token] + _tokenizer.encode(text) + [eot_token] for text in texts]
    result = torch.zeros(len(all_tokens), context_length, dtype=torch.long)

    for i, tokens in enumerate(all_tokens):
        if len(tokens) > context_length:
            tokens = tokens[:context_length]  # Truncate
            tokens[-1] = eot_token
        result[i, :len(tokens)] = torch.tensor(tokens)

    return result


class HFTokenizer:
    """
    功能概述：这个类是 `HFTokenizer`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 tokenizer_name，再调用 AutoTokenizer.from_pretrained 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    2. `__call__`：先接收输入参数 texts, context_length，接着根据条件分支选择不同处理路径，再调用 isinstance、whitespace_clean、self.tokenizer 等内部步骤完成主要工作，最后返回结果。
    """
    def __init__(self, tokenizer_name:str):  # 中文名称：初始化
        from transformers import AutoTokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)

    def __call__(self, texts:Union[str, List[str]], context_length:int=77) -> torch.Tensor:
        # same cleaning as for default tokenizer, except lowercasing
        # adding lower (for case-sensitive tokenizers) will make it more robust but less sensitive to nuance  # 中文名称：可调用执行
        if isinstance(texts, str):
            texts = [texts]
        texts = [whitespace_clean(basic_clean(text)) for text in texts]
        input_ids = self.tokenizer(texts, return_tensors='pt', max_length=context_length, padding='max_length', truncation=True).input_ids
        return input_ids
