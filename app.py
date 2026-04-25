import streamlit as st
import random
import time

# --- CẤU HÌNH HỆ THỐNG ---
TOTAL_DICE = 8

st.set_page_config(page_title="grat-omino battle", layout="wide")

# === MÔ ĐUN ÂM THANH & HIỆU ỨNG ===
def play_sound(sound_type):
    sounds = {
        'roll': "https://actions.google.com/sounds/v1/cartoon/wood_plank_flicks.ogg",
        'select': "https://actions.google.com/sounds/v1/cartoon/pop.ogg",
        'confirm': "https://actions.google.com/sounds/v1/cartoon/wood_block_flicks.ogg",
        'bust': "https://actions.google.com/sounds/v1/cartoon/slip_and_crash.ogg",
        'win': "https://actions.google.com/sounds/v1/cartoon/magic_chime_cord.ogg"
    }
    if sound_type in sounds:
        audio_id = f"sfx_{str(time.time()).replace('.', '')}"
        html = f"""
            <audio id="{audio_id}" autoplay style="display:none;">
                <source src="{sounds[sound_type]}" type="audio/ogg">
            </audio>
            <script>
                setTimeout(function() {{
                    var audio = document.getElementById("{audio_id}");
                    if(audio) audio.play().catch(e => console.log("Blocked autoplay:", e));
                }}, 50);
            </script>
        """
        st.markdown(html, unsafe_allow_html=True)

if 'sfx_trigger' not in st.session_state:
    st.session_state.sfx_trigger = None

if st.session_state.sfx_trigger:
    play_sound(st.session_state.sfx_trigger)
    st.session_state.sfx_trigger = None

if 'pending_toast' not in st.session_state:
    st.session_state.pending_toast = None

if st.session_state.pending_toast:
    st.toast(st.session_state.pending_toast['msg'], icon=st.session_state.pending_toast['icon'])
    st.session_state.pending_toast = None

