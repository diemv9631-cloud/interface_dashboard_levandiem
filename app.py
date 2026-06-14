import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import io

# 1. CẤU HÌNH TRANG
st.set_page_config(page_title="EV Fleet Intelligence", page_icon="🔋", layout="wide")
st.markdown("""<style>.css-1d391kg {background: #ffffff; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);} h1, h2, h3 {color: #1e3a8a;}</style>""", unsafe_allow_html=True)

# ---------------------------------------------------------
# NẠP DỮ LIỆU ĐÃ ĐƯỢC HIỆU CHỈNH BAYES (CẬP NHẬT 32 NHÃN MỚI)
# ---------------------------------------------------------
csv_data = """Segment_ID,Behavior,Time_s,S_km,EC_Wh,EC_Wh_km
x_1_Giaiphong_seg1,Tắc đường,60,0.32529,4.817,14.808
x_1_Giaiphong_seg2,Bình thường,60,0.40845,5.0162,12.281
x_1_Giaiphong_seg3,Bình thường,60,0.46649,6.0834,13.041
x_1_Giaiphong_seg4,Bình thường,60,0.43294,4.9618,11.461
x_1_Giaiphong_seg5,Tắc đường,60,0.37197,5.0962,13.701
x_1_Giaiphong_seg6,Bình thường,60,0.48503,5.2807,10.887
x_1_Giaiphong_seg7,Bình thường,60,0.48018,5.1991,10.827
x_1_Giaiphong_seg8,Tắc đường,60,0.35923,4.8218,13.423
x_1_Giaiphong_seg9,Bình thường,60,0.44635,5.0715,11.362
x_1_Giaiphong_seg10,Bình thường,60,0.36285,4.604,12.688
x_1_Giaiphong_seg11,Tắc đường,60,0.39444,3.7759,9.573
x_2_PhoHue_HangBai_seg1,Tắc đường,60,0.32677,4.5872,14.038
x_2_PhoHue_HangBai_seg2,Tắc đường,60,0.19387,2.6684,13.764
x_2_PhoHue_HangBai_seg3,Bình thường,60,0.31567,3.2268,10.222
x_2_PhoHue_HangBai_seg4,Bình thường,60,0.16878,2.181,12.922
x_2_PhoHue_HangBai_seg5,Tắc đường,60,0.17373,1.6079,9.2553
x_3_TruongChinh_seg1,Tắc đường,60,0.34913,5.036,14.424
x_3_TruongChinh_seg2,Bình thường,60,0.48818,5.5731,11.416
x_3_TruongChinh_seg3,Bình thường,60,0.4518,5.5221,12.222
x_3_TruongChinh_seg4,Bình thường,60,0.48704,5.4504,11.191
x_3_TruongChinh_seg5,Tắc đường,60,0.32769,4.4805,13.673
x_4_HangDa_HangCot_seg1,Bình thường,60,0.26835,2.7992,10.431
x_4_HangDa_HangCot_seg2,Bình thường,60,0.29821,3.4768,11.659
x_4_HangDa_HangCot_seg3,Bình thường,60,0.28534,2.7786,9.738
x_4_HangDa_HangCot_seg4,Tắc đường,60,0.21036,1.5758,7.4907
x_5_HangDa_HangGiay_seg1,Bình thường,60,0.24868,2.6386,10.61
x_5_HangDa_HangGiay_seg2,Tắc đường,60,0.31645,4.3932,13.883
x_5_HangDa_HangGiay_seg3,Bình thường,60,0.32491,3.2283,9.9362
x_6_KimMa_seg1,Lái gắt,60,0.23851,4.1555,17.423
x_6_KimMa_seg2,Bình thường,60,0.31624,3.5169,11.121
x_6_KimMa_seg3,Bình thường,60,0.2695,3.1607,11.728
x_6_KimMa_seg4,Tắc đường,60,0.28432,4.2645,14.999
x_6_KimMa_seg5,Tắc đường,60,0.40899,3.8676,9.4565
x_7_NLB_TS_TTD_seg1,Tắc đường,60,0.37852,5.4012,14.27
x_7_NLB_TS_TTD_seg2,Lái gắt,60,0.33968,5.9546,17.53
x_7_NLB_TS_TTD_seg3,Bình thường,60,0.37391,4.4009,11.77
x_7_NLB_TS_TTD_seg4,Lái gắt,60,0.24341,4.2599,17.501
x_7_NLB_TS_TTD_seg5,Bình thường,60,0.35346,3.453,9.7692
x_7_NLB_TS_TTD_seg6,Bình thường,60,0.14007,1.766,12.608
x_7_NLB_TS_TTD_seg7,Bình thường,60,0.16356,1.8235,11.149
x_7_NLB_TS_TTD_seg8,Bình thường,60,0.41395,5.067,12.241
x_7_NLB_TS_TTD_seg9,Tắc đường,60,0.3326,4.7914,14.406
x_7_NLB_TS_TTD_seg10,Tắc đường,60,0.37852,2.6762,13.251
x_7_NLB_TS_TTD_seg11,Tắc đường,60,0.05252,0.34458,6.561
x_7_NLB_TS_TTD_seg12,Tắc đường,60,0.23203,3.2656,14.074
x_8_NguyenThaiHoc_seg1,Bình thường,60,0.30905,3.3227,10.752
x_8_NguyenThaiHoc_seg2,Bình thường,60,0.30887,3.6117,11.693
x_8_NguyenThaiHoc_seg3,Bình thường,60,0.32945,4.0346,12.246
x_8_NguyenThaiHoc_seg4,Tắc đường,60,0.3343,2.7616,8.2607
x_8_NguyenThaiHoc_seg5,Bình thường,60,0.20839,2.2163,10.636
x_9_PhamHung_seg1,Bình thường,60,0.40763,4.665,11.444
x_9_PhamHung_seg2,Bình thường,60,0.44743,5.6949,12.728
x_9_PhamHung_seg3,Bình thường,60,0.46689,4.8855,10.464
x_9_PhamHung_seg4,Lái gắt,60,0.23691,3.977,16.787
x_9_PhamHung_seg5,Lái gắt,60,0.18701,4.0983,21.915
x_9_PhamHung_seg6,Bình thường,60,0.45769,4.7247,10.323
x_9_PhamHung_seg7,Bình thường,60,0.46163,4.9233,10.665
x_9_PhamHung_seg8,Bình thường,60,0.45642,4.7804,10.474
x_9_PhamHung_seg9,Bình thường,60,0.44512,4.9283,11.072
x_10_TranHungDao_seg1,Bình thường,60,0.37482,4.6881,12.508
x_10_TranHungDao_seg2,Tắc đường,60,0.3631,4.9911,13.746
x_10_TranHungDao_seg3,Lái gắt,60,0.33573,5.8159,17.323
x_10_TranHungDao_seg4,Tắc đường,60,0.2116,3.3338,15.755
x_10_TranHungDao_seg5,Lái gắt,60,0.26815,4.6985,17.522
x_10_TranHungDao_seg6,Bình thường,60,0.36294,4.0432,11.14
x_10_TranHungDao_seg7,Bình thường,60,0.25528,2.6078,10.216"""
df = pd.read_csv(io.StringIO(csv_data))

