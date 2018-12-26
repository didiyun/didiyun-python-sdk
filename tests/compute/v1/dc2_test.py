# coding: utf-8

from __future__ import print_function
import unittest
import time
import tests.common.client
import tests.common as c

cli = tests.common.client.DicloudClient()


def hex_to_str(s):
    return ''.join([chr(i) for i in [int(b, 16) for b in s.split(' ')]])

def str_to_hex(s):
    return ''.join([hex(ord(c)).replace('0x', '') for c in s])

class TestDc2(unittest.TestCase):

    def test_create_dc2(self):
        # 获取镜像并选择
        imgResp = cli.dc2Stub.ListImage(c.ListImageRequest(header=c.Header(regionId='gz')))
        self.assertEqual(imgResp.error.errno, 0)
        for img in imgResp.data:
            if img.osFamily == 'CentOS' and img.osVersion == '7.5':
                targetImgUuid = img.imgUuid
                break

        self.assertIsNotNone(targetImgUuid)
        print("choose image, uuid:", targetImgUuid)
        # 获取子网并选择
        vpcResp = cli.vpcStub.ListVpc(c.ListVpcRequest(header=c.Header(regionId='gz'),
                                                       start=0,
                                                       limit=10))
        self.assertEqual(vpcResp.error.errno, 0)
        subnetResp = cli.vpcStub.ListSubnet(c.ListSubnetRequest(header=c.Header(regionId='gz'),
                                                                condition=c.ListSubnetCondition(vpcUuid=vpcResp.data[0].vpcUuid),
                                                                start=0,
                                                                limit=10))
        self.assertEqual(subnetResp.error.errno, 0)
        print("choose subnet, uuid:",subnetResp.data[0].subnetUuid)
        createDc2Req = c.CreateDc2Request(header=c.Header(regionId='gz'),
                                                        name='test-python-sdk',
                                                        imgUuid=targetImgUuid,
                                                        subnetUuid=subnetResp.data[0].subnetUuid,
                                                        dc2Model='dc2.s1.small1.d20',
                                                        password=str_to_hex('YourPassword123'))  # 密码进行16位编码后传输
        createDc2Req.eip.bandwidth = 5   # 同时创建EIP，设置带宽
        ebs1 = createDc2Req.ebs.add()    # 同时创建EBS，对于数组参数调用add()添加
        ebs1.diskType = 'SSD'
        ebs1.size = 30
        createDc2Resp = cli.dc2Stub.CreateDc2(createDc2Req)   # 创建DC2
        self.assertEqual(createDc2Resp.error.errno, 0)
        print("createDc2, jobUuid:", createDc2Resp.data[0].jobUuid)
        done = False
        queryTimes = 0
        while not done:     # 轮询异步进度
            queryTimes = queryTimes + 1
            time.sleep(3)
            jobResultResp = cli.commonStub.JobResult(c.JobResultRequest(header=c.Header(regionId='gz'),
                                                                        jobUuids=[createDc2Resp.data[0].jobUuid]))
            if jobResultResp.error.errno != 0:
                print("query job", createDc2Resp.data[0].jobUuid, "Result error, errmsg:", jobResultResp.error.errmsg)
                break
            done = jobResultResp.data[0].done
            print("query job", createDc2Resp.data[0].jobUuid, "query times:", queryTimes, "done:", done, "success:", jobResultResp.data[0].success)


if __name__ == '__main__':
    unittest.main()
