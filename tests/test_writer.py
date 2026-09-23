import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import unittest

from quilt_zai_writer.writer import write_essay, write_pack


class TestWriter(unittest.TestCase):

    def test_requires_zai(self):
        os.environ.pop("ZAI_TOKEN", None)
        with self.assertRaises(RuntimeError):
            write_essay("test topic")


class TestLiveWriter(unittest.TestCase):

    @unittest.skipUnless(os.environ.get("ZAI_TOKEN"), "ZAI_TOKEN not set")
    def test_write_one_essay(self):
        # Use a very short max_tokens to keep test fast
        result = write_essay("the substrate walker canon", max_tokens=300)
        print(f"\n  wrote {result['chars']} chars on topic: {result['topic']}")
        print(f"  preview: {result['essay'][:200]}...")


if __name__ == "__main__":
    unittest.main()
