"""
Captain PKT Command Centre
60-Day Job Hunt Database + Intelligence System

SQLite database tracking:
- Job listings scraped from multiple sources
- Applications sent and their status
- Skills gap analysis per role
- Daily action items
- Competitor intelligence
"""

import sqlite3
import os
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "command_centre.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Jobs table - scraped listings
    c.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        company TEXT,
        location TEXT,
        salary_min REAL,
        salary_max REAL,
        currency TEXT DEFAULT 'GBP',
        job_type TEXT,  -- remote/hybrid/onsite
        contract_type TEXT,  -- permanent/contract/freelance
        source TEXT,  -- linkedin/indeed/adzuna/weworkremotely/remote.co
        url TEXT,
        is_sponsor INTEGER DEFAULT 0,  -- 1 if company sponsors visas
        requires_citizenship INTEGER DEFAULT 0,
        skills_required TEXT,  -- comma separated
        description TEXT,
        posted_date TEXT,
        scraped_date TEXT DEFAULT (date('now')),
        match_score REAL DEFAULT 0,  -- 0-100 how well it matches Captain PKT
        status TEXT DEFAULT 'new',  -- new/applied/rejected/interview/offer
        notes TEXT
    )""")

    # Applications table
    c.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_id INTEGER REFERENCES jobs(id),
        date_applied TEXT DEFAULT (date('now')),
        method TEXT,  -- linkedin_easy/email/company_site
        cv_version TEXT,
        cover_letter INTEGER DEFAULT 0,
        tailored_for TEXT,  -- what was customised
        response_date TEXT,
        response_type TEXT,  -- none/rejection/screening/interview/offer
        rejection_reason TEXT,
        interview_date TEXT,
        interview_type TEXT,  -- phone/video/onsite/technical
        interview_notes TEXT,
        follow_up_date TEXT,
        days_to_respond INTEGER
    )""")

    # Skills matrix
    c.execute("""
    CREATE TABLE IF NOT EXISTS skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        skill_name TEXT UNIQUE,
        category TEXT,  -- technical/tool/soft/certification
        pawan_level TEXT,  -- strong/moderate/basic/none
        market_demand TEXT,  -- high/medium/low
        appears_in_pct REAL DEFAULT 0,  -- % of scraped jobs requiring this
        evidence TEXT  -- which project proves this skill
    )""")

    # Daily plan
    c.execute("""
    CREATE TABLE IF NOT EXISTS daily_plan (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        day_number INTEGER,  -- 1-60
        date TEXT,
        phase TEXT,  -- weeks 1-2, 3-4, 5-6, 7-8
        task TEXT,
        category TEXT,  -- apply/build/learn/network/admin
        priority TEXT,  -- must/should/nice
        status TEXT DEFAULT 'pending',  -- pending/done/skipped
        notes TEXT
    )""")

    # Competitor profiles
    c.execute("""
    CREATE TABLE IF NOT EXISTS competitors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        linkedin_url TEXT,
        background TEXT,  -- degree/visa type
        got_hired INTEGER DEFAULT 0,
        company_hired TEXT,
        role_hired TEXT,
        key_skills TEXT,
        projects_count INTEGER,
        certifications TEXT,
        what_they_did_differently TEXT,
        source TEXT
    )""")

    # Targets - companies known to sponsor
    c.execute("""
    CREATE TABLE IF NOT EXISTS target_companies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT,
        industry TEXT,
        hq_location TEXT,
        sponsors_visa INTEGER DEFAULT 1,
        has_data_roles INTEGER DEFAULT 1,
        careers_url TEXT,
        glassdoor_rating REAL,
        notes TEXT,
        applied INTEGER DEFAULT 0,
        source TEXT  -- gov_sponsor_list/linkedin/referral
    )""")

    conn.commit()
    return conn


