from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QTextEdit, QFileDialog, QLabel, QProgressBar)

from src.worker import WorkerThread


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('商品分类助手')
        self.setGeometry(100, 100, 600, 600)
        self.setWindowIcon(QIcon('icon.png'))
        self.setStyleSheet("""
            QWidget {
                background-color: #010409;
                font-family: Arial, sans-serif;
            }
            QPushButton {
                background-color: #21262D;
                color: white;
                border: none;
                padding: 8px 16px;
                text-align: center;
                text-decoration: none;
                font-size: 14px;
                margin: 4px 2px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #292E36;
            }
            QLineEdit {
                padding: 8px;
                margin: 4px 2px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QTextEdit {
                border: 1px solid #ccc;
                border-radius: 4px;
            }
        """)

        main_layout = QVBoxLayout()

        # 文件选择
        file_layout = QHBoxLayout()
        self.file_path = QLineEdit()
        self.file_path.setPlaceholderText("选择Excel文件")
        file_button = QPushButton("选择文件")
        file_button.clicked.connect(self.select_file)
        file_layout.addWidget(self.file_path)
        file_layout.addWidget(file_button)
        main_layout.addLayout(file_layout)

        # API Key
        api_key_layout = QHBoxLayout()
        api_key_label = QLabel("   API Key：\t")
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("输入您的智谱AI API Key，或其他支持OpenAI-Like调用的API")
        api_key_layout.addWidget(api_key_label)
        api_key_layout.addWidget(self.api_key_input)
        main_layout.addLayout(api_key_layout)

        # Base URL
        base_url_layout = QHBoxLayout()
        base_url_label = QLabel("   Base URL：\t")
        self.base_url_input = QLineEdit()
        self.base_url_input.setText("https://open.bigmodel.cn/api/paas/v4/")
        self.base_url_input.setPlaceholderText("您可以修改模型请求地址，但服务商需支持OpenAI-Like调用")
        base_url_layout.addWidget(base_url_label)
        base_url_layout.addWidget(self.base_url_input)
        main_layout.addLayout(base_url_layout)

        # Model Name
        model_name_layout = QHBoxLayout()
        model_name_label = QLabel("   模型名称：\t")
        self.model_name_input = QLineEdit()
        self.model_name_input.setText("glm-4-air")
        self.model_name_input.setPlaceholderText("修改模型编码")
        model_name_layout.addWidget(model_name_label)
        model_name_layout.addWidget(self.model_name_input)
        main_layout.addLayout(model_name_layout)

        # 表头
        table_name_layout = QHBoxLayout()
        table_name_label = QLabel("   待分类表头：\t")
        self.table_name_input = QLineEdit()
        self.table_name_input.setText("物料名称")
        self.table_name_input.setPlaceholderText("输入待分类一列的表头")
        table_name_layout.addWidget(table_name_label)
        table_name_layout.addWidget(self.table_name_input)
        main_layout.addLayout(table_name_layout)

        # 标签
        labels_layout = QHBoxLayout()
        labels_label = QLabel("   分类标签：\t")
        self.labels_input = QLineEdit()
        self.labels_input.setText(
            "服务器、存储、服务器/存储配件、无线网络设备、负载均衡设备、有线网络设备、路由器、网络软件、光模块、网络线缆、网络服务、其他网络设备、通信设备、私有云、国内公有云、海外公有云、IDC租赁、UPS、精密空调、机房、专线租用、通信服务、工作站、笔记本、台式机、显示器、瘦客户机、移动终端（不含通讯终端如手机、电话等）、"
            "语音视频会议设备、其他计算机终端设备、传媒广电、工控机、工业设备、车载电脑、3D打印机、Andon系统、定制徽章、定制纪念章、地板、瓷砖、壁纸、石材、木材、乳胶漆、铝材、玻璃、生活家具、商业办公家具、儿童家具、电工电料、装饰材料、标识标牌（含广告灯箱、指示物料等）、门、窗、灯饰、卫浴洁具、水暖五金、厨房设备、"
            "电话机、传真机、打复扫设备、打卡机、碎纸机、文件管理用品、桌面办公用品、纸质办公用品、书写修正用品、财务用品、辅助办公用品、文化文教用品、会议文具、施印类、日用制冷（冰箱、冰柜、制冰机等）、空气及室温调节（含空调、加湿器、取暖器等）、厨房电器（不含商用的厨房设备，商用在基建工程处）、清洁电器、电器配件、"
            "手机、摄影摄像设备、摄影摄像附件、音视频播放器（含电视、投影、VR设备）、音视频附件、音频收放（含录音笔）、智能手表、服饰清洁养护用品、居室清洁用品、驱虫用品、清洁工具、生活用纸、水具酒具、餐具、厨房配件、烹饪锅具、茶具/咖啡具、刀剪菜板、五金工具、收纳用品、床上用品、家居饰品、居家布艺、地毯地垫、雨伞雨具、"
            "图书、刊物订阅、农资园艺、宠物生活、粮油速食、生鲜、酒水茶饮、休闲食品、滋补营养、贵金属首饰、宝石类首饰、其他材质类首饰、服装、鞋靴、箱包、户外服装装备、户外露营装备、户外出行工具、户外体育运动装备、体育娱乐用品、母婴用品、婴幼服饰、婴幼儿食品、婴童玩具、孕妈用品、早教教育产品、护肤品、彩妆香水、"
            "身体护理、口腔护理、美发洗护、女性护理、实体卡券、虚拟卡券、中式调料、西式调料、米、面粉、食用油、方便速食、速食烘焙、预制菜、南北干货、肉禽蛋奶、海鲜水产、新鲜蔬果、酒、水、乳制品、饮料、茶、冲调饮品、零食坚果、传统滋补、营养健康、安防监控、防盗报警、监控设备、交通安全设施、救生器材、门禁考勤、气体检测仪、"
            "生物识别技术设备、室内安全检测、消防设备、安全标识、安全检查、安全网、对讲设备、防爆器材、防静电产品、防雷电设备、化学品泄漏防护、自然灾害防护、头部防护用品、眼面防护用品、手部防护用品、足部防护用品、躯体防护用品、听力防护用品、呼吸防护用品、防护标识、坠落防护用品、放射性防护用品、触电防护用品、防毒防化用品")
        self.labels_input.setPlaceholderText("输入分类标签")
        labels_layout.addWidget(labels_label)
        labels_layout.addWidget(self.labels_input)
        main_layout.addLayout(labels_layout)

        # 批处理数量
        set_batch_size_layout = QHBoxLayout()
        set_batch_size_label = QLabel("   单批数量：\t")
        self.set_batch_size_input = QLineEdit()
        self.set_batch_size_input.setText("30")
        self.set_batch_size_input.setPlaceholderText("每批处理的数据越多，整体耗时越短。但过大的值会影响大模型分类准确性")
        set_batch_size_layout.addWidget(set_batch_size_label)
        set_batch_size_layout.addWidget(self.set_batch_size_input)
        main_layout.addLayout(set_batch_size_layout)

        # 并发数量
        concurrency_layout = QHBoxLayout()
        concurrency_label = QLabel("   并发批数：\t")
        self.concurrency_input = QLineEdit()
        self.concurrency_input.setText("5")
        self.concurrency_input.setPlaceholderText("并发数越大，整体耗时越短。该值受服务商RPM限制，过大可能带来意外错误")
        concurrency_layout.addWidget(concurrency_label)
        concurrency_layout.addWidget(self.concurrency_input)
        main_layout.addLayout(concurrency_layout)

        # 按钮布局
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("开始处理")
        self.start_button.clicked.connect(self.start_processing)
        self.stop_button = QPushButton("中断运行")
        self.stop_button.clicked.connect(self.stop_processing)
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        main_layout.addLayout(button_layout)

        # 进度条
        self.progress_bar = QProgressBar()
        main_layout.addWidget(self.progress_bar)

        # 状态输出
        self.status_output = QTextEdit()
        self.status_output.setReadOnly(True)
        main_layout.addWidget(self.status_output)

        # 添加底部文字
        footer_label = QLabel("从源码构建：https://gitcode.com/ZhangYichi-ZYc/Excel-Item-Classifier.git")
        footer_label.setStyleSheet("color: #888888; font-size: 10px;")
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 居中对齐
        main_layout.addWidget(footer_label)

        self.setLayout(main_layout)

    def select_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "选择Excel文件", "", "Excel Files (*.xlsx *.xls)")
        if file_name:
            self.file_path.setText(file_name)

    def start_processing(self):
        file_path = self.file_path.text()
        api_key = self.api_key_input.text()
        base_url = self.base_url_input.text()
        model_name = self.model_name_input.text()
        table_name = self.table_name_input.text()
        labels = self.labels_input.text()
        set_batch_size = self.set_batch_size_input.text()
        concurrency = self.concurrency_input.text()

        if not file_path or not api_key or not base_url or not model_name or not table_name or not set_batch_size or not concurrency or not labels:
            self.status_output.append("请填写所有必要信息")
            return

        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.progress_bar.setValue(0)
        self.status_output.clear()

        self.worker = WorkerThread(file_path, api_key, base_url, model_name, table_name, set_batch_size, concurrency,
                                   labels)
        self.worker.update_progress.connect(self.update_progress)
        self.worker.update_status.connect(self.update_status)
        self.worker.finished.connect(self.processing_finished)
        self.worker.start()

    def stop_processing(self):
        if self.worker:
            self.worker.stop()
            self.status_output.append("中断运行请求已发送，程序不会立即停止，请等待已并发的线程返回调用结果")
            self.stop_button.setEnabled(False)

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def update_status(self, status):
        self.status_output.append(status)

    def processing_finished(self):
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.progress_bar.setValue(100)
