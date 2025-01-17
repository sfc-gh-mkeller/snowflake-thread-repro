import logging
import os
import threading

from snowflake import connector


def connect_to_snowflake() -> connector.SnowflakeConnection:
    return connector.connect(
        user=os.getenv("SNOWSQL_USER"),
        password=os.getenv("SNOWSQL_PWD"),
        account=os.getenv("SNOWSQL_ACCOUNT"),
    )


def main():
    # https://docs.snowflake.com/developer-guide/python-connector/python-connector-example#logging
    for logger_name in ["snowflake.connector", "botocore", "boto3"]:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        ch = logging.FileHandler("python_connector.log")
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(threadName)s %(filename)s:%(lineno)d - %(funcName)s() - %(levelname)s - %(message)s"
            )
        )
        logger.addHandler(ch)

    # spins up 30 threads, results in error ~20% of the time
    threads = list()
    for i in range(31):
        print(f"Starting thread {i}")
        thread = threading.Thread(target=connect_to_snowflake)
        threads.append(thread)
        thread.start()
    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
