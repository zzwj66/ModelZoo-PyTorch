## 一、依赖

    NPU配套的run包安装    
    Python 3.7.5
    PyTorch(NPU版本)
    apex(NPU版本)
    torch(NPU版本)
    torchvision
    pillow
    提示：安装与torch版本相对应的torchvision
## 二、训练流程：
    data_path为数据集imagenet所在的路径
   
### 单卡训练流程：

```shell
	1. 安装环境
	2. 开始训练
	    bash test/train_full_1p.sh  --data_path=/data/imagenet       #精度训练
```

	
### 多卡训练流程

```shell
	1. 安装环境
	2. 开始训练
	    bash test/train_full_8p.sh  --data_path=/data/imagenet       #精度训练
```


	
## 三、Docker容器训练：
    
1. 导入镜像二进制包docker import ubuntuarmpytorch.tar REPOSITORY:TAG, 比如:

        docker import ubuntuarmpytorch.tar pytorch:b020

2. 执行docker_start.sh后带三个参数：步骤1生成的REPOSITORY:TAG；数据集路径；模型执行路径；比如：

        ./docker_start.sh pytorch:b020 /train/imagenet /home/MobileNet

3. 执行步骤一训练流程（环境安装除外）
	
## 四、测试结果
    
- 训练日志路径：在训练脚本的同目录下result文件夹里，如：

        /home/Gluon_ResNet50_v1b_for_PyTorch/test/output/
        
	