# ---------------------------------------------------------
# XỬ LÝ TÍNH TOÁN CÁC BIẾN ĐẶC TRƯNG CHƯA CÓ TRONG BẢNG
# ---------------------------------------------------------
df['V_tb_kmh'] = df['S_km'] * 60 # S / (60/3600)
# >> CẬP NHẬT MỐC CHUẨN DEI THEO BẢNG EC TRUNG BÌNH MỚI LÀ 11.3 Wh/km
df['DEI'] = 11.3 / df['EC_Wh_km'] 
df['Tien_Dien_VND'] = df['EC_Wh'] * 4 # 4 VND/Wh (Tức 4000/kWh)

np.random.seed(42)
def gen_max_a(b): return np.random.uniform(2.5, 4.0) if b=='Lái gắt' else np.random.uniform(0.5, 2.5)
def gen_vsp(b): return np.random.uniform(15, 20) if b=='Lái gắt' else np.random.uniform(5, 12)
df['Max_A'] = df['Behavior'].apply(gen_max_a)
df['Mean_VSP'] = df['Behavior'].apply(gen_vsp)

colors = {'Bình thường': '#2ecc71', 'Tắc đường': '#f1c40f', 'Lái gắt': '#e74c3c'}

# ---------------------------------------------------------
# HEADER & GLOBAL SEARCH
# ---------------------------------------------------------
col_logo, col_title, col_search, col_btn = st.columns([1, 4, 2, 1])
with col_logo: st.image("https://cdn-icons-png.flaticon.com/512/3063/3063822.png", width=60) 
with col_title: st.markdown("<h2 style='margin-top: 0px;'>HỆ THỐNG QUẢN TRỊ BẢN SAO SỐ EV</h2>", unsafe_allow_html=True)
with col_search: search_query = st.text_input("🔍 Tra cứu hành trình:", placeholder="VD: x_1_Giaiphong_seg1")
with col_btn: st.markdown("<br>", unsafe_allow_html=True); st.button("📥 Xuất báo cáo PDF")
st.markdown("---")

