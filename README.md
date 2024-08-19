# Excel Item Classifier

## 项目简介
一个自动标签分类工具，以OpenAI API格式调用第三方AI。

用户可以通过图形界面选择Excel文件，并配置相关参数，程序会将分类结果保存至新的Excel中。

## 安装与运行

### 环境依赖
Python 3.8及以上。

### 安装
1. 克隆本仓库：
    ```bash
    git clone https://gitcode.com/ZhangYichi-ZYc/Excel-Item-Classifier.git
    cd Excel-Item-Classifier
    ```

2. 安装依赖：
    ```bash
    pip install -r requirements.txt
    ```

### 运行
在项目根目录下运行以下命令启动程序：
```bash
python main.py
```

## 使用说明
1. 运行程序，选择待分类的Excel。
2. 根据需要输入API Key、Base URL、模型名称、待分类表头、分类标签、单批数量和并发批数。
3. 点击“开始处理”，进度条及输出窗口将实时呈现分类进度。
4. 分类完成后，结果将输出至与输入文件同目录下 `categorized_items_batch.xlsx`。

## 文件说明
- `main.py`：主程序入口，包含GUI界面。
- `src/`：包含核心功能模块。
  - `worker.py`：处理分类任务的工作线程。
  - `gui.py`：图形界面相关代码。
- `data/`：存放示例数据文件。
- `tests/`：包含单元测试。
- `docs/`：包含使用说明文档。

## 贡献
欢迎提交pull request或issue来改进本项目。

## 许可证
本项目使用 MIT 许可证。详细信息请参阅 LICENSE 文件。