# === CSS GAME CHÍNH: MÀU PASTEL & HIỆU ỨNG NỔI BẬT ===
st.markdown("""
    <style>
    /* ===== BOARD GAME PREMIUM UI ===== */

.tile-box {
    border-radius: 10px;
    padding: 10px 2px;
    text-align: center;
    background: linear-gradient(145deg, #ffffff, #f1f5f9);
    color: #0f172a !important;
    font-weight: 700;
    font-size: 22px;
    margin-bottom: 6px;
    box-shadow: 3px 3px 8px rgba(0,0,0,0.12),
                inset -2px -2px 4px rgba(255,255,255,0.6);
    transition: all 0.2s ease;
}
.tile-box:hover {
    transform: translateY(-3px);
}

.tile-empty {
    border: 1px dashed #94a3b8;
    border-radius: 10px;
    padding: 10px 2px;
    text-align: center;
    background-color: transparent;
    color: #94a3b8 !important;
    font-size: 20px;
    margin-bottom: 6px;
}

.worm-icon {
    font-size: 14px;
    letter-spacing: -2px;
    margin-top: -4px;
}

/* ===== DICE ===== */
.dice-active-display {
    display: flex;
align-items: center;
justify-content: center;
    width: 62px;
    height: 62px;
    border-radius: 14px;
    border: 2px solid rgba(0,0,0,0.15);
    margin: 10px auto 6px auto;
    position: relative;
    transition: all 0.18s ease;
    box-shadow: 
    6px 6px 12px rgba(0,0,0,0.18),
    inset -4px -4px 8px rgba(255,255,255,0.7),
    inset 3px 3px 6px rgba(0,0,0,0.08);
background: linear-gradient(145deg, rgba(255,255,255,0.95), rgba(240,240,240,0.8));
}

.dice-active-display:hover {
    transform: scale(1.05);
}

.dice-selected-pop {
    transform: translateY(-4px) scale(1.06);
    box-shadow: 0 0 12px rgba(0,0,0,0.2);
}

/* LOCKED */
.dice-locked-display {
    width: 62px;
    height: 62px;
    border-radius: 14px;
    border: 2px dashed #cbd5f5;
    margin: 10px auto 6px auto;
    position: relative;

    background: linear-gradient(145deg, #f1f5f9, #e2e8f0);
    
    /* ❌ bỏ opacity để không làm mờ 🐛 */
    opacity: 1;
}

/* chỉ làm mờ chấm số, KHÔNG làm mờ 🐛 */
.dice-locked-display.face-1,
.dice-locked-display.face-2,
.dice-locked-display.face-3,
.dice-locked-display.face-4,
.dice-locked-display.face-5 {
    filter: grayscale(90%);
}

/* đảm bảo 🐛 luôn rõ */
.face-W::after {
    content: "🐛";
    font-size: 26px;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    filter: none !important;
    opacity: 1 !important;
}

/* MINI */
.dice-graphic {
    width: 42px;
    height: 42px;
    border-radius: 10px;
    margin: 3px;
    display: inline-block;
    position: relative;

    box-shadow: 
        4px 4px 8px rgba(0,0,0,0.2),
        inset -3px -3px 5px rgba(255,255,255,0.7),
        inset 2px 2px 4px rgba(0,0,0,0.1);
}

.dice-small {
    width: 22px;
    height: 22px;
    border-radius: 6px;
    margin: 2px;
    display: inline-block;

    box-shadow: 
        2px 2px 4px rgba(0,0,0,0.2),
        inset -2px -2px 3px rgba(255,255,255,0.6);
}

.dice-active-display::after {
    content: "";
    position: absolute;
    top: 8%;
    left: 10%;
    width: 40%;
    height: 25%;
    background: rgba(255,255,255,0.4);
    border-radius: 50%;
    filter: blur(2px);
}

/* ===== FACES ===== */
.face-1 {
    background-color: #ffadad;
    background-image: radial-gradient(circle, #334155 35%, transparent 40%);
    background-position: center;
    background-size: 26% 26%;
    background-repeat: no-repeat;
}

.face-2 {
    background-color: #ffd6a5;
    background-image: 
        radial-gradient(circle, #334155 35%, transparent 40%),
        radial-gradient(circle, #334155 35%, transparent 40%);
    background-position: 25% 25%, 75% 75%;
    background-size: 26% 26%;
    background-repeat: no-repeat;
}

.face-3 {
    background-color: #fdffb6;
    background-image: 
        radial-gradient(circle, #334155 35%, transparent 40%),
        radial-gradient(circle, #334155 35%, transparent 40%),
        radial-gradient(circle, #334155 35%, transparent 40%);
    background-position: 20% 20%, 50% 50%, 80% 80%;
    background-size: 24% 24%;
    background-repeat: no-repeat;
}

.face-4 {
    background-color: #caffbf;
    background-image: 
        radial-gradient(circle, #334155 35%, transparent 40%),
        radial-gradient(circle, #334155 35%, transparent 40%),
        radial-gradient(circle, #334155 35%, transparent 40%),
        radial-gradient(circle, #334155 35%, transparent 40%);
    background-position: 25% 25%, 75% 25%, 25% 75%, 75% 75%;
    background-size: 26% 26%;
    background-repeat: no-repeat;
}

.face-5 {
    background-color: #9bf6ff;
    background-image: 
        radial-gradient(circle, #334155 35%, transparent 40%),
        radial-gradient(circle, #334155 35%, transparent 40%),
        radial-gradient(circle, #334155 35%, transparent 40%),
        radial-gradient(circle, #334155 35%, transparent 40%),
        radial-gradient(circle, #334155 35%, transparent 40%);
    background-position: 
        20% 20%, 80% 20%, 50% 50%, 20% 80%, 80% 80%;
    background-size: 24% 24%;
    background-repeat: no-repeat;
}
.face-W { background-color: #e5bef7; position: relative; }

/* WORM FIX CHUẨN CENTER */
.face-W {
    position: relative;
}

/* 🐛 luôn nằm chính giữa tuyệt đối (FIX LỆCH) */
.face-W::after {
    content: "🐛";
    font-size: 26px;
    line-height: 1;

    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);

    display: flex;
    align-items: center;
    justify-content: center;
}

.dice-small.face-W::after {
    font-size: 9px;
}

/* ===== BUTTON "CHỌN" ===== */
div[data-testid="stButton"] button[kind="secondary"] {
    font-size: 11px !important;
    padding: 2px 4px !important;
    min-height: 24px !important;
    border-radius: 6px !important;
    background: #f1f5f9 !important;
    border: none !important;
    color: #334155 !important;
    transition: all 0.15s ease;
}

div[data-testid="stButton"] button[kind="secondary"]:hover {
    background: #e2e8f0 !important;
    transform: scale(1.05);
}

/* ===== CONFIRM BUTTON ===== */
div[data-testid="stButton"] button[kind="primary"] {
    border-radius: 10px !important;
}

/* ===== STACK TILE (TÚI ĐỒ) ===== */

.tile-stack {
    width: 65px;
    height: 75px;
    border-radius: 12px;
    margin: 6px auto;
    padding: 6px 4px;

    background: linear-gradient(145deg, #ffffff, #e2e8f0);
    
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;

    box-shadow: 
        4px 4px 8px rgba(0,0,0,0.15),
        inset -2px -2px 4px rgba(255,255,255,0.7);
    
    transition: all 0.2s ease;
}

.tile-stack:hover {
    transform: translateY(-3px) scale(1.05);
}

/* số */
.tile-value {
    font-weight: 800;
    font-size: 20px;
    color: #0f172a;
}

/* sâu */
.tile-worm {
    font-size: 14px;
    letter-spacing: -2px;
}

/* thẻ trên cùng (highlight) */
.top-tile {
    border: 2px solid #ef4444;
    box-shadow: 
        0 0 12px rgba(239,68,68,0.6),
        4px 4px 8px rgba(0,0,0,0.2);
}
            
/* ===== ALIGN ===== */
div[data-testid="column"] {
    text-align: center;
}
    .dice-small.face-W::after { font-size: 10px; }
            /* Thu nhỏ riêng nút "Chọn" dưới xúc xắc */
div[data-testid="stButton"] button[kind="secondary"] {
    font-size: 11px !important;
    padding: 3px 6px !important;
    min-height: 26px !important;
}
    </style>
""", unsafe_allow_html=True)

