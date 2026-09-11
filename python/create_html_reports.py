#!/usr/bin/env python3
import json
from datetime import datetime
import sys
import os

from ai_analysis import get_ai_analysis

# Get JSON file from command line argument or use default
if len(sys.argv) > 1:
    json_file = sys.argv[1]
else:
    json_file = 'venue_data.json'

# Check if file exists
if not os.path.exists(json_file):
    print(f"Error: File not found: {json_file}")
    print(f"\nUsage: python create_html_reports.py <path_to_json_file>")
    print(f"\nExamples:")
    print(f"  python create_html_reports.py venue_data.json")
    print(f"\nNote: First run 'python generate_reports.py <csv_file>' to create venue_data.json")
    sys.exit(1)

print(f"Reading data from: {json_file}")

# Load the venue data
with open(json_file, 'r') as f:
    venue_data = json.load(f)

# Network benchmarks
benchmarks = {
    'ltr': 7.8,
    'fun': 4.1,
    'helpful': 4.2,
    'issues': 37.0,
    'resolution': 3.6
}

def get_status(metric, value, benchmark, is_issues=False):
    """Determine status compared to benchmark"""
    if is_issues:
        # For issues, lower is better
        if value < benchmark - 0.1:
            return "Above average ✓"
        elif value <= benchmark + 0.1:
            return "On par"
        else:
            return "Below average"
    else:
        # For other metrics, higher is better
        if value > benchmark + 0.1:
            return "Above average ✓"
        elif value >= benchmark - 0.1:
            return "On par"
        else:
            return "Below average"

def get_status_class(metric, value, benchmark, is_issues=False):
    """Determine CSS class for status pill"""
    if is_issues:
        # For issues, lower is better
        if value < benchmark - 0.1:
            return "good"
        elif value <= benchmark + 0.1:
            return "moderate"
        else:
            return "poor"
    else:
        # For other metrics, higher is better
        if value > benchmark + 0.1:
            return "good"
        elif value >= benchmark - 0.1:
            return "moderate"
        else:
            return "poor"

def get_assessment(metric, value):
    """Get assessment level for a metric"""
    if metric == 'ltr':
        if value >= 8.0:
            return "Excellent"
        elif value >= 7.0:
            return "Strong"
        elif value >= 6.0:
            return "Moderate"
        else:
            return "Weak"
    elif metric in ['fun', 'helpful']:
        if value >= 4.2:
            return "Excellent"
        elif value >= 3.8:
            return "Strong"
        elif value >= 3.4:
            return "Moderate"
        else:
            return "Weak"
    elif metric == 'issues':
        if value < 30:
            return "Low"
        elif value < 40:
            return "Moderate"
        elif value < 50:
            return "High"
        else:
            return "Critical"
    elif metric == 'resolution':
        if value >= 4.0:
            return "Excellent"
        elif value >= 3.5:
            return "Strong"
        elif value >= 3.0:
            return "Moderate"
        else:
            return "Weak"

def analyze_comments(data):
    """Analyze comments to identify themes and specific issues"""
    themes = {
        'equipment': [],
        'parking': [],
        'food': [],
        'staff': [],
        'games': [],
        'sonic': []
    }
    
    keywords = {
        'equipment': ['equipment', 'screen', 'tracking', 'game', 'bay', 'issue', 'problem', 'broken', 'malfunction'],
        'parking': ['parking', 'park', 'lot', 'space'],
        'food': ['food', 'order', 'eat', 'drink', 'restaurant', 'service'],
        'staff': ['staff', 'host', 'server', 'team', 'help', 'helpful', 'friendly', 'knowledge'],
        'games': ['game', 'fun', 'enjoy', 'play'],
        'sonic': ['sonic', 'new game']
    }
    
    for comment in data.get('comments', []):
        text = comment['text'].lower()
        for theme, keywords_list in keywords.items():
            if any(keyword in text for keyword in keywords_list):
                themes[theme].append(comment)
    
    return themes

