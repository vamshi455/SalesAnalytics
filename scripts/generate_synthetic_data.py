"""
SAP SD Sales Analytics - Synthetic Data Generator
Generates realistic synthetic data for all SAP SD tables with proper referential integrity
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from faker import Faker
import os

# Initialize Faker with multiple locales
fake = Faker(['en_US', 'de_DE', 'en_GB', 'fr_FR'])
Faker.seed(42)
np.random.seed(42)
random.seed(42)

# Configuration
NUM_CUSTOMERS = 5000  # Reduced for testing, can scale to 500K
NUM_MATERIALS = 2000  # Reduced for testing, can scale to 200K
NUM_ORDERS_PER_DAY = 500
NUM_DAYS = 30

# Get absolute path to project root
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'data')


class SAPDataGenerator:
    """Generate synthetic SAP SD data with referential integrity"""

    def __init__(self):
        self.customers = None
        self.materials = None
        self.orders = None
        self.sales_orgs = None
        self.company_codes = None

    def generate_master_data(self):
        """Generate all master data tables"""
        print("Generating Master Data...")

        # Generate organizational structures first
        self.company_codes = self.generate_t001_company_codes()
        self.sales_orgs = self.generate_tvko_sales_orgs()
        self.dist_channels = self.generate_tvtw_distribution_channels()
        self.divisions = self.generate_tspa_divisions()
        self.material_groups = self.generate_t023_material_groups()
        self.countries = self.generate_t005_countries()
        self.prod_hierarchy = self.generate_t171t_product_hierarchy()

        # Generate customer master data
        self.customers = self.generate_kna1_customer_master()
        self.customer_sales = self.generate_knvv_customer_sales()
        self.customer_company = self.generate_knb1_customer_company()
        self.customer_partners = self.generate_knvp_customer_partners()

        # Generate material master data
        self.materials = self.generate_mara_material_master()
        self.material_plant = self.generate_marc_material_plant()
        self.material_desc = self.generate_makt_material_descriptions()
        self.material_sales = self.generate_mvke_material_sales()

    def generate_transaction_data(self):
        """Generate all transaction data tables"""
        print("Generating Transaction Data...")

        # Generate sales orders
        self.orders = self.generate_vbak_sales_orders()
        self.order_items = self.generate_vbap_sales_items()
        self.order_status = self.generate_vbuk_order_status()
        self.item_status = self.generate_vbup_item_status()
        self.schedule_lines = self.generate_vbep_schedule_lines()

        # Generate deliveries
        self.deliveries = self.generate_likp_deliveries()
        self.delivery_items = self.generate_lips_delivery_items()

        # Generate billing
        self.billing = self.generate_vbrk_billing()
        self.billing_items = self.generate_vbrp_billing_items()

        # Generate support tables
        self.doc_flow = self.generate_vbfa_document_flow()
        self.pricing = self.generate_konv_pricing()
        self.partners = self.generate_vbpa_partners()
        self.shipments = self.generate_vttk_shipments()
        self.shipment_items = self.generate_vttp_shipment_items()

    # ==================== ORGANIZATIONAL TABLES ====================

    def generate_t001_company_codes(self):
        """T001 - Company Codes"""
        data = [
            {'BUKRS': '1000', 'BUTXT': 'US Company Inc.', 'WAERS': 'USD', 'LAND1': 'US'},
            {'BUKRS': '2000', 'BUTXT': 'Germany GmbH', 'WAERS': 'EUR', 'LAND1': 'DE'},
            {'BUKRS': '3000', 'BUTXT': 'UK Limited', 'WAERS': 'GBP', 'LAND1': 'GB'},
        ]
        df = pd.DataFrame(data)
        df.to_csv(f'{OUTPUT_DIR}/bronze/master/organizational/T001.csv', index=False)
        return df

    def generate_tvko_sales_orgs(self):
        """TVKO - Sales Organizations"""
        data = [
            {'VKORG': '1000', 'VTEXT': 'US Sales Org', 'BUKRS': '1000'},
            {'VKORG': '2000', 'VTEXT': 'Germany Sales Org', 'BUKRS': '2000'},
            {'VKORG': '3000', 'VTEXT': 'UK Sales Org', 'BUKRS': '3000'},
        ]
        df = pd.DataFrame(data)
        df.to_csv(f'{OUTPUT_DIR}/bronze/master/organizational/TVKO.csv', index=False)
        return df

    def generate_tvtw_distribution_channels(self):
        """TVTW - Distribution Channels"""
        data = [
            {'VTWEG': '10', 'VTEXT': 'Direct Sales'},
            {'VTWEG': '20', 'VTEXT': 'Wholesale'},
            {'VTWEG': '30', 'VTEXT': 'E-Commerce'},
        ]
        df = pd.DataFrame(data)
        df.to_csv(f'{OUTPUT_DIR}/bronze/master/organizational/TVTW.csv', index=False)
        return df

    def generate_tspa_divisions(self):
        """TSPA - Divisions"""
        data = [
            {'SPART': '00', 'VTEXT': 'Cross-Division'},
            {'SPART': '01', 'VTEXT': 'Electronics'},
            {'SPART': '02', 'VTEXT': 'Machinery'},
        ]
        df = pd.DataFrame(data)
        df.to_csv(f'{OUTPUT_DIR}/bronze/master/organizational/TSPA.csv', index=False)
        return df

    def generate_t023_material_groups(self):
        """T023 - Material Groups"""
        groups = ['ELEC', 'MACH', 'TOOL', 'PART', 'CONS']
        descriptions = ['Electronics', 'Machinery', 'Tools', 'Parts', 'Consumables']
        df = pd.DataFrame({
            'MATKL': groups,
            'WGBEZ': descriptions
        })
        df.to_csv(f'{OUTPUT_DIR}/bronze/master/organizational/T023.csv', index=False)
        return df

    def generate_t005_countries(self):
        """T005 - Countries"""
        countries = [
            {'LAND1': 'US', 'LANDX': 'United States', 'NATIO': 'US'},
            {'LAND1': 'DE', 'LANDX': 'Germany', 'NATIO': 'DE'},
            {'LAND1': 'GB', 'LANDX': 'United Kingdom', 'NATIO': 'GB'},
            {'LAND1': 'FR', 'LANDX': 'France', 'NATIO': 'FR'},
            {'LAND1': 'CN', 'LANDX': 'China', 'NATIO': 'CN'},
        ]
        df = pd.DataFrame(countries)
        df.to_csv(f'{OUTPUT_DIR}/bronze/master/organizational/T005.csv', index=False)
        return df

    def generate_t171t_product_hierarchy(self):
        """T171T - Product Hierarchy Text"""
        hierarchies = []
        for i in range(1, 21):
            hierarchies.append({
                'PRODH': f'{i:018d}',
                'SPRAS': 'E',
                'VTEXT': f'Product Group {i}'
            })
        df = pd.DataFrame(hierarchies)
        df.to_csv(f'{OUTPUT_DIR}/bronze/master/product_hierarchy/T171T.csv', index=False)
        return df

    # ==================== CUSTOMER MASTER DATA ====================

    def generate_kna1_customer_master(self):
        """KNA1 - Customer Master General"""
        customers = []
        for i in range(NUM_CUSTOMERS):
            country = np.random.choice(['US', 'DE', 'GB', 'FR'], p=[0.6, 0.2, 0.15, 0.05])
            customers.append({
                'KUNNR': f'{i+100000:010d}',
                'NAME1': fake.company(),
                'LAND1': country,
                'PSTLZ': fake.postcode(),
                'ORT01': fake.city(),
                'STRAS': fake.street_address(),
                'KTOKD': np.random.choice(['0001', '0002', '0003'], p=[0.7, 0.2, 0.1]),
                'BRSCH': np.random.choice(['1200', '2900', '5100', '7100'], p=[0.3, 0.25, 0.25, 0.2]),
                'ERDAT': (datetime.now() - timedelta(days=random.randint(1, 2000))).strftime('%Y%m%d'),
                'LOEVM': ''  # Not deleted
            })
        df = pd.DataFrame(customers)
        df.to_csv(f'{OUTPUT_DIR}/bronze/master/customer/KNA1.csv', index=False)
        return df

    def generate_knvv_customer_sales(self):
        """KNVV - Customer Sales Data"""
        sales_data = []
        for _, customer in self.customers.iterrows():
            # Each customer can have 1-3 sales org combinations
            num_sales_orgs = np.random.choice([1, 2, 3], p=[0.7, 0.2, 0.1])
            for _ in range(num_sales_orgs):
                sales_data.append({
                    'KUNNR': customer['KUNNR'],
                    'VKORG': np.random.choice(['1000', '2000', '3000'], p=[0.6, 0.3, 0.1]),
                    'VTWEG': np.random.choice(['10', '20', '30'], p=[0.5, 0.3, 0.2]),
                    'SPART': np.random.choice(['00', '01', '02'], p=[0.5, 0.3, 0.2]),
                    'KDGRP': np.random.choice(['01', '02', '03', '04']),  # Customer group
                    'WAERS': 'USD',
                    'KALKS': '1',  # Pricing procedure
                    'VSBED': np.random.choice(['01', '02']),  # Shipping conditions
                    'LPRIO': np.random.choice(['01', '02']),  # Delivery priority
                })
        df = pd.DataFrame(sales_data)
        df.to_csv(f'{OUTPUT_DIR}/bronze/master/customer/KNVV.csv', index=False)
        return df

    def generate_knb1_customer_company(self):
        """KNB1 - Customer Company Code Data"""
        company_data = []
        for _, customer in self.customers.iterrows():
            bukrs = np.random.choice(['1000', '2000', '3000'], p=[0.6, 0.3, 0.1])
            company_data.append({
                'KUNNR': customer['KUNNR'],
                'BUKRS': bukrs,
                'AKONT': '140000',  # Reconciliation account
                'ZTERM': 'Z030',  # Payment terms
                'FDGRV': '',  # Planning group
            })
        df = pd.DataFrame(company_data)
        df.to_csv(f'{OUTPUT_DIR}/bronze/master/customer/KNB1.csv', index=False)
        return df

    def generate_knvp_customer_partners(self):
        """KNVP - Customer Partner Functions"""
        partners = []
        for _, sales_data in self.customer_sales.iterrows():
            # Add common partner functions: Sold-to, Ship-to, Bill-to, Payer
            for parvw in ['AG', 'WE', 'RE', 'RG']:
                partners.append({
                    'KUNNR': sales_data['KUNNR'],
                    'VKORG': sales_data['VKORG'],
                    'VTWEG': sales_data['VTWEG'],
                    'SPART': sales_data['SPART'],
                    'PARVW': parvw,
                    'KUNN2': sales_data['KUNNR'],  # Partner is same customer for simplicity
                })
        df = pd.DataFrame(partners)
        df.to_csv(f'{OUTPUT_DIR}/bronze/master/customer/KNVP.csv', index=False)
        return df

    # ==================== MATERIAL MASTER DATA ====================

    def generate_mara_material_master(self):
        """MARA - Material General Data"""
        materials = []
        for i in range(NUM_MATERIALS):
            materials.append({
                'MATNR': f'{i+1:018d}',
                'MTART': np.random.choice(['FERT', 'HAWA', 'ROH'], p=[0.7, 0.2, 0.1]),  # Material type
                'MATKL': np.random.choice(['ELEC', 'MACH', 'TOOL', 'PART', 'CONS']),
                'MEINS': np.random.choice(['EA', 'KG', 'L'], p=[0.7, 0.2, 0.1]),  # Base UOM
                'MTPOS_MARA': 'NORM',  # Item category group
                'PRDHA': f'{np.random.randint(1, 21):018d}',  # Product hierarchy
                'ERNAM': 'SYSUSER',
                'ERSDA': (datetime.now() - timedelta(days=random.randint(100, 1000))).strftime('%Y%m%d'),
                'LAEDA': (datetime.now() - timedelta(days=random.randint(1, 100))).strftime('%Y%m%d'),
            })
        df = pd.DataFrame(materials)
        df.to_csv(f'{OUTPUT_DIR}/bronze/master/material/MARA.csv', index=False)
        return df

    def generate_marc_material_plant(self):
        """MARC - Material Plant Data"""
        plants = ['1000', '2000', '3000']
        plant_data = []
        for _, material in self.materials.iterrows():
            # Each material exists in 1-3 plants
            num_plants = np.random.choice([1, 2, 3], p=[0.5, 0.3, 0.2])
            for plant in np.random.choice(plants, num_plants, replace=False):
                plant_data.append({
                    'MATNR': material['MATNR'],
                    'WERKS': plant,
                    'PSTAT': 'KE',  # Maintenance status
                    'LVORM': '',  # Not deleted
                    'DISMM': 'PD',  # MRP type
                    'DISPO': '001',  # MRP controller
                    'EKGRP': '001',  # Purchasing group
                })
        df = pd.DataFrame(plant_data)
        df.to_csv(f'{OUTPUT_DIR}/bronze/master/material/MARC.csv', index=False)
        return df

    def generate_makt_material_descriptions(self):
        """MAKT - Material Descriptions"""
        descriptions = []
        material_names = [
            'Widget', 'Gadget', 'Device', 'Component', 'Assembly',
            'Module', 'Unit', 'System', 'Part', 'Tool'
        ]
        for _, material in self.materials.iterrows():
            descriptions.append({
                'MATNR': material['MATNR'],
                'SPRAS': 'E',
                'MAKTX': f'{random.choice(material_names)} {random.choice(["Pro", "Plus", "Standard", "Premium", "Basic"])} {random.randint(100, 9999)}'
            })
        df = pd.DataFrame(descriptions)
        df.to_csv(f'{OUTPUT_DIR}/bronze/master/material/MAKT.csv', index=False)
        return df

    def generate_mvke_material_sales(self):
        """MVKE - Material Sales Data"""
        sales_data = []
        for _, material in self.materials.iterrows():
            # Each material has sales data for 1-2 sales orgs
            for vkorg in np.random.choice(['1000', '2000', '3000'],
                                         np.random.choice([1, 2], p=[0.7, 0.3]),
                                         replace=False):
                sales_data.append({
                    'MATNR': material['MATNR'],
                    'VKORG': vkorg,
                    'VTWEG': '10',
                    'MVGR1': np.random.choice(['01', '02', '03']),  # Material group 1
                    'KONDM': '01',  # Material pricing group
                    'KTGRM': '01',  # Account assignment group
                })
        df = pd.DataFrame(sales_data)
        df.to_csv(f'{OUTPUT_DIR}/bronze/master/material/MVKE.csv', index=False)
        return df

    # ==================== TRANSACTION DATA - SALES ORDERS ====================

    def generate_vbak_sales_orders(self):
        """VBAK - Sales Document Header"""
        orders = []
        start_date = datetime.now() - timedelta(days=NUM_DAYS)
        order_num = 1000000

        for day in range(NUM_DAYS):
            current_date = start_date + timedelta(days=day)
            daily_orders = NUM_ORDERS_PER_DAY + np.random.randint(-50, 50)

            for hour in range(8, 20):  # Business hours
                hourly_orders = int(daily_orders / 12) + np.random.randint(-5, 5)

                for _ in range(hourly_orders):
                    customer = self.customers.sample(1).iloc[0]
                    vkorg = np.random.choice(['1000', '2000', '3000'], p=[0.6, 0.3, 0.1])

                    order_num += 1
                    erdat = current_date.strftime('%Y%m%d')
                    erzet = f'{hour:02d}{np.random.randint(0, 60):02d}{np.random.randint(0, 60):02d}'

                    # Some orders get changed later
                    aedat = erdat if np.random.random() < 0.3 else None

                    orders.append({
                        'VBELN': f'{order_num:010d}',
                        'ERDAT': erdat,
                        'ERZET': erzet,
                        'ERNAM': 'SALESUSER',
                        'AEDAT': aedat,
                        'AUDAT': erdat,
                        'VBTYP': 'C',  # Order
                        'AUART': np.random.choice(['OR', 'ZOR', 'QT'], p=[0.7, 0.2, 0.1]),
                        'VKORG': vkorg,
                        'VTWEG': np.random.choice(['10', '20', '30'], p=[0.5, 0.3, 0.2]),
                        'SPART': np.random.choice(['00', '01', '02'], p=[0.5, 0.3, 0.2]),
                        'KUNNR': customer['KUNNR'],
                        'VKBUR': f'{vkorg}1',  # Sales office
                        'VKGRP': '001',  # Sales group
                        'NETWR': 0,  # Will be calculated from items
                        'WAERK': 'USD' if vkorg == '1000' else 'EUR',
                        'GBSTK': np.random.choice(['A', 'B', 'C'], p=[0.4, 0.35, 0.25]),
                        'ABSTK': '',  # Rejection status
                        'LIFSK': np.random.choice(['', '01'], p=[0.9, 0.1]),  # Delivery block
                        'FAKSK': np.random.choice(['', '01'], p=[0.95, 0.05]),  # Billing block
                    })

        df = pd.DataFrame(orders)
        df.to_csv(f'{OUTPUT_DIR}/bronze/transactional/sales_orders/VBAK.csv', index=False)
        return df

    def generate_vbap_sales_items(self):
        """VBAP - Sales Document Item"""
        items = []

        for _, order in self.orders.iterrows():
            # Average 5 items per order
            num_items = max(1, int(np.random.poisson(5)))
            order_value = 0

            for item_num in range(1, num_items + 1):
                material = self.materials.sample(1).iloc[0]
                kwmeng = round(np.random.lognormal(3, 1.2), 3)
                netpr = round(np.random.uniform(10, 5000), 2)
                netwr = round(kwmeng * netpr, 2)
                order_value += netwr

                items.append({
                    'VBELN': order['VBELN'],
                    'POSNR': f'{item_num * 10:06d}',
                    'MATNR': material['MATNR'],
                    'ARKTX': f'Item description {item_num}',
                    'KWMENG': kwmeng,
                    'VRKME': material['MEINS'],
                    'UMVKZ': 1,  # Numerator for conversion
                    'UMVKN': 1,  # Denominator for conversion
                    'NETPR': netpr,
                    'NETWR': netwr,
                    'WAERK': order['WAERK'],
                    'WERKS': np.random.choice(['1000', '2000', '3000']),
                    'LGORT': '0001',  # Storage location
                    'PSTYV': 'TAN',  # Item category
                    'ERDAT': order['ERDAT'],
                    'ABGRU': '',  # Rejection reason
                })

        df = pd.DataFrame(items)
        df.to_csv(f'{OUTPUT_DIR}/bronze/transactional/sales_orders/VBAP.csv', index=False)
        return df

    def generate_vbuk_order_status(self):
        """VBUK - Sales Document Header Status"""
        status_data = []

        for _, order in self.orders.iterrows():
            status_data.append({
                'VBELN': order['VBELN'],
                'LFSTK': np.random.choice(['A', 'B', 'C'], p=[0.3, 0.5, 0.2]),  # Delivery status
                'FKSTK': np.random.choice(['A', 'B', 'C'], p=[0.25, 0.45, 0.3]),  # Billing status
                'GBSTK': order['GBSTK'],  # Overall status
                'ABSTK': order['ABSTK'],  # Rejection status
                'LFGSK': np.random.choice(['A', 'B', 'C'], p=[0.3, 0.5, 0.2]),  # Delivery status overall
                'FKIVK': '',  # Billing status invoice
                'UVALL': '',  # Incompletion status
                'CMGST': np.random.choice(['A', 'B', ''], p=[0.3, 0.2, 0.5]),  # Credit check status
            })

        df = pd.DataFrame(status_data)
        df.to_csv(f'{OUTPUT_DIR}/bronze/transactional/sales_orders/VBUK.csv', index=False)
        return df

    def generate_vbup_item_status(self):
        """VBUP - Sales Item Status"""
        status_data = []

        for _, item in self.order_items.iterrows():
            status_data.append({
                'VBELN': item['VBELN'],
                'POSNR': item['POSNR'],
                'LFSTA': np.random.choice(['A', 'B', 'C'], p=[0.3, 0.5, 0.2]),  # Delivery status
                'FKSTA': np.random.choice(['A', 'B', 'C'], p=[0.25, 0.45, 0.3]),  # Billing status
                'GBSTA': np.random.choice(['A', 'B', 'C'], p=[0.4, 0.35, 0.25]),  # Overall status
                'ABSTA': '',  # Rejection status
                'LFGSA': np.random.choice(['A', 'B', 'C'], p=[0.3, 0.5, 0.2]),  # Total delivery status
                'WBSTA': np.random.choice(['A', 'B', 'C'], p=[0.4, 0.4, 0.2]),  # Goods movement status
            })

        df = pd.DataFrame(status_data)
        df.to_csv(f'{OUTPUT_DIR}/bronze/transactional/sales_orders/VBUP.csv', index=False)
        return df

    def generate_vbep_schedule_lines(self):
        """VBEP - Sales Schedule Lines"""
        schedule_lines = []

        for _, item in self.order_items.iterrows():
            # Usually 1 schedule line per item, sometimes 2
            num_lines = np.random.choice([1, 2], p=[0.85, 0.15])

            for etenr in range(1, num_lines + 1):
                order_date = datetime.strptime(item['ERDAT'], '%Y%m%d')
                req_date = order_date + timedelta(days=random.randint(1, 14))

                schedule_lines.append({
                    'VBELN': item['VBELN'],
                    'POSNR': item['POSNR'],
                    'ETENR': f'{etenr:04d}',
                    'EDATU': req_date.strftime('%Y%m%d'),  # Requested delivery date
                    'BMENG': item['KWMENG'] / num_lines,  # Split quantity
                    'VRKME': item['VRKME'],
                    'ERDAT': item['ERDAT'],
                })

        df = pd.DataFrame(schedule_lines)
        df.to_csv(f'{OUTPUT_DIR}/bronze/transactional/sales_orders/VBEP.csv', index=False)
        return df

    # ==================== TRANSACTION DATA - DELIVERIES ====================

    def generate_likp_deliveries(self):
        """LIKP - Delivery Header"""
        deliveries = []
        delivery_num = 8000000000

        # Generate deliveries for ~60% of orders
        eligible_orders = self.orders.sample(frac=0.6)

        for _, order in eligible_orders.iterrows():
            delivery_num += 1
            order_date = datetime.strptime(order['ERDAT'], '%Y%m%d')
            delivery_date = order_date + timedelta(days=random.randint(1, 7))

            deliveries.append({
                'VBELN': f'{delivery_num:010d}',
                'ERNAM': 'WHSUSER',
                'ERDAT': delivery_date.strftime('%Y%m%d'),
                'ERZET': f'{np.random.randint(8, 18):02d}{np.random.randint(0, 60):02d}00',
                'WADAT_IST': delivery_date.strftime('%Y%m%d'),  # Actual GI date
                'WADAT': (delivery_date + timedelta(days=1)).strftime('%Y%m%d'),  # Planned GI date
                'LFART': 'LF',  # Delivery type
                'VKORG': order['VKORG'],
                'VSTEL': f'{order["VKORG"]}1',  # Shipping point
                'KUNNR': order['KUNNR'],
                'INCO1': 'EXW',  # Incoterms
                'LIFSK': '',  # Delivery block
                'KODAT': delivery_date.strftime('%Y%m%d'),  # Picking date
            })

        df = pd.DataFrame(deliveries)
        df.to_csv(f'{OUTPUT_DIR}/bronze/transactional/deliveries/LIKP.csv', index=False)
        return df

    def generate_lips_delivery_items(self):
        """LIPS - Delivery Item"""
        delivery_items = []

        for _, delivery in self.deliveries.iterrows():
            # Find the original order (simplified - using order number logic)
            # In real scenario, would use VBFA document flow
            order_items = self.order_items[
                self.order_items['VBELN'].isin(self.orders['VBELN'])
            ].sample(n=min(5, len(self.order_items)))

            for idx, (_, order_item) in enumerate(order_items.iterrows(), 1):
                delivery_items.append({
                    'VBELN': delivery['VBELN'],
                    'POSNR': f'{idx * 10:06d}',
                    'MATNR': order_item['MATNR'],
                    'LFIMG': order_item['KWMENG'],  # Delivered quantity
                    'VRKME': order_item['VRKME'],
                    'LGMNG': order_item['KWMENG'],  # Quantity in stock unit
                    'MEINS': order_item['VRKME'],
                    'WERKS': order_item['WERKS'],
                    'LGORT': order_item['LGORT'],
                    'VGBEL': order_item['VBELN'],  # Preceding document
                    'VGPOS': order_item['POSNR'],  # Preceding item
                    'ERDAT': delivery['ERDAT'],
                })

        df = pd.DataFrame(delivery_items)
        df.to_csv(f'{OUTPUT_DIR}/bronze/transactional/deliveries/LIPS.csv', index=False)
        return df

    # ==================== TRANSACTION DATA - BILLING ====================

    def generate_vbrk_billing(self):
        """VBRK - Billing Document Header"""
        billing_docs = []
        billing_num = 9000000000

        # Generate billing for ~80% of deliveries
        eligible_deliveries = self.deliveries.sample(frac=0.8)

        for _, delivery in eligible_deliveries.iterrows():
            billing_num += 1
            delivery_date = datetime.strptime(delivery['ERDAT'], '%Y%m%d')
            billing_date = delivery_date + timedelta(days=random.randint(0, 3))

            billing_docs.append({
                'VBELN': f'{billing_num:010d}',
                'FKART': np.random.choice(['F2', 'F8'], p=[0.95, 0.05]),  # Invoice type / Credit memo
                'FKDAT': billing_date.strftime('%Y%m%d'),  # Billing date
                'ERDAT': billing_date.strftime('%Y%m%d'),
                'ERZET': f'{np.random.randint(8, 18):02d}{np.random.randint(0, 60):02d}00',
                'ERNAM': 'BILLUSER',
                'KUNAG': delivery['KUNNR'],  # Sold-to party
                'KUNRG': delivery['KUNNR'],  # Payer
                'VKORG': delivery['VKORG'],
                'NETWR': 0,  # Will be calculated from items
                'WAERK': 'USD' if delivery['VKORG'] == '1000' else 'EUR',
                'FKSTO': '',  # Not cancelled
                'VBUND': '',  # Not bundled
                'RFBSK': np.random.choice(['A', 'B', 'C'], p=[0.7, 0.2, 0.1]),  # Accounting status
            })

        df = pd.DataFrame(billing_docs)
        df.to_csv(f'{OUTPUT_DIR}/bronze/transactional/billing/VBRK.csv', index=False)
        return df

    def generate_vbrp_billing_items(self):
        """VBRP - Billing Document Item"""
        billing_items = []

        for _, billing in self.billing.iterrows():
            # Get delivery items (simplified)
            delivery_items = self.delivery_items.sample(n=min(5, len(self.delivery_items)))
            billing_value = 0

            for idx, (_, del_item) in enumerate(delivery_items.iterrows(), 1):
                netwr = round(float(del_item['LFIMG']) * np.random.uniform(50, 1000), 2)
                billing_value += netwr

                billing_items.append({
                    'VBELN': billing['VBELN'],
                    'POSNR': f'{idx * 10:06d}',
                    'MATNR': del_item['MATNR'],
                    'ARKTX': f'Billing item {idx}',
                    'FKIMG': del_item['LFIMG'],  # Billed quantity
                    'VRKME': del_item['VRKME'],
                    'NETWR': netwr,
                    'WAERK': billing['WAERK'],
                    'WERKS': del_item['WERKS'],
                    'VGBEL': del_item['VBELN'],  # Reference delivery
                    'VGPOS': del_item['POSNR'],  # Reference item
                    'ERDAT': billing['ERDAT'],
                    'AUBEL': del_item['VGBEL'],  # Original order
                    'AUPOS': del_item['VGPOS'],  # Original item
                })

        df = pd.DataFrame(billing_items)
        df.to_csv(f'{OUTPUT_DIR}/bronze/transactional/billing/VBRP.csv', index=False)
        return df

    # ==================== TRANSACTION DATA - SUPPORT TABLES ====================

    def generate_vbfa_document_flow(self):
        """VBFA - Sales Document Flow"""
        doc_flows = []

        # Order -> Delivery flows
        for _, delivery_item in self.delivery_items.iterrows():
            if pd.notna(delivery_item.get('VGBEL')):
                doc_flows.append({
                    'VBELV': delivery_item['VGBEL'],  # Preceding doc
                    'POSNV': delivery_item['VGPOS'],  # Preceding item
                    'VBELN': delivery_item['VBELN'],  # Subsequent doc
                    'POSNN': delivery_item['POSNR'],  # Subsequent item
                    'VBTYP_N': 'J',  # Subsequent doc category (Delivery)
                    'VBTYP_V': 'C',  # Preceding doc category (Order)
                    'RFMNG': delivery_item['LFIMG'],  # Quantity
                    'MEINS': delivery_item['VRKME'],
                    'ERDAT': delivery_item['ERDAT'],
                })

        # Delivery -> Billing flows
        for _, billing_item in self.billing_items.iterrows():
            if pd.notna(billing_item.get('VGBEL')):
                doc_flows.append({
                    'VBELV': billing_item['VGBEL'],  # Preceding doc (delivery)
                    'POSNV': billing_item['VGPOS'],  # Preceding item
                    'VBELN': billing_item['VBELN'],  # Subsequent doc (billing)
                    'POSNN': billing_item['POSNR'],  # Subsequent item
                    'VBTYP_N': 'M',  # Subsequent doc category (Invoice)
                    'VBTYP_V': 'J',  # Preceding doc category (Delivery)
                    'RFMNG': billing_item['FKIMG'],  # Quantity
                    'MEINS': billing_item['VRKME'],
                    'ERDAT': billing_item['ERDAT'],
                })

        df = pd.DataFrame(doc_flows)
        df.to_csv(f'{OUTPUT_DIR}/bronze/transactional/document_flow/VBFA.csv', index=False)
        return df

    def generate_konv_pricing(self):
        """KONV - Pricing Conditions"""
        pricing_data = []

        for _, order_item in self.order_items.iterrows():
            knumv = f'{order_item["VBELN"]}'  # Document condition number

            # Add common pricing conditions
            conditions = [
                ('PR00', float(order_item['NETPR']), 'Base price'),
                ('K004', float(order_item['NETPR']) * -0.05, 'Discount'),
                ('MWST', float(order_item['NETWR']) * 0.08, 'Tax'),
            ]

            for idx, (kschl, kwert, desc) in enumerate(conditions, 1):
                pricing_data.append({
                    'KNUMV': knumv,
                    'KPOSN': order_item['POSNR'],
                    'STUNR': f'{idx:03d}',
                    'ZAEHK': '01',
                    'KSCHL': kschl,
                    'KWERT': round(kwert, 2),
                    'KBETR': round(kwert, 2),
                    'WAERS': order_item['WAERK'],
                })

        df = pd.DataFrame(pricing_data)
        df.to_csv(f'{OUTPUT_DIR}/bronze/transactional/pricing/KONV.csv', index=False)
        return df

    def generate_vbpa_partners(self):
        """VBPA - Sales Partners"""
        partners = []

        for _, order in self.orders.iterrows():
            # Add standard partner functions
            for parvw in ['AG', 'WE', 'RE', 'RG', 'SP']:  # Sold-to, Ship-to, Bill-to, Payer, Sales person
                partners.append({
                    'VBELN': order['VBELN'],
                    'POSNR': '000000',  # Header level
                    'PARVW': parvw,
                    'KUNNR': order['KUNNR'],  # Simplified - all point to same customer
                    'ADRNR': '',
                    'PERNR': '10000' if parvw == 'SP' else '',  # Sales person employee number
                })

        df = pd.DataFrame(partners)
        df.to_csv(f'{OUTPUT_DIR}/bronze/transactional/partners/VBPA.csv', index=False)
        return df

    def generate_vttk_shipments(self):
        """VTTK - Shipment Header"""
        shipments = []
        shipment_num = 700000000

        # Generate shipments for ~40% of deliveries (consolidated)
        eligible_deliveries = self.deliveries.sample(frac=0.4)

        for _, delivery in eligible_deliveries.iterrows():
            shipment_num += 1
            delivery_date = datetime.strptime(delivery['ERDAT'], '%Y%m%d')

            shipments.append({
                'TKNUM': f'{shipment_num:010d}',
                'SHTYP': 'ZSTD',  # Shipment type
                'ERNAM': 'SHIPUSER',
                'ERDAT': delivery_date.strftime('%Y%m%d'),
                'DATEN': delivery_date.strftime('%Y%m%d'),  # Shipment start date
                'DATBI': (delivery_date + timedelta(days=2)).strftime('%Y%m%d'),  # End date
                'VSTEL': delivery['VSTEL'],
                'TDLNR': f'CARR{np.random.randint(1, 6)}',  # Carrier
            })

        df = pd.DataFrame(shipments)
        df.to_csv(f'{OUTPUT_DIR}/bronze/transactional/shipment/VTTK.csv', index=False)
        return df

    def generate_vttp_shipment_items(self):
        """VTTP - Shipment Item"""
        shipment_items = []

        for _, shipment in self.shipments.iterrows():
            # Each shipment has 1-3 deliveries
            num_deliveries = np.random.choice([1, 2, 3], p=[0.6, 0.3, 0.1])
            deliveries = self.deliveries.sample(n=min(num_deliveries, len(self.deliveries)))

            for idx, (_, delivery) in enumerate(deliveries.iterrows(), 1):
                shipment_items.append({
                    'TKNUM': shipment['TKNUM'],
                    'TPNUM': f'{idx:04d}',
                    'VBELN': delivery['VBELN'],  # Delivery number
                    'ERDAT': shipment['ERDAT'],
                })

        df = pd.DataFrame(shipment_items)
        df.to_csv(f'{OUTPUT_DIR}/bronze/transactional/shipment/VTTP.csv', index=False)
        return df

    def save_all_data(self):
        """Convenience method to save all generated data"""
        print("\nAll synthetic data generated successfully!")
        print(f"\nData Statistics:")
        print(f"  Customers: {len(self.customers):,}")
        print(f"  Materials: {len(self.materials):,}")
        print(f"  Sales Orders: {len(self.orders):,}")
        print(f"  Order Items: {len(self.order_items):,}")
        print(f"  Deliveries: {len(self.deliveries):,}")
        print(f"  Delivery Items: {len(self.delivery_items):,}")
        print(f"  Billing Documents: {len(self.billing):,}")
        print(f"  Billing Items: {len(self.billing_items):,}")
        print(f"  Document Flows: {len(self.doc_flow):,}")
        print(f"  Pricing Records: {len(self.pricing):,}")
        print(f"  Partner Records: {len(self.partners):,}")
        print(f"  Shipments: {len(self.shipments):,}")


def main():
    """Main execution function"""
    print("=" * 80)
    print("SAP SD Sales Analytics - Synthetic Data Generator")
    print("=" * 80)

    # Create output directories
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    generator = SAPDataGenerator()

    # Generate all data
    generator.generate_master_data()
    generator.generate_transaction_data()
    generator.save_all_data()

    print(f"\nAll CSV files saved to: {OUTPUT_DIR}/bronze/")
    print("\nNext steps:")
    print("  1. Review the generated CSV files")
    print("  2. Convert CSVs to Parquet format for ADLS upload")
    print("  3. Upload to Azure Data Lake Storage Gen2")


if __name__ == "__main__":
    main()
