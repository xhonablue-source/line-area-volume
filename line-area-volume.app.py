import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

ASSETS = Path(__file__).parent / "assets"

st.set_page_config(
    page_title="Mr. H Math Worksheet Library",
    page_icon="📐",
    layout="centered",
)

# ---------------------------------------------------------------
# Angle / quadrant helpers (for the Bonus Mirror Angle Explorer)
# ---------------------------------------------------------------
def quadrant_of_angle(deg):
    """Return the quadrant name for an angle strictly inside one of the four
    90-degree wedges. Angles that land exactly on an axis are labeled as such."""
    d = deg % 360
    if d in (0, 90, 180, 270):
        axis_names = {0: "positive x-axis", 90: "positive y-axis",
                      180: "negative x-axis", 270: "negative y-axis"}
        return f"on the {axis_names[d]}"
    if 0 < d < 90:
        return "Quadrant I"
    if 90 < d < 180:
        return "Quadrant II"
    if 180 < d < 270:
        return "Quadrant III"
    return "Quadrant IV"


def wedge_quadrant(start_deg):
    """Given a starting angle that is a multiple of 90, return the quadrant
    name that the 90-degree wedge [start, start+90] fills."""
    s = start_deg % 360
    mapping = {0: "Quadrant I", 90: "Quadrant II", 180: "Quadrant III", 270: "Quadrant IV"}
    return mapping.get(s, "a mix of quadrants (start angle isn't a multiple of 90°)")


def draw_mirror_plot(start_deg, sweep_deg=90):
    """Draw the original ray, its 90-degree mirror, and the adjacent 45-degree
    bisector ray, with the wedge between them shaded."""
    fig, ax = plt.subplots(figsize=(4.2, 4.2))
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.set_aspect("equal")
    ax.axhline(0, color="#cfc4e6", linewidth=1)
    ax.axvline(0, color="#cfc4e6", linewidth=1)

    end_deg = start_deg + sweep_deg
    bisector_deg = start_deg + sweep_deg / 2

    # shade the wedge
    theta = np.linspace(np.radians(start_deg), np.radians(end_deg), 60)
    xs = np.concatenate([[0], np.cos(theta), [0]])
    ys = np.concatenate([[0], np.sin(theta), [0]])
    ax.fill(xs, ys, color="#F1E9FB", zorder=1)

    def ray(deg, color, label, lw=3, style="-"):
        r = np.radians(deg)
        ax.plot([0, np.cos(r)], [0, np.sin(r)], style, color=color, linewidth=lw, zorder=3)
        ax.plot(np.cos(r) * 1.12, np.sin(r) * 1.12, "", color=color)
        ax.annotate(label, (np.cos(r) * 1.18, np.sin(r) * 1.18), color=color,
                     fontsize=9, fontweight="bold", ha="center", va="center")

    ray(start_deg, "#8E5BDE", f"{start_deg}°\n(original line)")
    ray(end_deg, "#FF9F1C", f"{end_deg}°\n(90° mirror)")
    ray(bisector_deg, "#FF5FA0", f"{bisector_deg:g}°\n(45° mirror)", lw=2, style="--")

    ax.set_xticks([-1, 0, 1])
    ax.set_yticks([-1, 0, 1])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    return fig


