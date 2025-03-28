"""System Metrics Collector for Grafana

Copyright (c) 2021 Mathieu BARBE-GAYET
All Rights Reserved.
Released under the MIT license

"""
import time
from datetime import datetime
import mariadb
import psutil
import logging


def get_cpu_percent():
    """Get cpu usage

    Returns: CPU usage percentage in a dictionary

    Available fields : cpu_percent
    """
    stats = psutil.cpu_percent(
        interval=None,
        percpu=False
    )

    # Here, a dictionary is used and returned in case if we want to monitor each cpu core later
    stats_dict = {
        "cpu_percent": str(stats)
    }
    return stats_dict


def get_virtual_memory():
    """Get the virtual memory stats

    Returns: The virtual memory in a dictionary

    Available fields : total, available, percent, used, free
    """
    stats = psutil.virtual_memory()
    stats_dict = {
        "total": str(stats.total),
        "available": str(stats.available),
        "percent": str(stats.percent),
        "used": str(stats.used),
        "free": str(stats.free),
    }
    return stats_dict


def get_disk_usage():
    """Get rom usage

    Returns: Disk usage in a dictionary

    Available fields : total, used, free, percent
    """
    stats = psutil.disk_usage('/')
    stats_dict = {
        "total": str(stats.total),
        "used": str(stats.used),
        "free": str(stats.free),
        "percent": str(stats.percent)
    }
    return stats_dict


def get_net_io_counters():
    """Get the net I/O counters

    Returns: The NIC usage in a dictionary

    Available fields : bytes_sent, bytes_recv, packets_sent, packets_recv
    """
    stats = psutil.net_io_counters(
        pernic=False,
        nowrap=False,
    )
    stats_dict = {
        "bytes_sent": str(stats.bytes_sent),
        "bytes_recv": str(stats.bytes_recv),
        "packets_sent": str(stats.packets_sent),
        "packets_recv": str(stats.packets_recv)
    }
    return stats_dict


def get_cpu_statement(cpu_dict):
    """Builds the statement for cpu usage

    Args:
        cpu_dict (dict): Contains a set of stats related to cpu usage

    Returns: The statement for cpu usage
    """
    sql_statement = f"INSERT INTO cpu_percent " \
                    f"(percent) " \
                    f"VALUES " \
                    f"({cpu_dict['cpu_percent']})"
    return sql_statement


def get_mem_statement(mem_dict):
    """Builds the sql statement for virtual memory usage

    Args:
        mem_dict (dict): Contains a set of stats related to memory usage

    Returns: The sql statement for virtual memory usage
    """
    sql_statement = f"INSERT INTO virtual_mem " \
                    f"(total, available, percent, used, free) " \
                    f"VALUES " \
                    f"({mem_dict['total']}," \
                    f"{mem_dict['available']}," \
                    f"{mem_dict['percent']}," \
                    f"{mem_dict['used']}," \
                    f"{mem_dict['free']})"
    return sql_statement


def get_disk_statement(disk_dict):
    """Builds the sql statement for disk usage

    Args:
        disk_dict (dict): Contains a set of stats related to disk usage

    Returns: The sql statement for disk usage
    """
    sql_statement = f"INSERT INTO disk " \
                    f"(total, used, free, percent) " \
                    f"VALUES " \
                    f"({disk_dict['total']}," \
                    f"{disk_dict['used']}," \
                    f"{disk_dict['free']}," \
                    f"{disk_dict['percent']})"
    return sql_statement


def get_net_io_statement(net_dict):
    """Builds the sql statement for network usage

    Args:
        net_dict (dict): Contains a list of stats related to network usage

    Returns: The sql statement for network usage
    """
    sql_statement = f"INSERT INTO net_usage " \
                    f"(bytes_sent, bytes_recv, packets_sent, packets_recv) " \
                    f"VALUES " \
                    f"({net_dict['bytes_sent']}," \
                    f"{net_dict['bytes_recv']}," \
                    f"{net_dict['packets_sent']}," \
                    f"{net_dict['packets_recv']})"
    return sql_statement


def store_data_to_file(data, file_name):
    """Write string into a file

    Args:
        data (dict): The data to insert into the file, stored in a dictionary
        file_name (str): The file name to create with the open() function

    Returns: None
    """
    now = str(datetime.now())
    file_handle = open(file_name, "a")
    file_handle.write(now + " " + str(data) + "\n")
    file_handle.close()


def write_to_db(sql_statement):
    """Write to the database

    Args:
        sql_statement (str) : the SQL statement to execute
    """

    # Connexion to DB
    try:
        conn = mariadb.connect(
            user="root",
            password="root",
            host="127.0.0.1",
            port=3306,
            database="monitoring"
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return

    # Cursor create
    cur = conn.cursor()

    # Execute SQL statement
    cur.execute(sql_statement)

    # Commit DB
    conn.commit()

    # Close connection
    conn.close()

    print(sql_statement)


def main():
    """The main function"""
    while True:
        try:
            time.sleep(5)

            # Get the current timestamp to write in the log files
            dtf = "%d%m%Y"
            date = datetime.now().strftime(dtf)

            # For each statistic we monitor, we try to:
            # 1/ get the stats from psutils
            # 2/ store it into a dedicated log file
            # 3/ build a statement
            # 4/ use the statement to write statistics into the database
            try:
                cpu_percent = get_cpu_percent()
                store_data_to_file(cpu_percent, "./" + date + "-cpu_percent.log")
                cpu_statement = get_cpu_statement(cpu_percent)
                write_to_db(cpu_statement)
            except Exception as e:
                logging.error(date, 'CPU usage collection failed.', exc_info=e)

            try:
                virtual_mem = get_virtual_memory()
                store_data_to_file(virtual_mem, "./" + date + "-virtual_mem.log")
                mem_statement = get_mem_statement(virtual_mem)
                write_to_db(mem_statement)
            except Exception as e:
                logging.error(date, 'Virtual memory usage collection failed.', exc_info=e)

            try:
                disk = get_disk_usage()
                store_data_to_file(disk, "./" + date + "-disk.log")
                disk_statement = get_disk_statement(disk)
                write_to_db(disk_statement)
            except Exception as e:
                logging.error(date, 'Disk usage collection failed.', exc_info=e)

            try:
                net_usage = get_net_io_counters()
                store_data_to_file(net_usage, "./" + date + "-net_usage.log")
                net_io_statement = get_net_io_statement(net_usage)
                write_to_db(net_io_statement)
            except Exception as e:
                logging.error(date, 'Network card usage collection failed.', exc_info=e)

        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    main()
