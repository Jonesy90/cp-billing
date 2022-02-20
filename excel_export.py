import xlsxwriter
import datetime
from app import *

today = datetime.date.today()
first = today.replace(day=1)
last_month = first - datetime.timedelta(days=1)

def create_workbook(data, key):
    """
    Creates an Excel Workbook for each Content Provider group.
    Generate a formatting for the Excel documents for both sheets.

    """
    workbook = xlsxwriter.Workbook(f'excel/{key}.xlsx')
    worksheet1 = workbook.add_worksheet('Ad-VoD Statement')
    worksheet2 = workbook.add_worksheet('Detailed Report')


    #Shared Formatting
    title_format = workbook.add_format({'font_color': 'red', 'bold': True, 'align': 'center', 'valign': 'vcenter', 'font_size': 16})
    cell_background_colour = workbook.add_format({'bg_color': '#2F2431', 'font_color': 'white', 'bold': True, 'align': 'center', 'valign': 'vcenter', 'text_justlast': True, 'font_size': 12})
    currency_format = workbook.add_format({'bg_color': 'red', 'font_color': 'white', 'num_format': '_-£* #,##0.00_-;-£* #,##0.00_-;_-£* "-"??_-;_-@_-' })
    impressions_format = workbook.add_format({'bg_color': 'red', 'font_color': 'white', 'num_format': '#,##0_ ;-#,##0 ' })


    #Worksheet1 Formatting
    worksheet1.set_row(22, 40.00)
    worksheet1.insert_image('D5', 'virgin_media_logo.png')
    merge_format1 = workbook.add_format({
        'bold': True,
        'bg_color': '#2F2431',
        'font_color': 'white',
        'align': 'center',
        'valign': 'vcenter'
    })
    merge_format2 = workbook.add_format({
        'align': 'center',
        'valign': 'vcenter',
        'text_wrap': True
    })
    worksheet1.set_column(1, 6, 32.00)
    date_format = workbook.add_format({'num_format': 'mmmm yyyy'})


    #Worksheet2 Formatting
    worksheet2.set_row(6, 40.00)
    cp_format = workbook.add_format({'font_size': 16, 'bold': True, 'align': 'center', 'valign': 'vcenter'})
    worksheet2.insert_image('F1', 'virgin_media_logo.png')
    worksheet2.set_column(1, 9, 30.00)
    currency_format2 = workbook.add_format({'num_format': '_-£* #,##0.00_-;-£* #,##0.00_-;_-£* "-"??_-;_-@_-' })
    impressions_format2 = workbook.add_format({'num_format': '#,##0_ ;-#,##0 ' })

    #Worksheet 1
    worksheet1.merge_range('B2:F2', 'Content Provider', merge_format1)
    worksheet1.merge_range('E5:F12', 'Virgin Media, Media House, Comminication Building, Bartley Wood Business Park, Hook, Hampshire, RG27 9UP', merge_format2)
    worksheet1.write('B22', 'AD-VOD VIEWS', title_format)
    worksheet1.write('B23', 'Month', cell_background_colour)
    worksheet1.write('C23', 'Booked Views', cell_background_colour)
    worksheet1.write('D23', 'Total Revenue (- agency commission)', cell_background_colour)
    worksheet1.write('E23', 'Revenue Share to VM', cell_background_colour)
    worksheet1.write('F23', f'Revenue Share to {key}', cell_background_colour)

    worksheet1.write('B24', last_month, date_format)
    worksheet1.write_formula('C24', "='Detailed Report'!E8", impressions_format2)
    worksheet1.write_formula('D24', "='Detailed Report'!H8", currency_format2)
    worksheet1.write_formula('E24', "='Detailed Report'!I8", currency_format2)
    worksheet1.write_formula('F24', "='Detailed Report'!J8", currency_format2)

    #Worksheet 2
    worksheet2.write('C2', key, cp_format)
    worksheet2.write('C5', 'REPORT DATA', title_format)
    worksheet2.write('B7', 'Campaign External ID', cell_background_colour)
    worksheet2.write('C7', 'Campaign Name', cell_background_colour)
    worksheet2.write('D7', 'Content Provider', cell_background_colour)
    worksheet2.write('E7', 'Delivered Impressions', cell_background_colour)
    worksheet2.write('F7', 'CPM Rate', cell_background_colour)
    worksheet2.write('G7', 'Gross Revenue', cell_background_colour)
    worksheet2.write('H7', 'Net Revenue', cell_background_colour)
    worksheet2.write('I7', 'VM Revenue Share', cell_background_colour)
    worksheet2.write('J7', 'CP Revenue Share', cell_background_colour)


    rowIndex = 9

    for row in data:
        worksheet2.write('B' + str(rowIndex), row.campaign_external_id)
        worksheet2.write('C' + str(rowIndex), row.campaign_name)
        worksheet2.write('D' + str(rowIndex), row.content_provider)
        worksheet2.write('E' + str(rowIndex), row.delivered_impressions, impressions_format2)
        worksheet2.write('F' + str(rowIndex), row.cpm_rate, currency_format2)
        worksheet2.write('G' + str(rowIndex), row.gross_revenue, currency_format2)
        worksheet2.write('H' + str(rowIndex), row.net_revenue, currency_format2)
        worksheet2.write('I' + str(rowIndex), row.vm_revenue_share, currency_format2)
        worksheet2.write('J' + str(rowIndex), row.cp_revenue_share, currency_format2)

        rowIndex += 1

    worksheet2.write_formula('E8', '=sum(E9:E1000)', impressions_format)
    worksheet2.write_formula('G8', '=sum(G9:G1000)', currency_format)
    worksheet2.write_formula('H8', '=sum(H9:H1000)', currency_format)
    worksheet2.write_formula('I8', '=sum(I9:I1000)', currency_format)
    worksheet2.write_formula('J8', '=sum(J9:J1000)', currency_format)

    workbook.close()