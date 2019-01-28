# coding: utf-8

from __future__ import print_function
import unittest
import tests.common.client
import tests.common as c

cli = tests.common.client.DicloudClient()


class TestSnap(unittest.TestCase):
    """在有一个gz的DC2的情况下，才可运行此test"""
    def test_01_create_snap(self):
        print("================Begin Test Create Snap================")
        listDc2Resp = cli.dc2Stub.ListDc2(c.ListDc2Request(header=c.Header(regionId='gz'),
                                                           start=0, limit=10))  # 获取一个gz的DC2的Uuid
        self.assertEqual(listDc2Resp.error.errno, 0)
        self.assertTrue(len(listDc2Resp.data) > 0)
        createSnapReq = c.CreateSnapshotRequest(header=c.Header(regionId='gz'),
                                                dc2Uuid=listDc2Resp.data[0].dc2Uuid, snapName='testSnap')   # 给DC2打快照
        createSnapResp = cli.snapStub.CreateSnapshot(createSnapReq)
        print(createSnapResp)
        self.assertEqual(createSnapResp.error.errno, 0)
        print("createSnap, jobUuid:", createSnapResp.data[0].jobUuid)
        success = cli.wait_for_job_result('gz', createSnapResp.data[0].jobUuid)  # 轮询等待结果
        print("createSnap, success:", success)
        self.assertTrue(success)

    def test_02_list_snap(self):
        print("================Begin Test List Snap================")
        listResp = cli.snapStub.ListSnapshot(c.ListSnapshotRequest(header=c.Header(regionId='gz'), start=0, limit=10))
        print(listResp)
        self.assertEqual(listResp.error.errno, 0)
        self.assertTrue(len(listResp.data) > 0)

    def test_03_get_snap_total_cnt(self):
        print("================Begin Test Get Snap Total Cnt================")
        cntResp = cli.snapStub.GetSnapshotTotalCnt(c.GetSnapshotTotalCntRequest(header=c.Header(regionId='gz')))
        print(cntResp)
        self.assertEqual(cntResp.error.errno, 0)
        self.assertTrue(cntResp.data[0].totalCnt > 0)

    def test_04_revert_snap(self):
        print("================Begin Test Revert Snap================")
        listSnapResp = cli.snapStub.ListSnapshot(c.ListSnapshotRequest(header=c.Header(regionId='gz'),
                                                        start=0, limit=10))  # 获取一个gz的Snap的Uuid
        self.assertEqual(listSnapResp.error.errno, 0)
        self.assertTrue(len(listSnapResp.data) > 0)
        self.assertTrue(listSnapResp.data[0].canBeReverted)
        revertSnapReq = c.RevertSnapshotRequest(header=c.Header(regionId='gz'))
        snapToRevert = revertSnapReq.snap.add()
        snapToRevert.snapUuid = listSnapResp.data[0].snapUuid
        revertSnapResp = cli.snapStub.RevertSnapshot(revertSnapReq)
        print(revertSnapResp)
        self.assertEqual(revertSnapResp.error.errno, 0)
        print("revertSnap, jobUuid:", revertSnapResp.data[0].jobUuid)
        success = cli.wait_for_job_result('gz', revertSnapResp.data[0].jobUuid)  # 轮询等待结果
        print("revertSnap, success:", success)
        self.assertTrue(success)

    def test_05_change_snap_name(self):
        print("================Begin Test Detach Eip From Dc2================")
        listSnapResp = cli.snapStub.ListSnapshot(c.ListSnapshotRequest(header=c.Header(regionId='gz'),
                                                                       start=0, limit=10))  # 获取一个gz的Snap的Uuid
        self.assertEqual(listSnapResp.error.errno, 0)
        self.assertTrue(len(listSnapResp.data) > 0)
        changeSnapNameReq = c.ChangeSnapshotNameRequest(header=c.Header(regionId='gz'))
        snapToChangeName = changeSnapNameReq.snap.add()
        snapToChangeName.snapUuid = listSnapResp.data[0].snapUuid
        snapToChangeName.name = 'newSnapName'
        changeSnapNameResp = cli.snapStub.ChangeSnapshotName(changeSnapNameReq)
        print(changeSnapNameResp)
        self.assertEqual(changeSnapNameResp.error.errno, 0)
        print("changeSnapName, jobUuid:", changeSnapNameResp.data[0].jobUuid)
        success = cli.wait_for_job_result('gz', changeSnapNameResp.data[0].jobUuid)  # 轮询等待结果
        print("changeSnapName, success:", success)
        self.assertTrue(success)

    def test_06_delete_snap(self):
        print("================Begin Test Delete Snap================")
        listSnapResp = cli.snapStub.ListSnapshot(c.ListSnapshotRequest(header=c.Header(regionId='gz'),
                                                                       start=0, limit=10))  # 获取一个gz的Snap的Uuid
        self.assertEqual(listSnapResp.error.errno, 0)
        self.assertTrue(len(listSnapResp.data) > 0)
        deleteSnapReq = c.DeleteSnapshotRequest(header=c.Header(regionId='gz'))
        snapToDelete = deleteSnapReq.snap.add()
        snapToDelete.snapUuid = listSnapResp.data[0].snapUuid
        deleteSnapResp = cli.snapStub.DeleteSnapshot(deleteSnapReq)
        print(deleteSnapResp)
        self.assertEqual(deleteSnapResp.error.errno, 0)
        print("deleteSnap, jobUuid:", deleteSnapResp.data[0].jobUuid)
        success = cli.wait_for_job_result('gz', deleteSnapResp.data[0].jobUuid)  # 轮询等待结果
        print("deleteSnap, success:", success)
        self.assertTrue(success)


if __name__ == '__main__':
    unittest.main()

