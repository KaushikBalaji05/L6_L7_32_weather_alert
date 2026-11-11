# -*- coding: utf-8 -*-
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, HRFlowable, KeepTogether
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return
        
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))
        
        # Header
        self.drawString(54, 11 * 72 - 36, "Lab 7: Fuzzing for Input Validation Bugs -- Weather Alert Classifier")
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.5)
        self.line(54, 11 * 72 - 40, 8.5 * 72 - 54, 11 * 72 - 40)
        
        # Footer
        page_text = "Page " + str(self._pageNumber) + " of " + str(page_count)
        self.drawRightString(8.5 * 72 - 54, 34, page_text)
        self.drawString(54, 34, "SETA Lab 7 Report | L6_L7_32_weather_alert")
        self.line(54, 44, 8.5 * 72 - 54, 44)
        
        self.restoreState()


def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=48,
        bottomMargin=48
    )

    styles = getSampleStyleSheet()

    primary_color = colors.HexColor("#1A365D")
    secondary_color = colors.HexColor("#2B6CB0")
    dark_text = colors.HexColor("#2D3748")

    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=28,
        textColor=primary_color,
        alignment=1,
        spaceAfter=10
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=secondary_color,
        alignment=1,
        spaceAfter=18
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=primary_color,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=dark_text,
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#2C5282")
    )

    caption_style = ParagraphStyle(
        'Caption_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#4A5568"),
        alignment=1,
        spaceBefore=3,
        spaceAfter=6
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=dark_text
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=colors.white
    )

    story = []

    # =========================================================================
    # PAGE 1: TITLE & COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 35))
    story.append(Paragraph("LABORATORY REPORT", subtitle_style))
    story.append(Paragraph("Lab 7: Fuzzing for Input Validation Bugs", title_style))
    story.append(Paragraph("Automated Vulnerability Detection, Hypothesis Property-Based Fuzz Testing, and Defensive Hardening", subtitle_style))
    
    story.append(HRFlowable(width="65%", thickness=2, color=primary_color, spaceBefore=8, spaceAfter=20))

    meta_data = [
        [Paragraph("<b>Course:</b>", table_cell), Paragraph("Software Engineering: Testing and Automation (SETA)", table_cell)],
        [Paragraph("<b>Institution:</b>", table_cell), Paragraph("PES University", table_cell)],
        [Paragraph("<b>Repository:</b>", table_cell), Paragraph("SETAPESU26/L6_L7_32_weather_alert", table_cell)],
        [Paragraph("<b>Fork / Student:</b>", table_cell), Paragraph("Kaushik Balaji (KaushikBalaji05)", table_cell)],
        [Paragraph("<b>Scenario:</b>", table_cell), Paragraph("Weather Alert Classifier &amp; Meteorological Data Processor", table_cell)],
        [Paragraph("<b>Fuzzing Tool:</b>", table_cell), Paragraph("Hypothesis 6.170.15 (Python 3.13.7, pytest 9.1.1)", table_cell)],
        [Paragraph("<b>Date:</b>", table_cell), Paragraph("November 2026", table_cell)],
    ]
    meta_table = Table(meta_data, colWidths=[120, 340])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F7FAFC")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E0")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(meta_table)

    story.append(Spacer(1, 25))

    exec_text = (
        "<b>Executive Summary:</b> In this lab, we evaluated property-based fuzz testing as an automated "
        "vulnerability discovery and quality assurance technique. Using the <b>Hypothesis</b> fuzzing framework, "
        "we subjected three core meteorological data functions (<code>parse_reading</code>, <code>wind_category</code>, "
        "and <code>rainfall_spread</code>) to randomized Unicode text, empty inputs, malformed structures, "
        "and unexpected types (such as <code>None</code>). Hypothesis uncovered multiple critical vulnerabilities, including "
        "uncaught <code>ValueError</code>, <code>AttributeError</code>, and <code>TypeError</code> exceptions, as well as logical defects "
        "such as permitting physically invalid negative wind speeds and rainfall values. Through defensive validation and "
        "safe fallback semantics, all three functions were hardened to prevent crashes and enforce physical constraints while "
        "maintaining 100% backward compatibility for valid operational data."
    )
    exec_table = Table([[Paragraph(exec_text, body_style)]], colWidths=[460])
    exec_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EBF8FF")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#63B3ED")),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(exec_table)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: OBJECTIVES, TOOLS, METHODOLOGY, TARGET FUNCTIONS
    # =========================================================================
    story.append(Paragraph("1. Objective &amp; Learning Outcomes", h1_style))
    story.append(Paragraph(
        "The objective of this laboratory is to explore fuzz testing as a dynamic security and quality assurance methodology. "
        "Specifically, the experiment aims to: (1) Understand the limitations of example-based unit testing and the advantages of "
        "property-based fuzzing; (2) Apply Hypothesis to weather alert modules; (3) Uncover unhandled crashes and edge cases; "
        "(4) Analyze minimal counterexamples; and (5) Harden the codebase with defensive programming.", body_style
    ))

    story.append(Paragraph("2. Tools and Technologies", h1_style))
    tools_data = [
        [Paragraph("Tool / Component", table_header), Paragraph("Version", table_header), Paragraph("Role in Lab", table_header)],
        [Paragraph("Python", table_cell), Paragraph("3.13.7", table_cell), Paragraph("Runtime environment for execution and validation", table_cell)],
        [Paragraph("pytest", table_cell), Paragraph("9.1.1", table_cell), Paragraph("Test execution framework and test session orchestrator", table_cell)],
        [Paragraph("Hypothesis", table_cell), Paragraph("6.170.15", table_cell), Paragraph("Property-based fuzz testing and test case shrinking engine", table_cell)],
        [Paragraph("ReportLab &amp; Pillow", table_cell), Paragraph("4.4.10 / 11.3.0", table_cell), Paragraph("Evidence rendering and automated PDF documentation", table_cell)],
        [Paragraph("Git", table_cell), Paragraph("2.x", table_cell), Paragraph("Version control, branch preservation, and remote synchronization", table_cell)]
    ]
    tools_table = Table(tools_data, colWidths=[110, 75, 275])
    tools_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(tools_table)

    story.append(Paragraph("3. Understanding Hypothesis &amp; Property-Based Fuzz Testing", h1_style))
    story.append(Paragraph(
        "Traditional unit tests test only anticipated scenarios (e.g. <code>parse_reading('35.5/80')</code>). "
        "In contrast, <b>Hypothesis</b> generates hundreds of semi-random, edge-case, and malformed inputs to verify invariant properties. "
        "When an input causes a failure, Hypothesis applies <b>test-case shrinking</b> to find the minimal counterexample.", body_style
    ))

    story.append(Paragraph("4. Target Functions Under Test", h1_style))
    func_data = [
        [Paragraph("Function", table_header), Paragraph("Expected Purpose", table_header), Paragraph("Input Type", table_header), Paragraph("Original Implementation", table_header)],
        [
            Paragraph("<code>parse_reading(text)</code>", table_cell),
            Paragraph("Splits temperature and relative humidity reading.", table_cell),
            Paragraph("String (<code>'35.5/80'</code>)", table_cell),
            Paragraph("<code>temp, hum = text.split('/')<br/>return float(temp), int(hum)</code>", code_style)
        ],
        [
            Paragraph("<code>wind_category(speed_text)</code>", table_cell),
            Paragraph("Maps wind speed to warning, advisory, or none.", table_cell),
            Paragraph("Integer string (<code>'45'</code>)", table_cell),
            Paragraph("<code>speed = int(speed_text)<br/>if speed >= 89: 'warning'<br/>elif speed >= 39: 'advisory'<br/>return 'none'</code>", code_style)
        ],
        [
            Paragraph("<code>rainfall_spread(readings_csv)</code>", table_cell),
            Paragraph("Calculates range (max - min) across hourly rainfall measurements.", table_cell),
            Paragraph("CSV numbers (<code>'2,5.5,10'</code>)", table_cell),
            Paragraph("<code>r = [float(x) for x in readings_csv.split(',')spread]<br/>return max(r) - min(r)</code>", code_style)
        ]
    ]
    func_table = Table(func_data, colWidths=[95, 120, 105, 140])
    func_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), secondary_color),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(func_table)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: ORIGINAL EXECUTION & INITIAL FAILING FUZZ TESTS
    # =========================================================================
    story.append(Paragraph("5. Original Application Execution", h1_style))
    story.append(Paragraph(
        "Before modifying the codebase, we established a baseline by executing the original <code>processor.py</code> "
        "interactively with valid inputs (<code>'35.5/80'</code>, <code>'45'</code>, <code>'2,5.5,10'</code>). Under ideal inputs, it executes normally:",
        body_style
    ))

    ev_path_1 = r"C:\Users\kaush\L6_L7_32_weather_alert\lab7\evidence\01_original_processor.png"
    if os.path.exists(ev_path_1):
        img1 = Image(ev_path_1, width=460, height=460 * (420 / 950))
        story.append(KeepTogether([
            img1,
            Paragraph("<b>Figure 1:</b> Baseline execution of the original <code>processor.py</code> with typical valid inputs.", caption_style)
        ]))

    story.append(Paragraph("6. Initial Hypothesis Fuzz Failures", h1_style))
    story.append(Paragraph(
        "We executed <code>pytest -v test_processor.py</code> against the original buggy implementation. Hypothesis immediately uncovered "
        "6 failures across all three functions due to unhandled exceptions and missing input validation:",
        body_style
    ))

    ev_path_2 = r"C:\Users\kaush\L6_L7_32_weather_alert\lab7\evidence\02_initial_fuzz_failures.png"
    if os.path.exists(ev_path_2):
        img2 = Image(ev_path_2, width=460, height=460 * (600 / 950) * 0.75)
        story.append(KeepTogether([
            img2,
            Paragraph("<b>Figure 2:</b> Initial pytest execution showing 6 test failures uncovered by Hypothesis.", caption_style)
        ]))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: BUG ANALYSIS, MINIMAL COUNTEREXAMPLES & IMPLEMENTED FIXES
    # =========================================================================
    story.append(Paragraph("7. Analysis of Discovered Bugs and Minimal Counterexamples", h1_style))
    story.append(Paragraph(
        "Hypothesis successfully shrank failing test cases to minimal counterexamples, pinpointing exact root causes:",
        body_style
    ))

    ev_path_3 = r"C:\Users\kaush\L6_L7_32_weather_alert\lab7\evidence\03_failure_analysis.png"
    if os.path.exists(ev_path_3):
        img3 = Image(ev_path_3, width=460, height=460 * (620 / 950) * 0.70)
        story.append(KeepTogether([
            img3,
            Paragraph("<b>Figure 3:</b> Pytest failure traces showing minimal counterexamples and unhandled exceptions.", caption_style)
        ]))

    bugs_table_data = [
        [Paragraph("Function", table_header), Paragraph("Minimal Counterexample", table_header), Paragraph("Observed Crash / Bug", table_header), Paragraph("Root Cause", table_header)],
        [
            Paragraph("<code>parse_reading</code>", table_cell),
            Paragraph("<code>s = '/'</code><br/><code>s = ''</code><br/><code>s = None</code>", code_style),
            Paragraph("<code>ValueError: could not convert string to float: ''</code><br/><code>ValueError: not enough values to unpack</code><br/><code>AttributeError: 'NoneType' has no split</code>", table_cell),
            Paragraph("Directly split string without verifying presence of delimiter or valid numbers.", table_cell)
        ],
        [
            Paragraph("<code>wind_category</code>", table_cell),
            Paragraph("<code>s = ''</code><br/><code>s = None</code><br/><code>s = '-1'</code>", code_style),
            Paragraph("<code>ValueError: invalid literal for int()</code><br/><code>TypeError: int() arg must be str...</code><br/>Allowed <code>'-1'</code> and returned <code>'none'</code>", table_cell),
            Paragraph("Direct conversion to <code>int()</code> without validation; failed to reject negative speeds.", table_cell)
        ],
        [
            Paragraph("<code>rainfall_spread</code>", table_cell),
            Paragraph("<code>s = ''</code><br/><code>s = None</code><br/><code>s = '-5,10'</code>", code_style),
            Paragraph("<code>ValueError: could not convert string to float: ''</code><br/><code>AttributeError: 'NoneType' has no split</code><br/>Allowed negative rainfall", table_cell),
            Paragraph("Splitting empty string produces <code>['']</code>; no validation for empty tokens or negative rainfall.", table_cell)
        ]
    ]
    bugs_table = Table(bugs_table_data, colWidths=[85, 105, 150, 120])
    bugs_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(bugs_table)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: POST-FIX EXECUTION & FINAL PYTEST VERIFICATION
    # =========================================================================
    story.append(Paragraph("8. Defensive Hardening Implementation", h1_style))
    story.append(Paragraph(
        "All three functions were hardened using defensive programming principles: (1) <b><code>parse_reading</code></b> verifies string type, "
        "token count, numerical bounds (-100 to 100&deg;C, 0-100% humidity), and rejects NaN/Inf with <code>None</code>; (2) <b><code>wind_category</code></b> "
        "verifies integer digits, rejects booleans, floats, negative speeds (< 0), and unreal values (> 500 km/h) with <code>None</code>; "
        "(3) <b><code>rainfall_spread</code></b> verifies non-empty elements, valid non-negative floats (0-2000 mm), and rounds spread to 4 decimals.", body_style
    ))

    story.append(Paragraph("9. Execution of Fixed Application", h1_style))
    ev_path_4 = r"C:\Users\kaush\L6_L7_32_weather_alert\lab7\evidence\04_fixed_processor.png"
    if os.path.exists(ev_path_4):
        img4 = Image(ev_path_4, width=460, height=460 * (460 / 950) * 0.85)
        story.append(KeepTogether([
            img4,
            Paragraph("<b>Figure 4:</b> Execution of hardened <code>processor.py</code> showing correct output for valid inputs and safe fallback for edge cases.", caption_style)
        ]))

    story.append(Paragraph("10. Final Pytest Verification (100% Passing)", h1_style))
    ev_path_5 = r"C:\Users\kaush\L6_L7_32_weather_alert\lab7\evidence\05_final_passing_tests.png"
    if os.path.exists(ev_path_5):
        img5 = Image(ev_path_5, width=460, height=460 * (500 / 950) * 0.85)
        story.append(KeepTogether([
            img5,
            Paragraph("<b>Figure 5:</b> Final pytest execution showing all 9 Hypothesis tests passing with zero failures.", caption_style)
        ]))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: COMPARISON TABLE, LAB 6 INTEGRITY & CONCLUSION
    # =========================================================================
    story.append(Paragraph("11. Before vs After Test Results Comparison", h1_style))
    comp_data = [
        [Paragraph("Test Function", table_header), Paragraph("Initial Status", table_header), Paragraph("Final Status", table_header), Paragraph("Verification Notes", table_header)],
        [
            Paragraph("<code>test_parse_reading_no_crash</code>", table_cell),
            Paragraph("<font color='#E53E3E'><b>FAILED (3 crashes)</b></font>", table_cell),
            Paragraph("<font color='#38A169'><b>PASSED</b></font>", table_cell),
            Paragraph("Survives random Unicode, delimiters, and None.", table_cell)
        ],
        [
            Paragraph("<code>test_wind_category_no_crash</code>", table_cell),
            Paragraph("<font color='#E53E3E'><b>FAILED (2 crashes)</b></font>", table_cell),
            Paragraph("<font color='#38A169'><b>PASSED</b></font>", table_cell),
            Paragraph("Survives non-numeric strings, empty strings, and None.", table_cell)
        ],
        [
            Paragraph("<code>test_rainfall_spread_no_crash</code>", table_cell),
            Paragraph("<font color='#E53E3E'><b>FAILED (2 crashes)</b></font>", table_cell),
            Paragraph("<font color='#38A169'><b>PASSED</b></font>", table_cell),
            Paragraph("Survives trailing commas, empty tokens, and None.", table_cell)
        ],
        [
            Paragraph("<code>test_parse_reading_valid_inputs</code>", table_cell),
            Paragraph("<font color='#38A169'><b>PASSED</b></font>", table_cell),
            Paragraph("<font color='#38A169'><b>PASSED</b></font>", table_cell),
            Paragraph("Valid temperatures (-50 to 60&deg;C) and humidity (0-100%).", table_cell)
        ],
        [
            Paragraph("<code>test_wind_category_valid_inputs</code>", table_cell),
            Paragraph("<font color='#38A169'><b>PASSED</b></font>", table_cell),
            Paragraph("<font color='#38A169'><b>PASSED</b></font>", table_cell),
            Paragraph("Full range (0 to 300 km/h) mapped to correct thresholds.", table_cell)
        ],
        [
            Paragraph("<code>test_rainfall_spread_valid_inputs</code>", table_cell),
            Paragraph("<font color='#38A169'><b>PASSED</b></font>", table_cell),
            Paragraph("<font color='#38A169'><b>PASSED</b></font>", table_cell),
            Paragraph("Arbitrary list sizes (1 to 20) correctly calculate spread.", table_cell)
        ],
        [
            Paragraph("<code>test_parse_reading_invalid_inputs</code>", table_cell),
            Paragraph("<font color='#E53E3E'><b>FAILED (crashes)</b></font>", table_cell),
            Paragraph("<font color='#38A169'><b>PASSED</b></font>", table_cell),
            Paragraph("Safely returns None on corrupted formats.", table_cell)
        ],
        [
            Paragraph("<code>test_wind_category_invalid_inputs</code>", table_cell),
            Paragraph("<font color='#E53E3E'><b>FAILED (allowed -1)</b></font>", table_cell),
            Paragraph("<font color='#38A169'><b>PASSED</b></font>", table_cell),
            Paragraph("Strictly rejects negative speeds with None.", table_cell)
        ],
        [
            Paragraph("<code>test_rainfall_spread_invalid_inputs</code>", table_cell),
            Paragraph("<font color='#E53E3E'><b>FAILED (allowed -5)</b></font>", table_cell),
            Paragraph("<font color='#38A169'><b>PASSED</b></font>", table_cell),
            Paragraph("Strictly rejects negative readings with None.", table_cell)
        ]
    ]
    comp_table = Table(comp_data, colWidths=[150, 95, 80, 135])
    comp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(comp_table)

    story.append(Paragraph("12. Lab 6 Backward Compatibility &amp; Regression Integrity", h1_style))
    story.append(Paragraph(
        "To ensure zero regression on existing coursework, all 56 Lab 6 tests "
        "(<code>test_weather_alert.py</code>, <code>CodeCoverageTest_weather_alert.py</code>, and <code>BranchCoverageTest_weather_alert.py</code>) "
        "were re-executed in <code>lab6/</code>. <b>All 56 tests passed completely</b> (100% pass rate), confirming that Lab 6 functionality and deliverables remain intact.",
        body_style
    ))

    story.append(Paragraph("13. Conclusion", h1_style))
    story.append(Paragraph(
        "This laboratory clearly demonstrated the superiority of property-based fuzz testing over manual test writing for uncovering unexpected "
        "boundary and validation bugs. By combining Hypothesis test generation, counterexample shrinking, and defensive programming, "
        "we eliminated multiple crash vectors, enforced strict meteorological validity constraints, and elevated software robustness to production grade.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {filename}")

if __name__ == "__main__":
    out_pdf = r"C:\Users\kaush\L6_L7_32_weather_alert\lab7\Lab7_FuzzTesting_Final_Report.pdf"
    build_pdf(out_pdf)