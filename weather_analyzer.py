from datetime import datetime


class WeatherAnalyzer:
    def __init__(self):
        self.records = []

    def add_record(self, temperature, humidity, wind_speed, timestamp=None):
        if temperature < -90 or temperature > 60:
            raise ValueError(f"Temperatura non valida: {temperature}")
        if humidity < 0 or humidity > 100:
            raise ValueError(f"Umidità non valida: {humidity}")
        if wind_speed < 0:
            raise ValueError(f"Velocità vento non valida: {wind_speed}")

        self.records.append({
            "temperature": temperature,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "timestamp": timestamp or datetime.now().isoformat()
        })

    def get_statistics(self):
        if not self.records:
            return {}

        temps = [r["temperature"] for r in self.records]
        humidity = [r["humidity"] for r in self.records]
        winds = [r["wind_speed"] for r in self.records]

        return {
            "temperature": {
                "min": min(temps),
                "max": max(temps),
                "avg": round(sum(temps) / len(temps), 2)
            },
            "humidity": {
                "min": min(humidity),
                "max": max(humidity),
                "avg": round(sum(humidity) / len(humidity), 2)
            },
            "wind_speed": {
                "min": min(winds),
                "max": max(winds),
                "avg": round(sum(winds) / len(winds), 2)
            },
            "total_records": len(self.records)
        }

    def detect_anomalies(self):
        if not self.records:
            return []

        anomalies = []
        stats = self.get_statistics()
        avg_temp = stats["temperature"]["avg"]
        avg_wind = stats["wind_speed"]["avg"]

        for i, record in enumerate(self.records):
            if record["temperature"] > avg_temp + 10:
                anomalies.append({
                    "record_index": i,
                    "type": "high_temperature",
                    "value": record["temperature"],
                    "timestamp": record["timestamp"]
                })
            if record["wind_speed"] > avg_wind + 20:
                anomalies.append({
                    "record_index": i,
                    "type": "high_wind",
                    "value": record["wind_speed"],
                    "timestamp": record["timestamp"]
                })
            if record["humidity"] > 90:
                anomalies.append({
                    "record_index": i,
                    "type": "high_humidity",
                    "value": record["humidity"],
                    "timestamp": record["timestamp"]
                })

        return anomalies

    def generate_report(self):
        return {
            "generated_at": datetime.now().isoformat(),
            "statistics": self.get_statistics(),
            "anomalies": self.detect_anomalies(),
            "anomaly_count": len(self.detect_anomalies())
        }
