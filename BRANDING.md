# Cisco Branding Guide for AI-RRM Reports

## Overview

The AI-RRM Report Generator follows Cisco's official brand guidelines to ensure professional, consistent visual communication. This document outlines the branding elements applied to PDF reports.

## Branding Elements

### 1. Color Palette

The report uses Cisco's official brand colors:

#### Primary Brand Colors
- **Cisco Blue (#049fd9)** - Main brand color used for headings, key elements
- **Cisco Blue Dark (#015269)** - Secondary brand color for contrast
- **Cisco Blue Light (#a8ecff)** - Accent and background elements

#### Additional Colors
- **Medium Blue (#0a60ff, #0e3a99)** - Used for data visualization
- **Midnight Blue (#07182d)** - Used for strong emphasis

#### Status Colors
- **Success Green (#2c6611)** - For healthy/good status indicators
- **Success Green Light (#c9f2b6)** - Background for success states
- **Warning Orange (#ff9000)** - For warnings and attention items
- **Warning Orange Light (#ffedd6)** - Background for warning states
- **Danger Red (#d91821)** - For critical/error states
- **Danger Red Light (#ffe8ea)** - Background for danger states

#### Neutrals
- **Gray Dark (#26384f)** - Primary text color
- **Gray Medium (#667180, #536070)** - Secondary text
- **Gray Light (#e1e6eb, #b9c1c9)** - Borders and dividers
- **Gray Lighter (#f2f5f7)** - Subtle backgrounds

### 2. Typography

- **Font Family**: Helvetica (Helvetica-Bold for emphasis)
- **Title**: 28pt, Cisco Blue
- **Headings**: 16pt, Cisco Blue Dark
- **Subheadings**: 12pt, Gray Dark
- **Body Text**: 10pt, Gray Dark
- **Small Text/Captions**: 8-9pt, Gray Medium

### 3. Logo Usage

#### Official Cisco Logo
The report supports displaying the official Cisco logo on the title page. 

**Logo Specifications:**
- Format: PNG or JPG (vector formats recommended for best quality)
- Recommended size: Minimum 300 DPI at 2.5 inches width
- Placement: Centered at top of title page
- Clear space: Maintains proper spacing around logo per Cisco guidelines

#### How to Add Logo

**Option 1: Command Line**
```bash
python airrm_report.py --logo /path/to/cisco_logo.png
```

**Option 2: Environment Variable**
```bash
export LOGO_PATH=/path/to/cisco_logo.png
python airrm_report.py
```

**Option 3: .env File**
```
LOGO_PATH=/path/to/cisco_logo.png
```

#### Logo Fallback
If no logo is provided, the report displays "Cisco" text branding in Cisco Blue to maintain brand identity.

### 4. Page Layout

#### Margins
- Top: 1.0 inch (accommodates branded header)
- Bottom: 1.0 inch (accommodates branded footer)
- Left/Right: 0.75 inch

#### Headers
- Cisco Blue line (3pt) at top of page
- Maintains clean, professional appearance

#### Footers
Every page includes:
- **Cisco brand name** (left side, Cisco Blue, bold)
- **Report title** "AI-RRM Performance Report" (center)
- **Page number** (right side)
- Cisco Blue separator line (1pt) above footer

### 5. Visual Elements

#### Tables
- Header background: Cisco Blue (#049fd9)
- Header text: White
- Alternating row colors: White / Gray Lighter
- Border: Gray Light
- Health scores: Color-coded backgrounds (success/warning/danger)

#### Status Indicators
- ✓ (checkmark) - Excellent/Good performance (80+)
- ⚠ (warning) - Fair performance (60-79) or active insights
- ✗ (cross) - Poor performance (<60)

#### Decorative Elements
- Decorative lines use Cisco Blue
- Boxes and containers use subtle gray backgrounds
- Important content highlighted with appropriate status colors

### 6. Content Organization

#### Title Page
1. Cisco logo (if provided) or Cisco brand name
2. Report title in Cisco Blue
3. Subtitle with generation timestamp
4. Decorative Cisco Blue line
5. Report introduction in subtle gray box

#### Report Sections
1. **Executive Summary** - KPIs in colored stat boxes (Cisco Blue)
2. **Buildings with Issues** - Detailed insights with color-coded severity
3. **Complete Building Inventory** - Comprehensive table with status indicators

## Obtaining Cisco Brand Assets

### Official Logo
To maintain brand integrity, use official Cisco logos:

1. **For Cisco Employees**: Download from Cisco Brand Center (internal)
2. **For Partners**: Request from your Cisco partner representative
3. **Public Resources**: Use official logos from Cisco's public brand guidelines

### Logo Guidelines
- Never modify, distort, or recolor the logo
- Maintain proper clear space around the logo
- Use high-resolution files for professional output
- Ensure logo is visible against backgrounds (use white backgrounds for best results)

## Compliance Notes

### Official Cisco Branding
This report generator implements Cisco brand guidelines for:
- Color palette consistency
- Typography standards
- Professional layout and spacing
- Clear visual hierarchy

### Web vs. Print
Note: This is a PDF/print-focused implementation. For web-based reports, use Cisco's web design tokens and CSS frameworks (e.g., Cisco UI Kit, Momentum Design).

### Design System
For more detailed Cisco design guidelines:
- Cisco Brand Center (internal employees)
- Cisco Partner Brand Portal (partners)
- Cisco Design Guidelines (public resources)

## Customization

### Modifying Branding
If you need to customize branding elements:

1. **Colors**: Edit the `COLORS` dictionary in `src/pdf_generator.py`
2. **Typography**: Adjust `ParagraphStyle` definitions in `PDFReportGenerator.__init__`
3. **Layout**: Modify margin parameters in `SimpleDocTemplate` initialization
4. **Logo**: Update logo path and sizing in `_add_title_page` method

**Important**: Maintain Cisco brand guidelines when making modifications.

## Support

For questions about:
- **Cisco brand guidelines**: Contact Cisco Brand Team
- **Report generator**: See project README.md
- **Technical implementation**: Review source code documentation

---

**Version**: 1.0  
**Last Updated**: February 2026  
**Maintained By**: AI-RRM Report Generator Project
