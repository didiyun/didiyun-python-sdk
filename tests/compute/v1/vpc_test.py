# coding: utf-8

from __future__ import print_function
import unittest
import tests.common.client
import tests.common as c

cli = tests.common.client.DicloudClient()


class TestVpc(unittest.TestCase):

    def test_01_create_vpc(self):
        print("================Begin Test Create Vpc================")
        createVpcResp = cli.vpcStub.CreateVpc(c.CreateVpcRequest(header=c.Header(regionId='gz'),
                                                           name='testCreateVpc', cidr='172.16.0.0/12'))
        self.assertEqual(createVpcResp.error.errno, 0)
        print("createVpc, jobUuid:", createVpcResp.data[0].jobUuid)
        success = cli.wait_for_job_result('gz', createVpcResp.data[0].jobUuid)  # 轮询等待结果
        print("createVpc, success:", success)
        self.assertTrue(success)

    def test_02_create_subnet(self):
        print("================Begin Test Create Subnet================")
        listVpcResp = cli.vpcStub.ListVpc(c.ListVpcRequest(header=c.Header(regionId='gz'), start=0, limit=10))
        self.assertEqual(listVpcResp.error.errno, 0)
        self.assertTrue(len(listVpcResp.data) > 0)
        for vpc in listVpcResp.data:        # 选中刚才创建的VPC
            if vpc.name == 'testCreateVpc':
                vpcToCreate = vpc.vpcUuid
                break
        self.assertIsNotNone(vpcToCreate)
        createSubnetReq = c.CreateSubnetRequest(header=c.Header(regionId='gz'), vpcUuid=vpcToCreate)
        subnetToCreate = createSubnetReq.subnet.add()
        subnetToCreate.name='testCreateSubnet'
        subnetToCreate.cidr='172.16.0.0/16'
        subnetToCreate.zoneId='gz02'
        createSubnetResp = cli.vpcStub.CreateSubnet(createSubnetReq)
        self.assertEqual(createSubnetResp.error.errno, 0)
        print("createSubnet, jobUuid:", createSubnetResp.data[0].jobUuid)
        success = cli.wait_for_job_result('gz', createSubnetResp.data[0].jobUuid)  # 轮询等待结果
        print("createSubnet, success:", success)
        self.assertTrue(success)

    def test_03_list_vpc(self):
        print("================Begin Test List Vpc================")
        listResp = cli.vpcStub.ListVpc(c.ListVpcRequest(header=c.Header(regionId='gz'), start=0, limit=10))
        print(listResp)
        self.assertEqual(listResp.error.errno, 0)
        self.assertTrue(len(listResp.data) > 0)

    def test_04_get_vpc_total_cnt(self):
        print("================Begin Test Get Vpc Total Cnt================")
        cntResp = cli.vpcStub.GetVpcTotalCnt(c.GetVpcTotalCntRequest(header=c.Header(regionId='gz')))
        print(cntResp)
        self.assertEqual(cntResp.error.errno, 0)
        self.assertTrue(cntResp.data[0].totalCnt > 0)

    def test_05_list_subnet(self):
        print("================Begin Test List Subnet================")
        listVpcResp = cli.vpcStub.ListVpc(c.ListVpcRequest(header=c.Header(regionId='gz'), start=0, limit=10))
        print(listVpcResp)
        self.assertEqual(listVpcResp.error.errno, 0)
        self.assertTrue(len(listVpcResp.data) > 0)
        listSubnetResp = cli.vpcStub.ListSubnet(c.ListSubnetRequest(header=c.Header(regionId='gz'), start=0, limit=10,
                                                                    condition=c.ListSubnetCondition(vpcUuid=listVpcResp.data[0].vpcUuid)))
        print(listSubnetResp)
        self.assertEqual(listSubnetResp.error.errno, 0)
        self.assertTrue(len(listSubnetResp.data) > 0)

    def test_06_get_subnet_total_cnt(self):
        print("================Begin Test Get Subnet Total Cnt================")
        listVpcResp = cli.vpcStub.ListVpc(c.ListVpcRequest(header=c.Header(regionId='gz'), start=0, limit=10))
        print(listVpcResp)
        self.assertEqual(listVpcResp.error.errno, 0)
        self.assertTrue(len(listVpcResp.data) > 0)
        cntResp = cli.vpcStub.GetVpcTotalCnt(c.GetSubnetTotalCntRequest(header=c.Header(regionId='gz'),
                                                                        vpcUuid=listVpcResp.data[0].vpcUuid))
        print(cntResp)
        self.assertEqual(cntResp.error.errno, 0)
        self.assertTrue(cntResp.data[0].totalCnt > 0)

    def test_07_change_vpc_name(self):
        print("================Begin Test Change Vpc Name================")
        listVpcResp = cli.vpcStub.ListVpc(c.ListVpcRequest(header=c.Header(regionId='gz'), start=0, limit=10))
        self.assertEqual(listVpcResp.error.errno, 0)
        self.assertTrue(len(listVpcResp.data) > 0)
        for vpc in listVpcResp.data:  # 选中刚才创建的VPC
            if vpc.name == 'testCreateVpc':
                vpcToChangeUuid = vpc.vpcUuid
                break
        self.assertIsNotNone(vpcToChangeUuid)
        changeVpcNameReq = c.ChangeVpcNameRequest(header=c.Header(regionId='gz'))
        vpcToChangeName = changeVpcNameReq.vpc.add()
        vpcToChangeName.vpcUuid=vpcToChangeUuid
        vpcToChangeName.name = 'testChangeVpcName'

        changeVpcNameResp = cli.vpcStub.ChangeVpcName(changeVpcNameReq)
        print(changeVpcNameResp)
        self.assertEqual(changeVpcNameResp.error.errno, 0)
        print("changeVpcName, jobUuid:", changeVpcNameResp.data[0].jobUuid)
        success = cli.wait_for_job_result('gz', changeVpcNameResp.data[0].jobUuid)  # 轮询等待结果
        print("changeVpcName, success:", success)
        self.assertTrue(success)

    def test_08_change_subnet_name(self):
        print("================Begin Test Delete Snap================")
        listVpcResp = cli.vpcStub.ListVpc(c.ListVpcRequest(header=c.Header(regionId='gz'), start=0, limit=10))
        self.assertEqual(listVpcResp.error.errno, 0)
        self.assertTrue(len(listVpcResp.data) > 0)
        for vpc in listVpcResp.data:  # 选中刚才创建的VPC
            if vpc.name == 'testChangeVpcName':
                vpcToChangeUuid = vpc.vpcUuid
                break
        self.assertIsNotNone(vpcToChangeUuid)
        listSubnetResp = cli.vpcStub.ListSubnet(c.ListSubnetRequest(header=c.Header(regionId='gz'), start=0, limit=10,
                                                                    condition=c.ListSubnetCondition(
                                                                        vpcUuid=vpcToChangeUuid)))
        print(listSubnetResp)
        self.assertEqual(listSubnetResp.error.errno, 0)
        self.assertTrue(len(listSubnetResp.data) > 0)
        changeSubnetNameReq = c.ChangeSubnetNameRequest(header=c.Header(regionId='gz'),vpcUuid=vpcToChangeUuid)
        subnetToChangeName = changeSubnetNameReq.subnet.add()
        subnetToChangeName.subnetUuid = listSubnetResp.data[0].subnetUuid
        subnetToChangeName.name = 'testChangeSubnetName'
        changeSubnetNameResp = cli.vpcStub.ChangeSubnetName(changeSubnetNameReq)
        print(changeSubnetNameResp)
        self.assertEqual(changeSubnetNameResp.error.errno, 0)
        print("changeSubnetName, jobUuid:", changeSubnetNameResp.data[0].jobUuid)
        success = cli.wait_for_job_result('gz', changeSubnetNameResp.data[0].jobUuid)  # 轮询等待结果
        print("changeSubnetName, success:", success)
        self.assertTrue(success)

    def test_09_list_vpc_available_cidr(self):
        print("================Begin Test List Vpc Available Cidr================")
        listResp = cli.vpcStub.ListVpcAvailableCidr(c.ListVpcAvailableCidrRequest(header=c.Header(regionId='gz')))
        self.assertEqual(listResp.error.errno, 0)
        self.assertTrue(len(listResp.data) > 0)

    def test_10_check_subnet_cidr_overlap(self):
        print("================Begin Test Check Subnet Cidr Overlap================")
        listVpcResp = cli.vpcStub.ListVpc(c.ListVpcRequest(header=c.Header(regionId='gz'), start=0, limit=10))
        self.assertEqual(listVpcResp.error.errno, 0)
        self.assertTrue(len(listVpcResp.data) > 0)
        for vpc in listVpcResp.data:  # 选中刚才创建的VPC
            if vpc.name == 'testChangeVpcName':
                vpcToCheckUuid = vpc.vpcUuid
                break
        self.assertIsNotNone(vpcToCheckUuid)
        checkSubnetOverlapResp = cli.vpcStub.CheckSubnetCidrOverlap(c.CheckSubnetCidrOverlapRequest(header=c.Header(regionId='gz'),
                                                                       vpcUuid=vpcToCheckUuid,cidr='172.16.0.0/16'))
        self.assertEqual(checkSubnetOverlapResp.error.errno, 0)
        self.assertTrue(len(checkSubnetOverlapResp.data) > 0)

    def test_11_delete_subnet(self):
        print("================Begin Test Delete Subnet================")
        listVpcResp = cli.vpcStub.ListVpc(c.ListVpcRequest(header=c.Header(regionId='gz'), start=0, limit=10))
        self.assertEqual(listVpcResp.error.errno, 0)
        self.assertTrue(len(listVpcResp.data) > 0)
        for vpc in listVpcResp.data:  # 选中刚才创建的VPC
            if vpc.name == 'testChangeVpcName':
                vpcToCheckDelete = vpc.vpcUuid
                break
        self.assertIsNotNone(vpcToCheckDelete)
        listSubnetResp = cli.vpcStub.ListSubnet(c.ListSubnetRequest(header=c.Header(regionId='gz'), start=0, limit=10,
                                                                    condition=c.ListSubnetCondition(
                                                                        vpcUuid=vpcToCheckDelete)))
        self.assertEqual(listSubnetResp.error.errno, 0)
        self.assertTrue(len(listSubnetResp.data) > 0)
        deleteSubnetReq = c.DeleteSubnetRequest(header=c.Header(regionId='gz'),vpcUuid=vpcToCheckDelete)
        subnetToDelete = deleteSubnetReq.subnet.add()
        subnetToDelete.subnetUuid=listSubnetResp.data[0].subnetUuid
        deleteSubnetResp = cli.vpcStub.DeleteSubnet(deleteSubnetReq)
        print(deleteSubnetResp)
        self.assertEqual(deleteSubnetResp.error.errno, 0)
        print("deleteSubnet, jobUuid:", deleteSubnetResp.data[0].jobUuid)
        success = cli.wait_for_job_result('gz', deleteSubnetResp.data[0].jobUuid)  # 轮询等待结果
        print("deleteSubnet, success:", success)
        self.assertTrue(success)

    def test_12_delete_vpc(self):
        print("================Begin Test Delete Vpc================")
        listVpcResp = cli.vpcStub.ListVpc(c.ListVpcRequest(header=c.Header(regionId='gz'), start=0, limit=10))
        self.assertEqual(listVpcResp.error.errno, 0)
        self.assertTrue(len(listVpcResp.data) > 0)
        for vpc in listVpcResp.data:  # 选中刚才创建的VPC
            if vpc.name == 'testChangeVpcName':
                vpcToCheckDelete = vpc.vpcUuid
                break
        self.assertIsNotNone(vpcToCheckDelete)
        deleteVpcReq = c.DeleteVpcRequest(header=c.Header(regionId='gz'))
        vpcToDelete = deleteVpcReq.vpc.add()
        vpcToDelete.vpcUuid = listVpcResp.data[0].vpcUuid
        deleteVpcResp = cli.vpcStub.DeleteVpc(deleteVpcReq)
        print(deleteVpcResp)
        self.assertEqual(deleteVpcResp.error.errno, 0)
        print("deleteVpc, jobUuid:", deleteVpcResp.data[0].jobUuid)
        success = cli.wait_for_job_result('gz', deleteVpcResp.data[0].jobUuid)  # 轮询等待结果
        print("deleteVpc, success:", success)
        self.assertTrue(success)


if __name__ == '__main__':
    unittest.main()