def generate_overview(data):
    """Generate venue overview narrative"""
    ltr = data['ltr_avg']
    themes = analyze_comments(data)
    
    # Characterization
    if ltr >= 8.0:
        char = "high-performing"
    elif ltr >= 7.0:
        char = "strong"
    elif ltr >= 6.0:
        char = "moderate"
    else:
        char = "challenged"
    
    # Identify primary strength and challenge
    if data['fun_avg'] >= 4.0:
        strength = "delivers strong entertainment value"
    else:
        strength = "has moderate entertainment appeal"
    
    # Detect specific challenges from comments
    if themes['parking']:
        challenge = "faces parking accessibility challenges"
    elif data['issues_pct'] > 50:
        challenge = "faces critical equipment reliability issues"
    elif data['issues_pct'] > 40:
        challenge = "faces significant equipment challenges"
    elif data['issues_pct'] > 30:
        challenge = "experiences occasional operational issues"
    else:
        challenge = "maintains good operational reliability"
    
    overview = f"{data['venue']} is a {char} venue that {strength} but {challenge}. "
    
    # Add key insight
    if themes['parking']:
        overview += f"Guest feedback indicates parking accessibility is a significant concern affecting the overall visit experience. "
    elif data['issues_pct'] > 50:
        overview += f"The venue shows a clear pattern: equipment issues occur in {data['issues_pct']:.0f}% of visits, significantly impacting guest satisfaction. "
    else:
        overview += f"The venue shows strong fundamentals with {data['fun_avg']:.1f}/5 fun ratings and {data['helpful_avg']:.1f}/5 helpfulness scores. "
    
    # Capability assessment
    if data['issues_pct'] > 50 and data['resolution_avg'] < 3.5:
        overview += "The venue appears to have both capability gaps and execution challenges that need attention."
    elif data['issues_pct'] > 50:
        overview += "The venue has demonstrated resolution capability but needs to prevent issues from occurring."
    else:
        overview += "The venue is executing well across key experience dimensions."
    
    return overview

def generate_ups(data):
    """Generate positive drivers"""
    ups = []
    themes = analyze_comments(data)
    
    # Check for Sonic game mentions
    if themes['sonic']:
        sonic_count = len(themes['sonic'])
        ups.append(f"<strong>New Sonic game excitement:</strong> Guests are enthusiastic about the newly released Sonic game, with {sonic_count} positive mentions highlighting it as a major draw")
    
    if data['fun_avg'] >= 4.0:
        ups.append(f"<strong>Strong entertainment value:</strong> Guests consistently rate the games and experience as fun (average {data['fun_avg']:.1f}/5), indicating the core offering is working well")
    
    if data['helpful_avg'] >= 4.0:
        ups.append(f"<strong>Staff helpfulness:</strong> Team members are rated as helpful ({data['helpful_avg']:.1f}/5), with guests noting staff knowledge and willingness to assist")
    
    if data['resolution_avg'] >= 3.5:
        ups.append(f"<strong>Quick issue resolution:</strong> When problems occur, staff resolve them effectively (average {data['resolution_avg']:.1f}/5 satisfaction)")
    
    if not ups:
        ups.append(f"<strong>Positive guest sentiment:</strong> Despite challenges, guests appreciate the venue's entertainment value and staff friendliness")
    
    return ups[:3]

def generate_downs(data):
    """Generate negative drivers"""
    downs = []
    themes = analyze_comments(data)
    
    # Check for parking mentions
    if themes['parking']:
        parking_count = len(themes['parking'])
        downs.append(f"<strong>Parking accessibility issues:</strong> {parking_count} guests mentioned parking challenges, citing difficulty finding spots and long walks that detracted from their experience")
    
    if data['issues_pct'] > 50:
        downs.append(f"<strong>High equipment issue frequency:</strong> {data['issues_pct']:.0f}% of guests reported issues—significantly above the network average of 37%—indicating systemic problems")
    elif data['issues_pct'] > 30:
        downs.append(f"<strong>Equipment reliability concerns:</strong> {data['issues_pct']:.0f}% of guests experienced issues, slightly above network average")
    
    if data['helpful_avg'] < 4.0:
        downs.append(f"<strong>Helpfulness below expectations:</strong> Helpfulness rating of {data['helpful_avg']:.1f}/5 is below network average, likely reflecting guest frustration with issues")
    
    if data['ltr_avg'] < 7.0:
        downs.append(f"<strong>Lower recommendation intent:</strong> LTR of {data['ltr_avg']:.1f}/10 is below network average, indicating guests are less likely to recommend")
    
    return downs[:3]

