import streamlit as st
from docxtpl import DocxTemplate
import io

# 1. ตั้งค่าหน้าเพจ
st.set_page_config(page_title="ระบบงานเอกสารจิตเวช", layout="centered")

# --- จัดการความจำของหน้าเว็บ ---
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'form_type' not in st.session_state:
    st.session_state.form_type = ""

# 2. ส่วนหัวของโปรแกรม (ปรับแต่งสีตัวอักษรให้เป็นสีน้ำเงินกรมท่าแบบทางการ)
st.markdown("<h2 style='text-align: center; color: #003366;'>ระบบจัดทำหนังสือรายงานการคุมประพฤติ</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px; color: #555555;'>กลุ่มงานจิตเวชและยาเสพติด โรงพยาบาลพระนั่งเกล้า</p>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid #cccccc;'>", unsafe_allow_html=True)

# ==========================================
# หน้าที่ 1: เลือกแบบฟอร์ม (เปลี่ยนเป็นปุ่มกดขนาดใหญ่)
# ==========================================
if st.session_state.step == 1:
    st.markdown("<h5 style='color: #333333;'>ส่วนที่ ๑ : เลือกประเภทเอกสารที่ต้องการจัดทำ</h5>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # สร้างปุ่ม 2 ปุ่มเรียงคู่กัน
    col1, col2 = st.columns(2)
    with col1:
        # หากกดปุ่มนี้ ให้บันทึกค่าและไปหน้าที่ 2
        if st.button("📄 หนังสือรายงาน (ครบโปรแกรม)", use_container_width=True):
            st.session_state.form_type = "คุมประพฤติ ครบโปรแกรม"
            st.session_state.step = 2
            st.rerun()
            
    with col2:
        if st.button("📄 หนังสือรายงาน (ไม่ครบโปรแกรม)", use_container_width=True):
            st.session_state.form_type = "คุมประพฤติ ไม่ครบโปรแกรม"
            st.session_state.step = 2
            st.rerun()
            
    st.markdown("<br><p style='text-align: center; color: gray; font-size: 14px;'>* โปรดคลิกที่ปุ่มรายการเพื่อเข้าสู่หน้าต่างบันทึกข้อมูล</p>", unsafe_allow_html=True)

# ==========================================
# หน้าที่ 2: กรอกข้อมูล
# ==========================================
elif st.session_state.step == 2:
    st.markdown(f"<h5 style='color: #003366;'>ส่วนที่ ๒ : บันทึกข้อมูล ({st.session_state.form_type})</h5>", unsafe_allow_html=True)
    
    with st.container(border=True):
        month_year = st.text_input("เดือนและปี หนังสือ", placeholder="เช่น กันยายน ๒๕๖๙")
        ref_number = st.text_input("อ้างอิงหนังสือคุมประพฤติเลขที่ นบ.๐๐๒๕ /", placeholder="เช่น ๐๐๑๒")
        ref_date = st.text_input("อ้างอิงหนังสือคุมประพฤติวันที่", placeholder="เช่น ๕ ตุลาคม ๒๕๖๙")
        patient_name = st.text_input("ชื่อผู้รับการบำบัด", placeholder="เช่น นายตั้งใจ บำบัด")

        st.markdown("<br>", unsafe_allow_html=True)
        
        # แบ่งปุ่มย้อนกลับ และ ปุ่มสร้างเอกสาร
        col1, col2 = st.columns(2)
        with col1:
            if st.button("ย้อนกลับ", use_container_width=True):
                st.session_state.step = 1
                st.rerun()
        with col2:
            submit_btn = st.button("สร้างเอกสาร", type="primary", use_container_width=True)

    # เมื่อกดปุ่มสร้างเอกสาร
    if submit_btn:
        if st.session_state.form_type == "คุมประพฤติ ครบโปรแกรม":
            template_name = "คุมประพฤติ ครบ.docx"
        else:
            template_name = "คุมประพฤติ ไม่ครบ.docx"
            
        try:
            doc = DocxTemplate(template_name)
            context = {
                "เดือนและปีหนังสือออก": month_year,
                "เลขหนังสือคุมประพฤติ": ref_number,
                "ลงวันที่": ref_date,
                "ชื่อผู้รับการบำบัด": patient_name
            }
            doc.render(context)
            
            bio = io.BytesIO()
            doc.save(bio)
            
            st.success(f"สร้างเอกสารของ {patient_name} สำเร็จ! กรุณากดดาวน์โหลดด้านล่าง")
            st.download_button(
                label="ดาวน์โหลดไฟล์เอกสาร (Word)",
                data=bio.getvalue(),
                file_name=f"รายงาน_{patient_name}_{template_name}",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                type="primary"
            )
            
        except Exception as e:
            st.error(f"ไม่พบไฟล์ต้นแบบ '{template_name}' โปรดตรวจสอบในระบบอีกครั้ง")