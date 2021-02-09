"""Collector

Copyright (c) 2021 Mathieu BARBE-GAYET
All Rights Reserved.
Released under the MIT license

"""
import time
from datetime import datetime

import psutil


def get_cpu_times():
    """Get cpu usage for each core
    """
    return psutil.cpu_times(percpu=True)


def get_virtual_memory():
    """Get virtual memory usage
    """
    return psutil.virtual_memory()


def get_disk_usage():
    """Get rom usage
    """
    return psutil.disk_usage('/')


def get_net_io_counters():
    """Get the net I/O counters
    """
    return psutil.net_io_counters(
        pernic=True,
        nowrap=False,
    )


def store_data(data, file_name):
    now = str(datetime.now())
    file_handle = open(file_name, "a")
    file_handle.write(now + " " + str(data) + "\n")
    file_handle.close()


# def write_to_db(sqlstatement):
#     """Write to MariaDB
#     """
#     try:
#         conn = mariadb.connect(
#                 user="root",
#                 password="zvxmhwfn",
#                 host="127.0.0.1",
#                 port=3306,
#                 database="supervision"
#         )
#     except mariadb.Error as e:
#         print(f"Error connecting to MariaDB Platform: {e}")
#         return
#     cur = conn.cursor()
#     cur.execute(sqlstatement)
#     conn.commit()
#     conn.close()
#     print(sqlstatement)


def main():
    """The main function"""
    while True:
        try:
            time.sleep(5)
            now = datetime.now()
            dtf = "%d%m%Y"
            cpu = get_cpu_times()
            store_data(cpu, "./" + now.strftime(dtf) + "-cpu.log")
            print(datetime.now(), cpu)

            virtual_mem = get_virtual_memory()
            store_data(virtual_mem, "./" + now.strftime(dtf) + "-virtual_mem.log")
            print(datetime.now(), virtual_mem)

            disk = get_disk_usage()
            store_data(disk, "./" + now.strftime(dtf) + "-disk.log")
            print(datetime.now(), disk)

            net_usage = get_net_io_counters()
            store_data(net_usage, "./" + now.strftime(dtf) + "-net_usage.log")
            print(datetime.now(), net_usage)

            for nic_name in net_usage:
                host = "localhost"
                bytes_sent = net_usage[nic_name].bytes_sent
                # sqlstatement = f"INSERT INTO " \
                #                f"net_io_counter " \
                #                f"(" \
                #                f"host," \
                #                f" nic, " \
                #                f"bytes_sent" \
                #                f") " \
                #                f"VALUES (" \
                #                f"'{host}'," \
                #                f" '{nic_name}', " \
                #                f"'{bytes_sent}')"
                # write_to_db(sqlstatement)
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    main()