def generate_impact(data):
    """Generate top 3 impact drivers"""
    drivers = []
    themes = analyze_comments(data)
    
    # Parking impact (if mentioned)
    if themes['parking']:
        drivers.append(("Parking Accessibility", f"{len(themes['parking'])} guests reported parking challenges that significantly impacted their overall experience"))
    
    # Equipment reliability impact
    if data['issues_pct'] > 30:
        drivers.append(("Equipment Reliability", f"{data['issues_pct']:.0f}% of guests experienced issues; this is the primary detractor from satisfaction"))
    
    # Sonic game impact (if mentioned)
    if themes['sonic']:
        drivers.append(("New Sonic Game Launch", f"{len(themes['sonic'])} guests highlighted the new Sonic game as a major positive, driving excitement and repeat visit intent"))
    
    # Resolution quality impact
    if data['resolution_avg'] < 4.0:
        drivers.append(("Issue Resolution Quality", f"Average resolution satisfaction of {data['resolution_avg']:.1f}/5 shows inconsistent outcomes when problems occur"))
    
    # Entertainment value impact
    if data['fun_avg'] >= 4.0:
        drivers.append(("Entertainment Value", f"Consistent {data['fun_avg']:.1f}/5 fun ratings show guests enjoy the core experience"))
    
    # If we need more drivers
    if len(drivers) < 3:
        if data['helpful_avg'] >= 3.8:
            drivers.append(("Staff Knowledge", f"Helpful ratings of {data['helpful_avg']:.1f}/5 indicate staff are knowledgeable and engaged"))
        else:
            drivers.append(("Staff Responsiveness", f"Helpfulness rating of {data['helpful_avg']:.1f}/5 suggests need for faster response times"))
    
    return drivers[:3]

def generate_recommendations_html(data):
    """Generate dynamic recommendations based on detected issues"""
    themes = analyze_comments(data)
    html_sections = []
    
    # Determine critical priority
    if themes['parking']:
        critical_title = "Parking Accessibility"
        critical_items = [
            "<li><strong>Parking lot assessment:</strong> Conduct a comprehensive review of parking capacity and layout</li>",
            "<li><strong>Signage improvement:</strong> Add clear directional signage to guide guests to available parking</li>",
            "<li><strong>Valet service consideration:</strong> Evaluate feasibility of valet parking during peak hours</li>",
            "<li><strong>Guest communication:</strong> Provide parking information upfront when guests book or arrive</li>"
        ]
    elif data['issues_pct'] > 30:
        critical_title = "Equipment Reliability"
        critical_items = [
            f"<li><strong>Root cause analysis:</strong> Investigate why equipment issues occur in {data['issues_pct']:.0f}% of visits</li>",
            "<li><strong>Preventive maintenance audit:</strong> Review maintenance logs and assess current preventive maintenance schedule</li>",
            "<li><strong>Response time standardization:</strong> Establish and enforce response time standards for guest issues</li>",
            "<li><strong>Staff training:</strong> Ensure staff are trained on rapid issue detection and resolution procedures</li>"
        ]
    else:
        critical_title = "Guest Experience Consistency"
        critical_items = [
            "<li><strong>Service consistency:</strong> Ensure consistent service delivery across all shifts and staff members</li>",
            "<li><strong>Guest communication:</strong> Improve communication when issues occur to manage expectations</li>",
            "<li><strong>Staff empowerment:</strong> Give staff authority to resolve issues quickly without escalation</li>",
            "<li><strong>Monitoring system:</strong> Implement real-time monitoring of equipment and guest satisfaction</li>"
        ]
    
    # Secondary priority
    if data['helpful_avg'] < 4.0:
        secondary_title = "Staff Responsiveness"
    else:
        secondary_title = "Operational Consistency"
    
    secondary_items = [
        "<li><strong>Service consistency:</strong> Ensure consistent service delivery across all shifts and staff members</li>",
        "<li><strong>Guest communication:</strong> Improve communication when issues occur to manage expectations</li>",
        "<li><strong>Staff empowerment:</strong> Give staff authority to resolve issues quickly without escalation</li>",
        "<li><strong>Monitoring system:</strong> Implement real-time monitoring of equipment and guest satisfaction</li>"
    ]
    
    # Maintain strengths
    if themes['sonic']:
        maintain_title = "Sonic Game Momentum"
        maintain_items = [
            "<li><strong>Marketing campaign:</strong> Leverage the Sonic game excitement in marketing and social media</li>",
            "<li><strong>Staff training:</strong> Ensure all staff can provide expert guidance on the new Sonic game</li>",
            "<li><strong>Promotional events:</strong> Consider special events or tournaments around the Sonic game</li>",
            "<li><strong>Guest feedback loop:</strong> Continue gathering feedback to identify and address issues early</li>"
        ]
    elif data['fun_avg'] >= 4.0:
        maintain_title = "Entertainment Value"
        maintain_items = [
            "<li><strong>Protect core experience:</strong> Ensure equipment issues don't undermine the strong entertainment value</li>",
            "<li><strong>Staff recognition:</strong> Recognize and reward staff who deliver excellent service and quick resolutions</li>",
            "<li><strong>Consistency assurance:</strong> Maintain the positive service culture across all team members</li>",
            "<li><strong>Guest feedback loop:</strong> Continue gathering feedback to identify and address issues early</li>"
        ]
    else:
        maintain_title = "Staff Knowledge"
        maintain_items = [
            "<li><strong>Staff development:</strong> Invest in training to improve staff knowledge and engagement</li>",
            "<li><strong>Recognition program:</strong> Recognize staff who go above and beyond for guests</li>",
            "<li><strong>Culture building:</strong> Foster a positive service culture across all team members</li>",
            "<li><strong>Feedback integration:</strong> Use guest feedback to continuously improve service delivery</li>"
        ]
    
    return critical_title, critical_items, secondary_title, secondary_items, maintain_title, maintain_items

