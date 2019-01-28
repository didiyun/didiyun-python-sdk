# coding: utf-8

from __future__ import print_function
import unittest
import tests.common.client
import tests.common as c

cli = tests.common.client.DicloudClient()


def hex_to_str(s):
    return ''.join([chr(i) for i in [int(b, 16) for b in s.split(' ')]])


def str_to_hex(s):
    return ''.join([hex(ord(c)).replace('0x', '') for c in s])


class TestDc2(unittest.TestCase):

    def test_01_list_image(self):
        print("================Begin Test List Image================")
        # 获取镜像
        imgResp = cli.dc2Stub.ListImage(c.ListImageRequest(header=c.Header(regionId='gz')))
        print(imgResp)
        self.assertEqual(imgResp.error.errno, 0)

    def test_02_create_dc2(self):
        print("================Begin Test Create Dc2================")
        # 获取镜像并选择
        imgResp = cli.dc2Stub.ListImage(c.ListImageRequest(header=c.Header(regionId='gz')))
        self.assertEqual(imgResp.error.errno, 0)
        for img in imgResp.data:
            if img.osFamily == 'CentOS' and img.osVersion == '7.5':
                targetImgUuid = img.imgUuid
                break

        self.assertNotEqual(len(targetImgUuid), 0)
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
        print(createDc2Resp)
        self.assertEqual(createDc2Resp.error.errno, 0)
        print("createDc2, jobUuid:", createDc2Resp.data[0].jobUuid)
        success = cli.wait_for_job_result(createDc2Resp.data[0].jobUuid)    # 轮询等待结果
        print("createDc2, success:",success)
        self.assertTrue(success)

    def test_03_list_dc2(self):
        print("================Begin Test List Dc2================")
        listResp = cli.dc2Stub.ListDc2(c.ListDc2Request(header=c.Header(regionId='gz'), start=0, limit=10))
        print(listResp)
        self.assertEqual(listResp.error.errno, 0)
        self.assertTrue(len(listResp.data) > 0)

    def test_04_get_dc2_total_cnt(self):
        print("================Begin Test Get Dc2 Total Cnt================")
        cntResp = cli.dc2Stub.GetDc2TotalCnt(c.GetDc2TotalCntRequest(header=c.Header(regionId='gz')))
        print(cntResp)
        self.assertEqual(cntResp.error.errno, 0)
        self.assertTrue(cntResp.data[0].totalCnt > 0)

    def test_05_get_dc2_by_uuid(self):
        print("================Begin Test Get Dc2 By Uuid================")
        listResp = cli.dc2Stub.ListDc2(c.ListDc2Request(header=c.Header(regionId='gz'),
                                                        start=0, limit=10))   # 获取一个DC2的Uuid
        self.assertEqual(listResp.error.errno, 0)
        self.assertTrue(len(listResp.data) > 0)
        getDc2ByUuidResp = cli.dc2Stub.GetDc2ByUuid(c.GetDc2ByUuidRequest(header=c.Header(regionId='gz'),
                                                                          dc2Uuid=listResp.data[0].dc2Uuid))
        print(getDc2ByUuidResp)
        self.assertEqual(getDc2ByUuidResp.error.errno, 0)
        self.assertTrue(len(getDc2ByUuidResp.data) > 0)

    def test_06_stop_dc2(self):
        print("================Begin Test Stop Dc2================")
        listResp = cli.dc2Stub.ListDc2(c.ListDc2Request(header=c.Header(regionId='gz'),
                                                        start=0, limit=10))  # 获取一个DC2的Uuid
        self.assertEqual(listResp.error.errno, 0)
        self.assertTrue(len(listResp.data) > 0)
        stopDc2Request = c.StopDc2Request(header=c.Header(regionId='gz'))
        dc2ToStop = stopDc2Request.dc2.add()    # 添加一个待操作的dc2
        dc2ToStop.dc2Uuid = listResp.data[0].dc2Uuid
        stopDc2Resp = cli.dc2Stub.StopDc2(stopDc2Request)
        print(stopDc2Resp)
        self.assertEqual(stopDc2Resp.error.errno, 0)
        print("stopDc2, jobUuid:", stopDc2Resp.data[0].jobUuid)
        success = cli.wait_for_job_result(stopDc2Resp.data[0].jobUuid)  # 轮询等待结果
        print("stopDc2, success:", success)
        self.assertTrue(success)

    def test_07_start_dc2(self):
        print("================Begin Test Start Dc2================")
        listResp = cli.dc2Stub.ListDc2(c.ListDc2Request(header=c.Header(regionId='gz'),
                                                        start=0, limit=10))     # 获取一个DC2的Uuid
        self.assertEqual(listResp.error.errno, 0)
        self.assertTrue(len(listResp.data) > 0)
        startDc2Request = c.StartDc2Request(header=c.Header(regionId='gz'))
        dc2ToStart = startDc2Request.dc2.add()      # 添加一个待操作的dc2
        dc2ToStart.dc2Uuid = listResp.data[0].dc2Uuid
        startDc2Resp = cli.dc2Stub.StartDc2(startDc2Request)
        print(startDc2Resp)
        self.assertEqual(startDc2Resp.error.errno, 0)
        print("startDc2, jobUuid:", startDc2Resp.data[0].jobUuid)
        success = cli.wait_for_job_result(startDc2Resp.data[0].jobUuid)  # 轮询等待结果
        print("startDc2, success:", success)
        self.assertTrue(success)

    def test_08_reboot_dc2(self):
        print("================Begin Test Reboot Dc2================")
        listResp = cli.dc2Stub.ListDc2(c.ListDc2Request(header=c.Header(regionId='gz'),
                                                        start=0, limit=10))     # 获取一个DC2的Uuid
        self.assertEqual(listResp.error.errno, 0)
        self.assertTrue(len(listResp.data) > 0)
        rebootDc2Request = c.RebootDc2Request(header=c.Header(regionId='gz'))
        dc2ToReboot = rebootDc2Request.dc2.add()    # 添加一个待操作的dc2
        dc2ToReboot.dc2Uuid = listResp.data[0].dc2Uuid
        rebootDc2Resp = cli.dc2Stub.RebootDc2(rebootDc2Request)
        print(rebootDc2Resp)
        self.assertEqual(rebootDc2Resp.error.errno, 0)
        print("rebootDc2, jobUuid:", rebootDc2Resp.data[0].jobUuid)
        success = cli.wait_for_job_result(rebootDc2Resp.data[0].jobUuid)  # 轮询等待结果
        print("rebootDc2, success:", success)
        self.assertTrue(success)

    def test_09_change_dc2_name(self):
        print("================Begin Test Change Dc2 Name================")
        listResp = cli.dc2Stub.ListDc2(c.ListDc2Request(header=c.Header(regionId='gz'),
                                                        start=0, limit=10))  # 获取一个DC2的Uuid
        self.assertEqual(listResp.error.errno, 0)
        self.assertTrue(len(listResp.data) > 0)
        changeDc2NameRequest = c.ChangeDc2NameRequest(header=c.Header(regionId='gz'))
        dc2TochangeName = changeDc2NameRequest.dc2.add()    # 添加一个待操作的dc2
        dc2TochangeName.dc2Uuid = listResp.data[0].dc2Uuid
        dc2TochangeName.name = "newDc2Name"
        changeDc2NameResp = cli.dc2Stub.ChangeDc2Name(changeDc2NameRequest)
        print(changeDc2NameResp)
        self.assertEqual(changeDc2NameResp.error.errno, 0)
        print("changeDc2Name, jobUuid:", changeDc2NameResp.data[0].jobUuid)
        success = cli.wait_for_job_result(changeDc2NameResp.data[0].jobUuid)  # 轮询等待结果
        print("changeDc2Name, success:", success)
        self.assertTrue(success)

    def test_10_change_dc2_password(self):
        print("================Begin Test Change Dc2 Password================")
        listResp = cli.dc2Stub.ListDc2(c.ListDc2Request(header=c.Header(regionId='gz'),
                                                        start=0, limit=10))  # 获取一个DC2的Uuid
        self.assertEqual(listResp.error.errno, 0)
        self.assertTrue(len(listResp.data) > 0)
        changeDc2PasswordRequest = c.ChangeDc2PasswordRequest(header=c.Header(regionId='gz'))
        dc2ToChangePassword = changeDc2PasswordRequest.dc2.add()    # 添加一个待操作的dc2
        dc2ToChangePassword.dc2Uuid = listResp.data[0].dc2Uuid
        dc2ToChangePassword.password = str_to_hex("newDc2Password123")
        changeDc2PasswordResp = cli.dc2Stub.ChangeDc2Password(changeDc2PasswordRequest)
        print(changeDc2PasswordResp)
        self.assertEqual(changeDc2PasswordResp.error.errno, 0)
        print("changeDc2Password, jobUuid:", changeDc2PasswordResp.data[0].jobUuid)
        success = cli.wait_for_job_result(changeDc2PasswordResp.data[0].jobUuid)  # 轮询等待结果
        print("changeDc2Password, success:", success)
        self.assertTrue(success)

    def test_11_reinstall_dc2_system(self):
        print("================Begin Test Reinstall Dc2 System================")
        # 获取镜像并选择
        imgResp = cli.dc2Stub.ListImage(c.ListImageRequest(header=c.Header(regionId='gz')))
        self.assertEqual(imgResp.error.errno, 0)
        for img in imgResp.data:
            if img.osFamily == 'CentOS' and img.osVersion == '7.4':
                targetImgUuid = img.imgUuid
                break
        self.assertNotEqual(len(targetImgUuid), 0)
        listResp = cli.dc2Stub.ListDc2(c.ListDc2Request(header=c.Header(regionId='gz'),
                                                        start=0, limit=10))  # 获取一个DC2的Uuid
        self.assertEqual(listResp.error.errno, 0)
        self.assertTrue(len(listResp.data) > 0)
        reinstallDc2SystemRequest = c.ReinstallDc2SystemRequest(header=c.Header(regionId='gz'))
        dc2ToReinstallSystem = reinstallDc2SystemRequest.dc2.add()
        dc2ToReinstallSystem.dc2Uuid = listResp.data[0].dc2Uuid
        dc2ToReinstallSystem.imgUuid = targetImgUuid
        dc2ToReinstallSystem.password = str_to_hex("newDc2Password123")
        reinstallDc2SystemResp = cli.dc2Stub.ReinstallDc2System(reinstallDc2SystemRequest)
        print(reinstallDc2SystemResp)
        self.assertEqual(reinstallDc2SystemResp.error.errno, 0)
        print("reinstallDc2System, jobUuid:", reinstallDc2SystemResp.data[0].jobUuid)
        success = cli.wait_for_job_result(reinstallDc2SystemResp.data[0].jobUuid)  # 轮询等待结果
        print("reinstallDc2System, success:", success)
        self.assertTrue(success)

    def test_12_change_dc2_spec(self):
        print("================Begin Test Change Dc2 Spec================")
        listResp = cli.dc2Stub.ListDc2(c.ListDc2Request(header=c.Header(regionId='gz'),
                                                        start=0, limit=10))  # 获取一个DC2的Uuid
        self.assertEqual(listResp.error.errno, 0)
        self.assertTrue(len(listResp.data) > 0)
        changeDcSpecRequest = c.ChangeDc2SpecRequest(header=c.Header(regionId='gz'))
        dc2ToChangeSpec = changeDcSpecRequest.dc2.add()
        dc2ToChangeSpec.dc2Uuid = listResp.data[0].dc2Uuid
        dc2ToChangeSpec.dc2Model = "dc2.s1.small2.d40"
        changeDcSpecResp = cli.dc2Stub.ChangeDc2Spec(changeDcSpecRequest)
        print(changeDcSpecResp)
        self.assertEqual(changeDcSpecResp.error.errno, 0)
        print("changeDc2Spec, jobUuid:", changeDcSpecResp.data[0].jobUuid)
        success = cli.wait_for_job_result(changeDcSpecResp.data[0].jobUuid)  # 轮询等待结果
        print("changeDc2Spec, success:", success)
        self.assertTrue(success)

    def test_13_create_ssh_key(self):
        print("================Begin Test Create SSH Key================")
        createResp = cli.dc2Stub.CreateSshKey(c.CreateSshKeyRequest(header=c.Header(regionId='gz'),
                                                                       name='testCreateSshKey',
                                                                       key='ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDLPkD03IMvLLWMCO1R3M8xEIcePWj9MPKpFh/dOuraLWnP9tBNIgtEjFXHzomO1i72z8dwEpBy+Xk15RWoMV+C8F4eR9fUpl75On433ji4mLVfIGxDb4CYhWeT0O4KG7fkr4GU6266DBxHVX0HiykNjxHCjO5+fCJ6eeeHVPqfEDO+ZLXE92mxMbdb647wjrTIg94E4sJ6LhRmqHml/W8gS+L0TCcbhNbhyp71hsYrDM/2NTLeU7ehZrhUYNoTxgcHtLI24QT5W+vYLvWTasv0dTsK/CHMlewwjFEJJuhQ9LTSjffPB19xEMgc265a7TolBWEja8L+1VgqhHH3lh35 renlixiang@didichuxing.com'))
        print(createResp)
        self.assertEqual(createResp.error.errno, 0)

    def test_14_list_ssh_key(self):
        print("================Begin Test List SSH Key================")
        listResp = cli.dc2Stub.ListSshKey(c.ListSshKeyRequest(header=c.Header(regionId='gz')))
        print(listResp)
        self.assertEqual(listResp.error.errno, 0)
        self.assertTrue(len(listResp.data) > 0)

    def test_15_delete_ssh_key(self):
        print("================Begin Test Delete SSH Key================")
        listResp = cli.dc2Stub.ListSshKey(c.ListSshKeyRequest(header=c.Header(regionId='gz')))
        self.assertEqual(listResp.error.errno, 0)
        self.assertTrue(len(listResp.data) > 0)     # 获取一个sshKey

        deleteResp = cli.dc2Stub.DeleteSshKey(c.DeleteSshKeyRequest(header=c.Header(regionId='gz'),
                                                                    pubKeyUuid=listResp.data[0].pubKeyUuid))
        print(deleteResp)
        self.assertEqual(deleteResp.error.errno, 0)

    def test_16_destroy_dc2(self):
        print("================Begin Test Delete Dc2================")
        listResp = cli.dc2Stub.ListDc2(c.ListDc2Request(header=c.Header(regionId='gz'),
                                                        start=0, limit=10))  # 获取一个DC2的Uuid
        self.assertEqual(listResp.error.errno, 0)
        self.assertTrue(len(listResp.data) > 0)
        destroyDc2Request = c.DestroyDc2Request(header=c.Header(regionId='gz'),
                                                deleteEip=True, deleteEbs=True, ignoreSlb=True)  # 同时删除Eip，Ebs，忽略DC2上绑定的Slb
        dc2ToDetroy = destroyDc2Request.dc2.add()
        dc2ToDetroy.dc2Uuid = listResp.data[0].dc2Uuid
        destroyDc2Response = cli.dc2Stub.DestroyDc2(destroyDc2Request)
        print(destroyDc2Response)
        self.assertEqual(destroyDc2Response.error.errno, 0)
        print("destroyDc2, jobUuid:", destroyDc2Response.data[0].jobUuid)
        success = cli.wait_for_job_result(destroyDc2Response.data[0].jobUuid)  # 轮询等待结果
        print("destroyDc2, success:", success)
        self.assertTrue(success)


if __name__ == '__main__':
    unittest.main()
