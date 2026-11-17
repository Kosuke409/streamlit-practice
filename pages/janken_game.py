import streamlit as st
from models.janken import JankenGame, HANDS

st.set_page_config(page_title="連勝じゃんけん", page_icon="✊")

st.title("✊✌️🖐️ 連勝じゃんけん")
st.write("CPUに勝ち続けよう！あいこは連勝継続、負けたらリセットです。")

# --- ゲームの状態を session_state に保存（再実行されても消えないように）---
if "janken" not in st.session_state:
    st.session_state.janken = JankenGame()
if "janken_last" not in st.session_state:
    st.session_state.janken_last = None

game = st.session_state.janken

# --- 手を選ぶボタン ---
st.subheader("手を選んでね")
cols = st.columns(3)
for col, (name, emoji) in zip(cols, HANDS.items()):
    if col.button(f"{emoji}\n{name}", key=f"hand_{name}", use_container_width=True):
        st.session_state.janken_last = game.play(name)

# --- 直近の結果を表示 ---
last = st.session_state.janken_last
if last:
    st.divider()
    left, right = st.columns(2)
    left.metric("あなた", f"{HANDS[last['player']]} {last['player']}")
    right.metric("CPU", f"{HANDS[last['cpu']]} {last['cpu']}")

    if last["result"] == "win":
        st.success("🎉 あなたの勝ち！")
        if game.streak >= 3:
            st.balloons()
    elif last["result"] == "lose":
        st.error("😢 あなたの負け…連勝リセット")
    else:
        st.info("🤝 あいこ！")

# --- 成績 ---
st.divider()
c1, c2, c3 = st.columns(3)
c1.metric("🔥 現在の連勝", game.streak)
c2.metric("🏆 最高連勝", game.best_streak)
c3.metric("📊 勝率", f"{game.win_rate:.0f}%")

# --- 履歴 ---
if game.history:
    with st.expander("対戦履歴を見る"):
        labels = {"win": "勝ち", "lose": "負け", "draw": "あいこ"}
        for i, h in enumerate(game.history[:10], start=1):
            st.write(
                f"{i}. {HANDS[h['player']]} vs {HANDS[h['cpu']]} → {labels[h['result']]}"
            )

# --- リセット ---
if st.button("最初からやり直す"):
    st.session_state.janken = JankenGame()
    st.session_state.janken_last = None
    st.rerun()