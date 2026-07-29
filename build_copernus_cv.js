const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, Header, Footer, AlignmentType,
        HeadingLevel, PageNumber, BorderStyle } = require('docx');

const blue = '2F5496';

function h(t) { return new Paragraph({ spacing: { before: 280, after: 120 }, border: { bottom: { style: BorderStyle.SINGLE, size: 1, color: blue, space: 4 } }, children: [new TextRun({ text: t.toUpperCase(), bold: true, font: 'Arial', size: 22, color: blue })] }); }
function p(t, opts={}) { return new Paragraph({ spacing: { after: opts.after || 60 }, indent: opts.indent ? { left: 360 } : undefined, children: [new TextRun({ text: t, font: 'Arial', size: 20, ...opts })] }); }
function bp(t) { return new Paragraph({ spacing: { after: 40 }, indent: { left: 360 }, children: [new TextRun({ text: '- ' + t, font: 'Arial', size: 20 })] }); }
function role(company, loc, title, dates) { return [
  new Paragraph({ spacing: { before: 160, after: 40 }, children: [new TextRun({ text: company + ' | ' + loc, bold: true, font: 'Arial', size: 21 })]}),
  new Paragraph({ spacing: { after: 80 }, children: [new TextRun({ text: title + ' | ' + dates, font: 'Arial', size: 20, italics: true, color: '444444' })]})
]; }

const doc = new Document({
  styles: { default: { document: { run: { font: 'Arial', size: 20 } } } },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1080, right: 1260, bottom: 1080, left: 1260 } } },
    children: [
      // Name
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 }, children: [new TextRun({ text: 'Pawan Singh Kapkoti', bold: true, font: 'Arial', size: 32, color: blue })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 }, children: [new TextRun({ text: 'Hull, England | 07442382622 | pawankapkoti3889@gmail.com', font: 'Arial', size: 18, color: '666666' })] }),

      // Profile
      h('Profile'),
      p('Operational Team Leader at Copernus with 12 months of daily SI (Integreater) and SQL Server Reporting Services experience. MSc Data Analytics with Microsoft PL-300 Power BI certification (March 2026). Proposing to apply data analytics skills to improve factory reporting \u2014 connecting batch traceability, yield tracking, and despatch decisions to live dashboards built from existing SQL Server data.', { after: 120 }),

      // Key Skills
      h('Key Skills'),
      new Paragraph({ spacing: { after: 40 }, children: [
        new TextRun({ text: 'Factory Systems: ', bold: true, font: 'Arial', size: 20 }),
        new TextRun({ text: 'SI (Integreater), SSRS, OCM dashboards, Run Maintenance, Stock Tracker', font: 'Arial', size: 20 })
      ]}),
      new Paragraph({ spacing: { after: 40 }, children: [
        new TextRun({ text: 'Data & Analytics: ', bold: true, font: 'Arial', size: 20 }),
        new TextRun({ text: 'SQL Server, Python (pandas, matplotlib, scikit-learn), Power BI, Excel', font: 'Arial', size: 20 })
      ]}),
      new Paragraph({ spacing: { after: 40 }, children: [
        new TextRun({ text: 'Traceability: ', bold: true, font: 'Arial', size: 20 }),
        new TextRun({ text: 'Batch codes, Nav Codes, Vector Tags, MSC/RSPCA chain of custody', font: 'Arial', size: 20 })
      ]}),
      new Paragraph({ spacing: { after: 40 }, children: [
        new TextRun({ text: 'Production: ', bold: true, font: 'Arial', size: 20 }),
        new TextRun({ text: 'Yield calculation, giveaway control, FEFO stock rotation, plan attainment', font: 'Arial', size: 20 })
      ]}),
      new Paragraph({ spacing: { after: 40 }, children: [
        new TextRun({ text: 'Retailers: ', bold: true, font: 'Arial', size: 20 }),
        new TextRun({ text: 'Lidl, Iceland, Aldi, Tesco, M&S specifications', font: 'Arial', size: 20 })
      ]}),
      new Paragraph({ spacing: { after: 80 }, children: [
        new TextRun({ text: 'Certifications: ', bold: true, font: 'Arial', size: 20 }),
        new TextRun({ text: 'Microsoft PL-300 Power BI (Active, March 2026), Google Data Analytics Professional Certificate', font: 'Arial', size: 20 })
      ]}),

      // Work Experience
      h('Work Experience'),
      ...role('Copernus Fresh Fish', 'Hull', 'Operational Team Leader', 'April 2025 \u2013 Present'),
      bp('Operated SI (Integreater) ERP for production data management: batch traceability reports, yield KPI monitoring, weight variance reconciliation, and audit-ready compliance records for Lidl and Iceland'),
      bp('Managed operational data workflows across 11+ operatives: production scheduling, shift handover documentation, raw material allocation tracking'),
      bp('Owned end-to-end data integrity from batch activation through weight capture, metal detection logging, label verification, and dispatch reconciliation'),
      bp('Identified despatch use-by date mismatch between planned and actual batch dates \u2014 proposed data-driven solution connecting SQL Server data to a live priority dashboard'),
      bp('Supporting IT with planned Python migration to improve SQL Server query performance'),

      ...role('Cranswick Convenience Foods', 'Hull', 'Cover Team Lead (Curing & Processing)', 'October 2024 \u2013 April 2025'),
      bp('Managed batch-level traceability data for M&S and Tesco premium lines: Nav Code and Vector tag validation, allergen cross-referencing, full audit trail'),
      bp('Monitored production metrics on Metapress systems: throughput rates, equipment utilisation, QC pass/fail ratios to Tesco Welfare Approved standards'),
      bp('Carried out environmental swabs and rapid allergen testing for QA line start-up authorisation'),

      ...role('Cranswick Convenience Foods', 'Hull', 'Food Operative', 'July 2024 \u2013 October 2024'),
      bp('Assisted NPD team with product trials, adjusted machinery parameters, recorded trial output data'),

      // Data Projects
      h('Data Projects'),
      p('github.com/Pawansingh3889', { color: blue, after: 80 }),
      bp('End-to-end data pipeline: 99,675 records, API ingestion, PostgreSQL, dbt transformations, live Streamlit dashboard, 3 automated CI/CD workflows'),
      bp('XGBoost ML model (93% accuracy) on 96,470 e-commerce records with 94 automated dbt quality checks'),
      bp('14 SQL analytical queries: window functions, CTEs, conditional aggregation across 99,673 records'),

      // Education
      h('Education'),
      p('MSc Data Analytics | Aston University | Jan 2023 \u2013 Mar 2024', { after: 40 }),
      p('BCA Computer Applications | Amity University | Aug 2019 \u2013 Aug 2022', { after: 40 }),
      p('Sainik School Ghorakhal (Science) | Mar 2011 \u2013 Mar 2018', { after: 40 }),
    ]
  }]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync('C:/Projects/captain-pkt/Pawan_CV_Copernus_2026.docx', buf);
  console.log('Done: Pawan_CV_Copernus_2026.docx (' + buf.length + ' bytes)');
});
