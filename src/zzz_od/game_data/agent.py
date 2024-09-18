from cv2.typing import MatLike
from enum import Enum
from typing import Optional, List, Union

from one_dragon.utils.i18_utils import gt


class AgentTypeEnum(Enum):

    ATTACK = '强攻'
    STUN = '击破'
    SUPPORT = '支援'
    DEFENSE = '防护'
    ANOMALY = '异常'
    UNKNOWN = '未知'

    @classmethod
    def from_name(cls, name):
        if name in AgentTypeEnum.__members__:
            return cls[name]
        else:
            return cls.UNKNOWN


class DmgTypeEnum(Enum):

    ELECTRIC = '电属性'
    ETHER = '以太'
    PHYSICAL = '物理'
    FIRE = '火属性'
    ICE = '冰属性'
    UNKNOWN = '未知'

    @classmethod
    def from_name(cls, name):
        if name in DmgTypeEnum.__members__:
            return cls[name]
        else:
            return cls.UNKNOWN


class RareTypeEnum(Enum):

    S = 'S'
    A = 'A'
    UNKNOWN = '未知'

    @classmethod
    def from_name(cls, name):
        if name in RareTypeEnum.__members__:
            return cls[name]
        else:
            return cls.UNKNOWN


class AgentStateCheckWay(Enum):

    COLOR_RANGE_CONNECT: int = 1  # 根据颜色 在特定范围里匹配找连通块的数量
    BACKGROUND_GRAY_RANGE_LENGTH: int = 2  # 根据背景的灰度颜色 在特定范围里反推横条的长度
    COLOR_RANGE_EXIST: int = 3  # 根据颜色 在特定范围里匹配是否出现
    FOREGROUND_COLOR_RANGE_LENGTH: int = 4  # 根据前景颜色 在特定范围里计算横条的长度
    FOREGROUND_GRAY_RANGE_LENGTH: int = 5  # 根据前景的灰度颜色 在特定范围里计算横条的长度


class AgentStateDef:

    def __init__(self, state_name: str,
                 check_way: AgentStateCheckWay,
                 template_id: str,
                 lower_color: Union[MatLike, int] = None,
                 upper_color: Union[MatLike, int] = None,
                 connect_cnt: Optional[int] = None,
                 split_color_range: Optional[List[Union[MatLike, int]]] = None,
                 max_length: int = 100
                 ):
        self.state_name: str = state_name
        self.template_id: str = template_id
        self.check_way: AgentStateCheckWay = check_way

        # 需要匹配的颜色范围
        self.lower_color: Union[MatLike, int] = lower_color
        self.upper_color: Union[MatLike, int] = upper_color
        # 匹配用于分割的颜色范围 类似能量条的中间有空白时使用
        self.split_color_range: Optional[List[Union[MatLike, int]]] = split_color_range

        # 判断连通块时 所需的最小像素点数量
        self.connect_cnt: Optional[int] = connect_cnt

        # 判断长度时 用于调整最大长度 例如能量最大值是120
        self.max_length: int = max_length


class CommonAgentStateEnum(Enum):

    ENERGY_31 = AgentStateDef('前台-能量', AgentStateCheckWay.FOREGROUND_GRAY_RANGE_LENGTH,
                              lower_color=100, upper_color=255, template_id='energy_31',
                              split_color_range=[0, 20], max_length=120)
    ENERGY_32 = AgentStateDef('后台-1-能量', AgentStateCheckWay.FOREGROUND_GRAY_RANGE_LENGTH,
                              lower_color=100, upper_color=255, template_id='energy_32',
                              split_color_range=[0, 20], max_length=120)
    ENERGY_33 = AgentStateDef('后台-2-能量', AgentStateCheckWay.FOREGROUND_GRAY_RANGE_LENGTH,
                              lower_color=100, upper_color=255, template_id='energy_33',
                              split_color_range=[0, 20], max_length=120)
    ENERGY_21 = AgentStateDef('前台-能量', AgentStateCheckWay.FOREGROUND_GRAY_RANGE_LENGTH,
                              lower_color=100, upper_color=255, template_id='energy_21',
                              split_color_range=[0, 20], max_length=120)
    ENERGY_22 = AgentStateDef('后台-1-能量', AgentStateCheckWay.FOREGROUND_GRAY_RANGE_LENGTH,
                              lower_color=100, upper_color=255, template_id='energy_22',
                              split_color_range=[0, 20], max_length=120)
    LIFE_DEDUCTION = AgentStateDef('前台-血量扣减', AgentStateCheckWay.FOREGROUND_COLOR_RANGE_LENGTH,
                              lower_color=(140, 30, 30), upper_color=(160, 50, 50), template_id='life_deduction')


