# coding:utf-8

from __future__ import print_function
import grpc
import time
from grpc.beta import implementations
from compute.v1.common_pb2 import JobResultRequest
from base.v1.base_pb2 import Header
from bill.v1 import bill_pb2_grpc
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
        self.billStub = bill_pb2_grpc.BillStub(self.channel)
        self.dc2Stub = dc2_pb2_grpc.Dc2Stub(self.channel)
        self.eipStub = eip_pb2_grpc.EipStub(self.channel)
        self.ebsStub = ebs_pb2_grpc.EbsStub(self.channel)
        self.sgStub = sg_pb2_grpc.SgStub(self.channel)
        self.snapStub = snap_pb2_grpc.SnapStub(self.channel)
        self.vpcStub = vpc_pb2_grpc.VpcStub(self.channel)

    def wait_for_job_result(self, regionId, jobUuids):
        allDone = False
        queryTimes = 0
        successResult = []
        if isinstance(jobUuids, unicode):
            jobUuids = [jobUuids]

        while not allDone:  # 轮询异步进度
            queryTimes = queryTimes + 1
            time.sleep(3)
            jobResultResp = self.commonStub.JobResult(JobResultRequest(header=Header(regionId=regionId),
                                                                        jobUuids=jobUuids))
            if jobResultResp.error.errno != 0:
                print("query job uuids", jobUuids, "Result error, errmsg:", jobResultResp.error.errmsg)
                break
            allDone = True
            successResult = []
            for jobResult in jobResultResp.data:
                allDone = allDone and jobResult.done    # 记录任务的进度
                successResult.append(jobResult.success)
                if jobResult.done and (not jobResult.success):
                    print("query job", jobResult.jobUuid, "query times:", queryTimes, "failed, reason:", jobResult.result)
                elif jobResult.done and jobResult.success:
                    print("query job", jobResult.jobUuid, "query times:", queryTimes, "success")
                else:
                    print("query job", jobResult.jobUuid, "query times:", queryTimes, "not done yet")

        return successResult