# coding:utf-8

import grpc
from grpc.beta import implementations
from compute.v1 import common_pb2_grpc, dc2_pb2_grpc, ebs_pb2_grpc, eip_pb2_grpc, sg_pb2_grpc, snap_pb2_grpc, vpc_pb2_grpc


class DicloudClient(object):
    """简单实现的Client 谨作参考"""

    def __init__(self, oauth2_token='Your-Token', addr='open.didiyunapi.com:8080'):

        def oauth2token_credentials(context, callback):
            callback([('authorization', 'Bearer %s' % oauth2_token)], None)

        transport_creds = implementations.ssl_channel_credentials()
        auth_creds = implementations.metadata_call_credentials(oauth2token_credentials)
        channel_creds = implementations.composite_channel_credentials(transport_creds, auth_creds)
        self.channel = grpc.secure_channel(addr, channel_creds)
        self.commonStub = common_pb2_grpc.CommonStub(self.channel)
        self.dc2Stub = dc2_pb2_grpc.Dc2Stub(self.channel)
        self.eipStub = eip_pb2_grpc.EipStub(self.channel)
        self.ebsStub = ebs_pb2_grpc.EbsStub(self.channel)
        self.sgStub = sg_pb2_grpc.SgStub(self.channel)
        self.snapStub = snap_pb2_grpc.SnapStub(self.channel)
        self.vpcStub = vpc_pb2_grpc.VpcStub(self.channel)

