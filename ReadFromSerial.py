import serial

ser = serial.Serial('COM5', 115200)  # Replace 'COM1' with the appropriate port name
output_file = 'EMG_data.csv'
dictValues={}
i=0
with open(output_file, 'w') as file:
    while True:
        if ser.in_waiting > 0:
            value = ser.readline().decode('utf-8', errors='ignore').strip()
            if value != '':
                value_float = float(value)
                file.write(str(i) + ','  + str(value_float) + '\n')
                dictValues[i]=value_float
                i=i+1
                print(dictValues)
