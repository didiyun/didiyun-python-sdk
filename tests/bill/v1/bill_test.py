# coding: utf-8

from __future__ import print_function
import unittest
import tests.common.client
import tests.common as c

cli = tests.common.client.DicloudClient()


class TestBill(unittest.TestCase):

    def test_01_get_charge_info_and_spec(self):
        print("================Begin Test Get Charge Info And Spec================")
        # DC2
        listDc2Resp = cli.dc2Stub.ListDc2(c.ListDc2Request(header=c.Header(regionId='gz'),
                                                           start=0, limit=10))  # 获取一个DC2的Uuid
        self.assertEqual(listDc2Resp.error.errno, 0)
        self.assertTrue(len(listDc2Resp.data) > 0)
        dc2Req = c.GetChargeInfoAndSpecRequest(header=c.Header(regionId='gz'))
        resource = dc2Req.resource.add()
        resource.resourceUuid = listDc2Resp.data[0].dc2Uuid
        getDc2ChargeInfoAndSpecResp = cli.billStub.GetDc2ChargeInfoAndSpec(dc2Req)
        self.assertEqual(getDc2ChargeInfoAndSpecResp.error.errno, 0)
        self.assertTrue(len(getDc2ChargeInfoAndSpecResp.data) > 0)

        # EIP
        listEipResp = cli.eipStub.ListEip(c.ListEipRequest(header=c.Header(regionId='gz'),
                                                           start=0, limit=10))  # 获取一个Eip的Uuid
        self.assertEqual(listEipResp.error.errno, 0)
        self.assertTrue(len(listEipResp.data) > 0)
        eipReq = c.GetChargeInfoAndSpecRequest(header=c.Header(regionId='gz'))
        resource = eipReq.resource.add()
        resource.resourceUuid = listEipResp.data[0].eipUuid
        getEipChargeInfoAndSpecResp = cli.billStub.GetEipChargeInfoAndSpec(eipReq)
        self.assertEqual(getEipChargeInfoAndSpecResp.error.errno, 0)
        self.assertTrue(len(getEipChargeInfoAndSpecResp.data) > 0)

        # EBS
        listEbsResp = cli.ebsStub.ListEbs(c.ListEbsRequest(header=c.Header(regionId='gz'),
                                                           start=0, limit=10))  # 获取一个Ebs的Uuid
        self.assertEqual(listEbsResp.error.errno, 0)
        self.assertTrue(len(listEbsResp.data) > 0)
        ebsReq = c.GetChargeInfoAndSpecRequest(header=c.Header(regionId='gz'))
        resource = ebsReq.resource.add()
        resource.resourceUuid = listEbsResp.data[0].ebsUuid
        getEbsChargeInfoAndSpecResp = cli.billStub.GetEbsChargeInfoAndSpec(ebsReq)
        self.assertEqual(getEbsChargeInfoAndSpecResp.error.errno, 0)
        self.assertTrue(len(getEbsChargeInfoAndSpecResp.data) > 0)

    def test_02_check_dc2_price(self):
        print("================Begin Test Check Dc2 Price================")
        # 创建
        checkPriceResp = cli.billStub.CheckDc2Price(c.CheckDc2PriceRequest(header=c.Header(regionId='gz'),
                                                                           dc2Goods=c.CheckDc2PriceInput(count=2,
                                                                               payPeriod=3,
                                                                               dc2Model='dc2.s1.small1.d20',
                                                                               eip=c.CheckEipPriceInput(bandwidth=5),
                                                                               ebs=c.CheckEbsPriceInput(count=2,
                                                                                                        size=50,
                                                                                                        diskType='SSD'))))
        print(checkPriceResp)
        self.assertEqual(checkPriceResp.error.errno, 0)
        # 升配
        listResp = cli.dc2Stub.ListDc2(c.ListDc2Request(header=c.Header(regionId='gz'),
                                                        start=0, limit=10))  # 获取一个DC2的Uuid
        self.assertEqual(listResp.error.errno, 0)
        self.assertTrue(len(listResp.data) > 0)
        checkChangePriceResp = cli.billStub.CheckDc2Price(c.CheckDc2PriceRequest(header=c.Header(regionId='gz'),
                                                                                 isChange=True,
                                                                                 dc2Goods=c.CheckDc2PriceInput(
                                                                                     dc2Uuid=listResp.data[0].dc2Uuid,
                                                                                     dc2Model='dc2.s1.large4.d40')))
        print(checkChangePriceResp)
        self.assertEqual(checkChangePriceResp.error.errno, 0)

    def test_03_check_eip_price(self):
        print("================Begin Test Check Eip Price================")
        # 创建
        checkPriceResp = cli.billStub.CheckEipPrice(c.CheckEipPriceRequest(header=c.Header(regionId='gz'),
                                                                           eipGoods=c.CheckEipPriceInput(count=2,
                                                                                                         payPeriod=3,
                                                                                                         bandwidth=5)))
        print(checkPriceResp)
        self.assertEqual(checkPriceResp.error.errno, 0)
        # 升配
        listResp = cli.eipStub.ListEip(c.ListEipRequest(header=c.Header(regionId='gz'),
                                                        start=0, limit=10))  # 获取一个Eip的Uuid
        self.assertEqual(listResp.error.errno, 0)
        self.assertTrue(len(listResp.data) > 0)
        checkChangePriceResp = cli.billStub.CheckEipPrice(c.CheckEipPriceRequest(header=c.Header(regionId='gz'),
                                                                                 isChange=True,
                                                                                 eipGoods=c.CheckEipPriceInput(
                                                                                     eipUuid=listResp.data[0].eipUuid,
                                                                                     bandwidth=10)))
        print(checkChangePriceResp)
        self.assertEqual(checkChangePriceResp.error.errno, 0)

    def test_04_check_ebs_price(self):
        print("================Begin Test Check Ebs Price================")
        # 创建
        checkPriceResp = cli.billStub.CheckEbsPrice(c.CheckEbsPriceRequest(header=c.Header(regionId='gz'),
                                                                           ebsGoods=c.CheckEbsPriceInput(count=2,
                                                                                                         payPeriod=3,
                                                                                                         size=20,
                                                                                                         diskType='SSD')))
        print(checkPriceResp)
        self.assertEqual(checkPriceResp.error.errno, 0)
        # 升配
        listResp = cli.ebsStub.ListEbs(c.ListEbsRequest(header=c.Header(regionId='gz'),
                                                        start=0, limit=10))  # 获取一个Ebs的Uuid
        self.assertEqual(listResp.error.errno, 0)
        self.assertTrue(len(listResp.data) > 0)
        checkChangePriceResp = cli.billStub.CheckEbsPrice(c.CheckEbsPriceRequest(header=c.Header(regionId='gz'),
                                                                                 isChange=True,
                                                                                 ebsGoods=c.CheckEbsPriceInput(
                                                                                     ebsUuid=listResp.data[0].eipUuid,
                                                                                     size=50)))
        print(checkChangePriceResp)
        self.assertEqual(checkChangePriceResp.error.errno, 0)
        self.assertTrue(len(checkChangePriceResp.data) > 0)

    def test_05_continue_list(self):
        print("================Begin Test Continue List================")
        listResp = cli.billStub.ContinueList(c.ContinueListRequest(header=c.Header(regionId='gz'),
                                                                  start=0, limit=10,
                                                                  condition=c.ContinueListCondition(
                                                                      startTime=1546272000000, # 筛选在此之后到期的资源
                                                                      endTime=1548950400000, # 筛选在此之前到期的资源
                                                                      resourceType='dc2',
                                                                      regionId='gz',
                                                                      autoRenewFilter='enabled' # 已开通自动续费的资源
                                                                  )))
        print(listResp)
        self.assertEqual(listResp.error.errno, 0)
        self.assertTrue(len(listResp.data) > 0)

    def test_06_change_to_monthly(self):
        print("================Begin Test Change To Monthly================")
        listResp = cli.dc2Stub.ListDc2(c.ListDc2Request(header=c.Header(regionId='gz'),
                                                        start=0, limit=10))  # 获取一个DC2的Uuid
        self.assertEqual(listResp.error.errno, 0)
        self.assertTrue(len(listResp.data) > 0)
        changeToMonthlyReq = c.ChangeToMonthlyRequest(header=c.Header(regionId='gz'),payPeriod=3)  # 转3个月包月
        resourceToChangeMonthly = changeToMonthlyReq.resource.add()    # 添加一个待操作的资源
        resourceToChangeMonthly.resourceUuid = listResp.data[0].dc2Uuid
        resourceToChangeMonthly.resourceType = 'dc2'
        changeToMonthlyResp = cli.billStub.ChangeToMonthly(changeToMonthlyReq)
        print(changeToMonthlyResp)
        self.assertEqual(changeToMonthlyResp.error.errno, 0)

    def test_07_continue_monthly(self):
        print("================Begin Test Get Dc2 By Uuid================")
        listResp = cli.dc2Stub.ListDc2(c.ListDc2Request(header=c.Header(regionId='gz'),
                                                        start=0, limit=10))  # 获取一个DC2的Uuid
        self.assertEqual(listResp.error.errno, 0)
        self.assertTrue(len(listResp.data) > 0)
        continueMonthlyReq = c.ContinueMonthlyRequest(header=c.Header(regionId='gz'), payPeriod=3)  # 续费3个月
        resourceToContinueMonthly = continueMonthlyReq.resource.add()    # 添加一个待操作的资源
        resourceToContinueMonthly.resourceUuid = listResp.data[0].dc2Uuid
        resourceToContinueMonthly.resourceType = 'dc2'
        continueMonthlyResp = cli.billStub.ContinueMonthly(continueMonthlyReq)
        print(continueMonthlyResp)
        self.assertEqual(continueMonthlyResp.error.errno, 0)

    def test_08_change_expire_strategy(self):
        print("================Begin Test Start Dc2================")
        listResp = cli.dc2Stub.ListDc2(c.ListDc2Request(header=c.Header(regionId='gz'),
                                                        start=0, limit=10))  # 获取一个DC2的Uuid
        self.assertEqual(listResp.error.errno, 0)
        self.assertTrue(len(listResp.data) > 0)
        changeExpireStrategyReq = c.ChangeExpireStrategyRequest(header=c.Header(regionId='gz'),
                                                                autoRenewCnt=2,
                                                                autoSwitch=True)  # 到期自动续费2个月，若余额不足以续费则自动转包月
        resourceToChangeStrategy = changeExpireStrategyReq.resource.add()    # 添加一个待操作的资源
        resourceToChangeStrategy.resourceUuid = listResp.data[0].dc2Uuid
        resourceToChangeStrategy.resourceType = 'dc2'
        changeExpireStrategyResp = cli.billStub.ChangeExpireStrategy(changeExpireStrategyReq)
        print(changeExpireStrategyResp)
        self.assertEqual(changeExpireStrategyResp.error.errno, 0)


if __name__ == '__main__':
    unittest.main()
