import re
from datetime import datetime

import pandas as pd
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.http import require_POST  # Import the decorator
from .models import RawData  # Import your RawData model

# @require_POST  # Use the decorator to allow only POST requests
class RawDataUploadView(views.APIView):
    def get(self, request):
        file_path = "H:\ResourceManager\ResourceManagerProject\statics\CostReport_2011_Final.csv"  # Specify the local file path here
        print("start")
        try:
            # Read the CSV file using pandas
            df = pd.read_csv(file_path, encoding='utf-8')

            # Define the mapping between Excel column names and Django field names
            column_mapping = {
                'Report Record Number': 'RecordNumber',
                'Provider CCN': 'CCN',
                'Hospital Name': 'HospitalName',
                'Street Address': 'Address',
                'City': 'City',
                'State Code': 'StateCode',
                'Zip Code': 'ZipCode',
                'County': 'County',
                'Medicare CBSA Number': 'CBSANumber',
                'Rural Versus Urban': 'RuralUrban',
                'CCN Facility Type': 'FacilityType',
                'Provider Type': 'ProviderType',
                'Type of Control': 'ControlType',
                'Fiscal Year Begin Date': 'FiscalYearBegin',
                'Fiscal Year End Date': 'FiscalYearEnd',
                'FTE - Employees on Payroll': 'FTEEmployees',
                'Number of Interns and Residents (FTE)': 'InternsResidents',
                'Total Days Title V': 'TotalDaysTitleV',
                'Total Days Title XVIII': 'TotalDaysTitleXVIII',
                'Total Days Title XIX': 'TotalDaysTitleXIX',
                'Total Days (V + XVIII + XIX + Unknown)': 'TotalDaysTotal',
                'Number of Beds': 'Beds',
                'Total Bed Days Available': 'BedDaysAvailable',
                'Total Discharges Title V': 'DischargesTitleV',
                'Total Discharges Title XVIII': 'DischargesTitleXVIII',
                'Total Discharges Title XIX': 'DischargesTitleXIX',
                'Total Discharges (V + XVIII + XIX + Unknown)': 'DischargesTotal',
                'Total Days Title V + Total for all Subproviders': 'DaysTitleVTotal',
                'Total Days Title XVIII + Total for all Subproviders': 'DaysTitleXVIIITotal',
                'Total Days Title XIX + Total for all Subproviders': 'DaysTitleXIXTotal',
                'Total Days (V + XVIII + XIX + Unknown) + Total for all Subproviders': 'DaysTotalTotal',
                'Number of Beds + Total for all Subproviders': 'BedsTotal',
                'Total Bed Days Available + Total for all Subproviders': 'BedDaysAvailableTotal',
                'Total Discharges Title V + Total for all Subproviders': 'DischargesTitleVTotal',
                'Total Discharges Title XVIII + Total for all Subproviders': 'DischargesTitleXVIIITotal',
                'Total Discharges Title XIX + Total for all Subproviders': 'DischargesTitleXIXTotal',
                'Total Discharges (V + XVIII + XIX + Unknown) + Total for all Subproviders': 'DischargesTotalTotal',
                'Hospital Total Days Title V For Adults & Peds': 'DaysTitleVAdultsPeds',
                'Hospital Total Days Title XVIII For Adults & Peds': 'DaysTitleXVIIIAdultsPeds',
                'Hospital Total Days Title XIX For Adults & Peds': 'DaysTitleXIXAdultsPeds',
                'Hospital Total Days (V + XVIII + XIX + Unknown) For Adults & Peds': 'DaysTotalAdultsPeds',
                'Hospital Number of Beds For Adults & Peds': 'BedsAdultsPeds',
                'Hospital Total Bed Days Available For Adults & Peds': 'BedDaysAvailableAdultsPeds',
                'Hospital Total Discharges Title V For Adults & Peds': 'DischargesTitleVAdultsPeds',
                'Hospital Total Discharges Title XVIII For Adults & Peds': 'DischargesTitleXVIIIAdultsPeds',
                'Hospital Total Discharges Title XIX For Adults & Peds': 'DischargesTitleXIXAdultsPeds',
                'Hospital Total Discharges (V + XVIII + XIX + Unknown) For Adults & Peds': 'DischargesTotalAdultsPeds',
                'Cost of Charity Care': 'CharityCost',
                'Total Bad Debt Expense': 'BadDebtExpense',
                'Cost of Uncompensated Care': 'UncompensatedCost',
                'Total Unreimbursed and Uncompensated Care': 'UnreimbursedUncompensatedCost',
                'Total Salaries From Worksheet A': 'SalariesFromWorksheetA',
                'Overhead Non-Salary Costs': 'OverheadCost',
                'Depreciation Cost': 'DepreciationCost',
                'Total Costs': 'TotalCost',
                'Inpatient Total Charges': 'InpatientCharges',
                'Outpatient Total Charges': 'OutpatientCharges',
                'Combined Outpatient + Inpatient Total Charges': 'CombinedCharges',
                'Wage-Related Costs (Core)': 'WageRelatedCostsCore',
                'Wage-Related Costs (RHC/FQHC)': 'WageRelatedCostsRHC',
                'Total Salaries (adjusted)': 'SalariesAdjusted',
                'Contract Labor': 'ContractLabor',
                'Wage Related Costs for Part - A Teaching Physicians': 'WageRelatedCostsTeaching',
                'Wage Related Costs for Interns and Residents': 'WageRelatedCostsInternsResidents',
                'Cash on Hand and in Banks': 'Cash',
                'Temporary Investments': 'TemporaryInvestments',
                'Notes Receivable': 'NotesReceivable',
                'Accounts Receivable': 'AccountsReceivable',
                'Less: Allowances for Uncollectible Notes and Accounts Receivable': 'UncollectibleAccounts',
                'Inventory': 'Inventory',
                'Prepaid Expenses': 'PrepaidExpenses',
                'Other Current Assets': 'OtherCurrentAssets',
                'Total Current Assets': 'CurrentAssets',
                'Land': 'Land',
                'Land Improvements': 'LandImprovements',
                'Buildings': 'Buildings',
                'Leasehold Improvements': 'LeaseholdImprovements',
                'Fixed Equipment': 'FixedEquipment',
                'Major Movable Equipment': 'MovableEquipment',
                'Minor Equipment Depreciable': 'DepreciableEquipment',
                'Health Information Technology Designated Assets': 'HITAssets',
                'Total Fixed Assets': 'FixedAssets',
                'Investments': 'Investments',
                'Other Assets': 'OtherAssets',
                'Total Other Assets': 'TotalOtherAssets',
                'Total Assets': 'TotalAssets',
                'Accounts Payable': 'AccountsPayable',
                'Salaries, Wages, and Fees Payable': 'SalariesPayable',
                'Payroll Taxes Payable': 'PayrollTaxes',
                'Notes and Loans Payable (Short Term)': 'ShortTermLoans',
                'Deferred Income': 'DeferredIncome',
                'Other Current Liabilities': 'OtherLiabilities',
                'Total Current Liabilities': 'CurrentLiabilities',
                'Mortgage Payable': 'Mortgage',
                'Notes Payable': 'LongTermNotes',
                'Unsecured Loans': 'UnsecuredLoans',
                'Other Long Term Liabilities': 'OtherLongTermLiabilities',
                'Total Long Term Liabilities': 'LongTermLiabilities',
                'Total Liabilities': 'TotalLiabilities',
                'General Fund Balance': 'FundBalance',
                'Total Fund Balances': 'TotalFundBalances',
                'Total Liabilities and Fund Balances': 'LiabilitiesFundBalances',
                'DRG Amounts Other Than Outlier Payments': 'DRGNonOutliers',
                'DRG amounts before October 1': 'DRGBeforeOct',
                'DRG amounts after October 1': 'DRGAfterOct',
                'Outlier payments for discharges': 'OutlierPayments',
                'Disproportionate Share Adjustment': 'DisproportionateShare',
                'Allowable DSH Percentage': 'AllowableDSHPercentage',
                'Managed Care Simulated Payments': 'ManagedCarePayments',
                'Total IME Payment': 'IMEPayment',
                'Inpatient Revenue': 'InpatientRevenue',
                'Outpatient Revenue': 'OutpatientRevenue',
                'Gross Revenue': 'GrossRevenue',
                "Less Contractual Allowance and discounts on patients' accounts": 'ContractualAllowances',
                'Net Patient Revenue': 'NetPatientRevenue',
                'Less Total Operating Expense': 'OperatingExpenses',
                'Net Income from Service to Patients': 'ServiceIncome',
                'Total Other Income': 'OtherIncome',
                'Total Income': 'TotalIncome',
                'Total Other Expenses': 'OtherExpenses',
                'Net Income': 'NetIncome',
                'Cost To Charge Ratio': 'CostToChargeRatio',
                'Net Revenue from Medicaid': 'MedicaidRevenue',
                'Medicaid Charges': 'MedicaidCharges',
                'Net Revenue from Stand-Alone SCHIP': 'SCHIPRevenue',
                'Stand-Alone SCHIP Charges': 'SCHIPCharges',
            }

            df.rename(columns=column_mapping, inplace=True)

            convert_date = lambda date_str: (
                datetime.strptime(date_str, '%m-%d-%Y').strftime('%Y-%m-%d')
                if date_str and '-' in date_str
                else (
                    datetime.strptime(date_str, '%m/%d/%Y').strftime('%Y-%m-%d')
                    if date_str and '/' in date_str
                    else None
                )
            )

            for column in df.columns:
                if df[column].dtype == 'object':
                    df[column].fillna('', inplace=True)  # Replace NaN with an empty string for string columns
                else:
                    df[column].fillna(0, inplace=True)  # Replace NaN with 0 for numeric columns
            print(df.columns)
            for _, row in df.iterrows():
                data_dict = row.to_dict()
                for date_column in ['FiscalYearBegin', 'FiscalYearEnd']:
                    print(data_dict)
                    print(date_column, data_dict.get(date_column))
                    date_string = data_dict.get(date_column)
                    if date_string:
                        print(date_string, 'before')
                        data_dict[date_column] = convert_date(date_string)
                        print(data_dict[date_column], 'after')

                # print(data_dict)
                raw_data = RawData(**data_dict)
                # print(raw_data, "qwerty")
                raw_data.save()
                print("saved")

            return Response({"message": "Data uploaded successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
