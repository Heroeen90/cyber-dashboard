import streamlit as st
import requests
import re

st.set_page_config(page_title="Cyber Ops Platform - Real v1.0", page_icon="🛡️", layout="wide")

st.markdown("<h1 style='text-align: center; color: #10b981;'>🛡️ CYBER OPS REAL PLATFORM</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>النسخة الحقيقية المربوطة بسيرفر هجوم معزول وآمن</p>", unsafe_allow_html=True)
st.write("---")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🔑 ربط السيرفر الآمن")
    # هنا تضع رابط localtunnel
    server_url = st.text_input("رابط خادم الأدوات (Server URL):", placeholder="مثال: https://xxxx.localtunnel.me")
    api_key = st.text_input("مفتاح الأمان السري (API Key):", type="password", placeholder="ادخل مفتاح التشفير الخاص بك")

    st.write("---")
    st.subheader("⚙️ إعدادات المهمة")
    raw_target = st.text_input("الهدف المستهدف (Target):", placeholder="scanme.nmap.org")
    
    selected_tool = st.selectbox("اختر الأداة الحقيقية:", ["Nmap"])
    launch_btn = st.button("🚀 تنفيذ الهجوم الحقيقي", use_container_width=True)

with col2:
    st.subheader("💻 شاشة المخرجات الحقيقية (Real-time Console)")
    terminal_placeholder = st.empty()
    terminal_style = "<div style='background-color: #020617; color: #34d399; font-family: monospace; border-radius: 8px; padding: 15px; min-height: 400px; white-space: pre-wrap; border: 1px solid #1e293b;'>"
    
    terminal_placeholder.markdown(f"{terminal_style}في انتظار ربط السيرفر وإطلاق مهمة أمنية حقيقية...</div>", unsafe_allow_html=True)

    if launch_btn:
        if not server_url or not api_key or not raw_target:
            st.error("❌ يجب إدخال رابط السيرفر، مفتاح الأمان، والهدف أولاً!")
        else:
            terminal_placeholder.markdown(f"{terminal_style}[+] جاري تشفير الطلب وإرساله إلى خادمك الحقيقي على جوجل...\n</div>", unsafe_allow_html=True)
            
            # تنظيف الرابط من أي شرطة مائلة زائدة في النهاية
            clean_url = server_url.strip().rstrip('/')
            
            payload = {
                "tool": "nmap",
                "target": raw_target.strip(),
                "api_key": api_key.strip()
            }
            
            try:
                # إرسال الطلب بشكل حقيقي إلى خادم جوجل عبر مسار /run
                response = requests.post(f"{clean_url}/run", json=payload, timeout=120)
                
                if response.status_code == 200:
                    res_data = response.json()
                    output = res_data.get("output", "لم يتم إرجاع أي مخرجات من السيرفر.")
                    terminal_placeholder.markdown(f"{terminal_style}{output}</div>", unsafe_allow_html=True)
                elif response.status_code == 401:
                    st.error("🔒 فشل المصادقة: مفتاح الأمان غير صحيح!")
                else:
                    st.error(f"❌ خطأ من السيرفر الخلفي: {response.text}")
            except Exception as e:
                st.error(f"⚡ فشل الاتصال بخادمك الحقيقي: {str(e)}\nتأكد من أن السيرفر يعمل في Cloud Shell.")
