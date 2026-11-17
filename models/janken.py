import random

# 手の名前と絵文字
HANDS = {
    "グー": "✊",
    "チョキ": "✌️",
    "パー": "🖐️",
}

# プレイヤーが勝つ組み合わせ (プレイヤー, CPU)
WIN_PATTERNS = {
    ("グー", "チョキ"),
    ("チョキ", "パー"),
    ("パー", "グー"),
}


def judge(player_hand: str, cpu_hand: str) -> str:
    """勝敗を判定して 'win' / 'lose' / 'draw' を返す"""
    if player_hand == cpu_hand:
        return "draw"
    if (player_hand, cpu_hand) in WIN_PATTERNS:
        return "win"
    return "lose"


class JankenGame:
    """連勝じゃんけんゲームの状態を管理するクラス"""

    def __init__(self):
        self.streak = 0        # 現在の連勝数
        self.best_streak = 0   # 最高連勝記録
        self.total = 0         # 総対戦数
        self.wins = 0          # 勝利数
        self.history = []      # 対戦履歴

    def play(self, player_hand: str) -> dict:
        """1回勝負して結果を返す"""
        cpu_hand = random.choice(list(HANDS))
        result = judge(player_hand, cpu_hand)

        self.total += 1
        if result == "win":
            self.wins += 1
            self.streak += 1
            self.best_streak = max(self.best_streak, self.streak)
        elif result == "lose":
            self.streak = 0
        # あいこの場合は連勝数はそのまま

        record = {"player": player_hand, "cpu": cpu_hand, "result": result}
        self.history.insert(0, record)  # 新しい順に並べる
        return record

    @property
    def win_rate(self) -> float:
        """勝率(%)"""
        if self.total == 0:
            return 0.0
        return self.wins / self.total * 100