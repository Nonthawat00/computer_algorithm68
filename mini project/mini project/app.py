import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. การตั้งค่าหน้าเว็บ ---
st.set_page_config(page_title="ระบบจัดการการเรียน", page_icon="📝", layout="wide")

# --- 2. การจัดการข้อมูล (Session State) ---
if 'students' not in st.session_state:
    st.session_state.students = [
        {"id": "001", "name": "นายนนทวัฒน์ มีศักดิ์ประเสริฐ", "score": 100},
        {"id": "002", "name": "นางสาวสรัน รักเรียน", "score": 100},
        {"id": "003", "name": "นายเอกไช ขยันมาก", "score": 100},
    ]

# เก็บสถานะการเช็คชื่อชั่วคราวในแต่ละรอบ (ยังไม่ตัดคะแนน)
if 'temp_status' not in st.session_state:
    st.session_state.temp_status = {s['id']: "ยังไม่เช็ค" for s in st.session_state.students}

if 'history' not in st.session_state:
    st.session_state.history = []

# --- 3. ส่วนหัวและส่วนแก้ไขวันที่ ---
st.title("🏫 ระบบเช็คชื่อแบบยืนยันรายการ")

col_date, col_info = st.columns([1, 2])
with col_date:
    # ฟีเจอร์: แก้ไขวันที่ได้
    selected_date = st.date_input("📅 เลือกวันที่เช็คชื่อ", datetime.now())
    date_str = selected_date.strftime('%d/%m/%Y')

st.divider()

tab1, tab2, tab3 = st.tabs(["📋 หน้าเช็คชื่อ", "📜 ประวัติคะแนน", "⚙️ จัดการรายชื่อ"])

# --- TAB 1: หน้าเช็คชื่อ ---
with tab1:
    st.subheader(f"การเช็คชื่อประจำวันที่: {date_str}")
    
    # ตารางเช็คชื่อ
    h_col1, h_col2, h_col3, h_col4 = st.columns([1, 3, 2, 2])
    h_col1.write("**รหัส**")
    h_col2.write("**ชื่อ-นามสกุล**")
    h_col3.write("**เลือกสถานะ**")
    h_col4.write("**คะแนนปัจจุบัน**")

    for i, student in enumerate(st.session_state.students):
        s_id = student['id']
        cols = st.columns([1, 3, 2, 2])
        
        cols[0].write(f"`{s_id}`")
        cols[1].write(student['name'])
        
        # เลือกสถานะใส่ไว้ในตัวแปรชั่วคราว (ยังไม่บันทึกลงตัวหลัก)
        status_options = ["ยังไม่เช็ค", "มาเรียน", "สาย", "ขาด"]
        st.session_state.temp_status[s_id] = cols[2].selectbox(
            f"เลือกสถานะ {s_id}", 
            status_options, 
            key=f"select_{s_id}", 
            label_visibility="collapsed"
        )
        
        cols[3].write(f"{student['score']} คะแนน")

    st.write("")
    
    # --- ปุ่มยืนยันเพื่อตัดคะแนน ---
    st.markdown("### ⚠️ ยืนยันรายการ")
    if st.button("✅ ยืนยันการเช็คชื่อและหักคะแนนสำหรับวันนี้", type="primary", use_container_width=True):
        count_late = 0
        count_absent = 0
        
        for i, student in enumerate(st.session_state.students):
            s_id = student['id']
            status = st.session_state.temp_status[s_id]
            penalty = 0
            
            if status == "สาย":
                penalty = 2
                count_late += 1
            elif status == "ขาด":
                penalty = 5
                count_absent += 1
            
            # ทำการหักคะแนนจริง
            if penalty > 0:
                st.session_state.students[i]['score'] -= penalty
                # บันทึกประวัติ
                st.session_state.history.insert(0, {
                    "วันที่บันทึก": date_str,
                    "เวลา": datetime.now().strftime("%H:%M"),
                    "นักเรียน": student['name'],
                    "รายการ": f"เช็คชื่อ ({status})",
                    "หัก": f"-{penalty}",
                    "คะแนนเหลือ": st.session_state.students[i]['score']
                })
        
        st.success(f"บันทึกสำเร็จ! (สาย {count_late} คน, ขาด {count_absent} คน)")
        st.balloons()

# --- TAB 2: ประวัติคะแนน ---
with tab2:
    st.subheader("📜 ประวัติการทำรายการ")
    if st.session_state.history:
        st.table(pd.DataFrame(st.session_state.history))
    else:
        st.info("ยังไม่มีประวัติการหักคะแนน")

# --- TAB 3: จัดการรายชื่อ ---
# --- TAB 3: จัดการรายชื่อ ---
with tab3:

    st.subheader("➕ เพิ่ม/ลบ/แก้ไขรายชื่อ")

    # ---------- เพิ่มนักเรียน ----------
    with st.form("add_form"):
        aid = st.text_input("รหัสนักเรียน")
        aname = st.text_input("ชื่อ-นามสกุล")

        if st.form_submit_button("เพิ่มชื่อ"):
            if aid and aname:
                st.session_state.students.append({
                    "id": aid,
                    "name": aname,
                    "score": 100
                })

                st.session_state.temp_status[aid] = "ยังไม่เช็ค"

                st.success("เพิ่มนักเรียนสำเร็จ")
                st.rerun()

    st.divider()

    # ---------- ลบนักเรียน ----------
    del_list = [f"{s['id']} - {s['name']}" for s in st.session_state.students]

    to_del = st.selectbox("เลือกชื่อที่จะลบ", del_list)

    if st.button("ลบนักเรียน"):

        tid = to_del.split(" - ")[0]

        st.session_state.students = [
            s for s in st.session_state.students
            if s['id'] != tid
        ]

        st.success("ลบสำเร็จ")
        st.rerun()

    st.divider()

    # ---------- แก้ไขชื่อนักเรียน ----------
    st.subheader("✏️ แก้ไขชื่อนักเรียน")

    edit_list = [f"{s['id']} - {s['name']}" for s in st.session_state.students]

    selected_edit = st.selectbox("เลือกนักเรียนที่ต้องการแก้ไข", edit_list)

    edit_id = selected_edit.split(" - ")[0]

    student_data = next(s for s in st.session_state.students if s["id"] == edit_id)

    new_name = st.text_input("ชื่อใหม่", value=student_data["name"])

    if st.button("บันทึกการแก้ไข"):

        for s in st.session_state.students:
            if s["id"] == edit_id:
                s["name"] = new_name

        st.success("แก้ไขชื่อสำเร็จ")

        st.rerun()