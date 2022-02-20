from app import *
from models import *

import csv

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
