import math
import copy
import torch
import random
from torch import nn
import torch.utils.checkpoint
from transformers.utils import logging
from transformers.activations import ACT2FN
from typing import List, Optional, Tuple, Union
from transformers.modeling_utils import PreTrainedModel
from transformers.modeling_utils import PreTrainedModel
from torch.nn import BCEWithLogitsLoss, CrossEntropyLoss, MSELoss
from transformers.models.bart.configuration_bart import BartConfig
from transformers.modeling_outputs import (
    BaseModelOutput,
    BaseModelOutputWithPastAndCrossAttentions,
    CausalLMOutputWithCrossAttentions, Seq2SeqLMOutput, 
    Seq2SeqModelOutput, Seq2SeqQuestionAnsweringModelOutput, Seq2SeqSequenceClassifierOutput,
)

"""
Khi áp dụng hàm shift_tokens_right, 
các mã thông báo trong chuỗi đầu vào được dịch chuyển sang phải một vị trí. Mục đích của việc dịch chuyển này 
là để tạo ra một chuỗi mới mà mỗi từ tại vị trí i trong chuỗi mới tương ứng với từ tiếp theo mà mô hình cần dự đoán trong chuỗi ban đầu.
Bằng cách dịch chuyển mã thông báo sang phải, mô hình có thể học cách dự đoán từ tiếp theo dựa trên các từ trước đó trong chuỗi. Ví dụ, nếu chuỗi ban đầu là 
"Tôi thích ăn", sau khi áp dụng shift_tokens_right, chuỗi mới sẽ trở thành "Thích ăn" và mô hình có thể học cách dự đoán từ tiếp theo sau "ăn" là gì, ví dụ như "cơm" hoặc "trái cây".
"""

def shift_tokens_right(input_ids: torch.Tensor, pad_token_id: int, decoder_start_token_id: int):
    """
    Shift input ids one token to the right.
    
    """
    shifted_input_ids = input_ids.new_zeros(input_ids.shape)
    shifted_input_ids[:, 1:] = input_ids[:, :-1].clone()
    shifted_input_ids[:, 0] = decoder_start_token_id

    assert pad_token_id is not None, "self.model.config.pad_token_id has to be defined."

    shifted_input_ids.masked_fill_(shifted_input_ids == -100, pad_token_id); return shifted_input_ids

def _make_causal_mask(input_ids_shape: torch.Size, dtype: torch.dtype, past_key_values_length: int = 0):
    """
    Make causal mask used for bi-directional self-attention.
    """
    bsz, tgt_len = input_ids_shape
    mask = torch.full((tgt_len, tgt_len), float("-inf"))
    mask_cond = torch.arange(mask.size(-1))
    mask.masked_fill_(mask_cond < (mask_cond + 1).view(mask.size(-1), 1), 0)
    mask = mask.to(dtype)

    if past_key_values_length > 0:
        mask = torch.cat([torch.zeros(tgt_len, past_key_values_length, dtype=dtype), mask], dim=-1)
    return mask[None, None, :, :].expand(bsz, 1, tgt_len, tgt_len + past_key_values_length)