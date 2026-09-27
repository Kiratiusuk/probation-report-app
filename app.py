import streamlit as st
from docxtpl import DocxTemplate
import io

# 1. ตั้งค่าหน้าเพจ
st.set_page_config(page_title="ระบบงานเอกสารจิตเวช", layout="centered", page_icon="🏥")

# --- การตกแต่งด้วย CSS สไตล์ทางการ (สีน้ำเงินกรมท่า) ---
st.markdown("""
<style>
    .main-title {
        color: #003366;
        text-align: center;
        font-family: 'Sarabun', Tahoma, sans-serif;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .sub-title {
        color: #555555;
        text-align: center;
        font-size: 18px;
        margin-bottom: 30px;
    }
    hr {
        border-top: 2px solid #003366;
    }
    /* ปรับแต่งปุ่มกดให้เข้ากับธีมสีน้ำเงินกรมท่า */
    div.stButton > button {
        border-radius: 8px;
        border: 1px solid #003366;
        color: #003366;
        transition: 0.3s;
        background-color: #ffffff;
    }
    div.stButton > button:hover {
        background-color: #003366;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# --- ระบบจดจำหน้าเว็บว่าอยู่ขั้นตอนไหน ---
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'category' not in st.session_state:
    st.session_state.category = ""
if 'form_type' not in st.session_state:
    st.session_state.form_type = ""

# --- ส่วนหัวกระดาษ ---
st.markdown("<h2 class='main-title'>🏥 ระบบรายงานและรับรองการบำบัด</h2>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>กลุ่มงานจิตเวชและยาเสพติด โรงพยาบาลพระนั่งเกล้า</p>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ==========================================
# หน้าที่ 1: เมนูหลัก 5 หมวดหมู่
# ==========================================
if st.session_state.step == 1:
    st.markdown("<h5 style='text-align: center; color: #003366; margin-bottom: 20px;'>โปรดเลือกหน่วยงานหรือประเภทเอกสารที่ต้องการจัดทำ</h5>", unsafe_allow_html=True)
    
    # แถวที่ 1: แบ่งเป็น 3 คอลัมน์ (ศาล, คุมประพฤติ, สถานพินิจ)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<div style='text-align: center; font-size: 50px;'>⚖️</div>", unsafe_allow_html=True)
        if st.button("๑. ศาล", use_container_width=True):
            st.session_state.category = "ศาล"
            st.session_state.step = 2
            st.rerun()
            
    with col2:
        st.markdown("<div style='text-align: center; font-size: 50px;'>🛡️</div>", unsafe_allow_html=True)
        if st.button("๒. คุมประพฤติ", use_container_width=True):
            st.session_state.category = "คุมประพฤติ"
            st.session_state.step = 2
            st.rerun()
            
    with col3:
        st.markdown("<div style='text-align: center; font-size: 50px;'>🏫</div>", unsafe_allow_html=True)
        if st.button("๓. สถานพินิจ", use_container_width=True):
            st.session_state.category = "สถานพินิจ"
            st.session_state.step = 2
            st.rerun()

    st.write("") # เว้นบรรทัด
    
    # แถวที่ 2: แบ่งคอลัมน์ให้อยู่ตรงกลาง (เอกชน, ม.113/114)
    col4, col5, col6, col7 = st.columns([1, 2, 2, 1])
    
    with col5:
        st.markdown("<div style='text-align: center; font-size: 50px;'>🏢</div>", unsafe_allow_html=True)
        if st.button("๔. เอกชน", use_container_width=True):
            st.session_state.category = "เอกชน"
            st.session_state.step = 2
            st.rerun()
            
    with col6:
        st.markdown("<div style='text-align: center; font-size: 50px;'>📑</div>", unsafe_allow_html=True)
        if st.button("๕. รับรอง ม.113/114", use_container_width=True):
            st.session_state.category = "หนังสือรับรอง"
            st.session_state.step = 2
            st.rerun()

# ==========================================
# หน้าที่ 2: หน้าต่างกรอกข้อมูลของแต่ละหมวด
# ==========================================
elif st.session_state.step == 2:
    # ปุ่มย้อนกลับ
    if st.button("⬅️ กลับไปหน้าเมนูหลัก"):
        st.session_state.step = 1
        st.rerun()
        
    st.markdown(f"<h4 style='color: #003366; text-align: center;'>หมวด: {st.session_state.category}</h4>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    # ---------------------------------------------
    # 2.1 กรณีเลือก "คุมประพฤติ" (ฟอร์มที่เราทำเสร็จแล้วเมื่อวาน)
    # ---------------------------------------------
    if st.session_state.category == "คุมประพฤติ":
        
        st.session_state.form_type = st.selectbox(
            "โปรดเลือกแบบฟอร์มรายงานคุมประพฤติ:", 
            ["คุมประพฤติ ครบโปรแกรม", "คุมประพฤติ ไม่ครบโปรแกรม"]
        )
        
        with st.container(border=True):
            st.markdown(f"<h5 style='color: #003366;'>บันทึกข้อมูล ({st.session_state.form_type})</h5>", unsafe_allow_html=True)
            
            month_year = st.text_input("เดือนและปี หนังสือ", placeholder="เช่น กันยายน ๒๕๖๙")
            ref_number = st.text_input("อ้างอิงหนังสือคุมประพฤติเลขที่ นบ.๐๐๒๕ /", placeholder="เช่น ๐๐๑๒")
            ref_date = st.text_input("อ้างอิงหนังสือคุมประพฤติวันที่", placeholder="เช่น ๕ ตุลาคม ๒๕๖๙")
            patient_name = st.text_input("ชื่อผู้รับการบำบัด", placeholder="เช่น นายตั้งใจ บำบัด")

            st.markdown("<br>", unsafe_allow_html=True)
            submit_btn = st.button("สร้างเอกสาร", type="primary", use_container_width=True)

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
                
                st.success(f"✅ สร้างเอกสารของ {patient_name} สำเร็จ! กรุณากดดาวน์โหลดด้านล่าง")
                st.download_button(
                    label="ดาวน์โหลดไฟล์เอกสาร (Word)",
                    data=bio.getvalue(),
                    file_name=f"รายงาน_{patient_name}_{template_name}",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    type="primary"
                )
                
            except Exception as e:
                st.error(f"ไม่พบไฟล์ต้นแบบ '{template_name}' โปรดตรวจสอบในระบบอีกครั้ง")

    # ---------------------------------------------
    # 2.2 กรณีเลือกหมวดอื่นๆ (เตรียมไว้สำหรับอนาคต)
    # ---------------------------------------------
    else:
        st.info(f"📍 ท่านเข้าสู่หมวด **{st.session_state.category}**")
        st.write("ฟอร์มในหมวดหมู่นี้อยู่ระหว่างการพัฒนาช่องกรอกข้อมูลครับ...")
        st.write("ถ้าคุณเตรียมแบบฟอร์ม Word ของหมวดนี้ และรู้แล้วว่าอยากให้มีช่องกรอกอะไรบ้าง พิมพ์บอกผมได้เลยครับ เราจะเอามาเชื่อมต่อให้สมบูรณ์เหมือนของคุมประพฤติเลย!")