def populate_pawan_skills(conn):
    """Captain PKT's verified skill set with project evidence."""
    skills = [
        # Technical - Strong
        ('Python', 'technical', 'strong', 'high', 'Apex, uk-crime-pipeline, sql-crime-analytics'),
        ('SQL', 'technical', 'strong', 'high', 'sql-crime-analytics (14 queries), all pipeline projects'),
        ('PostgreSQL', 'technical', 'strong', 'high', 'uk-crime-pipeline (Neon), sql-crime-analytics (Docker)'),
        ('Data Pipelines', 'technical', 'strong', 'high', 'Apex (10-task Prefect), uk-crime-pipeline'),
        ('ETL', 'technical', 'strong', 'high', 'All pipeline projects'),
        ('Data Analysis', 'technical', 'strong', 'high', 'All projects'),
        ('Machine Learning', 'technical', 'strong', 'medium', 'Apex (XGBoost 93%, Isolation Forest)'),
        ('Statistics', 'technical', 'strong', 'medium', 'MSc Dissertation (Random Forest)'),

        # Tools - Strong
        ('dbt', 'tool', 'strong', 'high', 'uk-crime-pipeline (4 models, 53 tests), Apex'),
        ('Power BI', 'tool', 'strong', 'high', 'Apex (dashboard), PL-300 certified'),
        ('Streamlit', 'tool', 'strong', 'medium', 'uk-crime-pipeline (live dashboard)'),
        ('Docker', 'tool', 'strong', 'medium', 'Apex (Dockerfile), sql-crime-analytics'),
        ('Git/GitHub', 'tool', 'strong', 'high', 'All projects, CI/CD workflows'),
        ('GitHub Actions', 'tool', 'strong', 'medium', 'uk-crime-pipeline (3 workflows)'),
        ('Excel', 'tool', 'strong', 'high', 'uk-employment-excel (formulas, charts, VLOOKUP)'),
        ('Jupyter', 'tool', 'strong', 'medium', 'Apex, tax-fairness, all analysis projects'),

        # Tools - Moderate
        ('AWS (S3/Glue/Athena)', 'tool', 'moderate', 'high', 'Crime_Analysis project'),
        ('DuckDB', 'tool', 'moderate', 'medium', 'Apex project'),
        ('Prefect', 'tool', 'moderate', 'medium', 'Apex (10-task orchestration)'),
        ('Plotly', 'tool', 'moderate', 'medium', 'uk-crime-pipeline dashboard'),

        # Tools - Basic
        ('Spark', 'tool', 'basic', 'high', 'Mentioned in MSc but no standalone project'),
        ('Airflow', 'tool', 'none', 'high', 'No project - GAP'),
        ('Snowflake', 'tool', 'none', 'high', 'No project - GAP'),
        ('Terraform', 'tool', 'none', 'medium', 'No project - GAP'),
        ('Tableau', 'tool', 'none', 'medium', 'No project - uses Power BI instead'),
        ('Azure', 'tool', 'none', 'high', 'No project - GAP'),
        ('GCP/BigQuery', 'tool', 'none', 'high', 'No project - GAP'),

        # Certifications
        ('AWS DEA-C01', 'certification', 'strong', 'high', 'Certified'),
        ('PL-300 Power BI', 'certification', 'strong', 'high', 'Certified'),
        ('MSc Data Analytics', 'certification', 'strong', 'high', 'Aston University'),

        # Soft
        ('Communication', 'soft', 'strong', 'high', 'MSc, team lead duties at Cranswick'),
        ('Problem Solving', 'soft', 'strong', 'high', 'All projects demonstrate this'),
        ('Remote Work', 'soft', 'moderate', 'high', 'No direct evidence yet - GAP'),
    ]

    c = conn.cursor()
    for skill_data in skills:
        try:
            c.execute("INSERT OR REPLACE INTO skills (skill_name, category, pawan_level, market_demand, evidence) VALUES (?, ?, ?, ?, ?)", skill_data)
        except:
            pass
    conn.commit()


