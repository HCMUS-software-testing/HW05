#!/usr/bin/env python3
"""Tạo các PDF ngắn gọn, hỗ trợ Unicode từ báo cáo đã hoàn thiện."""

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
    canvas.drawString(18*mm, 9*mm, "HW05 Kiểm thử hiệu năng | MSSV 23127326")
    canvas.drawRightString(192*mm, 9*mm, f"Trang {doc.page}")
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
    story = [p("Báo cáo kiểm thử hiệu năng HW05", styles["title"]), p("MSSV 23127326 | Ngày chạy local 2026-08-30", styles["small"]), Spacer(1, 4*mm)]
    story += [p("1. Bối cảnh thực thi", styles["h1"]), table([
        ["Trường", "Giá trị"], ["SUT", "http://localhost:3000 | commit 85af3ba875c88283615e22cb108f13e2fccaf0e9"],
        ["Máy đo", "MacBook Pro 18,3 | Apple M1 Pro | 10 cores | 32 GB RAM | macOS 26.5.2"], ["Công cụ", "Apache JMeter 5.6.3 | Java 21 | chạy non-GUI"],
    ], [32*mm, 142*mm], styles)]
    story += [p("2. Workflow", styles["h1"]), p("Lockout probe -> login hợp lệ -> tìm sản phẩm -> thêm cart -> gửi quantity cập nhật -> đọc cart -> checkout -> assertion cart sau checkout. Mỗi VU chính thức dùng một tài khoản kiểm thử riêng và một file CSV riêng.", styles["body"])]
    story += [p("3. Kết quả kịch bản", styles["h1"]), table([
        ["Kịch bản", "Mẫu", "Lỗi HTTP", "Gap assertion", "p95 tổng / max label", "RPS"],
        ["Load", "3,287", "0 (0.00%)", "356 (10.83%)", "6 / 7 ms", "9.1583"],
        ["Stress", "16,433", "0 (0.00%)", "1,780 (10.83%)", "5 / 7 ms", "34.4137"],
        ["Spike", "7,171", "0 (0.00%)", "751 (10.47%)", "5 / 7 ms", "17.1228"],
        ["Endurance", "24,574", "0 (0.00%)", "2,699 (10.98%)", "6 / 8 ms", "30.4315"],
    ], [25*mm, 19*mm, 20*mm, 28*mm, 42*mm, 20*mm], styles), p("Mean tổng thể: Load 2.642 ms; Stress 1.914 ms; Spike 2.041 ms; Endurance 2.443 ms. Monitor resource: CPU tối đa 16,4-25,5%; RSS tối đa 75,8-120,8 MB; tối đa 11 thread.", styles["small"])]
    story += [p("4. Diễn giải", styles["h1"]), p("Tất cả mẫu fail là assertion cụ thể POST_CHECKOUT_CART - expected empty. SUT để cart không rỗng sau checkout. Vì vậy tỷ lệ fail 10,47-10,98% là bằng chứng gap nghiệp vụ, không phải lỗi transport hoặc HTTP. Response time thấp hơn threshold p95 1.000 ms.", styles["body"]), p("Lần rerun resource dùng monitor macOS đã sửa. RSS Endurance dao động 70,1-85,6 MB trong lần chạy local 13,5 phút; không kết luận leak ngoài mẫu này.", styles["body"])]
    story += [p("5. Gap SUT đã tái hiện", styles["h1"]), table([
        ["Gap", "Bằng chứng"], ["Lockout", "Bốn response: 401, 401, 403, 403; DB attempts 4; thời gian khóa 180 s. Xem evidence/issues/lockout-probe-20260830.jsonl."],
        ["Dọn cart sau checkout", "Assertion sau checkout fail ở mọi checkout quan sát được trong bốn workload."], ["Pagination / dòng cart trùng", "Đã có response probe độc lập trong evidence/issues/."],
    ], [38*mm, 136*mm], styles)]
    story += [p("6. Tái hiện và bằng chứng", styles["h1"]), p("JTL thô và HTML JMeter nằm trong results/{load,stress,spike,endurance}; resource-rerun có bản đo CPU/RSS/thread hợp lệ. Plan nằm trong test-plans; dữ liệu và script tạo fixture nằm trong data/ và tools/. AI audit, critique, đề xuất kiểm thử liên tục, hardware screenshot và GitHub Issue evidence được đính kèm. Video vẫn chờ sinh viên tự quay.", styles["body"])]
    d = doc(path); d.build(story); return path


