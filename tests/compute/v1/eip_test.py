# coding: utf-8

from __future__ import print_function
import unittest
import tests.common.client
import tests.common as c

cli = tests.common.client.DicloudClient()


class TestEip(unittest.TestCase):
    """在有一个gz的没绑定EIP的DC2的情况下，才可运行此test"""
    def test_01_create_eip(self):
        print("================Begin Test Create Eip================")
        createEipReq = c.CreateEipRequest(header=c.Header(regionId='gz', zoneId='gz01'), bandwidth=1)   # 1M带宽按时长计费
        createEipResp = cli.eipStub.CreateEip(createEipReq)  # 创建EBS
        print(createEipReq)
        self.assertEqual(createEipResp.error.errno, 0)
        print("createEip, jobUuid:", createEipResp.data[0].jobUuid)
        success = cli.wait_for_job_result(createEipResp.data[0].jobUuid)  # 轮询等待结果
        print("createEip, success:", success)
        self.assertTrue(success)

    def test_02_list_eip(self):
        print("================Begin Test List Eip================")
        listResp = cli.eipStub.ListEip(c.ListEipRequest(header=c.Header(regionId='gz'), start=0, limit=10))
        print(listResp)
        self.assertEqual(listResp.error.errno, 0)
        self.assertTrue(len(listResp.data) > 0)

    def test_03_get_eip_by_uuid(self):
        print("================Begin Test Get Eip By Uuid================")
        listResp = cli.eipStub.ListEip(c.ListEipRequest(header=c.Header(regionId='gz'),
                                                        start=0, limit=10))  # 获取一个EBS的Uuid
        self.assertEqual(listResp.error.errno, 0)
        self.assertTrue(len(listResp.data) > 0)
        getEipByUuidResp = cli.eipStub.GetEipByUuid(c.GetEipByUuidRequest(header=c.Header(regionId='gz'),
                                                                          eipUuid=listResp.data[0].eipUuid))
        print(getEipByUuidResp)
        self.assertEqual(getEipByUuidResp.error.errno, 0)
        self.assertTrue(len(getEipByUuidResp.data) > 0)

    def test_04_get_eip_total_cnt(self):
        print("================Begin Test Get Eip Total Cnt================")
        cntResp = cli.eipStub.GetEipTotalCnt(c.GetEipTotalCntRequest(header=c.Header(regionId='gz')))
        print(cntResp)
        self.assertEqual(cntResp.error.errno, 0)
        self.assertTrue(cntResp.data[0].totalCnt > 0)

    def test_05_attach_eip_to_dc2(self):
        print("================Begin Test Attach Eip To Dc2================")
        listDc2Resp = cli.dc2Stub.ListDc2(c.ListDc2Request(header=c.Header(regionId='gz'),
                                                        start=0, limit=10))  # 获取一个gz的DC2的Uuid
        self.assertEqual(listDc2Resp.error.errno, 0)
        self.assertTrue(len(listDc2Resp.data) > 0)
        self.assertEqual(len(listDc2Resp.data[0].eip.eipUuid), 0)

        listEipResp = cli.eipStub.ListEip(c.ListEipRequest(header=c.Header(regionId='gz'),
                                                        start=0, limit=10))  # 获取一个gz的EIP的Uuid
        self.assertEqual(listEipResp.error.errno, 0)
        self.assertTrue(len(listEipResp.data) > 0)
        self.assertEqual(len(listEipResp.data[0].dc2.dc2Uuid), 0)
        attachEipToDc2Req = c.AttachEipToDc2Request(header=c.Header(regionId='gz'))
        eipToAttach = attachEipToDc2Req.eip.add()
        eipToAttach.bindingUuid = listDc2Resp.data[0].dc2Uuid
        eipToAttach.eipUuid = listEipResp.data[0].eipUuid
        attachEipToDc2Resp = cli.eipStub.AttachEipToDc2(attachEipToDc2Req)
        print(attachEipToDc2Resp)
        self.assertEqual(attachEipToDc2Resp.error.errno, 0)
        print("attachEipToDc2, jobUuid:", attachEipToDc2Resp.data[0].jobUuid)
        success = cli.wait_for_job_result(attachEipToDc2Resp.data[0].jobUuid)  # 轮询等待结果
        print("attachEipToDc2, success:", success)
        self.assertTrue(success)

    def test_06_detach_eip_from_dc2(self):
        print("================Begin Test Detach Eip From Dc2================")
        listEipResp = cli.eipStub.ListEip(c.ListEipRequest(header=c.Header(regionId='gz'),
                                                           start=0, limit=10))  # 获取一个gz的EIP的Uuid
        self.assertEqual(listEipResp.error.errno, 0)
        self.assertTrue(len(listEipResp.data) > 0)
        self.assertIsNotNone(listEipResp.data[0].dc2)
        detachEipFromDc2Req = c.DetachEipFromDc2Request(header=c.Header(regionId='gz'))
        eipToDetach = detachEipFromDc2Req.eip.add()
        eipToDetach.eipUuid = listEipResp.data[0].eipUuid
        detachEipFromDc2Resp = cli.eipStub.DetachEipFromDc2(detachEipFromDc2Req)
        print(detachEipFromDc2Resp)
        self.assertEqual(detachEipFromDc2Resp.error.errno, 0)
        print("detachEipFromDc2, jobUuid:", detachEipFromDc2Resp.data[0].jobUuid)
        success = cli.wait_for_job_result(detachEipFromDc2Resp.data[0].jobUuid)  # 轮询等待结果
        print("detachEipFromDc2, success:", success)
        self.assertTrue(success)

    def test_07_change_eip_bandwidth(self):
        print("================Begin Test Change Ebs Size ================")
        listEipResp = cli.eipStub.ListEip(c.ListEipRequest(header=c.Header(regionId='gz'),
                                                           start=0, limit=10))  # 获取一个gz的EIP的Uuid
        self.assertEqual(listEipResp.error.errno, 0)
        self.assertTrue(len(listEipResp.data) > 0)
        changeEipBandwidthReq = c.ChangeEipBandwidthRequest(header=c.Header(regionId='gz'))
        eipToChangeBandwidth = changeEipBandwidthReq.eip.add()
        eipToChangeBandwidth.eipUuid = listEipResp.data[0].eipUuid
        eipToChangeBandwidth.bandwidth = 2
        changeEipBandwidthResp = cli.eipStub.ChangeEipBandwidth(changeEipBandwidthReq)
        print(changeEipBandwidthResp)
        self.assertEqual(changeEipBandwidthResp.error.errno, 0)
        print("changeEipBandwidth, jobUuid:", changeEipBandwidthResp.data[0].jobUuid)
        success = cli.wait_for_job_result(changeEipBandwidthResp.data[0].jobUuid)  # 轮询等待结果
        print("changeEipBandwidth, success:", success)
        self.assertTrue(success)

    def test_08_delete_eip(self):
        print("================Begin Test Delete Eip================")
        listEipResp = cli.eipStub.ListEip(c.ListEipRequest(header=c.Header(regionId='gz'),
                                                           start=0, limit=10))  # 获取一个gz的EIP的Uuid
        self.assertEqual(listEipResp.error.errno, 0)
        self.assertTrue(len(listEipResp.data) > 0)
        deleteEipReq = c.DeleteEipRequest(header=c.Header(regionId='gz'))
        eipToDelete = deleteEipReq.eip.add()
        eipToDelete.eipUuid = listEipResp.data[0].eipUuid
        deleteEipResp = cli.eipStub.DeleteEip(deleteEipReq)
        print(deleteEipResp)
        self.assertEqual(deleteEipResp.error.errno, 0)
        print("deleteEip, jobUuid:", deleteEipResp.data[0].jobUuid)
        success = cli.wait_for_job_result(deleteEipResp.data[0].jobUuid)  # 轮询等待结果
        print("deleteEip, success:", success)
        self.assertTrue(success)


if __name__ == '__main__':
    unittest.main()