def populate_60_day_plan(conn):
    """The 60-day battle plan for Captain PKT."""
    start = datetime(2025, 3, 19)
    c = conn.cursor()

    plan = [
        # WEEK 1-2: Foundation + First Wave (Days 1-14)
        (1, 'Week 1-2', 'Build portfolio website and deploy', 'build', 'must'),
        (1, 'Week 1-2', 'Update LinkedIn headline + About + Open to Work', 'admin', 'must'),
        (1, 'Week 1-2', 'Set up job alerts on LinkedIn/Indeed/Reed/Adzuna', 'admin', 'must'),
        (2, 'Week 1-2', 'Apply to 5 data analyst roles on LinkedIn', 'apply', 'must'),
        (2, 'Week 1-2', 'Apply to 5 data analyst roles on Indeed', 'apply', 'must'),
        (3, 'Week 1-2', 'Tailored CV for data analyst roles', 'build', 'must'),
        (3, 'Week 1-2', 'Tailored CV for data engineer roles', 'build', 'must'),
        (4, 'Week 1-2', 'Apply to 5 remote data roles on weworkremotely/remote.co', 'apply', 'must'),
        (4, 'Week 1-2', 'Connect with 10 data professionals on LinkedIn', 'network', 'should'),
        (5, 'Week 1-2', 'Apply to 5 more roles', 'apply', 'must'),
        (5, 'Week 1-2', 'Practice SQL interview questions (30 min)', 'learn', 'must'),
        (6, 'Week 1-2', 'Review and respond to any application responses', 'apply', 'must'),
        (7, 'Week 1-2', 'REST DAY - review week 1 stats', 'admin', 'should'),
        (8, 'Week 1-2', 'Apply to 10 roles (batch Monday)', 'apply', 'must'),
        (9, 'Week 1-2', 'Follow up on week 1 applications with no response', 'apply', 'should'),
        (10, 'Week 1-2', 'Practice Python interview questions (30 min)', 'learn', 'must'),
        (11, 'Week 1-2', 'Apply to 5 contract/freelance data roles', 'apply', 'must'),
        (12, 'Week 1-2', 'Apply to 5 roles on company career pages directly', 'apply', 'must'),
        (13, 'Week 1-2', 'Message 5 recruiters specialising in data roles', 'network', 'must'),
        (14, 'Week 1-2', 'WEEK 2 REVIEW: count applications, responses, adjust strategy', 'admin', 'must'),

        # WEEK 3-4: Scale Up + Network (Days 15-28)
        (15, 'Week 3-4', 'Apply to 10 roles (Monday batch)', 'apply', 'must'),
        (16, 'Week 3-4', 'Reach out to Aston University alumni in data roles', 'network', 'should'),
        (17, 'Week 3-4', 'Apply to 5 US remote roles (higher pay)', 'apply', 'must'),
        (18, 'Week 3-4', 'Practice SQL window functions + CTEs (30 min)', 'learn', 'must'),
        (19, 'Week 3-4', 'Apply to 5 roles', 'apply', 'must'),
        (20, 'Week 3-4', 'Post on LinkedIn about a project (visibility)', 'network', 'should'),
        (21, 'Week 3-4', 'REST DAY', 'admin', 'nice'),
        (22, 'Week 3-4', 'Apply to 10 roles (Monday batch)', 'apply', 'must'),
        (23, 'Week 3-4', 'Research top 20 UK companies that sponsor data analysts', 'apply', 'must'),
        (24, 'Week 3-4', 'Apply directly to those 20 companies', 'apply', 'must'),
        (25, 'Week 3-4', 'Practice behavioural interview questions', 'learn', 'must'),
        (26, 'Week 3-4', 'Apply to 5 roles on Toptal/Upwork (freelance backup)', 'apply', 'should'),
        (27, 'Week 3-4', 'Follow up on all unanswered applications', 'apply', 'must'),
        (28, 'Week 3-4', 'MONTH 1 REVIEW: total apps, response rate, interviews', 'admin', 'must'),

        # WEEK 5-6: Intensify + Pivot if needed (Days 29-42)
        (29, 'Week 5-6', 'Apply to 10 roles', 'apply', 'must'),
        (30, 'Week 5-6', 'If <5% response rate: revise CV completely', 'build', 'must'),
        (31, 'Week 5-6', 'Apply to EU remote roles (Germany, Netherlands)', 'apply', 'should'),
        (32, 'Week 5-6', 'Practice technical interview: walk through Apex project', 'learn', 'must'),
        (33, 'Week 5-6', 'Apply to 5 roles', 'apply', 'must'),
        (34, 'Week 5-6', 'Register on Turing.com (remote dev matching platform)', 'apply', 'should'),
        (35, 'Week 5-6', 'REST DAY', 'admin', 'nice'),
        (36, 'Week 5-6', 'Apply to 10 roles', 'apply', 'must'),
        (37, 'Week 5-6', 'Cold message 10 hiring managers on LinkedIn', 'network', 'must'),
        (38, 'Week 5-6', 'Apply to 5 roles', 'apply', 'must'),
        (39, 'Week 5-6', 'Practice dbt + data modelling interview questions', 'learn', 'must'),
        (40, 'Week 5-6', 'Apply to 5 roles', 'apply', 'must'),
        (41, 'Week 5-6', 'Research Germany job seeker visa requirements', 'admin', 'should'),
        (42, 'Week 5-6', 'WEEK 6 REVIEW', 'admin', 'must'),

        # WEEK 7-8: Final Push (Days 43-60)
        (43, 'Week 7-8', 'Apply to 10 roles', 'apply', 'must'),
        (44, 'Week 7-8', 'If interviews: prepare intensively', 'learn', 'must'),
        (45, 'Week 7-8', 'If no interviews: try recruitment agencies', 'apply', 'must'),
        (46, 'Week 7-8', 'Apply to 5 roles', 'apply', 'must'),
        (47, 'Week 7-8', 'Contact Hays/Robert Half/Michael Page recruiters', 'network', 'must'),
        (48, 'Week 7-8', 'Apply to 5 roles', 'apply', 'must'),
        (49, 'Week 7-8', 'REST DAY', 'admin', 'nice'),
        (50, 'Week 7-8', 'Apply to 10 roles', 'apply', 'must'),
        (51, 'Week 7-8', 'Decision point: UK sponsored vs remote vs EU', 'admin', 'must'),
        (52, 'Week 7-8', 'Apply to 5 roles', 'apply', 'must'),
        (53, 'Week 7-8', 'If going remote from India: set up Indian freelance entity', 'admin', 'should'),
        (54, 'Week 7-8', 'Apply to 5 roles', 'apply', 'must'),
        (55, 'Week 7-8', 'Follow up on all outstanding applications', 'apply', 'must'),
        (56, 'Week 7-8', 'Start UK exit checklist if leaving', 'admin', 'should'),
        (57, 'Week 7-8', 'Apply to 5 roles', 'apply', 'must'),
        (58, 'Week 7-8', 'Apply to 5 roles', 'apply', 'must'),
        (59, 'Week 7-8', 'Final follow-ups', 'apply', 'must'),
        (60, 'Week 7-8', 'DAY 60 REVIEW: total apps, interviews, offers, next move', 'admin', 'must'),
    ]

    for day, phase, task, category, priority in plan:
        date = (start + timedelta(days=day - 1)).strftime('%Y-%m-%d')
        c.execute("INSERT INTO daily_plan (day_number, date, phase, task, category, priority) VALUES (?, ?, ?, ?, ?, ?)",
                  (day, date, phase, task, category, priority))

    conn.commit()


