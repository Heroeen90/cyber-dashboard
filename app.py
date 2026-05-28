import streamlit as st
import subprocess
import re
import json
import os

# 1. إعدادات الصفحة والمظهر المظلم الاحترافي
st.set_page_config(page_title="Cyber Ops Platform", page_icon="🛡️", layout="wide")

# تصميم ترويسة الموقع
st.markdown("<h1 style='text-align: center; color: #10b981;'>🛡️ CYBER OPS PLATFORM</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>منصة إدارة واختبار الاختراق المركزية للموبايل</p>", unsafe_allow_html=True)
st.write("---")

# ملف حفظ الأدوات الديناميكية
DYNAMIC_TOOLS_FILE = "custom_tools.json"

def load_custom_tools():
    if os.path.exists(DYNAMIC_TOOLS_FILE):
        with open(DYNAMIC_TOOLS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_custom_tools(tools):
    with open(DYNAMIC_TOOLS_FILE, "w", encoding="utf-8") as f:
        json.dump(tools, f, indent=4, ensure_ascii=False)

# 2. حارس البوابة الأمنية لمنع Command Injection
def validate_input(target):
    target = target.strip()
    if not target:
        return None
    # السماح فقط بالأرقام، الحروف، النقط، والشرطة (IPs & Domains)
    if not re.match(r"^[a-zA-Z0-9.-]+$", target):
        st.error("⚡ تحذير أمني: مدخلات غير صالحة! يُسمح فقط بعناوين IP أو نطاقات شرعية.")
        return None
    return target

# 3. تقسيم الشاشة إلى عمودين (التحكم على اليسار، والترمينال على اليمين)
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("⚙️ إعدادات المهمة")
    
    # حقل الهدف
    raw_target = st.text_input("الهدف (Target IP / Domain):", placeholder="مثال: 127.0.0.1 أو target.com")
    
    # جلب الأدوات (الافتراضية + المخصصة)
    custom_tools = load_custom_tools()
    tool_options = ["Nmap - فحص الشبكة", "Nuclei - فحص الثغرات", "SQLmap - حقن قواعد البيانات"] + [t['name'] for t in custom_tools]
    
    selected_tool = st.selectbox("اختر أداة الفحص والتنفيذ:", tool_options)
    
    launch_btn = st.button("🚀 إطلاق الأداة الأمنية", use_container_width=True)
    
    st.write("---")
    # قسم إضافة أداة جديدة ديناميكياً
    with st.expander("➕ إضافة أداة مخصصة لترسانتك"):
        new_name = st.text_input("اسم الأداة:")
        new_cmd = st.text_input("أمر التشغيل الأساسي:", placeholder="مثال: python3 script.py -t")
        if st.button("حفظ الأداة في المنصة"):
            if new_name and new_cmd:
                if ";" in new_cmd or "&&" in new_cmd:
                    st.error("تحذير أمني: لا يُسمح برموز خبيثة في الأمر.")
                else:
                    tools = load_custom_tools()
                    tools.append({"name": new_name, "command": new_cmd})
                    save_custom_tools(tools)
                    st.success(f"تم دمج {new_name} بنجاح!")
                    st.rerun()

with col2:
    st.subheader("💻 شاشة الترمينال الحي (Live Console)")
    
    # صندوق محاكاة شاشة الترمينال السوداء
    terminal_placeholder = st.empty()
    terminal_style = "<div style='background-color: #020617; color: #34d399; font-family: monospace; p-3; border-radius: 8px; padding: 15px; min-height: 350px; white-space: pre-wrap; border: 1px solid #1e293b;'>"
    
    terminal_content = "الترمينال خامل حالياً... في انتظار إطلاق عملية أمنية."
    terminal_placeholder.markdown(f"{terminal_style}{terminal_content}</div>", unsafe_allow_html=True)

    if launch_btn:
        target = validate_input(raw_target)
        if target:
            terminal_content = f"[+] جاري بدء العملية الأمنية على الهدف: {target}...\n"
            terminal_placeholder.markdown(f"{terminal_style}{terminal_content}</div>", unsafe_allow_html=True)
            
            # تحديد مصفوفة الأمر بناءً على اختيارك
            if selected_tool == "Nmap - فحص الشبكة":
                cmd = ["nmap", "-F", target]
            elif selected_tool == "Nuclei - فحص الثغرات":
                cmd = ["nuclei", "-target", target, "-severity", "critical,high"]
            elif selected_tool == "SQLmap - حقن قواعد البيانات":
                cmd = ["sqlmap", "-u", f"http://{target}", "--batch"]
            else:
                # تشغيل الأداة الديناميكية المضافة من قبلك
                chosen = next(t for t in custom_tools if t['name'] == selected_tool)
                cmd = chosen['command'].split() + [target]
            
            try:
                # تشغيل الأداة وجلب المخرجات بأمان
                terminal_content += f"[+] جاري تنفيذ الأمر: {' '.join(cmd)}\n\n"
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                
                # تحديث الشاشة سطر بسطر (بث حي في المتصفح!)
                while True:
                    line = process.stdout.readline()
                    if not line:
                        break
                    terminal_content += line
                    terminal_placeholder.markdown(f"{terminal_style}{terminal_content}</div>", unsafe_allow_html=True)
                
                process.wait()
                terminal_content += f"\n[✓] اكتملت المهمة بكود حالة: {process.returncode}"
                terminal_placeholder.markdown(f"{terminal_style}{terminal_content}</div>", unsafe_allow_html=True)
                
            except Exception as e:
                terminal_content += f"\n⚡ خطأ أثناء التشغيل الفعلي: {str(e)}\n(تأكد من تثبيت الأداة على خادم المنصة)"
                terminal_placeholder.markdown(f"{terminal_style}{terminal_content}</div>", unsafe_allow_html=True)
