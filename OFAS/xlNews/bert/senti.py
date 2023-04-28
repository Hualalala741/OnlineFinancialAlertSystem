"""
_*_ coding : utf-8 -*_ 
@author：86136
@date：2023年04月12日
@File : senti
@Project : Archive
"""
import numpy as np
import random
import torch
from transformers import BertModel
from transformers import BertTokenizer


#加载字典和分词工具，即tokenizer



#初始化模型
class Model(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = torch.nn.Linear(768, 3)  # 单层网络模型，只包括了一个fc的神经网络 3是分为三类

    def forward(self, input_ids, attention_mask, token_type_ids):
        pretrained = BertModel.from_pretrained(
            r'D:\86136\新建文件夹\WeChat Files\guoyantong1397\FileStorage\File\2023-04\Archive\xlNews\bert\bert-base-chinese')
        pretrained = pretrained
        with torch.no_grad():
            out = pretrained(input_ids=input_ids,  # 先拿预训练模型来做一个计算，抽取数据当中的特征
                             attention_mask=attention_mask,
                             token_type_ids=token_type_ids)

        # 把抽取出来的特征放到全连接网络中运算，且特征的结果只需要第0个词的特征(跟bert模型的设计方式有关。对句子的情感分类，只需要拿特征中的第0个词来进行分类就可以了)
        out = self.fc(out.last_hidden_state[:, 0])  # torch.Size([16, 768])

        # 将softmax函数应用于一个n维输入张量，对其进行缩放，使n维输出张量的元素位于[0,1]范围内，总和为1
        out = out.softmax(dim=1)

        return out


def output(out):
    if out==0:
        return "积极"
    elif out==1:
        return "中立"
    else:
        return "消极"

def load_model():
    # 定义下游任务模型
    # 加载预训练模型
    set_seed(1)
    # 要跟预训练模型相匹配
    the_model = Model()
    m_state_dict = torch.load(
        r"D:\86136\新建文件夹\WeChat Files\guoyantong1397\FileStorage\File\2023-04\Archive\xlNews\bert\model.pt",
        map_location=torch.device('cpu'))
    the_model.load_state_dict(m_state_dict)
    token = BertTokenizer.from_pretrained('bert-base-chinese')

    return the_model,token


def set_seed(seed):
    """for reproducibility
    :param seed:
    :return:
    """
    np.random.seed(seed)
    random.seed(seed)

    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)

    torch.backends.cudnn.enabled = True
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True



def pred(text,token,the_model):
    the_model.eval()
    res = token.encode_plus(text,
                               truncag='max_length',   # 一律补0到max_length长度
                               max_letion=True,   # 当句子长度大于max_length时，截断
                               paddinngth='max_length',
                                max_length=500,
                                # model_max_length=500,
                               return_tensors='pt',   # 返回pytorch类型的tensor
                               return_length=True)   # 返回length，标识长度

    with torch.no_grad():
        out = the_model(input_ids=res.input_ids,
                    attention_mask=res.attention_mask,
                    token_type_ids=res.token_type_ids)
        out = out.argmax(dim=1)
        re=output(out)
        return re