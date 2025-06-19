from dataclasses import dataclass
from typing import List, Optional, Dict, Tuple
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import os

@dataclass
class Sensor:
    Machine_ID: str
    Machine_Type: str
    Installation_Year: int
    Operational_Hours: float
    Temperature_C: float
    Vibration_mms: float
    Sound_dB: float
    Oil_Level_pct: float
    Coolant_Level_pct: float
    Power_Consumption_kW: float
    Last_Maintenance_Days_Ago: int
    Maintenance_History_Count: int
    Failure_History_Count: int
    AI_Supervision: bool
    Error_Codes_Last_30_Days: int
    Remaining_Useful_Life_days: float
    Failure_Within_7_Days: bool
    Laser_Intensity: Optional[float]
    Hydraulic_Pressure_bar: Optional[float]
    Coolant_Flow_L_min: Optional[float]
    Heat_Index: Optional[float]
    AI_Override_Events: int

class SensorDataAnalyzer:
    """Class to analyze factory sensor data and provide insights."""
    
    def __init__(self, csv_path: str):
        """Initialize with the path to the CSV file."""
        self.csv_path = csv_path
        self.data = None
        self.load_data()
    
    def load_data(self):
        """Load the sensor data from CSV file."""
        self.data = pd.read_csv(self.csv_path)
        # Convert AI_Supervision to boolean
        self.data['AI_Supervision'] = self.data['AI_Supervision'].astype(bool)
        # Convert Failure_Within_7_Days to boolean
        self.data['Failure_Within_7_Days'] = self.data['Failure_Within_7_Days'].astype(bool)
        print(f"Loaded {len(self.data)} machine records from {self.csv_path}")
    
    def get_summary_statistics(self):
        """Get summary statistics of the sensor data."""
        numeric_cols = self.data.select_dtypes(include=['number']).columns
        return self.data[numeric_cols].describe()
    
    def get_machine_type_distribution(self):
        """Get the distribution of machine types."""
        return self.data['Machine_Type'].value_counts()
    
    def get_failure_risk_machines(self, days_threshold: int = 7):
        """Get machines that are at risk of failure within specified days."""
        return self.data[self.data['Remaining_Useful_Life_days'] <= days_threshold]
    
    def get_machines_by_age(self, current_year: int = 2025):
        """Group machines by age categories."""
        self.data['Age'] = current_year - self.data['Installation_Year']
        age_bins = [0, 5, 10, 15, 20, 25, float('inf')]
        age_labels = ['0-5 years', '6-10 years', '11-15 years', '16-20 years', '21-25 years', '>25 years']
        self.data['Age_Category'] = pd.cut(self.data['Age'], bins=age_bins, labels=age_labels)
        return self.data['Age_Category'].value_counts().sort_index()
    
    def get_maintenance_needed_machines(self, days_threshold: int = 180):
        """Get machines that haven't been maintained in a long time."""
        return self.data[self.data['Last_Maintenance_Days_Ago'] > days_threshold]
    
    def analyze_failure_correlation(self):
        """Analyze correlation between various factors and failure probability."""
        failure_data = self.data.copy()
        
        # Calculate correlation with Failure_Within_7_Days
        numeric_cols = failure_data.select_dtypes(include=['number']).columns
        correlations = {}
        for col in numeric_cols:
            if col != 'Failure_Within_7_Days':
                correlations[col] = failure_data[col].corr(failure_data['Failure_Within_7_Days'].astype(int))
        
        # Sort correlations by absolute value
        sorted_correlations = {k: v for k, v in sorted(correlations.items(), 
                                                      key=lambda item: abs(item[1]), 
                                                      reverse=True)}
        return sorted_correlations
    
    def get_critical_machines(self):
        """Get machines that are in critical condition (multiple warning signs)."""
        critical = self.data[
            (self.data['Failure_Within_7_Days'] == True) | 
            (self.data['Remaining_Useful_Life_days'] < 30) |
            ((self.data['Temperature_C'] > 80) & (self.data['Vibration_mms'] > 15)) |
            (self.data['Error_Codes_Last_30_Days'] > 5)
        ]
        return critical
    
    def visualize_machine_health(self, output_dir: str = None):
        """Create visualizations of machine health metrics."""
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        # Plot 1: Machine types distribution
        plt.figure(figsize=(12, 6))
        machine_counts = self.data['Machine_Type'].value_counts().sort_values(ascending=False)
        machine_counts.plot(kind='bar', color='skyblue')
        plt.title('Distribution of Machine Types')
        plt.xlabel('Machine Type')
        plt.ylabel('Count')
        plt.xticks(rotation=90)
        plt.tight_layout()
        if output_dir:
            plt.savefig(f"{output_dir}/machine_types.png")
        plt.close()
        
        # Plot 2: Remaining Useful Life Distribution
        plt.figure(figsize=(10, 6))
        plt.hist(self.data['Remaining_Useful_Life_days'].dropna(), bins=30, color='green', alpha=0.7)
        plt.title('Distribution of Remaining Useful Life')
        plt.xlabel('Days')
        plt.ylabel('Count')
        plt.grid(True, alpha=0.3)
        if output_dir:
            plt.savefig(f"{output_dir}/remaining_life.png")
        plt.close()
        
        # Plot 3: Temperature vs Vibration colored by failure risk
        plt.figure(figsize=(10, 8))
        failure = self.data[self.data['Failure_Within_7_Days'] == True]
        no_failure = self.data[self.data['Failure_Within_7_Days'] == False]
        
        plt.scatter(no_failure['Temperature_C'], no_failure['Vibration_mms'], 
                   alpha=0.5, color='blue', label='No Failure Risk')
        plt.scatter(failure['Temperature_C'], failure['Vibration_mms'], 
                   alpha=0.7, color='red', label='Failure Within 7 Days')
        
        plt.title('Temperature vs Vibration by Failure Risk')
        plt.xlabel('Temperature (°C)')
        plt.ylabel('Vibration (mm/s)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        if output_dir:
            plt.savefig(f"{output_dir}/temp_vs_vibration.png")
        plt.close()
        
        # Plot 4: Machine Age vs Remaining Life
        plt.figure(figsize=(10, 6))
        current_year = 2025
        self.data['Age'] = current_year - self.data['Installation_Year']
        
        plt.scatter(self.data['Age'], self.data['Remaining_Useful_Life_days'], 
                   alpha=0.5, c=self.data['Operational_Hours'], cmap='viridis')
        
        plt.colorbar(label='Operational Hours')
        plt.title('Machine Age vs Remaining Useful Life')
        plt.xlabel('Age (Years)')
        plt.ylabel('Remaining Useful Life (Days)')
        plt.grid(True, alpha=0.3)
        if output_dir:
            plt.savefig(f"{output_dir}/age_vs_remaining_life.png")
        plt.close()
        
        # Plot 5: Correlation heatmap
        plt.figure(figsize=(12, 10))
        numeric_data = self.data.select_dtypes(include=['number'])
        correlation = numeric_data.corr()
        
        plt.imshow(correlation, cmap='coolwarm')
        plt.colorbar(label='Correlation Coefficient')
        plt.title('Correlation Between Machine Metrics')
        
        # Add correlation values
        for i in range(len(correlation.columns)):
            for j in range(len(correlation.columns)):
                plt.text(i, j, f"{correlation.iloc[i, j]:.2f}", 
                        ha='center', va='center', color='white' if abs(correlation.iloc[i, j]) > 0.5 else 'black')
        
        plt.xticks(range(len(correlation.columns)), correlation.columns, rotation=90)
        plt.yticks(range(len(correlation.columns)), correlation.columns)
        plt.tight_layout()
        if output_dir:
            plt.savefig(f"{output_dir}/correlation_heatmap.png")
        plt.close()
    
    def generate_maintenance_report(self):
        """Generate a maintenance prioritization report."""
        # Score each machine based on various risk factors
        self.data['Risk_Score'] = (
            (self.data['Remaining_Useful_Life_days'] < 30).astype(int) * 5 +
            self.data['Failure_Within_7_Days'].astype(int) * 10 +
            (self.data['Temperature_C'] > 75).astype(int) * 2 +
            (self.data['Vibration_mms'] > 15).astype(int) * 3 +
            (self.data['Last_Maintenance_Days_Ago'] > 300).astype(int) * 2 +
            self.data['Error_Codes_Last_30_Days'] +
            self.data['Failure_History_Count']
        )
        
        # Sort by risk score
        maintenance_report = self.data.sort_values(by='Risk_Score', ascending=False)
        columns = ['Machine_ID', 'Machine_Type', 'Risk_Score', 'Remaining_Useful_Life_days', 
                  'Failure_Within_7_Days', 'Temperature_C', 'Vibration_mms', 
                  'Last_Maintenance_Days_Ago', 'Error_Codes_Last_30_Days']
        
        return maintenance_report[columns].head(20)

def analyze_factory_data(csv_path: str, output_dir: str = None):
    """Analyze factory sensor data and generate reports and visualizations."""
    analyzer = SensorDataAnalyzer(csv_path)
    
    # Generate reports
    summary = analyzer.get_summary_statistics()
    machine_distribution = analyzer.get_machine_type_distribution()
    failure_risk = analyzer.get_failure_risk_machines()
    age_distribution = analyzer.get_machines_by_age()
    maintenance_needed = analyzer.get_maintenance_needed_machines()
    critical_machines = analyzer.get_critical_machines()
    maintenance_report = analyzer.generate_maintenance_report()
    failure_correlation = analyzer.analyze_failure_correlation()
    
    # Print key findings
    print("\n=== FACTORY SENSOR DATA ANALYSIS ===")
    print(f"\nTotal machines analyzed: {len(analyzer.data)}")
    print(f"Machines at risk of failure within 7 days: {len(failure_risk)}")
    print(f"Machines in critical condition: {len(critical_machines)}")
    print(f"Machines needing maintenance: {len(maintenance_needed)}")
    
    print("\n=== TOP 10 PRIORITY MACHINES FOR MAINTENANCE ===")
    print(maintenance_report.head(10))
    
    print("\n=== MACHINE TYPE DISTRIBUTION ===")
    print(machine_distribution)
    
    print("\n=== MACHINE AGE DISTRIBUTION ===")
    print(age_distribution)
    
    print("\n=== TOP FACTORS CORRELATED WITH FAILURE ===")
    for factor, correlation in list(failure_correlation.items())[:10]:
        print(f"{factor}: {correlation:.4f}")
    
    # Generate visualizations
    if output_dir:
        analyzer.visualize_machine_health(output_dir)
        print(f"\nVisualizations saved to {output_dir}")
    
    return {
        "summary": summary,
        "machine_distribution": machine_distribution,
        "failure_risk": failure_risk,
        "age_distribution": age_distribution,
        "maintenance_needed": maintenance_needed,
        "critical_machines": critical_machines,
        "maintenance_report": maintenance_report,
        "failure_correlation": failure_correlation
    }

if __name__ == "__main__":
    # Path to the CSV file
    csv_path = Path(__file__).parent.parent.parent / "factory_sensor_simulator_2040.csv"
    
    # Output directory for visualizations
    output_dir = Path(__file__).parent.parent.parent / "analysis_results"
    
    # Run analysis
    results = analyze_factory_data(str(csv_path), str(output_dir))