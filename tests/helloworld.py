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
