import streamlit as st
from docxtpl import DocxTemplate
import io

# 1. ตั้งค่าหน้าเพจ
st.set_page_config(page_title="ระบบหนังสือคุมประพฤติ", page_icon="⚖️", layout="centered")

# --- ส่วนจัดการความจำของหน้าเว็บ (Session State) ---
if 'step' not in st.session_state:
    st.session_state.step = 1 # เริ่มต้นที่หน้าที่ 1 เสมอ
if 'form_type' not in st.session_state:
    st.session_state.form_type = "คุมประพฤติ ครบโปรแกรม"

st.title("⚖️ ระบบออกหนังสือรายงานคุมประพฤติ")
st.markdown("**โรงพยาบาลพระนั่งเกล้า**")
st.markdown("---")

# ==========================================
# หน้าที่ 1: เลือกแบบฟอร์ม
# ==========================================
if st.session_state.step == 1:
    st.subheader("📑 ขั้นตอนที่ 1: เลือกแบบฟอร์มที่ต้องการ")
    
    # ใช้กรอบเพื่อให้ดูสวยงาม
    with st.container(border=True):
        st.session_state.form_type = st.radio(
            "โปรดคลิกเลือกประเภทรายงาน:", 
            ["คุมประพฤติ ครบโปรแกรม", "คุมประพฤติ ไม่ครบโปรแกรม"]
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ปุ่มกดไปหน้าถัดไป
        if st.button("ถัดไป ➡️", type="primary", use_container_width=True):
            st.session_state.step = 2
            st.rerun() # สั่งให้เว็บโหลดหน้าใหม่เพื่อไปหน้าที่ 2

# ==========================================
# หน้าที่ 2: กรอกข้อมูล
# ==========================================
elif st.session_state.step == 2:
    st.subheader(f"📝 ขั้นตอนที่ 2: กรอกข้อมูล ({st.session_state.form_type})")
    
    with st.container(border=True):
        month_year = st.text_input("เดือนและปี หนังสือ", placeholder="เช่น กันยายน ๒๕๖๙")
        ref_number = st.text_input("อ้างอิงหนังสือคุมประพฤติเลขที่ นบ.๐๐๒๕ /", placeholder="เช่น ๐๐๑๒")
        ref_date = st.text_input("อ้างอิงหนังสือคุมประพฤติวันที่", placeholder="เช่น ๕ ตุลาคม ๒๕๖๙")
        patient_name = st.text_input("ชื่อผู้รับการบำบัด", placeholder="เช่น นายตั้งใจ บำบัด")

        st.markdown("<br>", unsafe_allow_html=True)
        
        # แบ่งคอลัมน์สำหรับปุ่มย้อนกลับ และ ปุ่มสร้างเอกสาร
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ ย้อนกลับ", use_container_width=True):
                st.session_state.step = 1
                st.rerun() # สั่งให้เว็บกลับไปหน้าที่ 1
        with col2:
            submit_btn = st.button("📄 สร้างเอกสาร", type="primary", use_container_width=True)

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
            
            st.success(f"✅ สร้างเอกสารของ {patient_name} สำเร็จ! กดดาวน์โหลดด้านล่างได้เลยครับ")
            st.download_button(
                label="⬇️ ดาวน์โหลดไฟล์ Word",
                data=bio.getvalue(),
                file_name=f"รายงาน_{patient_name}_{template_name}",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
            
        except Exception as e:
            st.error(f"❌ ไม่พบไฟล์ต้นแบบ '{template_name}' โปรดตรวจสอบว่ามีไฟล์นี้ในเครื่อง/GitHub หรือยังครับ")