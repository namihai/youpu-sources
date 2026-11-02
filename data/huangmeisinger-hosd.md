---
title: "黄梅戏唱腔与乐谱对齐数据集（HuangmeiSinger／HOSD）"
summary: "将黄梅戏唱腔录音与唱词、音素、音符及其时长关联，标注区分音节边界、音素边界和连音。"
canonical_url: "https://walkinginthelight.github.io/HuangmeiSinger.github.io/opera/"
publisher: "HuangmeiSinger 项目"
modality: "multimodal"
access_level: "request"
---

# 黄梅戏唱腔与乐谱对齐数据集（HuangmeiSinger／HOSD）

## 亮点

- 将黄梅戏唱腔录音与唱词、音素、音符及其时长关联，标注区分音节边界、音素边界和连音。
- 配套读取程序保留音符时长与音素时长两套序列，并使用连音标记表达唱词与旋律的对应关系。
- 原始录音采样率为44.1 kHz；配套模型处理配置使用24 kHz，两者属于不同处理环节。
- 许可协议：CC BY-NC-SA 4.0，需申请获取，另有引用及下载链接传播要求。
- URL：https://walkinginthelight.github.io/HuangmeiSinger.github.io/opera/

## 把唱词、发音和旋律放在同一条时间线上

HuangmeiSinger项目发布的黄梅戏唱腔数据，在申请表中称为HuangmeiOperaSingingDataset，简称HOSD。数据围绕唱段录音与详细乐谱信息建立标注，将原始谱面、录音、音节和音素边界、音高转写及对齐时长关联起来。

这种组织保留了唱词与旋律的不同粒度：一个字的发音可以延续到多个音符，音符的持续时间也不等同于单个音素的持续时间。连音标记与两套时长信息共同表达这种关系，避免将唱腔简化为逐字配一个音符的文本转录。

项目展示的唱词既有“入深宫”这样的短句，也有较长叙述，另保留“哇”“呀嘛”“喂”等唱词成分。展示页把原录音与不同模型的合成结果并列，原始唱段和模型生成音频分别呈现。

## 配套程序怎样读取标注

公开预处理程序约定从 `transcriptions.txt` 逐行读取记录，以竖线分隔字段；样本编号用于关联 `wavs/样本编号.wav`，其前缀再映射到演唱者编号。程序读取的核心内容包括：

| 标注内容 | 记录的关系 |
|---|---|
| 唱词文本与音素序列 | 唱什么、如何发音 |
| 音符序列与音符时长 | 旋律音高及持续时间 |
| 音素时长 | 发音单元在录音中的时间分配 |
| 连音标记 | 标记连续音的对应情况 |

程序将音符名称转换为MIDI音高数值，并将休止符 `rest` 单独处理；再按音素时长建立声学帧到音素的对齐。这里的MIDI数值是音高表示，不能据此推断数据包另含完整MIDI乐谱文件。

公开配置列有六个演唱者编号，但这属于配套实验的读取设置，不等同于对完整发布包演唱者总数的独立统计。原始录音的44.1 kHz与模型配置的24 kHz也需区分，不能把训练处理参数写成原始录音规格。

## 获取与使用条件

作者的[数据说明](https://github.com/WalkingInTheLight/HuangmeiSinger/tree/main/data/HuangmeiOperaDataset)要求填写申请表后获取下载链接。申请表列明CC BY-NC-SA 4.0，并要求引用相关论文；向他人传播下载链接前需告知作者，另含使用责任及代表所属机构作出承诺的条款。

公开README中的申请收件人仍写为“[anonymous]”，没有给出可直接使用的收件地址。当前公开目录提供申请文件和说明，完整唱腔数据需要另行取得。[代码仓库](https://github.com/WalkingInTheLight/HuangmeiSinger)提供预处理、训练与推理实现。
