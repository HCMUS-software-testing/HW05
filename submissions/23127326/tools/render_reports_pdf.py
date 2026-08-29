#!/usr/bin/env python3
"""Create compact, Unicode-safe PDF deliverables from the completed reports."""

from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph,
                                Spacer, Table, TableStyle, PageBreak)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "report"
FONT = "/System/Library/Fonts/Supplemental/Arial.ttf"
BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
pdfmetrics.registerFont(TTFont("Arial", FONT))
pdfmetrics.registerFont(TTFont("Arial-Bold", BOLD))


def p(text, style):
    return Paragraph(escape(text).replace("\n", "<br/>") , style)


def make_styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle("title", parent=base["Title"], fontName="Arial-Bold", fontSize=19, leading=24, textColor=colors.HexColor("#123B5D"), alignment=TA_CENTER, spaceAfter=9*mm),
        "h1": ParagraphStyle("h1", parent=base["Heading1"], fontName="Arial-Bold", fontSize=13, leading=16, textColor=colors.HexColor("#123B5D"), spaceBefore=5*mm, spaceAfter=2*mm),
        "h2": ParagraphStyle("h2", parent=base["Heading2"], fontName="Arial-Bold", fontSize=10.5, leading=13, textColor=colors.HexColor("#1E6A8D"), spaceBefore=3*mm, spaceAfter=1.5*mm),
        "body": ParagraphStyle("body", parent=base["BodyText"], fontName="Arial", fontSize=8.8, leading=12, spaceAfter=2.2*mm),
        "small": ParagraphStyle("small", parent=base["BodyText"], fontName="Arial", fontSize=7.6, leading=9.5, textColor=colors.HexColor("#4B5563")),
        "cell": ParagraphStyle("cell", parent=base["BodyText"], fontName="Arial", fontSize=7.2, leading=9),
        "cellb": ParagraphStyle("cellb", parent=base["BodyText"], fontName="Arial-Bold", fontSize=7.2, leading=9),
    }


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#D5E3EA"))
    canvas.line(18*mm, 14*mm, 192*mm, 14*mm)
    canvas.setFont("Arial", 7)
    canvas.setFillColor(colors.HexColor("#64748B"))
    canvas.drawString(18*mm, 9*mm, "HW05 Performance Testing | MSSV 23127326")
    canvas.drawRightString(192*mm, 9*mm, f"Page {doc.page}")
    canvas.restoreState()


def doc(path):
    frame = Frame(18*mm, 18*mm, 174*mm, 260*mm, id="normal")
    return BaseDocTemplate(str(path), pagesize=A4, leftMargin=18*mm, rightMargin=18*mm, topMargin=16*mm, bottomMargin=18*mm, pageTemplates=[PageTemplate(id="main", frames=[frame], onPage=header_footer)])


def table(rows, widths, styles):
    data = []
    for ridx, row in enumerate(rows):
        data.append([Paragraph(escape(str(x)), styles["cellb" if ridx == 0 else "cell"]) for x in row])
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DCEAF1")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#123B5D")),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#B8C9D2")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def main_report(styles):
    path = OUT / "main-report.pdf"
    story = [p("HW05 Performance Test Report", styles["title"]), p("Student ID 23127326 | Local run date 2026-08-30", styles["small"]), Spacer(1, 4*mm)]
    story += [p("1. Execution context", styles["h1"]), table([
        ["Field", "Value"], ["SUT", "http://localhost:3000 | commit 85af3ba875c88283615e22cb108f13e2fccaf0e9"],
        ["Host", "MacBook Pro 18,3 | Apple M1 Pro | 10 cores | 32 GB RAM | macOS 26.5.2"], ["Tool", "Apache JMeter 5.6.3 | Java 21 | headless non-GUI run"],
    ], [32*mm, 142*mm], styles)]
    story += [p("2. Workflow", styles["h1"]), p("Lockout probe -> valid login -> product search -> cart add -> cart quantity update -> cart read -> checkout -> post-checkout cart assertion. Each official VU uses a distinct synthetic account and a per-VU CSV file.", styles["body"])]
    story += [p("3. Scenario results", styles["h1"]), table([
        ["Scenario", "Samples", "HTTP err", "Assertion gap", "p95 overall / max label", "TPS"],
        ["Load", "3,314", "0 (0.00%)", "359 (10.83%)", "5 / 7 ms", "9.2766"],
        ["Stress", "16,519", "0 (0.00%)", "1,789 (10.83%)", "6 / 8 ms", "34.5021"],
        ["Spike", "7,175", "0 (0.00%)", "753 (10.49%)", "6 / 9 ms", "17.1743"],
        ["Endurance", "24,608", "0 (0.00%)", "2,700 (10.97%)", "5 / 7 ms", "30.4317"],
    ], [25*mm, 19*mm, 20*mm, 28*mm, 42*mm, 20*mm], styles), p("Weighted mean: Load 2.435 ms; Stress 2.297 ms; Spike 2.437 ms; Endurance 1.888 ms. Full label-level p50/p90/p95/p99/max is in report/metrics-20260830/*.json.", styles["small"])]
    story += [p("4. Interpretation", styles["h1"]), p("All failed samples are the explicit POST_CHECKOUT_CART - expected empty assertion. The SUT leaves the cart non-empty after checkout. Therefore the 10.49-10.97% failure rates are business-gap evidence, not transport or HTTP failure. Response times are below the provisional 1,000 ms p95 threshold.", styles["body"]), p("Resource conclusion is withheld. The official monitor used macOS-invalid ps field thcount and produced header-only files. The monitor tool is fixed to count threads with ps -M and validated with a real process sample, but that sample is not attributed to the four workload runs.", styles["body"])]
    story += [p("5. Reproduced SUT gaps", styles["h1"]), table([
        ["Gap", "Evidence"], ["Lockout", "Four responses: 401, 401, 403, 403; DB attempts 4; locked window 180 s. See evidence/issues/lockout-probe-20260830.jsonl."],
        ["Checkout cleanup", "Post-checkout assertion fails for every observed checkout in all four official workloads."], ["Pagination / duplicate line", "Implementation candidates retained; independent response probe still required before external issue."],
    ], [38*mm, 136*mm], styles)]
    story += [p("6. Reproduction and evidence", styles["h1"]), p("Raw JTL and JMeter HTML are under results/{load,stress,spike,endurance}. Plans are under test-plans. Synthetic data and provisioning scripts are under data/ and tools/. AI audit, critique and continuous-testing proposal are included. Video and GUI screenshots remain manual tasks for the student.", styles["body"])]
    d = doc(path); d.build(story); return path


