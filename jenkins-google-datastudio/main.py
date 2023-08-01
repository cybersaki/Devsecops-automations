import csv
import xlsxwriter
import pandas as pd

complaince_report = []
# Report format
# "Serial Number", "Workstation", "Model", "NETWORKDEVICE1", "NETWORKDEVICE2", "NETWORKDEVICE3", "NETWORKDEVICE4", "State", "MAC Address", "REDACTED"
header = ["Serial Number", "Workstation", "Model", "NETWORKDEVICE1", "NETWORKDEVICE2", "NETWORKDEVICE3", "NETWORKDEVICE4", "NETWORKDEVICE5", "NETWORKDEVICE6", "NETWORKDEVICE7", "Encryption", "State", "MAC Address", "REDACTED"]

def read_data_from_csv(filename):
    file = open(filename, "r")
    data = list(csv.reader(file, delimiter=","))
    file.close()
    return data

def check_complaince(asset_inventory, NETWORKDEVICE1, NETWORKDEVICE2, NETWORKDEVICE3, NETWORKDEVICE4, NETWORKDEVICE5, NETWORKDEVICE6):
    temp = []
    for data in asset_inventory[6:]:
        NETWORKDEVICE1_flag = 0
        NETWORKDEVICE2_flag = 0
        NETWORKDEVICE3_flag = 0
        NETWORKDEVICE4_flag = 0
        NETWORKDEVICE5_flag_only = 0
        NETWORKDEVICE5_flag = 0
        NETWORKDEVICE5_encryption_flag = 0
        windows_flag = 0
        only_mac = 0
        NETWORKDEVICE6_flag = 0
        for NETWORKDEVICE1_list in NETWORKDEVICE1:
            if data[10] == NETWORKDEVICE1_list[25]:
                NETWORKDEVICE1_flag += 1
                break
        for NETWORKDEVICE2_list in NETWORKDEVICE2:
            if data[10] == NETWORKDEVICE2_list[7]:
                NETWORKDEVICE2_flag += 1
                break
        for NETWORKDEVICE3_list in NETWORKDEVICE3:
            if data[0] == NETWORKDEVICE3_list[4]:
                NETWORKDEVICE3_flag += 1
                break
        for NETWORKDEVICE4_list in NETWORKDEVICE4:
            if data[0] == NETWORKDEVICE4_list[0]:
                NETWORKDEVICE4_flag += 1
                break
        for NETWORKDEVICE5_list_only in NETWORKDEVICE5:
            if not "windows" in  data[1].lower():
                only_mac += 1 
                if data[10] == NETWORKDEVICE5_list_only[3]:
                    NETWORKDEVICE5_flag_only += 1
                    break
        for NETWORKDEVICE5_list in NETWORKDEVICE5:
            if data[10] == NETWORKDEVICE5_list[3]:
                NETWORKDEVICE5_flag += 1
                if (NETWORKDEVICE5_list[2] == "Boot Partitions Encrypted"):
                    NETWORKDEVICE5_encryption_flag += 1
                break
        for NETWORKDEVICE7_list in NETWORKDEVICE7:
            if NETWORKDEVICE7_list[6] == "Dell Inc." or NETWORKDEVICE7_list[6] == "HP" or NETWORKDEVICE7_list[6] == "LENOVO":
                if data[3] == NETWORKDEVICE7_list[7]:
                    windows_flag += 1
                    if NETWORKDEVICE7_list[29] == "Fully Encrypted":
                        NETWORKDEVICE6_flag += 1
                    break
        temp.append(data[10])
        temp.append(data[0])
        temp.append(data[2])
        if NETWORKDEVICE1_flag >= 1:
            temp.append("Complaint")
        else:
            temp.append("Non - Complaint")
        if NETWORKDEVICE2_flag >= 1:
            temp.append("Complaint")
        else:
            temp.append("Non - Complaint")
        if NETWORKDEVICE3_flag >= 1:
            temp.append("Complaint")
        else:
            temp.append("Non - Complaint")
        if NETWORKDEVICE4_flag >= 1:
            temp.append("Complaint")
        else:
            temp.append("Non - Complaint")


        if only_mac>= 1 and NETWORKDEVICE5_flag_only >= 1:
            temp.append("Complaint")
        elif only_mac>= 1 and NETWORKDEVICE5_flag_only >= 0:
            temp.append("Non - Complaint")
        else:
            temp.append("Not Applicable")

        NETWORKDEVICE5_enc = ""
        windows_enc = ""

        if NETWORKDEVICE5_flag >= 1 and NETWORKDEVICE5_encryption_flag >= 1:
            NETWORKDEVICE5_enc = "Complaint"
            temp.append("Complaint")
        elif NETWORKDEVICE5_flag >= 1 and NETWORKDEVICE5_encryption_flag <= 0:
            NETWORKDEVICE5_enc = "Non - Complaint"
            temp.append("Non - Complaint")
        else:
            NETWORKDEVICE5_enc = "Not Applicable"
            temp.append("Not Applicable")

        
        if windows_flag >= 1 and NETWORKDEVICE6_flag >= 1:
            windows_enc = "Complaint"
            temp.append("Complaint")
        elif windows_flag >= 1 and NETWORKDEVICE6_flag <= 0:
            windows_enc = "Non - Complaint"
            temp.append("Non - Complaint")
        else:
            windows_enc = "Not Applicable"
            temp.append("Not Applicable")

        if NETWORKDEVICE5_enc == "Complaint" or windows_enc == "Complaint":
            temp.append("Complaint")
        else:
            temp.append("Non - Complaint")

        complaince_report.append(temp)
        temp.append(data[5])
        temp.append(data[6])
        temp.append(data[11])
        temp = []
    return complaince_report


