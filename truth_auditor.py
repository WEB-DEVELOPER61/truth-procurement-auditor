import re
from datetime import datetime

class TRUTHAuditor:
    """
    Project TRUTH: Automated Public Procurement Compliance Engine
    Statutory Benchmark: Rajasthan Transparency in Public Procurement (RTPP) Rules, 2013 (Rule 43)
    """

    def __init__(self):
        # RTPP Rule 43(7) Minimum Window Thresholds (in Days)
        self.RULE_43_THRESHOLDS = {
            "BELOW_10_LAKH": 7.0,      # Works up to Rs. 10 Lakhs -> Min 7 days
            "BETWEEN_10L_2CR": 10.0,   # Works Rs. 10 Lakhs to Rs. 2 Crores -> Min 10 days
            "ABOVE_2CR": 20.0          # Works above Rs. 2 Crores -> Min 20 days
        }

    def parse_datetime(self, date_str: str) -> datetime:
        """Parses common eProc portal timestamp formats."""
        cleaned = date_str.strip().replace("PM", " PM").replace("AM", " AM")
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        formats = [
            "%d-%b-%Y %I:%M %p",   # e.g., 30-Sep-2026 03:30 PM
            "%d-%m-%Y %I:%M %p",   # e.g., 30-09-2026 03:30 PM
            "%d-%b-%Y",            # e.g., 30-Sep-2026
            "%d/%m/%Y",            # e.g., 30/09/2026
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(cleaned, fmt)
            except ValueError:
                continue
        raise ValueError(f"Unrecognized date format: '{date_str}'")

    def audit_tender(self, tender_id: str, published_str: str, closing_str: str, cost_inr: float, department: str = "Unknown") -> dict:
        """
        Audits a single tender entry against RTPP statutory norms.
        """
        pub_dt = self.parse_datetime(published_str)
        close_dt = self.parse_datetime(closing_str)

        # Calculate Delta T in fractional days
        delta_seconds = (close_dt - pub_dt).total_seconds()
        bidding_window_days = round(delta_seconds / 86400.0, 2)

        # Determine statutory minimum under RTPP Rule 43(7)
        if cost_inr <= 1_000_000:
            mandated_min_days = self.RULE_43_THRESHOLDS["BELOW_10_LAKH"]
        elif cost_inr <= 20_000_000:
            mandated_min_days = self.RULE_43_THRESHOLDS["BETWEEN_10L_2CR"]
        else:
            mandated_min_days = self.RULE_43_THRESHOLDS["ABOVE_2CR"]

        deficit = round(mandated_min_days - bidding_window_days, 2)

        # Evaluate compliance status
        if bidding_window_days >= mandated_min_days:
            status = "COMPLIANT"
            severity = "GREEN"
        elif bidding_window_days < 5.0:
            status = "CRITICAL_VIOLATION"
            severity = "RED"
        else:
            status = "MODERATE_VIOLATION"
            severity = "AMBER"

        return {
            "tender_id": tender_id,
            "department": department,
            "cost_inr": cost_inr,
            "published_at": pub_dt.strftime("%Y-%m-%d %H:%M"),
            "closing_at": close_dt.strftime("%Y-%m-%d %H:%M"),
            "bidding_window_days": bidding_window_days,
            "statutory_min_days": mandated_min_days,
            "deficit_days": max(0.0, deficit),
            "status": status,
            "severity": severity
        }

if __name__ == "__main__":
    auditor = TRUTHAuditor()

    # Benchmark run on empirical Chirawa PWD case
    sample_records = [
        ("2026_CEPWD_602128_1", "30-Sep-2026 03:30 PM", "04-Oct-2026 06:00 PM", 4896000, "PWD Chirawa"),
        ("2026_CEPWD_602128_6", "30-Sep-2026 03:30 PM", "04-Oct-2026 06:00 PM", 495000, "PWD Chirawa"),
        ("2026_PHCJO_602073_1", "30-Sep-2026 02:00 PM", "12-Oct-2026 06:00 PM", 2302000, "PHED Sojat City"),
    ]

    print(f"{'TENDER ID':<22} | {'COST (INR)':<10} | {'WINDOW':<10} | {'MANDATE':<8} | {'STATUS'}")
    print("-" * 75)
    for tid, pub, close, cost, dept in sample_records:
        res = auditor.audit_tender(tid, pub, close, cost, dept)
        print(f"{res['tender_id']:<22} | Rs. {res['cost_inr']:<7} | {res['bidding_window_days']} days | {res['statutory_min_days']} days | {res['status']}")
