# AI-RRM Report Generator

Automated tool to collect AI-RRM (AI Radio Resource Management) metrics from Cisco DNA Center and generate comprehensive PDF reports.

## Features

- 🔐 Automatic authentication with DNA Center
- 🏢 Discovers all buildings with AI-RRM enabled
- 📊 Collects metrics across 2.4, 5, and 6 GHz frequency bands
- 📈 Tracks AP count, client count, RRM performance scores, and changes
- 💡 Captures and reports AI-generated insights
- 🚨 Highlights buildings requiring attention
- 📄 Generates professional PDF reports

## Metrics Collected

For each building and frequency band:
- **AP Count** - Number of access points
- **Client Count** - Number of connected clients
- **RRM Health Score** - Performance score (0-100)
- **RRM Changes** - Number of RRM optimization changes
- **Insights** - AI-generated recommendations and observations

## Requirements

- Python 3.7+
- Access to Cisco DNA Center with AI-RRM enabled
- Network connectivity to DNA Center

## Installation

1. Clone or download this repository

2. Create a virtual environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your DNA Center credentials
```

## Configuration

Edit the `.env` file with your DNA Center details:

```bash
DNA_CENTER_URL=https://your-dnac-server.com
DNA_CENTER_USERNAME=admin
DNA_CENTER_PASSWORD=your_password

# Report Configuration
FREQUENCY_BANDS=2.4,5,6  # Comma-separated bands to include in report
                         # Options: 2.4, 5, 6
                         # Examples:
                         #   2.4,5,6  - All bands (default)
                         #   5,6      - 5 GHz and 6 GHz only
                         #   5        - 5 GHz only

# Optional
VERIFY_SSL=false  # Set to true if using valid SSL certificates
LOG_LEVEL=INFO    # DEBUG, INFO, WARNING, ERROR

# Cisco Branding (Optional)
LOGO_PATH=/path/to/cisco_logo.png  # Path to Cisco logo for PDF branding
```

### Frequency Band Configuration

The `FREQUENCY_BANDS` setting allows you to control which frequency bands are included in the report:

- **All bands (default):** `FREQUENCY_BANDS=2.4,5,6`
- **5 GHz and 6 GHz only:** `FREQUENCY_BANDS=5,6` (useful when 2.4 GHz is not deployed)
- **5 GHz only:** `FREQUENCY_BANDS=5` (common in modern deployments)
- **6 GHz only:** `FREQUENCY_BANDS=6` (for Wi-Fi 6E exclusive environments)

This is particularly useful when:
- Your deployment doesn't use certain bands
- Your regulatory domain doesn't permit 6 GHz
- You want focused reports on specific bands
- You need to reduce report size and processing time


## Cisco Branding

The AI-RRM Report Generator includes full Cisco branding support to create professional, branded PDF reports.

### Branding Features

- ✓ **Cisco Color Palette** - Official Cisco brand colors throughout
- ✓ **Cisco Logo** - Optional logo on title page
- ✓ **Branded Headers/Footers** - Cisco-branded page elements
- ✓ **Professional Typography** - Helvetica font family per Cisco guidelines
- ✓ **Consistent Visual Design** - Tables, charts, and elements follow Cisco design standards

### Adding Cisco Logo

The report can display the official Cisco logo on the title page. You can provide the logo in three ways:

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
```env
LOGO_PATH=/path/to/cisco_logo.png
```

### Logo Requirements

- **Format**: PNG or JPG (PNG recommended for transparency)
- **Resolution**: Minimum 300 DPI for professional quality
- **Size**: Logo will be scaled to approximately 2.5 inches width
- **Aspect Ratio**: Original aspect ratio is preserved

### Obtaining Cisco Logo

To maintain brand integrity, use official Cisco logos:
- **Cisco Employees**: Download from Cisco Brand Center (internal)
- **Cisco Partners**: Request from your Cisco partner representative
- **Public Use**: Use official logos from Cisco's public brand guidelines

**Note**: If no logo is provided, the report displays "Cisco" text branding in Cisco Blue.

### Full Branding Documentation

For complete details about Cisco branding implementation, color palette, typography, and design guidelines, see [BRANDING.md](BRANDING.md).


## Usage

### Basic Usage

Generate a report with default settings:
```bash
python airrm_report.py
```

This will create a PDF report in the `output/` directory with a timestamp.

### Command Line Options

```bash
python airrm_report.py [OPTIONS]

