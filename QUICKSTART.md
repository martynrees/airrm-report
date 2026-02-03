# Quick Start Guide

## First Time Setup

1. **Navigate to the project directory:**
   ```bash
   cd "/Users/marrees/Documents/AI-RRM Report/airrm-report"
   ```

2. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```

3. **Copy and configure environment file:**
   ```bash
   cp .env.example .env
   ```

4. **Edit .env with your DNA Center credentials:**
   ```bash
   # Open in your favorite editor
   nano .env
   # or
   vim .env
   # or
   open -e .env
   ```
   
   Update these values:
   ```
   DNA_CENTER_URL=https://172.31.96.6
   DNA_CENTER_USERNAME=admin
   DNA_CENTER_PASSWORD=your_actual_password
   ```

## Running the Report

### Basic Usage
```bash
python airrm_report.py
```

This will:
- Connect to your DNA Center
- Discover all AI-RRM enabled buildings
- Collect metrics for 2.4, 5, and 6 GHz bands
- Generate a PDF report in the `output/` folder

### Custom Output Location
```bash
python airrm_report.py -o /path/to/my_report.pdf
```

### With Debug Logging
```bash
python airrm_report.py --log-level DEBUG
```

### For Self-Signed Certificates
```bash
python airrm_report.py --no-verify-ssl
```

## What the Report Contains

1. **Executive Summary**
   - Total buildings monitored
   - How many have issues
   - Total APs and clients
   - Average health score

2. **Buildings Requiring Attention** (RED section)
   - Buildings with health score < 70
   - Buildings with active insights
   - High RRM change counts

3. **Complete Building List**
   - All buildings with all metrics
   - Organized by building and frequency

4. **Detailed Insights**
   - Full descriptions of AI-generated recommendations
   - Reasons for each insight

## Understanding the Metrics

| Metric | Description | Good Range |
|--------|-------------|------------|
| Health Score | Overall RRM performance | 80-100 |
| RRM Changes | Number of optimizations | Lower is stable |
| Insights | AI recommendations | 0 = No issues |
| AP Count | Access points in building | - |
| Client Count | Connected clients | - |

## Troubleshooting

### "Authentication failed"
- Check username/password in .env
- Verify DNA Center URL is correct
- Ensure user has API access permissions

### "No buildings found"
- Verify buildings have AI-RRM profiles assigned
- Check user has permission to view AI-RRM

### "SSL Certificate Error"
- Add `--no-verify-ssl` to command
- Or set `VERIFY_SSL=false` in .env

### View detailed logs
```bash
python airrm_report.py --log-level DEBUG
cat airrm_report.log
```

## Automation Example

Run every Monday at 8 AM (add to crontab):
```bash
0 8 * * 1 cd "/Users/marrees/Documents/AI-RRM Report/airrm-report" && ./venv/bin/python airrm_report.py
```

## Need Help?

Check the full README.md for more details:
```bash
cat README.md
```