class Agent:

    def __init__(self, agent_id: str, agent_name: str,
                 rare_type: RareTypeEnum,
                 agent_type: AgentTypeEnum,
                 dmg_type: DmgTypeEnum,
                 state_list: Optional[List[AgentStateDef]] = None
                 ):
        """
        代理人
        """
        self.agent_id: str = agent_id  # 代理人的英文名称
        self.agent_name: str = agent_name  # 代理人的中文名称
        self.rare_type: RareTypeEnum = rare_type  # 稀有等级

        self.agent_type: AgentTypeEnum = agent_type  # 角色类型
        self.dmg_type: DmgTypeEnum = dmg_type  # 伤害类型

        self.state_list: List[AgentStateDef] = state_list  # 可能有的状态

    @property
    def agent_type_str(self) -> str:
        return gt(self.agent_type.value)


class AgentEnum(Enum):

    ANBY = Agent('anby', '安比', RareTypeEnum.A, AgentTypeEnum.STUN, DmgTypeEnum.ELECTRIC)
    ANTON = Agent('anton', '安东', RareTypeEnum.A, AgentTypeEnum.ATTACK, DmgTypeEnum.ELECTRIC)
    BEN = Agent('ben', '本', RareTypeEnum.A, AgentTypeEnum.DEFENSE, DmgTypeEnum.FIRE)
    BILLY = Agent('billy', '比利', RareTypeEnum.A, AgentTypeEnum.ATTACK, DmgTypeEnum.ELECTRIC)
    CORIN = Agent('corin', '可琳', RareTypeEnum.A, AgentTypeEnum.ATTACK, DmgTypeEnum.PHYSICAL)
    ELLEN = Agent('ellen', '艾莲', RareTypeEnum.S, AgentTypeEnum.ATTACK, DmgTypeEnum.ICE)
    GRACE = Agent('grace', '格莉丝', RareTypeEnum.S, AgentTypeEnum.ANOMALY, DmgTypeEnum.ELECTRIC)
    KOLEDA = Agent('koleda', '珂蕾妲', RareTypeEnum.S, AgentTypeEnum.STUN, DmgTypeEnum.FIRE)
    LUCY = Agent('lucy', '露西', RareTypeEnum.A, AgentTypeEnum.SUPPORT, DmgTypeEnum.FIRE)
    LYCAON = Agent('lycaon', '莱卡恩', RareTypeEnum.S, AgentTypeEnum.STUN, DmgTypeEnum.ICE)
    NEKOMATA = Agent('nekomata', '猫又', RareTypeEnum.S, AgentTypeEnum.ATTACK, DmgTypeEnum.PHYSICAL)
    NICOLE = Agent('nicole', '妮可', RareTypeEnum.A, AgentTypeEnum.SUPPORT, DmgTypeEnum.ETHER)
    PIPER = Agent('piper', '派派', RareTypeEnum.A, AgentTypeEnum.ANOMALY, DmgTypeEnum.PHYSICAL)
    RINA = Agent('rina', '丽娜', RareTypeEnum.S, AgentTypeEnum.SUPPORT, DmgTypeEnum.ELECTRIC)
    SOLDIER_11 = Agent('soldier_11', '11号', RareTypeEnum.S, AgentTypeEnum.ATTACK, DmgTypeEnum.FIRE)
    SOUKAKU = Agent('soukaku', '苍角', RareTypeEnum.A, AgentTypeEnum.SUPPORT, DmgTypeEnum.ICE)

    ZHU_YUAN = Agent('zhu_yuan', '朱鸢', RareTypeEnum.S, AgentTypeEnum.ATTACK, DmgTypeEnum.ETHER,
                     state_list=[AgentStateDef('朱鸢-子弹数', AgentStateCheckWay.COLOR_RANGE_CONNECT,
                                               template_id='zhu_yuan', lower_color=(240, 60, 0), upper_color=(255, 180, 20), connect_cnt=20)])

    QINGYI = Agent('qingyi', '青衣', RareTypeEnum.S, AgentTypeEnum.STUN, DmgTypeEnum.ELECTRIC,
                     state_list=[AgentStateDef('青衣-电压', AgentStateCheckWay.BACKGROUND_GRAY_RANGE_LENGTH,
                                               template_id='qingyi', lower_color=0, upper_color=100)])

    JANE_DOE = Agent('jane_doe', '简', RareTypeEnum.S, AgentTypeEnum.ANOMALY, DmgTypeEnum.PHYSICAL,
                     state_list=[AgentStateDef('简-萨霍夫跳', AgentStateCheckWay.COLOR_RANGE_EXIST,
                                               template_id='jane_attack', lower_color=(100, 20, 20), upper_color=(255, 255, 255), connect_cnt=10),
                                 AgentStateDef('简-狂热心流', AgentStateCheckWay.FOREGROUND_COLOR_RANGE_LENGTH,
                                               template_id='jane_red', lower_color=(200, 20, 20), upper_color=(255, 255, 255), connect_cnt=10)
                                 ])

    SETH_LOWELL = Agent('seth_lowell', '赛斯', RareTypeEnum.A, AgentTypeEnum.DEFENSE, DmgTypeEnum.ELECTRIC,
                     state_list=[AgentStateDef('赛斯-意气', AgentStateCheckWay.BACKGROUND_GRAY_RANGE_LENGTH,
                                               template_id='seth_lowell', lower_color=0, upper_color=10)])