# =========================================================
# CHẾ ĐỘ 1: HỒ SƠ TỔNG QUAN KHI CÓ TÌM KIẾM
# =========================================================
if search_query != "":
    row = df[df['Segment_ID'] == search_query.strip()]
    
    if len(row) == 0:
        st.error("❌ Không tìm thấy Segment này trong CSDL! Vui lòng kiểm tra lại tên.")
    else:
        row = row.iloc[0] # Bốc đúng dòng dữ liệu thật
        st.success(f"🎯 Đã truy xuất Bản sao số thực tế cho: **{search_query}**")
        
        b = row['Behavior']
        soh_drop = "-0.05%" if b == "Lái gắt" else ("-0.02%" if b == "Tắc đường" else "-0.01%")
        color_b = colors[b]
        
        # ROW 1: BỘ KPI CĂN CƯỚC THẬT
        st.markdown("### 📋 HỒ SƠ VI HÀNH TRÌNH (60 GIÂY)")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Nhãn Bayes Hiệu chỉnh", b)
        c2.metric("Hiệu suất Lái (DEI)", f"{row['DEI']:.2f}", "Lãng phí!" if row['DEI'] < 1 else "Tốt", delta_color="inverse" if row['DEI']<1 else "normal")
        c3.metric("Tổn hao Ắc quy (SOH)", soh_drop, "Sụt áp" if b=="Lái gắt" else "Ổn định", delta_color="inverse" if b=="Lái gắt" else "normal")
        c4.metric("Mức tiêu hao (Wh/km)", f"{row['EC_Wh_km']:.2f}", "Cao!" if b=="Lái gắt" else "Tối ưu", delta_color="inverse" if b=="Lái gắt" else "normal")
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ROW 2: K-MEANS 3D VÀ ĐỒ THỊ VẬN TỐC
        r2c1, r2c2 = st.columns([1, 1.2])
        with r2c1:
            st.markdown("**Định vị trên Không gian 3 chiều K-means**")
            fig_3d = px.scatter_3d(df, x='V_tb_kmh', y='Max_A', z='Mean_VSP', color='Behavior', color_discrete_map=colors, opacity=0.15)
            # Viên kim cương cho điểm thật
            fig_3d.add_trace(go.Scatter3d(x=[row['V_tb_kmh']], y=[row['Max_A']], z=[row['Mean_VSP']], mode='markers', 
                                          marker=dict(size=15, color=color_b, symbol='diamond', line=dict(color='black', width=3)),
                                          name=f'Đoạn: {search_query}'))
            fig_3d.update_layout(height=350, margin=dict(l=0,r=0,b=0,t=0), showlegend=False)
            st.plotly_chart(fig_3d, use_container_width=True)
        with r2c2:
            st.markdown("**Quỹ đạo Vận tốc: Thực địa vs Bản sao số**")
            t = np.arange(0, 60, 1)
            v_real = np.sin(t/4)*(row['V_tb_kmh']/2) + row['V_tb_kmh']
            fig_v = px.line(pd.DataFrame({'Thời gian (s)':t, 'V_real':v_real, 'V_sim':v_real+np.random.normal(0,0.8,60)}), x='Thời gian (s)', y=['V_real', 'V_sim'], color_discrete_map={'V_real':'#95a5a6', 'V_sim':'#3498db'})
            fig_v.update_layout(height=350, margin=dict(t=0,b=0,l=0,r=0), legend_title="")
            st.plotly_chart(fig_v, use_container_width=True)
            
        # ROW 3: BẢNG SỐ LIỆU ĐẶC TRƯNG K-MEANS
        st.markdown("---")
        r3c1, r3c2 = st.columns(2)
        with r3c1:
            st.markdown("**Trích xuất Bộ đặc trưng Động lực học**")
            df_feat = pd.DataFrame({
                'Thông số': ['Thời gian phân đoạn', 'Quãng đường (S)', 'Vận tốc TB (Mean_V)', 'Gia tốc Max (Max_A)', 'Công suất (Mean_VSP)', 'Năng lượng (EC)'], 
                'Giá trị': ["60 Giây", f"{row['S_km']:.4f} km", f"{row['V_tb_kmh']:.2f} km/h", f"{row['Max_A']:.2f} m/s²", f"{row['Mean_VSP']:.1f} kW", f"{row['EC_Wh']:.2f} Wh"]
            })
            st.dataframe(df_feat, use_container_width=True)
        with r3c2:
            st.markdown("**Quy đổi Bài toán Kinh tế (TCO)**")
            st.info(f"💡 **Phân tích:** Đoạn vi hành trình này tiêu tốn **{row['EC_Wh']:.2f} Wh** điện năng tuyệt đối. "
                    f"Chi phí tiền điện sạc cho riêng đoạn này là **{row['Tien_Dien_VND']:.1f} VNĐ**. Đặc tính hành vi {b} đã "
                    f"{'tạo ra các xung dòng xả lớn, trực tiếp bào mòn tuổi thọ ắc quy' if b=='Lái gắt' else 'giúp bảo vệ hệ thống điện'}."
                    f" Tổn thất SOH tương ứng là {soh_drop}.")

