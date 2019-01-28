# coding: utf-8

from __future__ import print_function
import unittest
import tests.common.client
import tests.common as c

cli = tests.common.client.DicloudClient()


class TestSg(unittest.TestCase):
    """在有一个在默认VPC的DC2的情况下，才可运行此test"""
    def test_01_create_sg(self):
        print("================Begin Test Create Sg================")
        listVpcResp = cli.vpcStub.ListVpc(c.ListVpcRequest(header=c.Header(regionId='gz'),
                                                           start=0, limit=10))  # 获取一个vpc的Uuid
        self.assertEqual(listVpcResp.error.errno, 0)
        self.assertTrue(len(listVpcResp.data) > 0)
        createSgReq = c.CreateSgRequest(header=c.Header(regionId='gz'),
                                            name='testSg',vpcUuid=listVpcResp.data[0].vpcUuid)   # 创建一个默认vpc的sg
        createSgResp = cli.sgStub.CreateSg(createSgReq)
        print(createSgResp)
        self.assertEqual(createSgResp.error.errno, 0)
        print("createSg, jobUuid:", createSgResp.data[0].jobUuid)
        success = cli.wait_for_job_result('gz', createSgResp.data[0].jobUuid)  # 轮询等待结果
        print("createSg, success:", success)
        self.assertTrue(success)

    def test_02_list_sg(self):
        print("================Begin Test List Sg================")
        listResp = cli.sgStub.ListSg(c.ListSgRequest(header=c.Header(regionId='gz'), start=0, limit=10))
        print(listResp)
        self.assertEqual(listResp.error.errno, 0)
        self.assertTrue(len(listResp.data) > 0)

    def test_03_get_sg_total_cnt(self):
        print("================Begin Test Get Sg Total Cnt================")
        cntResp = cli.sgStub.GetSgTotalCnt(c.GetSgTotalCntRequest(header=c.Header(regionId='gz')))
        print(cntResp)
        self.assertEqual(cntResp.error.errno, 0)
        self.assertTrue(cntResp.data[0].totalCnt > 0)

    def test_04_create_sg_rule(self):
        print("================Begin Test Create Sg Rule================")
        listSgResp = cli.sgStub.ListSg(c.ListSgRequest(header=c.Header(regionId='gz'),
                                                        start=0, limit=10))  # 获取一个gz的Sg的Uuid
        self.assertEqual(listSgResp.error.errno, 0)
        self.assertTrue(len(listSgResp.data) > 0)
        createSgRuleReq = c.CreateSgRuleRequest(header=c.Header(regionId='gz'), sgUuid=listSgResp.data[0].sgUuid)
        sgRuleToCreate = createSgRuleReq.sgRule.add()
        sgRuleToCreate.type = "Ingress"     # Ingress为入，Egress为出
        sgRuleToCreate.protocol = "TCP"     # TCP/UDP/ICMP
        sgRuleToCreate.startPort = 1
        sgRuleToCreate.endPort = 800
        sgRuleToCreate.allowedCidr = '0.0.0.0/0'
        createSgRuleResp = cli.sgStub.CreateSgRule(createSgRuleReq)
        print(createSgRuleResp)
        self.assertEqual(createSgRuleResp.error.errno, 0)
        print("createSgRule, jobUuid:", createSgRuleResp.data[0].jobUuid)
        success = cli.wait_for_job_result('gz', createSgRuleResp.data[0].jobUuid)  # 轮询等待结果
        print("createSgRule, success:", success)
        self.assertTrue(success)

    def test_05_list_sg_rule(self):
        print("================Begin Test List Sg Rule================")
        listSgResp = cli.sgStub.ListSg(c.ListSgRequest(header=c.Header(regionId='gz'),
                                                       start=0, limit=10))  # 获取一个gz的Sg的Uuid
        self.assertEqual(listSgResp.error.errno, 0)
        self.assertTrue(len(listSgResp.data) > 0)
        lisgSgRuleResp = cli.sgStub.ListSgRule(c.ListSgRuleRequest(header=c.Header(regionId='gz'),
                                                            start=0, limit=10,condition=c.ListSgRuleCondition(
                                                                sgUuid=listSgResp.data[0].sgUuid)))
        self.assertEqual(lisgSgRuleResp.error.errno, 0)
        self.assertTrue(len(lisgSgRuleResp.data) > 0)

    def test_06_get_sg_rule_total_cnt(self):
        print("================Begin Test Get Sg Rule Total Cnt================")
        listSgResp = cli.sgStub.ListSg(c.ListSgRequest(header=c.Header(regionId='gz'),
                                                       start=0, limit=10))  # 获取一个gz的Sg的Uuid
        self.assertEqual(listSgResp.error.errno, 0)
        self.assertTrue(len(listSgResp.data) > 0)
        cntResp = cli.sgStub.GetSgRuleTotalCnt(c.GetSgRuleTotalCntRequest(header=c.Header(regionId='gz'),
                                                                          sgUuid=listSgResp.data[0].sgUuid))
        print(cntResp)
        self.assertEqual(cntResp.error.errno, 0)
        self.assertTrue(cntResp.data[0].totalCnt > 0)

    def test_07_attach_dc2_to_sg(self):
        print("================Begin Test Attach Dc2 To Sg================")
        listSgResp = cli.sgStub.ListSg(c.ListSgRequest(header=c.Header(regionId='gz'),
                                                       start=0, limit=10))  # 获取一个gz的Sg的Uuid
        self.assertEqual(listSgResp.error.errno, 0)
        self.assertTrue(len(listSgResp.data) > 0)
        listDc2Resp = cli.dc2Stub.ListDc2(c.ListDc2Request(header=c.Header(regionId='gz'),
                                                        start=0, limit=10,
                                                        condition=c.ListDc2Condition(
                                                            sgUuid=listSgResp.data[0].sgUuid,
                                                            sgExclude=True)))  # 获取不在SG下的dc2的Uuid
        self.assertEqual(listDc2Resp.error.errno, 0)
        self.assertTrue(len(listDc2Resp.data) > 0)
        attachDc2ToSgReq = c.AttachDc2ToSgRequest(header=c.Header(regionId='gz'))
        sgToBeAttached = attachDc2ToSgReq.sg.add()
        dc2ToAttach = attachDc2ToSgReq.dc2.add()
        sgToBeAttached.sgUuid=listSgResp.data[0].sgUuid
        dc2ToAttach.dc2Uuid=listDc2Resp.data[0].dc2Uuid
        attachDc2ToSgResp = cli.sgStub.AttachDc2ToSg(attachDc2ToSgReq)
        print(attachDc2ToSgResp)
        self.assertEqual(attachDc2ToSgResp.error.errno, 0)
        print("attachDc2ToSg, jobUuid:", attachDc2ToSgResp.data[0].jobUuid)
        success = cli.wait_for_job_result('gz', attachDc2ToSgResp.data[0].jobUuid)  # 轮询等待结果
        print("attachDc2ToSg, success:", success)
        self.assertTrue(success)

    def test_08_detach_dc2_from_sg(self):
        print("================Begin Test Detach Dc2 From Sg================")
        listSgResp = cli.sgStub.ListSg(c.ListSgRequest(header=c.Header(regionId='gz'),
                                                       start=0, limit=10))  # 获取一个gz的Sg的Uuid
        self.assertEqual(listSgResp.error.errno, 0)
        self.assertTrue(len(listSgResp.data) > 0)
        listDc2Resp = cli.dc2Stub.ListDc2(c.ListDc2Request(header=c.Header(regionId='gz'),
                                                        start=0, limit=10,
                                                        condition=c.ListDc2Condition(
                                                            sgUuid=listSgResp.data[0].sgUuid)))  # 获取在此SG下的dc2的Uuid
        detachDc2FromSgReq = c.DetachDc2FromSgRequest(header=c.Header(regionId='gz'))
        sgToDetach = detachDc2FromSgReq.sg.add()
        dc2ToDetach = detachDc2FromSgReq.dc2.add()
        sgToDetach.sgUuid = listSgResp.data[0].sgUuid
        dc2ToDetach.dc2Uuid = listDc2Resp.data[0].dc2Uuid
        detachDc2FromSgResp = cli.sgStub.DetachDc2FromSg(detachDc2FromSgReq)
        print(detachDc2FromSgResp)
        self.assertEqual(detachDc2FromSgResp.error.errno, 0)
        print("detachDc2FromSg, jobUuid:", detachDc2FromSgResp.data[0].jobUuid)
        success = cli.wait_for_job_result('gz', detachDc2FromSgResp.data[0].jobUuid)  # 轮询等待结果
        print("detachDc2FromSg, success:", success)
        self.assertTrue(success)

    def test_09_delete_sg_rule(self):
        print("================Begin Test Delete Sg Rule================")
        listSgResp = cli.sgStub.ListSg(c.ListSgRequest(header=c.Header(regionId='gz'),
                                                       start=0, limit=10))  # 获取一个gz的Sg的Uuid
        self.assertEqual(listSgResp.error.errno, 0)
        self.assertTrue(len(listSgResp.data) > 0)
        lisgSgRuleResp = cli.sgStub.ListSgRule(c.ListSgRuleRequest(header=c.Header(regionId='gz'),
                                                                   start=0, limit=10,
                                               condition=c.ListSgRuleCondition(
                                                   sgUuid=listSgResp.data[0].sgUuid)))
        self.assertEqual(lisgSgRuleResp.error.errno, 0)
        self.assertTrue(len(lisgSgRuleResp.data) > 0)
        deleteSgRuleReq = c.DeleteSgRuleRequest(header=c.Header(regionId='gz'))
        sgToDelete = deleteSgRuleReq.sgRule.add()
        sgToDelete.sgRuleUuid = lisgSgRuleResp.data[0].sgRuleUuid
        deleteSgRuleResp = cli.sgStub.DeleteSgRule(deleteSgRuleReq)
        print(deleteSgRuleResp)
        self.assertEqual(deleteSgRuleResp.error.errno, 0)
        print("deleteSgRule, jobUuid:", deleteSgRuleResp.data[0].jobUuid)
        success = cli.wait_for_job_result('gz', deleteSgRuleResp.data[0].jobUuid)  # 轮询等待结果
        print("deleteSgRule, success:", success)
        self.assertTrue(success)

    def test_10_delete_sg(self):
        print("================Begin Test Delete Sg================")
        listSgResp = cli.sgStub.ListSg(c.ListSgRequest(header=c.Header(regionId='gz'),
                                                       start=0, limit=10))  # 获取一个gz的Sg的Uuid
        self.assertEqual(listSgResp.error.errno, 0)
        self.assertTrue(len(listSgResp.data) > 0)
        deleteSgReq = c.DeleteSgRequest(header=c.Header(regionId='gz'))
        sgToDelete = deleteSgReq.sg.add()
        sgToDelete.sgUuid = listSgResp.data[0].sgUuid
        deleteSgResp = cli.sgStub.DeleteSg(deleteSgReq)
        print(deleteSgResp)
        self.assertEqual(deleteSgResp.error.errno, 0)
        print("deleteSg, jobUuid:", deleteSgResp.data[0].jobUuid)
        success = cli.wait_for_job_result('gz', deleteSgResp.data[0].jobUuid)  # 轮询等待结果
        print("deleteSg, success:", success)
        self.assertTrue(success)


if __name__ == '__main__':
    unittest.main()

