import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication

from src.gui import MainWindow


@pytest.fixture
def app(qtbot):
    test_app = QApplication([])
    window = MainWindow()
    qtbot.addWidget(window)
    return window


def test_initial_ui_state(app):
    assert app.file_path.text() == ""
    assert app.api_key_input.text() == ""
    assert app.base_url_input.text() == "https://open.bigmodel.cn/api/paas/v4/"
    assert app.model_name_input.text() == "glm-4-air"
    assert app.table_name_input.text() == "物料名称"
    assert app.labels_input.text() != ""
    assert app.set_batch_size_input.text() == "30"
    assert app.concurrency_input.text() == "5"
    assert app.start_button.isEnabled() == True
    assert app.stop_button.isEnabled() == False
    assert app.progress_bar.value() == 0


def test_select_file(app, qtbot):
    QTest.mouseClick(app.findChild(QPushButton, "选择文件"), Qt.MouseButton.LeftButton)

    app.file_path.setText("test.xlsx")

    assert app.file_path.text() == "test.xlsx"


def test_start_processing_without_required_fields(app, qtbot):
    app.file_path.setText("")
    app.api_key_input.setText("")

    QTest.mouseClick(app.start_button, Qt.MouseButton.LeftButton)

    assert "请填写所有必要信息" in app.status_output.toPlainText()


def test_start_processing_with_required_fields(app, qtbot):
    app.file_path.setText("test.xlsx")
    app.api_key_input.setText("test_api_key")

    QTest.mouseClick(app.start_button, Qt.MouseButton.LeftButton)

    assert app.start_button.isEnabled() == False
    assert app.stop_button.isEnabled() == True
    assert app.progress_bar.value() == 0


def test_stop_processing(app, qtbot):
    app.file_path.setText("test.xlsx")
    app.api_key_input.setText("test_api_key")

    QTest.mouseClick(app.start_button, Qt.MouseButton.LeftButton)

    QTest.mouseClick(app.stop_button, Qt.MouseButton.LeftButton)

    assert "中断运行请求已发送" in app.status_output.toPlainText()
    assert app.stop_button.isEnabled() == False
