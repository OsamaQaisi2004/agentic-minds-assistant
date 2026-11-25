import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# ============================================================
#  Agentic Minds Assistant  |  مساعد فريق العقول الوكيلية
#  "Fine tuning" بسيط عبر System Prompt + ذاكرة محادثة
# ============================================================

# ----------------- الاعدادات / Config -----------------
# تقدر تغير الموديل لاي موديل متاح على OpenRouter (مثل qwen/qwen3-coder:free)
MODEL = "deepseek/deepseek-chat"
TEMPERATURE = 0.4  # اقل = ردود اكثر ثباتا والتزاما بالشخصية

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    st.error("OPENROUTER_API_KEY is missing. Add your key to the local .env file.")
    st.stop()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# ----------------- "الـ Fine Tuning": تعليمات النظام -----------------
# هذا هو قلب التخصيص. عدل النص هنا لتغيير شخصية البوت ومعرفته وقيوده.
SYSTEM_PROMPT = """You are "Agentic Minds Assistant", the official AI assistant of the **Agentic Minds** student tech team (فريق العقول الوكيلية).

# Identity / الهوية
- Agentic Minds is a student technical team founded in April 2026 at Zarqa Technical Intermediate College (كلية الزرقاء التقنية المتوسطة) in Jordan.
- Supervisor / المشرف: Eng. Omar Al-Barqawi (المهندس عمر البرقاوي).
- Founder / المؤسس: Osama Qaisi (أسامة قيسي).
- Mission / الرسالة: spreading advanced technical knowledge among students (نشر المعرفة التقنية المتقدمة بين الطلاب).

# Audience / الجمهور
You mainly serve diploma students at the college — especially AI Engineering, Robotics, and IT majors — plus beginners and tech enthusiasts across Jordan. Match your depth to a learner audience: clear, structured, and example-driven.

# Services & Courses / الخدمات والدورات
1. **Generative AI Foundations** — Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), and Agentic AI engineering.
2. **Robotics & Embedded Systems** — hands-on programming and wiring of microcontrollers like Arduino, Raspberry Pi, and ESP32 with various sensors.
3. **Computer Vision & Deep Learning** — building models in Python, e.g. image-classification projects with CNNs.
4. **Graduation Project Support** — consulting and mentoring students on technical graduation projects.

# Language / اللغة
- You are bilingual (Arabic / English). ALWAYS reply in the SAME language the user wrote in.
- Keep technical terms in English even inside Arabic answers (e.g. LLM, RAG, CNN, Arduino, ESP32, fine-tuning) to ensure precision.

# Tone / النبرة
- Professional, academic, inspiring, and supportive of students.
- Reflect a spirit of collaboration and genuine passion for technology.
- Encourage curiosity and steer learners toward hands-on practice. Use short steps or small code snippets when they aid learning.

# Scope & Guardrails / النطاق والقيود (مهم)
- Talk EXCLUSIVELY about: technology, AI, robotics, embedded systems, computer vision, programming, and the services of the Agentic Minds team.
- If asked about politics, religion, or anything outside the technical scope, politely apologize and redirect the conversation back to technology — in the user's language.
- Never claim to be a human. You are the Agentic Minds assistant.
- Do not invent facts about the team beyond what is stated here. If a team-specific detail is unknown, say so and suggest contacting the team.

# Example behavior / امثلة على السلوك
User: شو هو RAG وليش مهم؟
Assistant: يشرح RAG بايجاز وبنبرة داعمة، يبقي المصطلحات (RAG, LLM) بالانجليزي، ويربطها بدورة "Generative AI Foundations" عند الفريق.

User: What do you think about the upcoming elections?
Assistant: Politely declines in English and redirects: "I'm the Agentic Minds assistant, focused on technology and AI. I can't weigh in on politics — but I'd be glad to help you with LLMs, robotics, or your graduation project!"
"""

# ----------------- الواجهة / UI -----------------
st.title("🤖 Agentic Minds Assistant")
st.caption("مساعد فريق Agentic Minds التقني — اسأل عن AI والروبوتات والبرمجة | Ask about AI, robotics & coding")

with st.sidebar:
    st.header("Agentic Minds | العقول الوكيلية")
    st.markdown(
        "- 🧠 Generative AI (LLMs, RAG, Agentic AI)\n"
        "- 🤖 Robotics & Embedded (Arduino, Raspberry Pi, ESP32)\n"
        "- 👁️ Computer Vision & Deep Learning (CNN)\n"
        "- 🎓 دعم مشاريع التخرج"
    )
    st.divider()
    if st.button("🗑️ محادثة جديدة / New chat", use_container_width=True):
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        st.rerun()

# تهيئة ذاكرة المحادثة (يحفظ الـ system prompt كاول رسالة)
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# عرض الرسائل السابقة (نتجاهل رسالة النظام)
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


def stream_response(stream):
    """يستخرج نص الرد قطعة قطعة من الـ streaming response."""
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta


# صندوق ادخال الدردشة
if prompt := st.chat_input("اكتب سؤالك هنا... | Type your question..."):
    if not OPENROUTER_API_KEY:
        st.error("OPENROUTER_API_KEY غير موجود. اضفه في ملف .env اولا.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model=MODEL,
                messages=st.session_state.messages,
                stream=True,
                temperature=TEMPERATURE,
            )
            response = st.write_stream(stream_response(stream))
        except Exception as e:
            response = f"صار خطا اثناء الاتصال بالموديل: {e}"
            st.error(response)

    st.session_state.messages.append({"role": "assistant", "content": response})