# --- LOGIC NGHIỆP VỤ ---
def get_worms(tile):
    if 21 <= tile <= 24: return 1
    if 25 <= tile <= 28: return 2
    if 29 <= tile <= 32: return 3
    return 4

if 'game_started' not in st.session_state:
    st.session_state.game_started = False

if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'show_rules' not in st.session_state:
    st.session_state.show_rules = False

# === TRANG BẮT ĐẦU (START SCREEN UX/UI) ===
if not st.session_state.game_started:
# --- TRANG LUẬT CHƠI ---
    if st.session_state.show_rules:
        # CSS Hiệu ứng Sâu bò và Xóa khung trắng mặc định
        st.markdown("""
            <style>
            /* Xóa bỏ mọi khung nền mặc định của Streamlit ở trang luật */
            [data-testid="stVerticalBlock"] > div:has(div.rules-anchor) {
                background: transparent !important;
                box-shadow: none !important;
                border: none !important;
            }

            .worm-bg { 
                position: fixed; font-size: 45px; z-index: 0; 
                pointer-events: none; opacity: 0.3; 
            }
            
            .w1 { animation: crawlRight 18s linear infinite; top: 15%; left: -10%; }
            .w2 { animation: crawlLeft 22s linear infinite 3s; top: 70%; right: -10%; }
            .w3 { animation: crawlUp 25s linear infinite 1s; bottom: -10%; left: 30%; }
            
            @keyframes crawlRight {
                0% { left: -10%; transform: rotate(15deg); }
                100% { left: 110%; transform: rotate(15deg); }
            }
            @keyframes crawlLeft {
                0% { right: -10%; transform: scaleX(-1) rotate(15deg); }
                100% { right: 110%; transform: scaleX(-1) rotate(15deg); }
            }
            @keyframes crawlUp {
                0% { bottom: -10%; transform: rotate(-70deg); }
                100% { bottom: 110%; transform: rotate(-70deg); }
            }
            </style>
            
            <div class="rules-anchor"></div>
            <div class="worm-bg w1">🐛</div>
            <div class="worm-bg w2">🐛</div>
            <div class="worm-bg w3">🐛</div>
        """, unsafe_allow_html=True)
        
        st.title("📖 Luật chơi & Hướng dẫn grat-omino")
        st.markdown("""
        ### 🎯 Mục tiêu
        Trở thành người thu thập được nhiều **Sâu (🐛)** nhất khi trò chơi kết thúc (hết thẻ trên bàn).
        
        ### 🎲 Lượt tung xúc xắc (Roll)
        1. Mỗi lượt bạn có **8 viên xúc xắc**.
        2. Sau khi tung, bạn **BẮT BUỘC** phải chọn 1 giá trị xúc xắc (từ 1 đến 5, hoặc Sâu) để giữ lại. **Tất cả** các viên có giá trị đó sẽ được đưa vào lưới giữ.
        3. **Luật vàng:** Ở các lần tung tiếp theo trong cùng 1 lượt, bạn **KHÔNG ĐƯỢC** chọn lại giá trị đã giữ trước đó.
        4. *(Sâu tính là 5 điểm).*

        ### 🏦 Lấy thẻ & Cướp thẻ
        Để được lấy thẻ, bạn **BẮT BUỘC phải có ít nhất 1 viên Sâu (🐛)** trong số xúc xắc đã giữ.
        * **Lấy thẻ trên bàn:** Tổng điểm xúc xắc >= giá trị thẻ trên bàn. (Được quyền lấy thẻ lớn nhất nhỏ hơn hoặc bằng tổng điểm của bạn).
        * **Cướp thẻ đối thủ:** Nếu tổng điểm của bạn **BẰNG CHÍNH XÁC** với thẻ nằm *trên cùng* trong túi đồ của đối thủ, bạn có quyền cướp nó!
        * Lấy xong thẻ, lượt của bạn kết thúc.

        ### 💥 Nổ (Bust)
        Bạn sẽ bị "Nổ" và mất lượt nếu:
        1. Tung xúc xắc ra toàn các mặt **bạn đã giữ rồi** (không có mặt mới để chọn).
        2. Hết xúc xắc mà **không có con Sâu nào**, hoặc **không đủ điểm** lấy bất cứ thẻ nào.
        * **Hình phạt khi Nổ:** Bạn phải trả thẻ trên cùng của mình lại ra bàn. Thẻ lớn nhất hiện có trên bàn sẽ bị "Úp" (loại bỏ khỏi game).

        ---
        **🕹️ Hướng dẫn thao tác:** Bấm nút `👆 Chọn` dưới các viên xúc xắc cùng màu để giữ chúng lại. Bấm `✅ XÁC NHẬN` để chốt và đi tiếp.
        """)
        
        if st.button("⬅️ Quay lại màn hình chính", type="primary"):
            st.session_state.show_rules = False
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)
        st.stop()

    # --- TRANG CHÍNH (START SCREEN) ---
    # CSS Đặc biệt chỉ dành cho Trang Start Screen
    st.markdown("""
        <style>
        header {visibility: hidden;}
        .title-container { text-align: center; margin-top: 20px; margin-bottom: 10px; }
        .title-emoji { font-size: 4rem; display: inline-block; animation: floatWiggle 3s ease-in-out infinite; -webkit-text-fill-color: initial; }
        
        @keyframes floatWiggle {
            0%, 100% { transform: translateY(0) rotate(0deg); }
            25% { transform: translateY(-10px) rotate(-10deg); }
            75% { transform: translateY(5px) rotate(10deg); }
        }
        
        .start-title-text {
            font-size: 4.5rem; font-weight: 900; display: inline-block;
            background: linear-gradient(135deg, #7f1d1d 0%, #dc2626 50%, #ff4b4b 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            margin-left: 15px; vertical-align: top;
        }
        
        .start-subtitle { text-align: center; color: #475569; font-size: 1.1rem; margin-bottom: 40px; letter-spacing: 3px; text-transform: uppercase; font-weight: 700; }
        
        div[data-testid="stTextInput"] { max-width: 280px; margin: 0 auto; text-align: center; }
        div[data-testid="stTextInput"] label { justify-content: center; color: #334155 !important; font-size: 1rem; font-weight: 600; }
        div[data-testid="stTextInput"] input {
            border-radius: 8px !important; border: 2px solid #cbd5e1 !important; text-align: center;
            background-color: #f8fafc !important; box-shadow: 0 4px 6px rgba(0,0,0,0.05); font-size: 1.1rem; padding: 12px;
            color: #0f172a !important; transition: all 0.3s ease;
        }
        div[data-testid="stTextInput"] input:focus {
            border-color: transparent !important;
            background: linear-gradient(#f8fafc, #f8fafc) padding-box, linear-gradient(135deg, #dc2626, #ff4b4b) border-box !important;
            border: 2px solid transparent !important; box-shadow: 0 0 15px rgba(255, 75, 75, 0.4); outline: none;
        }
        
        /* Căn giữa toàn bộ vùng chứa nút */
        div[data-testid="stButton"] { 
            display: flex; 
            justify-content: center; 
            width: 100%;
        }

        /* Style cho Nút "BẮT ĐẦU" (Primary) */
        div[data-testid="stButton"] button[kind="primary"] {
            max-width: 250px; width: 100%; border-radius: 8px !important;
            background: linear-gradient(135deg, #991b1b 0%, #dc2626 100%) !important;
            color: white !important; border: none !important; font-size: 1.2rem !important; font-weight: bold !important;
            padding: 10px 20px !important; transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
            box-shadow: 0 4px 15px rgba(220, 38, 38, 0.3) !important; animation: breathe 3s infinite;
        }
        @keyframes breathe {
            0%, 100% { box-shadow: 0 4px 15px rgba(220, 38, 38, 0.3); }
            50% { box-shadow: 0 8px 20px rgba(185, 28, 28, 0.6); }
        }
        div[data-testid="stButton"] button[kind="primary"]:hover {
            transform: translateY(-4px) scale(1.05) !important; background: linear-gradient(135deg, #7f1d1d 0%, #b91c1c 100%) !important;
        }

        /* Style cho Nút "Luật Chơi" (Secondary) nhỏ gọn */
        div[data-testid="stButton"] button[kind="secondary"] {
            max-width: 250px; /* Thu gọn vừa phải để cân đối với nút trên */
            background: transparent !important; border: none !important;
            color: #64748b !important; box-shadow: none !important; animation: none !important;
            padding: 5px 10px !important; font-size: 0.95rem !important; font-weight: 600 !important;
            text-decoration: underline; text-underline-offset: 4px;
        }
        div[data-testid="stButton"] button[kind="secondary"]:hover {
            color: #334155 !important; transform: none !important; background: transparent !important;
        }
        
        .start-footer { text-align: center; color: #64748b; font-size: 12px; margin-top: 60px; font-style: italic; animation: fadeIn 3s; letter-spacing: 0.5px; }
        @keyframes fadeIn { 0% { opacity: 0; } 70% { opacity: 0; } 100% { opacity: 1; } }
        </style>
    """, unsafe_allow_html=True)

    # Hiển thị UI
    st.markdown("""
        <div class="title-container">
            <span class="title-emoji">🎲</span>
            <span class="start-title-text">grat-omino</span>
            <span class="title-emoji">🎲</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="start-subtitle">TRẬN CHIẾN BẮT SÂU</div>', unsafe_allow_html=True)
    st.write("")
    
    p1 = st.text_input("🔥 Tên Người chơi 1:", "")
    p2 = st.text_input("🎯 Tên Người chơi 2:", "")
    
    st.write("") # Tạo khoảng trống
    
    # CSS ở trên đã lo việc căn giữa, giờ chỉ cần gọi thẳng 2 nút ra
    start_clicked = st.button("🚀 BẮT ĐẦU CHIẾN!", use_container_width=True, type="primary")
    rules_clicked = st.button("📖 Hướng dẫn & Luật chơi", use_container_width=True, type="secondary")

    st.markdown('<div class="start-footer">grat-omino: grat sẽ thống lĩnh thế giới sâu 🐛</div>', unsafe_allow_html=True)

    if rules_clicked:
        st.session_state.show_rules = True
        st.rerun()

    if start_clicked:
        st.session_state.update({
            'game_started': True, 'names': [p1, p2], 'tiles': list(range(21, 37)), 
            'stacks': [[], []], 'turn': 0, 'kept_dice': [], 'already_kept': set(), 
            'current_roll': [], 'roll_history': [], 'exploded': False, 
            'selected_indices': set(), 'busting_roll': [], 'penalty_applied': False,
            'stats_busts': [0, 0], 'stats_steals': [0, 0], 'stats_max_roll': [0, 0],
            'surrendered': None
        })
        st.rerun()
    st.stop()

# === GAME CHÍNH BẮT ĐẦU TỪ ĐÂY ===

# Kiểm tra điều kiện thắng
if not st.session_state.tiles or st.session_state.surrendered is not None:
    st.title("🏆 TRÒ CHƠI KẾT THÚC!")
    w1 = sum(get_worms(t) for t in st.session_state.stacks[0])
    w2 = sum(get_worms(t) for t in st.session_state.stacks[1])
    
    st.header(f"Điểm số: {st.session_state.names[0]}: {w1} 🐛 | {st.session_state.names[1]}: {w2} 🐛")
    
    if st.session_state.surrendered is not None:
        loser_idx = st.session_state.surrendered
        winner_idx = 1 - loser_idx
        st.error(f"🏳️ {st.session_state.names[loser_idx].upper()} đã phất cờ trắng đầu hàng!")
        st.success(f"CHÚC MỪNG {st.session_state.names[winner_idx].upper()} CHIẾN THẮNG DỄ DÀNG!")
        st.snow()
    else:
        winner = st.session_state.names[0] if w1 > w2 else (st.session_state.names[1] if w2 > w1 else "HÒA")
        if winner != "HÒA":
            st.success(f"CHÚC MỪNG {winner.upper()} LÀ VUA SÂU!")
            st.balloons()
        else:
            st.info("BẤT PHÂN THẮNG BẠI! TRẬN ĐẤU KẾT THÚC HÒA!")
            
    st.divider()
    st.markdown("### 📊 Thống Kê Nổi Bật Lượt Đấu")
    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        st.metric("💥 Số lần Nổ (Busts)", f"{st.session_state.names[0]}: {st.session_state.stats_busts[0]} | {st.session_state.names[1]}: {st.session_state.stats_busts[1]}")
    with sc2:
        st.metric("🥷 Lần cướp thẻ (Steals)", f"{st.session_state.names[0]}: {st.session_state.stats_steals[0]} | {st.session_state.names[1]}: {st.session_state.stats_steals[1]}")
    with sc3:
        st.metric("🔥 Cú roll kỷ lục (Max Score)", f"{st.session_state.names[0]}: {st.session_state.stats_max_roll[0]} | {st.session_state.names[1]}: {st.session_state.stats_max_roll[1]}")

    st.write("")
    col_re1, col_re2 = st.columns(2)
    with col_re1:
        if st.button("🔄 Chơi lại trận mới (Giữ tên)", use_container_width=True, type="primary"):
            st.session_state.update({
                'tiles': list(range(21, 37)), 'stacks': [[], []], 'turn': 0, 'kept_dice': [], 
                'already_kept': set(), 'current_roll': [], 'roll_history': [], 'exploded': False, 
                'selected_indices': set(), 'busting_roll': [], 'penalty_applied': False,
                'stats_busts': [0, 0], 'stats_steals': [0, 0], 'stats_max_roll': [0, 0], 'surrendered': None
            })
            st.rerun()
    with col_re2:
        if st.button("🏠 Quay về màn hình chính", use_container_width=True):
            st.session_state.game_started = False
            st.rerun()
    st.stop()

turn_idx = st.session_state.turn
curr_name = st.session_state.names[turn_idx]
opp_idx = 1 - turn_idx
opp_name = st.session_state.names[opp_idx]

# --- SIDEBAR TÚI ĐỒ ---
st.sidebar.title("🎒 Túi đồ")
for i in [0, 1]:
    stack = st.session_state.stacks[i]
    worms = sum(get_worms(t) for t in stack)
    st.sidebar.markdown(f"### {st.session_state.names[i]}: **{worms} 🐛**")
    
    if stack:
        # Bỏ tính năng chọn thẻ, chỉ hiển thị danh sách thẻ đang có (thẻ trên cùng xếp trước)
        for t in reversed(stack):
            # Thẻ trên cùng (stack[-1]) được viền đỏ để báo hiệu đây là thẻ có thể bị cướp
            is_top = ' border: 3px solid #ff4b4b;' if t == stack[-1] else ''
            st.sidebar.markdown(f"""
<div class="tile-stack { 'top-tile' if t == stack[-1] else '' }">
    <div class="tile-value">{t}</div>
    <div class="tile-worm">{"🐛"*get_worms(t)}</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.divider()
if st.sidebar.button("🏳️ Đầu Hàng Ngay", use_container_width=True):
    st.session_state.surrendered = turn_idx
    st.rerun()

# Nút chơi lại nằm trong game
if st.sidebar.button("🔄 Làm mới trận đấu", use_container_width=True):
    if st.sidebar.checkbox("Xác nhận làm mới?"):
        st.session_state.update({
            'tiles': list(range(21, 37)), 'stacks': [[], []], 'turn': 0, 'kept_dice': [], 
            'already_kept': set(), 'current_roll': [], 'roll_history': [], 'exploded': False, 
            'selected_indices': set(), 'busting_roll': [], 'penalty_applied': False,
            'stats_busts': [0, 0], 'stats_steals': [0, 0], 'stats_max_roll': [0, 0], 'surrendered': None
        })
        st.rerun()

st.title(f"🎲 grat-omino 🎲: {st.session_state.names[0]} vs {st.session_state.names[1]}")
st.subheader(f"Lượt của: **{curr_name}**")

# --- TÍNH TOÁN ĐIỂM SỐ & LOGIC LẤY THẺ ---
total = sum([5 if d == 'W' else d for d in st.session_state.kept_dice])
has_worm = 'W' in st.session_state.already_kept
opp_stack = st.session_state.stacks[opp_idx]

# NGHIÊM NGẶT LUẬT MỚI: Chỉ được lấy/cướp thẻ khi ĐÃ CHỌN XONG XÚC XẮC (không còn viên nào đang roll) VÀ CHƯA BỊ NỔ
is_ready_to_take = (len(st.session_state.current_roll) == 0) and (not st.session_state.exploded)

can_steal = has_worm and opp_stack and (total == opp_stack[-1]) and is_ready_to_take

# Lọc thẻ đủ điều kiện (nhỏ hơn hoặc bằng điểm, phải có Sâu, và phải ở trạng thái sẵn sàng lấy)
eligible_tiles = [t for t in st.session_state.tiles if t <= total] if (has_worm and is_ready_to_take) else []

# Bơm CSS: Hiệu ứng thẻ hợp lệ và làm gọn nút "Lấy" thành màu xanh lá dễ chịu
st.markdown("""
    <style>
    /* Ép kiểu cho thẻ hợp lệ */
    .tile-eligible {
        border: 3px solid #4CAF50 !important;
        background-color: #f0fdf4 !important; 
        animation: pulseGreen 1.2s infinite alternate ease-in-out !important;
    }
    @keyframes pulseGreen {
        from { box-shadow: 0 0 2px #4CAF50; transform: scale(1); }
        to { box-shadow: 0 0 15px #4CAF50; transform: scale(1.05); }
    }
    
    /* CSS Hack: Biến hóa cái nút nằm ngay dưới thẻ hợp lệ */
    div.element-container:has(.tile-eligible) + div.element-container button {
        background-color: #4CAF50 !important; /* Xanh lá dễ chịu */
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0px !important;
        min-height: 28px !important; /* Thu nhỏ gọn gàng */
        font-size: 13px !important;
        font-weight: 600 !important;
        width: 75% !important; /* Ép nút nhỏ lại so với thẻ */
        margin: 0 auto !important; /* Căn giữa */
        display: block !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }
    div.element-container:has(.tile-eligible) + div.element-container button:hover {
        background-color: #45a049 !important;
        transform: translateY(-2px);
    }
    </style>
""", unsafe_allow_html=True)

# Hiển thị thẻ trên bàn
st.markdown("### 🏦 Thẻ bài trên bàn")
r1 = st.columns(8); r2 = st.columns(8)
for i, tile in enumerate(range(21, 37)):
    col = r1[i] if i < 8 else r2[i-8]
    with col:
        if tile in st.session_state.tiles:
            if tile in eligible_tiles:
                # Thẻ hợp lệ: Nhận class .tile-eligible và hiện nút CHỌN

                st.markdown(f'<div class="tile-box tile-eligible">{tile}<br><div class="worm-icon">{"🐛"*get_worms(tile)}</div></div>', unsafe_allow_html=True)

                if st.button("👆 CHỌN", key=f"take_{tile}", use_container_width=True, type="primary"):
                    st.session_state.tiles.remove(tile)
                    st.session_state.stacks[turn_idx].append(tile)
                    st.session_state.pending_toast = {"msg": f"🎉 NGON LÀNH! {curr_name} đã bốc được thẻ {tile}!", "icon": "✨"}
                    st.session_state.update({'turn': 1-turn_idx, 'kept_dice': [], 'already_kept': set(), 'current_roll': [], 'roll_history': []})
                    st.session_state.sfx_trigger = 'win'
                    st.rerun()
            else:
                st.markdown(f'<div class="tile-box">{tile}<br><div class="worm-icon">{"🐛"*get_worms(tile)}</div></div>', unsafe_allow_html=True)
        else: 
            st.markdown('<div class="tile-empty">--</div>', unsafe_allow_html=True)

st.divider()

# Xử lý Nổ & Hình phạt
if st.session_state.exploded:
    st.error(f"💥 BÙM! {curr_name.upper()} ĐÃ BỊ NỔ (BUST) VÀ MẤT LƯỢT!")
    
    if not st.session_state.penalty_applied:
        st.session_state.penalty_applied = True
        returned_tile = None
        highest_removed = None
        
        player_stack = st.session_state.stacks[turn_idx]
        if player_stack:
            returned_tile = player_stack.pop()
            st.session_state.tiles.append(returned_tile)
            st.session_state.tiles.sort()
            
        if st.session_state.tiles:
            highest_tile = max(st.session_state.tiles)
            if returned_tile != highest_tile:
                highest_removed = highest_tile
                st.session_state.tiles.remove(highest_tile)

        st.session_state.bust_msg_1 = f"📉 Hình phạt 1: Bạn phải trả lại thẻ **{returned_tile}** lên bàn." if returned_tile else "🤷 Bạn không có thẻ nào để bị trừ."
        st.session_state.bust_msg_2 = f"🔥 Hình phạt 2: Thẻ cao nhất trên bàn (**{highest_removed}**) đã bị úp (loại bỏ)!" if highest_removed else "✅ Không có thẻ nào trên bàn bị úp."
    
    st.warning(st.session_state.bust_msg_1)
    st.warning(st.session_state.bust_msg_2)
    
    if st.session_state.busting_roll:
        st.write("🎲 **Xúc xắc gây nổ:**")
        bust_html = "".join([f'<div class="dice-graphic face-{d}"></div>' for d in st.session_state.busting_roll])
        st.markdown(bust_html, unsafe_allow_html=True)
        
    if st.button("Kết thúc lượt", use_container_width=True, type="primary"):
        st.session_state.update({
            'turn': 1-turn_idx, 'kept_dice': [], 'already_kept': set(), 'exploded': False, 
            'current_roll': [], 'roll_history': [], 'selected_indices': set(), 
            'busting_roll': [], 'penalty_applied': False
        })
        st.rerun()
    st.stop()

c1, c2 = st.columns([1.5, 1])
with c1:
    remaining = TOTAL_DICE - len(st.session_state.kept_dice)
    can_roll = len(st.session_state.current_roll) == 0
    if st.button(f"🎲 TUNG XÚC XẮC ({remaining} viên)", use_container_width=True, type="primary", disabled=not can_roll):
        if remaining > 0:
            roll = [random.choice([1, 2, 3, 4, 5, 'W']) for _ in range(remaining)]
            st.session_state.roll_history.append(roll)
            
            if not (set(roll) - st.session_state.already_kept):
                st.session_state.exploded = True
                st.session_state.busting_roll = roll 
                st.session_state.current_roll = []
                st.session_state.selected_indices = set()
                st.session_state.sfx_trigger = 'bust'
                st.session_state.stats_busts[turn_idx] += 1
                st.session_state.pending_toast = {"msg": "💥 BÙM! Haha ngố đã bị nổ...", "icon": "💣"}
            else:
                st.session_state.current_roll = roll
                st.session_state.selected_indices = set()
                st.session_state.sfx_trigger = 'roll'
            st.rerun()

    if st.session_state.current_roll:
        st.write("### Nhấp 'Chọn' dưới viên xúc xắc bạn muốn giữ:")
        cols = st.columns(len(st.session_state.current_roll))
        for i, val in enumerate(st.session_state.current_roll):
            with cols[i]:
                is_disabled = val in st.session_state.already_kept
                is_sel = i in st.session_state.selected_indices
                
                if is_disabled: st.markdown(f'<div class="dice-locked-display face-{val}"></div>', unsafe_allow_html=True)
                else:
                    pop = "dice-selected-pop" if is_sel else ""
                    st.markdown(f'<div class="dice-active-display face-{val} {pop}"></div>', unsafe_allow_html=True)
                    st.markdown("<div style='margin-top:-6px'></div>", unsafe_allow_html=True)

                    label = "❌ Bỏ" if is_sel else "👆 Chọn"
                    if st.button(label, key=f"b_{i}", use_container_width=True, type="primary" if is_sel else "secondary"):
                        matching_indices = set(idx for idx, v in enumerate(st.session_state.current_roll) if v == val)
                        if st.session_state.selected_indices == matching_indices:
                            st.session_state.selected_indices = set() 
                        else:
                            st.session_state.selected_indices = matching_indices
                        st.session_state.sfx_trigger = 'select'
                        st.rerun()

        if st.session_state.selected_indices:
            sel_val = st.session_state.current_roll[list(st.session_state.selected_indices)[0]]
            if st.button(f"✅ XÁC NHẬN GIỮ {len(st.session_state.selected_indices)} VIÊN ({sel_val if sel_val != 'W' else '🐛'})", use_container_width=True, type="primary"):
                st.session_state.kept_dice.extend([st.session_state.current_roll[idx] for idx in st.session_state.selected_indices])
                st.session_state.already_kept.add(sel_val)
                st.session_state.current_roll = []; st.session_state.selected_indices = set()
                st.session_state.sfx_trigger = 'confirm'
                st.rerun()

    if st.session_state.roll_history:
        st.write("---")
        with st.expander("📜 Nhật ký lắc xúc xắc lượt này", expanded=True):
            for i, r in enumerate(st.session_state.roll_history):
                hist_html = "".join([f'<div class="dice-small face-{x}"></div>' for x in r])
                st.markdown(f"""
                    <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
                        <div style="min-width:70px; font-weight:600;">Lần {i+1}:</div>
                        <div style="display:flex; flex-wrap:wrap;">{hist_html}</div>
                    </div>
                """, unsafe_allow_html=True)

with c2:
    if total > st.session_state.stats_max_roll[turn_idx]:
        st.session_state.stats_max_roll[turn_idx] = total
        
    st.metric("Tổng điểm lượt này", total)
    kept_html = "".join([f'<div class="dice-graphic face-{d}"></div>' for d in st.session_state.kept_dice])
    st.markdown(f"**Đã giữ:** <br>{kept_html}", unsafe_allow_html=True)
    
    st.write("---")
    
    if can_steal:
        st.success(f"🔥 CƠ HỘI! Bạn có thể cướp thẻ của {opp_name.upper()}!")
        if st.button(f"🎯 CƯỚP THẺ {opp_stack[-1]} TỪ ĐỐI PHƯƠNG", use_container_width=True, type="primary"):
            st.session_state.stacks[turn_idx].append(opp_stack.pop())
            st.session_state.stats_steals[turn_idx] += 1
            st.session_state.pending_toast = {"msg": f"🥷 CÚ CƯỚP THẾ KỶ! {curr_name} đã cuỗm thẻ {st.session_state.stacks[turn_idx][-1]}!", "icon": "🔥"}
            st.session_state.update({'turn': 1-turn_idx, 'kept_dice': [], 'already_kept': set(), 'current_roll': [], 'roll_history': []})
            st.session_state.sfx_trigger = 'win'
            st.rerun()
            
    else:
        remaining_dice = TOTAL_DICE - len(st.session_state.kept_dice)
        
        if len(st.session_state.current_roll) > 0:
            st.warning("🎲 Bạn cần chốt chọn xúc xắc trước khi làm việc khác!")
        elif remaining_dice > 0:
            if not has_worm:
                st.info("⚠️ Bạn bắt buộc phải có ít nhất 1 con Sâu (🐛) mới có thể lấy thẻ!")
            elif eligible_tiles:
                st.success("🎯 Đã đủ điểm lấy thẻ! Nhấn nút 'LẤY' ở thẻ trên bàn, hoặc tung tiếp để cướp/lấy thẻ to hơn.")
            else:
                st.info("🎯 Điểm chưa đủ để bốc thẻ, hãy tung tiếp xúc xắc!")
        elif not st.session_state.exploded:
            st.error("❌ Hết xúc xắc nhưng không đủ điều kiện lấy thẻ. BẠN ĐÃ BỊ NỔ!")
            if st.button("Xác nhận Nổ", type="primary", use_container_width=True):
                st.session_state.exploded = True
                st.session_state.busting_roll = []
                st.session_state.sfx_trigger = 'bust'
                st.session_state.stats_busts[turn_idx] += 1
                st.session_state.pending_toast = {"msg": "💥 TRẮNG TAY! Cố quá thành quá cố rồi...", "icon": "💣"}
                st.rerun()