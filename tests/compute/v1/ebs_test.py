# coding: utf-8

from __future__ import print_function
import unittest
import tests.common.client
import tests.common as c

cli = tests.common.client.DicloudClient()


class TestEbs(unittest.TestCase):
    """在有一个gz01的DC2的情况下，才可运行此test"""
    def test_01_create_ebs(self):
        print("================Begin Test Create Ebs================")
        createEbsReq = c.CreateEbsRequest(header=c.Header(regionId='gz', zoneId='gz01'), size=20, diskType='SSD')  # 20G大小SSD 带宽按时长计费
        createEbsResp = cli.ebsStub.CreateEbs(createEbsReq)  # 创建EBS
        print(createEbsResp)
        self.assertEqual(createEbsResp.error.errno, 0)
        print("createEbs, jobUuid:", createEbsResp.data[0].jobUuid)
        success = cli.wait_for_job_result('gz', createEbsResp.data[0].jobUuid)  # 轮询等待结果
        print("createEbs, success:", success)
        self.assertTrue(success)

    def test_02_list_ebs(self):
        print("================Begin Test List Ebs================")
        listResp = cli.ebsStub.ListEbs(c.ListEbsRequest(header=c.Header(regionId='gz'), start=0, limit=10))
        print(listResp)
        self.assertEqual(listResp.error.errno, 0)
        self.assertTrue(len(listResp.data) > 0)

    def test_03_get_ebs_by_uuid(self):
        print("================Begin Test Get Ebs By Uuid================")
        listResp = cli.ebsStub.ListEbs(c.ListEbsRequest(header=c.Header(regionId='gz'),
                                                        start=0, limit=10))  # 获取一个EBS的Uuid
        self.assertEqual(listResp.error.errno, 0)
        self.assertTrue(len(listResp.data) > 0)
        getEbsByUuidResp = cli.ebsStub.GetEbsByUuid(c.GetEbsByUuidRequest(header=c.Header(regionId='gz'),
                                                                          ebsUuid=listResp.data[0].ebsUuid))
        print(getEbsByUuidResp)
        self.assertEqual(getEbsByUuidResp.error.errno, 0)
        self.assertTrue(len(getEbsByUuidResp.data) > 0)

    def test_04_get_ebs_total_cnt(self):
        print("================Begin Test Get Ebs Total Cnt================")
        cntResp = cli.ebsStub.GetEbsTotalCnt(c.GetDc2TotalCntRequest(header=c.Header(regionId='gz')))
        print(cntResp)
        self.assertEqual(cntResp.error.errno, 0)
        self.assertTrue(cntResp.data[0].totalCnt > 0)

    def test_05_attach_ebs_to_dc2(self):
        print("================Begin Test Attach Ebs To Dc2================")
        listDc2Resp = cli.dc2Stub.ListDc2(c.ListDc2Request(header=c.Header(regionId='gz',zoneId='gz01'),
                                                        start=0, limit=10))  # 获取一个gz01的DC2的Uuid
        self.assertEqual(listDc2Resp.error.errno, 0)
        self.assertTrue(len(listDc2Resp.data) > 0)
        listEbsResp = cli.ebsStub.ListEbs(c.ListEbsRequest(header=c.Header(regionId='gz',zoneId='gz01'),
                                                        start=0, limit=10))  # 获取一个gz01的EBS的Uuid
        self.assertEqual(listEbsResp.error.errno, 0)
        self.assertTrue(len(listEbsResp.data) > 0)
        self.assertEqual(len(listEbsResp.data[0].dc2.dc2Uuid),0 )
        attachEbsToDc2Req = c.AttachEbsRequest(header=c.Header(regionId='gz'))
        ebsToAttach = attachEbsToDc2Req.ebs.add()
        ebsToAttach.dc2Uuid = listDc2Resp.data[0].dc2Uuid
        ebsToAttach.ebsUuid = listEbsResp.data[0].ebsUuid
        attachEbsToDc2Resp = cli.ebsStub.AttachEbs(attachEbsToDc2Req)
        print(attachEbsToDc2Resp)
        self.assertEqual(attachEbsToDc2Resp.error.errno, 0)
        print("attachEbsToDc2, jobUuid:", attachEbsToDc2Resp.data[0].jobUuid)
        success = cli.wait_for_job_result('gz', attachEbsToDc2Resp.data[0].jobUuid)  # 轮询等待结果
        print("attachEbsToDc2, success:", success)
        self.assertTrue(success)

    def test_06_detach_ebs_from_dc2(self):
        print("================Begin Test Detach Ebs From Dc2================")
        listEbsResp = cli.ebsStub.ListEbs(c.ListEbsRequest(header=c.Header(regionId='gz', zoneId='gz01'),
                                                           start=0, limit=10))  # 获取一个gz01的EBS的Uuid
        self.assertEqual(listEbsResp.error.errno, 0)
        self.assertTrue(len(listEbsResp.data) > 0)
        self.assertNotEqual(listEbsResp.data[0].dc2.dc2Uuid, 0)   # 确认此EBS上面绑定了DC2
        detachEbsReq = c.DetachEbsRequest(header=c.Header(regionId='gz'))
        ebsToDetach = detachEbsReq.ebs.add()
        ebsToDetach.ebsUuid = listEbsResp.data[0].ebsUuid
        detachEbsResp = cli.ebsStub.DetachEbs(detachEbsReq)
        print(detachEbsResp)
        self.assertEqual(detachEbsResp.error.errno, 0)
        print("detachEbsFromDc2, jobUuid:", detachEbsResp.data[0].jobUuid)
        success = cli.wait_for_job_result('gz', detachEbsResp.data[0].jobUuid)  # 轮询等待结果
        print("detachEbsFromDc2, success:", success)
        self.assertTrue(success)

    def test_07_change_ebs_size(self):
        print("================Begin Test Change Ebs Size ================")
        listEbsResp = cli.ebsStub.ListEbs(c.ListEbsRequest(header=c.Header(regionId='gz', zoneId='gz01'),
                                                           start=0, limit=10))  # 获取一个gz01的EBS的Uuid
        self.assertEqual(listEbsResp.error.errno, 0)
        self.assertTrue(len(listEbsResp.data) > 0)
        changeEbsSizeReq = c.ChangeEbsSizeRequest(header=c.Header(regionId='gz'))
        ebsToChangeSize = changeEbsSizeReq.ebs.add()
        ebsToChangeSize.ebsUuid = listEbsResp.data[0].ebsUuid
        ebsToChangeSize.size = 21
        changeEbsSizeResp = cli.ebsStub.ChangeEbsSize(changeEbsSizeReq)
        print(changeEbsSizeResp)
        self.assertEqual(changeEbsSizeResp.error.errno, 0)
        print("changeEbsSize, jobUuid:", changeEbsSizeResp.data[0].jobUuid)
        success = cli.wait_for_job_result('gz', changeEbsSizeResp.data[0].jobUuid)  # 轮询等待结果
        print("changeEbsSize, success:", success)
        self.assertTrue(success)

    def test_08_change_ebs_name(self):
        print("================Begin Test Change Ebs Name================")
        listEbsResp = cli.ebsStub.ListEbs(c.ListEbsRequest(header=c.Header(regionId='gz', zoneId='gz01'),
                                                           start=0, limit=10))  # 获取一个gz01的EBS的Uuid
        self.assertEqual(listEbsResp.error.errno, 0)
        self.assertTrue(len(listEbsResp.data) > 0)
        changeEbsNameReq = c.ChangeEbsNameRequest(header=c.Header(regionId='gz'))
        ebsToChangeName = changeEbsNameReq.ebs.add()
        ebsToChangeName.ebsUuid = listEbsResp.data[0].ebsUuid
        ebsToChangeName.name = "newEbsName"
        changeEbsNameResp = cli.ebsStub.DetachEbs(changeEbsNameReq)
        print(changeEbsNameResp)
        self.assertEqual(changeEbsNameResp.error.errno, 0)
        print("changeEbsName, jobUuid:", changeEbsNameResp.data[0].jobUuid)
        success = cli.wait_for_job_result('gz', changeEbsNameResp.data[0].jobUuid)  # 轮询等待结果
        print("changeEbsName, success:", success)
        self.assertTrue(success)

    def test_09_delete_ebs(self):
        print("================Begin Test Delete Ebs================")
        listEbsResp = cli.ebsStub.ListEbs(c.ListEbsRequest(header=c.Header(regionId='gz', zoneId='gz01'),
                                                           start=0, limit=10))  # 获取一个gz01的EBS的Uuid
        self.assertEqual(listEbsResp.error.errno, 0)
        self.assertTrue(len(listEbsResp.data) > 0)
        deleteEbsReq = c.DeleteEbsRequest(header=c.Header(regionId='gz'))
        ebsToDelete = deleteEbsReq.ebs.add()
        ebsToDelete.ebsUuid = listEbsResp.data[0].ebsUuid
        deleteEbsResp = cli.ebsStub.DeleteEbs(deleteEbsReq)
        print(deleteEbsResp)
        self.assertEqual(deleteEbsResp.error.errno, 0)
        print("deleteEbs, jobUuid:", deleteEbsResp.data[0].jobUuid)
        success = cli.wait_for_job_result('gz', deleteEbsResp.data[0].jobUuid)  # 轮询等待结果
        print("deleteEbs, success:", success)
        self.assertTrue(success)


if __name__ == '__main__':
    unittest.main()