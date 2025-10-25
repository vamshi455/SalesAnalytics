"""
Create Cross-Reference Links between CRM and SAP Data
Establishes master data matching and transaction linkages
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
SAP_DIR = os.path.join(PROJECT_ROOT, 'data', 'raw', 'sap')
CRM_DIR = os.path.join(PROJECT_ROOT, 'data', 'raw', 'crm')
XREF_DIR = os.path.join(PROJECT_ROOT, 'data', 'raw', 'cross_reference')

# Create cross-reference directory
os.makedirs(XREF_DIR, exist_ok=True)


class CRMSAPLinker:
    """Create linkages between CRM and SAP data"""

    def __init__(self):
        self.account_customer_xref = None
        self.opportunity_order_xref = None
        self.contact_partner_xref = None
        self.quote_order_xref = None

    def create_account_customer_link(self):
        """Link CRM Account to SAP Customer (KNA1)"""
        print("Creating Account ↔ Customer Master Link...")

        # Load data
        accounts = pd.read_csv(f'{CRM_DIR}/Account.csv')
        kna1 = pd.read_csv(f'{SAP_DIR}/master/customer/KNA1.csv')

        # Filter only Customer accounts in CRM
        customer_accounts = accounts[accounts['Type'].str.contains('Customer', na=False)]

        # Create cross-reference
        xref = []

        # Map first N CRM customers to SAP customers
        num_links = min(len(customer_accounts), len(kna1))

        for i in range(num_links):
            crm_account = customer_accounts.iloc[i]
            sap_customer = kna1.iloc[i]

            xref.append({
                'CRM_AccountId': crm_account['Id'],
                'CRM_AccountNumber': crm_account['AccountNumber'],
                'CRM_AccountName': crm_account['Name'],
                'SAP_KUNNR': sap_customer['KUNNR'],
                'SAP_NAME1': sap_customer['NAME1'],
                'SAP_LAND1': sap_customer['LAND1'],
                'MatchType': 'Direct_Master_Match',
                'MatchConfidence': 100,
                'CreatedDate': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'DataSource': 'Synthetic_Generated'
            })

        self.account_customer_xref = pd.DataFrame(xref)
        self.account_customer_xref.to_csv(f'{XREF_DIR}/Account_Customer_XREF.csv', index=False)
        print(f"  ✓ Created {len(self.account_customer_xref):,} Account-Customer links")
        return self.account_customer_xref

    def create_opportunity_order_link(self):
        """Link CRM Closed Won Opportunities to SAP Sales Orders"""
        print("Creating Opportunity ↔ Sales Order Link...")

        # Load data
        opportunities = pd.read_csv(f'{CRM_DIR}/Opportunity.csv')
        vbak = pd.read_csv(f'{SAP_DIR}/transactional/sales_orders/VBAK.csv')
        account_xref = self.account_customer_xref

        # Filter Closed Won opportunities only
        closed_won_opps = opportunities[opportunities['StageName'] == 'Closed Won'].copy()

        # Merge with account cross-reference to get SAP customer
        closed_won_opps = closed_won_opps.merge(
            account_xref[['CRM_AccountId', 'SAP_KUNNR']],
            left_on='AccountId',
            right_on='CRM_AccountId',
            how='left'
        )

        xref = []
        vbak_used = set()

        for _, opp in closed_won_opps.iterrows():
            # Find matching SAP order
            # Match criteria: Same customer, order date after opportunity created date
            if pd.isna(opp.get('SAP_KUNNR')):
                continue

            opp_close_date = datetime.strptime(opp['CloseDate'], '%Y-%m-%d')

            # Find SAP orders for this customer created around close date
            customer_orders = vbak[
                (vbak['KUNNR'] == opp['SAP_KUNNR']) &
                (~vbak['VBELN'].isin(vbak_used))
            ]

            if len(customer_orders) == 0:
                continue

            # Take first available order for this customer
            sap_order = customer_orders.iloc[0]
            vbak_used.add(sap_order['VBELN'])

            xref.append({
                'CRM_OpportunityId': opp['Id'],
                'CRM_OpportunityName': opp['Name'],
                'CRM_Amount': opp['Amount'],
                'CRM_CloseDate': opp['CloseDate'],
                'CRM_AccountId': opp['AccountId'],
                'SAP_VBELN': sap_order['VBELN'],
                'SAP_NETWR': sap_order['NETWR'],
                'SAP_WAERK': sap_order['WAERK'],
                'SAP_ERDAT': sap_order['ERDAT'],
                'SAP_KUNNR': sap_order['KUNNR'],
                'LinkType': 'Opportunity_to_Order',
                'AmountVariance': float(opp['Amount']) - float(sap_order['NETWR']),
                'DaysFromCloseToOrder': (datetime.strptime(str(sap_order['ERDAT']), '%Y%m%d') - opp_close_date).days,
                'CreatedDate': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            })

        self.opportunity_order_xref = pd.DataFrame(xref)
        self.opportunity_order_xref.to_csv(f'{XREF_DIR}/Opportunity_Order_XREF.csv', index=False)
        print(f"  ✓ Created {len(self.opportunity_order_xref):,} Opportunity-Order links")
        print(f"  ✓ Closed Won Opportunities: {len(closed_won_opps):,}")
        print(f"  ✓ Linked to SAP Orders: {len(self.opportunity_order_xref):,}")
        print(f"  ✓ Unlinked Opportunities: {len(closed_won_opps) - len(self.opportunity_order_xref):,}")
        return self.opportunity_order_xref

    def create_contact_partner_link(self):
        """Link CRM Contacts to SAP Customer Partners (KNVP)"""
        print("Creating Contact ↔ Partner Function Link...")

        # Load data
        contacts = pd.read_csv(f'{CRM_DIR}/Contact.csv')
        knvp = pd.read_csv(f'{SAP_DIR}/master/customer/KNVP.csv')
        account_xref = self.account_customer_xref

        # Merge contacts with account cross-reference
        contacts_with_sap = contacts.merge(
            account_xref[['CRM_AccountId', 'SAP_KUNNR']],
            left_on='AccountId',
            right_on='CRM_AccountId',
            how='left'
        )

        xref = []

        for _, contact in contacts_with_sap.iterrows():
            if pd.isna(contact.get('SAP_KUNNR')):
                continue

            # Find partner functions for this customer
            customer_partners = knvp[knvp['KUNNR'] == contact['SAP_KUNNR']]

            if len(customer_partners) == 0:
                continue

            # Map contact to AG (Sold-to) partner by default
            sold_to_partner = customer_partners[customer_partners['PARVW'] == 'AG']

            if len(sold_to_partner) > 0:
                partner = sold_to_partner.iloc[0]

                xref.append({
                    'CRM_ContactId': contact['Id'],
                    'CRM_FirstName': contact['FirstName'],
                    'CRM_LastName': contact['LastName'],
                    'CRM_Email': contact['Email'],
                    'CRM_Title': contact['Title'],
                    'CRM_AccountId': contact['AccountId'],
                    'SAP_KUNNR': partner['KUNNR'],
                    'SAP_VKORG': partner['VKORG'],
                    'SAP_VTWEG': partner['VTWEG'],
                    'SAP_SPART': partner['SPART'],
                    'SAP_PARVW': partner['PARVW'],
                    'SAP_KUNN2': partner['KUNN2'],
                    'PartnerFunction': 'Sold-to Party',
                    'CreatedDate': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                })

        self.contact_partner_xref = pd.DataFrame(xref)
        self.contact_partner_xref.to_csv(f'{XREF_DIR}/Contact_Partner_XREF.csv', index=False)
        print(f"  ✓ Created {len(self.contact_partner_xref):,} Contact-Partner links")
        return self.contact_partner_xref

    def create_quote_order_link(self):
        """Link CRM Accepted Quotes to SAP Sales Orders"""
        print("Creating Quote ↔ Sales Order Link...")

        # Load data
        quotes = pd.read_csv(f'{CRM_DIR}/Quote.csv')
        opportunities = pd.read_csv(f'{CRM_DIR}/Opportunity.csv')

        # Use existing opportunity-order link
        opp_order_xref = self.opportunity_order_xref

        # Filter accepted quotes
        accepted_quotes = quotes[quotes['Status'] == 'Accepted']

        # Link through opportunities
        quote_links = accepted_quotes.merge(
            opp_order_xref[['CRM_OpportunityId', 'SAP_VBELN', 'SAP_NETWR']],
            left_on='OpportunityId',
            right_on='CRM_OpportunityId',
            how='left'
        )

        xref = []

        for _, quote in quote_links.iterrows():
            if pd.isna(quote.get('SAP_VBELN')):
                continue

            xref.append({
                'CRM_QuoteId': quote['Id'],
                'CRM_QuoteNumber': quote['QuoteNumber'],
                'CRM_OpportunityId': quote['OpportunityId'],
                'CRM_TotalPrice': quote['TotalPrice'],
                'CRM_Status': quote['Status'],
                'SAP_VBELN': quote['SAP_VBELN'],
                'SAP_NETWR': quote['SAP_NETWR'],
                'LinkType': 'Quote_to_Order',
                'AmountVariance': float(quote['TotalPrice']) - float(quote['SAP_NETWR']),
                'CreatedDate': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            })

        self.quote_order_xref = pd.DataFrame(xref)
        self.quote_order_xref.to_csv(f'{XREF_DIR}/Quote_Order_XREF.csv', index=False)
        print(f"  ✓ Created {len(self.quote_order_xref):,} Quote-Order links")
        print(f"  ✓ Accepted Quotes: {len(accepted_quotes):,}")
        print(f"  ✓ Linked to SAP Orders: {len(self.quote_order_xref):,}")
        return self.quote_order_xref

    def create_analytics_views(self):
        """Create denormalized analytical views combining CRM and SAP"""
        print("\nCreating Analytical Views...")

        # View 1: Customer 360 View
        print("  Creating Customer 360 View...")

        accounts = pd.read_csv(f'{CRM_DIR}/Account.csv')
        kna1 = pd.read_csv(f'{SAP_DIR}/master/customer/KNA1.csv')
        vbak = pd.read_csv(f'{SAP_DIR}/transactional/sales_orders/VBAK.csv')

        customer_360 = self.account_customer_xref.merge(
            accounts, left_on='CRM_AccountId', right_on='Id', how='left'
        )

        # Add order statistics from SAP
        order_stats = vbak.groupby('KUNNR').agg({
            'VBELN': 'count',
            'NETWR': 'sum',
            'ERDAT': ['min', 'max']
        }).reset_index()
        order_stats.columns = ['SAP_KUNNR', 'TotalOrders', 'TotalRevenue', 'FirstOrderDate', 'LastOrderDate']

        customer_360 = customer_360.merge(order_stats, on='SAP_KUNNR', how='left')
        customer_360.to_csv(f'{XREF_DIR}/Customer_360_View.csv', index=False)
        print(f"    ✓ Customer 360 View: {len(customer_360):,} records")

        # View 2: Opportunity to Order Analysis
        print("  Creating Opportunity-to-Order Analysis View...")

        opp_order_view = self.opportunity_order_xref.copy()
        opp_order_view['AmountMatch'] = (abs(opp_order_view['AmountVariance']) / opp_order_view['CRM_Amount'] * 100 < 10)
        opp_order_view['TimelyClosure'] = opp_order_view['DaysFromCloseToOrder'].between(-30, 30)

        opp_order_view.to_csv(f'{XREF_DIR}/Opportunity_Order_Analysis.csv', index=False)
        print(f"    ✓ Opportunity-Order Analysis: {len(opp_order_view):,} records")

        # View 3: Quote-to-Cash Cycle
        print("  Creating Quote-to-Cash Cycle View...")

        quotes = pd.read_csv(f'{CRM_DIR}/Quote.csv')
        vbrk = pd.read_csv(f'{SAP_DIR}/transactional/billing/VBRK.csv')

        quote_cash = self.quote_order_xref.merge(
            quotes[['Id', 'QuoteNumber', 'OpportunityId', 'CreatedDate', 'ExpirationDate']],
            left_on='CRM_QuoteId',
            right_on='Id',
            how='left'
        )

        # Add billing info
        billing_by_order = vbrk.groupby('KUNAG').agg({
            'VBELN': 'count',
            'NETWR': 'sum',
            'FKDAT': 'max'
        }).reset_index()

        quote_cash.to_csv(f'{XREF_DIR}/Quote_to_Cash_View.csv', index=False)
        print(f"    ✓ Quote-to-Cash View: {len(quote_cash):,} records")

    def generate_summary(self):
        """Generate summary statistics"""
        print("\n" + "="*80)
        print("CRM-SAP CROSS-REFERENCE SUMMARY")
        print("="*80)

        print(f"\nCross-Reference Tables Created:")
        print(f"  Account ↔ Customer Master:     {len(self.account_customer_xref):,} links")
        print(f"  Opportunity ↔ Sales Order:     {len(self.opportunity_order_xref):,} links")
        print(f"  Contact ↔ Partner Function:    {len(self.contact_partner_xref):,} links")
        print(f"  Quote ↔ Sales Order:           {len(self.quote_order_xref):,} links")

        print(f"\nData Quality Metrics:")

        # Opportunity matching rate
        opportunities = pd.read_csv(f'{CRM_DIR}/Opportunity.csv')
        closed_won = len(opportunities[opportunities['StageName'] == 'Closed Won'])
        if closed_won > 0:
            match_rate = len(self.opportunity_order_xref) / closed_won * 100
            print(f"  Closed Won Opportunity Match Rate: {match_rate:.1f}%")

        # Quote matching rate
        quotes = pd.read_csv(f'{CRM_DIR}/Quote.csv')
        accepted_quotes = len(quotes[quotes['Status'] == 'Accepted'])
        if accepted_quotes > 0:
            quote_match_rate = len(self.quote_order_xref) / accepted_quotes * 100
            print(f"  Accepted Quote Match Rate:      {quote_match_rate:.1f}%")

        # Amount variance analysis
        if len(self.opportunity_order_xref) > 0:
            avg_variance = self.opportunity_order_xref['AmountVariance'].abs().mean()
            print(f"  Average Amount Variance:        ${avg_variance:,.2f}")

        print(f"\nFiles Created:")
        print(f"  {XREF_DIR}/Account_Customer_XREF.csv")
        print(f"  {XREF_DIR}/Opportunity_Order_XREF.csv")
        print(f"  {XREF_DIR}/Contact_Partner_XREF.csv")
        print(f"  {XREF_DIR}/Quote_Order_XREF.csv")
        print(f"  {XREF_DIR}/Customer_360_View.csv")
        print(f"  {XREF_DIR}/Opportunity_Order_Analysis.csv")
        print(f"  {XREF_DIR}/Quote_to_Cash_View.csv")

        print("\n" + "="*80)
        print("Cross-reference linking completed successfully!")
        print("="*80)


def main():
    """Main execution"""
    print("="*80)
    print("CRM-SAP CROSS-REFERENCE GENERATOR")
    print("="*80)
    print(f"Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    linker = CRMSAPLinker()

    # Create all cross-references
    linker.create_account_customer_link()
    linker.create_opportunity_order_link()
    linker.create_contact_partner_link()
    linker.create_quote_order_link()

    # Create analytical views
    linker.create_analytics_views()

    # Generate summary
    linker.generate_summary()


if __name__ == "__main__":
    main()
