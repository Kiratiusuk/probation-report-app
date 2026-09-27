import streamlit as st
from docxtpl import DocxTemplate
import io

# 1. ตั้งค่าหน้าเพจ
st.set_page_config(page_title="ระบบงานเอกสารจิตเวช", layout="centered", page_icon="🏥")

# --- CSS ตกแต่ง ---
st.markdown("""
<style>
    .main-title { color: #003366; text-align: center; font-weight: bold; margin-bottom: 5px; }
    .sub-title { color: #555555; text-align: center; font-size: 18px; margin-bottom: 30px; }
    hr { border-top: 2px solid #003366; }
    div.stButton > button { border-radius: 8px; border: 1px solid #003366; color: #003366; background-color: #ffffff; }
    div.stButton > button:hover { background-color: #003366; color: white; }
</style>
""", unsafe_allow_html=True)

# --- จัดการ State ---
if 'step' not in st.session_state: st.session_state.step = 1
if 'category' not in st.session_state: st.session_state.category = ""

# --- หัวกระดาษ ---
st.markdown("<h2 class='main-title'>🏥 ระบบรายงานและรับรองการบำบัด</h2>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>กลุ่มงานจิตเวชและยาเสพติด โรงพยาบาลพระนั่งเกล้า</p>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ==========================================
# หน้าที่ 1: เมนูหลัก 5 หมวดหมู่
# ==========================================
if st.session_state.step == 1:
    st.markdown("<h5 style='text-align: center; color: #003366; margin-bottom: 20px;'>โปรดเลือกหน่วยงานหรือประเภทเอกสาร</h5>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div style='text-align: center; font-size: 50px;'>⚖️</div>", unsafe_allow_html=True)
        if st.button("๑. ศาล", use_container_width=True):
            st.session_state.category = "ศาล"
            st.session_state.step = 2; st.rerun()
    with col2:
        st.markdown("<div style='text-align: center; font-size: 50px;'>🛡️</div>", unsafe_allow_html=True)
        if st.button("๒. คุมประพฤติ", use_container_width=True):
            st.session_state.category = "คุมประพฤติ"
            st.session_state.step = 2; st.rerun()
    with col3:
        st.markdown("<div style='text-align: center; font-size: 50px;'>🏫</div>", unsafe_allow_html=True)
        if st.button("๓. สถานพินิจ", use_container_width=True):
            st.session_state.category = "สถานพินิจ"
            st.session_state.step = 2; st.rerun()

    st.write("") 
    col4, col5, col6, col7 = st.columns([1, 2, 2, 1])
    with col5:
        st.markdown("<div style='text-align: center; font-size: 50px;'>🏢</div>", unsafe_allow_html=True)
        if st.button("๔. เอกชน", use_container_width=True):
            st.session_state.category = "เอกชน"
            st.session_state.step = 2; st.rerun()
    with col6:
        st.markdown("<div style='text-align: center; font-size: 50px;'>📑</div>", unsafe_allow_html=True)
        if st.button("๕. รับรอง ม.113/114", use_container_width=True):
            st.session_state.category = "หนังสือรับรอง"
            st.session_state.step = 2; st.rerun()

# ==========================================
# หน้าที่ 2: กรอกข้อมูลแยกตามหมวด
# ==========================================
elif st.session_state.step == 2:
    if st.button("⬅️ กลับหน้าเมนูหลัก"):
        st.session_state.step = 1; st.rerun()
        
    st.markdown(f"<h4 style='color: #003366; text-align: center;'>หมวด: {st.session_state.category}</h4>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    # ---------------------------------------------
    # 🛡️ 2.1 หมวดคุมประพฤติ
    # ---------------------------------------------
    if st.session_state.category == "คุมประพฤติ":
        
        # เลือกเมนูย่อย นนทบุรี / จังหวัดอื่น
        sub_category = st.radio("เลือกหน่วยงานปลายทาง:", ["คุมประพฤติจังหวัดนนทบุรี", "คุมประพฤติอื่น"], horizontal=True)
        
        if sub_category == "คุมประพฤติจังหวัดนนทบุรี":
            with st.container(border=True):
                st.markdown("<h5 style='color: #003366;'>บันทึกข้อมูล (จังหวัดนนทบุรี)</h5>", unsafe_allow_html=True)
                
                # 4 ช่องพื้นฐาน
                month_year = st.text_input("๑. เดือนและปี หนังสือ", placeholder="เช่น กันยายน ๒๕๖๙")
                ref_number = st.text_input("๒. อ้างอิงหนังสือคุมประพฤติเลขที่ นบ.๐๐๒๕ /", placeholder="เช่น ๐๐๑๒")
                ref_date = st.text_input("๓. อ้างอิงหนังสือคุมประพฤติวันที่", placeholder="เช่น ๕ ตุลาคม ๒๕๖๙")
                patient_name = st.text_input("๔. ชื่อผู้รับการบำบัด", placeholder="เช่น นายตั้งใจ บำบัด")
                
                # ข้อ 5. สาเหตุส่งเข้ารับการบำบัดรักษา
                st.markdown("---")
                referral_reason = st.selectbox("๕. สาเหตุส่งเข้ารับการบำบัดรักษา", ["ตามคำพิพากษา", "แบบสมัครใจ", "อื่นๆ (ระบุเอง)"])
                custom_reason = ""
                if referral_reason == "อื่นๆ (ระบุเอง)":
                    custom_reason = st.text_input("โปรดระบุสาเหตุด้วยตนเอง:", placeholder="พิมพ์สาเหตุที่นี่...")

                # ข้อ 6. สถานะการบำบัด
                st.markdown("---")
                status = st.selectbox("๖. สถานะการบำบัด", [
                    "บำบัดครบ", 
                    "บำบัดไม่ครบ", 
                    "ไม่มารายงานตัว", 
                    "ขอย้ายสถานบำบัด", 
                    "ส่งตัวไปรักษาต่อ"
                ])
                
                # ตัวแปรสำหรับรับค่าเสริม
                num_times, hospital_name, reason = "", "", ""
                send_to, refer_reason = "", ""
                
                # กรณีขอย้ายสถานบำบัด
                if status == "ขอย้ายสถานบำบัด":
                    st.info("ระบุข้อมูลการย้ายสถานบำบัด:")
                    num_times = st.text_input("- ได้เข้ารับการฟื้นฟูฯ จำนวนกี่ครั้ง (ใส่เฉพาะตัวเลข)", placeholder="เช่น ๔")
                    hospital_name = st.text_input("- ขอย้ายไปที่ไหน (ชื่อ รพ. หรือ สถานที่บำบัด และ จังหวัด)", placeholder="เช่น โรงพยาบาลสมเด็จพระเจ้าตากสินมหาราช จังหวัดตาก")
                    reason = st.text_input("- เนื่องจากอะไร", placeholder="เช่น ย้ายสถานที่ทำงาน")
                
                # กรณีส่งตัวไปรักษาต่อ (Refer)
                elif status == "ส่งตัวไปรักษาต่อ":
                    st.warning("ระบบจะสลับไปใช้แบบฟอร์ม 'คุมประพฤติ Refer.docx' อัตโนมัติ")
                    
                    # ตัวเลือกสถานที่ส่งตัว
                    send_to_choice = st.selectbox("- ส่งตัวไปยัง", ["สถาบันบำบัดรักษาและฟื้นฟูผู้ติดยาเสพติดแห่งชาติบรมราชชนนี", "โรงพยาบาลศรีธัญญา", "อื่นๆ (ระบุเอง)"])
                    if send_to_choice == "อื่นๆ (ระบุเอง)":
                        send_to = st.text_input("โปรดระบุสถานที่ส่งตัว:")
                    else:
                        send_to = send_to_choice
                    
                    # ตัวเลือกสาเหตุการส่งตัว
                    refer_reason_choice = st.selectbox("- สาเหตุการส่งตัว", ["บำบัดแบบผู้ป่วยนอกไม่สำเร็จ", "มีปัญหาด้านอารมณ์และพฤติกรรมที่อาจเป็นอันตรายเนื่องจากยาเสพติด", "อื่นๆ (ระบุเอง)"])
                    if refer_reason_choice == "อื่นๆ (ระบุเอง)":
                        refer_reason = st.text_input("โปรดระบุสาเหตุการส่งตัว:")
                    else:
                        refer_reason = refer_reason_choice

                st.markdown("<br>", unsafe_allow_html=True)
                submit_btn = st.button("📄 สร้างเอกสาร Word", type="primary", use_container_width=True)

            # เมื่อกดปุ่มสร้างเอกสาร
            if submit_btn:
                
                # --- จัดการข้อความ สาเหตุที่เข้ารับการบำบัด ---
                reason_text_final = ""
                if referral_reason == "ตามคำพิพากษา":
                    reason_text_final = "ตามคำพิพากษาของศาล"
                elif referral_reason == "แบบสมัครใจ":
                    # แก้ไขข้อความตรงนี้ตามที่คุณแจ้งมาครับ
                    reason_text_final = "การติดยาเสพติดให้โทษแบบสมัครใจ"
                else:
                    reason_text_final = custom_reason

                # --- จัดการข้อความ สถานะการบำบัด และ เลือกไฟล์ต้นแบบ ---
                template_name = "คุมประพฤติรวม.docx"
                status_text = ""
                
                if status == "บำบัดครบ":
                    status_text = "ได้เข้ารับการฟื้นฟูฯ ครบตามระยะเวลาที่กำหนด"
                elif status == "บำบัดไม่ครบ":
                    status_text = "ได้มารายงานตัวเพื่อเข้ารับการรักษาการติดยาเสพติดและเข้ารับการบำบัดฟื้นฟูฯ แต่ไม่ครบตามระยะเวลาที่กำหนด"
                elif status == "ไม่มารายงานตัว":
                    status_text = "ไม่ได้มารายงานตัวเพื่อเข้ารับการรักษาและเข้ารับการฟื้นฟูฯ ตามระยะเวลาที่กำหนด"
                elif status == "ขอย้ายสถานบำบัด":
                    status_text = f"ได้เข้ารับการฟื้นฟูฯ จำนวน {num_times} ครั้ง และแจ้งขอย้ายสถานบำบัดไปยัง{hospital_name} เนื่องจาก{reason}"
                elif status == "ส่งตัวไปรักษาต่อ":
                    template_name = "คุมประพฤติ Refer.docx"
                    
                # 2. จัดคู่ข้อมูลเพื่อส่งไป Word
                try:
                    doc = DocxTemplate(template_name)
                    context = {
                        "เดือนและปีหนังสือออก": month_year,
                        "เลขหนังสือคุมประพฤติ": ref_number,
                        "ลงวันที่": ref_date,
                        "ชื่อผู้รับการบำบัด": patient_name,
                        "สาเหตุส่งเข้ารับการบำบัดรักษา": reason_text_final  
                    }
                    
                    # ถ้าเป็น Refer ส่ง 2 ตัวนี้ไปเพิ่ม ถ้าไม่ใช่ ส่งสถานะบำบัดไป
                    if status == "ส่งตัวไปรักษาต่อ":
                        context["ส่งตัวไปยัง"] = send_to
                        context["สาเหตุการส่งตัว"] = refer_reason
                    else:
                        context["สถานะการบำบัด"] = status_text
                    
                    doc.render(context)
                    
                    bio = io.BytesIO()
                    doc.save(bio)
                    
                    st.success(f"✅ สร้างเอกสาร '{status}' ของ {patient_name} สำเร็จ!")
                    st.download_button(
                        label="⬇️ ดาวน์โหลดไฟล์เอกสาร (Word)",
                        data=bio.getvalue(),
                        file_name=f"คุมประพฤติ_{status}_{patient_name}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        type="primary"
                    )
                    
                except Exception as e:
                    st.error(f"❌ ไม่พบไฟล์ต้นแบบ '{template_name}' หรือมีข้อผิดพลาด: {str(e)}")
                    st.error("โปรดตรวจสอบว่าได้อัปโหลดไฟล์ Word ขึ้น GitHub ถูกต้องแล้วครับ")

        elif sub_category == "คุมประพฤติอื่น":
            st.info("📍 กำลังอยู่ระหว่างการพัฒนาช่องกรอกข้อมูลสำหรับคุมประพฤติจังหวัดอื่นครับ")
            
    # ---------------------------------------------
    # 2.2 หมวดอื่นๆ
    # ---------------------------------------------
    else:
        st.info(f"📍 ท่านเข้าสู่หมวด **{st.session_state.category}**")
        st.write("ฟอร์มในหมวดหมู่นี้อยู่ระหว่างการพัฒนาช่องกรอกข้อมูลครับ")