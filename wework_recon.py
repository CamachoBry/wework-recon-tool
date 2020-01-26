#MySQL Connector
import mysql.connector

# Pandas
import pandas as pd

# Time
import datetime
date = datetime.datetime.now().date()

#OS
import os

#Streamlit
import streamlit as st

#SQLite for query connection test purposes (can delete after completed)
import sqlite3

#Application title
st.title('WeWork Reconcilation')

#Select box to allow choosing which region they want to connect to
region = st.selectbox("Please choose a region.", ['','US WEST', 'US EAST',
                                                  'APAC', 'EMEA', 'LATAM'])

#Select a date from - to for when to run the query (Between the two dates chosen)    
date_from = st.date_input('Please enter date from')
date_to = st.date_input('Please enter date to')                                              

#Upload box but only if CSV is in folder path of script
def file_selector(folder_path="./master-list"):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', filenames)
    return os.path.join(folder_path, selected_filename)


#Turns the master CSV into a dataframe for data manipulation
filename = file_selector()
master_list = pd.read_csv(filename)

#-----------------------------------------------------------------------------------------------------
#                       Database information per region
#-----------------------------------------------------------------------------------------------------
def useast_db():
    # Connect to server
    db = mysql.connector.connect(
    
        # host for USEAST
        host='host-name',
        port=3306,
        user="user",
        password="password",
        database="database"
    )
     # Get a cursor
    cur = db.cursor()
    
    #Query ran on region database to pull display_name, IP, serial number
    query = pd.read_sql_query(f"""SELECT display_name, physical_printer_id, serial_number
                 FROM tbl_printer
                 WHERE server_name = 'device'
                 AND deleted = 'N'
                 AND created_date between '{date_from}' AND '{date_to}' """ , db)
    
    # st.write(query)

    #Devices that are 'completely white' and are ready to bill (brand new devices)
    new_devices = query[~query['display_name'].str.lower().isin(master_list['display_name'].str.lower()) & ~query['serial_number'].isin(master_list['serial_number'])]

    #Devices that both the serial number and device name are in master 
    in_master = query[query['display_name'].str.lower().isin(master_list['display_name'].str.lower()) & query['serial_number'].isin(master_list['serial_number'])]

    #Devices that need to be checked
    check = query[~query.isin(new_devices) & ~query.isin(in_master)].dropna() 

    st.write('\n')
    st.write('TO BE BILLED')
    st.write(new_devices)

    #Saves TO BE BILLED dataframe to CSV file to importing
    if st.checkbox('Download TO BE BILLED CSV'):
        new_devices.to_csv(f'./TO_BE_BILLED/US_EAST_TO_BE_BILLED_{date}.csv')

    st.write('\n')
    st.write('TO BE CHECKED')
    st.write(check)

    #Saves TO BE BILLED dataframe to CSV file to importing
    if st.checkbox('Download TO BE CHECKED CSV'):
        check.to_csv(f'./TO_BE_CHECKED/US_EAST_TO_BE_CHECKED_{date}.csv')

def uswest_db():

    # Connect to server
    db = mysql.connector.connect(
    
        # host for USEAST
        host='host-name',
        port=3306,
        user="user",
        password="password",
        database="database"
    )
     # Get a cursor
    cur = db.cursor()

    #Query ran on region database to pull display_name, IP, serial number
    query = pd.read_sql_query(f"""SELECT display_name, physical_printer_id, serial_number
                 FROM tbl_printer
                 WHERE server_name = 'device'
                 AND deleted = 'N'
                 AND created_date between '{date_from}' AND '{date_to}' """ , db)
    
    #Devices that are 'completely white' and are ready to bill (brand new devices)
    new_devices = query[~query['display_name'].str.lower().isin(master_list['display_name'].str.lower()) & ~query['serial_number'].isin(master_list['serial_number'])]

    #Devices that both the serial number and device name are in master 
    in_master = query[query['display_name'].str.lower().isin(master_list['display_name'].str.lower()) & query['serial_number'].isin(master_list['serial_number'])]

    #Devices that need to be checked
    check = query[~query.isin(new_devices) & ~query.isin(in_master)].dropna() 

    #TO BE BILLED dataframe
    st.write('\n')
    st.write('TO BE BILLED')
    st.write(new_devices)

    #Saves TO BE BILLED dataframe to CSV file to importing
    if st.checkbox('Download TO BE BILLED CSV'):
        new_devices.to_csv(f'./TO_BE_BILLED/US_WEST_TO_BE_BILLED_{date}.csv')

    #TO BE CHECKED dataframe
    st.write('\n')
    st.write('TO BE CHECKED')
    st.write(check)

    #Saves TO BE BILLED dataframe to CSV file to importing
    if st.checkbox('Download TO BE CHECKED CSV'):
        check.to_csv(f'./TO_BE_CHECKED/US_WEST_TO_BE_CHECKED_{date}.csv')

