import streamlit as st
import requests

# إعداد مظهر اللوحة الأمنية
st.set_page_config(page_title="Cyber Ops Platform - Active v1.0", page_icon="🛡️", layout="wide")

st.markdown("<h1 style='text-align: center; color: #10b981;'>🛡️ CYBER OPS REAL PLATFORM</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>الاتصال المباشر والمشفر بسيرفر الأدوات الحقيقي</p>", unsafe_allow_html=True)
st.write("---")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🔑 إعدادات خادم الهجوم")
    # إدخال الرابط والمفتاح
    server_url = st.text_input("رابط الخادم العام (Server URL):", placeholder="https://xxxx.localtunnel.me")
    api_key = st.text_input("مفتاح الأمان (API Key):", type="password")

    st.write("---")
    st.subheader("⚙️ الهدف والأداة")
    raw_target = st.text_input("الهدف المستهدف (Target IP/Domain):", placeholder="scanme.nmap.org")
    
    selected_tool = st.selectbox("اختر أداة الفحص الحقيقية:", ["nmap", "nuclei", "sqlmap"])
    launch_btn = st.button("🚀 إطلاق العملية الحقيقية", use_container_width=True)

with col2:
    st.subheader("💻 شاشة المخرجات الحقيقية (Real Console)")
    terminal_placeholder = st.empty()
    terminal_style = "<div style='background-color: #020617; color: #34d399; font-family: monospace; border-radius: 8px; padding: 15px; min-height: 400px; white-space: pre-wrap; border: 1px solid #1e293b;'>"
    
    terminal_placeholder.markdown(f"{terminal_style}في انتظار إرسال الطلب إلى خادم جوجل السحابي...</div>", unsafe_allow_html=True)

    if launch_btn:
        if not server_url or not api_key or not raw_target:
            st.error("❌ تأكد من ملء جميع الحقول (الرابط، المفتاح، والهدف) قبل التنفيذ!")
        else:
            terminal_placeholder.markdown(f"{terminal_style}[+] جاري تشفير الأوامر وإرسالها عبر الجسر السحابي للهدف...\n</div>", unsafe_allow_html=True)
            
            # تنظيف الرابط للتأكد من صحته
            clean_url = server_url.strip().rstrip('/')
            
            # تجهيز البيانات للسيرفر الحقيقي
            payload = {
                "tool": selected_tool,
                "target": raw_target.strip(),
                "api_key": api_key.strip()
            }
            
            try:
                # إرسال طلب حقيقي بالكامل للخارج وتلقي النتيجة
                response = requests.post(f"{clean_url}/run", json=payload, timeout=120)
                
                if response.status_code == 200:
                    res_data = response.json()
                    output = res_data.get("output", "السيرفر لم يرسل أي مخرجات نصية.")
                    terminal_placeholder.markdown(f"{terminal_style}{output}</div>", unsafe_allow_html=True)
                elif response.status_code == 401:
                    terminal_placeholder.markdown(f"{terminal_style}🔒 خطأ أمني: مفتاح الأمان (API Key) الذي أدخلته غير صحيح!</div>", unsafe_allow_html=True)
                else:
                    terminal_placeholder.markdown(f"{terminal_style}❌ خطأ من السيرفر الخلفي: {response.text}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"⚡ فشل الاتصال برابط السيرفر: {str(e)}\nتأكد من أن السيرفر يعمل داخل Cloud Shell وأن الرابط لم ينتهِ.")
