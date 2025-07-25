import serial
import sys
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu

PORT = "502"

def main():

    # Connect to the slave
    master = modbus_rtu.RtuMaster(
        serial.Serial(port=PORT, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0)
    )
    master.set_timeout(5.0)
    master.set_verbose(True)
    '''
        1、READ_COILS H01 读线圈
        2、READ_DISCRETE_INPUTS H02 读离散输入
        3、READ_HOLDING_REGISTERS H03 读寄存器
        4、READ_INPUT_REGISTERS H04 读输入寄存器
        5、WRITE_SINGLE_COIL H05 写单一线圈
        6、WRITE_SINGLE_REGISTER H06 写单一寄存器
        7、WRITE_MULTIPLE_COILS H15 写多个线圈
        8、WRITE_MULTIPLE_REGISTERS H16 写多寄存器
    '''

    # 指令格式：机号 功能代码 起始地址 结束地址

    data = master.execute(1, cst.HOLDING_REGISTERS,0, 8)

if __name__ == "__main__":
    main()