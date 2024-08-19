import concurrent.futures
import os

import openai
import pandas as pd
from PyQt6.QtCore import QThread, pyqtSignal


class WorkerThread(QThread):
    update_progress = pyqtSignal(int)
    update_status = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, file_path, api_key, base_url, model_name, table_name, set_batch_size, concurrency, labels):
        super().__init__()
        self.file_path = file_path
        self.api_key = api_key
        self.base_url = base_url
        self.model_name = model_name
        self.table_name = table_name
        self.labels = labels
        self.set_batch_size = int(set_batch_size)
        self.concurrency = int(concurrency)
        self.error = False
        self._is_running = True

    def run(self):
        try:
            openai.api_base = self.base_url
            openai.api_key = self.api_key

            client = openai.OpenAI(
                api_key=openai.api_key,
                base_url=openai.api_base
            )

            self.update_status.emit(f"等待API返回中…首批数据返回一般在30s内")

            def get_categories_batch(batch, batch_index):
                if not self._is_running:
                    return batch_index, []

                prompt = "请从上述标签中，为以下商品选择最合适的1个。每个商品名称后接1个$，再给出1个标签。即商品名与标签之间用$分隔。如 Iphone 15$手机\n大益普洱茶$茶叶\n\n每个商品占一行。\n\n"
                for item in batch:
                    prompt += f"{item}\n"

                response = client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system",
                         "content": f"你是一个专业的商品分类助手。根据商品名称，你可以准确地选择分类标签。分类标签如下：{self.labels}"},
                        {"role": "user", "content": prompt}
                    ]
                )
                result = response.choices[0].message.content.strip()
                self.update_status.emit(f"模型返回结果:\n{result}\n")

                lines = result.split('\n')
                batch_categories = []
                for line in lines:
                    if '$' in line:
                        category = line.split('$')[1].strip()
                        batch_categories.append(category)

                if len(batch_categories) != len(batch):
                    self.update_status.emit(
                        f"<span style='color: red;'>警告：生成的分类数量 ({len(batch_categories)}) 与批次大小 ({len(batch)}) 不匹配，请仔细检查！</span>")
                    self.error = True
                    batch_categories.extend([''] * (len(batch) - len(batch_categories)))
                    batch_categories = batch_categories[:len(batch)]

                return batch_index, batch_categories

            def process_batches(item_names):
                categories = [None] * len(item_names)
                with concurrent.futures.ThreadPoolExecutor(max_workers=self.concurrency) as executor:
                    futures = []
                    for i in range(0, len(item_names), self.set_batch_size):
                        if not self._is_running:
                            break
                        batch = item_names[i:i + self.set_batch_size]
                        futures.append(executor.submit(get_categories_batch, batch, i))

                    for i, future in enumerate(concurrent.futures.as_completed(futures)):
                        if not self._is_running:
                            break
                        batch_index, batch_categories = future.result()
                        categories[batch_index:batch_index + len(batch_categories)] = batch_categories
                        self.update_progress.emit(min((i + 1) * 100 // len(futures), 100))
                        self.update_status.emit(f"已处理 {i + 1} / {len(futures)} 批次")

                return categories

            df = pd.read_excel(self.file_path)

            item_names = df[self.table_name].dropna().tolist()

            categories = process_batches(item_names)

            if len(categories) != len(df):
                self.update_status.emit(f"警告：生成的分类数量 ({len(categories)}) 与数据框行数 ({len(df)}) 不匹配")
                categories.extend([''] * (len(df) - len(categories)))
                categories = categories[:len(df)]

            df['分类标签'] = categories

            output_file = os.path.join(os.path.dirname(self.file_path), "categorized_items_batch.xlsx")
            df.to_excel(output_file, index=False)

            if self.error:
                self.update_status.emit(f"\n部分结果异常，请仔细检查生成的文件！\n")
            self.update_status.emit(f"数据处理完成，结果已保存到 {output_file}")
            self.finished.emit()

        except Exception as e:
            self.update_status.emit(f"发生错误: {str(e)}")
            self.finished.emit()

    def stop(self):
        self._is_running = False
