from re import sub as regex_replace


class FilterModule(object):

    def filters(self):
        return {
            "safe_key": self.safe_key,
            "get_dict": self.get_dict,
            "prepare_mariadb": self.prepare_mariadb,
        }

    @staticmethod
    def safe_key(key: str) -> str:
        return regex_replace(r'[^0-9a-zA-Z\.]+', '', key.replace(' ', '_'))

    @staticmethod
    def get_dict(key, value) -> dict:
        return {key: value}

    @staticmethod
    def prepare_mariadb(site: dict, name: str) -> dict:
        return {
            name: {
                'state': site['state'],
                'dbs': {site['database']['db']: 'present'},
                'backup': {'enabled': site['database']['backup']},
                'users': {
                    site['database']['user']: {
                        'priv': f"{site['database']['db']}.*:ALL",
                        'pwd': site['database']['pwd'],
                        'update_pwd:': 'on_create',
                    }
                },
            }
        }
