import mysql.connector
import json
from functools import wraps
from typing import Callable, Dict, Any, Optional, Union
import getpass

class DBConfigError(Exception):
    """Exception raised for errors in the database configuration."""
    pass

def _load_db_config(config: Optional[str]) -> Dict[str, Any]:
    """
    Load database configuration from a JSON file.

    Args:
        config (Optional[str]): JSON file path.

    Returns:
        Dict[str, Any]: Parsed database configuration.

    Raises:
        DBConfigError: If configuration is invalid or file cannot be read.
    """
    if config:
        try:
            with open(config, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise DBConfigError(f"Error loading JSON config: {e}")
    else:
        raise DBConfigError("No configuration file provided.")

def db_connector(config: Optional[str] = None, 
                 host: Optional[str] = None, 
                 port: int = 3306, 
                 user: Optional[str] = None, 
                 password: Optional[str] = None,
                 database: Optional[str] = None) -> Callable:
    """
    Decorator for managing database connections.

    This decorator can be used with either a JSON file path or direct connection parameters.

    Args:
        config (Optional[str]): Path to a JSON file containing the database connection configuration.
        host (Optional[str]): Database host.
        port (int): Database port, default is 3306.
        user (Optional[str]): Database user.
        password (Optional[str]): Database password.
        database (Optional[str]): Database name to connect to.

    Returns:
        Callable: The decorated function with database connection management.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def with_connection(*args: Any, **kwargs: Any) -> Any:
            db_config = {}
            if config:
                db_config = _load_db_config(config)
            else:
                if not all([host, user]):
                    raise DBConfigError("Host and user must be provided if config is not specified.")

                db_config = {
                    'host': host,
                    'port': port,
                    'user': user,
                    'password': password or getpass.getpass(f"Enter password of user {user}: "),
                    'database': database
                }

            # Check for illegal parameter combinations
            if config and (host or user or password or port or database):
                raise DBConfigError("Cannot provide both 'config' and individual connection parameters.")

            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            try:
                result = func(cursor, *args, **kwargs)
                conn.commit()
            except Exception as e:
                conn.rollback()
                print(f"An error occurred: {e}")
                raise
            finally:
                cursor.close()
                conn.close()
            return result
        return with_connection
    return decorator
