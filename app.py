#Internal Import
import datetime
from models import *
from content_providers import *

#External Import
import xlsxwriter
import csv
import argparse
import pathlib


parser = argparse.ArgumentParser(description='Uploads the CSV, process it.')
parser.add_argument('source_file', metavar='source_file', type=pathlib.Path, help='Upload the CSV file.')

args = parser.parse_args()

csv_upload = args.source_file

today = datetime.date.today()
first = today.replace(day=1)
last_month = first - datetime.timedelta(days=1)

print(f'Today: {today}')
print(f'First: {first}')
print(f'Last Month: {last_month}')

def add_csv():
    """
    Takes a CSV to commit to a SQLite Database.
    Checks each data is within a current database. If so, it will ignore and move on. Otherwise, it will commit to the DB.

    """

    with open(csv_upload, newline='') as csvfile:
        data = csv.DictReader(csvfile)
        for row in data:
            # print(row)
            campaign_external_id = row['\ufeffCampaign External ID']
            campaign_name = row['Campaign Name']
            content_provider = row['Content Provider']
            delivered_impressions = row['Delivered Impressions'].replace(',', '')
            cpm_rate = row['CPM Rate']
            gross_revenue = row['Gross Revenue'].replace(',', '').replace('-', '0')
            net_revenue = row['Net Revenue'].replace(',', '').replace('-', '0')

            new_data = ContentProvider(campaign_external_id=campaign_external_id, campaign_name=campaign_name, content_provider=content_provider, delivered_impressions=delivered_impressions, cpm_rate=cpm_rate, gross_revenue=float(gross_revenue), net_revenue=float(net_revenue))
            booking_in_db = session.query(ContentProvider).filter(ContentProvider.campaign_external_id==new_data.campaign_external_id, ContentProvider.content_provider==new_data.content_provider, ContentProvider.delivered_impressions==new_data.delivered_impressions).one_or_none()

            if booking_in_db != None:
                pass
            else:
                session.add(new_data)
                session.commit()

 
def calculate():
    """
    Calculates the split between Virgin Media and the Content Provider and places them all into a database.
    
    """

    try:
        for _, value in ALL_CONTENT_PROVIDERS.items():
            for key, value in value.items():
                # print(f'Key: {key}')
                # print(f'Value: {value}')
                database = session.query(ContentProvider).filter(ContentProvider.content_provider==key)
                # print(f'Database == {database}')
                for data in database:
                    campaign_external_id = data.campaign_external_id
                    campaign_name = data.campaign_name
                    content_provider = data.content_provider
                    delivered_impressions = data.delivered_impressions
                    cpm_rate = data.cpm_rate
                    gross_revenue = data.gross_revenue
                    net_revenue = data.net_revenue
                    vm_revenue_share = (data.net_revenue * value)
                    cp_revenue_share = data.net_revenue - vm_revenue_share

                    new_data = CpBilling(campaign_external_id=campaign_external_id, campaign_name=campaign_name, content_provider=content_provider, 
                        delivered_impressions=delivered_impressions, cpm_rate=cpm_rate, gross_revenue=gross_revenue, net_revenue=net_revenue,
                        vm_revenue_share=vm_revenue_share, cp_revenue_share=cp_revenue_share)
                    booking_in_db = session.query(CpBilling).filter(CpBilling.campaign_external_id==new_data.campaign_external_id, CpBilling.content_provider==new_data.content_provider).one_or_none()

                    if booking_in_db != None:
                        booking_in_db.delivered_impressions += new_data.delivered_impressions
                        booking_in_db.gross_revenue += new_data.gross_revenue
                        booking_in_db.net_revenue += net_revenue
                        booking_in_db.vm_revenue_share += vm_revenue_share
                        booking_in_db.cp_revenue_share += cp_revenue_share
                        session.commit()
                    else:
                        session.add(new_data)
                        session.commit()
            print('ALL ADDED')
            # print(session.query(CpBilling).all())
            data = session.query(CpBilling).all()
            download_csv(key)
            create_workbook(data, key)
            delete_table()
            print('ALL DELETED')
        delete_main_table()
    except TypeError:
        print(f'TYPEERROR: CP: {data.content_provider}, ID: {data.id}, Gross Revenue: {data.gross_revenue}, Net Revenue:{data.net_revenue}')


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


def download_csv(content_provider):
    """
    Generates a CSV file for each Content Provider group.

    """
    with open(f'csv/{content_provider}.csv', 'w') as csvfile:
        headers = ['Campaign External ID', 'Campaign Name', 'Content Provider', 'Delivered Impressions', 'CPM Rate', 'Gross Revenue', 'Net Revenue', 'VM Revenue Share', 'CP Revenue Share']
        backup = csv.DictWriter(csvfile, fieldnames=headers)
        backup.writeheader()

        for product in session.query(CpBilling).all():
            backup.writerow({'Campaign External ID': product.campaign_external_id, 'Content Provider': product.content_provider, 'Campaign Name': product.campaign_name, 'Delivered Impressions': product.delivered_impressions, 'CPM Rate': product.cpm_rate,
                'Gross Revenue': product.gross_revenue, 'Net Revenue': product.net_revenue, 'VM Revenue Share': product.vm_revenue_share,  'CP Revenue Share': product.cp_revenue_share})


def delete_table():
    """
    Delete the table each time a Content Group has sucessfully outputted a CSV and Excel file.
    Tables are deleted multiple times until all Content Provider Groups reports (CSV and Excel) are completed.

    """
    session.query(CpBilling).delete()
    session.commit()


def delete_main_table():
    """
    Delete the main table once all tasks are complete.

    """
    session.query(ContentProvider).delete()
    session.commit()


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    calculate()