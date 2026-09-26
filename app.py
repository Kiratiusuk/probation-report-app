import streamlit as st
from docxtpl import DocxTemplate
import io

# 1. ตั้งค่าหน้าเพจ
st.set_page_config(page_title="ระบบหนังสือคุมประพฤติ", page_icon="⚖️", layout="centered")

st.title("⚖️ ระบบออกหนังสือรายงานคุมประพฤติ")
st.markdown("โรงพยาบาลพระนั่งเกล้า")
st.markdown("---")

# 2. เมนูให้เลือกประเภทของฟอร์ม
form_type = st.radio(
    "👉 1. โปรดเลือกแบบฟอร์มที่ต้องการ:", 
    ["คุมประพฤติ ครบโปรแกรม", "คุมประพฤติ ไม่ครบโปรแกรม"], 
    horizontal=True
)

st.markdown("---")
st.subheader(f"📝 2. กรอกข้อมูลสำหรับ: {form_type}")

# 3. ช่องกรอกข้อมูล (ใช้ placeholder เพื่อแสดงตัวอย่างจางๆ)
month_year = st.text_input("เดือนและปี หนังสือ", placeholder="เช่น กันยายน ๒๕๖๙")
ref_number = st.text_input("อ้างอิงหนังสือคุมประพฤติเลขที่ นบ.๐๐๒๕ /", placeholder="เช่น ๐๐๑๒")
ref_date = st.text_input("อ้างอิงหนังสือคุมประพฤติวันที่", placeholder="เช่น ๕ ตุลาคม ๒๕๖๙")
patient_name = st.text_input("ชื่อผู้รับการบำบัด", placeholder="เช่น นายตั้งใจ บำบัด")

# 4. ปุ่มกดสร้างเอกสาร
st.markdown("---")
if st.button("📄 สร้างเอกสาร", type="primary", use_container_width=True):
    
    # โปรแกรมจะเลือกไฟล์ Word ตามที่ผู้ใช้คลิกเลือกด้านบน
    if form_type == "คุมประพฤติ ครบโปรแกรม":
        template_name = "คุมประพฤติ ครบ.docx"
    else:
        template_name = "คุมประพฤติ ไม่ครบ.docx"
        
    try:
        # เปิดไฟล์ Word ต้นแบบที่เลือก
        doc = DocxTemplate(template_name)
        
        # จัดคู่ข้อมูลที่กรอก ให้ตรงกับในวงเล็บของไฟล์ Word
        context = {
            "เดือนและปีหนังสือออก": month_year,
            "เลขหนังสือคุมประพฤติ": ref_number,
            "ลงวันที่": ref_date,
            "ชื่อผู้รับการบำบัด": patient_name
        }
        
        # สั่งประมวลผล
        doc.render(context)
        
        # เตรียมไฟล์สำหรับดาวน์โหลด
        bio = io.BytesIO()
        doc.save(bio)
        
        st.success(f"✅ สร้างเอกสารของ {patient_name} สำเร็จ! กดดาวน์โหลดด้านล่างได้เลยครับ")
        
        # ปุ่มดาวน์โหลด
        st.download_button(
            label="⬇️ ดาวน์โหลดไฟล์ Word",
            data=bio.getvalue(),
            file_name=f"รายงาน_{patient_name}_{template_name}",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        
    except Exception as e:
        # แจ้งเตือนถ้าลืมอัปโหลดไฟล์ Word
        st.error(f"❌ ไม่พบไฟล์ต้นแบบ '{template_name}' โปรดตรวจสอบใน GitHub ว่าอัปโหลดไฟล์นี้หรือยังครับ")