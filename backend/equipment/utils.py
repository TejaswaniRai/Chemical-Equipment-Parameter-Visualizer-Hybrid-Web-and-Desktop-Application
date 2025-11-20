import pandas as pd
from .models import Dataset, Equipment
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime


def process_csv_file(df, dataset_name, user):
    """
    Process CSV file and create dataset with equipment items
    
    Args:
        df: pandas DataFrame containing equipment data
        dataset_name: name of the dataset
        user: User who uploaded the file
    
    Returns:
        tuple: (dataset, equipment_list)
    """
    # Calculate summary statistics
    total_count = len(df)
    avg_flowrate = df['Flowrate'].mean()
    avg_pressure = df['Pressure'].mean()
    avg_temperature = df['Temperature'].mean()
    
    # Calculate equipment type distribution
    equipment_types = df['Type'].value_counts().to_dict()
    
    # Create Dataset
    dataset = Dataset.objects.create(
        name=dataset_name,
        uploaded_by=user,
        total_count=total_count,
        avg_flowrate=round(avg_flowrate, 2),
        avg_pressure=round(avg_pressure, 2),
        avg_temperature=round(avg_temperature, 2),
        equipment_types=equipment_types
    )
    
    # Create Equipment items
    equipment_list = []
    for _, row in df.iterrows():
        equipment = Equipment.objects.create(
            dataset=dataset,
            equipment_name=row['Equipment Name'],
            equipment_type=row['Type'],
            flowrate=row['Flowrate'],
            pressure=row['Pressure'],
            temperature=row['Temperature']
        )
        equipment_list.append(equipment)
    
    return dataset, equipment_list


def generate_pdf_report(dataset):
    """
    Generate a PDF report for a dataset
    
    Args:
        dataset: Dataset object
    
    Returns:
        BytesIO: PDF file buffer
    """
    buffer = BytesIO()
    
    # Create document with proper margins
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=50
    )
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=30,
        alignment=1,  # Center
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#34495E'),
        spaceAfter=12,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        fontName='Helvetica'
    )
    
    # Title
    title = Paragraph("<b>Chemical Equipment Analysis Report</b>", title_style)
    elements.append(title)
    
    # Subtitle with date
    subtitle = Paragraph(
        f"<i>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</i>",
        ParagraphStyle('subtitle', parent=styles['Normal'], alignment=1, fontSize=10, textColor=colors.grey)
    )
    elements.append(subtitle)
    elements.append(Spacer(1, 0.4*inch))
    
    # Dataset Information
    info_heading = Paragraph("<b>Dataset Information</b>", heading_style)
    elements.append(info_heading)
    elements.append(Spacer(1, 0.1*inch))
    
    info_data = [
        ['Dataset Name:', dataset.name],
        ['Upload Date:', dataset.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')],
        ['Uploaded By:', dataset.uploaded_by.username if dataset.uploaded_by else 'N/A'],
        ['Total Equipment Count:', str(dataset.total_count)],
    ]
    
    info_table = Table(info_data, colWidths=[2.2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E8F4F8')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elements.append(info_table)
    elements.append(Spacer(1, 0.4*inch))
    
    # Summary Statistics
    stats_heading = Paragraph("<b>Summary Statistics</b>", heading_style)
    elements.append(stats_heading)
    elements.append(Spacer(1, 0.1*inch))
    
    stats_data = [
        ['Metric', 'Average Value', 'Unit'],
        ['Flowrate', f"{dataset.avg_flowrate:.2f}", 'L/min'],
        ['Pressure', f"{dataset.avg_pressure:.2f}", 'bar'],
        ['Temperature', f"{dataset.avg_temperature:.2f}", '°C'],
    ]
    
    stats_table = Table(stats_data, colWidths=[2.5*inch, 2*inch, 1.7*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F0F8FF')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elements.append(stats_table)
    elements.append(Spacer(1, 0.4*inch))
    
    # Equipment Type Distribution
    type_heading = Paragraph("<b>Equipment Type Distribution</b>", heading_style)
    elements.append(type_heading)
    elements.append(Spacer(1, 0.1*inch))
    
    type_data = [['Equipment Type', 'Count', 'Percentage']]
    total = sum(dataset.equipment_types.values())
    for eq_type, count in sorted(dataset.equipment_types.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total * 100) if total > 0 else 0
        type_data.append([eq_type, str(count), f"{percentage:.1f}%"])
    
    type_table = Table(type_data, colWidths=[2.5*inch, 2*inch, 1.7*inch])
    type_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ECC71')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F0FFF0')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elements.append(type_table)
    elements.append(Spacer(1, 0.4*inch))
    
    # Equipment Details
    details_heading = Paragraph("<b>Equipment Details</b>", heading_style)
    elements.append(details_heading)
    elements.append(Spacer(1, 0.1*inch))
    
    equipment_data = [['Equipment Name', 'Type', 'Flowrate\n(L/min)', 'Pressure\n(bar)', 'Temp\n(°C)']]
    for equipment in dataset.equipment_items.all()[:25]:  # Show first 25 items
        equipment_data.append([
            equipment.equipment_name,
            equipment.equipment_type,
            f"{equipment.flowrate:.2f}",
            f"{equipment.pressure:.2f}",
            f"{equipment.temperature:.2f}"
        ])
    
    if dataset.equipment_items.count() > 25:
        equipment_data.append(['...', '...', '...', '...', '...'])
        remaining = dataset.total_count - 25
        equipment_data.append([f'+ {remaining} more items (showing 25 of {dataset.total_count})', '', '', '', ''])
    
    equipment_table = Table(equipment_data, colWidths=[1.9*inch, 1.4*inch, 1.1*inch, 1.1*inch, 0.7*inch])
    equipment_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E74C3C')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#FFF5F5')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elements.append(equipment_table)
    
    # Footer note
    elements.append(Spacer(1, 0.3*inch))
    footer_text = Paragraph(
        "<i>This report was automatically generated by the Chemical Equipment Visualizer System.</i>",
        ParagraphStyle('footer', parent=styles['Normal'], fontSize=8, textColor=colors.grey, alignment=1)
    )
    elements.append(footer_text)
    
    # Build PDF
    try:
        doc.build(elements)
    except Exception as e:
        print(f"Error building PDF: {e}")
        raise
    
    buffer.seek(0)
    return buffer