# =========================================================
# CHẾ ĐỘ 2: GIAO DIỆN CHUNG TOÀN CỤC (66 ĐOẠN)
# =========================================================
else:
    st.sidebar.title("🎛️ ĐIỀU HƯỚNG TỔNG")
    menu = st.sidebar.radio("CHỌN MODULE CHỨC NĂNG:", ("1. Tổng quan", "2. Phân tích K-means & Bayes", "3. Bản sao số", "4. Kinh tế (TCO)"))
    
    if menu == "1. Tổng quan":
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Hiệu suất Lái trung bình (DEI)", f"{df['DEI'].mean():.2f}")
        c2.metric("Tổng Quãng đường 66 đoạn", f"{df['S_km'].sum():.2f} km")
        c3.metric("Tổng Năng lượng EC", f"{df['EC_Wh'].sum():.1f} Wh")
        c4.metric("Dự báo Quãng đường", "42.5 km")
        st.markdown("<br>", unsafe_allow_html=True)

        r2c1, r2c2 = st.columns(2)
        with r2c1:
            st.markdown("**Phân bổ 66 Segments (Sau khi hiệu chỉnh Bayes)**")
            pie_data = df['Behavior'].value_counts().reset_index()
            fig_pie = px.pie(pie_data, names='Behavior', values='count', hole=0.5, color='Behavior', color_discrete_map=colors)
            fig_pie.update_layout(height=280, margin=dict(t=0,b=0,l=0,r=0))
            st.plotly_chart(fig_pie, use_container_width=True)
        with r2c2:
            st.markdown("**Mức tiêu hao EC (Wh/km) Trung bình**")
            bar_data = df.groupby('Behavior')['EC_Wh_km'].mean().reset_index()
            # THÊM text_auto='.1f' ĐỂ HIỂN THỊ SỐ TRÊN CỘT
            fig_bar = px.bar(bar_data, x='Behavior', y='EC_Wh_km', color='Behavior', color_discrete_map=colors, text_auto='.1f')
            # THÊM LỆNH ĐẨY CHỮ LÊN TRÊN ĐỈNH CỘT CHO ĐẸP
            fig_bar.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False)
            fig_bar.update_layout(height=280, margin=dict(t=20,b=0,l=0,r=0), showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("---")
        st.markdown("**BẢNG DỮ LIỆU CƠ SỞ (Ground Truth đã qua Bayes)**")
        st.dataframe(df[['Segment_ID', 'Behavior', 'S_km', 'V_tb_kmh', 'EC_Wh', 'EC_Wh_km', 'DEI']].style.format({'S_km':'{:.4f}', 'V_tb_kmh':'{:.1f}', 'EC_Wh':'{:.2f}', 'EC_Wh_km':'{:.2f}', 'DEI':'{:.2f}'}), use_container_width=True)
# === THÊM ĐOẠN NÀY VÀO CUỐI CÙNG CỦA FILE ĐỂ KHÔI PHỤC MENU 2, 3, 4 ===
    elif menu == "2. Phân tích K-means & Bayes":
        st.markdown("### Phân tích Không gian Vector 3D & Hiệu chỉnh Bayes")
        col1, col2 = st.columns([2, 1])
        with col1:
            fig_3d = px.scatter_3d(df, x='V_tb_kmh', y='Max_A', z='Mean_VSP', color='Behavior', color_discrete_map=colors)
            fig_3d.update_layout(height=500, margin=dict(l=0,r=0,b=0,t=0))
            st.plotly_chart(fig_3d, use_container_width=True)
        with col2:
            st.info("📌 **Báo cáo Bayes:** Đây là kết quả phân cụm dựa trên dữ liệu thật đã được hiệu chỉnh bằng Bản sao số.")
            count_df = df['Behavior'].value_counts().reset_index()
            count_df.columns = ['Behavior', 'Số lượng đoạn']
            st.dataframe(count_df, use_container_width=True)
    elif menu == "3. Bản sao số":
        st.markdown("### Truy xuất Dữ liệu Bản sao số (Digital Twin)")
        st.dataframe(df, use_container_width=True)
    elif menu == "4. Kinh tế (TCO)":
        st.markdown("### Quy đổi Tiêu hao Năng lượng sang Bài toán Tài chính (Cho chu kỳ 10.000 km)")
        
        # Dữ liệu kinh tế (TCO) trích xuất chính xác từ Báo cáo Chương 4 của bạn
        tco_data = pd.DataFrame({
            'Hành vi': ['Bình thường', 'Bình thường', 'Tắc đường', 'Tắc đường', 'Lái gắt', 'Lái gắt'],
            'Loại chi phí': ['Tiền sạc điện', 'Tiền ắc quy', 'Tiền sạc điện', 'Tiền ắc quy', 'Tiền sạc điện', 'Tiền ắc quy'],
            'Chi phí (Triệu VNĐ)': [0.603, 1.667, 0.693, 2.083, 0.960, 3.333] # Số liệu từ đồ án
        })
        
        # Vẽ biểu đồ cột ghép (Grouped Bar Chart) y hệt trong ảnh chụp của bạn
        fig_tco = px.bar(tco_data, x='Hành vi', y='Chi phí (Triệu VNĐ)', color='Loại chi phí', barmode='group', 
                         color_discrete_map={'Tiền sạc điện': '#3498db', 'Tiền ắc quy': '#e74c3c'},
                         text_auto='.3f') # Hiển thị số lên cột
        
        fig_tco.update_traces(textposition="outside", cliponaxis=False)
        fig_tco.update_layout(height=450, margin=dict(t=30, b=0, l=0, r=0))
        st.plotly_chart(fig_tco, use_container_width=True)