def populate_target_companies(conn):
    """UK companies known to sponsor data analyst/engineer roles."""
    companies = [
        ('Deloitte', 'Consulting', 'London', 1, 1, 'https://www2.deloitte.com/uk/en/careers.html', 4.0, 'Big 4 - sponsors regularly'),
        ('PwC', 'Consulting', 'London', 1, 1, 'https://www.pwc.co.uk/careers.html', 3.9, 'Big 4'),
        ('EY', 'Consulting', 'London', 1, 1, 'https://www.ey.com/en_uk/careers', 3.8, 'Big 4'),
        ('KPMG', 'Consulting', 'London', 1, 1, 'https://www.kpmgcareers.co.uk', 3.7, 'Big 4'),
        ('Accenture', 'Consulting', 'London', 1, 1, 'https://www.accenture.com/gb-en/careers', 3.9, 'Sponsors data roles'),
        ('Capgemini', 'Consulting', 'London', 1, 1, 'https://www.capgemini.com/gb-en/careers/', 3.7, 'Sponsors regularly'),
        ('Tata Consultancy', 'IT Services', 'London', 1, 1, 'https://www.tcs.com/careers/uk', 3.5, 'Indian company - sponsors'),
        ('Infosys', 'IT Services', 'London', 1, 1, 'https://www.infosys.com/careers/', 3.6, 'Indian company - sponsors'),
        ('Wipro', 'IT Services', 'London', 1, 1, 'https://careers.wipro.com', 3.4, 'Indian company - sponsors'),
        ('HCLTech', 'IT Services', 'London', 1, 1, 'https://www.hcltech.com/careers', 3.5, 'Indian company - sponsors'),
        ('NHS Digital', 'Healthcare', 'Leeds', 1, 1, 'https://digital.nhs.uk/careers', 3.8, 'Public sector - sponsors'),
        ('Home Office', 'Government', 'London', 1, 1, 'https://www.civilservicejobs.service.gov.uk', 3.5, 'Civil service - sponsors'),
        ('ONS', 'Government', 'Newport', 1, 1, 'https://www.ons.gov.uk/aboutus/careers', 3.7, 'Office for National Statistics'),
        ('Barclays', 'Banking', 'London', 1, 1, 'https://search.jobs.barclays', 3.7, 'Sponsors data roles'),
        ('HSBC', 'Banking', 'London', 1, 1, 'https://www.hsbc.com/careers', 3.6, 'Sponsors data roles'),
        ('Lloyds', 'Banking', 'London', 1, 1, 'https://www.lloydsbankinggroup.com/careers.html', 3.8, 'Sponsors'),
        ('Sky', 'Media', 'London', 1, 1, 'https://www.skygroup.sky/careers', 3.9, 'Tech company - sponsors'),
        ('BT', 'Telecom', 'London', 1, 1, 'https://www.bt.com/careers', 3.5, 'Sponsors data roles'),
        ('Rolls-Royce', 'Engineering', 'Derby', 1, 1, 'https://careers.rolls-royce.com', 4.0, 'Sponsors - Derby near you'),
        ('Booking.com', 'Travel', 'London', 1, 1, 'https://jobs.booking.com', 3.8, 'Remote-friendly + sponsors'),
        ('Revolut', 'Fintech', 'London', 1, 1, 'https://www.revolut.com/careers/', 3.2, 'Sponsors but demanding'),
        ('Wise', 'Fintech', 'London', 1, 1, 'https://www.wise.jobs', 4.2, 'Remote + sponsors'),
        ('Deliveroo', 'Tech', 'London', 1, 1, 'https://careers.deliveroo.co.uk', 3.5, 'Data-heavy company'),
        ('Just Eat', 'Tech', 'London', 1, 1, 'https://careers.justeattakeaway.com', 3.4, 'Data roles available'),
        ('Canonical', 'Tech', 'Remote', 1, 1, 'https://canonical.com/careers', 3.8, 'Fully remote - sponsors'),
    ]

    c = conn.cursor()
    for comp in companies:
        c.execute("INSERT INTO target_companies (company_name, industry, hq_location, sponsors_visa, has_data_roles, careers_url, glassdoor_rating, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", comp)
    conn.commit()


