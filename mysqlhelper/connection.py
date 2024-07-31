import mysql.connector
import json
from functools import wraps
from typing import Callable, Dict, Any, Optional, Union

class DBConfigError(Exception):
    """Exception raised for errors in the database configuration."""
    pass

def _load_db_config(config: Union[Dict[str, str], str, None]) -> Dict[str, str]:
    """
    Load database configuration.

    Args:
        config (Union[Dict[str, str], str, None]): Configuration dictionary, JSON file path, or None.

    Returns:
        Dict[str, str]: Parsed database configuration.

    Raises:
        DBConfigError: If configuration is invalid or file cannot be read.
    """
    if isinstance(config, str):
        try:
            with open(config, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise DBConfigError(f"Error loading JSON config: {e}")
    elif isinstance(config, dict):
        return config
    elif config is None:
        raise DBConfigError("No configuration provided.")
    else:
        raise DBConfigError("Invalid configuration format.")

def db_connector(**config: Optional[Dict[str, str]]) -> Callable:
    """
    Decorator for managing database connections.

    This decorator can be used with either a configuration dictionary, 
    a JSON file path, or direct connection parameters.

    Args:
        config (Optional[Dict[str, str]]): Database connection configuration.

    Returns:
        Callable: The decorated function with database connection management.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def with_connection(*args: Any, **kwargs: Any) -> Any:
            db_config = _load_db_config(config)
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
