from ast import In
from sqlalchemy import create_engine, Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///cp_billing.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class ContentProvider(Base):
    __tablename__ = 'contentprovider'

    id = Column(Integer, primary_key=True)
    campaign_external_id = Column('Campaign External ID', String)
    campaign_name = Column('Campaign Name', String)
    content_provider = Column('Content Provider', String)
    delivered_impressions = Column('Delivered Impressions', Integer)
    cpm_rate = Column('CPM Rate', Integer)
    gross_revenue = Column('Gross Revenue', Integer)
    net_revenue = Column('Net Revenue', Integer)

    def __repr__(self):
        return f'<ContentProvider(Campaign External ID={self.campaign_external_id}, campaign_name={self.campaign_name}, Content Provider={self.content_provider}, Delivered Impressions={self.delivered_impressions}, CPM Rate={self.cpm_rate}, Gross Revenue={self.gross_revenue}, Net Revenue={self.net_revenue}>'


class CpBilling(Base):
    __tablename__ = 'cpbilling'

    id = Column(Integer, primary_key=True)
    campaign_external_id = Column('Campaign External ID', String)
    campaign_name = Column('Campaign Name', String)
    content_provider = Column('Content Provider', String)
    delivered_impressions = Column('Delivered Impressions', Integer)
    cpm_rate = Column('CPM Rate', Float)
    gross_revenue = Column('Gross Revenue', Float)
    net_revenue = Column('Net Revenue', Float)
    vm_revenue_share = Column('VM Revenue Share', Float)
    cp_revenue_share = Column('CP Revenue Share', Float)

    def __repr__(self):
        return f'<CpBilling(Campaign External ID={self.campaign_external_id}, Campaign Name={self.campaign_name}, Content Provider={self.content_provider}, Delivered Impressions={self.delivered_impressions}, CPM Rate={self.cpm_rate}, Gross Revenue={self.gross_revenue}, Net Revenue={self.net_revenue}, VM Revenue Share={self.vm_revenue_share}, CP Revenue Share={self.cp_revenue_share})>'

