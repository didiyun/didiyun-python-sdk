# coding: utf-8

from __future__ import print_function
import unittest
import tests.common.client
import tests.common as c

cli = tests.common.client.DicloudClient()

class TestCounter(unittest.TestCase):

    def test_01_list_counter(self):
        print("================Begin Test List Counter================")
        # 获取曲线信息
        listCounterReq = c.ListCounterRequest(header=c.Header(regionId='gz'))
        resource1 = listCounterReq.resource.add()
        resource1.resourceUuids.append('ec8d243a009c5c52b1fb44d358eeaf31')
        resource1.resourceType = 'dc2'
        resource1.metric.extend(['cpu.util', 'disk.write', 'disk.read'])
        resource2 = listCounterReq.resource.add()
        resource2.resourceUuids.append('057ae1c9855c5062a4078183d497c13b')
        resource2.resourceType = 'eip'
        resource2.metric.extend(['rxbytes', 'txbytes'])
        counterResp = cli.monitorStub.ListCounter(listCounterReq)
        print(counterResp)
        self.assertEqual(counterResp.error.errno, 0)

    def test_02_list_counter_data(self):
        print("================Begin Test List Counter Data================")
        # 获取曲线信息
        listCounterDataReq = c.ListCounterDataRequest(header=c.Header(regionId='gz'))
        counter1 = listCounterDataReq.counter.add()
        counter1.resourceType = 'dc2'
        counter1.resourceUuid = 'ec8d243a009c5c52b1fb44d358eeaf31'
        counter1.monitorTags = 'device=vda'
        counter1.metric = 'disk.write'
        counter1.startTime = 1560997040
        counter1.endTime = 1561000640
        counter2 = listCounterDataReq.counter.add()
        counter2.resourceType = 'dc2'
        counter2.resourceUuid = 'ec8d243a009c5c52b1fb44d358eeaf31'
        counter2.monitorTags = 'device=vda'
        counter2.metric = 'disk.write'
        counter2.startTime = 1560997040
        counter2.endTime = 1561000640
        counter3 = listCounterDataReq.counter.add()
        counter3.resourceType = 'eip'
        counter3.resourceUuid = '057ae1c9855c5062a4078183d497c13b'
        counter3.monitorTags = ''
        counter3.metric = 'rxbytes'
        counter3.startTime = 1560997040
        counter3.endTime = 1561000640
        counterDataResp = cli.monitorStub.ListCounterData(listCounterDataReq)
        print(counterDataResp)
        self.assertEqual(counterDataResp.error.errno, 0)

if __name__ == '__main__':
    unittest.main()
