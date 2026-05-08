import unittest

from DataTypes.DirectoryContent import DirectoryContent, DirectoryContentFromGrcp
import robotcontrolapp_pb2


class DirectoryContentTest(unittest.TestCase):
    def test_init(self):
        dc = DirectoryContent()
        self.assertFalse(dc.success)
        self.assertEqual(dc.errorMessage, "")
        self.assertEqual(len(dc.entries), 0)

    def test_FromGrpc1(self):
        lfr = robotcontrolapp_pb2.ListFilesResponse()
        lfr.success = True
        lfr.error = "Foo"

        dc = DirectoryContentFromGrcp(lfr)
        self.assertTrue(dc.success)
        self.assertEqual(dc.errorMessage, "Foo")
        self.assertEqual(len(dc.entries), 0)

    def test_FromGrpc2(self):
        lfr = robotcontrolapp_pb2.ListFilesResponse()
        lfr.success = True
        lfr.error = "Bar"

        lfre1 = lfr.entries.add()
        lfre1.type = robotcontrolapp_pb2.ListFilesResponse.DirectoryEntry.Directory
        lfre1.name = "Dir1"

        lfre2 = lfr.entries.add()
        lfre2.type = robotcontrolapp_pb2.ListFilesResponse.DirectoryEntry.File
        lfre2.name = "File1"

        dc = DirectoryContentFromGrcp(lfr)
        self.assertTrue(dc.success)
        self.assertEqual(dc.errorMessage, "Bar")
        self.assertEqual(len(dc.entries), 2)

    def test_FromGrpc3(self):
        lfr = robotcontrolapp_pb2.ListFilesResponse()
        lfr.success = False
        lfr.error = "Baz"

        lfre1 = lfr.entries.add()
        lfre1.type = robotcontrolapp_pb2.ListFilesResponse.DirectoryEntry.Directory
        lfre1.name = "Dir1"

        lfre2 = lfr.entries.add()
        lfre2.type = robotcontrolapp_pb2.ListFilesResponse.DirectoryEntry.File
        lfre2.name = "File1"

        dc = DirectoryContentFromGrcp(lfr)
        self.assertFalse(dc.success)
        self.assertEqual(dc.errorMessage, "Baz")
        self.assertEqual(len(dc.entries), 2)


if __name__ == "__main__":
    unittest.main()