def generate_report(conn):
    """Print Captain PKT's situation report."""
    c = conn.cursor()

    print("=" * 60)
    print("  CAPTAIN PKT COMMAND CENTRE - SITUATION REPORT")
    print("=" * 60)

    # Skills
    c.execute("SELECT COUNT(*) FROM skills WHERE pawan_level = 'strong'")
    strong = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM skills WHERE pawan_level = 'none' AND market_demand = 'high'")
    gaps = c.fetchone()[0]
    print(f"\nSkills: {strong} strong | {gaps} high-demand gaps")

    c.execute("SELECT skill_name FROM skills WHERE pawan_level = 'none' AND market_demand = 'high'")
    print(f"Critical gaps: {', '.join(r[0] for r in c.fetchall())}")

    # Plan
    c.execute("SELECT COUNT(*) FROM daily_plan")
    total_tasks = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM daily_plan WHERE status = 'done'")
    done = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM daily_plan WHERE category = 'apply'")
    apply_tasks = c.fetchone()[0]
    print(f"\n60-Day Plan: {done}/{total_tasks} tasks done")
    print(f"Application tasks: {apply_tasks}")

    # Targets
    c.execute("SELECT COUNT(*) FROM target_companies")
    targets = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM target_companies WHERE applied = 1")
    applied = c.fetchone()[0]
    print(f"\nTarget companies: {targets} identified, {applied} applied")

    # Timeline
    from datetime import datetime
    days_left = (datetime(2026, 5, 1) - datetime.now()).days
    print(f"\nDays until PSW expires: {days_left}")
    print(f"Target: 200+ applications in 60 days")
    print(f"That's ~3-4 applications per day")
    print("=" * 60)


if __name__ == "__main__":
    conn = init_db()
    populate_pawan_skills(conn)
    populate_60_day_plan(conn)
    populate_target_companies(conn)
    generate_report(conn)
    conn.close()
    print(f"\nDatabase saved: {DB_PATH}")
