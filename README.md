# 快速开始 Getting Started

滴滴云Python开发者工具套件（didiyun-python-sdk）可让您在python语言环境下不用复杂编程即可访问滴滴云下计算产品线产品及账单类操作。本节介绍如何获取滴滴云python sdk并开始调用。

## 环境准备
* 滴滴云python sdk基于python语言，支持python2与python3。本文默认您已安装python的基本语言环境，将不再进行赘述。
* 滴滴云python sdk使用OAuth 2.0协议Bearer Token(RFC 6750)形式进行API访问授权。为使用滴滴云Python SDK，您需要为账号生成一个滴滴云API Token。您可在滴滴云控制台中的API Token管理页面上创建您的Token。

## 安装滴滴云python sdk
执行以下命令，安装滴滴云python sdk。滴滴云python sdk依赖google grpc及protobuf3.x等package，已为您将相关依赖集成在requirement.txt文件中。

```
git clone https://github.com/didiyun/didiyun-python-sdk
python -m pip install -r ./didiyun-python-sdk/requirements.txt
```

## 使用滴滴云python sdk
以下代码示例展示了调用滴滴云python sdk的三个主要步骤：

1. 使用oauth2 Token验证方式，调用grpc.secure_channel获取一个channel。
2. 使用此channel初始化需要访问的产品线对应的Stub。
3. 组装请求体，发起请求并处理应答或错误。

```
# coding:utf-8

from __future__ import print_function

import grpc

from grpc.beta import implementations
from base.v1 import base_pb2
from compute.v1 import dc2_pb2
from compute.v1 import dc2_pb2_grpc


def oauth2token_credentials(context, callback):
    callback([('authorization', 'Bearer Your-Token')], None)


def run():
    serverAddr = 'open.didiyunapi.com:8080'
    transport_creds = implementations.ssl_channel_credentials()
    auth_creds = implementations.metadata_call_credentials(oauth2token_credentials)
    channel_creds = implementations.composite_channel_credentials(transport_creds, auth_creds)
    with grpc.secure_channel(serverAddr, channel_creds) as channel:
        dc2_stub = dc2_pb2_grpc.Dc2Stub(channel)
        try:
            response = dc2_stub.ListImage(dc2_pb2.ListImageRequest(header=base_pb2.Header(regionId='gz')))
            print(response.error)
            print(response.data)
        except Exception as e:
            print("except: ", e)

if __name__ == '__main__':
    run()

```

# 参数结构
滴滴云python sdk中参数定义遵循google protobuf规范，我们使用创建DC2的请求来举例。

```
_CREATEDC2REQUEST = _descriptor.Descriptor(
  name='CreateDc2Request',
  full_name='didi.cloud.compute.v1.CreateDc2Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='header', full_name='didi.cloud.compute.v1.CreateDc2Request.header', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='count', full_name='didi.cloud.compute.v1.CreateDc2Request.count', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='autoContinue', full_name='didi.cloud.compute.v1.CreateDc2Request.autoContinue', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='payPeriod', full_name='didi.cloud.compute.v1.CreateDc2Request.payPeriod', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='couponId', full_name='didi.cloud.compute.v1.CreateDc2Request.couponId', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    
    ... //此处省略
    
    _descriptor.FieldDescriptor(
      name='eip', full_name='didi.cloud.compute.v1.CreateDc2Request.eip', index=18,
      number=19, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ebs', full_name='didi.cloud.compute.v1.CreateDc2Request.ebs', index=19,
      number=20, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_CREATEDC2REQUEST_EIP, _CREATEDC2REQUEST_EBS, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=3376,
  serialized_end=4058,
)

```

在如上展示的部分消息结构中，共有`header`、`count`、`autoContinue`、`payPeriod`、`couponId`、`eip`、`ebs`七个字段。

