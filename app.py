#Internal Import
import datetime
from models import *
from content_providers import *
from excel_export import *

#External Import
import csv
import argparse
import pathlib


parser = argparse.ArgumentParser(description='Uploads the CSV, process it.')
parser.add_argument('source_file', metavar='source_file', type=pathlib.Path, help='Upload the CSV file.')

args = parser.parse_args()

csv_upload = args.source_file

# today = datetime.date.today()
# first = today.replace(day=1)
# last_month = first - datetime.timedelta(days=1)

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
                    if value == 0.1:
                        cp_revenue_share = 0
                    else:
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
            data = session.query(CpBilling).all()
            download_csv(key)
            create_workbook(data, key)
            delete_table()
        delete_main_table()
    except TypeError:
        print(f'TYPEERROR: CP: {data.content_provider}, ID: {data.id}, Gross Revenue: {data.gross_revenue}, Net Revenue:{data.net_revenue}')


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