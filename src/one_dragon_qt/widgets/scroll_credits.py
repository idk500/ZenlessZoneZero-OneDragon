from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QPoint, Property, QEasingCurve
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from one_dragon.base.operation.one_dragon_env_context import OneDragonEnvContext
from one_dragon.utils.log_utils import log
from one_dragon.utils import os_utils
import yaml
import os


class ScrollCreditsWidget(QWidget):
    """
    滚动字幕组件，用于显示电影字幕般的致谢名单
    内容从本地contributer.yaml文件加载
    """
    
    def __init__(self, ctx: OneDragonEnvContext, parent=None):
        super().__init__(parent)
        self.ctx = ctx
        
        # 初始化UI
        self._init_ui()
        
        # 初始化动画
        self._init_animation()
        
        # 加载commit数据
        self._load_commit_data()
        
        # 启动滚动
        self._start_scroll()
    
    def _init_ui(self):
        """
        初始化UI布局
        """
        self.setMinimumHeight(300)
        self.setStyleSheet("""
            ScrollCreditsWidget {
                background-color: transparent;
                border-radius: 8px;
            }
        """)
        
        # 主布局
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # 滚动容器
        self.scroll_container = QWidget()
        self.scroll_container.setStyleSheet("background-color: transparent;")
        self.main_layout.addWidget(self.scroll_container)
        
        # 内容布局
        self.content_layout = QVBoxLayout(self.scroll_container)
        self.content_layout.setAlignment(Qt.AlignCenter)
        self.content_layout.setSpacing(30)
        
        # 标题
        self.title_label = QLabel("致谢名单")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            QLabel {
                color: #333333;
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 30px;
            }
        """)
        self.content_layout.addWidget(self.title_label)
        
        # 占位符，用于动态添加commit信息
        self.commits_container = QWidget()
        self.commits_container.setStyleSheet("background-color: transparent;")
        self.commits_layout = QVBoxLayout(self.commits_container)
        self.commits_layout.setAlignment(Qt.AlignCenter)
        self.commits_layout.setSpacing(30)
        self.content_layout.addWidget(self.commits_container)
    
    def _init_animation(self):
        """
        初始化滚动动画
        """
        # 创建动画对象
        self.animation = QPropertyAnimation(self.scroll_container, b"pos")
        self.animation.setDuration(30000)  # 30秒滚动一次
        self.animation.setLoopCount(-1)  # 无限循环
        
        # 设置动画曲线
        self.animation.setEasingCurve(QEasingCurve.Linear)
    
    def _load_commit_data(self):
        """
        从本地contributer.yaml文件加载贡献者信息
        """
        try:
            # 清空现有内容
            for i in reversed(range(self.commits_layout.count())):
                widget = self.commits_layout.itemAt(i).widget()
                if widget:
                    widget.deleteLater()
            
            # 读取本地contributer.yaml文件
            contributors_file = os.path.join(os_utils.get_work_dir(), 'contributer.yaml')
            
            if not os.path.exists(contributors_file):
                # 如果文件不存在，显示提示
                no_file_label = QLabel("contributer.yaml文件不存在")
                no_file_label.setAlignment(Qt.AlignCenter)
                no_file_label.setStyleSheet("""
                    QLabel {
                        color: #ff6666;
                        font-size: 14px;
                    }
                """)
                self.commits_layout.addWidget(no_file_label)
                return
            
            # 读取并解析YAML文件
            with open(contributors_file, 'r', encoding='utf-8') as f:
                contributors_data = yaml.safe_load(f)
            
            # 整合所有贡献者信息
            all_contributors = []
            
            # 核心贡献者
            if 'core_contributors' in contributors_data:
                all_contributors.extend(contributors_data['core_contributors'])
            
            # 近期贡献者
            if 'recent_contributors' in contributors_data:
                all_contributors.extend(contributors_data['recent_contributors'])
            
            # 文档组贡献者
            if 'documentation_contributors' in contributors_data:
                all_contributors.extend(contributors_data['documentation_contributors'])
            
            # 社区维护者
            if 'community_maintainers' in contributors_data:
                all_contributors.extend(contributors_data['community_maintainers'])
            
            # 其他贡献者
            if 'other_contributors' in contributors_data:
                all_contributors.extend(contributors_data['other_contributors'])
            
            # 添加贡献者信息
            for contributor in all_contributors:
                contributor_widget = self._create_contributor_widget(contributor)
                self.commits_layout.addWidget(contributor_widget)
            
            # 如果没有贡献者信息，显示提示
            if not all_contributors:
                no_data_label = QLabel("未获取到贡献者信息")
                no_data_label.setAlignment(Qt.AlignCenter)
                no_data_label.setStyleSheet("""
                    QLabel {
                        color: #999999;
                        font-size: 14px;
                    }
                """)
                self.commits_layout.addWidget(no_data_label)
            
        except Exception as e:
            log.error(f"加载贡献者数据失败: {e}")
            # 添加错误信息
            error_label = QLabel(f"加载贡献者信息失败: {str(e)}")
            error_label.setAlignment(Qt.AlignCenter)
            error_label.setStyleSheet("""
                QLabel {
                    color: #ff6666;
                    font-size: 14px;
                }
            """)
            self.commits_layout.addWidget(error_label)
    
    def _create_contributor_widget(self, contributor):
        """
        创建单个贡献者信息的widget
        
        Args:
            contributor: 贡献者信息字典，包含name和contributions
            
        Returns:
            显示贡献者信息的widget
        """
        widget = QWidget()
        widget.setStyleSheet("background-color: transparent;")
        widget.setMinimumHeight(100)  # 设置最小高度，确保文字完整显示
        
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        # 贡献者名称
        name_label = QLabel(f"{contributor['name']}")
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("""
            QLabel {
                color: #555555;
                font-size: 16px;
                font-weight: bold;
                padding: 5px;
                min-height: 24px;
            }
        """)
        layout.addWidget(name_label)
        
        # 贡献者角色
        if 'role' in contributor:
            role_label = QLabel(f"{contributor['role']}")
            role_label.setAlignment(Qt.AlignCenter)
            role_label.setStyleSheet("""
                QLabel {
                    color: #666666;
                    font-size: 14px;
                    padding: 5px;
                    min-height: 24px;
                    line-height: 20px;
                }
            """)
            role_label.setWordWrap(True)
            role_label.setMaximumWidth(400)
            layout.addWidget(role_label)
        
        # 贡献次数
        contributions_label = QLabel(f"{contributor['contributions']}")
        contributions_label.setAlignment(Qt.AlignCenter)
        contributions_label.setStyleSheet("""
            QLabel {
                color: #999999;
                font-size: 12px;
                padding: 5px;
                min-height: 20px;
            }
        """)
        layout.addWidget(contributions_label)
        
        return widget
    
    def _create_commit_widget(self, commit):
        """
        创建单个commit信息的widget
        
        兼容旧的commit数据结构，保留此方法以便后续扩展
        """
        widget = QWidget()
        widget.setStyleSheet("background-color: transparent;")
        widget.setMinimumHeight(100)  # 设置最小高度，确保文字完整显示
        
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        # 作者信息
        author_label = QLabel(f"{commit.author}")
        author_label.setAlignment(Qt.AlignCenter)
        author_label.setStyleSheet("""
            QLabel {
                color: #555555;
                font-size: 16px;
                font-weight: bold;
                padding: 5px;
                min-height: 24px;
            }
        """)
        layout.addWidget(author_label)
        
        # commit信息
        message_label = QLabel(f"{commit.commit_message}")
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setStyleSheet("""
            QLabel {
                color: #666666;
                font-size: 14px;
                padding: 5px;
                min-height: 40px;
                line-height: 20px;
            }
        """)
        message_label.setWordWrap(True)
        message_label.setMaximumWidth(400)
        message_label.setMinimumHeight(40)  # 设置最小高度，确保双行文字完整显示
        layout.addWidget(message_label)
        
        # 时间信息
        time_label = QLabel(f"{commit.commit_time}")
        time_label.setAlignment(Qt.AlignCenter)
        time_label.setStyleSheet("""
            QLabel {
                color: #999999;
                font-size: 12px;
                padding: 5px;
                min-height: 20px;
            }
        """)
        layout.addWidget(time_label)
        
        return widget
    
    def _start_scroll(self):
        """
        启动滚动动画
        """
        # 计算滚动距离
        content_height = self.scroll_container.sizeHint().height()
        container_height = self.height()
        
        # 设置动画起始和结束位置
        start_pos = QPoint(0, container_height)
        end_pos = QPoint(0, -content_height)
        
        self.animation.setStartValue(start_pos)
        self.animation.setEndValue(end_pos)
        
        # 启动动画
        self.animation.start()
    
    def resizeEvent(self, event):
        """
        窗口大小变化时重新计算动画
        """
        super().resizeEvent(event)
        
        # 重新设置动画
        self._start_scroll()
    
    # 定义pos属性，用于动画
    def _get_pos(self):
        return self.scroll_container.pos()
    
    def _set_pos(self, pos):
        self.scroll_container.move(pos)
    
    pos = Property(QPoint, _get_pos, _set_pos)