其中：
1. 字段的type值表明了参数的类型，可参考[滴滴云python sdk中的type属性枚举](#typeEnum)。
2. nested_types声明了此消息结构中的两个内联消息结构。
3. 通过label属性我们可判断此字段是否为一个数组，其中label=3时为数组类型。
需要注意的是，对于数组类型，需要调用其`.Add()`方法来添加元素后再设置其值，例：

```
ebs = createDc2Request.ebs.add()
ebs.diskType = 'SSD'
ebs.size = 30
```

<span id="typeEnum"></span>
滴滴云python sdk中的type属性枚举
```
  TYPE_DOUBLE         = 1   //double
  TYPE_FLOAT          = 2   //float
  TYPE_INT64          = 3   //int64
  TYPE_INT32          = 5   //int32
  TYPE_BOOL           = 8   //bool
  TYPE_STRING         = 9   //string
  TYPE_MESSAGE        = 11  //消息结构
```

# 错误处理
调用滴滴云python sdk中的所有Client的相应方法返回的Response均包含一个通用的滴滴云error字段和一个data字段，如下所示。

```
_descriptor.FieldDescriptor(
      name='error', full_name='didi.cloud.compute.v1.ListImageResponse.error', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
_descriptor.FieldDescriptor(
      name='data', full_name='didi.cloud.compute.v1.ListImageResponse.data', index=1,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
```

滴滴云python sdk在调用出错时，会返回相应的的错误信息。在调用结束时，建议您遵循以下步骤对调用响应进行处理：
1. 使用try对异常进行处理，确定sdk端的调用是否产生错误。
2. 对返回响应中的Error中的Errno进行判断，如果不为0，表示服务端产生了错误。
3. 若没有错误，处理返回响应中的Data部分。

```
try:
    response = dc2_stub.ListImage(dc2_pb2.ListImageRequest(header=base_pb2.Header(regionId='gz')))
    print(response.error)
    print(response.data)
except Exception as e:
    print("except: ", e)
```
   
# 异步调用
滴滴云python sdk中，所有对于资源的操作类请求都是异步实现的。在调用例如DC2开机等一系列异步操作类请求时，您可在返回值中获取到任务信息。

您需要调用JobResult方法，通过jobUuid来轮询获取此任务的进度。
其中，Done字段表示服务端是否还在处理此任务，Success字段表示处理结果是否成功。
建议您遵循以下步骤对异步任务进行处理：
1. 先判断调用响应是否有错误。
2. 对返回响应中的Done字段进行判断，若为false，则等待片刻重新轮询，若为true，表示任务完成，继续第3步。
3. 判断success字段，若为true，表示任务操作成功，若为false，表示任务失败，此时可读取result字段查看错误信息。

# 调用与错误示例
对于滴滴云python sdk提供的所有接口，文件内均有调用示例，您可运行每个接口的调用示例作为编写代码的参考。（部分示例的正确运行需要您手动指定正确参数）。

创建DC2包含了滴滴云python sdk的查询，异步请求以及轮询任务进度等一系列全过程，建议您以创建DC2作为参考。
您可使用以下命令运行创建DC2示例：

```
cd didiyun-python-sdk/tests/compute/v1
python dc2_test.py
```

在调用失败时，您可以通过错误码（Errno）与错误信息（Errmsg）得到调用错误的原因，若无法解决，可联系[滴滴云技术支持](#https://help.didiyun.com/hc/request/new/)。
常见错误码如下：

| 错误码  | 错误信息 |  描述  |
|-----|-----|-----|
| 0 | ok	| 调用成功 |
| 1 | 请求有点问题，请反馈客服 | 传入参数非法 |
| 2 | 服务开小差，请稍等| 系统错误，请联系技术支持 |
| 3 | 服务开小差，休息一会再试试 | 未知问题，请联系技术支持 |
| 4 | 认证错误/AccessDenied | token认证失败 |
| 13 | 调用方式有点小问题，请反馈客服 | 传入参数非法 |
| 40000 | 会话异常，请重新登录或稍后再试 | 会话异常，可稍后尝试，如仍有问题请联系技术支持 |
| 41017 | 查询SNAP信息失败 | - |
| 41025 | 查询套餐失败 | - |
| 41026 | 查询镜像失败 | - |
| 41039 | 查询EIP信息失败 | - |
| 41049 | 找不到SG | - |
| 41050 | 创建SG失败 | - |
| 41052 | 查询SG信息失败 | - |
| 41053 | 查询安全组规则失败 | - |
| 41054 | 删除SG失败 | - |
| 41056 | 绑定DC2至安全组失败 | - |
| 41057 | DC2从安全组解绑失败 | - |
| 41059 | 不允许删除默认SG | - |
| 41060 | 找不到指定SG规则 | - |
| 41063 | 找不到指定DC2 | - |
| 41088 | 创建EBS失败 | - |
| 41094 | 查询EBS信息失败 | - |
| 41099 | 创建DC2失败 | - |
| 41107 | 修改DC2规格失败 | - |
| 41108 | 查询DC2信息失败 | - |
| 41113 | 查询EBS总量失败 | - |
| 41115 | 查询SNAP总量失败 | - |
| 41117 | 查询DC2总量失败 | - |
| 41121 | 查询VPC信息失败 | - |
| 41126 | 查询SUBNET信息失败 | - |
| 41135 | 查询SUBNET总量失败 | - |
| 41139 | 校验子网网段失败 | - |
| 41153 | 请先解绑所有关联到该安全组的DC2 | - |
| 41164 | 不允许更改为不同类型的DC2规格 | - |
| 41165 | 不允许更改为更低配置的DC2规格 | - |
| 41172 | 通用型DC2根盘超过大小限制 | - |
| 41181 | 安全组规则存在重复项，请检查输入 | - |
| 1000011 | 账户已欠费，无法进行该操作 | 账户欠费被限制无法进行资源操作，请充值解除欠费状态后再试 |
| 1100017 | 包月到期策略设置失败 | 更改包月到期策略失败，请联系技术支持 |
| 1100018 | 包月续费设置失败 | 包月续费失败，请联系技术支持 |
| 1100020 | 余额不足 | 购买资源金额超过余额，请充值后再试 |
| 1100022 | 获取价格失败 | 获取资源价格失败，请联系技术支持 |
| 1100026 | 包月信息获取失败 | - |
| 1100027 | 包月资源不能删除 | - |
| 1100029 | 所选资源暂不允许包月购买 | - |
| 1100036 | 资源已转换为包月，无需重复操作 | - |
| 1300000 | 资源价格获取失败 | - |
| 2000001 | sshkey增加错误 | - |
| 2000002 | sshkey查询错误 | - |
| 2000003 | sshkey删除错误 | - |
| 2000004 | 不合法的sshkey | - |
| 10000001 | 没有权限，请联系管理员 | 无权限进行此操作，请咨询技术支持 |
| 16000002 | 查询地域与可用区信息失败 | - |
