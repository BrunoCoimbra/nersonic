import configparser


class ConfigManager:
    """
    Singleton class to manage configuration settings.
    """

    def __new__(cls):
        """Singleton pattern to ensure only one instance of ConfigManager exists."""
        if not hasattr(cls, 'instance'):
            cls.instance = super(ConfigManager, cls).__new__(cls)
        return cls.instance

    def __init__(self, config_file='settings.cfg'):
        self.config = configparser.ConfigParser()
        self.config_file = config_file
        self.load_config()

    def load_config(self, config_file=None):
        """Load the configuration file."""

        config_file = config_file or self.config_file
        self.config.read(config_file)

    def get(self, section, option):
        """Get a configuration value."""

        return self.config.get(section, option)

    def set(self, section, option, value):
        """Set a configuration value."""

        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, option, value)
        self.save_config()

    def save_config(self):
        """Save the configuration to the file."""

        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)