def get_analysis(data):
    """Get the overview/ups/downs/impact/recommendations content for a venue.

    Tries the AI-based analysis (via Claude Code CLI) first, since it actually
    reads the guest comments instead of just the aggregate metrics. Falls back
    to the keyword-based heuristics if the AI analysis isn't available.
    """
    ai_result = get_ai_analysis(data)
    if ai_result is not None:
        print(f"[analysis] Using AI-generated analysis for {data['venue']}")
        rec = ai_result['recommendations']
        impact = [(driver['title'], driver['description']) for driver in ai_result['impact']]

        def as_list_items(items):
            return [f"<li>{item}</li>" for item in items]

        return (
            ai_result['overview'],
            ai_result['ups'],
            ai_result['downs'],
            impact,
            rec['critical']['title'], as_list_items(rec['critical']['items']),
            rec['secondary']['title'], as_list_items(rec['secondary']['items']),
            rec['maintain']['title'], as_list_items(rec['maintain']['items']),
        )

    print(f"[analysis] Using keyword-based fallback analysis for {data['venue']}")
    overview = generate_overview(data)
    ups = generate_ups(data)
    downs = generate_downs(data)
    impact = generate_impact(data)
    critical_title, critical_items, secondary_title, secondary_items, maintain_title, maintain_items = generate_recommendations_html(data)
    return (
        overview, ups, downs, impact,
        critical_title, critical_items,
        secondary_title, secondary_items,
        maintain_title, maintain_items,
    )


