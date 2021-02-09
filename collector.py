"""Collector

Copyright (c) 2021 Mathieu BARBE-GAYET
All Rights Reserved.
Released under the MIT license

"""
import time

import mysql.connector
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


def store_data(data, file):
    pass


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
            time.sleep(10)
            cpu = get_cpu_times()
            print(cpu)
            virt_mem = get_virtual_memory()
            print(virt_mem)
            disk = get_disk_usage()
            print(disk)
            counters = get_net_io_counters()
            print(counters)

            for nic_name in counters:
                host = "localhost"
                bytes_sent = counters[nic_name].bytes_sent
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
