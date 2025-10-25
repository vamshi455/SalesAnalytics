"""
Salesforce CRM Data Generator
Generates realistic synthetic Salesforce CRM data with proper relationships
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from faker import Faker
import os

# Initialize Faker
fake = Faker(['en_US'])
Faker.seed(42)
np.random.seed(42)
random.seed(42)

# Configuration
NUM_ACCOUNTS = 1000
NUM_CONTACTS_PER_ACCOUNT = 3
NUM_LEADS = 2000
NUM_CAMPAIGNS = 20
NUM_OPPORTUNITIES_PER_ACCOUNT = 2
NUM_CASES_PER_ACCOUNT = 5
NUM_QUOTES_PER_OPP = 1

# Get absolute paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'data', 'raw', 'crm')


class SalesforceCRMGenerator:
    """Generate synthetic Salesforce CRM data"""

    def __init__(self):
        self.accounts = None
        self.contacts = None
        self.leads = None
        self.campaigns = None
        self.opportunities = None
        self.opportunity_line_items = None
        self.cases = None
        self.activities = None
        self.quotes = None

    # ==================== ACCOUNT (COMPANY MASTER) ====================

    def generate_accounts(self):
        """Account - Company Master Data"""
        print("Generating Accounts (Company Master)...")

        accounts = []
        industries = ['Technology', 'Manufacturing', 'Financial Services', 'Healthcare',
                     'Retail', 'Energy', 'Telecommunications', 'Media', 'Transportation']

        account_types = ['Customer - Direct', 'Customer - Channel', 'Prospect',
                        'Partner', 'Competitor']

        for i in range(NUM_ACCOUNTS):
            created_date = datetime.now() - timedelta(days=random.randint(1, 1825))  # 0-5 years ago

            accounts.append({
                'Id': f'001{i+10000:08d}',  # Salesforce Account ID format
                'Name': fake.company(),
                'AccountNumber': f'ACC-{i+10000:06d}',
                'Type': np.random.choice(account_types, p=[0.4, 0.15, 0.2, 0.15, 0.1]),
                'Industry': np.random.choice(industries),
                'AnnualRevenue': round(np.random.lognormal(15, 2), 2),  # $1M - $100M range
                'NumberOfEmployees': int(np.random.lognormal(5, 2)),  # 10 - 10000 employees
                'BillingStreet': fake.street_address(),
                'BillingCity': fake.city(),
                'BillingState': fake.state_abbr(),
                'BillingPostalCode': fake.zipcode(),
                'BillingCountry': 'USA',
                'Phone': fake.phone_number(),
                'Website': f'www.{fake.domain_name()}',
                'Rating': np.random.choice(['Hot', 'Warm', 'Cold'], p=[0.2, 0.5, 0.3]),
                'OwnerId': f'005{np.random.randint(1, 20):04d}',  # Sales rep user ID
                'CreatedDate': created_date.strftime('%Y-%m-%d %H:%M:%S'),
                'LastModifiedDate': (created_date + timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d %H:%M:%S'),
                'IsDeleted': False,
            })

        self.accounts = pd.DataFrame(accounts)
        self.accounts.to_csv(f'{OUTPUT_DIR}/Account.csv', index=False)
        print(f"  ✓ Generated {len(self.accounts):,} accounts")
        return self.accounts

    # ==================== CONTACT (DECISION MAKERS) ====================

    def generate_contacts(self):
        """Contact - Decision Makers and Stakeholders"""
        print("Generating Contacts (Decision Makers)...")

        contacts = []
        titles = ['CEO', 'CFO', 'CTO', 'VP Sales', 'VP Marketing', 'VP Operations',
                 'Director IT', 'Director Finance', 'Manager Procurement', 'Senior Buyer']

        departments = ['Executive', 'Finance', 'IT', 'Sales', 'Marketing',
                      'Operations', 'Procurement', 'HR']

        for _, account in self.accounts.iterrows():
            # Each account has 1-5 contacts
            num_contacts = np.random.choice([1, 2, 3, 4, 5], p=[0.1, 0.3, 0.4, 0.15, 0.05])

            for j in range(num_contacts):
                first_name = fake.first_name()
                last_name = fake.last_name()
                created_date = datetime.strptime(account['CreatedDate'], '%Y-%m-%d %H:%M:%S') + timedelta(days=random.randint(0, 180))

                contacts.append({
                    'Id': f'003{len(contacts)+10000:08d}',
                    'AccountId': account['Id'],
                    'FirstName': first_name,
                    'LastName': last_name,
                    'Email': f'{first_name.lower()}.{last_name.lower()}@{account["Website"].replace("www.", "")}',
                    'Phone': fake.phone_number(),
                    'MobilePhone': fake.phone_number(),
                    'Title': np.random.choice(titles),
                    'Department': np.random.choice(departments),
                    'MailingStreet': account['BillingStreet'],
                    'MailingCity': account['BillingCity'],
                    'MailingState': account['BillingState'],
                    'MailingPostalCode': account['BillingPostalCode'],
                    'MailingCountry': account['BillingCountry'],
                    'LeadSource': np.random.choice(['Web', 'Phone Inquiry', 'Partner Referral',
                                                    'Purchased List', 'Trade Show', 'Event']),
                    'OwnerId': account['OwnerId'],
                    'CreatedDate': created_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'LastModifiedDate': (created_date + timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d %H:%M:%S'),
                    'IsDeleted': False,
                })

        self.contacts = pd.DataFrame(contacts)
        self.contacts.to_csv(f'{OUTPUT_DIR}/Contact.csv', index=False)
        print(f"  ✓ Generated {len(self.contacts):,} contacts")
        return self.contacts

    # ==================== LEAD (PROSPECTS) ====================

    def generate_leads(self):
        """Lead - Prospects not yet converted"""
        print("Generating Leads (Prospects)...")

        leads = []
        lead_sources = ['Web', 'Phone Inquiry', 'Partner Referral', 'Purchased List',
                       'Trade Show', 'Webinar', 'Social Media', 'Employee Referral']

        lead_statuses = ['Open - Not Contacted', 'Working - Contacted', 'Closed - Converted',
                        'Closed - Not Converted']

        industries = ['Technology', 'Manufacturing', 'Financial Services', 'Healthcare',
                     'Retail', 'Energy', 'Telecommunications']

        for i in range(NUM_LEADS):
            created_date = datetime.now() - timedelta(days=random.randint(1, 365))
            status = np.random.choice(lead_statuses, p=[0.2, 0.4, 0.25, 0.15])

            first_name = fake.first_name()
            last_name = fake.last_name()
            company = fake.company()

            # Converted leads have conversion date
            converted = status == 'Closed - Converted'
            conversion_date = (created_date + timedelta(days=random.randint(7, 90))).strftime('%Y-%m-%d') if converted else None

            leads.append({
                'Id': f'00Q{i+10000:08d}',
                'FirstName': first_name,
                'LastName': last_name,
                'Company': company,
                'Title': np.random.choice(['Manager', 'Director', 'VP', 'Senior Manager', 'Analyst']),
                'Email': f'{first_name.lower()}.{last_name.lower()}@{fake.domain_name()}',
                'Phone': fake.phone_number(),
                'Street': fake.street_address(),
                'City': fake.city(),
                'State': fake.state_abbr(),
                'PostalCode': fake.zipcode(),
                'Country': 'USA',
                'Industry': np.random.choice(industries),
                'LeadSource': np.random.choice(lead_sources),
                'Status': status,
                'Rating': np.random.choice(['Hot', 'Warm', 'Cold'], p=[0.15, 0.45, 0.4]),
                'NumberOfEmployees': int(np.random.lognormal(4, 2)),
                'AnnualRevenue': round(np.random.lognormal(14, 2), 2),
                'OwnerId': f'005{np.random.randint(1, 20):04d}',
                'IsConverted': converted,
                'ConvertedDate': conversion_date,
                'ConvertedAccountId': f'001{np.random.randint(10000, 10000+NUM_ACCOUNTS):08d}' if converted else None,
                'ConvertedContactId': None if not converted else f'003{np.random.randint(10000, 10000+3000):08d}',
                'ConvertedOpportunityId': None if not converted else f'006{np.random.randint(10000, 12000):08d}',
                'CreatedDate': created_date.strftime('%Y-%m-%d %H:%M:%S'),
                'LastModifiedDate': (created_date + timedelta(days=random.randint(1, 180))).strftime('%Y-%m-%d %H:%M:%S'),
                'IsDeleted': False,
            })

        self.leads = pd.DataFrame(leads)
        self.leads.to_csv(f'{OUTPUT_DIR}/Lead.csv', index=False)
        print(f"  ✓ Generated {len(self.leads):,} leads")
        return self.leads

    # ==================== CAMPAIGN (MARKETING) ====================

    def generate_campaigns(self):
        """Campaign - Marketing Campaigns"""
        print("Generating Campaigns (Marketing)...")

        campaigns = []
        campaign_types = ['Email', 'Webinar', 'Conference', 'Trade Show', 'Direct Mail',
                         'Social Media', 'Content Marketing', 'PPC']

        statuses = ['Planned', 'In Progress', 'Completed', 'Aborted']

        for i in range(NUM_CAMPAIGNS):
            start_date = datetime.now() - timedelta(days=random.randint(30, 730))
            end_date = start_date + timedelta(days=random.randint(7, 90))
            status = np.random.choice(statuses, p=[0.1, 0.2, 0.6, 0.1])

            budget = round(np.random.uniform(5000, 200000), 2)
            actual_cost = round(budget * np.random.uniform(0.7, 1.2), 2) if status == 'Completed' else 0

            num_sent = int(np.random.uniform(500, 50000)) if status in ['Completed', 'In Progress'] else 0
            num_responses = int(num_sent * np.random.uniform(0.02, 0.15)) if num_sent > 0 else 0
            num_leads = int(num_responses * np.random.uniform(0.3, 0.7)) if num_responses > 0 else 0
            num_converted = int(num_leads * np.random.uniform(0.1, 0.4)) if num_leads > 0 else 0

            campaigns.append({
                'Id': f'701{i+1000:05d}',
                'Name': f'{np.random.choice(["Q1", "Q2", "Q3", "Q4"])} {np.random.choice(["2024", "2025"])} - {np.random.choice(["Product Launch", "Lead Gen", "Awareness", "Customer Retention"])}',
                'Type': np.random.choice(campaign_types),
                'Status': status,
                'StartDate': start_date.strftime('%Y-%m-%d'),
                'EndDate': end_date.strftime('%Y-%m-%d'),
                'BudgetedCost': budget,
                'ActualCost': actual_cost,
                'ExpectedRevenue': round(budget * np.random.uniform(3, 10), 2),
                'ExpectedResponse': round(np.random.uniform(2, 15), 2),  # Percentage
                'NumberSent': num_sent,
                'NumberOfResponses': num_responses,
                'NumberOfLeads': num_leads,
                'NumberOfConvertedLeads': num_converted,
                'NumberOfOpportunities': int(num_converted * np.random.uniform(0.6, 0.9)),
                'IsActive': status in ['Planned', 'In Progress'],
                'Description': fake.text(max_nb_chars=200),
                'OwnerId': f'005{np.random.randint(1, 20):04d}',
                'CreatedDate': (start_date - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S'),
                'IsDeleted': False,
            })

        self.campaigns = pd.DataFrame(campaigns)
        self.campaigns.to_csv(f'{OUTPUT_DIR}/Campaign.csv', index=False)
        print(f"  ✓ Generated {len(self.campaigns):,} campaigns")
        return self.campaigns

    # ==================== OPPORTUNITY (PIPELINE) ====================

    def generate_opportunities(self):
        """Opportunity - Sales Pipeline"""
        print("Generating Opportunities (Pipeline)...")

        opportunities = []
        stages = ['Prospecting', 'Qualification', 'Needs Analysis', 'Value Proposition',
                 'Proposal/Price Quote', 'Negotiation/Review', 'Closed Won', 'Closed Lost']

        stage_probabilities = [5, 10, 20, 40, 60, 80, 100, 0]

        lead_sources = ['Web', 'Phone Inquiry', 'Partner Referral', 'Purchased List',
                       'Trade Show', 'Campaign']

        opp_types = ['New Business', 'Existing Customer - Upgrade', 'Existing Customer - Replacement',
                    'Existing Customer - Downgrade']

        for _, account in self.accounts.iterrows():
            # Each account has 0-3 opportunities
            num_opps = np.random.choice([0, 1, 2, 3], p=[0.3, 0.4, 0.2, 0.1])

            for j in range(num_opps):
                created_date = datetime.strptime(account['CreatedDate'], '%Y-%m-%d %H:%M:%S') + timedelta(days=random.randint(30, 365))
                stage = np.random.choice(stages, p=[0.1, 0.15, 0.15, 0.15, 0.15, 0.1, 0.15, 0.05])

                stage_idx = stages.index(stage)
                probability = stage_probabilities[stage_idx]

                close_date = created_date + timedelta(days=random.randint(30, 180))
                is_closed = stage in ['Closed Won', 'Closed Lost']
                is_won = stage == 'Closed Won'

                amount = round(np.random.lognormal(11, 1.5), 2)  # $10K - $1M

                opportunities.append({
                    'Id': f'006{len(opportunities)+10000:08d}',
                    'AccountId': account['Id'],
                    'Name': f'{account["Name"]} - {np.random.choice(["Q1", "Q2", "Q3", "Q4"])} {np.random.choice(["2024", "2025"])}',
                    'StageName': stage,
                    'Probability': probability,
                    'Amount': amount,
                    'CloseDate': close_date.strftime('%Y-%m-%d'),
                    'Type': np.random.choice(opp_types, p=[0.5, 0.25, 0.15, 0.1]),
                    'LeadSource': np.random.choice(lead_sources),
                    'NextStep': fake.sentence() if not is_closed else None,
                    'IsClosed': is_closed,
                    'IsWon': is_won,
                    'ForecastCategory': 'Closed' if is_closed else ('Commit' if probability >= 70 else ('Best Case' if probability >= 50 else 'Pipeline')),
                    'ForecastCategoryName': 'Closed' if is_closed else ('Commit' if probability >= 70 else ('Best Case' if probability >= 50 else 'Omitted')),
                    'CampaignId': self.campaigns.sample(1)['Id'].values[0] if np.random.random() < 0.3 else None,
                    'HasOpportunityLineItem': True,
                    'OwnerId': account['OwnerId'],
                    'CreatedDate': created_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'LastModifiedDate': (created_date + timedelta(days=random.randint(1, 90))).strftime('%Y-%m-%d %H:%M:%S'),
                    'IsDeleted': False,
                })

        self.opportunities = pd.DataFrame(opportunities)
        self.opportunities.to_csv(f'{OUTPUT_DIR}/Opportunity.csv', index=False)
        print(f"  ✓ Generated {len(self.opportunities):,} opportunities")
        return self.opportunities

    # ==================== OPPORTUNITY LINE ITEM (PRODUCTS) ====================

    def generate_opportunity_line_items(self):
        """OpportunityLineItem - Products in Opportunities"""
        print("Generating Opportunity Line Items (Products)...")

        line_items = []

        # Sample product catalog
        products = [
            {'Id': 'P001', 'Name': 'Enterprise Software License', 'UnitPrice': 50000, 'ProductCode': 'SW-ENT-001'},
            {'Id': 'P002', 'Name': 'Professional Services - Implementation', 'UnitPrice': 25000, 'ProductCode': 'PS-IMP-001'},
            {'Id': 'P003', 'Name': 'Annual Support & Maintenance', 'UnitPrice': 10000, 'ProductCode': 'SUP-ANN-001'},
            {'Id': 'P004', 'Name': 'Training Package - 10 Users', 'UnitPrice': 5000, 'ProductCode': 'TRN-PKG-010'},
            {'Id': 'P005', 'Name': 'Hardware Appliance - Standard', 'UnitPrice': 15000, 'ProductCode': 'HW-APP-STD'},
            {'Id': 'P006', 'Name': 'Cloud Subscription - Monthly', 'UnitPrice': 2000, 'ProductCode': 'CLD-SUB-MTH'},
            {'Id': 'P007', 'Name': 'Consulting Services - Daily Rate', 'UnitPrice': 2500, 'ProductCode': 'CON-SVC-DAY'},
            {'Id': 'P008', 'Name': 'Data Migration Services', 'UnitPrice': 30000, 'ProductCode': 'PS-MIG-001'},
        ]

        for _, opp in self.opportunities.iterrows():
            # Each opportunity has 1-5 products
            num_items = np.random.choice([1, 2, 3, 4, 5], p=[0.3, 0.35, 0.2, 0.1, 0.05])
            selected_products = np.random.choice(products, size=min(num_items, len(products)), replace=False)

            for idx, product in enumerate(selected_products):
                quantity = np.random.choice([1, 2, 3, 5, 10, 20, 50, 100], p=[0.3, 0.2, 0.15, 0.1, 0.1, 0.05, 0.05, 0.05])
                list_price = product['UnitPrice']
                discount = round(np.random.uniform(0, 25), 2) if np.random.random() < 0.5 else 0
                unit_price = list_price * (1 - discount/100)
                total_price = round(quantity * unit_price, 2)

                line_items.append({
                    'Id': f'00k{len(line_items)+10000:08d}',
                    'OpportunityId': opp['Id'],
                    'Product2Id': product['Id'],
                    'ProductCode': product['ProductCode'],
                    'Name': product['Name'],
                    'Quantity': quantity,
                    'ListPrice': list_price,
                    'UnitPrice': round(unit_price, 2),
                    'Discount': discount,
                    'TotalPrice': total_price,
                    'Description': fake.text(max_nb_chars=100),
                    'ServiceDate': opp['CloseDate'],
                    'CreatedDate': opp['CreatedDate'],
                    'LastModifiedDate': opp['LastModifiedDate'],
                    'IsDeleted': False,
                })

        self.opportunity_line_items = pd.DataFrame(line_items)
        self.opportunity_line_items.to_csv(f'{OUTPUT_DIR}/OpportunityLineItem.csv', index=False)
        print(f"  ✓ Generated {len(self.opportunity_line_items):,} opportunity line items")
        return self.opportunity_line_items

    # ==================== CASE (SUPPORT TICKETS) ====================

    def generate_cases(self):
        """Case - Support Tickets"""
        print("Generating Cases (Support Tickets)...")

        cases = []
        case_types = ['Problem', 'Question', 'Feature Request', 'Bug Report', 'Configuration']
        statuses = ['New', 'Working', 'Escalated', 'Closed']
        priorities = ['Low', 'Medium', 'High', 'Critical']
        origins = ['Web', 'Phone', 'Email', 'Chat', 'Portal']

        for _, account in self.accounts.iterrows():
            # Only customer accounts have cases
            if 'Customer' not in account['Type']:
                continue

            # Each customer has 0-10 cases
            num_cases = np.random.choice([0, 1, 2, 3, 5, 10], p=[0.2, 0.3, 0.25, 0.15, 0.07, 0.03])

            # Get contacts for this account
            account_contacts = self.contacts[self.contacts['AccountId'] == account['Id']]

            for j in range(num_cases):
                created_date = datetime.now() - timedelta(days=random.randint(1, 730))
                status = np.random.choice(statuses, p=[0.15, 0.25, 0.1, 0.5])
                priority = np.random.choice(priorities, p=[0.4, 0.35, 0.2, 0.05])

                is_closed = status == 'Closed'
                closed_date = (created_date + timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d %H:%M:%S') if is_closed else None

                contact = account_contacts.sample(1).iloc[0] if len(account_contacts) > 0 else None

                cases.append({
                    'Id': f'500{len(cases)+10000:08d}',
                    'CaseNumber': f'CS-{len(cases)+100000:06d}',
                    'AccountId': account['Id'],
                    'ContactId': contact['Id'] if contact is not None else None,
                    'Status': status,
                    'Priority': priority,
                    'Type': np.random.choice(case_types),
                    'Origin': np.random.choice(origins),
                    'Subject': fake.sentence(nb_words=6),
                    'Description': fake.text(max_nb_chars=300),
                    'IsClosed': is_closed,
                    'IsEscalated': status == 'Escalated',
                    'ClosedDate': closed_date,
                    'OwnerId': f'005{np.random.randint(21, 40):04d}',  # Support rep
                    'CreatedDate': created_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'LastModifiedDate': (created_date + timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d %H:%M:%S'),
                    'IsDeleted': False,
                })

        self.cases = pd.DataFrame(cases)
        self.cases.to_csv(f'{OUTPUT_DIR}/Case.csv', index=False)
        print(f"  ✓ Generated {len(self.cases):,} cases")
        return self.cases

    # ==================== ACTIVITY (ENGAGEMENT) ====================

    def generate_activities(self):
        """Activity - Tasks and Events (Engagement)"""
        print("Generating Activities (Engagement)...")

        activities = []
        task_types = ['Call', 'Email', 'Meeting', 'Demo', 'Follow-up', 'Send Quote']
        statuses = ['Not Started', 'In Progress', 'Completed', 'Deferred']
        priorities = ['Low', 'Normal', 'High']

        # Generate activities for opportunities
        for _, opp in self.opportunities.iterrows():
            # Each opportunity has 3-10 activities
            num_activities = np.random.choice([3, 5, 7, 10], p=[0.3, 0.4, 0.2, 0.1])

            base_date = datetime.strptime(opp['CreatedDate'], '%Y-%m-%d %H:%M:%S')

            for j in range(num_activities):
                activity_date = base_date + timedelta(days=random.randint(0, 90))
                status = np.random.choice(statuses, p=[0.1, 0.15, 0.7, 0.05])

                activities.append({
                    'Id': f'00T{len(activities)+10000:08d}',
                    'WhoId': None,  # Contact or Lead
                    'WhatId': opp['Id'],  # Related to Opportunity
                    'Subject': np.random.choice(task_types),
                    'ActivityDate': activity_date.strftime('%Y-%m-%d'),
                    'Status': status,
                    'Priority': np.random.choice(priorities, p=[0.3, 0.5, 0.2]),
                    'Description': fake.sentence(),
                    'IsClosed': status == 'Completed',
                    'OwnerId': opp['OwnerId'],
                    'CreatedDate': activity_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'LastModifiedDate': (activity_date + timedelta(days=random.randint(0, 5))).strftime('%Y-%m-%d %H:%M:%S'),
                    'IsDeleted': False,
                })

        self.activities = pd.DataFrame(activities)
        self.activities.to_csv(f'{OUTPUT_DIR}/Activity.csv', index=False)
        print(f"  ✓ Generated {len(self.activities):,} activities")
        return self.activities

    # ==================== QUOTE (CPQ QUOTES) ====================

    def generate_quotes(self):
        """Quote - CPQ Quotes"""
        print("Generating Quotes (CPQ)...")

        quotes = []
        quote_statuses = ['Draft', 'In Review', 'Approved', 'Rejected', 'Presented to Customer', 'Accepted', 'Denied']

        for _, opp in self.opportunities.iterrows():
            # Opportunities in later stages have quotes
            if opp['Probability'] < 20:
                continue

            # Each qualified opportunity has 1-2 quotes
            num_quotes = np.random.choice([1, 2], p=[0.7, 0.3])

            for j in range(num_quotes):
                created_date = datetime.strptime(opp['CreatedDate'], '%Y-%m-%d %H:%M:%S') + timedelta(days=random.randint(14, 60))

                # Quote status based on opportunity status
                if opp['StageName'] == 'Closed Won':
                    status = 'Accepted'
                elif opp['StageName'] == 'Closed Lost':
                    status = np.random.choice(['Rejected', 'Denied'])
                else:
                    status = np.random.choice(quote_statuses[:5], p=[0.1, 0.2, 0.3, 0.2, 0.2])

                # Calculate quote total (similar to opportunity amount with variance)
                subtotal = opp['Amount'] * np.random.uniform(0.9, 1.1)
                discount = round(subtotal * np.random.uniform(0, 0.15), 2)
                tax = round((subtotal - discount) * 0.08, 2)
                total_price = round(subtotal - discount + tax, 2)

                expiration_date = created_date + timedelta(days=30)

                quotes.append({
                    'Id': f'0Q0{len(quotes)+10000:08d}',
                    'QuoteNumber': f'QT-{len(quotes)+100000:06d}',
                    'OpportunityId': opp['Id'],
                    'AccountId': opp['AccountId'],
                    'Name': f'Quote for {opp["Name"]}',
                    'Status': status,
                    'ExpirationDate': expiration_date.strftime('%Y-%m-%d'),
                    'Subtotal': round(subtotal, 2),
                    'Discount': discount,
                    'TotalPrice': total_price,
                    'Tax': tax,
                    'GrandTotal': total_price,
                    'ShippingHandling': round(np.random.uniform(0, 500), 2),
                    'Description': fake.text(max_nb_chars=200),
                    'IsSyncing': False,
                    'OwnerId': opp['OwnerId'],
                    'CreatedDate': created_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'LastModifiedDate': (created_date + timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d %H:%M:%S'),
                    'IsDeleted': False,
                })

        self.quotes = pd.DataFrame(quotes)
        self.quotes.to_csv(f'{OUTPUT_DIR}/Quote.csv', index=False)
        print(f"  ✓ Generated {len(self.quotes):,} quotes")
        return self.quotes

    def print_summary(self):
        """Print generation summary"""
        print("\n" + "="*80)
        print("SALESFORCE CRM DATA GENERATION SUMMARY")
        print("="*80)
        print(f"\nGenerated Records:")
        print(f"  Accounts (Company Master):     {len(self.accounts):,}")
        print(f"  Contacts (Decision Makers):    {len(self.contacts):,}")
        print(f"  Leads (Prospects):             {len(self.leads):,}")
        print(f"  Campaigns (Marketing):         {len(self.campaigns):,}")
        print(f"  Opportunities (Pipeline):      {len(self.opportunities):,}")
        print(f"  Opportunity Line Items:        {len(self.opportunity_line_items):,}")
        print(f"  Cases (Support Tickets):       {len(self.cases):,}")
        print(f"  Activities (Engagement):       {len(self.activities):,}")
        print(f"  Quotes (CPQ):                  {len(self.quotes):,}")
        print(f"\n  TOTAL RECORDS:                 {len(self.accounts) + len(self.contacts) + len(self.leads) + len(self.campaigns) + len(self.opportunities) + len(self.opportunity_line_items) + len(self.cases) + len(self.activities) + len(self.quotes):,}")
        print(f"\nAll CSV files saved to: {OUTPUT_DIR}/")
        print("="*80)


def main():
    """Main execution"""
    print("="*80)
    print("SALESFORCE CRM SYNTHETIC DATA GENERATOR")
    print("="*80)
    print(f"Generation Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    generator = SalesforceCRMGenerator()

    # Generate all CRM data in sequence (maintains referential integrity)
    generator.generate_accounts()
    generator.generate_contacts()
    generator.generate_leads()
    generator.generate_campaigns()
    generator.generate_opportunities()
    generator.generate_opportunity_line_items()
    generator.generate_cases()
    generator.generate_activities()
    generator.generate_quotes()

    generator.print_summary()


if __name__ == "__main__":
    main()