Options:
  -o, --output PATH       Output PDF file path
                          (default: output/airrm_report_YYYYMMDD_HHMMSS.pdf)
  
  --logo PATH             Path to Cisco logo image file (PNG/JPG recommended)
                          Overrides LOGO_PATH environment variable
  
  --log-level LEVEL       Set logging level: DEBUG, INFO, WARNING, ERROR
                          (default: INFO)
  
  --no-verify-ssl         Disable SSL certificate verification
                          (useful for self-signed certificates)
  
  -h, --help              Show help message
```

### Examples

Generate report with Cisco logo:
```bash
python airrm_report.py --logo assets/cisco_logo.png
```

Generate report with custom output path:
```bash
python airrm_report.py -o reports/monthly_report.pdf
```

Generate report with logo and custom path:
```bash
python airrm_report.py --logo assets/cisco_logo.png -o reports/branded_report.pdf
```

Enable debug logging:
```bash
python airrm_report.py --log-level DEBUG
```

Disable SSL verification (for self-signed certificates):
```bash
python airrm_report.py --no-verify-ssl
```

## Report Sections

The generated PDF report includes:

1. **Executive Summary** - High-level statistics
   - Total buildings monitored
   - Buildings requiring attention
   - Total APs and clients
   - Average health score

2. **Buildings Requiring Attention** - Highlighted issues
   - Buildings with low health scores (< 70)
   - Buildings with active insights
   - Buildings with high RRM change counts

3. **All Buildings - Detailed Metrics** - Comprehensive table
   - All metrics for all buildings and frequencies

4. **Detailed Insights** - AI-generated recommendations
   - Full insight descriptions and reasons

## Troubleshooting

### Authentication Fails
- Verify DNA_CENTER_URL, USERNAME, and PASSWORD in .env
- Check network connectivity to DNA Center
- Ensure user has appropriate permissions

### SSL Certificate Errors
- Use `--no-verify-ssl` flag for self-signed certificates
- Or set `VERIFY_SSL=false` in .env file

### No Buildings Found
- Verify buildings have AI-RRM profiles assigned
- Check user has access to view AI-RRM configuration

### Missing Metrics
- Some buildings may not have data for all frequency bands
- Check DNA Center logs for data collection issues

## Logging

Logs are written to:
- Console (stdout)
- `airrm_report.log` file in the current directory

Adjust log level with `--log-level` option for more or less detail.

## Automation

### Scheduled Reports (Linux/macOS)

Add to crontab for weekly reports:
```bash
# Every Monday at 8 AM
0 8 * * 1 cd /path/to/airrm-report && ./venv/bin/python airrm_report.py
```

### Scheduled Reports (Windows)

Use Windows Task Scheduler to run:
```bash
C:\path\to\airrm-report\venv\Scripts\python.exe airrm_report.py
```

## Project Structure

```
airrm-report/
├── airrm_report.py       # Main script
├── src/
│   ├── auth.py           # Authentication module
│   ├── api_client.py     # DNA Center API client
│   ├── data_collector.py # Metrics collection
│   └── pdf_generator.py  # PDF report generation
├── output/               # Generated reports
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variable template
├── BRANDING.md          # Cisco branding documentation
└── README.md            # This file
```

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review logs with `--log-level DEBUG`
3. Verify DNA Center API access and permissions

## License

Internal use only - Cisco DNA Center integration tool