# ---------------------------------------------------------------
# Styling
# ---------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Nunito:wght@400;600;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Nunito', sans-serif;
    }
    .lib-title {
        font-family: 'Baloo 2', cursive;
        font-weight: 800;
        font-size: 2.1rem;
        color: #8E5BDE;
        margin-bottom: 0;
    }
    .lib-subtitle {
        font-family: 'Baloo 2', cursive;
        font-weight: 700;
        font-size: 1rem;
        color: #FF9F1C;
        margin-top: 0;
    }
    .card {
        background: #FFFCF3;
        border: 2px solid #E4D6F7;
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 14px;
    }
    .card-title {
        font-family: 'Baloo 2', cursive;
        font-weight: 700;
        font-size: 1.1rem;
        color: #2E2440;
        margin-bottom: 4px;
    }
    .card-desc {
        font-size: 0.88rem;
        color: #4a3f5c;
        margin-bottom: 8px;
    }
    .pill {
        display: inline-block;
        font-family: 'Baloo 2', cursive;
        font-weight: 700;
        font-size: 0.72rem;
        border-radius: 999px;
        padding: 3px 10px;
        margin-right: 6px;
        margin-bottom: 6px;
    }
    .pill-ccss { background: #F1E9FB; color: #8E5BDE; border: 1.5px solid #D6BFF5; }
    .pill-mi   { background: #FFF3E0; color: #FF9F1C; border: 1.5px solid #FFD79A; }
    .pill-topic{ background: #EAF9EC; color: #3FAE5B; border: 1.5px solid #B7E8C0; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<p class="lib-title">📐 Mr. H Math Worksheet Library</p>', unsafe_allow_html=True)
st.markdown('<p class="lib-subtitle">Printable PDF worksheets, aligned to Common Core &amp; Michigan K-12 Math Standards</p>', unsafe_allow_html=True)
st.write("")

tab_library, tab_bonus = st.tabs(["📚 Worksheet Library", "🧭 Bonus: Mirror Angle Explorer"])

# ---------------------------------------------------------------
# Worksheet catalog
# Each entry: title, description, topic tag, CCSS code(s), Michigan code(s), filename
# ---------------------------------------------------------------
WORKSHEETS = [
    {
        "title": "The Jelly Bean Problem: Multiplying Fractions",
        "desc": "A candy-themed intro to multiplying a fraction by a whole number, with space to draw and color.",
        "topic": "Multiplying Fractions",
        "ccss": ["CCSS.MATH.CONTENT.5.NF.B.4"],
        "mi": ["MI.Math.Content.5.NF.B.4"],
        "file": "jelly_bean_fractions_worksheet.pdf",
    },
    {
        "title": "Tuesday Times Table Review (Speed Sheet)",
        "desc": "A 3-column, 36-problem timed multiplication drill covering the 2s through 9s.",
        "topic": "Multiplication Fluency",
        "ccss": ["CCSS.MATH.CONTENT.3.OA.C.7"],
        "mi": ["MI.Math.Content.3.OA.C.7"],
        "file": "tuesday_times_tables_speed_sheet.pdf",
    },
    {
        "title": "Factor Tree Frenzy: Equivalent Fractions",
        "desc": "Branches out of both the numerator and denominator down to primes, then cancels shared factors to simplify.",
        "topic": "Equivalent Fractions & GCF",
        "ccss": ["CCSS.MATH.CONTENT.4.NF.A.1", "CCSS.MATH.CONTENT.6.NS.B.4"],
        "mi": ["MI.Math.Content.4.NF.A.1", "MI.Math.Content.6.NS.B.4"],
        "file": "factor_tree_frenzy.pdf",
    },
    {
        "title": "Read It, Solve It: Fraction Word Problems",
        "desc": "Teaches SHARE (top) vs. GROUPS (bottom) to help students read a word problem into a fraction, then simplify.",
        "topic": "Fractions as Division",
        "ccss": ["CCSS.MATH.CONTENT.5.NF.B.3"],
        "mi": ["MI.Math.Content.5.NF.B.3"],
        "file": "read_it_solve_it_fractions.pdf",
    },
    {
        "title": "Improper to Mixed: Fraction Makeover",
        "desc": "Converts improper fractions to mixed numbers by circling objects into groups, without relying on long division.",
        "topic": "Mixed Numbers",
        "ccss": ["CCSS.MATH.CONTENT.4.NF.B.3.B"],
        "mi": ["MI.Math.Content.4.NF.B.3.b"],
        "file": "improper_to_mixed.pdf",
    },
    {
        "title": "Survey Says! Fraction Word Problems",
        "desc": "Fraction problems built from the class's own survey data — real counts, real classmates.",
        "topic": "Fractions & Simplifying",
        "ccss": ["CCSS.MATH.CONTENT.6.NS.B.4", "CCSS.MATH.CONTENT.6.RP.A.3"],
        "mi": ["MI.Math.Content.6.NS.B.4", "MI.Math.Content.6.RP.A.3"],
        "file": "survey_says_fractions.pdf",
    },
    {
        "title": "Multiplying Fractions: Word Problems Starring Our Class",
        "desc": "Wordy, story-driven multiplication problems featuring real classmates and real survey data.",
        "topic": "Multiplying Fractions",
        "ccss": ["CCSS.MATH.CONTENT.5.NF.B.4"],
        "mi": ["MI.Math.Content.5.NF.B.4"],
        "file": "multiplying_fractions_survey.pdf",
    },
    {
        "title": "Dividing Fractions: Word Problems Starring Our Class",
        "desc": "Teaches Keep-Change-Flip through classmate-driven story problems, then simplifies by cancelling factors.",
        "topic": "Dividing Fractions",
        "ccss": ["CCSS.MATH.CONTENT.6.NS.A.1"],
        "mi": ["MI.Math.Content.6.NS.A.1"],
        "file": "dividing_fractions_survey.pdf",
    },
    {
        "title": "Line \u2192 Area \u2192 Volume: How Small Structures Grow",
        "desc": "Connects writing structure (word \u2192 sentence \u2192 paragraph) to geometric growth (line \u2192 area \u2192 volume).",
        "topic": "Area & Volume",
        "ccss": ["CCSS.MATH.CONTENT.6.G.A.1", "CCSS.MATH.CONTENT.6.G.A.2"],
        "mi": ["MI.Math.Content.6.G.A.1", "MI.Math.Content.6.G.A.2"],
        "file": "line_area_volume_growth.pdf",
    },
    {
        "title": "Crack the Math Code! (Guessword Vocabulary Craft)",
        "desc": "A letter-blank vocabulary puzzle covering function, perpendicular planes, dimension, volume, and more.",
        "topic": "Math Vocabulary",
        "ccss": ["CCSS.MATH.CONTENT.6.G.A.1", "CCSS.MATH.CONTENT.8.F.A.1 (preview)"],
        "mi": ["MI.Math.Content.6.G.A.1", "MI.Math.Content.8.F.A.1 (preview)"],
        "file": "math_word_craft_guessword.pdf",
    },
]

# ---------------------------------------------------------------
# Render worksheet cards
# ---------------------------------------------------------------
with tab_library:
    topics = ["All"] + sorted({w["topic"] for w in WORKSHEETS})
    selected_topic = st.selectbox("Filter by topic", topics)

    for w in WORKSHEETS:
        if selected_topic != "All" and w["topic"] != selected_topic:
            continue

        pdf_path = ASSETS / w["file"]

        ccss_pills = "".join(f'<span class="pill pill-ccss">{c}</span>' for c in w["ccss"])
        mi_pills = "".join(f'<span class="pill pill-mi">{m}</span>' for m in w["mi"])
        topic_pill = f'<span class="pill pill-topic">{w["topic"]}</span>'

        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">{w['title']}</div>
                <div class="card-desc">{w['desc']}</div>
                {topic_pill}<br>
                {ccss_pills}<br>
                {mi_pills}
            </div>
            """,
            unsafe_allow_html=True,
        )

        if pdf_path.exists():
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label=f"⬇ Download PDF — {w['title']}",
                    data=f.read(),
                    file_name=w["file"],
                    mime="application/pdf",
                    key=w["file"],
                )
        else:
            st.warning(f"Missing file: {w['file']} (place it in the assets/ folder)")

        st.write("")

    st.divider()
    st.caption(
        "Michigan's K-12 Standards for Mathematics use the same content and numbering as the "
        "Common Core State Standards, prefixed 'MI.Math.Content.' instead of 'CCSS.MATH.CONTENT.' — "
        "both labels are shown above for each worksheet."
    )

# ---------------------------------------------------------------
# Bonus tab: the mirror-angle / quadrant puzzle we worked through,
# turned into a small interactive structure simulation
# ---------------------------------------------------------------
with tab_bonus:
    st.markdown(
        """
        <div class="card">
            <div class="card-title">🧭 Which Quadrant? A Mirror-Angle Puzzle</div>
            <div class="card-desc">
                Take any line out of the origin. Mirror it 90°, and mirror it again halfway there, at 45°.
                Both mirrors land inside the same 90° wedge as the original line — and that wedge is always
                one of the four quadrants. Pick a starting angle below and watch it happen.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    preset = st.select_slider(
        "Starting angle of the original line",
        options=[0, 90, 180, 270],
        value=0,
        format_func=lambda d: f"{d}°",
    )

    fig = draw_mirror_plot(preset)
    col_plot, col_info = st.columns([1.1, 1])
    with col_plot:
        st.pyplot(fig, use_container_width=True)
    with col_info:
        st.markdown(f"**Original line:** {preset}°")
        st.markdown(f"**90° mirror:** {(preset + 90) % 360}°")
        st.markdown(f"**45° mirror (bisector):** {(preset + 45) % 360}°")
        st.markdown(f"**Quadrant filled:** :violet[{wedge_quadrant(preset)}]")

    st.write("")
    st.markdown("##### Try any angle, not just the neat ones")
    free_angle = st.slider("Original line angle (any degree, 0–359)", 0, 359, 20)
    fig2 = draw_mirror_plot(free_angle)
    st.pyplot(fig2, use_container_width=True)
    st.markdown(
        f"That line sits **{quadrant_of_angle(free_angle)}**, its 90° mirror sits "
        f"**{quadrant_of_angle(free_angle + 90)}**, and its 45° mirror sits "
        f"**{quadrant_of_angle(free_angle + 45)}**."
    )
    if free_angle % 90 != 0:
        st.info(
            "Notice that when the starting angle isn't a clean multiple of 90°, the wedge "
            "between the two mirrors actually straddles **two** quadrants instead of filling "
            "just one. Try dragging back to 0°, 90°, 180°, or 270° above to see it snap into "
            "a single quadrant again."
        )

    st.divider()

    st.markdown("### Why This Kind of Simulation Matters")
    st.markdown(
        """
Dragging that slider is a tiny **structure simulation** — a model you can move through, instead of a
static drawing. That's the same idea behind the *Line → Area → Volume* worksheet: a shape isn't just a
picture, it's a **rule you can run**. A line rotated by a *function* of the angle sweeps out a plane; a
plane mirrored across a *perpendicular* plane sweeps out a solid. Once you can picture the rule moving,
you can predict where it lands before you even draw it — which is exactly what a mathematician (or a
programmer building a simulation) is doing.

This is also why the **vocabulary matters** so much here, not as a side detail but as the actual tool
for thinking:

- **Plane** — you can't picture "the surface something reflects across" without a word for the
  surface itself.
- **Perpendicular** — without this word, "90°" is just a number; *with* it, you have a mental picture
  of two things meeting square-on, which is what makes the mirror trick predictable.
- **Quadrant** — turns "somewhere on the grid" into one of four exact, nameable regions you can reason
  about and compare.
- **Function** — the idea that one thing (the mirrored angle) is *produced by a rule* from another
  thing (the original angle), which is the whole reason the slider above is predictable instead of random.

Precise vocabulary is what lets you hold a moving structure in your head, describe it to someone else
exactly, and reason about what happens next — which is the real skill underneath both this puzzle and
the *Crack the Math Code!* worksheet in the library tab.
        """
    )
