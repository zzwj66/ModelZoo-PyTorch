# Copyright 2020 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import time
import logging
from pathlib import Path
from collections import OrderedDict

import numpy as np

import torch
import torch.nn as nn

from timm.utils import *

torch.backends.cudnn.benchmark = True
_logger = logging.getLogger('train')


def _parse_args():

    parser = argparse.ArgumentParser(description='T2T-ViT postprocess.')
    parser.add_argument('--result-dir', type=str, metavar='DIR', help='path to model output')
    parser.add_argument('--gt-path', type=str, metavar='PATH', help='path to groundtruth')
    parser.add_argument('-b', '--batch-size', type=int, default=1, metavar='N',help='input batch size for training (default: 64)')
    args = parser.parse_args()

    args.prefetcher = True
    args.distributed = False
    args.device = 'cpu'
    args.world_size = 1
    args.rank = 0
    args.img_size = 224
    args.interpolation = ''
    args.mean = None
    args.std = None
    args.crop_pct = None
    args.channels_last = False
    args.tta = 0
    args.log_interval = 50
    args.local_rank = 0
    args.model_ema = True
    args.model_ema_force_cpu = False
    args.model_ema_decay = 0.99996
    args.seed = 42
    args.num_classes = 1000

    return args


def post_precess(result_dir, gt_path, args):

    labels = torch.from_numpy(np.load(gt_path))

    loss_fn = nn.CrossEntropyLoss()
    batch_time_m = AverageMeter()
    losses_m = AverageMeter()
    top1_m = AverageMeter()
    top5_m = AverageMeter()

    for res_path in Path(result_dir).iterdir():
        for res in Path(res_path).iterdir():
            batch_idx = int(res.stem.replace('_output_0', ''))
            for i in range(batch_idx*args.batch_size,(batch_idx+1)*args.batch_size):
                target = torch.tensor([labels[batch_idx][int(i%args.batch_size)]])
                output = np.fromfile(res.__str__(), dtype=np.float32)
                output = output[(i-batch_idx*args.batch_size)*1000:(i-batch_idx*args.batch_size)*1000+1000]
                output = torch.from_numpy(output.reshape(1, args.num_classes))

                reduce_factor = args.tta
                if reduce_factor > 1:
                    output = output.unfold(0, reduce_factor, reduce_factor).mean(dim=2)
                    target = target[0:target.size(0):reduce_factor]
                pred_label = output.argmax()
                loss = loss_fn(output, target)
                acc1, acc5 = accuracy(output, target, topk=(1, 5))

                if args.distributed:
                    reduced_loss = reduce_tensor(loss.data, args.world_size)
                    acc1 = reduce_tensor(acc1, args.world_size)
                    acc5 = reduce_tensor(acc5, args.world_size)
                else:
                    reduced_loss = loss.data

                losses_m.update(reduced_loss.item(), output.size(0))
                top1_m.update(acc1.item(), output.size(0))
                top5_m.update(acc5.item(), output.size(0))

                end = time.time()
                batch_time_m.update(time.time() - end)
                if args.local_rank == 0 and i % args.log_interval == 0:
                    log_name = 'Test'
                    _logger.info(
                        '{0}: [{1:>4d}]  '
                        'Time: {batch_time.val:.3f} ({batch_time.avg:.3f})  '
                        'Loss: {loss.val:>7.4f} ({loss.avg:>6.4f})  '
                        'Acc@1: {top1.val:>7.4f} ({top1.avg:>7.4f})  '
                        'Acc@5: {top5.val:>7.4f} ({top5.avg:>7.4f})'.format(
                        log_name, i, batch_time=batch_time_m,
                        loss=losses_m, top1=top1_m, top5=top5_m))

    metrics = OrderedDict([('loss', losses_m.avg), ('top1', top1_m.avg), ('top5', top5_m.avg)])
    print(f"Top-1 accuracy of the model is: {metrics['top1']:.1f}%")
    print(f"val_metrics: {metrics}")

    return metrics


def main():
    setup_default_logging()
    args = _parse_args()
    torch.manual_seed(args.seed + args.rank)

    post_precess(args.result_dir, args.gt_path, args)


if __name__ == '__main__':
    main()