def generate_html_report(venue_key, data):
    """Generate complete HTML report"""
    
    # Calculate dates
    start_date = data['date_range'][0]
    end_date = data['date_range'][1]
    start_obj = datetime.strptime(start_date, '%Y-%m-%d')
    end_obj = datetime.strptime(end_date, '%Y-%m-%d')
    
    start_formatted = start_obj.strftime('%B %d, %Y')
    end_formatted = end_obj.strftime('%B %d, %Y')
    week_formatted = start_obj.strftime('%B %d, %Y')
    
    # Generate content (AI-based analysis of guest comments, with keyword-based fallback)
    (overview, ups, downs, impact,
     critical_title, critical_items,
     secondary_title, secondary_items,
     maintain_title, maintain_items) = get_analysis(data)
    
    # Get assessments and statuses
    ltr_assessment = get_assessment('ltr', data['ltr_avg'])
    fun_assessment = get_assessment('fun', data['fun_avg'])
    helpful_assessment = get_assessment('helpful', data['helpful_avg'])
    issues_assessment = get_assessment('issues', data['issues_pct'])
    
    ltr_status = get_status('ltr', data['ltr_avg'], benchmarks['ltr'])
    fun_status = get_status('fun', data['fun_avg'], benchmarks['fun'])
    helpful_status = get_status('helpful', data['helpful_avg'], benchmarks['helpful'])
    issues_status = get_status('issues', data['issues_pct'], benchmarks['issues'], is_issues=True)
    resolution_status = get_status('resolution', data['resolution_avg'], benchmarks['resolution'])
    
    # Get status classes for pills
    ltr_status_class = get_status_class('ltr', data['ltr_avg'], benchmarks['ltr'])
    fun_status_class = get_status_class('fun', data['fun_avg'], benchmarks['fun'])
    helpful_status_class = get_status_class('helpful', data['helpful_avg'], benchmarks['helpful'])
    issues_status_class = get_status_class('issues', data['issues_pct'], benchmarks['issues'], is_issues=True)
    resolution_status_class = get_status_class('resolution', data['resolution_avg'], benchmarks['resolution'])
    
    # Build HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Topgolf Venue Report - 1 Page</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        :root {{
            --primary-dark: #050786;
            --primary-light: #2DFFFF;
            --primary-light-soft: rgba(45, 255, 255, 0.15);
            --accent-yellow: #FFFF00;
            --accent-yellow-soft: rgba(255, 255, 0, 0.12);
            --dark-bg: #0D1117;
            --white: #FFFFFF;
            --text-dark: #1a1a1a;
            --border-light: #e0e0e0;
            --border-accent: rgba(45, 255, 255, 0.3);
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, var(--dark-bg) 0%, #1a1a2e 100%);
            color: var(--text-dark);
            line-height: 1.6;
        }}

        .container {{
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
        }}

        /* Header */
        .header {{
            background: linear-gradient(135deg, var(--primary-dark) 0%, #1a0f8f 100%);
            color: var(--white);
            padding: 40px 30px;
            border-radius: 12px 12px 0 0;
            margin-bottom: 0;
            position: relative;
            overflow: hidden;
        }}

        .header::before {{
            content: '';
            position: absolute;
            top: -50%;
            right: -10%;
            width: 400px;
            height: 400px;
            background: radial-gradient(circle, var(--primary-light-soft) 0%, transparent 70%);
            opacity: 0.3;
            border-radius: 50%;
        }}

        .header-content {{
            position: relative;
            z-index: 1;
        }}

        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
            letter-spacing: -0.5px;
        }}

        .header-meta {{
            display: flex;
            gap: 30px;
            font-size: 0.95em;
            opacity: 0.95;
            flex-wrap: wrap;
        }}

        .header-meta span {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        /* Main Content */
        .main {{
            background: var(--white);
            padding: 40px;
            border-radius: 0 0 12px 12px;
            margin-bottom: 30px;
        }}

        /* Sections */
        .section {{
            margin-bottom: 40px;
        }}

        .section:last-child {{
            margin-bottom: 0;
        }}

        .section-title {{
            font-size: 1.8em;
            color: var(--primary-dark);
            margin-bottom: 20px;
            padding-bottom: 12px;
            border-bottom: 3px solid rgba(255, 255, 0, 0.4);
            font-weight: 700;
        }}

        .section-subtitle {{
            font-size: 1.2em;
            color: var(--primary-dark);
            margin-top: 25px;
            margin-bottom: 15px;
            font-weight: 600;
        }}

        /* Overview Box */
        .overview-box {{
            background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 100%);
            border-left: 5px solid var(--border-accent);
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            line-height: 1.8;
        }}

        /* Metrics Grid */
        .metrics-grid {{
            display: flex;
            flex-direction: row;
            flex-wrap: wrap;
            justify-content: space-between;
            margin-bottom: 10px;
        }}

        .metric-card {{
            background: linear-gradient(135deg, var(--white) 0%, #f9f9f9 100%);
            border: 2px solid var(--border-light);
            border-radius: 8px;
            padding: 15px;
            margin-right: 10px;
            width: 20%;
            transition: all 0.3s ease;
            cursor: pointer;
        }}

        .metric-card:hover {{
            border-color: var(--border-accent);
            box-shadow: 0 8px 24px rgba(45, 255, 255, 0.1);
            transform: translateY(-4px);
        }}

        .metric-label {{
            font-size: 0.9em;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
            font-weight: 600;
        }}

        .metric-value {{
            font-size: 2.2em;
            font-weight: 700;
            color: var(--primary-dark);
            margin-bottom: 8px;
        }}

        .metric-status {{
            font-size: 0.85em;
            padding: 6px 12px;
            border-radius: 20px;
            display: inline-block;
            font-weight: 600;
        }}

        .status-good {{
            background: #e8f5e9;
            color: #2e7d32;
        }}

        .status-moderate {{
            background: #fff3e0;
            color: #e65100;
        }}

        .status-poor {{
            background: #ffebee;
            color: #c62828;
        }}

        /* Table */
        .table-wrapper {{
            overflow: hidden;
            margin-bottom: 25px;
            border-radius: 12px;
            border: 2px solid var(--border-light);
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }}

        th {{
            background: var(--primary-dark);
            color: var(--white);
            padding: 15px;
            text-align: left;
            font-weight: 600;
            font-size: 0.95em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        td {{
            padding: 15px;
            border-bottom: 1px solid var(--border-light);
        }}

        tr:hover {{
            background: #f5f5f5;
        }}

        tr:last-child td {{
            border-bottom: none;
        }}

        /* Status Pills in Tables */
        .status-pill {{
            font-size: 0.85em;
            padding: 6px 12px;
            border-radius: 20px;
            display: inline-block;
            font-weight: 600;
        }}

        .status-pill.good {{
            background: #e8f5e9;
            color: #2e7d32;
        }}

        .status-pill.moderate {{
            background: #fff3e0;
            color: #e65100;
        }}

        .status-pill.poor {{
            background: #ffebee;
            color: #c62828;
        }}

        /* Lists */
        .list-section {{
            margin-bottom: 20px;
        }}

        .list-section ul {{
            list-style: none;
            padding-left: 0;
        }}

        .list-section li {{
            padding: 12px 0;
            padding-left: 30px;
            position: relative;
            border-bottom: 1px solid var(--border-light);
        }}

        .list-section li:last-child {{
            border-bottom: none;
        }}

        .list-section li::before {{
            content: '→';
            position: absolute;
            left: 0;
            color: rgba(45, 255, 255, 0.5);
            font-weight: bold;
            font-size: 1.2em;
        }}

        /* Highlight Box */
        .highlight-box {{
            background: linear-gradient(135deg, rgba(255, 255, 0, 0.15) 0%, rgba(255, 235, 59, 0.12) 100%);
            color: var(--primary-dark);
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            font-weight: 600;
            box-shadow: 0 4px 12px rgba(255, 255, 0, 0.08);
            border: 1px solid rgba(255, 255, 0, 0.2);
        }}

        /* Ranking */
        .ranking-list {{
            list-style: none;
            padding: 0;
        }}

        .ranking-list li {{
            display: flex;
            align-items: flex-start;
            gap: 15px;
            padding: 15px;
            background: #f9f9f9;
            border-radius: 8px;
            margin-bottom: 12px;
            border-left: 4px solid var(--border-accent);
        }}

        .ranking-number {{
            background: var(--primary-dark);
            color: var(--white);
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 1.1em;
            flex-shrink: 0;
        }}

        .ranking-content {{
            flex: 1;
        }}

        .ranking-title {{
            font-weight: 600;
            color: var(--primary-dark);
            margin-bottom: 4px;
        }}

        .ranking-description {{
            font-size: 0.9em;
            color: #666;
        }}

        /* Cards Layout */
        .cards-container {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 25px;
            margin-bottom: 30px;
        }}

        .card {{
            background: linear-gradient(135deg, #f9f9f9 0%, #f5f5f5 100%);
            border: 2px solid var(--border-light);
            border-radius: 12px;
            padding: 25px;
            transition: all 0.3s ease;
        }}

        .card:hover {{
            border-color: var(--border-accent);
            box-shadow: 0 8px 24px rgba(45, 255, 255, 0.1);
            transform: translateY(-4px);
        }}

        .card-title {{
            font-size: 1.4em;
            font-weight: 700;
            margin-bottom: 20px;
            padding-bottom: 12px;
            border-bottom: 3px solid rgba(255, 255, 0, 0.4);
            color: var(--primary-dark);
        }}

        .card.ups .card-title {{
            color: #2e7d32;
            border-bottom-color: rgba(46, 125, 50, 0.3);
        }}

        .card.downs .card-title {{
            color: #c62828;
            border-bottom-color: rgba(198, 40, 40, 0.3);
        }}

        .card-list {{
            list-style: none;
            padding: 0;
        }}

        .card-list li {{
            padding: 12px 0;
            padding-left: 25px;
            position: relative;
            border-bottom: 1px solid rgba(0, 0, 0, 0.08);
        }}

        .card-list li:last-child {{
            border-bottom: none;
        }}

        .card-list li::before {{
            content: '→';
            position: absolute;
            left: 0;
            font-weight: bold;
            font-size: 1.2em;
        }}

        .card.ups .card-list li::before {{
            color: #2e7d32;
        }}

        .card.downs .card-list li::before {{
            color: #c62828;
        }}

        /* Footer */
        .footer {{
            background: var(--primary-dark);
            color: var(--white);
            padding: 30px;
            border-radius: 12px;
            text-align: center;
            font-size: 0.9em;
            margin-top: 30px;
        }}

        .footer-logo {{
            font-size: 1.2em;
            font-weight: 700;
            margin-bottom: 10px;
            letter-spacing: 1px;
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            .container {{
                padding: 10px;
            }}

            .header {{
                padding: 30px 20px;
            }}

            .header h1 {{
                font-size: 1.8em;
            }}

            .main {{
                padding: 20px;
            }}

            .metrics-grid {{
                grid-template-columns: 1fr;
            }}

            .header-meta {{
                flex-direction: column;
                gap: 10px;
            }}

            .section-title {{
                font-size: 1.4em;
            }}

            .cards-container {{
                grid-template-columns: 1fr;
                gap: 20px;
            }}
        }}

        /* Print Styles */
        @media print {{
            body {{
                background: white;
            }}

            .container {{
                max-width: 100%;
            }}

            .header {{
                page-break-after: avoid;
            }}

            .section {{
                page-break-inside: avoid;
            }}

            .metric-card:hover {{
                border-color: var(--border-light);
                box-shadow: none;
                transform: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <div class="header-content">
                <h1>Topgolf Venue Report</h1>
                <div class="header-meta">
                    <span>📍 <strong>Venue:</strong> {data['venue']}</span>
                    <span>📅 <strong>Period:</strong> {start_formatted} - {end_formatted}</span>
                    <span>📊 <strong>Week:</strong> Week of {week_formatted}</span>
                </div>
            </div>
        </div>

        <!-- Main Content -->
        <div class="main">
            <!-- Venue Overview -->
            <div class="section">
                <h2 class="section-title">Venue Overview</h2>
                <div class="overview-box">
                    <p>{overview}</p>
                </div>
            </div>

            <!-- Performance Summary -->
            <div class="section">
                <h2 class="section-title">Performance Summary</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-label">LTR</div>
                        <div class="metric-value">{data['ltr_avg']:.1f}</div>
                        <span class="metric-status status-good">{ltr_assessment}</span>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Fun</div>
                        <div class="metric-value">{data['fun_avg']:.1f}</div>
                        <span class="metric-status status-good">{fun_assessment}</span>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Helpfulness</div>
                        <div class="metric-value">{data['helpful_avg']:.1f}</div>
                        <span class="metric-status status-moderate">{helpful_assessment}</span>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Issues Reported</div>
                        <div class="metric-value">{data['issues_pct']:.0f}%</div>
                        <span class="metric-status status-poor">{issues_assessment}</span>
                    </div>
                </div>

                <div class="highlight-box">
                    ✓ Overall Assessment: {data['venue']} demonstrates {'strong' if data['ltr_avg'] >= 7.0 else 'moderate'} performance with {'excellent' if data['fun_avg'] >= 4.0 else 'good'} entertainment value. {'Equipment reliability is a key concern affecting guest satisfaction.' if data['issues_pct'] > 50 else 'The venue maintains good operational consistency.'}
                </div>
            </div>

            <!-- Experience Metrics -->
            <div class="section">
                <h2 class="section-title">Experience Metrics - Current Period</h2>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Attribute</th>
                                <th style="text-align: right;">Score</th>
                                <th>Benchmark</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Likelihood to Recommend</td>
                                <td style="text-align: right;"><strong>{data['ltr_avg']:.1f} / 10</strong></td>
                                <td>7.8 (network avg)</td>
                                <td><span class="status-pill {ltr_status_class}">{ltr_status}</span></td>
                            </tr>
                            <tr>
                                <td>Fun</td>
                                <td style="text-align: right;"><strong>{data['fun_avg']:.1f} / 5</strong></td>
                                <td>4.1 (network avg)</td>
                                <td><span class="status-pill {fun_status_class}">{fun_status}</span></td>
                            </tr>
                            <tr>
                                <td>Helpfulness</td>
                                <td style="text-align: right;"><strong>{data['helpful_avg']:.1f} / 5</strong></td>
                                <td>4.2 (network avg)</td>
                                <td><span class="status-pill {helpful_status_class}">{helpful_status}</span></td>
                            </tr>
                            <tr>
                                <td>Issues Reported</td>
                                <td style="text-align: right;"><strong>{data['issues_pct']:.1f}%</strong></td>
                                <td>37.0% (network avg)</td>
                                <td><span class="status-pill {issues_status_class}">{issues_status}</span></td>
                            </tr>
                            <tr>
                                <td>Issue Resolution</td>
                                <td style="text-align: right;"><strong>{data['resolution_avg']:.1f} / 5</strong></td>
                                <td>3.6 (network avg)</td>
                                <td><span class="status-pill {resolution_status_class}">{resolution_status}</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Divider -->
            <hr style="border: none; border-top: 2px solid var(--border-light); margin: 30px 0;">

            <!-- What Made Scores Go Up & Down -->
            <div class="section">
                <div class="cards-container">
                    <!-- Ups Card -->
                    <div class="card ups">
                        <h3 class="card-title">📈 Ups</h3>
                        <ul class="card-list">
                            {''.join(f'<li>{up}</li>' for up in ups)}
                        </ul>
                    </div>

                    <!-- Downs Card -->
                    <div class="card downs">
                        <h3 class="card-title">📉 Downs</h3>
                        <ul class="card-list">
                            {''.join(f'<li>{down}</li>' for down in downs)}
                        </ul>
                    </div>
                </div>
            </div>

            <!-- Divider -->
            <hr style="border: none; border-top: 2px solid var(--border-light); margin: 30px 0;">

            <!-- What Impacted Scores Most -->
            <div class="section">
                <h2 class="section-title">Impact</h2>
                <ul class="ranking-list">
                    {''.join(f'''<li>
                        <div class="ranking-number">{i+1}</div>
                        <div class="ranking-content">
                            <div class="ranking-title">{driver[0]}</div>
                            <div class="ranking-description">{driver[1]}</div>
                        </div>
                    </li>''' for i, driver in enumerate(impact))}
                </ul>
            </div>

            <!-- Divider -->
            <hr style="border: none; border-top: 2px solid var(--border-light); margin: 30px 0;">

            <!-- Recommendations -->
            <div class="section">
                <h2 class="section-title">Recommendations</h2>

                <h3 class="section-subtitle">🔴 Critical Priority: {critical_title}</h3>
                <div class="list-section">
                    <ul>
                        {''.join(critical_items)}
                    </ul>
                </div>

                <h3 class="section-subtitle">🟡 Secondary Priority: {secondary_title}</h3>
                <div class="list-section">
                    <ul>
                        {''.join(secondary_items)}
                    </ul>
                </div>

                <h3 class="section-subtitle">🟢 Maintain Strengths: {maintain_title}</h3>
                <div class="list-section">
                    <ul>
                        {''.join(maintain_items)}
                    </ul>
                </div>
            </div>
        </div>

        <!-- Footer -->
        <div class="footer">
            <div class="footer-logo">TOPGOLF®</div>
            <p>Venue Performance Report | Confidential</p>
            <p style="margin-top: 10px; opacity: 0.8; font-size: 0.85em;">Generated on {datetime.now().strftime('%B %d, %Y')}</p>
        </div>
    </div>
</body>
</html>"""
    
    return html

# Generate reports for all venues in the data
for venue_key in sorted(venue_data.keys()):
    data = venue_data[venue_key]
    html = generate_html_report(venue_key, data)
    
    # Convert key back to proper venue name (e.g., 'dallas' -> 'Dallas')
    venue_name = data['venue']
    
    # Save to file (in reports folder)
    filename = f"../reports/Topgolf_Venue_Report_{venue_name.replace(' ', '_')}_1PAGE.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"Generated: {filename}")

print(f"\nReports generated successfully! ({len(venue_data)} venue(s))")