def audit_report(styles):
    path = OUT / "ai-audit-report.pdf"
    story = [p("AI Audit Report", styles["title"]), p("MSSV 23127326 | Audit date 2026-08-30", styles["small"]), p("Declaration", styles["h1"]), p("AI was used for endpoint mapping, workload/test-plan design, JMeter XML generation, correlation/assertion review, JTL analyzer design, threshold proposal, human-review checklist and continuous performance-testing proposal.", styles["body"]), p("Interaction log", styles["h1"]), table([
        ["#", "Prompt / action", "Output and human review"], ["1", "Read plan and Vietnamese requirements.", "Established deliverables and constraints; checked manually."], ["2", "Review SUT API and backend.", "Found lockout, pagination, cart and checkout gaps; retained live evidence."], ["3", "Generate three JMeter plans.", "Human review found shared-CSV EOF unfairness; changed to per-VU CSV."], ["4", "Analyze four raw JTLs.", "HTTP errors 0; all failures are post-checkout assertions. JSON is reproducible."], ["5", "Propose optimization actions.", "Accepted contract-backed actions only; rejected CPU/RSS conclusion due invalid monitor."],
    ], [10*mm, 63*mm, 101*mm], styles), p("Human review checklist", styles["h1"])]
    for item in ["No raw JTL, screenshot, video, metric or issue was fabricated.", "Every VU uses a distinct account and per-VU CSV lifecycle.", "Lockout probe is separate from positive workloads and reset is documented.", "Listener views are not treated as non-GUI measurements.", "HTTP errors are separated from business-gap assertions.", "Metrics are reproducible from raw JTL.", "Optimization claims are classified by implementation/profiling evidence.", "GUI screenshots and student video remain pending."]:
        story.append(p("[x] " + item if not item.endswith("pending.") else "[ ] " + item, styles["body"]))
    d = doc(path); d.build(story); return path


def critique_report(styles):
    path = OUT / "ai-critique.pdf"
    text = ("AI giúp chuyển yêu cầu thành workflow, correlation token, CSV data-driven và ba workload JMeter khá nhanh. "
            "Phần có giá trị nhất là việc đọc cả API contract lẫn backend: nếu chỉ nhìn HTTP 200, người kiểm thử dễ bỏ qua lockout cộng sai số lần, thời gian khóa 180 giây thay vì 30 giây, pagination không được áp dụng, cart thêm dòng trùng và checkout không dọn cart. Raw JTL đã xác nhận một gap: Load 359/3,314, Stress 1,789/16,519, Spike 753/7,175 và Endurance 2,700/24,608 đều fail đúng assertion cart sau checkout; HTTP error ở cả bốn run là 0. Vì vậy không được gọi 10-11% này là server failure.\n\n"
            "AI cũng từng tạo rủi ro kỹ thuật: CSV dùng chung làm thread đầu tiên tiêu thụ dữ liệu, và hiểu nhầm duration của JMeter khiến run sớm bị loại. Human review đã phát hiện, chuyển sang một file input cho mỗi VU, dùng 60 dòng lặp có kiểm soát, tách run invalid, rồi chạy lại bộ chính thức. Đây là lý do không nên tin JMX trông hợp lý nếu chưa kiểm tra lifecycle dữ liệu, số thread thực tế, label và raw response.\n\n"
            "Các khuyến nghị như index, connection pool, WAL hoặc tối ưu SQL chỉ là giả thuyết khi chưa có profiler. Resource monitor chính thức cũng không được diễn giải: field thcount không tồn tại trên macOS nên các file cũ chỉ có header. Tôi đã sửa tool và xác nhận bằng mẫu process thật, nhưng không gán mẫu đó cho bốn workload. Kết luận phải truy nguyên về implementation, JTL và evidence; phần screenshot/video vẫn cần sinh viên bổ sung.")
    story = [p("AI Critique", styles["title"]), p("Human-reviewed critique of the AI-assisted workflow", styles["small"]), p(text, styles["body"]), p("Source evidence: raw JTLs, SUT commit, lockout probe, metrics-20260830/*.json and monitor-pid-check-20260830-v6.csv.", styles["small"])]
    d = doc(path); d.build(story); return path


if __name__ == "__main__":
    styles = make_styles()
    OUT.mkdir(parents=True, exist_ok=True)
    for fn in (main_report, audit_report, critique_report):
        print(fn(styles))