def write_complaince_report(complaince_report):
    workbook = xlsxwriter.Workbook('test.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.set_column("A:Z",30)
    cell_format = workbook.add_format()
    cell_format.set_bottom(1)
    cell_format.set_top(1)
    cell_format.set_left(1)
    cell_format.set_right(1)
    cell_format.set_size(13)
    for row_num, row_data in enumerate(complaince_report):
        for col_num, col_data in enumerate(row_data):
            worksheet.write(row_num, col_num, col_data, cell_format)
    workbook.close()


def format_excel(complaince_report):
    df = pd.DataFrame(complaince_report, columns=header)
    writer = pd.ExcelWriter('Result.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    
    workbook  = writer.book
    worksheet = writer.sheets['Sheet1']

    (max_row, max_col) = df.shape
    column_settings = [{'header': column} for column in df.columns]
    worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})
    worksheet.set_column(0, max_col - 1, 12)

    worksheet.set_column("A:J", 30)
    red_format = workbook.add_format({'color':'red'})
    green_format = workbook.add_format({'color':'green'})
    yellow_format = workbook.add_format({'color':'yellow'})

    worksheet.conditional_format('A1:Z15000', {'type': 'text', 'criteria': 'containing', 'value': 'Non - Complaint', 'format': red_format})
    worksheet.conditional_format('A1:Z15000', {'type': 'text', 'criteria': 'containing', 'value': 'Complaint', 'format':  green_format})
    worksheet.conditional_format('A1:Z15000', {'type': 'text', 'criteria': 'containing', 'value': 'Not Applicable', 'format':  yellow_format})

    writer.save()

filename = "Files/AssetInventory.csv"
asset_inventory = read_data_from_csv(filename)

filename = "Files/NETWORKDEVICE1.csv"
NETWORKDEVICE1 = read_data_from_csv(filename)

filename = "Files/NETWORKDEVICE2.csv"
NETWORKDEVICE2 = read_data_from_csv(filename)

filename = "Files/NETWORKDEVICE3.csv"
NETWORKDEVICE3 = read_data_from_csv(filename)

filename = "Files/NETWORKDEVICE4.csv"
NETWORKDEVICE4 = read_data_from_csv(filename)

filename = "Files/NETWORKDEVICE5.csv"
NETWORKDEVICE5 = read_data_from_csv(filename)

filename = "Files/NETWORKDEVICE6.csv"
NETWORKDEVICE7 = read_data_from_csv(filename)


complaince_report = check_complaince(asset_inventory, NETWORKDEVICE1, NETWORKDEVICE2, NETWORKDEVICE3, NETWORKDEVICE4, NETWORKDEVICE5, NETWORKDEVICE7)
write_complaince_report(complaince_report)
format_excel(complaince_report)
