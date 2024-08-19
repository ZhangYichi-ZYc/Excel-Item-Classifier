import tempfile
import unittest

import pandas as pd

from src.worker import WorkerThread


class TestWorkerThread(unittest.TestCase):

    def setUp(self):
        # 创建临时Excel文件
        self.test_file = tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False)
        df = pd.DataFrame({
            '物料名称': ['商品1', '商品2', '商品3']
        })
        df.to_excel(self.test_file.name, index=False)
        self.test_file.close()

        self.worker = WorkerThread(
            file_path=self.test_file.name,
            api_key="test_api_key",
            base_url="https://api.example.com",
            model_name="test_model",
            table_name="物料名称",
            set_batch_size=2,
            concurrency=2,
            labels="标签1,标签2,标签3"
        )

    def tearDown(self):
        os.remove(self.test_file.name)

    def test_run(self):
        self.worker.run()
        # 检查生成的文件
        output_file = os.path.join(os.path.dirname(self.test_file.name), "categorized_items_batch.xlsx")
        self.assertTrue(os.path.exists(output_file))
        df = pd.read_excel(output_file)
        self.assertIn('分类标签', df.columns)


if __name__ == '__main__':
    unittest.main()
