# Importing the libraries
import pandas as pd


# This function grabs the address data from APPRAISAL_INFO.TXT
def getAddressData():
    df = pd.read_csv('data/2022-03-08_005901_APPRAISAL_INFO.TXT', sep='\t', header=None, encoding='latin-1', on_bad_lines='skip')
    df['prop_id'] = df[0].str[:12]
    df['prop_type_cd'] = df[0].str[12:17]
    df['prop_val_yr'] = df[0].str[18:22]
    df['imprv_state_cd'] = df[0].str[63:68]
    df['geo_id'] = df[0].str[546:596]
    df['Situs/Location Street Prefix'] = df[0].str[1039:1049]
    df['Situs/Location Street'] = df[0].str[1049:1099]
    df['Situs/Location Street Suffix'] = df[0].str[1099:1109]
    df['Situs/Location City'] = df[0].str[1109:1139]
    df['Situs/Location Zip'] = df[0].str[1139:1149]
    df['imprv_state_cd'] = df[0].str[2731:2741]
    df['imprv_state_cd'].replace(
        {'A1        ': 'SINGLE FAMILY RES',
        'F1        ': 'COMMERCIAL REAL PROPERTY',
        'B1        ' : 'MULTIFAMILY RESIDENCE',
        'F3        ':'NOMINAL ANCILLARY IMPROVEMENTS',
        'B2        ':'MULTIFAMILY OVER 4 UNITS',
        'F2        ': 'INDUSTRIAL AND MANUFACTURING REAL PROPERTY',
        'B6        ':'HOMESTEADED MULTIFAMLIY RESIDENCE',
        'J4        ':'TELEPHONE COMPANY',
        'A2        ':'MOBILE HOME WITH LAND',
        'O2        ':'IMPROVED INVENTORY',
        'C1        ': 'SMALL VACANT TRACTS OF LAND',
        'A         ':'SINGLE FAMILY RESIDENTIAL',
        'J7        ':'CABLE TELEVISION',
        'A3        ':'NOMINAL ANCILLARY IMPROVEMENTS',
        'M1        ':'MOBILE HOME ONLY ON LAND WITH DIFFERENT OWNERSHIP',
        'E1        ':'RES IMPS ON RURAL LAND, & NON QUALIFIED OPEN SPACE',
        'D2        ':'FARM AND RANCH IMPROVEMENTS ON QUALIFIED LAND',
        'E2        ':'MOBILE HOME ON RURAL LAND',
        'J2        ': 'GAS DISTRIBUTION',
        'J1        ':'WATER SYSTEMS',
        'X         ':'TOTALLY EXEMPT PROPERTY',
        'D5        ':'NOT IN USE',
        'J3        ':'ELECTRICAL COMPANY'}, inplace=True)
    df.drop(df.columns[0], axis=1, inplace=True)

    return df

# This function grabs the AC data from APPRAISAL_IMPROVEMENT_DETAIL_ATTR.TXT. It filters for only cooling attribute description.
def getACData():
    df = pd.read_csv('data/2022-03-08_005901_APPRAISAL_IMPROVEMENT_DETAIL_ATTR.TXT', sep='\t', header=None)

    df['prop_id'] = df[0].str[:12]
    df['year'] = df[0].str[12:16]
    df['Improvement ID'] = df[0].str[16:28]
    df['Improvement Detail ID'] = df[0].str[28:40]
    df['Improvement Attribute ID'] = df[0].str[40:52]
    df['Attribute Description'] = df[0].str[52:77]
    df['Attribute Code'] = df[0].str[77:87]
    # Use pandas.replace to replace the values in the Attribute Code column
    df['Attribute Code'].replace({'C         ' : 'Central', 'N         ' : 'None', 'O         ':'Other', 'S         ':'Solar', 'Y         ': 'Yes'}, inplace=True)

    df.drop(df.columns[0], axis=1, inplace=True)

    # Filter dataframe to include only records that have Cooling in the 'Attribute Description' column
    cooling_df = df[df['Attribute Description'].str.contains('Cooling')]
    return cooling_df

print('Getting address data...')
address_df = getAddressData()
print('Getting AC data...')
ac_df = getACData()
print('Merging dataframes...')
merged_df = pd.merge(ac_df, address_df, on='prop_id', how='inner')


# print('Exportng to XLSX...')
# merged_df.head(round(len(merged_df) * 0.1)).to_excel('output/replication.xlsx', index=False)
