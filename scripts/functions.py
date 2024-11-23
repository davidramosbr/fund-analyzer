class Functions:
    
    @staticmethod
    def convert_to_float(value):
        if isinstance(value, str):
            value = value.strip().replace("R$", "").replace(",", ".").strip()
            if "B" in value:
                return float(value.replace("B", "")) * 1_000_000_000
            elif "M" in value:
                return float(value.replace("M", "")) * 1_000_000
            elif value.replace(".", "", 1).isdigit():
                return float(value)
        return 0.0

    @staticmethod
    def convert_to_int(value):
        if isinstance(value, str):
            value = value.strip()
            value = value.replace(".", "")
            value = value.replace(",", "")
            if "B" in value:
                return int(float(value.replace("B", "")) * 1_000_000_000)
            elif "M" in value:
                return int(float(value.replace("M", "")) * 1_000_000)
            try:
                return int(value)
            except ValueError:
                return 0
        return 0