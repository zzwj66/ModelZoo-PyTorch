# BSD 3-Clause License
#
# Copyright (c) 2017 xxxx
# All rights reserved.
# Copyright 2021 Huawei Technologies Co., Ltd
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# ============================================================================
from .beit import *
from .byoanet import *
from .byobnet import *
from .cait import *
from .coat import *
from .convit import *
from .convmixer import *
from .crossvit import *
from .cspnet import *
from .densenet import *
from .dla import *
from .dpn import *
from .efficientnet import *
from .ghostnet import *
from .gluon_resnet import *
from .gluon_xception import *
from .hardcorenas import *
from .hrnet import *
from .inception_resnet_v2 import *
from .inception_v3 import *
from .inception_v4 import *
from .levit import *
from .mlp_mixer import *
from .mobilenetv3 import *
from .nasnet import *
from .nest import *
from .nfnet import *
from .pit import *
from .pnasnet import *
from .regnet import *
from .res2net import *
from .resnest import *
from .resnet import *
from .resnetv2 import *
from .rexnet import *
from .selecsls import *
from .senet import *
from .sknet import *
from .swin_transformer import *
from .tnt import *
from .tresnet import *
from .twins import *
from .vgg import *
from .visformer import *
from .vision_transformer import *
from .vision_transformer_hybrid import *
from .vovnet import *
from .xception import *
from .xception_aligned import *
from .xcit import *

from .factory import create_model, split_model_name, safe_model_name
from .helpers import load_checkpoint, resume_checkpoint, model_parameters
from .layers import TestTimePoolHead, apply_test_time_pool
from .layers import convert_splitbn_model
from .layers import is_scriptable, is_exportable, set_scriptable, set_exportable, is_no_jit, set_no_jit
from .registry import register_model, model_entrypoint, list_models, is_model, list_modules, is_model_in_modules,\
    has_model_default_key, is_model_default_key, get_model_default_value, is_model_pretrained
