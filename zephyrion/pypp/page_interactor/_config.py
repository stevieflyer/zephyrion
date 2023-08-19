class PageInteractionConfig:
    def __init__(self):
        self.new_page_wait = 1000
        """extra waittime when loading new page(in milliseconds)"""
        self.click_pre_wait = 1000
        """time to wait before clicking(in milliseconds)"""
        self.input_pre_wait = 1000
        """time to wait before typing input(in milliseconds)"""
        self.quick_wait = 200
        """quick wait time(in milliseconds)"""
        self.slow_wait = 2000
        """slow wait time(in milliseconds)"""
        self.selector_wait_time_out = 5000
        """selector wait time out(in milliseconds)"""

    def parse_config(self, config_path):
        # Parse config logic
        pass

    def dump_config(self, config_path):
        # Dump config logic
        pass
