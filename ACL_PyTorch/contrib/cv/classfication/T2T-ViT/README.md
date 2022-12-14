# T2T-ViT Onnx模型端到端推理指导

## 1 模型概述


### 1.1 论文地址

[Tokens-to-Token ViT: Training Vision Transformers from Scratch on ImageNet](https://arxiv.org/abs/2101.11986)

### 1.2 代码地址

开源仓：[https://github.com/yitu-opensource/T2T-ViT](https://github.com/yitu-opensource/T2T-ViT)<br>
branch：main<br>
commit_id：0f63dc9558f4d192de926504dbddfa1b3f5db6ca<br>

本离线推理项目实现的模型为开源仓中的T2T-ViT-14模型。

## 2 环境说明

该模型离线推理使用 Atlas 300I Pro 推理卡，所有步骤都在 [CANN 5.1.RC1](https://www.hiascend.com/software/cann/commercial) 环境下进行，CANN包以及相关驱动、固件的安装请参考 [软件安装](https://www.hiascend.com/document/detail/zh/canncommercial/51RC1/envdeployment/instg)。
### 2.1 安装依赖
```shell
conda create -n ${env_name} python=3.7.5
conda activate ${env_name}
pip install -r requirements.txt 
```
env_name为虚拟环境的名称

### 2.2 获取开源仓代码
```shell
git clone https://github.com/yitu-opensource/T2T-ViT.git
cd T2T-ViT
git checkout main
git reset --hard 0f63dc9558f4d192de926504dbddfa1b3f5db6ca
```

## 3 源码改动
1. models/token_performer.py文件打补丁：
```shell
patch -p1 models/token_performer.py token_performer.patch
```
改动原因：<br>
由于OM模型中Einsum算子低精度计算（float16）会放大误差，导致精度问题。在转OM时使用--keep_dtype参数，尝试让Einsum算子保持原精度(float32)计算，但Einsum算子前面的TransData算子又会使此操作失效。所以定位到Einsum算子在模型源码中的位置，对其进行等价替换后，重新转ONNX，转OM时再使用--keep_dtype参数，TransData算子被消除，--keep_dtype参数生效。<br>

2. 进入虚拟环境中 timm/models/layers/文件夹内：
```shell
patch -p1 helpers.py ${patch_path}
```
patch_path为helpers.patch文件路径。<br>
改动原因：<br>
torch在1.8版本之后container_abcs已经被移除，使用timm包内的models/layers/helpers.py时会报错。<br>

3. 进入虚拟环境中timm/data文件夹内：
```shell
patch -p1 loader.py ${patch_path}
```
patch_path为loaders.patch文件路径。<br>
改动原因：<br>
由于310P上无GPU，使用timm包内的data/loader.py时会报错。<br>

## 4 模型转换

### 4.1 Pytorch转ONNX模型

1. 下载pth权重文件
```shell
wget https://github.com/yitu-opensource/T2T-ViT/releases/download/main/81.5_T2T_ViT_14.pth.tar
```

2. 执行T2T_ViT_pth2onnx.py脚本，生成ONNX模型文件

```shell
python3.7 T2T_ViT_pth2onnx.py --pth-dir ${pth_path} --onnx-dir ${onnx_path}
```
参数说明：<br>
--pth-path: Pytorch模型文件路径<br>
--onnx-path: ONNX模型文件保存路径（包括文件名）<br>

### 4.2 ONNX转OM模型

1. 设置环境变量

```shell
source /usr/local/Ascend/ascend-toolkit/set_env.sh
```

该命令中使用CANN默认安装路径(/usr/local/Ascend/ascend-toolkit)中的环境变量，使用过程中请按照实际安装路径设置环境变量。

2、生成OM模型
ATC工具的使用请参考 [ATC模型转换](https://www.hiascend.com/document/detail/zh/canncommercial/51RC1/inferapplicationdev/atctool)

```shell
atc --framework=5 --model=${onnx-path} --output=${om-path} --input_format=NCHW --input_shape="image:${bs},3,224,224" --log=error --soc_version=Ascend${chip_name} --keep_dtype=keep_dtype.cfg
```
参数说明：<br>
--model：ONNX模型文件路径<br>
--output：生成OM模型的保存路径（含文件名）<br>
执行命令前，需设置--input_shape参数中bs的数值，例如：1、4、8、16、32、64。<br> 
chip_name可通过`npu-smi info`指令查看，例：310P3。<br>
![Image](https://gitee.com/ascend/ModelZoo-PyTorch/raw/master/ACL_PyTorch/images/310P3.png)

## 5 数据预处理


### 5.1 数据集获取

该模型使用[ImageNet官网](http://www.image-net.org/)的5万张验证集图片进行测试。<br>
数据集结构如下：
```
│imagenet/
├──train/
│  ├── n01440764
│  │   ├── n01440764_10026.JPEG
│  │   ├── n01440764_10027.JPEG
│  │   ├── ......
│  ├── ......
├──val/
│  ├── n01440764
│  │   ├── ILSVRC2012_val_00000293.JPEG
│  │   ├── ILSVRC2012_val_00002138.JPEG
│  │   ├── ......
│  ├── ......
```

### 5.2 数据集预处理

运行T2T_ViT_preprocess.py预处理脚本，生成数据集预处理后的bin文件。

```shell
python3.7 T2T_ViT_preprocess.py -–data-dir ${dataset_path} --out-dir ${prep_output_dir} –gt-path ${groundtruth_path} -–batch-size ${batch_size}
```
参数说明：<br>
--data-dir：数据集路径<br>
--out-dir：保存bin文件路径<br>
--gt-path：保存标签文件路径<br>
--batch-size：需要测试的batch_size<br>


## 6 离线推理

### 6.1 msame工具

本项目使用msame工具进行推理，msame编译及用法参考[msame推理工具](https://gitee.com/ascend/tools/tree/master/msame)。<br>
msame推理前需要设置环境变量：
``` shell
source /usr/local/Ascend/ascend-toolkit/set_env.sh 
```

该命令中使用CANN默认安装路径(/usr/local/Ascend/ascend-toolkit)中的环境变量，使用过程中请按照实际安装路径设置环境变量。

### 6.2 离线推理

运行如下命令进行离线推理：

```shell
./msame --model ${om_path}  --input ${input_dataset_path} --output ${output_dir} --outfmt BIN
```
参数说明：<br>
--model：为om模型文件路径<br>
--input：数据预处理后的bin文件路径<br>
--output：保存标签路径（含文件名）<br>

输出结果保存在output_dir中，文件类型为bin文件。

### 6.3 精度验证

运行T2T_ViT_postprocess.py脚本并与npy文件比对，可以获得Accuracy Top1数据。

```shell
python3.7 T2T_ViT_postprocess.py –result-dir ${msame_bin_path} –gt-path ${gt_path} --batch-size ${batch_size}
```
参数说明：<br>
--result-dir：生成推理结果所在路径<br>
--gt-path：标签数据文件路径<br>
--batch-size：需要测试的batch_size<br>


### 6.4 性能验证
需注意：性能测试前使用`npu-smi info`命令查看 NPU 设备的状态，确认空闲后再进行测试。<br>
用msame工具进行纯推理100次，然后根据平均耗时计算出吞吐率。
```shell
./msame --model ${om_path} --output ${output_path} --outfmt TXT --loop 100
```
参数说明：<br>
--model：为om模型文件路径<br>
--output：保存推理结果路径<br>

执行上述命令后，日志中会记录Inference average time without first time，即为NPU计算的平均耗时(ms)。以此计算出模型在对应 batch_size 下的吞吐率：
$$ 吞吐率 = \frac {bs * 1000} {time}$$



## 7 精度和性能对比

总结：
 1. 310P上离线推理的精度(81.414%)与Pytorch在线推理精度(81.5%)基本持平；
 2. 性能最优的batch_size为8，310P性能/性能基准=5.44倍。

各batch_size对比结果如下：

|     模型     |                        开源仓Pytorch精度                        | 310P离线推理精度 | 基准性能 | 310P性能 |
| :----------: | :-------------------------------------------------------: | :--------------: | :------: | :------: |
| T2T-ViT bs1  | [rank1:81.5%](https://github.com/yitu-opensource/T2T-ViT) |   rank1:81.4%    |  24fps   |  142fps  |
| T2T-ViT bs4  | [rank1:81.5%](https://github.com/yitu-opensource/T2T-ViT) |   rank1:81.4%    |  32fps   |  179fps  |
| T2T-ViT bs8  | [rank1:81.5%](https://github.com/yitu-opensource/T2T-ViT) |   rank1:81.4%    |  39fps   |  212fps  |
| T2T-ViT bs16 | [rank1:81.5%](https://github.com/yitu-opensource/T2T-ViT) |   rank1:81.4%    |  35fps   |  210fps  |
| T2T-ViT bs32 | [rank1:81.5%](https://github.com/yitu-opensource/T2T-ViT) |   rank1:81.4%    |  34fps   |  203fps  |
| T2T-ViT bs64 | [rank1:81.5%](https://github.com/yitu-opensource/T2T-ViT) |   rank1:81.4%    |  36fps   |  198fps  |