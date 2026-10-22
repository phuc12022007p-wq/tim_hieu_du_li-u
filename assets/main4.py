# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.animation import FuncAnimation, FFMpegWriter

# 1. Đọc dữ liệu từ file chuẩn abc-27.csv (365 ngày)
CSV_FILE = "abc-27.csv"
df = pd.read_csv(CSV_FILE, header=None)

cols = ["Mo_cua", "Phien_2", "Phien_3", "Phien_4", "Phien_5", "Phien_6", "Dong_cua"]
df.columns = cols

# 2. Gom nhóm dữ liệu CỨ MỖI 5 NGÀY THÀNH 1 NẾN
GROUP_SIZE = 5
n_rows = len(df)
n_candles = int(np.ceil(n_rows / GROUP_SIZE))

candles_data = []
for i in range(n_candles):
    group = df.iloc[i * GROUP_SIZE : (i + 1) * GROUP_SIZE]
    
    o = group["Mo_cua"].iloc[0]       
    c = group["Dong_cua"].iloc[-1]    
    h = group[cols].values.max()       
    l = group[cols].values.min()       
    
    start_idx = i * GROUP_SIZE
    ref = df.loc[start_idx - 1, "Dong_cua"] if start_idx > 0 else o

    floor = 0.9 * ref
    ceiling = 1.1 * ref

    start_day = start_idx + 1
    end_day = min((i + 1) * GROUP_SIZE, n_rows)
    
    candles_data.append({
        "Label": f"Nến {i+1} (Ngày {start_day}-{end_day})",
        "Open": o, "High": h, "Low": l, "Close": c,
        "Ref": ref, "Floor": floor, "Ceiling": ceiling
    })

c_df = pd.DataFrame(candles_data)

open_price = c_df["Open"].values
close_price = c_df["Close"].values
high_price = c_df["High"].values
low_price = c_df["Low"].values
ref_price = c_df["Ref"].values
floor_price = c_df["Floor"].values
ceil_price = c_df["Ceiling"].values

x_candles = np.arange(n_candles)

# Mức Max/Min lũy kế theo giai đoạn
cum_max = np.maximum.accumulate(high_price)
cum_min = np.minimum.accumulate(low_price)
global_max = high_price.max()

# 3. Cấu hình giao diện Dark Mode
plt.style.use('dark_background')
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 8), sharex=True, gridspec_kw={'hspace': 0.12})

width = 0.55

def get_price_color(price, ref, floor, ceiling):
    """Xác định màu sắc nến theo quy tắc biên độ sàn/trần/tham chiếu"""
    tol = max(1e-6, abs(ref) * 1e-6)
    if np.isclose(price, ceiling, atol=tol):
        return '#B026FF'      # Tím trần
    elif np.isclose(price, floor, atol=tol):
        return '#1E90FF'      # Xanh sàn
    elif np.isclose(price, ref, atol=tol):
        return '#FFD700'      # Vàng tham chiếu
    elif price > ref:
        return '#00E676'      # Xanh lá tăng
    else:
        return '#FF3B30'      # Đỏ giảm

def setup_axes():
    """Thiết lập cố định cho các trục đồ thị"""
    for ax in (ax1, ax2):
        ax.set_ylim(-1000, global_max * 1.15)
        ax.yaxis.set_major_formatter('{x:,.0f}')
        ax.grid(True, linestyle='--', alpha=0.12, color='gray')
        ax.tick_params(colors='gray', labelsize=9)

    ax1.set_ylabel("Giá (VND)", color='white', fontsize=10)
    ax2.set_ylabel("Giá (VND)", color='white', fontsize=10)
    ax2.set_xlabel("Mốc Ngày (Date)", color='white', fontsize=10)
    ax2.set_xlim(-1, n_candles + 3)

    tick_indices = [int(d / 5) for d in range(0, 365, 30) if int(d / 5) < n_candles]
    tick_labels = [str(d) for d in range(0, 365, 30)[:len(tick_indices)]]
    ax2.set_xticks(tick_indices)
    ax2.set_xticklabels(tick_labels)

def init():
    ax1.clear()
    ax2.clear()
    setup_axes()
    return []