def apac_db():

    # Connect to server
    db = mysql.connector.connect(
    
        # host for USEAST
        host='host-name',
        port=3306,
        user="user",
        password="password",
        database="database"
    )
    # Get a cursor
    cur = db.cursor()

    #Query ran on region database to pull display_name, IP, serial number
    query = pd.read_sql_query(f"""SELECT display_name, physical_printer_id, serial_number
                 FROM tbl_printer
                 WHERE server_name = 'device'
                 AND deleted = 'N'
                 AND created_date between '{date_from}' AND '{date_to}' """ , db)
    
    #Devices that are 'completely white' and are ready to bill (brand new devices)
    new_devices = query[~query['display_name'].str.lower().isin(master_list['display_name'].str.lower()) & ~query['serial_number'].isin(master_list['serial_number'])]

    #Devices that both the serial number and device name are in master 
    in_master = query[query['display_name'].str.lower().isin(master_list['display_name'].str.lower()) & query['serial_number'].isin(master_list['serial_number'])]

    #Devices that need to be checked
    check = query[~query.isin(new_devices) & ~query.isin(in_master)].dropna() 

    #TO BE BILLED dataframe
    st.write('\n')
    st.write('TO BE BILLED')
    st.write(new_devices)

    #Saves TO BE BILLED dataframe to CSV file to importing
    if st.checkbox('Download TO BE BILLED CSV'):
        new_devices.to_csv(f'./TO_BE_BILLED/TO_BE_BILLED\APAC_TO_BE_BILLED_{date}.csv')

    #TO BE CHECKED dataframe
    st.write('\n')
    st.write('TO BE CHECKED')
    st.write(check)

    #Saves TO BE BILLED dataframe to CSV file to importing
    if st.checkbox('Download TO BE CHECKED CSV'):
        check.to_csv(f'./TO_BE_CHECKED/TO_BE_CHECKED\APAC_TO_BE_CHECKED_{date}.csv')

def emea_db():
    # Connect to server
     db = mysql.connector.connect(
    
        # host for USEAST
        host='host-name',
        port=3306,
        user="user",
        password="password",
        database="database"
    )
    # Get a cursor
    cur = db.cursor()

    #Query ran on region database to pull display_name, IP, serial number
    query = pd.read_sql_query(f"""SELECT display_name, physical_printer_id, serial_number
                 FROM tbl_printer
                 WHERE server_name = 'device'
                 AND deleted = 'N'
                 AND created_date between '{date_from}' AND '{date_to}' """ , db)
    
    # st.write(query)

    #Devices that are 'completely white' and are ready to bill (brand new devices)
    new_devices = query[~query['display_name'].str.lower().isin(master_list['display_name'].str.lower()) & ~query['serial_number'].isin(master_list['serial_number'])]

    #Devices that both the serial number and device name are in master 
    in_master = query[query['display_name'].str.lower().isin(master_list['display_name'].str.lower()) & query['serial_number'].isin(master_list['serial_number'])]

    #Devices that need to be checked
    check = query[~query.isin(new_devices) & ~query.isin(in_master)].dropna() 

    #Checks for duplicates in device name or serial number within the query list itself
    # check1 = query[query.duplicated('display_name', keep=False) | query.duplicated('serial_number', keep=False)]
    # check = pd.concat([check,check1])

    st.write('\n')
    st.write('TO BE BILLED')
    st.write(new_devices)

    #Saves TO BE BILLED dataframe to CSV file to importing
    if st.checkbox('Download TO BE BILLED CSV'):
        new_devices.to_csv(f'./TO_BE_BILLED/EMEA_TO_BE_BILLED_{date}.csv')

    st.write('\n')
    st.write('TO BE CHECKED')
    st.write(check)

    #Saves TO BE BILLED dataframe to CSV file to importing
    if st.checkbox('Download TO BE CHECKED CSV'):
        check.to_csv(f'./TO_BE_CHECKED/EMEA_TO_BE_CHECKED_{date}.csv')

def latam_db():
    # Connect to server
     db = mysql.connector.connect(
    
        # host for USEAST
        host='host-name',
        port=3306,
        user="user",
        password="password",
        database="database"
    )
    # Get a cursor
    cur = db.cursor()

    #Query ran on region database to pull display_name, IP, serial number
    query = pd.read_sql_query(f"""SELECT display_name, physical_printer_id, serial_number
                 FROM tbl_printer
                 WHERE server_name = 'device'
                 AND deleted = 'N'
                 AND created_date between '{date_from}' AND '{date_to}' """ , db)
    
    # st.write(query)

    #Devices that are 'completely white' and are ready to bill (brand new devices)
    new_devices = query[~query['display_name'].str.lower().isin(master_list['display_name'].str.lower()) & ~query['serial_number'].isin(master_list['serial_number'])]

    #Devices that both the serial number and device name are in master 
    in_master = query[query['display_name'].str.lower().isin(master_list['display_name'].str.lower()) & query['serial_number'].isin(master_list['serial_number'])]

    #Devices that need to be checked
    check = query[~query.isin(new_devices) & ~query.isin(in_master)].dropna() 

    st.write('\n')
    st.write('TO BE BILLED')
    st.write(new_devices)

    #Saves TO BE BILLED dataframe to CSV file to importing
    if st.checkbox('Download TO BE BILLED CSV'):
        new_devices.to_csv(f'./TO_BE_BILLED/LATAM_TO_BE_BILLED_{date}.csv')

    st.write('\n')
    st.write('TO BE CHECKED')
    st.write(check)

    #Saves TO BE BILLED dataframe to CSV file to importing
    if st.checkbox('Download TO BE CHECKED CSV'):
        check.to_csv(f'./TO_BE_CHECKED/LATAM_TO_BE_CHECKED_{date}.csv')



#IF-ELSE that switches between each region when picked in the drop-down menu   
if region == 'US EAST':
    useast_db() 
elif region == 'US WEST':
    uswest_db()
elif region == 'APAC':
    apac_db()
elif region == 'EMEA':
    emea_db()
elif region == 'LATAM':
    latam_db()
else:
    return st.write("Error")

