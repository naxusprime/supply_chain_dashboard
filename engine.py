# engine.py
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///supply_chain.db"

def load_processed_data():
    engine = create_engine(DATABASE_URL)
    
    # Read core tables
    orders = pd.read_sql("SELECT * FROM orderlist", con=engine)
    wh_costs = pd.read_sql("SELECT * FROM whcosts", con=engine)
    wh_caps = pd.read_sql("SELECT * FROM whcapacities", con=engine)
    freight = pd.read_sql("SELECT * FROM freightrates", con=engine)
    
    # 1. Compute Warehouse Handling Costs
    df = orders.merge(wh_costs, left_on='Plant Code', right_on='WH', how='left')
    df['wh_total_cost'] = df['Unit quantity'] * df['Cost/unit']
    
    # 2. Compute Freight Transit Costs
    def match_freight(row):
        matches = freight[
            (freight['Carrier'] == row['Carrier']) &
            (freight['orig_port_cd'] == row['Origin Port']) &
            (freight['dest_port_cd'] == row['Destination Port']) &
            (freight['svc_cd'] == row['Service Level'])
        ]
        
        if matches.empty:
            return 0.0
            
        # Filter by weight tier
        weight_tier = matches[
            (matches['minm_wgh_qty'] <= row['Weight']) &
            (matches['max_wgh_qty'] >= row['Weight'])
        ]
        
        selected = weight_tier.iloc[0] if not weight_tier.empty else matches.iloc[0]
        calculated_cost = row['Weight'] * selected['rate']
        return max(calculated_cost, selected['minimum cost'])

    df['freight_cost'] = df.apply(match_freight, axis=1)
    df['total_supply_chain_cost'] = df['wh_total_cost'] + df['freight_cost']
    
    return df, wh_caps

def get_summary_metrics(df, wh_caps):
    # Total Spending Metrics
    total_wh_cost = df['wh_total_cost'].sum()
    total_freight_cost = df['freight_cost'].sum()
    total_cost = df['total_supply_chain_cost'].sum()
    total_units = df['Unit quantity'].sum()
    total_weight = df['Weight'].sum()
    
    # Plant Utilization & Bottlenecks
    plant_summary = df.groupby('Plant Code').agg(
        total_orders=('Order ID', 'count'),
        total_units=('Unit quantity', 'sum'),
        total_wh_cost=('wh_total_cost', 'sum'),
        total_freight_cost=('freight_cost', 'sum')
    ).reset_index()
    
    plant_summary = plant_summary.merge(wh_caps, left_on='Plant Code', right_on='Plant ID', how='left')
    plant_summary['cost_per_unit'] = plant_summary['total_wh_cost'] / plant_summary['total_units']
    
    return {
        'total_wh_cost': total_wh_cost,
        'total_freight_cost': total_freight_cost,
        'total_cost': total_cost,
        'total_units': total_units,
        'total_weight': total_weight,
        'plant_summary': plant_summary
    }

if __name__ == "__main__":
    df, wh_caps = load_processed_data()
    metrics = get_summary_metrics(df, wh_caps)
    print(f"Total Logistics Cost: ${metrics['total_cost']:,.2f}")
    print("\nPlant Fulfillment Summary:")
    print(metrics['plant_summary'][['Plant Code', 'total_orders', 'total_units', 'total_wh_cost', 'cost_per_unit']])