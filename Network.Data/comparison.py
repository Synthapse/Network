
# 152 534 records
import pandas as pd

# Read the Excel file
df_2014 = pd.read_excel("fixed-broadband-speeds-postcode-london-2014.xlsx", engine="openpyxl")
df_2021 = pd.read_csv("performance_postcode_files/202105_fixed_pc_performance_r01_BR.csv")

# Display the first few rows
filtered_df_2014 = df_2014[df_2014["pcd_nospaces"].str.startswith("BR", na=False)]
print(filtered_df_2014)

# Sum specific columns
columns_to_sum = [
    "Numberofconnections2MbitsbyPCnumberoflines",
    "Numberofconnections210MbitsbyPCnumberoflines",
    "Numberofconnections1030MbitsbyPCnumberoflines",
    "Numberofconnections30MbitsbyPCnumberoflines"
]

columns_to_sum2 = [
    "Number of connections < 2 Mbit/s (number of lines)",
    "Number of connections 30<300 Mbit/s (number of lines)",
    "Number of connections >= 300 Mbit/s (number of lines)",
    "Number of connections 10<30 Mbit/s (number of lines)"
]



df_2021[columns_to_sum2] = df_2021[columns_to_sum2].apply(pd.to_numeric, errors='coerce')


# Convert columns to numeric (forcing errors='coerce' to handle non-numeric values)
filtered_df_2014[columns_to_sum] = filtered_df_2014[columns_to_sum].apply(pd.to_numeric, errors='coerce')

# Sum the numeric values
summed_values = filtered_df_2014[columns_to_sum].sum()
summed_values2 = df_2021[columns_to_sum2].sum()

# Display the result
print(summed_values)
print(summed_values2)

# Brent District

#Logical Lines (Network Configuration)
# In some telecom and ISP contexts, "lines" may refer to logical connections, like VLANs or virtual circuits, rather than physical infrastructure.

# 2014

# Numberofconnections2MbitsbyPCnumberoflines        2757.0
# Numberofconnections210MbitsbyPCnumberoflines     27545.0
# Numberofconnections1030MbitsbyPCnumberoflines    27709.0
# Numberofconnections30MbitsbyPCnumberoflines      40444.0

# 2021

#Number of connections < 2 Mbit/s (number of lines)         280
#Number of connections 30<300 Mbit/s (number of lines)    82314
#Number of connections >= 300 Mbit/s (number of lines)     9113
#Number of connections 10<30 Mbit/s (number of lines)     14677

# Huge drop in sub-2 Mbit/s connections (from 2,757 to 280) → Indicates near elimination of extremely slow broadband.
# Massive growth in mid-to-high speed categories (30-300 Mbit/s) → Suggests the impact of fiber broadband (FTTC/FTTP) rollout.
# New ≥ 300 Mbit/s category introduced, meaning ultrafast broadband (Gigabit-capable connections) became a notable segment by 2021.

# FTTC and FTTP are NOT wireless –
# they are both fixed-line broadband technologies 
# that use fiber-optic cables to transmit data.
# However, once the internet reaches your home, you can use Wi-Fi (wireless) to connect your devices.

#Numberofconnections2MbitsbyPCnumberoflines
#Numberofconnections210MbitsbyPCnumberoflines
#Numberofconnections1030MbitsbyPCnumberoflines
#Numberofconnections30MbitsbyPCnumberoflines

# Number of connections < 2 Mbit/s (number of lines),
# Number of connections 2<5 Mbit/s (number of lines),
# Number of connections 5<10 Mbit/s (number of lines),
# Number of connections 10<30 Mbit/s (number of lines),
# Number of connections 30<300 Mbit/s (number of lines),
# Number of connections >= 300 Mbit/s (number of lines),
# Number of connections >= 30 Mbit/s (number of lines),


# BR
# CR
# DA
# E
# EN
# HA
# IG
# KT
# N
# NW
# RM
# SE
# SM
# SW
# TW
# UB
# W
# WC
# WD