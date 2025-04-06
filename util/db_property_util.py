import configparser

class DBPropertyUtil:
    @staticmethod
    def get_connection_string(filename: str) -> dict:
        config = configparser.ConfigParser()
        config.read(filename)

        print("DEBUG - Sections found:", config.sections())  # To verify if the section is loaded

        if 'database' not in config:
            raise Exception("Missing 'database' section in properties file")

        return {
            'host': config['database']['host'],
            'port': config['database']['port'],
            'user': config['database']['user'],
            'password': config['database']['password'],
            'database': config['database']['database']
        }

# Test this file directly
if __name__ == "__main__":
    props = DBPropertyUtil.get_connection_string("db.properties")
    print("Connection Properties:", props)
