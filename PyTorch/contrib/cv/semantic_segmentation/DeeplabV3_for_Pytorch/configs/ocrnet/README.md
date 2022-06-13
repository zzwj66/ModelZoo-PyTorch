# Object-Contextual Representations for Semantic Segmentation

## Introduction

<!-- [ALGORITHM] -->

```latex
@article{YuanW18,
  title={Ocnet: Object context network for scene parsing},
  author={Yuhui Yuan and Jingdong Wang},
  booktitle={arXiv preprint arXiv:1809.00916},
  year={2018}
}

@article{YuanCW20,
  title={Object-Contextual Representations for Semantic Segmentation},
  author={Yuhui Yuan and Xilin Chen and Jingdong Wang},
  booktitle={ECCV},
  year={2020}
}
```

## Results and models

### Cityscapes

#### HRNet backbone

| Method | Backbone           | Crop Size | Lr schd | Mem (GB) | Inf time (fps) |  mIoU | mIoU(ms+flip) | config                                                                                                                     | download                                                                                                                                                                                                                                                                                                                                                 |
| ------ | ------------------ | --------- | ------: | -------- | -------------- | ----: | ------------: | -------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| OCRNet | HRNetV2p-W18-Small | 512x1024  |   40000 | 3.5      | 10.45          | 74.30 |         75.95 | [config](   )  | [model](   ) &#124; [log](   )     |
| OCRNet | HRNetV2p-W18       | 512x1024  |   40000 | 4.7      | 7.50           | 77.72 |         79.49 | [config](   )   | [model](   ) &#124; [log](   )         |
| OCRNet | HRNetV2p-W48       | 512x1024  |   40000 | 8        | 4.22           | 80.58 |         81.79 | [config](   )   | [model](   ) &#124; [log](   )         |
| OCRNet | HRNetV2p-W18-Small | 512x1024  |   80000 | -        | -              | 77.16 |         78.66 | [config](   )  | [model](   ) &#124; [log](   )     |
| OCRNet | HRNetV2p-W18       | 512x1024  |   80000 | -        | -              | 78.57 |         80.46 | [config](   )   | [model](   ) &#124; [log](   )         |
| OCRNet | HRNetV2p-W48       | 512x1024  |   80000 | -        | -              | 80.70 |         81.87 | [config](   )   | [model](   ) &#124; [log](   )         |
| OCRNet | HRNetV2p-W18-Small | 512x1024  |  160000 | -        | -              | 78.45 |         79.97 | [config](   ) | [model](   ) &#124; [log](   ) |
| OCRNet | HRNetV2p-W18       | 512x1024  |  160000 | -        | -              | 79.47 |         80.91 | [config](   )  | [model](   ) &#124; [log](   )     |
| OCRNet | HRNetV2p-W48       | 512x1024  |  160000 | -        | -              | 81.35 |         82.70 | [config](   )  | [model](   ) &#124; [log](   )     |

#### ResNet backbone

| Method | Backbone | Crop Size | Batch Size | Lr schd | Mem (GB) | Inf time (fps) | mIoU  | mIoU(ms+flip) | config                                                                                                                          | download                                                                                                                                                                                                                                                                                                                                                     |
| ------ | -------- | --------- | ---------- | ------- | -------- | -------------- | ----- | ------------: | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| OCRNet | R-101-D8 | 512x1024  | 8          | 40000   | -        | -              | 80.09 |             - | [config](   )  | [model](   ) &#124; [log](   )     |
| OCRNet | R-101-D8 | 512x1024  | 16         | 40000   | 8.8      | 3.02           | 80.30 |             - | [config](   ) | [model](   ) &#124; [log](   ) |
| OCRNet | R-101-D8 | 512x1024  | 16         | 80000   | 8.8      | 3.02           | 80.81 |             - | [config](   ) | [model](   ) &#124; [log](   ) |

### ADE20K

| Method | Backbone           | Crop Size | Lr schd | Mem (GB) | Inf time (fps) |  mIoU | mIoU(ms+flip) | config                                                                                                                | download                                                                                                                                                                                                                                                                                                                             |
| ------ | ------------------ | --------- | ------: | -------- | -------------- | ----: | ------------: | --------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| OCRNet | HRNetV2p-W18-Small | 512x512   |   80000 | 6.7      | 28.98          | 35.06 |         35.80 | [config](   )  | [model](   ) &#124; [log](   )     |
| OCRNet | HRNetV2p-W18       | 512x512   |   80000 | 7.9      | 18.93          | 37.79 |         39.16 | [config](   )   | [model](   ) &#124; [log](   )         |
| OCRNet | HRNetV2p-W48       | 512x512   |   80000 | 11.2     | 16.99          | 43.00 |         44.30 | [config](   )   | [model](   ) &#124; [log](   )         |
| OCRNet | HRNetV2p-W18-Small | 512x512   |  160000 | -        | -              | 37.19 |         38.40 | [config](   ) | [model](   ) &#124; [log](   ) |
| OCRNet | HRNetV2p-W18       | 512x512   |  160000 | -        | -              | 39.32 |         40.80 | [config](   )  | [model](   ) &#124; [log](   )     |
| OCRNet | HRNetV2p-W48       | 512x512   |  160000 | -        | -              | 43.25 |         44.88 | [config](   )  | [model](   ) &#124; [log](   )     |

### Pascal VOC 2012 + Aug

| Method | Backbone           | Crop Size | Lr schd | Mem (GB) | Inf time (fps) |  mIoU | mIoU(ms+flip) | config                                                                                                                 | download                                                                                                                                                                                                                                                                                                                                 |
| ------ | ------------------ | --------- | ------: | -------- | -------------- | ----: | ------------: | ---------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| OCRNet | HRNetV2p-W18-Small | 512x512   |   20000 | 3.5      | 31.55          | 71.70 |         73.84 | [config](   ) | [model](   ) &#124; [log](   ) |
| OCRNet | HRNetV2p-W18       | 512x512   |   20000 | 4.7      | 19.91          | 74.75 |         77.11 | [config](   )  | [model](   ) &#124; [log](   )     |
| OCRNet | HRNetV2p-W48       | 512x512   |   20000 | 8.1      | 17.83          | 77.72 |         79.87 | [config](   )  | [model](   ) &#124; [log](   )     |
| OCRNet | HRNetV2p-W18-Small | 512x512   |   40000 | -        | -              | 72.76 |         74.60 | [config](   ) | [model](   ) &#124; [log](   ) |
| OCRNet | HRNetV2p-W18       | 512x512   |   40000 | -        | -              | 74.98 |         77.40 | [config](   )  | [model](   ) &#124; [log](   )     |
| OCRNet | HRNetV2p-W48       | 512x512   |   40000 | -        | -              | 77.14 |         79.71 | [config](   )  | [model](   ) &#124; [log](   )     |