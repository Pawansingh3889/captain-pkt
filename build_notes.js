const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        Header, Footer, AlignmentType, HeadingLevel,
        BorderStyle, WidthType, ShadingType, PageNumber, PageBreak } = require('docx');

const blue = '2F5496';
const sz = 22;
const border = { style: BorderStyle.SINGLE, size: 1, color: 'CCCCCC' };
const borders = { top: border, bottom: border, left: border, right: border };
const cellM = { top: 80, bottom: 80, left: 120, right: 120 };

function makeTable(headers, rows, colWidths) {
  const hdrRow = new TableRow({ children: headers.map((h, i) =>
    new TableCell({ borders, width: { size: colWidths[i], type: WidthType.DXA },
      shading: { fill: blue, type: ShadingType.CLEAR }, margins: cellM,
      children: [new Paragraph({ children: [new TextRun({ text: h, bold: true, color: 'FFFFFF', font: 'Arial', size: sz })] })]
    }))
  });
  const dataRows = rows.map((r, ri) => new TableRow({ children: r.map((c, ci) =>
    new TableCell({ borders, width: { size: colWidths[ci], type: WidthType.DXA },
      shading: ri % 2 === 0 ? { fill: 'F2F2F2', type: ShadingType.CLEAR } : undefined, margins: cellM,
      children: [new Paragraph({ children: [new TextRun({ text: c, font: 'Arial', size: sz })] })]
    }))
  }));
  return new Table({ width: { size: colWidths.reduce((a,b)=>a+b,0), type: WidthType.DXA }, columnWidths: colWidths, rows: [hdrRow, ...dataRows] });
}

function h1(t) { return new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun({ text: t, bold: true, font: 'Arial', size: 28, color: blue })] }); }
function h2(t) { return new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun({ text: t, bold: true, font: 'Arial', size: 24, color: blue })] }); }
function h3(t) { return new Paragraph({ children: [new TextRun({ text: t, bold: true, font: 'Arial', size: sz, color: blue })] }); }
function p(t) { return new Paragraph({ spacing: { after: 100 }, children: [new TextRun({ text: t, font: 'Arial', size: sz })] }); }
function bp(t) { return new Paragraph({ spacing: { after: 60 }, indent: { left: 360 }, children: [new TextRun({ text: '- ' + t, font: 'Arial', size: sz })] }); }
function quote(t) { return new Paragraph({ spacing: { after: 100 }, indent: { left: 360 }, children: [new TextRun({ text: t, font: 'Arial', size: sz, italics: true, color: '333333' })] }); }
function bold_p(l, t) { return new Paragraph({ spacing: { after: 100 }, children: [new TextRun({ text: l, bold: true, font: 'Arial', size: sz }), new TextRun({ text: t, font: 'Arial', size: sz })] }); }
function red_p(t) { return new Paragraph({ spacing: { after: 60 }, indent: { left: 360 }, children: [new TextRun({ text: t, font: 'Arial', size: sz, color: 'C00000' })] }); }