def update(frame):
    ax1.clear()
    ax2.clear()
    setup_axes()

    # --- TIÊU ĐỀ ---
    ax1.set_title(f"Mô phỏng biến động giá chứng khoán abc-27 | {c_df.loc[frame, 'Label']}", 
                  color='white', fontsize=12, pad=10, fontweight='bold')

    # --- BIỂU ĐỒ TRÊN: Biểu đồ nến Nhật ---
    for i in range(frame + 1):
        o, c, h, l = open_price[i], close_price[i], high_price[i], low_price[i]
        ref, flr, ceil = ref_price[i], floor_price[i], ceil_price[i]

        color = '#00FFFF' if i == frame else get_price_color(c, ref, flr, ceil)

        ax1.plot([i, i], [l, h], color=color, linewidth=1.2, zorder=2)
        height = max(abs(c - o), (h - l) * 0.01 if (h - l) > 0 else 1)
        bottom = min(o, c)
        rect = Rectangle((i - width/2, bottom), width, height, facecolor=color, edgecolor=color, zorder=3)
        ax1.add_patch(rect)

    # --- BIỂU ĐỒ DƯỚI: Range Chart + SƠ ĐỒ ĐƯỜNG GIÁ THÔ CỨNG + PHỦ BÓNG ---
    sub_x = x_candles[:frame+1]
    sub_high = high_price[:frame+1]
    sub_low = low_price[:frame+1]
    sub_close = close_price[:frame+1]

    # Dải biên độ High - Low
    ax2.fill_between(sub_x, sub_low, sub_high, color='#334422', alpha=0.3, label='Dải biên độ High-Low')
    ax2.plot(sub_x, sub_high, color='#7CFC00', linewidth=0.8, alpha=0.5, label='Giá Cao nhất (High)')
    ax2.plot(sub_x, sub_low, color='#FFA500', linewidth=0.8, alpha=0.5, label='Giá Thấp nhất (Low)')

    # Đường giá thô cứng
    cur_close = close_price[frame]
    cur_ref = ref_price[frame]
    cur_flr = floor_price[frame]
    cur_ceil = ceil_price[frame]
    cur_color = get_price_color(cur_close, cur_ref, cur_flr, cur_ceil)

    ax2.plot(sub_x, sub_close, color=cur_color, linewidth=1.2, label='Đường giá hiện tại', zorder=4)
    ax2.fill_between(sub_x, 0, sub_close, color=cur_color, alpha=0.08, zorder=3)

    # Các đường mốc cố định bên phải
    ax2.axhline(cur_ceil, color='#B026FF', linestyle=':', linewidth=0.9, alpha=0.6, label='Giá trần (+10%)')
    ax2.axhline(cur_flr, color='#1E90FF', linestyle=':', linewidth=0.9, alpha=0.6, label='Giá sàn (-10%)')
    
    stage_max, stage_min = cum_max[frame], cum_min[frame]
    ax2.axhline(stage_max, color='#00FF00', linestyle='--', linewidth=0.9, alpha=0.6, label='Max tích lũy')
    ax2.axhline(stage_min, color='#FF3B30', linestyle='--', linewidth=0.9, alpha=0.6, label='Min tích lũy')

    # Nhãn cố định rìa phải
    right_x = n_candles + 0.2
    labels = [
        (cur_ceil, f"Trần: {cur_ceil:,.0f}", '#B026FF'),
        (stage_max, f"Max: {stage_max:,.0f}", '#00FF00'),
        (stage_min, f"Min: {stage_min:,.0f}", '#FF3B30'),
        (cur_flr, f"Sàn: {cur_flr:,.0f}", '#1E90FF')
    ]
    for val, txt, col in labels:
        ax2.text(right_x, val, txt, color=col, fontsize=8.5, fontweight='bold', va='center', ha='left')

    # Mức giá hiện tại
    ax2.axhline(cur_close, color=cur_color, linestyle='-.', linewidth=0.7, alpha=0.4)
    ax2.plot(frame, cur_close, marker='o', color=cur_color, markersize=5, markeredgecolor='white', markeredgewidth=0.8, zorder=5)

    text_color = 'black' if cur_color in ['#FFD700', '#00E676'] else 'white'
    ax2.text(frame + 0.5, cur_close, f" Giá: {cur_close:,.0f} ", color=text_color, fontsize=8.5, fontweight='bold', va='center',
             bbox=dict(boxstyle='round,pad=0.2', facecolor=cur_color, edgecolor='none', alpha=0.9), zorder=6)

    ax2.legend(loc='upper left', fontsize=8, framealpha=0.4, facecolor='#111111', edgecolor='none', ncol=3)
    
    # Bỏ tight_layout trong update() để không bị warning
    return []

# Cấu hình tight_layout 1 lần cho figure ở ngoài
fig.tight_layout()

# --- CẤU HÌNH THỜI LƯỢNG 2 PHÚT (120 GIÂY) ---
TOTAL_DURATION_SEC = 120  # 2 phút
fps_val = n_candles / TOTAL_DURATION_SEC
interval_ms = (TOTAL_DURATION_SEC / n_candles) * 1000

ani = FuncAnimation(fig, update, frames=n_candles, init_func=init, interval=interval_ms, repeat=False)

# --- XUẤT RA FILE VIDEO MP4 ---
OUTPUT_FILE = "stock_simulation_2min.mp4"
print(f"Đang tiến hành xuất video 2 phút ({n_candles} nến)...")

try:
    writer = FFMpegWriter(fps=fps_val, metadata=dict(title='Mô phỏng giá chứng khoán 2 phút'), bitrate=1800)
    ani.save(OUTPUT_FILE, writer=writer)
    print(f"-> Hoàn tất xuất video thành công: {OUTPUT_FILE}")
except Exception as e:
    print(f"Không thể xuất MP4 trực tiếp (Do thiếu FFmpeg): {e}")
    print("Đang bật cửa sổ hiển thị mô phỏng 2 phút trực tiếp...")
    plt.show()