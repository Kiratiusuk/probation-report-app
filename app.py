import streamlit as st
from docxtpl import DocxTemplate
import io

# 1. ตั้งค่าหน้าเพจ
st.set_page_config(page_title="ระบบงานเอกสารจิตเวช", layout="centered", page_icon="🏥")

# --- CSS ตกแต่งธีมสีดำ-น้ำเงิน (Dark Navy Elegant) ---
st.markdown("""
<style>
    /* บังคับพื้นหลังสีดำ/กรมท่าเข้ม และตัวหนังสือสีสว่าง */
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
    }
    /* ปรับแต่งหัวข้อ */
    .main-title { 
        color: #60a5fa; 
        text-align: center; 
        font-weight: bold; 
        margin-bottom: 5px; 
    }
    .sub-title { 
        color: #94a3b8; 
        text-align: center; 
        font-size: 18px; 
        margin-bottom: 30px; 
    }
    hr { border-top: 1px solid #1e3a8a; }
    
    /* ปรับแต่งปุ่มกดทั่วไป */
    div.stButton > button {
        border-radius: 8px;
        border: 1px solid #1e3a8a;
        color: #bfdbfe;
        background-color: #0f172a;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #1e3a8a;
        color: white;
        border: 1px solid #3b82f6;
        box-shadow: 0px 4px 10px rgba(30, 58, 138, 0.6);
        transform: scale(1.02);
    }
    /* ปรับแต่งปุ่มหลัก (ปุ่มสร้างเอกสาร) ให้เป็นสีน้ำเงินเด่นชัด */
    div.stButton > button[kind="primary"] {
        background-color: #1d4ed8;
        color: white;
        border: none;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #2563eb;
        box-shadow: 0px 4px 15px rgba(37, 99, 235, 0.4);
    }
    
    /* ส่วนของเครดิตด้านล่างสุด */
    .footer {
        text-align: center;
        font-size: 13px;
        color: #64748b;
        margin-top: 60px;
        margin-bottom: 20px;
    }
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
# หน้าที่ 1: เมนูหลัก 5 หมวดหมู่ (จัดเรียงใหม่ตามลำดับ)
# ==========================================
if st.session_state.step == 1:
    st.markdown("<h5 style='text-align: center; color: #60a5fa; margin-bottom: 20px;'>โปรดเลือกหน่วยงานหรือประเภทเอกสาร</h5>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div style='text-align: center; font-size: 50px;'>🛡️</div>", unsafe_allow_html=True)
        if st.button("๑. คุมประพฤติ", use_container_width=True):
            st.session_state.category = "คุมประพฤติ"
            st.session_state.step = 2; st.rerun()
    with col2:
        st.markdown("<div style='text-align: center; font-size: 50px;'>⚖️</div>", unsafe_allow_html=True)
        if st.button("๒. ศาล", use_container_width=True):
            st.session_state.category = "ศาล"
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
        # เปลี่ยนชื่อปุ่มเป็นแบบเต็มตามที่ต้องการ
        if st.button("๕. หนังสือรับรองผลการบำบัด(ม.113/114)", use_container_width=True):
            st.session_state.category = "หนังสือรับรองการบำบัด"
            st.session_state.step = 2; st.rerun()

# ==========================================
# หน้าที่ 2: กรอกข้อมูลแยกตามหมวด
# ==========================================
elif st.session_state.step == 2:
    if st.button("⬅️ กลับหน้าเมนูหลัก"):
        st.session_state.step = 1; st.rerun()
        
    # ปรับชื่อหมวดให้แสดงผลถูกต้องบนหน้าต่างที่ 2
    display_category = "หนังสือรับรองผลการบำบัด(ม.113/114)" if st.session_state.category == "หนังสือรับรองการบำบัด" else st.session_state.category
    st.markdown(f"<h4 style='color: #60a5fa; text-align: center;'>หมวด: {display_category}</h4>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    # ---------------------------------------------
    # 🛡️ 2.1 หมวดคุมประพฤติ (เลื่อนขึ้นมาเป็นอันดับแรก)
    # ---------------------------------------------
    if st.session_state.category == "คุมประพฤติ":
        sub_category = st.radio("เลือกหน่วยงานปลายทาง:", ["คุมประพฤติจังหวัดนนทบุรี", "คุมประพฤติอื่น"], horizontal=True)
        
        if sub_category == "คุมประพฤติจังหวัดนนทบุรี":
            with st.container(border=True):
                st.markdown("<h5 style='color: #60a5fa;'>บันทึกข้อมูล (จังหวัดนนทบุรี)</h5>", unsafe_allow_html=True)
                
                month_year = st.text_input("๑. เดือนและปี หนังสือ", placeholder="เช่น กันยายน ๒๕๖๙")
                ref_number = st.text_input("๒. อ้างอิงหนังสือคุมประพฤติเลขที่ นบ.๐๐๒๕ /", placeholder="เช่น ๐๐๑๒")
                ref_date = st.text_input("๓. อ้างอิงหนังสือคุมประพฤติวันที่", placeholder="เช่น ๕ ตุลาคม ๒๕๖๙")
                patient_name = st.text_input("๔. ชื่อผู้รับการบำบัด", placeholder="เช่น นายตั้งใจ บำบัด")
                
                st.markdown("---")
                referral_reason = st.selectbox("๕. สาเหตุส่งเข้ารับการบำบัดรักษา", ["ตามคำพิพากษา", "แบบสมัครใจ", "อื่นๆ (ระบุเอง)"])
                custom_reason = ""
                if referral_reason == "อื่นๆ (ระบุเอง)":
                    custom_reason = st.text_input("โปรดระบุสาเหตุด้วยตนเอง:", placeholder="พิมพ์สาเหตุที่นี่...")

                st.markdown("---")
                status = st.selectbox("๖. สถานะการบำบัด", ["บำบัดครบ", "บำบัดไม่ครบ", "ไม่มารายงานตัว", "ขอย้ายสถานบำบัด", "ส่งตัวไปรักษาต่อ"])
                
                num_times, hospital_name, reason = "", "", ""
                send_to, refer_reason = "", ""
                
                if status == "ขอย้ายสถานบำบัด":
                    st.info("ระบุข้อมูลการย้ายสถานบำบัด:")
                    num_times = st.text_input("- ได้เข้ารับการฟื้นฟูฯ จำนวนกี่ครั้ง (ใส่เฉพาะตัวเลข)", placeholder="เช่น ๔")
                    hospital_name = st.text_input("- ขอย้ายไปที่ไหน (ชื่อ รพ. หรือ สถานที่บำบัด และ จังหวัด)", placeholder="เช่น โรงพยาบาลสมเด็จพระเจ้าตากสินมหาราช จังหวัดตาก")
                    reason = st.text_input("- เนื่องจากอะไร", placeholder="เช่น ย้ายสถานที่ทำงาน")
                
                elif status == "ส่งตัวไปรักษาต่อ":
                    st.warning("ระบบจะสลับไปใช้แบบฟอร์ม 'คุมประพฤติ Refer.docx' อัตโนมัติ")
                    send_to_choice = st.selectbox("- ส่งตัวไปยัง", ["สถาบันบำบัดรักษาและฟื้นฟูผู้ติดยาเสพติดแห่งชาติบรมราชชนนี", "โรงพยาบาลศรีธัญญา", "อื่นๆ (ระบุเอง)"])
                    if send_to_choice == "อื่นๆ (ระบุเอง)":
                        send_to = st.text_input("โปรดระบุสถานที่ส่งตัว:")
                    else:
                        send_to = send_to_choice
                    
                    refer_reason_choice = st.selectbox("- สาเหตุการส่งตัว", ["บำบัดแบบผู้ป่วยนอกไม่สำเร็จ มีปัญหาด้านอารมณ์และพฤติกรรมที่อาจเป็นอันตรายเนื่องจากยาเสพติด", "อื่นๆ (ระบุเอง)"])
                    if refer_reason_choice == "อื่นๆ (ระบุเอง)":
                        refer_reason = st.text_input("โปรดระบุสาเหตุการส่งตัว:")
                    else:
                        refer_reason = refer_reason_choice

                st.markdown("<br>", unsafe_allow_html=True)
                submit_btn = st.button("📄 สร้างเอกสาร Word", type="primary", use_container_width=True)

            if submit_btn:
                reason_text_final = ""
                if referral_reason == "ตามคำพิพากษา": reason_text_final = "ตามคำพิพากษาของศาล"
                elif referral_reason == "แบบสมัครใจ": reason_text_final = "การติดยาเสพติดให้โทษแบบสมัครใจ"
                else: reason_text_final = custom_reason

                template_name = "คุมประพฤติรวม.docx"
                status_text = ""
                if status == "บำบัดครบ": status_text = "ได้เข้ารับการฟื้นฟูฯ ครบตามระยะเวลาที่กำหนด"
                elif status == "บำบัดไม่ครบ": status_text = "ได้มารายงานตัวเพื่อเข้ารับการรักษาการติดยาเสพติดและเข้ารับการบำบัดฟื้นฟูฯ แต่ไม่ครบตามระยะเวลาที่กำหนด"
                elif status == "ไม่มารายงานตัว": status_text = "ไม่ได้มารายงานตัวเพื่อเข้ารับการรักษาและเข้ารับการฟื้นฟูฯ ตามระยะเวลาที่กำหนด"
                elif status == "ขอย้ายสถานบำบัด": status_text = f"ได้เข้ารับการฟื้นฟูฯ จำนวน {num_times} ครั้ง และแจ้งขอย้ายสถานบำบัดไปยัง{hospital_name} เนื่องจาก{reason}"
                elif status == "ส่งตัวไปรักษาต่อ": template_name = "คุมประพฤติ Refer.docx"
                    
                try:
                    doc = DocxTemplate(template_name)
                    context = {
                        "เดือนและปีหนังสือออก": month_year,
                        "เลขหนังสือคุมประพฤติ": ref_number,
                        "ลงวันที่": ref_date,
                        "ชื่อผู้รับการบำบัด": patient_name,
                        "สาเหตุส่งเข้ารับการบำบัดรักษา": reason_text_final  
                    }
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
                        label="⬇️ ดาวน์โหลดไฟล์เอกสาร (Word)", data=bio.getvalue(),
                        file_name=f"คุมประพฤติ_{status}_{patient_name}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        type="primary"
                    )
                except Exception as e:
                    st.error(f"❌ ไม่พบไฟล์ต้นแบบ '{template_name}' หรือมีข้อผิดพลาด: {str(e)}")

        elif sub_category == "คุมประพฤติอื่น":
            with st.container(border=True):
                st.markdown("<h5 style='color: #60a5fa;'>บันทึกข้อมูล (คุมประพฤติจังหวัดอื่น)</h5>", unsafe_allow_html=True)
                
                agency_name = st.text_input("๑. หน่วยงานที่ส่งมา", placeholder="เช่น คุมประพฤติกรุงเทพมหานคร ๒")
                month_year_other = st.text_input("๒. เดือนและปี หนังสือ", placeholder="เช่น กันยายน ๒๕๖๙", key="month_other")
                ref_number_other = st.text_input("๓. อ้างอิงหนังสือคุมประพฤติเลขที่", placeholder="เช่น ยธ ๐๓๑๐/๘๔๖๖ (โปรดพิมพ์ให้ครบถ้วน)", key="ref_other")
                ref_date_other = st.text_input("๔. อ้างอิงหนังสือคุมประพฤติวันที่", placeholder="เช่น ๕ ตุลาคม ๒๕๖๙", key="date_other")
                patient_name_other = st.text_input("๕. ชื่อผู้รับการบำบัด", placeholder="เช่น นายตั้งใจ บำบัด", key="name_other")
                
                st.markdown("---")
                referral_reason_other = st.selectbox("๖. สาเหตุส่งเข้ารับการบำบัดรักษา", ["ตามคำพิพากษา", "แบบสมัครใจ", "อื่นๆ (ระบุเอง)"], key="reason_select_other")
                custom_reason_other = ""
                if referral_reason_other == "อื่นๆ (ระบุเอง)":
                    custom_reason_other = st.text_input("โปรดระบุสาเหตุด้วยตนเอง:", placeholder="พิมพ์สาเหตุที่นี่...", key="custom_reason_other")

                st.markdown("---")
                status_other = st.selectbox("๗. สถานะการบำบัด", ["บำบัดครบ", "บำบัดไม่ครบ", "ไม่มารายงานตัว", "ขอย้ายสถานบำบัด", "ส่งตัวไปรักษาต่อ"], key="status_select_other")
                
                num_times_other, hospital_name_other, reason_move_other = "", "", ""
                send_to_other, refer_reason_txt_other = "", ""
                
                if status_other == "ขอย้ายสถานบำบัด":
                    st.info("ระบุข้อมูลการย้ายสถานบำบัด:")
                    num_times_other = st.text_input("- ได้เข้ารับการฟื้นฟูฯ จำนวนกี่ครั้ง (ใส่เฉพาะตัวเลข)", placeholder="เช่น ๔", key="num_times_other")
                    hospital_name_other = st.text_input("- ขอย้ายไปที่ไหน (ชื่อ รพ. หรือ สถานที่บำบัด และ จังหวัด)", placeholder="เช่น โรงพยาบาลสมเด็จพระเจ้าตากสินมหาราช จังหวัดตาก", key="hosp_other")
                    reason_move_other = st.text_input("- เนื่องจากอะไร", placeholder="เช่น ย้ายสถานที่ทำงาน", key="move_reason_other")
                
                elif status_other == "ส่งตัวไปรักษาต่อ":
                    st.warning("ระบบจะสลับไปใช้แบบฟอร์ม 'คุมประพฤติอื่น Refer.docx' อัตโนมัติ")
                    send_to_choice_other = st.selectbox("- ส่งตัวไปยัง", ["สถาบันบำบัดรักษาและฟื้นฟูผู้ติดยาเสพติดแห่งชาติบรมราชชนนี", "โรงพยาบาลศรีธัญญา", "อื่นๆ (ระบุเอง)"], key="send_to_sel_other")
                    if send_to_choice_other == "อื่นๆ (ระบุเอง)":
                        send_to_other = st.text_input("โปรดระบุสถานที่ส่งตัว:", key="send_to_txt_other")
                    else:
                        send_to_other = send_to_choice_other
                    
                    refer_reason_choice_other = st.selectbox("- สาเหตุการส่งตัว", ["บำบัดแบบผู้ป่วยนอกไม่สำเร็จ มีปัญหาด้านอารมณ์และพฤติกรรมที่อาจเป็นอันตรายเนื่องจากยาเสพติด", "อื่นๆ (ระบุเอง)"], key="ref_reason_sel_other")
                    if refer_reason_choice_other == "อื่นๆ (ระบุเอง)":
                        refer_reason_txt_other = st.text_input("โปรดระบุสาเหตุการส่งตัว:", key="ref_reason_txt_other")
                    else:
                        refer_reason_txt_other = refer_reason_choice_other

                st.markdown("<br>", unsafe_allow_html=True)
                submit_btn_other = st.button("📄 สร้างเอกสาร Word", type="primary", use_container_width=True, key="submit_other")

            if submit_btn_other:
                reason_text_final_other = ""
                if referral_reason_other == "ตามคำพิพากษา": reason_text_final_other = "ตามคำพิพากษาของศาล"
                elif referral_reason_other == "แบบสมัครใจ": reason_text_final_other = "การติดยาเสพติดให้โทษแบบสมัครใจ"
                else: reason_text_final_other = custom_reason_other

                template_name_other = "คุมประพฤติอื่นรวม.docx"
                status_text_other = ""
                
                if status_other == "บำบัดครบ": status_text_other = "ได้เข้ารับการฟื้นฟูฯ ครบตามระยะเวลาที่กำหนด"
                elif status_other == "บำบัดไม่ครบ": status_text_other = "ได้มารายงานตัวเพื่อเข้ารับการรักษาการติดยาเสพติดและเข้ารับการบำบัดฟื้นฟูฯ แต่ไม่ครบตามระยะเวลาที่กำหนด"
                elif status_other == "ไม่มารายงานตัว": status_text_other = "ไม่ได้มารายงานตัวเพื่อเข้ารับการรักษาและเข้ารับการฟื้นฟูฯ ตามระยะเวลาที่กำหนด"
                elif status_other == "ขอย้ายสถานบำบัด": status_text_other = f"ได้เข้ารับการฟื้นฟูฯ จำนวน {num_times_other} ครั้ง และแจ้งขอย้ายสถานบำบัดไปยัง{hospital_name_other} เนื่องจาก{reason_move_other}"
                elif status_other == "ส่งตัวไปรักษาต่อ": template_name_other = "คุมประพฤติอื่น Refer.docx"
                    
                try:
                    doc = DocxTemplate(template_name_other)
                    context_other = {
                        "หน่วยงานที่ส่งมา": agency_name,
                        "เดือนและปีหนังสือออก": month_year_other,
                        "เลขหนังสือคุมประพฤติ": ref_number_other,
                        "ลงวันที่": ref_date_other,
                        "ชื่อผู้รับการบำบัด": patient_name_other,
                        "สาเหตุส่งเข้ารับการบำบัดรักษา": reason_text_final_other  
                    }
                    if status_other == "ส่งตัวไปรักษาต่อ":
                        context_other["ส่งตัวไปยัง"] = send_to_other
                        context_other["สาเหตุการส่งตัว"] = refer_reason_txt_other
                    else:
                        context_other["สถานะการบำบัด"] = status_text_other
                    
                    doc.render(context_other)
                    bio_other = io.BytesIO()
                    doc.save(bio_other)
                    
                    st.success(f"✅ สร้างเอกสาร '{status_other}' ของ {patient_name_other} สำเร็จ!")
                    st.download_button(
                        label="⬇️ ดาวน์โหลดไฟล์เอกสาร (Word)", data=bio_other.getvalue(),
                        file_name=f"คุมประพฤติอื่น_{status_other}_{patient_name_other}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        type="primary",
                        key="download_other"
                    )
                except Exception as e:
                    st.error(f"❌ ไม่พบไฟล์ต้นแบบ '{template_name_other}' หรือมีข้อผิดพลาด: {str(e)}")

    # ---------------------------------------------
    # ⚖️ 2.2 หมวดศาล (เลื่อนมาเป็นอันดับที่ 2)
    # ---------------------------------------------
    elif st.session_state.category == "ศาล":
        with st.container(border=True):
            st.markdown("<h5 style='color: #60a5fa;'>บันทึกข้อมูล (ศาล)</h5>", unsafe_allow_html=True)
            
            month_year_court = st.text_input("๑. เดือนและปี หนังสือออก", placeholder="เช่น กันยายน 2569")
            ref_number_court = st.text_input("๒. เลขหนังสือศาล", placeholder="เช่น (ป) ๑๗๒๑")
            
            ref_date_court = st.text_input("๓. หนังสือศาลลงวันที่", placeholder="เช่น ๒๐ พฤษภาคม ๒๕๖๘")
            patient_name_court = st.text_input("๔. ชื่อผู้รับการบำบัด", placeholder="เช่น นายตั้งใจ หยุดเสพ")
            
            st.markdown("---")
            section_court = st.selectbox("๕. มาตรา", [
                "166", 
                "168", 
                "166 ประกอบประมวลกฎหมายอาญามาตรา ๕๖", 
                "168 ประกอบประมวลกฎหมายอาญามาตรา ๕๖"
            ], index=None, placeholder="-- โปรดเลือกมาตรา --")
            
            st.markdown("---")
            status_court = st.selectbox("๖. สถานะการบำบัด", [
                "บำบัดครบ", 
                "บำบัดไม่ครบ", 
                "ไม่มารายงานตัว", 
                "ขอย้ายสถานบำบัด"
            ], index=None, placeholder="-- โปรดเลือกสถานะการบำบัด --")
            
            num_times_court, hospital_name_court, reason_court = "", "", ""
            
            if status_court == "ขอย้ายสถานบำบัด":
                st.info("ระบุข้อมูลการย้ายสถานบำบัด:")
                num_times_court = st.text_input("- ได้เข้ารับการฟื้นฟูฯ จำนวนกี่ครั้ง (ใส่เฉพาะตัวเลข)", placeholder="เช่น ๔", key="num_court")
                hospital_name_court = st.text_input("- ขอย้ายไปที่ไหน (ชื่อ รพ. หรือ สถานที่บำบัด และ จังหวัด)", placeholder="เช่น โรงพยาบาลสมเด็จพระเจ้าตากสินมหาราช จังหวัดตาก", key="hosp_court")
                reason_court = st.text_input("- เนื่องจากอะไร", placeholder="เช่น ย้ายสถานที่ทำงาน", key="reason_court")

            st.markdown("<br>", unsafe_allow_html=True)
            submit_btn_court = st.button("📄 สร้างเอกสาร Word", type="primary", use_container_width=True)

        if submit_btn_court:
            if section_court is None or status_court is None:
                st.warning("⚠️ โปรดเลือก 'มาตรา' และ 'สถานะการบำบัด' ให้ครบถ้วนก่อนกดสร้างเอกสารครับ")
            else:
                status_text_court = ""
                if status_court == "บำบัดครบ":
                    status_text_court = "ได้มารายงานตัวเพื่อเข้ารับการบำบัดรักษาและเข้ารับการฟื้นฟูฯ ครบตามโปรแกรมที่กำหนด"
                elif status_court == "บำบัดไม่ครบ":
                    status_text_court = "ได้มารายงานตัวเพื่อเข้ารับการบำบัดรักษาและเข้ารับการฟื้นฟูฯ แต่ไม่ครบตามโปรแกรมที่กำหนด"
                elif status_court == "ไม่มารายงานตัว":
                    status_text_court = "ไม่ได้มารายงานตัวเพื่อเข้ารับการรักษาและเข้ารับการฟื้นฟูฯ ตามโปรมแกรมที่กำหนด"
                elif status_court == "ขอย้ายสถานบำบัด":
                    status_text_court = f"ได้เข้ารับการฟื้นฟูฯ จำนวน {num_times_court} ครั้ง และแจ้งขอย้ายสถานบำบัดไปยัง{hospital_name_court} เนื่องจาก{reason_court}"
                
                template_name_court = "ศาลรวม.docx"
                try:
                    doc = DocxTemplate(template_name_court)
                    context_court = {
                        "เดือนและปีหนังสือออก": month_year_court,
                        "เลขหนังสือศาล": ref_number_court,
                        "ลงวันที่": ref_date_court,
                        "ชื่อผู้รับการบำบัด": patient_name_court,
                        "มาตรา": section_court,
                        "สถานะการบำบัด": status_text_court
                    }
                    
                    doc.render(context_court)
                    bio_court = io.BytesIO()
                    doc.save(bio_court)
                    
                    st.success(f"✅ สร้างเอกสาร '{status_court}' ของ {patient_name_court} สำเร็จ!")
                    st.download_button(
                        label="⬇️ ดาวน์โหลดไฟล์เอกสาร (Word)", data=bio_court.getvalue(),
                        file_name=f"ศาล_{status_court}_{patient_name_court}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        type="primary"
                    )
                except Exception as e:
                    st.error(f"❌ ไม่พบไฟล์ต้นแบบ '{template_name_court}' หรือมีข้อผิดพลาด: {str(e)}")

    # ---------------------------------------------
    # 📑 2.3 หมวดหนังสือรับรองผลการบำบัด (ม.113/114)
    # ---------------------------------------------
    elif st.session_state.category == "หนังสือรับรองการบำบัด":
        with st.container(border=True):
            st.markdown("<h5 style='color: #60a5fa;'>บันทึกข้อมูล (หนังสือรับรองผลการบำบัด)</h5>", unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 1])
            with col1:
                month_year_cert = st.text_input("๑. เดือนและปี หนังสือออก", placeholder="เช่น กันยายน ๒๕๖๙")
                section_cert = st.selectbox("๙. มาตรา", ["มาตรา 113", "มาตรา 114"])
            
            st.markdown("---")
            st.markdown("<b>ข้อมูลผู้รับการบำบัด</b>", unsafe_allow_html=True)
            
            col_name, col_age, col_id = st.columns([2, 1, 2])
            with col_name:
                patient_name_cert = st.text_input("๒. ชื่อผู้รับการบำบัด", placeholder="เช่น นายตั้งใจ บำบัด")
            with col_age:
                age_cert = st.text_input("๓. อายุ (ปี)", placeholder="เช่น 32")
            with col_id:
                id_card_cert = st.text_input("๔. เลขบัตรประชาชน", placeholder="เช่น 1150050000253")
            
            col_house, col_subdist, col_dist, col_prov = st.columns(4)
            with col_house:
                address_cert = st.text_input("๕. บ้านเลขที่", placeholder="เช่น 31/22")
            with col_subdist:
                sub_district_cert = st.text_input("๖. ตำบล/แขวง", placeholder="เช่น บางกระสอ")
            with col_dist:
                district_cert = st.text_input("๗. อำเภอ/เขต", placeholder="เช่น เมืองนนทบุรี")
            with col_prov:
                province_cert = st.text_input("๘. จังหวัด", placeholder="เช่น นนทบุรี")
                
            st.markdown("---")
            st.markdown("<b>ระยะเวลาและผลการบำบัด</b>", unsafe_allow_html=True)
            
            col_start, col_end = st.columns(2)
            with col_start:
                start_date_cert = st.text_input("๑๐. วันที่เริ่มบำบัด", placeholder="เช่น 16 ธันวาคม 2569")
            with col_end:
                end_date_cert = st.text_input("๑๑. วันสิ้นสุดการบำบัด", placeholder="เช่น 10 เมษายน 2570")
                
            result_choice = st.selectbox("๑๒. ผลการบำบัด", ["เป็นที่น่าพอใจ", "ไม่เป็นที่น่าพอใจ", "อื่นๆ (ระบุเอง)"])
            result_cert = ""
            if result_choice == "อื่นๆ (ระบุเอง)":
                result_cert = st.text_input("โปรดระบุผลการบำบัด:", placeholder="พิมพ์ผลการบำบัดที่นี่...")
            else:
                result_cert = result_choice

            st.markdown("<br>", unsafe_allow_html=True)
            submit_btn_cert = st.button("📄 สร้างเอกสาร Word", type="primary", use_container_width=True)

        if submit_btn_cert:
            template_name_cert = "หนังสือรับรองการบำบัด.docx"
            try:
                doc = DocxTemplate(template_name_cert)
                context_cert = {
                    "เดือนและปีหนังสือออก": month_year_cert,
                    "ชื่อผู้รับการบำบัด": patient_name_cert,
                    "อายุ": age_cert,
                    "เลขบัตรประชาชน": id_card_cert,
                    "บ้านเลขที่": address_cert,
                    "ตำบล": sub_district_cert,
                    "อำเภอ": district_cert,
                    "จังหวัด": province_cert,
                    "มาตรา": section_cert,
                    "วันที่เริ่มบำบัด": start_date_cert,
                    "วันสิ้นสุดการบำบัด": end_date_cert,
                    "ผลการบำบัด": result_cert
                }
                
                doc.render(context_cert)
                bio_cert = io.BytesIO()
                doc.save(bio_cert)
                
                st.success(f"✅ สร้างเอกสารหนังสือรับรองของ {patient_name_cert} สำเร็จ!")
                st.download_button(
                    label="⬇️ ดาวน์โหลดไฟล์เอกสาร (Word)", data=bio_cert.getvalue(),
                    file_name=f"หนังสือรับรอง_{section_cert}_{patient_name_cert}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    type="primary"
                )
            except Exception as e:
                st.error(f"❌ ไม่พบไฟล์ต้นแบบ '{template_name_cert}' หรือมีข้อผิดพลาด: {str(e)}")

    # ---------------------------------------------
    # 2.4 หมวดอื่นๆ (สถานพินิจ, เอกชน)
    # ---------------------------------------------
    else:
        st.info(f"📍 ท่านเข้าสู่หมวด **{st.session_state.category}**")
        st.write("ฟอร์มในหมวดหมู่นี้อยู่ระหว่างการพัฒนาช่องกรอกข้อมูลครับ")

# ==========================================
# เครดิตด้านล่างสุดของโปรแกรม
# ==========================================
st.markdown("<div class='footer'>พัฒนาโดยกลุ่มงานจิตเวชและยาเสพติด โรงพยาบาลพระนั่งเกล้า</div>", unsafe_allow_html=True)