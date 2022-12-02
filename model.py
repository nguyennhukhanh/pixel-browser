import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from final_variable import url, home
from cache.step3_save import save_history


class isMain(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(isMain, self).__init__(*args, **kwargs)

        # THÊM WINDOWS
        # THÊM TIỆN ÍCH TAB ĐỂ HIỂN THỊ CÁC THẺ TRONG TRANG WEB
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.setCentralWidget(self.tabs)

        # LẮNG NGHE SỰ KIỆN DOUBLE CLICK
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        # LẮNG NGHE SỰ KIỆN TAB ĐÃ ĐÓNG
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        # LẮNG NGHE SỰ KIỆN TAB HIỆN TẠI
        self.tabs.currentChanged.connect(self.current_tab_changed)

        # THÊM THANH CÔNG CỤ ĐIỀU HƯỚNG
        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(16, 16))
        self.addToolBar(navtb)

        # THÊM CÁC NÚT VÀO THANH CÔNG CỤ ĐIỀU HƯỚNG
        # NÚT TRỞ VỀ TRANG WEB TRƯỚC
        back_btn = QAction(
            QIcon(os.path.join('icons', 'left-arrow.png')), "Back", self)
        back_btn.setStatusTip("Quay lại trang trước")
        navtb.addAction(back_btn)
        # ĐIỀU HƯỚNG ĐẾN TRANG TRƯỚC
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())

        # NÚT ĐỂ CHUYỂN ĐẾN TRANG WEB TIẾP THEO
        next_btn = QAction(
            QIcon(os.path.join('icons', 'right-arrow.png')), "Forward", self)
        next_btn.setStatusTip("Chuyển tiếp đến trang tiếp theo")
        navtb.addAction(next_btn)
        # ĐIỀU HƯỚNG ĐẾN TRANG TIẾP THEO
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())

        # NÚT LÀM MỚI TRANG WEB
        reload_btn = QAction(
            QIcon(os.path.join('icons', 'redo.png')), "Reload", self)
        reload_btn.setStatusTip("Tải lại trang")
        navtb.addAction(reload_btn)
        # LÀM MỚI TRANG WEB HIỆN TẠI
        reload_btn.triggered.connect(
            lambda: self.tabs.currentWidget().reload())

        # NÚT TRANG CHỦ
        home_btn = QAction(
            QIcon(os.path.join('icons', 'home.png')), "Home", self)
        home_btn.setStatusTip("Đến trang chủ")
        navtb.addAction(home_btn)
        # ĐIỀU HƯỚNG ĐẾN TRANG CHỦ MẶC ĐỊNH
        home_btn.triggered.connect(self.navigate_home)

        # THÊM DẤU PHÂN CÁCH VÀO CÁC NÚT ĐIỀU HƯỚNG
        navtb.addSeparator()

        # THÊM BIỂU TƯỢNG NHÃN ĐỂ HIỂN THỊ TRẠNG THÁI BẢO MẬT CỦA URL ĐƯỢC TẢI
        self.httpsicon = QLabel()
        self.httpsicon.setPixmap(
            QPixmap(os.path.join('icons', 'unlock.png')))
        navtb.addWidget(self.httpsicon)

        # THÊM CHỈNH SỬA DÒNG ĐỂ HIỂN THỊ VÀ CHỈNH SỬA URL
        self.urlbar = QLineEdit()
        navtb.addWidget(self.urlbar)
        # TẢI URL KHI NHẤN NÚT ON PRESS
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        

        # THÊM NÚT DỪNG ĐỂ DỪNG TẢI URL
        stop_btn = QAction(
            QIcon(os.path.join('icons', 'stop.png')), "Stop", self)
        stop_btn.setStatusTip("Dừng tải trang hiện tại")
        navtb.addAction(stop_btn)
        # DỪNG TẢI URL
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())

        # THÊM TOP MENU
        # File menu
        file_menu = self.menuBar().addMenu("&File")
        # THAO TÁC MENU THÊM TỆP
        new_tab_action = QAction(
            QIcon(os.path.join('icons', 'tab.png')), "New Tab", self)
        new_tab_action.setStatusTip("Mở một tab mới")
        file_menu.addAction(new_tab_action)
        # THÊM NEW TAB
        new_tab_action.triggered.connect(lambda _: self.add_new_tab())

        #LỊCH SỬ DUYỆT WEB
        history_tab_action = QAction(
            QIcon(os.path.join('icons', 'history.png')), "History", self)
        history_tab_action.setStatusTip("Lịch sử duyệt web")
        file_menu.addAction(history_tab_action)
        # THÊM HISTORY TAB
        history_tab_action.triggered.connect(lambda _: self.history_tab())

        # Help menu
        help_menu = self.menuBar().addMenu("&Help")
        # THÊM TÁC VỤ HELP MENU
        navigate_home_action = QAction(QIcon(os.path.join('icons', 'back-to-home.png')),
                                       "Homepage", self)
        navigate_home_action.setStatusTip("Đến trang chủ")
        help_menu.addAction(navigate_home_action)
        # ĐIỀU HƯỚNG ĐẾN TRANG WEB MẶC ĐỊNH
        navigate_home_action.triggered.connect(self.navigate_home)

        # ĐẶT TÊN VÀ BIỂU TƯỢNG CHO ỨNG DỤNG
        self.setWindowTitle("Pixel Browser")
        self.setWindowIcon(QIcon(os.path.join('icons', 'maple-leaf.png')))

        # THÊM STYLESHEET ĐỂ TÙY CHỈNH WINDOWS
        # STYLESHEET (DARK MODE)
        self.setStyleSheet("""QWidget{
            /* MÀU NAVBAR = XÁM, MÀU CHỮ TRÊN THANH NAVBAR = ĐEN */
           background-color: rgb(245, 245, 245);
           color: rgb(0, 0, 0);
        }
        QTabWidget::pane { /* KHUNG TIỆN ÍCH (TAB) */
            border-top: 2px solid rgb(255,255,255);
            position: absolute;
            top: -0.5em;
            color: rgb(0, 0, 0);
            padding: 5px;
        }

        QTabWidget::tab-bar {
            alignment: left;
        }

        /* Tạo style cho tab, gồm: back, reload, search,... */
        QLabel, QToolButton, QTabBar::tab {
            /*Màu button:  back, reload,... = xám*/
            background: rgb(245,245,245);
            /* Viền btn */
            border: 2px solid rgb(245,245,245);
            border-radius: 10px;
            min-width: 8ex;
            padding: 5px;
            margin-right: 2px;
            color: rgb(0, 0, 0);
        }

        QLabel:hover, QToolButton::hover, QTabBar::tab:selected, QTabBar::tab:hover {
            background: rgb(0, 49, 49);
            /*Màu border button:  back, reload,... = xám*/
            border: 2px solid rgb(245,245,245);
            /* New Tab = trắng, hover btn = trắng */
            background-color: rgb(255,255,255);
        }

        /*Thanh Tìm Kiếm*/
        QLineEdit {
            /* Xám */
            border: 2px solid rgb(211,211,211);
            border-radius: 10px;
            padding: 5px;
            background-color: rgb(255,255,255);
            color: rgb(0, 0, 0);
        }
        QLineEdit:hover {
            /*Xanh dương nhạt*/
            border: 2px solid rgb(135,206,250);
        }
        QLineEdit:focus{
            /* Xanh dương đậm */
            border: 2px solid rgb(30,144,255);
            color: rgb(96, 96, 96);
        }
        QPushButton{
            background: rgb(49, 49, 49);
            border: 2px solid rgb(0, 36, 36);
            background-color: rgb(0, 36, 36);
            padding: 5px;
            border-radius: 10px;
        }""")

        # MẶC ĐỊNH HOME PAGE LÀ GOOGLE.COM
        label = 'Homepage'
        self.add_new_tab(QUrl(url), label)

        # SHOW MAIN WINDOW
        self.show()

    # ############################################
    # FUNCTIONS
    ##############################################
    # THÊM NEW TAB
    def add_new_tab(self, qurl=None, label="Blank"):
        # Kiểm tra xem giá trị url có trống không
        if qurl is None:
            qurl = QUrl('')  # Gán chuỗi rỗng vào url

        # Tải url đã ghi đè
        browser = QWebEngineView()
        browser.setUrl(qurl)

        # THÊM TAB CHO TRANG WEB
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        # LẮNG NGHE CÁC SỰ KIỆN TRÊN TRÌNH DUYỆT
        # KHI THAY ĐỔI URL
        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_urlbar(qurl, browser))
        # KHI TẢI XONG
        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))

    #THÊM LỊCH SỬ TAB
    def history_tab(self, qurl=None, label="Lịch Sử"):
        # Kiểm tra xem giá trị url có trống không
        if qurl is None:
            qurl = QUrl('http://localhost:1410/history')  # Gán chuỗi rỗng vào url

        # Tải url đã ghi đè
        browser = QWebEngineView()
        browser.setUrl(qurl)

        # THÊM TAB CHO TRANG WEB
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        # LẮNG NGHE CÁC SỰ KIỆN TRÊN TRÌNH DUYỆT
        # KHI THAY ĐỔI URL
        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_urlbar(qurl, browser))
        # KHI TẢI XONG
        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))

    # THÊM TAB MỚI KHI NHẤP ĐÚP CHUỘT
    def tab_open_doubleclick(self, i):
        if i == -1:  # Tab luôn lớn hơn 1, có nghĩa là nhỏ hơn 1
            self.add_new_tab()

    # ĐÓNG TẤT CẢ CÁC TABS
    def close_current_tab(self, i):
        if self.tabs.count() < 2:  # Chỉ đóng nếu có nhiều tab đang mở
            return

        self.tabs.removeTab(i)

    # CẬP NHẬT VĂN BẢN URL KHI TAB HOẠT ĐỘNG ĐƯỢC THAY ĐỔI
    def update_urlbar(self, q, browser=None):
        #q = QURL
        if browser != self.tabs.currentWidget():
            # Nếu điều này không phải từ tab hiện tại, bỏ qua nó
            return
        # URL Schema
        if q.scheme() == 'https':
            # Nếu Schema là https, thay đổi biểu tượng thành ổ khóa bị khóa để cho biết rằng trang web được bảo mật
            self.httpsicon.setPixmap(
                QPixmap(os.path.join('icons', 'locked.png')))
            #Lưu lịch sử vào db
            save_history(q.toString())

        else:
            # Nếu Schema không phải là https, thay đổi biểu tượng thành ổ khóa bị khóa để cho biết rằng trang web không an toàn
            self.httpsicon.setPixmap(
                QPixmap(os.path.join('icons', 'unlock.png')))

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    # TAB HIỆN ĐÃ BỊ THAY ĐỔI
    def current_tab_changed(self, i):
        # i = tab index
        # LẤY URL TAB HIỆN TẠI
        qurl = self.tabs.currentWidget().url()
        # CẬP NHẬT URL TEXT
        self.update_urlbar(qurl, self.tabs.currentWidget())
        # CẬP NHẬT WINDOWS TITTLE
        self.update_title(self.tabs.currentWidget())

    # CẬP NHẬT WINDOWS TITTLE
    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            # Nếu điều này không phải từ tab hiện tại, bỏ qua nó
            return

        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle(title)

    # ĐIỀU HƯỚNG ĐẾN URL
    def navigate_to_url(self):  # Không nhận được Url
        # LẤY URL TEXT
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            # Mặc định url scheme là http
            q.setScheme("http")
        if q.scheme() == 'http':
            q = QUrl(url+"search?q="+self.urlbar.text())
        self.tabs.currentWidget().setUrl(q)

    # ĐIỀU HƯỚNG ĐẾN TRANG CHỦ
    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl(home))


app = QApplication(sys.argv)