// ========== DOCUMENT 1: Meeting Notes ==========
const doc1 = new Document({
  styles: { default: { document: { run: { font: 'Arial', size: sz } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 28, bold: true, font: 'Arial', color: blue }, paragraph: { spacing: { before: 300, after: 160 }, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 24, bold: true, font: 'Arial', color: blue }, paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 1 } },
    ]
  },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1260, right: 1260, bottom: 1260, left: 1260 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: 'CONFIDENTIAL - For Pawan Only | Page ', font: 'Arial', size: 16, color: 'C00000' }), new TextRun({ children: [PageNumber.CURRENT], font: 'Arial', size: 16 })] })] }) },
    children: [
      h1('Meeting Notes - Cheat Sheet'),
      p('Read before each meeting. Memorise key points.'),

      h1('For Megan (HR) - Email + Brief Chat'),
      h2('Key Points:'),
      bp('NOT asking to leave production. NOT asking for a new role right now.'),
      bp('Proposing to help IT with Python migration AFTER finishing team leader duties.'),
      bp('Aware that timing is sensitive - BRCGS audit is coming in a couple of months.'),
      bp('Will not start training until Line 2 has adequate team leader coverage.'),
      bp('The data improvements (reducing paperwork) actually support the BRCGS audit preparation.'),
      h3('What to say:'),
      quote('"I have a proposal to help IT with some data improvements on the factory floor. I understand the timing needs to work around production - I am not asking to step away from my team leader role. I would like to discuss it with Danny first. Could you help arrange a meeting on Monday?"'),
      h3('What NOT to say:'),
      red_p('Do not mention visa, sponsorship, or CoS'),
      red_p('Do not mention leaving the company'),
      red_p('Do not attach your CV'),
      red_p('Do not mention wanting a different job title'),
      h3('Megan already knows:'),
      bp('She interviewed you for Supply Chain Junior in February'),
      bp('She commended your professionalism and retained your CV'),
      bp('She has applied for a Certificate of Sponsorship (discuss LATER, not now)'),

      new Paragraph({ children: [new PageBreak()] }),
      h1('For Danny (Factory Manager) - Monday Meeting'),
      h3('Open with (60 seconds):'),
      quote('"Danny, you remember when we discussed the despatch use-by date problem in my interview. I have been thinking about it since. The data to fix it already exists in SQL Server. I have put together a proposal showing how I can build a dashboard that connects batch codes to actual use-by dates. Despatch would see which stock to ship first without needing QA concessions. It would take about two weeks for a working prototype."'),
      h2('Key Points:'),
      bp('The despatch problem is real - he already acknowledged it'),
      bp('Nobody was hired for the IT vacancy - the problem is still unsolved'),
      bp('Paul (IT) is already planning Python - this supports an existing plan'),
      bp('PL-300 certification earned this week - directly relevant'),
      bp('Zero risk - read-only database access, stop in 2 weeks if it does not work'),
      h3('Numbers Danny cares about:'),
      bold_p('Loma giveaway: ', '14.4g per pack over target = 26kg free product per batch = \u00A3260-390 lost'),
      bold_p('Rejection rate: ', '17% on Salmon Fillet Joint batch - needs investigation'),
      bold_p('QA concessions: ', 'Each one costs time and audit risk'),
      bold_p('RSPCA on GG: ', 'Premium cost, standard revenue - no visibility'),
      h3('What Danny will ask:'),
      bold_p('"When would you do this?" ', '- "After my team leader duties. I am aware we have 5 team leaders across 4 lines, and 2 lines need 2 leaders each. I would not start until Line 2 has adequate coverage. Production comes first."'),
      bold_p('"What about BRCGS?" ', '- "The dashboards would help audit preparation - batch traceability in seconds instead of hours. But the timing has to work for you and Simon."'),
      bold_p('"Can Paul not do this?" ', '- "Paul is one person managing all IT. I am offering to help him, not replace him. Two people move faster than one."'),
      bold_p('"What do you need?" ', '- "Read-only SQL Server access from Paul, and your feedback on which dashboard is most useful first. The software is free."'),
      h3('Show Danny:'),
      bp('Proposal_Short_Version.docx (he reads this)'),
      bp('Copernus_Future_Goals.docx (flip through to show vision)'),
      bp('PL-300 certificate on phone (only if asked)'),
      h3('What NOT to say to Danny:'),
      red_p('Do not mention visa or sponsorship'),
      red_p('Do not mention wanting to leave production'),
      red_p('Do not criticise current systems or people'),
      red_p('Say "opportunity to add visibility" not "the data is wrong"'),

      new Paragraph({ children: [new PageBreak()] }),
      h1('For Simon (Production Manager)'),
      h3('What to say:'),
      quote('"Simon, I have been looking at how we can use the data we already have in SQL Server more effectively. The plan attainment tracking you do in Excel could be automated - the data is already in OCM and SI. Would it help if I built something that pulls it automatically? I would do this after finishing my team leader duties, not during production time."'),
      h3('Key Points:'),
      bp('You are NOT leaving his team - adding a skill that helps the team'),
      bp('His Excel report gets automated - saves him 30+ minutes daily'),
      bp('Team leader coverage is your priority first'),
      bp('BRCGS preparation - the dashboards help with audit readiness'),
      h3('What NOT to say:'),
      red_p('Do not say "your Excel is inefficient"'),
      red_p('Frame it as "making your job easier" not "replacing your work"'),

      h1('For the Director - Personal Conversation'),
      h3('What to say:'),
      quote('"We have a strong production setup with SI and SQL Server. What we are missing is an analytics layer on top - something that turns data into decisions. The despatch team makes shipping decisions on planned use-by dates, but actual batch dates are different. That costs us QA concessions and audit risk. I can build a prototype in two weeks using Power BI, which is already included in our Microsoft licence."'),
      h3('Show:'),
      bp('Proposal_Short_Version.docx (1 page quick read)'),
      bp('Copernus_Future_Goals.docx (10 initiatives - shows vision)'),
      bp('Loma number: "14.4g per pack = 26kg free product per batch"'),

      new Paragraph({ children: [new PageBreak()] }),
      h1('Quick Memory Card - Read 5 Minutes Before'),
      h2('Numbers:'),
      bp('14.4g giveaway per pack (Loma data)'),
      bp('26kg free product per batch'),
      bp('\u00A3260-390 lost per batch'),
      bp('17% rejection rate on Salmon Fillet Joint'),
      bp('5 team leaders, 4 lines, 2 lines need 2 leaders'),
      bp('BRCGS audit: couple of months away'),
      bp('PL-300 certified: March 18, 2026'),
      bp('Power BI: free with Microsoft licence'),
      bp('Proof of concept: 2 weeks'),
      h2('Phrases TO USE:'),
      bp('"Read-only access - cannot break anything"'),
      bp('"The data already exists - it just needs connecting"'),
      bp('"Two-week proof of concept - stop if it does not work"'),
      bp('"After my team leader duties - production comes first"'),
      bp('"This actually reduces paperwork long term"'),
      h2('Phrases to AVOID:'),
      red_p('"I want a different role"'),
      red_p('"The current system is bad"'),
      red_p('"I need visa sponsorship"'),
      red_p('"My visa expires soon"'),
      red_p('"I want to leave production"'),
    ]
  }]
});

