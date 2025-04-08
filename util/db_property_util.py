import configparser

class DBPropertyUtil:
    @staticmethod
    def get_connection_string(file_path: str):
        config = configparser.ConfigParser()
        config.read(file_path)

        # Debugging: Print sections found in the file
        print("DEBUG - Sections found:", config.sections())

        if 'database' not in config:
            raise Exception("Missing 'database' section in properties file")

        db_config = config['database']
        return {
            'host': db_config.get('host'),
            'port': db_config.get('port'),
            'user': db_config.get('user'),
            'password': db_config.get('password'),
            'database': db_config.get('database')
        }