def audit_report(styles):
    path = OUT / "ai-audit-report.pdf"
    story = [p("Báo cáo nhật ký sử dụng AI", styles["title"]), p("MSSV 23127326 | Ngày audit 2026-08-30", styles["small"]), p("Tuyên bố", styles["h1"]), p("AI được dùng để lập bản đồ endpoint, thiết kế workload/test plan, sinh XML JMeter, review correlation/assertion, thiết kế analyzer JTL, đề xuất threshold, checklist human review và đề xuất kiểm thử hiệu năng liên tục.", styles["body"]), p("Nhật ký tương tác", styles["h1"]), table([
        ["#", "Prompt / thao tác", "Output và review của người"], ["1", "Đọc plan và đề tiếng Việt.", "Xác định deliverable và ràng buộc; đối chiếu thủ công."], ["2", "Review API và backend SUT.", "Phát hiện gap lockout, pagination, cart, checkout; giữ evidence thật."], ["3", "Sinh ba JMeter plan.", "Human review phát hiện lỗi dùng chung CSV; chuyển sang CSV riêng từng VU."], ["4", "Phân tích bốn JTL thô.", "HTTP error 0%; mọi failure là assertion sau checkout; JSON truy nguyên được."], ["5", "Đề xuất tối ưu.", "Chỉ nhận claim có căn cứ; loại monitor cũ và rerun đủ bốn workload."], ["6", "Audit package và dịch tài liệu.", "Bổ sung summary, threshold, hardware screenshot, ảnh kết hợp và issue evidence."],
    ], [10*mm, 63*mm, 101*mm], styles), p("Checklist review của người", styles["h1"])]
    for item in ["Không bịa JTL, ảnh, video, metric hoặc issue.", "Mỗi VU dùng tài khoản riêng và lifecycle CSV riêng.", "Lockout probe tách khỏi positive workload và có hướng dẫn reset.", "Listener không được dùng làm số đo non-GUI chính thức.", "Tách lỗi HTTP khỏi assertion lỗi nghiệp vụ.", "Metric truy nguyên được về JTL thô.", "Claim tối ưu được phân loại theo bằng chứng implementation/profiling.", "Có ảnh JMeter, Activity Monitor, hardware và GitHub Issue evidence.", "Video demo vẫn chờ sinh viên tự quay."]:
        story.append(p("[x] " + item if not item.endswith("quay.") else "[ ] " + item, styles["body"]))
    d = doc(path); d.build(story); return path


def critique_report(styles):
    path = OUT / "ai-critique.pdf"
    text = ("AI giúp chuyển yêu cầu thành workflow, correlation token, dữ liệu CSV và ba workload JMeter. Giá trị lớn nhất là đọc API contract và backend: nếu chỉ nhìn HTTP 200, dễ bỏ qua lockout cộng sai số lần, thời gian khóa 180 giây thay vì 30 giây, pagination không được áp dụng, cart tạo dòng trùng và checkout không dọn cart. JTL thô xác nhận lỗi nghiệp vụ: Load 359/3.314, Stress 1.789/16.519, Spike 753/7.175 và Endurance 2.700/24.608; HTTP error ở cả bốn lần chạy là 0%. Vì vậy không được gọi tỷ lệ 10-11% này là server failure.\n\n"
            "AI cũng tạo rủi ro kỹ thuật: CSV dùng chung làm thread đầu tiên tiêu thụ dữ liệu, và hiểu nhầm duration của JMeter khiến một số lần chạy sớm bị loại. Human review phát hiện, chuyển sang một file input cho mỗi VU, dùng 60 dòng lặp có kiểm soát, tách run invalid rồi chạy lại bộ chính thức. JMX phải được kiểm tra bằng lifecycle dữ liệu, số thread, label và raw response.\n\n"
            "Các khuyến nghị như index, connection pool, WAL hoặc tối ưu SQL chỉ là giả thuyết khi chưa có profiler. Monitor đầu tiên cũng không được diễn giải vì thcount không tồn tại trên macOS. Sau khi sửa tool, bốn workload được rerun; CPU tối đa 16,4-25,5%, RSS tối đa 75,8-120,8 MB và tối đa 11 thread. Bài học chính: mọi kết luận phải truy nguyên về implementation, JTL và evidence; AI không thay thế trách nhiệm xác minh của tester.")
    story = [p("Phê bình việc cộng tác với AI", styles["title"]), p("Review của người đối với workflow có hỗ trợ AI", styles["small"]), p(text, styles["body"]), p("Evidence nguồn: JTL thô, commit SUT, lockout probe, JSON metric, JTL/HTML resource-rerun và monitor CPU/RSS/thread hợp lệ.", styles["small"])]
    d = doc(path); d.build(story); return path


if __name__ == "__main__":
    styles = make_styles()
    OUT.mkdir(parents=True, exist_ok=True)
    for fn in (main_report, audit_report, critique_report):
        print(fn(styles))