// ========== DOCUMENT 2: HR Staffing Note ==========
const doc2 = new Document({
  styles: { default: { document: { run: { font: 'Arial', size: sz } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 28, bold: true, font: 'Arial', color: blue }, paragraph: { spacing: { before: 300, after: 160 }, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 24, bold: true, font: 'Arial', color: blue }, paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 1 } },
    ]
  },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1260, right: 1260, bottom: 1260, left: 1260 } } },
    children: [
      h1('Staffing Context - Internal Note'),
      h2('Current Team Leader Structure'),
      makeTable(['Line', 'Team Leaders', 'Roles'], [
        ['Line 1', '1', 'Line control'],
        ['Line 2', '2', '1 line control + 1 paperwork'],
        ['Line 3', '1', 'Line control'],
        ['Line 4', '2 (when required)', '1 line control + 1 paperwork'],
        ['Total', '5', ''],
      ], [2000, 2000, 5026]),
      h2('Why 2 Team Leaders on Some Lines'),
      bp('BRCGS A-level certification requires detailed paperwork at every stage'),
      bp('One team leader manages the production line (operators, output, quality)'),
      bp('Second team leader maintains paperwork (batch records, traceability, compliance)'),
      bp('Both roles are essential - dropping either risks audit failure'),
      h2('Current Pressures'),
      bp('Production manager Simon regularly steps onto the line to help when short-staffed'),
      bp('If one team leader takes holiday, remaining team leaders cover multiple responsibilities'),
      bp('BRCGS audit approximately 2 months away - standards cannot slip'),
      bp('Company culture is collaborative but goodwill cannot replace staffing'),
      h2('My Commitment'),
      bp('Team leader duties on Line 2 are my first priority'),
      bp('IT/data training will only begin once Line 2 has adequate team leader coverage'),
      bp('If a new team leader is hired for Line 2, that frees capacity for data work'),
      bp('Until then, any data work happens strictly outside production hours'),
      h2('How Data Improvements Reduce Staffing Pressure'),
      p('The reason 2 team leaders are needed on some lines is largely the paperwork burden:'),
      makeTable(['Current Manual Task', 'Proposed Automation', 'Impact'], [
        ['Manual weight recording from Loma', 'Automated data capture to SQL Server', 'Removes one manual recording step'],
        ['Manual basket counting (salmon)', 'OCM individual basket weighing', 'More accurate, less manual work'],
        ['Plan attainment tracking in Excel', 'Auto-calculated from OCM/SI data', 'Saves Simon 30+ min daily'],
        ['Walking coldstore to check dates', 'FEFO dashboard on screen', 'Saves despatch 15+ min per check'],
        ['Compiling traceability for audits', 'One-click query from SQL Server', 'Audit prep: hours to minutes'],
      ], [3000, 3000, 3026]),
      p('Long-term outcome: If paperwork is automated, the second team leader role on lines that require 2 becomes less critical. This does not eliminate the role - it reduces the workload enough that 1 strong team leader with automated tools could potentially manage what currently requires 2.'),
    ]
  }]
});

Promise.all([
  Packer.toBuffer(doc1).then(buf => { fs.writeFileSync('C:/Projects/captain-pkt/For_Pawan_Reference/Meeting_Notes_All.docx', buf); console.log('Meeting_Notes_All.docx: ' + buf.length); }),
  Packer.toBuffer(doc2).then(buf => { fs.writeFileSync('C:/Projects/captain-pkt/For_Pawan_Reference/HR_Staffing_Note.docx', buf); console.log('HR_Staffing_Note.docx: ' + buf.length); }),
]);
