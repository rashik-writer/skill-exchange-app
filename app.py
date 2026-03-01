import streamlit as st
import sqlite3   # if you already have this, keep it
import json      # if you already have this, keep it

st.title("Skill Exchange App")
st.caption("Created by Mohamed Rashik")

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="SkillBridge", page_icon="⟁", layout="wide")

# ─── CSS Styling ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@300;400;600;700&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; background-color: #f7f5f0; }

h1, h2, h3 { font-family: 'Crimson Pro', Georgia, serif !important; color: #1a1a2e; }

.header-bar {
    background: #1a1a2e;
    color: #f7f5f0;
    padding: 18px 32px;
    border-radius: 10px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 12px;
}

.skill-card {
    background: #ffffff;
    border: 1px solid #e8e3d9;
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 16px;
    transition: all 0.2s;
}

.skill-card:hover { box-shadow: 0 4px 20px rgba(0,0,0,0.08); }

.profile-card {
    background: #ffffff;
    border: 1px solid #e8e3d9;
    border-radius: 10px;
    padding: 28px;
    margin-bottom: 20px;
}

.avatar-circle {
    background: linear-gradient(135deg, #1a1a2e, #4a4a7a);
    color: white;
    width: 52px;
    height: 52px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 18px;
    margin-right: 12px;
}

.tag {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
    margin: 2px;
}
.tag-tech  { background: #e8edf8; color: #3a5a9a; }
.tag-design{ background: #f8e8ef; color: #9a3a5a; }
.tag-math  { background: #e8f5e8; color: #3a7a3a; }
.tag-lang  { background: #fff3e0; color: #9a6a1a; }
.tag-arts  { background: #f3e8f8; color: #7a3a9a; }
.tag-other { background: #f0ede6; color: #5a5a7a; }

.stat-box {
    background: #f7f5f0;
    border-radius: 8px;
    padding: 16px;
    text-align: center;
    border: 1px solid #e8e3d9;
}

.success-msg {
    background: #e8f5e8;
    color: #2d7a2d;
    padding: 12px 18px;
    border-radius: 8px;
    font-weight: 500;
    margin-top: 10px;
}

.stButton > button {
    background-color: #1a1a2e !important;
    color: white !important;
    border-radius: 6px !important;
    border: none !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    padding: 8px 20px !important;
    transition: all 0.2s !important;
}
.stButton > button:hover { background-color: #2d2d50 !important; }

.stTextInput > div > input, .stTextArea > div > textarea, .stSelectbox > div {
    border-radius: 6px !important;
    border: 1.5px solid #e0dbd0 !important;
    font-family: 'DM Sans', sans-serif !important;
}

hr { border-color: #e8e3d9; }
</style>
""", unsafe_allow_html=True)

# ─── Session State Init ─────────────────────────────────────────────────────────
if "students" not in st.session_state:
    st.session_state.students = [
        {"name": "Mohamed Rashik",   "avatar": "MR", "dept": "Mechanical Engineering", "year": "1st Year",
         "offering": ["writing"], "seeking": ["python"],
         "bio": "Passionate about AI and open-source.", "rating": 4.8, "sessions": 12, "category": "Technology"},
        {"name": "Sara Chen",     "avatar": "SC", "dept": "Design Studies",   "year": "2nd Year",
         "offering": ["UI/UX Design", "Figma"], "seeking": ["Python", "Statistics"],
         "bio": "Designer who loves clean and minimal interfaces.", "rating": 4.9, "sessions": 8, "category": "Design"},
        {"name": "Liam O'Brien",  "avatar": "LO", "dept": "Mathematics",      "year": "4th Year",
         "offering": ["Statistics", "R Programming"], "seeking": ["Web Development", "Spanish"],
         "bio": "Math nerd. Love teaching stats and probability.", "rating": 4.7, "sessions": 20, "category": "Mathematics"},
        {"name": "Maria Flores",  "avatar": "MF", "dept": "Linguistics",      "year": "1st Year",
         "offering": ["Spanish", "French"], "seeking": ["Music Theory", "Photography"],
         "bio": "Language lover, fluent in 3 languages.", "rating": 5.0, "sessions": 5, "category": "Languages"},
        {"name": "James Park",    "avatar": "JP", "dept": "Fine Arts",        "year": "3rd Year",
         "offering": ["Music Theory", "Piano"], "seeking": ["Data Science", "German"],
         "bio": "Classical musician exploring digital arts.", "rating": 4.6, "sessions": 15, "category": "Arts"},
        {"name": "Priya Sharma",  "avatar": "PS", "dept": "Computer Science", "year": "4th Year",
         "offering": ["Web Development", "React"], "seeking": ["Photography", "Spanish"],
         "bio": "Full-stack dev, love building side projects.", "rating": 4.8, "sessions": 18, "category": "Technology"},
        {"name": "Ella Wright",   "avatar": "EW", "dept": "Media Studies",    "year": "2nd Year",
         "offering": ["Photography", "Video Editing"], "seeking": ["Python", "Piano"],
         "bio": "Visual storyteller, Instagram: @ellashots.", "rating": 4.9, "sessions": 9, "category": "Arts"},
        {"name": "Noah Kim",      "avatar": "NK", "dept": "Data Analytics",   "year": "4th Year",
         "offering": ["Data Science", "Tableau"], "seeking": ["Graphic Design", "French"],
         "bio": "Data is the new language — let me teach you.", "rating": 4.7, "sessions": 22, "category": "Technology"},
    ]

if "my_profile" not in st.session_state:
    st.session_state.my_profile = {
        "name": "Your Name", "avatar": "YN", "dept": "Mechanical Engineering", "year": "1st Year",
        "offering": ["Python", "Machine Learning"], "seeking": ["UI/UX Design", "French"],
        "bio": "Passionate about AI and building things. Always looking to learn something new.",
        "rating": 4.8, "sessions": 7, "category": "Technology"
    }

if "messages" not in st.session_state:
    st.session_state.messages = {}  # {student_name: [{"from": "me/them", "text": "..."}]}

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "🔍 Browse Skills"


# ─── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-bar">
    <div style="font-size:28px">⟁</div>
    <div>
        <div style="font-size:22px; font-weight:700; font-family:'Crimson Pro',serif;">SkillBridge</div>
        <div style="font-size:11px; color:#9090b0; letter-spacing:1.5px; text-transform:uppercase;">Student Skill Exchange Network</div>
    </div>
    <div style="margin-left:auto; text-align:right;">
        <div style="font-size:15px; font-weight:600;">{name}</div>
        <div style="font-size:11px; color:#9090b0;">{dept} · {year}</div>
    </div>
</div>
""".format(**st.session_state.my_profile), unsafe_allow_html=True)

# ─── Navigation ────────────────────────────────────────────────────────────────
tabs = ["🔍 Browse Skills", "➕ Post a Skill", "💬 Messages", "👤 My Profile"]
selected = st.tabs(tabs)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1: BROWSE SKILLS
# ═══════════════════════════════════════════════════════════════════════════════
with selected[0]:
    st.markdown("## Discover Skills")
    st.markdown("Connect with students ready to teach and learn together.")
    st.markdown("---")

    col_search, col_filter = st.columns([3, 1])
    with col_search:
        search = st.text_input("🔎 Search by skill, name, or department", placeholder="e.g. Python, Maria, Design...")
    with col_filter:
        category = st.selectbox("Category", ["All", "Technology", "Design", "Mathematics", "Languages", "Arts"])

    st.markdown("<br>", unsafe_allow_html=True)

    cat_colors = {
        "Technology": "tag-tech", "Design": "tag-design",
        "Mathematics": "tag-math", "Languages": "tag-lang",
        "Arts": "tag-arts", "Other": "tag-other"
    }

    # Filter students
    results = []
    for s in st.session_state.students:
        match_search = (
            search.lower() in s["name"].lower() or
            search.lower() in s["dept"].lower() or
            any(search.lower() in sk.lower() for sk in s["offering"]) or
            any(search.lower() in sk.lower() for sk in s["seeking"])
        ) if search else True
        match_cat = (category == "All" or s["category"] == category)
        if match_search and match_cat:
            results.append(s)

    if not results:
        st.info("No students found. Try a different search or category.")
    else:
        cols = st.columns(2)
        for i, s in enumerate(results):
            with cols[i % 2]:
                tag_class = cat_colors.get(s["category"], "tag-other")
                offering_tags = " ".join([f'<span class="tag tag-tech">{sk}</span>' for sk in s["offering"]])
                seeking_tags  = " ".join([f'<span class="tag tag-other">{sk}</span>' for sk in s["seeking"]])
                stars = "★" * round(s["rating"]) + "☆" * (5 - round(s["rating"]))

                st.markdown(f"""
                <div class="skill-card">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                        <div style="display:flex; align-items:center;">
                            <div style="background:linear-gradient(135deg,#1a1a2e,#4a4a7a);color:white;width:44px;height:44px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-weight:700;font-size:15px;margin-right:10px;">{s['avatar']}</div>
                            <div>
                                <div style="font-weight:600;font-size:15px;">{s['name']}</div>
                                <div style="font-size:12px;color:#999;">{s['dept']} · {s['year']}</div>
                            </div>
                        </div>
                        <span class="tag {tag_class}">{s['category']}</span>
                    </div>
                    <div style="margin-bottom:10px;">
                        <div style="font-size:12px;color:#aaa;font-weight:600;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:5px;">Offering</div>
                        {offering_tags}
                    </div>
                    <div style="margin-bottom:12px;">
                        <div style="font-size:12px;color:#aaa;font-weight:600;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:5px;">Seeking</div>
                        {seeking_tags}
                    </div>
                    <div style="font-size:13px;color:#777;margin-bottom:4px;">
                        <span style="color:#c5a028;">{stars}</span> {s['rating']} · {s['sessions']} sessions
                    </div>
                </div>
                """, unsafe_allow_html=True)

                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    if st.button(f"💬 Message", key=f"msg_{i}"):
                        if s["name"] not in st.session_state.messages:
                            st.session_state.messages[s["name"]] = []
                        st.session_state.active_chat = s["name"]
                        st.success(f"Go to 💬 Messages tab to chat with {s['name']}!")
                with btn_col2:
                    with st.expander(f"👤 View Profile"):
                        st.markdown(f"**Bio:** {s['bio']}")
                        st.markdown(f"**Department:** {s['dept']}")
                        st.markdown(f"**Year:** {s['year']}")


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2: POST A SKILL
# ═══════════════════════════════════════════════════════════════════════════════
with selected[1]:
    st.markdown("## Post a Skill")
    st.markdown("Share what you can teach and what you'd like to learn in return.")
    st.markdown("---")

    with st.form("post_skill_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            skill_name = st.text_input("Skill I'm Offering *", placeholder="e.g. Machine Learning, Guitar, French...")
            skill_category = st.selectbox("Category", ["Technology", "Design", "Mathematics", "Languages", "Arts", "Other"])
        with col2:
            skill_seeking = st.text_input("Skills I'm Seeking", placeholder="e.g. Photography, Spanish (comma-separated)")
            skill_year = st.selectbox("Year", ["1st Year", "2nd Year", "3rd Year", "4th Year", "Masters", "PhD"])

        skill_dept = st.text_input("Department", placeholder="e.g. Computer Science, Fine Arts...")
        skill_bio  = st.text_area("Tell others about your experience", placeholder="Describe your background with this skill...", height=100)

        submitted = st.form_submit_button("✅ Post Skill", use_container_width=True)

        if submitted:
            if skill_name.strip():
                seeking_list = [s.strip() for s in skill_seeking.split(",") if s.strip()]
                new_student = {
                    "name": st.session_state.my_profile["name"],
                    "avatar": st.session_state.my_profile["avatar"],
                    "dept": skill_dept or st.session_state.my_profile["dept"],
                    "year": skill_year,
                    "offering": [skill_name],
                    "seeking": seeking_list or ["Open to anything!"],
                    "bio": skill_bio or st.session_state.my_profile["bio"],
                    "rating": st.session_state.my_profile["rating"],
                    "sessions": st.session_state.my_profile["sessions"],
                    "category": skill_category,
                }
                st.session_state.students.append(new_student)
                st.session_state.my_profile["offering"].append(skill_name)
                st.success(f"🎉 '{skill_name}' posted successfully! It's now visible in Browse Skills.")
            else:
                st.error("Please enter the skill you're offering.")

    st.markdown("---")
    st.markdown("### My Current Skills")
    my = st.session_state.my_profile
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**Offering:**")
        for sk in my["offering"]:
            st.markdown(f'<span class="tag tag-tech">✓ {sk}</span>', unsafe_allow_html=True)
    with col_b:
        st.markdown("**Seeking:**")
        for sk in my["seeking"]:
            st.markdown(f'<span class="tag tag-lang">→ {sk}</span>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3: MESSAGES
# ═══════════════════════════════════════════════════════════════════════════════
with selected[2]:
    st.markdown("## Messages")
    st.markdown("---")

    if not st.session_state.messages:
        st.info("No conversations yet. Browse skills and click 'Message' to start chatting!")
    else:
        chat_names = list(st.session_state.messages.keys())
        active = st.session_state.get("active_chat", chat_names[0] if chat_names else None)

        col_list, col_chat = st.columns([1, 2])

        with col_list:
            st.markdown("**Conversations**")
            for name in chat_names:
                if st.button(f"👤 {name}", key=f"chat_btn_{name}", use_container_width=True):
                    st.session_state.active_chat = name
                    active = name

        with col_chat:
            if active and active in st.session_state.messages:
                st.markdown(f"**Chat with {active}**")
                st.markdown("---")

                chat_history = st.session_state.messages[active]
                if not chat_history:
                    st.caption("No messages yet. Say hello!")
                else:
                    for msg in chat_history:
                        if msg["from"] == "me":
                            st.markdown(f"""
                            <div style="text-align:right;margin:8px 0;">
                                <span style="background:#1a1a2e;color:white;padding:10px 16px;border-radius:16px 16px 4px 16px;display:inline-block;max-width:70%;font-size:14px;">{msg['text']}</span>
                            </div>""", unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div style="text-align:left;margin:8px 0;">
                                <span style="background:#f0ede6;color:#1a1a2e;padding:10px 16px;border-radius:16px 16px 16px 4px;display:inline-block;max-width:70%;font-size:14px;">{msg['text']}</span>
                            </div>""", unsafe_allow_html=True)

                with st.form(f"msg_form_{active}", clear_on_submit=True):
                    msg_col, send_col = st.columns([4, 1])
                    with msg_col:
                        new_msg = st.text_input("Type a message...", label_visibility="collapsed", placeholder="Type a message...")
                    with send_col:
                        send = st.form_submit_button("Send")
                    if send and new_msg.strip():
                        st.session_state.messages[active].append({"from": "me", "text": new_msg})
                        st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4: MY PROFILE
# ═══════════════════════════════════════════════════════════════════════════════
with selected[3]:
    st.markdown("## My Profile")
    st.markdown("---")

    me = st.session_state.my_profile
    stars = "★" * round(me["rating"]) + "☆" * (5 - round(me["rating"]))

    st.markdown(f"""
    <div class="profile-card">
        <div style="display:flex;align-items:center;gap:16px;margin-bottom:16px;">
            <div style="background:linear-gradient(135deg,#1a1a2e,#4a4a7a);color:white;width:64px;height:64px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:22px;">{me['avatar']}</div>
            <div>
                <div style="font-size:24px;font-weight:700;font-family:'Crimson Pro',serif;">{me['name']}</div>
                <div style="color:#888;font-size:14px;">{me['dept']} · {me['year']}</div>
                <div style="color:#c5a028;margin-top:4px;">{stars} {me['rating']} &nbsp;·&nbsp; {me['sessions']} sessions completed</div>
            </div>
        </div>
        <p style="color:#555;font-size:15px;line-height:1.7;">{me['bio']}</p>
    </div>
    """, unsafe_allow_html=True)

    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.markdown(f'<div class="stat-box"><div style="font-size:28px;font-weight:700;color:#1a1a2e;">{len(me["offering"])}</div><div style="font-size:12px;color:#aaa;">Skills Offering</div></div>', unsafe_allow_html=True)
    with col_stat2:
        st.markdown(f'<div class="stat-box"><div style="font-size:28px;font-weight:700;color:#1a1a2e;">{len(me["seeking"])}</div><div style="font-size:12px;color:#aaa;">Skills Seeking</div></div>', unsafe_allow_html=True)
    with col_stat3:
        st.markdown(f'<div class="stat-box"><div style="font-size:28px;font-weight:700;color:#1a1a2e;">{me["sessions"]}</div><div style="font-size:12px;color:#aaa;">Sessions Done</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### ✏️ Edit Profile")

    with st.form("edit_profile"):
        e_col1, e_col2 = st.columns(2)
        with e_col1:
            new_name = st.text_input("Full Name", value=me["name"])
            new_dept = st.text_input("Department", value=me["dept"])
        with e_col2:
            new_year = st.selectbox("Year", ["1st Year", "2nd Year", "3rd Year", "4th Year", "Masters", "PhD"],
                                    index=["1st Year", "2nd Year", "3rd Year", "4th Year", "Masters", "PhD"].index(me["year"]))
            new_offering = st.text_input("Skills Offering (comma-separated)", value=", ".join(me["offering"]))

        new_seeking = st.text_input("Skills Seeking (comma-separated)", value=", ".join(me["seeking"]))
        new_bio = st.text_area("Bio", value=me["bio"], height=100)
        save = st.form_submit_button("💾 Save Changes", use_container_width=True)

        if save:
            st.session_state.my_profile.update({
                "name": new_name,
                "dept": new_dept,
                "year": new_year,
                "bio": new_bio,
                "offering": [s.strip() for s in new_offering.split(",") if s.strip()],
                "seeking":  [s.strip() for s in new_seeking.split(",") if s.strip()],
                "avatar": "".join([w[0].upper() for w in new_name.split()[:2]])
            })
            st.success("✅ Profile updated successfully!")
            st.rerun()
